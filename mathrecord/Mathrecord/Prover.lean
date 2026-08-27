import Mathrecord.HeadDump
import Mathrecord.Ho

/-! The first closed-loop dynamic prover: best-first search over live proof
states inside the elaborator.

State = (Meta.SavedState, open goal mvars) - metavariable coupling between
subgoals is preserved because the whole MetavarContext travels with the
node; no serialization boundary exists.  Actions are organized in banks:

  s  structural : intro, assumption, rfl-family, constructors of the goal
  b  backward   : apply a toolkit theorem whose conclusion head matches
  r  rewrite    : rewrite with a toolkit equality/iff, either direction,
                  filtered by LHS/RHS head occurrence in the goal
  p  automation : default simp set

Every attempted action (success or failure) costs one unit of the Lean-call
budget.  Duplicate child states are merged by a canonical key.  Per-run
statistics record, for each bank: attempts, legal actions, duplicate
children - the multi-bank legality census falls out of every run.

CLI: mathrecord prove <ImportMathlib.lean> <tasks.json> <out.jsonl>
       <banks e.g. sbrp> <budget>

tasks.json: {"tasks":[{"n": <goal theorem>, "bw":[names], "rw":[names]}]}
The toolkit lists come from the python side under the CONSERVATIVE
accessibility regime (imports only, own module excluded).
-/

namespace Mathrecord.Prover

open Lean Meta Mathrecord Mathrecord.HeadDump

structure Task where
  name : Name
  bw   : Array Name
  rw   : Array Name
  forbid : Array Name := #[]   -- own-module constants outside the statement cone

structure Node where
  saved : Meta.SavedState
  goals : List MVarId
  cost  : Float
  depth : Nat
  path  : List String
  heads : List String := []   -- head of the goal each action attacked

structure Stats where
  attempts : Std.HashMap String Nat := {}
  legal    : Std.HashMap String Nat := {}
  dups     : Nat := 0
  expansions : Nat := 0

def bump (m : Std.HashMap String Nat) (k : String) : Std.HashMap String Nat :=
  m.insert k (m.getD k 0 + 1)

def parseTasks (j : Json) : Except String (Array Task) := do
  let ts ← (← j.getObjVal? "tasks").getArr?
  ts.mapM fun t => do
    let n ← (← t.getObjVal? "n").getStr?
    let bw ← (← t.getObjVal? "bw").getArr?
    let rw ← (← t.getObjVal? "rw").getArr?
    let fb := match t.getObjVal? "fb" with
      | .ok v => (v.getArr?).toOption.getD #[]
      | .error _ => #[]
    pure { name := String.toName n,
           bw := ← bw.mapM (fun c => do pure (String.toName (← c.getStr?))),
           rw := ← rw.mapM (fun c => do pure (String.toName (← c.getStr?))),
           forbid := fb.filterMap (fun c => (c.getStr?).toOption.map String.toName) }

/-- Canonical-ish key for a state: per goal, the sorted rendered local
context (non-implementation hypotheses) plus the rendered target -
goals differing only in their hypotheses are distinct states. -/
def stateKey (goals : List MVarId) : MetaM String := do
  let mut parts : Array String := #[]
  for g in goals do
    let s ← try
      g.withContext do
        let mut hs : Array String := #[]
        for d? in (← getLCtx).decls do
          match d? with
          | some d =>
            if !d.isImplementationDetail then
              hs := hs.push (toString (← instantiateMVars d.type))
          | none => pure ()
        let t ← instantiateMVars (← g.getType)
        pure (String.intercalate ";" (hs.qsort (· < ·)).toList
              ++ "⊢" ++ toString t)
    catch _ => pure "?"
    parts := parts.push s
  pure (String.intercalate "|" (parts.qsort (· < ·)).toList)

def goalHead (g : MVarId) : MetaM String := do
  let t ← instantiateMVars (← g.getType)
  pure (headTag t)

/-- Precomputed candidate info. -/
structure Cand where
  name : Name
  concl : String            -- conclusion head tag
structure RwCand where
  name : Name
  lhs : String
  rhs : String

def prepCands (env : Environment) (names : Array Name) : Array Cand := Id.run do
  let mut out := #[]
  for n in names do
    match env.find? n with
    | some ci =>
      let (_, concl) := telescope ci.type
      out := out.push { name := n, concl := headTag concl }
    | none => pure ()
  return out

def prepRw (env : Environment) (names : Array Name) : Array RwCand := Id.run do
  let mut out := #[]
  for n in names do
    match env.find? n with
    | some ci =>
      let (_, concl) := telescope ci.type
      let c := concl.consumeMData
      let args := c.getAppArgs
      if (headTag c == "Eq" && args.size >= 3) then
        out := out.push { name := n, lhs := headTag args[1]!, rhs := headTag args[2]! }
      else if (headTag c == "Iff" && args.size >= 2) then
        out := out.push { name := n, lhs := headTag args[0]!, rhs := headTag args[1]! }
    | none => pure ()
  return out

/-- Boolean-per-module import closure of the target's module: the modules a
proof at that source location may legally draw from. -/
def allowedModules (env : Environment) (own : Nat) : Array Bool := Id.run do
  let names := env.header.moduleNames
  let data := env.header.moduleData
  let mut idxOf : Std.HashMap Name Nat := {}
  for i in [0:names.size] do
    idxOf := idxOf.insert names[i]! i
  let mut allowed := (Array.range names.size).map (fun _ => false)
  let mut stack : Array Nat := #[own]
  allowed := allowed.set! own true
  while stack.size > 0 do
    let m := stack.back!
    stack := stack.pop
    match data[m]? with
    | none => pure ()
    | some md =>
      for imp in md.imports do
        match idxOf.get? imp.module with
        | some j =>
          if !(allowed[j]?.getD true) then
            allowed := allowed.set! j true
            stack := stack.push j
        | none => pure ()
  return allowed

abbrev Attempt := MetaM (List MVarId)

/-- Run one action attempt from the parent state; return child goals of the
acted-on goal on success.  Caller must have restored the parent state. -/
def tryAct (act : Attempt) : MetaM (Option (List MVarId)) := do
  try
    Core.withCurrHeartbeats do
      withOptions (fun o => o.set `maxHeartbeats (25000 : Nat)) do
        let gs ← act
        pure (some gs)
  catch _ => pure none

structure RunResult where
  solved : Bool := false
  verified : Bool := false
  path : List String := []
  callsUsed : Nat := 0
  stats : Stats := {}
  frontierLeft : Nat := 0
  usedConsts : Array String := #[]   -- constants in the discovered proof term
  goalHeads : List String := []      -- per-decision goal heads (winning path)
  partsData : Array String := #[]    -- oracle data parts provided (custom runs)
  partsProp : Array String := #[]
  guidedErrs : Array String := #[]   -- guided-act failure messages (capped)

/-- Extract ORACLE CUSTOM PARTS from a reference proof body: data-typed
subterms (witnesses, functions, motives - never proof-typed subterms, which
would leak assembly) and Prop-typed binders of lets/beta-redexes (the
intermediate `have` statements).  Binders of the theorem are instantiated
with the search telescope `xs`, so parts remain valid in every search
state.  Closed subterms only (no loose bound variables) - a documented
under-collection. -/
def collectCustomParts (xs : Array Expr) (val? : Option Expr) :
    MetaM (Array Expr × Array Expr) := do
  let some val := val? | return (#[], #[])
  let body := val.beta xs
  let mut data : Array Expr := #[]
  let mut props : Array Expr := #[]
  let mut stack : Array Expr := #[body]
  let mut fuel := 30000
  while stack.size > 0 && fuel > 0 do
    fuel := fuel - 1
    let e := (stack.back!).consumeMData
    stack := stack.pop
    match e with
    | .app .. =>
      let fn := e.getAppFn.consumeMData
      if let .lam _ t _ _ := fn then   -- beta-redex: `have`-style intermediate
        if !t.hasLooseBVars && props.size < 16 && !props.contains t then
          if ← (try Meta.isProp t catch _ => pure false) then
            props := props.push t
      -- `have h : P := v; b` elaborates to `letFun P _ v fun h => b`
      if fn.isConstOf ``letFun then
        let args := e.getAppArgs
        if args.size >= 1 then
          let t := args[0]!.consumeMData
          if !t.hasLooseBVars && props.size < 16 && !props.contains t then
            if ← (try Meta.isProp t catch _ => pure false) then
              props := props.push t
      stack := stack.push fn
      for a in e.getAppArgs do
        stack := stack.push a
        let c := a.consumeMData
        if !c.hasLooseBVars && !c.isFVar && !c.isConst && !c.isSort &&
           !c.isMVar && data.size < 24 && !data.contains c then
          let isData ← try
            let τ ← instantiateMVars (← inferType c)
            -- custom part = not a proof, not typeclass-instance plumbing
            pure (!(← Meta.isProp τ) && (← Meta.isClass? τ).isNone)
          catch _ => pure false
          if isData then
            data := data.push c
    | .lam _ _ b _ => stack := stack.push b
    | .letE _ t v b _ =>
      if !t.hasLooseBVars && props.size < 16 && !props.contains t then
        if ← (try Meta.isProp t catch _ => pure false) then
          props := props.push t
      stack := (stack.push v).push b
    | .proj _ _ s => stack := stack.push s
    | _ => pure ()
  return (data, props)

/-- Assign the oracle occurrence term directly at a data goal. -/
def oracleAssign (g : MVarId) (e : Expr) : Attempt := g.withContext do
  if ← isDefEq (mkMVar g) e then pure []
  else throwError "oracle data mismatch"

/-- Delta-unfold every target-attached auxiliary (plain `T.*` or private
`_private.….T.*` form) inside a reference term, so guided proofs and the
data terms they assign verbatim never cite them. -/
partial def deAux (env : Environment) (selfStr : String) (e : Expr)
    (fuel : Nat := 8) : Expr :=
  if fuel == 0 then e else
  let isAuxName (s : String) : Bool :=
    s.startsWith (selfStr ++ ".") ||
    (s.startsWith "_private." && (s.splitOn ("." ++ selfStr ++ ".")).length > 1)
  let e' := e.replace fun sub =>
    match sub with
    | .const c lvls =>
      if isAuxName c.toString then
        match env.find? c with
        | some ci =>
          match ci.value? (allowOpaque := true) with
          | some v => some (v.instantiateLevelParams ci.levelParams lvls)
          | none => none
        | none => none
      else none
    | _ => none
  if e' == e then e else deAux env selfStr e' (fuel - 1)

/-- Backward application with mechanical higher-order fallback: ordinary
`apply` first; on failure, a fresh telescope whose failed first-order
conclusion unification is retried with motive synthesis (kabstract) and
congruence decomposition.  No reference information is consulted. -/
def hoApply (g : MVarId) (cn : Name) : MetaM (List MVarId) := do
  try g.apply (← mkConstWithFreshMVarLevels cn)
  catch _ =>
    g.withContext do
      let ce ← mkConstWithFreshMVarLevels cn
      let hType ← inferType ce
      let (mvs, _, concl) ← forallMetaTelescope hType
      let gType ← instantiateMVars (← g.getType)
      unless ← Mathrecord.Ho.tryMotiveSynth concl gType do
        throwError "hoApply: no unifier"
      for mv in mvs do
        let m := mv.mvarId!
        unless ← m.isAssigned do
          let τ ← instantiateMVars (← m.getType)
          let isCls ← try pure (← Meta.isClass? τ).isSome catch _ => pure false
          if isCls && !τ.hasExprMVar then
            try m.assign (← synthInstance τ) catch _ => pure ()
      g.assign (mkAppN ce mvs)
      let mut out : List MVarId := []
      for mv in mvs.reverse do
        let m := mv.mvarId!
        unless ← m.isAssigned do out := m :: out
      pure out

mutual

/-- GUIDED DESCENT.  Apply the head of reference application `e` at `g`
through the engine's own unification: iterative bounded metavariable
telescope (over-applied heads re-telescoped after each assignment round),
conclusion unified last.  Proof-argument metavariables become new goals,
registered in the guide map with their reference subterms; data-argument
metavariables are assigned from the reference when `assignData`, else
registered (for the occurrence-oracle mode) and left to unification, with
a synthesis attempt for closed class-typed holes (mirroring `apply`).

CONCLUSION DEFERRAL: when eager conclusion unification fails because the
goal's endpoints are still undetermined (they are owned by a child
equation - the T2 phenomenon at the conclusion level), the guided proof
children are executed first and the conclusion is retried against the
then-concrete goal, including the mechanical synthesis fallback. -/
partial def guidedApply (guide : IO.Ref (Std.HashMap Name Expr))
    (env : Environment) (selfStr : String)
    (g : MVarId) (e : Expr) (assignData : Bool) (fuel : Nat := 48) :
    MetaM (List MVarId) :=
    g.withContext do
  let fn := e.getAppFn.consumeMData
  let args := e.getAppArgs
  let hType ← inferType fn
  let mut curType := hType
  let mut allMvs : Array Expr := #[]
  let mut proofPairs : Array (MVarId × Expr) := #[]
  let mut idx := 0
  for _ in [0:args.size] do
    if idx ≥ args.size then break
    let (mvs, _, concl) ← forallMetaBoundedTelescope curType (args.size - idx)
    if mvs.size == 0 then throwError "guided telescope stalled"
    for i in [0:mvs.size] do
      let a := args[idx + i]!
      let aP ← try Meta.isProp (← inferType a) catch _ => pure false
      if aP then
        guide.modify (·.insert mvs[i]!.mvarId!.name a)
        proofPairs := proofPairs.push (mvs[i]!.mvarId!, a)
      else if assignData then
        -- checkpointed assignment: an argument whose in-place unification
        -- fails (open sibling proof metavariables in its expected type)
        -- is deferred - registered for goal-time oracle assignment
        let s ← Meta.saveState
        let okA ← try isDefEq mvs[i]! a catch _ => pure false
        unless okA do
          s.restore
          guide.modify (·.insert mvs[i]!.mvarId!.name a)
      else
        guide.modify (·.insert mvs[i]!.mvarId!.name a)
    allMvs := allMvs ++ mvs
    curType ← instantiateMVars concl
    idx := idx + mvs.size
  -- INSTANTIATE: by the time this step runs, the goal's type metavariable
  -- may have been assigned through sibling coupling - the raw alias hides
  -- the concrete goal from the mechanical-synthesis pattern matches
  let gType ← instantiateMVars (← g.getType)
  let firstOk ← isDefEq curType gType
  -- mechanical higher-order fallback (motive synthesis / congruence
  -- decomposition) - consults ONLY the goal, never the reference
  let synthOk ← if firstOk then pure true else
    Mathrecord.Ho.tryMotiveSynth curType gType
  -- CONCLUSION DEFERRAL: run the guided proof children first when the
  -- eager conclusion fails (open endpoints owned by a child equation),
  -- then retry against the concretized goal
  let mut cOk := synthOk
  let mut deferLeft : List MVarId := []
  if !cOk && fuel > 0 then
    let s ← Meta.saveState
    let r ← try
      let mut lo : List MVarId := []
      for (pm, ref) in proofPairs do
        unless ← pm.isAssigned do
          lo := lo ++ (← solveGuidedRec guide env selfStr pm ref assignData (fuel - 1))
      let curT ← instantiateMVars curType
      let gT ← instantiateMVars (← g.getType)
      let r1 ← isDefEq curT gT
      let r2 ← if r1 then pure true else Mathrecord.Ho.tryMotiveSynth curT gT
      pure (some (r2, lo))
    catch _ => pure none
    match r with
    | some (true, lo) =>
      cOk := true
      deferLeft := lo
    | _ => s.restore
  let finalOk ← if cOk then pure true else
    -- composed search states can render defeq-but-unification-hard forms;
    -- escalate transparency before giving up
    withTransparency TransparencyMode.all
      (isDefEq (← instantiateMVars curType) (← instantiateMVars (← g.getType)))
  unless finalOk do
    let fnStr := match fn with
      | .const c _ => c.toString
      | _ => "?"
    let extra ← match gType with
      | .mvar m => do
        let d ← m.getDecl
        let k := match d.kind with
          | .natural => "natural" | .synthetic => "synthetic"
          | .syntheticOpaque => "synOpaque"
        let rev ← try isDefEq gType curType catch _ => pure false
        let occ ← try occursCheck m curType catch _ => pure false
        let freshOk ← try
          withoutModifyingState do
            let fr ← mkFreshExprMVar (← inferType curType)
            isDefEq fr curType
        catch _ => pure false
        pure s!" [kind={k} assignable={← m.isAssignable} rev={rev} occurs={occ} freshAssign={freshOk}]"
      | _ => do
        let why ← try Mathrecord.Ho.congrFromDiffDbg curType gType
                  catch _ => pure "dbg_exception"
        pure s!" [congrDbg={why}]"
    throwError "guided conclusion mismatch {fnStr} ⟦{((toString curType).take 110).toString}⟧ vs ⟦{((toString gType).take 110).toString}⟧{extra}"
  for mv in allMvs do
    let m := mv.mvarId!
    unless ← m.isAssigned do
      let τ ← instantiateMVars (← m.getType)
      let isCls ← try pure (← Meta.isClass? τ).isSome catch _ => pure false
      if isCls && !τ.hasExprMVar then
        try m.assign (← synthInstance τ) catch _ => pure ()
  g.assign (mkAppN fn allMvs)
  let mut out : List MVarId := []
  for mv in allMvs.reverse do
    let m := mv.mvarId!
    unless ← m.isAssigned do out := m :: out
  for m in deferLeft do
    unless ← m.isAssigned do out := out ++ [m]
  pure out

/-- One guided step at goal `g` whose reference subterm is `e`: lambda ->
intro; let (elaborated `have`) -> assert; application with const/fvar head
-> guidedApply; anything else -> direct assignment of the reference term.
Target-attached auxiliaries (`T._proof_*` etc.) are delta-unfolded first,
so the constructed proof never cites them. -/
partial def guidedAct (guide : IO.Ref (Std.HashMap Name Expr))
    (env : Environment) (selfStr : String)
    (g : MVarId) (e : Expr) (assignData : Bool) (fuel : Nat := 48) :
    MetaM (List MVarId) :=
    g.withContext do
  let e := e.consumeMData
  let fn0 := e.getAppFn.consumeMData
  if let .const c lvls := fn0 then
    -- target-attached auxiliaries appear both as `T._proof_*` and in
    -- private form `_private.<Module>.0.T._proof_*`
    let s := c.toString
    let isAux := s == selfStr || s.startsWith (selfStr ++ ".") ||
      (s.startsWith "_private." &&
        (s.splitOn ("." ++ selfStr ++ ".")).length > 1)
    if isAux then
      if let some ci := env.find? c then
        if let some v := ci.value? (allowOpaque := true) then
          let v := v.instantiateLevelParams ci.levelParams lvls
          return ← guidedAct guide env selfStr g (v.beta e.getAppArgs) assignData fuel
  match e with
  | .lam _ _ b _ =>
    let (fv, g') ← g.intro1P
    guide.modify (·.insert g'.name (b.instantiate1 (mkFVar fv)))
    pure [g']
  | .letE _ t v b _ =>
    let pm ← mkFreshExprMVar t
    let g2 ← g.assert `hguided t pm
    let (fv, g3) ← g2.intro1P
    guide.modify (·.insert pm.mvarId!.name v)
    guide.modify (·.insert g3.name (b.instantiate1 (mkFVar fv)))
    pure [pm.mvarId!, g3]
  | .app .. =>
    let fn := e.getAppFn.consumeMData
    if fn.isConst || fn.isFVar then
      guidedApply guide env selfStr g e assignData fuel
    else if ← isDefEq (mkMVar g) e then pure []
    else throwError "guided direct-assign failed"
  | _ =>
    if ← isDefEq (mkMVar g) e then pure []
    else throwError "guided direct-assign failed"

/-- Fully execute the guided subtree rooted at `g`, children-first,
returning the unresolved leftover goals (open data holes). -/
partial def solveGuidedRec (guide : IO.Ref (Std.HashMap Name Expr))
    (env : Environment) (selfStr : String)
    (g : MVarId) (e : Expr) (assignData : Bool) (fuel : Nat) :
    MetaM (List MVarId) := do
  if fuel == 0 then throwError "guided descent out of fuel"
  let gs ← guidedAct guide env selfStr g e assignData fuel
  let mut leftover : List MVarId := []
  for g' in gs do
    unless ← g'.isAssigned do
      match (← guide.get).get? g'.name with
      | some r =>
        let isP ← try
          Meta.isProp (← instantiateMVars (← g'.getType))
        catch _ => pure false
        if isP then
          leftover := leftover ++
            (← solveGuidedRec guide env selfStr g' r assignData (fuel - 1))
        else if assignData then
          leftover := leftover ++ (← try oracleAssign g' r catch _ => pure [g'])
        else
          leftover := leftover ++ [g']
      | none => leftover := leftover ++ [g']
  pure leftover

end

def searchCore (env : Environment) (task : Task) (banks : String)
    (budget : Nat) (ci : ConstantInfo) (xs : Array Expr) (concl : Expr) :
    MetaM RunResult := do
  let bwCands := prepCands env task.bw
  let rwCands := prepRw env task.rw
  let simpThms ← Meta.getSimpTheorems
  let simprocs ← Simp.getSimprocs
  -- 'q': source-safe simp built ONLY from the supplied support lemmas -
  -- no global [simp] set, no simprocs
  let restricted ← if banks.contains 'q' then do
      let mut st : SimpTheorems := {}
      for c in task.bw ++ task.rw do
        try st ← st.addConst c catch _ => pure ()
      pure (some st)
    else pure none
  let root ← mkFreshExprMVar concl
  let selfStr := task.name.toString
  -- guided modes: '1' exact heads + oracle data (G1), '2' exact heads
  -- only (G2), '3' reference head as top-priority hint (G3), 'c'
  -- occurrence-specific data oracle (Condition C)
  let gmode : Char :=
    if banks.contains '1' then '1' else if banks.contains '2' then '2'
    else if banks.contains '3' then '3' else if banks.contains 'c' then 'c'
    else ' '
  let guide ← IO.mkRef ({} : Std.HashMap Name Expr)
  let gerrs ← IO.mkRef (#[] : Array String)
  if gmode != ' ' then
    if let some val := ci.value? (allowOpaque := true) then
      -- auxiliaries are unfolded THROUGHOUT the reference (heads and
      -- inside data terms alike) so no guided proof can cite them
      guide.modify (·.insert root.mvarId!.name
        (deAux env selfStr (val.beta xs)))
  -- oracle custom parts ('w'/'v'): read the reference proof ONLY here
  let (dparts, pparts) ←
    if banks.contains 'w' || banks.contains 'v' then
      collectCustomParts xs (ci.value? (allowOpaque := true))
    else pure (#[], #[])
  let goals0 := [root.mvarId!]
  let saved0 ← Meta.saveState
  let mut frontier : Array Node :=
    #[{ saved := saved0, goals := goals0, cost := 0.0, depth := 0, path := [] }]
  let mut seen : Std.HashSet String := {}
  let mut calls := 0
  let mut stats : Stats := {}

  while calls < budget && frontier.size > 0 do
    -- pop min priority (swap-with-last then pop; Node has no Inhabited)
    let prio := fun (n : Node) => n.cost + 0.5 * Float.ofNat n.goals.length
    let mut best := 0
    for i in [1:frontier.size] do
      match frontier[i]?, frontier[best]? with
      | some a, some b => if prio a < prio b then best := i
      | _, _ => pure ()
    let some node := frontier[best]? | break
    match frontier.back? with
    | some last => frontier := (frontier.set! best last).pop
    | none => frontier := frontier.pop
    node.saved.restore
    -- goals whose metavariable was already assigned through coupling
    -- (sibling solving, conclusion unification) are closed; drop them
    let mut live : List MVarId := []
    for gg in node.goals do
      let dead ← try
        pure ((← gg.isAssigned) || (← gg.isDelayedAssigned))
      catch _ => pure false
      if !dead then live := live ++ [gg]
    if live.isEmpty then
      -- candidate success: verify, then enforce source-cleanliness -
      -- a proof citing the target, its derived auxiliaries, or forbidden
      -- own-module facts is REJECTED and the search continues (dirty
      -- proofs must not shadow clean ones)
      let proof ← mkLambdaFVars xs (← instantiateMVars root)
      let ok ← try
        Meta.check proof
        isDefEq (← inferType proof) ci.type
      catch _ => pure false
      let usedNames := proof.getUsedConstantsAsSet.toArray
      let forbidSet : Std.HashSet Name :=
        task.forbid.foldl (init := {}) (·.insert ·)
      let ownIdx := (env.getModuleIdxFor? task.name).map (·.toNat)
      let allowedMod := match ownIdx with
        | some o => allowedModules env o
        | none => #[]
      let dirty := usedNames.any fun c =>
        c == task.name || (c.toString).startsWith (selfStr ++ ".") ||
        forbidSet.contains c ||
        (match ownIdx, env.getModuleIdxFor? c with
         | some o, some m =>
           m.toNat != o && !((allowedMod[m.toNat]?).getD true)
         | _, _ => false)
      if ok && !dirty then
        return { solved := true, verified := ok, path := node.path.reverse,
                 callsUsed := calls, stats, frontierLeft := frontier.size,
                 usedConsts := usedNames.map toString,
                 goalHeads := node.heads.reverse,
                 partsData := dparts.map (fun e => ((toString e).take 300).toString),
                 partsProp := pparts.map (fun e => ((toString e).take 300).toString),
                 guidedErrs := ← gerrs.get }
      stats := { stats with attempts := bump stats.attempts "dirty_rejected" }
      continue
    stats := { stats with expansions := stats.expansions + 1 }
    -- goal selection: with 'g', expand the syntactically smallest goal
    -- (later goals can be easy or instantiate shared metavariables)
    let (g, rest) ← do
      let arr0 := live.toArray
      if gmode == '2' then
        -- exact-head rung without a data oracle: expand PROOF goals
        -- first, so metavariable coupling can determine the data holes
        let mut pidx : Option Nat := none
        for i in [0:arr0.size] do
          if pidx.isNone then
            let isP ← try
              Meta.isProp (← instantiateMVars (← arr0[i]!.getType))
            catch _ => pure true
            if isP then pidx := some i
        let sel := pidx.getD 0
        let rest := (List.range arr0.size).filterMap
          (fun i => if i == sel then none else arr0[i]?)
        pure (arr0[sel]!, rest)
      else do
      -- FIRST-CLASS DATA HOLES: non-proof goals are fabrication holes;
      -- resolve them first - they are cheap and unlock proof goals
      let mut dataIdx : Option Nat := none
      for i in [0:arr0.size] do
        if dataIdx.isNone then
          let isP ← try
            Meta.isProp (← instantiateMVars (← arr0[i]!.getType))
          catch _ => pure true
          if !isP then dataIdx := some i
      if let some di := dataIdx then
        let rest := (List.range arr0.size).filterMap
          (fun i => if i == di then none else arr0[i]?)
        pure (arr0[di]!, rest)
      else if banks.contains 'g' && arr0.size > 1 then
        let mut bi := 0
        let mut bsz := 1000000
        for i in [0:arr0.size] do
          let sz ← try
            pure (toString (← instantiateMVars (← arr0[i]!.getType))).length
          catch _ => pure 1000000
          if sz < bsz then
            bsz := sz
            bi := i
        let rest := (List.range arr0.size).filterMap
          (fun i => if i == bi then none else arr0[i]?)
        pure (arr0[bi]!, rest)
      else
        pure (arr0[0]!, arr0.toList.tail)
    let ghead ← try goalHead g catch _ => pure "?"
    let gIsProp ← try
      Meta.isProp (← instantiateMVars (← g.getType))
    catch _ => pure true
    let gconsts ← try
      pure (← instantiateMVars (← g.getType)).getUsedConstantsAsSet
    catch _ => pure default
    -- guided modes: the reference subterm tracked for this goal, if any
    let gEntry : Option Expr ←
      if gmode == ' ' then pure none
      else do pure ((← guide.get).get? g.name)

    -- assemble the action list for this goal
    let mut acts : Array (String × String × Float × Attempt) := #[]  -- (bank, label, cost, act)
    if banks.contains 's' then
      acts := acts.push ("structural", "intro", 0.3,
        do let (fv, g') ← g.intro1P
           if gmode == 'c' then
             if let some e := gEntry then
               if let .lam _ _ b _ := e.consumeMData then
                 guide.modify (·.insert g'.name (b.instantiate1 (mkFVar fv)))
           pure [g'])
      acts := acts.push ("structural", "assumption", 0.2,
        do if ← g.assumptionCore then pure []
           else throwError "no assumption")
      if ghead == "Eq" || ghead == "HEq" then
        acts := acts.push ("structural", "rfl", 0.2,
          do g.applyConst ``rfl)
      if ghead == "Iff" then
        acts := acts.push ("structural", "iff_rfl", 0.2,
          do g.applyConst ``Iff.rfl)
      if ghead == "Eq" || ghead == "HEq" || ghead == "Iff" then
        -- mechanical congruence step (core congrN): decomposes f a = f b
        -- style goals the way `congr 1` does
        acts := acts.push ("structural", "congr1", 0.7,
          g.congrN 1 (closePre := true) (closePost := false))
      -- constructors of the goal-head inductive (small arity only)
      match env.find? (String.toName ghead) with
      | some (.inductInfo iv) =>
        if gIsProp && iv.ctors.length ≤ 4 then
          for ctor in iv.ctors do
            let guidedCtor := gmode == 'c' &&
              (match gEntry with
               | some e =>
                 e.consumeMData.getAppFn.consumeMData.constName? == some ctor
               | none => false)
            if guidedCtor then
              acts := acts.push ("structural", s!"ctor {ctor} (guided)", 0.5,
                guidedApply guide env selfStr g ((gEntry.getD default).consumeMData) false)
            else
              acts := acts.push ("structural", s!"ctor {ctor}", 0.5,
                do g.applyConst ctor)
      | _ => pure ()
    if banks.contains 'h' then
      -- head refinement with local hypotheses: apply any hypothesis, with
      -- argument holes (assumption covers only the zero-argument case)
      let decls ← try
        g.withContext do
          pure ((← getLCtx).decls.toList.filterMap id
            |>.filter (fun d => !d.isImplementationDetail))
      catch _ => pure []
      for d in decls do
        let guidedHyp := gmode == 'c' &&
          (match gEntry with
           | some e => e.consumeMData.getAppFn.consumeMData == mkFVar d.fvarId
           | none => false)
        if guidedHyp then
          acts := acts.push ("hyp", s!"apply hyp {d.userName} (guided)", 0.6,
            guidedApply guide env selfStr g ((gEntry.getD default).consumeMData) false)
        else
          acts := acts.push ("hyp", s!"apply hyp {d.userName}", 0.6,
            do g.apply (mkFVar d.fvarId))
    if banks.contains 'b' && gIsProp then
      let small := bwCands.size ≤ 48   -- oracle supports: try everything
      let mut nb := 0
      for c in bwCands do
        if nb < 50 && (small || c.concl == ghead) &&
           c.name.toString != task.name.toString then
          nb := nb + 1
          let guidedHead := gmode == 'c' &&
            (match gEntry with
             | some e =>
               e.consumeMData.getAppFn.consumeMData.constName? == some c.name
             | none => false)
          if guidedHead then
            -- Condition C: the same head the free search would try, but
            -- applied through guidedApply so its argument holes acquire
            -- occurrence-specific reference terms (same cost, same slot)
            acts := acts.push ("backward", s!"apply {c.name} (guided)", 1.0,
              guidedApply guide env selfStr g ((gEntry.getD default).consumeMData) false)
          else
            acts := acts.push ("backward", s!"apply {c.name}", 1.0,
              hoApply g c.name)
    if banks.contains 'r' && gIsProp then
      -- rewrite v2: forward (simp) orientation only, tight cap - the v1
      -- bidirectional bank was measured net-negative at fixed budget
      let mut nr := 0
      for c in rwCands do
        if nr < 15 && c.name.toString != task.name.toString then
          if gconsts.contains (String.toName c.lhs) then
            nr := nr + 1
            acts := acts.push ("rewrite", s!"rw {c.name}", 1.2, do
              let r ← g.rewrite (← g.getType)
                        (← mkConstWithFreshMVarLevels c.name) false
              let g' ← g.replaceTargetEq r.eNew r.eqProof
              pure (g' :: r.mvarIds))
    if banks.contains 'p' && gIsProp then
      acts := acts.push ("automation", "simp", 1.5, do
        let ctx ← Simp.mkContext (simpTheorems := #[simpThms])
                    (congrTheorems := ← Meta.getSimpCongrTheorems)
        let (res, _) ← simpGoal g ctx (simprocs := #[simprocs])
        match res with
        | none => pure []
        | some (_, g') => pure [g'])
    if banks.contains 'w' && !gIsProp then
      -- oracle data parts offered ONLY at fabrication holes
      for i in [0:dparts.size] do
        let p := dparts[i]!
        acts := acts.push ("part", s!"part {i}", 0.8,
          do if ← isDefEq (mkMVar g) p then pure []
             else throwError "part mismatch")
    if banks.contains 'v' then
      -- oracle intermediate propositions: assert as a `have`
      for i in [0:pparts.size] do
        let p := pparts[i]!
        acts := acts.push ("have", s!"have {i}", 0.9, do
          let pm ← mkFreshExprMVar p
          let g2 ← g.assert (Name.mkSimple s!"hp{i}") p pm
          let (_, g3) ← g2.intro1P
          pure [pm.mvarId!, g3])
    match restricted with
    | some st =>
      acts := acts.push ("automation", "simp_restricted", 1.2, do
        let ctx ← Simp.mkContext (simpTheorems := #[st])
                    (congrTheorems := ← Meta.getSimpCongrTheorems)
        let (res, _) ← simpGoal g ctx (simprocs := #[])
        match res with
        | none => pure []
        | some (_, g') => pure [g'])
    | none => pure ()
    -- guided-mode actions
    if let some e := gEntry then
      let logged (assignData : Bool) : Attempt := do
        try guidedAct guide env selfStr g e assignData
        catch ex =>
          let msg ← try ex.toMessageData.toString catch _ => pure "?"
          gerrs.modify (fun a =>
            if a.size < 24 then a.push s!"{ghead}: {(msg.take 340).toString}" else a)
          throw ex
      if gmode == '1' then
        if gIsProp then
          acts := #[("guided", "guided", 0.1, logged true)]
        else
          acts := #[("guided", "oracle_data", 0.1, oracleAssign g e)]
      else if gmode == '2' then
        if gIsProp then
          -- 'f': keep bank actions (e.g. simp) as FALLBACK when the exact
          -- head is not mechanically executable - tests whether the
          -- residual gap is simp-certificate reconstruction fragility
          if banks.contains 'f' then
            acts := #[(("guided", "guided", 0.1, logged false) :
              String × String × Float × Attempt)] ++ acts
          else
            acts := #[("guided", "guided", 0.1, logged false)]
        else if banks.contains 'o' then
          -- G2a: mechanical synthesis first-class, oracle only for the
          -- RESIDUAL data holes that survive it
          acts := #[("guided", "oracle_data", 0.1, oracleAssign g e)]
      else if gmode == '3' then
        if gIsProp then
          -- PREPEND: the guided child must claim the duplicate-state key
          -- before the plain backward child of the same head does, or the
          -- correspondence registrations are discarded with it
          acts := #[(("guided", "guided_pri", 0.05,
            guidedAct guide env selfStr g e false) :
              String × String × Float × Attempt)] ++ acts
      else if gmode == 'c' then
        if !gIsProp then
          acts := #[(("guided", "oracle_data", 0.05,
            oracleAssign g e) : String × String × Float × Attempt)] ++ acts

    -- guided-exact diagnostics: a node dying with no action is a
    -- correspondence loss - record where and what kind of goal
    if (gmode == '1' || gmode == '2') && acts.isEmpty then
      let kind := if gIsProp then "P" else "D"
      let hasE := if gEntry.isSome then "entry" else "noentry"
      stats := { stats with
        attempts := bump stats.attempts s!"dead_{kind}_{hasE}_{ghead}" }

    -- execute attempts
    for (bank, label, acost, act) in acts do
      if calls ≥ budget then break
      calls := calls + 1
      stats := { stats with attempts := bump stats.attempts bank }
      node.saved.restore
      match ← tryAct act with
      | none => pure ()
      | some newGoals =>
        stats := { stats with legal := bump stats.legal bank }
        let goals' := newGoals ++ rest
        let key ← try stateKey goals' catch _ => pure s!"?{calls}"
        -- guided children carry correspondence registrations and may
        -- legitimately re-render an earlier state key (id / Eq.mpr-style
        -- steps); suppressing them kills the branch-factor-1 rungs
        let guidedChild := bank == "guided" || label.endsWith "(guided)"
        if seen.contains key && !guidedChild then
          stats := { stats with dups := stats.dups + 1 }
        else
          seen := seen.insert key
          let childSaved ← Meta.saveState
          frontier := frontier.push
            { saved := childSaved, goals := goals',
              cost := node.cost + acost, depth := node.depth + 1,
              path := label :: node.path, heads := ghead :: node.heads }
  return { solved := false, callsUsed := calls, stats,
           frontierLeft := frontier.size,
           partsData := dparts.map (fun e => ((toString e).take 300).toString),
           partsProp := pparts.map (fun e => ((toString e).take 300).toString),
           guidedErrs := ← gerrs.get }

def search (env : Environment) (task : Task) (banks : String) (budget : Nat) :
    MetaM RunResult := do
  let some ci := env.find? task.name | return {}
  Meta.forallTelescope ci.type fun xs concl =>
    searchCore env task banks budget ci xs concl

/-- Diagnostic: run custom-part extraction for comma-separated theorem
names and print counts plus samples. -/
def partsDiag (path : System.FilePath) (namesArg : String) : IO Unit := do
  let pf ← Mathrecord.processFile path Mathrecord.Study.mathlibOptions
  let env := pf.env
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  for nm in (namesArg.splitOn ",") do
    let n := String.toName nm.trim
    let act : MetaM Unit := do
      let some ci := env.find? n | IO.println s!"{nm}: NOT FOUND"
      Meta.forallTelescope ci.type fun xs _ => do
        let (d, p) ← collectCustomParts xs (ci.value? (allowOpaque := true))
        IO.println s!"{nm}: data={d.size} props={p.size} hasVal={(ci.value?).isSome} tele={xs.size}"
        for e in d do IO.println s!"  DATA: {((toString e).take 160).toString}"
        for e in p do IO.println s!"  PROP: {((toString e).take 160).toString}"
    let _ ← (act.run' {} {}).toIO coreCtx { env }

/-- Standalone reproduction of the G2 congrArg-vs-flex-goal unification
refusal: telescope congrArg's real type, unify its conclusion with a bare
Sort-mvar goal, print each stage. -/
def hoDiag (path : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path Mathrecord.Study.mathlibOptions
  let env := pf.env
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let act : MetaM Unit := do
    let ce ← mkConstWithFreshMVarLevels ``congrArg
    let hType ← inferType ce
    let (mvs, _, concl) ← forallMetaBoundedTelescope hType 6
    IO.println s!"telescope: {mvs.size} mvars, concl={← instantiateMVars concl}"
    let u ← mkFreshLevelMVar
    let gT ← mkFreshExprMVar (mkSort u)
    IO.println s!"goal type: {gT} : Sort {u}"
    let r1 ← isDefEq concl gT
    IO.println s!"isDefEq concl gT = {r1}"
    unless r1 do
      let r2 ← isDefEq gT concl
      IO.println s!"reversed: isDefEq gT concl = {r2}"
      let ct ← inferType concl
      IO.println s!"type of concl: {ct}"
      let r3 ← isDefEq (mkSort u) ct
      IO.println s!"sort unify: {r3}"
    -- variant: goal type created BEFORE the telescope (parent-first order,
    -- as in the real search)
    let u2 ← mkFreshLevelMVar
    let gT2 ← mkFreshExprMVar (mkSort u2)
    let ce2 ← mkConstWithFreshMVarLevels ``congrArg
    let (_, _, concl2) ← forallMetaBoundedTelescope (← inferType ce2) 6
    IO.println s!"parent-first: isDefEq concl2 gT2 = {← isDefEq concl2 gT2}"
  let _ ← (act.run' {} {}).toIO coreCtx { env }

def statsJson (s : Stats) : Json :=
  Json.mkObj [
    ("attempts", Json.mkObj (s.attempts.toList.map fun (k, v) => (k, toJson v))),
    ("legal", Json.mkObj (s.legal.toList.map fun (k, v) => (k, toJson v))),
    ("dups", toJson s.dups),
    ("expansions", toJson s.expansions)]

def prove (path : System.FilePath) (inp : System.FilePath)
    (out : System.FilePath) (banks : String) (budget : Nat) : IO Unit := do
  let pf ← Mathrecord.processFile path Mathrecord.Study.mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules; banks={banks} budget={budget}"
  let raw ← IO.FS.readFile inp
  let j ← IO.ofExcept (Json.parse raw)
  let tasks ← IO.ofExcept (parseTasks j)
  IO.println s!"{tasks.size} theorems to attempt"
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let mut solvedN := 0
  let mut count := 0
  for task in tasks do
    let act : MetaM RunResult := search env task banks budget
    let res ← try
      let (r, _) ← (act.run' {} {}).toIO coreCtx { env }
      pure r
    catch _ => pure {}
    if res.solved then solvedN := solvedN + 1
    let row := Json.mkObj [
      ("n", Json.str (toString task.name)),
      ("solved", toJson res.solved),
      ("verified", toJson res.verified),
      ("calls", toJson res.callsUsed),
      ("path", Json.arr (res.path.toArray.map Json.str)),
      ("frontier_left", toJson res.frontierLeft),
      ("used_consts", Json.arr (res.usedConsts.map Json.str)),
      ("goal_heads", Json.arr (res.goalHeads.toArray.map Json.str)),
      ("parts_data", Json.arr (res.partsData.map Json.str)),
      ("parts_prop", Json.arr (res.partsProp.map Json.str)),
      ("guided_errors", Json.arr (res.guidedErrs.map Json.str)),
      ("stats", statsJson res.stats)]
    h.putStrLn row.compress
    count := count + 1
    if count % 10 == 0 then
      IO.println s!"  {count}/{tasks.size} attempted, {solvedN} solved"
      h.flush
  IO.println s!"done: {solvedN}/{tasks.size} solved"
  h.flush

end Mathrecord.Prover
