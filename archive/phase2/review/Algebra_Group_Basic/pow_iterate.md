# pow_iterate

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* automation · *proof-term size:* 117 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive, simp]
lemma pow_iterate (k : ℕ) : ∀ n : ℕ, (fun x : M ↦ x ^ k)^[n] = (· ^ k ^ n)
  | 0 => by ext; simp
  | n + 1 => by ext; simp [pow_iterate, Nat.pow_succ', pow_mul]
```

Exact proof reference: record decl `d413` in `studies/Algebra_Group_Basic.study.json` (type `x31930`, value `x31951`).

## P2 — support set (body)  [deterministic-derived]

**Domain (4):** `Monoid`, `Nat`, `Eq`, `Nat.iterate`

**Classified infrastructure (8):** `Nat.brecOn` (generated), `HPow.hPow` (structure-projection), `instHPow` (typeclass-instance), `NPow.toPow` (typeclass-instance), `Monoid.toNPow` (structure-projection,typeclass-instance), `instPowNat` (typeclass-instance), `instNatPowNat` (typeclass-instance), `pow_iterate._f` (internal-detail)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Monoid` (1 args) : <sort>
- `Nat` (0 args)
- `Nat` (0 args)
- `Nat.brecOn` (3 args) : Eq [Prop]
  - `Nat` (0 args)
  - `Eq` (3 args) : <sort>
    - `Nat.iterate` (3 args) : <pi>
      - `HPow.hPow` (6 args) : <local>
        - `Nat` (0 args)
        - `instHPow` (3 args) : HPow
          - `Nat` (0 args)
          - `NPow.toPow` (2 args) : Pow
            - `Monoid.toNPow` (2 args) : NPow
    - `HPow.hPow` (6 args) : <local>
      - `Nat` (0 args)
      - `instHPow` (3 args) : HPow
        - `Nat` (0 args)
        - `NPow.toPow` (2 args) : Pow
          - `Monoid.toNPow` (2 args) : NPow
      - `HPow.hPow` (6 args) : Nat
        - `Nat` (0 args)
        - `Nat` (0 args)
        - `Nat` (0 args)
        - `instHPow` (3 args) : HPow
          - `Nat` (0 args)
          - `Nat` (0 args)
          - `instPowNat` (2 args) : Pow
            - `Nat` (0 args)
            - `instNatPowNat` (0 args)
  - `pow_iterate._f` (3 args) : <pi> [Prop]
  ... (30 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

(none)

## P5 — source-level use events  [observed]

- `simp` → (no named attribution) — `simp`
- `simp` → `Nat.pow_succ'`, `pow_mul`, `Nat.pow_succ'`, `pow_mul` — `simp [pow_iterate, Nat.pow_succ', pow_mul]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Monoid` — inductive, module `Mathlib.Algebra.Group.Defs`
- `Nat` — inductive, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`
- `Nat.iterate` — def, module `Mathlib.Logic.Function.Iterate`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
