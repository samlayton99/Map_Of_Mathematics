import Mathrecord.HeadDump

/-! Mechanical replay of reference proofs + occurrence-level trace extraction.

For every proof-valued node of a reference proof term, test whether the
engine's own unification pipeline can reconstruct that step: take the
node's head, metavariable-telescope its type to the node's argument count,
unify the conclusion with the node's goal type, then assign each reference
argument positionally through `isDefEq`.

Any failure is an implementation defect of the assembly pipeline, not a
search or learning problem - the reference proof certifies the step.

Each node simultaneously emits an occurrence-level trace record: the goal
type, the chosen head, and for every argument whether it is a proof hole
(assembly) or a data hole (fabrication), with the reference data argument
serialized.  This is the reference-derived training dataset for the
assembler (head selection) and the fabricator (typed custom terms).

CLI: mathrecord replay <ImportMathlib.lean> <tasks.json> <out.jsonl>
-/

namespace Mathrecord.Replay

open Lean Meta Mathrecord Mathrecord.HeadDump

structure Ctx where
  fuel : IO.Ref Nat
  rows : IO.Ref (Array Json)
  bad  : IO.Ref Nat

partial def walk (ctx : Ctx) (e : Expr) : MetaM Unit := do
  if (← ctx.fuel.get) == 0 then return ()
  ctx.fuel.set ((← ctx.fuel.get) - 1)
  let e := e.consumeMData
  let t ← try instantiateMVars (← inferType e) catch _ => return ()
  let isP ← try Meta.isProp t catch _ => pure false
  if !isP then return ()               -- only proof nodes drive assembly
  match e with
  | .lam .. =>
    lambdaTelescope e fun _ body => walk ctx body
  | .letE nm ty val body _ =>
    walk ctx val
    withLetDecl nm ty val fun x => walk ctx (body.instantiate1 x)
  | .app .. =>
    let fn := e.getAppFn.consumeMData
    let args := e.getAppArgs
    -- beta-redex / letFun: recurse through both sides
    if fn.isLambda then
      walk ctx fn
      for a in args do walk ctx a
      return ()
    -- stepwise reconstruction: does OUR pipeline accept this exact step?
    let (stepOk, dataArgs, nProof, nData) ← try
      withoutModifyingState do
        let hType ← inferType fn
        let (mvs, _, concl) ← forallMetaBoundedTelescope hType args.size
        if mvs.size != args.size then
          pure (false, #[], 0, 0)
        else do
          let ok1 ← isDefEq concl t
          let mut ok := ok1
          let mut dArgs : Array String := #[]
          let mut np := 0
          let mut nd := 0
          for i in [0:args.size] do
            let aP ← try Meta.isProp (← inferType args[i]!) catch _ => pure false
            if aP then np := np + 1
            else
              nd := nd + 1
              dArgs := dArgs.push (((toString args[i]!).take 240).toString)
            unless ← isDefEq mvs[i]! args[i]! do ok := false
          pure (ok, dArgs, np, nd)
    catch _ => pure (false, #[], 0, 0)
    let headStr := match fn with
      | .const c _ => toString c
      | .fvar _ => "FVAR"
      | _ => "OTHER"
    ctx.rows.modify (·.push (Json.mkObj [
      ("head", Json.str headStr),
      ("ok", toJson stepOk),
      ("goal", Json.str (((toString t).take 240).toString)),
      ("n_proof_args", toJson nProof),
      ("n_data_args", toJson nData),
      ("data_args", Json.arr (dataArgs.map Json.str))]))
    if !stepOk then ctx.bad.modify (· + 1)
    for a in args do walk ctx a          -- recurse (walk filters non-proof)
  | .proj _ _ s =>
    walk ctx s
  | _ =>
    -- leaf proof: a hypothesis or a bare constant - trivially replayable
    let headStr := match e with
      | .const c _ => toString c
      | .fvar _ => "FVAR"
      | _ => "LEAF"
    ctx.rows.modify (·.push (Json.mkObj [
      ("head", Json.str headStr), ("ok", toJson true),
      ("goal", Json.str (((toString t).take 240).toString)),
      ("n_proof_args", toJson 0), ("n_data_args", toJson 0),
      ("data_args", Json.arr #[])]))

def replay (path : System.FilePath) (inp : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path Mathrecord.Study.mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let raw ← IO.FS.readFile inp
  let j ← IO.ofExcept (Json.parse raw)
  let ts ← IO.ofExcept ((← IO.ofExcept (j.getObjVal? "goals" <|> j.getObjVal? "tasks")).getArr?)
  let names := ts.filterMap (fun t => (do
    (← t.getObjVal? "n").getStr? : Except String String).toOption)
  IO.println s!"{names.size} theorems to replay"
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let mut count := 0
  let mut allOkCount := 0
  for nm in names do
    let n := String.toName nm
    let act : MetaM Json := do
      let some ci := env.find? n
        | return Json.mkObj [("n", Json.str nm), ("error", Json.str "not found")]
      let some val := ci.value? (allowOpaque := true)
        | return Json.mkObj [("n", Json.str nm), ("error", Json.str "no value")]
      Meta.forallTelescope ci.type fun xs _ => do
        let fuel ← IO.mkRef 400
        let rows ← IO.mkRef (#[] : Array Json)
        let bad ← IO.mkRef 0
        walk { fuel, rows, bad } (val.beta xs)
        let rs ← rows.get
        let nb ← bad.get
        return Json.mkObj [
          ("n", Json.str nm),
          ("n_nodes", toJson rs.size),
          ("n_failed", toJson nb),
          ("all_ok", toJson (nb == 0 && rs.size > 0)),
          ("nodes", Json.arr rs)]
    let row ← try
      let (r, _) ← (act.run' {} {}).toIO coreCtx { env }
      pure r
    catch _ => pure (Json.mkObj [("n", Json.str nm), ("error", Json.str "exception")])
    if (row.getObjValAs? Bool "all_ok").toOption == some true then
      allOkCount := allOkCount + 1
    h.putStrLn row.compress
    count := count + 1
    if count % 25 == 0 then
      IO.println s!"  {count}/{names.size} replayed, {allOkCount} fully ok"
      h.flush
  IO.println s!"done: {allOkCount}/{count} fully replayable"
  h.flush

end Mathrecord.Replay
