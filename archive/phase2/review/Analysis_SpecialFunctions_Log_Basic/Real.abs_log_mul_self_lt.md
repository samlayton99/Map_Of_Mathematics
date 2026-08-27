# Real.abs_log_mul_self_lt

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 65663 nodes

## Statement and source  [lean-exact]

```lean
/-- Bound for `|log x * x|` in the interval `(0, 1]`. -/
theorem abs_log_mul_self_lt (x : ℝ) (h1 : 0 < x) (h2 : x ≤ 1) : |log x * x| < 1 := by
  have : 0 < 1 / x := by simpa only [one_div, inv_pos] using h1
  replace := log_le_sub_one_of_pos this
  replace : log (1 / x) < 1 / x := by linarith
  rw [log_div one_ne_zero h1.ne', log_one, zero_sub, lt_div_iff₀ h1] at this
  have aux : 0 ≤ -log x * x := by
    refine mul_nonneg ?_ h1.le
    rw [← log_inv]
    apply log_nonneg
    rw [← le_inv_comm₀ h1 zero_lt_one, inv_one]
    exact h2
  rw [← abs_of_nonneg aux, neg_mul, abs_neg] at this
  exact this
```

Exact proof reference: record decl `d20` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x4342`, value `x5837`).

## P2 — support set (body)  [deterministic-derived]

**Domain (84):** `Real`, `Eq`, `one_div`, `Real.log`, `Real.log_le_sub_one_of_pos`, `lt_of_not_ge`, `Mathlib.Tactic.Linarith.lt_irrefl`, `inferInstance`, `AddMonoidWithOne`, `Mathlib.Tactic.Ring.of_eq`, `Mathlib.Tactic.Ring.Common.add_congr`, `Nat`, `Nat.rawCast`, `Int.rawCast`, `Ring`, `Int.negOfNat`, `Mathlib.Meta.NormNum.instAddMonoidWithOne`, `Mathlib.Tactic.Ring.Common.neg_congr`, `Mathlib.Tactic.Ring.cast_pos`, `Mathlib.Meta.NormNum.isNat_ofNat`, `Nat.cast_one`, `Mathlib.Tactic.Ring.Common.neg_add`, `Mathlib.Meta.NormNum.IsInt.to_raw_eq`, `Mathlib.Meta.NormNum.isInt_neg`, `Int.ofNat`, `Mathlib.Meta.NormNum.IsNat.to_isInt`, `Mathlib.Meta.NormNum.IsNat.of_raw`, `Int`, `Mathlib.Tactic.Ring.Common.neg_zero`, `Mathlib.Tactic.Ring.Common.sub_congr`, `Mathlib.Tactic.Ring.Common.mul_congr`, `Mathlib.Tactic.Ring.Common.atom_pf`, `Mathlib.Tactic.Ring.Common.add_mul`, `Mathlib.Tactic.Ring.Common.mul_add`, `Mathlib.Tactic.Ring.Common.mul_pf_right`, `Mathlib.Meta.NormNum.IsNat.to_raw_eq`, `Mathlib.Meta.NormNum.isNat_mul`, `Mathlib.Tactic.Ring.Common.mul_zero`, `Mathlib.Tactic.Ring.Common.add_pf_add_zero`, `Mathlib.Tactic.Ring.Common.zero_mul`, `Mathlib.Tactic.Ring.Common.div_congr`, `Mathlib.Tactic.Ring.Common.div_pf`, `Mathlib.Tactic.Ring.Common.inv_single`, `Mathlib.Tactic.Ring.Common.inv_mul`, `Mathlib.Meta.NormNum.instAddMonoidWithOne'`, `Mathlib.Meta.NormNum.IsNNRat.to_isNat`, `Mathlib.Meta.NormNum.isNNRat_inv_pos`, `Mathlib.Meta.NormNum.IsNat.to_isNNRat`, `Mathlib.Tactic.Ring.Common.sub_pf`, `Mathlib.Tactic.Ring.Common.add_pf_add_gt`, `Mathlib.Meta.NormNum.IsInt.to_isNat`, `Mathlib.Meta.NormNum.IsInt.of_raw`, `Mathlib.Tactic.Ring.Common.neg_mul`, `Mathlib.Tactic.Ring.Common.add_pf_add_lt`, `Mathlib.Tactic.Ring.Common.add_pf_zero_add`, `Mathlib.Tactic.Ring.Common.add_pf_add_overlap_zero`, `Mathlib.Meta.NormNum.isInt_add`, `Mathlib.Tactic.Ring.Common.add_overlap_pf_zero`, `Mathlib.Tactic.Ring.cast_zero`, `Nat.cast_zero`, `Mathlib.Tactic.Linarith.add_lt_of_neg_of_le`, `neg_neg_of_pos`, `Mathlib.Tactic.Linarith.zero_lt_one`, `Mathlib.Tactic.Linarith.without_one_mul`, `Mathlib.Tactic.CancelDenoms.sub_subst`, `Mul`, `Mathlib.Tactic.Linarith.sub_nonpos_of_le`, `mul_nonneg`, `Real.log_inv`, `Real.log_nonneg`, `le_inv_comm₀`, `zero_lt_one`, `inv_one`, `LT.lt.le`, `abs`, `abs_neg`, `neg_mul`, `abs_of_nonneg`, `lt_div_iff₀`, `zero_sub`, `Real.log_one`, `Real.log_div`, `one_ne_zero`, `LT.lt.ne'`

**Classified infrastructure (136):** `LT.lt` (structure-projection), `Real.instLT` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `LE.le` (structure-projection), `Real.instLE` (typeclass-instance), `One.toOfNat1` (typeclass-instance), `Real.instOne` (typeclass-instance), `HDiv.hDiv` (structure-projection), `instHDiv` (typeclass-instance), `DivInvMonoid.toDiv` (structure-projection,typeclass-instance), `Real.instDivInvMonoid` (typeclass-instance), `Eq.mpr` (eq-machinery), `Preorder.toLT` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `Real.partialOrder` (typeclass-instance), `MulZeroClass.toZero` (structure-projection,typeclass-instance), `MulZeroOneClass.toMulZeroClass` (typeclass-instance), `MonoidWithZero.toMulZeroOneClass` (typeclass-instance), `GroupWithZero.toMonoidWithZero` (structure-projection,typeclass-instance), `DivisionSemiring.toGroupWithZero` (typeclass-instance), `Semifield.toDivisionSemiring` (typeclass-instance), `Field.toSemifield` (typeclass-instance), `Real.instField` (typeclass-instance), `id` (eq-machinery), `Eq.trans` (eq-machinery), `Inv.inv` (structure-projection), `DivInvMonoid.toInv` (structure-projection,typeclass-instance), `congrArg` (eq-machinery), `_private.Basic.0.Real.abs_log_mul_self_lt._simp_1` (internal-detail), `PosMulReflectLE.toPosMulReflectLT` (typeclass-instance), `instMulZeroClassOfSemiring` (typeclass-instance), `Real.semiring` (typeclass-instance), `PosMulStrictMono.toPosMulReflectLE` (typeclass-instance), `MulZeroClass.toMul` (structure-projection,typeclass-instance), `Real.linearOrder` (typeclass-instance), `IsStrictOrderedRing.toPosMulStrictMono` (structure-projection,typeclass-instance), `Real.instIsStrictOrderedRing` (typeclass-instance), `HSub.hSub` (structure-projection), `instHSub` (typeclass-instance), `Real.instSub` (typeclass-instance), `Preorder.toLE` (structure-projection,typeclass-instance), `LinearOrder.toPartialOrder` (structure-projection,typeclass-instance), `Real.instPreorder` (typeclass-instance), `Eq.mp` (eq-machinery), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `AddSemigroup.toAdd` (structure-projection,typeclass-instance), `AddMonoid.toAddSemigroup` (structure-projection,typeclass-instance), `Real.instAddMonoid` (typeclass-instance), `Neg.neg` (structure-projection), `NegZeroClass.toNeg` (structure-projection,typeclass-instance), `SubNegZeroMonoid.toNegZeroClass` (typeclass-instance), `SubtractionMonoid.toSubNegZeroMonoid` (typeclass-instance), `SubtractionCommMonoid.toSubtractionMonoid` (structure-projection,typeclass-instance), `AddCommGroup.toDivisionAddCommMonoid` (typeclass-instance), `Real.instAddCommGroup` (typeclass-instance), `AddMonoidWithOne.toOne` (structure-projection,typeclass-instance), `AddCommMonoidWithOne.toAddMonoidWithOne` (structure-projection,typeclass-instance), `NonAssocSemiring.toAddCommMonoidWithOne` (typeclass-instance), `Semiring.toNonAssocSemiring` (typeclass-instance), `SubNegMonoid.toSub` (structure-projection,typeclass-instance), `AddGroup.toSubNegMonoid` (structure-projection,typeclass-instance), `AddGroupWithOne.toAddGroup` (typeclass-instance), `Ring.toAddGroupWithOne` (typeclass-instance), `DivisionRing.toRing` (structure-projection,typeclass-instance), `Field.toDivisionRing` (typeclass-instance), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `Distrib.toMul` (structure-projection,typeclass-instance), `instDistribOfSemiring` (typeclass-instance), `DivisionSemiring.toSemiring` (structure-projection,typeclass-instance), `AddGroupWithOne.toAddMonoidWithOne` (structure-projection,typeclass-instance), `Ring.toSemiring` (structure-projection,typeclass-instance), `Real.instRing` (typeclass-instance), `CommSemiring.toSemiring` (structure-projection,typeclass-instance), `Real.instCommSemiring` (typeclass-instance), `Distrib.toAdd` (structure-projection,typeclass-instance), `HPow.hPow` (structure-projection), `instHPow` (typeclass-instance), `NPow.toPow` (typeclass-instance), `Monoid.toNPow` (structure-projection,typeclass-instance), `Semiring.toMonoid` (structure-projection,typeclass-instance), `Nat.instCommSemiring` (typeclass-instance), `InvOneClass.toInv` (structure-projection,typeclass-instance), `DivInvOneMonoid.toInvOneClass` (typeclass-instance), `DivisionMonoid.toDivInvOneMonoid` (typeclass-instance), `DivisionCommMonoid.toDivisionMonoid` (structure-projection,typeclass-instance), `CommGroupWithZero.toDivisionCommMonoid` (typeclass-instance), `Semifield.toCommGroupWithZero` (typeclass-instance), `CommRing.toRing` (structure-projection,typeclass-instance), `Real.commRing` (typeclass-instance), `Ring.toAddCommGroup` (typeclass-instance), `Eq.refl` (eq-machinery), `rfl` (eq-machinery), `Eq.symm` (eq-machinery), `GroupWithZero.toDivisionMonoid` (typeclass-instance), `FloorSemiring.instCharZero` (typeclass-instance), `FloorRing.toFloorSemiring` (typeclass-instance), `Real.instFloorRing` (typeclass-instance), `Eq.rec` (eq-machinery,generated,recursor), `Real.instIsOrderedAddMonoid` (typeclass-instance), `MulZeroOneClass.toMulOneClass` (structure-projection,typeclass-instance), `instMulZeroOneClassOfSemiring` (typeclass-instance), `Real.instIsOrderedRing` (typeclass-instance), `Real.instMul` (typeclass-instance), `Real.instNeg` (typeclass-instance), `IsOrderedRing.toPosMulMono` (structure-projection,typeclass-instance), `Real.instInv` (typeclass-instance), `propext` (eq-machinery), `MulPosReflectLE.toMulPosReflectLT` (typeclass-instance), `MulPosStrictMono.toMulPosReflectLE` (typeclass-instance), `IsStrictOrderedRing.toMulPosStrictMono` (structure-projection,typeclass-instance), `Real.instZeroLEOneClass` (typeclass-instance), `NeZero.charZero_one` (typeclass-instance), `InvOneClass.toOne` (structure-projection,typeclass-instance), `Real.lattice` (typeclass-instance), `Real.instAddGroup` (typeclass-instance), `AddGroup.toSubtractionMonoid` (typeclass-instance), `NonUnitalNonAssocSemiring.toDistrib` (typeclass-instance), `NonUnitalNonAssocRing.toNonUnitalNonAssocSemiring` (typeclass-instance), `NonUnitalNonAssocCommRing.toNonUnitalNonAssocRing` (structure-projection,typeclass-instance), `NonUnitalCommRing.toNonUnitalNonAssocCommRing` (typeclass-instance), `CommRing.toNonUnitalCommRing` (typeclass-instance), `InvolutiveNeg.toNeg` (structure-projection,typeclass-instance), `HasDistribNeg.toInvolutiveNeg` (structure-projection,typeclass-instance), `NonUnitalNonAssocRing.toHasDistribNeg` (typeclass-instance), `IsOrderedAddMonoid.toAddLeftMono` (typeclass-instance), `Real.instAddCommMonoid` (typeclass-instance), `SubNegMonoid.toNeg` (structure-projection,typeclass-instance), `GroupWithZero.toDivInvMonoid` (typeclass-instance), `AddZero.toZero` (structure-projection,typeclass-instance), `AddZeroClass.toAddZero` (structure-projection,typeclass-instance), `AddMonoid.toAddZeroClass` (typeclass-instance), `SubNegMonoid.toAddMonoid` (structure-projection,typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `LT.lt` (4 args) : <sort>
  - `Real` (0 args)
  - `Real.instLT` (0 args)
  - `OfNat.ofNat` (3 args) : Real
    - `Real` (0 args)
    - `Zero.toOfNat0` (2 args) : OfNat
      - `Real` (0 args)
      - `Real.instZero` (0 args)
- `LE.le` (4 args) : <sort>
  - `Real` (0 args)
  - `Real.instLE` (0 args)
  - `OfNat.ofNat` (3 args) : Real
    - `Real` (0 args)
    - `One.toOfNat1` (2 args) : OfNat
      - `Real` (0 args)
      - `Real.instOne` (0 args)
- `LT.lt` (4 args) : <sort>
  - `Real` (0 args)
  - `Real.instLT` (0 args)
  - `OfNat.ofNat` (3 args) : Real
    - `Real` (0 args)
    - `Zero.toOfNat0` (2 args) : OfNat
      - `Real` (0 args)
      - `Real.instZero` (0 args)
  - `HDiv.hDiv` (6 args) : Real
    - `Real` (0 args)
    - `Real` (0 args)
    - `Real` (0 args)
    - `instHDiv` (2 args) : HDiv
  ... (30949 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `one_div` (3 args) : Eq (depth 4)
- `Real.log_le_sub_one_of_pos` (2 args) : LE.le (depth 0)
- `lt_of_not_ge` (5 args) : LT.lt (depth 0)
- `Mathlib.Tactic.Linarith.lt_irrefl` (4 args) : False (depth 1)
- `Mathlib.Tactic.Ring.of_eq` (6 args) : Eq (depth 4)
- `Mathlib.Tactic.Ring.Common.add_congr` (10 args) : Eq (depth 5)
- `Mathlib.Tactic.Ring.Common.add_congr` (10 args) : Eq (depth 6)
- `Mathlib.Tactic.Ring.Common.neg_congr` (7 args) : Eq (depth 7)
- `Mathlib.Tactic.Ring.cast_pos` (5 args) : Eq (depth 8)
- `Mathlib.Meta.NormNum.isNat_ofNat` (5 args) : Mathlib.Meta.NormNum.IsNat (depth 9)
- `Nat.cast_one` (2 args) : Eq (depth 10)
- `Mathlib.Tactic.Ring.Common.neg_add` (8 args) : Eq (depth 8)
- `Mathlib.Meta.NormNum.IsInt.to_raw_eq` (5 args) : Eq (depth 9)
- `Mathlib.Meta.NormNum.isInt_neg` (9 args) : Mathlib.Meta.NormNum.IsInt (depth 10)
- `Mathlib.Meta.NormNum.IsNat.to_isInt` (5 args) : Mathlib.Meta.NormNum.IsInt (depth 11)
- `Mathlib.Meta.NormNum.IsNat.of_raw` (3 args) : Mathlib.Meta.NormNum.IsNat (depth 12)
- `Mathlib.Tactic.Ring.Common.neg_zero` (2 args) : Eq (depth 9)
- `Mathlib.Tactic.Ring.Common.sub_congr` (10 args) : Eq (depth 7)
- `Mathlib.Tactic.Ring.Common.mul_congr` (10 args) : Eq (depth 8)
- `Mathlib.Tactic.Ring.cast_pos` (5 args) : Eq (depth 9)
- `Mathlib.Meta.NormNum.isNat_ofNat` (5 args) : Mathlib.Meta.NormNum.IsNat (depth 10)
- `Nat.cast_one` (2 args) : Eq (depth 11)
- `Mathlib.Tactic.Ring.Common.atom_pf` (7 args) : Eq (depth 9)
- `Mathlib.Tactic.Ring.Common.add_mul` (11 args) : Eq (depth 9)
- `Mathlib.Tactic.Ring.Common.mul_add` (11 args) : Eq (depth 10)
  ... (243 occurrences total)

## P5 — source-level use events  [observed]

- `exact` → (no named attribution) — `exact h2`
- `exact` → (no named attribution) — `exact this`
- `rewrite` → `Real.log_inv` — `rewrite  [ ← log_inv ]`
- `apply` → `Real.log_nonneg` — `apply log_nonneg`
- `refine` → `mul_nonneg` — `refine mul_nonneg ?_ h1.le`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  have := log_le_sub_one_of_pos this ;  ?  _`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  (    have  : log (1 / x) < 1 / x  :=  ?  body  ;  ?`
- `rewrite` → `le_inv_comm₀`, `inv_one` — `rewrite  [ ← le_inv_comm₀ h1 zero_lt_one, inv_one ]`
- `rewrite` → `abs_of_nonneg`, `neg_mul`, `abs_neg` — `rewrite  [ ← abs_of_nonneg aux, neg_mul, abs_neg ] at this`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  (    have  : 0 < 1 / x  :=  ?  body  ;  ?  _  )`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  (    have aux  : 0 ≤ -log x * x  :=  ?  body  ;  ? `
- `rewrite` → `Real.log_div`, `Real.log_one`, `zero_sub`, `lt_div_iff₀` — `rewrite  [ log_div one_ne_zero h1.ne', log_one, zero_sub, lt_div_iff₀ h1 ] at th`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `one_div` — axiom, module `Mathlib.Algebra.Group.Defs`
- `Real.log` — def, module `Basic`
- `Real.log_le_sub_one_of_pos` — theorem, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
