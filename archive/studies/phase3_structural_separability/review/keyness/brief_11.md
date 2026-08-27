# Proof 11

Theorem `Function.support_eq_empty_iff` (Mathlib source below).

```lean
theorem support_eq_empty_iff {x : R⟦Γ⟧} : x.support = ∅ ↔ x = 0 :=
  Function.support_eq_empty_iff.trans coeff_fun_eq_zero_iff

```

## Candidate views (anonymized)

### View A
  (none)

### View B
  - Eq.symm
  - Eq.trans
  - Function.support_subset_iff'
  - Set.mem_empty_iff_false
  - Set.subset_empty_iff
  - congrArg
  - congrFun'
  - forall_congr
  - forall_const
  - funext_iff
  - iff_self
  - implies_congr
  - not_false_eq_true
  - of_eq_true

### View C
  1. Set.subset_empty_iff
  2. Function.support_subset_iff'
  3. forall_const
  4. iff_self
  5. of_eq_true
  6. Set.mem_empty_iff_false
  7. not_false_eq_true
  8. funext_iff
  9. forall_congr
  10. congrArg

### View D
  - Set.subset_empty_iff
  - Function.support_subset_iff'
  - forall_const
  - iff_self
  - of_eq_true
  - Set.mem_empty_iff_false

### View E
  1. iff_self
  2. congrArg
  3. funext_iff
  4. forall_const
  5. of_eq_true
  6. Set.mem_empty_iff_false
  7. Set.subset_empty_iff
  8. congrFun'
  9. not_false_eq_true
  10. Eq.symm