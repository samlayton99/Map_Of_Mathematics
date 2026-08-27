# Real.log_le_self

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* automation · *proof-term size:* 11389 nodes

## Statement and source  [lean-exact]

```lean
/-- See `Real.log_le_sub_one_of_pos` for the stronger version when `x ≠ 0`. -/
lemma log_le_self (hx : 0 ≤ x) : log x ≤ x := by
  obtain rfl | hx := hx.eq_or_lt
  · simp
  · exact (log_le_sub_one_of_pos hx).trans (by linarith)
```

Exact proof reference: record decl `d79` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x12111`, value `x12327`).

## P2 — support set (body)  [deterministic-derived]

**Domain (53):** `Real`, `Eq`, `Or`, `Real.log`, `LE.le.eq_or_lt`, `of_eq_true`, `True`, `congrFun'`, `Real.log_zero`, `LE.le.trans`, `Real.log_le_sub_one_of_pos`, `le_of_not_gt`, `Mathlib.Tactic.Linarith.lt_irrefl`, `Mathlib.Tactic.Ring.of_eq`, `Mathlib.Tactic.Ring.Common.add_congr`, `Int.rawCast`, `inferInstance`, `Ring`, `Int.negOfNat`, `Nat.rawCast`, `Mathlib.Meta.NormNum.instAddMonoidWithOne`, `Mathlib.Tactic.Ring.Common.neg_congr`, `Mathlib.Tactic.Ring.cast_pos`, `Mathlib.Meta.NormNum.isNat_ofNat`, `Nat.cast_one`, `Mathlib.Tactic.Ring.Common.neg_add`, `Mathlib.Meta.NormNum.IsInt.to_raw_eq`, `Mathlib.Meta.NormNum.isInt_neg`, `Int.ofNat`, `Mathlib.Meta.NormNum.IsNat.to_isInt`, `Mathlib.Meta.NormNum.IsNat.of_raw`, `Int`, `Mathlib.Tactic.Ring.Common.neg_zero`, `Mathlib.Tactic.Ring.Common.sub_congr`, `Nat`, `Mathlib.Tactic.Ring.Common.atom_pf`, `Mathlib.Tactic.Ring.Common.sub_pf`, `Mathlib.Tactic.Ring.Common.add_pf_add_gt`, `Mathlib.Tactic.Ring.Common.add_pf_add_zero`, `Mathlib.Meta.NormNum.IsNat.to_raw_eq`, `Mathlib.Meta.NormNum.IsInt.to_isNat`, `Mathlib.Meta.NormNum.IsInt.of_raw`, `Mathlib.Tactic.Ring.Common.neg_mul`, `Mathlib.Tactic.Ring.Common.add_pf_add_overlap_zero`, `Mathlib.Tactic.Ring.Common.add_overlap_pf_zero`, `Mathlib.Meta.NormNum.isInt_add`, `Mathlib.Tactic.Ring.Common.add_pf_zero_add`, `Mathlib.Tactic.Ring.cast_zero`, `Nat.cast_zero`, `Mathlib.Tactic.Linarith.add_neg`, `neg_neg_of_pos`, `Mathlib.Tactic.Linarith.zero_lt_one`, `Mathlib.Tactic.Linarith.sub_neg_of_lt`

**Classified infrastructure (73):** `LE.le` (structure-projection), `Real.instLE` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `Or.casesOn` (generated), `LT.lt` (structure-projection), `Preorder.toLT` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `Real.partialOrder` (typeclass-instance), `Eq.ndrec` (eq-machinery,generated), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery), `Std.le_refl._simp_1` (internal-detail), `instReflLe` (typeclass-instance), `Real.instPreorder` (typeclass-instance), `HSub.hSub` (structure-projection), `instHSub` (typeclass-instance), `Real.instSub` (typeclass-instance), `One.toOfNat1` (typeclass-instance), `Real.instOne` (typeclass-instance), `Real.linearOrder` (typeclass-instance), `LinearOrder.toPartialOrder` (structure-projection,typeclass-instance), `Eq.mp` (eq-machinery), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `AddSemigroup.toAdd` (structure-projection,typeclass-instance), `AddMonoid.toAddSemigroup` (structure-projection,typeclass-instance), `Real.instAddMonoid` (typeclass-instance), `Neg.neg` (structure-projection), `NegZeroClass.toNeg` (structure-projection,typeclass-instance), `SubNegZeroMonoid.toNegZeroClass` (typeclass-instance), `SubtractionMonoid.toSubNegZeroMonoid` (typeclass-instance), `SubtractionCommMonoid.toSubtractionMonoid` (structure-projection,typeclass-instance), `AddCommGroup.toDivisionAddCommMonoid` (typeclass-instance), `Real.instAddCommGroup` (typeclass-instance), `AddMonoidWithOne.toOne` (structure-projection,typeclass-instance), `AddCommMonoidWithOne.toAddMonoidWithOne` (structure-projection,typeclass-instance), `NonAssocSemiring.toAddCommMonoidWithOne` (typeclass-instance), `Semiring.toNonAssocSemiring` (typeclass-instance), `Real.semiring` (typeclass-instance), `SubNegMonoid.toSub` (structure-projection,typeclass-instance), `AddGroup.toSubNegMonoid` (structure-projection,typeclass-instance), `AddGroupWithOne.toAddGroup` (typeclass-instance), `Ring.toAddGroupWithOne` (typeclass-instance), `Real.instRing` (typeclass-instance), `MulZeroClass.toZero` (structure-projection,typeclass-instance), `instMulZeroClassOfSemiring` (typeclass-instance), `CommSemiring.toSemiring` (structure-projection,typeclass-instance), `Real.instCommSemiring` (typeclass-instance), `Distrib.toAdd` (structure-projection,typeclass-instance), `instDistribOfSemiring` (typeclass-instance), `CommRing.toRing` (structure-projection,typeclass-instance), `Real.commRing` (typeclass-instance), `AddGroupWithOne.toAddMonoidWithOne` (structure-projection,typeclass-instance), `Ring.toAddCommGroup` (typeclass-instance), `Eq.refl` (eq-machinery), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `Distrib.toMul` (structure-projection,typeclass-instance), `HPow.hPow` (structure-projection), `instHPow` (typeclass-instance), `NPow.toPow` (typeclass-instance), `Monoid.toNPow` (structure-projection,typeclass-instance), `Semiring.toMonoid` (structure-projection,typeclass-instance), `Nat.instCommSemiring` (typeclass-instance), `rfl` (eq-machinery), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `Eq.symm` (eq-machinery), `Real.instIsStrictOrderedRing` (typeclass-instance), `Real.instIsOrderedAddMonoid` (typeclass-instance), `Real.instIsOrderedRing` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `LE.le` (4 args) : <sort>
  - `Real` (0 args)
  - `Real.instLE` (0 args)
  - `OfNat.ofNat` (3 args) : Real
    - `Real` (0 args)
    - `Zero.toOfNat0` (2 args) : OfNat
      - `Real` (0 args)
      - `Real.instZero` (0 args)
- `Or.casesOn` (6 args) : LE.le [Prop]
  - `Eq` (3 args) : <sort>
    - `Real` (0 args)
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `LT.lt` (4 args) : <sort>
    - `Real` (0 args)
    - `Preorder.toLT` (2 args) : LT
      - `Real` (0 args)
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `Real` (0 args)
        - `Real.partialOrder` (0 args)
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `Or` (2 args) : <sort>
  ... (5299 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `LE.le.eq_or_lt` (5 args) : Or (depth 1)
- `of_eq_true` (2 args) : LE.le (depth 2)
- `congrFun'` (6 args) : Eq (depth 4)
- `LE.le.trans` (7 args) : LE.le (depth 1)
- `Real.log_le_sub_one_of_pos` (2 args) : LE.le (depth 2)
- `le_of_not_gt` (5 args) : LE.le (depth 2)
- `Mathlib.Tactic.Linarith.lt_irrefl` (4 args) : False (depth 3)
- `Mathlib.Tactic.Ring.of_eq` (6 args) : Eq (depth 6)
- `Mathlib.Tactic.Ring.Common.add_congr` (10 args) : Eq (depth 7)
- `Mathlib.Tactic.Ring.Common.neg_congr` (7 args) : Eq (depth 8)
- `Mathlib.Tactic.Ring.cast_pos` (5 args) : Eq (depth 9)
- `Mathlib.Meta.NormNum.isNat_ofNat` (5 args) : Mathlib.Meta.NormNum.IsNat (depth 10)
- `Nat.cast_one` (2 args) : Eq (depth 11)
- `Mathlib.Tactic.Ring.Common.neg_add` (8 args) : Eq (depth 9)
- `Mathlib.Meta.NormNum.IsInt.to_raw_eq` (5 args) : Eq (depth 10)
- `Mathlib.Meta.NormNum.isInt_neg` (9 args) : Mathlib.Meta.NormNum.IsInt (depth 11)
- `Mathlib.Meta.NormNum.IsNat.to_isInt` (5 args) : Mathlib.Meta.NormNum.IsInt (depth 12)
- `Mathlib.Meta.NormNum.IsNat.of_raw` (3 args) : Mathlib.Meta.NormNum.IsNat (depth 13)
- `Mathlib.Tactic.Ring.Common.neg_zero` (2 args) : Eq (depth 10)
- `Mathlib.Tactic.Ring.Common.sub_congr` (10 args) : Eq (depth 8)
- `Mathlib.Tactic.Ring.Common.atom_pf` (7 args) : Eq (depth 9)
- `Mathlib.Tactic.Ring.Common.sub_congr` (10 args) : Eq (depth 9)
- `Mathlib.Tactic.Ring.Common.atom_pf` (7 args) : Eq (depth 10)
- `Mathlib.Tactic.Ring.cast_pos` (5 args) : Eq (depth 10)
- `Mathlib.Meta.NormNum.isNat_ofNat` (5 args) : Mathlib.Meta.NormNum.IsNat (depth 11)
  ... (71 occurrences total)

## P5 — source-level use events  [observed]

- `exact` → `LE.le.trans` — `exact (log_le_sub_one_of_pos hx).trans (by linarith)`
- `simp` → (no named attribution) — `simp`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Or` — inductive, module `Init.Prelude`
- `Real.log` — def, module `Basic`
- `LE.le.eq_or_lt` — axiom, module `Mathlib.Order.Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
