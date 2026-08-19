# Review packet — `Function.Bijective.existsUnique_iff`

*domain file:* Logic_Function_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
theorem Bijective.existsUnique_iff {f : α → β} (hf : Bijective f) {p : β → Prop} :
    (∃! y, p y) ↔ ∃! x, p (f x)
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V8:** `Function.Bijective`, `Iff.intro`, `ExistsUnique`, `_private.Basic.0.Function.Bijective.existsUnique_iff.match_1`, `Eq`, `_private.Basic.0.Function.Surjective.forall.match_1`, `Exists`, `Function.Bijective.surjective`
**V2:** `Eq`, `ExistsUnique`, `And`, `And.intro`, `Eq.mpr`, `Eq.rec`, `Exists`, `Exists.intro`
**V7:** `_private.Basic.0.Function.Bijective.existsUnique_iff.match_1`, `_private.Basic.0.Function.Bijective.existsUnique_iff.match_2`, `Function.Bijective.surjective`, `Function.Bijective.injective`, `_private.Basic.0.Function.Surjective.forall.match_1`, `And`, `And.intro`, `Eq`
**V3:** `Function.Bijective`, `ExistsUnique`, `Eq`, `Exists`, `Function.Bijective.surjective`, `And`, `Function.Bijective.injective`, `Iff.intro`
**V1:** `Function.Bijective.surjective`, `Function.Bijective.injective`, `Function.Bijective`, `Iff.intro`, `ExistsUnique`, `_private.Basic.0.Function.Bijective.existsUnique_iff.match_1`, `_private.Basic.0.Function.Bijective.existsUnique_iff.match_2`, `Eq`
**V4:** `ExistsUnique`, `Function.Bijective`, `Eq`, `Iff.intro`, `Exists.intro`, `_private.Basic.0.Function.Surjective.forall.match_1`, `_private.Basic.0.Function.Bijective.existsUnique_iff.match_1`, `_private.Basic.0.Function.Bijective.existsUnique_iff.match_2`
**V6:** `ExistsUnique`, `Function.Bijective`, `Eq`, `Iff.intro`, `Exists`, `Function.Bijective.surjective`, `_private.Basic.0.Function.Surjective.forall.match_1`, `_private.Basic.0.Function.Bijective.existsUnique_iff.match_1`
**V5:** `Function.Bijective.surjective`, `Function.Bijective.injective`, `ExistsUnique`, `Function.Bijective`, `Eq`, `Iff.intro`, `Exists`, `_private.Basic.0.Function.Surjective.forall.match_1`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
theorem Bijective.existsUnique_iff {f : α → β} (hf : Bijective f) {p : β → Prop} :
    (∃! y, p y) ↔ ∃! x, p (f x) :=
  ⟨fun ⟨y, hpy, hy⟩ ↦
    let ⟨x, hx⟩ := hf.surjective y
    ⟨x, by simpa [hx], fun z (hz : p (f z)) ↦ hf.injective <| hx.symm ▸ hy _ hz⟩,
    fun ⟨x, hpx, hx⟩ ↦
    ⟨f x, hpx, fun y hy ↦
      let ⟨z, hz⟩ := hf.surjective y
      hz ▸ congr_arg f (hx _ (by simpa [hz]))⟩⟩

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
