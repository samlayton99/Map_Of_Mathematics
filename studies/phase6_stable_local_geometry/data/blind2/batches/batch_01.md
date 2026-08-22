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

Target: `HomotopicalAlgebra.PrepathObject.p`

```lean
noncomputable def p : P.P ⟶ A ⨯ A
```

Proof / construction:

```lean
:= prod.lift P.p₀ P.p₁
```

Candidates (7), random order:

1. `HomotopicalAlgebra.PrepathObject.P`

```lean
P : C
```

2. `CategoryTheory.Limits.HasBinaryProduct`

```lean
abbrev HasBinaryProduct (X Y : C)
```

3. `HomotopicalAlgebra.PrepathObject`

```lean
structure PrepathObject (A : C)
```

4. `HomotopicalAlgebra.PrepathObject.p₁`

```lean
p₁ : P ⟶ A
```

5. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

6. `HomotopicalAlgebra.PrepathObject.p₀`

```lean
p₀ : P ⟶ A
```

7. `CategoryTheory.Limits.prod.lift`

```lean
noncomputable abbrev prod.lift {W X Y : C} [HasBinaryProduct X Y]
    (f : W ⟶ X) (g : W ⟶ Y) : W ⟶ X ⨯ Y
```


---

## t002

Target: `CategoryTheory.Bicategory.RightLift.IsKan.whiskerOfCommute`

```lean
def whiskerOfCommute (s t : RightLift f g) (i : s ≅ t) {x : B} (h : x ⟶ c)
    (P : IsKan (s.whisker h)) :
    IsKan (t.whisker h)
```

Proof / construction:

```lean
:=
  P.ofIsoKan <| whiskerIso i h
```

Candidates (14), random order:

1. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

2. `CategoryTheory.Bicategory.RightLift.IsKan.ofIsoKan`

```lean
def ofIsoKan (P : IsKan s) (i : s ≅ t) : IsKan t
```

3. `CategoryTheory.Bicategory.homCategory`

```lean
homCategory : ∀ a b : B, Category.{w} (a ⟶ b)
```

4. `CategoryTheory.Bicategory`

```lean
class Bicategory (B : Type u) extends CategoryStruct.{v} B
```

5. `CategoryTheory.Bicategory.postcomp`

```lean
def postcomp (a : B) (f : b ⟶ c) : (a ⟶ b) ⥤ (a ⟶ c)
```

6. `CategoryTheory.Bicategory.toCategoryStruct`

```lean
class Bicategory (B : Type u) extends CategoryStruct.{v} B
```

7. `CategoryTheory.instCategoryCostructuredArrow_1`

```lean
CategoryTheory.instCategoryCostructuredArrow_1
```

8. `CategoryTheory.Bicategory.RightLift`

```lean
abbrev RightLift (f : b ⟶ a) (g : c ⟶ a)
```

9. `CategoryTheory.Bicategory.RightLift.whiskerIso`

```lean
def whiskerIso (i : s ≅ t) {x : B} (h : x ⟶ c) :
    s.whisker h ≅ t.whisker h
```

10. `CategoryTheory.Bicategory.RightLift.whisker`

```lean
def whisker (t : RightLift f g) {x : B} (h : x ⟶ c) : RightLift f (h ≫ g)
```

11. `CategoryTheory.Iso`

```lean
structure Iso {C : Type u} [Category.{v} C] (X Y : C)
```

12. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

13. `CategoryTheory.CategoryStruct.comp`

```lean
comp : ∀ {X Y Z : obj}, (X ⟶ Y) → (Y ⟶ Z) → (X ⟶ Z)
```

14. `CategoryTheory.Bicategory.RightLift.IsKan`

```lean
abbrev IsKan (t : RightLift f g)
```


---

## t003

Target: `Computation.length`

```lean
def length : ℕ
```

Proof / construction:

```lean
:=
  Nat.find ((terminates_def _).1 h)
```

Candidates (18), random order:

1. `OfNat.ofNat`

```lean
ofNat : α
```

2. `Bool`

```lean
inductive Bool : Type
```

3. `instDecidableEqBool`

```lean
instDecidableEqBool
```

4. `HAdd.hAdd`

```lean
hAdd : α → β → γ
```

5. `Nat`

```lean
inductive Nat
```

6. `Option.some`

```lean
| some (val : α) : Option α
```

7. `Subtype.val`

```lean
val : α
```

8. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

9. `Bool.true`

```lean
| true : Bool
```

10. `instAddNat`

```lean
instance instAddNat : Add Nat
```

11. `Stream'`

```lean
def Stream' (α : Type u)
```

12. `Nat.find`

```lean
protected def find : ℕ
```

13. `Eq`

```lean
inductive Eq : α → α → Prop
```

14. `Computation.Terminates`

```lean
class Terminates (s : Computation α) : Prop
```

15. `Option`

```lean
inductive Option (α : Type u)
```

16. `Computation`

```lean
def Computation (α : Type u) : Type u
```

17. `instHAdd`

```lean
instance instHAdd [Add α] : HAdd α α α
```

18. `Option.isSome`

```lean
@[inline, implicit_reducible] def isSome : Option α → Bool
  | some _ => true
  | none   => false
```


---

## t004

Target: `Nat.instUniqueSubtypeMemFinsetIicOfNat`

```lean
instance : Unique (Iic 0)
```

Proof / construction:

```lean
:= by
  rw [← Nat.bot_eq_zero]
  infer_instance
```

Candidates (21), random order:

1. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

2. `Nat.instLocallyFiniteOrder`

```lean
instance instLocallyFiniteOrder : LocallyFiniteOrder ℕ
```

3. `Finset.instSetLike`

```lean
instance : SetLike (Finset α) α
```

4. `LocallyFiniteOrder.toLocallyFiniteOrderBot`

```lean
LocallyFiniteOrder.toLocallyFiniteOrderBot
```

5. `Membership.mem`

```lean
mem : γ → α → Prop
```

6. `Nat.instPreorder`

```lean
instance : Preorder ℕ
```

7. `Nat.instPartialOrder`

```lean
instance : PartialOrder ℕ
```

8. `Nat`

```lean
inductive Nat
```

9. `OfNat.ofNat`

```lean
ofNat : α
```

10. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

11. `Finset.instUniqueSubtypeMemIicBot`

```lean
instance [OrderBot α] : Unique (Iic (⊥ : α))
```

12. `Finset.Iic`

```lean
Finset.Iic
```

13. `OrderBot.toBot`

```lean
@[to_dual] class OrderBot (α : Type u) [LE α] extends Bot α
```

14. `Bot.bot`

```lean
bot : α
```

15. `Nat.instOrderBot`

```lean
instance instOrderBot : OrderBot ℕ
```

16. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

17. `Finset`

```lean
structure Finset (α : Type*)
```

18. `inferInstance`

```lean
abbrev inferInstance {α : Sort u} [i : α] : α
```

19. `Unique`

```lean
structure Unique (α : Sort u) extends Inhabited α
```

20. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

21. `instLENat`

```lean
instance instLENat : LE Nat
```


---

## t005

Target: `Circle.centeredArc`

```lean
noncomputable def centeredArc (r : ℝ) : Set Circle
```

Proof / construction:

```lean
:=
  exp '' {x | |x| < r}
```

Candidates (17), random order:

1. `Circle`

```lean
def Circle : Type
```

2. `Real.instAddGroup`

```lean
Real.instAddGroup
```

3. `instTopologicalSpaceCircle`

```lean
instTopologicalSpaceCircle
```

4. `abs`

```lean
abs
```

5. `Set.image`

```lean
def image {β : Type v} (f : α → β) (s : Set α) : Set β
```

6. `Real.lattice`

```lean
instance lattice : Lattice ℝ
```

7. `PseudoMetricSpace.toUniformSpace`

```lean
toUniformSpace : UniformSpace α
```

8. `Circle.exp`

```lean
def exp : C(ℝ, Circle)
```

9. `ContinuousMap.instFunLike`

```lean
instance instFunLike : FunLike C(X, Y) X Y
```

10. `UniformSpace.toTopologicalSpace`

```lean
class UniformSpace (α : Type u) extends TopologicalSpace α
```

11. `Real.pseudoMetricSpace`

```lean
instance Real.pseudoMetricSpace : PseudoMetricSpace ℝ
```

12. `Real`

```lean
structure Real
```

13. `Real.instLT`

```lean
instance : LT ℝ
```

14. `ContinuousMap`

```lean
structure ContinuousMap (X Y : Type*) [TopologicalSpace X] [TopologicalSpace Y]
```

15. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

16. `LT.lt`

```lean
lt : α → α → Prop
```

17. `Set.ofPred`

```lean
def Set.ofPred {α : Type u} (p : α → Prop) : Set α
```


---

## t006

Target: `Complex.instOne`

```lean
instance : One ℂ
```

Proof / construction:

```lean
:=
  ⟨(1 : ℝ)⟩
```

Candidates (7), random order:

1. `Real.instOne`

```lean
instance : One ℝ
```

2. `Complex`

```lean
structure Complex : Type
```

3. `One.toOfNat1`

```lean
instance (priority := 300) One.toOfNat1 {α} [One α] : OfNat α (nat_lit 1)
```

4. `Complex.ofReal`

```lean
def ofReal (r : ℝ) : ℂ
```

5. `Real`

```lean
structure Real
```

6. `OfNat.ofNat`

```lean
ofNat : α
```

7. `One.mk`

```lean
class One (α : Type u)
```


---

## t007

Target: `CategoryTheory.MonoOver.pullbackSelf`

```lean
def pullbackSelf {A B : C} (f : A ⟶ B) [Mono f] : (pullback f).obj (mk f) ≅ ⊤
```

Proof / construction:

```lean
:=
  iso_of_both_ways (leTop _) (topLEPullbackSelf _)
```

Candidates (19), random order:

1. `CategoryTheory.Limits.HasPullbacks`

```lean
abbrev HasPullbacks
```

2. `CategoryTheory.MonoOver.instTop`

```lean
instance {X : C} : Top (MonoOver X)
```

3. `CategoryTheory.Mono`

```lean
class Mono (f : X ⟶ Y) : Prop
```

4. `CategoryTheory.MonoOver`

```lean
abbrev MonoOver (X : C)
```

5. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

6. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

7. `CategoryTheory.iso_of_both_ways`

```lean
def iso_of_both_ways {X Y : C} (f : X ⟶ Y) (g : Y ⟶ X) :
    X ≅ Y
```

8. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

9. `CategoryTheory.Over`

```lean
def Over (X : T)
```

10. `Top.top`

```lean
top : α
```

11. `CategoryTheory.Over.isMono`

```lean
abbrev Over.isMono (X : C) : ObjectProperty (Over X)
```

12. `CategoryTheory.MonoOver.leTop`

```lean
def leTop (f : MonoOver X) : f ⟶ ⊤
```

13. `CategoryTheory.MonoOver.pullback`

```lean
def pullback (f : X ⟶ Y) : MonoOver Y ⥤ MonoOver X
```

14. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

15. `CategoryTheory.ObjectProperty.FullSubcategory.category`

```lean
instance FullSubcategory.category : Category.{v} P.FullSubcategory
```

16. `CategoryTheory.MonoOver.mk`

```lean
def mk {X A : C} (f : A ⟶ X) [hf : Mono f] : MonoOver X
```

17. `CategoryTheory.MonoOver.topLEPullbackSelf`

```lean
def topLEPullbackSelf {A B : C} (f : A ⟶ B) [Mono f] :
    (⊤ : MonoOver A) ⟶ (pullback f).obj (mk f)
```

18. `CategoryTheory.Functor.obj`

```lean
obj : C → D
```

19. `CategoryTheory.instCategoryOver`

```lean
CategoryTheory.instCategoryOver
```


---

## t008

Target: `HomologicalComplex.truncGE'.XIso`

```lean
noncomputable def XIso {i : ι} (hi : ¬ e.BoundaryGE i) :
    X K e i ≅ K.X (e.f i)
```

Proof / construction:

```lean
:=
  eqToIso (if_neg hi)
```

Candidates (12), random order:

1. `HomologicalComplex.X`

```lean
X : ι → V
```

2. `CategoryTheory.Limits.HasZeroMorphisms`

```lean
class HasZeroMorphisms
```

3. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

4. `CategoryTheory.eqToIso`

```lean
def eqToIso {X Y : C} (p : X = Y) : X ≅ Y
```

5. `ComplexShape`

```lean
structure ComplexShape (ι : Type*)
```

6. `HomologicalComplex.HasHomology`

```lean
abbrev HasHomology
```

7. `ComplexShape.Embedding.BoundaryGE`

```lean
def BoundaryGE (j : ι) : Prop
```

8. `ComplexShape.Embedding.f`

```lean
f : ι → ι'
```

9. `Not`

```lean
@[implicit_reducible] def Not (a : Prop) : Prop
```

10. `HomologicalComplex`

```lean
structure HomologicalComplex (c : ComplexShape ι)
```

11. `HomologicalComplex.truncGE'.X`

```lean
noncomputable def X (i : ι) : C
```

12. `ComplexShape.Embedding`

```lean
structure Embedding
```


---

## t009

Target: `Subgroup.transferFocal`

```lean
noncomputable def transferFocal [H.FiniteIndex] : G →* H ⧸ focalSubgroupOf H
```

Proof / construction:

```lean
:=
  MonoidHom.transfer (QuotientGroup.mk' (focalSubgroupOf H))
```

Candidates (15), random order:

1. `HasQuotient.Quotient`

```lean
HasQuotient.Quotient
```

2. `Subgroup.instSetLike`

```lean
instance : SetLike (Subgroup G) G
```

3. `QuotientGroup.Quotient.group`

```lean
instance Quotient.group : Group (G ⧸ N)
```

4. `Subgroup.toGroup`

```lean
instance toGroup {G : Type*} [Group G] (H : Subgroup G) : Group H
```

5. `Membership.mem`

```lean
mem : γ → α → Prop
```

6. `Subgroup.focalSubgroupOf`

```lean
def focalSubgroupOf : Subgroup H
```

7. `IsMulCommutative.instCommGroup`

```lean
IsMulCommutative.instCommGroup
```

8. `Subgroup`

```lean
structure Subgroup (G : Type*) [Group G] extends Submonoid G
```

9. `QuotientGroup.mk'`

```lean
def mk' : G →* G ⧸ N
```

10. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

11. `QuotientGroup.instHasQuotientSubgroup`

```lean
instance instHasQuotientSubgroup : HasQuotient α (Subgroup α)
```

12. `Subgroup.FiniteIndex`

```lean
@[to_additive] class FiniteIndex : Prop
```

13. `Group`

```lean
class Group (G : Type u) extends DivInvMonoid G
```

14. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

15. `MonoidHom.transfer`

```lean
def transfer [FiniteIndex H] : G →* A
```


---

## t010

Target: `CategoryTheory.Cat.FreeRefl.instCategory`

```lean
instance : Category (FreeRefl V)
```

Proof / construction:

```lean
:=
  inferInstanceAs (Category (Quotient _))
```

Candidates (3), random order:

1. `CategoryTheory.ReflQuiver`

```lean
class ReflQuiver (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

2. `CategoryTheory.Category.mk`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

3. `CategoryTheory.Cat.FreeRefl`

```lean
def FreeRefl
```


---
