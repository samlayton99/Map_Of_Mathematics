# Nat.gcd_right_comm

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 481 nodes

## Statement and source  [lean-exact]

```lean
theorem gcd_right_comm (a b c : ℕ) : gcd (gcd a b) c = gcd (gcd a c) b := by
  rw [gcd_assoc, gcd_assoc, gcd_comm b c]
```

Exact proof reference: record decl `d67` in `studies/Data_Nat_GCD_Basic.study.json` (type `x4616`, value `x4685`).

## P2 — support set (body)  [deterministic-derived]

**Domain (5):** `Nat`, `Eq`, `Nat.gcd`, `Nat.gcd_assoc`, `Nat.gcd_comm`

**Classified infrastructure (4):** `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.refl` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `Nat` (0 args)
- `Eq.mpr` (4 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `Nat` (0 args)
    - `Nat.gcd` (2 args) : Nat
      - `Nat.gcd` (2 args) : Nat
    - `Nat.gcd` (2 args) : Nat
      - `Nat.gcd` (2 args) : Nat
  - `Eq` (3 args) : <sort>
    - `Nat` (0 args)
    - `Nat.gcd` (2 args) : Nat
      - `Nat.gcd` (2 args) : Nat
    - `Nat.gcd` (2 args) : Nat
      - `Nat.gcd` (2 args) : Nat
  - `id` (2 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
        - `Nat` (0 args)
        - `Nat.gcd` (2 args) : Nat
          - `Nat.gcd` (2 args) : Nat
        - `Nat.gcd` (2 args) : Nat
          - `Nat.gcd` (2 args) : Nat
      - `Eq` (3 args) : <sort>
        - `Nat` (0 args)
        - `Nat.gcd` (2 args) : Nat
          - `Nat.gcd` (2 args) : Nat
        - `Nat.gcd` (2 args) : Nat
          - `Nat.gcd` (2 args) : Nat
  ... (123 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Nat.gcd_assoc` (3 args) : Eq (depth 3)
- `Nat.gcd_assoc` (3 args) : Eq (depth 4)
- `Nat.gcd_comm` (2 args) : Eq (depth 5)

## P5 — source-level use events  [observed]

- `rewrite` → `Nat.gcd_assoc`, `Nat.gcd_assoc`, `Nat.gcd_comm` — `rewrite  [ gcd_assoc, gcd_assoc, gcd_comm b c ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`
- `Nat.gcd` — axiom, module `Init.Data.Nat.Gcd`
- `Nat.gcd_assoc` — axiom, module `Init.Data.Nat.Gcd`
- `Nat.gcd_comm` — axiom, module `Init.Data.Nat.Gcd`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
