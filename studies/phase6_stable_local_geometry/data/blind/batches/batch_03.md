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

Target: `CategoryTheory.ShortComplex.instPreadditive`

```lean
instance : Preadditive (ShortComplex C)
```

Proof / construction:

```lean
where
```

Candidates (12), random order:

1. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

2. `inferInstance`

```lean
abbrev inferInstance {α : Sort u} [i : α] : α
```

3. `CategoryTheory.ShortComplex.instAddCommGroupHom`

```lean
CategoryTheory.ShortComplex.instAddCommGroupHom
```

4. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

5. `CategoryTheory.ShortComplex.instCategory`

```lean
instance : Category (ShortComplex C)
```

6. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

7. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`

```lean
instance (priority := 100) preadditiveHasZeroMorphisms : HasZeroMorphisms C
```

8. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

9. `CategoryTheory.ShortComplex`

```lean
structure ShortComplex
```

10. `CategoryTheory.Preadditive.mk`

```lean
class Preadditive
```

11. `CategoryTheory.Preadditive`

```lean
class Preadditive
```

12. `AddCommGroup`

```lean
class AddCommGroup (G : Type u) extends AddGroup G, AddCommMonoid G
```


---

## t022

Target: `derangements.Equiv.RemoveNone.fiber`

```lean
def RemoveNone.fiber (a : Option α) : Set (Perm α)
```

Proof / construction:

```lean
:=
  { f : Perm α | (a, f) ∈ Equiv.Perm.decomposeOption '' derangements (Option α) }
```

Candidates (16), random order:

1. `Equiv.Perm.decomposeOption`

```lean
def Equiv.Perm.decomposeOption {α : Type*} [DecidableEq α] :
    Perm (Option α) ≃ Option α × Perm α
```

2. `Prod`

```lean
structure Prod (α : Type u) (β : Type v)
```

3. `derangements`

```lean
def derangements (α : Type*) : Set (Perm α)
```

4. `Set.ofPred`

```lean
def Set.ofPred {α : Type u} (p : α → Prop) : Set α
```

5. `Equiv`

```lean
structure Equiv (α β : Sort*)
```

6. `EquivLike.toFunLike`

```lean
instance (priority := 100) toFunLike : FunLike E α β
```

7. `DecidableEq`

```lean
abbrev DecidableEq (α : Sort u)
```

8. `Option`

```lean
inductive Option (α : Type u)
```

9. `DFunLike.coe`

```lean
coe : F → ∀ a : α, β a
```

10. `Membership.mem`

```lean
mem : γ → α → Prop
```

11. `Set.image`

```lean
def image {β : Type v} (f : α → β) (s : Set α) : Set β
```

12. `Equiv.instEquivLike`

```lean
instance : EquivLike (α ≃ β) α β
```

13. `Set.instMembership`

```lean
instance : Membership α (Set α)
```

14. `Set`

```lean
def Set (α : Type u)
```

15. `Prod.mk`

```lean
structure Prod (α : Type u) (β : Type v)
```

16. `Equiv.Perm`

```lean
abbrev Equiv.Perm (α : Sort*)
```


---

## t023

Target: `CategoryTheory.LocalizerMorphism.inv`

```lean
noncomputable def inv : LocalizerMorphism W₂ W₁
```

Proof / construction:

```lean
where
  functor := Φ.functor.inv
  map := by
    simp only [← Φ.inverseImage_eq]
    intro X Y f hf
    exact (W₂.arrow_mk_iso_iff
      (Arrow.isoMk (Φ.functor.asEquivalence.counitIso.app _)
        (Φ.functor.asEquivalence.counitIso.app _))).2 hf
```

Candidates (10), random order:

1. `CategoryTheory.Functor.IsEquivalence`

```lean
class Functor.IsEquivalence (F : C ⥤ D) : Prop
```

2. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

3. `CategoryTheory.LocalizerMorphism`

```lean
structure LocalizerMorphism
```

4. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

5. `CategoryTheory.MorphismProperty.RespectsIso`

```lean
abbrev RespectsIso (P : MorphismProperty C) : Prop
```

6. `CategoryTheory.MorphismProperty`

```lean
def MorphismProperty (C : Type u) [CategoryStruct.{v} C]
```

7. `CategoryTheory.LocalizerMorphism.mk`

```lean
structure LocalizerMorphism
```

8. `CategoryTheory.Functor.inv`

```lean
noncomputable def inv (F : C ⥤ D) [F.IsEquivalence] : D ⥤ C
```

9. `CategoryTheory.LocalizerMorphism.functor`

```lean
functor : C₁ ⥤ C₂
```

10. `CategoryTheory.LocalizerMorphism.IsInduced`

```lean
class IsInduced (Φ : LocalizerMorphism W₁ W₂) : Prop
```


---

## t024

Target: `List.rtakeWhile_concat_pos`

```lean
theorem rtakeWhile_concat_pos (x : α) (h : p x) :
    rtakeWhile p (l ++ [x]) = rtakeWhile p l ++ [x]
```

Proof / construction:

```lean
:= by rw [rtakeWhile_concat, if_pos h]
```

Candidates (18), random order:

1. `instHAppendOfAppend`

```lean
instance [Append α] : HAppend α α α
```

2. `Bool.true`

```lean
| true : Bool
```

3. `if_pos`

```lean
theorem if_pos {c : Prop} {h : Decidable c} (hc : c) {α : Sort u} {t e : α} : (ite c t e) = t
```

4. `instDecidableEqBool`

```lean
instDecidableEqBool
```

5. `Eq`

```lean
inductive Eq : α → α → Prop
```

6. `id`

```lean
@[inline, implicit_reducible] def id {α : Sort u} (a : α) : α
```

7. `List.instAppend`

```lean
instance : Append (List α)
```

8. `List.nil`

```lean
| nil : List α
```

9. `congrArg`

```lean
theorem congrArg {α : Sort u} {β : Sort v} {a₁ a₂ : α} (f : α → β) (h : Eq a₁ a₂) : Eq (f a₁) (f a₂)
```

10. `Eq.refl`

```lean
| refl (a : α) : Eq a a
```

11. `Eq.mpr`

```lean
@[macro_inline] def Eq.mpr {α β : Sort u} (h : α = β) (b : β) : α
```

12. `List`

```lean
inductive List (α : Type u)
```

13. `List.cons`

```lean
| cons (head : α) (tail : List α) : List α
```

14. `List.rtakeWhile_concat`

```lean
theorem rtakeWhile_concat (x : α) :
    rtakeWhile p (l ++ [x]) = if p x then rtakeWhile p l ++ [x] else []
```

15. `Bool`

```lean
inductive Bool : Type
```

16. `ite`

```lean
def ite {α : Sort u} (c : Prop) [h : Decidable c] (t e : α) : α
```

17. `List.rtakeWhile`

```lean
def rtakeWhile : List α
```

18. `HAppend.hAppend`

```lean
hAppend : α → β → γ
```


---

## t025

Target: `legendreSym.eq_one_iff`

```lean
theorem eq_one_iff {a : ℤ} (ha0 : (a : ZMod p) ≠ 0) : legendreSym p a = 1 ↔ IsSquare (a : ZMod p)
```

Proof / construction:

```lean
:=
  quadraticChar_one_iff_isSquare ha0
```

Candidates (22), random order:

1. `Fact`

```lean
class Fact (p : Prop) : Prop
```

2. `Int.cast`

```lean
protected def Int.cast {R : Type u} [IntCast R] : Int → R
```

3. `ZMod.fintype`

```lean
instance fintype : ∀ (n : ℕ) [NeZero n], Fintype (ZMod n)
  | 0, h => (h.ne _ rfl).elim
  | n + 1, _ => Fin.fintype (n + 1)
```

4. `ZMod.decidableEq`

```lean
instance ZMod.decidableEq : ∀ n : ℕ, DecidableEq (ZMod n)
  | 0 => inferInstanceAs <| DecidableEq ℤ
  | n + 1 => inferInstanceAs <| DecidableEq (Fin (n + 1))
```

5. `Ring.toAddGroupWithOne`

```lean
class Ring (R : Type u) extends Semiring R, AddCommGroup R, AddGroupWithOne R
```

6. `Nat.Prime`

```lean
def Prime (p : ℕ)
```

7. `quadraticChar_one_iff_isSquare`

```lean
theorem quadraticChar_one_iff_isSquare {a : F} (ha : a ≠ 0) :
    quadraticChar F a = 1 ↔ IsSquare a
```

8. `Semifield.toDivisionSemiring`

```lean
class Semifield (K : Type*) extends CommSemiring K, DivisionSemiring K, CommGroupWithZero K
```

9. `Field.toDivisionRing`

```lean
class Field (K : Type u) extends CommRing K, DivisionRing K
```

10. `OfNat.ofNat`

```lean
ofNat : α
```

11. `ZMod.instField`

```lean
instance : Field (ZMod p)
```

12. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

13. `ZMod`

```lean
def ZMod : ℕ → Type
  | 0 => ℤ
  | n + 1 => Fin (n + 1)
```

14. `instMulZeroClassOfSemiring`

```lean
instance [Semiring α] : MulZeroClass α
```

15. `DivisionSemiring.toSemiring`

```lean
class DivisionSemiring (K : Type*) extends Semiring K, GroupWithZero K, NNRatCast K
```

16. `Nat`

```lean
inductive Nat
```

17. `Field.toSemifield`

```lean
instance (priority := 100) Field.toSemifield [Field K] : Semifield K
```

18. `Zero.toOfNat0`

```lean
instance (priority := 300) Zero.toOfNat0 {α} [Zero α] : OfNat α (nat_lit 0)
```

19. `Int`

```lean
inductive Int : Type
```

20. `AddGroupWithOne.toIntCast`

```lean
class AddGroupWithOne (R : Type u) extends IntCast R, AddMonoidWithOne R, AddGroup R
```

21. `DivisionRing.toRing`

```lean
class DivisionRing (K : Type*)
  extends Ring K, DivInvMonoid K, Nontrivial K, NNRatCast K, RatCast K
```

22. `MulZeroClass.toZero`

```lean
class MulZeroClass (M₀ : Type u) extends Mul M₀, Zero M₀
```


---

## t026

Target: `partialFunEquivPointed`

```lean
noncomputable def partialFunEquivPointed : PartialFun.{u} ≌ Pointed
```

Proof / construction:

```lean
where
  functor := partialFunToPointed
  inverse := pointedToPartialFun
  unitIso := NatIso.ofComponents (fun X => PartialFun.Iso.mk
      { toFun := fun a => ⟨some a, some_ne_none a⟩
        invFun := fun a => Option.get _ (Option.ne_none_iff_isSome.1 a.2)
        left_inv := fun _ => Option.get_some _ _
        right_inv := fun a => by simp only [some_get, Subtype.coe_eta] })
      fun f =>
        PFun.ext fun a b => by
          dsimp [PartialFun.Iso.mk, CategoryStruct.comp, pointedToPartialFun]
          rw [Part.bind_some]
          refine (Part.mem_bind_iff.trans ?_).trans PFun.mem_toSubtype_iff.symm
          obtain ⟨b | b, hb⟩ := b
          · exact (hb rfl).elim
          · simp only [ne_eq, Part.mem_some_iff]
            classical
            refine ⟨fun ⟨w, hw, h⟩ ↦ ?_, fun h ↦ ⟨b, Part.mem_toOption.mp h.symm, rfl⟩⟩
            rw [Subtype.ext_iff] at h
            dsimp at h
            rw [h]
            rw [← Part.mem_toOption, mem_def] at hw
            exact hw.symm
  counitIso :=
    NatIso.ofComponents
      (fun X ↦ Pointed.Iso.mk (by classical exact Equiv.optionSubtypeNe X.point) rfl)
      fun {X Y} f ↦ Pointed.Hom.ext <| funext fun a ↦ by
        obtain _ | ⟨a, ha⟩ := a
        · exact f.map_point.symm
        simp_all [Equiv.optionSubtypeNe, Equiv.optionSubtype,
          Option.casesOn'_eq_elim, Part.elim_toOption]
  functor_unitIso_comp X := by
    ext (_ | x)
    · rfl
    · simp
      rfl
```

Candidates (24), random order:

1. `Equiv.mk`

```lean
structure Equiv (α β : Sort*)
```

2. `CategoryTheory.Functor.obj`

```lean
obj : C → D
```

3. `Pointed.largeCategory`

```lean
instance largeCategory : LargeCategory Pointed
```

4. `Pointed.point`

```lean
point : X
```

5. `Pointed.Iso.mk`

```lean
def Iso.mk {α β : Pointed} (e : α ≃ β) (he : e α.point = β.point) : α ≅ β
```

6. `PartialFun.largeCategory`

```lean
instance largeCategory : LargeCategory.{u} PartialFun
```

7. `CategoryTheory.Functor.comp`

```lean
def comp (F : C ⥤ D) (G : D ⥤ E) : C ⥤ E
```

8. `Subtype.val`

```lean
val : α
```

9. `CategoryTheory.NatIso.ofComponents`

```lean
def ofComponents (app : ∀ X : C, F.obj X ≅ G.obj X)
    (naturality : ∀ {X Y : C} (f : X ⟶ Y),
      F.map f ≫ (app Y).hom = (app X).hom ≫ G.map f := by cat_disch) :
    F ≅ G
```

10. `Subtype.mk`

```lean
structure Subtype {α : Sort u} (p : α → Prop)
```

11. `PartialFun.Iso.mk`

```lean
def Iso.mk {α β : PartialFun.{u}} (e : α ≃ β) : α ≅ β
```

12. `Option.get`

```lean
@[inline, implicit_reducible] def get {α : Type u} : (o : Option α) → isSome o → α
  | some x, _ => x
```

13. `Pointed`

```lean
structure Pointed : Type (u + 1)
```

14. `Equiv.optionSubtypeNe`

```lean
def optionSubtypeNe (a : α) : Option {b // b ≠ a} ≃ α
```

15. `CategoryTheory.Equivalence.mk'`

```lean
abbrev mk''
    {C : Type u₁} {D : Type u₂} [Category.{v₁} C] [Category.{v₂} D]
    (functor : C ⥤ D) (inverse : D ⥤ C)
    (unitIso : 𝟭 C ≅ functor ⋙ inverse) (counitIso : inverse ⋙ functor ≅ 𝟭 D)
    (functor_unitIso_comp : dsimp% ∀ (X : C),
      counitIso.inv.app (functor.obj X) ≫ functor.map (unitIso.inv.app X) = 𝟙 (functor.obj X)) :
    Equivalence C D
```

16. `pointedToPartialFun`

```lean
def pointedToPartialFun : Pointed.{u} ⥤ PartialFun
```

17. `partialFunToPointed`

```lean
noncomputable def partialFunToPointed : PartialFun ⥤ Pointed
```

18. `Ne`

```lean
@[reducible] def Ne {α : Sort u} (a b : α)
```

19. `Pointed.X`

```lean
protected X : Type u
```

20. `PartialFun`

```lean
def PartialFun : Type (u + 1)
```

21. `CategoryTheory.Functor.id`

```lean
protected def id : C ⥤ C
```

22. `Classical.propDecidable`

```lean
noncomputable scoped instance (priority := low) propDecidable (a : Prop) : Decidable a
```

23. `Option.some`

```lean
| some (val : α) : Option α
```

24. `Eq`

```lean
inductive Eq : α → α → Prop
```


---

## t027

Target: `CategoryTheory.ShortComplex.asIsoHomologyπ`

```lean
noncomputable def asIsoHomologyπ (hf : S.f = 0) [S.HasHomology] :
    S.cycles ≅ S.homology
```

Proof / construction:

```lean
:= by
  have := S.isIso_homologyπ hf
  exact asIso S.homologyπ
```

Candidates (20), random order:

1. `CategoryTheory.ShortComplex.isIso_homologyπ`

```lean
lemma isIso_homologyπ (hf : S.f = 0) [S.HasHomology] :
    IsIso S.homologyπ
```

2. `CategoryTheory.ShortComplex`

```lean
structure ShortComplex
```

3. `CategoryTheory.Limits.HasZeroMorphisms.zero`

```lean
CategoryTheory.Limits.HasZeroMorphisms.zero
```

4. `CategoryTheory.IsIso`

```lean
class IsIso (f : X ⟶ Y) : Prop
```

5. `CategoryTheory.ShortComplex.homologyπ`

```lean
noncomputable def homologyπ : S.cycles ⟶ S.homology
```

6. `Eq`

```lean
inductive Eq : α → α → Prop
```

7. `CategoryTheory.ShortComplex.X₁`

```lean
CategoryTheory.ShortComplex.X₁
```

8. `CategoryTheory.ShortComplex.X₂`

```lean
CategoryTheory.ShortComplex.X₂
```

9. `CategoryTheory.ShortComplex.HasHomology`

```lean
class HasHomology : Prop
```

10. `CategoryTheory.Limits.HasZeroMorphisms`

```lean
class HasZeroMorphisms
```

11. `Quiver.Hom`

```lean
Hom : V → V → Type v
```

12. `CategoryTheory.Category.toCategoryStruct`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

13. `Zero.toOfNat0`

```lean
instance (priority := 300) Zero.toOfNat0 {α} [Zero α] : OfNat α (nat_lit 0)
```

14. `OfNat.ofNat`

```lean
ofNat : α
```

15. `CategoryTheory.ShortComplex.cycles`

```lean
noncomputable def cycles : C
```

16. `CategoryTheory.CategoryStruct.toQuiver`

```lean
class CategoryStruct (obj : Type u) : Type max u (v + 1) extends Quiver.{v} obj
```

17. `CategoryTheory.asIso`

```lean
noncomputable def asIso (f : X ⟶ Y) [IsIso f] : X ≅ Y
```

18. `CategoryTheory.ShortComplex.f`

```lean
f : X₁ ⟶ X₂
```

19. `CategoryTheory.Category`

```lean
class Category (obj : Type u) : Type max u (v + 1) extends CategoryStruct.{v} obj
```

20. `CategoryTheory.ShortComplex.homology`

```lean
noncomputable def homology [HasHomology S] : C
```


---

## t028

Target: `MeasureTheory.IntegrableOn.mono_set_ae`

```lean
theorem IntegrableOn.mono_set_ae (h : IntegrableOn f t μ) (hst : s ≤ᵐ[μ] t) : IntegrableOn f s μ
```

Proof / construction:

```lean
:=
  h.integrable.mono_measure <| Measure.restrict_mono_ae hst
```

Candidates (14), random order:

1. `MeasureTheory.Measure`

```lean
structure Measure (α : Type*) [MeasurableSpace α] extends OuterMeasure α
```

2. `MeasurableSpace`

```lean
@[class] structure MeasurableSpace (α : Type*)
```

3. `MeasureTheory.Measure.restrict_mono_ae`

```lean
theorem restrict_mono_ae (h : s ≤ᵐ[μ] t) : μ.restrict s ≤ μ.restrict t
```

4. `TopologicalSpace`

```lean
class TopologicalSpace (X : Type u)
```

5. `MeasureTheory.Integrable.mono_measure`

```lean
theorem Integrable.mono_measure {f : α → ε} (h : Integrable f ν) (hμ : μ ≤ ν) : Integrable f μ
```

6. `Set`

```lean
def Set (α : Type u)
```

7. `Filter.EventuallyLE`

```lean
def EventuallyLE [LE β] (l : Filter α) (f g : α → β) : Prop
```

8. `MeasureTheory.Measure.instFunLike`

```lean
instance Measure.instFunLike [MeasurableSpace α] : FunLike (Measure α) (Set α) ℝ≥0∞
```

9. `ContinuousENorm`

```lean
class ContinuousENorm (E : Type*) [TopologicalSpace E] extends ENorm E
```

10. `MeasureTheory.Measure.restrict`

```lean
noncomputable def restrict {_m0 : MeasurableSpace α} (μ : Measure α) (s : Set α) : Measure α
```

11. `MeasureTheory.IntegrableOn.integrable`

```lean
theorem IntegrableOn.integrable (h : IntegrableOn f s μ) : Integrable f (μ.restrict s)
```

12. `MeasureTheory.ae`

```lean
def ae (μ : F) : Filter α
```

13. `MeasureTheory.IntegrableOn`

```lean
def IntegrableOn (f : α → ε) (s : Set α) (μ : Measure α := by volume_tac) : Prop
```

14. `Prop.le`

```lean
instance Prop.le : LE Prop
```


---

## t029

Target: `Matroid.Dep.of_isMinor`

```lean
lemma Dep.of_isMinor {D : Set α} (hD : M.Dep D) (hDN : D ⊆ N.E) (hNM : N ≤m M) : N.Dep D
```

Proof / construction:

```lean
:=
  ⟨fun h ↦ hD.not_indep <| h.of_isMinor hNM, hDN⟩
```

Candidates (12), random order:

1. `Matroid.Dep.not_indep`

```lean
theorem Dep.not_indep (hD : M.Dep D) : ¬ M.Indep D
```

2. `Matroid.Dep`

```lean
def Dep (M : Matroid α) (D : Set α) : Prop
```

3. `Matroid.Indep.of_isMinor`

```lean
lemma Indep.of_isMinor (hI : N.Indep I) (hNM : N ≤m M) : M.Indep I
```

4. `Matroid`

```lean
structure Matroid (α : Type*)
```

5. `Matroid.Indep`

```lean
Matroid.Indep
```

6. `Not`

```lean
@[implicit_reducible] def Not (a : Prop) : Prop
```

7. `Set`

```lean
def Set (α : Type u)
```

8. `And.intro`

```lean
structure And (a b : Prop) : Prop
```

9. `LE.le`

```lean
le : α → α → Prop
```

10. `Matroid.IsMinor`

```lean
def IsMinor (N M : Matroid α) : Prop
```

11. `Matroid.E`

```lean
Matroid.E
```

12. `Set.instLE`

```lean
instance : LE (Set α)
```


---

## t030

Target: `Topology.WithUpper.toUpper_symm`

```lean
@[simp] lemma toUpper_symm {α} : (@toUpper α).symm = ofUpper
```

Proof / construction:

```lean
:= rfl
```

Candidates (5), random order:

1. `Equiv.symm`

```lean
protected def symm (e : α ≃ β) : β ≃ α
```

2. `Equiv`

```lean
structure Equiv (α β : Sort*)
```

3. `Topology.WithUpper.toUpper`

```lean
@[match_pattern] def toUpper : α ≃ WithUpper α
```

4. `Topology.WithUpper`

```lean
def WithUpper (α : Type*)
```

5. `rfl`

```lean
@[match_pattern] def rfl {α : Sort u} {a : α} : Eq a a
```


---
