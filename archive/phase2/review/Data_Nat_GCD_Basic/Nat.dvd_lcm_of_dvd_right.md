# Nat.dvd_lcm_of_dvd_right

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* term · *proof-term size:* 39 nodes

## Statement and source  [lean-exact]

```lean
theorem dvd_lcm_of_dvd_right {a b : ℕ} (h : a ∣ b) (c : ℕ) : a ∣ lcm c b :=
  h.trans (dvd_lcm_right c b)
```

Exact proof reference: record decl `d60` in `studies/Data_Nat_GCD_Basic.study.json` (type `x1170`, value `x4062`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `Nat`, `Dvd.dvd.trans`, `Nat.lcm`, `Nat.dvd_lcm_right`

**Classified infrastructure (3):** `Dvd.dvd` (structure-projection), `Nat.instDvd` (typeclass-instance), `Nat.instSemigroup` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `Dvd.dvd` (4 args) : <sort>
  - `Nat` (0 args)
  - `Nat.instDvd` (0 args)
- `Nat` (0 args)
- `Dvd.dvd.trans` (7 args) : Dvd.dvd [Prop]
  - `Nat` (0 args)
  - `Nat.instSemigroup` (0 args)
  - `Nat.lcm` (2 args) : Nat
  - `Nat.dvd_lcm_right` (2 args) : Dvd.dvd [Prop]

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Dvd.dvd.trans` (7 args) : Dvd.dvd (depth 0)
- `Nat.dvd_lcm_right` (2 args) : Dvd.dvd (depth 1)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `Dvd.dvd.trans` — axiom, module `Mathlib.Algebra.Divisibility.Basic`
- `Nat.lcm` — def, module `Init.Data.Nat.Lcm`
- `Nat.dvd_lcm_right` — axiom, module `Init.Data.Nat.Lcm`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
