# Blind grading batch 01 — 10 items

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
{"t001": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t001

Target: `FreeRing.of_ne_one`

```lean
theorem of_ne_one (x : α) : of x ≠ 1
```

Proof / construction:

```lean
:= FreeAbelianGroup.of_injective.ne <| FreeMonoid.of_ne_one _
```

Candidates (15), random order:

1. `CancelMonoid.toRightCancelMonoid`

```lean
class CancelMonoid (M : Type u) extends LeftCancelMonoid M, RightCancelMonoid M
```

2. `One.toOfNat1`

```lean
instance (priority := 300) One.toOfNat1 {α} [One α] : OfNat α (nat_lit 1)
```

3. `FreeAbelianGroup.of_injective`

```lean
theorem of_injective : Function.Injective (of : α → FreeAbelianGroup α)
```

4. `Function.Injective.ne`

```lean
theorem Injective.ne (hf : Injective f) {a₁ a₂ : α} : a₁ ≠ a₂ → f a₁ ≠ f a₂
```

5. `RightCancelMonoid.toMonoid`

```lean
class RightCancelMonoid (M : Type u) extends Monoid M, RightCancelSemigroup M
```

6. `FreeAbelianGroup`

```lean
def FreeAbelianGroup : Type u
```

7. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

8. `Monoid.toMulOneClass`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

9. `FreeMonoid.instCancelMonoid`

```lean
instance : CancelMonoid (FreeMonoid α)
```

10. `MulOne.toOne`

```lean
class MulOne (M : Type*) extends One M, Mul M
```

11. `FreeMonoid.of_ne_one`

```lean
theorem of_ne_one (a : α) : of a ≠ 1
```

12. `FreeMonoid.of`

```lean
def of (x : α) : FreeMonoid α
```

13. `FreeAbelianGroup.of`

```lean
def of (x : α) : FreeAbelianGroup α
```

14. `FreeMonoid`

```lean
def FreeMonoid (α)
```

15. `OfNat.ofNat`

```lean
ofNat : α
```


---

## t002

Target: `Matrix.instPartialOrder`

```lean
abbrev instPartialOrder : PartialOrder (Matrix n n 𝕜)
```

Proof / construction:

```lean
where
  le_antisymm A B h₁ h₂ := by
    simpa [sub_eq_zero, eq_comm] using le_antisymm_aux h₁
     (by simpa only [← neg_sub B, le_iff] using h₂)
```

Candidates (6), random order:

1. `RCLike`

```lean
class RCLike (K : semiOutParam Type*) extends DenselyNormedField K, StarRing K,
    NormedAlgebra ℝ K, CompleteSpace K
```

2. `PartialOrder.mk`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

3. `LE.le`

```lean
le : α → α → Prop
```

4. `Matrix.instPreOrder`

```lean
abbrev instPreOrder : Preorder (Matrix n n 𝕜)
```

5. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

6. `Matrix`

```lean
def Matrix (m : Type u) (n : Type u') (α : Type v) : Type max u u' v
```


---

## t003

Target: `Scott.IsωSup`

```lean
def IsωSup {α : Type u} [Preorder α] (c : Chain α) (x : α) : Prop
```

Proof / construction:

```lean
:=
  (∀ i, c i ≤ x) ∧ ∀ y, (∀ i, c i ≤ y) → x ≤ y
```

Candidates (8), random order:

1. `And`

```lean
structure And (a b : Prop) : Prop
```

2. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

3. `OmegaCompletePartialOrder.Chain.instFunLikeNat`

```lean
instance : FunLike (Chain α) ℕ α
```

4. `Nat`

```lean
inductive Nat
```

5. `OmegaCompletePartialOrder.Chain`

```lean
structure Chain (α : Type u) [Preorder α] extends ℕ →o α
```

6. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

7. `LE.le`

```lean
le : α → α → Prop
```

8. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```


---

## t004

Target: `MeasureTheory.Measure.ae_ae_of_ae_prod`

```lean
theorem ae_ae_of_ae_prod {p : α × β → Prop} (h : ∀ᵐ z ∂μ.prod ν, p z) :
    ∀ᵐ x ∂μ, ∀ᵐ y ∂ν, p (x, y)
```

Proof / construction:

```lean
:=
  measure_ae_null_of_prod_null h
```

Candidates (14), random order:

1. `MeasureTheory.SFinite`

```lean
class SFinite (μ : Measure α) : Prop
```

2. `MeasurableSpace`

```lean
@[class] structure MeasurableSpace (α : Type*)
```

3. `Set.instCompl`

```lean
instance : Compl (Set α)
```

4. `MeasureTheory.Measure.prod`

```lean
MeasureTheory.Measure.prod
```

5. `Set`

```lean
def Set (α : Type u)
```

6. `Filter.Eventually`

```lean
protected def Eventually (p : α → Prop) (f : Filter α) : Prop
```

7. `MeasureTheory.Measure.measure_ae_null_of_prod_null`

```lean
theorem measure_ae_null_of_prod_null {s : Set (α × β)} (h : μ.prod ν s = 0) :
    (fun x => ν (Prod.mk x ⁻¹' s)) =ᵐ[μ] 0
```

8. `MeasureTheory.Measure.instFunLike`

```lean
instance Measure.instFunLike [MeasurableSpace α] : FunLike (Measure α) (Set α) ℝ≥0∞
```

9. `Prod`

```lean
structure Prod (α : Type u) (β : Type v)
```

10. `MeasureTheory.ae`

```lean
def ae (μ : F) : Filter α
```

11. `Set.ofPred`

```lean
def Set.ofPred {α : Type u} (p : α → Prop) : Set α
```

12. `Prod.instMeasurableSpace`

```lean
instance Prod.instMeasurableSpace {α β} [m₁ : MeasurableSpace α] [m₂ : MeasurableSpace β] :
    MeasurableSpace (α × β)
```

13. `Compl.compl`

```lean
compl : α → α
```

14. `MeasureTheory.Measure`

```lean
structure Measure (α : Type*) [MeasurableSpace α] extends OuterMeasure α
```


---

## t005

Target: `edist_nndist`

```lean
theorem edist_nndist (x y : α) : edist x y = nndist x y
```

Proof / construction:

```lean
:= by
  rw [edist_dist, dist_nndist, ENNReal.ofReal_coe_nnreal]
```

Candidates (20), random order:

1. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

2. `edist_dist`

```lean
theorem edist_dist (x y : α) : edist x y = ENNReal.ofReal (dist x y)
```

3. `ENNReal.ofReal`

```lean
protected def ofReal (r : Real) : ℝ≥0∞
```

4. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

5. `NNDist.nndist`

```lean
nndist : α → α → ℝ≥0
```

6. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

7. `Eq.refl`

```lean
| refl (a : α) : Eq a a
```

8. `ENNReal`

```lean
def ENNReal
```

9. `Real`

```lean
structure Real
```

10. `PseudoMetricSpace.toEDist`

```lean
instance (priority := 200) PseudoMetricSpace.toEDist : EDist α
```

11. `PseudoMetricSpace.toDist`

```lean
class PseudoMetricSpace (α : Type u) : Type u extends Dist α
```

12. `Dist.dist`

```lean
dist : α → α → ℝ
```

13. `ENNReal.ofReal_coe_nnreal`

```lean
@[simp] theorem ofReal_coe_nnreal : ENNReal.ofReal p = p
```

14. `dist_nndist`

```lean
theorem dist_nndist (x y : α) : dist x y = nndist x y
```

15. `PseudoMetricSpace`

```lean
class PseudoMetricSpace (α : Type u) : Type u extends Dist α
```

16. `PseudoMetricSpace.toNNDist`

```lean
instance (priority := 100) PseudoMetricSpace.toNNDist : NNDist α
```

17. `Eq`

```lean
inductive Eq : α → α → Prop
```

18. `NNReal.toReal`

```lean
@[coe] def toReal : ℝ≥0 → ℝ
```

19. `EDist.edist`

```lean
edist : α → α → ℝ≥0∞
```

20. `ENNReal.ofNNReal`

```lean
@[coe, match_pattern] def ofNNReal : ℝ≥0 → ℝ≥0∞
```


---

## t006

Target: `PreAbstractSimplicialComplex.instSetLikeFinset`

```lean
instance : SetLike (PreAbstractSimplicialComplex ι) (Finset ι)
```

Proof / construction:

```lean
where
  coe K := K.faces
  coe_injective K _ _ := by
    cases K
    congr
```

Candidates (6), random order:

1. `PreAbstractSimplicialComplex`

```lean
structure PreAbstractSimplicialComplex
```

2. `SetLike.mk`

```lean
class SetLike (A : Type*) (B : outParam Type*)
```

3. `Eq`

```lean
inductive Eq : α → α → Prop
```

4. `PreAbstractSimplicialComplex.faces`

```lean
faces : Set (Finset ι)
```

5. `Finset`

```lean
structure Finset (α : Type*)
```

6. `Set`

```lean
def Set (α : Type u)
```


---

## t007

Target: `SimpleGraph.Hom.map`

```lean
protected def map (f : V → W) (G : SimpleGraph V) (h : ∀ {u v}, G.Adj u v → f u ≠ f v) :
    G →g G.map f
```

Proof / construction:

```lean
where
  toFun := f
  map_rel' {u v} hadj := ⟨h hadj, u, v, hadj, rfl, rfl⟩
```

Candidates (5), random order:

1. `SimpleGraph.Adj`

```lean
Adj : V → V → Prop
```

2. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

3. `SimpleGraph`

```lean
structure SimpleGraph (V : Type u)
```

4. `SimpleGraph.map`

```lean
protected def map (f : V → W) (G : SimpleGraph V) : SimpleGraph W
```

5. `RelHom.mk`

```lean
structure RelHom {α β : Type*} (r : α → α → Prop) (s : β → β → Prop)
```


---

## t008

Target: `Ordinal.one_toType_eq`

```lean
theorem one_toType_eq (x : ToType 1) : x = enum (· < ·) ⟨0, by simp⟩
```

Proof / construction:

```lean
:=
  Unique.eq_default x
```

Candidates (7), random order:

1. `OfNat.ofNat`

```lean
ofNat : α
```

2. `Ordinal`

```lean
def Ordinal : Type (u + 1)
```

3. `Ordinal.uniqueToTypeOne`

```lean
instance uniqueToTypeOne : Unique (ToType 1)
```

4. `Ordinal.ToType`

```lean
def Ordinal.ToType (o : Ordinal.{u}) : Type u
```

5. `Unique.eq_default`

```lean
theorem eq_default (a : α) : a = default
```

6. `One.toOfNat1`

```lean
instance (priority := 300) One.toOfNat1 {α} [One α] : OfNat α (nat_lit 1)
```

7. `Ordinal.one`

```lean
instance one : One Ordinal
```


---

## t009

Target: `Complex.conjAe`

```lean
def conjAe : ℂ ≃ₐ[ℝ] ℂ
```

Proof / construction:

```lean
:=
  { conj with
    invFun := conj
    left_inv := star_star
    right_inv := star_star
    commutes' := conj_ofReal }
```

Candidates (24), random order:

1. `Complex.instCommSemiring`

```lean
instance : CommSemiring ℂ
```

2. `AlgEquiv.mk`

```lean
structure AlgEquiv (R : Type u) (A : Type v) (B : Type w) [CommSemiring R] [Semiring A] [Semiring B]
  [Algebra R A] [Algebra R B] extends A ≃ B, A ≃* B, A ≃+ B, A ≃+* B
```

3. `NonAssocSemiring.toMulZeroOneClass`

```lean
class NonAssocSemiring (α : Type u) extends NonUnitalNonAssocSemiring α, MulZeroOneClass α,
    AddCommMonoidWithOne α
```

4. `Complex.instStarRing`

```lean
instance : StarRing ℂ
```

5. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

6. `Equiv.mk`

```lean
structure Equiv (α β : Sort*)
```

7. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

8. `starRingEnd`

```lean
def starRingEnd : R →+* R
```

9. `MulOne.toOne`

```lean
class MulOne (M : Type*) extends One M, Mul M
```

10. `Real.instCommSemiring`

```lean
instance : CommSemiring ℝ
```

11. `Real`

```lean
structure Real
```

12. `MulZeroOneClass.toMulOneClass`

```lean
class MulZeroOneClass (M₀ : Type u) extends MulOneClass M₀, MulZeroClass M₀
```

13. `RingHom.toMonoidHom`

```lean
RingHom.toMonoidHom
```

14. `Complex`

```lean
structure Complex : Type
```

15. `Complex.conj_ofReal`

```lean
theorem conj_ofReal (r : ℝ) : conj (r : ℂ) = r
```

16. `OneHom.toFun`

```lean
protected toFun : M → N
```

17. `Complex.instSemiring`

```lean
instance : Semiring ℂ
```

18. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

19. `RingHom`

```lean
structure RingHom (α : Type*) (β : Type*) [NonAssocSemiring α] [NonAssocSemiring β] extends
  α →* β, α →+ β, α →ₙ+* β, α →*₀ β
```

20. `MonoidHom.toOneHom`

```lean
structure MonoidHom (M : Type*) (N : Type*) [MulOne M] [MulOne N]
  extends OneHom M N, M →ₙ* N
```

21. `Algebra.id`

```lean
instance (priority := 1100) id : Algebra R R
```

22. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

23. `Algebra.complexToReal`

```lean
instance (priority := 900) Algebra.complexToReal {A : Type*} [Semiring A] [Algebra ℂ A] :
    Algebra ℝ A
```

24. `RingHom.instFunLike`

```lean
instance instFunLike : FunLike (α →+* β) α β
```


---

## t010

Target: `List.sortedLT_iff_isChain`

```lean
theorem sortedLT_iff_isChain : l.SortedLT ↔ IsChain (· < ·) l
```

Proof / construction:

```lean
:=
  sortedLT_iff_pairwise.trans isChain_iff_pairwise.symm
```

Candidates (12), random order:

1. `List`

```lean
inductive List (α : Type u)
```

2. `instTransLT`

```lean
instance instTransLT : @Trans α α α LT.lt LT.lt LT.lt
```

3. `Iff.trans`

```lean
theorem Iff.trans (h₁ : a ↔ b) (h₂ : b ↔ c) : a ↔ c
```

4. `Iff.symm`

```lean
@[symm] theorem Iff.symm (h : a ↔ b) : b ↔ a
```

5. `List.sortedLT_iff_pairwise`

```lean
@[grind =] theorem sortedLT_iff_pairwise : l.SortedLT ↔ l.Pairwise (· < ·)
```

6. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

7. `List.IsChain`

```lean
inductive IsChain (R : α → α → Prop) : List α → Prop
```

8. `Preorder.toLT`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

9. `List.isChain_iff_pairwise`

```lean
theorem isChain_iff_pairwise [Trans R R R] : IsChain R l ↔ Pairwise R l
```

10. `List.Pairwise`

```lean
inductive Pairwise : List α → Prop
  /-- All elements of the empty list are vacuously pairwise related. -/
  | nil : Pairwise []
  /--
  A nonempty list is pairwise related with `R` if the head is related to every element of the tail
  and the tail is itself pairwise related.

  That is, `a :: l` is `Pairwise R` if:
   * `R` relates `a` to every element of `l`
   * `l` is `Pairwise R`.
  -/
  | cons : ∀ {a : α} {l : List α}, (∀ a', a' ∈ l → R a a') → Pairwise l → Pairwise (a :: l)
```

11. `LT.lt`

```lean
lt : α → α → Prop
```

12. `List.SortedLT`

```lean
def SortedLT (l : List α)
```


---
