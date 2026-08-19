# isOpen_empty

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 213 nodes

## Statement and source  [lean-exact]

```lean
@[simp] theorem isOpen_empty : IsOpen (∅ : Set X) := by
  rw [← sUnion_empty]; exact isOpen_sUnion fun a => False.elim
```

Exact proof reference: record decl `d56` in `studies/Topology_Basic.study.json` (type `x3902`, value `x3939`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `TopologicalSpace`, `IsOpen`, `Set`, `Set.sUnion`, `Eq`, `Set.sUnion_empty`, `isOpen_sUnion`

**Classified infrastructure (7):** `Eq.mpr` (eq-machinery), `EmptyCollection.emptyCollection` (structure-projection), `Set.instEmptyCollection` (typeclass-instance), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.symm` (eq-machinery), `False.elim` (logic-core)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `TopologicalSpace` (1 args) : <sort>
- `Eq.mpr` (4 args) : IsOpen [Prop]
  - `IsOpen` (3 args) : <sort>
    - `EmptyCollection.emptyCollection` (2 args) : Set
      - `Set` (1 args) : <sort>
      - `Set.instEmptyCollection` (1 args) : EmptyCollection
  - `IsOpen` (3 args) : <sort>
    - `Set.sUnion` (2 args) : Set
      - `EmptyCollection.emptyCollection` (2 args) : Set
        - `Set` (1 args) : <sort>
          - `Set` (1 args) : <sort>
        - `Set.instEmptyCollection` (1 args) : EmptyCollection
          - `Set` (1 args) : <sort>
  - `id` (2 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `IsOpen` (3 args) : <sort>
        - `EmptyCollection.emptyCollection` (2 args) : Set
          - `Set` (1 args) : <sort>
          - `Set.instEmptyCollection` (1 args) : EmptyCollection
      - `IsOpen` (3 args) : <sort>
        - `Set.sUnion` (2 args) : Set
          - `EmptyCollection.emptyCollection` (2 args) : Set
            - `Set` (1 args) : <sort>
              - `Set` (1 args) : <sort>
            - `Set.instEmptyCollection` (1 args) : EmptyCollection
              - `Set` (1 args) : <sort>
    - `congrArg` (6 args) : Eq [Prop]
      - `Set` (1 args) : <sort>
      - `EmptyCollection.emptyCollection` (2 args) : Set
        - `Set` (1 args) : <sort>
  ... (60 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Set.sUnion_empty` (1 args) : Eq (depth 4)
- `isOpen_sUnion` (4 args) : IsOpen (depth 1)

## P5 — source-level use events  [observed]

- `rewrite` → `Set.sUnion_empty` — `rewrite  [ ← sUnion_empty ]`
- `exact` → `isOpen_sUnion` — `exact isOpen_sUnion fun a => False.elim`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `IsOpen` — def, module `Mathlib.Topology.Defs.Basic`
- `Set` — def, module `Mathlib.Data.Set.Defs`
- `Set.sUnion` — def, module `Mathlib.Order.SetNotation`
- `Eq` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
