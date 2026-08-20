# Proof 9

Theorem `CategoryTheory.GrpObj.mulRight_one` (Mathlib source below).

```lean
lemma mulRight_one (A : C) [GrpObj A] : mulRight η[A] = Iso.refl A := by
  ext; simp

```

## Candidate views (anonymized)

### View A
  1. CategoryTheory.Iso.ext
  2. CategoryTheory.MonObj.lift_comp_one_right
  3. eq_self
  4. of_eq_true
  5. congrArg
  6. Eq.trans
  7. congrFun'

### View B
  - CategoryTheory.GrpObj.mulRight_hom
  - CategoryTheory.Iso.ext
  - CategoryTheory.MonObj.lift_comp_one_right
  - Eq.trans
  - congrArg
  - congrFun'
  - eq_self
  - of_eq_true

### View C
  - CategoryTheory.GrpObj.mulRight_hom
  - CategoryTheory.Iso.ext
  - CategoryTheory.MonObj.lift_comp_one_right
  - of_eq_true
  - eq_self
  - congrArg

### View D
  (none)

### View E
  1. CategoryTheory.Iso.ext
  2. congrArg
  3. of_eq_true
  4. CategoryTheory.GrpObj.mulRight_hom
  5. congrFun'
  6. CategoryTheory.MonObj.lift_comp_one_right
  7. eq_self
  8. Eq.trans