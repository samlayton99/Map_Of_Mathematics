# sup_assoc

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* automation · *proof-term size:* 2743 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual]
theorem sup_assoc (a b c : α) : a ⊔ b ⊔ c = a ⊔ (b ⊔ c) :=
  eq_of_forall_ge_iff fun x => by simp only [sup_le_iff]; rw [and_assoc]
```

Exact proof reference: record decl `d468` in `studies/Order_Lattice.study.json` (type `x30068`, value `x30194`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `SemilatticeSup`, `eq_of_forall_ge_iff`, `Iff`, `And`, `Eq`, `congrFun'`, `and_assoc`

**Classified infrastructure (14):** `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `Eq.mpr` (eq-machinery), `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `id` (eq-machinery), `congr` (eq-machinery), `congrArg` (eq-machinery), `Eq.trans` (eq-machinery), `sup_le_iff._simp_1` (internal-detail), `propext` (eq-machinery), `Iff.rfl` (logic-core)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `SemilatticeSup` (1 args) : <sort>
- `eq_of_forall_ge_iff` (5 args) : Eq [Prop]
  - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
  - `Max.max` (4 args) : <local>
    - `SemilatticeSup.toMax` (2 args) : Max
    - `Max.max` (4 args) : <local>
      - `SemilatticeSup.toMax` (2 args) : Max
  - `Max.max` (4 args) : <local>
    - `SemilatticeSup.toMax` (2 args) : Max
    - `Max.max` (4 args) : <local>
      - `SemilatticeSup.toMax` (2 args) : Max
  - `Eq.mpr` (4 args) : Iff [Prop]
    - `Iff` (2 args) : <sort>
      - `LE.le` (4 args) : <sort>
        - `Preorder.toLE` (2 args) : LE
          - `PartialOrder.toPreorder` (2 args) : Preorder
            - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
        - `Max.max` (4 args) : <local>
          - `SemilatticeSup.toMax` (2 args) : Max
          - `Max.max` (4 args) : <local>
            - `SemilatticeSup.toMax` (2 args) : Max
      - `LE.le` (4 args) : <sort>
        - `Preorder.toLE` (2 args) : LE
          - `PartialOrder.toPreorder` (2 args) : Preorder
            - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
        - `Max.max` (4 args) : <local>
          - `SemilatticeSup.toMax` (2 args) : Max
          - `Max.max` (4 args) : <local>
            - `SemilatticeSup.toMax` (2 args) : Max
    - `Iff` (2 args) : <sort>
  ... (533 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `eq_of_forall_ge_iff` (5 args) : Eq (depth 0)
- `congrFun'` (6 args) : Eq (depth 6)
- `and_assoc` (3 args) : Iff (depth 6)

## P5 — source-level use events  [observed]

- `simp` → `sup_le_iff`, `sup_le_iff` — `simp only [sup_le_iff]`
- `rewrite` → `and_assoc` — `rewrite  [ and_assoc ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `SemilatticeSup` — inductive, module `Lattice`
- `eq_of_forall_ge_iff` — axiom, module `Mathlib.Order.Basic`
- `Iff` — inductive, module `Init.Core`
- `And` — inductive, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
