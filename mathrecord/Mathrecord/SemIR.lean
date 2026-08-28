import Mathrecord.Semantic
import Mathrecord.Ho

/-! Semantic IR v1: a serializable, executable action language, and the
deterministic SEMANTIC REPLAY harness over it.

## Why this module exists

`Semantic.lean` gives certificate-region compression, but its semantic
action is never reified: `Prover.searchCore` computes it live from the
reference subterm at each guided node (`certRegionRoot e` ->
`semSimpAct guide g e`), inside a budgeted best-first search.  Two
consequences:

  * there is no semantic action SEQUENCE to execute, only a reference proof
    term consulted at execution time;
  * a gate failure surfaces as a dead frontier or an exhausted budget, not
    as a named defect of a named action.

This module reifies the action and separates the two questions:

  EXTRACTION  - is there an IR v1 parameterization of this reference step?
                Parameters that the reference term does not state outright
                (fact orientation, continuation ownership) are determined
                by BOUNDED TRIAL against the live goal and RECORDED.
                Failure here = the action language is not expressive
                enough, localized to one action, with a reason.

  REPLAY      - does the recorded IR reproduce the proof?  Executes the
                recorded parameters ONCE, in order, with no search, no
                budget, no ranker, no retry, and - critically - no access
                to the reference term.  Failure here = an executor defect.

An action that cannot be parameterized is classified as an unsupported
semantic family (`Family.unsupported` + reason), never hidden behind a
certificate-grain fallback.

## What v1 promotes out of `semSimpAct`

Every retry and silent closer inside `Semantic.semSimpAct` is a missing IR
field in disguise.  v1 makes all four explicit:

  forward-set -> inverted-set -> mixed retry   ==>  per-fact `inverted`
  `for c in conts do isDefEq g'T cT` scan      ==>  `contIdx`
  `try g'.refl`                                ==>  `Family.exact` (rfl)
  `if <- g'.assumptionCore`                    ==>  `Family.exact` (hyp)

## v1 boundary (documented, not hidden)

`FactRef.inst` and `HeadRef.term` carry `Expr` payloads, so the IR is
executable in-process and JSON-renderable but not yet JSON-ROUND-TRIPPABLE
(a faithful `Expr` decoder is separate work; `Extract.encodeExpr` is the
encoder half).  The no-reference-consultation guarantee is enforced
structurally instead: `execNode` receives an `IRNode` and has no parameter
through which the reference term could reach it.
-/

namespace Mathrecord.SemIR

open Lean Meta Mathrecord

/-! ## Families

Small, fixed, MECHANISM-defined.  No family is keyed on a declaration name
or a certificate name. -/

inductive Family where
  | intro            -- lambda: introduce binders
  | apply            -- application of a const/fvar head, proof children
  | exact            -- terminal: hypothesis, constant, rfl
  | ctor             -- application of an inductive constructor
  | cases            -- eliminator of a NON-recursive inductive
  | induct           -- eliminator of a RECURSIVE inductive
  | rewrite          -- certificate region executed as one rewrite action
  | have_            -- let / elaborated `have`: prove a stated Prop, then use it
  | change           -- definitional reduction only: goal changes, proof does not
  | unsupported      -- no IR v1 parameterization; carries a reason
  deriving Inhabited, BEq

def Family.toStr : Family → String
  | .intro => "INTRO"   | .apply => "APPLY"   | .exact => "EXACT"
  | .ctor  => "CONSTRUCTOR" | .cases => "CASES" | .induct => "INDUCT"
  | .rewrite => "REWRITE" | .have_ => "HAVE"  | .change => "CHANGE"
  | .unsupported => "UNSUPPORTED"

/-! ## Eliminator classification without name matching

`Semantic.elimFamily` classifies by string suffix (`.casesOn`, `.rec`,
`.recOn`, `.ndrec`, `.elim`) and collapses CASES and INDUCT.  Instead:
delta-unfold the head until it lands on a `recInfo` constant, then split on
the inductive's `isRec`. -/

/-- Head constant of a term's body, after peeling lambdas. -/
partial def headConstOfBody (e : Expr) : Option Name :=
  match e.consumeMData with
  | .lam _ _ b _ => headConstOfBody b
  | e' => match e'.getAppFn.consumeMData with
          | .const c _ => some c
          | _ => none

/-- Does `c` denote an eliminator, and is its inductive recursive?
`none` = not an eliminator.  `some true` = recursive (INDUCT).
`some false` = non-recursive (CASES). -/
partial def elimRecursive? (env : Environment) (c : Name) (fuel : Nat := 6) :
    Option Bool :=
  if fuel == 0 then none else
  match env.find? c with
  | some (.recInfo v) =>
    match v.all.head? with
    | some t => match env.find? t with
                | some (.inductInfo iv) => some iv.isRec
                | _ => some false
    | none => some false
  | some ci =>
    -- `casesOn`/`recOn`/`ndrec` are definitions that unfold to `.rec`
    match ci.value? (allowOpaque := true) with
    | some v => match headConstOfBody v with
                | some c' => if c' == c then none else elimRecursive? env c' (fuel - 1)
                | none => none
    | none => none
  | none => none

/-! ## Parameters -/

/-- How a rewrite fact is named.  `cnst` and `hyp` are re-instantiated by
the simplifier; `inst` is an already-instantiated proof term. -/
inductive FactRef where
  | cnst (n : Name)
  | hyp  (idx : Nat) (user : Name)
  | inst (e : Expr)
  deriving Inhabited

def FactRef.render : FactRef → String
  | .cnst n => s!"const:{n}"
  | .hyp i u => s!"hyp:{i}:{u}"
  | .inst _ => "inst"

/-- A rewrite fact with its recorded ORIENTATION.  `inverted` is the field
promoted out of `semSimpAct`'s forward/backward retry. -/
structure Fact where
  ref      : FactRef
  inverted : Bool := false
  /-- `true`: single-pass `rw`-style application (kabstract all current
  occurrences ONCE, no re-iteration) - required for instance-bridge
  equations, which self-loop under simp's keyed matching.  `false`:
  iterated simp-only rewriting.  Recorded per step in ordered mode. -/
  rw       : Bool := false
  deriving Inhabited

/-- Where a rewrite acts. v1 records goal vs a named hypothesis; occurrence
selection is NOT a v1 field (see `unsupported` reasons - it is added only
if replay shows a repeated occurrence-ambiguity class). -/
inductive Loc where
  | goal
  | hyp (idx : Nat) (user : Name)
  deriving Inhabited

def Loc.render : Loc → String
  | .goal => "goal"
  | .hyp i u => s!"hyp:{i}:{u}"

/-- Head of an APPLY/CONSTRUCTOR/CASES/INDUCT action. -/
inductive HeadRef where
  | cnst (n : Name)
  | hyp  (idx : Nat) (user : Name)
  deriving Inhabited

def HeadRef.render : HeadRef → String
  | .cnst n => s!"const:{n}"
  | .hyp i u => s!"hyp:{i}:{u}"

/-- Terminal EXACT forms - the promoted silent closers. -/
inductive ExactKind where
  | hypothesis (idx : Nat) (user : Name)
  | constant (n : Name)
  | rfl
  deriving Inhabited

def ExactKind.render : ExactKind → String
  | .hypothesis i u => s!"hyp:{i}:{u}"
  | .constant n => s!"const:{n}"
  | .rfl => "rfl"

/-! ## The action -/

/-- One semantic action plus the actions for the subgoals it produces.
`kids` is POSITIONAL: `kids[i]` is the action for the i-th subgoal the
executor returns.  A size mismatch is a named replay discrepancy
(`arity`), never silently absorbed. -/
structure IRNode where
  fam     : Family
  -- INTRO
  nIntro  : Nat := 0
  -- APPLY / CONSTRUCTOR / CASES / INDUCT
  head?   : Option HeadRef := none
  /-- Total argument count of the head.  RECORDED, not derived: a proof
  argument that unification closes appears in neither `dataArgs` nor
  `kids`, so deriving the arity truncates the telescope and produces a
  different conclusion. -/
  nArgs   : Nat := 0
  /-- Data (non-proof) arguments the reference supplies. Recorded as terms
  because v1 does not yet fabricate; replay consuming reference data is
  reported separately. -/
  dataArgs : Array (Nat × Expr) := #[]
  -- REWRITE
  facts   : Array Fact := #[]
  /-- `false`: one simultaneous `simp only` with the whole fact set.
  `true`: the facts are applied ONE AT A TIME in the recorded order - the
  certificate was an `Eq.trans` CHAIN whose steps ping-pong as a set
  (e.g. the same rewrite at two instance paths).  This is the
  ordering/mode field of the rewrite IR, determined at extraction. -/
  ordered : Bool := false
  loc     : Loc := .goal
  /-- Which region continuation owns the residual goal, promoted out of the
  `isDefEq` scan. `none` = the action closes the goal outright. -/
  contIdx : Option Nat := none
  -- EXACT
  exact?  : Option ExactKind := none
  -- HAVE
  haveTy? : Option Expr := none
  -- UNSUPPORTED
  reason  : String := ""
  -- structure
  kids    : Array IRNode := #[]
  /-- certificate nodes this one action covers (compression numerator). -/
  covers  : Nat := 1
  deriving Inhabited

partial def IRNode.size (n : IRNode) : Nat :=
  n.kids.foldl (fun acc k => acc + k.size) 1

partial def IRNode.covered (n : IRNode) : Nat :=
  n.kids.foldl (fun acc k => acc + k.covered) n.covers

partial def IRNode.horizon (n : IRNode) : Nat :=
  1 + n.kids.foldl (fun acc k => Nat.max acc k.horizon) 0

/-- Families present in the subtree, with counts. -/
partial def IRNode.tally (n : IRNode) (m : Std.HashMap String Nat := {}) :
    Std.HashMap String Nat :=
  let k := n.fam.toStr
  let m := m.insert k ((m.getD k 0) + 1)
  n.kids.foldl (fun acc c => c.tally acc) m

partial def IRNode.unsupportedReasons (n : IRNode) : Array String :=
  let here := if n.fam == .unsupported then #[n.reason] else #[]
  n.kids.foldl (fun acc k => acc ++ k.unsupportedReasons) here

partial def IRNode.toJson (n : IRNode) : Json :=
  let base : List (String × Json) :=
    [("f", Json.str n.fam.toStr), ("cov", Lean.toJson n.covers)]
  let base := base ++ (match n.head? with
    | some h => [("head", Json.str h.render)] | none => [])
  let base := base ++ (if n.nIntro > 0 then [("nintro", Lean.toJson n.nIntro)] else [])
  let base := base ++ (if n.facts.isEmpty then [] else
    [("facts", Json.arr (n.facts.map fun f =>
       Json.mkObj [("r", Json.str f.ref.render), ("inv", Lean.toJson f.inverted),
                   ("rw", Lean.toJson f.rw)])),
     ("ord", Lean.toJson n.ordered),
     ("loc", Json.str n.loc.render),
     ("cont", match n.contIdx with
        | some i => Lean.toJson i | none => Json.null)])
  let base := base ++ (match n.exact? with
    | some k => [("exact", Json.str k.render)] | none => [])
  let base := base ++ (if n.dataArgs.isEmpty then [] else
    [("ndata", Lean.toJson n.dataArgs.size)])
  let base := base ++ (if n.reason == "" then [] else [("why", Json.str n.reason)])
  let base := base ++ (if n.kids.isEmpty then [] else
    [("kids", Json.arr (n.kids.map IRNode.toJson))])
  Json.mkObj base

/-! ## Local-context references

A hypothesis is recorded by its INDEX in the goal's local context plus its
user name; resolution checks both, so a context that has drifted is a named
discrepancy rather than a silent wrong-hypothesis pick. -/

def lctxIndexOf (g : MVarId) (f : FVarId) : MetaM (Option (Nat × Name)) :=
  g.withContext do
    let lctx ← getLCtx
    let mut i := 0
    for d in lctx do
      if !d.isImplementationDetail then
        if d.fvarId == f then return some (i, d.userName)
        i := i + 1
    return none

def resolveHyp (g : MVarId) (idx : Nat) (user : Name) :
    MetaM (Option FVarId) := g.withContext do
  let lctx ← getLCtx
  let mut i := 0
  for d in lctx do
    if !d.isImplementationDetail then
      if i == idx then
        return if d.userName == user then some d.fvarId else none
      i := i + 1
  return none


/-- The goal's local-context free variables, in context order.  Recorded
terms are ABSTRACTED over this array and re-instantiated against the replay
goal's array: the intro'd fvars of the extraction run do not exist in the
replay run, so a raw term would reference an unknown free variable. -/
def lctxFVars (g : MVarId) : MetaM (Array Expr) := g.withContext do
  let lctx ← getLCtx
  let mut out : Array Expr := #[]
  for d in lctx do
    out := out.push (mkFVar d.fvarId)
  pure out

/-- Record a term relative to the goal's local context. -/
def absLocal (g : MVarId) (e : Expr) : MetaM Expr := do
  pure (e.abstract (← lctxFVars g))

/-- Re-instantiate a recorded term against the replay goal's context. -/
def instLocal (g : MVarId) (e : Expr) : MetaM Expr := do
  pure (e.instantiateRev (← lctxFVars g))

/-! ## Execution

The executor sees an `IRNode` and a goal.  It has NO parameter through
which the reference proof term could reach it, and it performs no retry:
one recorded parameterization, executed once.  Any failure throws with a
named reason that becomes the replay discrepancy class. -/

/-- Build the simp theorem set from recorded facts, honouring each fact's
recorded orientation.  No forward/backward retry: `inverted` is data. -/
def buildFactSet (g : MVarId) (facts : Array Fact) : MetaM SimpTheorems :=
  g.withContext do
    let mut thms : SimpTheorems := {}
    let mut i := 0
    for f in facts do
      match f.ref with
      | .cnst c => thms ← thms.addConst c (inv := f.inverted)
      | .hyp idx user =>
        let some fv ← resolveHyp g idx user
          | throwError "irfact: hypothesis {idx}/{user} not in context"
        if f.inverted then
          let t ← Meta.mkEqSymm (mkFVar fv)
          thms ← thms.add (.other (Name.mkSimple s!"irfact{i}")) #[] t
        else
          thms ← thms.add (.fvar fv) #[] (mkFVar fv)
      | .inst e0 =>
        let e := e0.instantiateRev (← lctxFVars g)
        -- an HEq-typed fact is not a rewrite rule; when its endpoints'
        -- types agree it converts to Eq (generic `eq_of_heq`, no name cases)
        let e ← do
          let τ ← inferType e
          if τ.getForallBody.consumeMData.getAppFn.consumeMData matches
              .const ``HEq _ then
            try Meta.mkEqOfHEq e catch _ => pure e
          else pure e
        let t ← if f.inverted then Meta.mkEqSymm e else pure e
        thms ← thms.add (.other (Name.mkSimple s!"irfact{i}")) #[] t
      i := i + 1
    pure thms

/-- Proof term of a recorded fact, in the goal's context. -/
def factProof (g : MVarId) (r : FactRef) : MetaM Expr := g.withContext do
  match r with
  | .cnst c => mkConstWithFreshMVarLevels c
  | .hyp idx user => do
    let some fv ← resolveHyp g idx user
      | throwError "irfact: hypothesis {idx}/{user} not in context"
    pure (mkFVar fv)
  | .inst e => pure (e.instantiateRev (← lctxFVars g))

/-- One `rw`-style step: kabstract every current occurrence, rewrite once,
never re-iterate.  Loop-free where simp's keyed matching is not. -/
def rwStep (g : MVarId) (f : Fact) : MetaM (Option MVarId) := g.withContext do
  let prf0 ← factProof g f.ref
  let prf ← if f.inverted then Meta.mkEqSymm prf0 else pure prf0
  let r ← g.rewrite (← g.getType) prf
  let g' ← g.replaceTargetEq r.eNew r.eqProof
  unless r.mvarIds.isEmpty do
    throwError "irexec: rw step left side-goals"
  pure (some g')

/-- Execute a REWRITE action: one `simp only` over exactly the recorded
facts at the recorded location.  `contIdx = none` means the action must
close the goal; `some _` means exactly one residual goal is expected. -/
def execRewrite (n : IRNode) (g : MVarId) (simprocs : Simp.Simprocs) :
    MetaM (List MVarId) := g.withContext do
  match n.loc with
  | .hyp _ _ => throwError "irexec: hypothesis-location rewrite unsupported in v1"
  | .goal =>
    let res ← if n.ordered then do
      -- ordered mode: each recorded fact is its own simp-only step, in
      -- order; a step that fails or no-ops is a named discrepancy
      let mut cur := g
      let mut closed := false
      for i in [0:n.facts.size] do
        if closed then
          throwError "irexec: ordered rewrite closed early at step {i}"
        let f := n.facts[i]!
        let res ← if f.rw then rwStep cur f
          else do
            let thms ← buildFactSet cur #[f]
            let ctx ← Simp.mkContext (simpTheorems := #[thms])
                        (congrTheorems := ← Meta.getSimpCongrTheorems)
            let (r, _) ← simpGoal cur ctx (simprocs := #[simprocs])
            pure (r.map (fun x => x.2))
        let before ← instantiateMVars (← cur.getType)
        match res with
        | none => closed := true
        | some g' => do
          let after ← instantiateMVars (← g'.getType)
          if after == before then
            throwError "irexec: ordered rewrite step {i} made no progress"
          cur := g'
      pure (if closed then none else some (#[], cur))
    else do
      let thms ← buildFactSet g n.facts
      let ctx ← Simp.mkContext (simpTheorems := #[thms])
                  (congrTheorems := ← Meta.getSimpCongrTheorems)
      let (res, _) ← simpGoal g ctx (simprocs := #[simprocs])
      pure res
    -- arity (0 or 1 residual) is checked by `execNode`; `contIdx` is
    -- metadata recording WHICH region continuation owned the residual,
    -- and is `none` when the residual is closed by a promoted terminal.
    match res with
    | none => pure []
    | some (_, g') => pure [g']

/-- Execute APPLY / CONSTRUCTOR / CASES / INDUCT: instantiate the recorded
head, assign the recorded data arguments positionally, unify the conclusion
with the goal, and return the open PROOF metavariables in order. -/
def execHead (n : IRNode) (g : MVarId) : MetaM (List MVarId) := g.withContext do
  let some h := n.head? | throwError "irexec: no head recorded"
  let fn ← match h with
    | .cnst c => mkConstWithFreshMVarLevels c
    | .hyp idx user => do
      let some fv ← resolveHyp g idx user
        | throwError "irexec: head hypothesis {idx}/{user} not in context"
      pure (mkFVar fv)
  let hType ← inferType fn
  let fvs ← lctxFVars g
  let dataMap : Std.HashMap Nat Expr :=
    n.dataArgs.foldl (fun m (i, e) => m.insert i (e.instantiateRev fvs)) {}
  let arity := n.nArgs
  let mut curType := hType
  let mut allMvs : Array Expr := #[]
  let mut idx := 0
  for _ in [0:arity] do
    if idx ≥ arity then break
    let (mvs, _, concl) ← forallMetaBoundedTelescope curType (arity - idx)
    if mvs.size == 0 then throwError "irexec: head telescope stalled at arg {idx}"
    for i in [0:mvs.size] do
      if let some a := dataMap.get? (idx + i) then
        let s ← Meta.saveState
        unless ← (try isDefEq mvs[i]! a catch _ => pure false) do s.restore
    allMvs := allMvs ++ mvs
    curType ← instantiateMVars concl
    idx := idx + mvs.size
  let gType ← instantiateMVars (← g.getType)
  let ok ← isDefEq curType gType
  let ok ← if ok then pure true else Mathrecord.Ho.tryMotiveSynth curType gType
  unless ok do
    throwError "irexec: conclusion mismatch for {h.render}"
  -- synthesize class-typed holes, exactly as the prover's apply does
  for mv in allMvs do
    let m := mv.mvarId!
    unless ← m.isAssigned do
      let τ ← instantiateMVars (← m.getType)
      unless τ.hasExprMVar do
        if (← Meta.isClass? τ).isSome then
          try m.assign (← synthInstance τ) catch _ => pure ()
  g.assign (mkAppN fn allMvs)
  let mut out : List MVarId := []
  for mv in allMvs.reverse do
    let m := mv.mvarId!
    unless ← m.isAssigned do out := m :: out
  pure out

/-- Execute a terminal EXACT. -/
def execExact (n : IRNode) (g : MVarId) : MetaM (List MVarId) := g.withContext do
  let some k := n.exact? | throwError "irexec: no exact form recorded"
  match k with
  | .rfl => do
    try g.refl catch _ => g.applyRfl
    pure []
  | .hypothesis idx user => do
    let some fv ← resolveHyp g idx user
      | throwError "irexec: exact hypothesis {idx}/{user} not in context"
    unless ← isDefEq (mkMVar g) (mkFVar fv) do
      throwError "irexec: exact hypothesis {user} does not close the goal"
    pure []
  | .constant c => do
    let e ← mkConstWithFreshMVarLevels c
    unless ← isDefEq (mkMVar g) e do
      throwError "irexec: exact constant {c} does not close the goal"
    pure []

/-- Execute one node and recurse positionally into `kids`.  A mismatch
between the subgoals produced and the recorded children is the named
`arity` discrepancy, never silently absorbed. -/
partial def execNode (n : IRNode) (g : MVarId) (simprocs : Simp.Simprocs)
    (trace : IO.Ref (Array Json)) (depth : Nat := 0) : MetaM Unit := do
  let before ← try pure ((toString (← instantiateMVars (← g.getType))).take 200).toString
               catch _ => pure "?"
  let record (status : String) (detail : String) : MetaM Unit :=
    trace.modify (·.push (Json.mkObj [
      ("d", Lean.toJson depth), ("f", Json.str n.fam.toStr),
      ("before", Json.str before), ("status", Json.str status),
      ("detail", Json.str (detail.take 300).toString)]))
  if n.fam == .unsupported then
    record "unsupported" n.reason
    throwError "irexec: unsupported semantic family ({n.reason})"
  let subs ← try
      match n.fam with
      | .intro => do
        let (_, g') ← g.introNP n.nIntro
        pure [g']
      | .rewrite => execRewrite n g simprocs
      | .exact => execExact n g
      | .have_ => do
        let some t0 := n.haveTy? | throwError "irexec: no have type recorded"
        let t ← instLocal g t0
        let pm ← mkFreshExprMVar t
        let g2 ← g.assert `hir t pm
        let (_, g3) ← g2.intro1P
        pure [pm.mvarId!, g3]
      | .change => do
        let some t0 := n.haveTy? | throwError "irexec: no change type recorded"
        let g' ← g.change (← instLocal g t0)
        pure [g']
      | .apply | .ctor | .cases | .induct => execHead n g
      | .unsupported => throwError "unreachable"
    catch ex => do
      let msg ← try ex.toMessageData.toString catch _ => pure "?"
      record "exec_failed" msg
      throw ex
  if subs.length != n.kids.size then
    record "arity" s!"produced {subs.length} subgoals, recorded {n.kids.size}"
    throwError "irexec: arity mismatch at {n.fam.toStr}"
  record "ok" ""
  for (g', k) in subs.zip n.kids.toList do
    unless ← g'.isAssigned do
      execNode k g' simprocs trace (depth + 1)


/-! ## Extraction

Walks the reference proof term against the LIVE goal state, deciding for
each step whether IR v1 can parameterize it.  Parameters the reference does
not state outright are found by BOUNDED TRIAL and recorded; a step for
which no parameterization is found becomes `Family.unsupported` with a
reason, which is the per-action failure class.

Extraction executes as it walks (the child steps must be extracted against
real successor goals), so at the end the reference goal is closed.  Replay
then runs on a FRESH goal from the recorded IR alone. -/

structure ExCtx where
  env      : Environment
  simprocs : Simp.Simprocs
  fuel     : IO.Ref Nat
  /-- orientation vectors tried per rewrite region before giving up -/
  orientCap : Nat := 5

/-- Classify an application head into a family, without name matching. -/
def headFamily (env : Environment) (fn : Expr) : Family :=
  match fn.consumeMData with
  | .const c _ =>
    match elimRecursive? env c with
    | some true => .induct
    | some false => .cases
    | none => match env.find? c with
              | some (.ctorInfo _) => .ctor
              | _ => .apply
  | .fvar _ => .apply
  | _ => .apply

/-- Introduce at most `k` binders: the largest prefix the goal actually
grants.  `none` when the goal offers no binder at all. -/
partial def introUpTo (g : MVarId) (k : Nat) :
    MetaM (Option (Nat × Array FVarId × MVarId)) := do
  if k == 0 then return none
  let s ← Meta.saveState
  match ← (try (do let r ← g.introNP k; pure (some r)) catch _ => pure none) with
  | some (fvs, g') => pure (some (k, fvs, g'))
  | none => do s.restore; introUpTo g (k - 1)

/-- Endpoints of an equality-family conclusion. -/
def eqEndpoints (concl : Expr) : Option (Expr × Expr) :=
  let c := concl.consumeMData
  match c.getAppFn.consumeMData with
  | .const n _ =>
    let a := c.getAppArgs
    if n == ``Eq && a.size >= 3 then some (a[1]!, a[2]!)
    else if n == ``Iff && a.size >= 2 then some (a[0]!, a[1]!)
    else if n == ``HEq && a.size >= 4 then some (a[1]!, a[3]!)
    else none
  | _ => none

/-- Does `pat` occur in `e` (keyed matching, the same test the simplifier
uses to decide applicability)? -/
def occursIn (pat : Expr) (e : Expr) : MetaM Bool := do
  try pure (← kabstract e pat).hasLooseBVars catch _ => pure false

/-- Type of a recorded fact, in the goal's context. -/
def factType (g : MVarId) (r : FactRef) : MetaM (Option Expr) := g.withContext do
  try
    match r with
    | .cnst c => pure (some (← inferType (← mkConstWithFreshMVarLevels c)))
    | .hyp idx user => do
      match ← resolveHyp g idx user with
      | some f => pure (some (← f.getType))
      | none => pure none
    | .inst e => pure (some (← inferType (e.instantiateRev (← lctxFVars g))))
  catch _ => pure none

/-- INFER a fact's orientation instead of searching for it: the direction
whose source endpoint actually occurs in the goal.  This is what makes
`inverted` a determinable IR field rather than a retry. -/
def inferOrientation (g : MVarId) (r : FactRef) : MetaM Bool := g.withContext do
  let some t ← factType g r | return false
  try
    forallTelescopeReducing t fun _ concl => do
      let some (lhs, rhs) := eqEndpoints concl | return false
      let gT ← instantiateMVars (← g.getType)
      if ← occursIn lhs gT then return false
      if ← occursIn rhs gT then return true
      return false
  catch _ => pure false

/-- All orientation vectors of length `k`, all-forward and all-inverted
first (the two cases `semSimpAct` retried), then the rest in binary order.
Empty when `k` exceeds the cap. -/
def orientVectors (k : Nat) (cap : Nat) : Array (Array Bool) :=
  if k == 0 then #[#[]]
  else
    let allF := Array.replicate k false
    let allT := Array.replicate k true
    if k > cap then #[allF, allT]
    else Id.run do
      let mut out := #[allF, allT]
      for m in [0:2 ^ k] do
        let v := (Array.range k).map fun i => (m / (2 ^ i)) % 2 == 1
        if v != allF && v != allT then out := out.push v
      pure out

/-- Lower the recursion cap for one bounded trial.  Raising the harness
cap (`Core.Context.maxRecDepth`) lets a looping rewrite set overflow the
REAL stack before the counter fires - and a hardware overflow is not
catchable in MetaM, so it aborts the whole theorem.  Trials run shallow;
only a committed action gets the full depth. -/
def withTrialDepth (x : MetaM α) : MetaM α :=
  withTheReader Core.Context (fun c => { c with maxRecDepth := 2000 }) x

/-- Try one orientation vector at goal `g`.  Returns (result, depth-hit):
result is the residual goal (if any) on success; depth-hit marks a trial
that died on the recursion cap. -/
def tryOrient (ctx : ExCtx) (g : MVarId) (facts : Array Fact) :
    MetaM (Option (Option MVarId) × Bool) := do
  let s ← Meta.saveState
  -- `tryCatchRuntimeEx`, not `try`: `Core.tryCatch` deliberately re-throws
  -- runtime exceptions (the "maximum recursion depth" form among them), so
  -- an ordinary catch lets a looping trial abort the whole theorem.
  tryCatchRuntimeEx
    (withTrialDepth do
      let thms ← buildFactSet g facts
      let sctx ← Simp.mkContext (simpTheorems := #[thms])
                   (congrTheorems := ← Meta.getSimpCongrTheorems)
      let (res, _) ← simpGoal g sctx (simprocs := #[ctx.simprocs])
      match res with
      | none => pure (some none, false)
      | some (_, g') => pure (some (some g'), false))
    (fun ex => do
      s.restore
      let m ← try ex.toMessageData.toString catch _ => pure ""
      pure (none, (m.splitOn "recursion depth").length > 1))

/-- Turn a certificate region's boundary leaves into `FactRef`s. -/
def leafFacts (g : MVarId) (leaves : Array Semantic.Leaf) :
    MetaM (Array FactRef) := g.withContext do
  let mut out : Array FactRef := #[]
  for l in leaves do
    let t := l.term.consumeMData
    match t with
    | .const c _ => out := out.push (.cnst c)
    | .fvar f =>
      match ← lctxIndexOf g f with
      | some (i, u) => out := out.push (.hyp i u)
      | none => out := out.push (.inst (← absLocal g t))
    | _ =>
      if l.generalized then
        match t.getAppFn.consumeMData with
        | .const c _ => out := out.push (.cnst c)
        | .fvar f =>
          match ← lctxIndexOf g f with
          | some (i, u) => out := out.push (.hyp i u)
          | none => out := out.push (.inst (← absLocal g t))
        | _ => out := out.push (.inst (← absLocal g t))
      else out := out.push (.inst (← absLocal g t))
  pure out

/-- Terminal promotion: the residual goal that `semSimpAct` used to close
silently with `refl` or `assumptionCore` becomes an explicit EXACT node. -/
def promoteTerminal (g : MVarId) : MetaM (Option IRNode) := g.withContext do
  let s ← Meta.saveState
  let isRfl ← try (do g.refl; pure true) catch _ => pure false
  s.restore
  -- `refl` covers Eq/HEq only; `applyRfl` extends to every `@[refl]`
  -- relation (Iff first among them) - attribute-driven, no name cases
  let isRfl ← if isRfl then pure true else do
    let r ← try (do g.applyRfl; pure true) catch _ => pure false
    s.restore
    pure r
  if isRfl then return some { fam := .exact, exact? := some .rfl }
  let lctx ← getLCtx
  let gT ← instantiateMVars (← g.getType)
  let mut i := 0
  for d in lctx do
    if !d.isImplementationDetail then
      let ok ← try isDefEq d.type gT catch _ => pure false
      if ok then
        return some { fam := .exact, exact? := some (.hypothesis i d.userName) }
      i := i + 1
  pure none

mutual

/-- Extract the IR for the reference subterm `e` at goal `g`, executing as
it goes.  Never throws: an unparameterizable step becomes an
`unsupported` node carrying its reason. -/
partial def extract (ctx : ExCtx) (g : MVarId) (e : Expr) : MetaM IRNode := do
  if (← ctx.fuel.get) == 0 then
    return { fam := .unsupported, reason := "fuel_exhausted" }
  ctx.fuel.modify (· - 1)
  try extractCore ctx g e
  catch ex =>
    let msg ← try ex.toMessageData.toString catch _ => pure "?"
    pure { fam := .unsupported,
           reason := s!"extract_exception:{(msg.take 120).toString}" }

partial def extractCore (ctx : ExCtx) (g : MVarId) (e : Expr) :
    MetaM IRNode := g.withContext do
  let e := e.consumeMData
  -- REWRITE: a maximal certificate region is ONE action
  if Semantic.certRegionRoot e then
    return ← extractRewrite ctx g e
  match e with
  | .lam .. =>
    -- The reference term may bind more lambdas than the goal currently
    -- offers as binders (the next one hides behind a definitional
    -- unfolding).  Peel only what the GOAL grants; the remainder stays a
    -- lambda and the child INTRO takes it.
    let nWant := Id.run do
      let mut k := 0
      let mut cur := e
      while cur.isLambda do
        k := k + 1
        cur := cur.bindingBody!
      pure k
    match ← introUpTo g nWant with
    | none => pure { fam := .unsupported, reason := "intro_no_binder_available" }
    | some (k, fvs, g') =>
      let body := e.beta (fvs.map mkFVar)
      let kid ← extract ctx g' body
      pure { fam := .intro, nIntro := k, kids := #[kid] }
  | .letE nm ty val body _ => do
    let pm ← mkFreshExprMVar ty
    let g2 ← g.assert nm ty pm
    let (fv, g3) ← g2.intro1P
    let k1 ← extract ctx pm.mvarId! val
    let k2 ← extract ctx g3 (body.instantiate1 (mkFVar fv))
    pure { fam := .have_, haveTy? := some (← absLocal g ty), kids := #[k1, k2] }
  | .app .. => extractHead ctx g e
  | .fvar f => do
    match ← lctxIndexOf g f with
    | some (i, u) =>
      unless ← isDefEq (mkMVar g) e do
        return { fam := .unsupported, reason := "exact_hyp_mismatch" }
      pure { fam := .exact, exact? := some (.hypothesis i u) }
    | none => pure { fam := .unsupported, reason := "exact_hyp_not_in_context" }
  | .const c _ => do
    unless ← isDefEq (mkMVar g) e do
      return { fam := .unsupported, reason := "exact_const_mismatch" }
    pure { fam := .exact, exact? := some (.constant c) }
  | _ => do
    -- definitional-only step: the goal changes, the proof does not
    if ← (try isDefEq (mkMVar g) e catch _ => pure false) then
      pure { fam := .exact, exact? := some .rfl }
    else
      pure { fam := .unsupported, reason := "unclassified_term" }

/-- REWRITE region: extract the fact set, DETERMINE each fact's
orientation by bounded trial, and record it. -/
partial def extractRewrite (ctx : ExCtx) (g : MVarId) (e : Expr) :
    MetaM IRNode := do
  let (leaves, conts, nStruct) ←
    try Semantic.regionParts e catch _ => pure (#[], #[], 0)
  if leaves.isEmpty && conts.isEmpty then
    return { fam := .unsupported, reason := "empty_region" }
  let refs ← leafFacts g leaves
  -- INFERRED orientation first (per fact, from endpoint occurrence), then
  -- the two uniform vectors `semSimpAct` used to retry, then - only for
  -- small fact sets - the remaining combinations.
  let inferred ← refs.mapM fun r => inferOrientation g r
  let vectors := #[inferred] ++ orientVectors refs.size ctx.orientCap
  let wide := refs.size > ctx.orientCap
  let mut anyDepth := false
  for v in vectors do
    let facts := (Array.range refs.size).map fun i =>
      ({ ref := refs[i]!, inverted := v[i]?.getD false } : Fact)
    -- STATE DISCIPLINE: a trial that does not commit must leave no trace.
    -- `simpGoal` mutates the goal, so an uncommitted orientation would
    -- otherwise hand the next trial an already-rewritten goal.
    let snap ← Meta.saveState
    let (r, depthHit) ← tryOrient ctx g facts
    if depthHit then anyDepth := true
    match r with
    | none => snap.restore; continue
    | some none =>
      -- closed outright
      return { fam := .rewrite, facts, loc := .goal, contIdx := none,
               covers := nStruct + 1, kids := #[] }
    | some (some g') =>
      -- one residual: does a region continuation own it?
      let g'T ← instantiateMVars (← g'.getType)
      let mut owner : Option Nat := none
      let mut oi := 0
      for c in conts do
        if owner.isNone then
          let cT ← try instantiateMVars (← inferType c) catch _ => pure default
          if ← (try isDefEq g'T cT catch _ => pure false) then owner := some oi
        oi := oi + 1
      match owner with
      | some i =>
        let kid ← extract ctx g' conts[i]!
        return { fam := .rewrite, facts, loc := .goal, contIdx := some i,
                 covers := nStruct + 1, kids := #[kid] }
      | none =>
        -- promoted terminal (the old silent `refl` / `assumptionCore`)
        match ← promoteTerminal g' with
        | some t =>
          let _ ← try execExact t g' catch _ => pure []
          return { fam := .rewrite, facts, loc := .goal, contIdx := none,
                   covers := nStruct + 1, kids := #[t] }
        | none => snap.restore; continue
  -- ORDERED MODE: the certificate is an `Eq.trans` CHAIN; when the
  -- flattened set fails (ping-pong between near-identical facts, one
  -- fact's output feeding the next's input), apply the facts ONE AT A
  -- TIME in leaf order, choosing each step's orientation by trial
  -- (linear, not exponential).  A fact that fires in neither direction
  -- is skipped - instance-variant duplicates of an applied fact.
  -- Soundness is unchanged: success still requires the goal closed, a
  -- continuation owning the residual, or a promoted terminal.
  let ordSnap ← Meta.saveState
  let mut ordNote := ""
  let ordResult ← do
    let mut cur := g
    let mut steps : Array Fact := #[]
    let mut closed := false
    for i in [0:refs.size] do
      if !closed then
        let mut fired := false
        -- rw-mode first: single-pass, loop-free (instance-bridge safe);
        -- simp-mode second: iterated, catches conditional rewrites
        for md in #[true, false] do
          for inv in #[inferred[i]?.getD false, !(inferred[i]?.getD false)] do
            if !fired then
              let f : Fact := { ref := refs[i]!, inverted := inv, rw := md }
              let stepSnap ← Meta.saveState
              let before ← cur.withContext do instantiateMVars (← cur.getType)
              let (r, dh) ← if md then
                  tryCatchRuntimeEx
                    (withTrialDepth do pure (some (← rwStep cur f), false))
                    (fun _ => do stepSnap.restore; pure (none, false))
                else tryOrient ctx cur #[f]
              if dh then anyDepth := true
              match r with
              | none => stepSnap.restore
              | some none =>
                steps := steps.push f; closed := true; fired := true
              | some (some g') => do
                let after ← g'.withContext do instantiateMVars (← g'.getType)
                if after == before then stepSnap.restore
                else
                  steps := steps.push f; cur := g'; fired := true
    pure (if steps.isEmpty then none else some (steps, closed, cur))
  match ordResult with
  | some (steps, true, _) =>
    return { fam := .rewrite, facts := steps, ordered := true, loc := .goal,
             contIdx := none, covers := nStruct + 1, kids := #[] }
  | some (steps, false, cur) => do
    let g'T ← cur.withContext do instantiateMVars (← cur.getType)
    let mut owner : Option Nat := none
    let mut oi := 0
    for c in conts do
      if owner.isNone then
        let cT ← try instantiateMVars (← inferType c) catch _ => pure default
        if ← (try isDefEq g'T cT catch _ => pure false) then owner := some oi
      oi := oi + 1
    match owner with
    | some i =>
      let kid ← extract ctx cur conts[i]!
      return { fam := .rewrite, facts := steps, ordered := true, loc := .goal,
               contIdx := some i, covers := nStruct + 1, kids := #[kid] }
    | none =>
      match ← promoteTerminal cur with
      | some t =>
        let _ ← try execExact t cur catch _ => pure []
        return { fam := .rewrite, facts := steps, ordered := true, loc := .goal,
                 contIdx := none, covers := nStruct + 1, kids := #[t] }
      | none => do
        let resid ← cur.withContext do
          pure (((toString (← instantiateMVars (← cur.getType))).take 80).toString)
        ordNote := s!"|ord={steps.size}/{refs.size}fired,resid={resid}"
        ordSnap.restore
  | none => do
    ordNote := s!"|ord=0/{refs.size}fired"
    ordSnap.restore

  -- DIAGNOSTIC: does either endpoint of each fact occur in the goal at
  -- all?  `occ` = at least one fact is applicable and the failure is about
  -- HOW it is applied (occurrence/motive/mode); `noocc` = no fact matches
  -- the goal, so the failure is a STATE mismatch, not a rewrite parameter.
  let mut anyOcc := false
  for r in refs do
    if !anyOcc then
      if let some t ← factType g r then
        let occ ← try
          forallTelescopeReducing t fun _ concl => do
            let some (lhs, rhs) := eqEndpoints concl | pure false
            let gT ← instantiateMVars (← g.getType)
            pure ((← occursIn lhs gT) || (← occursIn rhs gT))
          catch _ => pure false
        if occ then anyOcc := true
  let nGen := leaves.foldl (fun acc l => if l.generalized then acc + 1 else acc) 0
  let gHead ← g.withContext do
    let gT ← instantiateMVars (← g.getType)
    pure ((toString gT).take 100).toString
  let mut fdescs : Array String := #[]
  for r in (refs.extract 0 4) do
    let td ← match ← factType g r with
      | some t => pure (((toString t).take 80).toString)
      | none => pure "?"
    fdescs := fdescs.push s!"{r.render}={td}"
  let fdesc := " ;; ".intercalate fdescs.toList
  pure { fam := .unsupported,
         reason := (if anyDepth then "rewrite_depth_overflow"
                    else if wide then "orient_search_too_wide"
                    else "rewrite_no_orientation")
                   ++ (if anyOcc then "_occ" else "_noocc")
                   ++ s!":{refs.size}facts:{conts.size}conts:{nGen}gen"
                   ++ ordNote ++ s!"|goal={gHead}|{fdesc}" }

/-- APPLY / CONSTRUCTOR / CASES / INDUCT: record the head, split the
arguments into recorded data and proof children, execute, and extract each
child against its own successor goal. -/
partial def extractHead (ctx : ExCtx) (g : MVarId) (e : Expr) :
    MetaM IRNode := do
  let fn := e.getAppFn.consumeMData
  let args := e.getAppArgs
  if fn.isLambda then
    return { fam := .unsupported, reason := "beta_redex_head" }
  let head? : Option HeadRef ← match fn with
    | .const c _ => pure (some (.cnst c))
    | .fvar f => do
      match ← lctxIndexOf g f with
      | some (i, u) => pure (some (.hyp i u))
      | none => pure none
    | _ => pure none
  let some head := head?
    | return { fam := .unsupported, reason := "head_not_referenceable" }
  let fam := headFamily ctx.env fn
  let hType ← inferType fn
  let mut curType := hType
  let mut allMvs : Array Expr := #[]
  let mut dataArgs : Array (Nat × Expr) := #[]
  let mut proofRef : Std.HashMap Nat Expr := {}
  let mut idx := 0
  for _ in [0:args.size] do
    if idx ≥ args.size then break
    let (mvs, _, concl) ← forallMetaBoundedTelescope curType (args.size - idx)
    if mvs.size == 0 then
      return { fam := .unsupported, reason := "head_telescope_stalled" }
    for i in [0:mvs.size] do
      let j := idx + i
      let a := args[j]!
      let aP ← try Meta.isProp (← inferType a) catch _ => pure false
      if aP then proofRef := proofRef.insert j a
      else
        dataArgs := dataArgs.push (j, ← absLocal g a)
        let s ← Meta.saveState
        unless ← (try isDefEq mvs[i]! a catch _ => pure false) do s.restore
    allMvs := allMvs ++ mvs
    curType ← instantiateMVars concl
    idx := idx + mvs.size
  let gType ← instantiateMVars (← g.getType)
  let ok ← try isDefEq curType gType catch _ => pure false
  let ok ← if ok then pure true else
    try Mathrecord.Ho.tryMotiveSynth curType gType catch _ => pure false
  unless ok do
    return { fam := .unsupported, reason := s!"head_conclusion_mismatch:{head.render}" }
  -- DEFERRED DATA ASSIGNMENT (the guided engine's fix, replicated): a data
  -- argument whose eager unification failed on open sibling holes usually
  -- unifies once the conclusion has bound the telescope.  Left open, its
  -- metavariable leaks into hypothesis TYPES of child contexts, and any
  -- rewrite fact citing such a hypothesis is unusable.
  let dataRef : Std.HashMap Nat Expr :=
    dataArgs.foldl (fun m (i, e) => m.insert i e) {}
  let fvsNow ← lctxFVars g
  let mut j2 := 0
  for mv in allMvs do
    let m := mv.mvarId!
    unless ← m.isAssigned do
      if let some a0 := dataRef.get? j2 then
        let a := a0.instantiateRev fvsNow
        let s ← Meta.saveState
        unless ← (try isDefEq mv a catch _ => pure false) do s.restore
    j2 := j2 + 1
  for mv in allMvs do
    let m := mv.mvarId!
    unless ← m.isAssigned do
      let τ ← instantiateMVars (← m.getType)
      unless τ.hasExprMVar do
        if (← Meta.isClass? τ).isSome then
          try m.assign (← synthInstance τ) catch _ => pure ()
  g.assign (mkAppN fn allMvs)
  -- children in the SAME order `execHead` will produce them.  The open
  -- list must be taken EAGERLY: extracting a child assigns metavariables,
  -- so a lazily-tested list is shorter than the one replay will see.
  let mut openIdx : Array Nat := #[]
  let mut j := 0
  for mv in allMvs do
    unless ← mv.mvarId!.isAssigned do openIdx := openIdx.push j
    j := j + 1
  let mut kids : Array IRNode := #[]
  for i in openIdx do
    let m := allMvs[i]!.mvarId!
    if ← m.isAssigned then
      kids := kids.push { fam := .unsupported, reason := "sibling_assigned_child" }
    else
      match proofRef.get? i with
      | some r => kids := kids.push (← extract ctx m r)
      | none => kids := kids.push { fam := .unsupported, reason := "open_data_hole" }
  pure { fam, head? := some head, nArgs := args.size, dataArgs, kids }

end


/-! ## Deterministic semantic replay

Extraction and replay are run as two separate passes over two separate
fresh goals.  Replay receives the `IRNode` only.  There is no budget, no
frontier, no ranker, and no fallback: the run either executes the recorded
sequence or stops at a named first discrepancy. -/

/-- First trace entry whose status is not `ok` - the exact first
discrepancy.  `none` when the whole sequence executed. -/
def firstDiscrepancy (tr : Array Json) : Option Json :=
  tr.find? fun r =>
    match r.getObjValAs? String "status" with
    | .ok st => st != "ok"
    | .error _ => false

def semreplay (path : System.FilePath) (inp : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path Mathrecord.Study.mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let raw ← IO.FS.readFile inp
  let j ← IO.ofExcept (Json.parse raw)
  let ts ← IO.ofExcept ((← IO.ofExcept
    (j.getObjVal? "goals" <|> j.getObjVal? "tasks")).getArr?)
  IO.println s!"{ts.size} theorems"
  let h ← IO.FS.Handle.mk out .write
  -- `maxRecDepth` is a cached field of `Core.Context`, NOT read from the
  -- options set by `withOptions`: a runaway simp inside one certificate
  -- region otherwise aborts the whole theorem before it can be classified.
  let coreCtx : Core.Context :=
    { fileName := pf.fileName, fileMap := default, maxRecDepth := 8000 }
  let mut count := 0
  let mut extractClean := 0
  let mut replayOk := 0
  let mut verifiedN := 0
  for tj in ts do
    let nm := ((do (← tj.getObjVal? "n").getStr? :
      Except String String)).toOption.getD ""
    if nm == "" then continue
    let n := String.toName nm
    let act : MetaM Json := do
      let some ci := env.find? n
        | return Json.mkObj [("n", Json.str nm), ("error", Json.str "not found")]
      let some val := ci.value? (allowOpaque := true)
        | return Json.mkObj [("n", Json.str nm), ("error", Json.str "no value")]
      let simprocs ← Simp.getSimprocs
      Meta.forallTelescope ci.type fun xs concl => do
        let term := Semantic.unfoldAux env nm (val.beta xs)
        let nRaw ← try Semantic.rawCount term catch _ => pure 0
        -- PASS 1: extraction (executes; state discarded afterwards).
        -- Guarded at the pass level too: a hardware stack overflow is not
        -- catchable inside MetaM, but this outer catch (one monadic layer
        -- up, no deep frame below it) still fires for the counter-based
        -- form and anything else that escapes the per-node handlers.
        let fuel ← IO.mkRef 4000
        let ir ← tryCatchRuntimeEx
            (withoutModifyingState do
              let g0 ← mkFreshExprMVar concl
              extract { env, simprocs, fuel } g0.mvarId! term)
            (fun ex => do
              let m ← try ex.toMessageData.toString catch _ => pure "?"
              pure { fam := .unsupported,
                     reason := s!"pass1_escape:{(m.take 100).toString}" })
        let reasons := ir.unsupportedReasons
        -- PASS 2: replay from the IR ALONE, on a fresh goal
        let trace ← IO.mkRef (#[] : Array Json)
        let root ← mkFreshExprMVar concl
        let replayErr ← tryCatchRuntimeEx
            (do execNode ir root.mvarId! simprocs trace
                pure (none : Option String))
            (fun ex => do
              let msg ← try ex.toMessageData.toString catch _ => pure "?"
              pure (some ("pass2:" ++ (msg.take 200).toString)))
        -- verification of what replay actually built
        let (verified, vwhy) ← if replayErr.isSome then pure (false, "replay_failed") else
          try
            let proof ← mkLambdaFVars xs (← instantiateMVars root)
            if proof.hasExprMVar then do
              -- name the open holes: their TYPES say whether they are
              -- instances, motives, or plain values
              let st := Lean.Expr.collectMVars {} proof
              let mut tys : Array String := #[]
              for m in st.result.toList.take 3 do
                let τ ← try instantiateMVars (← m.getType) catch _ => pure default
                tys := tys.push (((toString τ).take 70).toString)
              pure (false, s!"open_mvars:{st.result.size}:" ++ " ;; ".intercalate tys.toList)
            else
            let ok0 ← try
              Meta.check proof
              isDefEq (← inferType proof) ci.type
            catch _ => pure false
            if ok0 then pure (true, "") else
              match Kernel.Environment.addDecl (← getEnv).toKernelEnv {}
                  (.thmDecl { name := `_mrSemIRArbiter,
                              levelParams := ci.levelParams,
                              type := ci.type, value := proof }) with
              | Except.ok _ => pure (true, "kernel_arbited")
              | Except.error e => do
                let m ← try (e.toMessageData {}).toString catch _ => pure "?"
                pure (false, s!"kernel:{(m.take 160).toString}")
          catch ex => do
            let m ← try ex.toMessageData.toString catch _ => pure "?"
            pure (false, s!"assemble:{(m.take 160).toString}")
        let tr ← trace.get
        let tally := ir.tally
        return Json.mkObj [
          ("n", Json.str nm),
          ("extract_clean", Lean.toJson reasons.isEmpty),
          ("unsupported", Json.arr (reasons.map Json.str)),
          ("replay_ok", Lean.toJson replayErr.isNone),
          ("verified", Lean.toJson verified),
          ("verify_why", Json.str vwhy),
          ("replay_err", match replayErr with
             | some m => Json.str m | none => Json.null),
          ("first_discrepancy", (firstDiscrepancy tr).getD Json.null),
          ("n_actions", Lean.toJson ir.size),
          ("n_covered", Lean.toJson ir.covered),
          ("n_raw", Lean.toJson nRaw),
          ("horizon", Lean.toJson ir.horizon),
          ("families", Json.mkObj (tally.toList.map fun (k, v) => (k, Lean.toJson v))),
          ("ir", ir.toJson),
          ("trace", Json.arr tr)]
    let row ← try
      let (r, _) ← (act.run' {} {}).toIO coreCtx { env }
      pure r
    catch e =>
      pure (Json.mkObj [("n", Json.str nm),
                        ("error", Json.str ((toString e).take 200).toString)])
    if (row.getObjValAs? Bool "extract_clean").toOption == some true then
      extractClean := extractClean + 1
    if (row.getObjValAs? Bool "replay_ok").toOption == some true then
      replayOk := replayOk + 1
    if (row.getObjValAs? Bool "verified").toOption == some true then
      verifiedN := verifiedN + 1
    h.putStrLn row.compress
    count := count + 1
    if count % 10 == 0 then
      IO.println s!"  {count}/{ts.size}: extract-clean {extractClean}, replay {replayOk}, verified {verifiedN}"
      h.flush
  IO.println s!"done: {count} theorems; extract-clean {extractClean}; replay-ok {replayOk}; verified {verifiedN}"
  h.flush

end Mathrecord.SemIR
