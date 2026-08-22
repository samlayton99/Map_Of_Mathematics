# Blind grading batch 12 — 10 items

Each item below gives you one Lean declaration: its statement, then the proof
or construction that establishes it. After that comes the list of declarations
that proof or construction cites, in random order. Grade every candidate in
every item.

## Rubric

Grade each candidate 0-4 by its mathematical function in THIS proof/construction:
4 = a core move: the proof's central idea or decisive step depends on it
3 = a major step: substantive mathematics the proof genuinely builds on
2 = a legitimate connective step: honest but routine glue between the real steps
1 = boilerplate: bookkeeping that any formalization would need; contributes no mathematical content
0 = noise: irrelevant or purely administrative
Judge from the mathematics alone. If unsure between two grades, give the lower.
There are no quotas; a proof may have several 4s or none.

## Output

Return only a JSON object, no commentary: one key per item id, mapping each
candidate number to its grade.

```json
{"t111": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t111

Target: `Matroid.closure_disjoint_coloops_of_disjoint_coloops`

```lean
lemma closure_disjoint_coloops_of_disjoint_coloops (hX : Disjoint X (M.coloops)) :
    Disjoint (M.closure X) M.coloops
```

Proof / construction:

```lean
:=
  closure_disjoint_of_disjoint_of_subset_coloops hX Subset.rfl
```

Candidates (15), random order:

1. `Set.Subset.rfl`

```lean
theorem Subset.rfl {s : Set α} : s ⊆ s
```

2. `Matroid.closure_disjoint_of_disjoint_of_subset_coloops`

```lean
lemma closure_disjoint_of_disjoint_of_subset_coloops (hXK : Disjoint X K) (hK : K ⊆ M.coloops) :
    Disjoint (M.closure X) K
```

3. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`

```lean
class CompleteAtomicBooleanAlgebra (α : Type u) extends CompleteBooleanAlgebra α
```

4. `CompleteBooleanAlgebra.toCompleteDistribLattice`

```lean
instance (priority := 100) CompleteBooleanAlgebra.toCompleteDistribLattice
    [CompleteBooleanAlgebra α] : CompleteDistribLattice α
```

5. `Set.instCompleteAtomicBooleanAlgebra`

```lean
instance instCompleteAtomicBooleanAlgebra : CompleteAtomicBooleanAlgebra (Set α)
```

6. `CompleteBooleanAlgebra.toCompleteLattice`

```lean
class CompleteBooleanAlgebra (α) extends CompleteLattice α, BooleanAlgebra α
```

7. `CompleteDistribLattice.toFrame`

```lean
class CompleteDistribLattice (α : Type*) extends Frame α, Coframe α, BiheytingAlgebra α
```

8. `HeytingAlgebra.toOrderBot`

```lean
class HeytingAlgebra (α : Type*) extends GeneralizedHeytingAlgebra α, OrderBot α, Compl α
```

9. `Set`

```lean
def Set (α : Type u)
```

10. `ChainCompletePartialOrder.toPartialOrder`

```lean
class ChainCompletePartialOrder (α : Type*) extends PartialOrder α
```

11. `Matroid`

```lean
structure Matroid (α : Type*)
```

12. `Matroid.coloops`

```lean
def coloops (M : Matroid α)
```

13. `Order.Frame.toHeytingAlgebra`

```lean
class Order.Frame (α : Type*) extends CompleteLattice α, HeytingAlgebra α
```

14. `ChainCompletePartialOrder.instOfCompleteLattice`

```lean
ChainCompletePartialOrder.instOfCompleteLattice
```

15. `Disjoint`

```lean
def Disjoint (a b : α) : Prop
```


---

## t112

Target: `Encodable.instAntisymmPreimageNatCoeEmbeddingEncode'Le`

```lean
instance {α} [Encodable α] : Std.Antisymm (Encodable.encode' α ⁻¹'o (· ≤ ·))
```

Proof / construction:

```lean
:=
  (RelEmbedding.preimage _ _).antisymm
```

Candidates (11), random order:

1. `Function.instFunLikeEmbedding`

```lean
instance {α : Sort u} {β : Sort v} : FunLike (α ↪ β) α β
```

2. `Nat`

```lean
inductive Nat
```

3. `Order.Preimage`

```lean
def Order.Preimage (f : α → β) (s : β → β → Prop) (x y : α) : Prop
```

4. `Function.Embedding`

```lean
structure Embedding (α : Sort*) (β : Sort*)
```

5. `Encodable.encode'`

```lean
def encode' (α) [Encodable α] : α ↪ ℕ
```

6. `RelEmbedding.preimage`

```lean
def preimage (f : α ↪ β) (s : β → β → Prop) : f ⁻¹'o s ↪r s
```

7. `RelEmbedding.antisymm`

```lean
protected theorem antisymm : ∀ (_ : r ↪r s) [Std.Antisymm s], Std.Antisymm r
  | ⟨f, o⟩, ⟨H⟩ => ⟨fun _ _ h₁ h₂ => f.inj' (H _ _ (o.2 h₁) (o.2 h₂))⟩
```

8. `Encodable`

```lean
class Encodable (α : Type*)
```

9. `LE.le`

```lean
le : α → α → Prop
```

10. `instLENat`

```lean
instance instLENat : LE Nat
```

11. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```


---

## t113

Target: `Monoid.Coprod.lift_swap`

```lean
theorem lift_swap (f : M →* P) (g : N →* P) (x : N ∗ M) : lift f g (swap N M x) = lift g f x
```

Proof / construction:

```lean
:=
  DFunLike.congr_fun (lift_comp_swap f g) x
```

Candidates (13), random order:

1. `DFunLike.congr_fun`

```lean
protected theorem congr_fun {f g : F} (h₁ : f = g) (x : α) : f x = g x
```

2. `MonoidHom.instFunLike`

```lean
instance MonoidHom.instFunLike : FunLike (M →* N) M N
```

3. `MonoidHom.comp`

```lean
def MonoidHom.comp [MulOne M] [MulOne N] [MulOne P] (hnp : N →* P) (hmn : M →* N) :
    M →* P
```

4. `MulOneClass`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

5. `Monoid.toMulOneClass`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

6. `Monoid`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

7. `Monoid.Coprod.swap`

```lean
def swap : M ∗ N →* N ∗ M
```

8. `Monoid.Coprod.instMulOneClass`

```lean
@[to_additive] protected instance : MulOneClass (M ∗ N)
```

9. `MonoidHom`

```lean
structure MonoidHom (M : Type*) (N : Type*) [MulOne M] [MulOne N]
  extends OneHom M N, M →ₙ* N
```

10. `Monoid.Coprod.lift_comp_swap`

```lean
theorem lift_comp_swap (f : M →* P) (g : N →* P) : (lift f g).comp (swap N M) = lift g f
```

11. `Monoid.Coprod`

```lean
def Coprod (M N : Type*) [MulOneClass M] [MulOneClass N]
```

12. `Monoid.Coprod.lift`

```lean
def lift (f : M →* P) (g : N →* P) : (M ∗ N) →* P
```

13. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```


---

## t114

Target: `Polynomial.coeff_ofNat_mul`

```lean
@[simp] lemma coeff_ofNat_mul {a k : ℕ} [Nat.AtLeastTwo a] :
    coeff ((ofNat(a) : R[X]) * p) k = ofNat(a) * coeff p k
```

Proof / construction:

```lean
:= coeff_C_mul _
```

Candidates (10), random order:

1. `AddCommMonoidWithOne.toAddMonoidWithOne`

```lean
class AddCommMonoidWithOne (R : Type*) extends AddMonoidWithOne R, AddCommMonoid R
```

2. `NonAssocSemiring.toAddCommMonoidWithOne`

```lean
class NonAssocSemiring (α : Type u) extends NonUnitalNonAssocSemiring α, MulZeroOneClass α,
    AddCommMonoidWithOne α
```

3. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

4. `Nat.AtLeastTwo`

```lean
class AtLeastTwo (n : ℕ) : Prop
```

5. `Nat.cast`

```lean
protected def Nat.cast {R : Type u} [NatCast R] : Nat → R
```

6. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

7. `Polynomial.coeff_C_mul`

```lean
theorem coeff_C_mul (p : R[X]) : coeff (C a * p) n = a * coeff p n
```

8. `Polynomial`

```lean
structure Polynomial (R : Type*) [Semiring R]
```

9. `Nat`

```lean
inductive Nat
```

10. `AddMonoidWithOne.toNatCast`

```lean
class AddMonoidWithOne (R : Type*) extends NatCast R, AddMonoid R, One R
```


---

## t115

Target: `IsUltrametricDist.isUltrametricDist_iff_isNonarchimedean_nnnorm`

```lean
lemma isUltrametricDist_iff_isNonarchimedean_nnnorm {R} [SeminormedAddCommGroup R] :
    IsUltrametricDist R ↔ IsNonarchimedean (‖·‖₊ : R → ℝ)
```

Proof / construction:

```lean
:=
  ⟨fun h => h.isNonarchimedean_norm, IsUltrametricDist.isUltrametricDist_of_isNonarchimedean_norm⟩
```

Candidates (19), random order:

1. `NNReal.toReal`

```lean
@[coe] def toReal : ℝ≥0 → ℝ
```

2. `IsUltrametricDist.isNonarchimedean_norm`

```lean
lemma isNonarchimedean_norm {R} [SeminormedAddCommGroup R] [IsUltrametricDist R] :
    IsNonarchimedean (‖·‖ : R → ℝ)
```

3. `Iff.intro`

```lean
structure Iff (a b : Prop) : Prop
```

4. `AddCommGroup.toAddCommMonoid`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

5. `SeminormedAddCommGroup.toPseudoMetricSpace`

```lean
class SeminormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E,
  PseudoMetricSpace E
```

6. `PseudoMetricSpace.toDist`

```lean
class PseudoMetricSpace (α : Type u) : Type u extends Dist α
```

7. `SeminormedAddGroup.toNNNorm`

```lean
instance (priority := 100) SeminormedGroup.toNNNorm : NNNorm E
```

8. `AddCommMonoid.toAddCommSemigroup`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

9. `Real`

```lean
structure Real
```

10. `SeminormedAddCommGroup.toSeminormedAddGroup`

```lean
SeminormedAddCommGroup.toSeminormedAddGroup
```

11. `Real.linearOrder`

```lean
noncomputable instance linearOrder : LinearOrder ℝ
```

12. `NNNorm.nnnorm`

```lean
nnnorm : E → ℝ≥0
```

13. `SeminormedAddCommGroup`

```lean
class SeminormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E,
  PseudoMetricSpace E
```

14. `IsUltrametricDist.isUltrametricDist_of_isNonarchimedean_norm`

```lean
lemma isUltrametricDist_of_isNonarchimedean_norm {S' : Type*} [SeminormedAddGroup S']
    (h : IsNonarchimedean (norm : S' → ℝ)) : IsUltrametricDist S'
```

15. `AddCommSemigroup.toAddCommMagma`

```lean
class AddCommSemigroup (G : Type u) extends AddSemigroup G, AddCommMagma G
```

16. `SeminormedAddCommGroup.toAddCommGroup`

```lean
class SeminormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E,
  PseudoMetricSpace E
```

17. `IsUltrametricDist`

```lean
class IsUltrametricDist (X : Type*) [Dist X] : Prop
```

18. `IsNonarchimedean`

```lean
def IsNonarchimedean {α : Type*} [Add α] (f : α → R) : Prop
```

19. `AddCommMagma.toAdd`

```lean
class AddCommMagma (G : Type u) extends Add G
```


---

## t116

Target: `Metric.unitClosedBall.instSemigroupWithZero`

```lean
instance Metric.unitClosedBall.instSemigroupWithZero [NonUnitalSeminormedRing 𝕜] :
    SemigroupWithZero (closedBall (0 : 𝕜) 1)
```

Proof / construction:

```lean
where
  zero_mul _ := Subtype.ext <| zero_mul _
  mul_zero _ := Subtype.ext <| mul_zero _
```

Candidates (17), random order:

1. `Zero.toOfNat0`

```lean
instance (priority := 300) Zero.toOfNat0 {α} [Zero α] : OfNat α (nat_lit 0)
```

2. `NonUnitalNonAssocSemiring.toMulZeroClass`

```lean
class NonUnitalNonAssocSemiring (α : Type u) extends AddCommMonoid α, Distrib α, MulZeroClass α
```

3. `MulZeroClass.toZero`

```lean
class MulZeroClass (M₀ : Type u) extends Mul M₀, Zero M₀
```

4. `NonUnitalSeminormedRing.toNonUnitalRing`

```lean
class NonUnitalSeminormedRing (α : Type*) extends Norm α, NonUnitalRing α,
  PseudoMetricSpace α
```

5. `One.toOfNat1`

```lean
instance (priority := 300) One.toOfNat1 {α} [One α] : OfNat α (nat_lit 1)
```

6. `Metric.unitClosedBall.instZero`

```lean
instance Metric.unitClosedBall.instZero [Zero 𝕜] [PseudoMetricSpace 𝕜] :
    Zero (closedBall (0 : 𝕜) 1)
```

7. `Real`

```lean
structure Real
```

8. `NonUnitalSeminormedRing`

```lean
class NonUnitalSeminormedRing (α : Type*) extends Norm α, NonUnitalRing α,
  PseudoMetricSpace α
```

9. `NonUnitalRing.toNonUnitalNonAssocRing`

```lean
class NonUnitalRing (α : Type*) extends NonUnitalNonAssocRing α, NonUnitalSemiring α
```

10. `Metric.closedBall`

```lean
def closedBall (x : α) (ε : ℝ)
```

11. `NonUnitalSeminormedRing.toPseudoMetricSpace`

```lean
class NonUnitalSeminormedRing (α : Type*) extends Norm α, NonUnitalRing α,
  PseudoMetricSpace α
```

12. `NonUnitalNonAssocRing.toNonUnitalNonAssocSemiring`

```lean
class NonUnitalNonAssocRing (α : Type u) extends AddCommGroup α, NonUnitalNonAssocSemiring α
```

13. `OfNat.ofNat`

```lean
ofNat : α
```

14. `Set.Elem`

```lean
@[coe, reducible] def Elem (s : Set α) : Type u
```

15. `Metric.unitClosedBall.instSemigroup`

```lean
instance Metric.unitClosedBall.instSemigroup [NonUnitalSeminormedRing 𝕜] :
    Semigroup (closedBall (0 : 𝕜) 1)
```

16. `SemigroupWithZero.mk`

```lean
class SemigroupWithZero (S₀ : Type u) extends Semigroup S₀, MulZeroClass S₀
```

17. `Real.instOne`

```lean
instance : One ℝ
```


---

## t117

Target: `TensorProduct.liftAux`

```lean
def liftAux : M ⊗[R] N →+ P₂
```

Proof / construction:

```lean
:=
  liftAddHom (LinearMap.toAddMonoidHom'.comp <| f'.toAddMonoidHom)
    fun r m n => by dsimp; rw [LinearMap.map_smulₛₗ₂, map_smulₛₗ]
```

Candidates (19), random order:

1. `LinearMap.addMonoid`

```lean
instance addMonoid : AddMonoid (M →ₛₗ[σ₁₂] M₂)
```

2. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

3. `AddMonoidHom.comp`

```lean
-- Mathlib generates `AddMonoidHom.comp` from the declaration below.
def MonoidHom.comp [MulOne M] [MulOne N] [MulOne P] (hnp : N →* P) (hmn : M →* N) :
    M →* P
```

4. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

5. `LinearMap`

```lean
structure LinearMap {R S : Type*} [Semiring R] [Semiring S] (σ : R →+* S) (M : Type*)
    (M₂ : Type*) [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends
    AddHom M M₂, MulActionHom σ M M₂
```

6. `LinearMap.toAddMonoidHom`

```lean
def toAddMonoidHom {modM₁ : Module R M₁} {modM₂ : Module S M₂} {σ : R →+* S} (f : M₁ →ₛₗ[σ] M₂) :
    M₁ →+ M₂
```

7. `LinearMap.module`

```lean
instance module : Module S (M →ₛₗ[σ₁₂] M₂)
```

8. `LinearMap.toAddMonoidHom'`

```lean
def toAddMonoidHom' : (M →ₛₗ[σ₁₂] M₂) →+ M →+ M₂
```

9. `AddMonoidHom.instAddCommMonoid`

```lean
instance AddMonoid.End.instAddCommMonoid [AddCommMonoid M] : AddCommMonoid (AddMonoid.End M)
```

10. `LinearMap.addCommMonoid`

```lean
instance addCommMonoid : AddCommMonoid (M →ₛₗ[σ₁₂] M₂)
```

11. `AddCommMonoid.toAddMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

12. `CommSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

13. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

14. `TensorProduct.liftAddHom`

```lean
def liftAddHom (f : M →+ N →+ P)
    (hf : ∀ (r : R) (m : M) (n : N), f (r • m) n = f m (r • n)) :
    M ⊗[R] N →+ P
```

15. `RingHom`

```lean
structure RingHom (α : Type*) (β : Type*) [NonAssocSemiring α] [NonAssocSemiring β] extends
  α →* β, α →+ β, α →ₙ+* β, α →*₀ β
```

16. `AddZeroClass.toAddZero`

```lean
class AddZeroClass (M : Type u) extends AddZero M
```

17. `AddMonoid.toAddZeroClass`

```lean
class AddMonoid (M : Type u) extends AddSemigroup M, AddZeroClass M, NSMul M
```

18. `AddMonoidHom`

```lean
structure AddMonoidHom (M : Type*) (N : Type*) [AddZero M] [AddZero N]
  extends ZeroHom M N, AddHom M N
```

19. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```


---

## t118

Target: `CategoryTheory.ObjectProperty.isClosedUnderColimitsOfShape_iff_unop`

```lean
lemma isClosedUnderColimitsOfShape_iff_unop :
    Q.IsClosedUnderColimitsOfShape J ↔
      Q.unop.IsClosedUnderLimitsOfShape Jᵒᵖ
```

Proof / construction:

```lean
:=
  (Q.unop.isClosedUnderLimitsOfShape_op_iff_op J).symm
```

Candidates (12), random order:

1. `CategoryTheory.ObjectProperty.IsClosedUnderColimitsOfShape`

```lean
class IsClosedUnderColimitsOfShape (P : ObjectProperty C) (J : Type u') [Category.{v'} J]
```

2. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

3. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

4. `CategoryTheory.ObjectProperty.op`

```lean
protected def op (P : ObjectProperty C) : ObjectProperty Cᵒᵖ
```

5. `CategoryTheory.ObjectProperty`

```lean
abbrev ObjectProperty (C : Type u) [CategoryStruct.{v} C] : Type u
```

6. `Opposite`

```lean
structure Opposite
```

7. `Iff.symm`

```lean
@[symm] theorem Iff.symm (h : a ↔ b) : b ↔ a
```

8. `CategoryTheory.ObjectProperty.isClosedUnderLimitsOfShape_op_iff_op`

```lean
lemma isClosedUnderLimitsOfShape_op_iff_op :
    P.IsClosedUnderLimitsOfShape Jᵒᵖ ↔
      P.op.IsClosedUnderColimitsOfShape J
```

9. `CategoryTheory.ObjectProperty.IsClosedUnderLimitsOfShape`

```lean
class IsClosedUnderLimitsOfShape (P : ObjectProperty C) (J : Type u') [Category.{v'} J]
```

10. `CategoryTheory.ObjectProperty.unop`

```lean
protected def unop (P : ObjectProperty Cᵒᵖ) : ObjectProperty C
```

11. `CategoryTheory.CategoryStruct.opposite`

```lean
instance CategoryStruct.opposite : CategoryStruct.{v₁} Cᵒᵖ
```

12. `CategoryTheory.Category.opposite`

```lean
instance Category.opposite : Category.{v₁} Cᵒᵖ
```


---

## t119

Target: `Function.Injective.exists_ne`

```lean
protected theorem Function.Injective.exists_ne [Nontrivial α] {f : α → β}
    (hf : Function.Injective f) (y : β) : ∃ x, f x ≠ y
```

Proof / construction:

```lean
:= by
  rcases exists_pair_ne α with ⟨x₁, x₂, hx⟩
  by_cases h : f x₂ = y
  · exact ⟨x₁, (hf.ne_iff' h).2 hx⟩
  · exact ⟨x₂, h⟩
```

Candidates (13), random order:

1. `Function.Injective.ne_iff'`

```lean
theorem Injective.ne_iff' (hf : Injective f) {x y : α} {z : β} (h : f y = z) : f x ≠ z ↔ x ≠ y
```

2. `Eq`

```lean
inductive Eq : α → α → Prop
```

3. `Exists.intro`

```lean
| intro (w : α) (h : p w) : Exists p
```

4. `Iff.mpr`

```lean
mpr : b → a
```

5. `exists_pair_ne`

```lean
theorem exists_pair_ne (α : Type*) [Nontrivial α] : ∃ x y : α, x ≠ y
```

6. `Not`

```lean
@[implicit_reducible] def Not (a : Prop) : Prop
```

7. `Exists`

```lean
inductive Exists {α : Sort u} (p : α → Prop) : Prop
```

8. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

9. `Classical.propDecidable`

```lean
noncomputable scoped instance (priority := low) propDecidable (a : Prop) : Decidable a
```

10. `dite`

```lean
def dite {α : Sort u} (c : Prop) [h : Decidable c] (t : c → α) (e : Not c → α) : α
```

11. `Function.Injective`

```lean
def Injective (f : α → β) : Prop
```

12. `Exists.casesOn`

```lean
Exists.casesOn
```

13. `Nontrivial`

```lean
class Nontrivial (α : Type*) : Prop
```


---

## t120

Target: `CategoryTheory.hasExactColimitsOfShape_discrete_finite`

```lean
noncomputable instance hasExactColimitsOfShape_discrete_finite (J : Type*) [Finite J] :
    HasExactColimitsOfShape (Discrete J) C
```

Proof / construction:

```lean
where
  preservesFiniteLimits := preservesFiniteLimits_of_natIso HasBiproductsOfShape.colimIsoLim.symm
```

Candidates (14), random order:

1. `CategoryTheory.Functor.category`

```lean
instance Functor.category : Category.{max u₁ v₂} (C ⥤ D)
```

2. `CategoryTheory.Limits.HasBiproductsOfShape.colimIsoLim`

```lean
def HasBiproductsOfShape.colimIsoLim [HasBiproductsOfShape J C] :
    colim (J := Discrete J) (C := C) ≅ lim
```

3. `CategoryTheory.Limits.HasZeroMorphisms`

```lean
class HasZeroMorphisms
```

4. `CategoryTheory.Limits.lim`

```lean
def lim : (J ⥤ C) ⥤ C
```

5. `CategoryTheory.Limits.colim`

```lean
def colim : (J ⥤ C) ⥤ C
```

6. `CategoryTheory.HasExactColimitsOfShape.mk`

```lean
class HasExactColimitsOfShape (J : Type u') [Category.{v'} J] (C : Type u) [Category.{v} C]
    [HasColimitsOfShape J C]
```

7. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

8. `CategoryTheory.Discrete`

```lean
structure Discrete (α : Type u₁)
```

9. `CategoryTheory.Iso.symm`

```lean
def symm (I : X ≅ Y) : Y ≅ X
```

10. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

11. `CategoryTheory.Limits.HasFiniteBiproducts`

```lean
class HasFiniteBiproducts : Prop
```

12. `CategoryTheory.discreteCategory`

```lean
instance discreteCategory (α : Type u₁) : SmallCategory (Discrete α)
```

13. `CategoryTheory.Limits.preservesFiniteLimits_of_natIso`

```lean
lemma preservesFiniteLimits_of_natIso {F G : C ⥤ D} (h : F ≅ G) [PreservesFiniteLimits F] :
    PreservesFiniteLimits G
```

14. `Finite`

```lean
class inductive Finite (α : Sort*) : Prop
  | intro {n : ℕ} : α ≃ Fin n → Finite _
```


---
