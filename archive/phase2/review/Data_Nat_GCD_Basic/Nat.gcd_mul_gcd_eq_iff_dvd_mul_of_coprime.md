# Nat.gcd_mul_gcd_eq_iff_dvd_mul_of_coprime

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 419 nodes

## Statement and source  [lean-exact]

```lean
theorem gcd_mul_gcd_eq_iff_dvd_mul_of_coprime (hcop : Coprime n m) :
    gcd x n * gcd x m = x ↔ x ∣ n * m := by
  refine ⟨fun h ↦ ?_, (dvd_antisymm ?_ <| dvd_gcd_mul_gcd_iff_dvd_mul.mpr ·)⟩
  refine h ▸ Nat.mul_dvd_mul ?_ ?_ <;> exact x.gcd_dvd_right _
  refine (hcop.gcd_both x x).mul_dvd_of_dvd_of_dvd ?_ ?_ <;> exact x.gcd_dvd_left _
```

Exact proof reference: record decl `d65` in `studies/Data_Nat_GCD_Basic.study.json` (type `x4203`, value `x4272`).

## P2 — support set (body)  [deterministic-derived]

**Domain (12):** `Nat`, `Nat.Coprime`, `Eq`, `Nat.gcd`, `Nat.mul_dvd_mul`, `Nat.gcd_dvd_right`, `dvd_antisymm`, `Units`, `Nat.Coprime.mul_dvd_of_dvd_of_dvd`, `Nat.Coprime.gcd_both`, `Nat.gcd_dvd_left`, `Nat.dvd_gcd_mul_gcd_iff_dvd_mul`

**Classified infrastructure (14):** `Iff.intro` (logic-core,logic-core-ctor), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `instMulNat` (typeclass-instance), `Dvd.dvd` (structure-projection), `Nat.instDvd` (typeclass-instance), `Eq.rec` (eq-machinery,generated,recursor), `Nat.instCommMonoidWithZero` (typeclass-instance), `Nat.instIsCancelMulZero` (typeclass-instance), `Unique.instSubsingleton` (typeclass-instance), `MonoidWithZero.toMonoid` (structure-projection,typeclass-instance), `CommMonoidWithZero.toMonoidWithZero` (typeclass-instance), `Nat.unique_units` (typeclass-instance), `Iff.mpr` (logic-core,structure-projection)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `Nat` (0 args)
- `Nat.Coprime` (2 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `Eq` (3 args) : <sort>
    - `Nat` (0 args)
    - `HMul.hMul` (6 args) : Nat
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `instHMul` (2 args) : HMul
        - `Nat` (0 args)
        - `instMulNat` (0 args)
      - `Nat.gcd` (2 args) : Nat
      - `Nat.gcd` (2 args) : Nat
  - `Dvd.dvd` (4 args) : <sort>
    - `Nat` (0 args)
    - `Nat.instDvd` (0 args)
    - `HMul.hMul` (6 args) : Nat
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `instHMul` (2 args) : HMul
        - `Nat` (0 args)
        - `instMulNat` (0 args)
  - `Eq` (3 args) : <sort>
    - `Nat` (0 args)
    - `HMul.hMul` (6 args) : Nat
      - `Nat` (0 args)
  ... (137 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Nat.mul_dvd_mul` (6 args) : Dvd.dvd (depth 2)
- `Nat.gcd_dvd_right` (2 args) : Dvd.dvd (depth 3)
- `dvd_antisymm` (8 args) : Eq (depth 1)
- `Nat.Coprime.mul_dvd_of_dvd_of_dvd` (6 args) : Dvd.dvd (depth 2)
- `Nat.Coprime.gcd_both` (5 args) : Nat.Coprime (depth 3)
- `Nat.gcd_dvd_left` (2 args) : Dvd.dvd (depth 3)
- `Nat.dvd_gcd_mul_gcd_iff_dvd_mul` (3 args) : Iff (depth 3)

## P5 — source-level use events  [observed]

- `refine` → `Eq.rec` — `refine h ▸ Nat.mul_dvd_mul ?_ ?_`
- `refine` → `Nat.Coprime.mul_dvd_of_dvd_of_dvd` — `refine (hcop.gcd_both x x).mul_dvd_of_dvd_of_dvd ?_ ?_`
- `exact` → `Nat.gcd_dvd_right` — `exact x.gcd_dvd_right _`
- `refine` → `Iff.intro` — `refine ⟨fun h ↦ ?_, (dvd_antisymm ?_ <| dvd_gcd_mul_gcd_iff_dvd_mul.mpr ·)⟩`
- `exact` → `Nat.gcd_dvd_left` — `exact x.gcd_dvd_left _`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `Nat.Coprime` — def, module `Init.Data.Nat.Coprime`
- `Eq` — inductive, module `Init.Prelude`
- `Nat.gcd` — axiom, module `Init.Data.Nat.Gcd`
- `Nat.mul_dvd_mul` — axiom, module `Init.Data.Nat.Dvd`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
