# Blind grading batch 06 — 10 items

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
{"t051": {"1": 2, "2": 4, "3": 0}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---


## t051

Target: `OpenPartialHomeomorph.isOpen_image_iff_of_subset_source`

```lean
theorem isOpen_image_iff_of_subset_source {s : Set X} (hs : s ⊆ e.source) :
    IsOpen (e '' s) ↔ IsOpen s
```

Proof / construction:

```lean
:= by
  rw [← e.symm.isOpen_symm_image_iff_of_subset_target hs, e.symm_symm]
```

Candidates (22), random order:

1. `OpenPartialHomeomorph.symm`

```lean
protected def symm : OpenPartialHomeomorph Y X
```

2. `Set.instLE`

```lean
instance : LE (Set α)
```

3. `Eq.symm`

```lean
@[symm] theorem Eq.symm {α : Sort u} {a b : α} (h : Eq a b) : Eq b a
```

4. `Set.image`

```lean
def image {β : Type v} (f : α → β) (s : Set α) : Set β
```

5. `LE.le`

```lean
le : α → α → Prop
```

6. `PartialEquiv.source`

```lean
source : Set α
```

7. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

8. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

9. `Iff.rfl`

```lean
protected theorem Iff.rfl {a : Prop} : a ↔ a
```

10. `IsOpen`

```lean
def IsOpen : Set X → Prop
```

11. `propext`

```lean
axiom propext {a b : Prop} : (a ↔ b) → a = b
```

12. `Set`

```lean
def Set (α : Type u)
```

13. `OpenPartialHomeomorph.toFun'`

```lean
@[coe] def toFun' : X → Y
```

14. `OpenPartialHomeomorph`

```lean
structure OpenPartialHomeomorph (X : Type*) (Y : Type*) [TopologicalSpace X]
    [TopologicalSpace Y] extends PartialHomeomorph X Y
```

15. `OpenPartialHomeomorph.symm_symm`

```lean
@[simp, mfld_simps] theorem symm_symm : e.symm.symm = e
```

16. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

17. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

18. `OpenPartialHomeomorph.isOpen_symm_image_iff_of_subset_target`

```lean
lemma isOpen_symm_image_iff_of_subset_target {t : Set Y} (hs : t ⊆ e.target) :
    IsOpen (e.symm '' t) ↔ IsOpen t
```

19. `PartialHomeomorph.toPartialEquiv`

```lean
structure PartialHomeomorph (X : Type*) (Y : Type*) [TopologicalSpace X]
    [TopologicalSpace Y] extends PartialEquiv X Y
```

20. `Eq`

```lean
inductive Eq : α → α → Prop
```

21. `Iff`

```lean
structure Iff (a b : Prop) : Prop
```

22. `OpenPartialHomeomorph.toPartialHomeomorph`

```lean
structure OpenPartialHomeomorph (X : Type*) (Y : Type*) [TopologicalSpace X]
    [TopologicalSpace Y] extends PartialHomeomorph X Y
```


---

## t052

Target: `AlgebraicGeometry.Scheme.Hom.normalizationPullback_snd`

```lean
lemma normalizationPullback_snd :
    f.normalizationPullback g ≫ pullback.snd _ _ = (pullback.snd f g).fromNormalization
```

Proof / construction:

```lean
:=
  (pullback.snd f g).normalizationDesc_comp ..
```

Candidates (16), random order:

1. `AlgebraicGeometry.QuasiCompact`

```lean
class QuasiCompact (f : X ⟶ Y) : Prop
```

2. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

3. `AlgebraicGeometry.Scheme`

```lean
structure Scheme extends LocallyRingedSpace
```

4. `CategoryTheory.CategoryStruct.id`

```lean
id : ∀ X : obj, Hom X X
```

5. `AlgebraicGeometry.Scheme.Hom.normalizationDesc_comp`

```lean
lemma normalizationDesc_comp (H : f = f₁ ≫ f₂) :
    f.normalizationDesc f₁ f₂ H ≫ f₂ = f.fromNormalization
```

6. `AlgebraicGeometry.Scheme.instCategory`

```lean
instance : Category Scheme
```

7. `CategoryTheory.Limits.pullback.snd`

```lean
abbrev pullback.snd {X Y Z : C} (f : X ⟶ Z) (g : Y ⟶ Z) [HasPullback f g] : pullback f g ⟶ Y
```

8. `CategoryTheory.Limits.pullback`

```lean
abbrev pullback {X Y Z : C} (f : X ⟶ Z) (g : Y ⟶ Z) [HasPullback f g]
```

9. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

10. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

11. `AlgebraicGeometry.Scheme.Hom.fromNormalization`

```lean
def fromNormalization : f.normalization ⟶ Y
```

12. `AlgebraicGeometry.Scheme.Hom.normalizationPullback`

```lean
noncomputable def normalizationPullback :
    (pullback.snd f g).normalization ⟶ pullback f.fromNormalization g
```

13. `CategoryTheory.Limits.pullback.map`

```lean
abbrev pullback.map {W X Y Z S T : C} (f₁ : W ⟶ S) (f₂ : X ⟶ S) [HasPullback f₁ f₂] (g₁ : Y ⟶ T)
    (g₂ : Z ⟶ T) [HasPullback g₁ g₂] (i₁ : W ⟶ Y) (i₂ : X ⟶ Z) (i₃ : S ⟶ T)
    (eq₁ : f₁ ≫ i₃ = i₁ ≫ g₁) (eq₂ : f₂ ≫ i₃ = i₂ ≫ g₂) : pullback f₁ f₂ ⟶ pullback g₁ g₂
```

14. `AlgebraicGeometry.QuasiSeparated`

```lean
class QuasiSeparated (f : X ⟶ Y) : Prop
```

15. `AlgebraicGeometry.Scheme.Hom.normalization`

```lean
def normalization : Scheme
```

16. `AlgebraicGeometry.Scheme.Hom.toNormalization`

```lean
def toNormalization : X ⟶ f.normalization
```


---

## t053

Target: `Submonoid.topEquiv`

```lean
def topEquiv : (⊤ : Submonoid M) ≃* M
```

Proof / construction:

```lean
where
  toFun x := x
  invFun x := ⟨x, mem_top x⟩
  left_inv x := x.eta _
  map_mul' _ _ := rfl
```

Candidates (16), random order:

1. `Membership.mem`

```lean
mem : γ → α → Prop
```

2. `Submonoid`

```lean
structure Submonoid (M : Type*) [MulOneClass M] extends Subsemigroup M
```

3. `Submonoid.instSetLike`

```lean
instance : SetLike (Submonoid M) M
```

4. `Top.top`

```lean
top : α
```

5. `MulOne.toMul`

```lean
class MulOne (M : Type*) extends One M, Mul M
```

6. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

7. `Submonoid.instTop`

```lean
instance : Top (Submonoid M)
```

8. `MulEquiv.mk`

```lean
structure MulEquiv (M N : Type*) [Mul M] [Mul N] extends M ≃ N, M →ₙ* N
```

9. `Submonoid.mem_top`

```lean
theorem mem_top (x : M) : x ∈ (⊤ : Submonoid M)
```

10. `Submonoid.mul`

```lean
instance mul : Mul S
```

11. `Subtype.mk`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

12. `Subtype.val`

```lean
val : α
```

13. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

14. `MulOneClass.toMulOne`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

15. `MulOneClass`

```lean
class MulOneClass (M : Type u) extends MulOne M
```

16. `Equiv.mk`

```lean
structure Equiv (α β : Sort*)
```


---

## t054

Target: `tsub_eq_of_eq_add_rev`

```lean
theorem tsub_eq_of_eq_add_rev (h : a = b + c) : a - b = c
```

Proof / construction:

```lean
:=
  Contravariant.AddLECancellable.tsub_eq_of_eq_add_rev h
```

Candidates (14), random order:

1. `Preorder.toLE`

```lean
class Preorder (α : Type*) extends LE α, LT α
```

2. `Eq`

```lean
inductive Eq : α → α → Prop
```

3. `Contravariant.AddLECancellable`

```lean
-- Mathlib generates `Contravariant.AddLECancellable` from the declaration below.
theorem Contravariant.MulLECancellable [Mul α] [LE α] [MulLeftReflectLE α]
    {a : α} :
    MulLECancellable a
```

4. `AddCommSemigroup.toAddCommMagma`

```lean
class AddCommSemigroup (G : Type u) extends AddSemigroup G, AddCommMagma G
```

5. `PartialOrder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

6. `OrderedSub`

```lean
class OrderedSub (α : Type*) [LE α] [Add α] [Sub α] : Prop
```

7. `AddLeftReflectLE`

```lean
class AddLeftReflectLE [Add M] [LE M] : Prop
```

8. `AddCommMagma.toAdd`

```lean
class AddCommMagma (G : Type u) extends Add G
```

9. `AddLECancellable.tsub_eq_of_eq_add_rev`

```lean
protected theorem tsub_eq_of_eq_add_rev (hb : AddLECancellable b) (h : a = b + c) : a - b = c
```

10. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```

11. `HAdd.hAdd`

```lean
hAdd : α → β → γ
```

12. `Sub`

```lean
class Sub (α : Type u)
```

13. `AddCommSemigroup`

```lean
class AddCommSemigroup (G : Type u) extends AddSemigroup G, AddCommMagma G
```

14. `instHAdd`

```lean
instance instHAdd [Add α] : HAdd α α α
```


---

## t055

Target: `CategoryTheory.Arrow.leftHomotopic`

```lean
def leftHomotopic : HomRel (Arrow V)
```

Proof / construction:

```lean
:= fun _ _ f g => Nonempty (LeftHomotopy f g)
```

Candidates (7), random order:

1. `CategoryTheory.Preadditive`

```lean
class Preadditive
```

2. `CategoryTheory.Arrow`

```lean
def Arrow
```

3. `CategoryTheory.instQuiverArrow`

```lean
instance : Quiver (Arrow T)
```

4. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

5. `CategoryTheory.Arrow.LeftHomotopy`

```lean
structure LeftHomotopy
```

6. `Nonempty`

```lean
class inductive Nonempty (α : Sort u) : Prop
```

7. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```


---

## t056

Target: `Nat.coprime_add_mul_right_left`

```lean
theorem coprime_add_mul_right_left (m n k : ℕ) : Coprime (m + k * n) n ↔ Coprime m n
```

Proof / construction:

```lean
:= by
  rw [Coprime, Coprime, gcd_add_mul_right_left]
```

Candidates (18), random order:

1. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

2. `Eq`

```lean
inductive Eq : α → α → Prop
```

3. `instOfNatNat`

```lean
instance instOfNatNat (n : Nat) : OfNat Nat n
```

4. `Nat.Coprime`

```lean
@[reducible, expose] def Coprime (m n : Nat) : Prop
```

5. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

6. `instAddNat`

```lean
instance instAddNat : Add Nat
```

7. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

8. `Iff`

```lean
structure Iff (a b : Prop) : Prop
```

9. `instMulNat`

```lean
instance instMulNat : Mul Nat
```

10. `instHAdd`

```lean
instance instHAdd [Add α] : HAdd α α α
```

11. `HMul.hMul`

```lean
hMul : α → β → γ
```

12. `Nat.gcd_add_mul_right_left`

```lean
@[simp] theorem gcd_add_mul_right_left (m n k : Nat) : gcd (n + k * m) m = gcd n m
```

13. `HAdd.hAdd`

```lean
hAdd : α → β → γ
```

14. `Nat.gcd`

```lean
def gcd (m n : @& Nat) : Nat
```

15. `Iff.rfl`

```lean
protected theorem Iff.rfl {a : Prop} : a ↔ a
```

16. `OfNat.ofNat`

```lean
ofNat : α
```

17. `Nat`

```lean
inductive Nat
```

18. `instHMul`

```lean
instance instHMul [Mul α] : HMul α α α
```


---

## t057

Target: `NonUnitalRingHom.coe_srangeRestrict`

```lean
theorem coe_srangeRestrict (f : F) (x : R) : (srangeRestrict f x : S) = f x
```

Proof / construction:

```lean
:=
  rfl
```

Candidates (16), random order:

1. `NonUnitalNonAssocSemiring`

```lean
class NonUnitalNonAssocSemiring (α : Type u) extends AddCommMonoid α, Distrib α, MulZeroClass α
```

2. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

3. `Subtype.val`

```lean
val : α
```

4. `NonUnitalRingHom.instFunLike`

```lean
instance instFunLike : FunLike (α →+* β) α β
```

5. `SetLike.instMembership`

```lean
instance (priority := 100) instMembership : Membership B A
```

6. `Membership.mem`

```lean
mem : γ → α → Prop
```

7. `FunLike`

```lean
abbrev FunLike F α β
```

8. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

9. `NonUnitalRingHom.srange`

```lean
def srange : NonUnitalSubsemiring S
```

10. `NonUnitalRingHom.srangeRestrict`

```lean
def srangeRestrict (f : F) : R →ₙ+* (srange f : NonUnitalSubsemiring S)
```

11. `NonUnitalSubsemiringClass.toNonUnitalNonAssocSemiring`

```lean
instance (priority := 75) toNonUnitalNonAssocSemiring :
    NonUnitalNonAssocSemiring s
```

12. `NonUnitalRingHomClass`

```lean
class NonUnitalRingHomClass (F : Type*) (α β : outParam Type*) [NonUnitalNonAssocSemiring α]
  [NonUnitalNonAssocSemiring β] [FunLike F α β] : Prop
  extends MulHomClass F α β, AddMonoidHomClass F α β
```

13. `NonUnitalSubsemiring`

```lean
structure NonUnitalSubsemiring (R : Type u) [NonUnitalNonAssocSemiring R] extends AddSubmonoid R,
  Subsemigroup R
```

14. `Subtype`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

15. `NonUnitalSubsemiring.instSetLike`

```lean
instance : SetLike (NonUnitalSubsemiring R) R
```

16. `NonUnitalRingHom`

```lean
structure NonUnitalRingHom (α β : Type*) [NonUnitalNonAssocSemiring α]
  [NonUnitalNonAssocSemiring β] extends α →ₙ* β, α →+ β
```


---

## t058

Target: `NonUnitalRingHom.coe_snd`

```lean
theorem coe_snd : ⇑(snd R S) = Prod.snd
```

Proof / construction:

```lean
:=
  rfl
```

Candidates (8), random order:

1. `Prod`

```lean
structure Prod (α : Type u) (β : Type v)
```

2. `Prod.instNonUnitalNonAssocSemiring`

```lean
instance instNonUnitalNonAssocSemiring [NonUnitalNonAssocSemiring R] [NonUnitalNonAssocSemiring S] :
    NonUnitalNonAssocSemiring (R × S)
```

3. `NonUnitalNonAssocSemiring`

```lean
class NonUnitalNonAssocSemiring (α : Type u) extends AddCommMonoid α, Distrib α, MulZeroClass α
```

4. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

5. `NonUnitalRingHom.snd`

```lean
def snd : R × S →ₙ+* S
```

6. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

7. `NonUnitalRingHom.instFunLike`

```lean
instance instFunLike : FunLike (α →+* β) α β
```

8. `NonUnitalRingHom`

```lean
structure NonUnitalRingHom (α β : Type*) [NonUnitalNonAssocSemiring α]
  [NonUnitalNonAssocSemiring β] extends α →ₙ* β, α →+ β
```


---

## t059

Target: `AlgebraicGeometry.PresheafedSpace.IsOpenImmersion.toLocallyRingedSpace_toSheafedSpace`

```lean
theorem toLocallyRingedSpace_toSheafedSpace :
    (toLocallyRingedSpace Y f).toSheafedSpace = toSheafedSpace Y.1 f
```

Proof / construction:

```lean
:=
  rfl
```

Candidates (14), random order:

1. `CommRingCat`

```lean
structure CommRingCat
```

2. `AlgebraicGeometry.SheafedSpace.toPresheafedSpace`

```lean
structure SheafedSpace extends PresheafedSpace C
```

3. `AlgebraicGeometry.LocallyRingedSpace`

```lean
structure LocallyRingedSpace extends SheafedSpace CommRingCat.{u}
```

4. `AlgebraicGeometry.PresheafedSpace.categoryOfPresheafedSpaces`

```lean
instance categoryOfPresheafedSpaces : Category (PresheafedSpace C)
```

5. `AlgebraicGeometry.LocallyRingedSpace.toSheafedSpace`

```lean
structure LocallyRingedSpace extends SheafedSpace CommRingCat.{u}
```

6. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

7. `AlgebraicGeometry.PresheafedSpace.IsOpenImmersion.toLocallyRingedSpace`

```lean
def toLocallyRingedSpace : LocallyRingedSpace
```

8. `CommRingCat.instCategory`

```lean
instance : Category CommRingCat
```

9. `AlgebraicGeometry.SheafedSpace`

```lean
structure SheafedSpace extends PresheafedSpace C
```

10. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

11. `AlgebraicGeometry.PresheafedSpace.IsOpenImmersion`

```lean
class PresheafedSpace.IsOpenImmersion {X Y : PresheafedSpace C} (f : X ⟶ Y) : Prop
```

12. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```

13. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

14. `AlgebraicGeometry.PresheafedSpace`

```lean
AlgebraicGeometry.PresheafedSpace
```


---

## t060

Target: `MulArchimedeanClass.mk_out`

```lean
theorem mk_out (A : MulArchimedeanClass M) : mk A.out = A
```

Proof / construction:

```lean
:= Quotient.out_eq' A
```

Candidates (16), random order:

1. `LinearOrder`

```lean
class LinearOrder (α : Type*) extends PartialOrder α, Min α, Max α, Ord α
```

2. `CommGroup`

```lean
class CommGroup (G : Type u) extends Group G, CommMonoid G
```

3. `Quotient.out_eq'`

```lean
theorem out_eq' (q : Quotient s₁) : Quotient.mk'' q.out = q
```

4. `IsOrderedMonoid`

```lean
class IsOrderedMonoid (α : Type*) [CommMonoid α] [Preorder α]
```

5. `AntisymmRel.setoid`

```lean
def AntisymmRel.setoid : Setoid α
```

6. `MulArchimedeanOrder.instLE`

```lean
instance : LE (MulArchimedeanOrder M)
```

7. `SemilatticeInf.toPartialOrder`

```lean
class SemilatticeInf (α : Type u) extends PartialOrder α
```

8. `instDistribLatticeOfLinearOrder`

```lean
instDistribLatticeOfLinearOrder
```

9. `CommGroup.toCommMonoid`

```lean
class CommGroup (G : Type u) extends Group G, CommMonoid G
```

10. `MulArchimedeanOrder`

```lean
def MulArchimedeanOrder
```

11. `CommGroup.toGroup`

```lean
class CommGroup (G : Type u) extends Group G, CommMonoid G
```

12. `MulArchimedeanClass`

```lean
def MulArchimedeanClass
```

13. `DistribLattice.toLattice`

```lean
class DistribLattice (α) extends Lattice α
```

14. `Lattice.toSemilatticeInf`

```lean
class Lattice (α : Type u) extends SemilatticeSup α, SemilatticeInf α
```

15. `LE.le`

```lean
le : α → α → Prop
```

16. `PartialOrder.toPreorder`

```lean
class PartialOrder (α : Type*) extends Preorder α
```


---
