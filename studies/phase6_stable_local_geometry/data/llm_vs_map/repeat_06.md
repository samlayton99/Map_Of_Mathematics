# Premise retrieval — batch 06

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


## q51  `Finsupp.mem_range_embDomain_iff`
module: `Mathlib.Data.Finsupp.Basic`

```lean
lemma mem_range_embDomain_iff [AddCommMonoid M] (f : α ↪ β) (x : β →₀ M) :
    x ∈ Set.range (embDomain f) ↔ ↑x.support ⊆ Set.range f
```

## q52  `eventually_singleton_add_smul_subset`
module: `Mathlib.Analysis.Normed.Module.Ball.Pointwise`

```lean
theorem eventually_singleton_add_smul_subset {x : E} {s : Set E} (hs : Bornology.IsBounded s)
    {u : Set E} (hu : u ∈ 𝓝 x) : ∀ᶠ r in 𝓝 (0 : 𝕜), {x} + r • s ⊆ u
```

## q53  `Matrix.adjugate_fin_two`
module: `Mathlib.LinearAlgebra.Matrix.Adjugate`

```lean
theorem adjugate_fin_two (A : Matrix (Fin 2) (Fin 2) α) :
    adjugate A = !![A 1 1, -A 0 1; -A 1 0, A 0 0]
```

## q54  `TopCat.nonempty_isColimit_iff_eq_coinduced`
module: `Mathlib.Topology.Category.TopCat.Limits.Basic`

```lean
lemma nonempty_isColimit_iff_eq_coinduced (c : Cocone F) (hc : IsColimit ((forget).mapCocone c)) :
    Nonempty (IsColimit c) ↔ c.pt.str = ⨆ j, (F.obj j).str.coinduced (c.ι.app j)
```

## q55  `Set.uIoc_eq_union`
module: `Mathlib.Order.Interval.Set.UnorderedInterval`

```lean
lemma uIoc_eq_union : Ι a b = Ioc a b ∪ Ioc b a
```

## q56  `Real.closedBall_eq_Icc`
module: `Mathlib.Topology.MetricSpace.Pseudo.Defs`

```lean
theorem Real.closedBall_eq_Icc {x r : ℝ} : closedBall x r = Icc (x - r) (x + r)
```

## q57  `MeasureTheory.lpMeasToLpTrimLie_symm_indicator`
module: `Mathlib.MeasureTheory.Function.ConditionalExpectation.AEMeasurable`

```lean
theorem lpMeasToLpTrimLie_symm_indicator [one_le_p : Fact (1 ≤ p)] [NormedSpace ℝ F] {hm : m ≤ m0}
    {s : Set α} {μ : Measure α} (hs : MeasurableSet[m] s) (hμs : μ.trim hm s ≠ ∞) (c : F) :
    ((lpMeasToLpTrimLie F ℝ p μ hm).symm (indicatorConstLp p hs hμs c) : Lp F p μ) =
      indicatorConstLp p (hm s hs) ((le_trim hm).trans_lt hμs.lt_top).ne c
```

## q58  `Finset.inter_sdiff_left_comm`
module: `Mathlib.Data.Finset.SDiff`

```lean
lemma inter_sdiff_left_comm (s t u : Finset α) : s ∩ (t \ u) = t ∩ (s \ u)
```

## q59  `RCLike.ofReal_finsupp_sum`
module: `Mathlib.Analysis.RCLike.Basic`

```lean
theorem ofReal_finsupp_sum {α M : Type*} [Zero M] (f : α →₀ M) (g : α → M → ℝ) :
    ((f.sum fun a b => g a b : ℝ) : K) = f.sum fun a b => (g a b : K)
```

## q60  `AddCircle.exists_gcd_eq_one_of_isOfFinAddOrder`
module: `Mathlib.Topology.Instances.AddCircle.Defs`

```lean
theorem exists_gcd_eq_one_of_isOfFinAddOrder {u : AddCircle p} (h : IsOfFinAddOrder u) :
    ∃ m : ℕ, m.gcd (addOrderOf u) = 1 ∧ m < addOrderOf u ∧ ↑((m : 𝕜) / addOrderOf u * p) = u
```
