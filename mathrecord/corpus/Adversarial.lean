/- Gate 1 adversarial conformance corpus.
   Each block targets a construct known to break naive representations.
   `hasSorry` is deliberate: extraction must classify it loudly, not store it silently. -/

namespace Corpus

universe u v

/- structures and projections (also: inductive, constructor, recursor decls;
   the auto-generated `Point.x` has an `Expr.proj` body) -/
structure Point (α : Type u) where
  x : α
  y : α

def Point.swap {α : Type u} (p : Point α) : Point α := ⟨p.y, p.x⟩

/- dependent functions -/
def depApply {α : Type u} {β : α → Type v} (f : (a : α) → β a) (a : α) : β a := f a

/- dependent products (Sigma with dependent second component) -/
def mkSigma (n : Nat) : Σ m : Nat, Fin (m + 1) := ⟨n, ⟨n, Nat.lt_succ_self n⟩⟩

/- local let: term-mode -/
def withLet (n : Nat) : Nat :=
  let k := n + 1
  k * k

/- local let: tactic-mode (produces an ldecl in the local context) -/
theorem letTactic (n : Nat) : n + 1 > 0 := by
  let m := n + 1
  show m > 0
  exact Nat.succ_pos n

/- equality and rewriting -/
theorem rwDemo (a b : Nat) (h : a = b) : a + b = b + b := by
  rw [h]

/- existential witness -/
theorem existsDemo (n : Nat) : ∃ m, n < m := ⟨n + 1, Nat.lt_succ_self n⟩

/- recursion (equation compiler) -/
def sumTo : Nat → Nat
  | 0 => 0
  | n + 1 => (n + 1) + sumTo n

/- induction with a branching proof state (two goals after `induction`) -/
theorem sumTo_ge (n : Nat) : sumTo n ≥ 0 := by
  induction n with
  | zero => exact Nat.zero_le _
  | succ k ih => exact Nat.zero_le _

/- typeclass synthesis -/
class HasZero (α : Type u) where
  zero : α

instance : HasZero Nat := ⟨0⟩

def getZero (α : Type u) [HasZero α] : α := HasZero.zero

theorem getZero_nat : getZero Nat = 0 := rfl

/- coercion (Nat → Int) -/
def natToInt (n : Nat) : Int := n

/- implicit, strict-implicit, instance-implicit, explicit binders -/
def binders {a : Nat} ⦃b : Nat⦄ [HasZero Nat] (c : Nat) : Nat := a + b + c

/- universe polymorphism -/
def constFun.{w, z} {α : Type w} {β : Type z} (a : α) (_b : β) : α := a

/- transparency spectrum -/
@[reducible] def reducibleDef (n : Nat) : Nat := n + 1
@[irreducible] def irreducibleDef (n : Nat) : Nat := n + 2
opaque opaqueConst : Nat

/- an explicitly branching proof state: one action, two successor goals -/
theorem branching (n : Nat) : n + 0 = n ∧ 0 + n = n := by
  constructor
  · exact Nat.add_zero n
  · exact Nat.zero_add n

/- two distinct proofs of the same proposition -/
theorem twoProofsA : 2 + 2 = 4 := rfl
theorem twoProofsB : 2 + 2 = 4 := by decide

/- unsupported on purpose: proof contains sorryAx -/
theorem hasSorry (n : Nat) : n ≤ n + 1 := by sorry

end Corpus
