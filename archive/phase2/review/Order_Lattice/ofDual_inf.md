# ofDual_inf

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* term · *proof-term size:* 81 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual (attr := simp)]
```

Exact proof reference: record decl `d455` in `studies/Order_Lattice.study.json` (type `x29452`, value `x29458`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `Max`, `OrderDual`, `Equiv`, `OrderDual.ofDual`

**Classified infrastructure (6):** `rfl` (eq-machinery), `DFunLike.coe` (structure-projection), `EquivLike.toFunLike` (typeclass-instance), `Equiv.instEquivLike` (typeclass-instance), `Min.min` (structure-projection), `OrderDual.instMinOfMax` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Max` (1 args) : <sort>
- `OrderDual` (1 args) : <sort>
- `OrderDual` (1 args) : <sort>
- `rfl` (2 args) : Eq [Prop]
  - `DFunLike.coe` (6 args) : <local>
    - `Equiv` (2 args) : <sort>
      - `OrderDual` (1 args) : <sort>
    - `OrderDual` (1 args) : <sort>
    - `OrderDual` (1 args) : <sort>
    - `EquivLike.toFunLike` (4 args) : FunLike
      - `Equiv` (2 args) : <sort>
        - `OrderDual` (1 args) : <sort>
      - `OrderDual` (1 args) : <sort>
      - `Equiv.instEquivLike` (2 args) : EquivLike
        - `OrderDual` (1 args) : <sort>
    - `OrderDual.ofDual` (1 args) : Equiv
    - `Min.min` (4 args) : OrderDual
      - `OrderDual` (1 args) : <sort>
      - `OrderDual.instMinOfMax` (2 args) : Min

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

(none)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Max` — inductive, module `Init.Prelude`
- `OrderDual` — def, module `Mathlib.Order.OrderDual`
- `Equiv` — inductive, module `Mathlib.Logic.Equiv.Defs`
- `OrderDual.ofDual` — def, module `Mathlib.Order.OrderDual`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
