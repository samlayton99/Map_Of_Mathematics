# Function.Injective.isPartialInv

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 2259 nodes

## Statement and source  [lean-exact]

```lean
theorem Injective.isPartialInv {α β} {f : α → β} (I : Injective f) : IsPartialInv f (partialInv f)
  | a, b =>
  ⟨fun h =>
    open scoped Classical in
    have hpi : partialInv f b = if h : ∃ a, f a = b then some (Classical.choose h) else none :=
      rfl
    if h' : ∃ a, f a = b
    then by rw [hpi, dif_pos h'] at h
            injection h with h
            subst h
            apply Classical.choose_spec h'
    else by rw [hpi, dif_neg h'] at h; contradiction,
  fun e => e ▸ have h : ∃ a', f a' = f a := ⟨_, rfl⟩
              (dif_pos h).trans (congr_arg _ (I <| Classical.choose_spec h))⟩
```

Exact proof reference: record decl `d40` in `studies/Logic_Function_Basic.study.json` (type `x2971`, value `x3281`).

## P2 — support set (body)  [deterministic-derived]

**Domain (19):** `Function.Injective`, `Iff`, `Eq`, `Option`, `Function.partialInv`, `Option.some`, `dite`, `Exists`, `Classical.propDecidable`, `Classical.choose`, `Not`, `Option.none`, `dif_pos`, `HEq`, `Classical.choose_spec`, `eq_of_heq`, `noConfusion_of_Nat`, `Option.ctorIdx`, `dif_neg`

**Classified infrastructure (12):** `_private.Basic.0.Function.Injective.isPartialInv.match_1` (internal-detail,generated), `Iff.intro` (logic-core,logic-core-ctor), `rfl` (eq-machinery), `Option.some.noConfusion` (generated), `Eq.mp` (eq-machinery), `congrArg` (eq-machinery), `Eq.ndrec` (eq-machinery,generated), `False.elim` (logic-core), `Eq.rec` (eq-machinery,generated,recursor), `Exists.intro` (logic-core,logic-core-ctor), `Eq.trans` (eq-machinery), `congr_arg` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Function.Injective` (3 args) : <sort>
- `_private.Basic.0.Function.Injective.isPartialInv.match_1` (6 args) : Iff [Prop]
  - `Iff` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Option` (1 args) : <sort>
      - `Function.partialInv` (4 args) : Option
      - `Option.some` (2 args) : Option
    - `Eq` (3 args) : <sort>
  - `Iff.intro` (4 args) : Iff [Prop]
    - `Eq` (3 args) : <sort>
      - `Option` (1 args) : <sort>
      - `Function.partialInv` (4 args) : Option
      - `Option.some` (2 args) : Option
    - `Eq` (3 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `Option` (1 args) : <sort>
      - `Function.partialInv` (4 args) : Option
      - `Option.some` (2 args) : Option
    - `Eq` (3 args) : <sort>
      - `Option` (1 args) : <sort>
      - `Function.partialInv` (4 args) : Option
      - `dite` (5 args) : Option
        - `Option` (1 args) : <sort>
        - `Exists` (2 args) : <sort>
          - `Eq` (3 args) : <sort>
        - `Classical.propDecidable` (1 args) : Decidable
          - `Exists` (2 args) : <sort>
            - `Eq` (3 args) : <sort>
        - `Exists` (2 args) : <sort>
          - `Eq` (3 args) : <sort>
  ... (358 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `dite` (5 args) : Eq (depth 2)
- `dif_pos` (6 args) : Eq (depth 6)
- `Classical.choose_spec` (3 args) : Eq (depth 5)
- `eq_of_heq` (4 args) : Eq (depth 5)
- `noConfusion_of_Nat` (5 args) : Bool.rec (depth 4)
- `dif_neg` (6 args) : Eq (depth 7)
- `dif_pos` (6 args) : Eq (depth 4)

## P5 — source-level use events  [observed]

- `rewrite` → `dif_pos` — `rewrite  [ hpi, dif_pos h' ] at h`
- `rewrite` → `dif_neg` — `rewrite  [ hpi, dif_neg h' ] at h`
- `apply` → `Classical.choose_spec` — `apply Classical.choose_spec h'`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Function.Injective` — def, module `Init.Data.Function`
- `Iff` — inductive, module `Init.Core`
- `Eq` — inductive, module `Init.Prelude`
- `Option` — inductive, module `Init.Prelude`
- `Function.partialInv` — def, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
