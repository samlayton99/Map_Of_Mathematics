# Proof 3

Theorem `AddGroupFilterBasis.t2Space_iff_sInter_subset` (Mathlib source below).

```lean
lemma t2Space_iff_sInter_subset [t : TopologicalSpace G] (F : GroupFilterBasis G)
    (hG : F.topology = t) : T2Space G ↔ ⋂₀ F.sets ⊆ {1} := by
  rw [F.t2Space_iff hG, subset_antisymm_iff, and_iff_left_iff_imp]
  rintro -
  simpa using! fun _ ↦ F.one

```

## Candidate views (anonymized)

### View A
  - AddGroupFilterBasis.t2Space_iff
      . IsTopologicalAddGroup.t2Space_iff_zero_closed
      . R0Space.closure_singleton
      . AddGroupFilterBasis.isTopologicalAddGroup
      . closure_eq_iff_isClosed
  - Set.subset_sInter_iff
  - subset_antisymm_iff
  - Set.singleton_subset_iff
  - FilterBasis.mem_sets
  - AddGroupFilterBasis.zero

### View B
  - AddGroupFilterBasis.t2Space_iff
  - AddGroupFilterBasis.zero
  - Eq.trans
  - FilterBasis.mem_sets
  - Set.singleton_subset_iff
  - Set.subset_sInter_iff
  - and_iff_left_iff_imp
  - congrArg
  - forall_congr
  - implies_congr
  - propext
  - subset_antisymm_iff

### View C
  (none)

### View D
  1. R0Space.closure_singleton
  2. IsTopologicalAddGroup.t1Space
  3. AddGroupFilterBasis.isTopologicalAddGroup
  4. closure_eq_iff_isClosed
  5. AddGroupFilterBasis.nhds_zero_eq
  6. FilterBasis.ker_filter
  7. Set.subset_sInter_iff
  8. subset_antisymm_iff
  9. Set.singleton_subset_iff
  10. FilterBasis.mem_sets

### View E
  1. subset_antisymm_iff
  2. congrArg
  3. implies_congr
  4. Set.singleton_subset_iff
  5. and_iff_left_iff_imp
  6. AddGroupFilterBasis.t2Space_iff
  7. Set.subset_sInter_iff
  8. FilterBasis.mem_sets
  9. Eq.trans
  10. forall_congr