# Proof 2

Theorem `isCyclotomicExtension_iff_eq_adjoin` (Mathlib source below).

```lean
theorem isCyclotomicExtension_iff_eq_adjoin (C : Subalgebra A B)
    (hS : ∀ n ∈ S, n ≠ 0 → ∃ r : B, IsPrimitiveRoot r n) :
    IsCyclotomicExtension S A C ↔ C = Algebra.adjoin A {x : B | ∃ n ∈ S, n ≠ 0 ∧ x ^ n = 1} := by
  refine ⟨fun h ↦ ?_, fun h ↦ h ▸ isCyclotomicExtension_adjoin_of_exists_isPrimitiveRoot S A B hS⟩
  have := congr_arg (Subalgebra.map C.val) ((IsCyclotomicExtension.iff_adjoin_eq_top _ _ _).mp h).2
  rw [← Subalgebra.range_val C, ← Algebra.map_top, ← this, AlgHom.map_adjoin]
  congr; ext
  simp only [Subalgebra.coe_val, ne_eq, ← Subalgebra.coe_eq_one, SubmonoidClass.coe_pow,
    Set.mem_image, Set.mem_ofPred_eq, Subtype.exists, exists_and_left, exists_prop,
    exists_eq_right_right, and_iff_left_iff_imp, forall_exists_index, and_imp]
  exact fun n hn₁ hn₂ hx ↦ h.mem_of_pow_eq_one S C hn₁ hn₂ hx

```

## Candidate views (anonymized)

### View A
  - IsCyclotomicExtension.mem_of_pow_eq_one
      . IsPrimitiveRoot.eq_pow_of_pow_eq_one
      . IsPrimitiveRoot.map_of_injective
      . Subalgebra.pow_mem
      . FaithfulSMul.algebraMap_injective
  - IsCyclotomicExtension.iff_adjoin_eq_top
  - Algebra.map_top
  - AlgHom.map_adjoin
  - Algebra.isCyclotomicExtension_adjoin_of_exists_isPrimitiveRoot
  - Subalgebra.range_val

### View B
  - AlgHom.map_adjoin
  - Algebra.isCyclotomicExtension_adjoin_of_exists_isPrimitiveRoot
  - Algebra.map_top
  - And.right
  - Eq.symm
  - Eq.trans
  - Iff.mp
  - Iff.of_eq
  - IsCyclotomicExtension.iff_adjoin_eq_top
  - IsCyclotomicExtension.mem_of_pow_eq_one
  - Set.ext
  - Subalgebra.range_val
  - _private.Mathlib.NumberTheory.Cyclotomic.Basic.0.isCyclotomicExtension_iff_eq_adjoin._simp_1_1
  - _private.Mathlib.NumberTheory.Cyclotomic.Basic.0.isCyclotomicExtension_iff_eq_adjoin._simp_1_2

### View C
  1. ne_eq
  2. forall_exists_index
  3. exists_prop
  4. exists_eq_right_right
  5. exists_and_left
  6. and_imp
  7. and_iff_left_iff_imp
  8. Subtype.exists
  9. SubmonoidClass.coe_pow
  10. Subalgebra.coe_val

### View D
  1. Subalgebra.range_val
  2. congrArg
  3. _private.Mathlib.NumberTheory.Cyclotomic.Basic.0.isCyclotomicExtension_iff_eq_adjoin._simp_1_1
  4. Set.ext
  5. Eq.symm
  6. propext
  7. _private.Mathlib.NumberTheory.Cyclotomic.Basic.0.isCyclotomicExtension_iff_eq_adjoin._simp_1_6
  8. implies_congr
  9. _private.Mathlib.NumberTheory.Cyclotomic.Basic.0.isCyclotomicExtension_iff_eq_adjoin._simp_1_7
  10. Iff.mp

### View E
  1. IsPrimitiveRoot.eq_pow_of_pow_eq_one
  2. IsCyclotomicExtension.iff_adjoin_eq_top
  3. Algebra.map_top
  4. AlgHom.map_adjoin
  5. Algebra.isCyclotomicExtension_adjoin_of_exists_isPrimitiveRoot
  6. IsPrimitiveRoot.map_of_injective
  7. Subalgebra.range_val
  8. _private.Mathlib.NumberTheory.Cyclotomic.Basic.0.isCyclotomicExtension_iff_eq_adjoin._simp_1_1
  9. Subalgebra.pow_mem
  10. FaithfulSMul.algebraMap_injective