import Mathrecord.Frontend
import Mathrecord.Record

/-! MathRecord validator.

Reads a stored record plus the corpus source file, re-elaborates the source in
a fresh process, and checks — from the STORED data, not the live objects:

1. coverage: no declaration silently missing (stored + unsupported = env);
2. round-trip: decode(stored expr) is structurally identical (`Expr.equal`,
   binder names and universes included) to the mdata-stripped original;
3. kernel: stored (levelParams, type, value) of every def/theorem re-checks
   via `Environment.addDeclCore`; other kinds via `Meta.check` + `isDefEq`;
4. dependencies recomputed from decoded exprs match the originals;
5. every mvar-free stored state: rebuilt local context is well-formed and the
   decoded target type-checks in it; state sid is reproduced exactly (encode
   after decode is a fixpoint);
6. corpus-specific structural assertions (branching, two-proofs, loud sorry,
   ldecl presence, universe polymorphism, kind coverage).
-/

namespace Mathrecord.Validate

open Lean Meta Mathrecord

abbrev DecM := StateT (Std.HashMap String Expr) (Except String)

structure RecordFile where
  json : Json
  nodes : Std.HashMap String Json
  decls : Array Json
  states : Array Json
  transitions : Array Json
  failures : Array Json
  unsupported : Array Json

def getStr (j : Json) (k : String) : Except String String :=
  match j.getObjValAs? String k with
  | .ok s => .ok s | .error e => .error s!"field {k}: {e}"

def getArr (j : Json) (k : String) : Except String (Array Json) :=
  match j.getObjVal? k with
  | .ok (Json.arr a) => .ok a
  | .ok _ => .error s!"field {k}: not an array"
  | .error e => .error s!"field {k}: {e}"

def loadRecord (path : System.FilePath) : IO RecordFile := do
  let txt ← IO.FS.readFile path
  let json ← IO.ofExcept (Json.parse txt)
  let exprs ← IO.ofExcept (getArr json "expressions")
  let mut nodes : Std.HashMap String Json := {}
  let mut i := 0
  for n in exprs do
    nodes := nodes.insert (exprIdStr i) n
    i := i + 1
  return { json, nodes,
           decls := ← IO.ofExcept (getArr json "declarations"),
           states := ← IO.ofExcept (getArr json "states"),
           transitions := ← IO.ofExcept (getArr json "transitions"),
           failures := ← IO.ofExcept (getArr json "failures"),
           unsupported := ← IO.ofExcept (getArr json "unsupported") }

def biOfString : String → Except String BinderInfo
  | "default" => .ok .default | "implicit" => .ok .implicit
  | "strictImplicit" => .ok .strictImplicit | "instImplicit" => .ok .instImplicit
  | s => .error s!"bad binderInfo {s}"

partial def decodeLevel (j : Json) : Except String Level := do
  match ← getStr j "k" with
  | "zero" => return .zero
  | "succ" => return .succ (← decodeLevel (← j.getObjVal? "u"))
  | "max" => return .max (← decodeLevel (← j.getObjVal? "u")) (← decodeLevel (← j.getObjVal? "v"))
  | "imax" => return .imax (← decodeLevel (← j.getObjVal? "u")) (← decodeLevel (← j.getObjVal? "v"))
  | "param" => return .param (Name.mkSimple (← getStr j "n"))
  | "lmvar" => throw "level metavariable: not decodable outside its trace"
  | k => throw s!"bad level kind {k}"

/-- Decode a stored expression. `fvars` maps lvar ordinals to fvar exprs. -/
partial def decodeExpr (nodes : Std.HashMap String Json) (fvars : Array Expr)
    (id : String) : DecM Expr := do
  if let some e := (← get).get? id then
    return e
  let some j := nodes.get? id | throw s!"dangling expr id {id}"
  let k ← getStr j "k"
  let e ← match k with
    | "bvar" => do
      let i ← liftExcept (j.getObjValAs? Nat "i"); pure (Expr.bvar i)
    | "lvar" => do
      let i ← liftExcept (j.getObjValAs? Nat "i")
      match fvars[i]? with
      | some f => pure f
      | none => throw s!"lvar {i} out of context (size {fvars.size})"
    | "mvar" => throw "metavariable: not decodable outside its trace"
    | "sort" => do pure (Expr.sort (← liftExcept (decodeLevel (← liftExcept (j.getObjVal? "u")))))
    | "const" => do
      let n ← liftExcept (getStr j "n")
      let us ← liftExcept (getArr j "us")
      let ls ← us.toList.mapM (fun u => liftExcept (decodeLevel u))
      pure (Expr.const n.toName ls)
    | "app" => do
      pure (Expr.app (← decodeExpr nodes fvars (← liftExcept (getStr j "f")))
                     (← decodeExpr nodes fvars (← liftExcept (getStr j "a"))))
    | "lam" => do
      let bi ← liftExcept (biOfString (← liftExcept (getStr j "bi")))
      pure (Expr.lam (← liftExcept (getStr j "d")).toName
        (← decodeExpr nodes fvars (← liftExcept (getStr j "t")))
        (← decodeExpr nodes fvars (← liftExcept (getStr j "b"))) bi)
    | "pi" => do
      let bi ← liftExcept (biOfString (← liftExcept (getStr j "bi")))
      pure (Expr.forallE (← liftExcept (getStr j "d")).toName
        (← decodeExpr nodes fvars (← liftExcept (getStr j "t")))
        (← decodeExpr nodes fvars (← liftExcept (getStr j "b"))) bi)
    | "let" => do
      let nd ← liftExcept (j.getObjValAs? Bool "nd")
      pure (Expr.letE (← liftExcept (getStr j "d")).toName
        (← decodeExpr nodes fvars (← liftExcept (getStr j "t")))
        (← decodeExpr nodes fvars (← liftExcept (getStr j "v")))
        (← decodeExpr nodes fvars (← liftExcept (getStr j "b"))) nd)
    | "lit" => do
      match ← liftExcept (getStr j "lt") with
      | "nat" => do
        let v ← liftExcept (getStr j "v")
        match v.toNat? with
        | some n => pure (Expr.lit (.natVal n))
        | none => throw s!"bad nat literal {v}"
      | "str" => do pure (Expr.lit (.strVal (← liftExcept (getStr j "v"))))
      | lt => throw s!"bad literal kind {lt}"
    | "proj" => do
      pure (Expr.proj (← liftExcept (getStr j "s")).toName
        (← liftExcept (j.getObjValAs? Nat "i"))
        (← decodeExpr nodes fvars (← liftExcept (getStr j "b"))))
    | k => throw s!"unknown node kind {k}"
  -- memoize only closed-scope decodes keyed by id; safe because fvars mapping is
  -- fixed per decode session (a fresh memo map is used per state / per decl).
  modify (·.insert id e)
  return e

def runDec {α} (x : DecM α) : Except String α := (x.run {}).map (·.1)

structure CheckResult where
  name : String
  passed : Bool
  detail : String

def check (name : String) (cond : Bool) (detail : String := "") : CheckResult :=
  { name, passed := cond, detail }

/-- Name decoding: stored names are full dotted names. `String.toName` handles
components; sufficient for the corpus (documented limitation for exotic atoms). -/

def validateDecls (env : Environment) (rec : RecordFile) : IO (Array CheckResult) := do
  let mut results : Array CheckResult := #[]
  -- coverage
  let envNames := (env.constants.map₂.toList.map (toString ·.1)).toArray.qsort (· < ·)
  let storedNames ← IO.ofExcept <| rec.decls.mapM (fun d => getStr d "name")
  let unsupNames ← IO.ofExcept <| rec.unsupported.mapM (fun d => getStr d "name")
  let coveredNames := (storedNames ++ unsupNames).qsort (· < ·)
  results := results.push <| check "coverage:no-silent-loss"
    (envNames == coveredNames)
    s!"env={envNames.size} stored={storedNames.size} unsupported={unsupNames.size}"
  -- per-declaration checks
  let mut rtOk := 0
  let mut rtFail : List String := []
  let mut kernelOk := 0
  let mut kernelFail : List String := []
  let mut metaOk := 0
  let mut metaFail : List String := []
  let mut depsOk := 0
  let mut depsFail : List String := []
  for d in rec.decls do
    let name ← IO.ofExcept (getStr d "name")
    let kind ← IO.ofExcept (getStr d "kind")
    let some ci := env.find? name.toName | rtFail := name :: rtFail; continue
    let levelParams := (d.getObjValAs? (List String) "levelParams").toOption.getD [] |>.map Name.mkSimple
    let decType := runDec (decodeExpr rec.nodes #[] (← IO.ofExcept (getStr d "type")))
    let decValue : Option (Except String Expr) := match getStr d "value" with
      | .ok vid => some (runDec (decodeExpr rec.nodes #[] vid))
      | .error _ => none
    -- round-trip structural equality against mdata-stripped originals
    match decType with
    | .error e => rtFail := s!"{name}(type:{e})" :: rtFail
    | .ok t =>
      let origT := stripMData ci.type
      let valOk ← match decValue, ci.value? (allowOpaque := true) with
        | none, none => pure true
        | some (.ok v), some ov => pure (v == stripMData ov)
        | some (.error e), _ => rtFail := s!"{name}(value:{e})" :: rtFail; pure false
        | _, _ => pure false
      if t == origT && valOk then
        rtOk := rtOk + 1
      else if valOk then
        rtFail := s!"{name}(type-mismatch)" :: rtFail
      else
        rtFail := s!"{name}(value-mismatch)" :: rtFail
      -- dependency recomputation from decoded exprs
      let depT := t.getUsedConstants == origT.getUsedConstants
      let depV := match decValue, ci.value? (allowOpaque := true) with
        | some (.ok v), some ov => v.getUsedConstants == (stripMData ov).getUsedConstants
        | _, _ => true
      if depT && depV then depsOk := depsOk + 1 else depsFail := name :: depsFail
      -- kernel / meta checking from stored data
      match kind, decValue with
      | "theorem", some (.ok v) =>
        let decl := Declaration.thmDecl
          { name := (name ++ "_rt").toName, levelParams, type := t, value := v }
        match env.addDeclCore 0 8192 decl none with
        | .ok _ => kernelOk := kernelOk + 1
        | .error _ => kernelFail := name :: kernelFail
      | "def", some (.ok v) =>
        let safety := (d.getObjVal? "extras").toOption.bind (fun ex => (getStr ex "safety").toOption)
          |>.getD "safe"
        if safety == "safe" then
          let decl := Declaration.defnDecl
            { name := (name ++ "_rt").toName, levelParams, type := t, value := v,
              hints := .opaque, safety := .safe }
          match env.addDeclCore 0 8192 decl none with
          | .ok _ => kernelOk := kernelOk + 1
          | .error _ => kernelFail := name :: kernelFail
        else
          -- unsafe/partial defs are outside kernel re-checking; Meta-check instead
          let coreCtx : Core.Context := { fileName := "<validate>", fileMap := default }
          let act : MetaM Bool := do
            try
              Meta.check t
              Meta.check v
              let vt ← Meta.inferType v
              return (← Meta.isDefEq vt t)
            catch _ => return false
          let (ok, _) ← (act.run' {} {}).toIO coreCtx { env }
          if ok then metaOk := metaOk + 1 else metaFail := name :: metaFail
      | _, _ =>
        -- other kinds: Meta-level checking of the stored type (and value if any)
        let coreCtx : Core.Context := { fileName := "<validate>", fileMap := default }
        let act : MetaM Bool := do
          try
            Meta.check t
            if let some (.ok v) := decValue then
              Meta.check v
              let vt ← Meta.inferType v
              return (← Meta.isDefEq vt t)
            return true
          catch _ => return false
        let (ok, _) ← (act.run' {} {}).toIO coreCtx { env }
        if ok then metaOk := metaOk + 1 else metaFail := name :: metaFail
  results := results.push <| check "roundtrip:decode-equals-original"
    rtFail.isEmpty s!"ok={rtOk} fail={rtFail}"
  results := results.push <| check "kernel:stored-defs-theorems-recheck"
    kernelFail.isEmpty s!"ok={kernelOk} fail={kernelFail}"
  results := results.push <| check "meta:other-kinds-typecheck"
    metaFail.isEmpty s!"ok={metaOk} fail={metaFail}"
  results := results.push <| check "deps:recomputable-from-stored"
    depsFail.isEmpty s!"ok={depsOk} fail={depsFail}"
  return results

def validateStates (env : Environment) (rec : RecordFile) : IO (Array CheckResult) := do
  let mut okCount := 0
  let mut skipped := 0
  let mut failures : List String := []
  let mut sidOkCount := 0
  let mut sidFail : List String := []
  for st in rec.states do
    let sidStored ← IO.ofExcept (getStr st "id")
    let hasMVars := (st.getObjValAs? Bool "hasMVars").toOption.getD true
    if hasMVars then
      skipped := skipped + 1
      continue
    let ctxArr ← IO.ofExcept (getArr st "ctx")
    let targetId ← IO.ofExcept (getStr st "target")
    let storedSid ← IO.ofExcept (getStr st "sid")
    -- rebuild the local context from the stored record only
    let coreCtx : Core.Context := { fileName := "<validate>", fileMap := default }
    let act : MetaM (Bool × String) := do
      let mut lctx : LocalContext := {}
      let mut fvars : Array Expr := #[]
      let mut fvarOrd : Std.HashMap FVarId Nat := {}
      let mut memo : Std.HashMap String Expr := {}
      let mut idx := 0
      for entry in ctxArr do
        let fvarId ← mkFreshFVarId
        let userName := Name.mkSimple ((getStr entry "d").toOption.getD s!"h{idx}")
        let tId ← match getStr entry "t" with
          | .ok s => pure s | .error e => throwError e
        let tE ← match (decodeExpr rec.nodes fvars tId).run memo with
          | .ok (e, m) => memo := m; pure e
          | .error e => throwError e
        let bi ← match biOfString ((getStr entry "bi").toOption.getD "default") with
          | .ok b => pure b | .error e => throwError e
        let ldKind : LocalDeclKind := match (getStr entry "ldKind").toOption.getD "default" with
          | "implDetail" => .implDetail | "auxDecl" => .auxDecl | _ => .default
        match getStr entry "v" with
        | .ok vId =>
          let vE ← match (decodeExpr rec.nodes fvars vId).run memo with
            | .ok (e, m) => memo := m; pure e
            | .error e => throwError e
          let nonDep := (entry.getObjValAs? Bool "nonDep").toOption.getD false
          lctx := lctx.mkLetDecl fvarId userName tE vE nonDep ldKind
        | .error _ =>
          lctx := lctx.mkLocalDecl fvarId userName tE bi ldKind
        fvarOrd := fvarOrd.insert fvarId idx
        fvars := fvars.push (mkFVar fvarId)
        idx := idx + 1
      let targetE ← match (decodeExpr rec.nodes fvars targetId).run memo with
        | .ok (e, _) => pure e
        | .error e => throwError e
      withLCtx lctx {} do
        -- context well-formedness + target well-formedness, via Lean's checker
        for f in fvars do
          let d ← f.fvarId!.getDecl
          Meta.check d.type
          if let some v := d.value? then Meta.check v
        Meta.check targetE
        -- sid fixpoint: re-encode the decoded state, name-free
        let sc : Scope := { fvarOrd := some fvarOrd, allowMVars := true }
        let mut ctxSid : Array String := #[]
        for f in fvars do
          let d ← f.fvarId!.getDecl
          let tsid ← match sidOf sc {} {} (stripMData d.type) with
            | .ok s => pure s | .error e => throwError (toString e)
          match d with
          | .cdecl _ _ _ _ bi _ =>
            ctxSid := ctxSid.push s!"({biToString bi},{d.isImplementationDetail},{tsid})"
          | .ldecl _ _ _ _ v _ _ =>
            let vsid ← match sidOf sc {} {} (stripMData v) with
              | .ok s => pure s | .error e => throwError (toString e)
            ctxSid := ctxSid.push s!"(let,{d.isImplementationDetail},{tsid},{vsid})"
        let targetSid ← match sidOf sc {} {} (stripMData targetE) with
          | .ok s => pure s | .error e => throwError (toString e)
        let rebuiltSid := s!"St([{";".intercalate ctxSid.toList}];{targetSid})"
        return (rebuiltSid == storedSid, rebuiltSid)
    let outcome ← try
      let ((ok, _), _) ← ((act.run' {} {}).toIO coreCtx { env })
      pure (some ok)
    catch e =>
      failures := s!"{sidStored}: {e.toString.take 100}" :: failures
      pure none
    match outcome with
    | some true => okCount := okCount + 1; sidOkCount := sidOkCount + 1
    | some false => okCount := okCount + 1; sidFail := sidStored :: sidFail
    | none => pure ()
  let mut results : Array CheckResult := #[]
  results := results.push <| check "states:context-and-target-wellformed"
    failures.isEmpty s!"checked={okCount} skipped(mvars)={skipped} fail={failures}"
  results := results.push <| check "states:sid-fixpoint-after-decode"
    sidFail.isEmpty s!"ok={sidOkCount} fail={sidFail}"
  return results

def validateCorpusAssertions (rec : RecordFile) : IO (Array CheckResult) := do
  let mut results : Array CheckResult := #[]
  -- branching and closing transitions
  let mut branching := false
  let mut closing := false
  for t in rec.transitions do
    let after := (getArr t "after").toOption.getD #[]
    if after.size ≥ 2 then branching := true
    if after.size == 0 then closing := true
  results := results.push <| check "transitions:branching-state-observed" branching
  results := results.push <| check "transitions:closing-step-observed" closing
  -- two distinct proofs of the same proposition
  let mut proofA : Option (String × String) := none
  let mut proofB : Option (String × String) := none
  for d in rec.decls do
    let name := (getStr d "name").toOption.getD ""
    if name == "Corpus.twoProofsA" then
      proofA := some ((getStr d "typeSid").toOption.getD "?", (getStr d "valueSid").toOption.getD "?")
    if name == "Corpus.twoProofsB" then
      proofB := some ((getStr d "typeSid").toOption.getD "?", (getStr d "valueSid").toOption.getD "?")
  match proofA, proofB with
  | some (ta, va), some (tb, vb) =>
    results := results.push <| check "alt-proofs:same-statement-distinct-proofs"
      (ta == tb && va != vb) s!"typeEq={ta == tb} valueEq={va == vb}"
  | _, _ =>
    results := results.push <| check "alt-proofs:same-statement-distinct-proofs" false "decls missing"
  -- loud sorry classification
  let unsupNames := rec.unsupported.filterMap (fun d => (getStr d "name").toOption)
  results := results.push <| check "unsupported:sorry-classified-loudly"
    (unsupNames.contains "Corpus.hasSorry") s!"unsupported={unsupNames}"
  -- some state has a local let (ldecl with value)
  let mut hasLdecl := false
  for st in rec.states do
    for entry in (getArr st "ctx").toOption.getD #[] do
      if (getStr entry "v").isOk then hasLdecl := true
  results := results.push <| check "states:local-let-preserved" hasLdecl
  -- universe polymorphism preserved
  let mut hasPoly := false
  for d in rec.decls do
    if (getStr d "name").toOption == some "Corpus.constFun" then
      let lp := (d.getObjValAs? (List String) "levelParams").toOption.getD []
      hasPoly := lp.length == 2
  results := results.push <| check "decls:universe-polymorphism-preserved" hasPoly
  -- declaration kind coverage
  let kinds := rec.decls.filterMap (fun d => (getStr d "kind").toOption)
  let need := ["def", "theorem", "inductive", "constructor", "recursor", "opaque"]
  let missing := need.filter (fun k => !kinds.contains k)
  results := results.push <| check "decls:kind-coverage" missing.isEmpty s!"missing={missing}"
  return results

def validateFailingAssertions (rec : RecordFile) : IO (Array CheckResult) := do
  let mut results : Array CheckResult := #[]
  results := results.push <| check "failing:error-event-recorded" (rec.failures.size ≥ 1)
    s!"failures={rec.failures.size}"
  results := results.push <| check "failing:prior-transitions-still-observed"
    (rec.transitions.size ≥ 1) s!"transitions={rec.transitions.size}"
  let declNames := rec.decls.filterMap (fun d => (getStr d "name").toOption)
  results := results.push <| check "failing:failed-theorem-not-stored-as-fact"
    (!declNames.contains "CorpusFail.bad") s!"decls={declNames}"
  return results

end Mathrecord.Validate
