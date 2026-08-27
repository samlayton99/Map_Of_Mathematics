# IsOpen.union

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 337 nodes

## Statement and source  [lean-exact]

```lean
theorem IsOpen.union (h₁ : IsOpen s₁) (h₂ : IsOpen s₂) : IsOpen (s₁ ∪ s₂) := by
  rw [union_eq_iUnion]; exact isOpen_iUnion (Bool.forall_bool.2 ⟨h₂, h₁⟩)
```

Exact proof reference: record decl `d20` in `studies/Topology_Basic.study.json` (type `x1066`, value `x1132`).

## P2 — support set (body)  [deterministic-derived]

**Domain (13):** `Set`, `TopologicalSpace`, `IsOpen`, `Set.iUnion`, `Bool`, `cond`, `Eq`, `Set.union_eq_iUnion`, `isOpen_iUnion`, `And`, `Bool.false`, `Bool.true`, `Bool.forall_bool`

**Classified infrastructure (7):** `Eq.mpr` (eq-machinery), `Union.union` (structure-projection), `Set.instUnion` (typeclass-instance), `id` (eq-machinery), `congrArg` (eq-machinery), `Iff.mpr` (logic-core,structure-projection), `And.intro` (logic-core,logic-core-ctor)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Set` (1 args) : <sort>
- `Set` (1 args) : <sort>
- `TopologicalSpace` (1 args) : <sort>
- `IsOpen` (3 args) : <sort>
- `IsOpen` (3 args) : <sort>
- `Eq.mpr` (4 args) : IsOpen [Prop]
  - `IsOpen` (3 args) : <sort>
    - `Union.union` (4 args) : Set
      - `Set` (1 args) : <sort>
      - `Set.instUnion` (1 args) : Union
  - `IsOpen` (3 args) : <sort>
    - `Set.iUnion` (3 args) : Set
      - `Bool` (0 args)
      - `Bool` (0 args)
      - `cond` (4 args) : Set
        - `Set` (1 args) : <sort>
  - `id` (2 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `IsOpen` (3 args) : <sort>
        - `Union.union` (4 args) : Set
          - `Set` (1 args) : <sort>
          - `Set.instUnion` (1 args) : Union
      - `IsOpen` (3 args) : <sort>
        - `Set.iUnion` (3 args) : Set
          - `Bool` (0 args)
          - `Bool` (0 args)
          - `cond` (4 args) : Set
            - `Set` (1 args) : <sort>
    - `congrArg` (6 args) : Eq [Prop]
      - `Set` (1 args) : <sort>
  ... (74 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Set.union_eq_iUnion` (3 args) : Eq (depth 3)
- `isOpen_iUnion` (5 args) : IsOpen (depth 1)
- `Bool.forall_bool` (1 args) : Iff (depth 3)

## P5 — source-level use events  [observed]

- `rewrite` → `Set.union_eq_iUnion` — `rewrite  [ union_eq_iUnion ]`
- `exact` → `isOpen_iUnion` — `exact isOpen_iUnion (Bool.forall_bool.2 ⟨h₂, h₁⟩)`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Set` — def, module `Mathlib.Data.Set.Defs`
- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `IsOpen` — def, module `Mathlib.Topology.Defs.Basic`
- `Set.iUnion` — def, module `Mathlib.Order.SetNotation`
- `Bool` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
