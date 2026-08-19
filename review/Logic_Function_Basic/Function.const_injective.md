# Function.const_injective

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* term · *proof-term size:* 81 nodes

## Statement and source  [lean-exact]

```lean
theorem const_injective [Nonempty α] : Injective (const α : β → α → β) := fun _ _ h ↦
  let ⟨x⟩ := ‹Nonempty α›
  congr_fun h x
```

Exact proof reference: record decl `d129` in `studies/Logic_Function_Basic.study.json` (type `x7840`, value `x7865`).

## P2 — support set (body)  [deterministic-derived]

**Domain (3):** `Nonempty`, `Eq`, `Function.const`

**Classified infrastructure (2):** `_private.Basic.0.Function.const_injective.match_1` (internal-detail,generated), `congr_fun` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nonempty` (1 args) : <sort>
- `Eq` (3 args) : <sort>
  - `Function.const` (3 args) : <pi>
  - `Function.const` (3 args) : <pi>
- `_private.Basic.0.Function.const_injective.match_1` (4 args) : Eq [Prop]
  - `Nonempty` (1 args) : <sort>
  - `Eq` (3 args) : <sort>
  - `congr_fun` (6 args) : Eq [Prop]
    - `Function.const` (3 args) : <pi>
    - `Function.const` (3 args) : <pi>

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

(none)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nonempty` — inductive, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`
- `Function.const` — def, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
