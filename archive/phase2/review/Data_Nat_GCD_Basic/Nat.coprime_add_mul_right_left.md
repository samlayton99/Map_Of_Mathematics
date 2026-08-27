# Nat.coprime_add_mul_right_left

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 1103 nodes

## Statement and source  [lean-exact]

```lean
@[simp]
theorem coprime_add_mul_right_left (m n k : ℕ) : Coprime (m + k * n) n ↔ Coprime m n := by
  rw [Coprime, Coprime, gcd_add_mul_right_left]
```

Exact proof reference: record decl `d21` in `studies/Data_Nat_GCD_Basic.study.json` (type `x1642`, value `x1701`).

## P2 — support set (body)  [deterministic-derived]

**Domain (6):** `Nat`, `Iff`, `Nat.Coprime`, `Eq`, `Nat.gcd`, `Nat.gcd_add_mul_right_left`

**Classified infrastructure (13):** `Eq.mpr` (eq-machinery), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `instAddNat` (typeclass-instance), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `instMulNat` (typeclass-instance), `OfNat.ofNat` (structure-projection), `instOfNatNat` (typeclass-instance), `id` (eq-machinery), `congrArg` (eq-machinery), `Nat.Coprime.eq_1` (internal-detail,generated), `Iff.rfl` (logic-core)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `Nat` (0 args)
- `Eq.mpr` (4 args) : Iff [Prop]
  - `Iff` (2 args) : <sort>
    - `Nat.Coprime` (2 args) : <sort>
      - `HAdd.hAdd` (6 args) : Nat
        - `Nat` (0 args)
        - `Nat` (0 args)
        - `Nat` (0 args)
        - `instHAdd` (2 args) : HAdd
          - `Nat` (0 args)
          - `instAddNat` (0 args)
        - `HMul.hMul` (6 args) : Nat
          - `Nat` (0 args)
          - `Nat` (0 args)
          - `Nat` (0 args)
          - `instHMul` (2 args) : HMul
            - `Nat` (0 args)
            - `instMulNat` (0 args)
    - `Nat.Coprime` (2 args) : <sort>
  - `Iff` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Nat` (0 args)
      - `Nat.gcd` (2 args) : Nat
        - `HAdd.hAdd` (6 args) : Nat
          - `Nat` (0 args)
          - `Nat` (0 args)
          - `Nat` (0 args)
          - `instHAdd` (2 args) : HAdd
  ... (390 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Nat.gcd_add_mul_right_left` (3 args) : Eq (depth 5)

## P5 — source-level use events  [observed]

- `rewrite` → `Nat.Coprime`, `Nat.Coprime.eq_1`, `Nat.Coprime`, `Nat.Coprime.eq_1`, `Nat.gcd_add_mul_right_left` — `rewrite  [ Coprime, Coprime, gcd_add_mul_right_left ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `Iff` — inductive, module `Init.Core`
- `Nat.Coprime` — def, module `Init.Data.Nat.Coprime`
- `Eq` — inductive, module `Init.Prelude`
- `Nat.gcd` — axiom, module `Init.Data.Nat.Gcd`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
