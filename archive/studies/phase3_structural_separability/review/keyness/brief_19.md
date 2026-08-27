# Proof 19

Theorem `AddMonoidAlgebra.supDegree_single` (Mathlib source below).

```lean
theorem supDegree_single (a : A) (r : R) :
    (single a r).supDegree D = if r = 0 then ⊥ else D a := by
  split_ifs with hr <;> simp [supDegree_single_ne_zero, hr]

```

## Candidate views (anonymized)

### View A
  - AddMonoidAlgebra.single_zero
  - AddMonoidAlgebra.supDegree_single_ne_zero
  - Finset.sup_eq_bot_iff._simp_2
  - Finset.notMem_empty._simp_1
  - IsEmpty.forall_iff._simp_1
  - if_pos

### View B
  1. if_pos
  2. Finset.sup_eq_bot_iff._simp_2
  3. congrArg
  4. IsEmpty.forall_iff._simp_1
  5. of_eq_true
  6. if_neg
  7. congrFun'
  8. AddMonoidAlgebra.single_zero
  9. Finset.notMem_empty._simp_1
  10. eq_self

### View C
  - AddMonoidAlgebra.single_zero
  - AddMonoidAlgebra.supDegree_single_ne_zero
  - Eq.trans
  - Finset.notMem_empty._simp_1
  - Finset.sup_eq_bot_iff._simp_2
  - IsEmpty.forall_iff._simp_1
  - congrArg
  - congrFun'
  - eq_false
  - eq_self
  - forall_congr
  - if_neg
  - if_pos
  - implies_congr

### View D
  1. AddMonoidAlgebra.single_zero
  2. AddMonoidAlgebra.supDegree_single_ne_zero
  3. Finset.sup_eq_bot_iff._simp_2
  4. Finset.notMem_empty._simp_1
  5. IsEmpty.forall_iff._simp_1
  6. if_pos
  7. if_neg
  8. of_eq_true
  9. eq_self
  10. implies_true

### View E
  1. AddMonoidAlgebra.supDegree_single_ne_zero