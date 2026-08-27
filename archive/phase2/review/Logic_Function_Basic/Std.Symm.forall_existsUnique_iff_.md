# Std.Symm.forall_existsUnique_iff'

*file:* `Mathlib/Logic/Function/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 841 nodes

## Statement and source  [lean-exact]

```lean
/-- A symmetric relation `r : α → α → Prop` is "function-like"
(for each `a` there exists a unique `b` such that `r a b`)
if and only if it is `(f · = ·)` for some involutive function `f`. -/
protected lemma Std.Symm.forall_existsUnique_iff' {r : α → α → Prop} [Std.Symm r] :
    (∀ a, ∃! b, r a b) ↔ ∃ f : α → α, Involutive f ∧ r = (f · = ·) := by
  refine ⟨fun h ↦ ?_, fun ⟨f, _, hf⟩ ↦ forall_existsUnique_iff'.2 ⟨f, hf⟩⟩
  rcases forall_existsUnique_iff'.1 h with ⟨f, rfl : r = _⟩
  exact ⟨f, symm_apply_eq_iff.1 ‹_›, rfl⟩
```

Exact proof reference: record decl `d280` in `studies/Logic_Function_Basic.study.json` (type `x17685`, value `x17894`).

## P2 — support set (body)  [deterministic-derived]

**Domain (8):** `Std.Symm`, `ExistsUnique`, `Exists`, `And`, `Function.Involutive`, `Eq`, `forall_existsUnique_iff'`, `Function.symm_apply_eq_iff`

**Classified infrastructure (10):** `Iff.intro` (logic-core,logic-core-ctor), `Exists.casesOn` (generated), `Iff.mp` (logic-core,structure-projection), `Eq.ndrec` (eq-machinery,generated), `Exists.intro` (logic-core,logic-core-ctor), `And.intro` (logic-core,logic-core-ctor), `rfl` (eq-machinery), `Eq.symm` (eq-machinery), `_private.Basic.0.Std.Symm.forall_existsUnique_iff'.match_1` (internal-detail,generated), `Iff.mpr` (logic-core,structure-projection)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Std.Symm` (2 args) : <sort>
- `Iff.intro` (4 args) : Iff [Prop]
  - `ExistsUnique` (2 args) : <sort>
  - `Exists` (2 args) : <sort>
    - `And` (2 args) : <sort>
      - `Function.Involutive` (2 args) : <sort>
      - `Eq` (3 args) : <sort>
        - `Eq` (3 args) : <sort>
  - `ExistsUnique` (2 args) : <sort>
  - `Exists.casesOn` (5 args) : Exists [Prop]
    - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
    - `Exists` (2 args) : <sort>
      - `Eq` (3 args) : <sort>
        - `Eq` (3 args) : <sort>
    - `Exists` (2 args) : <sort>
      - `And` (2 args) : <sort>
        - `Function.Involutive` (2 args) : <sort>
        - `Eq` (3 args) : <sort>
          - `Eq` (3 args) : <sort>
    - `Iff.mp` (4 args) : Exists [Prop]
      - `ExistsUnique` (2 args) : <sort>
      - `Exists` (2 args) : <sort>
        - `Eq` (3 args) : <sort>
          - `Eq` (3 args) : <sort>
      - `forall_existsUnique_iff'` (3 args) : Iff [Prop]
    - `Eq` (3 args) : <sort>
      - `Eq` (3 args) : <sort>
    - `Eq.ndrec` (8 args) : Exists [Prop]
      - `Eq` (3 args) : <sort>
  ... (85 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `forall_existsUnique_iff'` (3 args) : Iff (depth 3)
- `Function.symm_apply_eq_iff` (2 args) : Iff (depth 6)

## P5 — source-level use events  [observed]

- `exact` → `Exists.intro` — `exact ⟨f, symm_apply_eq_iff.1 ‹_›, rfl⟩`
- `refine` → `Iff.intro` — `refine ⟨fun h ↦ ?_, fun ⟨f, _, hf⟩ ↦ forall_existsUnique_iff'.2 ⟨f, hf⟩⟩`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Std.Symm` — inductive, module `Init.Core`
- `ExistsUnique` — def, module `Mathlib.Logic.ExistsUnique`
- `Exists` — inductive, module `Init.Core`
- `And` — inductive, module `Init.Prelude`
- `Function.Involutive` — def, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
