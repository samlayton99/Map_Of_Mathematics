# Real.surjOn_log

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* term · *proof-term size:* 129 nodes

## Statement and source  [lean-exact]

```lean
theorem surjOn_log : SurjOn log (Ioi 0) univ := fun x _ => ⟨exp x, exp_pos x, log_exp x⟩
```

Exact proof reference: record decl `d127` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x18033`, value `x18052`).

## P2 — support set (body)  [deterministic-derived]

**Domain (10):** `Real`, `Set`, `Set.univ`, `And`, `Set.Ioi`, `Eq`, `Real.log`, `Real.exp`, `Real.exp_pos`, `Real.log_exp`

**Classified infrastructure (8):** `Membership.mem` (structure-projection), `Set.instMembership` (typeclass-instance), `Exists.intro` (logic-core,logic-core-ctor), `Real.instPreorder` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `And.intro` (logic-core,logic-core-ctor)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `Membership.mem` (5 args) : <sort>
  - `Real` (0 args)
  - `Set` (1 args) : <sort>
    - `Real` (0 args)
  - `Set.instMembership` (1 args) : Membership
    - `Real` (0 args)
  - `Set.univ` (1 args) : Set
    - `Real` (0 args)
- `Exists.intro` (4 args) : Exists [Prop]
  - `Real` (0 args)
  - `Real` (0 args)
  - `And` (2 args) : <sort>
    - `Membership.mem` (5 args) : <sort>
      - `Real` (0 args)
      - `Set` (1 args) : <sort>
        - `Real` (0 args)
      - `Set.instMembership` (1 args) : Membership
        - `Real` (0 args)
      - `Set.Ioi` (3 args) : Set
        - `Real` (0 args)
        - `Real.instPreorder` (0 args)
        - `OfNat.ofNat` (3 args) : Real
          - `Real` (0 args)
          - `Zero.toOfNat0` (2 args) : OfNat
            - `Real` (0 args)
            - `Real.instZero` (0 args)
    - `Eq` (3 args) : <sort>
      - `Real` (0 args)
      - `Real.log` (1 args) : Real
  ... (53 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Real.exp_pos` (1 args) : LT.lt (depth 2)
- `Real.log_exp` (1 args) : Eq (depth 2)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Set` — def, module `Mathlib.Data.Set.Defs`
- `Set.univ` — def, module `Mathlib.Data.Set.Defs`
- `And` — inductive, module `Init.Prelude`
- `Set.Ioi` — def, module `Mathlib.Order.Interval.Set.Defs`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
