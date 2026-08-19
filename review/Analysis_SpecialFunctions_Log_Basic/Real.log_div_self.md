# Real.log_div_self

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* automation · *proof-term size:* 1401 nodes

## Statement and source  [lean-exact]

```lean
/-- This holds true for all `x : ℝ` because of the junk values `0 / 0 = 0` and `log 0 = 0`. -/
@[simp] lemma log_div_self (x : ℝ) : log (x / x) = 0 := by
  obtain rfl | hx := eq_or_ne x 0 <;> simp [*]
```

Exact proof reference: record decl `d67` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x10302`, value `x10413`).

## P2 — support set (body)  [deterministic-derived]

**Domain (18):** `Real`, `Eq`, `Ne`, `Or`, `Real.log`, `eq_or_ne`, `of_eq_true`, `True`, `congrFun'`, `div_zero`, `Real.log_zero`, `eq_self`, `div_self`, `Not`, `False`, `eq_false`, `not_false_eq_true`, `Real.log_one`

**Classified infrastructure (25):** `Or.casesOn` (generated), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `HDiv.hDiv` (structure-projection), `instHDiv` (typeclass-instance), `DivInvMonoid.toDiv` (structure-projection,typeclass-instance), `Real.instDivInvMonoid` (typeclass-instance), `Eq.ndrec` (eq-machinery,generated), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery), `MulZeroClass.toZero` (structure-projection,typeclass-instance), `MulZeroOneClass.toMulZeroClass` (typeclass-instance), `MonoidWithZero.toMulZeroOneClass` (typeclass-instance), `GroupWithZero.toMonoidWithZero` (structure-projection,typeclass-instance), `DivisionSemiring.toGroupWithZero` (typeclass-instance), `Semifield.toDivisionSemiring` (typeclass-instance), `Field.toSemifield` (typeclass-instance), `Real.instField` (typeclass-instance), `Eq.symm` (eq-machinery), `One.toOfNat1` (typeclass-instance), `InvOneClass.toOne` (structure-projection,typeclass-instance), `DivInvOneMonoid.toInvOneClass` (typeclass-instance), `DivisionMonoid.toDivInvOneMonoid` (typeclass-instance), `GroupWithZero.toDivisionMonoid` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `Or.casesOn` (6 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `Real` (0 args)
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `Ne` (3 args) : <sort>
    - `Real` (0 args)
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `Or` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Real` (0 args)
      - `OfNat.ofNat` (3 args) : Real
        - `Real` (0 args)
        - `Zero.toOfNat0` (2 args) : OfNat
          - `Real` (0 args)
          - `Real.instZero` (0 args)
    - `Ne` (3 args) : <sort>
      - `Real` (0 args)
      - `OfNat.ofNat` (3 args) : Real
        - `Real` (0 args)
        - `Zero.toOfNat0` (2 args) : OfNat
          - `Real` (0 args)
  ... (610 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `eq_or_ne` (3 args) : Or (depth 1)
- `of_eq_true` (2 args) : Eq (depth 2)
- `congrFun'` (6 args) : Eq (depth 4)
- `div_zero` (3 args) : Eq (depth 8)
- `eq_self` (2 args) : Eq (depth 4)
- `of_eq_true` (2 args) : Eq (depth 1)
- `congrFun'` (6 args) : Eq (depth 3)
- `div_self` (4 args) : Eq (depth 7)
- `of_eq_true` (2 args) : Not (depth 8)
- `eq_false` (2 args) : Eq (depth 11)
- `eq_self` (2 args) : Eq (depth 3)

## P5 — source-level use events  [observed]

- `simp` → (no named attribution) — `simp [*]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Ne` — def, module `Init.Core`
- `Or` — inductive, module `Init.Prelude`
- `Real.log` — def, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
