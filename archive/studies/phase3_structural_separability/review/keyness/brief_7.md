# Proof 7

Theorem `Algebra.IsAlgebraic.trdeg_le_cardinalMk` (Mathlib source below).

```lean
theorem trdeg_le_cardinalMk [alg : Algebra.IsAlgebraic (adjoin R s) A] : trdeg R A ≤ #s := by
  by_cases h : Injective (algebraMap R A)
  on_goal 2 => simp [trdeg_eq_zero_of_not_injective h]
  have := isDomain_of_adjoin_range R s
  have := (faithfulSMul_iff_algebraMap_injective R A).mpr h
  rw [← matroid_spanning_iff, ← matroid_cRank_eq] at *
  exact alg.cRank_le_cardinalMk

```

## Candidate views (anonymized)

### View A
  - AlgebraicIndependent.matroid_spanning_iff
  - Algebra.IsAlgebraic.isDomain_of_adjoin_range
  - AlgebraicIndependent.matroid_cRank_eq
  - trdeg_eq_zero_of_not_injective
      . Algebra.trdeg.eq_1
      . isEmpty_algebraicIndependent
      . ciSup_of_empty
      . bot_eq_zero
  - Matroid.Spanning.cRank_le_cardinalMk
      . Matroid.Spanning.exists_isBase_subset
      . Matroid.IsBase.cardinalMk_eq_cRank
      . Cardinal.mk_le_mk_of_subset
      . _private.Mathlib.Combinatorics.Matroid.Rank.Cardinal.0.Matroid.Spanning.cRank_le_cardinalMk.match_1_1
  - faithfulSMul_iff_algebraMap_injective

### View B
  1. Iff.mpr
  2. congrArg
  3. trdeg_eq_zero_of_not_injective
  4. AlgebraicIndependent.matroid_spanning_iff
  5. AlgebraicIndependent.matroid_cRank_eq
  6. Matroid.Spanning.cRank_le_cardinalMk
  7. Algebra.IsAlgebraic.isDomain_of_adjoin_range
  8. of_eq_true
  9. congrFun'
  10. faithfulSMul_iff_algebraMap_injective

### View C
  1. AlgebraicIndependent.matroid_cRank_eq
  2. AlgebraicIndependent.matroid_spanning_iff
  3. trdeg_eq_zero_of_not_injective
  4. faithfulSMul_iff_algebraMap_injective
  5. Algebra.IsAlgebraic.isDomain_of_adjoin_range

### View D
  - Algebra.IsAlgebraic.isDomain_of_adjoin_range
  - AlgebraicIndependent.matroid_cRank_eq
  - AlgebraicIndependent.matroid_spanning_iff
  - Eq.symm
  - Eq.trans
  - Iff.mpr
  - Matroid.Spanning.cRank_le_cardinalMk
  - congrArg
  - congrFun'
  - faithfulSMul_iff_algebraMap_injective
  - of_eq_true
  - propext
  - trdeg_eq_zero_of_not_injective
  - zero_le._simp_1

### View E
  1. AlgebraicIndependent.matroid_spanning_iff
  2. Algebra.IsAlgebraic.isDomain_of_adjoin_range
  3. AlgebraicIndependent.matroid_cRank_eq
  4. trdeg_eq_zero_of_not_injective
  5. Matroid.Spanning.cRank_le_cardinalMk
  6. faithfulSMul_iff_algebraMap_injective
  7. zero_le._simp_1
  8. of_eq_true
  9. congrArg
  10. congrFun'