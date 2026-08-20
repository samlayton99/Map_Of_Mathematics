# Proof 23

Theorem `Finset.le_prod_nonempty_of_submultiplicative_on_pred` (Mathlib source below).

```lean
theorem le_prod_nonempty_of_submultiplicative_on_pred [IsOrderedMonoid N] (f : M → N) (p : M → Prop)
    (h_mul : ∀ x y, p x → p y → f (x * y) ≤ f x * f y) (hp_mul : ∀ x y, p x → p y → p (x * y))
    (g : ι → M) (s : Finset ι) (hs_nonempty : s.Nonempty) (hs : ∀ i ∈ s, p (g i)) :
    f (∏ i ∈ s, g i) ≤ ∏ i ∈ s, f (g i) := by
  refine le_trans
    (Multiset.le_prod_nonempty_of_submultiplicative_on_pred f p h_mul hp_mul _ ?_ ?_) ?_
  · simp [hs_nonempty.ne_empty]
  · exact Multiset.forall_mem_map_iff.mpr hs
  simp

```

## Candidate views (anonymized)

### View A
  - Finset.Nonempty.ne_empty
  - Finset.val_eq_zero._simp_1
  - Multiset.map_eq_zero._simp_1
  - Multiset.forall_mem_map_iff
  - Multiset.le_prod_nonempty_of_submultiplicative_on_pred
      . Multiset.coe_eq_zero._simp_1
      . List.le_prod_nonempty_of_submultiplicative_on_pred
      . Quotient.inductionOn
      . congrArg
  - Multiset.map_congr

### View B
  1. le_trans
  2. Iff.mpr
  3. congrArg
  4. Std.le_refl._simp_1
  5. Multiset.map_eq_zero._simp_1
  6. Finset.val_eq_zero._simp_1
  7. of_eq_true
  8. Finset.Nonempty.ne_empty
  9. Multiset.le_prod_nonempty_of_submultiplicative_on_pred
  10. congrFun'

### View C
  (none)

### View D
  - Eq.trans
  - Finset.Nonempty.ne_empty
  - Finset.val_eq_zero._simp_1
  - Iff.mpr
  - Multiset.forall_mem_map_iff
  - Multiset.le_prod_nonempty_of_submultiplicative_on_pred
  - Multiset.map_congr
  - Multiset.map_eq_zero._simp_1
  - Multiset.map_map
  - Std.le_refl._simp_1
  - congrArg
  - congrFun'
  - eq_false
  - le_trans

### View E
  1. Finset.Nonempty.ne_empty
  2. Finset.val_eq_zero._simp_1
  3. Multiset.map_eq_zero._simp_1
  4. Multiset.forall_mem_map_iff
  5. Multiset.le_prod_nonempty_of_submultiplicative_on_pred
  6. Multiset.map_congr
  7. Multiset.map_map
  8. Std.le_refl._simp_1
  9. of_eq_true
  10. not_false_eq_true