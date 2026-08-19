# TopologicalSpace.ext_iff

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 191 nodes

## Statement and source  [lean-exact]

```lean
protected theorem TopologicalSpace.ext_iff {t t' : TopologicalSpace X} :
    t = t' ↔ ∀ s, IsOpen[t] s ↔ IsOpen[t'] s :=
  ⟨fun h _ => h ▸ Iff.rfl, fun h => by ext; exact h _⟩
```

Exact proof reference: record decl `d25` in `studies/Topology_Basic.study.json` (type `x1758`, value `x1806`).

## P2 — support set (body)  [deterministic-derived]

**Domain (6):** `TopologicalSpace`, `Eq`, `Set`, `Iff`, `IsOpen`, `TopologicalSpace.ext`

**Classified infrastructure (5):** `Iff.intro` (logic-core,logic-core-ctor), `Eq.rec` (eq-machinery,generated,recursor), `Iff.rfl` (logic-core), `funext` (eq-machinery), `propext` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `TopologicalSpace` (1 args) : <sort>
- `TopologicalSpace` (1 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `Eq` (3 args) : <sort>
    - `TopologicalSpace` (1 args) : <sort>
  - `Set` (1 args) : <sort>
  - `Iff` (2 args) : <sort>
    - `IsOpen` (3 args) : <sort>
    - `IsOpen` (3 args) : <sort>
  - `Eq` (3 args) : <sort>
    - `TopologicalSpace` (1 args) : <sort>
  - `Set` (1 args) : <sort>
  - `Eq.rec` (6 args) : Iff [Prop]
    - `TopologicalSpace` (1 args) : <sort>
    - `TopologicalSpace` (1 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `TopologicalSpace` (1 args) : <sort>
    - `Iff` (2 args) : <sort>
      - `IsOpen` (3 args) : <sort>
      - `IsOpen` (3 args) : <sort>
    - `Iff.rfl` (1 args) : Iff [Prop]
      - `IsOpen` (3 args) : <sort>
  - `Set` (1 args) : <sort>
  - `Iff` (2 args) : <sort>
    - `IsOpen` (3 args) : <sort>
    - `IsOpen` (3 args) : <sort>
  - `TopologicalSpace.ext` (4 args) : Eq [Prop]
    - `funext` (5 args) : Eq [Prop]
      - `Set` (1 args) : <sort>
      - `Set` (1 args) : <sort>
  ... (36 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `TopologicalSpace.ext` (4 args) : Eq (depth 1)

## P5 — source-level use events  [observed]

- `exact` → (no named attribution) — `exact h _`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Set` — def, module `Mathlib.Data.Set.Defs`
- `Iff` — inductive, module `Init.Core`
- `IsOpen` — def, module `Mathlib.Topology.Defs.Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
