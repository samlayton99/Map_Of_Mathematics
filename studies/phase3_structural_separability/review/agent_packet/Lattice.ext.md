# Review packet — `Lattice.ext`

*domain file:* Order_Lattice

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[to_dual self]
theorem Lattice.ext {α} {A B : Lattice α} (H : ∀ x y : α, (haveI := A; x ≤ y) ↔ x ≤ y) :
    A = B
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V4:** `Lattice`, `Iff`, `LE.le`, `Preorder.toLE`, `PartialOrder.toPreorder`, `SemilatticeInf.toPartialOrder`, `Lattice.toSemilatticeInf`, `Lattice.casesOn`
**V7:** `Lattice.mk`, `Lattice.toSemilatticeSup`, `Lattice.toSemilatticeInf`, `LE.le`, `PartialOrder.toPreorder`, `Preorder.toLE`, `Eq`, `SemilatticeSup.toPartialOrder`
**V1:** `SemilatticeSup.ext`, `SemilatticeInf.ext`, `SemilatticeInf.mk.noConfusion`, `Lattice.casesOn`, `Lattice.toSemilatticeInf`, `Lattice.le_inf`, `Lattice.inf_le_left`, `Lattice.inf_le_right`
**V2:** `Lattice`, `Iff`, `Eq`, `SemilatticeSup`, `Lattice.mk`, `HEq`, `SemilatticeSup.ext`, `SemilatticeInf`
**V8:** `HEq.refl`, `SemilatticeSup.ext`, `SemilatticeInf.ext`, `eq_of_heq`, `Iff`, `Lattice`, `Lattice.casesOn`, `Eq`
**V6:** `Lattice`, `Iff`, `LE.le`, `Eq`, `Preorder.toLE`, `PartialOrder.toPreorder`, `Lattice.toSemilatticeInf`, `SemilatticeSup.ext`
**V3:** `Lattice`, `Eq`, `SemilatticeSup.ext`, `SemilatticeInf.ext`, `Lattice.toSemilatticeInf`, `Iff`, `SemilatticeSup`, `LE.le`
**V5:** `SemilatticeSup.ext`, `SemilatticeInf.ext`, `HEq.refl`, `eq_of_heq`, `Lattice`, `Eq`, `Lattice.toSemilatticeInf`, `Iff`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[to_dual self]
theorem Lattice.ext {α} {A B : Lattice α} (H : ∀ x y : α, (haveI := A; x ≤ y) ↔ x ≤ y) :
    A = B := by
  cases A
  cases B
  cases SemilatticeSup.ext H
  cases SemilatticeInf.ext H
  congr

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
