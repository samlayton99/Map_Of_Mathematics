# Proof 1

Theorem `Complex.I_mul_im` (Mathlib source below).

```lean
theorem I_mul_im (z : ℂ) : (I * z).im = z.re := by simp

set_option backward.isDefEq.respectTransparency.types false in
@[simp]
theorem equivRealProd_symm_apply (p : ℝ × ℝ) : equivRealProd.symm p = p.1 + p.2 * I := by
  ext <;> simp [Complex.equivRealProd, ofReal]

```

## Candidate views (anonymized)

### View A
  - Complex.mul_im
  - of_eq_true
  - eq_self
  - zero_add
  - one_mul
  - MulZeroClass.zero_mul

### View B
  1. Complex.mul_im
  2. of_eq_true
  3. eq_self
  4. zero_add
  5. one_mul
  6. MulZeroClass.zero_mul
  7. congr
  8. congrArg
  9. congrFun'
  10. Eq.trans

### View C
  (none)

### View D
  - Complex.mul_im
  - Eq.trans
  - MulZeroClass.zero_mul
  - congr
  - congrArg
  - congrFun'
  - eq_self
  - of_eq_true
  - one_mul
  - zero_add

### View E
  1. of_eq_true
  2. congr
  3. congrArg
  4. MulZeroClass.zero_mul
  5. congrFun'
  6. zero_add
  7. eq_self
  8. Eq.trans
  9. Complex.mul_im
  10. one_mul