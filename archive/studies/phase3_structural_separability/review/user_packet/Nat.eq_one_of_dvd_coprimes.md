# Review packet — `Nat.eq_one_of_dvd_coprimes`

*domain file:* Data_Nat_GCD_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
/-- If `k:ℕ` divides coprime `a` and `b` then `k = 1` -/
theorem eq_one_of_dvd_coprimes {a b k : ℕ} (h_ab_coprime : Coprime a b) (hka : k ∣ a)
    (hkb : k ∣ b) : k = 1
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V1:** `Nat`, `Nat.Coprime`, `Dvd.dvd`, `Nat.instDvd`, `Iff.mp`, `OfNat.ofNat`, `instOfNatNat`, `Eq`
**V3:** `Nat`, `Dvd.dvd`, `Nat.instCommMonoid`, `CommMonoid.toMonoid`, `Iff.mp`, `Nat.instDvd`, `OfNat.ofNat`, `Nat.Coprime`
**V2:** `Nat.coprime_iff_isRelPrime`, `CommMonoid.toMonoid`, `Dvd.dvd`, `Eq`, `Iff.mp`, `IsRelPrime`, `IsUnit`, `Monoid.toMulOneClass`
**V4:** `Nat`, `Nat.Coprime`, `Eq`, `Nat.dvd_one`, `IsUnit`, `isUnit_iff_dvd_one`, `IsRelPrime`, `Nat.coprime_iff_isRelPrime`
**V5:** `Nat.dvd_one`, `isUnit_iff_dvd_one`, `Nat.coprime_iff_isRelPrime`, `Dvd.dvd`, `Iff.mp`, `Nat`, `Nat.Coprime`, `Eq`
**V6:** `Nat`, `Dvd.dvd`, `Nat.Coprime`, `Nat.instDvd`, `Iff.mp`, `OfNat.ofNat`, `Eq`, `instOfNatNat`
**V7:** `Nat`, `Nat.Coprime`, `Dvd.dvd`, `Eq`, `Nat.instDvd`, `Iff.mp`, `OfNat.ofNat`, `Nat.instCommMonoid`
**V8:** `Nat.dvd_one`, `isUnit_iff_dvd_one`, `Nat.coprime_iff_isRelPrime`, `Nat`, `Nat.Coprime`, `Dvd.dvd`, `Eq`, `Nat.instDvd`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
/-- If `k:ℕ` divides coprime `a` and `b` then `k = 1` -/
theorem eq_one_of_dvd_coprimes {a b k : ℕ} (h_ab_coprime : Coprime a b) (hka : k ∣ a)
    (hkb : k ∣ b) : k = 1 :=
  dvd_one.mp (isUnit_iff_dvd_one.mp <| coprime_iff_isRelPrime.mp h_ab_coprime hka hkb)

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
