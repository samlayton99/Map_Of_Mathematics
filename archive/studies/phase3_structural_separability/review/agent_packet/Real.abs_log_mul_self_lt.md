# Review packet — `Real.abs_log_mul_self_lt`

*domain file:* Analysis_SpecialFunctions_Log_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
/-- Bound for `|log x * x|` in the interval `(0, 1]`. -/
theorem abs_log_mul_self_lt (x : ℝ) (h1 : 0 < x) (h2 : x ≤ 1) : |log x * x| < 1
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V6:** `Real`, `LT.lt`, `Real.instLT`, `OfNat.ofNat`, `Zero.toOfNat0`, `Real.instZero`, `LE.le`, `Real.instLE`
**V7:** `Real`, `Nat`, `CommSemiring.toSemiring`, `Real.instCommSemiring`, `AddCommMonoidWithOne.toAddMonoidWithOne`, `NonAssocSemiring.toAddCommMonoidWithOne`, `Semiring.toNonAssocSemiring`, `Nat.rawCast`
**V4:** `Real.log_inv`, `Real.log_div`, `Real.log_nonneg`, `DivisionMonoid.toDivInvOneMonoid`, `Real.log_le_sub_one_of_pos`, `_private.Basic.0.Real.abs_log_mul_self_lt._simp_1`, `SubtractionMonoid.toSubNegZeroMonoid`, `Real.log_one`
**V8:** `Real`, `Eq`, `one_div`, `Real.log`, `Real.log_le_sub_one_of_pos`, `lt_of_not_ge`, `Mathlib.Tactic.Linarith.lt_irrefl`, `inferInstance`
**V3:** `Real.log_le_sub_one_of_pos`, `lt_of_not_ge`, `mul_nonneg`, `LT.lt.le`, `Mathlib.Tactic.Linarith.lt_irrefl`, `Real.log_nonneg`, `abs_neg`, `Mathlib.Tactic.Linarith.add_lt_of_neg_of_le`
**V1:** `Real`, `LT.lt`, `LE.le`, `mul_nonneg`, `OfNat.ofNat`, `HMul.hMul`, `Real.log`, `One.toOfNat1`
**V5:** `Real`, `mul_nonneg`, `LT.lt`, `Real.log`, `LE.le`, `OfNat.ofNat`, `Real.log_nonneg`, `Zero.toOfNat0`
**V2:** `mul_nonneg`, `Real.log_nonneg`, `Real.log_inv`, `abs_neg`, `Real.log_le_sub_one_of_pos`, `Real.log_one`, `neg_mul`, `Real.log_div`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
/-- Bound for `|log x * x|` in the interval `(0, 1]`. -/
theorem abs_log_mul_self_lt (x : ℝ) (h1 : 0 < x) (h2 : x ≤ 1) : |log x * x| < 1 := by
  have : 0 < 1 / x := by simpa only [one_div, inv_pos] using h1
  replace := log_le_sub_one_of_pos this
  replace : log (1 / x) < 1 / x := by linarith
  rw [log_div one_ne_zero h1.ne', log_one, zero_sub, lt_div_iff₀ h1] at this
  have aux : 0 ≤ -log x * x := by
    refine mul_nonneg ?_ h1.le
    rw [← log_inv]
    apply log_nonneg
    rw [← le_inv_comm₀ h1 zero_lt_one, inv_one]
    exact h2
  rw [← abs_of_nonneg aux, neg_mul, abs_neg] at this
  exact this

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
