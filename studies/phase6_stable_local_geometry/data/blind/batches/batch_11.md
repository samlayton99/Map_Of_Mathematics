# Blind grading batch 11 — 10 items

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
{"t101": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t101

Target: `ModelWithCorners.toPartialEquiv_coe_symm`

```lean
theorem toPartialEquiv_coe_symm : (I.toPartialEquiv.symm : E → H) = I.symm
```

Proof / construction:

```lean
:=
  rfl
```

Candidates (11), random order:

1. `NormedSpace`

```lean
class NormedSpace (𝕜 : Type*) (E : Type*) [NormedField 𝕜] [SeminormedAddCommGroup E]
    extends Module 𝕜 E
```

2. `NontriviallyNormedField`

```lean
class NontriviallyNormedField (α : Type*) extends NormedField α
```

3. `NontriviallyNormedField.toNormedField`

```lean
class NontriviallyNormedField (α : Type*) extends NormedField α
```

4. `PartialEquiv.toFun`

```lean
toFun : α → β
```

5. `NormedAddCommGroup.toSeminormedAddCommGroup`

```lean
NormedAddCommGroup.toSeminormedAddCommGroup
```

6. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

7. `ModelWithCorners.toPartialEquiv`

```lean
structure ModelWithCorners (𝕜 : Type*) [NontriviallyNormedField 𝕜] (E : Type*)
    [NormedAddCommGroup E] [NormedSpace 𝕜 E] (H : Type*) [TopologicalSpace H] extends
    PartialEquiv H E
```

8. `PartialEquiv.symm`

```lean
protected def symm : PartialEquiv β α
```

9. `ModelWithCorners`

```lean
structure ModelWithCorners (𝕜 : Type*) [NontriviallyNormedField 𝕜] (E : Type*)
    [NormedAddCommGroup E] [NormedSpace 𝕜 E] (H : Type*) [TopologicalSpace H] extends
    PartialEquiv H E
```

10. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

11. `NormedAddCommGroup`

```lean
class NormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E, MetricSpace E
```


---

## t102

Target: `DirectSum.component.lof_self`

```lean
theorem component.lof_self [DecidableEq ι] (i : ι) (b : M i) :
    component R ι M i ((lof R ι M i) b) = b
```

Proof / construction:

```lean
:=
  lof_apply R i b
```

Candidates (5), random order:

1. `DecidableEq`

```lean
abbrev DecidableEq (α : Sort u)
```

2. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

3. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

4. `DirectSum.lof_apply`

```lean
theorem lof_apply [DecidableEq ι] (i : ι) (b : M i) : ((lof R ι M i) b) i = b
```

5. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```


---

## t103

Target: `IsLocalExtrOn.isLocalExtr`

```lean
theorem IsLocalExtrOn.isLocalExtr (hf : IsLocalExtrOn f s a) (hs : s ∈ 𝓝 a) : IsLocalExtr f a
```

Proof / construction:

```lean
:=
  hf.elim (fun hf => (hf.isLocalMin hs).isExtr) fun hf => (hf.isLocalMax hs).isExtr
```

Candidates (16), random order:

1. `IsMinFilter.isExtr`

```lean
theorem IsMinFilter.isExtr : IsMinFilter f l a → IsExtrFilter f l a
```

2. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

3. `Filter`

```lean
structure Filter (α : Type*)
```

4. `IsLocalMinOn.isLocalMin`

```lean
theorem IsLocalMinOn.isLocalMin (hf : IsLocalMinOn f s a) (hs : s ∈ 𝓝 a) : IsLocalMin f a
```

5. `IsLocalExtrOn`

```lean
def IsLocalExtrOn
```

6. `nhds`

```lean
nhds
```

7. `IsLocalMinOn`

```lean
def IsLocalMinOn
```

8. `IsLocalMaxOn.isLocalMax`

```lean
theorem IsLocalMaxOn.isLocalMax (hf : IsLocalMaxOn f s a) (hs : s ∈ 𝓝 a) : IsLocalMax f a
```

9. `Membership.mem`

```lean
mem : γ → α → Prop
```

10. `Filter.instMembership`

```lean
instance instMembership : Membership (Set α) (Filter α)
```

11. `Set`

```lean
def Set (α : Type u)
```

12. `IsLocalExtr`

```lean
def IsLocalExtr
```

13. `IsMaxFilter.isExtr`

```lean
theorem IsMaxFilter.isExtr : IsMaxFilter f l a → IsExtrFilter f l a
```

14. `IsLocalExtrOn.elim`

```lean
theorem IsLocalExtrOn.elim {p : Prop} :
    IsLocalExtrOn f s a → (IsLocalMinOn f s a → p) → (IsLocalMaxOn f s a → p) → p
```

15. `IsLocalMaxOn`

```lean
def IsLocalMaxOn
```

16. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```


---

## t104

Target: `Cycle.nodup_reverse_iff`

```lean
theorem nodup_reverse_iff {s : Cycle α} : s.reverse.Nodup ↔ s.Nodup
```

Proof / construction:

```lean
:=
  Quot.inductionOn s fun _ => nodup_reverse
```

Candidates (9), random order:

1. `Cycle.Nodup`

```lean
nonrec def Nodup (s : Cycle α) : Prop
```

2. `Quot.inductionOn`

```lean
protected theorem inductionOn {α : Sort u} {r : α → α → Prop} {motive : Quot r → Prop}
    (q : Quot r)
    (h : (a : α) → motive (Quot.mk r a))
    : motive q
```

3. `Setoid.r`

```lean
r : α → α → Prop
```

4. `List.IsRotated.setoid`

```lean
def IsRotated.setoid (α : Type*) : Setoid (List α)
```

5. `Cycle.reverse`

```lean
nonrec def reverse (s : Cycle α) : Cycle α
```

6. `List`

```lean
inductive List (α : Type u)
```

7. `Cycle`

```lean
def Cycle (α : Type*) : Type _
```

8. `List.nodup_reverse`

```lean
theorem nodup_reverse {l : List α} : Nodup (reverse l) ↔ Nodup l
```

9. `Iff`

```lean
structure Iff (a b : Prop) : Prop
```


---

## t105

Target: `LinearMap.HasFiniteRange`

```lean
def HasFiniteRange (f : V →ₗ[K] V₂) : Prop
```

Proof / construction:

```lean
:=
  f.range.FG
```

Candidates (8), random order:

1. `LinearMap.range`

```lean
def range [RingHomSurjective τ₁₂] (f : M →ₛₗ[τ₁₂] M₂) : Submodule R₂ M₂
```

2. `Submodule.FG`

```lean
def FG (N : Submodule R M) : Prop
```

3. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

4. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

5. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

6. `LinearMap`

```lean
structure LinearMap {R S : Type*} [Semiring R] [Semiring S] (σ : R →+* S) (M : Type*)
    (M₂ : Type*) [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends
    AddHom M M₂, MulActionHom σ M M₂
```

7. `RingHom.id`

```lean
def id (α : Type*) [NonAssocSemiring α] : α →+* α
```

8. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```


---

## t106

Target: `AlgebraicGeometry.Scheme.IdealSheafData.comap_sup`

```lean
@[simp] lemma comap_sup : comap (J₁ ⊔ J₂) f = comap J₁ f ⊔ comap J₂ f
```

Proof / construction:

```lean
:= (map_gc f).l_sup
```

Candidates (13), random order:

1. `AlgebraicGeometry.Scheme.IdealSheafData`

```lean
structure IdealSheafData (X : Scheme.{u}) : Type u
```

2. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

3. `AlgebraicGeometry.Scheme.instCategory`

```lean
instance : Category Scheme
```

4. `IdemSemiring.toSemilatticeSup`

```lean
class IdemSemiring (α : Type*) extends Semiring α, SemilatticeSup α, OrderBot α
```

5. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

6. `AlgebraicGeometry.Scheme.IdealSheafData.comap`

```lean
def comap (I : Y.IdealSheafData) (f : X ⟶ Y) : X.IdealSheafData
```

7. `AlgebraicGeometry.Scheme.IdealSheafData.map`

```lean
def map (I : X.IdealSheafData) (f : X ⟶ Y) : Y.IdealSheafData
```

8. `AlgebraicGeometry.Scheme.IdealSheafData.map_gc`

```lean
lemma map_gc : GaloisConnection (comap · f) (map · f)
```

9. `AlgebraicGeometry.Scheme`

```lean
structure Scheme extends LocallyRingedSpace
```

10. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

11. `AlgebraicGeometry.Scheme.IdealSheafData.instIdemCommSemiring`

```lean
instance : IdemCommSemiring X.IdealSheafData
```

12. `IdemCommSemiring.toIdemSemiring`

```lean
class IdemCommSemiring (α : Type*) extends CommSemiring α, IdemSemiring α
```

13. `GaloisConnection.l_sup`

```lean
theorem l_sup (gc : GaloisConnection l u) : l (a₁ ⊔ a₂) = l a₁ ⊔ l a₂
```


---

## t107

Target: `NNRat.ext_num_den_iff`

```lean
theorem ext_num_den_iff : p = q ↔ p.num = q.num ∧ p.den = q.den
```

Proof / construction:

```lean
:=
  ⟨by rintro rfl; exact ⟨rfl, rfl⟩, fun h ↦ ext_num_den h.1 h.2⟩
```

Candidates (13), random order:

1. `Nat`

```lean
inductive Nat
```

2. `And.right`

```lean
right : b
```

3. `Iff.intro`

```lean
structure Iff (a b : Prop) : Prop
```

4. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

5. `NNRat.ext_num_den`

```lean
theorem ext_num_den (hn : p.num = q.num) (hd : p.den = q.den) : p = q
```

6. `NNRat.num`

```lean
def num (q : ℚ≥0) : ℕ
```

7. `Eq.ndrec`

```lean
Eq.ndrec
```

8. `And`

```lean
structure And (a b : Prop) : Prop
```

9. `Eq`

```lean
inductive Eq : α → α → Prop
```

10. `And.intro`

```lean
structure And (a b : Prop) : Prop
```

11. `NNRat`

```lean
def NNRat
```

12. `NNRat.den`

```lean
def den (q : ℚ≥0) : ℕ
```

13. `And.left`

```lean
left : a
```


---

## t108

Target: `IsFractionRing.ringEquivOfRingEquiv`

```lean
noncomputable def ringEquivOfRingEquiv : K ≃+* L
```

Proof / construction:

```lean
:=
  IsLocalization.ringEquivOfRingEquiv K L h (MulEquivClass.map_nonZeroDivisors h)
```

Candidates (12), random order:

1. `IsLocalization.ringEquivOfRingEquiv`

```lean
noncomputable def ringEquivOfRingEquiv (h : R ≃+* P) (H : M.map h.toMonoidHom = T) : S ≃+* Q
```

2. `RingEquiv`

```lean
structure RingEquiv (R S : Type*) [Mul R] [Mul S] [Add R] [Add S] extends R ≃ S, R ≃* S, R ≃+ S
```

3. `CommRing`

```lean
class CommRing (α : Type u) extends Ring α, CommMonoid α
```

4. `CommRing.toCommSemiring`

```lean
instance (priority := 100) CommRing.toCommSemiring [s : CommRing α] : CommSemiring α
```

5. `Distrib.toMul`

```lean
class Distrib (R : Type*) extends Mul R, Add R
```

6. `instDistribOfSemiring`

```lean
instance [Semiring α] : Distrib α
```

7. `Distrib.toAdd`

```lean
class Distrib (R : Type*) extends Mul R, Add R
```

8. `Semiring.toMonoidWithZero`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

9. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

10. `IsFractionRing`

```lean
abbrev IsFractionRing (R : Type*) [CommSemiring R] (K : Type*) [CommSemiring K] [Algebra R K]
```

11. `Algebra`

```lean
class Algebra (R : Type u) (A : Type v) [CommSemiring R] [Semiring A] extends SMul R A
```

12. `nonZeroDivisors`

```lean
def nonZeroDivisors (M₀ : Type*) [MonoidWithZero M₀] : Submonoid M₀
```


---

## t109

Target: `Unit.borelSpace`

```lean
instance Unit.borelSpace : BorelSpace Unit
```

Proof / construction:

```lean
:=
  ⟨borel_eq_top_of_discrete.symm⟩
```

Candidates (19), random order:

1. `CompleteLattice.toLattice`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

2. `MeasurableSpace.instCompleteLattice`

```lean
instance : CompleteLattice (MeasurableSpace α)
```

3. `CompleteLattice.toBoundedOrder`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

4. `borel`

```lean
def borel (α : Type u) [TopologicalSpace α] : MeasurableSpace α
```

5. `OrderTop.toTop`

```lean
class OrderTop (α : Type u) [LE α] extends Top α
```

6. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

7. `instTopologicalSpacePUnit`

```lean
instTopologicalSpacePUnit
```

8. `BoundedOrder.toOrderTop`

```lean
class BoundedOrder (α : Type u) [LE α] extends OrderTop α, OrderBot α
```

9. `Lattice.toSemilatticeSup`

```lean
class Lattice (α : Type u) extends SemilatticeSup α, SemilatticeInf α
```

10. `borel_eq_top_of_discrete`

```lean
theorem borel_eq_top_of_discrete [TopologicalSpace α] [DiscreteTopology α] : borel α = ⊤
```

11. `PUnit`

```lean
inductive PUnit : Sort u
```

12. `PUnit.instMeasurableSpace`

```lean
instance PUnit.instMeasurableSpace : MeasurableSpace PUnit
```

13. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

14. `BorelSpace.mk`

```lean
class BorelSpace (α : Type*) [TopologicalSpace α] [MeasurableSpace α] : Prop
```

15. `MeasurableSpace`

```lean
@[class] structure MeasurableSpace (α : Type*)
```

16. `SemilatticeSup.toPartialOrder`

```lean
class SemilatticeSup (α : Type u) extends PartialOrder α
```

17. `Unit`

```lean
abbrev Unit : Type
```

18. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```

19. `Top.top`

```lean
top : α
```


---

## t110

Target: `IsometryEquiv.piCongrLeft'`

```lean
def piCongrLeft' {ι' : Type*} [Fintype ι] [Fintype ι'] {Y : ι → Type*}
    [∀ j, PseudoEMetricSpace (Y j)] (e : ι ≃ ι') : (∀ i, Y i) ≃ᵢ ∀ j, Y (e.symm j)
```

Proof / construction:

```lean
where
  toEquiv := Equiv.piCongrLeft' _ e
  isometry_toFun x1 x2 := by
    simp_rw [edist_pi_def, Finset.sup_univ_eq_iSup]
    exact (Equiv.iSup_comp (g := fun b ↦ edist (x1 b) (x2 b)) e.symm)
```

Candidates (10), random order:

1. `Equiv.symm`

```lean
protected def symm (e : α ≃ β) : β ≃ α
```

2. `Equiv.instEquivLike`

```lean
instance : EquivLike (α ≃ β) α β
```

3. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

4. `Equiv`

```lean
structure Equiv (α β : Sort*)
```

5. `pseudoEMetricSpacePi`

```lean
instance pseudoEMetricSpacePi [∀ b, PseudoEMetricSpace (X b)] : PseudoEMetricSpace (∀ b, X b)
```

6. `IsometryEquiv.mk`

```lean
structure IsometryEquiv (α : Type u) (β : Type v) [PseudoEMetricSpace α] [PseudoEMetricSpace β]
    extends α ≃ β
```

7. `Fintype`

```lean
class Fintype (α : Type*)
```

8. `PseudoEMetricSpace`

```lean
class PseudoEMetricSpace (α : Type u) : Type u extends EDist α
```

9. `EquivLike.toFunLike`

```lean
instance (priority := 100) toFunLike : FunLike E α β
```

10. `Equiv.piCongrLeft'`

```lean
def piCongrLeft' (P : α → Sort*) (e : α ≃ β) : (∀ a, P a) ≃ ∀ b, P (e.symm b)
```


---
