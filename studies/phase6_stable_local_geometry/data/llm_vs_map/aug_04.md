# Premise retrieval with structural hints — batch 04

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


## q31  `Topology.IsEmbedding.piMap`
module: `Mathlib.Topology.Constructions`

```lean
protected lemma Topology.IsEmbedding.piMap {f : ∀ i, A i → B i}
    (hf : ∀ i, IsEmbedding (f i)) : IsEmbedding (Pi.map f)
```

structural index suggests:
  1. `continuous_induced_rng`
  2. `continuous_pi_iff`
  3. `pi_generateFrom_eq`
  4. `WeakBilin.coeFn_continuous`
  5. `induced_compose`
  6. `continuous_pi`
  7. `induced_to_pi`
  8. `LinearMap.IsWeak.continuous_eval`
  9. `Topology.isInducing_iff`
  10. `induced_iInf`

## q32  `Finset.union_sdiff_self_eq_union`
module: `Mathlib.Data.Finset.SDiff`

```lean
theorem union_sdiff_self_eq_union : s ∪ t \ s = s ∪ t
```

structural index: no suggestion for this item.

## q33  `AlgebraicGeometry.LocallyRingedSpace.restrictStalkIso_inv_eq_germ`
module: `Mathlib.Geometry.RingedSpace.LocallyRingedSpace`

```lean
lemma restrictStalkIso_inv_eq_germ :
    X.presheaf.germ (h.functor.obj V) (f x) ⟨x, hx, rfl⟩ ≫
      (X.restrictStalkIso h x).inv = (X.restrict h).presheaf.germ _ x hx
```

structural index suggests:
  1. `Part.mem_bind_iff`

## q34  `Nat.size_bit`
module: `Mathlib.Data.Nat.Size`

```lean
theorem size_bit {b n} (h : bit b n ≠ 0) : size (bit b n) = succ (size n)
```

structural index: no suggestion for this item.

## q35  `CategoryTheory.Localization.Preadditive.neg'_add'_self`
module: `Mathlib.CategoryTheory.Localization.CalculusOfFractions.Preadditive`

```lean
lemma neg'_add'_self (f : L.obj X ⟶ L.obj Y) :
    add' W (neg' W f) f = L.map 0
```

structural index suggests:
  1. `CategoryTheory.Localization.Preadditive.add'_eq`
  2. `CategoryTheory.Localization.exists_leftFraction₂`
  3. `CategoryTheory.Localization.Preadditive.add'_comm`
  4. `CategoryTheory.Localization.Preadditive.add'_zero`
  5. `CategoryTheory.Localization.Preadditive.zero_add'`
  6. `CategoryTheory.Localization.Preadditive.add'_assoc`
  7. `ChainComplex.next_nat_succ`
  8. `CochainComplex.prev_nat_succ`
  9. `CategoryTheory.Preadditive.hasKernel_of_hasEqualizer`
  10. `CategoryTheory.Preadditive.hasEqualizer_of_hasKernel`

## q36  `completedRiemannZeta₀_zero`
module: `Mathlib.NumberTheory.Harmonic.ZetaAsymp`

```lean
lemma completedRiemannZeta₀_zero : completedRiemannZeta₀ 0 = (γ - Complex.log (4 * π)) / 2 + 1
```

structural index suggests:
  1. `Complex.ofReal_mul`
  2. `Real.pi_pos`
  3. `Complex.ofReal_inj`
  4. `Complex.ofReal_div`
  5. `Complex.ofReal_neg`
  6. `Complex.ofReal_add`
  7. `Complex.mul_im`
  8. `Complex.mul_re`
  9. `Complex.ofReal_cos`
  10. `Complex.norm_real`

## q37  `UniformOnFun.postcomp_uniformContinuous`
module: `Mathlib.Topology.UniformSpace.UniformConvergenceTopology`

```lean
protected theorem postcomp_uniformContinuous [UniformSpace γ] {f : γ → β}
    (hf : UniformContinuous f) : UniformContinuous (ofFun 𝔖 ∘ (f ∘ ·) ∘ toFun 𝔖)
```

structural index suggests:
  1. `UniformSpace.comap_iInf`
  2. `uniformContinuous_iff_le_comap`
  3. `Pi.uniformSpace_eq`
  4. `UniformSpace.ext`
  5. `UniformSpace.replaceTopology_eq`
  6. `UniformSpace.comap_inf`
  7. `UniformOnFun.precomp_uniformContinuous`
  8. `UniformSpace.comap_comap`
  9. `IsProperMap.isCompact_preimage`
  10. `iInf_uniformity`

## q38  `AddLECancellable.tsub_eq_iff_eq_add_of_le`
module: `Mathlib.Algebra.Order.Sub.Unbundled.Basic`

```lean
protected theorem tsub_eq_iff_eq_add_of_le (hb : AddLECancellable b) (h : b ≤ a) :
    a - b = c ↔ a = c + b
```

structural index: no suggestion for this item.

## q39  `hasSum_coe_mul_geometric_of_norm_lt_one`
module: `Mathlib.Analysis.SpecificLimits.Normed`

```lean
theorem hasSum_coe_mul_geometric_of_norm_lt_one {r : 𝕜} (hr : ‖r‖ < 1) :
    HasSum (fun n ↦ n * r ^ n : ℕ → 𝕜) (r / (1 - r) ^ 2)
```

structural index suggests:
  1. `Summable.hasSum`
  2. `Multipliable.hasProd`
  3. `HasSum.tsum_eq`
  4. `Finset.sum_congr`
  5. `tsum_zero`
  6. `ENNReal.summable`
  7. `HasProd.tprod_eq`
  8. `Finset.prod_congr`
  9. `norm_nonneg`
  10. `MeasureTheory.measure_mono`

## q40  `finprod_mem_eq_finite_toFinset_prod`
module: `Mathlib.Algebra.BigOperators.Finprod`

```lean
theorem finprod_mem_eq_finite_toFinset_prod (f : α → M) {s : Set α} (hs : s.Finite) :
    ∏ᶠ i ∈ s, f i = ∏ i ∈ hs.toFinset, f i
```

structural index suggests:
  1. `Set.Finite.mem_toFinset`
  2. `Set.Finite.coe_toFinset`
  3. `Finset.finite_toSet`
  4. `Finset.sum_congr`
  5. `Set.Finite.subset`
  6. `Filter.TendstoCofinite.finite_preimage_singleton`
  7. `Set.ncard_eq_toFinset_card`
  8. `finsum_eq_sum`
  9. `Finset.ext`
  10. `Set.toFinite_toFinset`
