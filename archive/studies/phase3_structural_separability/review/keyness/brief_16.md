# Proof 16

Theorem `SimpleGraph.neighborSet_sum_inr` (Mathlib source below).

```lean
lemma neighborSet_sum_inr (w : W) : (G ⊕g H).neighborSet (.inr w) = Sum.inr '' H.neighborSet w := by
  ext (v' | w') <;> simp

```

## Candidate views (anonymized)

### View A
  1. Set.ext
  2. SimpleGraph.mem_neighborSet._simp_1
  3. iff_self
  4. congrArg
  5. congr
  6. exists_false._simp_1
  7. funext
  8. of_eq_true
  9. Set.mem_image._simp_1
  10. and_false

### View B
  - Eq.trans
  - Set.ext
  - Set.mem_image._simp_1
  - SimpleGraph.mem_neighborSet._simp_1
  - SimpleGraph.sum_adj
  - Sum.inr.injEq
  - and_false
  - congr
  - congrArg
  - eq_false'
  - exists_eq_right._simp_1
  - exists_false._simp_1
  - funext
  - iff_self

### View C
  - SimpleGraph.sum_adj
  - Sum.inr.injEq
  - exists_false._simp_1
  - Set.mem_image._simp_1
  - SimpleGraph.mem_neighborSet._simp_1
  - iff_self

### View D
  1. SimpleGraph.sum_adj
  2. Sum.inr.injEq
  3. exists_false._simp_1
  4. Set.mem_image._simp_1
  5. SimpleGraph.mem_neighborSet._simp_1
  6. iff_self
  7. noConfusion_of_Nat
  8. of_eq_true
  9. and_false
  10. eq_false'

### View E
  (none)