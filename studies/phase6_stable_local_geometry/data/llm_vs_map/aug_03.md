# Premise retrieval with structural hints — batch 03

For each Lean 4 / Mathlib theorem you are shown its statement, plus a
list of CANDIDATE declarations proposed by a structural index. The
index knows nothing about mathematics or names: it ranks declarations
purely by which lemmas tend to be cited together with the things this
theorem's statement mentions. Its suggestions are often in the right
neighbourhood but the wrong lemma, and are sometimes useless. Roughly
one in ten of its top suggestions is actually used by the proof.

Use the hints as evidence, not as an answer key. You may keep, reorder,
or discard any of them, and you should add your own candidates freely.

For each item, give the 10 declarations you judge most likely to be
cited by the PROOF, most likely first. Rules:

- Fully-qualified Mathlib names, exactly as they appear in the library.
- Substantive mathematical lemmas/definitions, not tactic plumbing
  (`Eq.mpr`, `congrArg`, `rfl`, `id`), and not things already named in
  the statement.
- Exactly 10 names per item, no commentary, no duplicates.

Answer as JSON only:
{"q01": ["Name.one", ...], "q02": [...], ...}

---


## q21  `CategoryTheory.Limits.pullbackZeroZeroIso_hom_fst`
module: `Mathlib.CategoryTheory.Limits.Constructions.ZeroObjects`

```lean
theorem pullbackZeroZeroIso_hom_fst (X Y : C) [HasBinaryProduct X Y] :
    (pullbackZeroZeroIso X Y).hom ≫ prod.fst = pullback.fst 0 0
```

structural index suggests:
  1. `CategoryTheory.Limits.pullback.condition`
  2. `CategoryTheory.Limits.PullbackCone.mk_π_app`
  3. `CategoryTheory.Limits.limit.lift_π_assoc`
  4. `CategoryTheory.Limits.pullback.hom_ext`
  5. `CategoryTheory.IsPullback.of_hasPullback`
  6. `CategoryTheory.Limits.pullback.lift_fst`
  7. `CategoryTheory.Limits.prod.comp_lift`
  8. `CategoryTheory.Limits.pullback.lift_snd`
  9. `CategoryTheory.Limits.prod.map_snd`
  10. `CategoryTheory.Limits.prod.hom_ext`

## q22  `Finset.not_disjoint_iff`
module: `Mathlib.Data.Finset.Disjoint`

```lean
theorem not_disjoint_iff : ¬Disjoint s t ↔ ∃ a, a ∈ s ∧ a ∈ t
```

structural index suggests:
  1. `Finpartition.card_bind`
  2. `SzemerediRegularity.card_aux₂`
  3. `SzemerediRegularity.card_aux₁`
  4. `SzemerediRegularity.a_add_one_le_four_pow_parts_card`
  5. `Finset.sum_apply_dite._proof_1`
  6. `Finset.univ_eq_attach`
  7. `Finset.sum_const_nat`
  8. `Finset.card_filter_add_card_filter_not`
  9. `Part.mem_bind_iff`
  10. `Finset.Nonempty.card_pos`

## q23  `MulRingNormClass.toRingNormClass`
module: `Mathlib.Algebra.Order.Hom.Basic`

```lean
instance (priority := 100) MulRingNormClass.toRingNormClass [NonAssocRing α]
    [Semiring β] [PartialOrder β] [MulRingNormClass F α β] : RingNormClass F α β
```

structural index: no suggestion for this item.

## q24  `CoxeterSystem.IsReflection.inv`
module: `Mathlib.GroupTheory.Coxeter.Inversion`

```lean
theorem inv : t⁻¹ = t
```

structural index suggests:
  1. `CoxeterSystem.inv_simple`
  2. `CoxeterSystem.simple_mul_simple_self`
  3. `CoxeterSystem.wordProd_cons`
  4. `CoxeterSystem.wordProd_nil`
  5. `CoxeterSystem.lengthParity_simple`
  6. `CoxeterSystem.wordProd_singleton`
  7. `CoxeterSystem.isReflection_simple`
  8. `CoxeterSystem.length_simple`
  9. `CoxeterSystem.simple_mul_simple_cancel_left`
  10. `CoxeterSystem.lengthParity_eq_ofAdd_length`

## q25  `Real.one_sub_div_pow_le_exp_neg`
module: `Mathlib.Analysis.Complex.Exponential`

```lean
theorem one_sub_div_pow_le_exp_neg {n : ℕ} {t : ℝ} (ht' : t ≤ n) : (1 - t / n) ^ n ≤ exp (-t)
```

structural index suggests:
  1. `Real.exp_pos`
  2. `Real.exp_zero`
  3. `Real.exp_log`
  4. `Real.rpow_def_of_pos`
  5. `Complex.ofReal_exp`
  6. `Real.pi_pos`
  7. `Real.exp_add`
  8. `norm_nonneg`
  9. `Real.exp_neg`
  10. `Real.log_exp`

## q26  `Matrix.diagonal_transvection_induction`
module: `Mathlib.LinearAlgebra.Matrix.Transvection`

```lean
theorem diagonal_transvection_induction (P : Matrix n n 𝕜 → Prop) (M : Matrix n n 𝕜)
    (hdiag : ∀ D : n → 𝕜, det (diagonal D) = det M → P (diagonal D))
    (htransvec : ∀ t : TransvectionStruct n 𝕜, P t.toMatrix) (hmul : ∀ A B, P A → P B → P (A * B)) :
    P M
```

structural index suggests:
  1. `Matrix.det_transpose`
  2. `Matrix.det_mul`
  3. `RingHom.mapMatrix_apply`
  4. `Matrix.det_one`
  5. `Finset.sum_congr`
  6. `LinearMap.det_toMatrix`
  7. `RingHom.map_det`
  8. `Finset.prod_congr`
  9. `Matrix.det_fin_two`
  10. `Matrix.det_diagonal`

## q27  `Ordinal.invVeblen₂_gamma`
module: `Mathlib.SetTheory.Ordinal.Veblen`

```lean
theorem invVeblen₂_gamma (o : Ordinal) : invVeblen₂ (Γ_ o) = 0
```

structural index suggests:
  1. `Ordinal.veblen_invVeblen₁_invVeblen₂`
  2. `Ordinal.enum_typein`
  3. `Ordinal.typein_lt_type`
  4. `Ordinal.type_toType`
  5. `Ordinal.enum_lt_enum`
  6. `Ordinal.veblen_le_veblen_iff_right`
  7. `Order.lt_succ`
  8. `_private.Mathlib.SetTheory.Ordinal.Exponential.0.Ordinal.opow_of_ne_zero`
  9. `Ordinal.limitRecOn_limit`
  10. `Ordinal.typein_lt_self`

## q28  `legendreSym.eq_one_of_sq_sub_mul_sq_eq_zero'`
module: `Mathlib.NumberTheory.LegendreSymbol.Basic`

```lean
theorem eq_one_of_sq_sub_mul_sq_eq_zero' {p : ℕ} [Fact p.Prime] {a : ℤ} (ha : (a : ZMod p) ≠ 0)
    {x y : ZMod p} (hx : x ≠ 0) (hxy : x ^ 2 - a * y ^ 2 = 0) : legendreSym p a = 1
```

structural index suggests:
  1. `Nat.Prime.ne_one`
  2. `Lean.Grind.of_eq_eq_true`
  3. `Lean.Grind.not_and`
  4. `Lean.Grind.not_not`
  5. `Lean.Grind.iff_eq`
  6. `Classical.byContradiction`
  7. `Std.Iter.step_filterMap`
  8. `Nat.Prime.pos`
  9. `IntermediateField.algebraMap_mem`
  10. `Subfield.closure_eq`

## q29  `MonoidHom.ker_transferSylow_disjoint`
module: `Mathlib.GroupTheory.Transfer`

```lean
theorem ker_transferSylow_disjoint (Q : Subgroup G) (hQ : IsPGroup p Q) :
    Disjoint (transferSylow P hP).ker Q
```

structural index suggests:
  1. `Nat.card_eq_fintype_card`
  2. `Nat.card_congr`
  3. `Nat.card_eq_zero_of_infinite`
  4. `Nat.card_pos`
  5. `Nat.finite_of_card_ne_zero`
  6. `Nat.card_prod`
  7. `Fintype.card_eq_nat_card`
  8. `Set.ncard_univ`
  9. `nonempty_fintype`
  10. `Nat.card_eq_one_iff_unique`

## q30  `AddMonoidAlgebra.isGroupLikeElem_of`
module: `Mathlib.RingTheory.Bialgebra.MonoidAlgebra`

```lean
lemma isGroupLikeElem_of (m : M) : IsGroupLikeElem R (of A M m)
```

structural index suggests:
  1. `toAdd_ofAdd`
  2. `ofAdd_toAdd`
  3. `toAdd_mul`
  4. `Multiplicative.toAdd_le`
  5. `Multiplicative.toAdd_lt`
  6. `WithZero.coe_lt_coe`
  7. `WithZero.coe_le_coe`
  8. `isAddLeftRegular_toAdd`
  9. `isAddRightRegular_toAdd`
  10. `Multiplicative.ext_iff`
