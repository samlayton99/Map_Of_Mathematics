# Premise retrieval with structural hints — batch 05

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


## q41  `Metric.isBounded_range_of_cauchy_map_cofinite`
module: `Mathlib.Topology.MetricSpace.Bounded`

```lean
theorem isBounded_range_of_cauchy_map_cofinite {f : β → α} (hf : Cauchy (map f cofinite)) :
    IsBounded (range f)
```

structural index suggests:
  1. `compl_compl`
  2. `Nat.cofinite_eq_atTop`
  3. `Filter.mem_cofinite`
  4. `Filter.cocompact_eq_cofinite`
  5. `RestrictedProduct.continuous_inclusion`
  6. `Filter.eventually_cofinite`
  7. `Set.Finite.mem_toFinset`
  8. `Set.Finite.subset`
  9. `RestrictedProduct.nhds_eq_map_inclusion`
  10. `Function.Injective.tendsto_cofinite`

## q42  `Polynomial.leval_eq_smeval.linearMap`
module: `Mathlib.Algebra.Polynomial.Smeval`

```lean
theorem leval_eq_smeval.linearMap {R : Type*} [Semiring R] (r : R) :
    leval r = smeval.linearMap R r
```

structural index suggests:
  1. `Polynomial.eval_X`
  2. `Polynomial.eval_C`
  3. `Polynomial.eval_mul`
  4. `Polynomial.eval_sub`
  5. `Polynomial.eval_add`
  6. `Polynomial.eval_one`
  7. `Polynomial.eval_pow`
  8. `Polynomial.IsRoot.def`
  9. `Finset.sum_congr`
  10. `Polynomial.eval_map`

## q43  `Real.differentiableAt_negMulLog_iff`
module: `Mathlib.Analysis.SpecialFunctions.Log.NegMulLog`

```lean
lemma differentiableAt_negMulLog_iff {x : ℝ} : DifferentiableAt ℝ negMulLog x ↔ x ≠ 0
```

structural index suggests:
  1. `Real.log_one`
  2. `Real.log_zero`
  3. `Real.log_mul`
  4. `Real.exp_log`
  5. `Real.log_pos`
  6. `Real.log_inv`
  7. `IsBoundedSMul.continuousSMul`
  8. `Real.rpow_pos_of_pos`
  9. `Real.rpow_def_of_pos`
  10. `Real.log_le_log`

## q44  `Nat.le_fib_add_one`
module: `Mathlib.Data.Nat.Fib.Basic`

```lean
lemma le_fib_add_one : ∀ n, n ≤ fib n + 1
  | 0 => zero_le_one
  | 1 => one_le_two
  | 2 => le_rfl
  | 3 => le_rfl
  | 4 => le_rfl
  | _n + 5 => (le_fib_self le_add_self).trans <| le_succ _
```

structural index: no suggestion for this item.

## q45  `Module.End.lTensorAlgHom`
module: `Mathlib.RingTheory.TensorProduct.Maps`

```lean
def lTensorAlgHom : Module.End R M →ₐ[R] Module.End R (N ⊗[R] M)
```

structural index suggests:
  1. `TensorProduct.induction_on`
  2. `Finset.sum_congr`
  3. `TensorProduct.AlgebraTensorModule.curry_injective`
  4. `TensorProduct.ext`
  5. `TensorProduct.tmul_zero`
  6. `TensorProduct.map_comp`
  7. `TensorProduct.zero_tmul`
  8. `TensorProduct.ext'`
  9. `TensorProduct.AlgebraTensorModule.curry_apply`
  10. `TensorProduct.add_tmul`

## q46  `AlgHom.norm_apply_le_self_mul_norm_one`
module: `Mathlib.Analysis.Normed.Algebra.Spectrum`

```lean
theorem norm_apply_le_self_mul_norm_one [FunLike F A 𝕜] [AlgHomClass F 𝕜 A 𝕜] (f : F) (a : A) :
    ‖f a‖ ≤ ‖a‖ * ‖(1 : A)‖
```

structural index suggests:
  1. `NNRat.instCharZero`
  2. `Numbering.card_prefixed`
  3. `Nat.cast_choose`
  4. `Fintype.card_numbering`
  5. `Finset.card_le_univ`

## q47  `WithTop.untop₀_eq_zero`
module: `Mathlib.Algebra.Order.WithTop.Untop0`

```lean
lemma untop₀_eq_zero {a : WithTop α} :
    a.untop₀ = 0 ↔ a = 0 ∨ a = ⊤
```

structural index: no suggestion for this item.

## q48  `MvPolynomial.isWeightedHomogeneous_of_total_degree_zero`
module: `Mathlib.RingTheory.MvPolynomial.WeightedHomogeneous`

```lean
theorem isWeightedHomogeneous_of_total_degree_zero [SemilatticeSup M] [OrderBot M] (w : σ → M)
    {p : MvPolynomial σ R} (hp : weightedTotalDegree w p = (⊥ : M)) :
    IsWeightedHomogeneous w p (⊥ : M)
```

structural index suggests:
  1. `MvPolynomial.mem_support_iff`
  2. `MvPolynomial.ext`
  3. `Finset.sum_congr`
  4. `MvPolynomial.coeff_monomial`
  5. `Finsupp.degree_eq_weight_one`
  6. `MvPolynomial.coeff_add`
  7. `MvPolynomial.coeff_weightedHomogeneousComponent`
  8. `Finset.prod_congr`
  9. `MvPowerSeries.coeff_eq_zero_of_lt_weightedOrder`
  10. `Finset.sum_eq_zero`

## q49  `MeasureTheory.condExp_min_stopping_time_ae_eq_restrict_le_const`
module: `Mathlib.Probability.Process.Stopping`

```lean
theorem condExp_min_stopping_time_ae_eq_restrict_le_const (hτ : IsStoppingTime ℱ τ) (i : ι)
    [SigmaFinite (μ.trim (hτ.min_const i).measurableSpace_le)] :
    μ[f | (hτ.min_const i).measurableSpace] =ᵐ[μ.restrict {x | τ x ≤ i}]
      μ[f | hτ.measurableSpace]
```

structural index suggests:
  1. `MeasureTheory.Measure.restrict_apply`
  2. `Measurable.aemeasurable`
  3. `MeasureTheory.Measure.ext`
  4. `MeasureTheory.ae_restrict_iff'`
  5. `MeasureTheory.Integrable.integrableOn`
  6. `MeasureTheory.integral_congr_ae`
  7. `MeasureTheory.withDensity_apply`
  8. `intervalIntegral.integral_of_le`
  9. `MeasureTheory.ae_restrict_of_ae`
  10. `MeasureTheory.AEStronglyMeasurable.ae_eq_mk`

## q50  `Submodule.linearMap_qext`
module: `Mathlib.LinearAlgebra.Quotient.Defs`

```lean
theorem linearMap_qext ⦃f g : M ⧸ p →ₛₗ[τ₁₂] M₂⦄ (h : f.comp p.mkQ = g.comp p.mkQ) : f = g
```

structural index suggests:
  1. `Submodule.ker_mkQ`
  2. `LinearMap.ext`
  3. `Submodule.mkQ_surjective`
  4. `Submodule.Quotient.mk_eq_zero`
  5. `Submodule.ext`
  6. `Submodule.mkQ_apply`
  7. `Submodule.range_subtype`
  8. `Submodule.range_mkQ`
  9. `LinearMap.mem_ker`
  10. `Submodule.map_smul''`
