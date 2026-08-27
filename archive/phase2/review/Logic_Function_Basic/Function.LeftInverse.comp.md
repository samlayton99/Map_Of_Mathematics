# Function.LeftInverse.comp

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 242 nodes

## Statement and source  [lean-exact]

```lean
theorem LeftInverse.comp {f : α → β} {g : β → α} {h : β → γ} {i : γ → β} (hf : LeftInverse f g)
    (hh : LeftInverse h i) : LeftInverse (h ∘ f) (g ∘ i) :=
  fun a ↦ show h (f (g (i a))) = a by rw [hf (i a), hh a]
```

Exact proof reference: record decl `d78` in `studies/Logic_Function_Basic.study.json` (type `x5212`, value `x5269`).

## P2 — support set (body)  [deterministic-derived]

**Domain (2):** `Function.LeftInverse`, `Eq`

**Classified infrastructure (4):** `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.refl` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Function.LeftInverse` (4 args) : <sort>
- `Function.LeftInverse` (4 args) : <sort>
- `Eq` (3 args) : <sort>
- `Eq.mpr` (4 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
  - `Eq` (3 args) : <sort>
  - `id` (2 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
    - `congrArg` (6 args) : Eq [Prop]
      - `Eq` (3 args) : <sort>
  - `Eq.mpr` (4 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
    - `Eq` (3 args) : <sort>
    - `id` (2 args) : Eq [Prop]
      - `Eq` (3 args) : <sort>
        - `Eq` (3 args) : <sort>
        - `Eq` (3 args) : <sort>
      - `congrArg` (6 args) : Eq [Prop]
        - `Eq` (3 args) : <sort>
    - `Eq.refl` (2 args) : Eq [Prop]

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

(none)

## P5 — source-level use events  [observed]

- `rw` → (no named attribution) — `rw [hf (i a), hh a]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Function.LeftInverse` — def, module `Init.Data.Function`
- `Eq` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
