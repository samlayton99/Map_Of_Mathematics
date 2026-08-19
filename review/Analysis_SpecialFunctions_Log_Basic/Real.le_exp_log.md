# Real.le_exp_log

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 4089 nodes

## Statement and source  [lean-exact]

```lean
theorem le_exp_log (x : ℝ) : x ≤ exp (log x) := by
  by_cases h_zero : x = 0
  · rw [h_zero, log, dif_pos rfl, exp_zero]
    exact zero_le_one
  · rw [exp_log_eq_abs h_zero]
    exact le_abs_self _
```

Exact proof reference: record decl `d56` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x8349`, value `x8475`).

## P2 — support set (body)  [deterministic-derived]

**Domain (19):** `Real`, `dite`, `Real.exp`, `Real.log`, `Eq`, `Not`, `OrderIso`, `Set.Elem`, `Set.Ioi`, `Set`, `OrderIso.symm`, `Real.expOrderIso`, `Subtype.mk`, `abs`, `dif_pos`, `Real.exp_zero`, `zero_le_one`, `Real.exp_log_eq_abs`, `le_abs_self`

**Classified infrastructure (23):** `LE.le` (structure-projection), `Real.instLE` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `Real.decidableEq` (typeclass-instance), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `DFunLike.coe` (structure-projection), `Real.instPreorder` (typeclass-instance), `Subtype.instLE` (typeclass-instance), `Membership.mem` (structure-projection), `Set.instMembership` (typeclass-instance), `instFunLikeOrderIso` (typeclass-instance), `Real.lattice` (typeclass-instance), `Real.instAddGroup` (typeclass-instance), `Real.log._proof_1` (internal-detail), `Real.log.eq_1` (internal-detail,generated), `rfl` (eq-machinery), `One.toOfNat1` (typeclass-instance), `Real.instOne` (typeclass-instance), `Real.instZeroLEOneClass` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `dite` (5 args) : LE.le [Prop]
  - `LE.le` (4 args) : <sort>
    - `Real` (0 args)
    - `Real.instLE` (0 args)
    - `Real.exp` (1 args) : Real
      - `Real.log` (1 args) : Real
  - `Eq` (3 args) : <sort>
    - `Real` (0 args)
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `Real.decidableEq` (2 args) : Decidable
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `Eq` (3 args) : <sort>
    - `Real` (0 args)
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `Eq.mpr` (4 args) : LE.le [Prop]
    - `LE.le` (4 args) : <sort>
      - `Real` (0 args)
  ... (1790 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `dite` (5 args) : LE.le (depth 0)
- `dif_pos` (6 args) : Eq (depth 6)
- `zero_le_one` (5 args) : LE.le (depth 5)
- `Real.exp_log_eq_abs` (2 args) : Eq (depth 4)
- `le_abs_self` (4 args) : LE.le (depth 2)

## P5 — source-level use events  [observed]

- `exact` → `zero_le_one` — `exact zero_le_one`
- `exact` → `le_abs_self` — `exact le_abs_self _`
- `refine` → `dite` — `refine  if h_zero  : x = 0 then  ?  pos  else  ?  neg`
- `rewrite` → `Real.exp_log_eq_abs` — `rewrite  [ exp_log_eq_abs h_zero ]`
- `rewrite` → `Real.log`, `Real.log.eq_1`, `dif_pos`, `Real.exp_zero` — `rewrite  [ h_zero, log, dif_pos rfl, exp_zero ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `dite` — def, module `Init.Prelude`
- `Real.exp` — def, module `Mathlib.Analysis.Complex.Exponential`
- `Real.log` — def, module `Basic`
- `Eq` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
