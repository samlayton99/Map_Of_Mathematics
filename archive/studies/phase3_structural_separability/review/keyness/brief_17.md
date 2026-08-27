# Proof 17

Theorem `IsCovariantDerivativeOn.congr_of_eventuallyEq` (Mathlib source below).

```lean
lemma congr_of_eventuallyEq (hP : IsLocalSourceTargetProperty P)
    (hf : LiftSourceTargetPropertyAt I J n f x P)
    (h' : f =ᶠ[nhds x] g) : LiftSourceTargetPropertyAt I J n g x P := by
  obtain ⟨s', hxs', hfg⟩ := h'.exists_mem
  obtain ⟨s, hss', hs, hxs⟩ := mem_nhds_iff.mp hxs'
  refine ⟨hf.domChart.restr s, hf.codChart, ?_, ?_, ?_, hf.codChart_mem_maximalAtlas, ?_, ?_⟩
  · simpa using ⟨mem_domChart_source hf, by rwa [interior_eq_iff_isOpen.mpr hs]⟩
  · exact hfg (mem_of_mem_nhds hxs') ▸ mem_codChart_source hf
  · exact restr_mem_maximalAtlas _ hf.domChart_mem_maximalAtlas hs
  · trans s' ∩ f ⁻¹' hf.codChart.source
    · apply subset_inter
      · exact Subset.trans (by simp [interior_eq_iff_isOpen.mpr hs]) hss'
      · exact Subset.trans (by simp) hf.source_subset_preimage_source
    · rw [hfg.inter_preimage_eq]; exact inter_subset_right
  · exact hP.congr (hfg.mono hss' |>.mono (by grind)) <| hP.mono_source hs hf.property

```

## Candidate views (anonymized)

### View A
  1. HasMFDerivAt.mfderiv
  2. hasMFDerivAt_const
  3. HasMFDerivAt.congr_of_eventuallyEq
  4. IsCovariantDerivativeOn.mono
  5. IsCovariantDerivativeOn.leibniz
  6. ContinuousLinearMap.smulRight.congr_simp
  7. ContinuousLinearMap.zero_smulRight
  8. ContinuousLinearMap.comp_zero
  9. HasMFDerivAt.mdifferentiableAt
  10. mem_of_mem_nhds

### View B
  1. IsCovariantDerivativeOn.congr_of_eqOn
  2. Classical.choose_spec
  3. Set.inter_subset_left
  4. congrArg
  5. And.right
  6. And.left
  7. IsCovariantDerivativeOn.mono
  8. Filter.inter_mem
  9. propext
  10. Filter.eventually_iff_exists_mem

### View C
  (none)

### View D
  - IsCovariantDerivativeOn.congr_of_eqOn
      . HasMFDerivAt.mfderiv
      . hasMFDerivAt_const
      . HasMFDerivAt.congr_of_eventuallyEq
      . IsCovariantDerivativeOn.leibniz
  - IsCovariantDerivativeOn.mono
  - Filter.eventually_iff_exists_mem
  - Classical.choose_spec
  - Filter.inter_mem
  - Set.inter_subset_left

### View E
  - And.left
  - And.right
  - Classical.choose_spec
  - Filter.eventually_iff_exists_mem
  - Filter.inter_mem
  - IsCovariantDerivativeOn.congr_of_eqOn
  - IsCovariantDerivativeOn.mono
  - Set.inter_subset_left
  - congrArg
  - propext