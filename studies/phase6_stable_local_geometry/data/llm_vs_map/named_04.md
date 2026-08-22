# Premise retrieval — batch 04

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


## q31  `Topology.IsEmbedding.piMap`
module: `Mathlib.Topology.Constructions`

```lean
protected lemma Topology.IsEmbedding.piMap {f : ∀ i, A i → B i}
    (hf : ∀ i, IsEmbedding (f i)) : IsEmbedding (Pi.map f)
```

## q32  `Finset.union_sdiff_self_eq_union`
module: `Mathlib.Data.Finset.SDiff`

```lean
theorem union_sdiff_self_eq_union : s ∪ t \ s = s ∪ t
```

## q33  `AlgebraicGeometry.LocallyRingedSpace.restrictStalkIso_inv_eq_germ`
module: `Mathlib.Geometry.RingedSpace.LocallyRingedSpace`

```lean
lemma restrictStalkIso_inv_eq_germ :
    X.presheaf.germ (h.functor.obj V) (f x) ⟨x, hx, rfl⟩ ≫
      (X.restrictStalkIso h x).inv = (X.restrict h).presheaf.germ _ x hx
```

## q34  `Nat.size_bit`
module: `Mathlib.Data.Nat.Size`

```lean
theorem size_bit {b n} (h : bit b n ≠ 0) : size (bit b n) = succ (size n)
```

## q35  `CategoryTheory.Localization.Preadditive.neg'_add'_self`
module: `Mathlib.CategoryTheory.Localization.CalculusOfFractions.Preadditive`

```lean
lemma neg'_add'_self (f : L.obj X ⟶ L.obj Y) :
    add' W (neg' W f) f = L.map 0
```

## q36  `completedRiemannZeta₀_zero`
module: `Mathlib.NumberTheory.Harmonic.ZetaAsymp`

```lean
lemma completedRiemannZeta₀_zero : completedRiemannZeta₀ 0 = (γ - Complex.log (4 * π)) / 2 + 1
```

## q37  `UniformOnFun.postcomp_uniformContinuous`
module: `Mathlib.Topology.UniformSpace.UniformConvergenceTopology`

```lean
protected theorem postcomp_uniformContinuous [UniformSpace γ] {f : γ → β}
    (hf : UniformContinuous f) : UniformContinuous (ofFun 𝔖 ∘ (f ∘ ·) ∘ toFun 𝔖)
```

## q38  `AddLECancellable.tsub_eq_iff_eq_add_of_le`
module: `Mathlib.Algebra.Order.Sub.Unbundled.Basic`

```lean
protected theorem tsub_eq_iff_eq_add_of_le (hb : AddLECancellable b) (h : b ≤ a) :
    a - b = c ↔ a = c + b
```

## q39  `hasSum_coe_mul_geometric_of_norm_lt_one`
module: `Mathlib.Analysis.SpecificLimits.Normed`

```lean
theorem hasSum_coe_mul_geometric_of_norm_lt_one {r : 𝕜} (hr : ‖r‖ < 1) :
    HasSum (fun n ↦ n * r ^ n : ℕ → 𝕜) (r / (1 - r) ^ 2)
```

## q40  `finprod_mem_eq_finite_toFinset_prod`
module: `Mathlib.Algebra.BigOperators.Finprod`

```lean
theorem finprod_mem_eq_finite_toFinset_prod (f : α → M) {s : Set α} (hs : s.Finite) :
    ∏ᶠ i ∈ s, f i = ∏ i ∈ hs.toFinset, f i
```
