# DistribLattice.le_sup_inf

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* term · *proof-term size:* 8 nodes

## Statement and source  [lean-exact]

```lean
  protected le_sup_inf : ∀ x y z : α, (x ⊔ y) ⊓ (x ⊔ z) ≤ x ⊔ y ⊓ z
```

Exact proof reference: record decl `d21` in `studies/Order_Lattice.study.json` (type `x2863`, value `x2866`).

## P2 — support set (body)  [deterministic-derived]

**Domain (1):** `DistribLattice`

**Classified infrastructure (0):** (none)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `DistribLattice` (1 args) : <sort>

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

(none)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `DistribLattice` — inductive, module `Lattice`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
