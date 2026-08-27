# sup_left_right_swap

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* rewrite · *proof-term size:* 1045 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual]
theorem sup_left_right_swap (a b c : α) : a ⊔ b ⊔ c = c ⊔ b ⊔ a := by
  rw [sup_comm, sup_comm a, sup_assoc]
```

Exact proof reference: record decl `d498` in `studies/Order_Lattice.study.json` (type `x31821`, value `x31884`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `SemilatticeSup`, `Eq`, `sup_comm`, `sup_assoc`

**Classified infrastructure (6):** `Eq.mpr` (eq-machinery), `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.refl` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `SemilatticeSup` (1 args) : <sort>
- `Eq.mpr` (4 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `Max.max` (4 args) : <local>
      - `SemilatticeSup.toMax` (2 args) : Max
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
    - `Max.max` (4 args) : <local>
      - `SemilatticeSup.toMax` (2 args) : Max
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
  - `id` (2 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
        - `Max.max` (4 args) : <local>
          - `SemilatticeSup.toMax` (2 args) : Max
          - `Max.max` (4 args) : <local>
            - `SemilatticeSup.toMax` (2 args) : Max
        - `Max.max` (4 args) : <local>
          - `SemilatticeSup.toMax` (2 args) : Max
          - `Max.max` (4 args) : <local>
  ... (168 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `sup_comm` (4 args) : Eq (depth 3)
- `sup_comm` (4 args) : Eq (depth 4)
- `sup_assoc` (5 args) : Eq (depth 5)

## P5 — source-level use events  [observed]

- `rewrite` → `sup_comm`, `sup_comm`, `sup_assoc` — `rewrite  [ sup_comm, sup_comm a, sup_assoc ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `SemilatticeSup` — inductive, module `Lattice`
- `Eq` — inductive, module `Init.Prelude`
- `sup_comm` — theorem, module `Lattice`
- `sup_assoc` — theorem, module `Lattice`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
