# div_eq_div_iff_div_eq_div

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 3835 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive]
theorem div_eq_div_iff_div_eq_div : a / b = c / d ↔ a / c = b / d := by
  rw [div_eq_iff_eq_mul, div_mul_eq_mul_div, div_eq_iff_eq_mul', mul_div_assoc]
```

Exact proof reference: record decl `d134` in `studies/Algebra_Group_Basic.study.json` (type `x11339`, value `x11543`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `CommGroup`, `Iff`, `Eq`, `div_eq_iff_eq_mul`, `div_mul_eq_mul_div`, `div_eq_iff_eq_mul'`, `mul_div_assoc`

**Classified infrastructure (19):** `Eq.mpr` (eq-machinery), `HDiv.hDiv` (structure-projection), `instHDiv` (typeclass-instance), `DivInvMonoid.toDiv` (structure-projection,typeclass-instance), `Group.toDivInvMonoid` (structure-projection,typeclass-instance), `CommGroup.toGroup` (structure-projection,typeclass-instance), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `MulOne.toMul` (structure-projection,typeclass-instance), `MulOneClass.toMulOne` (structure-projection,typeclass-instance), `Monoid.toMulOneClass` (typeclass-instance), `DivInvMonoid.toMonoid` (structure-projection,typeclass-instance), `id` (eq-machinery), `congrArg` (eq-machinery), `propext` (eq-machinery), `DivisionMonoid.toDivInvMonoid` (structure-projection,typeclass-instance), `DivisionCommMonoid.toDivisionMonoid` (structure-projection,typeclass-instance), `CommGroup.toDivisionCommMonoid` (typeclass-instance), `Iff.rfl` (logic-core)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `CommGroup` (1 args) : <sort>
- `Eq.mpr` (4 args) : Iff [Prop]
  - `Iff` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `HDiv.hDiv` (6 args) : <local>
        - `instHDiv` (2 args) : HDiv
          - `DivInvMonoid.toDiv` (2 args) : Div
            - `Group.toDivInvMonoid` (2 args) : DivInvMonoid
              - `CommGroup.toGroup` (2 args) : Group
      - `HDiv.hDiv` (6 args) : <local>
        - `instHDiv` (2 args) : HDiv
          - `DivInvMonoid.toDiv` (2 args) : Div
            - `Group.toDivInvMonoid` (2 args) : DivInvMonoid
              - `CommGroup.toGroup` (2 args) : Group
    - `Eq` (3 args) : <sort>
      - `HDiv.hDiv` (6 args) : <local>
        - `instHDiv` (2 args) : HDiv
          - `DivInvMonoid.toDiv` (2 args) : Div
            - `Group.toDivInvMonoid` (2 args) : DivInvMonoid
              - `CommGroup.toGroup` (2 args) : Group
      - `HDiv.hDiv` (6 args) : <local>
        - `instHDiv` (2 args) : HDiv
          - `DivInvMonoid.toDiv` (2 args) : Div
            - `Group.toDivInvMonoid` (2 args) : DivInvMonoid
              - `CommGroup.toGroup` (2 args) : Group
  - `Iff` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `HMul.hMul` (6 args) : <local>
        - `instHMul` (2 args) : HMul
          - `MulOne.toMul` (2 args) : Mul
  ... (710 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `div_eq_iff_eq_mul` (5 args) : Iff (depth 4)
- `div_mul_eq_mul_div` (5 args) : Eq (depth 4)
- `div_eq_iff_eq_mul'` (5 args) : Iff (depth 6)
- `mul_div_assoc` (5 args) : Eq (depth 6)

## P5 — source-level use events  [observed]

- `rewrite` → `div_eq_iff_eq_mul`, `div_mul_eq_mul_div`, `div_eq_iff_eq_mul'`, `mul_div_assoc` — `rewrite  [ div_eq_iff_eq_mul, div_mul_eq_mul_div, div_eq_iff_eq_mul', mul_div_as`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `CommGroup` — inductive, module `Mathlib.Algebra.Group.Defs`
- `Iff` — inductive, module `Init.Core`
- `Eq` — inductive, module `Init.Prelude`
- `div_eq_iff_eq_mul` — theorem, module `Basic`
- `div_mul_eq_mul_div` — theorem, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
