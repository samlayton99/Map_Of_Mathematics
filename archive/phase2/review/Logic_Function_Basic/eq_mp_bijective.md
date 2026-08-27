# eq_mp_bijective

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* induction · *proof-term size:* 407 nodes

## Statement and source  [lean-exact]

```lean
theorem eq_mp_bijective {α β : Sort _} (h : α = β) : Function.Bijective (Eq.mp h) := by
  -- TODO: mathlib3 uses `eq_rec_on_bijective`, difference in elaboration here
  -- due to `@[macro_inline]` possibly?
  cases h
  exact ⟨fun _ _ ↦ id, fun x ↦ ⟨x, rfl⟩⟩
```

Exact proof reference: record decl `d338` in `studies/Logic_Function_Basic.study.json` (type `x27537`, value `x27605`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `Eq`, `HEq`, `Function.Bijective`, `Function.Injective`, `Function.Surjective`, `eq_of_heq`, `HEq.refl`

**Classified infrastructure (9):** `Eq.casesOn` (generated), `Eq.mp` (eq-machinery), `Eq.ndrec` (eq-machinery,generated), `Eq.refl` (eq-machinery), `And.intro` (logic-core,logic-core-ctor), `id` (eq-machinery), `Exists.intro` (logic-core,logic-core-ctor), `rfl` (eq-machinery), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Eq` (3 args) : <sort>
- `Eq.casesOn` (8 args) : Function.Bijective [Prop]
  - `Eq` (3 args) : <sort>
  - `Eq` (3 args) : <sort>
  - `HEq` (4 args) : <sort>
    - `Eq` (3 args) : <sort>
    - `Eq` (3 args) : <sort>
  - `Function.Bijective` (3 args) : <sort>
    - `Eq.mp` (3 args) : <pi>
  - `Eq` (3 args) : <sort>
  - `Eq.ndrec` (7 args) : <pi> [Prop]
    - `Eq` (3 args) : <sort>
    - `HEq` (4 args) : <sort>
      - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
      - `Eq.refl` (2 args) : Eq [Prop]
    - `Function.Bijective` (3 args) : <sort>
      - `Eq.mp` (3 args) : <pi>
    - `Eq` (3 args) : <sort>
    - `HEq` (4 args) : <sort>
      - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
      - `Eq.refl` (2 args) : Eq [Prop]
    - `Eq.ndrec` (6 args) : Function.Bijective [Prop]
      - `Eq` (3 args) : <sort>
      - `Eq.refl` (2 args) : Eq [Prop]
      - `Eq` (3 args) : <sort>
      - `Function.Bijective` (3 args) : <sort>
        - `Eq.mp` (3 args) : <pi>
      - `And.intro` (4 args) : And [Prop]
  ... (59 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `eq_of_heq` (4 args) : Eq (depth 4)
- `HEq.refl` (2 args) : HEq (depth 1)

## P5 — source-level use events  [observed]

- `exact` → `And.intro` — `exact ⟨fun _ _ ↦ id, fun x ↦ ⟨x, rfl⟩⟩`
- `cases` → (no named attribution) — `cases h`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Eq` — inductive, module `Init.Prelude`
- `HEq` — inductive, module `Init.Prelude`
- `Function.Bijective` — def, module `Mathlib.Logic.Function.Defs`
- `Function.Injective` — def, module `Init.Data.Function`
- `Function.Surjective` — def, module `Init.Data.Function`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
