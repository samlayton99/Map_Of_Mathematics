import Mathrecord.Frontend
import Mathrecord.Record

/-! MathRecord extractor: one Lean source file (one process) → one canonical
JSON record containing E (environment), X (expressions), D (declarations),
S (local states), and a T spike (observed + programmatic transitions). -/

namespace Mathrecord.Extract

open Lean Elab Meta Mathrecord

def extractorVersion := "mathrecord/0.1.0"

/-- Deterministic 64-bit content hash rendered as hex (fingerprint use only;
identity claims always rest on full canonical strings, not hashes). -/
def hex64 (s : String) : String :=
  let h := s.hash
  (Nat.toDigits 16 h.toNat).asString

def posJson (p : Position) : Json :=
  Json.mkObj [("line", toJson p.line), ("col", toJson p.column)]

def spanJsonOfStx (fileMap : FileMap) (stx : Syntax) : Json :=
  match stx.getPos?, stx.getTailPos? with
  | some b, some e =>
    Json.mkObj [("start", posJson (fileMap.toPosition b)), ("end", posJson (fileMap.toPosition e))]
  | _, _ => Json.null

/-- Display-only source text of a syntax node (never used as formal content). -/
def stxText (_fileMap : FileMap) (stx : Syntax) : String :=
  match stx.reprint with
  | some s => s.trimAscii.toString
  | none => toString stx.getKind

def reducibilityString (env : Environment) (n : Name) : String :=
  match getReducibilityStatusCore env n with
  | .reducible => "reducible" | .semireducible => "semireducible" | .irreducible => "irreducible"
  | .implicitReducible => "implicitReducible" | .instanceReducible => "instanceReducible"

def kindString : ConstantInfo → String
  | .axiomInfo _  => "axiom"      | .defnInfo _   => "def"
  | .thmInfo _    => "theorem"    | .opaqueInfo _ => "opaque"
  | .quotInfo _   => "quot"       | .inductInfo _ => "inductive"
  | .ctorInfo _   => "constructor"| .recInfo _    => "recursor"

/-- Kind-specific structural fields (completeness; no silent loss of decl kind data). -/
def kindExtras (sc : Scope) (ci : ConstantInfo) : EncM Json := do
  match ci with
  | .defnInfo v =>
    let hints := match v.hints with
      | .abbrev => "abbrev" | .opaque => "opaque" | .regular n => s!"regular:{n}"
    let safety := match v.safety with
      | .safe => "safe" | .unsafe => "unsafe" | .partial => "partial"
    return Json.mkObj [("hints", Json.str hints), ("safety", Json.str safety)]
  | .axiomInfo v => return Json.mkObj [("isUnsafe", Json.bool v.isUnsafe)]
  | .opaqueInfo v => return Json.mkObj [("isUnsafe", Json.bool v.isUnsafe)]
  | .inductInfo v =>
    return Json.mkObj [("numParams", toJson v.numParams), ("numIndices", toJson v.numIndices),
      ("all", toJson (v.all.map toString)), ("ctors", toJson (v.ctors.map toString)),
      ("isRec", Json.bool v.isRec)]
  | .ctorInfo v =>
    return Json.mkObj [("induct", Json.str (toString v.induct)), ("cidx", toJson v.cidx),
      ("numParams", toJson v.numParams), ("numFields", toJson v.numFields)]
  | .recInfo v =>
    let rules ← v.rules.mapM fun r => do
      return Json.mkObj [("ctor", Json.str (toString r.ctor)), ("nfields", toJson r.nfields),
        ("rhs", Json.str (← encodeExpr sc (stripMData r.rhs)))]
    return Json.mkObj [("all", toJson (v.all.map toString)), ("numParams", toJson v.numParams),
      ("numIndices", toJson v.numIndices), ("numMotives", toJson v.numMotives),
      ("numMinors", toJson v.numMinors), ("k", Json.bool v.k), ("rules", Json.arr rules.toArray)]
  | .quotInfo v =>
    let k := match v.kind with
      | .type => "type" | .ctor => "ctor" | .lift => "lift" | .ind => "ind"
    return Json.mkObj [("quotKind", Json.str k)]
  | .thmInfo _ => return Json.mkObj []

structure ExtractedState where
  id      : String
  sid     : String
  json    : Json

structure StWork where
  states      : Array Json := #[]
  stateBySid  : Std.HashMap String String := {}   -- content sid → state id (dedup)
  mvarToState : Std.HashMap MVarId String := {}   -- first materialization wins
  transitions : Array Json := #[]
  stateMeta   : Array (MVarId × ContextInfo × MetavarContext) := #[]  -- for spike

/-- Syntax kinds that are structural glue rather than proof actions. -/
def glueKinds : List Name :=
  [`Lean.Parser.Term.byTactic, `by, `Lean.Parser.Tactic.tacticSeq,
   `Lean.Parser.Tactic.tacticSeq1Indented, `null, `Lean.Parser.Tactic.paren,
   `Lean.Parser.Term.byTactic']

partial def collectTacticInfos (t : InfoTree) (ctx? : Option ContextInfo := none) :
    List (ContextInfo × TacticInfo) :=
  match t with
  | .context pctx t => collectTacticInfos t (pctx.mergeIntoOuter? ctx?)
  | .node i cs =>
    let rest := cs.toList.flatMap (collectTacticInfos · ctx?)
    match i, ctx? with
    | .ofTacticInfo ti, some ctx => (ctx, ti) :: rest
    | _, _ => rest
  | .hole _ => []

/-- Materialize one local state from (mctx, goal mvar). Returns state id. -/
def materializeState (ctx : ContextInfo) (mctx : MetavarContext) (g : MVarId)
    (fileMap : FileMap) (stx : Syntax) : StateT StWork EncM (Option String) := do
  let w ← get
  if let some sid := w.mvarToState.get? g then
    return some sid
  let some md := mctx.findDecl? g | return none
  -- ordered context: build fvar ordinal map first
  let mut fvarOrd : Std.HashMap FVarId Nat := {}
  let mut ord := 0
  for ld in md.lctx do
    fvarOrd := fvarOrd.insert ld.fvarId ord
    ord := ord + 1
  let sc : Scope := { fvarOrd := some fvarOrd, allowMVars := true }
  -- reset per-state mvar ordinals
  modifyThe EncState fun s => { s with mvarOrd := {}, lmvarOrd := {} }
  let inst (e : Expr) : Expr := (instantiateMVarsCore mctx e).1
  let mut ctxJson : Array Json := #[]
  let mut ctxSid : Array String := #[]
  let mut hasMVars := false
  let mut i := 0
  for ld in md.lctx do
    let t := stripMData (inst ld.type)
    let tid ← liftM (m := EncM) (encodeExpr sc t)
    let encSt ← getThe EncState
    let tsid ← match sidOf sc encSt.mvarOrd encSt.lmvarOrd t with
      | .ok s => pure s
      | .error e => throw e
    hasMVars := hasMVars || t.hasMVar || t.hasLevelMVar
    let ldKind := match ld.kind with
      | .default => "default" | .implDetail => "implDetail" | .auxDecl => "auxDecl"
    match ld with
    | .cdecl _ _ un _ bi _ =>
      ctxJson := ctxJson.push <| Json.mkObj [("i", toJson i), ("d", Json.str (toString un)),
        ("bi", Json.str (biToString bi)), ("ldKind", Json.str ldKind),
        ("t", Json.str tid)]
      ctxSid := ctxSid.push s!"({biToString bi},{ld.isImplementationDetail},{tsid})"
    | .ldecl _ _ un _ v nonDep _ =>
      let v := stripMData (inst v)
      let vid ← liftM (m := EncM) (encodeExpr sc v)
      let encSt ← getThe EncState
      let vsid ← match sidOf sc encSt.mvarOrd encSt.lmvarOrd v with
        | .ok s => pure s
        | .error e => throw e
      hasMVars := hasMVars || v.hasMVar || v.hasLevelMVar
      ctxJson := ctxJson.push <| Json.mkObj [("i", toJson i), ("d", Json.str (toString un)),
        ("bi", Json.str "default"), ("ldKind", Json.str ldKind),
        ("nonDep", Json.bool nonDep), ("t", Json.str tid), ("v", Json.str vid)]
      ctxSid := ctxSid.push s!"(let,{ld.isImplementationDetail},{tsid},{vsid})"
    i := i + 1
  let target := stripMData (inst md.type)
  let targetId ← liftM (m := EncM) (encodeExpr sc target)
  let encSt ← getThe EncState
  let targetSid ← match sidOf sc encSt.mvarOrd encSt.lmvarOrd target with
    | .ok s => pure s
    | .error e => throw e
  hasMVars := hasMVars || target.hasMVar || target.hasLevelMVar
  let stateSid := s!"St([{";".intercalate ctxSid.toList}];{targetSid})"
  let w ← get
  match w.stateBySid.get? stateSid with
  | some sid =>
    modify fun w => { w with mvarToState := w.mvarToState.insert g sid }
    return some sid
  | none =>
    let sid := s!"s{w.states.size}"
    let json := Json.mkObj [
      ("id", Json.str sid),
      ("decl", Json.str (toString (ctx.parentDecl?.getD Name.anonymous))),
      ("goalUserName", Json.str (toString md.userName)),
      ("ctx", Json.arr ctxJson),
      ("target", Json.str targetId),
      ("sid", Json.str stateSid),
      ("src", spanJsonOfStx fileMap stx),
      ("status", Json.str "open"),
      ("hasMVars", Json.bool hasMVars),
      ("trust", Json.str "lean-exact")]
    modify fun w => { w with
      states := w.states.push json
      stateBySid := w.stateBySid.insert stateSid sid
      mvarToState := w.mvarToState.insert g sid
      stateMeta := w.stateMeta.push (g, ctx, mctx) }
    return some sid

def extractStatesAndTransitions (pf : ProcessedFile) (fileMap : FileMap) :
    StateT StWork EncM Unit := do
  let tacInfos := pf.trees.flatMap (collectTacticInfos ·)
  for (ctx, ti) in tacInfos do
    if glueKinds.contains ti.stx.getKind then
      continue
    let mut before : Array String := #[]
    for g in ti.goalsBefore do
      if let some sid ← materializeState ctx ti.mctxBefore g fileMap ti.stx then
        before := before.push sid
    let mut after : Array String := #[]
    for g in ti.goalsAfter do
      if let some sid ← materializeState ctx ti.mctxAfter g fileMap ti.stx then
        after := after.push sid
    let w ← get
    let tid := s!"t{w.transitions.size}"
    let tj := Json.mkObj [
      ("id", Json.str tid),
      ("actionKind", Json.str (toString ti.stx.getKind)),
      ("actionText", Json.str (stxText fileMap ti.stx)),
      ("src", spanJsonOfStx fileMap ti.stx),
      ("before", toJson before),
      ("after", toJson after),
      ("outcome", Json.str "success"),
      ("trust", Json.str "observed"),
      ("note", Json.str "nested-syntax spike; not a normalized trace")]
    modify fun w => { w with transitions := w.transitions.push tj }

/-- Programmatic transition spike: run `skip` (succeeds) and `done` (fails)
against the first recorded state, with its real metavariable context. -/
def programmaticSpike (pf : ProcessedFile) (w : StWork) : IO (Array Json) := do
  let some (g, ctx, mctx) := w.stateMeta[0]? | return #[]
  let some beforeId := w.mvarToState.get? g | return #[]
  let mut out : Array Json := #[]
  for (tacStr, expectSuccess) in [("skip", true), ("done", false)] do
    match Parser.runParserCategory pf.env `tactic tacStr "<spike>" with
    | .error e => out := out.push <| Json.mkObj [("error", Json.str e)]
    | .ok stx =>
      let lctx := (mctx.findDecl? g).map (·.lctx) |>.getD {}
      let result ← ctx.runMetaM lctx do
        setMCtx mctx
        try
          let (goals, _) ← Elab.runTactic g stx
          -- `Tactic.run` recovers from errors by admitting the goal (sorryAx)
          -- and logging the error; detect that as a failure, loudly.
          let assignment ← instantiateMVars (mkMVar g)
          if assignment.hasSorry then
            let msgs := (← Core.getMessageLog).toList
            let errs ← msgs.filterMapM fun m =>
              if m.severity == .error then some <$> m.data.toString else pure none
            pure (Sum.inr (String.intercalate "; " errs))
          else
            pure (Sum.inl goals.length)
        catch ex =>
          pure (Sum.inr (← ex.toMessageData.toString))
      let (outcome, diag, nAfter) := match result with
        | .inl n => (if expectSuccess then "success" else "unexpected-success", "", n)
        | .inr msg => (if expectSuccess then "unexpected-failure" else "failure", msg, 0)
      out := out.push <| Json.mkObj [
        ("actionText", Json.str tacStr),
        ("before", Json.str beforeId),
        ("afterCount", toJson nAfter),
        ("outcome", Json.str outcome),
        ("diagnostic", Json.str diag),
        ("trust", Json.str "observed-programmatic"),
        ("note", Json.str "after-states not materialized (spike only)")]
  return out

def envJson (pf : ProcessedFile) : Json :=
  let imports := (pf.env.header.imports.map (toString ·.module)).toList.eraseDups
  let moduleNamesHash := hex64 (String.intercalate "," (pf.env.header.moduleNames.map toString).toList)
  let fingerprint := hex64 <| String.intercalate "|"
    ([Lean.versionString, Lean.githash] ++ imports ++ [moduleNamesHash, extractorVersion])
  Json.mkObj [
    ("environment_id", Json.str s!"env:{fingerprint}"),
    ("lean_version", Json.str Lean.versionString),
    ("lean_githash", Json.str Lean.githash),
    ("ordered_imports", toJson imports),
    ("module_count", toJson pf.env.header.moduleNames.size),
    ("module_names_hash", Json.str moduleNamesHash),
    ("extractor", Json.str extractorVersion),
    ("fingerprint", Json.str fingerprint)]

/-- All artifacts of one extraction pass, for reuse by `extract` and `study`. -/
structure RawExtraction where
  pf : ProcessedFile
  fileMap : FileMap
  encSt : EncState
  declJsons : Array Json
  unsupported : Array Json
  work : StWork
  failures : Array Json
  progSpike : Array Json
  /-- names of stored declarations, in stored order -/
  storedNames : Array Name

/-- Run the full extraction pass (declarations, states, transitions, failures). -/
def runExtraction (path : System.FilePath) (spike : Bool) : IO RawExtraction := do
  let pf ← Mathrecord.processFile path
  let fileMap := FileMap.ofString (← IO.FS.readFile path)
  -- declarations: everything defined in this file (constants.map₂), sorted
  let localDecls := pf.env.constants.map₂.toList
  let sorted := localDecls.toArray.qsort (fun a b => toString a.1 < toString b.1)
  let mut encSt : EncState := {}
  let mut declJsons : Array Json := #[]
  let mut unsupported : Array Json := #[]
  -- decl ranges need CoreM
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := fileMap }
  let ranges ← (do
    let act : CoreM (Array (Name × Option DeclarationRanges)) := do
      sorted.mapM fun (n, _) => do pure (n, ← findDeclarationRanges? n)
    let (a, _) ← act.toIO coreCtx { env := pf.env }
    pure a)
  let rangeMap : Std.HashMap Name (Option DeclarationRanges) := ranges.foldl (fun m (n, r) => m.insert n r) {}
  for (name, ci) in sorted do
    let deps := ci.type.getUsedConstants ++ (ci.value? (allowOpaque := true) |>.map (·.getUsedConstants) |>.getD #[])
    if deps.contains ``sorryAx then
      unsupported := unsupported.push <| Json.mkObj
        [("name", Json.str (toString name)), ("reason", Json.str "contains sorryAx (incomplete proof)")]
      continue
    let sc : Scope := { levelParams := ci.levelParams }
    let declId := s!"d{declJsons.size}"
    let spanJ := match rangeMap.get? name |>.join with
      | some r => Json.mkObj [("start", posJson r.range.pos), ("end", posJson r.range.endPos)]
      | none => Json.null
    let reduc := reducibilityString pf.env name
    let mainMod := toString pf.env.mainModule
    let enc : EncM Json := do
      let typeId ← encodeExpr sc (stripMData ci.type)
      let typeSid ← match sidOf sc {} {} (stripMData ci.type) with
        | .ok s => pure s | .error e => throw e
      let valueData ← match ci.value? (allowOpaque := true) with
        | some v => do
          let vid ← encodeExpr sc (stripMData v)
          let vsid ← match sidOf sc {} {} (stripMData v) with
            | .ok s => pure s | .error e => throw e
          pure (some (vid, vsid))
        | none => pure none
      let extras ← kindExtras sc ci
      let base := [
        ("id", Json.str declId),
        ("name", Json.str (toString name)),
        ("kind", Json.str (kindString ci)),
        ("levelParams", toJson (ci.levelParams.map toString)),
        ("type", Json.str typeId),
        ("typeSid", Json.str typeSid),
        ("module", Json.str mainMod),
        ("span", spanJ),
        ("reducibility", Json.str reduc),
        ("extras", extras),
        ("trust", Json.str "lean-exact")]
      let full := match valueData with
        | some (vid, vsid) => base ++ [("value", Json.str vid), ("valueSid", Json.str vsid)]
        | none => base
      pure (Json.mkObj full)
    match enc.run encSt with
    | .ok (j, s) =>
      encSt := s
      declJsons := declJsons.push j
    | .error e =>
      unsupported := unsupported.push <| Json.mkObj
        [("name", Json.str (toString name)), ("reason", Json.str (toString e))]
  -- states and transitions
  let stRes := ((extractStatesAndTransitions pf fileMap).run {}).run encSt
  let (work, encSt') ← match stRes with
    | .ok ((_, w), s) => pure (w, s)
    | .error e => throw <| IO.userError s!"state extraction failed loudly: {e}"
  encSt := encSt'
  -- failure events from the message log
  let mut failures : Array Json := #[]
  for m in pf.messages.toList do
    if m.severity == .error then
      failures := failures.push <| Json.mkObj [
        ("severity", Json.str "error"),
        ("src", posJson m.pos),
        ("diagnostic", Json.str (← m.data.toString)),
        ("trust", Json.str "observed")]
  -- programmatic spike
  let progSpike ← if spike then programmaticSpike pf work else pure #[]
  let storedNames ← IO.ofExcept <| declJsons.mapM fun d =>
    (d.getObjValAs? String "name").map (·.toName)
  return { pf, fileMap, encSt, declJsons, unsupported, work, failures, progSpike, storedNames }

/-- Assemble the Gate-1 record JSON (byte-compatible with the validated format). -/
def assembleRecord (path : System.FilePath) (raw : RawExtraction) : IO Json := do
  let sourceText ← IO.FS.readFile path
  return Json.mkObj [
    ("schema", Json.str "mathrecord-0.1"),
    ("source", Json.mkObj [("file", Json.str path.toString),
                           ("contentHash", Json.str (hex64 sourceText))]),
    ("environment", envJson raw.pf),
    ("expressions", Json.arr raw.encSt.nodes),
    ("declarations", Json.arr raw.declJsons),
    ("states", Json.arr raw.work.states),
    ("transitions", Json.arr raw.work.transitions),
    ("programmaticTransitions", Json.arr raw.progSpike),
    ("failures", Json.arr raw.failures),
    ("unsupported", Json.arr raw.unsupported)]

/-- Extract one file into a record. -/
def extractFile (path : System.FilePath) (spike : Bool) : IO Json := do
  assembleRecord path (← runExtraction path spike)

end Mathrecord.Extract
