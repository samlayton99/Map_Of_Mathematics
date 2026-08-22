# Premise retrieval — batch 05

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


## q41  `Metric.isBounded_range_of_cauchy_map_cofinite`
module: `Mathlib.Topology.MetricSpace.Bounded`

```lean
theorem isBounded_range_of_cauchy_map_cofinite {f : β → α} (hf : Cauchy (map f cofinite)) :
    IsBounded (range f)
```

## q42  `Polynomial.leval_eq_smeval.linearMap`
module: `Mathlib.Algebra.Polynomial.Smeval`

```lean
theorem leval_eq_smeval.linearMap {R : Type*} [Semiring R] (r : R) :
    leval r = smeval.linearMap R r
```

## q43  `Real.differentiableAt_negMulLog_iff`
module: `Mathlib.Analysis.SpecialFunctions.Log.NegMulLog`

```lean
lemma differentiableAt_negMulLog_iff {x : ℝ} : DifferentiableAt ℝ negMulLog x ↔ x ≠ 0
```

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

## q45  `Module.End.lTensorAlgHom`
module: `Mathlib.RingTheory.TensorProduct.Maps`

```lean
def lTensorAlgHom : Module.End R M →ₐ[R] Module.End R (N ⊗[R] M)
```

## q46  `AlgHom.norm_apply_le_self_mul_norm_one`
module: `Mathlib.Analysis.Normed.Algebra.Spectrum`

```lean
theorem norm_apply_le_self_mul_norm_one [FunLike F A 𝕜] [AlgHomClass F 𝕜 A 𝕜] (f : F) (a : A) :
    ‖f a‖ ≤ ‖a‖ * ‖(1 : A)‖
```

## q47  `WithTop.untop₀_eq_zero`
module: `Mathlib.Algebra.Order.WithTop.Untop0`

```lean
lemma untop₀_eq_zero {a : WithTop α} :
    a.untop₀ = 0 ↔ a = 0 ∨ a = ⊤
```

## q48  `MvPolynomial.isWeightedHomogeneous_of_total_degree_zero`
module: `Mathlib.RingTheory.MvPolynomial.WeightedHomogeneous`

```lean
theorem isWeightedHomogeneous_of_total_degree_zero [SemilatticeSup M] [OrderBot M] (w : σ → M)
    {p : MvPolynomial σ R} (hp : weightedTotalDegree w p = (⊥ : M)) :
    IsWeightedHomogeneous w p (⊥ : M)
```

## q49  `MeasureTheory.condExp_min_stopping_time_ae_eq_restrict_le_const`
module: `Mathlib.Probability.Process.Stopping`

```lean
theorem condExp_min_stopping_time_ae_eq_restrict_le_const (hτ : IsStoppingTime ℱ τ) (i : ι)
    [SigmaFinite (μ.trim (hτ.min_const i).measurableSpace_le)] :
    μ[f | (hτ.min_const i).measurableSpace] =ᵐ[μ.restrict {x | τ x ≤ i}]
      μ[f | hτ.measurableSpace]
```

## q50  `Submodule.linearMap_qext`
module: `Mathlib.LinearAlgebra.Quotient.Defs`

```lean
theorem linearMap_qext ⦃f g : M ⧸ p →ₛₗ[τ₁₂] M₂⦄ (h : f.comp p.mkQ = g.comp p.mkQ) : f = g
```
