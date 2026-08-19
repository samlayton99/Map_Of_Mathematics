# Nat.coprime_add_iff_left

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* automation · *proof-term size:* 439 nodes

## Statement and source  [lean-exact]

```lean
lemma coprime_add_iff_left (h : a ∣ c) : Coprime a (b + c) ↔ Coprime a b := by
  obtain ⟨n, rfl⟩ := h; simp
```

Exact proof reference: record decl `d15` in `studies/Data_Nat_GCD_Basic.study.json` (type `x1338`, value `x1397`).

## P2 — support set (body)  [deterministic-derived]

**Domain (8):** `Nat`, `Eq`, `Iff`, `Nat.Coprime`, `of_eq_true`, `True`, `congrFun'`, `iff_self`

**Classified infrastructure (14):** `Dvd.dvd` (structure-projection), `Nat.instDvd` (typeclass-instance), `Exists.casesOn` (generated), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `instMulNat` (typeclass-instance), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `instAddNat` (typeclass-instance), `Eq.ndrec` (eq-machinery,generated), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery), `Nat.coprime_add_mul_left_right._simp_1` (internal-detail), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `Nat` (0 args)
- `Dvd.dvd` (4 args) : <sort>
  - `Nat` (0 args)
  - `Nat.instDvd` (0 args)
- `Exists.casesOn` (5 args) : Iff [Prop]
  - `Nat` (0 args)
  - `Nat` (0 args)
  - `Eq` (3 args) : <sort>
    - `Nat` (0 args)
    - `HMul.hMul` (6 args) : Nat
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `instHMul` (2 args) : HMul
        - `Nat` (0 args)
        - `instMulNat` (0 args)
  - `Dvd.dvd` (4 args) : <sort>
    - `Nat` (0 args)
    - `Nat.instDvd` (0 args)
  - `Iff` (2 args) : <sort>
    - `Nat.Coprime` (2 args) : <sort>
      - `HAdd.hAdd` (6 args) : Nat
        - `Nat` (0 args)
        - `Nat` (0 args)
        - `Nat` (0 args)
        - `instHAdd` (2 args) : HAdd
          - `Nat` (0 args)
          - `instAddNat` (0 args)
  ... (151 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `of_eq_true` (2 args) : Iff (depth 2)
- `congrFun'` (6 args) : Eq (depth 4)
- `iff_self` (1 args) : Eq (depth 4)

## P5 — source-level use events  [observed]

- `simp` → (no named attribution) — `simp`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`
- `Iff` — inductive, module `Init.Core`
- `Nat.Coprime` — def, module `Init.Data.Nat.Coprime`
- `of_eq_true` — axiom, module `Init.SimpLemmas`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
