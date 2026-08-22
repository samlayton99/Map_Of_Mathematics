# Blind grading batch 07 — 10 items

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
{"t061": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t061

Target: `Set.coe_toFinset`

```lean
theorem coe_toFinset (s : Set α) [Fintype s] : (↑s.toFinset : Set α) = s
```

Proof / construction:

```lean
:=
  Set.ext fun _ => mem_toFinset
```

Candidates (9), random order:

1. `Set.mem_toFinset`

```lean
theorem mem_toFinset {s : Set α} [Fintype s] {a : α} : a ∈ s.toFinset ↔ a ∈ s
```

2. `Set`

```lean
def Set (α : Type u)
```

3. `Set.toFinset`

```lean
def toFinset (s : Set α) [Fintype s] : Finset α
```

4. `Set.Elem`

```lean
@[coe, reducible] def Elem (s : Set α) : Type u
```

5. `Set.ext`

```lean
theorem ext {a b : Set α} (h : ∀ (x : α), x ∈ a ↔ x ∈ b) : a = b
```

6. `SetLike.coe`

```lean
protected coe : A → Set B
```

7. `Finset`

```lean
structure Finset (α : Type*)
```

8. `Finset.instSetLike`

```lean
instance : SetLike (Finset α) α
```

9. `Fintype`

```lean
class Fintype (α : Type*)
```


---

## t062

Target: `Ordinal.preOmega`

```lean
def preOmega : Ordinal.{u} ↪o Ordinal.{u}
```

Proof / construction:

```lean
where
  toFun := enumOrd {x | IsInitial x}
  inj' _ _ h := enumOrd_injective not_bddAbove_isInitial h
  map_rel_iff' := enumOrd_le_enumOrd not_bddAbove_isInitial
```

Candidates (10), random order:

1. `Ordinal.IsInitial`

```lean
def IsInitial (o : Ordinal) : Prop
```

2. `Ordinal.enumOrd`

```lean
noncomputable def enumOrd (s : Set Ordinal.{u}) (o : Ordinal.{u}) : Ordinal.{u}
```

3. `RelEmbedding.mk`

```lean
structure RelEmbedding {α β : Type*} (r : α → α → Prop) (s : β → β → Prop) extends α ↪ β
```

4. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

5. `LE.le`

```lean
le : α → α → Prop
```

6. `Set.ofPred`

```lean
def Set.ofPred {α : Type u} (p : α → Prop) : Set α
```

7. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

8. `Function.Embedding.mk`

```lean
structure Embedding (α : Sort*) (β : Sort*)
```

9. `Ordinal.partialOrder`

```lean
instance partialOrder : PartialOrder Ordinal
```

10. `Ordinal`

```lean
def Ordinal : Type (u + 1)
```


---

## t063

Target: `MeasurableSpace.generateMeasurableRec_subset`

```lean
theorem generateMeasurableRec_subset (s : Set (Set α)) (i : Ordinal) :
    generateMeasurableRec s i ⊆ { t | GenerateMeasurable s t }
```

Proof / construction:

```lean
:= by
  apply WellFoundedLT.induction i
  exact fun i IH t ht => generateMeasurableRec_induction .basic .empty
    (fun u _ ⟨j, hj, hj'⟩ => .compl _ (IH j hj hj')) (fun f H => .iUnion _ fun n => (H n).1) ht
```

Candidates (25), random order:

1. `And.left`

```lean
left : a
```

2. `Membership.mem`

```lean
mem : γ → α → Prop
```

3. `Set.instMembership`

```lean
instance : Membership α (Set α)
```

4. `Set.instCompl`

```lean
instance : Compl (Set α)
```

5. `Ordinal.partialOrder`

```lean
instance partialOrder : PartialOrder Ordinal
```

6. `Compl.compl`

```lean
compl : α → α
```

7. `MeasurableSpace.GenerateMeasurable.iUnion`

```lean
protected theorem MeasurableSet.iUnion [Countable ι] ⦃f : ι → Set α⦄
    (h : ∀ b, MeasurableSet (f b)) : MeasurableSet (⋃ b, f b)
```

8. `Set`

```lean
def Set (α : Type u)
```

9. `LT.lt`

```lean
lt : α → α → Prop
```

10. `MeasurableSpace.GenerateMeasurable.empty`

```lean
theorem MeasurableSet.empty [MeasurableSpace α] : MeasurableSet (∅ : Set α)
```

11. `Set.instLE`

```lean
instance : LE (Set α)
```

12. `MeasurableSpace.GenerateMeasurable.compl`

```lean
protected theorem MeasurableSet.compl : MeasurableSet s → MeasurableSet sᶜ
```

13. `WellFoundedLT.induction`

```lean
theorem induction {motive : α → Prop} (a : α)
    (ind : ∀ x, (∀ y, y < x → motive y) → motive x) : motive a
```

14. `MeasurableSpace.GenerateMeasurable.basic`

```lean
MeasurableSpace.GenerateMeasurable.basic
```

15. `Ordinal`

```lean
def Ordinal : Type (u + 1)
```

16. `Preorder.toLT`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

17. `MeasurableSpace.GenerateMeasurable`

```lean
inductive GenerateMeasurable (s : Set (Set α)) : Set α → Prop
  | protected basic : ∀ u ∈ s, GenerateMeasurable s u
  | protected empty : GenerateMeasurable s ∅
  | protected compl : ∀ t, GenerateMeasurable s t → GenerateMeasurable s tᶜ
  | protected iUnion : ∀ f : ℕ → Set α, (∀ n, GenerateMeasurable s (f n)) →
      GenerateMeasurable s (⋃ i, f i)
```

18. `LE.le`

```lean
le : α → α → Prop
```

19. `Nat`

```lean
inductive Nat
```

20. `Set.ofPred`

```lean
def Set.ofPred {α : Type u} (p : α → Prop) : Set α
```

21. `Exists`

```lean
inductive Exists {α : Sort u} (p : α → Prop) : Prop
```

22. `MeasurableSpace.generateMeasurableRec`

```lean
def generateMeasurableRec (s : Set (Set α)) (i : Ordinal) : Set (Set α)
```

23. `MeasurableSpace.generateMeasurableRec_induction`

```lean
theorem generateMeasurableRec_induction {s : Set (Set α)} {i : Ordinal} {t : Set α}
    {p : Set α → Prop} (hs : ∀ t ∈ s, p t) (h0 : p ∅)
    (hc : ∀ u, p u → (∃ j < i, u ∈ generateMeasurableRec s j) → p uᶜ)
    (hn : ∀ f : ℕ → Set α,
      (∀ n, p (f n) ∧ ∃ j < i, f n ∈ generateMeasurableRec s j) → p (⋃ n, f n)) :
    t ∈ generateMeasurableRec s i → p t
```

24. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

25. `And`

```lean
structure And (a b : Prop) : Prop
```


---

## t064

Target: `AlgebraicGeometry.PresheafedSpace.forget`

```lean
def forget : PresheafedSpace C ⥤ TopCat
```

Proof / construction:

```lean
where
  obj X := (X : TopCat)
  map f := f.base
```

Candidates (11), random order:

1. `TopCat`

```lean
structure TopCat
```

2. `AlgebraicGeometry.PresheafedSpace.categoryOfPresheafedSpaces`

```lean
instance categoryOfPresheafedSpaces : Category (PresheafedSpace C)
```

3. `AlgebraicGeometry.PresheafedSpace.carrier`

```lean
carrier : TopCat.{u}
```

4. `TopCat.instCategory`

```lean
instance : Category TopCat
```

5. `AlgebraicGeometry.PresheafedSpace`

```lean
AlgebraicGeometry.PresheafedSpace
```

6. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

7. `CategoryTheory.Functor.mk`

```lean
structure Functor (C : Type u₁) [Category.{v₁} C] (D : Type u₂) [Category.{v₂} D] :
    Type max v₁ v₂ u₁ u₂
```

8. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

9. `AlgebraicGeometry.PresheafedSpace.Hom.base`

```lean
base : (X : TopCat) ⟶ (Y : TopCat)
```

10. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

11. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```


---

## t065

Target: `RelIso.instFunLike`

```lean
instance : FunLike (r ≃r s) α β
```

Proof / construction:

```lean
where
  coe x := x
  coe_injective := Equiv.coe_fn_injective.comp toEquiv_injective
```

Candidates (6), random order:

1. `DFunLike.mk`

```lean
class DFunLike (F : Sort*) (α : outParam (Sort*)) (β : outParam <| α → Sort*)
```

2. `RelEmbedding`

```lean
structure RelEmbedding {α β : Type*} (r : α → α → Prop) (s : β → β → Prop) extends α ↪ β
```

3. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

4. `RelIso.toRelEmbedding`

```lean
def toRelEmbedding (f : r ≃r s) : r ↪r s
```

5. `RelEmbedding.instFunLike`

```lean
instance : FunLike (r ↪r s) α β
```

6. `RelIso`

```lean
structure RelIso {α β : Type*} (r : α → α → Prop) (s : β → β → Prop) extends α ≃ β
```


---

## t066

Target: `Fin.preimage_castAdd_Ici_castAdd`

```lean
theorem preimage_castAdd_Ici_castAdd (m) (i : Fin n) : castAdd m ⁻¹' Ici (castAdd m i) = Ici i
```

Proof / construction:

```lean
:=
  rfl
```

Candidates (12), random order:

1. `Fin`

```lean
structure Fin (n : Nat)
```

2. `Fin.instPartialOrder`

```lean
instance instPartialOrder : PartialOrder (Fin n)
```

3. `HAdd.hAdd`

```lean
hAdd : α → β → γ
```

4. `Set`

```lean
def Set (α : Type u)
```

5. `instAddNat`

```lean
instance instAddNat : Add Nat
```

6. `instHAdd`

```lean
instance instHAdd [Add α] : HAdd α α α
```

7. `Set.Ici`

```lean
Set.Ici
```

8. `Fin.castAdd`

```lean
@[inline, implicit_reducible] def castAdd (m) : Fin n → Fin (n + m)
```

9. `Nat`

```lean
inductive Nat
```

10. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

11. `Set.preimage`

```lean
def preimage (f : α → β) (s : Set β) : Set α
```

12. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```


---

## t067

Target: `CongruenceSubgroup.Gamma0_is_congruence`

```lean
theorem Gamma0_is_congruence (N : ℕ) [NeZero N] : IsCongruenceSubgroup (Gamma0 N)
```

Proof / construction:

```lean
:=
  isCongruenceSubgroup_trans _ _ (Gamma1_in_Gamma0 N) (Gamma1_is_congruence N)
```

Candidates (9), random order:

1. `CongruenceSubgroup.Gamma1_is_congruence`

```lean
theorem Gamma1_is_congruence (N : ℕ) [NeZero N] : IsCongruenceSubgroup (Gamma1 N)
```

2. `MulZeroClass.toZero`

```lean
class MulZeroClass (M₀ : Type u) extends Mul M₀, Zero M₀
```

3. `CongruenceSubgroup.Gamma0`

```lean
def Gamma0 : Subgroup SL(2, ℤ)
```

4. `CongruenceSubgroup.Gamma1_in_Gamma0`

```lean
theorem Gamma1_in_Gamma0 (N : ℕ) : Gamma1 N ≤ Gamma0 N
```

5. `Nat`

```lean
inductive Nat
```

6. `CongruenceSubgroup.Gamma1`

```lean
def Gamma1 (N : ℕ) : Subgroup SL(2, ℤ)
```

7. `NeZero`

```lean
class NeZero (n : R) : Prop
```

8. `Nat.instMulZeroClass`

```lean
instance instMulZeroClass : MulZeroClass ℕ
```

9. `CongruenceSubgroup.isCongruenceSubgroup_trans`

```lean
theorem isCongruenceSubgroup_trans (H K : Subgroup SL(2, ℤ)) (h : H ≤ K)
    (h2 : IsCongruenceSubgroup H) : IsCongruenceSubgroup K
```


---

## t068

Target: `ciSup_le`

```lean
theorem ciSup_le [Nonempty ι] {f : ι → α} {c : α} (H : ∀ x, f x ≤ c) : iSup f ≤ c
```

Proof / construction:

```lean
:=
  csSup_le (range_nonempty f) (by rwa [forall_mem_range])
```

Candidates (23), random order:

1. `Membership.mem`

```lean
mem : γ → α → Prop
```

2. `Set.forall_mem_range`

```lean
theorem forall_mem_range {p : α → Prop} : (∀ a ∈ range f, p a) ↔ ∀ i, p (f i)
```

3. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

4. `propext`

```lean
axiom propext {a b : Prop} : (a ↔ b) → a = b
```

5. `Set.range_nonempty`

```lean
theorem range_nonempty [h : Nonempty ι] (f : ι → α) : (range f).Nonempty
```

6. `ConditionallyCompletePartialOrderSup.toPartialOrder`

```lean
class ConditionallyCompletePartialOrderSup (α : Type*)
    extends PartialOrder α, SupSet α
```

7. `ConditionallyCompleteLattice.toLattice`

```lean
class ConditionallyCompleteLattice (α : Type*) extends Lattice α, SupSet α, InfSet α
```

8. `csSup_le`

```lean
theorem csSup_le (h₁ : s.Nonempty) (h₂ : ∀ b ∈ s, b ≤ a) : sSup s ≤ a
```

9. `ConditionallyCompleteLattice.toConditionallyCompletePartialOrder`

```lean
instance (priority := 100) ConditionallyCompleteLattice.toConditionallyCompletePartialOrder :
    ConditionallyCompletePartialOrder α
```

10. `LE.le`

```lean
le : α → α → Prop
```

11. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

12. `SemilatticeInf.toPartialOrder`

```lean
class SemilatticeInf (α : Type u) extends PartialOrder α
```

13. `Eq`

```lean
inductive Eq : α → α → Prop
```

14. `ConditionallyCompleteLattice`

```lean
class ConditionallyCompleteLattice (α : Type*) extends Lattice α, SupSet α, InfSet α
```

15. `Set.range`

```lean
def range (f : ι → α) : Set α
```

16. `Nonempty`

```lean
class inductive Nonempty (α : Sort u) : Prop
```

17. `ConditionallyCompletePartialOrder.toConditionallyCompletePartialOrderSup`

```lean
class ConditionallyCompletePartialOrder (α : Type*)
    extends ConditionallyCompletePartialOrderSup α, ConditionallyCompletePartialOrderInf α
```

18. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

19. `Set`

```lean
def Set (α : Type u)
```

20. `Lattice.toSemilatticeInf`

```lean
class Lattice (α : Type u) extends SemilatticeSup α, SemilatticeInf α
```

21. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

22. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

23. `Set.instMembership`

```lean
instance : Membership α (Set α)
```


---

## t069

Target: `SimpleGraph.ediam_ne_top_of_diam_ne_zero`

```lean
lemma ediam_ne_top_of_diam_ne_zero (h : G.diam ≠ 0) : G.ediam ≠ ⊤
```

Proof / construction:

```lean
:=
  mt diam_eq_zero_of_ediam_eq_top h
```

Candidates (13), random order:

1. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

2. `SimpleGraph.diam`

```lean
noncomputable def diam (G : SimpleGraph α)
```

3. `ENat`

```lean
def ENat : Type
```

4. `mt`

```lean
theorem mt {a b : Prop} (h₁ : a → b) (h₂ : ¬b) : ¬a
```

5. `Eq`

```lean
inductive Eq : α → α → Prop
```

6. `SimpleGraph.diam_eq_zero_of_ediam_eq_top`

```lean
lemma diam_eq_zero_of_ediam_eq_top (h : G.ediam = ⊤) : G.diam = 0
```

7. `SimpleGraph.ediam`

```lean
noncomputable def ediam (G : SimpleGraph α) : ℕ∞
```

8. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

9. `OfNat.ofNat`

```lean
ofNat : α
```

10. `Nat`

```lean
inductive Nat
```

11. `Top.top`

```lean
top : α
```

12. `SimpleGraph`

```lean
structure SimpleGraph (V : Type u)
```

13. `instTopENat`

```lean
instTopENat
```


---

## t070

Target: `ENNReal.ofReal_eq_ofNat`

```lean
lemma ofReal_eq_ofNat {r : ℝ} {n : ℕ} [n.AtLeastTwo] :
    ENNReal.ofReal r = ofNat(n) ↔ r = OfNat.ofNat n
```

Proof / construction:

```lean
:=
  ofReal_eq_natCast (NeZero.ne n)
```

Candidates (7), random order:

1. `Nat.instMulZeroClass`

```lean
instance instMulZeroClass : MulZeroClass ℕ
```

2. `NeZero.ne`

```lean
theorem NeZero.ne (n : R) [h : NeZero n] : n ≠ 0
```

3. `ENNReal.ofReal_eq_natCast`

```lean
lemma ofReal_eq_natCast {r : ℝ} {n : ℕ} (h : n ≠ 0) : ENNReal.ofReal r = n ↔ r = n
```

4. `Nat.AtLeastTwo`

```lean
class AtLeastTwo (n : ℕ) : Prop
```

5. `Real`

```lean
structure Real
```

6. `Nat`

```lean
inductive Nat
```

7. `MulZeroClass.toZero`

```lean
class MulZeroClass (M₀ : Type u) extends Mul M₀, Zero M₀
```


---
