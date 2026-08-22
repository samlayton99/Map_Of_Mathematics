# Premise retrieval — batch 02

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


## q11  `MeasureTheory.IsStoppingTime.piecewise_of_le`
module: `Mathlib.Probability.Process.Stopping`

```lean
theorem IsStoppingTime.piecewise_of_le (hτ_st : IsStoppingTime 𝒢 τ) (hη_st : IsStoppingTime 𝒢 η)
    (hτ : ∀ ω, i ≤ τ ω) (hη : ∀ ω, i ≤ η ω) (hs : MeasurableSet[𝒢 i] s) :
    IsStoppingTime 𝒢 (s.piecewise τ η)
```

## q12  `PartialEquiv.trans_refl`
module: `Mathlib.Logic.Equiv.PartialEquiv`

```lean
theorem trans_refl : e.trans (PartialEquiv.refl β) = e
```

## q13  `Multiset.nodup_iff_pairwise`
module: `Mathlib.Data.Multiset.Replicate`

```lean
theorem nodup_iff_pairwise {α} {s : Multiset α} : Nodup s ↔ Pairwise (· ≠ ·) s
```

## q14  `PerfectRing.lift_comp_lift_apply_eq_self`
module: `Mathlib.FieldTheory.IsPerfectClosure`

```lean
theorem lift_comp_lift_apply_eq_self [PerfectRing L p] (x : L) :
    lift j i p (lift i j p x) = x
```

## q15  `Matrix.permanent_zero`
module: `Mathlib.LinearAlgebra.Matrix.Permanent`

```lean
theorem permanent_zero [Nonempty n] : permanent (0 : Matrix n n R) = 0
```

## q16  `Finset.piecewise_piecewise_of_subset_left`
module: `Mathlib.Data.Finset.Piecewise`

```lean
lemma piecewise_piecewise_of_subset_left {s t : Finset ι} [∀ i, Decidable (i ∈ s)]
    [∀ i, Decidable (i ∈ t)] (h : s ⊆ t) (f₁ f₂ g : ∀ a, π a) :
    s.piecewise (t.piecewise f₁ f₂) g = s.piecewise f₁ g
```

## q17  `CategoryTheory.Limits.biproduct.matrixEquiv`
module: `Mathlib.CategoryTheory.Limits.Shapes.Biproducts`

```lean
def biproduct.matrixEquiv : (⨁ f ⟶ ⨁ g) ≃ ∀ j k, f j ⟶ g k
```

## q18  `ciInf_mono`
module: `Mathlib.Order.ConditionallyCompleteLattice.Indexed`

```lean
theorem ciInf_mono {f g : ι → α} (B : BddBelow (range f)) (H : ∀ x, f x ≤ g x) : iInf f ≤ iInf g
```

## q19  `SubMulAction.val_preimage_orbit`
module: `Mathlib.GroupTheory.GroupAction.SubMulAction`

```lean
theorem val_preimage_orbit {p : SubMulAction R M} (m : p) :
    Subtype.val ⁻¹' MulAction.orbit R (m : M) = MulAction.orbit R m
```

## q20  `IsLocallyConstant.of_constant_on_connected_clopens`
module: `Mathlib.Topology.LocallyConstant.Basic`

```lean
theorem of_constant_on_connected_clopens [LocallyConnectedSpace X] {f : X → Y}
    (h : ∀ U : Set X, IsConnected U → IsClopen U → ∀ x ∈ U, ∀ y ∈ U, f y = f x) :
    IsLocallyConstant f
```
