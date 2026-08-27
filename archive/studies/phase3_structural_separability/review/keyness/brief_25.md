# Proof 25

Theorem `exists_compact_closed_between` (Mathlib source below).

```lean
theorem exists_compact_closed_between [LocallyCompactSpace X] [RegularSpace X]
    {K U : Set X} (hK : IsCompact K) (hU : IsOpen U) (h_KU : K ⊆ U) :
    ∃ L, IsCompact L ∧ IsClosed L ∧ K ⊆ interior L ∧ L ⊆ U :=
  let ⟨L, L_comp, KL, LU⟩ := exists_compact_between hK hU h_KU
  ⟨closure L, L_comp.closure, isClosed_closure, KL.trans <| interior_mono subset_closure,
    L_comp.closure_subset_of_isOpen hU LU⟩

```

## Candidate views (anonymized)

### View A
  1. _private.Mathlib.Topology.Separation.Regular.0.exists_compact_closed_between.match_1_1
  2. IsCompact.closure
  3. IsCompact.closure_subset_of_isOpen
  4. subset_closure
  5. LE.le.trans
  6. interior_mono
  7. isClosed_closure
  8. exists_compact_between

### View B
  1. subset_closure
  2. isClosed_closure
  3. interior_mono
  4. exists_compact_between

### View C
  1. IsCompact.closure
  2. IsCompact.closure_subset_of_isOpen
  3. exists_compact_between
  4. isClosed_closure
  5. interior_mono
  6. subset_closure
  7. _private.Mathlib.Topology.Separation.Regular.0.exists_compact_closed_between.match_1_1
  8. LE.le.trans

### View D
  - IsCompact.closure
  - IsCompact.closure_subset_of_isOpen
  - LE.le.trans
  - _private.Mathlib.Topology.Separation.Regular.0.exists_compact_closed_between.match_1_1
  - exists_compact_between
  - interior_mono
  - isClosed_closure
  - subset_closure

### View E
  - IsCompact.closure
  - IsCompact.closure_subset_of_isOpen
  - exists_compact_between
  - isClosed_closure
  - interior_mono
  - subset_closure