# Proof 6

Theorem `BoxIntegral.Prepartition.coe_eq_of_mem_split_of_lt_mem` (Mathlib source below).

```lean
theorem coe_eq_of_mem_split_of_lt_mem {y : ι → ℝ} (h₁ : J ∈ split I i x) (h₂ : y ∈ J)
    (h₃ : x < y i) : (J : Set (ι → ℝ)) = ↑I ∩ { y | x < y i } := by
  refine (mem_split_iff'.1 h₁).resolve_left fun H => ?_
  rw [← Box.mem_coe, H] at h₂
  exact h₃.not_ge h₂.2

```

## Candidate views (anonymized)

### View A
  - And.right
  - BoxIntegral.Box.mem_coe
  - BoxIntegral.Prepartition.mem_split_iff'
  - Eq.symm
  - Iff.mp
  - LT.lt.not_ge
  - Or.resolve_left
  - congrArg
  - propext

### View B
  - BoxIntegral.Prepartition.mem_split_iff'
  - BoxIntegral.Box.mem_coe
  - Or.resolve_left
  - LT.lt.not_ge
  - congrArg
  - Eq.symm

### View C
  1. Or.resolve_left
  2. congrArg
  3. Iff.mp
  4. And.right
  5. BoxIntegral.Prepartition.mem_split_iff'
  6. LT.lt.not_ge
  7. BoxIntegral.Box.mem_coe
  8. Eq.symm
  9. propext

### View D
  1. BoxIntegral.Prepartition.mem_split_iff'
  2. BoxIntegral.Box.mem_coe
  3. Or.resolve_left
  4. LT.lt.not_ge
  5. congrArg
  6. Eq.symm
  7. Iff.mp
  8. And.right
  9. propext

### View E
  1. BoxIntegral.Prepartition.mem_split_iff'
  2. BoxIntegral.Box.mem_coe