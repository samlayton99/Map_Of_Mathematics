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


## q31

```lean
protected lemma target_thm {f : ∀ i, A i → B i}
    (hf : ∀ i, IsEmbedding (f i)) : IsEmbedding (Pi.map f)
```

## q32

```lean
theorem target_thm : s ∪ t \ s = s ∪ t
```

## q33

```lean
lemma target_thm :
    X.presheaf.germ (h.functor.obj V) (f x) ⟨x, hx, rfl⟩ ≫
      (X.restrictStalkIso h x).inv = (X.restrict h).presheaf.germ _ x hx
```

## q34

```lean
theorem target_thm {b n} (h : bit b n ≠ 0) : size (bit b n) = succ (size n)
```

## q35

```lean
lemma target_thm (f : L.obj X ⟶ L.obj Y) :
    add' W (neg' W f) f = L.map 0
```

## q36

```lean
lemma target_thm : completedRiemannZeta₀ 0 = (γ - Complex.log (4 * π)) / 2 + 1
```

## q37

```lean
protected theorem target_thm [UniformSpace γ] {f : γ → β}
    (hf : UniformContinuous f) : UniformContinuous (ofFun 𝔖 ∘ (f ∘ ·) ∘ toFun 𝔖)
```

## q38

```lean
protected theorem target_thm (hb : AddLECancellable b) (h : b ≤ a) :
    a - b = c ↔ a = c + b
```

## q39

```lean
theorem target_thm {r : 𝕜} (hr : ‖r‖ < 1) :
    HasSum (fun n ↦ n * r ^ n : ℕ → 𝕜) (r / (1 - r) ^ 2)
```

## q40

```lean
theorem target_thm (f : α → M) {s : Set α} (hs : s.Finite) :
    ∏ᶠ i ∈ s, f i = ∏ i ∈ hs.toFinset, f i
```
