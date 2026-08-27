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

/-- Structural diff of two expressions: the single consistent differing
subterm pair, descending through equal application spines.  Returns none
when the sides are equal or the difference is not a single consistent
pair. -/
partial def diffPair (A B : Expr) : Option (Expr × Expr) :=
  if A == B then none
  else
    let fa := A.getAppFn
    let fb := B.getAppFn
    let as := A.getAppArgs
    let bs := B.getAppArgs
    if fa == fb && as.size == bs.size && as.size > 0 then
      let diffs := (as.zip bs).filterMap
        (fun (x, y) => if x == y then none else some (x, y))
      match diffs with
      | #[(x, y)] => (diffPair x y).orElse (fun _ => some (x, y))
      | _ =>
        -- several args differ: consistent only if all share one pair
        if diffs.size > 1 && diffs.all (fun d => d == diffs[0]!) then
          some diffs[0]!
        else some (A, B)
    else some (A, B)

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
  let some (a, b) := diffPair A B | return false
  let τa ← inferType a
  let fBody ← kabstract A a
  if !fBody.hasLooseBVars then return false
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
def tryMotiveSynth (concl gType : Expr) : MetaM Bool := do
  if ← (try motiveFromGoal concl gType catch _ => pure false) then
    return true
  try congrFromDiff concl gType catch _ => pure false

end Mathrecord.Ho
