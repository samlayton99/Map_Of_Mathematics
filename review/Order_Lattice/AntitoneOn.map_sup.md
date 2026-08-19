# AntitoneOn.map_sup

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* automation · *proof-term size:* 1329 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual]
theorem map_sup [SemilatticeInf β] (hf : AntitoneOn f s) (hx : x ∈ s) (hy : y ∈ s) :
    f (x ⊔ y) = f x ⊓ f y := by
  cases le_total x y <;> have := hf ?_ ?_ ‹_› <;>
    first
    | assumption
    | simp only [*, sup_of_le_left, sup_of_le_right, inf_of_le_left, inf_of_le_right]
```

Exact proof reference: record decl `d10` in `studies/Order_Lattice.study.json` (type `x1912`, value `x2066`).

## P2 — support set (body)  [deterministic-derived]

**Domain (14):** `Set`, `LinearOrder`, `SemilatticeInf`, `AntitoneOn`, `Or`, `Eq`, `le_total`, `of_eq_true`, `True`, `sup_of_le_right`, `inf_of_le_right`, `eq_self`, `sup_of_le_left`, `inf_of_le_left`

**Classified infrastructure (22):** `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeInf.toPartialOrder` (structure-projection,typeclass-instance), `Lattice.toSemilatticeInf` (typeclass-instance), `DistribLattice.toLattice` (structure-projection,typeclass-instance), `instDistribLatticeOfLinearOrder` (typeclass-instance), `Membership.mem` (structure-projection), `Set.instMembership` (typeclass-instance), `Or.casesOn` (generated), `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `LinearOrder.toPartialOrder` (structure-projection,typeclass-instance), `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `Lattice.toSemilatticeSup` (structure-projection,typeclass-instance), `Min.min` (structure-projection), `SemilatticeInf.toMin` (typeclass-instance), `Or.inl` (logic-core,logic-core-ctor), `Eq.trans` (eq-machinery), `congr` (eq-machinery), `congrArg` (eq-machinery), `Or.inr` (logic-core,logic-core-ctor), `Eq.refl` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Set` (1 args) : <sort>
- `LinearOrder` (1 args) : <sort>
- `SemilatticeInf` (1 args) : <sort>
- `AntitoneOn` (6 args) : <sort>
  - `PartialOrder.toPreorder` (2 args) : Preorder
    - `SemilatticeInf.toPartialOrder` (2 args) : PartialOrder
      - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
        - `DistribLattice.toLattice` (2 args) : Lattice
          - `instDistribLatticeOfLinearOrder` (2 args) : DistribLattice
  - `PartialOrder.toPreorder` (2 args) : Preorder
    - `SemilatticeInf.toPartialOrder` (2 args) : PartialOrder
- `Membership.mem` (5 args) : <sort>
  - `Set` (1 args) : <sort>
  - `Set.instMembership` (1 args) : Membership
- `Membership.mem` (5 args) : <sort>
  - `Set` (1 args) : <sort>
  - `Set.instMembership` (1 args) : Membership
- `Or.casesOn` (7 args) : Eq [Prop]
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `LinearOrder.toPartialOrder` (2 args) : PartialOrder
  - `LE.le` (4 args) : <sort>
    - `Preorder.toLE` (2 args) : LE
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `LinearOrder.toPartialOrder` (2 args) : PartialOrder
  - `Or` (2 args) : <sort>
    - `LE.le` (4 args) : <sort>
      - `Preorder.toLE` (2 args) : LE
        - `PartialOrder.toPreorder` (2 args) : Preorder
  ... (220 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `le_total` (4 args) : Or (depth 2)
- `le_total` (4 args) : Or (depth 1)
- `of_eq_true` (2 args) : Eq (depth 1)
- `sup_of_le_right` (5 args) : Eq (depth 6)
- `inf_of_le_right` (5 args) : Eq (depth 4)
- `eq_self` (2 args) : Eq (depth 3)
- `sup_of_le_left` (5 args) : Eq (depth 6)
- `inf_of_le_left` (5 args) : Eq (depth 4)

## P5 — source-level use events  [observed]

- `cases` → `le_total` — `cases le_total x y`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  have := hf ?_ ?_ ‹_› ;  ?  _`
- `simp` → `sup_of_le_left`, `sup_of_le_right`, `inf_of_le_left`, `inf_of_le_right`, `sup_of_le_left`, `sup_of_le_right`, `inf_of_le_left`, `inf_of_le_right` — `simp only [*, sup_of_le_left, sup_of_le_right, inf_of_le_left, inf_of_le_right]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Set` — def, module `Mathlib.Data.Set.Defs`
- `LinearOrder` — inductive, module `Mathlib.Order.Defs.LinearOrder`
- `SemilatticeInf` — inductive, module `Lattice`
- `AntitoneOn` — def, module `Mathlib.Order.Monotone.Defs`
- `Or` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
