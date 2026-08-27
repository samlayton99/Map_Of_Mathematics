# Lattice.ext

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* induction · *proof-term size:* 4609 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual self]
theorem Lattice.ext {α} {A B : Lattice α} (H : ∀ x y : α, (haveI := A; x ≤ y) ↔ x ≤ y) :
    A = B := by
  cases A
  cases B
  cases SemilatticeSup.ext H
  cases SemilatticeInf.ext H
  congr
```

Exact proof reference: record decl `d84` in `studies/Order_Lattice.study.json` (type `x7666`, value `x8829`).

## P2 — support set (body)  [deterministic-derived]

**Domain (12):** `Lattice`, `Iff`, `Eq`, `SemilatticeSup`, `Lattice.mk`, `HEq`, `SemilatticeSup.ext`, `SemilatticeInf`, `SemilatticeInf.ext`, `PartialOrder`, `eq_of_heq`, `HEq.refl`

**Classified infrastructure (17):** `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeInf.toPartialOrder` (structure-projection,typeclass-instance), `Lattice.toSemilatticeInf` (typeclass-instance), `Lattice.casesOn` (generated), `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `Eq.ndrec` (eq-machinery,generated), `Eq.casesOn` (generated), `Lattice.toSemilatticeSup` (structure-projection,typeclass-instance), `Eq.refl` (eq-machinery), `SemilatticeInf.mk.noConfusion` (generated), `Lattice.inf` (structure-projection), `Lattice.inf_le_left` (structure-projection), `Lattice.inf_le_right` (structure-projection), `Lattice.le_inf` (structure-projection), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Lattice` (1 args) : <sort>
- `Lattice` (1 args) : <sort>
- `Iff` (2 args) : <sort>
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeInf.toPartialOrder` (2 args) : PartialOrder
          - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeInf.toPartialOrder` (2 args) : PartialOrder
          - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
- `Lattice.casesOn` (5 args) : Eq [Prop]
  - `Lattice` (1 args) : <sort>
  - `Eq` (3 args) : <sort>
    - `Lattice` (1 args) : <sort>
  - `Eq` (3 args) : <sort>
    - `Lattice` (1 args) : <sort>
  - `SemilatticeSup` (1 args) : <sort>
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
  ... (659 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `SemilatticeSup.ext` (4 args) : Eq (depth 6)
- `SemilatticeSup.ext` (4 args) : Eq (depth 5)
- `SemilatticeInf.ext` (4 args) : Eq (depth 8)
- `SemilatticeInf.ext` (4 args) : Eq (depth 7)
- `SemilatticeInf.ext` (4 args) : Eq (depth 9)
- `eq_of_heq` (4 args) : Eq (depth 10)
- `HEq.refl` (2 args) : HEq (depth 7)
- `HEq.refl` (2 args) : HEq (depth 5)

## P5 — source-level use events  [observed]

- `cases` → `SemilatticeSup.ext` — `cases SemilatticeSup.ext H`
- `cases` → `SemilatticeInf.ext` — `cases SemilatticeInf.ext H`
- `cases` → (no named attribution) — `cases A`
- `cases` → (no named attribution) — `cases B`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Lattice` — inductive, module `Lattice`
- `Iff` — inductive, module `Init.Core`
- `Eq` — inductive, module `Init.Prelude`
- `SemilatticeSup` — inductive, module `Lattice`
- `Lattice.mk` — constructor, module `Lattice`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
