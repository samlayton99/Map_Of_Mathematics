# Proof 0

Theorem `NNRat.cast_strictMono` (Mathlib source below).

```lean
theorem cast_strictMono : StrictMono ((↑) : ℚ≥0 → K) := fun p q h => by
  rwa [NNRat.cast_def, NNRat.cast_def, div_lt_div_iff₀, ← Nat.cast_mul, ← Nat.cast_mul,
    Nat.cast_lt (α := K), ← NNRat.lt_def]
  · simp
  · simp

```

## Candidate views (anonymized)

### View A
  - Eq.symm
  - Eq.trans
  - NNRat.cast_def
  - NNRat.den_pos._simp_1
  - NNRat.lt_def
  - Nat.cast_lt
  - Nat.cast_mul
  - Nat.cast_pos._simp_1
  - congrArg
  - div_lt_div_iff₀
  - of_eq_true
  - propext

### View B
  - NNRat.lt_def
  - NNRat.den_pos._simp_1
      . NNRat.den_pos
      . eq_true
  - NNRat.cast_def
  - Nat.cast_pos._simp_1
  - Nat.cast_lt
  - div_lt_div_iff₀

### View C
  (none)

### View D
  1. NNRat.lt_def
  2. NNRat.den_pos._simp_1
  3. NNRat.cast_def
  4. Nat.cast_pos._simp_1
  5. Nat.cast_lt
  6. div_lt_div_iff₀
  7. Nat.cast_mul
  8. of_eq_true
  9. congrArg
  10. Eq.trans

### View E
  1. Nat.cast_mul
  2. NNRat.cast_def
  3. congrArg
  4. Nat.cast_lt
  5. of_eq_true
  6. Eq.trans
  7. Eq.symm
  8. NNRat.lt_def
  9. propext
  10. div_lt_div_iff₀