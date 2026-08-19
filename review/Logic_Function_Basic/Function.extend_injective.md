# Function.extend_injective

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* automation · *proof-term size:* 456 nodes

## Statement and source  [lean-exact]

```lean
theorem extend_injective (hf : Injective f) (e' : β → γ) : Injective fun g ↦ extend f g e' := by
  intro g₁ g₂ hg
  refine funext fun x ↦ ?_
  have H := congr_fun hg (f x)
  simp only [hf.extend_apply] at H
  exact H
```

Exact proof reference: record decl `d148` in `studies/Logic_Function_Basic.study.json` (type `x9791`, value `x9893`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `Function.Injective`, `Eq`, `Function.extend`, `Function.Injective.extend_apply`

**Classified infrastructure (5):** `funext` (eq-machinery), `congr_fun` (eq-machinery), `Eq.mp` (eq-machinery), `congr` (eq-machinery), `congrArg` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Function.Injective` (3 args) : <sort>
- `Eq` (3 args) : <sort>
  - `Function.extend` (6 args) : <pi>
  - `Function.extend` (6 args) : <pi>
- `funext` (5 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `Function.extend` (6 args) : <pi>
    - `Function.extend` (6 args) : <pi>
  - `congr_fun` (6 args) : Eq [Prop]
    - `Function.extend` (6 args) : <pi>
    - `Function.extend` (6 args) : <pi>
  - `Eq.mp` (4 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `Function.extend` (6 args) : <pi>
      - `Function.extend` (6 args) : <pi>
    - `Eq` (3 args) : <sort>
    - `congr` (8 args) : Eq [Prop]
      - `Eq` (2 args) : <pi>
        - `Function.extend` (6 args) : <pi>
      - `Eq` (2 args) : <pi>
      - `Function.extend` (6 args) : <pi>
      - `congrArg` (6 args) : Eq [Prop]
        - `Function.extend` (6 args) : <pi>
        - `Eq` (1 args) : <pi>
        - `Function.Injective.extend_apply` (5 args) : <pi> [Prop]
      - `Function.Injective.extend_apply` (5 args) : <pi> [Prop]

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Function.Injective.extend_apply` (5 args) : <pi> (depth 4)
- `Function.Injective.extend_apply` (5 args) : <pi> (depth 3)

## P5 — source-level use events  [observed]

- `refine` → `funext` — `refine funext fun x ↦ ?_`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  have H := congr_fun hg (f x) ;  ?  _`
- `simp` → `Function.Injective.extend_apply` — `simp only [hf.extend_apply] at H`
- `exact` → (no named attribution) — `exact H`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Function.Injective` — def, module `Init.Data.Function`
- `Eq` — inductive, module `Init.Prelude`
- `Function.extend` — def, module `Basic`
- `Function.Injective.extend_apply` — theorem, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
