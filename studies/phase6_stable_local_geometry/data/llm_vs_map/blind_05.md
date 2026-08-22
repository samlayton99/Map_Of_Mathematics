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
{"q01": ["Name.one", "Name.two", ...], "q02": [...], ...}

---


## q41

```lean
theorem target_thm {f : β → α} (hf : Cauchy (map f cofinite)) :
    IsBounded (range f)
```

## q42

```lean
theorem leval_eq_smeval.target_thm {R : Type*} [Semiring R] (r : R) :
    leval r = smeval.target_thm R r
```

## q43

```lean
lemma target_thm {x : ℝ} : DifferentiableAt ℝ negMulLog x ↔ x ≠ 0
```

## q44

```lean
lemma target_thm : ∀ n, n ≤ fib n + 1
  | 0 => zero_le_one
  | 1 => one_le_two
  | 2 => le_rfl
  | 3 => le_rfl
  | 4 => le_rfl
  | _n + 5 => (le_fib_self le_add_self).trans <| le_succ _
```

## q45

```lean
def target_thm : Module.End R M →ₐ[R] Module.End R (N ⊗[R] M)
```

## q46

```lean
theorem target_thm [FunLike F A 𝕜] [AlgHomClass F 𝕜 A 𝕜] (f : F) (a : A) :
    ‖f a‖ ≤ ‖a‖ * ‖(1 : A)‖
```

## q47

```lean
lemma target_thm {a : WithTop α} :
    a.untop₀ = 0 ↔ a = 0 ∨ a = ⊤
```

## q48

```lean
theorem target_thm [SemilatticeSup M] [OrderBot M] (w : σ → M)
    {p : MvPolynomial σ R} (hp : weightedTotalDegree w p = (⊥ : M)) :
    IsWeightedHomogeneous w p (⊥ : M)
```

## q49

```lean
theorem target_thm (hτ : IsStoppingTime ℱ τ) (i : ι)
    [SigmaFinite (μ.trim (hτ.min_const i).measurableSpace_le)] :
    μ[f | (hτ.min_const i).measurableSpace] =ᵐ[μ.restrict {x | τ x ≤ i}]
      μ[f | hτ.measurableSpace]
```

## q50

```lean
theorem target_thm ⦃f g : M ⧸ p →ₛₗ[τ₁₂] M₂⦄ (h : f.comp p.mkQ = g.comp p.mkQ) : f = g
```
