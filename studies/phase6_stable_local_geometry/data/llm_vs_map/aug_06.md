# Premise retrieval with structural hints — batch 06

For each Lean 4 / Mathlib theorem you are shown its statement, plus a
list of CANDIDATE declarations proposed by a structural index. The
index knows nothing about mathematics or names: it ranks declarations
purely by which lemmas tend to be cited together with the things this
theorem's statement mentions. Its suggestions are often in the right
neighbourhood but the wrong lemma, and are sometimes useless. Roughly
one in ten of its top suggestions is actually used by the proof.

Use the hints as evidence, not as an answer key. You may keep, reorder,
or discard any of them, and you should add your own candidates freely.

For each item, give the 10 declarations you judge most likely to be
cited by the PROOF, most likely first. Rules:

- Fully-qualified Mathlib names, exactly as they appear in the library.
- Substantive mathematical lemmas/definitions, not tactic plumbing
  (`Eq.mpr`, `congrArg`, `rfl`, `id`), and not things already named in
  the statement.
- Exactly 10 names per item, no commentary, no duplicates.

Answer as JSON only:
{"q01": ["Name.one", ...], "q02": [...], ...}

---


## q51  `Finsupp.mem_range_embDomain_iff`
module: `Mathlib.Data.Finsupp.Basic`

```lean
lemma mem_range_embDomain_iff [AddCommMonoid M] (f : α ↪ β) (x : β →₀ M) :
    x ∈ Set.range (embDomain f) ↔ ↑x.support ⊆ Set.range f
```

structural index suggests:
  1. `Finsupp.ext`
  2. `Finsupp.embDomain_apply_self`
  3. `Finsupp.embDomain_eq_mapDomain`
  4. `Finsupp.embDomain_apply`
  5. `Finset.sum_congr`
  6. `Finsupp.embDomain_of_notMem_range`
  7. `Finsupp.sum_embDomain`
  8. `Finsupp.embDomain_inj`
  9. `Finsupp.coe_update`
  10. `Finsupp.sum_single_index`

## q52  `eventually_singleton_add_smul_subset`
module: `Mathlib.Analysis.Normed.Module.Ball.Pointwise`

```lean
theorem eventually_singleton_add_smul_subset {x : E} {s : Set E} (hs : Bornology.IsBounded s)
    {u : Set E} (hu : u ∈ 𝓝 x) : ∀ᶠ r in 𝓝 (0 : 𝕜), {x} + r • s ⊆ u
```

structural index suggests:
  1. `Complex.norm_real`
  2. `Real.norm_of_nonneg`
  3. `norm_nonneg`
  4. `Finset.sum_congr`
  5. `Convexity.iConvexComb_eq_sum`
  6. `AEMeasurable.aestronglyMeasurable`
  7. `MeasureTheory.Integrable.aestronglyMeasurable`
  8. `Complex.ofReal_inj`
  9. `Filter.tendsto_map'_iff`
  10. `Filter.map_map`

## q53  `Matrix.adjugate_fin_two`
module: `Mathlib.LinearAlgebra.Matrix.Adjugate`

```lean
theorem adjugate_fin_two (A : Matrix (Fin 2) (Fin 2) α) :
    adjugate A = !![A 1 1, -A 0 1; -A 1 0, A 0 0]
```

structural index suggests:
  1. `Finset.sum_congr`
  2. `Matrix.det_transpose`
  3. `RingHom.mapMatrix_apply`
  4. `Matrix.det_mul`
  5. `Matrix.det_one`
  6. `RingHom.map_det`
  7. `Matrix.cons_val_succ`
  8. `LinearMap.det_toMatrix`
  9. `Finset.prod_congr`
  10. `Matrix.cons_val_fin_one`

## q54  `TopCat.nonempty_isColimit_iff_eq_coinduced`
module: `Mathlib.Topology.Category.TopCat.Limits.Basic`

```lean
lemma nonempty_isColimit_iff_eq_coinduced (c : Cocone F) (hc : IsColimit ((forget).mapCocone c)) :
    Nonempty (IsColimit c) ↔ c.pt.str = ⨆ j, (F.obj j).str.coinduced (c.ι.app j)
```

structural index suggests:
  1. `CategoryTheory.NatTrans.ext'`
  2. `CategoryTheory.Limits.PullbackCone.mk_π_app`
  3. `CategoryTheory.Limits.limit.lift_π_assoc`
  4. `CategoryTheory.Limits.IsColimit.hom_ext`
  5. `CategoryTheory.NatTrans.congr_app`
  6. `CategoryTheory.Iso.ext`
  7. `CategoryTheory.Limits.IsLimit.hom_ext`
  8. `CategoryTheory.Limits.colimit.hom_ext`
  9. `CategoryTheory.Limits.limit.hom_ext`
  10. `CategoryTheory.Limits.Cocone.w`

## q55  `Set.uIoc_eq_union`
module: `Mathlib.Order.Interval.Set.UnorderedInterval`

```lean
lemma uIoc_eq_union : Ι a b = Ioc a b ∪ Ioc b a
```

structural index suggests:
  1. `Set.uIoc_of_le`
  2. `Set.uIoc_comm`
  3. `StrictMono.monotone`
  4. `Monotone.map_min`
  5. `Monotone.map_max`
  6. `Set.uIoc_of_ge`
  7. `Set.Ioc_union_Ioc_eq_Ioc`
  8. `Fin.preimage_natAdd_Ioc_natAdd`
  9. `OrderEmbedding.preimage_Ioc`
  10. `Fin.image_val_Ioc`

## q56  `Real.closedBall_eq_Icc`
module: `Mathlib.Topology.MetricSpace.Pseudo.Defs`

```lean
theorem Real.closedBall_eq_Icc {x r : ℝ} : closedBall x r = Icc (x - r) (x + r)
```

structural index suggests:
  1. `Metric.mem_closedBall`
  2. `norm_nonneg`
  3. `Metric.nhds_basis_closedBall`
  4. `Metric.ball_subset_closedBall`
  5. `norm_zero`
  6. `IsBoundedSMul.continuousSMul`
  7. `mem_closedBall_zero_iff`
  8. `abs_of_nonneg`
  9. `Real.norm_of_nonneg`
  10. `Metric.mem_ball`

## q57  `MeasureTheory.lpMeasToLpTrimLie_symm_indicator`
module: `Mathlib.MeasureTheory.Function.ConditionalExpectation.AEMeasurable`

```lean
theorem lpMeasToLpTrimLie_symm_indicator [one_le_p : Fact (1 ≤ p)] [NormedSpace ℝ F] {hm : m ≤ m0}
    {s : Set α} {μ : Measure α} (hs : MeasurableSet[m] s) (hμs : μ.trim hm s ≠ ∞) (c : F) :
    ((lpMeasToLpTrimLie F ℝ p μ hm).symm (indicatorConstLp p hs hμs c) : Lp F p μ) =
      indicatorConstLp p (hm s hs) ((le_trim hm).trans_lt hμs.lt_top).ne c
```

structural index suggests:
  1. `MeasureTheory.integral_congr_ae`
  2. `MeasureTheory.Lp.ext`
  3. `MeasureTheory.MemLp.coeFn_toLp`
  4. `MeasureTheory.measure_mono`
  5. `Measurable.aemeasurable`
  6. `norm_nonneg`
  7. `MeasureTheory.Lp.memLp`
  8. `MeasureTheory.lintegral_congr_ae`
  9. `MeasureTheory.eLpNorm_congr_ae`
  10. `MeasureTheory.AEStronglyMeasurable.stronglyMeasurable_mk`

## q58  `Finset.inter_sdiff_left_comm`
module: `Mathlib.Data.Finset.SDiff`

```lean
lemma inter_sdiff_left_comm (s t u : Finset α) : s ∩ (t \ u) = t ∩ (s \ u)
```

structural index: no suggestion for this item.

## q59  `RCLike.ofReal_finsupp_sum`
module: `Mathlib.Analysis.RCLike.Basic`

```lean
theorem ofReal_finsupp_sum {α M : Type*} [Zero M] (f : α →₀ M) (g : α → M → ℝ) :
    ((f.sum fun a b => g a b : ℝ) : K) = f.sum fun a b => (g a b : K)
```

structural index suggests:
  1. `norm_nonneg`
  2. `hasSum_geometric_of_lt_one`
  3. `Finset.sum_le_sum`
  4. `Finset.prod_congr`
  5. `Finset.sum_congr`
  6. `NNRat.instCharZero`
  7. `Numbering.card_prefixed`
  8. `Nat.cast_choose`
  9. `Summable.mul_of_nonneg`
  10. `BoundingSieve.siftedSum_le_sum_of_upperMoebius`

## q60  `AddCircle.exists_gcd_eq_one_of_isOfFinAddOrder`
module: `Mathlib.Topology.Instances.AddCircle.Defs`

```lean
theorem exists_gcd_eq_one_of_isOfFinAddOrder {u : AddCircle p} (h : IsOfFinAddOrder u) :
    ∃ m : ℕ, m.gcd (addOrderOf u) = 1 ∧ m < addOrderOf u ∧ ↑((m : 𝕜) / addOrderOf u * p) = u
```

structural index suggests:
  1. `QuotientAddGroup.eq`
  2. `Nat.gcd_dvd_right`
  3. `QuotientAddGroup.eq_zero_iff`
  4. `Nat.gcd_comm`
  5. `Nat.gcd_dvd_left`
  6. `QuotientAddGroup.induction_on`
  7. `Nat.gcd_zero_left`
  8. `Nat.dvd_gcd`
  9. `Nat.Coprime.gcd_eq_one`
  10. `Nat.one_mul`
