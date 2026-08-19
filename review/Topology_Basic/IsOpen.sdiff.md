# IsOpen.sdiff

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* term · *proof-term size:* 69 nodes

## Statement and source  [lean-exact]

```lean
theorem IsOpen.sdiff (h₁ : IsOpen s) (h₂ : IsClosed t) : IsOpen (s \ t) :=
  IsOpen.inter h₁ h₂.isOpen_compl
```

Exact proof reference: record decl `d19` in `studies/Topology_Basic.study.json` (type `x1042`, value `x1059`).

## P2 — support set (body)  [deterministic-derived]

**Domain (6):** `Set`, `TopologicalSpace`, `IsOpen`, `IsClosed`, `IsOpen.inter`, `False`

**Classified infrastructure (3):** `Membership.mem` (structure-projection), `Set.instMembership` (typeclass-instance), `IsClosed.isOpen_compl` (structure-projection)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Set` (1 args) : <sort>
- `Set` (1 args) : <sort>
- `TopologicalSpace` (1 args) : <sort>
- `IsOpen` (3 args) : <sort>
- `IsClosed` (3 args) : <sort>
- `IsOpen.inter` (6 args) : IsOpen [Prop]
  - `Membership.mem` (5 args) : <sort>
    - `Set` (1 args) : <sort>
    - `Set.instMembership` (1 args) : Membership
  - `False` (0 args)
  - `IsClosed.isOpen_compl` (4 args) : IsOpen [Prop]

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `IsOpen.inter` (6 args) : IsOpen (depth 0)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Set` — def, module `Mathlib.Data.Set.Defs`
- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `IsOpen` — def, module `Mathlib.Topology.Defs.Basic`
- `IsClosed` — inductive, module `Mathlib.Topology.Defs.Basic`
- `IsOpen.inter` — axiom, module `Mathlib.Topology.Defs.Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
