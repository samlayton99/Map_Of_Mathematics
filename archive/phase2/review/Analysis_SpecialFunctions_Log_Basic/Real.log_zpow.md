# Real.log_zpow

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* induction · *proof-term size:* 6821 nodes

## Statement and source  [lean-exact]

```lean
@[simp, push]
theorem log_zpow (x : ℝ) (n : ℤ) : log (x ^ n) = n * log x := by
  cases n
  · rw [Int.ofNat_eq_natCast, zpow_natCast, log_pow, Int.cast_natCast]
  · rw [zpow_negSucc, log_inv, log_pow, Int.cast_negSucc, Nat.cast_add_one, neg_mul_eq_neg_mul]
```

Exact proof reference: record decl `d116` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x16948`, value `x17285`).

## P2 — support set (body)  [deterministic-derived]

**Domain (18):** `Real`, `Int`, `Eq`, `Real.log`, `Int.cast`, `Nat`, `Int.ofNat`, `Nat.cast`, `Int.ofNat_eq_natCast`, `zpow_natCast`, `Real.log_pow`, `Int.cast_natCast`, `Int.negSucc`, `zpow_negSucc`, `Real.log_inv`, `Int.cast_negSucc`, `Nat.cast_add_one`, `neg_mul_eq_neg_mul`

**Classified infrastructure (54):** `Int.casesOn` (generated), `HPow.hPow` (structure-projection), `instHPow` (typeclass-instance), `ZPow.toPow` (typeclass-instance), `DivInvMonoid.toZPow` (structure-projection,typeclass-instance), `Real.instDivInvMonoid` (typeclass-instance), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `Real.instMul` (typeclass-instance), `Real.instIntCast` (typeclass-instance), `Eq.ndrec` (eq-machinery,generated), `Eq.mpr` (eq-machinery), `instNatCastInt` (typeclass-instance), `id` (eq-machinery), `congrArg` (eq-machinery), `NPow.toPow` (typeclass-instance), `Monoid.toNPow` (structure-projection,typeclass-instance), `DivInvMonoid.toMonoid` (structure-projection,typeclass-instance), `Real.instNatCast` (typeclass-instance), `Real.instMonoid` (typeclass-instance), `AddMonoidWithOne.toNatCast` (structure-projection,typeclass-instance), `AddGroupWithOne.toAddMonoidWithOne` (structure-projection,typeclass-instance), `Ring.toAddGroupWithOne` (typeclass-instance), `Real.instRing` (typeclass-instance), `AddGroupWithOne.toIntCast` (structure-projection,typeclass-instance), `Eq.refl` (eq-machinery), `Eq.symm` (eq-machinery), `Inv.inv` (structure-projection), `DivInvMonoid.toInv` (structure-projection,typeclass-instance), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `instAddNat` (typeclass-instance), `OfNat.ofNat` (structure-projection), `instOfNatNat` (typeclass-instance), `Neg.neg` (structure-projection), `Real.instNeg` (typeclass-instance), `Real.instInv` (typeclass-instance), `NegZeroClass.toNeg` (structure-projection,typeclass-instance), `SubNegZeroMonoid.toNegZeroClass` (typeclass-instance), `SubtractionMonoid.toSubNegZeroMonoid` (typeclass-instance), `AddGroup.toSubtractionMonoid` (typeclass-instance), `AddGroupWithOne.toAddGroup` (typeclass-instance), `AddSemigroup.toAdd` (structure-projection,typeclass-instance), `AddMonoid.toAddSemigroup` (structure-projection,typeclass-instance), `AddMonoidWithOne.toAddMonoid` (structure-projection,typeclass-instance), `One.toOfNat1` (typeclass-instance), `AddMonoidWithOne.toOne` (structure-projection,typeclass-instance), `InvolutiveNeg.toNeg` (structure-projection,typeclass-instance), `HasDistribNeg.toInvolutiveNeg` (structure-projection,typeclass-instance), `NonUnitalNonAssocRing.toHasDistribNeg` (typeclass-instance), `NonUnitalNonAssocCommRing.toNonUnitalNonAssocRing` (structure-projection,typeclass-instance), `NonUnitalCommRing.toNonUnitalNonAssocCommRing` (typeclass-instance), `CommRing.toNonUnitalCommRing` (typeclass-instance), `Real.commRing` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `Int` (0 args)
- `Int.casesOn` (5 args) : Eq [Prop]
  - `Int` (0 args)
  - `Eq` (3 args) : <sort>
    - `Int` (0 args)
  - `Eq` (3 args) : <sort>
    - `Real` (0 args)
    - `Real.log` (1 args) : Real
      - `HPow.hPow` (6 args) : Real
        - `Real` (0 args)
        - `Int` (0 args)
        - `Real` (0 args)
        - `instHPow` (3 args) : HPow
          - `Real` (0 args)
          - `Int` (0 args)
          - `ZPow.toPow` (2 args) : Pow
            - `Real` (0 args)
            - `DivInvMonoid.toZPow` (2 args) : ZPow
              - `Real` (0 args)
              - `Real.instDivInvMonoid` (0 args)
    - `HMul.hMul` (6 args) : Real
      - `Real` (0 args)
      - `Real` (0 args)
      - `Real` (0 args)
      - `instHMul` (2 args) : HMul
        - `Real` (0 args)
        - `Real.instMul` (0 args)
      - `Int.cast` (3 args) : Real
        - `Real` (0 args)
  ... (3037 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Int.ofNat_eq_natCast` (1 args) : Eq (depth 5)
- `zpow_natCast` (4 args) : Eq (depth 6)
- `Real.log_pow` (2 args) : Eq (depth 7)
- `Int.cast_natCast` (3 args) : Eq (depth 8)
- `zpow_negSucc` (4 args) : Eq (depth 5)
- `Real.log_inv` (1 args) : Eq (depth 6)
- `Int.cast_negSucc` (3 args) : Eq (depth 8)
- `Nat.cast_add_one` (3 args) : Eq (depth 9)
- `neg_mul_eq_neg_mul` (5 args) : Eq (depth 10)

## P5 — source-level use events  [observed]

- `rewrite` → `Int.ofNat_eq_natCast`, `zpow_natCast`, `Real.log_pow`, `Int.cast_natCast` — `rewrite  [ Int.ofNat_eq_natCast, zpow_natCast, log_pow, Int.cast_natCast ]`
- `cases` → (no named attribution) — `cases n`
- `rewrite` → `zpow_negSucc`, `Real.log_inv`, `Real.log_pow`, `Int.cast_negSucc`, `Nat.cast_add_one`, `neg_mul_eq_neg_mul` — `rewrite  [ zpow_negSucc, log_inv, log_pow, Int.cast_negSucc, Nat.cast_add_one, n`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Int` — inductive, module `Init.Data.Int.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Real.log` — def, module `Basic`
- `Int.cast` — def, module `Init.Data.Int.Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
