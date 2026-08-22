# Premise retrieval with structural hints — batch 02

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


## q11  `MeasureTheory.IsStoppingTime.piecewise_of_le`
module: `Mathlib.Probability.Process.Stopping`

```lean
theorem IsStoppingTime.piecewise_of_le (hτ_st : IsStoppingTime 𝒢 τ) (hη_st : IsStoppingTime 𝒢 η)
    (hτ : ∀ ω, i ≤ τ ω) (hη : ∀ ω, i ≤ η ω) (hs : MeasurableSet[𝒢 i] s) :
    IsStoppingTime 𝒢 (s.piecewise τ η)
```

structural index suggests:
  1. `Lean.Grind.of_eq_eq_true`
  2. `Lean.Grind.not_and`
  3. `Lean.Grind.not_not`
  4. `Lean.Grind.iff_eq`
  5. `Classical.byContradiction`
  6. `Set.le_piecewise`
  7. `Std.Internal.List.getValue?_eq_some_getValue`
  8. `Part.mem_bind_iff`
  9. `Lean.Grind.not_or`
  10. `Bool.cond_eq_ite`

## q12  `PartialEquiv.trans_refl`
module: `Mathlib.Logic.Equiv.PartialEquiv`

```lean
theorem trans_refl : e.trans (PartialEquiv.refl β) = e
```

structural index suggests:
  1. `Set.univ_inter`
  2. `PartialEquiv.ext`
  3. `PartialEquiv.trans_assoc`
  4. `PartialEquiv.trans_source`
  5. `PartialEquiv.transEquiv_eq_trans`
  6. `Equiv.trans_toPartialEquiv`
  7. `PartialEquiv.symm_image_target_inter_eq`
  8. `PartialEquiv.trans_target''`
  9. `ModelWithCorners.toPartialEquiv_coe`
  10. `Bundle.Pretrivialization.symm_trans_source_eq`

## q13  `Multiset.nodup_iff_pairwise`
module: `Mathlib.Data.Multiset.Replicate`

```lean
theorem nodup_iff_pairwise {α} {s : Multiset α} : Nodup s ↔ Pairwise (· ≠ ·) s
```

structural index suggests:
  1. `Multiset.coe_eq_zero`
  2. `Multiset.coe_toList`
  3. `Multiset.sum_coe`
  4. `Multiset.induction_on`
  5. `Multiset.prod_coe`
  6. `Multiset.nodup_cons`
  7. `List.le_prod_nonempty_of_submultiplicative`
  8. `List.le_sum_nonempty_of_subadditive_on_pred`
  9. `List.le_sum_nonempty_of_subadditive`
  10. `Multiset.powersetCardAux_eq_map_coe`

## q14  `PerfectRing.lift_comp_lift_apply_eq_self`
module: `Mathlib.FieldTheory.IsPerfectClosure`

```lean
theorem lift_comp_lift_apply_eq_self [PerfectRing L p] (x : L) :
    lift j i p (lift i j p x) = x
```

structural index suggests:
  1. `PerfectRing.lift_comp`
  2. `PerfectRing.comp_lift`
  3. `IsPRadical.injective_comp_of_perfect`
  4. `PerfectRing.lift_comp_apply`
  5. `PerfectRing.lift_comp_lift`
  6. `iterateFrobeniusEquiv_zero`
  7. `PerfectRing.lift_apply`
  8. `WeierstrassCurve.map_Δ`
  9. `RingHom.algebraMap_toAlgebra`
  10. `PerfectRing.lift_lift`

## q15  `Matrix.permanent_zero`
module: `Mathlib.LinearAlgebra.Matrix.Permanent`

```lean
theorem permanent_zero [Nonempty n] : permanent (0 : Matrix n n R) = 0
```

structural index suggests:
  1. `Multiset.map_map`
  2. `Multiset.map_congr`
  3. `Finset.sum_apply`
  4. `Finset.prod_mul_distrib`
  5. `Finset.sum_add_distrib`
  6. `Finset.prod_const`
  7. `Finset.sum_const`
  8. `Finset.prod_apply`
  9. `Multiset.card_map`
  10. `Finset.prod_congr`

## q16  `Finset.piecewise_piecewise_of_subset_left`
module: `Mathlib.Data.Finset.Piecewise`

```lean
lemma piecewise_piecewise_of_subset_left {s t : Finset ι} [∀ i, Decidable (i ∈ s)]
    [∀ i, Decidable (i ∈ t)] (h : s ⊆ t) (f₁ f₂ g : ∀ a, π a) :
    s.piecewise (t.piecewise f₁ f₂) g = s.piecewise f₁ g
```

structural index suggests:
  1. `Finset.piecewise_eq_of_mem`
  2. `Finset.piecewise_eq_of_notMem`
  3. `Finset.sum_congr`
  4. `Finset.piecewise_empty`
  5. `Finset.piecewise_insert`
  6. `Finset.piecewise_univ`
  7. `Finset.induction_on`
  8. `Finset.prod_congr`
  9. `Finset.prod_piecewise`
  10. `Finset.update_eq_piecewise`

## q17  `CategoryTheory.Limits.biproduct.matrixEquiv`
module: `Mathlib.CategoryTheory.Limits.Shapes.Biproducts`

```lean
def biproduct.matrixEquiv : (⨁ f ⟶ ⨁ g) ≃ ∀ j k, f j ⟶ g k
```

structural index: no suggestion for this item.

## q18  `ciInf_mono`
module: `Mathlib.Order.ConditionallyCompleteLattice.Indexed`

```lean
theorem ciInf_mono {f g : ι → α} (B : BddBelow (range f)) (H : ∀ x, f x ≤ g x) : iInf f ≤ iInf g
```

structural index: no suggestion for this item.

## q19  `SubMulAction.val_preimage_orbit`
module: `Mathlib.GroupTheory.GroupAction.SubMulAction`

```lean
theorem val_preimage_orbit {p : SubMulAction R M} (m : p) :
    Subtype.val ⁻¹' MulAction.orbit R (m : M) = MulAction.orbit R m
```

structural index suggests:
  1. `Part.mem_bind_iff`

## q20  `IsLocallyConstant.of_constant_on_connected_clopens`
module: `Mathlib.Topology.LocallyConstant.Basic`

```lean
theorem of_constant_on_connected_clopens [LocallyConnectedSpace X] {f : X → Y}
    (h : ∀ U : Set X, IsConnected U → IsClopen U → ∀ x ∈ U, ∀ y ∈ U, f y = f x) :
    IsLocallyConstant f
```

structural index suggests:
  1. `Part.mem_bind_iff`
