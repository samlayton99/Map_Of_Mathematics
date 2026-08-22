# Blind grading batch 05 — 10 items

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

Target: `Set.ordConnected_range`

```lean
theorem ordConnected_range {E : Type*} [EquivLike E α β] [OrderIsoClass E α β] (e : E) :
    OrdConnected (range e)
```

Proof / construction:

```lean
:= by
  simp_rw [← image_univ]
  exact ordConnected_image (e : α ≃o β)
```

Candidates (19), random order:

1. `OrderIsoClass.toOrderIso`

```lean
def OrderIsoClass.toOrderIso [LE α] [LE β] [EquivLike F α β] [OrderIsoClass F α β] (f : F) :
    α ≃o β
```

2. `Set`

```lean
def Set (α : Type u)
```

3. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

4. `Set.OrdConnected`

```lean
class OrdConnected (s : Set α) : Prop
```

5. `Set.ordConnected_image`

```lean
theorem ordConnected_image {E : Type*} [EquivLike E α β] [OrderIsoClass E α β] (e : E) {s : Set α}
    [hs : OrdConnected s] : OrdConnected (e '' s)
```

6. `OrderIso.instEquivLike`

```lean
instance : EquivLike (α ≃o β) α β
```

7. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

8. `Set.image`

```lean
def image {β : Type v} (f : α → β) (s : Set α) : Set β
```

9. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

10. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

11. `Set.univ`

```lean
def univ : Set α
```

12. `EquivLike.toFunLike`

```lean
instance (priority := 100) toFunLike : FunLike E α β
```

13. `OrderIsoClass`

```lean
class OrderIsoClass (F : Type*) (α β : outParam Type*) [LE α] [LE β] [EquivLike F α β] :
    Prop
```

14. `OrderIso`

```lean
abbrev OrderIso (α β : Type*) [LE α] [LE β]
```

15. `EquivLike`

```lean
class EquivLike (E : Sort*) (α β : outParam (Sort*))
```

16. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

17. `Eq`

```lean
inductive Eq : α → α → Prop
```

18. `Set.range`

```lean
def range (f : ι → α) : Set α
```

19. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```


---

## t042

Target: `CategoryTheory.Limits.preservesColimit_iff_isColimit_mapCocone`

```lean
lemma preservesColimit_iff_isColimit_mapCocone {F : C ⥤ D} {t : Cocone K} (h : IsColimit t) :
    PreservesColimit K F ↔ Nonempty (IsColimit (F.mapCocone t))
```

Proof / construction:

```lean
:=
  ⟨fun _ ↦ ⟨isColimitOfPreserves _ h⟩,
    fun h' ↦ preservesColimit_of_preserves_colimit_cocone h h'.some⟩
```

Candidates (13), random order:

1. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

2. `Nonempty`

```lean
class inductive Nonempty (α : Sort u) : Prop
```

3. `CategoryTheory.Functor.mapCocone`

```lean
CategoryTheory.Functor.mapCocone
```

4. `CategoryTheory.Limits.PreservesColimit`

```lean
class PreservesColimit (K : J ⥤ C) (F : C ⥤ D) : Prop
```

5. `CategoryTheory.Limits.isColimitOfPreserves`

```lean
def isColimitOfPreserves (F : C ⥤ D) {c : Cocone K} (t : IsColimit c) [PreservesColimit K F] :
    IsColimit (F.mapCocone c)
```

6. `Nonempty.some`

```lean
protected noncomputable abbrev Nonempty.some {α} (h : Nonempty α) : α
```

7. `CategoryTheory.Functor.comp`

```lean
def comp (F : C ⥤ D) (G : D ⥤ E) : C ⥤ E
```

8. `Iff.intro`

```lean
structure Iff (a b : Prop) : Prop
```

9. `Nonempty.intro`

```lean
| intro (val : α) : Nonempty α
```

10. `CategoryTheory.Limits.IsColimit`

```lean
structure IsColimit (t : Cocone F)
```

11. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

12. `CategoryTheory.Limits.Cocone`

```lean
structure Cocone (F : J ⥤ C)
```

13. `CategoryTheory.Limits.preservesColimit_of_preserves_colimit_cocone`

```lean
lemma preservesColimit_of_preserves_colimit_cocone {F : C ⥤ D} {t : Cocone K} (h : IsColimit t)
    (hF : IsColimit (F.mapCocone t)) : PreservesColimit K F
```


---

## t043

Target: `NNReal.continuousOn_rpow_const_compl_zero`

```lean
theorem continuousOn_rpow_const_compl_zero {r : ℝ} :
    ContinuousOn (fun z : ℝ≥0 => z ^ r) {0}ᶜ
```

Proof / construction:

```lean
:=
  fun _ h => ContinuousAt.continuousWithinAt <| NNReal.continuousAt_rpow_const (.inl h)
```

Candidates (23), random order:

1. `Membership.mem`

```lean
mem : γ → α → Prop
```

2. `Set`

```lean
def Set (α : Type u)
```

3. `Real.instZero`

```lean
instance : Zero ℝ
```

4. `NNReal.instTopologicalSpace`

```lean
instance : TopologicalSpace ℝ≥0
```

5. `Or.inl`

```lean
| inl (h : a) : Or a b
```

6. `Singleton.singleton`

```lean
singleton : α → β
```

7. `ContinuousAt.continuousWithinAt`

```lean
theorem ContinuousAt.continuousWithinAt (h : ContinuousAt f x) :
    ContinuousWithinAt f s x
```

8. `Set.instSingletonSet`

```lean
instance instSingletonSet : Singleton α (Set α)
```

9. `NNReal.instPowReal`

```lean
noncomputable instance : Pow ℝ≥0 ℝ
```

10. `OfNat.ofNat`

```lean
ofNat : α
```

11. `Real.instLE`

```lean
instance : LE ℝ
```

12. `instHPow`

```lean
instance instHPow [Pow α β] : HPow α β α
```

13. `LE.le`

```lean
le : α → α → Prop
```

14. `Real`

```lean
structure Real
```

15. `Compl.compl`

```lean
compl : α → α
```

16. `NNReal.instZero`

```lean
instance : Zero ℝ≥0
```

17. `Set.instMembership`

```lean
instance : Membership α (Set α)
```

18. `NNReal.continuousAt_rpow_const`

```lean
theorem continuousAt_rpow_const {x : ℝ≥0} {y : ℝ} (h : x ≠ 0 ∨ 0 ≤ y) :
    ContinuousAt (fun z => z ^ y) x
```

19. `HPow.hPow`

```lean
hPow : α → β → γ
```

20. `Zero.toOfNat0`

```lean
instance (priority := 300) Zero.toOfNat0 {α} [Zero α] : OfNat α (nat_lit 0)
```

21. `NNReal`

```lean
def NNReal
```

22. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

23. `Set.instCompl`

```lean
instance : Compl (Set α)
```


---

## t044

Target: `LocallyConstant.congrRightₐ`

```lean
def congrRightₐ (R : Type*) [CommSemiring R] [Semiring Y] [Algebra R Y] [Semiring Z] [Algebra R Z]
    (e : Y ≃ₐ[R] Z) : LocallyConstant X Y ≃ₐ[R] LocallyConstant X Z
```

Proof / construction:

```lean
where
  toEquiv := congrRight e
  __ := mapₐ R e.toAlgHom
```

Candidates (16), random order:

1. `LocallyConstant`

```lean
structure LocallyConstant (X Y : Type*) [TopologicalSpace X]
```

2. `LocallyConstant.instSemiring`

```lean
instance [Semiring Y] : Semiring (LocallyConstant X Y)
```

3. `AlgEquiv.instEquivLike`

```lean
instance : EquivLike (A₁ ≃ₐ[R] A₂) A₁ A₂
```

4. `Equiv`

```lean
structure Equiv (α β : Sort*)
```

5. `Algebra`

```lean
class Algebra (R : Type u) (A : Type v) [CommSemiring R] [Semiring A] extends SMul R A
```

6. `AlgEquiv`

```lean
structure AlgEquiv (R : Type u) (A : Type v) (B : Type w) [CommSemiring R] [Semiring A] [Semiring B]
  [Algebra R A] [Algebra R B] extends A ≃ B, A ≃* B, A ≃+ B, A ≃+* B
```

7. `LocallyConstant.instAlgebra`

```lean
instance : Algebra R (LocallyConstant X Y)
```

8. `AlgEquiv.toAlgHom`

```lean
def toAlgHom : A₁ →ₐ[R] A₂
```

9. `EquivLike.toEquiv`

```lean
def EquivLike.toEquiv {F} [EquivLike F α β] (f : F) : α ≃ β
```

10. `LocallyConstant.congrRight`

```lean
def congrRight (e : Y ≃ Z) : LocallyConstant X Y ≃ LocallyConstant X Z
```

11. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

12. `CommSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

13. `AlgEquiv.mk`

```lean
structure AlgEquiv (R : Type u) (A : Type v) (B : Type w) [CommSemiring R] [Semiring A] [Semiring B]
  [Algebra R A] [Algebra R B] extends A ≃ B, A ≃* B, A ≃+ B, A ≃+* B
```

14. `AlgHom`

```lean
structure AlgHom (R : Type u) (A : Type v) (B : Type w) [CommSemiring R] [Semiring A] [Semiring B]
  [Algebra R A] [Algebra R B] extends RingHom A B
```

15. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

16. `LocallyConstant.mapₐ`

```lean
def mapₐ (R : Type*) [CommSemiring R] [Semiring Y] [Algebra R Y] [Semiring Z] [Algebra R Z]
    (f : Y →ₐ[R] Z) : LocallyConstant X Y →ₐ[R] LocallyConstant X Z
```


---

## t045

Target: `OrderType.instOrderBot`

```lean
instance : OrderBot OrderType
```

Proof / construction:

```lean
where
  bot := 0
  bot_le := OrderType.zero_le
```

Candidates (8), random order:

1. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

2. `OfNat.ofNat`

```lean
ofNat : α
```

3. `Zero.toOfNat0`

```lean
instance (priority := 300) Zero.toOfNat0 {α} [Zero α] : OfNat α (nat_lit 0)
```

4. `OrderType.instPreorder`

```lean
instance : Preorder OrderType
```

5. `OrderBot.mk`

```lean
@[to_dual] class OrderBot (α : Type u) [LE α] extends Bot α
```

6. `OrderType.zero_le`

```lean
protected theorem zero_le (o : OrderType) : 0 ≤ o
```

7. `OrderType.instZero`

```lean
instance : Zero OrderType
```

8. `OrderType`

```lean
def OrderType : Type (u + 1)
```


---

## t046

Target: `ContinuousMap.congr_arg`

```lean
protected theorem congr_arg (f : C(X, Y)) {x y : X} (h : x = y) : f x = f y
```

Proof / construction:

```lean
:=
  h ▸ rfl
```

Candidates (7), random order:

1. `ContinuousMap`

```lean
structure ContinuousMap (X Y : Type*) [TopologicalSpace X] [TopologicalSpace Y]
```

2. `ContinuousMap.instFunLike`

```lean
instance instFunLike : FunLike C(X, Y) X Y
```

3. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

4. `Eq.rec`

```lean
Eq.rec
```

5. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

6. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

7. `Eq`

```lean
inductive Eq : α → α → Prop
```


---

## t047

Target: `LTSeries.head_le`

```lean
lemma head_le (x : LTSeries α) (n : Fin (x.length + 1)) : x.head ≤ x n
```

Proof / construction:

```lean
:=
  x.monotone (Fin.zero_le n)
```

Candidates (18), random order:

1. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

2. `Nat`

```lean
inductive Nat
```

3. `HAdd.hAdd`

```lean
hAdd : α → β → γ
```

4. `LT.lt`

```lean
lt : α → α → Prop
```

5. `instHAdd`

```lean
instance instHAdd [Add α] : HAdd α α α
```

6. `OfNat.ofNat`

```lean
ofNat : α
```

7. `LTSeries`

```lean
abbrev LTSeries
```

8. `Fin`

```lean
structure Fin (n : Nat)
```

9. `RelSeries.length`

```lean
length : ℕ
```

10. `Preorder.toLT`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

11. `Set.ofPred`

```lean
def Set.ofPred {α : Type u} (p : α → Prop) : Set α
```

12. `Fin.instOfNat`

```lean
instance instOfNat {n : Nat} [NeZero n] {i : Nat} : OfNat (Fin n) i
```

13. `FiniteDimensionalOrder`

```lean
abbrev FiniteDimensionalOrder (γ : Type*) [Preorder γ]
```

14. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

15. `instAddNat`

```lean
instance instAddNat : Add Nat
```

16. `Fin.zero_le`

```lean
@[simp] theorem zero_le [NeZero n] (a : Fin n) : 0 ≤ a
```

17. `Prod`

```lean
structure Prod (α : Type u) (β : Type v)
```

18. `LTSeries.monotone`

```lean
lemma monotone (x : LTSeries α) : Monotone x
```


---

## t048

Target: `QuadraticAlgebra.im_intCast`

```lean
theorem im_intCast (n : ℤ) : (n : QuadraticAlgebra R a b).im = 0
```

Proof / construction:

```lean
:= rfl
```

Candidates (9), random order:

1. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

2. `QuadraticAlgebra`

```lean
structure QuadraticAlgebra (R : Type u) (a b : R) : Type u
```

3. `AddCommGroupWithOne.toAddGroupWithOne`

```lean
class AddCommGroupWithOne (R : Type u)
  extends AddCommGroup R, AddGroupWithOne R, AddCommMonoidWithOne R
```

4. `Int.cast`

```lean
protected def Int.cast {R : Type u} [IntCast R] : Int → R
```

5. `AddGroupWithOne.toIntCast`

```lean
class AddGroupWithOne (R : Type u) extends IntCast R, AddMonoidWithOne R, AddGroup R
```

6. `AddCommGroupWithOne`

```lean
class AddCommGroupWithOne (R : Type u)
  extends AddCommGroup R, AddGroupWithOne R, AddCommMonoidWithOne R
```

7. `Int`

```lean
inductive Int : Type
```

8. `QuadraticAlgebra.im`

```lean
im : R
```

9. `QuadraticAlgebra.instAddCommGroupWithOne`

```lean
QuadraticAlgebra.instAddCommGroupWithOne
```


---

## t049

Target: `WithTop.subtypeOrderIso`

```lean
def subtypeOrderIso [PartialOrder α] [OrderTop α] [DecidablePred (· = (⊤ : α))] :
    WithTop {a : α // a ≠ ⊤} ≃o α
```

Proof / construction:

```lean
where
  toFun a := (a.map (↑)).untopD ⊤
  invFun a := if h : a = ⊤ then ⊤ else .some ⟨a, h⟩
  left_inv
  | .some ⟨a, h⟩ => by simp [h]
  | ⊤ => by simp
  right_inv a := by dsimp only; split_ifs <;> simp [*]
  map_rel_iff' {a b} := match a, b with
  | .some a, .some b => by simp
  | ⊤, .some ⟨b, h⟩ => by simp [h]
  | a, ⊤ => by simp
```

Candidates (24), random order:

1. `Subtype.val`

```lean
val : α
```

2. `WithTop`

```lean
WithTop
```

3. `DecidablePred`

```lean
abbrev DecidablePred {α : Sort u} (r : α → Prop)
```

4. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

5. `OrderTop.toTop`

```lean
class OrderTop (α : Type u) [LE α] extends Top α
```

6. `Top.top`

```lean
top : α
```

7. `Equiv.mk`

```lean
structure Equiv (α β : Sort*)
```

8. `RelIso.mk`

```lean
structure RelIso {α β : Type*} (r : α → α → Prop) (s : β → β → Prop) extends α ≃ β
```

9. `WithTop.top`

```lean
WithTop.top
```

10. `WithTop.instPreorder`

```lean
instance [Preorder α] : Preorder (WithBot α)
```

11. `Subtype.preorder`

```lean
instance preorder [Preorder α] (p : α → Prop) : Preorder (Subtype p)
```

12. `Not`

```lean
@[implicit_reducible] def Not (a : Prop) : Prop
```

13. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

14. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

15. `Subtype.mk`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

16. `dite`

```lean
def dite {α : Sort u} (c : Prop) [h : Decidable c] (t : c → α) (e : Not c → α) : α
```

17. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

18. `PartialOrder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

19. `WithTop.untopD`

```lean
WithTop.untopD
```

20. `WithTop.map`

```lean
def map (f : α → β) : WithBot α → WithBot β
```

21. `Eq`

```lean
inductive Eq : α → α → Prop
```

22. `OrderTop`

```lean
class OrderTop (α : Type u) [LE α] extends Top α
```

23. `WithTop.some`

```lean
def some : α → WithBot α
```

24. `LE.le`

```lean
le : α → α → Prop
```


---

## t050

Target: `CategoryTheory.Functor.isDenseAt_iff`

```lean
lemma isDenseAt_iff {X : D} :
    F.isDenseAt X ↔ Nonempty (IsColimit <| (LeftExtension.mk (𝟭 D) F.rightUnitor.inv).coconeAt X)
```

Proof / construction:

```lean
:=
  .rfl
```

Candidates (4), random order:

1. `Iff.rfl`

```lean
protected theorem Iff.rfl {a : Prop} : a ↔ a
```

2. `CategoryTheory.Functor`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

3. `CategoryTheory.Functor.isDenseAt`

```lean
def isDenseAt : ObjectProperty D
```

4. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```


---
