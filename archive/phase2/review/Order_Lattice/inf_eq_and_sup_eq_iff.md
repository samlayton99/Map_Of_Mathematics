# inf_eq_and_sup_eq_iff

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* tactic-other · *proof-term size:* 1471 nodes

## Statement and source  [lean-exact]

```lean
@[to_dual]
lemma inf_eq_and_sup_eq_iff : a ⊓ b = c ∧ a ⊔ b = c ↔ a = c ∧ b = c := by
  refine ⟨fun h ↦ ?_, ?_⟩
  · obtain rfl := sup_eq_inf.1 (h.2.trans h.1.symm)
    simpa using h
  · rintro ⟨rfl, rfl⟩
    exact ⟨inf_idem _, sup_idem _⟩
```

Exact proof reference: record decl `d344` in `studies/Order_Lattice.study.json` (type `x24978`, value `x25251`).

## P2 — support set (body)  [deterministic-derived]

**Domain (11):** `Lattice`, `And`, `Eq`, `and_self`, `congrFun'`, `inf_of_le_left`, `of_eq_true`, `sup_of_le_left`, `sup_eq_inf`, `inf_idem`, `sup_idem`

**Classified infrastructure (27):** `Iff.intro` (logic-core,logic-core-ctor), `Min.min` (structure-projection), `SemilatticeInf.toMin` (typeclass-instance), `Lattice.toSemilatticeInf` (typeclass-instance), `Max.max` (structure-projection), `SemilatticeSup.toMax` (typeclass-instance), `Lattice.toSemilatticeSup` (structure-projection,typeclass-instance), `Eq.ndrec` (eq-machinery,generated), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `Eq.mp` (eq-machinery), `Eq.trans` (eq-machinery), `congr` (eq-machinery), `congrArg` (eq-machinery), `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `SemilatticeInf.toPartialOrder` (structure-projection,typeclass-instance), `Std.le_refl._simp_1` (internal-detail), `instReflLe` (typeclass-instance), `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `Iff.mp` (logic-core,structure-projection), `And.right` (logic-core,structure-projection), `Eq.symm` (eq-machinery), `And.left` (logic-core,structure-projection), `And.casesOn` (generated), `And.intro` (logic-core,logic-core-ctor)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Lattice` (1 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `And` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Min.min` (4 args) : <local>
        - `SemilatticeInf.toMin` (2 args) : Min
          - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
    - `Eq` (3 args) : <sort>
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
          - `Lattice.toSemilatticeSup` (2 args) : SemilatticeSup
  - `And` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
    - `Eq` (3 args) : <sort>
  - `And` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Min.min` (4 args) : <local>
        - `SemilatticeInf.toMin` (2 args) : Min
          - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
    - `Eq` (3 args) : <sort>
      - `Max.max` (4 args) : <local>
        - `SemilatticeSup.toMax` (2 args) : Max
          - `Lattice.toSemilatticeSup` (2 args) : SemilatticeSup
  - `Eq.ndrec` (7 args) : And [Prop]
    - `And` (2 args) : <sort>
      - `Eq` (3 args) : <sort>
        - `Min.min` (4 args) : <local>
          - `SemilatticeInf.toMin` (2 args) : Min
            - `Lattice.toSemilatticeInf` (2 args) : SemilatticeInf
      - `Eq` (3 args) : <sort>
  ... (255 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `and_self` (1 args) : Eq (depth 4)
- `congrFun'` (6 args) : Eq (depth 7)
- `inf_of_le_left` (5 args) : Eq (depth 9)
- `of_eq_true` (2 args) : LE.le (depth 10)
- `congrFun'` (6 args) : Eq (depth 6)
- `sup_of_le_left` (5 args) : Eq (depth 8)
- `of_eq_true` (2 args) : LE.le (depth 9)
- `and_self` (1 args) : Eq (depth 5)
- `sup_eq_inf` (4 args) : Iff (depth 3)
- `inf_idem` (3 args) : Eq (depth 5)
- `sup_idem` (3 args) : Eq (depth 5)

## P5 — source-level use events  [observed]

- `refine` → `Iff.intro` — `refine ⟨fun h ↦ ?_, ?_⟩`
- `exact` → `And.intro` — `exact ⟨inf_idem _, sup_idem _⟩`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Lattice` — inductive, module `Lattice`
- `And` — inductive, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`
- `and_self` — axiom, module `Init.SimpLemmas`
- `congrFun'` — axiom, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
