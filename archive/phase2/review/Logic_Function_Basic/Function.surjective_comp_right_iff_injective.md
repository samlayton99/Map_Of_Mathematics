# Function.surjective_comp_right_iff_injective

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* automation · *proof-term size:* 2037 nodes

## Statement and source  [lean-exact]

```lean
theorem surjective_comp_right_iff_injective {γ : Type*} [Nontrivial γ] :
    Surjective (fun g : β → γ ↦ g ∘ f) ↔ Injective f := by
  classical
  refine ⟨not_imp_not.mp fun not_inj surj ↦ not_subsingleton γ ⟨fun c c' ↦ ?_⟩,
    (·.surjective_comp_right)⟩
  simp only [Injective, not_forall] at not_inj
  have ⟨a₁, a₂, eq, ne⟩ := not_inj
  have ⟨f, hf⟩ := surj (if · = a₂ then c else c')
  have h₁ := congr_fun hf a₁
  have h₂ := congr_fun hf a₂
  simp only [comp_apply, if_neg ne, reduceIte] at h₁ h₂
  rw [← h₁, eq, h₂]
```

Exact proof reference: record decl `d228` in `studies/Logic_Function_Basic.study.json` (type `x13877`, value `x14316`).

## P2 — support set (body)  [deterministic-derived]

**Domain (19):** `Nontrivial`, `Function.Surjective`, `Function.comp`, `Function.Injective`, `Not`, `not_imp_not`, `not_subsingleton`, `Subsingleton.intro`, `Exists`, `Eq`, `ite`, `Classical.propDecidable`, `Decidable`, `if_neg`, `True`, `ite_congr`, `eq_self`, `ite_cond_eq_true`, `Function.Injective.surjective_comp_right`

**Classified infrastructure (16):** `Iff.intro` (logic-core,logic-core-ctor), `Iff.mp` (logic-core,structure-projection), `_private.Basic.0.Function.surjective_comp_right_iff_injective.match_1` (internal-detail,generated), `Eq.mp` (eq-machinery), `Eq.trans` (eq-machinery), `_private.Basic.0.Function.not_injective_iff._simp_2` (internal-detail), `congrArg` (eq-machinery), `funext` (eq-machinery), `_private.Basic.0.Function.surjective_comp_right_iff_injective.match_2` (internal-detail,generated), `congr_fun` (eq-machinery), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `Eq.symm` (eq-machinery), `instDecidableTrue` (typeclass-instance), `Eq.refl` (eq-machinery), `Nontrivial.to_nonempty` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nontrivial` (1 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `Function.Surjective` (3 args) : <sort>
    - `Function.comp` (5 args) : <pi>
  - `Function.Injective` (3 args) : <sort>
  - `Iff.mp` (4 args) : <pi> [Prop]
    - `Not` (1 args) : <sort>
      - `Function.Injective` (3 args) : <sort>
    - `Not` (1 args) : <sort>
      - `Function.Surjective` (3 args) : <sort>
        - `Function.comp` (5 args) : <pi>
    - `Function.Surjective` (3 args) : <sort>
      - `Function.comp` (5 args) : <pi>
    - `Function.Injective` (3 args) : <sort>
    - `not_imp_not` (2 args) : Iff [Prop]
      - `Function.Injective` (3 args) : <sort>
      - `Function.Surjective` (3 args) : <sort>
        - `Function.comp` (5 args) : <pi>
    - `Not` (1 args) : <sort>
      - `Function.Injective` (3 args) : <sort>
    - `Function.Surjective` (3 args) : <sort>
      - `Function.comp` (5 args) : <pi>
    - `not_subsingleton` (3 args) : False [Prop]
      - `Subsingleton.intro` (2 args) : Subsingleton [Prop]
        - `_private.Basic.0.Function.surjective_comp_right_iff_injective.match_1` (6 args) : Eq [Prop]
          - `Exists` (2 args) : <sort>
            - `Exists` (2 args) : <sort>
              - `Exists` (2 args) : <sort>
                - `Eq` (3 args) : <sort>
                - `Eq` (3 args) : <sort>
  ... (261 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `not_imp_not` (2 args) : Iff (depth 2)
- `not_subsingleton` (3 args) : False (depth 2)
- `Subsingleton.intro` (2 args) : Subsingleton (depth 3)
- `if_neg` (6 args) : Eq (depth 12)
- `ite_congr` (12 args) : Eq (depth 14)
- `eq_self` (2 args) : Eq (depth 15)
- `ite_cond_eq_true` (6 args) : Eq (depth 14)
- `Function.Injective.surjective_comp_right` (6 args) : Function.Surjective (depth 1)

## P5 — source-level use events  [observed]

- `rw` → (no named attribution) — `rw [← h₁, eq, h₂]`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  have h₁ := congr_fun hf a₁ ;  ?  _`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  have h₂ := congr_fun hf a₂ ;  ?  _`
- `refine` → `Iff.intro` — `refine ⟨not_imp_not.mp fun not_inj surj ↦ not_subsingleton γ ⟨fun c c' ↦ ?_⟩,
  `
- `refine` → `_private.Basic.0.Function.surjective_comp_right_iff_injective.match_1` — `refine  no_implicit_lambda%  have ⟨a₁, a₂, eq, ne⟩ := not_inj ;  ?  _`
- `simp` → `Function.Injective`, `Classical.not_forall`, `Function.Injective`, `Classical.not_forall` — `simp only [Injective, not_forall] at not_inj`
- `refine` → `_private.Basic.0.Function.surjective_comp_right_iff_injective.match_2` — `refine  no_implicit_lambda%  have ⟨f, hf⟩ := surj (if · = a₂ then c else c') ;  `
- `simp` → `Function.comp_apply`, `reduceIte`, `Function.comp_apply`, `if_neg`, `reduceIte` — `simp only [comp_apply, if_neg ne, reduceIte] at h₁ h₂`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nontrivial` — inductive, module `Mathlib.Logic.Nontrivial.Defs`
- `Function.Surjective` — def, module `Init.Data.Function`
- `Function.comp` — def, module `Init.Prelude`
- `Function.Injective` — def, module `Init.Data.Function`
- `Not` — def, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
