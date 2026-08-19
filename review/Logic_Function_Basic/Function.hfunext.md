# Function.hfunext

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 429 nodes

## Statement and source  [lean-exact]

```lean
lemma hfunext {α α' : Sort u} {β : α → Sort v} {β' : α' → Sort v} {f : ∀ a, β a} {f' : ∀ a, β' a}
    (hα : α = α') (h : ∀ a a', a ≍ a' → f a ≍ f' a') : f ≍ f' := by
  subst hα
  have : ∀ a, f a ≍ f' a := fun a ↦ h a a (HEq.refl a)
  have : β = β' := by funext a; exact type_eq_of_heq (this a)
  subst this
  grind
```

Exact proof reference: record decl `d155` in `studies/Logic_Function_Basic.study.json` (type `x10543`, value `x10702`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `Eq`, `HEq`, `HEq.refl`, `type_eq_of_heq`

**Classified infrastructure (3):** `Eq.ndrec` (eq-machinery,generated), `funext` (eq-machinery), `_private.Basic.0.Function.hfunext._proof_1` (internal-detail)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Eq` (3 args) : <sort>
- `HEq` (4 args) : <sort>
- `HEq` (4 args) : <sort>
- `Eq.ndrec` (9 args) : HEq [Prop]
  - `HEq` (4 args) : <sort>
  - `HEq` (4 args) : <sort>
  - `HEq` (4 args) : <sort>
  - `HEq` (4 args) : <sort>
  - `HEq` (4 args) : <sort>
  - `HEq` (4 args) : <sort>
  - `HEq.refl` (2 args) : HEq [Prop]
  - `Eq` (3 args) : <sort>
  - `funext` (5 args) : Eq [Prop]
    - `type_eq_of_heq` (5 args) : Eq [Prop]
  - `Eq.ndrec` (9 args) : HEq [Prop]
    - `HEq` (4 args) : <sort>
    - `HEq` (4 args) : <sort>
    - `HEq` (4 args) : <sort>
    - `HEq` (4 args) : <sort>
    - `HEq` (4 args) : <sort>
    - `HEq` (4 args) : <sort>
    - `HEq` (4 args) : <sort>
    - `_private.Basic.0.Function.hfunext._proof_1` (5 args) : <mdata> [Prop]

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `HEq.refl` (2 args) : HEq (depth 1)
- `type_eq_of_heq` (5 args) : Eq (depth 2)

## P5 — source-level use events  [observed]

- `apply` → `funext` — `apply  funext`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  have : ∀ a, f a ≍ f' a := fun a ↦ h a a (HEq.refl a`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  (    have  : β = β'  :=  ?  body  ;  ?  _  )`
- `exact` → `type_eq_of_heq` — `exact type_eq_of_heq (this a)`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Eq` — inductive, module `Init.Prelude`
- `HEq` — inductive, module `Init.Prelude`
- `HEq.refl` — constructor, module `Init.Prelude`
- `type_eq_of_heq` — axiom, module `Init.Core`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
