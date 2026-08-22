# Blind grading batch 02 — 10 items

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
{"t011": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t011

Target: `AddGroup.nilpotencyClass`

```lean
noncomputable def Group.nilpotencyClass : ℕ
```

Proof / construction:

```lean
:=
  if hG : IsNilpotent G then Nat.find hG.nilpotent else 0
```

Candidates (15), random order:

1. `Classical.propDecidable`

```lean
noncomputable scoped instance (priority := low) propDecidable (a : Prop) : Decidable a
```

2. `AddGroup.IsNilpotent.nilpotent`

```lean
lemma IsNilpotent.nilpotent (G : Type*) [Group G] [IsNilpotent G] :
    ∃ n : ℕ, upperCentralSeries G n = ⊤
```

3. `AddSubgroup`

```lean
structure AddSubgroup (G : Type*) [AddGroup G] extends AddSubmonoid G
```

4. `Top.top`

```lean
top : α
```

5. `dite`

```lean
def dite {α : Sort u} (c : Prop) [h : Decidable c] (t : c → α) (e : Not c → α) : α
```

6. `OfNat.ofNat`

```lean
ofNat : α
```

7. `Nat`

```lean
inductive Nat
```

8. `Not`

```lean
@[implicit_reducible] def Not (a : Prop) : Prop
```

9. `AddSubgroup.instTop`

```lean
instance : Top (Subgroup G)
```

10. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

11. `Eq`

```lean
inductive Eq : α → α → Prop
```

12. `AddGroup`

```lean
class AddGroup (A : Type u) extends SubNegMonoid A
```

13. `AddSubgroup.upperCentralSeries`

```lean
@[deprecated (since := "2026-03-25")] alias upperCentralSeries
```

14. `Nat.find`

```lean
protected def find : ℕ
```

15. `AddGroup.IsNilpotent`

```lean
class _root_.AddGroup.IsNilpotent (G : Type*) [AddGroup G] : Prop
```


---

## t012

Target: `FirstOrder.Language.Embedding.domRestrict`

```lean
def domRestrict (f : M ↪[L] N) (p : L.Substructure M) : p ↪[L] N
```

Proof / construction:

```lean
:=
  f.comp p.subtype
```

Candidates (11), random order:

1. `FirstOrder.Language.Structure`

```lean
class Structure
```

2. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

3. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

4. `FirstOrder.Language`

```lean
structure Language
```

5. `FirstOrder.Language.Substructure.subtype`

```lean
def subtype (S : L.Substructure M) : S ↪[L] M
```

6. `FirstOrder.Language.Substructure.inducedStructure`

```lean
instance inducedStructure {S : L.Substructure M} : L.Structure S
```

7. `FirstOrder.Language.Substructure`

```lean
structure Substructure
```

8. `FirstOrder.Language.Substructure.instSetLike`

```lean
instance instSetLike : SetLike (L.Substructure M) M
```

9. `Membership.mem`

```lean
mem : γ → α → Prop
```

10. `FirstOrder.Language.Embedding`

```lean
structure Embedding extends M ↪ N
```

11. `FirstOrder.Language.Embedding.comp`

```lean
def comp (hnp : N ↪[L] P) (hmn : M ↪[L] N) : M ↪[L] P
```


---

## t013

Target: `RatFunc.mapRingHom`

```lean
def mapRingHom [RingHomClass F R[X] S[X]] (φ : F) (hφ : R[X]⁰ ≤ S[X]⁰.comap φ) :
    R⟮X⟯ →+* S⟮X⟯
```

Proof / construction:

```lean
:=
  { map φ hφ with
    map_zero' := by
      simp_rw [MonoidHom.toFun_eq_coe, ← ofFractionRing_zero, ← Localization.mk_zero (1 : R[X]⁰),
        ← Localization.mk_zero (1 : S[X]⁰), map_apply_ofFractionRing_mk, map_zero,
        Localization.mk_eq_mk', IsLocalization.mk'_zero]
    map_add' := by
      rintro ⟨x⟩ ⟨y⟩
      induction x using Localization.induction_on
      induction y using Localization.induction_on
      · simp only [← ofFractionRing_add, Localization.add_mk, map_add, map_mul,
          MonoidHom.toFun_eq_coe, map_apply_ofFractionRing_mk, Submonoid.coe_mul,
          -- We have to specify `S[X]⁰` to `mk_mul_mk`, otherwise it will try to rewrite
          -- the wrong occurrence.
          Submonoid.mk_mul_mk S[X]⁰] }
```

Candidates (25), random order:

1. `Polynomial.semiring`

```lean
instance semiring : Semiring R[X]
```

2. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

3. `MonoidWithZero.toMulZeroOneClass`

```lean
class MonoidWithZero (M₀ : Type u) extends Monoid M₀, MulZeroOneClass M₀, SemigroupWithZero M₀
```

4. `RatFunc.map`

```lean
def map [MonoidHomClass F R[X] S[X]] (φ : F) (hφ : R[X]⁰ ≤ S[X]⁰.comap φ) :
    R⟮X⟯ →* S⟮X⟯
```

5. `Semiring.toMonoidWithZero`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

6. `nonZeroDivisors`

```lean
def nonZeroDivisors (M₀ : Type*) [MonoidWithZero M₀] : Submonoid M₀
```

7. `Polynomial`

```lean
structure Polynomial (R : Type*) [Semiring R]
```

8. `instMulZeroOneClassOfSemiring`

```lean
instance [Semiring α] : MulZeroOneClass α
```

9. `CommRing`

```lean
class CommRing (α : Type u) extends Ring α, CommMonoid α
```

10. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

11. `Submonoid`

```lean
structure Submonoid (M : Type*) [MulOneClass M] extends Subsemigroup M
```

12. `RatFunc`

```lean
structure RatFunc [CommRing K] : Type u
```

13. `FunLike`

```lean
abbrev FunLike F α β
```

14. `RatFunc.instCommRing`

```lean
instance instCommRing : CommRing K⟮X⟯
```

15. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

16. `Submonoid.comap`

```lean
def comap (f : F) (S : Submonoid N) :
    Submonoid M
```

17. `RingHomClass`

```lean
class RingHomClass (F : Type*) (α β : outParam Type*)
    [NonAssocSemiring α] [NonAssocSemiring β] [FunLike F α β] : Prop
  extends MonoidHomClass F α β, AddMonoidHomClass F α β, MonoidWithZeroHomClass F α β
```

18. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

19. `LE.le`

```lean
le : α → α → Prop
```

20. `RingHom.mk`

```lean
structure RingHom (α : Type*) (β : Type*) [NonAssocSemiring α] [NonAssocSemiring β] extends
  α →* β, α →+ β, α →ₙ+* β, α →*₀ β
```

21. `Submonoid.instPartialOrder`

```lean
@[to_additive] instance : PartialOrder (Submonoid M)
```

22. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

23. `CommRing.toCommSemiring`

```lean
instance (priority := 100) CommRing.toCommSemiring [s : CommRing α] : CommSemiring α
```

24. `MulZeroOneClass.toMulOneClass`

```lean
class MulZeroOneClass (M₀ : Type u) extends MulOneClass M₀, MulZeroClass M₀
```

25. `MonoidHom`

```lean
structure MonoidHom (M : Type*) (N : Type*) [MulOne M] [MulOne N]
  extends OneHom M N, M →ₙ* N
```


---

## t014

Target: `Flag.instGradeOrderSubtypeMem`

```lean
instance [GradeOrder 𝕆 α] (s : Flag α) : GradeOrder 𝕆 s
```

Proof / construction:

```lean
:=
  .liftRight _ (Subtype.strictMono_coe _) fun _ _ ↦ coe_covBy_coe.2
```

Candidates (13), random order:

1. `GradeOrder`

```lean
class GradeOrder (𝕆 α : Type*) [Preorder 𝕆] [Preorder α]
```

2. `Flag.instSetLike`

```lean
instance : SetLike (Flag α) α
```

3. `Subtype.preorder`

```lean
instance preorder [Preorder α] (p : α → Prop) : Preorder (Subtype p)
```

4. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

5. `Membership.mem`

```lean
mem : γ → α → Prop
```

6. `Subtype.val`

```lean
val : α
```

7. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

8. `PartialOrder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

9. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

10. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

11. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

12. `Flag`

```lean
structure Flag (α : Type*) [LE α]
```

13. `GradeOrder.liftRight`

```lean
abbrev GradeOrder.liftRight [GradeOrder 𝕆 β] (f : α → β) (hf : StrictMono f)
    (hcovBy : ∀ a b, a ⋖ b → f a ⋖ f b) : GradeOrder 𝕆 α
```


---

## t015

Target: `HomologicalComplex₂.D₂`

```lean
noncomputable def D₂ (i₁₂ i₁₂' : I₁₂) :
    K.toGradedObject.mapObj (ComplexShape.π c₁ c₂ c₁₂) i₁₂ ⟶
      K.toGradedObject.mapObj (ComplexShape.π c₁ c₂ c₁₂) i₁₂'
```

Proof / construction:

```lean
:=
  GradedObject.descMapObj _ (ComplexShape.π c₁ c₂ c₁₂)
    (fun ⟨i₁, i₂⟩ _ => K.d₂ c₁₂ i₁ i₂ i₁₂')
```

Candidates (20), random order:

1. `TotalComplexShape`

```lean
class TotalComplexShape
```

2. `HomologicalComplex₂.HasTotal`

```lean
abbrev HasTotal
```

3. `HomologicalComplex₂.toGradedObject`

```lean
def toGradedObject (K : HomologicalComplex₂ C c₁ c₂) :
    GradedObject (I₁ × I₂) C
```

4. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

5. `Eq`

```lean
inductive Eq : α → α → Prop
```

6. `CategoryTheory.GradedObject.mapObj`

```lean
noncomputable def mapObj : GradedObject J C
```

7. `Prod`

```lean
structure Prod (α : Type u) (β : Type v)
```

8. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

9. `ComplexShape`

```lean
structure ComplexShape (ι : Type*)
```

10. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

11. `Prod.mk`

```lean
structure Prod (α : Type u) (β : Type v)
```

12. `HomologicalComplex₂.D₁`

```lean
noncomputable def D₁ (i₁₂ i₁₂' : I₁₂) :
    K.toGradedObject.mapObj (ComplexShape.π c₁ c₂ c₁₂) i₁₂ ⟶
      K.toGradedObject.mapObj (ComplexShape.π c₁ c₂ c₁₂) i₁₂'
```

13. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

14. `CategoryTheory.GradedObject.descMapObj`

```lean
noncomputable def descMapObj {A : C} {j : J} (φ : ∀ (i : I) (_ : p i = j), X i ⟶ A) :
    X.mapObj p j ⟶ A
```

15. `DecidableEq`

```lean
abbrev DecidableEq (α : Sort u)
```

16. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`

```lean
instance (priority := 100) preadditiveHasZeroMorphisms : HasZeroMorphisms C
```

17. `ComplexShape.π`

```lean
abbrev π (i : I₁ × I₂) : I₁₂
```

18. `HomologicalComplex₂.d₂`

```lean
noncomputable def d₂ :
    (K.X i₁).X i₂ ⟶ (K.toGradedObject.mapObj (ComplexShape.π c₁ c₂ c₁₂)) i₁₂
```

19. `HomologicalComplex₂`

```lean
abbrev HomologicalComplex₂
```

20. `CategoryTheory.Preadditive`

```lean
class Preadditive
```


---

## t016

Target: `AffineMap.id_linear`

```lean
theorem id_linear : (id k P1).linear = LinearMap.id
```

Proof / construction:

```lean
:=
  rfl
```

Candidates (13), random order:

1. `AddTorsor`

```lean
class AddTorsor (G : outParam Type*) (P : Type*) [AddGroup G] extends AddAction G P,
  VSub G P
```

2. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

3. `AffineMap.id`

```lean
nonrec def id : P1 →ᵃ[k] P1
```

4. `Ring.toSemiring`

```lean
class Ring (R : Type u) extends Semiring R, AddCommGroup R, AddGroupWithOne R
```

5. `AddCommGroup.toAddGroup`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

6. `AddCommGroup`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

7. `RingHom.id`

```lean
def id (α : Type*) [NonAssocSemiring α] : α →+* α
```

8. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

9. `AddCommGroup.toAddCommMonoid`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

10. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

11. `LinearMap`

```lean
structure LinearMap {R S : Type*} [Semiring R] [Semiring S] (σ : R →+* S) (M : Type*)
    (M₂ : Type*) [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends
    AddHom M M₂, MulActionHom σ M M₂
```

12. `AffineMap.linear`

```lean
linear : V1 →ₗ[k] V2
```

13. `Ring`

```lean
class Ring (R : Type u) extends Semiring R, AddCommGroup R, AddGroupWithOne R
```


---

## t017

Target: `orderOf_map_dvd`

```lean
theorem orderOf_map_dvd {H : Type*} [Monoid H] (ψ : G →* H) (x : G) :
    orderOf (ψ x) ∣ orderOf x
```

Proof / construction:

```lean
:= by
  apply orderOf_dvd_of_pow_eq_one
  rw [← map_pow, pow_orderOf_eq_one]
  apply map_one
```

Candidates (24), random order:

1. `NPow.toPow`

```lean
instance NPow.toPow {M : Type*} [NPow M] : Pow M ℕ
```

2. `map_pow`

```lean
theorem map_pow [Monoid G] [Monoid H] [MonoidHomClass F G H] (f : F) (a : G) :
    ∀ n : ℕ, f (a ^ n) = f a ^ n
  | 0 => by rw [pow_zero, pow_zero, map_one]
  | n + 1 => by rw [pow_succ, pow_succ, map_mul, map_pow f a n]
```

3. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

4. `orderOf`

```lean
noncomputable def orderOf (x : G) : ℕ
```

5. `Monoid`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

6. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```

7. `pow_orderOf_eq_one`

```lean
theorem pow_orderOf_eq_one (x : G) : x ^ orderOf x = 1
```

8. `Monoid.toNPow`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

9. `MonoidHom`

```lean
structure MonoidHom (M : Type*) (N : Type*) [MulOne M] [MulOne N]
  extends OneHom M N, M →ₙ* N
```

10. `Nat`

```lean
inductive Nat
```

11. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

12. `Eq`

```lean
inductive Eq : α → α → Prop
```

13. `HPow.hPow`

```lean
hPow : α → β → γ
```

14. `Monoid.toMulOneClass`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

15. `OfNat.ofNat`

```lean
ofNat : α
```

16. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

17. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

18. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

19. `map_one`

```lean
theorem map_one [OneHomClass F M N] (f : F) : f 1 = 1
```

20. `MulOne.toOne`

```lean
class MulOne (M : Type*) extends One M, Mul M
```

21. `One.toOfNat1`

```lean
instance (priority := 300) One.toOfNat1 {α} [One α] : OfNat α (nat_lit 1)
```

22. `orderOf_dvd_of_pow_eq_one`

```lean
theorem orderOf_dvd_of_pow_eq_one (h : x ^ n = 1) : orderOf x ∣ n
```

23. `instHPow`

```lean
instance instHPow [Pow α β] : HPow α β α
```

24. `MonoidHom.instFunLike`

```lean
instance MonoidHom.instFunLike : FunLike (M →* N) M N
```


---

## t018

Target: `CategoryTheory.Functor.mapTriangleOpCompTriangleOpEquivalenceFunctorApp`

```lean
noncomputable def mapTriangleOpCompTriangleOpEquivalenceFunctorApp (T : Triangle C) :
    (triangleOpEquivalence D).functor.obj (op (F.mapTriangle.obj T)) ≅
      F.op.mapTriangle.obj ((triangleOpEquivalence C).functor.obj (op T))
```

Proof / construction:

```lean
:=
  Triangle.isoMk _ _ (Iso.refl _) (Iso.refl _) (Iso.refl _) (by simp) (by simp)
      (by simp [shift_map_op, map_opShiftFunctorEquivalence_counitIso_inv_app_unop])
```

Candidates (23), random order:

1. `Int.instAddMonoid`

```lean
instance instAddMonoid        : AddMonoid ℤ
```

2. `CategoryTheory.Functor.obj`

```lean
obj : C → D
```

3. `CategoryTheory.Pretriangulated.Opposite.instHasShiftOppositeInt`

```lean
scoped instance : HasShift Cᵒᵖ ℤ
```

4. `Int`

```lean
inductive Int : Type
```

5. `Opposite`

```lean
structure Opposite
```

6. `CategoryTheory.Functor.op`

```lean
protected def op (F : C ⥤ D) : Cᵒᵖ ⥤ Dᵒᵖ
```

7. `Opposite.op`

```lean
structure Opposite
```

8. `CategoryTheory.Pretriangulated.Triangle.isoMk`

```lean
def Triangle.isoMk (A B : Triangle C)
    (iso₁ : A.obj₁ ≅ B.obj₁) (iso₂ : A.obj₂ ≅ B.obj₂) (iso₃ : A.obj₃ ≅ B.obj₃)
    (comm₁ : A.mor₁ ≫ iso₂.hom = iso₁.hom ≫ B.mor₁ := by cat_disch)
    (comm₂ : A.mor₂ ≫ iso₃.hom = iso₂.hom ≫ B.mor₂ := by cat_disch)
    (comm₃ : A.mor₃ ≫ iso₁.hom⟦1⟧' = iso₃.hom ≫ B.mor₃ := by cat_disch) : A ≅ B
```

9. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

10. `CategoryTheory.Pretriangulated.triangleOpEquivalence`

```lean
noncomputable def triangleOpEquivalence :
    (Triangle C)ᵒᵖ ≌ Triangle Cᵒᵖ
```

11. `CategoryTheory.Iso.refl`

```lean
def refl (X : C) : X ≅ X
```

12. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

13. `CategoryTheory.Pretriangulated.Triangle`

```lean
structure Triangle
```

14. `CategoryTheory.Functor.CommShift`

```lean
class CommShift (F : C ⥤ D) (A : Type*) [AddMonoid A] [HasShift C A] [HasShift D A]
```

15. `CategoryTheory.Functor.mapTriangle`

```lean
def mapTriangle : Triangle C ⥤ Triangle D
```

16. `CategoryTheory.Category.opposite`

```lean
instance Category.opposite : Category.{v₁} Cᵒᵖ
```

17. `CategoryTheory.Pretriangulated.triangleCategory`

```lean
instance triangleCategory : Category (Triangle C)
```

18. `CategoryTheory.HasShift`

```lean
class HasShift (C : Type u) (A : Type*) [Category.{v} C] [AddMonoid A]
```

19. `CategoryTheory.Pretriangulated.Opposite.commShiftFunctorOpInt`

```lean
noncomputable scoped instance commShiftFunctorOpInt : F.op.CommShift ℤ
```

20. `CategoryTheory.Pretriangulated.Triangle.obj₃`

```lean
obj₃ : C
```

21. `CategoryTheory.Equivalence.functor`

```lean
functor : C ⥤ D
```

22. `CategoryTheory.Pretriangulated.Triangle.obj₁`

```lean
obj₁ : C
```

23. `CategoryTheory.Pretriangulated.Triangle.obj₂`

```lean
obj₂ : C
```


---

## t019

Target: `Cardinal.mk_set_ne_zero_iff`

```lean
theorem mk_set_ne_zero_iff {s : Set α} : #s ≠ 0 ↔ s.Nonempty
```

Proof / construction:

```lean
:= by
  rw [mk_ne_zero_iff, nonempty_coe_sort]
```

Candidates (19), random order:

1. `Zero.toOfNat0`

```lean
instance (priority := 300) Zero.toOfNat0 {α} [Zero α] : OfNat α (nat_lit 0)
```

2. `Cardinal`

```lean
def Cardinal : Type (u + 1)
```

3. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

4. `OfNat.ofNat`

```lean
ofNat : α
```

5. `Set.Nonempty`

```lean
protected def Nonempty (s : Set α) : Prop
```

6. `Cardinal.mk`

```lean
def mk : Type u → Cardinal
```

7. `Nonempty`

```lean
class inductive Nonempty (α : Sort u) : Prop
```

8. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

9. `Set.nonempty_coe_sort`

```lean
theorem nonempty_coe_sort {s : Set α} : Nonempty ↥s ↔ s.Nonempty
```

10. `Cardinal.instZero`

```lean
instance : Zero Cardinal.{u}
```

11. `Set`

```lean
def Set (α : Type u)
```

12. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

13. `propext`

```lean
axiom propext {a b : Prop} : (a ↔ b) → a = b
```

14. `Iff.rfl`

```lean
protected theorem Iff.rfl {a : Prop} : a ↔ a
```

15. `Set.Elem`

```lean
@[coe, reducible] def Elem (s : Set α) : Type u
```

16. `Eq`

```lean
inductive Eq : α → α → Prop
```

17. `Iff`

```lean
structure Iff (a b : Prop) : Prop
```

18. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

19. `Cardinal.mk_ne_zero_iff`

```lean
theorem mk_ne_zero_iff {α : Type u} : #α ≠ 0 ↔ Nonempty α
```


---

## t020

Target: `PiTensorProduct.instNonemptyElemFreeAddMonoidProdForallLifts`

```lean
instance (x : ⨂[R] i, s i) : Nonempty ↑x.lifts
```

Proof / construction:

```lean
:= nonempty_subtype.mpr (nonempty_lifts x)
```

Candidates (17), random order:

1. `PiTensorProduct.lifts`

```lean
def lifts (x : ⨂[R] i, s i) : Set (FreeAddMonoid (R × Π i, s i))
```

2. `PiTensorProduct.nonempty_lifts`

```lean
lemma nonempty_lifts (x : ⨂[R] i, s i) : Set.Nonempty (lifts x)
```

3. `PiTensorProduct`

```lean
def PiTensorProduct : Type _
```

4. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

5. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

6. `FreeAddMonoid`

```lean
FreeAddMonoid
```

7. `Set.instMembership`

```lean
instance : Membership α (Set α)
```

8. `Prod`

```lean
structure Prod (α : Type u) (β : Type v)
```

9. `Exists`

```lean
inductive Exists {α : Sort u} (p : α → Prop) : Prop
```

10. `CommSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

11. `Nonempty`

```lean
class inductive Nonempty (α : Sort u) : Prop
```

12. `Set`

```lean
def Set (α : Type u)
```

13. `Membership.mem`

```lean
mem : γ → α → Prop
```

14. `nonempty_subtype`

```lean
theorem nonempty_subtype {α} {p : α → Prop} : Nonempty (Subtype p) ↔ ∃ a : α, p a
```

15. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

16. `Iff.mpr`

```lean
mpr : b → a
```

17. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```


---
