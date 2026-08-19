# IsClosed.and

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* term · *proof-term size:* 39 nodes

## Statement and source  [lean-exact]

```lean
@[closedness .]
theorem IsClosed.and :
    IsClosed { x | p₁ x } → IsClosed { x | p₂ x } → IsClosed { x | p₁ x ∧ p₂ x } :=
  IsClosed.inter
```

Exact proof reference: record decl `d10` in `studies/Topology_Basic.study.json` (type `x510`, value `x521`).

## P2 — support set (body)  [deterministic-derived]

**Domain (3):** `TopologicalSpace`, `IsClosed.inter`, `Set.ofPred`

**Classified infrastructure (0):** (none)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `TopologicalSpace` (1 args) : <sort>
- `IsClosed.inter` (4 args) : <pi> [Prop]
  - `Set.ofPred` (2 args) : Set
  - `Set.ofPred` (2 args) : Set

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `IsClosed.inter` (4 args) : <pi> (depth 0)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `IsClosed.inter` — theorem, module `Basic`
- `Set.ofPred` — def, module `Mathlib.Data.Set.Defs`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
