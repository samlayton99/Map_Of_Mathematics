# isClosed_sInter

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* term · *proof-term size:* 1117 nodes

## Statement and source  [lean-exact]

```lean
@[closedness .]
theorem isClosed_sInter {s : Set (Set X)} : (∀ t ∈ s, IsClosed t) → IsClosed (⋂₀ s) := by
  simpa only [← isOpen_compl_iff, compl_sInter, sUnion_image] using isOpen_biUnion
```

Exact proof reference: record decl `d47` in `studies/Topology_Basic.study.json` (type `x3589`, value `x3697`).

## P2 — support set (body)  [deterministic-derived]

**Domain (14):** `TopologicalSpace`, `Set`, `IsClosed`, `Set.sInter`, `IsOpen`, `Set.iUnion`, `Eq`, `implies_congr`, `forall_congr`, `Set.sUnion`, `Set.image`, `Set.compl_sInter`, `Set.sUnion_image`, `isOpen_biUnion`

**Classified infrastructure (10):** `Eq.mpr` (eq-machinery), `Membership.mem` (structure-projection), `Set.instMembership` (typeclass-instance), `Compl.compl` (structure-projection), `Set.instCompl` (typeclass-instance), `id` (eq-machinery), `Eq.refl` (eq-machinery), `_private.Basic.0.IsClosed.union._simp_1` (internal-detail), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `TopologicalSpace` (1 args) : <sort>
- `Set` (1 args) : <sort>
  - `Set` (1 args) : <sort>
- `Eq.mpr` (4 args) : <pi> [Prop]
  - `Set` (1 args) : <sort>
  - `Membership.mem` (5 args) : <sort>
    - `Set` (1 args) : <sort>
    - `Set` (1 args) : <sort>
      - `Set` (1 args) : <sort>
    - `Set.instMembership` (1 args) : Membership
      - `Set` (1 args) : <sort>
  - `IsClosed` (3 args) : <sort>
  - `IsClosed` (3 args) : <sort>
    - `Set.sInter` (2 args) : Set
  - `Set` (1 args) : <sort>
  - `Membership.mem` (5 args) : <sort>
    - `Set` (1 args) : <sort>
    - `Set` (1 args) : <sort>
      - `Set` (1 args) : <sort>
    - `Set.instMembership` (1 args) : Membership
      - `Set` (1 args) : <sort>
  - `IsOpen` (3 args) : <sort>
    - `Compl.compl` (3 args) : Set
      - `Set` (1 args) : <sort>
      - `Set.instCompl` (1 args) : Compl
  - `IsOpen` (3 args) : <sort>
    - `Set.iUnion` (3 args) : Set
      - `Set` (1 args) : <sort>
      - `Set` (1 args) : <sort>
      - `Set.iUnion` (3 args) : Set
  ... (277 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `implies_congr` (6 args) : Eq (depth 2)
- `forall_congr` (4 args) : Eq (depth 3)
- `implies_congr` (6 args) : Eq (depth 4)
- `Set.compl_sInter` (2 args) : Eq (depth 6)
- `Set.sUnion_image` (4 args) : Eq (depth 6)
- `isOpen_biUnion` (5 args) : <pi> (depth 1)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `Set` — def, module `Mathlib.Data.Set.Defs`
- `IsClosed` — inductive, module `Mathlib.Topology.Defs.Basic`
- `Set.sInter` — def, module `Mathlib.Order.SetNotation`
- `IsOpen` — def, module `Mathlib.Topology.Defs.Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
