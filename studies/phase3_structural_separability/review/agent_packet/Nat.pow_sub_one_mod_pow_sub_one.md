# Review packet — `Nat.pow_sub_one_mod_pow_sub_one`

*domain file:* Data_Nat_GCD_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[simp]
theorem pow_sub_one_mod_pow_sub_one (a b c : ℕ) : (a ^ c - 1) % (a ^ b - 1) = a ^ (c % b) - 1
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V5:** `Nat`, `WellFounded.Nat.fix`, `Eq`, `HMod.hMod`, `instHMod`, `Nat.instMod`, `HSub.hSub`, `instHSub`
**V2:** `Nat`, `Int`, `OfNat.ofNat`, `HSub.hSub`, `instHSub`, `instOfNatNat`, `instSubNat`, `Nat.instMonoid`
**V8:** `AddMonoid.toAddZeroClass`, `AddZero.toAdd`, `AddZero.toZero`, `AddZeroClass.toAddZero`, `And`, `And.left`, `And.right`, `Bool`
**V6:** `Nat`, `WellFounded.Nat.fix`, `Eq`, `InvImage`, `GT.gt`, `Or`, `Nat.eq_zero_or_pos`, `ite`
**V7:** `WellFounded.Nat.fix`, `Nat.eq_zero_or_pos`, `Nat.eq_or_lt_of_le`, `dite`, `of_eq_true`, `lt_or_ge`, `congrFun'`, `eq_self`
**V4:** `Nat`, `Eq`, `HSub.hSub`, `OfNat.ofNat`, `HMod.hMod`, `instHSub`, `HPow.hPow`, `instOfNatNat`
**V1:** `Nat`, `Eq`, `WellFounded.Nat.fix`, `InvImage`, `HMod.hMod`, `OfNat.ofNat`, `HSub.hSub`, `instSubNat`
**V3:** `WellFounded.Nat.fix`, `InvImage`, `Nat.mod_self`, `zero_pow_eq`, `Nat.mod_eq_of_lt`, `Nat.add_mod_right`, `Nat.add_sub_assoc`, `Nat.mul_add_one`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[simp]
theorem pow_sub_one_mod_pow_sub_one (a b c : ℕ) : (a ^ c - 1) % (a ^ b - 1) = a ^ (c % b) - 1 := by
  rcases eq_zero_or_pos a with rfl | ha0
  · simp [zero_pow_eq]; split_ifs <;> simp
  rcases Nat.eq_or_lt_of_le ha0 with rfl | ha1
  · simp
  rcases eq_zero_or_pos b with rfl | hb0
  · simp
  rcases lt_or_ge c b with h | h
  · rw [mod_eq_of_lt, mod_eq_of_lt h]
    rwa [Nat.sub_lt_sub_iff_right (one_le_pow c a ha0), Nat.pow_lt_pow_iff_right ha1]
  · suffices a ^ (c - b + b) - 1 = a ^ (c - b) * (a ^ b - 1) + (a ^ (c - b) - 1) by
      rw [← Nat.sub_add_cancel h, add_mod_right, this, add_mod, mul_mod, mod_self,
        mul_zero, zero_mod, zero_add, mod_mod, pow_sub_one_mod_pow_sub_one]
    rw [← Nat.add_sub_assoc (one_le_pow (c - b) a ha0), ← mul_add_one, pow_add,
      Nat.sub_add_cancel (one_le_pow b a ha0)]

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
