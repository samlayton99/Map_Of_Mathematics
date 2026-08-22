# Blind grading batch 04 — 10 items

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
{"t031": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t031

Target: `Rep.instMonoidalActionTypeLinearization`

```lean
instance (f : A ⟶ B) [Mono f] : Mono f.toModuleCatHom
```

Proof / construction:

```lean
:=
  inferInstanceAs <| Mono ((forget₂ _ _).map f)
```

Candidates (18), random order:

1. `Rep.instCategory`

```lean
instance : Category (Rep.{w} k G)
```

2. `CategoryTheory.types`

```lean
instance CategoryTheory.types : Category.{u} (Type u)
```

3. `Action`

```lean
structure Action (G : Type*) [Monoid G]
```

4. `CategoryTheory.SemiCartesianMonoidalCategory.toMonoidalCategory`

```lean
class SemiCartesianMonoidalCategory (C : Type u) [Category.{v} C] extends MonoidalCategory C
```

5. `CategoryTheory.typesCartesianMonoidalCategory`

```lean
instance typesCartesianMonoidalCategory : CartesianMonoidalCategory (Type u)
```

6. `Rep.instLaxMonoidalActionTypeLinearization`

```lean
Rep.instLaxMonoidalActionTypeLinearization
```

7. `CategoryTheory.CartesianMonoidalCategory.toSemiCartesianMonoidalCategory`

```lean
class CartesianMonoidalCategory (C : Type u) [Category.{v} C] extends
    SemiCartesianMonoidalCategory C
```

8. `Rep`

```lean
structure Rep (k : Type u) (G : Type v) [Semiring k] [Monoid G]
```

9. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

10. `Rep.linearization`

```lean
abbrev linearization : Action (Type w) G ⥤ Rep.{max w u} k G
```

11. `CommRing`

```lean
class CommRing (α : Type u) extends Ring α, CommMonoid α
```

12. `CategoryTheory.Functor.Monoidal.mk`

```lean
class Monoidal (F : C ⥤ D) extends F.LaxMonoidal, F.OplaxMonoidal
```

13. `Rep.instMonoidalCategory`

```lean
Rep.instMonoidalCategory
```

14. `Rep.instOplaxMonoidalActionTypeLinearization`

```lean
Rep.instOplaxMonoidalActionTypeLinearization
```

15. `Action.instMonoidalCategory`

```lean
instance instMonoidalCategory : MonoidalCategory (Action V G)
```

16. `Monoid`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

17. `CommRing.toCommSemiring`

```lean
instance (priority := 100) CommRing.toCommSemiring [s : CommRing α] : CommSemiring α
```

18. `Action.instCategory`

```lean
instance : Category (Action V G)
```


---

## t032

Target: `FractionalIdeal`

```lean
def FractionalIdeal
```

Proof / construction:

```lean
:=
  { I : Submodule R P // IsFractional S I }
```

Candidates (12), random order:

1. `Semiring.toAddCommMonoid`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

2. `CommRing`

```lean
class CommRing (α : Type u) extends Ring α, CommMonoid α
```

3. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

4. `Submonoid`

```lean
structure Submonoid (M : Type*) [MulOneClass M] extends Subsemigroup M
```

5. `CommRing.toCommSemiring`

```lean
instance (priority := 100) CommRing.toCommSemiring [s : CommRing α] : CommSemiring α
```

6. `Algebra.toModule`

```lean
instance (priority := 200) toModule {R A} {_ : CommSemiring R} {_ : Semiring A} [Algebra R A] :
    Module R A
```

7. `IsFractional`

```lean
def IsFractional (I : Submodule R P)
```

8. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

9. `instMulZeroOneClassOfSemiring`

```lean
instance [Semiring α] : MulZeroOneClass α
```

10. `Submodule`

```lean
structure Submodule (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] [Module R M] : Type v
    extends AddSubmonoid M, SubMulAction R M
```

11. `Algebra`

```lean
class Algebra (R : Type u) (A : Type v) [CommSemiring R] [Semiring A] extends SMul R A
```

12. `MulZeroOneClass.toMulOneClass`

```lean
class MulZeroOneClass (M₀ : Type u) extends MulOneClass M₀, MulZeroClass M₀
```


---

## t033

Target: `Rep.liftHomOfSurj`

```lean
abbrev liftHomOfSurj {X Y : Rep k G} (hf : Function.Surjective f) (f' : res f X ⟶ res f Y) :
    X ⟶ Y
```

Proof / construction:

```lean
:= ofHom ⟨f'.hom.toLinearMap, fun g ↦ by obtain ⟨h, rfl⟩ := hf g; simpa using f'.hom.2 h⟩
```

Candidates (23), random order:

1. `Rep.hV2`

```lean
Rep.hV2
```

2. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

3. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

4. `Monoid.toMulOneClass`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

5. `Representation.IntertwiningMap.toLinearMap`

```lean
Representation.IntertwiningMap.toLinearMap
```

6. `Rep.ρ`

```lean
Rep.ρ
```

7. `Rep.instCategory`

```lean
instance : Category (Rep.{w} k G)
```

8. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

9. `Rep`

```lean
structure Rep (k : Type u) (G : Type v) [Semiring k] [Monoid G]
```

10. `Function.Surjective`

```lean
def Surjective (f : α → β) : Prop
```

11. `Rep.ofHom`

```lean
abbrev ofHom (f : ρ.IntertwiningMap σ) : of ρ ⟶ of σ
```

12. `Rep.Hom.hom`

```lean
abbrev Hom.hom (f : Hom A B)
```

13. `AddCommGroup.toAddCommMonoid`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

14. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

15. `Rep.V`

```lean
V : Type w
```

16. `Monoid`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

17. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

18. `MonoidHom.instFunLike`

```lean
instance MonoidHom.instFunLike : FunLike (M →* N) M N
```

19. `Rep.hV1`

```lean
Rep.hV1
```

20. `Rep.res`

```lean
abbrev res (f : H →* G) (M : Rep k G)
```

21. `MonoidHom`

```lean
structure MonoidHom (M : Type*) (N : Type*) [MulOne M] [MulOne N]
  extends OneHom M N, M →ₙ* N
```

22. `Representation.IntertwiningMap.mk`

```lean
structure IntertwiningMap extends V →ₗ[A] W
```

23. `Quiver.Hom`

```lean
Hom : V → V → Type v
```


---

## t034

Target: `NumberField.Units.complexEmbedding`

```lean
protected def complexEmbedding (φ : K →+* ℂ) : (𝓞 K)ˣ →* ℂˣ
```

Proof / construction:

```lean
:=
  (map φ).comp (map (algebraMap (𝓞 K) K).toMonoidHom)
```

Candidates (24), random order:

1. `Field.toSemifield`

```lean
instance (priority := 100) Field.toSemifield [Field K] : Semifield K
```

2. `Semifield.toDivisionSemiring`

```lean
class Semifield (K : Type*) extends CommSemiring K, DivisionSemiring K, CommGroupWithZero K
```

3. `MonoidHomClass.toMonoidHom`

```lean
def MonoidHomClass.toMonoidHom [MonoidHomClass F M N] (f : F) : M →* N
```

4. `RingHom`

```lean
structure RingHom (α : Type*) (β : Type*) [NonAssocSemiring α] [NonAssocSemiring β] extends
  α →* β, α →+ β, α →ₙ+* β, α →*₀ β
```

5. `RingHom.instFunLike`

```lean
instance instFunLike : FunLike (α →+* β) α β
```

6. `Field`

```lean
class Field (K : Type u) extends CommRing K, DivisionRing K
```

7. `NumberField.RingOfIntegers.instAlgebra_1`

```lean
NumberField.RingOfIntegers.instAlgebra_1
```

8. `CommRing.toCommSemiring`

```lean
instance (priority := 100) CommRing.toCommSemiring [s : CommRing α] : CommSemiring α
```

9. `DivisionSemiring.toSemiring`

```lean
class DivisionSemiring (K : Type*) extends Semiring K, GroupWithZero K, NNRatCast K
```

10. `Complex.instSemiring`

```lean
instance : Semiring ℂ
```

11. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

12. `MonoidHom.comp`

```lean
def MonoidHom.comp [MulOne M] [MulOne N] [MulOne P] (hnp : N →* P) (hmn : M →* N) :
    M →* P
```

13. `Units.instMulOneClass`

```lean
instance instMulOneClass : MulOneClass αˣ
```

14. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

15. `NumberField.instCommRingRingOfIntegers`

```lean
NumberField.instCommRingRingOfIntegers
```

16. `Units.map`

```lean
def map (f : M →* N) : Mˣ →* Nˣ
```

17. `Semiring.toMonoid`

```lean
Semiring.toMonoid
```

18. `Monoid.toMulOneClass`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

19. `RingHom.toMonoidHom`

```lean
RingHom.toMonoidHom
```

20. `NumberField.RingOfIntegers`

```lean
def RingOfIntegers : Type _
```

21. `Units`

```lean
structure Units (α : Type u) [Monoid α]
```

22. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

23. `Algebra.algebraMap`

```lean
Algebra.algebraMap
```

24. `Complex`

```lean
structure Complex : Type
```


---

## t035

Target: `CategoryTheory.CostructuredArrow.costructuredArrowToOverEquivalence.inverse`

```lean
def inverse : CostructuredArrow F Y.left ⥤ CostructuredArrow (toOver F X) Y
```

Proof / construction:

```lean
where
  obj Z :=
    CostructuredArrow.mk (Y := CostructuredArrow.mk (Z.hom ≫ Y.hom))
      (Over.homMk Z.hom)
  map f :=
    CostructuredArrow.homMk
      (CostructuredArrow.homMk f.left)
        (by ext; exact CostructuredArrow.w f)
```

Candidates (25), random order:

1. `CategoryTheory.CostructuredArrow.toOver`

```lean
def toOver (F : D ⥤ T) (X : T) : CostructuredArrow F X ⥤ Over X
```

2. `CategoryTheory.Over`

```lean
def Over (X : T)
```

3. `CategoryTheory.CommaMorphism.left`

```lean
left : X.left ⟶ Y.left
```

4. `CategoryTheory.Functor.mk`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

5. `CategoryTheory.CostructuredArrow.left`

```lean
abbrev left (X : CostructuredArrow S T) : C
```

6. `CategoryTheory.Functor.obj`

```lean
obj : C → D
```

7. `CategoryTheory.CostructuredArrow`

```lean
def CostructuredArrow (S : C ⥤ D) (T : D)
```

8. `CategoryTheory.CategoryStruct.comp`

```lean
comp : ∀ {X Y Z : obj}, (X ⟶ Y) → (Y ⟶ Z) → (X ⟶ Z)
```

9. `CategoryTheory.Over.homMk`

```lean
def homMk {U V : Over X} (f : U.left ⟶ V.left) (w : f ≫ V.hom = U.hom := by cat_disch) : U ⟶ V
```

10. `CategoryTheory.Functor.fromPUnit`

```lean
abbrev fromPUnit (X : C) : Discrete PUnit.{w + 1} ⥤ C
```

11. `CategoryTheory.Discrete`

```lean
structure Discrete (α : Type u₁)
```

12. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

13. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

14. `CategoryTheory.discreteCategory`

```lean
instance discreteCategory (α : Type u₁) : SmallCategory (Discrete α)
```

15. `CategoryTheory.Over.hom`

```lean
abbrev hom (f : Over X) : f.left ⟶ X
```

16. `CategoryTheory.CostructuredArrow.homMk`

```lean
def homMk {f f' : CostructuredArrow S T} (g : f.left ⟶ f'.left)
    (w : S.map g ≫ f'.hom = f.hom := by cat_disch) : f ⟶ f'
```

17. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

18. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

19. `CategoryTheory.CostructuredArrow.mk`

```lean
def mk (f : S.obj Y ⟶ T) : CostructuredArrow S T
```

20. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

21. `CategoryTheory.CostructuredArrow.hom`

```lean
abbrev hom (X : CostructuredArrow S T) : S.obj X.left ⟶ T
```

22. `CategoryTheory.instCategoryOver`

```lean
CategoryTheory.instCategoryOver
```

23. `CategoryTheory.instCategoryCostructuredArrow_1`

```lean
CategoryTheory.instCategoryCostructuredArrow_1
```

24. `CategoryTheory.Over.left`

```lean
abbrev left (f : Over X) : T
```

25. `PUnit`

```lean
inductive PUnit : Sort u
```


---

## t036

Target: `HurwitzZeta.completedHurwitzZetaEven₀`

```lean
def completedHurwitzZetaEven₀ (a : UnitAddCircle) (s : ℂ) : ℂ
```

Proof / construction:

```lean
:=
  ((hurwitzEvenFEPair a).Λ₀ (s / 2)) / 2
```

Candidates (16), random order:

1. `instOfNatAtLeastTwo`

```lean
instance (priority := 100) instOfNatAtLeastTwo {n : ℕ} [NatCast R] [Nat.AtLeastTwo n] :
    OfNat R n
```

2. `NormedAddCommGroup.toSeminormedAddCommGroup`

```lean
NormedAddCommGroup.toSeminormedAddCommGroup
```

3. `instHDiv`

```lean
instance instHDiv [Div α] : HDiv α α α
```

4. `Complex.instNormedAddCommGroup`

```lean
instance instNormedAddCommGroup : NormedAddCommGroup ℂ
```

5. `InnerProductSpace.toNormedSpace`

```lean
class InnerProductSpace (𝕜 : Type*) (E : Type*) [RCLike 𝕜] [SeminormedAddCommGroup E] extends
    NormedSpace 𝕜 E, Inner 𝕜 E
```

6. `UnitAddCircle`

```lean
abbrev UnitAddCircle
```

7. `Complex.instDivInvMonoid`

```lean
noncomputable instance instDivInvMonoid : DivInvMonoid ℂ
```

8. `RCLike.innerProductSpace`

```lean
instance RCLike.innerProductSpace : InnerProductSpace 𝕜 𝕜
```

9. `Complex.instRCLike`

```lean
noncomputable instance : RCLike ℂ
```

10. `HDiv.hDiv`

```lean
hDiv : α → β → γ
```

11. `OfNat.ofNat`

```lean
ofNat : α
```

12. `Complex.instNatCast`

```lean
instance instNatCast : NatCast ℂ
```

13. `DivInvMonoid.toDiv`

```lean
class DivInvMonoid (G : Type u) extends Monoid G, Inv G, Div G, ZPow G
```

14. `WeakFEPair.Λ₀`

```lean
def Λ₀ : ℂ → E
```

15. `Complex`

```lean
structure Complex : Type
```

16. `HurwitzZeta.hurwitzEvenFEPair`

```lean
def hurwitzEvenFEPair (a : UnitAddCircle) : WeakFEPair ℂ
```


---

## t037

Target: `CategoryTheory.inhabitedLiftsToColimit`

```lean
instance inhabitedLiftsToColimit (K : J ⥤ C) (F : C ⥤ D) [CreatesColimit K F] (c : Cocone (K ⋙ F))
    (t : IsColimit c) : Inhabited (LiftsToColimit _ _ _ t)
```

Proof / construction:

```lean
:=
  ⟨liftsToColimitOfCreates K F c t⟩
```

Candidates (9), random order:

1. `CategoryTheory.Limits.Cocone`

```lean
structure Cocone (F : J ⥤ C)
```

2. `CategoryTheory.LiftsToColimit`

```lean
structure LiftsToColimit (K : J ⥤ C) (F : C ⥤ D) (c : Cocone (K ⋙ F)) (t : IsColimit c) extends
  LiftableCocone K F c
```

3. `CategoryTheory.Limits.IsColimit`

```lean
structure IsColimit (t : Cocone F)
```

4. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

5. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

6. `Inhabited.mk`

```lean
class Inhabited (α : Sort u)
```

7. `CategoryTheory.liftsToColimitOfCreates`

```lean
def liftsToColimitOfCreates (K : J ⥤ C) (F : C ⥤ D) [CreatesColimit K F] (c : Cocone (K ⋙ F))
    (t : IsColimit c) : LiftsToColimit K F c t
```

8. `CategoryTheory.CreatesColimit`

```lean
class CreatesColimit (K : J ⥤ C) (F : C ⥤ D) extends ReflectsColimit K F
```

9. `CategoryTheory.Functor.comp`

```lean
def comp (F : C ⥤ D) (G : D ⥤ E) : C ⥤ E
```


---

## t038

Target: `Lean.PrettyPrinter.Delaborator.annotateGoToSyntaxDef`

```lean
def annotateGoToSyntaxDef (stx : Term) : DelabM Term
```

Proof / construction:

```lean
:= do
  annotateGoToDef stx stx.raw.getKind
```

Candidates (7), random order:

1. `Lean.Syntax.getKind`

```lean
def getKind (stx : Syntax) : SyntaxNodeKind
```

2. `Lean.PrettyPrinter.Delaborator.annotateGoToDef`

```lean
def annotateGoToDef (stx : Term) (target : Name) : DelabM Term
```

3. `Lean.Name.mkStr1`

```lean
@[expose, reducible] def mkStr1 (s₁ : String) : Name
```

4. `Lean.Syntax.Term`

```lean
abbrev Term
```

5. `Lean.SyntaxNodeKind`

```lean
abbrev SyntaxNodeKind
```

6. `Lean.TSyntax.raw`

```lean
raw : Syntax
```

7. `List.nil`

```lean
| nil : List α
```


---

## t039

Target: `AffineMap.prodMap`

```lean
def prodMap (f : P1 →ᵃ[k] P2) (g : P3 →ᵃ[k] P4) : P1 × P3 →ᵃ[k] P2 × P4
```

Proof / construction:

```lean
where
  toFun := Prod.map f g
  linear := f.linear.prodMap g.linear
  map_vadd' := by simp
```

Candidates (18), random order:

1. `AddCommGroup.toAddGroup`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

2. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

3. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

4. `AffineMap.linear`

```lean
linear : V1 →ₗ[k] V2
```

5. `Ring`

```lean
class Ring (R : Type u) extends Semiring R, AddCommGroup R, AddGroupWithOne R
```

6. `Prod.instAddTorsor`

```lean
Prod.instAddTorsor
```

7. `Prod.map`

```lean
@[implicit_reducible] def Prod.map {α₁ : Type u₁} {α₂ : Type u₂} {β₁ : Type v₁} {β₂ : Type v₂}
    (f : α₁ → α₂) (g : β₁ → β₂) : α₁ × β₁ → α₂ × β₂
  | (a, b) => (f a, g b)
```

8. `Prod`

```lean
structure Prod (α : Type u) (β : Type v)
```

9. `AddTorsor`

```lean
class AddTorsor (G : outParam Type*) (P : Type*) [AddGroup G] extends AddAction G P,
  VSub G P
```

10. `Prod.instAddCommGroup`

```lean
Prod.instAddCommGroup
```

11. `AddCommGroup.toAddCommMonoid`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

12. `LinearMap.prodMap`

```lean
def prodMap (f : M →ₗ[R] M₃) (g : M₂ →ₗ[R] M₄) : M × M₂ →ₗ[R] M₃ × M₄
```

13. `AffineMap.mk`

```lean
structure AffineMap (k : Type*) {V1 : Type*} (P1 : Type*) {V2 : Type*} (P2 : Type*) [Ring k]
  [AddCommGroup V1] [Module k V1] [AffineSpace V1 P1] [AddCommGroup V2] [Module k V2]
  [AffineSpace V2 P2]
```

14. `AffineMap`

```lean
structure AffineMap (k : Type*) {V1 : Type*} (P1 : Type*) {V2 : Type*} (P2 : Type*) [Ring k]
  [AddCommGroup V1] [Module k V1] [AffineSpace V1 P1] [AddCommGroup V2] [Module k V2]
  [AffineSpace V2 P2]
```

15. `Prod.instModule`

```lean
instance instModule [Semiring R] [AddCommMonoid M] [AddCommMonoid N] [Module R M] [Module R N] :
    Module R (M × N)
```

16. `Ring.toSemiring`

```lean
class Ring (R : Type u) extends Semiring R, AddCommGroup R, AddGroupWithOne R
```

17. `AddCommGroup`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

18. `AffineMap.instFunLike`

```lean
instance AffineMap.instFunLike (k : Type*) {V1 : Type*} (P1 : Type*) {V2 : Type*} (P2 : Type*)
    [Ring k] [AddCommGroup V1] [Module k V1] [AffineSpace V1 P1] [AddCommGroup V2] [Module k V2]
    [AffineSpace V2 P2] : FunLike (P1 →ᵃ[k] P2) P1 P2
```


---

## t040

Target: `CategoryTheory.Limits.Cotrident.π`

```lean
abbrev Cotrident.π (t : Cotrident f)
```

Proof / construction:

```lean
:=
  t.ι.app one
```

Candidates (16), random order:

1. `CategoryTheory.Functor.category`

```lean
instance Functor.category : Category.{max u₁ v₂} (C ⥤ D)
```

2. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

3. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

4. `CategoryTheory.Functor.obj`

```lean
obj : C → D
```

5. `CategoryTheory.Functor.const`

```lean
def const : C ⥤ J ⥤ C
```

6. `CategoryTheory.Limits.Cotrident`

```lean
abbrev Cotrident
```

7. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

8. `CategoryTheory.Limits.WalkingParallelFamily.one`

```lean
| one : WalkingParallelFamily J
```

9. `CategoryTheory.NatTrans.app`

```lean
CategoryTheory.NatTrans.app
```

10. `CategoryTheory.Limits.WalkingParallelFamily`

```lean
inductive WalkingParallelFamily (J : Type w) : Type w
  | zero : WalkingParallelFamily J
  | one : WalkingParallelFamily J
```

11. `CategoryTheory.Limits.WalkingParallelFamily.category`

```lean
instance WalkingParallelFamily.category : SmallCategory (WalkingParallelFamily J)
```

12. `CategoryTheory.Limits.parallelFamily`

```lean
def parallelFamily : WalkingParallelFamily J ⥤ C
```

13. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

14. `CategoryTheory.Limits.Cocone.pt`

```lean
pt : C
```

15. `CategoryTheory.Limits.Cocone.ι`

```lean
CategoryTheory.Limits.Cocone.ι
```

16. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```


---
