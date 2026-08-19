# Real.log_finprod

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* automation · *proof-term size:* 9711 nodes

## Statement and source  [lean-exact]

```lean
lemma log_finprod {α : Type*} {f : α → ℝ} (h : ∀ a, 0 < f a) :
    log (∏ᶠ a, f a) = ∑ᶠ a, log (f a) := by
  classical
  have H : (fun i ↦ log (f i)).support = f.mulSupport := by
    grind [mem_mulSupport, mem_support, log_eq_zero]
  have H' : HasFiniteMulSupport f ↔ HasFiniteSupport fun a ↦ log (f a) := by
    simp [HasFiniteMulSupport, HasFiniteSupport, H]
  simp only [finprod_def, finsum_def]
  by_cases h' : HasFiniteMulSupport f
  · simp [h', log_prod (fun a _ ↦ (h a).ne'), H'.mp h', H]
  · simp [h', mt H'.mpr h']
```

Exact proof reference: record decl `d71` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x10694`, value `x11160`).

## P2 — support set (body)  [deterministic-derived]

**Domain (35):** `Real`, `Eq`, `Set`, `Function.support`, `Real.log`, `Function.mulSupport`, `Iff`, `Function.HasFiniteMulSupport`, `Function.HasFiniteSupport`, `of_eq_true`, `Set.Finite`, `True`, `iff_self`, `finprod`, `finsum`, `dite`, `Classical.propDecidable`, `Finset.prod`, `Set.Finite.toFinset`, `Not`, `Finset.sum`, `finprod_def`, `finsum_def`, `eq_true`, `dite_cond_eq_true`, `Finset`, `Real.log_prod`, `LT.lt.ne'`, `Finset.sum_congr`, `Set.Finite.toFinset.congr_simp`, `eq_self`, `dite_cond_eq_false`, `eq_false`, `Real.log_one`, `mt`

**Classified infrastructure (31):** `LT.lt` (structure-projection), `Real.instLT` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `Real.instOne` (typeclass-instance), `_private.Basic.0.Real.log_finprod._proof_1` (internal-detail), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery), `Eq.mpr` (eq-machinery), `Real.instCommMonoid` (typeclass-instance), `Real.instAddCommMonoid` (typeclass-instance), `MulOne.toOne` (structure-projection,typeclass-instance), `MulOneClass.toMulOne` (structure-projection,typeclass-instance), `Monoid.toMulOneClass` (typeclass-instance), `CommMonoid.toMonoid` (structure-projection,typeclass-instance), `One.toOfNat1` (typeclass-instance), `AddZero.toZero` (structure-projection,typeclass-instance), `AddZeroClass.toAddZero` (structure-projection,typeclass-instance), `AddMonoid.toAddZeroClass` (typeclass-instance), `AddCommMonoid.toAddMonoid` (structure-projection,typeclass-instance), `id` (eq-machinery), `congr` (eq-machinery), `Eq.ndrec` (eq-machinery,generated), `Iff.mp` (logic-core,structure-projection), `Membership.mem` (structure-projection), `SetLike.instMembership` (typeclass-instance), `Finset.instSetLike` (typeclass-instance), `Real.instPreorder` (typeclass-instance), `Eq.refl` (eq-machinery), `Iff.mpr` (logic-core,structure-projection)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `LT.lt` (4 args) : <sort>
  - `Real` (0 args)
  - `Real.instLT` (0 args)
  - `OfNat.ofNat` (3 args) : Real
    - `Real` (0 args)
    - `Zero.toOfNat0` (2 args) : OfNat
      - `Real` (0 args)
      - `Real.instZero` (0 args)
- `Eq` (3 args) : <sort>
  - `Set` (1 args) : <sort>
  - `Function.support` (4 args) : Set
    - `Real` (0 args)
    - `Real.instZero` (0 args)
    - `Real.log` (1 args) : Real
  - `Function.mulSupport` (4 args) : Set
    - `Real` (0 args)
    - `Real.instOne` (0 args)
- `_private.Basic.0.Real.log_finprod._proof_1` (3 args) : Eq [Prop]
- `Iff` (2 args) : <sort>
  - `Function.HasFiniteMulSupport` (4 args) : <sort>
    - `Real` (0 args)
    - `Real.instOne` (0 args)
  - `Function.HasFiniteSupport` (4 args) : <sort>
    - `Real` (0 args)
    - `Real.instZero` (0 args)
    - `Real.log` (1 args) : Real
- `of_eq_true` (2 args) : Iff [Prop]
  - `Iff` (2 args) : <sort>
    - `Set.Finite` (2 args) : <sort>
  ... (3633 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `of_eq_true` (2 args) : Iff (depth 0)
- `iff_self` (1 args) : Eq (depth 2)
- `finprod_def` (5 args) : Eq (depth 5)
- `finsum_def` (5 args) : Eq (depth 3)
- `dite` (5 args) : Eq (depth 1)
- `of_eq_true` (2 args) : Eq (depth 2)
- `of_eq_true` (2 args) : Function.HasFiniteMulSupport (depth 7)
- `eq_true` (2 args) : Eq (depth 8)
- `of_eq_true` (2 args) : Function.HasFiniteSupport (depth 8)
- `eq_true` (2 args) : Eq (depth 9)
- `of_eq_true` (2 args) : Function.HasFiniteMulSupport (depth 8)
- `of_eq_true` (2 args) : Function.HasFiniteMulSupport (depth 10)
- `eq_true` (2 args) : Eq (depth 11)
- `of_eq_true` (2 args) : Function.HasFiniteMulSupport (depth 9)
- `eq_true` (2 args) : Eq (depth 10)
- `dite_cond_eq_true` (6 args) : Eq (depth 8)
- `Real.log_prod` (4 args) : Eq (depth 7)
- `LT.lt.ne'` (5 args) : Ne (depth 8)
- `of_eq_true` (2 args) : Function.HasFiniteSupport (depth 9)
- `dite_cond_eq_true` (6 args) : Eq (depth 6)
- `eq_true` (2 args) : Eq (depth 7)
- `Finset.sum_congr` (9 args) : Eq (depth 6)
- `Set.Finite.toFinset.congr_simp` (5 args) : Eq (depth 7)
- `of_eq_true` (2 args) : Function.HasFiniteSupport (depth 10)
- `eq_self` (2 args) : Eq (depth 4)
  ... (54 occurrences total)

## P5 — source-level use events  [observed]

- `simp` → `mt` — `simp [h', mt H'.mpr h']`
- `simp` → `finprod_def`, `finsum_def`, `finprod_def`, `finsum_def` — `simp only [finprod_def, finsum_def]`
- `refine` → `dite` — `refine  if h'  : HasFiniteMulSupport f then  ?  pos  else  ?  neg`
- `simp` → `Function.HasFiniteMulSupport`, `Function.HasFiniteSupport`, `Function.HasFiniteMulSupport`, `Function.HasFiniteSupport` — `simp [HasFiniteMulSupport, HasFiniteSupport, H]`
- `simp` → `Real.log_prod`, `Iff.mp` — `simp [h', log_prod (fun a _ ↦ (h a).ne'), H'.mp h', H]`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  (    have H  : (fun i ↦ log (f i)).support = f.mulS`
- `refine` → (no named attribution) — `refine  no_implicit_lambda%  (    have H'  : HasFiniteMulSupport f ↔ HasFiniteSu`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Set` — def, module `Mathlib.Data.Set.Defs`
- `Function.support` — def, module `Mathlib.Algebra.Notation.Support`
- `Real.log` — def, module `Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
