# Proof 15

Theorem `MvPowerSeries.antidiagonal_dominant` (Mathlib source below).

```lean
lemma antidiagonal_dominant (i j : σ →₀ ℕ) (vna : IsNonarchimedean v)
    (vMulEq : ∀ a b, v (a * b) = v a * v b) (vNeg : ∀ a, v a = v (-a))
    (hdom : ∀ p ∈ Finset.antidiagonal (i + j), p ≠ (i, j) →
      v (coeff p.1 f * coeff p.2 g) < v (coeff i f) * v (coeff j g)) :
    v (coeff (i + j) (f * g))  = v (coeff i f * coeff j g) := by
  rw [← vMulEq] at hdom
  rw [coeff_mul, IsNonarchimedean.apply_sum_eq_of_lt vna (by grind) (k := (i, j))
    (s := Finset.antidiagonal (i + j)) (Finset.mem_antidiagonal.mpr rfl) hdom]

```

## Candidate views (anonymized)

### View A
  1. Iff.mpr
  2. Finset.HasAntidiagonal.mem_antidiagonal
  3. congrArg
  4. IsNonarchimedean.apply_sum_eq_of_lt
  5. MvPowerSeries.coeff_mul
  6. Eq.symm
  7. _private.Mathlib.RingTheory.MvPowerSeries.GaussNorm.0.MvPowerSeries.antidiagonal_dominant._proof_1_1
  8. rfl

### View B
  1. rfl
  2. MvPowerSeries.coeff_mul
  3. IsNonarchimedean.apply_sum_eq_of_lt
  4. Finset.HasAntidiagonal.mem_antidiagonal

### View C
  - MvPowerSeries.coeff_mul
  - IsNonarchimedean.apply_sum_eq_of_lt
  - _private.Mathlib.RingTheory.MvPowerSeries.GaussNorm.0.MvPowerSeries.antidiagonal_dominant._proof_1_1
      . Classical.byContradiction
      . Eq.trans
      . Eq.symm
      . eq_false
  - Finset.HasAntidiagonal.mem_antidiagonal
  - congrArg
  - Eq.symm

### View D
  1. MvPowerSeries.coeff_mul
  2. IsNonarchimedean.apply_sum_eq_of_lt
  3. _private.Mathlib.RingTheory.MvPowerSeries.GaussNorm.0.MvPowerSeries.antidiagonal_dominant._proof_1_1
  4. Finset.HasAntidiagonal.mem_antidiagonal
  5. congrArg
  6. Eq.symm
  7. rfl
  8. Iff.mpr

### View E
  - Eq.symm
  - Finset.HasAntidiagonal.mem_antidiagonal
  - Iff.mpr
  - IsNonarchimedean.apply_sum_eq_of_lt
  - MvPowerSeries.coeff_mul
  - _private.Mathlib.RingTheory.MvPowerSeries.GaussNorm.0.MvPowerSeries.antidiagonal_dominant._proof_1_1
  - congrArg
  - rfl