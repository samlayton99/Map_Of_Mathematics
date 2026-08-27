# Proof 24

Theorem `Equiv.Perm.cycleOf_mul_of_apply_right_eq_self` (Mathlib source below).

```lean
theorem cycleOf_mul_of_apply_right_eq_self [DecidableRel f.SameCycle]
    [DecidableRel (f * g).SameCycle]
    (h : Commute f g) (x : α) (hx : g x = x) : (f * g).cycleOf x = f.cycleOf x := by
  ext y
  by_cases hxy : (f * g).SameCycle x y
  · obtain ⟨z, rfl⟩ := hxy
    rw [cycleOf_apply_apply_zpow_self]
    simp [h.mul_zpow, zpow_apply_eq_self_of_apply_eq_self hx]
  · rw [cycleOf_apply_of_not_sameCycle hxy, cycleOf_apply_of_not_sameCycle]
    contrapose hxy
    obtain ⟨z, rfl⟩ := hxy
    refine ⟨z, ?_⟩
    simp [h.mul_zpow, zpow_apply_eq_self_of_apply_eq_self hx]

```

## Candidate views (anonymized)

### View A
  1. Equiv.Perm.zpow_apply_eq_self_of_apply_eq_self
  2. Equiv.Perm.cycleOf_apply_of_not_sameCycle
  3. Equiv.Perm.cycleOf_apply_apply_zpow_self

### View B
  1. Equiv.Perm.ext
  2. Equiv.Perm.cycleOf_apply_of_not_sameCycle
  3. congrArg
  4. congr
  5. of_eq_true
  6. congrFun'
  7. Commute.mul_zpow
  8. Equiv.Perm.zpow_apply_eq_self_of_apply_eq_self
  9. eq_self
  10. Eq.trans

### View C
  - Equiv.Perm.cycleOf_apply_apply_zpow_self
  - Equiv.Perm.cycleOf_apply_of_not_sameCycle
  - Equiv.Perm.zpow_apply_eq_self_of_apply_eq_self
  - Commute.mul_zpow
  - Equiv.Perm.ext
  - of_eq_true

### View D
  - Commute.mul_zpow
  - Eq.trans
  - Equiv.Perm.cycleOf_apply_apply_zpow_self
  - Equiv.Perm.cycleOf_apply_of_not_sameCycle
  - Equiv.Perm.ext
  - Equiv.Perm.zpow_apply_eq_self_of_apply_eq_self
  - Exists.casesOn
  - Mathlib.Tactic.Contrapose.contrapose₄
  - congr
  - congrArg
  - congrFun'
  - eq_self
  - of_eq_true

### View E
  1. Equiv.Perm.cycleOf_apply_apply_zpow_self
  2. Equiv.Perm.cycleOf_apply_of_not_sameCycle
  3. Equiv.Perm.zpow_apply_eq_self_of_apply_eq_self
  4. Commute.mul_zpow
  5. Equiv.Perm.ext
  6. of_eq_true
  7. eq_self
  8. Mathlib.Tactic.Contrapose.contrapose₄
  9. congrArg
  10. congr