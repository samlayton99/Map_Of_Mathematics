# zpow_add_one

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* automation · *proof-term size:* 11873 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive add_one_zsmul]
lemma zpow_add_one (a : G) : ∀ n : ℤ, a ^ (n + 1) = a ^ n * a
  | (n : ℕ) => by simp only [← Int.natCast_succ, zpow_natCast, pow_succ]
  | -1 => by simp [Int.add_left_neg]
  | .negSucc (n + 1) => by
    rw [zpow_negSucc, pow_succ', mul_inv_rev, inv_mul_cancel_right]
    rw [Int.negSucc_eq, Int.neg_add, Int.neg_add_cancel_right]
    exact zpow_negSucc _ _
```

Exact proof reference: record decl `d500` in `studies/Algebra_Group_Basic.study.json` (type `x37884`, value `x38198`).

## P2 — support set (body)  [deterministic-derived]

**Domain (27):** `Group`, `Int`, `Eq`, `Nat`, `of_eq_true`, `Nat.cast`, `True`, `Nat.succ`, `zpow_natCast`, `pow_succ`, `congrFun'`, `eq_self`, `Unit`, `Int.add_left_neg`, `zpow_ofNat`, `pow_zero`, `zpow_neg`, `pow_one`, `inv_mul_cancel`, `Int.negSucc`, `zpow_negSucc`, `pow_succ'`, `mul_inv_rev`, `inv_mul_cancel_right`, `Int.negSucc_eq`, `Int.neg_add`, `Int.neg_add_cancel_right`

**Classified infrastructure (38):** `_private.Basic.0.zpow_add_one.match_1` (internal-detail,generated), `HPow.hPow` (structure-projection), `instHPow` (typeclass-instance), `ZPow.toPow` (typeclass-instance), `DivInvMonoid.toZPow` (structure-projection,typeclass-instance), `Group.toDivInvMonoid` (structure-projection,typeclass-instance), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `Int.instAdd` (typeclass-instance), `OfNat.ofNat` (structure-projection), `instOfNat` (typeclass-instance), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `MulOne.toMul` (structure-projection,typeclass-instance), `MulOneClass.toMulOne` (structure-projection,typeclass-instance), `Monoid.toMulOneClass` (typeclass-instance), `DivInvMonoid.toMonoid` (structure-projection,typeclass-instance), `instNatCastInt` (typeclass-instance), `Eq.trans` (eq-machinery), `NPow.toPow` (typeclass-instance), `Monoid.toNPow` (structure-projection,typeclass-instance), `congr` (eq-machinery), `congrArg` (eq-machinery), `Neg.neg` (structure-projection), `Int.instNegInt` (typeclass-instance), `One.toOfNat1` (typeclass-instance), `MulOne.toOne` (structure-projection,typeclass-instance), `instOfNatNat` (typeclass-instance), `Inv.inv` (structure-projection), `InvOneClass.toInv` (structure-projection,typeclass-instance), `DivInvOneMonoid.toInvOneClass` (typeclass-instance), `DivisionMonoid.toDivInvOneMonoid` (typeclass-instance), `Group.toDivisionMonoid` (typeclass-instance), `DivisionMonoid.toDivInvMonoid` (structure-projection,typeclass-instance), `Eq.mpr` (eq-machinery), `instAddNat` (typeclass-instance), `DivInvMonoid.toInv` (structure-projection,typeclass-instance), `id` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Group` (1 args) : <sort>
- `Int` (0 args)
- `_private.Basic.0.zpow_add_one.match_1` (5 args) : Eq [Prop]
  - `Int` (0 args)
  - `Eq` (3 args) : <sort>
    - `HPow.hPow` (6 args) : <local>
      - `Int` (0 args)
      - `instHPow` (3 args) : HPow
        - `Int` (0 args)
        - `ZPow.toPow` (2 args) : Pow
          - `DivInvMonoid.toZPow` (2 args) : ZPow
            - `Group.toDivInvMonoid` (2 args) : DivInvMonoid
      - `HAdd.hAdd` (6 args) : Int
        - `Int` (0 args)
        - `Int` (0 args)
        - `Int` (0 args)
        - `instHAdd` (2 args) : HAdd
          - `Int` (0 args)
          - `Int.instAdd` (0 args)
        - `OfNat.ofNat` (3 args) : Int
          - `Int` (0 args)
          - `instOfNat` (1 args) : OfNat
    - `HMul.hMul` (6 args) : <local>
      - `instHMul` (2 args) : HMul
        - `MulOne.toMul` (2 args) : Mul
          - `MulOneClass.toMulOne` (2 args) : MulOne
            - `Monoid.toMulOneClass` (2 args) : MulOneClass
              - `DivInvMonoid.toMonoid` (2 args) : Monoid
                - `Group.toDivInvMonoid` (2 args) : DivInvMonoid
      - `HPow.hPow` (6 args) : <local>
  ... (3414 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `of_eq_true` (2 args) : Eq (depth 1)
- `zpow_natCast` (4 args) : Eq (depth 6)
- `pow_succ` (4 args) : Eq (depth 6)
- `congrFun'` (6 args) : Eq (depth 4)
- `eq_self` (2 args) : Eq (depth 3)
- `Int.add_left_neg` (1 args) : Eq (depth 8)
- `zpow_ofNat` (4 args) : Eq (depth 7)
- `pow_zero` (3 args) : Eq (depth 6)
- `congrFun'` (6 args) : Eq (depth 5)
- `zpow_neg` (4 args) : Eq (depth 8)
- `zpow_ofNat` (4 args) : Eq (depth 10)
- `pow_one` (3 args) : Eq (depth 10)
- `inv_mul_cancel` (3 args) : Eq (depth 5)
- `zpow_negSucc` (4 args) : Eq (depth 4)
- `pow_succ'` (4 args) : Eq (depth 5)
- `mul_inv_rev` (4 args) : Eq (depth 6)
- `inv_mul_cancel_right` (4 args) : Eq (depth 7)
- `Int.negSucc_eq` (1 args) : Eq (depth 8)
- `Int.neg_add` (2 args) : Eq (depth 9)
- `Int.neg_add_cancel_right` (2 args) : Eq (depth 10)
- `zpow_negSucc` (4 args) : Eq (depth 8)

## P5 — source-level use events  [observed]

- `exact` → `zpow_negSucc` — `exact zpow_negSucc _ _`
- `simp` → `Int.add_left_neg`, `Int.add_left_neg` — `simp [Int.add_left_neg]`
- `rewrite` → `Int.negSucc_eq`, `Int.neg_add`, `Int.neg_add_cancel_right` — `rewrite  [ Int.negSucc_eq, Int.neg_add, Int.neg_add_cancel_right ]`
- `rewrite` → `zpow_negSucc`, `pow_succ'`, `mul_inv_rev`, `inv_mul_cancel_right` — `rewrite  [ zpow_negSucc, pow_succ', mul_inv_rev, inv_mul_cancel_right ]`
- `simp` → `zpow_natCast`, `pow_succ`, `Int.natCast_succ`, `zpow_natCast`, `pow_succ` — `simp only [← Int.natCast_succ, zpow_natCast, pow_succ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Group` — inductive, module `Mathlib.Algebra.Group.Defs`
- `Int` — inductive, module `Init.Data.Int.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Nat` — inductive, module `Init.Prelude`
- `of_eq_true` — axiom, module `Init.SimpLemmas`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
