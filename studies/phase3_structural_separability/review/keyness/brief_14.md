# Proof 14

Theorem `HasStrictDerivAt.finsetProd` (Mathlib source below).

```lean
protected theorem finsetProd {γ} [CommMonoid β] [ContinuousMul β] {U : γ → ι → Ω → β}
    {s : Finset γ} (h : ∀ c ∈ s, IsStronglyProgressive f (U c)) :
    IsStronglyProgressive f fun i a => ∏ c ∈ s, U c i a := by
  convert! IsStronglyProgressive.finsetProd' h using 1; ext (i a); simp only [Finset.prod_apply]

```

## Candidate views (anonymized)

### View A
  - HasStrictDerivAt.fun_finsetProd
  - Finset.prod_apply
  - IsBoundedSMul.continuousSMul
  - eq_of_heq
  - of_eq_true
  - eq_self

### View B
  1. eq_of_heq
  2. congrArg
  3. funext
  4. of_eq_true
  5. HasStrictDerivAt.fun_finsetProd
  6. Finset.prod_apply
  7. congrFun'
  8. IsBoundedSMul.continuousSMul
  9. eq_self
  10. Eq.symm

### View C
  - Eq.symm
  - Eq.trans
  - Finset.prod_apply
  - HasStrictDerivAt.fun_finsetProd
  - IsBoundedSMul.continuousSMul
  - congrArg
  - congrFun'
  - eq_of_heq
  - eq_self
  - funext
  - of_eq_true

### View D
  1. HasStrictDerivAt.fun_finsetProd
  2. Finset.prod_apply
  3. IsBoundedSMul.continuousSMul
  4. eq_of_heq
  5. of_eq_true
  6. eq_self
  7. funext
  8. congrArg
  9. congrFun'
  10. Eq.symm

### View E
  (none)