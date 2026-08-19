# Nat.pow_sub_one_mod_pow_sub_one

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* automation · *proof-term size:* 133344 nodes

## Statement and source  [lean-exact]

```lean
@[simp]
theorem pow_sub_one_mod_pow_sub_one (a b c : ℕ) : (a ^ c - 1) % (a ^ b - 1) = a ^ (c % b) - 1 := by
  rcases eq_zero_or_pos a with rfl | ha0
  · simp [zero_pow_eq]; split_ifs <;> simp
  rcases Nat.eq_or_lt_of_le ha0 with rfl | ha1
  · simp
  rcases eq_zero_or_pos b with rfl | hb0
  · simp
  rcases lt_or_ge c b with h | h
  · rw [mod_eq_of_lt, mod_eq_of_lt h]
    rwa [Nat.sub_lt_sub_iff_right (one_le_pow c a ha0), Nat.pow_lt_pow_iff_right ha1]
  · suffices a ^ (c - b + b) - 1 = a ^ (c - b) * (a ^ b - 1) + (a ^ (c - b) - 1) by
      rw [← Nat.sub_add_cancel h, add_mod_right, this, add_mod, mul_mod, mod_self,
        mul_zero, zero_mod, zero_add, mod_mod, pow_sub_one_mod_pow_sub_one]
    rw [← Nat.add_sub_assoc (one_le_pow (c - b) a ha0), ← mul_add_one, pow_add,
      Nat.sub_add_cancel (one_le_pow b a ha0)]
```

Exact proof reference: record decl `d71` in `studies/Data_Nat_GCD_Basic.study.json` (type `x5166`, value `x7474`).

## P2 — support set (body)  [deterministic-derived]

**Domain (81):** `Nat`, `WellFounded.Nat.fix`, `Eq`, `InvImage`, `GT.gt`, `Or`, `Nat.eq_zero_or_pos`, `ite`, `congrFun'`, `zero_pow_eq`, `dite`, `if_pos`, `of_eq_true`, `True`, `Nat.sub_self`, `Nat.mod_self`, `eq_self`, `Not`, `if_neg`, `Nat.sub_eq_zero_of_le`, `Nat.succ`, `Nat.eq_or_lt_of_le`, `zero_add`, `one_pow`, `pow_zero`, `Nat.mod_zero`, `lt_or_ge`, `Nat.mod_eq_of_lt`, `Nat.sub_lt_sub_iff_right`, `Nat.one_le_pow`, `Nat.pow_lt_pow_iff_right`, `Nat.add_sub_assoc`, `Nat.mul_add_one`, `pow_add`, `Nat.sub_add_cancel`, `Nat.add_mod_right`, `Nat.add_mod`, `Nat.mul_mod`, `Nat.zero_mod`, `Nat.mod_mod`, `Decidable.byContradiction`, `And`, `Int`, `Nat.cast`, `False`, `Lean.Omega.Int.ofNat_sub_dichotomy`, `Lean.Omega.Constraint.not_sat'_of_isImpossible`, `Lean.Omega.Constraint.mk`, `Option.some`, `of_decide_eq_true`, `Bool`, `Lean.Omega.Constraint.isImpossible`, `Bool.true`, `Decidable.decide`, `List.cons`, `List.nil`, `Lean.Omega.Coeffs.ofList`, `Lean.Omega.Constraint.combine_sat'`, `Option.none`, `Lean.Omega.combo_sat'`, `Lean.Omega.Constraint.addEquality_sat`, `Lean.Omega.LinearCombo.eval`, `Lean.Omega.LinearCombo`, `Lean.Omega.LinearCombo.mk`, `Lean.Omega.LinearCombo.coordinate`, `Lean.Omega.Int.sub_congr`, `Lean.Omega.LinearCombo.coordinate_eval_6`, `Lean.Omega.LinearCombo.coordinate_eval_2`, `Lean.Omega.LinearCombo.coordinate_eval_1`, `Lean.Omega.LinearCombo.sub_eval`, `Int.sub_eq_zero_of_eq`, `Lean.Omega.Constraint.addInequality_sat`, `le_of_le_of_eq`, `Int.sub_nonneg_of_le`, `Int.add_one_le_of_lt`, `Lean.Omega.Int.ofNat_lt_of_lt`, `Lean.Omega.tidy_sat`, `Lean.Omega.Int.ofNat_le_of_le`, `Nat.le_of_not_lt`, `Lean.Omega.Int.add_congr`, `Lean.Omega.LinearCombo.add_eval`

**Classified infrastructure (76):** `HMod.hMod` (structure-projection), `instHMod` (typeclass-instance), `Nat.instMod` (typeclass-instance), `HSub.hSub` (structure-projection), `instHSub` (typeclass-instance), `instSubNat` (typeclass-instance), `HPow.hPow` (structure-projection), `instHPow` (typeclass-instance), `NPow.toPow` (typeclass-instance), `Monoid.toNPow` (structure-projection,typeclass-instance), `Nat.instMonoid` (typeclass-instance), `OfNat.ofNat` (structure-projection), `instOfNatNat` (typeclass-instance), `LT.lt` (structure-projection), `instLTNat` (typeclass-instance), `Or.casesOn` (generated), `Eq.ndrec` (eq-machinery,generated), `Eq.mpr` (eq-machinery), `instDecidableEqNat` (typeclass-instance), `One.toOfNat1` (typeclass-instance), `MulOne.toOne` (structure-projection,typeclass-instance), `MulOneClass.toMulOne` (structure-projection,typeclass-instance), `MulZeroOneClass.toMulOneClass` (structure-projection,typeclass-instance), `MonoidWithZero.toMulZeroOneClass` (typeclass-instance), `Nat.instMonoidWithZero` (typeclass-instance), `Zero.toOfNat0` (typeclass-instance), `MulZeroClass.toZero` (structure-projection,typeclass-instance), `MulZeroOneClass.toMulZeroClass` (typeclass-instance), `id` (eq-machinery), `congr` (eq-machinery), `congrArg` (eq-machinery), `Eq.trans` (eq-machinery), `LE.le` (structure-projection), `instLENat` (typeclass-instance), `Nat.zero_le._simp_1` (internal-detail), `Eq.symm` (eq-machinery), `Monoid.toMulOneClass` (typeclass-instance), `AddMonoid.toAddZeroClass` (typeclass-instance), `Nat.instAddMonoid` (typeclass-instance), `Preorder.toLT` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `LinearOrder.toPartialOrder` (structure-projection,typeclass-instance), `Nat.instLinearOrder` (typeclass-instance), `Preorder.toLE` (structure-projection,typeclass-instance), `instPowNat` (typeclass-instance), `instNatPowNat` (typeclass-instance), `propext` (eq-machinery), `Eq.refl` (eq-machinery), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `instAddNat` (typeclass-instance), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `instMulNat` (typeclass-instance), `MulOne.toMul` (structure-projection,typeclass-instance), `Nat.instMulZeroClass` (typeclass-instance), `MulZeroClass.toMul` (structure-projection,typeclass-instance), `MulZeroClass.mul_zero` (structure-projection), `AddZero.toAdd` (structure-projection,typeclass-instance), `AddZeroClass.toAddZero` (structure-projection,typeclass-instance), `AddZero.toZero` (structure-projection,typeclass-instance), `Nat.decLt` (typeclass-instance), `Or.elim` (logic-core), `instNatCastInt` (typeclass-instance), `Int.instSub` (typeclass-instance), `instOfNat` (typeclass-instance), `instDecidableEqBool` (typeclass-instance), `Neg.neg` (structure-projection), `Int.instNegInt` (typeclass-instance), `Int.instMul` (typeclass-instance), `Lean.Omega.LinearCombo.instSub` (typeclass-instance), `And.right` (logic-core,structure-projection), `Int.instAdd` (typeclass-instance), `Int.instLEInt` (typeclass-instance), `And.left` (logic-core,structure-projection), `Lean.Omega.LinearCombo.instAdd` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `WellFounded.Nat.fix` (4 args) : <pi> [Prop]
  - `Nat` (0 args)
  - `Nat` (0 args)
  - `Eq` (3 args) : <sort>
    - `Nat` (0 args)
    - `HMod.hMod` (6 args) : Nat
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `instHMod` (2 args) : HMod
        - `Nat` (0 args)
        - `Nat.instMod` (0 args)
      - `HSub.hSub` (6 args) : Nat
        - `Nat` (0 args)
        - `Nat` (0 args)
        - `Nat` (0 args)
        - `instHSub` (2 args) : HSub
          - `Nat` (0 args)
          - `instSubNat` (0 args)
        - `HPow.hPow` (6 args) : Nat
          - `Nat` (0 args)
          - `Nat` (0 args)
          - `Nat` (0 args)
          - `instHPow` (3 args) : HPow
            - `Nat` (0 args)
            - `Nat` (0 args)
            - `NPow.toPow` (2 args) : Pow
              - `Nat` (0 args)
  ... (57029 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `WellFounded.Nat.fix` (4 args) : <pi> (depth 0)
- `Nat.eq_zero_or_pos` (1 args) : Or (depth 2)
- `congrFun'` (6 args) : Eq (depth 9)
- `zero_pow_eq` (3 args) : Eq (depth 11)
- `congrFun'` (6 args) : Eq (depth 8)
- `zero_pow_eq` (3 args) : Eq (depth 10)
- `congrFun'` (6 args) : Eq (depth 6)
- `zero_pow_eq` (3 args) : Eq (depth 8)
- `dite` (5 args) : Eq (depth 4)
- `congrFun'` (6 args) : Eq (depth 7)
- `congrFun'` (6 args) : Eq (depth 11)
- `if_pos` (6 args) : Eq (depth 13)
- `dite` (5 args) : Eq (depth 6)
- `congrFun'` (6 args) : Eq (depth 12)
- `if_pos` (6 args) : Eq (depth 14)
- `dite` (5 args) : Eq (depth 8)
- `of_eq_true` (2 args) : Eq (depth 10)
- `Nat.sub_self` (1 args) : Eq (depth 17)
- `Nat.sub_self` (1 args) : Eq (depth 16)
- `Nat.mod_self` (1 args) : Eq (depth 15)
- `Nat.sub_self` (1 args) : Eq (depth 13)
- `eq_self` (2 args) : Eq (depth 12)
- `if_neg` (6 args) : Eq (depth 14)
- `Nat.sub_eq_zero_of_le` (3 args) : Eq (depth 13)
- `of_eq_true` (2 args) : LE.le (depth 14)
  ... (215 occurrences total)

## P5 — source-level use events  [observed]

- `simp` → `zero_pow_eq`, `zero_pow_eq` — `simp [zero_pow_eq]`
- `refine` → `dite` — `refine  if  h._@.Basic.2330553057._hygCtx._hyg.74  :  ?  m  then  ?  pos  else  `
- `rewrite` → `Nat.mod_eq_of_lt`, `Nat.mod_eq_of_lt` — `rewrite  [ mod_eq_of_lt, mod_eq_of_lt h ]`
- `simp` → (no named attribution) — `simp`
- `rewrite` → `Nat.add_sub_assoc`, `Nat.mul_add_one`, `pow_add`, `Nat.sub_add_cancel` — `rewrite  [ ← Nat.add_sub_assoc (one_le_pow (c - b) a ha0), ← mul_add_one, pow_ad`
- `simp` → `Lean.Meta.Simp.Config.unfoldPartialApp`, `Bool.true`, `Lean.Meta.Simp.Config.zetaDelta`, `Bool.true`, `Lean.Meta.Simp.Config.failIfUnchanged`, `Bool.false`, `invImage`, `InvImage`, `Prod.lex`, `sizeOfWFRel`, `measure`, `Nat.lt_wfRel`, `WellFoundedRelation.rel`, `sizeOf_nat` — `simp  +  unfoldPartialApp  +  zetaDelta  -  failIfUnchanged  only  [  invImage  `
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  suffices a ^ (c - b + b) - 1 = a ^ (c - b) * (a ^ b`
- `rewrite` → `Nat.sub_add_cancel`, `Nat.add_mod_right`, `Nat.add_mod`, `Nat.mul_mod`, `Nat.mod_self`, `MulZeroClass.mul_zero`, `Nat.zero_mod`, `zero_add`, `Nat.mod_mod` — `rewrite  [ ← Nat.sub_add_cancel h, add_mod_right, this, add_mod, mul_mod, mod_se`
- `simp` → (no named attribution) — `simp`
- `simp` → (no named attribution) — `simp`
- `rewrite` → `Nat.sub_lt_sub_iff_right`, `Nat.pow_lt_pow_iff_right` — `rewrite  [ Nat.sub_lt_sub_iff_right (one_le_pow c a ha0), Nat.pow_lt_pow_iff_rig`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `WellFounded.Nat.fix` — def, module `Init.WF`
- `Eq` — inductive, module `Init.Prelude`
- `InvImage` — def, module `Init.Core`
- `GT.gt` — def, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
