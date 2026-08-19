# Review packet — `add_one_zsmul`

*domain file:* Algebra_Group_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[to_additive add_one_zsmul]

```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V6:** `AddGroup`, `Int`, `_private.Basic.0.add_one_zsmul.match_1`, `Eq`, `HSMul.hSMul`, `instHSMul`, `ZSMul.toSMul`, `SubNegMonoid.toZSMul`
**V4:** `Nat`, `Int`, `HAdd.hAdd`, `instHAdd`, `AddGroup.toSubNegMonoid`, `OfNat.ofNat`, `HSMul.hSMul`, `instHSMul`
**V5:** `neg_zsmul`, `SubtractionMonoid.toSubNegZeroMonoid`, `_private.Basic.0.add_one_zsmul.match_1`, `AddGroup`, `AddGroup.toSubNegMonoid`, `AddGroup.toSubtractionMonoid`, `AddMonoid.toAddZeroClass`, `AddMonoid.toNSMul`
**V7:** `AddGroup`, `Int`, `Eq`, `Nat`, `of_eq_true`, `Nat.cast`, `True`, `Nat.succ`
**V1:** `of_eq_true`, `eq_self`, `congrFun'`, `negSucc_zsmul`, `neg_add_cancel`, `succ_nsmul'`, `natCast_zsmul`, `neg_add_rev`
**V3:** `Int`, `AddGroup`, `Eq`, `HAdd.hAdd`, `HSMul.hSMul`, `instHAdd`, `instHSMul`, `OfNat.ofNat`
**V2:** `Int`, `Eq`, `AddGroup`, `Nat`, `HSMul.hSMul`, `OfNat.ofNat`, `instHSMul`, `_private.Basic.0.add_one_zsmul.match_1`
**V8:** `neg_zsmul`, `negSucc_zsmul`, `neg_add_cancel`, `ofNat_zsmul`, `neg_add_cancel_right`, `succ_nsmul'`, `Int.negSucc_eq`, `Int.add_left_neg`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[to_additive add_one_zsmul]

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
