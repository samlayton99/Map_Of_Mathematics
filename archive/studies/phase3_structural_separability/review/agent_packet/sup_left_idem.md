# Review packet — `sup_left_idem`

*domain file:* Order_Lattice

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[to_dual]
theorem sup_left_idem (a b : α) : a ⊔ (a ⊔ b) = a ⊔ b
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V7:** `SemilatticeSup`, `of_eq_true`, `Eq`, `Max.max`, `SemilatticeSup.toMax`, `Eq.trans`, `True`, `congrFun'`
**V3:** `Max.max`, `SemilatticeSup.toMax`, `Eq`, `of_eq_true`, `Eq.trans`, `LE.le`, `PartialOrder.toPreorder`, `Preorder.toLE`
**V8:** `SemilatticeSup.toMax`, `sup_of_le_right`, `le_sup_left._simp_1`, `SemilatticeSup.toPartialOrder`, `Eq`, `Eq.trans`, `LE.le`, `Max.max`
**V6:** `SemilatticeSup`, `of_eq_true`, `Eq`, `True`, `congrFun'`, `sup_of_le_right`, `eq_self`, `Max.max`
**V2:** `of_eq_true`, `congrFun'`, `eq_self`, `sup_of_le_right`, `SemilatticeSup`, `Eq`, `Eq.trans`, `Max.max`
**V1:** `Max.max`, `SemilatticeSup.toMax`, `SemilatticeSup`, `Eq`, `of_eq_true`, `Eq.trans`, `True`, `congrFun'`
**V4:** `SemilatticeSup`, `Eq`, `Max.max`, `SemilatticeSup.toMax`, `of_eq_true`, `sup_of_le_right`, `le_sup_left._simp_1`, `eq_self`
**V5:** `of_eq_true`, `sup_of_le_right`, `eq_self`, `congrFun'`, `SemilatticeSup`, `Eq`, `Max.max`, `SemilatticeSup.toMax`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[to_dual]
theorem sup_left_idem (a b : α) : a ⊔ (a ⊔ b) = a ⊔ b := by simp

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
