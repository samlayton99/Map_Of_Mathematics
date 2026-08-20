# Proof 13

Theorem `LinearMap.toSpanSingleton_add` (Mathlib source below).

```lean
theorem toSpanSingleton_add [ContinuousAdd M₁] (x y : M₁) :
    toSpanSingleton R₁ (x + y) = toSpanSingleton R₁ x + toSpanSingleton R₁ y :=
  coe_inj.mp <| LinearMap.toSpanSingleton_add _ _

```

## Candidate views (anonymized)

### View A
  - LinearMap.toSpanSingleton_apply
  - LinearMap.ext_ring
  - one_smul
  - of_eq_true
  - eq_self
  - smul_add

### View B
  - Eq.trans
  - LinearMap.ext_ring
  - LinearMap.toSpanSingleton_apply
  - congr
  - congrArg
  - eq_self
  - of_eq_true
  - one_smul
  - smul_add

### View C
  1. LinearMap.ext_ring
  2. smul_add
  3. congr
  4. congrArg
  5. one_smul
  6. of_eq_true
  7. eq_self
  8. Eq.trans
  9. LinearMap.toSpanSingleton_apply

### View D
  1. LinearMap.toSpanSingleton_apply
  2. LinearMap.ext_ring
  3. one_smul
  4. of_eq_true
  5. eq_self
  6. smul_add
  7. congr
  8. congrArg
  9. Eq.trans

### View E
  (none)