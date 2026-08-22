# Blind grading batch 08 — 10 items

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
{"t071": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t071

Target: `CategoryTheory.AddMon.leftUnitor_hom_hom`

```lean
lemma leftUnitor_hom_hom (X : Mon C) : (λ_ X).hom.hom = (λ_ X.X).hom
```

Proof / construction:

```lean
:= rfl
```

Candidates (16), random order:

1. `CategoryTheory.AddMon.X`

```lean
X : C
```

2. `CategoryTheory.AddMon.instCategory`

```lean
instance : Category (Mon C)
```

3. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

4. `CategoryTheory.MonoidalCategoryStruct.leftUnitor`

```lean
leftUnitor : ∀ X : C, tensorObj tensorUnit X ≅ X
```

5. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

6. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

7. `CategoryTheory.MonoidalCategoryStruct.tensorObj`

```lean
tensorObj : C → C → C
```

8. `CategoryTheory.AddMon.monMonoidalStruct`

```lean
instance monMonoidalStruct : MonoidalCategoryStruct (Mon C)
```

9. `CategoryTheory.AddMon`

```lean
structure AddMon
```

10. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

11. `CategoryTheory.Iso.hom`

```lean
hom : X ⟶ Y
```

12. `CategoryTheory.MonoidalCategory`

```lean
class MonoidalCategory (C : Type u) [𝒞 : Category.{v} C] extends MonoidalCategoryStruct C
```

13. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

14. `CategoryTheory.MonoidalCategoryStruct.tensorUnit`

```lean
CategoryTheory.MonoidalCategoryStruct.tensorUnit
```

15. `CategoryTheory.BraidedCategory`

```lean
class BraidedCategory (C : Type u) [Category.{v} C] [MonoidalCategory.{v} C]
```

16. `CategoryTheory.AddMon.Hom.hom`

```lean
hom : M.X ⟶ N.X
```


---

## t072

Target: `Ordinal.cof_lsub_le_lift`

```lean
theorem cof_lsub_le_lift {ι} (f : ι → Ordinal) :
    cof (lsub.{u, v} f) ≤ Cardinal.lift.{v, u} #ι
```

Proof / construction:

```lean
:= by
  rw [← lift_id'.{u} (lsub f), ← Cardinal.lift_umax.{u, v}]
  exact cof_lift_iSup_add_one_le _
```

Candidates (17), random order:

1. `Cardinal`

```lean
def Cardinal : Type (u + 1)
```

2. `Ordinal.cof`

```lean
def cof (o : Ordinal.{u}) : Cardinal.{u}
```

3. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```

4. `Cardinal.mk`

```lean
def mk : Type u → Cardinal
```

5. `Cardinal.lift`

```lean
def lift (c : Cardinal.{v}) : Cardinal.{max v u}
```

6. `LE.le`

```lean
le : α → α → Prop
```

7. `Cardinal.lift_umax`

```lean
theorem lift_umax : lift.{max u v, u} = lift.{v, u}
```

8. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

9. `Cardinal.instLE`

```lean
instance : LE Cardinal.{u}
```

10. `Ordinal.lift`

```lean
def lift (o : Ordinal.{v}) : Ordinal.{max v u}
```

11. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

12. `Ordinal`

```lean
def Ordinal : Type (u + 1)
```

13. `Ordinal.cof_lift_iSup_add_one_le`

```lean
theorem cof_lift_iSup_add_one_le [Small.{u} β] (f : β → Ordinal.{u}) :
    cof (lift.{v} (⨆ i, f i + 1)) ≤ Cardinal.lift.{u} (#β)
```

14. `Ordinal.lsub`

```lean
def lsub {ι : Type u} (f : ι → Ordinal.{max u v}) : Ordinal
```

15. `Eq`

```lean
inductive Eq : α → α → Prop
```

16. `Ordinal.lift_id'`

```lean
theorem lift_id' (a : Ordinal) : lift a = a
```

17. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```


---

## t073

Target: `Meromorphic.iterated_deriv`

```lean
lemma iterated_deriv [CompleteSpace E] {n : ℕ} (hf : Meromorphic f) :
    Meromorphic (deriv^[n] f)
```

Proof / construction:

```lean
:= fun x ↦ (hf x).iterated_deriv
```

Candidates (11), random order:

1. `MeromorphicAt.iterated_deriv`

```lean
@[fun_prop] theorem iterated_deriv [CompleteSpace E] {n : ℕ} {f : 𝕜 → E} {x : 𝕜}
    (h : MeromorphicAt f x) :
    MeromorphicAt (_root_.deriv^[n] f) x
```

2. `CompleteSpace`

```lean
class CompleteSpace (α : Type u) [UniformSpace α] : Prop
```

3. `PseudoMetricSpace.toUniformSpace`

```lean
toUniformSpace : UniformSpace α
```

4. `NormedSpace`

```lean
class NormedSpace (𝕜 : Type*) (E : Type*) [NormedField 𝕜] [SeminormedAddCommGroup E]
    extends Module 𝕜 E
```

5. `Meromorphic`

```lean
def Meromorphic (f : 𝕜 → E)
```

6. `NontriviallyNormedField`

```lean
class NontriviallyNormedField (α : Type*) extends NormedField α
```

7. `NormedAddCommGroup.toSeminormedAddCommGroup`

```lean
NormedAddCommGroup.toSeminormedAddCommGroup
```

8. `Nat`

```lean
inductive Nat
```

9. `NormedAddCommGroup`

```lean
class NormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E, MetricSpace E
```

10. `NontriviallyNormedField.toNormedField`

```lean
class NontriviallyNormedField (α : Type*) extends NormedField α
```

11. `SeminormedAddCommGroup.toPseudoMetricSpace`

```lean
class SeminormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E,
  PseudoMetricSpace E
```


---

## t074

Target: `Ordinal.isInitial_omega`

```lean
theorem isInitial_omega (o : Ordinal) : IsInitial (omega o)
```

Proof / construction:

```lean
:=
  isInitial_preOmega _
```

Candidates (17), random order:

1. `SemilatticeInf.toPartialOrder`

```lean
class SemilatticeInf (α : Type u) extends PartialOrder α
```

2. `RelEmbedding.toEmbedding`

```lean
RelEmbedding.toEmbedding
```

3. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

4. `Function.Embedding`

```lean
structure Embedding (α : Sort*) (β : Sort*)
```

5. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

6. `Ordinal.instLinearOrder`

```lean
instance : LinearOrder Ordinal
```

7. `Lattice.toSemilatticeInf`

```lean
class Lattice (α : Type u) extends SemilatticeSup α, SemilatticeInf α
```

8. `Ordinal.add`

```lean
instance add : Add Ordinal.{u}
```

9. `Function.instFunLikeEmbedding`

```lean
instance {α : Sort u} {β : Sort v} : FunLike (α ↪ β) α β
```

10. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

11. `Ordinal.isInitial_preOmega`

```lean
theorem isInitial_preOmega (o : Ordinal) : IsInitial (preOmega o)
```

12. `OrderEmbedding.addLeft`

```lean
OrderEmbedding.addLeft
```

13. `LE.le`

```lean
le : α → α → Prop
```

14. `instDistribLatticeOfLinearOrder`

```lean
instDistribLatticeOfLinearOrder
```

15. `DistribLattice.toLattice`

```lean
class DistribLattice (α) extends Lattice α
```

16. `Ordinal.omega0`

```lean
def omega0 : Ordinal.{u}
```

17. `Ordinal`

```lean
def Ordinal : Type (u + 1)
```


---

## t075

Target: `Fin.append_right_cons`

```lean
theorem append_right_cons {n m} {α : Sort*} (xs : Fin n → α) (y : α) (ys : Fin m → α) :
    Fin.append xs (Fin.cons y ys) =
      Fin.append (Fin.snoc xs y) ys ∘ Fin.cast (Nat.succ_add_eq_add_succ ..).symm
```

Proof / construction:

```lean
:= by
  rw [append_left_snoc]; rfl
```

Candidates (21), random order:

1. `Nat`

```lean
inductive Nat
```

2. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

3. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

4. `Fin`

```lean
structure Fin (n : Nat)
```

5. `Fin.cons`

```lean
def cons (x : α 0) (p : ∀ i : Fin n, α i.succ) : ∀ i, α i
```

6. `Eq.refl`

```lean
| refl (a : α) : Eq a a
```

7. `Fin.snoc`

```lean
def snoc (p : ∀ i : Fin n, α i.castSucc) (x : α (last n)) (i : Fin (n + 1)) : α i
```

8. `OfNat.ofNat`

```lean
ofNat : α
```

9. `Fin.append_left_snoc`

```lean
theorem append_left_snoc {n m} {α : Sort*} (xs : Fin n → α) (x : α) (ys : Fin m → α) :
    Fin.append (Fin.snoc xs x) ys =
      Fin.append xs (Fin.cons x ys) ∘ Fin.cast (Nat.succ_add_eq_add_succ ..)
```

10. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```

11. `Eq`

```lean
inductive Eq : α → α → Prop
```

12. `instHAdd`

```lean
instance instHAdd [Add α] : HAdd α α α
```

13. `Function.comp`

```lean
@[inline, implicit_reducible] def Function.comp {α : Sort u} {β : Sort v} {δ : Sort w} (f : β → δ) (g : α → β) : α → δ
```

14. `Fin.append`

```lean
def append (a : Fin m → α) (b : Fin n → α) : Fin (m + n) → α
```

15. `Nat.succ`

```lean
| succ (n : Nat) : Nat
```

16. `instAddNat`

```lean
instance instAddNat : Add Nat
```

17. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

18. `Nat.succ_add_eq_add_succ`

```lean
theorem succ_add_eq_add_succ (a b) : succ a + b = a + succ b
```

19. `Fin.cast`

```lean
@[inline, implicit_reducible] protected def cast (eq : n = m) (i : Fin n) : Fin m
```

20. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

21. `HAdd.hAdd`

```lean
hAdd : α → β → γ
```


---

## t076

Target: `DirectSum.lmap_injective`

```lean
theorem lmap_injective : Function.Injective (lmap f) ↔ ∀ i, Function.Injective (f i)
```

Proof / construction:

```lean
:= by
  exact DFinsupp.mapRange_injective (hf := fun _ ↦ map_zero _)
```

Candidates (18), random order:

1. `AddZeroClass.toAddZero`

```lean
class AddZeroClass (M : Type u) extends AddZero M
```

2. `DFinsupp.mapRange_injective`

```lean
theorem mapRange_injective (f : ∀ i, β₁ i → β₂ i) (hf : ∀ i, f i 0 = 0) :
    Function.Injective (mapRange f hf) ↔ ∀ i, Function.Injective (f i)
```

3. `RingHom.instFunLike`

```lean
instance instFunLike : FunLike (α →+* β) α β
```

4. `AddCommMonoid.toAddMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

5. `LinearMap.instFunLike`

```lean
instance instFunLike : FunLike (M →ₛₗ[σ] M₃) M M₃
```

6. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

7. `RingHom.id`

```lean
def id (α : Type*) [NonAssocSemiring α] : α →+* α
```

8. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

9. `RingHom`

```lean
structure RingHom (α : Type*) (β : Type*) [NonAssocSemiring α] [NonAssocSemiring β] extends
  α →* β, α →+ β, α →ₙ+* β, α →*₀ β
```

10. `AddZero.toZero`

```lean
class AddZero (M : Type*) extends Zero M, Add M
```

11. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

12. `AddMonoid.toAddZeroClass`

```lean
class AddMonoid (M : Type u) extends AddSemigroup M, AddZeroClass M, NSMul M
```

13. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

14. `Module.toDistribMulAction`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

15. `LinearMap`

```lean
structure LinearMap {R S : Type*} [Semiring R] [Semiring S] (σ : R →+* S) (M : Type*)
    (M₂ : Type*) [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends
    AddHom M M₂, MulActionHom σ M M₂
```

16. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

17. `Semiring.toMonoid`

```lean
Semiring.toMonoid
```

18. `map_zero`

```lean
map_zero : ∀ f : F, f 0 = 0
```


---

## t077

Target: `CategoryTheory.to_initial_isIso`

```lean
instance to_initial_isIso [HasInitial C] (f : A ⟶ ⊥_ C) : IsIso f
```

Proof / construction:

```lean
:=
  strict_initial initialIsInitial _
```

Candidates (12), random order:

1. `CategoryTheory.Limits.initialIsInitial`

```lean
def initialIsInitial [HasInitial C] : IsInitial (⊥_ C)
```

2. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

3. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

4. `CategoryTheory.CartesianMonoidalCategory.toSemiCartesianMonoidalCategory`

```lean
class CartesianMonoidalCategory (C : Type u) [Category.{v} C] extends
    SemiCartesianMonoidalCategory C
```

5. `CategoryTheory.Limits.initial`

```lean
abbrev initial [HasInitial C] : C
```

6. `CategoryTheory.Closed`

```lean
class Closed {C : Type u} [Category.{v} C] [MonoidalCategory.{v} C] (X : C)
```

7. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

8. `CategoryTheory.Limits.HasInitial`

```lean
abbrev HasInitial
```

9. `CategoryTheory.strict_initial`

```lean
theorem strict_initial {I : C} (t : IsInitial I) (f : A ⟶ I) : IsIso f
```

10. `CategoryTheory.SemiCartesianMonoidalCategory.toMonoidalCategory`

```lean
class SemiCartesianMonoidalCategory (C : Type u) [Category.{v} C] extends MonoidalCategory C
```

11. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

12. `CategoryTheory.CartesianMonoidalCategory`

```lean
class CartesianMonoidalCategory (C : Type u) [Category.{v} C] extends
    SemiCartesianMonoidalCategory C
```


---

## t078

Target: `OpenAddSubgroup.instInhabited`

```lean
instance : Inhabited (OpenSubgroup G)
```

Proof / construction:

```lean
:=
  ⟨⊤⟩
```

Candidates (6), random order:

1. `AddGroup`

```lean
class AddGroup (A : Type u) extends SubNegMonoid A
```

2. `Inhabited.mk`

```lean
class Inhabited (α : Sort u)
```

3. `OpenAddSubgroup.instTop`

```lean
@[to_additive] instance : Top (OpenSubgroup G)
```

4. `OpenAddSubgroup`

```lean
structure OpenAddSubgroup (G : Type*) [AddGroup G] [TopologicalSpace G] extends AddSubgroup G
```

5. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

6. `Top.top`

```lean
top : α
```


---

## t079

Target: `UniformFunOn.uniformContinuousConstSMul`

```lean
instance UniformFunOn.uniformContinuousConstSMul {𝔖 : Set (Set α)} :
    UniformContinuousConstSMul M (α →ᵤ[𝔖] X)
```

Proof / construction:

```lean
where
  uniformContinuous_const_smul c := UniformOnFun.postcomp_uniformContinuous <|
    uniformContinuous_const_smul c
```

Candidates (12), random order:

1. `UniformContinuousConstSMul.mk`

```lean
class UniformContinuousConstSMul [SMul M X] : Prop
```

2. `Set`

```lean
def Set (α : Type u)
```

3. `UniformOnFun`

```lean
def UniformOnFun (α β : Type*) (_ : Set (Set α))
```

4. `instNSMulUniformOnFun`

```lean
instNSMulUniformOnFun
```

5. `SMul`

```lean
class SMul (M : Type u) (α : Type v)
```

6. `UniformSpace`

```lean
class UniformSpace (α : Type u) extends TopologicalSpace α
```

7. `UniformContinuousConstSMul`

```lean
class UniformContinuousConstSMul [SMul M X] : Prop
```

8. `instHSMul`

```lean
instance instHSMul {α β} [SMul α β] : HSMul α β β
```

9. `UniformOnFun.uniformSpace`

```lean
instance uniformSpace : UniformSpace (α →ᵤ[𝔖] β)
```

10. `UniformContinuousConstSMul.uniformContinuous_const_smul`

```lean
uniformContinuous_const_smul : ∀ c : M, UniformContinuous (c • · : X → X)
```

11. `UniformOnFun.postcomp_uniformContinuous`

```lean
protected theorem postcomp_uniformContinuous [UniformSpace γ] {f : γ → β}
    (hf : UniformContinuous f) : UniformContinuous (ofFun 𝔖 ∘ (f ∘ ·) ∘ toFun 𝔖)
```

12. `HSMul.hSMul`

```lean
hSMul : α → β → γ
```


---

## t080

Target: `Stirling.stirlingSeq`

```lean
noncomputable def stirlingSeq (n : ℕ) : ℝ
```

Proof / construction:

```lean
:=
  n ! / (√(2 * n : ℝ) * (n / exp 1) ^ n)
```

Candidates (23), random order:

1. `Real.exp`

```lean
nonrec def exp (x : ℝ) : ℝ
```

2. `instHMul`

```lean
instance instHMul [Mul α] : HMul α α α
```

3. `Real.sqrt`

```lean
@[irreducible] noncomputable def sqrt (x : ℝ) : ℝ
```

4. `Nat.cast`

```lean
protected def Nat.cast {R : Type u} [NatCast R] : Nat → R
```

5. `Real.instOne`

```lean
instance : One ℝ
```

6. `Nat.factorial`

```lean
def factorial : ℕ → ℕ
  | 0 => 1
  | succ n => succ n * factorial n
```

7. `Nat`

```lean
inductive Nat
```

8. `Real.instNatCast`

```lean
instance instNatCast : NatCast ℝ
```

9. `Real`

```lean
structure Real
```

10. `Real.instMul`

```lean
instance : Mul ℝ
```

11. `DivInvMonoid.toDiv`

```lean
class DivInvMonoid (G : Type u) extends Monoid G, Inv G, Div G, ZPow G
```

12. `instHPow`

```lean
instance instHPow [Pow α β] : HPow α β α
```

13. `HDiv.hDiv`

```lean
hDiv : α → β → γ
```

14. `One.toOfNat1`

```lean
instance (priority := 300) One.toOfNat1 {α} [One α] : OfNat α (nat_lit 1)
```

15. `Real.instDivInvMonoid`

```lean
noncomputable instance instDivInvMonoid : DivInvMonoid ℝ
```

16. `instHDiv`

```lean
instance instHDiv [Div α] : HDiv α α α
```

17. `Real.instMonoid`

```lean
instance : Monoid ℝ
```

18. `HMul.hMul`

```lean
hMul : α → β → γ
```

19. `Monoid.toNPow`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

20. `NPow.toPow`

```lean
instance NPow.toPow {M : Type*} [NPow M] : Pow M ℕ
```

21. `instOfNatAtLeastTwo`

```lean
instance (priority := 100) instOfNatAtLeastTwo {n : ℕ} [NatCast R] [Nat.AtLeastTwo n] :
    OfNat R n
```

22. `OfNat.ofNat`

```lean
ofNat : α
```

23. `HPow.hPow`

```lean
hPow : α → β → γ
```


---
