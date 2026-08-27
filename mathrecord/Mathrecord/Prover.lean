import Mathrecord.HeadDump

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

/-- Canonical-ish key for a state: sorted rendered goal types. -/
def stateKey (goals : List MVarId) : MetaM String := do
  let mut parts : Array String := #[]
  for g in goals do
    let t ← instantiateMVars (← g.getType)
    parts := parts.push (toString t)
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
    if node.goals.isEmpty then
      -- candidate success: verify, then enforce source-cleanliness -
      -- a proof citing the target, its derived auxiliaries, or forbidden
      -- own-module facts is REJECTED and the search continues (dirty
      -- proofs must not shadow clean ones)
      node.saved.restore
      let proof ← mkLambdaFVars xs (← instantiateMVars root)
      let ok ← try
        Meta.check proof
        isDefEq (← inferType proof) ci.type
      catch _ => pure false
      let usedNames := proof.getUsedConstantsAsSet.toArray
      let selfStr := task.name.toString
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
                 partsProp := pparts.map (fun e => ((toString e).take 300).toString) }
      stats := { stats with attempts := bump stats.attempts "dirty_rejected" }
      continue
    stats := { stats with expansions := stats.expansions + 1 }
    node.saved.restore
    -- goal selection: with 'g', expand the syntactically smallest goal
    -- (later goals can be easy or instantiate shared metavariables)
    let (g, rest) ← do
      -- FIRST-CLASS DATA HOLES: non-proof goals are fabrication holes;
      -- resolve them first - they are cheap and unlock proof goals
      let arr0 := node.goals.toArray
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
      else if banks.contains 'g' && node.goals.length > 1 then
        let arr := node.goals.toArray
        let mut bi := 0
        let mut bsz := 1000000
        for i in [0:arr.size] do
          let sz ← try
            pure (toString (← instantiateMVars (← arr[i]!.getType))).length
          catch _ => pure 1000000
          if sz < bsz then
            bsz := sz
            bi := i
        let rest := (List.range arr.size).filterMap
          (fun i => if i == bi then none else arr[i]?)
        pure (arr[bi]!, rest)
      else
        pure (node.goals.head!, node.goals.tail!)
    let ghead ← try goalHead g catch _ => pure "?"
    let gIsProp ← try
      Meta.isProp (← instantiateMVars (← g.getType))
    catch _ => pure true
    let gconsts ← try
      pure (← instantiateMVars (← g.getType)).getUsedConstantsAsSet
    catch _ => pure default

    -- assemble the action list for this goal
    let mut acts : Array (String × String × Float × Attempt) := #[]  -- (bank, label, cost, act)
    if banks.contains 's' then
      acts := acts.push ("structural", "intro", 0.3,
        do let (_, g') ← g.intro1P; pure [g'])
      acts := acts.push ("structural", "assumption", 0.2,
        do if ← g.assumptionCore then pure []
           else throwError "no assumption")
      if ghead == "Eq" || ghead == "HEq" then
        acts := acts.push ("structural", "rfl", 0.2,
          do g.applyConst ``rfl)
      if ghead == "Iff" then
        acts := acts.push ("structural", "iff_rfl", 0.2,
          do g.applyConst ``Iff.rfl)
      -- constructors of the goal-head inductive (small arity only)
      match env.find? (String.toName ghead) with
      | some (.inductInfo iv) =>
        if gIsProp && iv.ctors.length ≤ 4 then
          for ctor in iv.ctors do
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
        acts := acts.push ("hyp", s!"apply hyp {d.userName}", 0.6,
          do g.apply (mkFVar d.fvarId))
    if banks.contains 'b' && gIsProp then
      let small := bwCands.size ≤ 48   -- oracle supports: try everything
      let mut nb := 0
      for c in bwCands do
        if nb < 50 && (small || c.concl == ghead) &&
           c.name.toString != task.name.toString then
          nb := nb + 1
          acts := acts.push ("backward", s!"apply {c.name}", 1.0,
            do g.apply (← mkConstWithFreshMVarLevels c.name))
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
        if seen.contains key then
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
           partsProp := pparts.map (fun e => ((toString e).take 300).toString) }

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
      ("stats", statsJson res.stats)]
    h.putStrLn row.compress
    count := count + 1
    if count % 10 == 0 then
      IO.println s!"  {count}/{tasks.size} attempted, {solvedN} solved"
      h.flush
  IO.println s!"done: {solvedN}/{tasks.size} solved"
  h.flush

end Mathrecord.Prover
