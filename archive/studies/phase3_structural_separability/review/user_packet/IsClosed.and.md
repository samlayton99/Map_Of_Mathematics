# Review packet — `IsClosed.and`

*domain file:* Topology_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[closedness .]
theorem IsClosed.and :
    IsClosed { x | p₁ x } → IsClosed { x | p₂ x } → IsClosed { x | p₁ x ∧ p₂ x }
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V7:** `TopologicalSpace`, `IsClosed.inter`, `Set.ofPred`
**V1:** `Set.ofPred`, `IsClosed.inter`, `TopologicalSpace`
**V3:** `IsClosed.inter`, `Set.ofPred`, `TopologicalSpace`
**V4:** `TopologicalSpace`, `IsClosed.inter`, `Set.ofPred`
**V2:** `IsClosed.inter`, `TopologicalSpace`, `Set.ofPred`
**V8:** `TopologicalSpace`, `Set.ofPred`, `IsClosed.inter`
**V6:** `TopologicalSpace`, `Set.ofPred`, `IsClosed.inter`
**V5:** `IsClosed.inter`, `TopologicalSpace`, `Set.ofPred`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[closedness .]
theorem IsClosed.and :
    IsClosed { x | p₁ x } → IsClosed { x | p₂ x } → IsClosed { x | p₁ x ∧ p₂ x } :=
  IsClosed.inter

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
