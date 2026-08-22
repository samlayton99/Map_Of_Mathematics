# Premise retrieval with structural hints — batch 01

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


## q01  `QuadraticForm.discr'_smul`
module: `Mathlib.LinearAlgebra.QuadraticForm.Basic`

```lean
theorem discr'_smul (a : R) : (a • Q).discr' = a ^ Fintype.card n * Q.discr'
```

structural index suggests:
  1. `Matrix.det_transpose`
  2. `Matrix.det_mul`
  3. `RingHom.mapMatrix_apply`
  4. `Matrix.det_one`
  5. `Finset.sum_congr`
  6. `LinearMap.det_toMatrix`
  7. `RingHom.map_det`
  8. `Finset.prod_congr`
  9. `Matrix.det_fin_two`
  10. `Matrix.det_diagonal`

## q02  `Bornology.IsVonNBounded.restrict_scalars_of_nontrivial`
module: `Mathlib.Analysis.LocallyConvex.Bounded`

```lean
protected theorem Bornology.IsVonNBounded.restrict_scalars_of_nontrivial
    [NormedField 𝕜] [NormedRing 𝕜'] [NormedAlgebra 𝕜 𝕜'] [Nontrivial 𝕜']
    [Zero E] [TopologicalSpace E]
    [SMul 𝕜 E] [MulAction 𝕜' E] [IsScalarTower 𝕜 𝕜' E] {s : Set E}
    (h : IsVonNBounded 𝕜' s) : IsVonNBounded 𝕜 s
```

structural index suggests:
  1. `Filter.tendsto_map'_iff`
  2. `Filter.map_map`
  3. `Filter.IsBounded.mono`
  4. `upperSemicontinuous_iff_frequently`
  5. `lowerSemicontinuousAt_iff_frequently`
  6. `upperSemicontinuousAt_iff_frequently`
  7. `IsLinearTopology.tendsto_smul_zero`
  8. `Bornology.isVonNBounded_union`
  9. `Set.image_inter_nonempty_iff`
  10. `IntermediateField.algebraMap_mem`

## q03  `Turing.TM2to1.addBottom_map`
module: `Mathlib.Computability.TuringMachine.StackTuringMachine`

```lean
theorem addBottom_map (L : ListBlank (∀ k, Option (Γ k))) :
    (addBottom L).map ⟨Prod.snd, by rfl⟩ = L
```

structural index suggests:
  1. `Turing.ListBlank.head_cons`
  2. `Turing.ListBlank.tail_cons`
  3. `Turing.ListBlank.cons_head_tail`
  4. `Turing.ListBlank.head_map`
  5. `Turing.ListBlank.tail_map`
  6. `Turing.ListBlank.nth_succ`
  7. `Turing.Tape.move_right_n_head`
  8. `Turing.Tape.mk'_nth_nat`
  9. `Turing.TM2to1.stk_nth_val`
  10. `Turing.TM2to1.addBottom_nth_snd`

## q04  `MeasureTheory.pdf.IsUniform.pdf_eq_zero_of_measure_eq_zero_or_top`
module: `Mathlib.Probability.Distributions.Uniform`

```lean
theorem pdf_eq_zero_of_measure_eq_zero_or_top {X : Ω → E} {s : Set E}
    (hu : IsUniform X s ℙ μ) (hμs : μ s = 0 ∨ μ s = ∞) : pdf X ℙ μ =ᵐ[μ] 0
```

structural index suggests:
  1. `Measurable.aemeasurable`
  2. `MeasureTheory.Measure.ext`
  3. `MeasureTheory.Measure.restrict_apply`
  4. `MeasureTheory.Measure.map_apply`
  5. `MeasureTheory.Measure.measurable_rnDeriv`
  6. `MeasureTheory.measure_mono`
  7. `MeasureTheory.withDensity_apply`
  8. `MeasureTheory.measure_ne_top`
  9. `MeasureTheory.lintegral_congr_ae`
  10. `MeasureTheory.ae_restrict_iff'`

## q05  `Real.tendsto_mul_log_one_add_of_tendsto`
module: `Mathlib.Analysis.SpecialFunctions.Complex.LogBounds`

```lean
lemma tendsto_mul_log_one_add_of_tendsto {g : ℝ → ℝ} {t : ℝ}
    (hg : Tendsto (fun x ↦ x * g x) atTop (𝓝 t)) :
    Tendsto (fun x ↦ x * log (1 + g x)) atTop (𝓝 t)
```

structural index suggests:
  1. `Complex.ofReal_mul`
  2. `Complex.ofReal_inj`
  3. `Real.log_one`
  4. `Complex.mul_re`
  5. `Complex.ofReal_div`
  6. `Real.log_zero`
  7. `Complex.ofReal_add`
  8. `Complex.mul_im`
  9. `Complex.ofReal_neg`
  10. `Complex.norm_real`

## q06  `ContinuousMultilinearMap.ofSubsingletonₗᵢ`
module: `Mathlib.Analysis.Normed.Module.Multilinear.Basic`

```lean
def ofSubsingletonₗᵢ [Subsingleton ι] (i : ι) :
    (G →L[𝕜] G') ≃ₗᵢ[𝕜] ContinuousMultilinearMap 𝕜 (fun _ : ι ↦ G) G'
```

structural index suggests:
  1. `LinearMap.ext`
  2. `Submodule.ext`
  3. `Submodule.mem_map`
  4. `LinearMap.map_smul_of_tower`
  5. `LinearMap.mem_ker`
  6. `LinearEquiv.ext`
  7. `map_sum`
  8. `LinearPMap.mem_graph_iff`
  9. `LinearEquiv.injective`
  10. `Submodule.mem_prod`

## q07  `mem_pathComponentIn_self`
module: `Mathlib.Topology.Connected.PathConnected`

```lean
theorem mem_pathComponentIn_self (h : x ∈ F) : x ∈ pathComponentIn F x
```

structural index suggests:
  1. `Part.mem_bind_iff`

## q08  `MeasureTheory.ennrealPreVariation`
module: `Mathlib.MeasureTheory.Measure.PreVariation`

```lean
noncomputable def ennrealPreVariation (hf : IsSigmaSubadditiveSetFun f) (hf' : f ∅ = 0) :
    VectorMeasure X ℝ≥0∞
```

structural index suggests:
  1. `MeasureTheory.measure_mono`
  2. `MeasureTheory.Measure.ext`
  3. `ENNReal.coe_ne_top`
  4. `ENNReal.ofNat_ne_top`
  5. `MeasureTheory.measure_empty`
  6. `MeasureTheory.Measure.const_comp`
  7. `Measurable.aemeasurable`
  8. `MeasureTheory.measure_ne_top`
  9. `ENNReal.smul_def`
  10. `ENNReal.coe_eq_zero`

## q09  `Real.one_div_sub_hasFPowerSeriesOnBall_zero`
module: `Mathlib.Analysis.Analytic.Binomial`

```lean
theorem one_div_sub_hasFPowerSeriesOnBall_zero {r : ℝ} (hr : r ≠ 0) :
    HasFPowerSeriesOnBall (fun x ↦ 1 / (r - x)) (.ofScalars ℝ fun n ↦ (r ^ (n + 1))⁻¹) 0 ‖r‖ₑ
```

structural index suggests:
  1. `MeasureTheory.measure_mono`
  2. `MeasureTheory.Measure.ext`
  3. `ENNReal.coe_ne_top`
  4. `ENNReal.ofNat_ne_top`
  5. `norm_nonneg`
  6. `MeasureTheory.Measure.const_comp`
  7. `MeasureTheory.measure_empty`
  8. `IsBoundedSMul.continuousSMul`
  9. `ENNReal.coe_le_coe`
  10. `MeasureTheory.measure_ne_top`

## q10  `Filter.hasBasis_smallSets`
module: `Mathlib.Order.Filter.SmallSets`

```lean
theorem hasBasis_smallSets (l : Filter α) :
    HasBasis l.smallSets (fun t : Set α => t ∈ l) powerset
```

structural index suggests:
  1. `Part.mem_bind_iff`
