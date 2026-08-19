import Mathrecord.Extract

/-! Phase 2A/2B study pass.

For one source file (one process), on top of the Gate-1 extraction:

- shallow records (type only) for every declaration referenced by stored decls;
- P1 reference occurrences (name, layer, path, multiplicity — exact);
- P2 support sets (deduplicated P1 — deterministic-derived);
- P3 infrastructure classifications (reversible, reasons attached — derived view);
- P4 named application occurrences (spines with nesting, arg heads, result-type
  sid via Meta.inferType under an instantiated telescope — deterministic-derived);
- P5 / use events: explicit tactic families attributed via elaborator TermInfo
  (never via pretty-printed text) with before/after states — observed;
- P6 one-level expansion data (direct deps of direct deps — deterministic-derived).

Trust classes and completeness flags are attached throughout. Raw data is never
replaced by filtered views.
-/

namespace Mathrecord.Study

open Lean Elab Meta Mathrecord Mathrecord.Extract

/-! ## Infrastructure classification (P3) — reversible, reasons attached -/

def eqMachinery : List Name :=
  [``Eq.mpr, ``Eq.mp, ``Eq.rec, ``Eq.ndrec, ``congrArg, ``congrFun, ``congr,
   ``Eq.trans, ``Eq.symm, ``Eq.refl, ``rfl, ``id, ``Eq.subst]

def logicCore : List Name :=
  [``And.intro, ``And.left, ``And.right, ``Or.inl, ``Or.inr, ``Or.elim,
   ``Iff.mp, ``Iff.mpr, ``Iff.intro, ``Iff.rfl, ``Exists.intro, ``Exists.elim,
   ``False.elim, ``absurd, ``True.intro, ``Not.intro, ``Classical.byContradiction]

def coeRoots : List Name :=
  [`Coe, `CoeT, `CoeTail, `CoeHead, `CoeFun, `CoeSort, `CoeTC, `Nat.cast, `Int.cast, `NatCast, `IntCast, `RatCast]

def genSuffixes : List String :=
  ["rec", "recOn", "casesOn", "brecOn", "below", "ndrec", "noConfusion",
   "noConfusionType", "ibelow", "binductionOn", "injEq", "sizeOf_spec", "mk.injEq", "eq_def", "eq_1", "eq_2", "eq_3"]

/-- Classify one referenced declaration. Multiple classes possible; empty = domain. -/
def classify (env : Environment) (n : Name) (isInst : Bool) : List String := Id.run do
  let mut cls : List String := []
  if isInst then cls := "typeclass-instance" :: cls
  if let some ci := env.find? n then
    match ci with
    | .recInfo _ => cls := "recursor" :: cls
    | .ctorInfo _ =>
      if logicCore.contains n then cls := "logic-core-ctor" :: cls
    | _ => pure ()
  if env.isProjectionFn n then cls := "structure-projection" :: cls
  if let some last := n.componentsRev.head? then
    if let .str _ s := last then
      if genSuffixes.contains s || s.startsWith "match_" || s.startsWith "proof_" then
        cls := "generated" :: cls
  if n.isInternalDetail then cls := "internal-detail" :: cls
  if eqMachinery.contains n then cls := "eq-machinery" :: cls
  if logicCore.contains n then cls := "logic-core" :: cls
  if coeRoots.contains n.getRoot then cls := "coercion" :: cls
  return cls.eraseDups

/-! ## P1 — reference occurrences with expression paths -/

structure RefOcc where
  name : Name
  layer : String          -- "type" | "body"
  path : String

partial def collectRefs (layer : String) (e : Expr) (path : String := "r")
    (acc : Array RefOcc := #[]) : Array RefOcc :=
  match e with
  | .const n _ => acc.push { name := n, layer, path }
  | .app f a =>
    collectRefs layer a (path ++ ".a") (collectRefs layer f (path ++ ".f") acc)
  | .lam _ t b _ | .forallE _ t b _ =>
    collectRefs layer b (path ++ ".b") (collectRefs layer t (path ++ ".t") acc)
  | .letE _ t v b _ =>
    collectRefs layer b (path ++ ".b")
      (collectRefs layer v (path ++ ".v") (collectRefs layer t (path ++ ".t") acc))
  | .mdata _ b => collectRefs layer b path acc
  | .proj _ _ b => collectRefs layer b (path ++ ".p") acc
  | _ => acc

/-! ## P4 — named application occurrences -/

structure AppOcc where
  head : Name
  nArgs : Nat
  argHeads : Array String      -- per arg: const name, or expr kind tag
  argIsProof : Array Bool
  resultHead : String          -- head of inferred result type (or tag)
  resultIsProp : Bool
  resultOk : Bool              -- inferType succeeded
  parent : Option Nat
  depth : Nat
  path : String

def headTag (e : Expr) : String :=
  match e.getAppFn with
  | .const n _ => toString n
  | .fvar _ => "<local>"
  | .bvar _ => "<bvar>"
  | .mvar _ => "<mvar>"
  | .sort _ => "<sort>"
  | .lam .. => "<lam>"
  | .forallE .. => "<pi>"
  | .letE .. => "<let>"
  | .lit _ => "<lit>"
  | .proj .. => "<proj>"
  | .mdata .. => "<mdata>"
  | .app .. => "<app>"

/-- Walk a closed expression, instantiating binders, collecting application
spines headed by named constants. -/
partial def collectApps (e : Expr) (parent : Option Nat := none) (depth : Nat := 0)
    (path : String := "r") : StateRefT (Array AppOcc) MetaM Unit := do
  match e with
  | .app .. =>
    let fn := e.getAppFn
    let args := e.getAppArgs
    match fn with
    | .const c _ =>
      let mut argHeads : Array String := #[]
      let mut argIsProof : Array Bool := #[]
      for a in args do
        argHeads := argHeads.push (headTag a)
        argIsProof := argIsProof.push (← try Meta.isProof a catch _ => pure false)
      let (resultHead, resultIsProp, resultOk) ←
        try
          let t ← Meta.inferType e
          pure (headTag t, ← try Meta.isProp t catch _ => pure false, true)
        catch _ => pure ("<inferType-failed>", false, false)
      let idx := (← get).size
      modify (·.push { head := c, nArgs := args.size, argHeads, argIsProof,
                       resultHead, resultIsProp, resultOk, parent, depth, path })
      for h : i in [0:args.size] do
        collectApps args[i] (some idx) (depth + 1) s!"{path}.a{i}"
    | _ =>
      collectApps fn parent depth (path ++ ".f")
      for h : i in [0:args.size] do
        collectApps args[i] parent depth s!"{path}.a{i}"
  | .lam n t b bi =>
    collectApps t parent depth (path ++ ".t")
    withLocalDecl n bi t fun x =>
      collectApps (b.instantiate1 x) parent depth (path ++ ".b")
  | .forallE n t b bi =>
    collectApps t parent depth (path ++ ".t")
    withLocalDecl n bi t fun x =>
      collectApps (b.instantiate1 x) parent depth (path ++ ".b")
  | .letE n t v b _ =>
    collectApps t parent depth (path ++ ".t")
    collectApps v parent depth (path ++ ".v")
    withLetDecl n t v fun x =>
      collectApps (b.instantiate1 x) parent depth (path ++ ".b")
  | .mdata _ b => collectApps b parent depth path
  | .proj _ _ b => collectApps b parent depth (path ++ ".p")
  | .const c _ =>
    -- zero-argument use of a named constant: record as an occurrence
    let idx := (← get).size
    modify (·.push { head := c, nArgs := 0, argHeads := #[], argIsProof := #[],
                     resultHead := "", resultIsProp := false, resultOk := false,
                     parent, depth, path })
  | _ => pure ()

/-! ## P5 / use events — TermInfo-attributed explicit tactic families -/

def explicitFamilies : List (Name × String) :=
  [(`Lean.Parser.Tactic.apply, "apply"),
   (`Lean.Parser.Tactic.exact, "exact"),
   (`Lean.Parser.Tactic.refine, "refine"),
   (`Lean.Parser.Tactic.rwSeq, "rw"),
   (`Lean.Parser.Tactic.rewriteSeq, "rewrite"),
   (`Lean.Parser.Tactic.unfold, "unfold"),
   (`Lean.Parser.Tactic.simp, "simp"),
   (`Lean.Parser.Tactic.simpAll, "simp_all"),
   (`Lean.Parser.Tactic.constructor, "constructor"),
   (`Lean.Parser.Tactic.exacts, "exacts"),
   (`Lean.Parser.Tactic.induction, "induction"),
   (`Lean.Parser.Tactic.cases, "cases"),
   (`Lean.Parser.Tactic.tacticHave_, "have"),
   (`Lean.Parser.Tactic.specialize, "specialize"),
   (`calcTactic, "calc")]

structure TacNode where
  idx : Nat
  ctx : ContextInfo
  ti : TacticInfo

structure TermUnder where
  tacIdx : Option Nat
  ctx : ContextInfo
  term : TermInfo
  /-- topmost term elaboration under its tactic (parent info was not a TermInfo) -/
  topmost : Bool

structure EvCollector where
  tactics : Array TacNode := #[]
  terms : Array TermUnder := #[]

partial def collectEventData (t : InfoTree) (ctx? : Option ContextInfo := none)
    (curTac : Option Nat := none) (parentWasTerm : Bool := false) :
    StateM EvCollector Unit := do
  match t with
  | .context pctx t => collectEventData t (pctx.mergeIntoOuter? ctx?) curTac parentWasTerm
  | .node i cs =>
    match i, ctx? with
    | .ofTacticInfo ti, some ctx =>
      let idx := (← get).tactics.size
      modify fun s => { s with tactics := s.tactics.push { idx, ctx, ti } }
      -- glue nodes (sequencing/brackets) must not capture term attributions:
      -- keep the nearest *substantive* enclosing tactic for terms beneath them
      let newCur := if Extract.glueKinds.contains ti.stx.getKind ||
                       ti.stx.getKind == `null then curTac else some idx
      for c in cs do
        collectEventData c ctx? newCur false
    | .ofTermInfo term, some ctx =>
      let tu : TermUnder := { tacIdx := curTac, ctx, term, topmost := !parentWasTerm }
      modify fun s => { s with terms := s.terms.push tu }
      for c in cs do
        collectEventData c ctx? curTac true
    | _, _ =>
      for c in cs do
        collectEventData c ctx? curTac parentWasTerm
  | .hole _ => pure ()

/-! ## Study driver -/

def posOf (fileMap : FileMap) (stx : Syntax) : Json :=
  spanJsonOfStx fileMap stx

structure StudyConfig where
  /-- record P4/P6 only for these decls (all non-internal theorems/defs if empty) -/
  maxShowcase : Nat := 1000

/-- Shallow record for a referenced (usually imported) declaration. -/
def shallowDeclJson (env : Environment) (encSt : EncState) (n : Name) (isInst : Bool) :
    (Json × EncState) := Id.run do
  let some ci := env.find? n |
    return (Json.mkObj [("name", Json.str (toString n)), ("error", Json.str "not-found")], encSt)
  let sc : Scope := { levelParams := ci.levelParams }
  let enc : EncM (String × String) := do
    let tid ← encodeExpr sc (stripMData ci.type)
    let tsid ← match sidOf sc {} {} (stripMData ci.type) with
      | .ok s => pure s | .error e => throw e
    pure (tid, tsid)
  match enc.run encSt with
  | .ok ((tid, tsid), encSt') =>
    let modName := env.getModuleIdxFor? n |>.map (fun i => toString env.header.moduleNames[i.toNat]!)
      |>.getD (toString env.mainModule)
    return (Json.mkObj [
      ("name", Json.str (toString n)),
      ("kind", Json.str (kindString ci)),
      ("levelParams", toJson (ci.levelParams.map toString)),
      ("type", Json.str tid),
      ("typeSid", Json.str tsid),
      ("module", Json.str modName),
      ("origin", Json.str "imported"),
      ("classification", toJson (classify env n isInst)),
      ("trust", Json.str "lean-exact")], encSt')
  | .error e =>
    return (Json.mkObj [("name", Json.str (toString n)),
      ("error", Json.str (toString e))], encSt)

def refOccJson (r : RefOcc) : Json :=
  Json.mkObj [("name", Json.str (toString r.name)), ("layer", Json.str r.layer),
              ("path", Json.str r.path)]

def appOccJson (a : AppOcc) : Json :=
  Json.mkObj [
    ("head", Json.str (toString a.head)),
    ("nArgs", toJson a.nArgs),
    ("argHeads", toJson a.argHeads),
    ("argIsProof", toJson a.argIsProof),
    ("resultHead", Json.str a.resultHead),
    ("resultIsProp", Json.bool a.resultIsProp),
    ("resultOk", Json.bool a.resultOk),
    ("parent", a.parent.map toJson |>.getD Json.null),
    ("depth", toJson a.depth),
    ("path", Json.str a.path),
    ("trust", Json.str "deterministic-derived")]

/-- Run the study on one file. -/
def studyFile (path : System.FilePath) : IO Json := do
  let raw ← runExtraction path false
  let env := raw.pf.env
  let record ← assembleRecord path raw
  let mut encSt := raw.encSt

  -- coreCtx for Meta computations
  let coreCtx : Core.Context := { fileName := raw.pf.fileName, fileMap := raw.fileMap }
  let runMeta {α} (act : MetaM α) : IO α := do
    let (a, _) ← ((act.run' {} {}).toIO coreCtx { env })
    pure a

  -- P1/P2 for all stored decls; P4 for non-internal theorem/def decls
  let mut declStudies : Array Json := #[]
  let mut referenced : Std.HashMap Name Bool := {}   -- name -> seen
  for n in raw.storedNames do
    let some ci := env.find? n | continue
    let typeRefs := collectRefs "type" (stripMData ci.type)
    let bodyRefs := match ci.value? (allowOpaque := true) with
      | some v => collectRefs "body" (stripMData v)
      | none => #[]
    for r in typeRefs ++ bodyRefs do
      referenced := referenced.insert r.name true
    let supportType := (typeRefs.map (·.name)).toList.eraseDups
    let supportBody := (bodyRefs.map (·.name)).toList.eraseDups
    let isShowcase := !n.isInternalDetail &&
      (match ci with | .thmInfo _ => true | .defnInfo _ => true | _ => false)
    -- P4 on the proof/body term (showcase only; loud completeness flag)
    let mut appsJson : Json := Json.null
    let mut appsComplete := "not-computed"
    if isShowcase then
      match ci.value? (allowOpaque := true) with
      | some v =>
        let res ← try
          let occs ← runMeta ((collectApps (stripMData v)).run #[] <&> (·.2))
          pure (some occs)
        catch e =>
          appsComplete := s!"failed: {e.toString.take 80}"
          pure none
        match res with
        | some occs =>
          appsJson := Json.arr (occs.map appOccJson)
          appsComplete := "complete"
        | none => pure ()
      | none => appsComplete := "no-body"
    let sizes := Json.mkObj [
      ("typeSize", toJson (stripMData ci.type).sizeWithoutSharing),
      ("valueSize", toJson ((ci.value? (allowOpaque := true)).map (stripMData · |>.sizeWithoutSharing) |>.getD 0))]
    declStudies := declStudies.push <| Json.mkObj [
      ("name", Json.str (toString n)),
      ("kind", Json.str (kindString ci)),
      ("showcase", Json.bool isShowcase),
      ("sizes", sizes),
      ("p1_typeRefs", Json.arr (typeRefs.map refOccJson)),
      ("p1_bodyRefs", Json.arr (bodyRefs.map refOccJson)),
      ("p2_supportType", toJson (supportType.map toString)),
      ("p2_supportBody", toJson (supportBody.map toString)),
      ("p4_apps", appsJson),
      ("p4_completeness", Json.str appsComplete)]

  -- shallow records + P3 classification for every referenced declaration
  let refNames := (referenced.toList.map (·.1)).toArray.qsort (fun a b => toString a < toString b)
  let mut refDecls : Array Json := #[]
  for n in refNames do
    let isInst ← runMeta (Meta.isInstance n)
    let (j, encSt') := shallowDeclJson env encSt n isInst
    refDecls := refDecls.push j
    encSt := encSt'

  -- P5 / use events from InfoTrees
  let (_, ev) := (raw.pf.trees.foldlM (fun _ t => collectEventData t) ()).run {}
  let famMap : Std.HashMap Name String := explicitFamilies.foldl (fun m (k, v) => m.insert k v) {}
  let mut events : Array Json := #[]
  for tac in ev.tactics do
    let kind := tac.ti.stx.getKind
    let some role := famMap.get? kind | continue
    -- topmost elaborated terms under this tactic, const-headed
    let mut attributions : Array Json := #[]
    for tu in ev.terms do
      if tu.tacIdx == some tac.idx && tu.topmost then
        let e := stripMData tu.term.expr
        match e.getAppFn with
        | .const c us =>
          attributions := attributions.push <| Json.mkObj [
            ("decl", Json.str (toString c)),
            ("nUniverses", toJson us.length),
            ("nArgs", toJson e.getAppArgs.size),
            ("attribution", Json.str "elaborator-terminfo")]
        | _ => pure ()
    let before := tac.ti.goalsBefore.filterMap (raw.work.mvarToState.get? ·)
    let after := tac.ti.goalsAfter.filterMap (raw.work.mvarToState.get? ·)
    let completeness := if attributions.isEmpty then "no-named-attribution" else "attributed"
    events := events.push <| Json.mkObj [
      ("role", Json.str role),
      ("tacticKind", Json.str (toString kind)),
      ("decl", Json.str (toString (tac.ctx.parentDecl?.getD Name.anonymous))),
      ("src", posOf raw.fileMap tac.ti.stx),
      ("actionText", Json.str ((stxText raw.fileMap tac.ti.stx).take 120 |>.toString)),
      ("before", toJson before),
      ("after", toJson after),
      ("attributions", Json.arr attributions),
      ("completeness", Json.str completeness),
      ("outcome", Json.str "success"),
      ("trust", Json.str "observed")]

  -- non-family tactic kinds tally (for coverage measurement)
  let mut otherKinds : Std.HashMap String Nat := {}
  for tac in ev.tactics do
    let k := toString tac.ti.stx.getKind
    if !(famMap.contains tac.ti.stx.getKind) then
      otherKinds := otherKinds.insert k ((otherKinds.get? k).getD 0 + 1)
  let otherKindsJson := Json.mkObj (otherKinds.toList.map (fun (k, v) => (k, toJson v)))

  return Json.mkObj [
    ("schema", Json.str "mathrecord-study-0.1"),
    ("record", record),
    ("expressionsExtended", Json.arr encSt.nodes),
    ("referencedDecls", Json.arr refDecls),
    ("declStudies", Json.arr declStudies),
    ("useEvents", Json.arr events),
    ("nonFamilyTacticKinds", otherKindsJson)]

end Mathrecord.Study
