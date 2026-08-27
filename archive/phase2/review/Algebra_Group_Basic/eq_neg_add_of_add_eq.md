# eq_neg_add_of_add_eq

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* term · *proof-term size:* 605 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive]
```

Exact proof reference: record decl `d200` in `studies/Algebra_Group_Basic.study.json` (type `x16226`, value `x16251`).

## P2 — support set (body)  [deterministic-derived]

**Domain (6):** `AddGroup`, `Eq`, `of_eq_true`, `True`, `neg_add_cancel_left`, `eq_self`

**Classified infrastructure (15):** `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `AddZero.toAdd` (structure-projection,typeclass-instance), `AddZeroClass.toAddZero` (structure-projection,typeclass-instance), `AddMonoid.toAddZeroClass` (typeclass-instance), `SubNegMonoid.toAddMonoid` (structure-projection,typeclass-instance), `AddGroup.toSubNegMonoid` (structure-projection,typeclass-instance), `Neg.neg` (structure-projection), `NegZeroClass.toNeg` (structure-projection,typeclass-instance), `SubNegZeroMonoid.toNegZeroClass` (typeclass-instance), `SubtractionMonoid.toSubNegZeroMonoid` (typeclass-instance), `AddGroup.toSubtractionMonoid` (typeclass-instance), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `AddGroup` (1 args) : <sort>
- `Eq` (3 args) : <sort>
  - `HAdd.hAdd` (6 args) : <local>
    - `instHAdd` (2 args) : HAdd
      - `AddZero.toAdd` (2 args) : Add
        - `AddZeroClass.toAddZero` (2 args) : AddZero
          - `AddMonoid.toAddZeroClass` (2 args) : AddZeroClass
            - `SubNegMonoid.toAddMonoid` (2 args) : AddMonoid
              - `AddGroup.toSubNegMonoid` (2 args) : SubNegMonoid
- `of_eq_true` (2 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `HAdd.hAdd` (6 args) : <local>
      - `instHAdd` (2 args) : HAdd
        - `AddZero.toAdd` (2 args) : Add
          - `AddZeroClass.toAddZero` (2 args) : AddZero
            - `AddMonoid.toAddZeroClass` (2 args) : AddZeroClass
              - `SubNegMonoid.toAddMonoid` (2 args) : AddMonoid
                - `AddGroup.toSubNegMonoid` (2 args) : SubNegMonoid
      - `Neg.neg` (3 args) : <local>
        - `NegZeroClass.toNeg` (2 args) : Neg
          - `SubNegZeroMonoid.toNegZeroClass` (2 args) : NegZeroClass
            - `SubtractionMonoid.toSubNegZeroMonoid` (2 args) : SubNegZeroMonoid
              - `AddGroup.toSubtractionMonoid` (2 args) : SubtractionMonoid
  - `Eq.trans` (6 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `HAdd.hAdd` (6 args) : <local>
        - `instHAdd` (2 args) : HAdd
          - `AddZero.toAdd` (2 args) : Add
            - `AddZeroClass.toAddZero` (2 args) : AddZero
              - `AddMonoid.toAddZeroClass` (2 args) : AddZeroClass
  ... (115 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `of_eq_true` (2 args) : Eq (depth 0)
- `neg_add_cancel_left` (4 args) : Eq (depth 4)
- `eq_self` (2 args) : Eq (depth 2)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `AddGroup` — inductive, module `Mathlib.Algebra.Group.Defs`
- `Eq` — inductive, module `Init.Prelude`
- `of_eq_true` — axiom, module `Init.SimpLemmas`
- `True` — inductive, module `Init.Prelude`
- `neg_add_cancel_left` — axiom, module `Mathlib.Algebra.Group.Defs`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
