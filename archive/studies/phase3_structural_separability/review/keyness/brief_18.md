# Proof 18

Theorem `uniformity_dist_of_mem_uniformity` (Mathlib source below).

```lean
theorem uniformity_dist_of_mem_uniformity [LT β] {U : Filter (α × α)} (z : β)
    (D : α → α → β) (H : ∀ s, s ∈ U ↔ ∃ ε > z, ∀ {a b : α}, D a b < ε → (a, b) ∈ s) :
    U = ⨅ ε > z, 𝓟 { p : α × α | D p.1 p.2 < ε } :=
  HasBasis.eq_biInf ⟨fun s => by simp only [H, subset_def, Prod.forall, mem_ofPred]⟩

```

## Candidate views (anonymized)

### View A
  1. Set.subset_def
  2. Set.mem_ofPred
  3. Prod.forall
  4. Filter.HasBasis.eq_biInf

### View B
  1. Filter.HasBasis.eq_biInf
  2. _private.Mathlib.Topology.EMetricSpace.Defs.0.uniformity_dist_of_mem_uniformity._simp_1_2
  3. iff_self
  4. of_eq_true
  5. _private.Mathlib.Topology.EMetricSpace.Defs.0.uniformity_dist_of_mem_uniformity._simp_1_1
  6. forall_congr
  7. congr
  8. implies_congr
  9. funext
  10. congrArg

### View C
  - Filter.HasBasis.eq_biInf
  - _private.Mathlib.Topology.EMetricSpace.Defs.0.uniformity_dist_of_mem_uniformity._simp_1_2
      . Set.mem_ofPred
      . propext
  - iff_self
  - of_eq_true
  - _private.Mathlib.Topology.EMetricSpace.Defs.0.uniformity_dist_of_mem_uniformity._simp_1_1
      . Prod.forall
      . propext
  - forall_congr

### View D
  1. Filter.HasBasis.eq_biInf
  2. _private.Mathlib.Topology.EMetricSpace.Defs.0.uniformity_dist_of_mem_uniformity._simp_1_2
  3. iff_self
  4. congrArg
  5. congr
  6. funext
  7. of_eq_true
  8. Eq.trans
  9. _private.Mathlib.Topology.EMetricSpace.Defs.0.uniformity_dist_of_mem_uniformity._simp_1_1
  10. forall_congr

### View E
  - Eq.trans
  - Filter.HasBasis.eq_biInf
  - _private.Mathlib.Topology.EMetricSpace.Defs.0.uniformity_dist_of_mem_uniformity._simp_1_1
  - _private.Mathlib.Topology.EMetricSpace.Defs.0.uniformity_dist_of_mem_uniformity._simp_1_2
  - congr
  - congrArg
  - forall_congr
  - funext
  - iff_self
  - implies_congr
  - of_eq_true
  - propext