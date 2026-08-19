# Bool.involutive_not

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* term · *proof-term size:* 1 nodes

## Statement and source  [lean-exact]

```lean
theorem _root_.Bool.involutive_not : Involutive not :=
  Bool.not_not
```

Exact proof reference: record decl `d0` in `studies/Logic_Function_Basic.study.json` (type `x4`, value `x5`).

## P2 — support set (body)  [deterministic-derived]

**Domain (1):** `Bool.not_not`

**Classified infrastructure (0):** (none)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Bool.not_not` (0 args)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

(none)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Bool.not_not` — axiom, module `Init.SimpLemmas`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
