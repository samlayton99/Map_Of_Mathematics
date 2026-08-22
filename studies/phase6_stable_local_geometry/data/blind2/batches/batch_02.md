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

Target: `closedAbsConvexHull`

```lean
def closedAbsConvexHull : ClosureOperator (Set E)
```

Proof / construction:

```lean
:=
  .ofCompletePred (fun s => AbsConvex 𝕜 s ∧ IsClosed s) fun _ ↦ absConvex_closed_sInter
```

Candidates (14), random order:

1. `IsClosed`

```lean
class IsClosed (s : Set X) : Prop
```

2. `CompleteBooleanAlgebra.toCompleteLattice`

```lean
class CompleteBooleanAlgebra (α) extends CompleteLattice α, BooleanAlgebra α
```

3. `SMul`

```lean
class SMul (M : Type u) (α : Type v)
```

4. `ClosureOperator.ofCompletePred`

```lean
def ofCompletePred (p : α → Prop) (hsinf : ∀ s, (∀ a ∈ s, p a) → p (sInf s)) : ClosureOperator α
```

5. `SeminormedRing`

```lean
class SeminormedRing (α : Type*) extends Norm α, Ring α, PseudoMetricSpace α
```

6. `AbsConvex`

```lean
def AbsConvex (s : Set E) : Prop
```

7. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

8. `Set`

```lean
def Set (α : Type u)
```

9. `absConvex_closed_sInter`

```lean
theorem absConvex_closed_sInter {S : Set (Set E)} (h : ∀ s ∈ S, AbsConvex 𝕜 s ∧ IsClosed s) :
    AbsConvex 𝕜 (⋂₀ S) ∧ IsClosed (⋂₀ S)
```

10. `Set.instCompleteAtomicBooleanAlgebra`

```lean
instance instCompleteAtomicBooleanAlgebra : CompleteAtomicBooleanAlgebra (Set α)
```

11. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`

```lean
class CompleteAtomicBooleanAlgebra (α : Type u) extends CompleteBooleanAlgebra α
```

12. `And`

```lean
structure And (a b : Prop) : Prop
```

13. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

14. `PartialOrder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```


---

## t012

Target: `CategoryTheory.Subgroupoid.generatedNormal`

```lean
def generatedNormal : Subgroupoid C
```

Proof / construction:

```lean
:=
  sInf {S : Subgroupoid C | (∀ c d, X c d ⊆ S.arrows c d) ∧ S.IsNormal}
```

Candidates (15), random order:

1. `InfSet.sInf`

```lean
sInf : Set α → α
```

2. `LE.le`

```lean
le : α → α → Prop
```

3. `CategoryTheory.Subgroupoid.IsNormal`

```lean
structure IsNormal : Prop extends IsWide S
```

4. `CategoryTheory.Groupoid.toCategory`

```lean
class Groupoid (obj : Type u) : Type max u (v + 1) extends Category.{v} obj
```

5. `CategoryTheory.Groupoid`

```lean
class Groupoid (obj : Type u) : Type max u (v + 1) extends Category.{v} obj
```

6. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

7. `Set.instLE`

```lean
instance : LE (Set α)
```

8. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

9. `Set`

```lean
def Set (α : Type u)
```

10. `CategoryTheory.Subgroupoid.arrows`

```lean
arrows : ∀ c d : C, Set (c ⟶ d)
```

11. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

12. `Set.ofPred`

```lean
def Set.ofPred {α : Type u} (p : α → Prop) : Set α
```

13. `CategoryTheory.Subgroupoid`

```lean
structure Subgroupoid (C : Type u) [Groupoid C]
```

14. `CategoryTheory.Subgroupoid.instInfSet`

```lean
instance : InfSet (Subgroupoid C)
```

15. `And`

```lean
structure And (a b : Prop) : Prop
```


---

## t013

Target: `Sigma.instLocallyFiniteOrderTop`

```lean
instance instLocallyFiniteOrderTop : LocallyFiniteOrderTop (Σ i, α i)
```

Proof / construction:

```lean
where
  finsetIci | ⟨i, a⟩ => (Ici a).map (Embedding.sigmaMk i)
  finsetIoi | ⟨i, a⟩ => (Ioi a).map (Embedding.sigmaMk i)
  finset_mem_Ici := fun ⟨i, a⟩ ⟨j, b⟩ => by
    obtain rfl | hij := eq_or_ne i j
    · simp
    · simp [hij, le_def]
  finset_mem_Ioi := fun ⟨i, a⟩ ⟨j, b⟩ => by
    obtain rfl | hij := eq_or_ne i j
    · simp
    · simp [hij, lt_def]
```

Candidates (11), random order:

1. `Finset.Ioi`

```lean
def Ioi (a : α) : Finset α
```

2. `Sigma.preorder`

```lean
protected instance preorder [∀ i, Preorder (α i)] : Preorder (Σ i, α i)
```

3. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

4. `LocallyFiniteOrderTop.mk`

```lean
class LocallyFiniteOrderTop (α : Type*) [Preorder α]
```

5. `Finset.map`

```lean
def map (f : α ↪ β) (s : Finset α) : Finset β
```

6. `Finset`

```lean
structure Finset (α : Type*)
```

7. `Sigma.instLocallyFiniteOrderBot`

```lean
instance instLocallyFiniteOrderBot : LocallyFiniteOrderBot (Σ i, α i)
```

8. `Function.Embedding.sigmaMk`

```lean
def sigmaMk (a : α) : β a ↪ Σ x, β x
```

9. `Sigma`

```lean
structure Sigma {α : Type u} (β : α → Type v)
```

10. `Finset.Ici`

```lean
def Ici (a : α) : Finset α
```

11. `LocallyFiniteOrderTop`

```lean
class LocallyFiniteOrderTop (α : Type*) [Preorder α]
```


---

## t014

Target: `OrderHom.Subtype.val`

```lean
def Subtype.val (p : α → Prop) : Subtype p →o α
```

Proof / construction:

```lean
:=
  ⟨_root_.Subtype.val, fun _ _ h => h⟩
```

Candidates (7), random order:

1. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

2. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

3. `Preorder`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

4. `Subtype.val`

```lean
val : α
```

5. `OrderHom.mk`

```lean
structure OrderHom (α β : Type*) [Preorder α] [Preorder β]
```

6. `Subtype.preorder`

```lean
instance preorder [Preorder α] (p : α → Prop) : Preorder (Subtype p)
```

7. `LE.le`

```lean
le : α → α → Prop
```


---

## t015

Target: `MulAction.toPermHom`

```lean
def MulAction.toPermHom : G →* Equiv.Perm α
```

Proof / construction:

```lean
where
  toFun := MulAction.toPerm
  map_one' := Equiv.ext <| one_smul G
  map_mul' u₁ u₂ := Equiv.ext <| mul_smul (u₁ : G) u₂
```

Candidates (12), random order:

1. `MonoidHom.mk`

```lean
structure MonoidHom (M : Type*) (N : Type*) [MulOne M] [MulOne N]
  extends OneHom M N, M →ₙ* N
```

2. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

3. `Equiv.Perm`

```lean
abbrev Equiv.Perm (α : Sort*)
```

4. `MulOne.toOne`

```lean
class MulOne (M : Type*) extends One M, Mul M
```

5. `Group.toDivInvMonoid`

```lean
class Group (G : Type u) extends DivInvMonoid G
```

6. `MulAction.toPerm`

```lean
def MulAction.toPerm (a : α) : Equiv.Perm β
```

7. `DivInvMonoid.toMonoid`

```lean
class DivInvMonoid (G : Type u) extends Monoid G, Inv G, Div G, ZPow G
```

8. `Equiv.Perm.permGroup`

```lean
instance permGroup : Group (Perm α)
```

9. `Monoid.toMulOneClass`

```lean
class Monoid (M : Type u) extends Semigroup M, MulOneClass M, NPow M
```

10. `Group`

```lean
class Group (G : Type u) extends DivInvMonoid G
```

11. `MulAction`

```lean
class MulAction (α : Type*) (β : Type*) [Monoid α] extends SemigroupAction α β
```

12. `OneHom.mk`

```lean
structure OneHom (M : Type*) (N : Type*) [One M] [One N]
```


---

## t016

Target: `Submodule.FG`

```lean
def FG (N : Submodule R M) : Prop
```

Proof / construction:

```lean
:=
  ∃ S : Finset M, span R ↑S = N
```

Candidates (10), random order:

1. `Submodule`

```lean
structure Submodule (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] [Module R M] : Type v
    extends AddSubmonoid M, SubMulAction R M
```

2. `Submodule.span`

```lean
def span (s : Set M) : Submodule R M
```

3. `Finset.instSetLike`

```lean
instance : SetLike (Finset α) α
```

4. `Exists`

```lean
inductive Exists {α : Sort u} (p : α → Prop) : Prop
```

5. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

6. `SetLike.coe`

```lean
protected coe : A → Set B
```

7. `Eq`

```lean
inductive Eq : α → α → Prop
```

8. `Finset`

```lean
structure Finset (α : Type*)
```

9. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

10. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```


---

## t017

Target: `Complex.orthonormalBasisOneI`

```lean
def Complex.orthonormalBasisOneI : OrthonormalBasis (Fin 2) ℝ ℂ
```

Proof / construction:

```lean
:=
  Complex.basisOneI.toOrthonormalBasis
    (by
      rw [orthonormal_iff_ite]
      intro i; fin_cases i <;> intro j <;> fin_cases j <;> simp [real_inner_eq_re_inner])
```

Candidates (12), random order:

1. `Module.Basis.toOrthonormalBasis`

```lean
def _root_.Module.Basis.toOrthonormalBasis (v : Basis ι 𝕜 E) (hv : Orthonormal 𝕜 v) :
    OrthonormalBasis ι 𝕜 E
```

2. `Fin.fintype`

```lean
instance Fin.fintype (n : ℕ) : Fintype (Fin n)
```

3. `Real`

```lean
structure Real
```

4. `Nat`

```lean
inductive Nat
```

5. `Fin`

```lean
structure Fin (n : Nat)
```

6. `Complex`

```lean
structure Complex : Type
```

7. `OfNat.ofNat`

```lean
ofNat : α
```

8. `Complex.basisOneI`

```lean
noncomputable def basisOneI : Basis (Fin 2) ℝ ℂ
```

9. `Real.instRCLike`

```lean
noncomputable instance Real.instRCLike : RCLike ℝ
```

10. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

11. `instInnerProductSpaceRealComplex`

```lean
instance : InnerProductSpace ℝ ℂ
```

12. `Complex.instNormedAddCommGroup`

```lean
instance instNormedAddCommGroup : NormedAddCommGroup ℂ
```


---

## t018

Target: `LinearMap.lTensorHom`

```lean
def lTensorHom : (N →ₗ[R] P) →ₗ[R] M ⊗[R] N →ₗ[R] M ⊗[R] P
```

Proof / construction:

```lean
where
  toFun := lTensor M
  map_add' f g := by
    ext x y
    simp only [compr₂ₛₗ_apply, mk_apply, add_apply, lTensor_tmul, tmul_add]
  map_smul' r f := by
    dsimp
    ext x y
    simp only [compr₂ₛₗ_apply, mk_apply, tmul_smul, smul_apply, lTensor_tmul]
```

Candidates (18), random order:

1. `AddCommSemigroup.toAddCommMagma`

```lean
class AddCommSemigroup (G : Type u) extends AddSemigroup G, AddCommMagma G
```

2. `CommSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

3. `TensorProduct`

```lean
def TensorProduct : Type _
```

4. `RingHom.id`

```lean
def id (α : Type*) [NonAssocSemiring α] : α →+* α
```

5. `LinearMap.module`

```lean
instance module : Module S (M →ₛₗ[σ₁₂] M₂)
```

6. `AddCommMonoid.toAddCommSemigroup`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

7. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

8. `AddCommMagma.toAdd`

```lean
class AddCommMagma (G : Type u) extends Add G
```

9. `LinearMap.mk`

```lean
structure LinearMap {R S : Type*} [Semiring R] [Semiring S] (σ : R →+* S) (M : Type*)
    (M₂ : Type*) [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends
    AddHom M M₂, MulActionHom σ M M₂
```

10. `AddHom.mk`

```lean
structure AddHom (M : Type*) (N : Type*) [Add M] [Add N]
```

11. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

12. `LinearMap.addCommMonoid`

```lean
instance addCommMonoid : AddCommMonoid (M →ₛₗ[σ₁₂] M₂)
```

13. `AddCommMonoid`

```lean
class AddCommMonoid (M : Type u) extends AddMonoid M, AddCommSemigroup M
```

14. `CommSemiring.toSemiring`

```lean
class CommSemiring (R : Type u) extends Semiring R, CommMonoid R
```

15. `TensorProduct.addCommMonoid`

```lean
instance addCommMonoid : AddCommMonoid (M ⊗[R] N)
```

16. `TensorProduct.instModule`

```lean
instance : Module R (M ⊗[R] N)
```

17. `LinearMap`

```lean
structure LinearMap {R S : Type*} [Semiring R] [Semiring S] (σ : R →+* S) (M : Type*)
    (M₂ : Type*) [AddCommMonoid M] [AddCommMonoid M₂] [Module R M] [Module S M₂] extends
    AddHom M M₂, MulActionHom σ M M₂
```

18. `LinearMap.lTensor`

```lean
def lTensor (f : N →ₗ[R] P) : M ⊗[R] N →ₗ[R] M ⊗[R] P
```


---

## t019

Target: `BooleanSubalgebra.instBotCoe`

```lean
instance instBotCoe : Bot L
```

Proof / construction:

```lean
where bot := ⟨⊥, bot_mem⟩
```

Candidates (11), random order:

1. `Membership.mem`

```lean
mem : γ → α → Prop
```

2. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

3. `BooleanSubalgebra`

```lean
structure BooleanSubalgebra [BooleanAlgebra α] extends Sublattice α
```

4. `BooleanSubalgebra.instSetLike`

```lean
instance instSetLike : SetLike (BooleanSubalgebra α) α
```

5. `BooleanSubalgebra.bot_mem`

```lean
@[simp] lemma bot_mem : ⊥ ∈ L
```

6. `Subtype.mk`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

7. `BooleanAlgebra.toBot`

```lean
class BooleanAlgebra (α : Type u) extends
    DistribLattice α, Compl α, SDiff α, HImp α, Top α, Bot α
```

8. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

9. `BooleanAlgebra`

```lean
class BooleanAlgebra (α : Type u) extends
    DistribLattice α, Compl α, SDiff α, HImp α, Top α, Bot α
```

10. `Bot.bot`

```lean
bot : α
```

11. `Bot.mk`

```lean
class Bot (α : Type*)
```


---

## t020

Target: `SemiNormedGrp₁.mkIso`

```lean
def mkIso {M N : SemiNormedGrp} (f : M ≅ N) (i : f.hom.hom.NormNoninc) (i' : f.inv.hom.NormNoninc) :
    SemiNormedGrp₁.of M ≅ SemiNormedGrp₁.of N
```

Proof / construction:

```lean
where
  hom := mkHom f.hom.hom i
  inv := mkHom f.inv.hom i'
```

Candidates (13), random order:

1. `CategoryTheory.Iso`

```lean
structure Iso {C : Type u} [Category.{v} C] (X Y : C)
```

2. `NormedAddGroupHom.NormNoninc`

```lean
def NormNoninc (f : NormedAddGroupHom V W) : Prop
```

3. `SemiNormedGrp.carrier`

```lean
carrier : Type u
```

4. `CategoryTheory.Iso.hom`

```lean
hom : X ⟶ Y
```

5. `CategoryTheory.Iso.inv`

```lean
inv : Y ⟶ X
```

6. `SemiNormedGrp₁.mkHom`

```lean
abbrev mkHom {M N : Type u} [SeminormedAddCommGroup M] [SeminormedAddCommGroup N]
    (f : NormedAddGroupHom M N) (i : f.NormNoninc) :
    SemiNormedGrp₁.of M ⟶ SemiNormedGrp₁.of N
```

7. `SemiNormedGrp.instLargeCategory`

```lean
SemiNormedGrp.instLargeCategory
```

8. `CategoryTheory.Iso.mk`

```lean
structure Iso {C : Type u} [Category.{v} C] (X Y : C)
```

9. `SemiNormedGrp.str`

```lean
SemiNormedGrp.str
```

10. `SemiNormedGrp₁.instLargeCategory`

```lean
SemiNormedGrp₁.instLargeCategory
```

11. `SemiNormedGrp₁`

```lean
structure SemiNormedGrp₁ : Type (u + 1)
```

12. `SemiNormedGrp`

```lean
structure SemiNormedGrp : Type (u + 1)
```

13. `SemiNormedGrp.Hom.hom`

```lean
abbrev Hom.hom {M N : SemiNormedGrp.{u}} (f : Hom M N)
```


---
