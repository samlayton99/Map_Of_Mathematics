# Real.range_log

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* term · *proof-term size:* 9 nodes

## Statement and source  [lean-exact]

```lean
@[simp]
theorem range_log : range log = univ :=
  log_surjective.range_eq
```

Exact proof reference: record decl `d123` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x17752`, value `x17758`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `Function.Surjective.range_eq`, `Real`, `Real.log`, `Real.log_surjective`

**Classified infrastructure (0):** (none)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Function.Surjective.range_eq` (4 args) : Eq [Prop]
  - `Real` (0 args)
  - `Real` (0 args)
  - `Real.log` (0 args)
  - `Real.log_surjective` (0 args)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Function.Surjective.range_eq` (4 args) : Eq (depth 0)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Function.Surjective.range_eq` — axiom, module `Mathlib.Data.Set.Image`
- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Real.log` — def, module `Basic`
- `Real.log_surjective` — theorem, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
