# Review packet — `limUnder_of_not_tendsto`

*domain file:* Topology_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
theorem limUnder_of_not_tendsto [hX : Nonempty X] {f : Filter α} {g : α → X}
    (h : ¬ ∃ x, Tendsto g f (𝓝 x)) :
    limUnder f g = Classical.choice hX
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V1:** `TopologicalSpace`, `Nonempty`, `Filter`, `Not`, `Exists`, `Filter.Tendsto`, `nhds`, `id`
**V3:** `Filter`, `Filter.map`, `nhds`, `Filter.instPartialOrder`, `LE.le`, `PartialOrder.toPreorder`, `Preorder.toLE`, `Exists`
**V5:** `Classical.choice`, `Classical.epsilon`, `Classical.indefiniteDescription`, `Classical.propDecidable`, `Classical.strongIndefiniteDescription`, `Classical.strongIndefiniteDescription._proof_1`, `Classical.strongIndefiniteDescription._proof_2`, `Decidable`
**V7:** `TopologicalSpace`, `Nonempty`, `Filter`, `Not`, `Exists`, `Filter.Tendsto`, `nhds`, `Eq`
**V2:** `of_eq_true`, `congrFun'`, `eq_self`, `dif_neg`, `Filter`, `Nonempty`, `Not`, `TopologicalSpace`
**V8:** `Filter`, `Not`, `Exists`, `Filter.Tendsto`, `Filter.limUnder`, `nhds`, `Nonempty`, `TopologicalSpace`
**V4:** `Filter`, `Exists`, `TopologicalSpace`, `Filter.Tendsto`, `Nonempty`, `Eq`, `Not`, `Filter.limUnder`
**V6:** `Filter.Tendsto`, `Filter.limUnder`, `Classical.epsilon`, `Classical.strongIndefiniteDescription`, `Filter.lim`, `dif_neg`, `eq_self`, `of_eq_true`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
theorem limUnder_of_not_tendsto [hX : Nonempty X] {f : Filter α} {g : α → X}
    (h : ¬ ∃ x, Tendsto g f (𝓝 x)) :
    limUnder f g = Classical.choice hX := by
  simp_rw [Tendsto] at h
  simp_rw [limUnder, lim, Classical.epsilon, Classical.strongIndefiniteDescription, dif_neg h]

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
