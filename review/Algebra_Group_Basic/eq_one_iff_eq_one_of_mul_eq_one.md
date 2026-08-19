# eq_one_iff_eq_one_of_mul_eq_one

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 1057 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive]
theorem eq_one_iff_eq_one_of_mul_eq_one {a b : M} (h : a * b = 1) : a = 1 ↔ b = 1 := by
  constructor <;> (rintro rfl; simpa using h)
```

Exact proof reference: record decl `d213` in `studies/Algebra_Group_Basic.study.json` (type `x16860`, value `x17005`).

## P2 — support set (body)  [deterministic-derived]

**Domain (5):** `MulOneClass`, `Eq`, `congrFun'`, `one_mul`, `mul_one`

**Classified infrastructure (12):** `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `MulOne.toMul` (structure-projection,typeclass-instance), `MulOneClass.toMulOne` (structure-projection,typeclass-instance), `OfNat.ofNat` (structure-projection), `One.toOfNat1` (typeclass-instance), `MulOne.toOne` (structure-projection,typeclass-instance), `Iff.intro` (logic-core,logic-core-ctor), `Eq.ndrec` (eq-machinery,generated), `Eq.mp` (eq-machinery), `congrArg` (eq-machinery), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `MulOneClass` (1 args) : <sort>
- `Eq` (3 args) : <sort>
  - `HMul.hMul` (6 args) : <local>
    - `instHMul` (2 args) : HMul
      - `MulOne.toMul` (2 args) : Mul
        - `MulOneClass.toMulOne` (2 args) : MulOne
  - `OfNat.ofNat` (3 args) : <local>
    - `One.toOfNat1` (2 args) : OfNat
      - `MulOne.toOne` (2 args) : One
        - `MulOneClass.toMulOne` (2 args) : MulOne
- `Iff.intro` (4 args) : Iff [Prop]
  - `Eq` (3 args) : <sort>
    - `OfNat.ofNat` (3 args) : <local>
      - `One.toOfNat1` (2 args) : OfNat
        - `MulOne.toOne` (2 args) : One
          - `MulOneClass.toMulOne` (2 args) : MulOne
  - `Eq` (3 args) : <sort>
    - `OfNat.ofNat` (3 args) : <local>
      - `One.toOfNat1` (2 args) : OfNat
        - `MulOne.toOne` (2 args) : One
          - `MulOneClass.toMulOne` (2 args) : MulOne
  - `Eq` (3 args) : <sort>
    - `OfNat.ofNat` (3 args) : <local>
      - `One.toOfNat1` (2 args) : OfNat
        - `MulOne.toOne` (2 args) : One
          - `MulOneClass.toMulOne` (2 args) : MulOne
  - `Eq.ndrec` (7 args) : Eq [Prop]
    - `OfNat.ofNat` (3 args) : <local>
      - `One.toOfNat1` (2 args) : OfNat
        - `MulOne.toOne` (2 args) : One
  ... (195 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `congrFun'` (6 args) : Eq (depth 3)
- `one_mul` (3 args) : Eq (depth 5)
- `mul_one` (3 args) : Eq (depth 5)

## P5 — source-level use events  [observed]

- `constructor` → (no named attribution) — `constructor`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `MulOneClass` — inductive, module `Mathlib.Algebra.Group.Defs`
- `Eq` — inductive, module `Init.Prelude`
- `congrFun'` — axiom, module `Init.Prelude`
- `one_mul` — axiom, module `Mathlib.Algebra.Group.Defs`
- `mul_one` — axiom, module `Mathlib.Algebra.Group.Defs`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
