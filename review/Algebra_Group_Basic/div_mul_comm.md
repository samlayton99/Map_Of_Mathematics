# div_mul_comm

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* automation · *proof-term size:* 2707 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive]
theorem div_mul_comm : a / b * c = c / b * a := by simp
```

Exact proof reference: record decl `d157` in `studies/Algebra_Group_Basic.study.json` (type `x13206`, value `x13243`).

## P2 — support set (body)  [deterministic-derived]

**Domain (9):** `DivisionCommMonoid`, `of_eq_true`, `Eq`, `True`, `congrFun'`, `div_eq_mul_inv`, `mul_comm`, `mul_left_comm`, `eq_self`

**Classified infrastructure (20):** `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `MulOne.toMul` (structure-projection,typeclass-instance), `MulOneClass.toMulOne` (structure-projection,typeclass-instance), `Monoid.toMulOneClass` (typeclass-instance), `DivInvMonoid.toMonoid` (structure-projection,typeclass-instance), `DivisionMonoid.toDivInvMonoid` (structure-projection,typeclass-instance), `DivisionCommMonoid.toDivisionMonoid` (structure-projection,typeclass-instance), `HDiv.hDiv` (structure-projection), `instHDiv` (typeclass-instance), `DivInvMonoid.toDiv` (structure-projection,typeclass-instance), `Eq.trans` (eq-machinery), `CommMagma.toMul` (structure-projection,typeclass-instance), `CommSemigroup.toCommMagma` (typeclass-instance), `CommMonoid.toCommSemigroup` (typeclass-instance), `DivisionCommMonoid.toCommMonoid` (typeclass-instance), `Inv.inv` (structure-projection), `DivInvMonoid.toInv` (structure-projection,typeclass-instance), `congr` (eq-machinery), `congrArg` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `DivisionCommMonoid` (1 args) : <sort>
- `of_eq_true` (2 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `HMul.hMul` (6 args) : <local>
      - `instHMul` (2 args) : HMul
        - `MulOne.toMul` (2 args) : Mul
          - `MulOneClass.toMulOne` (2 args) : MulOne
            - `Monoid.toMulOneClass` (2 args) : MulOneClass
              - `DivInvMonoid.toMonoid` (2 args) : Monoid
                - `DivisionMonoid.toDivInvMonoid` (2 args) : DivInvMonoid
                  - `DivisionCommMonoid.toDivisionMonoid` (2 args) : DivisionMonoid
      - `HDiv.hDiv` (6 args) : <local>
        - `instHDiv` (2 args) : HDiv
          - `DivInvMonoid.toDiv` (2 args) : Div
            - `DivisionMonoid.toDivInvMonoid` (2 args) : DivInvMonoid
              - `DivisionCommMonoid.toDivisionMonoid` (2 args) : DivisionMonoid
    - `HMul.hMul` (6 args) : <local>
      - `instHMul` (2 args) : HMul
        - `MulOne.toMul` (2 args) : Mul
          - `MulOneClass.toMulOne` (2 args) : MulOne
            - `Monoid.toMulOneClass` (2 args) : MulOneClass
              - `DivInvMonoid.toMonoid` (2 args) : Monoid
                - `DivisionMonoid.toDivInvMonoid` (2 args) : DivInvMonoid
                  - `DivisionCommMonoid.toDivisionMonoid` (2 args) : DivisionMonoid
      - `HDiv.hDiv` (6 args) : <local>
        - `instHDiv` (2 args) : HDiv
          - `DivInvMonoid.toDiv` (2 args) : Div
            - `DivisionMonoid.toDivInvMonoid` (2 args) : DivInvMonoid
              - `DivisionCommMonoid.toDivisionMonoid` (2 args) : DivisionMonoid
  - `Eq.trans` (6 args) : Eq [Prop]
  ... (521 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `of_eq_true` (2 args) : Eq (depth 0)
- `congrFun'` (6 args) : Eq (depth 6)
- `div_eq_mul_inv` (4 args) : Eq (depth 8)
- `mul_comm` (4 args) : Eq (depth 6)
- `mul_left_comm` (5 args) : Eq (depth 5)
- `congrFun'` (6 args) : Eq (depth 4)
- `div_eq_mul_inv` (4 args) : Eq (depth 6)
- `mul_comm` (4 args) : Eq (depth 4)
- `eq_self` (2 args) : Eq (depth 2)

## P5 — source-level use events  [observed]

- `simp` → (no named attribution) — `simp`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `DivisionCommMonoid` — inductive, module `Mathlib.Algebra.Group.Defs`
- `of_eq_true` — axiom, module `Init.SimpLemmas`
- `Eq` — inductive, module `Init.Prelude`
- `True` — inductive, module `Init.Prelude`
- `congrFun'` — axiom, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
