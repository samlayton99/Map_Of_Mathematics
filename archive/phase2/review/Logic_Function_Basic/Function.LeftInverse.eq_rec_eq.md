# Function.LeftInverse.eq_rec_eq

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 423 nodes

## Statement and source  [lean-exact]

```lean
theorem Function.LeftInverse.eq_rec_eq {γ : β → Sort v} {f : α → β} {g : β → α}
    (h : Function.LeftInverse g f) (C : ∀ a : α, γ (f a)) (a : α) :
    -- TODO: mathlib3 uses `(congr_arg f (h a)).rec (C (g (f a)))` for LHS
    @Eq.rec β (f (g (f a))) (fun x _ ↦ γ x) (C (g (f a))) (f a) (congr_arg f (h a)) = C a :=
  eq_of_heq <| (eqRec_heq _ _).trans <| by rw [h]
```

Exact proof reference: record decl `d81` in `studies/Logic_Function_Basic.study.json` (type `x5350`, value `x5421`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `Function.LeftInverse`, `eq_of_heq`, `Eq`, `HEq.trans`, `eqRec_heq`, `HEq`, `HEq.rfl`

**Classified infrastructure (6):** `Eq.rec` (eq-machinery,generated,recursor), `congr_arg` (eq-machinery), `Eq.recOn` (generated), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Function.LeftInverse` (4 args) : <sort>
- `eq_of_heq` (4 args) : Eq [Prop]
  - `Eq.rec` (6 args) : <local>
    - `Eq` (3 args) : <sort>
    - `congr_arg` (6 args) : Eq [Prop]
  - `HEq.trans` (8 args) : HEq [Prop]
    - `Eq.recOn` (6 args) : <local>
      - `Eq` (3 args) : <sort>
      - `congr_arg` (6 args) : Eq [Prop]
    - `eqRec_heq` (6 args) : HEq [Prop]
      - `congr_arg` (6 args) : Eq [Prop]
    - `Eq.mpr` (4 args) : HEq [Prop]
      - `HEq` (4 args) : <sort>
      - `HEq` (4 args) : <sort>
      - `id` (2 args) : Eq [Prop]
        - `Eq` (3 args) : <sort>
          - `HEq` (4 args) : <sort>
          - `HEq` (4 args) : <sort>
        - `congrArg` (6 args) : Eq [Prop]
          - `HEq` (4 args) : <sort>
      - `HEq.rfl` (2 args) : HEq [Prop]

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `eq_of_heq` (4 args) : Eq (depth 0)
- `HEq.trans` (8 args) : HEq (depth 1)
- `eqRec_heq` (6 args) : HEq (depth 2)
- `HEq.rfl` (2 args) : HEq (depth 3)

## P5 — source-level use events  [observed]

- `exact` → `HEq.rfl` — `exact  HEq.rfl`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Function.LeftInverse` — def, module `Init.Data.Function`
- `eq_of_heq` — axiom, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`
- `HEq.trans` — axiom, module `Init.Core`
- `eqRec_heq` — axiom, module `Init.Core`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
