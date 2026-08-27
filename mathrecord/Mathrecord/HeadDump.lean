import Mathrecord.Study

/-! Head-schema dump: every declaration as a typed hyperedge schema.

For each constant `c : ∀ (x₁:A₁)…(xₖ:Aₖ), B` emit the head constant of the
conclusion `B` (the goal shape `c` can attack backward), the head constants
of the explicit premises (the subgoals it would open), binder counts by
kind, and — when a proof/definition body exists — the head constant of the
value after stripping lambdas: the actual top-level move of the recorded
proof. Syntactic telescope only (no whnf/delta): heads are as-written.
-/

namespace Mathrecord.HeadDump

open Lean Mathrecord Mathrecord.Extract Mathrecord.Study

/-- Collect binder types (with binder info) and the conclusion, syntactically. -/
partial def telescope (e : Expr) (acc : Array (Expr × BinderInfo) := #[]) :
    Array (Expr × BinderInfo) × Expr :=
  match e.consumeMData with
  | .forallE _ t b bi => telescope b (acc.push (t, bi))
  | e' => (acc, e')

partial def stripForalls (e : Expr) : Expr :=
  match e.consumeMData with
  | .forallE _ _ b _ => stripForalls b
  | e' => e'

partial def stripLams (e : Expr) : Expr :=
  match e.consumeMData with
  | .lam _ _ b _ => stripLams b
  | e' => e'

/-- Head tag of an expression: constant name, or a small vocabulary of
non-constant shapes. -/
def headTag (e : Expr) : String :=
  let b := e.consumeMData
  if b.isLet then "LET" else
  match b.getAppFn.consumeMData with
  | .const n _ => toString n
  | .bvar _ => "VAR" | .fvar _ => "VAR" | .mvar _ => "MVAR"
  | .sort _ => "SORT" | .lit _ => "LIT" | .lam .. => "LAM"
  | .forallE .. => "FORALL" | .proj s i _ => s!"PROJ:{s}.{i}"
  | _ => "OTHER"

def headDump (path : System.FilePath) (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let h ← IO.FS.Handle.mk out .write
  let mut count := 0
  for (n, ci) in env.constants.toList do
    let (prems, concl) := telescope ci.type
    let mut ne := 0; let mut nimp := 0; let mut ninst := 0
    let mut ph : Array Json := #[]
    for (t, bi) in prems do
      match bi with
      | .default =>
        ne := ne + 1
        ph := ph.push (Json.str (headTag (stripForalls t)))
      | .instImplicit => ninst := ninst + 1
      | _ => nimp := nimp + 1
    let vh : Json := match ci.value? (allowOpaque := true) with
      | some v => Json.str (headTag (stripLams v))
      | none => Json.null
    let ca : Array Json :=
      (concl.getAppArgs.toList.take 3).toArray.map (fun a => Json.str (headTag a))
    let j := Json.mkObj [
      ("n", Json.str (toString n)),
      ("k", Json.str (kindString ci)),
      ("ch", Json.str (headTag concl)),
      ("ca", Json.arr ca),
      ("ph", Json.arr ph),
      ("ne", toJson ne), ("ni", toJson ninst), ("nm", toJson nimp),
      ("vh", vh)]
    h.putStrLn j.compress
    count := count + 1
    if count % 100000 == 0 then
      IO.println s!"  {count} constants dumped"
  IO.println s!"done: {count} constants"
  h.flush

end Mathrecord.HeadDump
