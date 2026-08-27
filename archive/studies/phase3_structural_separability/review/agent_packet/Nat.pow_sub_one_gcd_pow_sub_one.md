# Review packet — `Nat.pow_sub_one_gcd_pow_sub_one`

*domain file:* Data_Nat_GCD_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[simp]
theorem pow_sub_one_gcd_pow_sub_one (a b c : ℕ) :
    gcd (a ^ b - 1) (a ^ c - 1) = a ^ gcd b c - 1
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V1:** `Nat`, `Nat.pow_sub_one_gcd_pow_sub_one._unary`, `PSigma.mk`
**V3:** `Nat`, `Nat.pow_sub_one_gcd_pow_sub_one._unary`, `PSigma.mk`
**V7:** `Nat.pow_sub_one_gcd_pow_sub_one._unary`, `Nat`, `PSigma.mk`
**V2:** `Nat`, `PSigma.mk`, `Nat.pow_sub_one_gcd_pow_sub_one._unary`
**V6:** `Nat`, `Nat.pow_sub_one_gcd_pow_sub_one._unary`, `PSigma.mk`
**V5:** `Nat`, `Nat.pow_sub_one_gcd_pow_sub_one._unary`, `PSigma.mk`
**V4:** `Nat`, `PSigma.mk`, `Nat.pow_sub_one_gcd_pow_sub_one._unary`
**V8:** `Nat`, `PSigma.mk`, `Nat.pow_sub_one_gcd_pow_sub_one._unary`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[simp]
theorem pow_sub_one_gcd_pow_sub_one (a b c : ℕ) :
    gcd (a ^ b - 1) (a ^ c - 1) = a ^ gcd b c - 1 := by
  rcases eq_zero_or_pos b with rfl | hb
  · simp
  replace hb : c % b < b := mod_lt c hb
  rw [gcd_rec, pow_sub_one_mod_pow_sub_one, pow_sub_one_gcd_pow_sub_one, ← gcd_rec]

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
