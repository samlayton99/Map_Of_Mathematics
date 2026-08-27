# Review packet — `Real.one_sub_inv_le_log_of_pos`

*domain file:* Analysis_SpecialFunctions_Log_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
lemma one_sub_inv_le_log_of_pos (hx : 0 < x) : 1 - x⁻¹ ≤ log x
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V8:** `Real`, `LT.lt`, `Real.instLT`, `OfNat.ofNat`, `Zero.toOfNat0`, `Real.instZero`, `Eq.mpr`, `LE.le`
**V3:** `Real`, `Inv.inv`, `Real.log`, `Real.instLE`, `OfNat.ofNat`, `LE.le`, `DivisionSemiring.toGroupWithZero`, `Field.toSemifield`
**V5:** `Real.log_inv`, `DivisionMonoid.toDivInvOneMonoid`, `Real.log_le_sub_one_of_pos`, `Real.log`, `AddCommGroup.toAddGroup`, `AddCommMagma.toAdd`, `AddCommSemigroup.toAddCommMagma`, `AddGroup.toOrderedSub`
**V6:** `Real`, `Real.log`, `Eq`, `add_comm`, `congrFun'`, `Real.log_inv`, `Real.log_le_sub_one_of_pos`, `inv_pos`
**V1:** `Real.log_le_sub_one_of_pos`, `congrFun'`, `add_comm`, `inv_pos`, `Real.log_inv`, `Eq.mpr`, `LT.lt`, `Real`
**V2:** `Real`, `LT.lt`, `OfNat.ofNat`, `LE.le`, `Real.log`, `Real.instLE`, `Inv.inv`, `One.toOfNat1`
**V4:** `Real`, `LT.lt`, `Real.log`, `Real.instLE`, `OfNat.ofNat`, `LE.le`, `Real.instInv`, `Real.instOne`
**V7:** `Real.log_le_sub_one_of_pos`, `Real.log_inv`, `inv_pos`, `add_comm`, `congrFun'`, `Real`, `LT.lt`, `Real.log`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
lemma one_sub_inv_le_log_of_pos (hx : 0 < x) : 1 - x⁻¹ ≤ log x := by
  simpa [add_comm] using log_le_sub_one_of_pos (inv_pos.2 hx)

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
