# sup_eq_and_inf_eq_iff

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* term · *proof-term size:* 1527 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual]
```

Exact proof reference: record decl `d472` in `studies/Order_Lattice.study.json` (type `x30364`, value `x30484`).

## P2 — support set (body)  [deterministic-derived]

**Domain (13):** `Lattice`, `And`, `Eq`, `and_self`, `congrFun'`, `sup_of_le_left`, `of_eq_true`, `eq_true`, `Std.ge_refl`, `inf_of_le_left`, `inf_eq_sup`, `sup_idem`, `inf_idem`

**Classified infrastructure (26):** `Iff.intro` (logic-core,logic-core-ctor), `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `Lattice.toSemilatticeSup` (structure-projection,typeclass-instance), `Min.min` (structure-projection), `SemilatticeInf.toMin` (typeclass-instance), `Lattice.toSemilatticeInf` (typeclass-instance), `Eq.ndrec` (eq-machinery,generated), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `Eq.mp` (eq-machinery), `Eq.trans` (eq-machinery), `congr` (eq-machinery), `congrArg` (eq-machinery), `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `instReflGe` (typeclass-instance), `SemilatticeInf.toPartialOrder` (structure-projection,typeclass-instance), `Iff.mp` (logic-core,structure-projection), `And.right` (logic-core,structure-projection), `Eq.symm` (eq-machinery), `And.left` (logic-core,structure-projection), `And.casesOn` (generated), `And.intro` (logic-core,logic-core-ctor)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Lattice` (1 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `And` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
          - `Lattice.toSemilatticeSup` (2 args) : SemilatticeSup
    - `Eq` (3 args) : <sort>
      - `Min.min` (4 args) : <local>
        - `SemilatticeInf.toMin` (2 args) : Min
          - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
  - `And` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
    - `Eq` (3 args) : <sort>
  - `And` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
          - `Lattice.toSemilatticeSup` (2 args) : SemilatticeSup
    - `Eq` (3 args) : <sort>
      - `Min.min` (4 args) : <local>
        - `SemilatticeInf.toMin` (2 args) : Min
          - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
  - `Eq.ndrec` (7 args) : And [Prop]
    - `And` (2 args) : <sort>
      - `Eq` (3 args) : <sort>
        - `Max.max` (4 args) : <local>
          - `SemilatticeSup.toMax` (2 args) : Max
            - `Lattice.toSemilatticeSup` (2 args) : SemilatticeSup
      - `Eq` (3 args) : <sort>
  ... (267 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `and_self` (1 args) : Eq (depth 4)
- `congrFun'` (6 args) : Eq (depth 7)
- `sup_of_le_left` (5 args) : Eq (depth 9)
- `of_eq_true` (2 args) : LE.le (depth 10)
- `eq_true` (2 args) : Eq (depth 11)
- `Std.ge_refl` (4 args) : LE.le (depth 12)
- `congrFun'` (6 args) : Eq (depth 6)
- `inf_of_le_left` (5 args) : Eq (depth 8)
- `of_eq_true` (2 args) : LE.le (depth 9)
- `eq_true` (2 args) : Eq (depth 10)
- `Std.ge_refl` (4 args) : LE.le (depth 11)
- `and_self` (1 args) : Eq (depth 5)
- `inf_eq_sup` (4 args) : Iff (depth 3)
- `sup_idem` (3 args) : Eq (depth 5)
- `inf_idem` (3 args) : Eq (depth 5)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Lattice` — inductive, module `Lattice`
- `And` — inductive, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`
- `and_self` — axiom, module `Init.SimpLemmas`
- `congrFun'` — axiom, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
