# Nat.pow_sub_one_gcd_pow_sub_one

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* automation · *proof-term size:* 21 nodes

## Statement and source  [lean-exact]

```lean
@[simp]
theorem pow_sub_one_gcd_pow_sub_one (a b c : ℕ) :
    gcd (a ^ b - 1) (a ^ c - 1) = a ^ gcd b c - 1 := by
  rcases eq_zero_or_pos b with rfl | hb
  · simp
  replace hb : c % b < b := mod_lt c hb
  rw [gcd_rec, pow_sub_one_mod_pow_sub_one, pow_sub_one_gcd_pow_sub_one, ← gcd_rec]
```

Exact proof reference: record decl `d69` in `studies/Data_Nat_GCD_Basic.study.json` (type `x4734`, value `x4746`).

## P2 — support set (body)  [deterministic-derived]

**Domain (2):** `Nat`, `PSigma.mk`

**Classified infrastructure (1):** `Nat.pow_sub_one_gcd_pow_sub_one._unary` (internal-detail)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `Nat` (0 args)
- `Nat.pow_sub_one_gcd_pow_sub_one._unary` (2 args) : Eq [Prop]
  - `PSigma.mk` (4 args) : PSigma
    - `Nat` (0 args)
    - `Nat` (0 args)
    - `Nat` (0 args)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

(none)

## P5 — source-level use events  [observed]

- `refine` → (no named attribution) — `refine  no_implicit_lambda%  have hb : c % b < b := mod_lt c hb ;  ?  _`
- `simp` → `Lean.Meta.Simp.Config.unfoldPartialApp`, `Bool.true`, `Lean.Meta.Simp.Config.zetaDelta`, `Bool.true`, `Lean.Meta.Simp.Config.failIfUnchanged`, `Bool.false`, `invImage`, `InvImage`, `Prod.lex`, `sizeOfWFRel`, `measure`, `Nat.lt_wfRel`, `WellFoundedRelation.rel`, `sizeOf_nat` — `simp  +  unfoldPartialApp  +  zetaDelta  -  failIfUnchanged  only  [  invImage  `
- `simp` → (no named attribution) — `simp`
- `rewrite` → `Nat.gcd_rec`, `Nat.pow_sub_one_mod_pow_sub_one`, `Nat.gcd_rec` — `rewrite  [ gcd_rec, pow_sub_one_mod_pow_sub_one, pow_sub_one_gcd_pow_sub_one, ← `

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `PSigma.mk` — constructor, module `Init.Core`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
