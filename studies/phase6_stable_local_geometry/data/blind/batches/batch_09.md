# Blind grading batch 09 — 10 items

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
{"t081": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t081

Target: `MonoidHom.mrangeRestrict_surjective`

```lean
theorem mrangeRestrict_surjective (f : M →* N) : Function.Surjective f.mrangeRestrict
```

Proof / construction:

```lean
:=
  fun ⟨_, ⟨x, rfl⟩⟩ => ⟨x, rfl⟩
```

Candidates (18), random order:

1. `MulOneClass`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

2. `Submonoid.instSetLike`

```lean
instance : SetLike (Submonoid M) M
```

3. `Subtype.mk`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

4. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

5. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

6. `Membership.mem`

```lean
mem : γ → α → Prop
```

7. `MonoidHom.mrangeRestrict`

```lean
def mrangeRestrict {N} [MulOneClass N] (f : M →* N) : M →* (mrange f)
```

8. `MonoidHom.mrange`

```lean
def mrange (f : F) : Submonoid N
```

9. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

10. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

11. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

12. `Submonoid.toMulOneClass`

```lean
instance toMulOneClass {M : Type*} [MulOneClass M] (S : Submonoid M) : MulOneClass S
```

13. `MonoidHom.instFunLike`

```lean
instance MonoidHom.instFunLike : FunLike (M →* N) M N
```

14. `Submonoid`

```lean
structure Submonoid (M : Type*) [MulOneClass M] extends Subsemigroup M
```

15. `Exists.intro`

```lean
| intro (w : α) (h : p w) : Exists p
```

16. `Exists`

```lean
inductive Exists {α : Sort u} (p : α → Prop) : Prop
```

17. `MonoidHom`

```lean
structure MonoidHom (M : Type*) (N : Type*) [MulOne M] [MulOne N]
  extends OneHom M N, M →ₙ* N
```

18. `Eq`

```lean
inductive Eq : α → α → Prop
```


---

## t082

Target: `Subgroup.top_lowerCentralSeries_pi_of_finite`

```lean
theorem Subgroup.top_lowerCentralSeries_pi_of_finite [Finite η] (n : ℕ) :
    (⊤ : Subgroup (∀ i, Gs i)).lowerCentralSeries n = Subgroup.pi Set.univ
      fun i => (⊤ : Subgroup (Gs i)).lowerCentralSeries n
```

Proof / construction:

```lean
:= by
  rw [← pi_top (I := Set.univ), lowerCentralSeries_pi_of_finite]
```

Candidates (18), random order:

1. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```

2. `Top.top`

```lean
top : α
```

3. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

4. `Subgroup.instTop`

```lean
instance : Top (Subgroup G)
```

5. `Nat`

```lean
inductive Nat
```

6. `Group`

```lean
class Group (G : Type u) extends DivInvMonoid G
```

7. `Subgroup.pi_top`

```lean
theorem pi_top (I : Set η) : (pi I fun i => (⊤ : Subgroup (f i))) = ⊤
```

8. `Pi.group`

```lean
instance group [∀ i, Group (f i)] : Group (∀ i, f i)
```

9. `Subgroup.lowerCentralSeries`

```lean
def lowerCentralSeries (S : Subgroup G) : ℕ → Subgroup G
  | 0 => S
  | n + 1 => ⁅lowerCentralSeries S n, S⁆
```

10. `Finite`

```lean
class inductive Finite (α : Sort*) : Prop
  | intro {n : ℕ} : α ≃ Fin n → Finite _
```

11. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

12. `Subgroup`

```lean
structure Subgroup (G : Type*) [Group G] extends Submonoid G
```

13. `Subgroup.pi`

```lean
def pi (I : Set η) (H : ∀ i, Subgroup (f i)) : Subgroup (∀ i, f i)
```

14. `Eq`

```lean
inductive Eq : α → α → Prop
```

15. `Set.univ`

```lean
def univ : Set α
```

16. `Eq.refl`

```lean
| refl (a : α) : Eq a a
```

17. `Subgroup.lowerCentralSeries_pi_of_finite`

```lean
theorem Subgroup.lowerCentralSeries_pi_of_finite [Finite η] (Ss : ∀ i, Subgroup (Gs i)) (n : ℕ) :
    (Subgroup.pi Set.univ Ss).lowerCentralSeries n = Subgroup.pi Set.univ
      fun i => (Ss i).lowerCentralSeries n
```

18. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```


---

## t083

Target: `MeasureTheory.Measure.comap_apply`

```lean
theorem comap_apply (f : α → β) (hfi : Injective f)
    (hf : ∀ s, MeasurableSet s → MeasurableSet (f '' s)) (μ : Measure β) (hs : MeasurableSet s) :
    comap f μ s = μ (f '' s)
```

Proof / construction:

```lean
:=
  comap_apply₀ f μ hfi (fun s hs => (hf s hs).nullMeasurableSet) hs.nullMeasurableSet
```

Candidates (9), random order:

1. `MeasureTheory.Measure`

```lean
structure Measure (α : Type*) [MeasurableSpace α] extends OuterMeasure α
```

2. `MeasurableSet`

```lean
def MeasurableSet [MeasurableSpace α] (s : Set α) : Prop
```

3. `Set`

```lean
def Set (α : Type u)
```

4. `Function.Injective`

```lean
def Injective (f : α → β) : Prop
```

5. `MeasureTheory.Measure.comap_apply₀`

```lean
theorem comap_apply₀ (f : α → β) (μ : Measure β) (hfi : Injective f)
    (hf : ∀ s, MeasurableSet s → NullMeasurableSet (f '' s) μ)
    (hs : NullMeasurableSet s (comap f μ)) : comap f μ s = μ (f '' s)
```

6. `MeasureTheory.Measure.comap`

```lean
def comap [MeasurableSpace α] [MeasurableSpace β] (f : α → β) (μ : Measure β) : Measure α
```

7. `MeasurableSpace`

```lean
@[class] structure MeasurableSpace (α : Type*)
```

8. `Set.image`

```lean
def image {β : Type v} (f : α → β) (s : Set α) : Set β
```

9. `MeasurableSet.nullMeasurableSet`

```lean
theorem _root_.MeasurableSet.nullMeasurableSet (h : MeasurableSet s) : NullMeasurableSet s μ
```


---

## t084

Target: `Matroid.IsBasis.eRk_eq_encard`

```lean
lemma IsBasis.eRk_eq_encard (hIX : M.IsBasis I X) : M.eRk X = I.encard
```

Proof / construction:

```lean
:= by
  rw [← hIX.eRk_eq_eRk, hIX.indep.eRk_eq_encard]
```

Candidates (15), random order:

1. `ENat`

```lean
def ENat : Type
```

2. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

3. `Matroid.IsBasis`

```lean
def IsBasis (M : Matroid α) (I X : Set α) : Prop
```

4. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

5. `Set.encard`

```lean
noncomputable def encard (s : Set α) : ℕ∞
```

6. `Set`

```lean
def Set (α : Type u)
```

7. `Matroid.Indep.eRk_eq_encard`

```lean
lemma Indep.eRk_eq_encard (hI : M.Indep I) : M.eRk I = I.encard
```

8. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

9. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```

10. `Matroid.IsBasis.indep`

```lean
theorem IsBasis.indep (hI : M.IsBasis I X) : M.Indep I
```

11. `Eq.refl`

```lean
| refl (a : α) : Eq a a
```

12. `Matroid.eRk`

```lean
noncomputable def eRk (M : Matroid α) (X : Set α) : ℕ∞
```

13. `Eq`

```lean
inductive Eq : α → α → Prop
```

14. `Matroid.IsBasis.eRk_eq_eRk`

```lean
lemma IsBasis.eRk_eq_eRk (hIX : M.IsBasis I X) : M.eRk I = M.eRk X
```

15. `Matroid`

```lean
structure Matroid (α : Type*)
```


---

## t085

Target: `HomotopicalAlgebra.instCategoryWithFibrationsOver`

```lean
instance : CategoryWithFibrations (Over S)
```

Proof / construction:

```lean
where
  fibrations := (fibrations C).over
```

Candidates (7), random order:

1. `CategoryTheory.MorphismProperty.over`

```lean
def over (W : MorphismProperty T) {X : T} : MorphismProperty (Over X)
```

2. `CategoryTheory.instCategoryOver`

```lean
CategoryTheory.instCategoryOver
```

3. `HomotopicalAlgebra.CategoryWithFibrations`

```lean
class CategoryWithFibrations
```

4. `CategoryTheory.Over`

```lean
def Over (X : T)
```

5. `HomotopicalAlgebra.CategoryWithFibrations.mk`

```lean
class CategoryWithFibrations
```

6. `HomotopicalAlgebra.fibrations`

```lean
def fibrations : MorphismProperty C
```

7. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```


---

## t086

Target: `HomogeneousIdeal.eq_bot_iff`

```lean
theorem eq_bot_iff (I : HomogeneousIdeal 𝒜) : I = ⊥ ↔ I.toIdeal = ⊥
```

Proof / construction:

```lean
:=
  toIdeal_injective.eq_iff.symm
```

Candidates (20), random order:

1. `AddSubmonoidClass`

```lean
class AddSubmonoidClass (S : Type*) (M : outParam Type*) [AddZeroClass M] [SetLike S M] : Prop
  extends AddMemClass S M, ZeroMemClass S M
```

2. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

3. `NonAssocSemiring.toAddCommMonoidWithOne`

```lean
class NonAssocSemiring (α : Type u) extends NonUnitalNonAssocSemiring α, MulZeroOneClass α,
    AddCommMonoidWithOne α
```

4. `Ideal`

```lean
abbrev Ideal (R : Type u) [Semiring R]
```

5. `AddCommMonoidWithOne.toAddMonoidWithOne`

```lean
class AddCommMonoidWithOne (R : Type*) extends AddMonoidWithOne R, AddCommMonoid R
```

6. `Function.Injective.eq_iff`

```lean
theorem Injective.eq_iff (I : Injective f) {a b : α} : f a = f b ↔ a = b
```

7. `DecidableEq`

```lean
abbrev DecidableEq (α : Sort u)
```

8. `SetLike`

```lean
class SetLike (A : Type*) (B : outParam Type*)
```

9. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

10. `Bot.bot`

```lean
bot : α
```

11. `AddMonoid.toAddZeroClass`

```lean
class AddMonoid (M : Type u) extends AddSemigroup M, AddZeroClass M, NSMul M
```

12. `HomogeneousIdeal`

```lean
abbrev HomogeneousIdeal
```

13. `HomogeneousIdeal.toIdeal_injective`

```lean
theorem HomogeneousIdeal.toIdeal_injective :
    Function.Injective (HomogeneousIdeal.toIdeal : HomogeneousIdeal 𝒜 → Ideal A)
```

14. `AddMonoid`

```lean
class AddMonoid (M : Type u) extends AddSemigroup M, AddZeroClass M, NSMul M
```

15. `Iff.symm`

```lean
@[symm] theorem Iff.symm (h : a ↔ b) : b ↔ a
```

16. `Eq`

```lean
inductive Eq : α → α → Prop
```

17. `HomogeneousIdeal.toIdeal`

```lean
abbrev HomogeneousIdeal.toIdeal (I : HomogeneousIdeal 𝒜) : Ideal A
```

18. `AddMonoidWithOne.toAddMonoid`

```lean
class AddMonoidWithOne (R : Type*) extends NatCast R, AddMonoid R, One R
```

19. `HomogeneousIdeal.instBot`

```lean
instance : Bot (HomogeneousIdeal 𝒜)
```

20. `GradedRing`

```lean
class GradedRing (𝒜 : ι → σ) extends SetLike.GradedMonoid 𝒜, DirectSum.Decomposition 𝒜
```


---

## t087

Target: `ENNReal.mul_inv_cancel_right`

```lean
protected lemma mul_inv_cancel_right (hb₀ : b ≠ 0) (hb : b ≠ ∞) : a * b * b⁻¹ = a
```

Proof / construction:

```lean
:=
  ENNReal.mul_inv_cancel_right' (by simp [hb₀]) (by simp [hb])
```

Candidates (17), random order:

1. `implies_congr`

```lean
theorem implies_congr {p₁ p₂ : Sort u} {q₁ q₂ : Sort v} (h₁ : p₁ = p₂) (h₂ : q₁ = q₂) : (p₁ → q₁) = (p₂ → q₂)
```

2. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

3. `of_eq_true`

```lean
theorem of_eq_true (h : p = True) : p
```

4. `Eq`

```lean
inductive Eq : α → α → Prop
```

5. `IsEmpty.forall_iff`

```lean
theorem forall_iff {p : α → Prop} : (∀ a, p a) ↔ True
```

6. `Top.top`

```lean
top : α
```

7. `False`

```lean
inductive False : Prop
```

8. `eq_false`

```lean
theorem eq_false (h : ¬ p) : p = False
```

9. `True`

```lean
inductive True : Prop
```

10. `OfNat.ofNat`

```lean
ofNat : α
```

11. `ENNReal.mul_inv_cancel_right'`

```lean
protected lemma mul_inv_cancel_right' (hb₀ : b = 0 → a = 0) (hb : b = ∞ → a = 0) :
    a * b * b⁻¹ = a
```

12. `Eq.refl`

```lean
| refl (a : α) : Eq a a
```

13. `Eq.trans`

```lean
theorem Eq.trans {α : Sort u} {a b c : α} (h₁ : Eq a b) (h₂ : Eq b c) : Eq a c
```

14. `ENNReal.instTop`

```lean
ENNReal.instTop
```

15. `Zero.toOfNat0`

```lean
instance (priority := 300) Zero.toOfNat0 {α} [Zero α] : OfNat α (nat_lit 0)
```

16. `ENNReal.instZero`

```lean
instance : Zero ℝ≥0∞
```

17. `ENNReal`

```lean
def ENNReal
```


---

## t088

Target: `LinearEquiv.coe_injective`

```lean
theorem coe_injective : @Injective (M ≃ₛₗ[σ] M₂) (M → M₂) DFunLike.coe
```

Proof / construction:

```lean
:=
  DFunLike.coe_injective
```

Candidates (10), random order:

1. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

2. `RingHom`

```lean
structure RingHom (α : Type*) (β : Type*) [NonAssocSemiring α] [NonAssocSemiring β] extends
  α →* β, α →+ β, α →ₙ+* β, α →*₀ β
```

3. `LinearEquiv.instEquivLike`

```lean
instance : EquivLike (M ≃ₛₗ[σ] M₂) M M₂
```

4. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

5. `RingHomInvPair`

```lean
class RingHomInvPair (σ : R₁ →+* R₂) (σ' : outParam (R₂ →+* R₁)) : Prop
```

6. `DFunLike.coe_injective`

```lean
coe_injective : Function.Injective coe
```

7. `LinearEquiv`

```lean
structure LinearEquiv {R : Type*} {S : Type*} [Semiring R] [Semiring S] (σ : R →+* S)
  {σ' : S →+* R} [RingHomInvPair σ σ'] [RingHomInvPair σ' σ] (M : Type*) (M₂ : Type*)
  [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends LinearMap σ M M₂, M ≃+ M₂
```

8. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

9. `EquivLike.toFunLike`

```lean
instance (priority := 100) toFunLike : FunLike E α β
```

10. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```


---

## t089

Target: `LinearMap.BilinMap.toQuadraticMap_list_sum`

```lean
theorem toQuadraticMap_list_sum (B : List (BilinMap R M N)) :
    B.sum.toQuadraticMap = (B.map toQuadraticMap).sum
```

Proof / construction:

```lean
:=
  map_list_sum (toQuadraticMapAddMonoidHom R M) B
```

Candidates (21), random order:

1. `RingHom.id`

```lean
def id (α : Type*) [NonAssocSemiring α] : α →+* α
```

2. `QuadraticMap`

```lean
structure QuadraticMap (R : Type u) (M : Type v) (N : Type w) [CommSemiring R] [AddCommMonoid M]
    [Module R M] [AddCommMonoid N] [Module R N]
```

3. `map_list_sum`

```lean
-- Mathlib generates `map_list_sum` from the declaration below.
theorem map_list_prod {F : Type*} [FunLike F M N] [MonoidHomClass F M N] (f : F) (l : List M) :
    f l.prod = (l.map f).prod
```

4. `LinearMap.BilinMap.toQuadraticMapAddMonoidHom`

```lean
def toQuadraticMapAddMonoidHom : (BilinMap R M N) →+ QuadraticMap R M N
```

5. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

6. `CommSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

7. `List`

```lean
inductive List (α : Type u)
```

8. `AddCommMonoid.toAddMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

9. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

10. `QuadraticMap.instAddCommMonoid`

```lean
QuadraticMap.instAddCommMonoid
```

11. `LinearMap.addCommMonoid`

```lean
instance addCommMonoid : AddCommMonoid (M →ₛₗ[σ₁₂] M₂)
```

12. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

13. `LinearMap`

```lean
structure LinearMap {R S : Type*} [Semiring R] [Semiring S] (σ : R →+* S) (M : Type*)
    (M₂ : Type*) [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends
    AddHom M M₂, MulActionHom σ M M₂
```

14. `LinearMap.BilinMap`

```lean
protected abbrev BilinMap : Type _
```

15. `LinearMap.addMonoid`

```lean
instance addMonoid : AddMonoid (M →ₛₗ[σ₁₂] M₂)
```

16. `AddMonoidHom.instFunLike`

```lean
-- Mathlib generates `AddMonoidHom.instFunLike` from the declaration below.
instance MonoidHom.instFunLike : FunLike (M →* N) M N
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

19. `AddZeroClass.toAddZero`

```lean
class AddZeroClass (M : Type u) extends AddZero M
```

20. `LinearMap.module`

```lean
instance module : Module S (M →ₛₗ[σ₁₂] M₂)
```

21. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```


---

## t090

Target: `CategoryTheory.Idempotents.Karoubi.instCategory`

```lean
instance : Category (Karoubi C)
```

Proof / construction:

```lean
where
  Hom := Karoubi.Hom
  id P := ⟨P.p, by repeat' rw [P.idem]⟩
  comp f g := ⟨f.f ≫ g.f, Karoubi.comp_proof g f⟩
```

Candidates (11), random order:

1. `CategoryTheory.Idempotents.Karoubi.X`

```lean
X : C
```

2. `CategoryTheory.Idempotents.Karoubi.Hom.f`

```lean
f : P.X ⟶ Q.X
```

3. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

4. `CategoryTheory.Category.mk`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

5. `CategoryTheory.Idempotents.Karoubi.comp_proof`

```lean
theorem comp_proof {P Q R : Karoubi C} (g : Hom Q R) (f : Hom P Q) :
    P.p ≫ (f.f ≫ g.f) ≫ R.p = f.f ≫ g.f
```

6. `CategoryTheory.Idempotents.Karoubi`

```lean
structure Karoubi
```

7. `CategoryTheory.Idempotents.Karoubi.p`

```lean
p : X ⟶ X
```

8. `CategoryTheory.Idempotents.Karoubi.Hom`

```lean
structure Hom (P Q : Karoubi C)
```

9. `CategoryTheory.CategoryStruct.comp`

```lean
comp : ∀ {X Y Z : obj}, (X ⟶ Y) → (Y ⟶ Z) → (X ⟶ Z)
```

10. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

11. `CategoryTheory.Idempotents.Karoubi.Hom.mk`

```lean
structure Hom (P Q : Karoubi C)
```


---
