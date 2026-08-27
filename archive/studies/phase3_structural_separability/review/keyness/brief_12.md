# Proof 12

Theorem `CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHomLeft_tensor` (Mathlib source below).

```lean
theorem actionHomLeft_tensor {z z' : D} (f : z ⟶ z') (x y : C) :
    (f ⊵ᵣ (x ⊗ y)) = (αᵣ z x y).hom ≫ (f ⊵ᵣ x) ⊵ᵣ y ≫ (αᵣ z' x y).inv := by
  simp only [← actionHom_id]
  rw [← Category.assoc, ← actionAssocIso_hom_naturality]
  simp

```

## Candidate views (anonymized)

### View A
  - CategoryTheory.Category.assoc
  - CategoryTheory.Category.comp_id
  - CategoryTheory.Iso.hom_inv_id
  - CategoryTheory.MonoidalCategory.MonoidalRightAction.actionAssocIso_hom_naturality
  - CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHom_id
  - CategoryTheory.MonoidalCategory.id_whiskerRight
  - CategoryTheory.MonoidalCategory.tensorHom_id
  - Eq.symm
  - Eq.trans
  - _private.Mathlib.CategoryTheory.Monoidal.Action.Basic.0.CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHomLeft_tensor._simp_1_1
  - congr
  - congrArg
  - congrFun
  - congrFun'

### View B
  1. CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHom_id
  2. CategoryTheory.MonoidalCategory.tensorHom_id
  3. of_eq_true
  4. eq_self
  5. CategoryTheory.MonoidalCategory.MonoidalRightAction.actionAssocIso_hom_naturality
  6. CategoryTheory.MonoidalCategory.id_whiskerRight
  7. CategoryTheory.Iso.hom_inv_id
  8. congrFun
  9. congrArg
  10. congr

### View C
  1. CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHom_id
  2. CategoryTheory.MonoidalCategory.MonoidalRightAction.actionAssocIso_hom_naturality
  3. CategoryTheory.Category.assoc

### View D
  - _private.Mathlib.CategoryTheory.Monoidal.Action.Basic.0.CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHomLeft_tensor._simp_1_1
      . CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHom_id
      . Eq.symm
  - CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHom_id
  - CategoryTheory.MonoidalCategory.tensorHom_id
  - of_eq_true
  - eq_self
  - CategoryTheory.MonoidalCategory.MonoidalRightAction.actionAssocIso_hom_naturality

### View E
  1. congrFun
  2. congrArg
  3. congr
  4. of_eq_true
  5. CategoryTheory.MonoidalCategory.id_whiskerRight
  6. CategoryTheory.Category.assoc
  7. CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHom_id
  8. CategoryTheory.Category.comp_id
  9. _private.Mathlib.CategoryTheory.Monoidal.Action.Basic.0.CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHomLeft_tensor._simp_1_1
  10. eq_self