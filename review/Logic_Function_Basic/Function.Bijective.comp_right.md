# Function.Bijective.comp_right

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* automation · *proof-term size:* 659 nodes

## Statement and source  [lean-exact]

```lean
theorem Bijective.comp_right (hf : Bijective f) : Bijective fun g : β → γ ↦ g ∘ f :=
  ⟨hf.surjective.injective_comp_right, fun g ↦
    ⟨g ∘ surjInv hf.surjective,
     by simp only [comp_assoc g _ f, (leftInverse_surjInv hf).comp_eq_id, comp_id]⟩⟩
```

Exact proof reference: record decl `d3` in `studies/Logic_Function_Basic.study.json` (type `x118`, value `x296`).

## P2 — support set (body)  [deterministic-derived]

**Domain (15):** `Function.Bijective`, `Function.Injective`, `Function.comp`, `Function.Surjective`, `Function.Surjective.injective_comp_right`, `Function.Bijective.surjective`, `Eq`, `Function.surjInv`, `of_eq_true`, `True`, `congrFun'`, `Function.comp_assoc`, `Function.LeftInverse.comp_eq_id`, `Function.leftInverse_surjInv`, `eq_self`

**Classified infrastructure (6):** `And.intro` (logic-core,logic-core-ctor), `Exists.intro` (logic-core,logic-core-ctor), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery), `id` (eq-machinery), `And.right` (logic-core,structure-projection)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Function.Bijective` (3 args) : <sort>
- `And.intro` (4 args) : And [Prop]
  - `Function.Injective` (3 args) : <sort>
    - `Function.comp` (5 args) : <pi>
  - `Function.Surjective` (3 args) : <sort>
    - `Function.comp` (5 args) : <pi>
  - `Function.Surjective.injective_comp_right` (5 args) : Function.Injective [Prop]
    - `Function.Bijective.surjective` (4 args) : Function.Surjective [Prop]
  - `Exists.intro` (4 args) : Exists [Prop]
    - `Eq` (3 args) : <sort>
      - `Function.comp` (5 args) : <pi>
    - `Function.comp` (5 args) : <pi>
      - `Function.surjInv` (4 args) : <pi>
        - `Function.Bijective.surjective` (4 args) : Function.Surjective [Prop]
    - `of_eq_true` (2 args) : Eq [Prop]
      - `Eq` (3 args) : <sort>
        - `Function.comp` (5 args) : <pi>
        - `Function.comp` (5 args) : <pi>
          - `Function.surjInv` (4 args) : <pi>
            - `Function.Bijective.surjective` (4 args) : Function.Surjective [Prop]
      - `Eq.trans` (6 args) : Eq [Prop]
        - `Eq` (3 args) : <sort>
          - `Function.comp` (5 args) : <pi>
          - `Function.comp` (5 args) : <pi>
            - `Function.surjInv` (4 args) : <pi>
              - `Function.Bijective.surjective` (4 args) : Function.Surjective [Prop]
        - `Eq` (3 args) : <sort>
        - `True` (0 args)
        - `congrFun'` (6 args) : Eq [Prop]
          - `Eq` (2 args) : <pi>
  ... (68 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Function.Surjective.injective_comp_right` (5 args) : Function.Injective (depth 1)
- `Function.Bijective.surjective` (4 args) : Function.Surjective (depth 2)
- `Function.Bijective.surjective` (4 args) : Function.Surjective (depth 4)
- `of_eq_true` (2 args) : Eq (depth 2)
- `Function.Bijective.surjective` (4 args) : Function.Surjective (depth 6)
- `Function.Bijective.surjective` (4 args) : Function.Surjective (depth 7)
- `congrFun'` (6 args) : Eq (depth 4)
- `Function.Bijective.surjective` (4 args) : Function.Surjective (depth 8)
- `Function.Bijective.surjective` (4 args) : Function.Surjective (depth 10)
- `Function.comp_assoc` (7 args) : Eq (depth 7)
- `Function.LeftInverse.comp_eq_id` (5 args) : Eq (depth 8)
- `Function.leftInverse_surjInv` (4 args) : Function.LeftInverse (depth 9)
- `eq_self` (2 args) : Eq (depth 4)

## P5 — source-level use events  [observed]

- `simp` → `Function.comp_id`, `Function.comp_assoc`, `Function.LeftInverse.comp_eq_id`, `Function.comp_id` — `simp only [comp_assoc g _ f, (leftInverse_surjInv hf).comp_eq_id, comp_id]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Function.Bijective` — def, module `Mathlib.Logic.Function.Defs`
- `Function.Injective` — def, module `Init.Data.Function`
- `Function.comp` — def, module `Init.Prelude`
- `Function.Surjective` — def, module `Init.Data.Function`
- `Function.Surjective.injective_comp_right` — theorem, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
