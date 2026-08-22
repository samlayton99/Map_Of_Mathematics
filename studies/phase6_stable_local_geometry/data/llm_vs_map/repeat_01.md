# Premise retrieval — batch 01

For each Lean 4 / Mathlib theorem below you are shown ONLY its statement.
The proof is not shown and you must not try to recall the file.

For each item, predict which Mathlib declarations the PROOF uses: name
the 10 declarations you judge most likely to be cited by the proof,
most likely first. Rules:

- Give fully-qualified Mathlib names exactly as they appear in the
  library (e.g. `Finset.sum_congr`, `Polynomial.degree_mul`).
- Predict the substantive mathematical lemmas/definitions the proof
  builds on, not tactic-level plumbing (`Eq.mpr`, `congrArg`, `rfl`,
  `id`) and not things already named in the statement itself.
- Exactly 10 names per item, no commentary, no duplicates.

Answer as JSON only:
{"q01": ["Name.one", ...], "q02": [...], ...}

---


## q01  `QuadraticForm.discr'_smul`
module: `Mathlib.LinearAlgebra.QuadraticForm.Basic`

```lean
theorem discr'_smul (a : R) : (a • Q).discr' = a ^ Fintype.card n * Q.discr'
```

## q02  `Bornology.IsVonNBounded.restrict_scalars_of_nontrivial`
module: `Mathlib.Analysis.LocallyConvex.Bounded`

```lean
protected theorem Bornology.IsVonNBounded.restrict_scalars_of_nontrivial
    [NormedField 𝕜] [NormedRing 𝕜'] [NormedAlgebra 𝕜 𝕜'] [Nontrivial 𝕜']
    [Zero E] [TopologicalSpace E]
    [SMul 𝕜 E] [MulAction 𝕜' E] [IsScalarTower 𝕜 𝕜' E] {s : Set E}
    (h : IsVonNBounded 𝕜' s) : IsVonNBounded 𝕜 s
```

## q03  `Turing.TM2to1.addBottom_map`
module: `Mathlib.Computability.TuringMachine.StackTuringMachine`

```lean
theorem addBottom_map (L : ListBlank (∀ k, Option (Γ k))) :
    (addBottom L).map ⟨Prod.snd, by rfl⟩ = L
```

## q04  `MeasureTheory.pdf.IsUniform.pdf_eq_zero_of_measure_eq_zero_or_top`
module: `Mathlib.Probability.Distributions.Uniform`

```lean
theorem pdf_eq_zero_of_measure_eq_zero_or_top {X : Ω → E} {s : Set E}
    (hu : IsUniform X s ℙ μ) (hμs : μ s = 0 ∨ μ s = ∞) : pdf X ℙ μ =ᵐ[μ] 0
```

## q05  `Real.tendsto_mul_log_one_add_of_tendsto`
module: `Mathlib.Analysis.SpecialFunctions.Complex.LogBounds`

```lean
lemma tendsto_mul_log_one_add_of_tendsto {g : ℝ → ℝ} {t : ℝ}
    (hg : Tendsto (fun x ↦ x * g x) atTop (𝓝 t)) :
    Tendsto (fun x ↦ x * log (1 + g x)) atTop (𝓝 t)
```

## q06  `ContinuousMultilinearMap.ofSubsingletonₗᵢ`
module: `Mathlib.Analysis.Normed.Module.Multilinear.Basic`

```lean
def ofSubsingletonₗᵢ [Subsingleton ι] (i : ι) :
    (G →L[𝕜] G') ≃ₗᵢ[𝕜] ContinuousMultilinearMap 𝕜 (fun _ : ι ↦ G) G'
```

## q07  `mem_pathComponentIn_self`
module: `Mathlib.Topology.Connected.PathConnected`

```lean
theorem mem_pathComponentIn_self (h : x ∈ F) : x ∈ pathComponentIn F x
```

## q08  `MeasureTheory.ennrealPreVariation`
module: `Mathlib.MeasureTheory.Measure.PreVariation`

```lean
noncomputable def ennrealPreVariation (hf : IsSigmaSubadditiveSetFun f) (hf' : f ∅ = 0) :
    VectorMeasure X ℝ≥0∞
```

## q09  `Real.one_div_sub_hasFPowerSeriesOnBall_zero`
module: `Mathlib.Analysis.Analytic.Binomial`

```lean
theorem one_div_sub_hasFPowerSeriesOnBall_zero {r : ℝ} (hr : r ≠ 0) :
    HasFPowerSeriesOnBall (fun x ↦ 1 / (r - x)) (.ofScalars ℝ fun n ↦ (r ^ (n + 1))⁻¹) 0 ‖r‖ₑ
```

## q10  `Filter.hasBasis_smallSets`
module: `Mathlib.Order.Filter.SmallSets`

```lean
theorem hasBasis_smallSets (l : Filter α) :
    HasBasis l.smallSets (fun t : Set α => t ∈ l) powerset
```
