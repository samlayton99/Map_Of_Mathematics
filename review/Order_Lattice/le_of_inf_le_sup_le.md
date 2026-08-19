# le_of_inf_le_sup_le

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* rewrite · *proof-term size:* 3563 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual self (reorder := x y, h₁ h₂)]
theorem le_of_inf_le_sup_le (h₁ : x ⊓ z ≤ y ⊓ z) (h₂ : x ⊔ z ≤ y ⊔ z) : x ≤ y :=
  calc
    x ≤ y ⊓ z ⊔ x := le_sup_right
    _ = (y ⊔ x) ⊓ (x ⊔ z) := by rw [sup_inf_right, sup_comm x]
    _ ≤ (y ⊔ x) ⊓ (y ⊔ z) := inf_le_inf_left _ h₂
    _ = y ⊔ x ⊓ z := by rw [← sup_inf_left]
    _ ≤ y ⊔ y ⊓ z := sup_le_sup_left h₁ _
    _ ≤ _ := sup_le (le_refl y) inf_le_left
```

Exact proof reference: record decl `d428` in `studies/Order_Lattice.study.json` (type `x28633`, value `x28810`).

## P2 — support set (body)  [deterministic-derived]

**Domain (11):** `DistribLattice`, `Eq`, `le_sup_right`, `sup_inf_right`, `sup_comm`, `inf_le_inf_left`, `sup_inf_left`, `sup_le_sup_left`, `sup_le`, `le_refl`, `inf_le_left`

**Classified infrastructure (19):** `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeInf.toPartialOrder` (structure-projection,typeclass-instance), `Lattice.toSemilatticeInf` (typeclass-instance), `DistribLattice.toLattice` (structure-projection,typeclass-instance), `Min.min` (structure-projection), `SemilatticeInf.toMin` (typeclass-instance), `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `Lattice.toSemilatticeSup` (structure-projection,typeclass-instance), `Trans.trans` (eq-machinery,structure-projection), `instTransLE` (typeclass-instance), `instTransEq_1` (typeclass-instance), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.refl` (eq-machinery), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `DistribLattice` (1 args) : <sort>
- `LE.le` (4 args) : <sort>
  - `Preorder.toLE` (2 args) : LE
    - `PartialOrder.toPreorder` (2 args) : Preorder
      - `SemilatticeInf.toPartialOrder` (2 args) : PartialOrder
        - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
          - `DistribLattice.toLattice` (2 args) : Lattice
  - `Min.min` (4 args) : <local>
    - `SemilatticeInf.toMin` (2 args) : Min
      - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
        - `DistribLattice.toLattice` (2 args) : Lattice
  - `Min.min` (4 args) : <local>
    - `SemilatticeInf.toMin` (2 args) : Min
      - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
        - `DistribLattice.toLattice` (2 args) : Lattice
- `LE.le` (4 args) : <sort>
  - `Preorder.toLE` (2 args) : LE
    - `PartialOrder.toPreorder` (2 args) : Preorder
      - `SemilatticeInf.toPartialOrder` (2 args) : PartialOrder
        - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
          - `DistribLattice.toLattice` (2 args) : Lattice
  - `Max.max` (4 args) : <local>
    - `SemilatticeSup.toMax` (2 args) : Max
      - `Lattice.toSemilatticeSup` (2 args) : SemilatticeSup
        - `DistribLattice.toLattice` (2 args) : Lattice
  - `Max.max` (4 args) : <local>
    - `SemilatticeSup.toMax` (2 args) : Max
      - `Lattice.toSemilatticeSup` (2 args) : SemilatticeSup
        - `DistribLattice.toLattice` (2 args) : Lattice
- `Trans.trans` (12 args) : LE.le [Prop]
  ... (698 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `le_sup_right` (4 args) : LE.le (depth 5)
- `sup_inf_right` (5 args) : Eq (depth 8)
- `sup_comm` (4 args) : Eq (depth 9)
- `inf_le_inf_left` (6 args) : LE.le (depth 4)
- `sup_inf_left` (5 args) : Eq (depth 7)
- `sup_le_sup_left` (6 args) : LE.le (depth 2)
- `sup_le` (7 args) : LE.le (depth 1)
- `le_refl` (3 args) : LE.le (depth 2)
- `inf_le_left` (4 args) : LE.le (depth 2)

## P5 — source-level use events  [observed]

- `rewrite` → `sup_inf_left` — `rewrite  [ ← sup_inf_left ]`
- `rewrite` → `sup_inf_right`, `sup_comm` — `rewrite  [ sup_inf_right, sup_comm x ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `DistribLattice` — inductive, module `Lattice`
- `Eq` — inductive, module `Init.Prelude`
- `le_sup_right` — theorem, module `Lattice`
- `sup_inf_right` — theorem, module `Lattice`
- `sup_comm` — theorem, module `Lattice`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
