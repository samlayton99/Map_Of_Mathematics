# Review packet — `sup_eq_and_inf_eq_iff`

*domain file:* Order_Lattice

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[to_dual]

```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V4:** `Lattice`, `Iff.intro`, `And`, `Eq`, `Max.max`, `SemilatticeSup.toMax`, `Lattice.toSemilatticeSup`, `Min.min`
**V1:** `Eq`, `Lattice.toSemilatticeSup`, `Lattice.toSemilatticeInf`, `And`, `Max.max`, `SemilatticeSup.toMax`, `Min.min`, `SemilatticeInf.toMin`
**V7:** `inf_eq_sup`, `inf_idem`, `inf_of_le_left`, `sup_of_le_left`, `sup_idem`, `SemilatticeSup.toMax`, `SemilatticeInf.toMin`, `Lattice.toSemilatticeInf`
**V2:** `Lattice`, `And`, `Eq`, `and_self`, `congrFun'`, `sup_of_le_left`, `of_eq_true`, `eq_true`
**V6:** `inf_eq_sup`, `and_self`, `inf_idem`, `sup_idem`, `congrFun'`, `inf_of_le_left`, `of_eq_true`, `sup_of_le_left`
**V3:** `Eq`, `Lattice`, `And`, `Max.max`, `Lattice.toSemilatticeSup`, `Min.min`, `SemilatticeSup.toMax`, `Lattice.toSemilatticeInf`
**V8:** `Lattice`, `Eq`, `And`, `Lattice.toSemilatticeInf`, `Max.max`, `Min.min`, `SemilatticeSup.toMax`, `SemilatticeInf.toMin`
**V5:** `inf_eq_sup`, `inf_idem`, `sup_idem`, `and_self`, `inf_of_le_left`, `sup_of_le_left`, `Std.ge_refl`, `eq_true`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[to_dual]

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
