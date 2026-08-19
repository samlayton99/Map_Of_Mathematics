# Real.le_exp_of_log_le

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 309 nodes

## Statement and source  [lean-exact]

```lean
/-- One direction of `Real.log_le_iff_le_exp` without positivity assumption. -/
lemma le_exp_of_log_le (h : log x ≤ y) : x ≤ exp y := by
  rcases le_or_gt x 0 with hx | hx
  · exact hx.trans <| exp_nonneg y
  · exact (log_le_iff_le_exp hx).mp h
```

Exact proof reference: record decl `d57` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x8481`, value `x8527`).

## P2 — support set (body)  [deterministic-derived]

**Domain (8):** `Real`, `Real.log`, `Or`, `Real.exp`, `le_or_gt`, `LE.le.trans`, `Real.exp_nonneg`, `Real.log_le_iff_le_exp`

**Classified infrastructure (14):** `LE.le` (structure-projection), `Real.instLE` (typeclass-instance), `Or.casesOn` (generated), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `LinearOrder.toPartialOrder` (structure-projection,typeclass-instance), `Real.linearOrder` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `LT.lt` (structure-projection), `Preorder.toLT` (structure-projection,typeclass-instance), `Real.instPreorder` (typeclass-instance), `Iff.mp` (logic-core,structure-projection)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `Real` (0 args)
- `LE.le` (4 args) : <sort>
  - `Real` (0 args)
  - `Real.instLE` (0 args)
  - `Real.log` (1 args) : Real
- `Or.casesOn` (6 args) : LE.le [Prop]
  - `LE.le` (4 args) : <sort>
    - `Real` (0 args)
    - `Preorder.toLE` (2 args) : LE
      - `Real` (0 args)
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `Real` (0 args)
        - `LinearOrder.toPartialOrder` (2 args) : PartialOrder
          - `Real` (0 args)
          - `Real.linearOrder` (0 args)
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `LT.lt` (4 args) : <sort>
    - `Real` (0 args)
    - `Preorder.toLT` (2 args) : LT
      - `Real` (0 args)
      - `PartialOrder.toPreorder` (2 args) : Preorder
        - `Real` (0 args)
        - `LinearOrder.toPartialOrder` (2 args) : PartialOrder
          - `Real` (0 args)
          - `Real.linearOrder` (0 args)
  ... (124 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `le_or_gt` (4 args) : Or (depth 1)
- `LE.le.trans` (7 args) : LE.le (depth 1)
- `Real.exp_nonneg` (1 args) : LE.le (depth 2)
- `Real.log_le_iff_le_exp` (3 args) : Iff (depth 2)

## P5 — source-level use events  [observed]

- `exact` → `LE.le.trans` — `exact hx.trans <| exp_nonneg y`
- `exact` → `Iff.mp` — `exact (log_le_iff_le_exp hx).mp h`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Real.log` — def, module `Basic`
- `Or` — inductive, module `Init.Prelude`
- `Real.exp` — def, module `Mathlib.Analysis.Complex.Exponential`
- `le_or_gt` — axiom, module `Mathlib.Order.Defs.LinearOrder`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
