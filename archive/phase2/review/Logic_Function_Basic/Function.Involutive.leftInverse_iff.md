# Function.Involutive.leftInverse_iff

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 505 nodes

## Statement and source  [lean-exact]

```lean
theorem leftInverse_iff {g : α → α} :
    g.LeftInverse f ↔ g = f :=
  ⟨fun hg ↦ funext fun x ↦ by rw [← h x, hg, h], fun he ↦ he ▸ h.leftInverse⟩
```

Exact proof reference: record decl `d68` in `studies/Logic_Function_Basic.study.json` (type `x4532`, value `x4647`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `Function.Involutive`, `Function.LeftInverse`, `Eq`, `Function.Involutive.leftInverse`

**Classified infrastructure (8):** `Iff.intro` (logic-core,logic-core-ctor), `funext` (eq-machinery), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.symm` (eq-machinery), `Eq.refl` (eq-machinery), `Eq.rec` (eq-machinery,generated,recursor)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Function.Involutive` (2 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `Function.LeftInverse` (4 args) : <sort>
  - `Eq` (3 args) : <sort>
  - `Function.LeftInverse` (4 args) : <sort>
  - `funext` (5 args) : Eq [Prop]
    - `Eq.mpr` (4 args) : Eq [Prop]
      - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
      - `id` (2 args) : Eq [Prop]
        - `Eq` (3 args) : <sort>
          - `Eq` (3 args) : <sort>
          - `Eq` (3 args) : <sort>
        - `congrArg` (6 args) : Eq [Prop]
          - `Eq` (3 args) : <sort>
          - `Eq.symm` (4 args) : Eq [Prop]
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
  ... (44 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Function.Involutive.leftInverse` (3 args) : Function.LeftInverse (depth 3)

## P5 — source-level use events  [observed]

- `rw` → (no named attribution) — `rw [← h x, hg, h]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Function.Involutive` — def, module `Basic`
- `Function.LeftInverse` — def, module `Init.Data.Function`
- `Eq` — inductive, module `Init.Prelude`
- `Function.Involutive.leftInverse` — theorem, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
