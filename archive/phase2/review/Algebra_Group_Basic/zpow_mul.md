# zpow_mul

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 27699 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive mul_zsmul'] lemma zpow_mul (a : α) : ∀ m n : ℤ, a ^ (m * n) = (a ^ m) ^ n
  | (m : ℕ), (n : ℕ) => by
    rw [zpow_natCast, zpow_natCast, ← pow_mul, ← zpow_natCast]
    rfl
  | (m : ℕ), .negSucc n => by
    rw [zpow_natCast, zpow_negSucc, ← pow_mul, Int.ofNat_mul_negSucc, zpow_neg, inv_inj,
      ← zpow_natCast]
  | .negSucc m, (n : ℕ) => by
    rw [zpow_natCast, zpow_negSucc, ← inv_pow, ← pow_mul, Int.negSucc_mul_ofNat, zpow_neg, inv_pow,
      inv_inj, ← zpow_natCast]
  | .negSucc m, .negSucc n => by
    rw [zpow_negSucc, zpow_negSucc, Int.negSucc_mul_negSucc, inv_pow, inv_inv, ← pow_mul, ←
      zpow_natCast]
    rfl
```

Exact proof reference: record decl `d508` in `studies/Algebra_Group_Basic.study.json` (type `x39117`, value `x39755`).

## P2 — support set (body)  [deterministic-derived]

**Domain (17):** `DivisionMonoid`, `Int`, `Eq`, `Nat`, `Nat.cast`, `zpow_natCast`, `pow_mul`, `Int.negSucc`, `zpow_negSucc`, `Nat.succ`, `Int.ofNat_mul_negSucc`, `zpow_neg`, `inv_inj`, `inv_pow`, `Int.negSucc_mul_ofNat`, `Int.negSucc_mul_negSucc`, `inv_inv`

**Classified infrastructure (34):** `_private.Basic.0.zpow_mul.match_1` (internal-detail,generated), `HPow.hPow` (structure-projection), `instHPow` (typeclass-instance), `ZPow.toPow` (typeclass-instance), `DivInvMonoid.toZPow` (structure-projection,typeclass-instance), `DivisionMonoid.toDivInvMonoid` (structure-projection,typeclass-instance), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `Int.instMul` (typeclass-instance), `Eq.mpr` (eq-machinery), `instNatCastInt` (typeclass-instance), `NPow.toPow` (typeclass-instance), `Monoid.toNPow` (structure-projection,typeclass-instance), `DivInvMonoid.toMonoid` (structure-projection,typeclass-instance), `id` (eq-machinery), `congrArg` (eq-machinery), `instMulNat` (typeclass-instance), `Eq.symm` (eq-machinery), `Eq.refl` (eq-machinery), `Inv.inv` (structure-projection), `DivInvMonoid.toInv` (structure-projection,typeclass-instance), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `instAddNat` (typeclass-instance), `OfNat.ofNat` (structure-projection), `instOfNatNat` (typeclass-instance), `Neg.neg` (structure-projection), `Int.instNegInt` (typeclass-instance), `InvOneClass.toInv` (structure-projection,typeclass-instance), `DivInvOneMonoid.toInvOneClass` (typeclass-instance), `DivisionMonoid.toDivInvOneMonoid` (typeclass-instance), `InvolutiveInv.toInv` (structure-projection,typeclass-instance), `DivisionMonoid.toInvolutiveInv` (typeclass-instance), `propext` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `DivisionMonoid` (1 args) : <sort>
- `Int` (0 args)
- `Int` (0 args)
- `_private.Basic.0.zpow_mul.match_1` (7 args) : Eq [Prop]
  - `Int` (0 args)
  - `Int` (0 args)
  - `Eq` (3 args) : <sort>
    - `HPow.hPow` (6 args) : <local>
      - `Int` (0 args)
      - `instHPow` (3 args) : HPow
        - `Int` (0 args)
        - `ZPow.toPow` (2 args) : Pow
          - `DivInvMonoid.toZPow` (2 args) : ZPow
            - `DivisionMonoid.toDivInvMonoid` (2 args) : DivInvMonoid
      - `HMul.hMul` (6 args) : Int
        - `Int` (0 args)
        - `Int` (0 args)
        - `Int` (0 args)
        - `instHMul` (2 args) : HMul
          - `Int` (0 args)
          - `Int.instMul` (0 args)
    - `HPow.hPow` (6 args) : <local>
      - `Int` (0 args)
      - `instHPow` (3 args) : HPow
        - `Int` (0 args)
        - `ZPow.toPow` (2 args) : Pow
          - `DivInvMonoid.toZPow` (2 args) : ZPow
            - `DivisionMonoid.toDivInvMonoid` (2 args) : DivInvMonoid
      - `HPow.hPow` (6 args) : <local>
        - `Int` (0 args)
  ... (8378 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `zpow_natCast` (4 args) : Eq (depth 4)
- `zpow_natCast` (4 args) : Eq (depth 5)
- `pow_mul` (5 args) : Eq (depth 7)
- `zpow_natCast` (4 args) : Eq (depth 8)
- `zpow_negSucc` (4 args) : Eq (depth 5)
- `Int.ofNat_mul_negSucc` (2 args) : Eq (depth 7)
- `zpow_neg` (4 args) : Eq (depth 8)
- `inv_inj` (4 args) : Iff (depth 10)
- `zpow_natCast` (4 args) : Eq (depth 11)
- `inv_pow` (4 args) : Eq (depth 7)
- `pow_mul` (5 args) : Eq (depth 8)
- `Int.negSucc_mul_ofNat` (2 args) : Eq (depth 8)
- `zpow_neg` (4 args) : Eq (depth 9)
- `inv_pow` (4 args) : Eq (depth 10)
- `inv_inj` (4 args) : Iff (depth 12)
- `zpow_natCast` (4 args) : Eq (depth 13)
- `zpow_negSucc` (4 args) : Eq (depth 4)
- `Int.negSucc_mul_negSucc` (2 args) : Eq (depth 6)
- `inv_inv` (3 args) : Eq (depth 8)
- `pow_mul` (5 args) : Eq (depth 10)
  ... (27 occurrences total)

## P5 — source-level use events  [observed]

- `rewrite` → `zpow_negSucc`, `zpow_negSucc`, `Int.negSucc_mul_negSucc`, `inv_pow`, `inv_inv`, `pow_mul`, `zpow_natCast` — `rewrite  [ zpow_negSucc, zpow_negSucc, Int.negSucc_mul_negSucc, inv_pow, inv_inv`
- `rewrite` → `zpow_natCast`, `zpow_negSucc`, `pow_mul`, `Int.ofNat_mul_negSucc`, `zpow_neg`, `inv_inj`, `zpow_natCast` — `rewrite  [ zpow_natCast, zpow_negSucc, ← pow_mul, Int.ofNat_mul_negSucc, zpow_ne`
- `rewrite` → `zpow_natCast`, `zpow_negSucc`, `inv_pow`, `pow_mul`, `Int.negSucc_mul_ofNat`, `zpow_neg`, `inv_pow`, `inv_inj`, `zpow_natCast` — `rewrite  [ zpow_natCast, zpow_negSucc, ← inv_pow, ← pow_mul, Int.negSucc_mul_ofN`
- `rewrite` → `zpow_natCast`, `zpow_natCast`, `pow_mul`, `zpow_natCast` — `rewrite  [ zpow_natCast, zpow_natCast, ← pow_mul, ← zpow_natCast ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `DivisionMonoid` — inductive, module `Mathlib.Algebra.Group.Defs`
- `Int` — inductive, module `Init.Data.Int.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Nat` — inductive, module `Init.Prelude`
- `Nat.cast` — def, module `Init.Data.Cast`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
