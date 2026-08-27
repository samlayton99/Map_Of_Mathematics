# Nat.eq_one_of_dvd_coprimes

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* term · *proof-term size:* 173 nodes

## Statement and source  [lean-exact]

```lean
/-- If `k:ℕ` divides coprime `a` and `b` then `k = 1` -/
theorem eq_one_of_dvd_coprimes {a b k : ℕ} (h_ab_coprime : Coprime a b) (hka : k ∣ a)
    (hkb : k ∣ b) : k = 1 :=
  dvd_one.mp (isUnit_iff_dvd_one.mp <| coprime_iff_isRelPrime.mp h_ab_coprime hka hkb)
```

Exact proof reference: record decl `d63` in `studies/Data_Nat_GCD_Basic.study.json` (type `x4100`, value `x4134`).

## P2 — support set (body)  [deterministic-derived]

**Domain (8):** `Nat`, `Nat.Coprime`, `Eq`, `Nat.dvd_one`, `IsUnit`, `isUnit_iff_dvd_one`, `IsRelPrime`, `Nat.coprime_iff_isRelPrime`

**Classified infrastructure (14):** `Dvd.dvd` (structure-projection), `Nat.instDvd` (typeclass-instance), `Iff.mp` (logic-core,structure-projection), `OfNat.ofNat` (structure-projection), `instOfNatNat` (typeclass-instance), `CommMonoid.toMonoid` (structure-projection,typeclass-instance), `Nat.instCommMonoid` (typeclass-instance), `semigroupDvd` (typeclass-instance), `Monoid.toSemigroup` (structure-projection,typeclass-instance), `One.toOfNat1` (typeclass-instance), `MulOne.toOne` (structure-projection,typeclass-instance), `MulOneClass.toMulOne` (structure-projection,typeclass-instance), `Monoid.toMulOneClass` (typeclass-instance), `Nat.instMonoid` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `Nat` (0 args)
- `Nat.Coprime` (2 args) : <sort>
- `Dvd.dvd` (4 args) : <sort>
  - `Nat` (0 args)
  - `Nat.instDvd` (0 args)
- `Dvd.dvd` (4 args) : <sort>
  - `Nat` (0 args)
  - `Nat.instDvd` (0 args)
- `Iff.mp` (4 args) : Eq [Prop]
  - `Dvd.dvd` (4 args) : <sort>
    - `Nat` (0 args)
    - `Nat.instDvd` (0 args)
    - `OfNat.ofNat` (3 args) : Nat
      - `Nat` (0 args)
      - `instOfNatNat` (1 args) : OfNat
  - `Eq` (3 args) : <sort>
    - `Nat` (0 args)
    - `OfNat.ofNat` (3 args) : Nat
      - `Nat` (0 args)
      - `instOfNatNat` (1 args) : OfNat
  - `Nat.dvd_one` (1 args) : Iff [Prop]
  - `Iff.mp` (4 args) : Dvd.dvd [Prop]
    - `IsUnit` (3 args) : <sort>
      - `Nat` (0 args)
      - `CommMonoid.toMonoid` (2 args) : Monoid
        - `Nat` (0 args)
        - `Nat.instCommMonoid` (0 args)
    - `Dvd.dvd` (4 args) : <sort>
  ... (60 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Nat.dvd_one` (1 args) : Iff (depth 1)
- `isUnit_iff_dvd_one` (3 args) : Iff (depth 2)
- `Nat.coprime_iff_isRelPrime` (2 args) : Iff (depth 3)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `Nat.Coprime` — def, module `Init.Data.Nat.Coprime`
- `Eq` — inductive, module `Init.Prelude`
- `Nat.dvd_one` — axiom, module `Init.Data.Nat.Dvd`
- `IsUnit` — def, module `Mathlib.Algebra.Group.Units.Defs`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
