# Proof 4

Theorem `ExpGrowth.expGrowthSup_sum` (Mathlib source below).

```lean
lemma expGrowthSup_sum {α : Type*} (u : α → ℕ → ℝ≥0∞) (s : Finset α) :
    expGrowthSup (∑ x ∈ s, u x) = ⨆ x ∈ s, expGrowthSup (u x) := by
  classical
  induction s using Finset.induction_on with
  | empty => rw [Finset.sum_empty, ← Finset.iSup_coe, Finset.coe_empty, iSup_emptyset,
    expGrowthSup_zero]
  | insert a t a_t ha => rw [Finset.sum_insert a_t, expGrowthSup_add, ← Finset.iSup_coe,
    Finset.coe_insert a t, iSup_insert, Finset.iSup_coe, ha]

```

## Candidate views (anonymized)

### View A
  1. Finset.iSup_coe
  2. ExpGrowth.expGrowthSup_zero
  3. iSup_insert
  4. iSup_emptyset
  5. Finset.sum_insert
  6. Finset.sum_empty
  7. Finset.induction_on
  8. Finset.coe_insert
  9. Finset.coe_empty
  10. ExpGrowth.expGrowthSup_add

### View B
  1. Finset.induction_on
  2. Finset.sum_empty
  3. congrArg
  4. Finset.coe_empty
  5. iSup_insert
  6. Finset.coe_insert
  7. Finset.iSup_coe
  8. ExpGrowth.expGrowthSup_add
  9. iSup_emptyset
  10. Finset.sum_insert

### View C
  - Eq.symm
  - ExpGrowth.expGrowthSup_add
  - ExpGrowth.expGrowthSup_zero
  - Finset.coe_empty
  - Finset.coe_insert
  - Finset.iSup_coe
  - Finset.induction_on
  - Finset.sum_empty
  - Finset.sum_insert
  - congrArg
  - iSup_emptyset
  - iSup_insert

### View D
  1. ExpGrowth.expGrowthSup_add
  2. ExpGrowth.expGrowthSup_zero
  3. Finset.coe_insert
  4. Finset.iSup_coe
  5. iSup_insert
  6. iSup_emptyset
  7. Finset.induction_on
  8. Finset.coe_empty
  9. Finset.sum_insert
  10. Finset.sum_empty

### View E
  - ExpGrowth.expGrowthSup_add
  - ExpGrowth.expGrowthSup_zero
  - Finset.coe_insert
  - Finset.iSup_coe
  - iSup_insert
  - iSup_emptyset