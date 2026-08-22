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


## q11

```lean
theorem IsStoppingTime.target_thm (hτ_st : IsStoppingTime 𝒢 τ) (hη_st : IsStoppingTime 𝒢 η)
    (hτ : ∀ ω, i ≤ τ ω) (hη : ∀ ω, i ≤ η ω) (hs : MeasurableSet[𝒢 i] s) :
    IsStoppingTime 𝒢 (s.piecewise τ η)
```

## q12

```lean
theorem target_thm : e.trans (PartialEquiv.refl β) = e
```

## q13

```lean
theorem target_thm {α} {s : Multiset α} : Nodup s ↔ Pairwise (· ≠ ·) s
```

## q14

```lean
theorem target_thm [PerfectRing L p] (x : L) :
    lift j i p (lift i j p x) = x
```

## q15

```lean
theorem target_thm [Nonempty n] : permanent (0 : Matrix n n R) = 0
```

## q16

```lean
lemma target_thm {s t : Finset ι} [∀ i, Decidable (i ∈ s)]
    [∀ i, Decidable (i ∈ t)] (h : s ⊆ t) (f₁ f₂ g : ∀ a, π a) :
    s.piecewise (t.piecewise f₁ f₂) g = s.piecewise f₁ g
```

## q17

```lean
def biproduct.target_thm : (⨁ f ⟶ ⨁ g) ≃ ∀ j k, f j ⟶ g k
```

## q18

```lean
theorem target_thm {f g : ι → α} (B : BddBelow (range f)) (H : ∀ x, f x ≤ g x) : iInf f ≤ iInf g
```

## q19

```lean
theorem target_thm {p : SubMulAction R M} (m : p) :
    Subtype.val ⁻¹' MulAction.orbit R (m : M) = MulAction.orbit R m
```

## q20

```lean
theorem target_thm [LocallyConnectedSpace X] {f : X → Y}
    (h : ∀ U : Set X, IsConnected U → IsClopen U → ∀ x ∈ U, ∀ y ∈ U, f y = f x) :
    IsLocallyConstant f
```
