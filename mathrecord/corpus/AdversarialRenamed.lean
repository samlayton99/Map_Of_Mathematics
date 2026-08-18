/- Alpha-renamed twin of Adversarial.lean.
   Same declaration names and statements; every binder name, local hypothesis
   name, let-name, and universe parameter name is renamed. Structural identity
   (sid) of paired declarations must be unchanged. -/

namespace Corpus

universe u v

structure Point (α : Type u) where
  x : α
  y : α

def Point.swap {γ : Type u} (q : Point γ) : Point γ := ⟨q.y, q.x⟩

def depApply {A : Type u} {B : A → Type v} (g : (z : A) → B z) (z : A) : B z := g z

def mkSigma (p : Nat) : Σ w : Nat, Fin (w + 1) := ⟨p, ⟨p, Nat.lt_succ_self p⟩⟩

def withLet (p : Nat) : Nat :=
  let r := p + 1
  r * r

theorem letTactic (p : Nat) : p + 1 > 0 := by
  let w := p + 1
  show w > 0
  exact Nat.succ_pos p

theorem rwDemo (x y : Nat) (hxy : x = y) : x + y = y + y := by
  rw [hxy]

theorem existsDemo (p : Nat) : ∃ q, p < q := ⟨p + 1, Nat.lt_succ_self p⟩

def sumTo : Nat → Nat
  | 0 => 0
  | m + 1 => (m + 1) + sumTo m

theorem sumTo_ge (p : Nat) : sumTo p ≥ 0 := by
  induction p with
  | zero => exact Nat.zero_le _
  | succ j hj => exact Nat.zero_le _

class HasZero (β : Type u) where
  zero : β

instance : HasZero Nat := ⟨0⟩

def getZero (β : Type u) [HasZero β] : β := HasZero.zero

theorem getZero_nat : getZero Nat = 0 := rfl

def natToInt (p : Nat) : Int := p

def binders {x : Nat} ⦃y : Nat⦄ [HasZero Nat] (z : Nat) : Nat := x + y + z

def constFun.{s, t} {A : Type s} {B : Type t} (x : A) (_y : B) : A := x

@[reducible] def reducibleDef (p : Nat) : Nat := p + 1
@[irreducible] def irreducibleDef (p : Nat) : Nat := p + 2
opaque opaqueConst : Nat

theorem branching (p : Nat) : p + 0 = p ∧ 0 + p = p := by
  constructor
  · exact Nat.add_zero p
  · exact Nat.zero_add p

theorem twoProofsA : 2 + 2 = 4 := rfl
theorem twoProofsB : 2 + 2 = 4 := by decide

theorem hasSorry (p : Nat) : p ≤ p + 1 := by sorry

end Corpus
