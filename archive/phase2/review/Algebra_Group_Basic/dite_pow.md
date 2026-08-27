# dite_pow

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 1669 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive (attr := simp, to_additive) smul_dite]
lemma dite_pow (p : Prop) [Decidable p] (a : p → α) (b : ¬ p → α) (c : β) :
    (if h : p then a h else b h) ^ c = if h : p then a h ^ c else b h ^ c := by split_ifs <;> rfl
```

Exact proof reference: record decl `d121` in `studies/Algebra_Group_Basic.study.json` (type `x9622`, value `x9748`).

## P2 — support set (body)  [deterministic-derived]

**Domain (8):** `Pow`, `Decidable`, `Not`, `dite`, `Eq`, `congrFun'`, `dif_pos`, `dif_neg`

**Classified infrastructure (7):** `HPow.hPow` (structure-projection), `instHPow` (typeclass-instance), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congr` (eq-machinery), `congrArg` (eq-machinery), `Eq.refl` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Pow` (2 args) : <sort>
- `Decidable` (1 args) : <sort>
- `Not` (1 args) : <sort>
- `dite` (5 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `HPow.hPow` (6 args) : <local>
      - `instHPow` (3 args) : HPow
      - `dite` (5 args) : <local>
        - `Not` (1 args) : <sort>
    - `dite` (5 args) : <local>
      - `HPow.hPow` (6 args) : <local>
        - `instHPow` (3 args) : HPow
      - `Not` (1 args) : <sort>
      - `HPow.hPow` (6 args) : <local>
        - `instHPow` (3 args) : HPow
  - `Eq.mpr` (4 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `HPow.hPow` (6 args) : <local>
        - `instHPow` (3 args) : HPow
        - `dite` (5 args) : <local>
          - `Not` (1 args) : <sort>
      - `dite` (5 args) : <local>
        - `HPow.hPow` (6 args) : <local>
          - `instHPow` (3 args) : HPow
        - `Not` (1 args) : <sort>
        - `HPow.hPow` (6 args) : <local>
          - `instHPow` (3 args) : HPow
    - `Eq` (3 args) : <sort>
      - `HPow.hPow` (6 args) : <local>
        - `instHPow` (3 args) : HPow
  ... (182 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `dite` (5 args) : Eq (depth 0)
- `congrFun'` (6 args) : Eq (depth 5)
- `dif_pos` (6 args) : Eq (depth 7)
- `dif_pos` (6 args) : Eq (depth 4)
- `dif_neg` (6 args) : Eq (depth 7)
- `dif_neg` (6 args) : Eq (depth 4)

## P5 — source-level use events  [observed]

- `refine` → `dite` — `refine  if  h._@.Basic.166684508._hygCtx._hyg.85  :  ?  m  then  ?  pos  else  ?`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Pow` — inductive, module `Init.Prelude`
- `Decidable` — inductive, module `Init.Prelude`
- `Not` — def, module `Init.Prelude`
- `dite` — def, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
