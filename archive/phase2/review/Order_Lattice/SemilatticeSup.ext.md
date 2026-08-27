# SemilatticeSup.ext

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* induction · *proof-term size:* 3389 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual (reorder := H (x y))]
theorem SemilatticeSup.ext {α} {A B : SemilatticeSup α}
    (H : ∀ x y : α, (haveI := A; x ≤ y) ↔ x ≤ y) :
    A = B := by
  cases A
  cases B
  cases PartialOrder.ext H
  congr
  ext; apply SemilatticeSup.ext_sup H
```

Exact proof reference: record decl `d242` in `studies/Order_Lattice.study.json` (type `x17829`, value `x18552`).

## P2 — support set (body)  [deterministic-derived]

**Domain (9):** `SemilatticeSup`, `Iff`, `Eq`, `PartialOrder`, `SemilatticeSup.mk`, `HEq`, `PartialOrder.ext`, `SemilatticeSup.ext_sup`, `HEq.refl`

**Classified infrastructure (11):** `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `SemilatticeSup.casesOn` (generated), `Eq.ndrec` (eq-machinery,generated), `Eq.casesOn` (generated), `Eq.refl` (eq-machinery), `Eq.rec` (eq-machinery,generated,recursor), `funext` (eq-machinery), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `SemilatticeSup` (1 args) : <sort>
- `SemilatticeSup` (1 args) : <sort>
- `Iff` (2 args) : <sort>
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
- `SemilatticeSup.casesOn` (5 args) : Eq [Prop]
  - `SemilatticeSup` (1 args) : <sort>
  - `Eq` (3 args) : <sort>
    - `SemilatticeSup` (1 args) : <sort>
  - `Eq` (3 args) : <sort>
    - `SemilatticeSup` (1 args) : <sort>
  - `PartialOrder` (1 args) : <sort>
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
  ... (461 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `PartialOrder.ext` (4 args) : Eq (depth 6)
- `PartialOrder.ext` (4 args) : Eq (depth 5)
- `SemilatticeSup.ext_sup` (6 args) : Eq (depth 8)
- `HEq.refl` (2 args) : HEq (depth 5)

## P5 — source-level use events  [observed]

- `cases` → `PartialOrder.ext` — `cases PartialOrder.ext H`
- `apply` → `SemilatticeSup.ext_sup` — `apply SemilatticeSup.ext_sup H`
- `cases` → (no named attribution) — `cases A`
- `cases` → (no named attribution) — `cases B`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `SemilatticeSup` — inductive, module `Lattice`
- `Iff` — inductive, module `Init.Core`
- `Eq` — inductive, module `Init.Prelude`
- `PartialOrder` — inductive, module `Mathlib.Order.Defs.PartialOrder`
- `SemilatticeSup.mk` — constructor, module `Lattice`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
