# sup_eq_maxDefault

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* tactic-other · *proof-term size:* 943 nodes

## Statement and source  [lean-exact]

```lean
theorem sup_eq_maxDefault [SemilatticeSup α] [DecidableLE α] [@Std.Total α (· ≤ ·)] :
    (· ⊔ ·) = (maxDefault : α → α → α) := by
  ext x y
  unfold maxDefault
  split_ifs with h'
  exacts [sup_of_le_right h', sup_of_le_left <| (total_of (· ≤ ·) x y).resolve_left h']
```

Exact proof reference: record decl `d478` in `studies/Order_Lattice.study.json` (type `x30742`, value `x30848`).

## P2 — support set (body)  [deterministic-derived]

**Domain (14):** `SemilatticeSup`, `DecidableLE`, `Std.Total`, `maxDefault`, `Eq`, `dite`, `ite`, `if_pos`, `sup_of_le_right`, `Not`, `if_neg`, `sup_of_le_left`, `Or.resolve_left`, `total_of`

**Classified infrastructure (10):** `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `LE.le` (structure-projection), `funext` (eq-machinery), `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `id` (eq-machinery), `Eq.mpr` (eq-machinery), `congrArg` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `SemilatticeSup` (1 args) : <sort>
- `DecidableLE` (2 args) : <sort>
  - `Preorder.toLE` (2 args) : LE
    - `PartialOrder.toPreorder` (2 args) : Preorder
      - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
- `Std.Total` (2 args) : <sort>
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
- `funext` (5 args) : Eq [Prop]
  - `Max.max` (4 args) : <local>
    - `SemilatticeSup.toMax` (2 args) : Max
  - `maxDefault` (3 args) : <pi>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
  - `funext` (5 args) : Eq [Prop]
    - `Max.max` (4 args) : <local>
      - `SemilatticeSup.toMax` (2 args) : Max
    - `maxDefault` (4 args) : <pi>
      - `Preorder.toLE` (2 args) : LE
        - `PartialOrder.toPreorder` (2 args) : Preorder
          - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
    - `id` (2 args) : Eq [Prop]
      - `Eq` (3 args) : <sort>
        - `Max.max` (4 args) : <local>
          - `SemilatticeSup.toMax` (2 args) : Max
        - `maxDefault` (5 args) : <local>
          - `Preorder.toLE` (2 args) : LE
  ... (148 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `dite` (5 args) : Eq (depth 3)
- `if_pos` (6 args) : Eq (depth 7)
- `sup_of_le_right` (5 args) : Eq (depth 5)
- `if_neg` (6 args) : Eq (depth 7)
- `sup_of_le_left` (5 args) : Eq (depth 5)
- `Or.resolve_left` (4 args) : LE.le (depth 6)
- `total_of` (5 args) : Or (depth 7)

## P5 — source-level use events  [observed]

- `unfold` → `maxDefault` — `unfold maxDefault`
- `refine` → `dite` — `refine  if  h'  :  ?  m  then  ?  pos  else  ?  neg`
- `exact` → `sup_of_le_right` — `exact sup_of_le_right h'`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `SemilatticeSup` — inductive, module `Lattice`
- `DecidableLE` — def, module `Init.Prelude`
- `Std.Total` — inductive, module `Init.Core`
- `maxDefault` — def, module `Mathlib.Order.Defs.LinearOrder`
- `Eq` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
