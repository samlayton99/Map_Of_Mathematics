# Function.Bijective.existsUnique_iff

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* term · *proof-term size:* 687 nodes

## Statement and source  [lean-exact]

```lean
theorem Bijective.existsUnique_iff {f : α → β} (hf : Bijective f) {p : β → Prop} :
    (∃! y, p y) ↔ ∃! x, p (f x) :=
  ⟨fun ⟨y, hpy, hy⟩ ↦
    let ⟨x, hx⟩ := hf.surjective y
    ⟨x, by simpa [hx], fun z (hz : p (f z)) ↦ hf.injective <| hx.symm ▸ hy _ hz⟩,
    fun ⟨x, hpx, hx⟩ ↦
    ⟨f x, hpx, fun y hy ↦
      let ⟨z, hz⟩ := hf.surjective y
      hz ▸ congr_arg f (hx _ (by simpa [hz]))⟩⟩
```

Exact proof reference: record decl `d5` in `studies/Logic_Function_Basic.study.json` (type `x356`, value `x639`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `Function.Bijective`, `ExistsUnique`, `Eq`, `Exists`, `Function.Bijective.surjective`, `And`, `Function.Bijective.injective`

**Classified infrastructure (12):** `Iff.intro` (logic-core,logic-core-ctor), `_private.Basic.0.Function.Bijective.existsUnique_iff.match_1` (internal-detail,generated), `_private.Basic.0.Function.Surjective.forall.match_1` (internal-detail,generated), `Exists.intro` (logic-core,logic-core-ctor), `And.intro` (logic-core,logic-core-ctor), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.rec` (eq-machinery,generated,recursor), `Eq.symm` (eq-machinery), `_private.Basic.0.Function.Bijective.existsUnique_iff.match_2` (internal-detail,generated), `congr_arg` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Function.Bijective` (3 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `ExistsUnique` (2 args) : <sort>
  - `ExistsUnique` (2 args) : <sort>
  - `ExistsUnique` (2 args) : <sort>
  - `_private.Basic.0.Function.Bijective.existsUnique_iff.match_1` (5 args) : ExistsUnique [Prop]
    - `ExistsUnique` (2 args) : <sort>
    - `ExistsUnique` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
    - `_private.Basic.0.Function.Surjective.forall.match_1` (7 args) : ExistsUnique [Prop]
      - `Exists` (2 args) : <sort>
        - `Eq` (3 args) : <sort>
      - `ExistsUnique` (2 args) : <sort>
      - `Function.Bijective.surjective` (5 args) : Exists [Prop]
      - `Eq` (3 args) : <sort>
      - `Exists.intro` (4 args) : Exists [Prop]
        - `And` (2 args) : <sort>
          - `Eq` (3 args) : <sort>
        - `And.intro` (4 args) : And [Prop]
          - `Eq` (3 args) : <sort>
          - `Eq.mpr` (4 args) : <lam> [Prop]
            - `id` (2 args) : Eq [Prop]
              - `Eq` (3 args) : <sort>
              - `congrArg` (6 args) : Eq [Prop]
          - `Function.Bijective.injective` (7 args) : Eq [Prop]
            - `Eq.rec` (6 args) : Eq [Prop]
              - `Eq` (3 args) : <sort>
              - `Eq` (3 args) : <sort>
              - `Eq.symm` (4 args) : Eq [Prop]
  - `ExistsUnique` (2 args) : <sort>
  ... (53 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Function.Bijective.surjective` (5 args) : Exists (depth 3)
- `Function.Bijective.injective` (7 args) : Eq (depth 5)
- `Function.Bijective.surjective` (5 args) : Exists (depth 5)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Function.Bijective` — def, module `Mathlib.Logic.Function.Defs`
- `ExistsUnique` — def, module `Mathlib.Logic.ExistsUnique`
- `Eq` — inductive, module `Init.Prelude`
- `Exists` — inductive, module `Init.Core`
- `Function.Bijective.surjective` — theorem, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
