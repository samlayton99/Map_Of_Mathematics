# isClosed_iUnion_of_finite

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* automation · *proof-term size:* 405 nodes

## Statement and source  [lean-exact]

```lean
@[closedness .]
theorem isClosed_iUnion_of_finite [Finite ι] {s : ι → Set X} (h : ∀ i, IsClosed (s i)) :
    IsClosed (⋃ i, s i) := by
  simp only [← isOpen_compl_iff, compl_iUnion] at *
  exact isOpen_iInter_of_finite h
```

Exact proof reference: record decl `d45` in `studies/Topology_Basic.study.json` (type `x3435`, value `x3498`).

## P2 — support set (body)  [deterministic-derived]

**Domain (11):** `TopologicalSpace`, `Finite`, `Set`, `IsClosed`, `Set.iUnion`, `IsOpen`, `Set.iInter`, `Eq`, `Set.compl_iUnion`, `isOpen_iInter_of_finite`, `forall_congr`

**Classified infrastructure (8):** `Eq.mpr` (eq-machinery), `Compl.compl` (structure-projection), `Set.instCompl` (typeclass-instance), `id` (eq-machinery), `Eq.trans` (eq-machinery), `_private.Basic.0.IsClosed.union._simp_1` (internal-detail), `congrArg` (eq-machinery), `Eq.mp` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `TopologicalSpace` (1 args) : <sort>
- `Finite` (1 args) : <sort>
- `Set` (1 args) : <sort>
- `IsClosed` (3 args) : <sort>
- `Eq.mpr` (4 args) : IsClosed [Prop]
  - `IsClosed` (3 args) : <sort>
    - `Set.iUnion` (3 args) : Set
  - `IsOpen` (3 args) : <sort>
    - `Set.iInter` (3 args) : Set
      - `Compl.compl` (3 args) : Set
        - `Set` (1 args) : <sort>
        - `Set.instCompl` (1 args) : Compl
  - `id` (2 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `IsClosed` (3 args) : <sort>
        - `Set.iUnion` (3 args) : Set
      - `IsOpen` (3 args) : <sort>
        - `Set.iInter` (3 args) : Set
          - `Compl.compl` (3 args) : Set
            - `Set` (1 args) : <sort>
            - `Set.instCompl` (1 args) : Compl
    - `Eq.trans` (6 args) : Eq [Prop]
      - `IsClosed` (3 args) : <sort>
        - `Set.iUnion` (3 args) : Set
      - `IsOpen` (3 args) : <sort>
        - `Compl.compl` (3 args) : Set
          - `Set` (1 args) : <sort>
          - `Set.instCompl` (1 args) : Compl
          - `Set.iUnion` (3 args) : Set
      - `IsOpen` (3 args) : <sort>
  ... (65 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Set.compl_iUnion` (3 args) : Eq (depth 4)
- `isOpen_iInter_of_finite` (6 args) : IsOpen (depth 1)
- `forall_congr` (4 args) : Eq (depth 3)

## P5 — source-level use events  [observed]

- `exact` → `isOpen_iInter_of_finite` — `exact isOpen_iInter_of_finite h`
- `simp` → `Set.compl_iUnion`, `isOpen_compl_iff`, `Set.compl_iUnion` — `simp only [← isOpen_compl_iff, compl_iUnion] at *`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `Finite` — inductive, module `Mathlib.Data.Finite.Defs`
- `Set` — def, module `Mathlib.Data.Set.Defs`
- `IsClosed` — inductive, module `Mathlib.Topology.Defs.Basic`
- `Set.iUnion` — def, module `Mathlib.Order.SetNotation`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
