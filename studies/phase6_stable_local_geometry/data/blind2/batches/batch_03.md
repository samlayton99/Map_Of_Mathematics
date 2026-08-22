# Blind grading batch 03 — 10 items

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
{"t021": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t021

Target: `CategoryTheory.Limits.coequalizer.isoTargetOfSelf`

```lean
noncomputable def coequalizer.isoTargetOfSelf : coequalizer f f ≅ Y
```

Proof / construction:

```lean
:=
  (asIso (coequalizer.π f f)).symm
```

Candidates (8), random order:

1. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

2. `CategoryTheory.Limits.coequalizer`

```lean
noncomputable abbrev coequalizer : C
```

3. `CategoryTheory.Limits.coequalizer.π`

```lean
noncomputable abbrev coequalizer.π : Y ⟶ coequalizer f g
```

4. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

5. `CategoryTheory.Iso.symm`

```lean
def symm (I : X ≅ Y) : Y ≅ X
```

6. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

7. `CategoryTheory.asIso`

```lean
noncomputable def asIso (f : X ⟶ Y) [IsIso f] : X ≅ Y
```

8. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```


---

## t022

Target: `CategoryTheory.Limits.createsLimitsOfShapeOfRightOp`

```lean
def createsLimitsOfShapeOfRightOp (F : Cᵒᵖ ⥤ D) [CreatesColimitsOfShape Jᵒᵖ F.rightOp] :
    CreatesLimitsOfShape J F
```

Proof / construction:

```lean
where CreatesLimit {K} := createsLimitOfRightOp K F
```

Candidates (10), random order:

1. `CategoryTheory.Functor.rightOp`

```lean
protected def rightOp (F : Cᵒᵖ ⥤ D) : C ⥤ Dᵒᵖ
```

2. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

3. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

4. `CategoryTheory.CreatesLimitsOfShape.mk`

```lean
class CreatesLimitsOfShape (J : Type w) [Category.{w'} J] (F : C ⥤ D)
```

5. `CategoryTheory.Limits.createsLimitOfRightOp`

```lean
def createsLimitOfRightOp (K : J ⥤ Cᵒᵖ) (F : Cᵒᵖ ⥤ D) [CreatesColimit K.leftOp F.rightOp] :
    CreatesLimit K F
```

6. `CategoryTheory.CreatesColimitsOfShape.CreatesColimit`

```lean
CreatesColimit : ∀ {K : J ⥤ C}, CreatesColimit K F
```

7. `Opposite`

```lean
structure Opposite
```

8. `CategoryTheory.Functor.leftOp`

```lean
protected def leftOp (F : C ⥤ Dᵒᵖ) : Cᵒᵖ ⥤ D
```

9. `CategoryTheory.CreatesColimitsOfShape`

```lean
class CreatesColimitsOfShape (J : Type w) [Category.{w'} J] (F : C ⥤ D)
```

10. `CategoryTheory.Category.opposite`

```lean
instance Category.opposite : Category.{v₁} Cᵒᵖ
```


---

## t023

Target: `CategoryTheory.StructuredArrow.ofDiagEquivalence.functor`

```lean
def ofDiagEquivalence.functor (X : T × T) :
    StructuredArrow X (Functor.diag _) ⥤ StructuredArrow X.2 (Under.forget X.1)
```

Proof / construction:

```lean
:=
  Functor.toStructuredArrow
    (Functor.toUnder (StructuredArrow.proj X _) _
      (fun f ↦ f.hom.1) (fun g ↦ by simp [← w g])) _ _
    (fun f ↦ f.hom.2) (fun g ↦ by simp [← w g])
```

Candidates (20), random order:

1. `Prod.snd`

```lean
snd : β
```

2. `CategoryTheory.uniformProd`

```lean
instance uniformProd : Category (C × D)
```

3. `CategoryTheory.Under`

```lean
def Under (X : T)
```

4. `Prod`

```lean
structure Prod (α : Type u) (β : Type v)
```

5. `CategoryTheory.Under.forget`

```lean
def forget : Under X ⥤ T
```

6. `CategoryTheory.Functor.obj`

```lean
obj : C → D
```

7. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

8. `CategoryTheory.instCategoryUnder`

```lean
CategoryTheory.instCategoryUnder
```

9. `CategoryTheory.Functor.toUnder`

```lean
def toUnder (F : S ⥤ T) (X : T) (f : (Y : S) → X ⟶ F.obj Y)
    (h : ∀ {Y Z : S} (g : Y ⟶ Z), f Y ≫ F.map g = f Z) : S ⥤ Under X
```

10. `Prod.fst`

```lean
fst : α
```

11. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

12. `CategoryTheory.StructuredArrow.proj`

```lean
def proj (S : D) (T : C ⥤ D) : StructuredArrow S T ⥤ C
```

13. `CategoryTheory.StructuredArrow.right`

```lean
abbrev right (X : StructuredArrow S T) : C
```

14. `CategoryTheory.Functor.toStructuredArrow`

```lean
def toStructuredArrow (G : E ⥤ C) (X : D) (F : C ⥤ D) (f : (Y : E) → X ⟶ F.obj (G.obj Y))
    (h : ∀ {Y Z : E} (g : Y ⟶ Z), f Y ≫ F.map (G.map g) = f Z) : E ⥤ StructuredArrow X F
```

15. `CategoryTheory.Functor.diag`

```lean
def diag : C ⥤ C × C
```

16. `CategoryTheory.instCategoryStructuredArrow`

```lean
CategoryTheory.instCategoryStructuredArrow
```

17. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

18. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

19. `CategoryTheory.StructuredArrow`

```lean
def StructuredArrow (S : D) (T : C ⥤ D)
```

20. `CategoryTheory.StructuredArrow.hom`

```lean
abbrev hom (X : StructuredArrow S T) : S ⟶ T.obj X.right
```


---

## t024

Target: `Set.DefinableFun`

```lean
def DefinableFun (f : (α → M) → M) : Prop
```

Proof / construction:

```lean
:=
  A.Definable L f.tupleGraph
```

Candidates (6), random order:

1. `Set.Definable`

```lean
def Definable (s : Set (α → M)) : Prop
```

2. `FirstOrder.Language.Structure`

```lean
class Structure
```

3. `Option`

```lean
inductive Option (α : Type u)
```

4. `Set`

```lean
def Set (α : Type u)
```

5. `FirstOrder.Language`

```lean
structure Language
```

6. `Function.tupleGraph`

```lean
def tupleGraph (f : (α → β) → β) : Set (Option α → β)
```


---

## t025

Target: `GroupTopology.instTop`

```lean
instance : Top (GroupTopology α)
```

Proof / construction:

```lean
:=
  let _t : TopologicalSpace α := ⊤
  ⟨{  continuous_mul := continuous_top
      continuous_inv := continuous_top }⟩
```

Candidates (15), random order:

1. `SemilatticeSup.toPartialOrder`

```lean
class SemilatticeSup (α : Type u) extends PartialOrder α
```

2. `Top.mk`

```lean
class Top (α : Type*)
```

3. `BoundedOrder.toOrderTop`

```lean
class BoundedOrder (α : Type u) [LE α] extends OrderTop α, OrderBot α
```

4. `GroupTopology`

```lean
structure GroupTopology (α : Type u) [Group α] : Type u
  extends TopologicalSpace α, IsTopologicalGroup α
```

5. `CompleteLattice.toLattice`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

6. `Group`

```lean
class Group (G : Type u) extends DivInvMonoid G
```

7. `Lattice.toSemilatticeSup`

```lean
class Lattice (α : Type u) extends SemilatticeSup α, SemilatticeInf α
```

8. `GroupTopology.mk`

```lean
structure GroupTopology (α : Type u) [Group α] : Type u
  extends TopologicalSpace α, IsTopologicalGroup α
```

9. `CompleteLattice.toBoundedOrder`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

10. `Top.top`

```lean
top : α
```

11. `OrderTop.toTop`

```lean
class OrderTop (α : Type u) [LE α] extends Top α
```

12. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

13. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

14. `TopologicalSpace.instCompleteLattice`

```lean
instance : CompleteLattice (TopologicalSpace α)
```

15. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```


---

## t026

Target: `TopCat.toDeltaGenerated`

```lean
abbrev TopCat.toDeltaGenerated : TopCat.{u} ⥤ DeltaGenerated.{u}
```

Proof / construction:

```lean
:=
  TopCat.toGeneratedByTopCat
```

Candidates (8), random order:

1. `PseudoMetricSpace.toUniformSpace`

```lean
toUniformSpace : UniformSpace α
```

2. `Fin`

```lean
structure Fin (n : Nat)
```

3. `Pi.topologicalSpace`

```lean
instance Pi.topologicalSpace {ι : Type*} {Y : ι → Type v} [t₂ : (i : ι) → TopologicalSpace (Y i)] :
    TopologicalSpace ((i : ι) → Y i)
```

4. `Nat`

```lean
inductive Nat
```

5. `UniformSpace.toTopologicalSpace`

```lean
class UniformSpace (α : Type u) extends TopologicalSpace α
```

6. `Real.pseudoMetricSpace`

```lean
instance Real.pseudoMetricSpace : PseudoMetricSpace ℝ
```

7. `Real`

```lean
structure Real
```

8. `TopCat.toGeneratedByTopCat`

```lean
def TopCat.toGeneratedByTopCat : TopCat.{v} ⥤ GeneratedByTopCat X
```


---

## t027

Target: `HomotopicalAlgebra.RightHomotopyRel.rightHomotopy`

```lean
noncomputable def RightHomotopyRel.rightHomotopy
    (h : RightHomotopyRel f g) (P : PathObject Y) [P.IsGood] :
    P.RightHomotopy f g
```

Proof / construction:

```lean
:=
  LeftHomotopyRel.rightHomotopy (by rwa [leftHomotopyRel_iff_rightHomotopyRel]) _
```

Candidates (14), random order:

1. `HomotopicalAlgebra.ModelCategory.categoryWithFibrations`

```lean
categoryWithFibrations : CategoryWithFibrations C
```

2. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

3. `HomotopicalAlgebra.ModelCategory`

```lean
class ModelCategory
```

4. `HomotopicalAlgebra.IsFibrant`

```lean
abbrev IsFibrant (X : C) : Prop
```

5. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

6. `HomotopicalAlgebra.ModelCategory.categoryWithCofibrations`

```lean
categoryWithCofibrations : CategoryWithCofibrations C
```

7. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

8. `HomotopicalAlgebra.ModelCategory.categoryWithWeakEquivalences`

```lean
categoryWithWeakEquivalences : CategoryWithWeakEquivalences C
```

9. `HomotopicalAlgebra.PathObject.IsGood`

```lean
class IsGood [HasBinaryProduct A A] [CategoryWithFibrations C] : Prop
```

10. `HomotopicalAlgebra.LeftHomotopyRel.rightHomotopy`

```lean
noncomputable def rightHomotopy (h : LeftHomotopyRel f g) (Q : PathObject Y) [Q.IsGood] :
    Q.RightHomotopy f g
```

11. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

12. `HomotopicalAlgebra.PathObject`

```lean
structure PathObject [CategoryWithWeakEquivalences C] (A : C) extends PrepathObject A
```

13. `HomotopicalAlgebra.RightHomotopyRel`

```lean
def RightHomotopyRel [CategoryWithWeakEquivalences C] : HomRel C
```

14. `HomotopicalAlgebra.IsCofibrant`

```lean
abbrev IsCofibrant (X : C) : Prop
```


---

## t028

Target: `Complex.ofRealCLM`

```lean
def ofRealCLM : ℝ →L[ℝ] ℂ
```

Proof / construction:

```lean
:=
  ofRealLI.toContinuousLinearMap
```

Candidates (19), random order:

1. `LinearIsometry.toContinuousLinearMap`

```lean
def toContinuousLinearMap : E →SL[σ₁₂] E₂
```

2. `Complex.ofRealLI`

```lean
def ofRealLI : ℝ →ₗᵢ[ℝ] ℂ
```

3. `Real`

```lean
structure Real
```

4. `NormedSpace.toModule`

```lean
class NormedSpace (𝕜 : Type*) (E : Type*) [NormedField 𝕜] [SeminormedAddCommGroup E]
    extends Module 𝕜 E
```

5. `Complex.instNormedField`

```lean
instance : NormedField ℂ
```

6. `SeminormedCommRing.toNonUnitalSeminormedCommRing`

```lean
instance (priority := 100) SeminormedCommRing.toNonUnitalSeminormedCommRing
    [β : SeminormedCommRing α] : NonUnitalSeminormedCommRing α
```

7. `NormedField.toNormedSpace`

```lean
instance NormedField.toNormedSpace : NormedSpace 𝕜 𝕜
```

8. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

9. `Semiring.toModule`

```lean
instance (priority := 1100) Semiring.toModule [Semiring R] : Module R R
```

10. `RingHom.id`

```lean
def id (α : Type*) [NonAssocSemiring α] : α →+* α
```

11. `NormedSpace.complexToReal`

```lean
instance (priority := 900) _root_.NormedSpace.complexToReal : NormedSpace ℝ E
```

12. `Real.normedField`

```lean
noncomputable instance Real.normedField : NormedField ℝ
```

13. `NormedCommRing.toSeminormedCommRing`

```lean
instance (priority := 100) NormedCommRing.toSeminormedCommRing [β : NormedCommRing α] :
    SeminormedCommRing α
```

14. `Complex`

```lean
structure Complex : Type
```

15. `NonUnitalSeminormedRing.toSeminormedAddCommGroup`

```lean
instance (priority := 100) NonUnitalSeminormedRing.toSeminormedAddCommGroup
    [NonUnitalSeminormedRing α] : SeminormedAddCommGroup α
```

16. `Real.semiring`

```lean
instance semiring : Semiring ℝ
```

17. `NormedField.toNormedCommRing`

```lean
instance (priority := 100) NormedField.toNormedCommRing : NormedCommRing α
```

18. `Real.normedCommRing`

```lean
instance Real.normedCommRing : NormedCommRing ℝ
```

19. `NonUnitalSeminormedCommRing.toNonUnitalSeminormedRing`

```lean
class NonUnitalSeminormedCommRing (α : Type*)
    extends NonUnitalSeminormedRing α, NonUnitalCommRing α
```


---

## t029

Target: `MeasureTheory.Measure.inv`

```lean
protected noncomputable def inv [Inv G] (μ : Measure G) : Measure G
```

Proof / construction:

```lean
:=
  Measure.map inv μ
```

Candidates (5), random order:

1. `Inv`

```lean
class Inv (α : Type u)
```

2. `MeasureTheory.Measure`

```lean
structure Measure (α : Type*) [MeasurableSpace α] extends OuterMeasure α
```

3. `MeasurableSpace`

```lean
@[class] structure MeasurableSpace (α : Type*)
```

4. `MeasureTheory.Measure.map`

```lean
MeasureTheory.Measure.map
```

5. `Inv.inv`

```lean
inv : α → α
```


---

## t030

Target: `Polynomial.natTrailingDegree`

```lean
def natTrailingDegree (p : R[X]) : ℕ
```

Proof / construction:

```lean
:=
  ENat.toNat (trailingDegree p)
```

Candidates (4), random order:

1. `ENat.toNat`

```lean
def toNat : ℕ∞ → ℕ
```

2. `Polynomial.trailingDegree`

```lean
def trailingDegree (p : R[X]) : ℕ∞
```

3. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

4. `Polynomial`

```lean
structure Polynomial (R : Type*) [Semiring R]
```


---
