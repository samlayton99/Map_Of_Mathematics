# Proof 5

Theorem `MulMemClass.mul_right_mem_add_closure` (Mathlib source below).

```lean
lemma mul_right_mem_add_closure (ha : a ∈ closure (S : Set R)) (hb : b ∈ S) :
    a * b ∈ closure (S : Set R) := by
  induction ha using closure_induction with
  | mem r hr => exact mem_closure.mpr fun y hy => hy (mul_mem hr hb)
  | zero => simp only [zero_mul, zero_mem _]
  | add r s _ _ hr hs => simpa only [add_mul] using add_mem hr hs

```

## Candidate views (anonymized)

### View A
  1. AddSubmonoid.closure_induction
  2. AddSubmonoid.mem_closure
  3. add_mul
  4. MulMemClass.mul_mem
  5. MulZeroClass.zero_mul
  6. of_eq_true
  7. AddMemClass.add_mem
  8. ZeroMemClass.zero_mem
  9. AddSubmonoidClass.toZeroMemClass
  10. eq_true

### View B
  1. add_mul
  2. MulZeroClass.zero_mul
  3. ZeroMemClass.zero_mem
  4. MulMemClass.mul_mem
  5. AddSubmonoid.mem_closure
  6. AddSubmonoid.closure_induction
  7. AddMemClass.add_mem

### View C
  - AddSubmonoid.closure_induction
  - AddSubmonoid.mem_closure
  - add_mul
  - MulMemClass.mul_mem
  - MulZeroClass.zero_mul
  - of_eq_true

### View D
  - AddMemClass.add_mem
  - AddSubmonoid.closure_induction
  - AddSubmonoid.mem_closure
  - AddSubmonoidClass.toZeroMemClass
  - Eq.trans
  - Iff.mpr
  - MulMemClass.mul_mem
  - MulZeroClass.zero_mul
  - ZeroMemClass.zero_mem
  - add_mul
  - congrArg
  - eq_true
  - of_eq_true

### View E
  1. AddSubmonoid.closure_induction
  2. Iff.mpr
  3. AddMemClass.add_mem
  4. congrArg
  5. add_mul
  6. MulZeroClass.zero_mul
  7. of_eq_true
  8. Eq.trans
  9. AddSubmonoid.mem_closure
  10. ZeroMemClass.zero_mem