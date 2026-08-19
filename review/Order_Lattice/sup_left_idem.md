# sup_left_idem

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* automation · *proof-term size:* 343 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual]
theorem sup_left_idem (a b : α) : a ⊔ (a ⊔ b) = a ⊔ b := by simp
```

Exact proof reference: record decl `d497` in `studies/Order_Lattice.study.json` (type `x31783`, value `x31811`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `SemilatticeSup`, `of_eq_true`, `Eq`, `True`, `congrFun'`, `sup_of_le_right`, `eq_self`

**Classified infrastructure (9):** `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery), `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `le_sup_left._simp_1` (internal-detail)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `SemilatticeSup` (1 args) : <sort>
- `of_eq_true` (2 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `Max.max` (4 args) : <local>
      - `SemilatticeSup.toMax` (2 args) : Max
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
    - `Max.max` (4 args) : <local>
      - `SemilatticeSup.toMax` (2 args) : Max
  - `Eq.trans` (6 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
        - `Max.max` (4 args) : <local>
          - `SemilatticeSup.toMax` (2 args) : Max
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
    - `Eq` (3 args) : <sort>
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
    - `True` (0 args)
    - `congrFun'` (6 args) : Eq [Prop]
      - `Eq` (2 args) : <pi>
        - `Max.max` (4 args) : <local>
          - `SemilatticeSup.toMax` (2 args) : Max
          - `Max.max` (4 args) : <local>
            - `SemilatticeSup.toMax` (2 args) : Max
      - `Eq` (2 args) : <pi>
  ... (56 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `of_eq_true` (2 args) : Eq (depth 0)
- `congrFun'` (6 args) : Eq (depth 2)
- `sup_of_le_right` (5 args) : Eq (depth 4)
- `of_eq_true` (2 args) : LE.le (depth 5)
- `eq_self` (2 args) : Eq (depth 2)

## P5 — source-level use events  [observed]

- `simp` → (no named attribution) — `simp`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `SemilatticeSup` — inductive, module `Lattice`
- `of_eq_true` — axiom, module `Init.SimpLemmas`
- `Eq` — inductive, module `Init.Prelude`
- `True` — inductive, module `Init.Prelude`
- `congrFun'` — axiom, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
