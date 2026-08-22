# Blind grading batch 10 — 10 items

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
{"t091": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t091

Target: `Disjoint.frontier_right`

```lean
theorem Disjoint.frontier_right (hs : IsOpen s) (hd : Disjoint s t) : Disjoint s (frontier t)
```

Proof / construction:

```lean
:=
  (hd.symm.frontier_left hs).symm
```

Candidates (18), random order:

1. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

2. `Order.Frame.toHeytingAlgebra`

```lean
class Order.Frame (α : Type*) extends CompleteLattice α, HeytingAlgebra α
```

3. `Disjoint.frontier_left`

```lean
theorem Disjoint.frontier_left (ht : IsOpen t) (hd : Disjoint s t) : Disjoint (frontier s) t
```

4. `ConditionallyCompletePartialOrder.toConditionallyCompletePartialOrderSup`

```lean
class ConditionallyCompletePartialOrder (α : Type*)
    extends ConditionallyCompletePartialOrderSup α, ConditionallyCompletePartialOrderInf α
```

5. `HeytingAlgebra.toOrderBot`

```lean
class HeytingAlgebra (α : Type*) extends GeneralizedHeytingAlgebra α, OrderBot α, Compl α
```

6. `CompleteBooleanAlgebra.toCompleteLattice`

```lean
class CompleteBooleanAlgebra (α) extends CompleteLattice α, BooleanAlgebra α
```

7. `Disjoint.symm`

```lean
theorem Disjoint.symm ⦃a b : α⦄ : Disjoint a b → Disjoint b a
```

8. `CompleteBooleanAlgebra.toCompleteDistribLattice`

```lean
instance (priority := 100) CompleteBooleanAlgebra.toCompleteDistribLattice
    [CompleteBooleanAlgebra α] : CompleteDistribLattice α
```

9. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`

```lean
class CompleteAtomicBooleanAlgebra (α : Type u) extends CompleteBooleanAlgebra α
```

10. `CompleteLattice.toConditionallyCompleteLattice`

```lean
instance (priority := 100) CompleteLattice.toConditionallyCompleteLattice [CompleteLattice α] :
    ConditionallyCompleteLattice α
```

11. `CompleteDistribLattice.toFrame`

```lean
class CompleteDistribLattice (α : Type*) extends Frame α, Coframe α, BiheytingAlgebra α
```

12. `IsOpen`

```lean
def IsOpen : Set X → Prop
```

13. `frontier`

```lean
def frontier (s : Set X) : Set X
```

14. `Set.instCompleteAtomicBooleanAlgebra`

```lean
instance instCompleteAtomicBooleanAlgebra : CompleteAtomicBooleanAlgebra (Set α)
```

15. `ConditionallyCompleteLattice.toConditionallyCompletePartialOrder`

```lean
instance (priority := 100) ConditionallyCompleteLattice.toConditionallyCompletePartialOrder :
    ConditionallyCompletePartialOrder α
```

16. `ConditionallyCompletePartialOrderSup.toPartialOrder`

```lean
class ConditionallyCompletePartialOrderSup (α : Type*)
    extends PartialOrder α, SupSet α
```

17. `Set`

```lean
def Set (α : Type u)
```

18. `Disjoint`

```lean
def Disjoint (a b : α) : Prop
```


---

## t092

Target: `iSup_or`

```lean
theorem iSup_or {p q : Prop} {s : p ∨ q → α} :
    ⨆ x, s x = (⨆ i, s (Or.inl i)) ⊔ ⨆ j, s (Or.inr j)
```

Proof / construction:

```lean
:=
  le_antisymm
    (iSup_le fun i =>
      match i with
      | Or.inl _ => le_sup_of_le_left <| le_iSup (fun _ => s _) _
      | Or.inr _ => le_sup_of_le_right <| le_iSup (fun _ => s _) _)
    (sup_le (iSup_comp_le _ _) (iSup_comp_le _ _))
```

Candidates (23), random order:

1. `CompleteSemilatticeInf.toPartialOrder`

```lean
class CompleteSemilatticeInf (α : Type*) extends PartialOrder α, InfSet α
```

2. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

3. `CompleteLattice.toCompleteSemilatticeInf`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

4. `LE.le`

```lean
le : α → α → Prop
```

5. `Or`

```lean
inductive Or (a b : Prop) : Prop
```

6. `CompleteLattice.toCompleteSemilatticeSup`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

7. `le_sup_of_le_right`

```lean
theorem le_sup_of_le_right (h : c ≤ b) : c ≤ a ⊔ b
```

8. `SemilatticeSup.toMax`

```lean
instance SemilatticeSup.toMax [SemilatticeSup α] : Max α
```

9. `CompleteLattice.toLattice`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

10. `iSup`

```lean
def iSup [SupSet α] (s : ι → α) : α
```

11. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

12. `iSup_le`

```lean
theorem iSup_le (h : ∀ i, f i ≤ a) : iSup f ≤ a
```

13. `Or.inl`

```lean
| inl (h : a) : Or a b
```

14. `Or.inr`

```lean
| inr (h : b) : Or a b
```

15. `le_iSup`

```lean
theorem le_iSup (f : ι → α) (i : ι) : f i ≤ iSup f
```

16. `CompleteLattice`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

17. `CompleteSemilatticeSup.toSupSet`

```lean
class CompleteSemilatticeSup (α : Type*) extends PartialOrder α, SupSet α
```

18. `le_sup_of_le_left`

```lean
theorem le_sup_of_le_left (h : c ≤ a) : c ≤ a ⊔ b
```

19. `iSup_comp_le`

```lean
theorem iSup_comp_le {ι' : Sort*} (f : ι' → α) (g : ι → ι') : ⨆ x, f (g x) ≤ ⨆ y, f y
```

20. `sup_le`

```lean
theorem sup_le : a ≤ c → b ≤ c → a ⊔ b ≤ c
```

21. `le_antisymm`

```lean
lemma le_antisymm : a ≤ b → b ≤ a → a = b
```

22. `Max.max`

```lean
max : α → α → α
```

23. `Lattice.toSemilatticeSup`

```lean
class Lattice (α : Type u) extends SemilatticeSup α, SemilatticeInf α
```


---

## t093

Target: `CategoryTheory.Mon.whiskerLeft_hom`

```lean
lemma whiskerLeft_hom {X Y : Mon C} (f : X ⟶ Y) (Z : Mon C) : (f ▷ Z).hom = f.hom ▷ Z.X
```

Proof / construction:

```lean
:= rfl
```

Candidates (14), random order:

1. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

2. `CategoryTheory.BraidedCategory`

```lean
class BraidedCategory (C : Type u) [Category.{v} C] [MonoidalCategory.{v} C]
```

3. `CategoryTheory.Mon`

```lean
structure Mon
```

4. `CategoryTheory.MonoidalCategoryStruct.tensorObj`

```lean
tensorObj : C → C → C
```

5. `CategoryTheory.Mon.X`

```lean
X : C
```

6. `CategoryTheory.Mon.monMonoidalStruct`

```lean
instance monMonoidalStruct : MonoidalCategoryStruct (Mon C)
```

7. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

8. `CategoryTheory.MonoidalCategoryStruct.whiskerRight`

```lean
CategoryTheory.MonoidalCategoryStruct.whiskerRight
```

9. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

10. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

11. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

12. `CategoryTheory.Mon.instCategory`

```lean
instance : Category (Mon C)
```

13. `CategoryTheory.MonoidalCategory`

```lean
class MonoidalCategory (C : Type u) [𝒞 : Category.{v} C] extends MonoidalCategoryStruct C
```

14. `CategoryTheory.Mon.Hom.hom`

```lean
hom : M.X ⟶ N.X
```


---

## t094

Target: `CategoryTheory.Functor.final_of_comp_full_faithful'`

```lean
theorem final_of_comp_full_faithful' [Full G] [Faithful G] [Final (F ⋙ G)] : Final G
```

Proof / construction:

```lean
:=
  have := final_of_comp_full_faithful F G
  final_of_final_comp F G
```

Candidates (8), random order:

1. `CategoryTheory.Functor.final_of_final_comp`

```lean
theorem final_of_final_comp [hF : Final F] [hFG : Final (F ⋙ G)] : Final G
```

2. `CategoryTheory.Functor.Full`

```lean
class Full (F : C ⥤ D) : Prop
```

3. `CategoryTheory.Functor.comp`

```lean
def comp (F : C ⥤ D) (G : D ⥤ E) : C ⥤ E
```

4. `CategoryTheory.Functor.Final`

```lean
class Final (F : C ⥤ D) : Prop
```

5. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

6. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

7. `CategoryTheory.Functor.final_of_comp_full_faithful`

```lean
theorem final_of_comp_full_faithful [Full G] [Faithful G] [Final (F ⋙ G)] : Final F
```

8. `CategoryTheory.Functor.Faithful`

```lean
class Faithful (F : C ⥤ D) : Prop
```


---

## t095

Target: `EsakiaHom.coe_copy`

```lean
theorem coe_copy (f : EsakiaHom α β) (f' : α → β) (h : f' = f) : ⇑(f.copy f' h) = f'
```

Proof / construction:

```lean
:= rfl
```

Candidates (8), random order:

1. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

2. `EsakiaHom.copy`

```lean
protected def copy (f : EsakiaHom α β) (f' : α → β) (h : f' = f) : EsakiaHom α β
```

3. `Eq`

```lean
inductive Eq : α → α → Prop
```

4. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

5. `EsakiaHom.instFunLike`

```lean
instance instFunLike : FunLike (EsakiaHom α β) α β
```

6. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

7. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

8. `EsakiaHom`

```lean
structure EsakiaHom (α β : Type*) [TopologicalSpace α] [Preorder α] [TopologicalSpace β]
  [Preorder β] extends α →Co β
```


---

## t096

Target: `BoundarylessManifold.isInteriorPoint`

```lean
lemma _root_.BoundarylessManifold.isInteriorPoint {x : M} [BoundarylessManifold I M] :
    IsInteriorPoint I x
```

Proof / construction:

```lean
:= BoundarylessManifold.isInteriorPoint' x
```

Candidates (10), random order:

1. `NormedAddCommGroup`

```lean
class NormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E, MetricSpace E
```

2. `BoundarylessManifold`

```lean
class _root_.BoundarylessManifold {𝕜 : Type*} [NontriviallyNormedField 𝕜]
    {E : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type*} [TopologicalSpace H] (I : ModelWithCorners 𝕜 E H)
    (M : Type*) [TopologicalSpace M] [ChartedSpace H M] : Prop
```

3. `ModelWithCorners`

```lean
structure ModelWithCorners (𝕜 : Type*) [NontriviallyNormedField 𝕜] (E : Type*)
    [NormedAddCommGroup E] [NormedSpace 𝕜 E] (H : Type*) [TopologicalSpace H] extends
    PartialEquiv H E
```

4. `NormedAddCommGroup.toSeminormedAddCommGroup`

```lean
NormedAddCommGroup.toSeminormedAddCommGroup
```

5. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

6. `NormedSpace`

```lean
class NormedSpace (𝕜 : Type*) (E : Type*) [NormedField 𝕜] [SeminormedAddCommGroup E]
    extends Module 𝕜 E
```

7. `NontriviallyNormedField`

```lean
class NontriviallyNormedField (α : Type*) extends NormedField α
```

8. `NontriviallyNormedField.toNormedField`

```lean
class NontriviallyNormedField (α : Type*) extends NormedField α
```

9. `ChartedSpace`

```lean
class ChartedSpace (H : Type*) [TopologicalSpace H] (M : Type*) [TopologicalSpace M]
```

10. `BoundarylessManifold.isInteriorPoint'`

```lean
isInteriorPoint' : ∀ x : M, IsInteriorPoint I x
```


---

## t097

Target: `AlgebraicTopology.alternatingFaceMapComplex_obj_X`

```lean
theorem alternatingFaceMapComplex_obj_X (X : SimplicialObject C) (n : ℕ) :
    ((alternatingFaceMapComplex C).obj X).X n = X _⦋n⦌
```

Proof / construction:

```lean
:=
  rfl
```

Candidates (24), random order:

1. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

2. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`

```lean
instance (priority := 100) preadditiveHasZeroMorphisms : HasZeroMorphisms C
```

3. `AddSemigroup.toAdd`

```lean
class AddSemigroup (G : Type u) extends Add G
```

4. `CategoryTheory.SimplicialObject`

```lean
abbrev SimplicialObject
```

5. `CategoryTheory.Category.opposite`

```lean
instance Category.opposite : Category.{v₁} Cᵒᵖ
```

6. `CategoryTheory.Functor.category`

```lean
instance Functor.category : Category.{max u₁ v₂} (C ⥤ D)
```

7. `CategoryTheory.Preadditive`

```lean
class Preadditive
```

8. `Nat.instOne`

```lean
instance instOne              : One ℕ
```

9. `AddCancelCommMonoid.toAddCancelMonoid`

```lean
AddCancelCommMonoid.toAddCancelMonoid
```

10. `CategoryTheory.Functor.obj`

```lean
obj : C → D
```

11. `SimplexCategory.smallCategory`

```lean
instance smallCategory : SmallCategory.{0} SimplexCategory
```

12. `SimplexCategory`

```lean
structure SimplexCategory : Type
```

13. `HomologicalComplex.X`

```lean
X : ι → V
```

14. `AlgebraicTopology.alternatingFaceMapComplex`

```lean
def alternatingFaceMapComplex : SimplicialObject C ⥤ ChainComplex C ℕ
```

15. `ChainComplex`

```lean
abbrev ChainComplex (α : Type*) [AddRightCancelSemigroup α] [One α] : Type _
```

16. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

17. `ComplexShape.down`

```lean
def up (α : Type*) [Add α] [IsRightCancelAdd α] [One α] : ComplexShape α
```

18. `Nat`

```lean
inductive Nat
```

19. `HomologicalComplex.instCategory`

```lean
instance : Category (HomologicalComplex V c)
```

20. `Nat.instAddCancelCommMonoid`

```lean
instance instAddCancelCommMonoid : AddCancelCommMonoid ℕ
```

21. `AddRightCancelMonoid.toAddRightCancelSemigroup`

```lean
class AddRightCancelMonoid (M : Type u) extends AddMonoid M, AddRightCancelSemigroup M
```

22. `AddRightCancelSemigroup.toAddSemigroup`

```lean
class AddRightCancelSemigroup (G : Type u) extends AddSemigroup G, IsRightCancelAdd G
```

23. `Opposite`

```lean
structure Opposite
```

24. `AddCancelMonoid.toAddRightCancelMonoid`

```lean
class AddCancelMonoid (M : Type u) extends AddLeftCancelMonoid M, AddRightCancelMonoid M
```


---

## t098

Target: `IsCompact.of_isClosed_subset`

```lean
theorem IsCompact.of_isClosed_subset (hs : IsCompact s) (ht : IsClosed t) (h : t ⊆ s) :
    IsCompact t
```

Proof / construction:

```lean
:=
  inter_eq_self_of_subset_right h ▸ hs.inter_right ht
```

Candidates (12), random order:

1. `Set.instLE`

```lean
instance : LE (Set α)
```

2. `IsClosed`

```lean
class IsClosed (s : Set X) : Prop
```

3. `Eq`

```lean
inductive Eq : α → α → Prop
```

4. `Set.inter_eq_self_of_subset_right`

```lean
theorem inter_eq_self_of_subset_right {s t : Set α} : t ⊆ s → s ∩ t = t
```

5. `Eq.rec`

```lean
Eq.rec
```

6. `Inter.inter`

```lean
inter : α → α → α
```

7. `Set`

```lean
def Set (α : Type u)
```

8. `IsCompact`

```lean
def IsCompact (s : Set X)
```

9. `LE.le`

```lean
le : α → α → Prop
```

10. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

11. `IsCompact.inter_right`

```lean
theorem IsCompact.inter_right (hs : IsCompact s) (ht : IsClosed t) : IsCompact (s ∩ t)
```

12. `Set.instInter`

```lean
instance : Inter (Set α)
```


---

## t099

Target: `LightCondSet.LocallyConstant.instFaithfulLightCondensedTypeDiscrete`

```lean
noncomputable instance : functor.Faithful
```

Proof / construction:

```lean
:= functorFullyFaithful.faithful
```

Candidates (21), random order:

1. `CategoryTheory.coherentTopology`

```lean
def coherentTopology [Precoherent C] : GrothendieckTopology C
```

2. `LightCondSet.LocallyConstant.functor`

```lean
abbrev functor : Type u ⥤ LightCondSet.{u}
```

3. `LightCondSet.LocallyConstant.iso`

```lean
noncomputable def iso : functor ≅ LightCondensed.discrete (Type u)
```

4. `SecondCountableTopology`

```lean
class _root_.SecondCountableTopology : Prop
```

5. `And`

```lean
structure And (a b : Prop) : Prop
```

6. `TotallyDisconnectedSpace`

```lean
class TotallyDisconnectedSpace (α : Type u) [TopologicalSpace α] : Prop
```

7. `CompHausLike.category`

```lean
instance category : Category (CompHausLike P)
```

8. `CategoryTheory.Category.opposite`

```lean
instance Category.opposite : Category.{v₁} Cᵒᵖ
```

9. `TopCat.str`

```lean
TopCat.str
```

10. `TopCat`

```lean
structure TopCat
```

11. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

12. `LightProfinite`

```lean
abbrev LightProfinite
```

13. `CategoryTheory.ObjectProperty.FullSubcategory.category`

```lean
instance FullSubcategory.category : Category.{v} P.FullSubcategory
```

14. `TopCat.carrier`

```lean
carrier : Type u
```

15. `CategoryTheory.Functor.Faithful.of_iso`

```lean
theorem Faithful.of_iso [F.Faithful] (α : F ≅ F') : F'.Faithful
```

16. `CategoryTheory.Presheaf.IsSheaf`

```lean
def IsSheaf (P : Cᵒᵖ ⥤ A) : Prop
```

17. `LightCondensed.discrete`

```lean
noncomputable def discrete : C ⥤ LightCondensed.{u} C
```

18. `Opposite`

```lean
structure Opposite
```

19. `CategoryTheory.Functor.category`

```lean
instance Functor.category : Category.{max u₁ v₂} (C ⥤ D)
```

20. `CategoryTheory.types`

```lean
instance CategoryTheory.types : Category.{u} (Type u)
```

21. `LightCondensed`

```lean
abbrev LightCondensed (C : Type w) [Category.{v} C]
```


---

## t100

Target: `MeasureTheory.MeasurePreserving.restrict_preimage_emb`

```lean
theorem restrict_preimage_emb {f : α → β} (hf : MeasurePreserving f μa μb)
    (h₂ : MeasurableEmbedding f) (s : Set β) :
    MeasurePreserving f (μa.restrict (f ⁻¹' s)) (μb.restrict s)
```

Proof / construction:

```lean
:=
  ⟨hf.measurable, by rw [← hf.map_eq, h₂.restrict_map]⟩
```

Candidates (18), random order:

1. `MeasureTheory.MeasurePreserving.measurable`

```lean
protected measurable : Measurable f
```

2. `MeasurableEmbedding.restrict_map`

```lean
theorem restrict_map (μ : Measure α) (s : Set β) :
    (μ.map f).restrict s = (μ.restrict <| f ⁻¹' s).map f
```

3. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

4. `MeasurableSpace`

```lean
@[class] structure MeasurableSpace (α : Type*)
```

5. `MeasureTheory.Measure.restrict`

```lean
noncomputable def restrict {_m0 : MeasurableSpace α} (μ : Measure α) (s : Set α) : Measure α
```

6. `Eq.refl`

```lean
| refl (a : α) : Eq a a
```

7. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

8. `MeasureTheory.Measure.map`

```lean
MeasureTheory.Measure.map
```

9. `Set.preimage`

```lean
def preimage (f : α → β) (s : Set β) : Set α
```

10. `MeasureTheory.MeasurePreserving.map_eq`

```lean
protected map_eq : map f μa = μb
```

11. `Eq`

```lean
inductive Eq : α → α → Prop
```

12. `Set`

```lean
def Set (α : Type u)
```

13. `MeasureTheory.MeasurePreserving`

```lean
structure MeasurePreserving (f : α → β)
  (μa : Measure α := by volume_tac) (μb : Measure β := by volume_tac) : Prop
```

14. `MeasureTheory.Measure`

```lean
structure Measure (α : Type*) [MeasurableSpace α] extends OuterMeasure α
```

15. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```

16. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

17. `MeasurableEmbedding`

```lean
structure MeasurableEmbedding [MeasurableSpace α] [MeasurableSpace β] (f : α → β) : Prop
```

18. `MeasureTheory.MeasurePreserving.mk`

```lean
structure MeasurePreserving (f : α → β)
  (μa : Measure α := by volume_tac) (μb : Measure β := by volume_tac) : Prop
```


---
