# Review packet — `zpow_mul`

*domain file:* Algebra_Group_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[to_additive mul_zsmul'] lemma zpow_mul (a : α) : ∀ m n : ℤ, a ^ (m * n) = (a ^ m) ^ n
  | (m : ℕ), (n : ℕ) =>
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V2:** `DivisionMonoid`, `Int`, `_private.Basic.0.zpow_mul.match_1`, `Eq`, `HPow.hPow`, `instHPow`, `ZPow.toPow`, `DivInvMonoid.toZPow`
**V8:** `Nat`, `Int`, `DivisionMonoid.toDivInvMonoid`, `HPow.hPow`, `instHPow`, `HMul.hMul`, `instHMul`, `Nat.cast`
**V1:** `zpow_neg`, `inv_pow`, `DivisionMonoid.toDivInvOneMonoid`, `inv_inj`, `_private.Basic.0.zpow_mul.match_1`, `DivInvMonoid.toInv`, `DivInvMonoid.toMonoid`, `DivInvMonoid.toZPow`
**V7:** `DivisionMonoid`, `Int`, `Eq`, `Nat`, `Nat.cast`, `zpow_natCast`, `pow_mul`, `Int.negSucc`
**V3:** `zpow_natCast`, `zpow_negSucc`, `Int.negSucc_mul_negSucc`, `Int.ofNat_mul_negSucc`, `inv_pow`, `pow_mul`, `Int.negSucc_mul_ofNat`, `inv_inv`
**V6:** `Int`, `DivisionMonoid`, `Eq`, `HPow.hPow`, `instHPow`, `HMul.hMul`, `DivisionMonoid.toDivInvMonoid`, `Nat`
**V4:** `Int`, `Eq`, `DivisionMonoid`, `Nat`, `HPow.hPow`, `DivisionMonoid.toDivInvMonoid`, `instHPow`, `zpow_neg`
**V5:** `zpow_neg`, `zpow_natCast`, `inv_pow`, `zpow_negSucc`, `pow_mul`, `Int.negSucc_mul_negSucc`, `Int.ofNat_mul_negSucc`, `Int.negSucc_mul_ofNat`

## PART 2 — source proof (read only after Part 1 ratings)

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

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
