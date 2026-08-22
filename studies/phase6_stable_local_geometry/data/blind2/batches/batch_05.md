# Blind grading batch 05 — 8 items

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
{"t041": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t041

Target: `ComplexShape.Embedding.extendHomotopyFunctor`

```lean
noncomputable def extendHomotopyFunctor :
    HomotopyCategory C c ⥤ HomotopyCategory C c'
```

Proof / construction:

```lean
:=
  CategoryTheory.Quotient.lift _ (e.extendFunctor C ⋙ HomotopyCategory.quotient C c') (by
    rintro K L f₁ f₂ ⟨h⟩
    exact HomotopyCategory.eq_of_homotopy _ _ (h.extend e))
```

Candidates (16), random order:

1. `HomologicalComplex.instCategory`

```lean
instance : Category (HomologicalComplex V c)
```

2. `HomologicalComplex`

```lean
structure HomologicalComplex (c : ComplexShape ι)
```

3. `homotopic`

```lean
def homotopic : HomRel (HomologicalComplex V c)
```

4. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

5. `CategoryTheory.Functor.comp`

```lean
def comp (F : C ⥤ D) (G : D ⥤ E) : C ⥤ E
```

6. `CategoryTheory.Quotient.lift`

```lean
def lift (H : ∀ (x y : C) (f₁ f₂ : x ⟶ y), r f₁ f₂ → F.map f₁ = F.map f₂) : Quotient r ⥤ D
```

7. `instCategoryHomotopyCategory`

```lean
instance : Category (HomotopyCategory V c)
```

8. `CategoryTheory.Preadditive`

```lean
class Preadditive
```

9. `ComplexShape`

```lean
structure ComplexShape (ι : Type*)
```

10. `ComplexShape.Embedding.IsRelIff`

```lean
class IsRelIff : Prop
```

11. `ComplexShape.Embedding`

```lean
structure Embedding
```

12. `HomotopyCategory.quotient`

```lean
def quotient : HomologicalComplex V c ⥤ HomotopyCategory V c
```

13. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`

```lean
instance (priority := 100) preadditiveHasZeroMorphisms : HasZeroMorphisms C
```

14. `ComplexShape.Embedding.extendFunctor`

```lean
noncomputable def extendFunctor [HasZeroMorphisms C] :
    HomologicalComplex C c ⥤ HomologicalComplex C c'
```

15. `CategoryTheory.Limits.HasZeroObject`

```lean
class HasZeroObject : Prop
```

16. `HomotopyCategory`

```lean
def HomotopyCategory
```


---

## t042

Target: `MaximalSpectrum.PiLocalization`

```lean
abbrev PiLocalization : Type _
```

Proof / construction:

```lean
:= Π I : MaximalSpectrum R, Localization.AtPrime I.1
```

Candidates (4), random order:

1. `Localization.AtPrime`

```lean
protected abbrev Localization.AtPrime
```

2. `MaximalSpectrum.asIdeal`

```lean
asIdeal : Ideal R
```

3. `MaximalSpectrum`

```lean
structure MaximalSpectrum (R : Type*) [CommSemiring R]
```

4. `CommSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```


---

## t043

Target: `Nat.roughNumbersUpTo`

```lean
def roughNumbersUpTo (N k : ℕ) : Finset ℕ
```

Proof / construction:

```lean
:=
  {n ∈ Finset.range (N + 1) | n ≠ 0 ∧ n ∉ smoothNumbers k}
```

Candidates (20), random order:

1. `Nat`

```lean
inductive Nat
```

2. `instDecidableAnd`

```lean
instDecidableAnd
```

3. `Finset.range`

```lean
def range (n : ℕ) : Finset ℕ
```

4. `Eq`

```lean
inductive Eq : α → α → Prop
```

5. `HAdd.hAdd`

```lean
hAdd : α → β → γ
```

6. `instHAdd`

```lean
instance instHAdd [Add α] : HAdd α α α
```

7. `instDecidableNot`

```lean
instDecidableNot
```

8. `And`

```lean
structure And (a b : Prop) : Prop
```

9. `OfNat.ofNat`

```lean
ofNat : α
```

10. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

11. `Not`

```lean
@[implicit_reducible] def Not (a : Prop) : Prop
```

12. `Membership.mem`

```lean
mem : γ → α → Prop
```

13. `instAddNat`

```lean
instance instAddNat : Add Nat
```

14. `Set.instMembership`

```lean
instance : Membership α (Set α)
```

15. `Nat.instDecidablePredMemSetSmoothNumbers`

```lean
Nat.instDecidablePredMemSetSmoothNumbers
```

16. `Set`

```lean
def Set (α : Type u)
```

17. `Nat.smoothNumbers`

```lean
def smoothNumbers (n : ℕ) : Set ℕ
```

18. `Finset.filter`

```lean
def filter (s : Finset α) : Finset α
```

19. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

20. `instDecidableEqNat`

```lean
instDecidableEqNat
```


---

## t044

Target: `CochainComplex.shiftFunctorObjXIso`

```lean
def shiftFunctorObjXIso (K : CochainComplex C ℤ) (n i m : ℤ) (hm : m = i + n) :
    ((shiftFunctor C n).obj K).X i ≅ K.X m
```

Proof / construction:

```lean
:= K.XIsoOfEq hm.symm
```

Candidates (21), random order:

1. `AddGroupWithOne.toAddMonoidWithOne`

```lean
class AddGroupWithOne (R : Type u) extends IntCast R, AddMonoidWithOne R, AddGroup R
```

2. `AddMonoidWithOne.toOne`

```lean
class AddMonoidWithOne (R : Type*) extends NatCast R, AddMonoid R, One R
```

3. `AddRightCancelSemigroup.toAddSemigroup`

```lean
class AddRightCancelSemigroup (G : Type u) extends AddSemigroup G, IsRightCancelAdd G
```

4. `CochainComplex`

```lean
abbrev CochainComplex (α : Type*) [AddRightCancelSemigroup α] [One α] : Type _
```

5. `AddCancelMonoid.toAddRightCancelMonoid`

```lean
class AddCancelMonoid (M : Type u) extends AddLeftCancelMonoid M, AddRightCancelMonoid M
```

6. `Int.instRing`

```lean
instance instRing         : Ring ℤ
```

7. `Eq`

```lean
inductive Eq : α → α → Prop
```

8. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`

```lean
instance (priority := 100) preadditiveHasZeroMorphisms : HasZeroMorphisms C
```

9. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

10. `HomologicalComplex.XIsoOfEq`

```lean
def XIsoOfEq (K : HomologicalComplex V c) {p q : ι} (h : p = q) : K.X p ≅ K.X q
```

11. `Int.instAddGroup`

```lean
instance instAddGroup         : AddGroup ℤ
```

12. `CategoryTheory.Preadditive`

```lean
class Preadditive
```

13. `Int.instAdd`

```lean
instance : Add Int
```

14. `Int`

```lean
inductive Int : Type
```

15. `AddSemigroup.toAdd`

```lean
class AddSemigroup (G : Type u) extends Add G
```

16. `ComplexShape.up`

```lean
def up (α : Type*) [Add α] [IsRightCancelAdd α] [One α] : ComplexShape α
```

17. `AddRightCancelMonoid.toAddRightCancelSemigroup`

```lean
class AddRightCancelMonoid (M : Type u) extends AddMonoid M, AddRightCancelSemigroup M
```

18. `AddGroup.toAddCancelMonoid`

```lean
AddGroup.toAddCancelMonoid
```

19. `Ring.toAddGroupWithOne`

```lean
class Ring (R : Type u) extends Semiring R, AddCommGroup R, AddGroupWithOne R
```

20. `instHAdd`

```lean
instance instHAdd [Add α] : HAdd α α α
```

21. `HAdd.hAdd`

```lean
hAdd : α → β → γ
```


---

## t045

Target: `CategoryTheory.Limits.IsLimit.ofWhiskerEquivalence`

```lean
def ofWhiskerEquivalence {s : Cone F} (e : K ≌ J) (P : IsLimit (s.whisker e.functor)) : IsLimit s
```

Proof / construction:

```lean
:=
  equivIsoLimit ((Cone.whiskeringEquivalence e).unitIso.app s).symm
    (ofRightAdjoint (Cone.whiskeringEquivalence e).toAdjunction P)
```

Candidates (23), random order:

1. `CategoryTheory.Functor.id`

```lean
protected def id : C ⥤ C
```

2. `CategoryTheory.Limits.IsLimit`

```lean
structure IsLimit (t : Cone F)
```

3. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

4. `CategoryTheory.Equivalence.inverse`

```lean
inverse : D ⥤ C
```

5. `CategoryTheory.Limits.IsLimit.equivIsoLimit`

```lean
def equivIsoLimit {r t : Cone F} (i : r ≅ t) : IsLimit r ≃ IsLimit t
```

6. `CategoryTheory.Iso.app`

```lean
def app {F G : C ⥤ D} (α : F ≅ G) (X : C) :
    F.obj X ≅ G.obj X
```

7. `CategoryTheory.Equivalence.toAdjunction`

```lean
def toAdjunction : e.functor ⊣ e.inverse
```

8. `CategoryTheory.Equivalence.unitIso`

```lean
unitIso : 𝟭 C ≅ functor ⋙ inverse
```

9. `CategoryTheory.Equivalence.functor`

```lean
functor : C ⥤ D
```

10. `CategoryTheory.Equivalence`

```lean
structure Equivalence (C : Type u₁) (D : Type u₂) [Category.{v₁} C] [Category.{v₂} D]
```

11. `Equiv`

```lean
structure Equiv (α β : Sort*)
```

12. `EquivLike.toFunLike`

```lean
instance (priority := 100) toFunLike : FunLike E α β
```

13. `CategoryTheory.Functor.comp`

```lean
def comp (F : C ⥤ D) (G : D ⥤ E) : C ⥤ E
```

14. `CategoryTheory.Functor.obj`

```lean
obj : C → D
```

15. `CategoryTheory.Limits.Cone.whisker`

```lean
def whisker (E : K ⥤ J) (c : Cone F) : Cone (E ⋙ F)
```

16. `Equiv.instEquivLike`

```lean
instance : EquivLike (α ≃ β) α β
```

17. `CategoryTheory.Limits.IsLimit.ofRightAdjoint`

```lean
def ofRightAdjoint {D : Type u₄} [Category.{v₄} D] {G : K ⥤ D} {left : Cone F ⥤ Cone G}
    {right : Cone G ⥤ Cone F}
    (adj : left ⊣ right) {c : Cone G} (t : IsLimit c) : IsLimit (right.obj c)
```

18. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

19. `CategoryTheory.Limits.Cone.whiskeringEquivalence`

```lean
def whiskeringEquivalence (e : K ≌ J) : Cone F ≌ Cone (e.functor ⋙ F)
```

20. `CategoryTheory.Limits.Cone.category`

```lean
instance Cone.category : Category (Cone F)
```

21. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

22. `CategoryTheory.Iso.symm`

```lean
def symm (I : X ≅ Y) : Y ≅ X
```

23. `CategoryTheory.Limits.Cone`

```lean
structure Cone (F : J ⥤ C)
```


---

## t046

Target: `CategoryTheory.LeftExactFunctor.of`

```lean
def LeftExactFunctor.of (F : C ⥤ D) [PreservesFiniteLimits F] : C ⥤ₗ D
```

Proof / construction:

```lean
:=
  ⟨F, by simpa⟩
```

Candidates (6), random order:

1. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

2. `CategoryTheory.ObjectProperty.FullSubcategory.mk`

```lean
structure FullSubcategory
```

3. `CategoryTheory.leftExactFunctor`

```lean
def leftExactFunctor : ObjectProperty (C ⥤ D)
```

4. `CategoryTheory.Limits.PreservesFiniteLimits`

```lean
class PreservesFiniteLimits (F : C ⥤ D) : Prop
```

5. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

6. `CategoryTheory.Functor.category`

```lean
instance Functor.category : Category.{max u₁ v₂} (C ⥤ D)
```


---

## t047

Target: `PolyEquivTensor.toFunBilinear`

```lean
def toFunBilinear : A →ₗ[A] R[X] →ₗ[R] A[X]
```

Proof / construction:

```lean
:=
  LinearMap.toSpanSingleton A _ (aeval (Polynomial.X : A[X])).toLinearMap
```

Candidates (21), random order:

1. `LinearMap`

```lean
structure LinearMap {R S : Type*} [Semiring R] [Semiring S] (σ : R →+* S) (M : Type*)
    (M₂ : Type*) [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends
    AddHom M M₂, MulActionHom σ M M₂
```

2. `AlgHom.toLinearMap`

```lean
def toLinearMap : A →ₗ[R] B
```

3. `Polynomial.module`

```lean
instance module {S} [Semiring S] [Module S R] : Module S R[X]
```

4. `LinearMap.toSpanSingleton`

```lean
def toSpanSingleton (x : M) : R →ₗ[R] M
```

5. `Algebra.id`

```lean
instance (priority := 1100) id : Algebra R R
```

6. `Polynomial.algebraOfAlgebra`

```lean
instance algebraOfAlgebra : Algebra R A[X]
```

7. `Algebra`

```lean
class Algebra (R : Type u) (A : Type v) [CommSemiring R] [Semiring A] extends SMul R A
```

8. `Semiring.toAddCommMonoid`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

9. `Algebra.toModule`

```lean
instance (priority := 200) toModule {R A} {_ : CommSemiring R} {_ : Semiring A} [Algebra R A] :
    Module R A
```

10. `Polynomial.semiring`

```lean
instance semiring : Semiring R[X]
```

11. `CommSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

12. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

13. `Polynomial.X`

```lean
def X : R[X]
```

14. `Polynomial`

```lean
structure Polynomial (R : Type*) [Semiring R]
```

15. `LinearMap.module`

```lean
instance module : Module S (M →ₛₗ[σ₁₂] M₂)
```

16. `RingHom.id`

```lean
def id (α : Type*) [NonAssocSemiring α] : α →+* α
```

17. `Polynomial.aeval`

```lean
def aeval : R[X] →ₐ[R] A
```

18. `Semiring.toModule`

```lean
instance (priority := 1100) Semiring.toModule [Semiring R] : Module R R
```

19. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

20. `LinearMap.addCommMonoid`

```lean
instance addCommMonoid : AddCommMonoid (M →ₛₗ[σ₁₂] M₂)
```

21. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```


---

## t048

Target: `Filter.instSup`

```lean
instance instSup : Max (Filter α)
```

Proof / construction:

```lean
where
  max f g := .copy (sSup {f, g}) {s | s ∈ f ∧ s ∈ g} <| by simp
```

Candidates (14), random order:

1. `Filter.instSupSet`

```lean
instance instSupSet : SupSet (Filter α)
```

2. `Filter.copy`

```lean
protected def copy (f : Filter α) (S : Set (Set α)) (hmem : ∀ s, s ∈ S ↔ s ∈ f) : Filter α
```

3. `Membership.mem`

```lean
mem : γ → α → Prop
```

4. `Set.ofPred`

```lean
def Set.ofPred {α : Type u} (p : α → Prop) : Set α
```

5. `Set.instInsert`

```lean
instance : Insert α (Set α)
```

6. `Set.instSingletonSet`

```lean
instance instSingletonSet : Singleton α (Set α)
```

7. `Max.mk`

```lean
class Max (α : Type u)
```

8. `Singleton.singleton`

```lean
singleton : α → β
```

9. `And`

```lean
structure And (a b : Prop) : Prop
```

10. `Insert.insert`

```lean
insert : α → γ → γ
```

11. `Filter.instMembership`

```lean
instance instMembership : Membership (Set α) (Filter α)
```

12. `Set`

```lean
def Set (α : Type u)
```

13. `Filter`

```lean
structure Filter (α : Type*)
```

14. `SupSet.sSup`

```lean
sSup : Set α → α
```


---
