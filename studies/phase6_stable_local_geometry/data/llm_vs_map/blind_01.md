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
{"q01": ["Name.one", "Name.two", ...], "q02": [...], ...}

---


## q01

```lean
theorem target_thm (a : R) : (a • Q).discr' = a ^ Fintype.card n * Q.discr'
```

## q02

```lean
protected theorem target_thm
    [NormedField 𝕜] [NormedRing 𝕜'] [NormedAlgebra 𝕜 𝕜'] [Nontrivial 𝕜']
    [Zero E] [TopologicalSpace E]
    [SMul 𝕜 E] [MulAction 𝕜' E] [IsScalarTower 𝕜 𝕜' E] {s : Set E}
    (h : IsVonNBounded 𝕜' s) : IsVonNBounded 𝕜 s
```

## q03

```lean
theorem target_thm (L : ListBlank (∀ k, Option (Γ k))) :
    (addBottom L).map ⟨Prod.snd, by rfl⟩ = L
```

## q04

```lean
theorem target_thm {X : Ω → E} {s : Set E}
    (hu : IsUniform X s ℙ μ) (hμs : μ s = 0 ∨ μ s = ∞) : pdf X ℙ μ =ᵐ[μ] 0
```

## q05

```lean
lemma target_thm {g : ℝ → ℝ} {t : ℝ}
    (hg : Tendsto (fun x ↦ x * g x) atTop (𝓝 t)) :
    Tendsto (fun x ↦ x * log (1 + g x)) atTop (𝓝 t)
```

## q06

```lean
def target_thm [Subsingleton ι] (i : ι) :
    (G →L[𝕜] G') ≃ₗᵢ[𝕜] ContinuousMultilinearMap 𝕜 (fun _ : ι ↦ G) G'
```

## q07

```lean
theorem target_thm (h : x ∈ F) : x ∈ pathComponentIn F x
```

## q08

```lean
noncomputable def target_thm (hf : IsSigmaSubadditiveSetFun f) (hf' : f ∅ = 0) :
    VectorMeasure X ℝ≥0∞
```

## q09

```lean
theorem target_thm {r : ℝ} (hr : r ≠ 0) :
    HasFPowerSeriesOnBall (fun x ↦ 1 / (r - x)) (.ofScalars ℝ fun n ↦ (r ^ (n + 1))⁻¹) 0 ‖r‖ₑ
```

## q10

```lean
theorem target_thm (l : Filter α) :
    HasBasis l.smallSets (fun t : Set α => t ∈ l) powerset
```
