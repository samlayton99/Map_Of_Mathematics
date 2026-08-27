# mul_right_comm

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 1851 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive]
theorem mul_right_comm (a b c : G) : a * b * c = a * c * b := by
  rw [mul_assoc, mul_comm b, mul_assoc]
```

Exact proof reference: record decl `d327` in `studies/Algebra_Group_Basic.study.json` (type `x24119`, value `x24189`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `CommSemigroup`, `Eq`, `mul_assoc`, `mul_comm`

**Classified infrastructure (10):** `Eq.mpr` (eq-machinery), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `CommMagma.toMul` (structure-projection,typeclass-instance), `CommSemigroup.toCommMagma` (typeclass-instance), `Semigroup.toMul` (structure-projection,typeclass-instance), `CommSemigroup.toSemigroup` (structure-projection,typeclass-instance), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.refl` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `CommSemigroup` (1 args) : <sort>
- `Eq.mpr` (4 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `HMul.hMul` (6 args) : <local>
      - `instHMul` (2 args) : HMul
        - `CommMagma.toMul` (2 args) : Mul
          - `CommSemigroup.toCommMagma` (2 args) : CommMagma
      - `HMul.hMul` (6 args) : <local>
        - `instHMul` (2 args) : HMul
          - `CommMagma.toMul` (2 args) : Mul
            - `CommSemigroup.toCommMagma` (2 args) : CommMagma
    - `HMul.hMul` (6 args) : <local>
      - `instHMul` (2 args) : HMul
        - `CommMagma.toMul` (2 args) : Mul
          - `CommSemigroup.toCommMagma` (2 args) : CommMagma
      - `HMul.hMul` (6 args) : <local>
        - `instHMul` (2 args) : HMul
          - `CommMagma.toMul` (2 args) : Mul
            - `CommSemigroup.toCommMagma` (2 args) : CommMagma
  - `Eq` (3 args) : <sort>
    - `HMul.hMul` (6 args) : <local>
      - `instHMul` (2 args) : HMul
        - `Semigroup.toMul` (2 args) : Mul
          - `CommSemigroup.toSemigroup` (2 args) : Semigroup
      - `HMul.hMul` (6 args) : <local>
        - `instHMul` (2 args) : HMul
          - `Semigroup.toMul` (2 args) : Mul
            - `CommSemigroup.toSemigroup` (2 args) : Semigroup
    - `HMul.hMul` (6 args) : <local>
      - `instHMul` (2 args) : HMul
  ... (303 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `mul_assoc` (5 args) : Eq (depth 3)
- `mul_comm` (4 args) : Eq (depth 4)
- `mul_assoc` (5 args) : Eq (depth 5)

## P5 — source-level use events  [observed]

- `rewrite` → `mul_assoc`, `mul_comm`, `mul_assoc` — `rewrite  [ mul_assoc, mul_comm b, mul_assoc ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `CommSemigroup` — inductive, module `Mathlib.Algebra.Group.Defs`
- `Eq` — inductive, module `Init.Prelude`
- `mul_assoc` — axiom, module `Mathlib.Algebra.Group.Defs`
- `mul_comm` — axiom, module `Mathlib.Algebra.Group.Defs`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
