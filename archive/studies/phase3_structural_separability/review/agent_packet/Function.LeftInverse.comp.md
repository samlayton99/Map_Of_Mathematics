# Review packet — `Function.LeftInverse.comp`

*domain file:* Logic_Function_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
theorem LeftInverse.comp {f : α → β} {g : β → α} {h : β → γ} {i : γ → β} (hf : LeftInverse f g)
    (hh : LeftInverse h i) : LeftInverse (h ∘ f) (g ∘ i)
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V3:** `Function.LeftInverse`, `Eq`, `Eq.mpr`, `id`, `congrArg`, `Eq.refl`
**V1:** `Eq`, `Eq.mpr`, `Function.LeftInverse`, `congrArg`, `id`, `Eq.refl`
**V2:** `Eq`, `Eq.mpr`, `Eq.refl`, `Function.LeftInverse`, `congrArg`, `id`
**V4:** `Function.LeftInverse`, `Eq`, `Eq.mpr`, `id`, `congrArg`, `Eq.refl`
**V6:** `Eq`, `Eq.mpr`, `Function.LeftInverse`, `id`, `Eq.refl`, `congrArg`
**V5:** `Function.LeftInverse`, `Eq`, `Eq.mpr`, `id`, `congrArg`, `Eq.refl`
**V7:** `Eq`, `Function.LeftInverse`, `Eq.mpr`, `id`, `congrArg`, `Eq.refl`
**V8:** `Eq`, `Function.LeftInverse`, `Eq.mpr`, `id`, `congrArg`, `Eq.refl`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
theorem LeftInverse.comp {f : α → β} {g : β → α} {h : β → γ} {i : γ → β} (hf : LeftInverse f g)
    (hh : LeftInverse h i) : LeftInverse (h ∘ f) (g ∘ i) :=
  fun a ↦ show h (f (g (i a))) = a by rw [hf (i a), hh a]

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
