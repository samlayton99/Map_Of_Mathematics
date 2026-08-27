# Review packet — `isClosed_sInter`

*domain file:* Topology_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[closedness .]
theorem isClosed_sInter {s : Set (Set X)} : (∀ t ∈ s, IsClosed t) → IsClosed (⋂₀ s)
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V3:** `TopologicalSpace`, `Set`, `Eq.mpr`, `Membership.mem`, `Set.instMembership`, `IsClosed`, `Set.sInter`, `IsOpen`
**V1:** `Set`, `Membership.mem`, `Set.instMembership`, `Compl.compl`, `Set.instCompl`, `Set.iUnion`, `IsOpen`, `IsClosed`
**V7:** `isOpen_biUnion`, `_private.Basic.0.IsClosed.union._simp_1`, `Compl.compl`, `Eq`, `Eq.mpr`, `Eq.refl`, `Eq.trans`, `IsClosed`
**V6:** `TopologicalSpace`, `Set`, `IsClosed`, `Set.sInter`, `IsOpen`, `Set.iUnion`, `Eq`, `implies_congr`
**V5:** `isOpen_biUnion`, `implies_congr`, `forall_congr`, `Set.compl_sInter`, `Set.sUnion_image`, `Eq.mpr`, `Set`, `TopologicalSpace`
**V8:** `Set`, `Membership.mem`, `TopologicalSpace`, `Set.instMembership`, `IsClosed`, `Set.sInter`, `Eq.mpr`, `IsOpen`
**V2:** `Set`, `TopologicalSpace`, `IsClosed`, `Membership.mem`, `Set.sInter`, `Set.instMembership`, `IsOpen`, `Set.iUnion`
**V4:** `implies_congr`, `Set.compl_sInter`, `Set.sUnion_image`, `isOpen_biUnion`, `forall_congr`, `Set`, `TopologicalSpace`, `IsClosed`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[closedness .]
theorem isClosed_sInter {s : Set (Set X)} : (∀ t ∈ s, IsClosed t) → IsClosed (⋂₀ s) := by
  simpa only [← isOpen_compl_iff, compl_sInter, sUnion_image] using isOpen_biUnion

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
