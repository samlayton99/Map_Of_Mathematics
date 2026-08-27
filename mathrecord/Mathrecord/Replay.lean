import Mathrecord.HeadDump

/-! Mechanical replay of reference proofs + occurrence-level trace extraction
+ the inference-shadow test.

For every proof-valued node of a reference proof term, test whether the
engine's own unification pipeline can reconstruct that step: iteratively
metavariable-telescope the head's type against the node's argument count
(over-applied heads - eliminators, `id`, `Iff.mp` - expose further binders
only after the motive/function argument is assigned, so the telescope is
re-run after each assignment round), assign each reference argument
positionally through `isDefEq`, then unify the final conclusion.

Any failure is an implementation defect of the assembly pipeline, not a
search or learning problem - the reference proof certifies the step.

INFERENCE-SHADOW: for every data (non-proof) argument, measure whether the
engine would have had to fabricate it at all, in three tiers:
  T1 "immediately inferable"  - withholding it, unifying only the
      conclusion with the goal already determines it;
  T2 "inferable once constraints accumulate" - withholding it, assigning
      every sibling argument plus the conclusion determines it;
  T3 "genuine fabrication"    - neither determines it.

Each node simultaneously emits an occurrence-level trace record: the goal
type, the chosen head, and per-argument records (proof/data split, the
reference data term, its shape/class, and its shadow tiers).  This is the
reference-derived training dataset for the assembler (head selection) and
the fabricator (typed custom terms).

CLI: mathrecord replay <ImportMathlib.lean> <tasks.json> <out.jsonl>
-/

namespace Mathrecord.Replay

open Lean Meta Mathrecord Mathrecord.HeadDump

structure Ctx where
  fuel : IO.Ref Nat
  rows : IO.Ref (Array Json)
  bad  : IO.Ref Nat
  withShadow : Bool := true
  -- support candidates (name, statement type) for hard-negative emission:
  -- at every proof node, which of these heads is Lean-legal at the goal
  cands : Array (Name × Expr) := #[]

/-- Iteratively metavariable-telescope `hType` against `args`, assigning
reference arguments positionally, then unify the final conclusion with `t`.

`skip`: withhold this argument index (inference-shadow) - its metavariable
is returned for determination analysis.  `conclOnly`: assign no arguments;
only unify the conclusion.  Returns (ok, withheldMVar?, stalled) where
`stalled` means the telescope could not expose enough binders (the withheld
or unassigned argument was structurally necessary to proceed). -/
def reconstruct (hType : Expr) (args : Array Expr) (t : Expr)
    (skip : Option Nat := none) (conclOnly : Bool := false) :
    MetaM (Bool × Option Expr × Bool) := do
  let mut curType := hType
  let mut idx := 0
  let mut ok := true
  let mut stalled := false
  let mut withheld : Option Expr := none
  for _ in [0:args.size] do
    if idx ≥ args.size || !ok then break
    let (mvs, _, concl) ← forallMetaBoundedTelescope curType (args.size - idx)
    if mvs.size == 0 then
      ok := false
      stalled := true
    else
      for i in [0:mvs.size] do
        let j := idx + i
        if skip == some j then
          withheld := some mvs[i]!
        else if !conclOnly then
          unless ← isDefEq mvs[i]! args[j]! do ok := false
      curType ← instantiateMVars concl
      idx := idx + mvs.size
  if ok && idx < args.size then
    ok := false
    stalled := true
  if ok then
    unless ← isDefEq curType t do ok := false
  pure (ok, withheld, stalled)

/-- Determination status of a withheld argument's metavariable after the
surrounding constraints were applied. -/
def detStatus (mv? : Option Expr) (ref : Expr) : MetaM String := do
  let some mv := mv? | return "undet"
  let v ← instantiateMVars mv
  if v.hasExprMVar then return "undet"
  if ← (try isDefEq v ref catch _ => pure false) then return "det"
  return "diff"

/-- Three-tier inference-shadow for data argument `j`.  "det" at T1 =
immediately inferable; "det" at T2 = inferable once sibling constraints
accumulate; anything else at both = genuine fabrication. -/
def shadowTiers (hType : Expr) (args : Array Expr) (t : Expr) (j : Nat) :
    MetaM (String × String) := do
  let t1 ← withoutModifyingState do
    let (ok, wh, stalled) ← reconstruct hType args t (skip := some j) (conclOnly := true)
    if stalled then pure "stall"
    else if !ok then pure "noconcl"
    else detStatus wh args[j]!
  if t1 == "det" then return (t1, "det")
  let t2 ← withoutModifyingState do
    let (ok, wh, stalled) ← reconstruct hType args t (skip := some j)
    if stalled then pure "stall"
    else if !ok then pure "fail"
    else detStatus wh args[j]!
  return (t1, t2)

/-- Which support heads are Lean-legal at goal type `t` (conclusion
unifies through a fresh metavariable telescope) - the hard negatives for
the head-selection dataset. -/
def legalHeads (cands : Array (Name × Expr)) (t : Expr) :
    MetaM (Array String) := do
  let mut legal : Array String := #[]
  for (cn, cty) in cands do
    let ok ← withoutModifyingState do
      try
        let (_, _, ccl) ← forallMetaTelescope cty
        isDefEq ccl t
      catch _ => pure false
    if ok then legal := legal.push (toString cn)
  pure legal

partial def walk (ctx : Ctx) (e : Expr) (depth : Nat := 0) : MetaM Unit := do
  if (← ctx.fuel.get) == 0 then return ()
  ctx.fuel.set ((← ctx.fuel.get) - 1)
  let e := e.consumeMData
  let t ← try instantiateMVars (← inferType e) catch _ => return ()
  let isP ← try Meta.isProp t catch _ => pure false
  if !isP then return ()               -- only proof nodes drive assembly
  match e with
  | .lam .. =>
    lambdaTelescope e fun _ body => walk ctx body (depth + 1)
  | .letE nm ty val body _ =>
    walk ctx val (depth + 1)
    withLetDecl nm ty val fun x => walk ctx (body.instantiate1 x) (depth + 1)
  | .app .. =>
    let fn := e.getAppFn.consumeMData
    let args := e.getAppArgs
    -- beta-redex / letFun: recurse through both sides
    if fn.isLambda then
      walk ctx fn (depth + 1)
      for a in args do walk ctx a (depth + 1)
      return ()
    -- stepwise reconstruction: does OUR pipeline accept this exact step?
    let res ← try
      withoutModifyingState do
        let hType ← inferType fn
        let mut np := 0
        let mut dataIdx : Array Nat := #[]
        for i in [0:args.size] do
          let aP ← try Meta.isProp (← inferType args[i]!) catch _ => pure false
          if aP then np := np + 1 else dataIdx := dataIdx.push i
        let (ok, _, _) ← withoutModifyingState (reconstruct hType args t)
        let mut recs : Array Json := #[]
        for j in dataIdx do
          let a := args[j]!
          let shape := match a.consumeMData with
            | .fvar _ => "fvar" | .const .. => "const" | .lit .. => "lit"
            | .lam .. => "lam" | .app .. => "app" | .sort .. => "sort"
            | .mvar _ => "mvar" | .proj .. => "proj"
            | .forallE .. => "pi" | .letE .. => "let" | _ => "other"
          let τ ← try instantiateMVars (← inferType a) catch _ => pure (mkSort levelZero)
          let cls ← try
            if τ.getForallBody.isSort then pure "type"
            else if (← Meta.isClass? τ).isSome then pure "instance"
            else pure "value"
          catch _ => pure "value"
          let (s1, s2) ← if ok && ctx.withShadow then
              try shadowTiers hType args t j catch _ => pure ("err", "err")
            else pure ("untested", "untested")
          recs := recs.push (Json.mkObj [
            ("i", toJson j),
            ("term", Json.str (((toString a).take 240).toString)),
            ("ty", Json.str (((toString τ).take 160).toString)),
            ("shape", Json.str shape),
            ("has_fvar", toJson a.hasFVar),
            ("cls", Json.str cls),
            ("t1", Json.str s1), ("t2", Json.str s2)])
        pure (some (ok, recs, np, dataIdx.size))
    catch _ => pure none
    let (stepOk, argRecs, nProof, nData) := match res with
      | some (a, b, c, d) => (a, b, c, d)
      | none => (false, #[], 0, 0)
    let headStr := match fn with
      | .const c _ => toString c
      | .fvar _ => "FVAR"
      | _ => "OTHER"
    let legal ← try legalHeads ctx.cands t catch _ => pure #[]
    ctx.rows.modify (·.push (Json.mkObj [
      ("head", Json.str headStr),
      ("ok", toJson stepOk),
      ("goal", Json.str (((toString t).take 240).toString)),
      ("depth", toJson depth),
      ("legal_heads", Json.arr (legal.map Json.str)),
      ("n_proof_args", toJson nProof),
      ("n_data_args", toJson nData),
      ("data_args", Json.arr argRecs)]))
    if !stepOk then ctx.bad.modify (· + 1)
    for a in args do walk ctx a (depth + 1)  -- recurse (walk filters non-proof)
  | .proj _ _ s =>
    walk ctx s (depth + 1)
  | _ =>
    -- leaf proof: a hypothesis or a bare constant - trivially replayable
    let headStr := match e with
      | .const c _ => toString c
      | .fvar _ => "FVAR"
      | _ => "LEAF"
    let legal ← try legalHeads ctx.cands t catch _ => pure #[]
    ctx.rows.modify (·.push (Json.mkObj [
      ("head", Json.str headStr), ("ok", toJson true),
      ("goal", Json.str (((toString t).take 240).toString)),
      ("depth", toJson depth),
      ("legal_heads", Json.arr (legal.map Json.str)),
      ("n_proof_args", toJson 0), ("n_data_args", toJson 0),
      ("data_args", Json.arr #[])]))

def replay (path : System.FilePath) (inp : System.FilePath)
    (out : System.FilePath) (mode : String := "") : IO Unit := do
  let pf ← Mathrecord.processFile path Mathrecord.Study.mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules; mode={mode}"
  let raw ← IO.FS.readFile inp
  let j ← IO.ofExcept (Json.parse raw)
  let ts ← IO.ofExcept ((← IO.ofExcept (j.getObjVal? "goals" <|> j.getObjVal? "tasks")).getArr?)
  -- "neg": emit Lean-legal support heads per node (hard negatives for the
  -- assembler dataset), shadow tiers off for speed
  let withNeg := mode == "neg"
  let withShadow := mode != "neg"
  IO.println s!"{ts.size} theorems to replay"
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let mut count := 0
  let mut allOkCount := 0
  for tj in ts do
    let nm := ((do (← tj.getObjVal? "n").getStr? :
      Except String String)).toOption.getD ""
    if nm == "" then continue
    let bwNames : Array Name :=
      if withNeg then
        match (do (← tj.getObjVal? "bw").getArr? : Except String (Array Json)) with
        | .ok arr =>
          (arr.filterMap (fun c => (c.getStr?).toOption.map String.toName)).extract 0 120
        | .error _ => #[]
      else #[]
    let n := String.toName nm
    let act : MetaM Json := do
      let some ci := env.find? n
        | return Json.mkObj [("n", Json.str nm), ("error", Json.str "not found")]
      let some val := ci.value? (allowOpaque := true)
        | return Json.mkObj [("n", Json.str nm), ("error", Json.str "no value")]
      let cands : Array (Name × Expr) := bwNames.filterMap fun c =>
        match env.find? c with
        | some cci => some (c, cci.type)
        | none => none
      Meta.forallTelescope ci.type fun xs _ => do
        let fuel ← IO.mkRef 400
        let rows ← IO.mkRef (#[] : Array Json)
        let bad ← IO.mkRef 0
        walk { fuel, rows, bad, withShadow, cands } (val.beta xs)
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
      IO.println s!"  {count}/{ts.size} replayed, {allOkCount} fully ok"
      h.flush
  IO.println s!"done: {allOkCount}/{count} fully replayable"
  h.flush

end Mathrecord.Replay
