# Review packet — `Function.Injective.isPartialInv`

*domain file:* Logic_Function_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
theorem Injective.isPartialInv {α β} {f : α → β} (I : Injective f) : IsPartialInv f (partialInv f)
  | a, b =>
  ⟨fun h =>
    open scoped Classical in
    have hpi : partialInv f b = if h : ∃ a, f a = b then some (Classical.choose h) else none
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V5:** `Function.Injective`, `_private.Basic.0.Function.Injective.isPartialInv.match_1`, `Iff`, `Eq`, `Option`, `Function.partialInv`, `Option.some`, `Iff.intro`
**V4:** `Eq`, `Exists`, `Option`, `Option.some`, `Classical.choose`, `Option.none`, `Classical.propDecidable`, `Not`
**V6:** `Function.partialInv`, `Classical.choose`, `Classical.choose_spec`, `Classical.propDecidable`, `Eq`, `Eq.mp`, `Eq.ndrec`, `Eq.rec`
**V3:** `Function.Injective`, `Iff`, `Eq`, `Option`, `Function.partialInv`, `Option.some`, `dite`, `Exists`
**V7:** `dif_pos`, `noConfusion_of_Nat`, `Classical.choose_spec`, `eq_of_heq`, `dif_neg`, `Function.Injective`, `_private.Basic.0.Function.Injective.isPartialInv.match_1`, `Iff`
**V2:** `Function.Injective`, `Function.partialInv`, `_private.Basic.0.Function.Injective.isPartialInv.match_1`, `Eq`, `dif_pos`, `Classical.choose_spec`, `Exists`, `dif_neg`
**V1:** `Function.Injective`, `Function.partialInv`, `Eq`, `_private.Basic.0.Function.Injective.isPartialInv.match_1`, `Classical.choose_spec`, `dif_pos`, `Option`, `Exists`
**V8:** `Classical.choose_spec`, `dif_pos`, `dif_neg`, `noConfusion_of_Nat`, `eq_of_heq`, `Function.Injective`, `Function.partialInv`, `Eq`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
theorem Injective.isPartialInv {α β} {f : α → β} (I : Injective f) : IsPartialInv f (partialInv f)
  | a, b =>
  ⟨fun h =>
    open scoped Classical in
    have hpi : partialInv f b = if h : ∃ a, f a = b then some (Classical.choose h) else none :=
      rfl
    if h' : ∃ a, f a = b
    then by rw [hpi, dif_pos h'] at h
            injection h with h
            subst h
            apply Classical.choose_spec h'
    else by rw [hpi, dif_neg h'] at h; contradiction,
  fun e => e ▸ have h : ∃ a', f a' = f a := ⟨_, rfl⟩
              (dif_pos h).trans (congr_arg _ (I <| Classical.choose_spec h))⟩

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
