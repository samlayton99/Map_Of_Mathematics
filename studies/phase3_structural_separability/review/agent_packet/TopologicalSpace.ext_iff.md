# Review packet — `TopologicalSpace.ext_iff`

*domain file:* Topology_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
protected theorem TopologicalSpace.ext_iff {t t' : TopologicalSpace X} :
    t = t' ↔ ∀ s, IsOpen[t] s ↔ IsOpen[t'] s
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V8:** `TopologicalSpace`, `Iff.intro`, `Eq`, `Set`, `Iff`, `IsOpen`, `Eq.rec`, `Iff.rfl`
**V4:** `IsOpen`, `TopologicalSpace`, `Set`, `Eq`, `Iff`, `Eq.rec`, `Iff.intro`, `Iff.rfl`
**V2:** `TopologicalSpace.ext`, `Eq`, `Eq.rec`, `Iff`, `Iff.intro`, `Iff.rfl`, `IsOpen`, `Set`
**V3:** `TopologicalSpace`, `Eq`, `Set`, `Iff`, `IsOpen`, `TopologicalSpace.ext`, `Iff.intro`, `Eq.rec`
**V6:** `TopologicalSpace.ext`, `Iff.intro`, `TopologicalSpace`, `Eq`, `Eq.rec`, `Iff`, `Set`, `Iff.rfl`
**V1:** `TopologicalSpace`, `IsOpen`, `Set`, `Eq`, `Iff`, `Iff.intro`, `Eq.rec`, `TopologicalSpace.ext`
**V5:** `TopologicalSpace`, `Set`, `IsOpen`, `Eq`, `Iff.intro`, `Iff`, `TopologicalSpace.ext`, `funext`
**V7:** `TopologicalSpace.ext`, `TopologicalSpace`, `Set`, `IsOpen`, `Eq`, `Iff.intro`, `Iff`, `funext`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
protected theorem TopologicalSpace.ext_iff {t t' : TopologicalSpace X} :
    t = t' ↔ ∀ s, IsOpen[t] s ↔ IsOpen[t'] s :=
  ⟨fun h _ => h ▸ Iff.rfl, fun h => by ext; exact h _⟩

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
