# Real.log_lt_iff_lt_exp

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 447 nodes

## Statement and source  [lean-exact]

```lean
theorem log_lt_iff_lt_exp (hx : 0 < x) : log x < y ↔ x < exp y := by rw [← exp_lt_exp, exp_log hx]
```

Exact proof reference: record decl `d82` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x12872`, value `x12921`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `Real`, `Iff`, `Real.log`, `Real.exp`, `Eq`, `Real.exp_lt_exp`, `Real.exp_log`

**Classified infrastructure (11):** `LT.lt` (structure-projection), `Real.instLT` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.symm` (eq-machinery), `propext` (eq-machinery), `Iff.rfl` (logic-core)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `Real` (0 args)
- `LT.lt` (4 args) : <sort>
  - `Real` (0 args)
  - `Real.instLT` (0 args)
  - `OfNat.ofNat` (3 args) : Real
    - `Real` (0 args)
    - `Zero.toOfNat0` (2 args) : OfNat
      - `Real` (0 args)
      - `Real.instZero` (0 args)
- `Eq.mpr` (4 args) : Iff [Prop]
  - `Iff` (2 args) : <sort>
    - `LT.lt` (4 args) : <sort>
      - `Real` (0 args)
      - `Real.instLT` (0 args)
      - `Real.log` (1 args) : Real
    - `LT.lt` (4 args) : <sort>
      - `Real` (0 args)
      - `Real.instLT` (0 args)
      - `Real.exp` (1 args) : Real
  - `Iff` (2 args) : <sort>
    - `LT.lt` (4 args) : <sort>
      - `Real` (0 args)
      - `Real.instLT` (0 args)
      - `Real.exp` (1 args) : Real
        - `Real.log` (1 args) : Real
      - `Real.exp` (1 args) : Real
    - `LT.lt` (4 args) : <sort>
      - `Real` (0 args)
      - `Real.instLT` (0 args)
  ... (156 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Real.exp_lt_exp` (2 args) : Iff (depth 5)
- `Real.exp_log` (2 args) : Eq (depth 4)

## P5 — source-level use events  [observed]

- `rewrite` → `Real.exp_lt_exp`, `Real.exp_log` — `rewrite  [ ← exp_lt_exp, exp_log hx ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Iff` — inductive, module `Init.Core`
- `Real.log` — def, module `Basic`
- `Real.exp` — def, module `Mathlib.Analysis.Complex.Exponential`
- `Eq` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
