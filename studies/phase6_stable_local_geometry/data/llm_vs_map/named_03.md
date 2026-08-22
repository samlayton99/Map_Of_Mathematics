# Premise retrieval — batch 03

For each Lean 4 / Mathlib theorem below you are shown ONLY its statement.
The proof is not shown and you must not try to recall the file.

For each item, predict which Mathlib declarations the PROOF uses: name
the 10 declarations you judge most likely to be cited by the proof,
most likely first. Rules:

- Give fully-qualified Mathlib names exactly as they appear in the
  library (e.g. `Finset.sum_congr`, `Polynomial.degree_mul`).
- Predict the substantive mathematical lemmas/definitions the proof
  builds on, not tactic-level plumbing (`Eq.mpr`, `congrArg`, `rfl`,
  `id`) and not things already named in the statement itself.
- Exactly 10 names per item, no commentary, no duplicates.

Answer as JSON only:
{"q01": ["Name.one", "Name.two", ...], "q02": [...], ...}

---


## q21  `CategoryTheory.Limits.pullbackZeroZeroIso_hom_fst`
module: `Mathlib.CategoryTheory.Limits.Constructions.ZeroObjects`

```lean
theorem pullbackZeroZeroIso_hom_fst (X Y : C) [HasBinaryProduct X Y] :
    (pullbackZeroZeroIso X Y).hom ≫ prod.fst = pullback.fst 0 0
```

## q22  `Finset.not_disjoint_iff`
module: `Mathlib.Data.Finset.Disjoint`

```lean
theorem not_disjoint_iff : ¬Disjoint s t ↔ ∃ a, a ∈ s ∧ a ∈ t
```

## q23  `MulRingNormClass.toRingNormClass`
module: `Mathlib.Algebra.Order.Hom.Basic`

```lean
instance (priority := 100) MulRingNormClass.toRingNormClass [NonAssocRing α]
    [Semiring β] [PartialOrder β] [MulRingNormClass F α β] : RingNormClass F α β
```

## q24  `CoxeterSystem.IsReflection.inv`
module: `Mathlib.GroupTheory.Coxeter.Inversion`

```lean
theorem inv : t⁻¹ = t
```

## q25  `Real.one_sub_div_pow_le_exp_neg`
module: `Mathlib.Analysis.Complex.Exponential`

```lean
theorem one_sub_div_pow_le_exp_neg {n : ℕ} {t : ℝ} (ht' : t ≤ n) : (1 - t / n) ^ n ≤ exp (-t)
```

## q26  `Matrix.diagonal_transvection_induction`
module: `Mathlib.LinearAlgebra.Matrix.Transvection`

```lean
theorem diagonal_transvection_induction (P : Matrix n n 𝕜 → Prop) (M : Matrix n n 𝕜)
    (hdiag : ∀ D : n → 𝕜, det (diagonal D) = det M → P (diagonal D))
    (htransvec : ∀ t : TransvectionStruct n 𝕜, P t.toMatrix) (hmul : ∀ A B, P A → P B → P (A * B)) :
    P M
```

## q27  `Ordinal.invVeblen₂_gamma`
module: `Mathlib.SetTheory.Ordinal.Veblen`

```lean
theorem invVeblen₂_gamma (o : Ordinal) : invVeblen₂ (Γ_ o) = 0
```

## q28  `legendreSym.eq_one_of_sq_sub_mul_sq_eq_zero'`
module: `Mathlib.NumberTheory.LegendreSymbol.Basic`

```lean
theorem eq_one_of_sq_sub_mul_sq_eq_zero' {p : ℕ} [Fact p.Prime] {a : ℤ} (ha : (a : ZMod p) ≠ 0)
    {x y : ZMod p} (hx : x ≠ 0) (hxy : x ^ 2 - a * y ^ 2 = 0) : legendreSym p a = 1
```

## q29  `MonoidHom.ker_transferSylow_disjoint`
module: `Mathlib.GroupTheory.Transfer`

```lean
theorem ker_transferSylow_disjoint (Q : Subgroup G) (hQ : IsPGroup p Q) :
    Disjoint (transferSylow P hP).ker Q
```

## q30  `AddMonoidAlgebra.isGroupLikeElem_of`
module: `Mathlib.RingTheory.Bialgebra.MonoidAlgebra`

```lean
lemma isGroupLikeElem_of (m : M) : IsGroupLikeElem R (of A M m)
```
