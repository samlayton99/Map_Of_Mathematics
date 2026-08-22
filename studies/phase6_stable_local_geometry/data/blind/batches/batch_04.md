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

Target: `IsometryEquiv.preimage_sphere`

```lean
theorem preimage_sphere (h : α ≃ᵢ β) (x : β) (r : ℝ) :
    h ⁻¹' Metric.sphere x r = Metric.sphere (h.symm x) r
```

Proof / construction:

```lean
:= by
  rw [← h.isometry.preimage_sphere (h.symm x) r, h.apply_symm_apply]
```

Candidates (20), random order:

1. `IsometryEquiv`

```lean
structure IsometryEquiv (α : Type u) (β : Type v) [PseudoEMetricSpace α] [PseudoEMetricSpace β]
    extends α ≃ β
```

2. `PseudoMetricSpace`

```lean
class PseudoMetricSpace (α : Type u) : Type u extends Dist α
```

3. `Set`

```lean
def Set (α : Type u)
```

4. `Isometry.preimage_sphere`

```lean
theorem preimage_sphere (hf : Isometry f) (x : α) (r : ℝ) :
    f ⁻¹' Metric.sphere (f x) r = Metric.sphere x r
```

5. `IsometryEquiv.instEquivLike`

```lean
instance : EquivLike (α ≃ᵢ β) α β
```

6. `PseudoMetricSpace.toPseudoEMetricSpace`

```lean
instance (priority := 100) PseudoMetricSpace.toPseudoEMetricSpace : PseudoEMetricSpace α
```

7. `Eq.refl`

```lean
| refl (a : α) : Eq a a
```

8. `Eq`

```lean
inductive Eq : α → α → Prop
```

9. `IsometryEquiv.isometry`

```lean
protected theorem isometry (h : α ≃ᵢ β) : Isometry h
```

10. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

11. `IsometryEquiv.symm`

```lean
protected def symm (h : α ≃ᵢ β) : β ≃ᵢ α
```

12. `Real`

```lean
structure Real
```

13. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

14. `Set.preimage`

```lean
def preimage (f : α → β) (s : Set β) : Set α
```

15. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

16. `IsometryEquiv.apply_symm_apply`

```lean
theorem apply_symm_apply (h : α ≃ᵢ β) (y : β) : h (h.symm y) = y
```

17. `Metric.sphere`

```lean
def sphere (x : α) (ε : ℝ)
```

18. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

19. `EquivLike.toFunLike`

```lean
instance (priority := 100) toFunLike : FunLike E α β
```

20. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```


---

## t032

Target: `ProbabilityTheory.iIndepSet_iff_iIndepSets_singleton`

```lean
theorem iIndepSet_iff_iIndepSets_singleton {f : ι → Set Ω} (hf : ∀ i, MeasurableSet (f i)) :
    iIndepSet f μ ↔ iIndepSets (fun i ↦ {f i}) μ
```

Proof / construction:

```lean
:=
  Kernel.iIndepSet_iff_iIndepSets_singleton hf
```

Candidates (10), random order:

1. `ProbabilityTheory.Kernel.const`

```lean
def const (α : Type*) {β : Type*} [MeasurableSpace α] {_ : MeasurableSpace β} (μβ : Measure β) :
    Kernel α β
```

2. `MeasureTheory.Measure`

```lean
structure Measure (α : Type*) [MeasurableSpace α] extends OuterMeasure α
```

3. `MeasurableSet`

```lean
def MeasurableSet [MeasurableSpace α] (s : Set α) : Prop
```

4. `Unit`

```lean
abbrev Unit : Type
```

5. `ProbabilityTheory.Kernel.iIndepSet_iff_iIndepSets_singleton`

```lean
theorem iIndepSet_iff_iIndepSets_singleton {_mΩ : MeasurableSpace Ω} {κ : Kernel α Ω}
    {μ : Measure α} {f : ι → Set Ω} (hf : ∀ i, MeasurableSet (f i)) :
    iIndepSet f κ μ ↔ iIndepSets (fun i ↦ {f i}) κ μ
```

6. `PUnit.instMeasurableSpace`

```lean
instance PUnit.instMeasurableSpace : MeasurableSpace PUnit
```

7. `MeasurableSpace`

```lean
@[class] structure MeasurableSpace (α : Type*)
```

8. `Unit.unit`

```lean
@[match_pattern] abbrev Unit.unit : Unit
```

9. `MeasureTheory.Measure.dirac`

```lean
def dirac (a : α) : Measure α
```

10. `Set`

```lean
def Set (α : Type u)
```


---

## t033

Target: `PiLp.antilipschitzWith_toLp`

```lean
lemma antilipschitzWith_toLp [∀ i, PseudoEMetricSpace (β i)] :
    AntilipschitzWith 1 (@toLp p (∀ i, β i))
```

Proof / construction:

```lean
:=
  (lipschitzWith_ofLp p β).to_rightInverse (ofLp_toLp p)
```

Candidates (18), random order:

1. `WithLp.ofLp`

```lean
ofLp : V
```

2. `ENNReal.instLE`

```lean
ENNReal.instLE
```

3. `PseudoEMetricSpace`

```lean
class PseudoEMetricSpace (α : Type u) : Type u extends EDist α
```

4. `NNReal`

```lean
def NNReal
```

5. `ENNReal.instOne`

```lean
instance : One ℝ≥0∞
```

6. `NNReal.instOne`

```lean
instance : One ℝ≥0
```

7. `PiLp.instPseudoEMetricSpace`

```lean
instance [∀ i, PseudoEMetricSpace (β i)] : PseudoEMetricSpace (PiLp p β)
```

8. `PiLp.lipschitzWith_ofLp`

```lean
lemma lipschitzWith_ofLp [∀ i, PseudoEMetricSpace (β i)] :
    LipschitzWith 1 (@ofLp p (∀ i, β i))
```

9. `LE.le`

```lean
le : α → α → Prop
```

10. `pseudoEMetricSpacePi`

```lean
instance pseudoEMetricSpacePi [∀ b, PseudoEMetricSpace (X b)] : PseudoEMetricSpace (∀ b, X b)
```

11. `One.toOfNat1`

```lean
instance (priority := 300) One.toOfNat1 {α} [One α] : OfNat α (nat_lit 1)
```

12. `WithLp.ofLp_toLp`

```lean
lemma ofLp_toLp (x : V) : ofLp (toLp p x) = x
```

13. `WithLp`

```lean
structure WithLp (p : ℝ≥0∞) (V : Type*)
```

14. `Fact`

```lean
class Fact (p : Prop) : Prop
```

15. `OfNat.ofNat`

```lean
ofNat : α
```

16. `LipschitzWith.to_rightInverse`

```lean
theorem LipschitzWith.to_rightInverse [PseudoEMetricSpace α] [PseudoEMetricSpace β] {K : ℝ≥0}
    {f : α → β} (hf : LipschitzWith K f) {g : β → α} (hg : Function.RightInverse g f) :
    AntilipschitzWith K g
```

17. `ENNReal`

```lean
def ENNReal
```

18. `Fintype`

```lean
class Fintype (α : Type*)
```


---

## t034

Target: `FiniteField.Extension.frob`

```lean
noncomputable def Extension.frob :
    Gal(Extension k p n / k)
```

Proof / construction:

```lean
:=
  haveI := Fintype.ofFinite k
  FiniteField.frobeniusAlgEquivOfAlgebraic _ _
```

Candidates (18), random order:

1. `Nat`

```lean
inductive Nat
```

2. `Fact`

```lean
class Fact (p : Prop) : Prop
```

3. `Nat.instMulZeroClass`

```lean
instance instMulZeroClass : MulZeroClass ℕ
```

4. `FiniteField.instFieldExtension`

```lean
FiniteField.instFieldExtension
```

5. `FiniteField.Extension`

```lean
def Extension : Type
```

6. `Finite`

```lean
class inductive Finite (α : Sort*) : Prop
  | intro {n : ℕ} : α ≃ Fin n → Finite _
```

7. `NeZero`

```lean
class NeZero (n : R) : Prop
```

8. `AddGroupWithOne.toAddMonoidWithOne`

```lean
class AddGroupWithOne (R : Type u) extends IntCast R, AddMonoidWithOne R, AddGroup R
```

9. `Field`

```lean
class Field (K : Type u) extends CommRing K, DivisionRing K
```

10. `Field.toDivisionRing`

```lean
class Field (K : Type u) extends CommRing K, DivisionRing K
```

11. `Nat.Prime`

```lean
def Prime (p : ℕ)
```

12. `DivisionRing.toRing`

```lean
class DivisionRing (K : Type*)
  extends Ring K, DivInvMonoid K, Nontrivial K, NNRatCast K, RatCast K
```

13. `FiniteField.instAlgebraExtension`

```lean
noncomputable instance : Algebra k (Extension k p n)
```

14. `MulZeroClass.toZero`

```lean
class MulZeroClass (M₀ : Type u) extends Mul M₀, Zero M₀
```

15. `CharP`

```lean
class _root_.CharP (R : Type*) [AddMonoidWithOne R] (p : outParam ℕ) : Prop
```

16. `Ring.toAddGroupWithOne`

```lean
class Ring (R : Type u) extends Semiring R, AddCommGroup R, AddGroupWithOne R
```

17. `FiniteField.frobeniusAlgEquivOfAlgebraic`

```lean
@[simps!] noncomputable def frobeniusAlgEquivOfAlgebraic [Algebra.IsAlgebraic K L] : Gal(L/K)
```

18. `Fintype.ofFinite`

```lean
noncomputable def Fintype.ofFinite (α : Type*) [Finite α] : Fintype α
```


---

## t035

Target: `CategoryTheory.Abelian.FreydMitchell.EmbeddingRing`

```lean
def EmbeddingRing : Type (max u v)
```

Proof / construction:

```lean
:=
  IsGrothendieckAbelian.OppositeModuleEmbedding.EmbeddingRing
    (Ind.yoneda (C := (AsSmall.{max u v} C)ᵒᵖ)).rightOp
```

Candidates (14), random order:

1. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

2. `CategoryTheory.instCategoryInd`

```lean
CategoryTheory.instCategoryInd
```

3. `CategoryTheory.AsSmall.abelian`

```lean
noncomputable instance abelian [Abelian C] :
    Abelian (AsSmall.{w} C)
```

4. `CategoryTheory.instAbelianInd`

```lean
noncomputable instance : Abelian (Ind C)
```

5. `CategoryTheory.AsSmall`

```lean
CategoryTheory.AsSmall
```

6. `Opposite`

```lean
structure Opposite
```

7. `CategoryTheory.Abelian.IsGrothendieckAbelian.OppositeModuleEmbedding.EmbeddingRing`

```lean
def EmbeddingRing : Type v
```

8. `CategoryTheory.Ind`

```lean
def Ind : Type (max u (v + 1))
```

9. `CategoryTheory.instSmallCategoryAsSmall`

```lean
instance : SmallCategory (AsSmall.{w₁} C)
```

10. `CategoryTheory.Abelian`

```lean
class Abelian extends Preadditive C, IsNormalMonoCategory C, IsNormalEpiCategory C
```

11. `CategoryTheory.Ind.yoneda`

```lean
protected noncomputable def Ind.yoneda : C ⥤ Ind C
```

12. `CategoryTheory.Functor.rightOp`

```lean
protected def rightOp (F : Cᵒᵖ ⥤ D) : C ⥤ Dᵒᵖ
```

13. `CategoryTheory.Category.opposite`

```lean
instance Category.opposite : Category.{v₁} Cᵒᵖ
```

14. `CategoryTheory.instAbelianOpposite`

```lean
instance : Abelian Cᵒᵖ
```


---

## t036

Target: `AddSubsemigroup.mem_op`

```lean
theorem mem_op {x : Mᵐᵒᵖ} {S : Subsemigroup M} : x ∈ S.op ↔ x.unop ∈ S
```

Proof / construction:

```lean
:= Iff.rfl
```

Candidates (9), random order:

1. `Iff.rfl`

```lean
protected theorem Iff.rfl {a : Prop} : a ↔ a
```

2. `AddOpposite.instAdd`

```lean
instance instAdd [Add α] : Add αᵐᵒᵖ
```

3. `AddSubsemigroup.op`

```lean
protected def op (x : Subsemigroup M) : Subsemigroup Mᵐᵒᵖ
```

4. `AddSubsemigroup`

```lean
structure AddSubsemigroup (M : Type*) [Add M]
```

5. `Membership.mem`

```lean
mem : γ → α → Prop
```

6. `AddOpposite`

```lean
-- Mathlib generates `AddOpposite` from the declaration below.
def MulOpposite (α : Type*) : Type _
```

7. `AddSubsemigroup.instSetLike`

```lean
instance : SetLike (Subsemigroup M) M
```

8. `Add`

```lean
class Add (α : Type u)
```

9. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```


---

## t037

Target: `Fin.map_valEmbedding_Ioc`

```lean
theorem map_valEmbedding_Ioc : (Ioc a b).map Fin.valEmbedding = Ioc (a : ℕ) b
```

Proof / construction:

```lean
:=
  map_valEmbedding_attachFin _
```

Candidates (8), random order:

1. `Finset.map_valEmbedding_attachFin`

```lean
lemma map_valEmbedding_attachFin {s : Finset ℕ} (h : ∀ m ∈ s, m < n) :
    map Fin.valEmbedding (s.attachFin h) = s
```

2. `Fin.instLocallyFiniteOrder`

```lean
instance instLocallyFiniteOrder (n : ℕ) : LocallyFiniteOrder (Fin n)
```

3. `Finset.Ioc`

```lean
def Ioc (a b : α) : Finset α
```

4. `Fin`

```lean
structure Fin (n : Nat)
```

5. `Nat`

```lean
inductive Nat
```

6. `Nat.instLocallyFiniteOrder`

```lean
instance instLocallyFiniteOrder : LocallyFiniteOrder ℕ
```

7. `Fin.val`

```lean
val  : Nat
```

8. `Nat.instPreorder`

```lean
instance : Preorder ℕ
```


---

## t038

Target: `LinearIsometryEquiv.Simps.symm_apply`

```lean
def Simps.symm_apply (σ₁₂ : R →+* R₂) {σ₂₁ : R₂ →+* R} [RingHomInvPair σ₁₂ σ₂₁]
    [RingHomInvPair σ₂₁ σ₁₂] (E E₂ : Type*) [SeminormedAddCommGroup E] [SeminormedAddCommGroup E₂]
    [Module R E] [Module R₂ E₂] (h : E ≃ₛₗᵢ[σ₁₂] E₂) : E₂ → E
```

Proof / construction:

```lean
:=
  h.symm
```

Candidates (13), random order:

1. `LinearIsometryEquiv.symm`

```lean
def symm : E₂ ≃ₛₗᵢ[σ₂₁] E
```

2. `LinearIsometryEquiv.instEquivLike`

```lean
instance instEquivLike : EquivLike (E ≃ₛₗᵢ[σ₁₂] E₂) E E₂
```

3. `RingHom`

```lean
structure RingHom (α : Type*) (β : Type*) [NonAssocSemiring α] [NonAssocSemiring β] extends
  α →* β, α →+ β, α →ₙ+* β, α →*₀ β
```

4. `Module`

```lean
class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
  DistribMulAction R M
```

5. `RingHomInvPair`

```lean
class RingHomInvPair (σ : R₁ →+* R₂) (σ' : outParam (R₂ →+* R₁)) : Prop
```

6. `Semiring.toNonAssocSemiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

7. `AddCommGroup.toAddCommMonoid`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```

8. `Semiring`

```lean
class Semiring (α : Type u) extends AddCommMonoid α, MonoidWithZero α, NonUnitalSemiring α,
  NonAssocSemiring α
```

9. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

10. `EquivLike.toFunLike`

```lean
instance (priority := 100) toFunLike : FunLike E α β
```

11. `SeminormedAddCommGroup.toAddCommGroup`

```lean
class SeminormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E,
  PseudoMetricSpace E
```

12. `LinearIsometryEquiv`

```lean
structure LinearIsometryEquiv (σ₁₂ : R →+* R₂) {σ₂₁ : R₂ →+* R} [RingHomInvPair σ₁₂ σ₂₁]
  [RingHomInvPair σ₂₁ σ₁₂] (E E₂ : Type*) [SeminormedAddCommGroup E] [SeminormedAddCommGroup E₂]
  [Module R E] [Module R₂ E₂] extends E ≃ₛₗ[σ₁₂] E₂
```

13. `SeminormedAddCommGroup`

```lean
class SeminormedAddCommGroup (E : Type*) extends Norm E, AddCommGroup E,
  PseudoMetricSpace E
```


---

## t039

Target: `Metric.toUniformSpace_eq`

```lean
theorem toUniformSpace_eq :
    ‹PseudoMetricSpace α›.toUniformSpace = .ofDist dist dist_self dist_comm dist_triangle
```

Proof / construction:

```lean
:=
  UniformSpace.ext PseudoMetricSpace.uniformity_dist
```

Candidates (10), random order:

1. `dist_comm`

```lean
theorem dist_comm (x y : α) : dist x y = dist y x
```

2. `Dist.dist`

```lean
dist : α → α → ℝ
```

3. `PseudoMetricSpace.toDist`

```lean
class PseudoMetricSpace (α : Type u) : Type u extends Dist α
```

4. `UniformSpace.ofDist`

```lean
def UniformSpace.ofDist (dist : α → α → ℝ) (dist_self : ∀ x : α, dist x x = 0)
    (dist_comm : ∀ x y : α, dist x y = dist y x)
    (dist_triangle : ∀ x y z : α, dist x z ≤ dist x y + dist y z) : UniformSpace α
```

5. `dist_triangle`

```lean
theorem dist_triangle (x y z : α) : dist x z ≤ dist x y + dist y z
```

6. `dist_self`

```lean
theorem dist_self (x : α) : dist x x = 0
```

7. `PseudoMetricSpace.uniformity_dist`

```lean
uniformity_dist : 𝓤 α = ⨅ ε > 0, 𝓟 { p : α × α | dist p.1 p.2 < ε }
```

8. `PseudoMetricSpace.toUniformSpace`

```lean
toUniformSpace : UniformSpace α
```

9. `PseudoMetricSpace`

```lean
class PseudoMetricSpace (α : Type u) : Type u extends Dist α
```

10. `UniformSpace.ext`

```lean
protected theorem UniformSpace.ext {u₁ u₂ : UniformSpace α} (h : 𝓤[u₁] = 𝓤[u₂]) : u₁ = u₂
```


---

## t040

Target: `CompleteSublattice.coe_sInf`

```lean
@[simp] theorem coe_sInf (S : Set L) : (↑(sInf S) : α) = sInf {(s : α) | s ∈ S}
```

Proof / construction:

```lean
:= rfl
```

Candidates (11), random order:

1. `CompleteSublattice`

```lean
structure CompleteSublattice extends Sublattice α
```

2. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

3. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

4. `InfSet.sInf`

```lean
sInf : Set α → α
```

5. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

6. `CompleteLattice`

```lean
class CompleteLattice (α : Type*) extends Lattice α, CompleteSemilatticeSup α,
    CompleteSemilatticeInf α, BoundedOrder α
```

7. `CompleteSublattice.instInfSet`

```lean
instance instInfSet : InfSet L
```

8. `CompleteSublattice.instSetLike`

```lean
instance instSetLike : SetLike (CompleteSublattice α) α
```

9. `Membership.mem`

```lean
mem : γ → α → Prop
```

10. `Set`

```lean
def Set (α : Type u)
```

11. `Subtype.val`

```lean
val : α
```


---
