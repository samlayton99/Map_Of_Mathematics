# le_iff_exists_sup

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* tactic-other · *proof-term size:* 385 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual]
theorem le_iff_exists_sup : a ≤ b ↔ ∃ c, b = a ⊔ c := by
  constructor
  · intro h
    exact ⟨b, (sup_eq_right.mpr h).symm⟩
  · rintro ⟨c, rfl : _ = _ ⊔ _⟩
    exact le_sup_left
```

Exact proof reference: record decl `d421` in `studies/Order_Lattice.study.json` (type `x28414`, value `x28465`).

## P2 — support set (body)  [deterministic-derived]

**Domain (5):** `SemilatticeSup`, `Exists`, `Eq`, `sup_eq_right`, `le_sup_left`

**Classified infrastructure (12):** `Iff.intro` (logic-core,logic-core-ctor), `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `Exists.intro` (logic-core,logic-core-ctor), `Eq.symm` (eq-machinery), `Iff.mpr` (logic-core,structure-projection), `Exists.casesOn` (generated), `Eq.ndrec` (eq-machinery,generated)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `SemilatticeSup` (1 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
  - `Exists` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
  - `Exists.intro` (4 args) : Exists [Prop]
    - `Eq` (3 args) : <sort>
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
    - `Eq.symm` (4 args) : Eq [Prop]
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
      - `Iff.mpr` (4 args) : Eq [Prop]
        - `Eq` (3 args) : <sort>
          - `Max.max` (4 args) : <local>
            - `SemilatticeSup.toMax` (2 args) : Max
        - `LE.le` (4 args) : <sort>
          - `Preorder.toLE` (2 args) : LE
            - `PartialOrder.toPreorder` (2 args) : Preorder
              - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
        - `sup_eq_right` (4 args) : Iff [Prop]
  ... (60 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `sup_eq_right` (4 args) : Iff (depth 4)
- `le_sup_left` (4 args) : LE.le (depth 3)

## P5 — source-level use events  [observed]

- `constructor` → (no named attribution) — `constructor`
- `exact` → `le_sup_left` — `exact le_sup_left`
- `exact` → `Exists.intro` — `exact ⟨b, (sup_eq_right.mpr h).symm⟩`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `SemilatticeSup` — inductive, module `Lattice`
- `Exists` — inductive, module `Init.Core`
- `Eq` — inductive, module `Init.Prelude`
- `sup_eq_right` — theorem, module `Lattice`
- `le_sup_left` — theorem, module `Lattice`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
