import Lean

/-! Mechanical higher-order application support.

The engine's backward application is first-order: it unifies a candidate
head's conclusion with the goal through fresh metavariables.  Reference
proofs, however, are full of heads whose conclusion contains flex
applications - `?motive ?b` (eliminators) or `?f ?a₁ = ?f ?a₂`
(congruence) - which first-order unification cannot solve.  Standard
tactics solve these MECHANICALLY: `rw` abstracts the goal at the
rewritten occurrences (`kabstract`), `congr` structurally decomposes the
two sides of an equality.  This module packages both procedures as a
unification fallback usable by the prover's action generator, the guided
rungs, and the legality probe.

Nothing here consults reference terms: inputs are the candidate's
conclusion (with its open metavariables) and the goal type.
-/

namespace Mathrecord.Ho

open Lean Meta

/-- Positional structural diff-abstraction: rebuild `A` with every
position at which it differs from `B` replaced by a loose bound variable
(index = binders crossed), provided all differing positions carry the
SAME (a, b) pair of closed subterms.  Unlike `kabstract`, this abstracts
exactly the changed occurrences - `a + a = b + a` yields `fun x => x + a`,
not `fun x => x + x`.  Returns (body-with-loose-bvars, a, b). -/
partial def diffAbstract (A B : Expr) : Option (Expr × Expr × Expr) :=
  match go (A.consumeMData) (B.consumeMData) 0 with
  | some (body, some (a, b)) => some (body, a, b)
  | _ => none
where
  leaf (A B : Expr) (d : Nat) : Option (Expr × Option (Expr × Expr)) :=
    if A.hasLooseBVars || B.hasLooseBVars then none
    else some (.bvar d, some (A, B))
  merge : Option (Expr × Expr) → Option (Expr × Expr) →
      Option (Option (Expr × Expr))
    | some p, some q => if p == q then some (some p) else none
    | some p, none => some (some p)
    | none, some q => some (some q)
    | none, none => some none
  go (A B : Expr) (d : Nat) : Option (Expr × Option (Expr × Expr)) :=
    let A := A.consumeMData
    let B := B.consumeMData
    if A == B then some (A, none)
    else
      match A, B with
      | .app fa aa, .app fb ab =>
        match go fa fb d, go aa ab d with
        | some (f', pf), some (a', pa) =>
          match merge pf pa with
          | some p => some (.app f' a', p)
          | none => leaf A B d
        | _, _ => leaf A B d
      | .lam n t b i, .lam _ t' b' _ =>
        if t == t' then
          match go b b' (d + 1) with
          | some (b2, p) => some (.lam n t b2 i, p)
          | none => leaf A B d
        else leaf A B d
      | .forallE n t b i, .forallE _ t' b' _ =>
        if t == t' then
          match go b b' (d + 1) with
          | some (b2, p) => some (.forallE n t b2 i, p)
          | none => leaf A B d
        else leaf A B d
      | _, _ => leaf A B d

/-- Mechanical motive synthesis, case 1: the conclusion is a flex
application `?m a₁ … aₖ` whose arguments are concrete.  Build the motive
by abstracting the goal at each argument (rw-style `kabstract`), assign,
and recheck. -/
def motiveFromGoal (concl gType : Expr) : MetaM Bool := do
  let c ← instantiateMVars concl
  let fn := c.getAppFn
  unless fn.isMVar && c.getAppNumArgs > 0 do return false
  let args := c.getAppArgs
  if args.any (·.hasExprMVar) then return false
  let mut motive := gType
  for a in args.reverse do
    let τa ← inferType a
    let ab ← kabstract motive a
    motive := mkLambda `x .default τa ab
  unless ← isDefEq fn motive do return false
  isDefEq (← instantiateMVars c) gType

/-- Mechanical congruence, case 2: the conclusion is `?f ?a₁ = ?f ?a₂`
(congrArg shape) and the goal is `A = B`.  Derive (f, a, b) from the
structural diff of A and B, validate `f a ≡ A` and `f b ≡ B`, assign. -/
def congrFromDiff (concl gType : Expr) : MetaM Bool := do
  let c ← instantiateMVars concl
  unless c.isAppOfArity ``Eq 3 && gType.isAppOfArity ``Eq 3 do return false
  let cl := c.getAppArgs[1]!
  let cr := c.getAppArgs[2]!
  -- congrArg shape: both sides `?f x` with the same flex head
  unless cl.isApp && cr.isApp && cl.appFn!.isMVar &&
         cl.appFn! == cr.appFn! do return false
  let A := gType.getAppArgs[1]!
  let B := gType.getAppArgs[2]!
  let some (fBody, a, b) := diffAbstract A B | return false
  -- an open side admits only the vacuous identity decomposition
  if a.consumeMData.isMVar || b.consumeMData.isMVar then return false
  let τa ← inferType a
  let f := mkLambda `x .default τa fBody
  -- validate the decomposition on BOTH sides before assigning
  unless ← isDefEq (mkApp f a) A do return false
  unless ← isDefEq (mkApp f b) B do return false
  unless ← isDefEq cl.appFn! f do return false
  unless ← isDefEq cl.appArg! a do return false
  unless ← isDefEq cr.appArg! b do return false
  isDefEq (← instantiateMVars c) gType

/-- Combined mechanical fallback for a failed first-order conclusion
unification.  Side effects on success: the relevant metavariables are
assigned. -/
def tryMotiveSynth (concl gType₀ : Expr) : MetaM Bool := do
  let gType ← instantiateMVars gType₀   -- never match on a raw mvar alias
  if ← (try motiveFromGoal concl gType catch _ => pure false) then
    return true
  try congrFromDiff concl gType catch _ => pure false

end Mathrecord.Ho
