# Proof 20

Theorem `Pell.modEq_of_xn_modEq` (Mathlib source below).

```lean
theorem modEq_of_xn_modEq {i j n} (ipos : 0 < i) (hin : i ≤ n)
    (h : xn a1 j ≡ xn a1 i [MOD xn a1 n]) :
    j ≡ i [MOD 4 * n] ∨ j + i ≡ 0 [MOD 4 * n] :=
  let j' := j % (4 * n)
  have n4 : 0 < 4 * n := mul_pos (by decide) (ipos.trans_le hin)
  have jl : j' < 4 * n := Nat.mod_lt _ n4
  have jj : j ≡ j' [MOD 4 * n] := by delta ModEq; rw [Nat.mod_eq_of_lt jl]
  have : ∀ j q, xn a1 (j + 4 * n * q) ≡ xn a1 j [MOD xn a1 n] := by
    intro j q; induction q with
    | zero => simp [ModEq.refl]
    | succ q IH =>
      rw [Nat.mul_succ, ← add_assoc, add_comm]
      exact (xn_modEq_x4n_add _ _ _).trans IH
  Or.imp (fun ji : j' = i => by rwa [← ji])
    (fun ji : j' + i = 4 * n =>
      (jj.add_right _).trans <| by
        rw [ji]
        exact dvd_rfl.modEq_zero_nat)
    (eq_of_xn_modEq' a1 ipos hin jl.le <|
      (h.symm.trans <| by
          rw [← Nat.mod_add_div j (4 * n)]
          exact this j' _).symm)

```

## Candidate views (anonymized)

### View A
  1. Nat.mul_succ
  2. Nat.ModEq.refl
  3. mul_pos
  4. dvd_rfl
  5. add_comm
  6. add_assoc
  7. Pell.xn_modEq_x4n_add
  8. Pell.eq_of_xn_modEq'
  9. Or.imp
  10. Nat.mod_lt

### View B
  - Pell.eq_of_xn_modEq'
      . Pell.eq_of_xn_modEq
      . Pell.xn_modEq_x4n_sub
      . _private.Mathlib.NumberTheory.PellMatiyasevic.0.Pell.eq_of_xn_modEq'._proof_1_3
      . _private.Mathlib.NumberTheory.PellMatiyasevic.0.Pell.eq_of_xn_modEq'._proof_1_2
  - Pell.xn_modEq_x4n_add
      . Pell.xn_modEq_x2n_add
      . Nat.ModEq.add_right_cancel'
      . Nat.ModEq.trans
      . Nat.ModEq.symm
  - Nat.ModEq.add_right
  - Dvd.dvd.modEq_zero_nat
  - Nat.mod_add_div
  - Nat.mod_eq_of_lt

### View C
  1. _private.Mathlib.NumberTheory.PellMatiyasevic.0.Pell.eq_of_xn_modEq'._proof_1_3
  2. Pell.xn_modEq_x2n_sub_lem
  3. _private.Mathlib.NumberTheory.PellMatiyasevic.0.Pell.eq_of_xn_modEq'._proof_1_2
  4. Nat.ToInt.toNat_nonneg
  5. Int.Internal.Linear.le_norm_expr
  6. Pell.xn_modEq_x4n_add
  7. Int.Internal.Linear.eq_of_le_ge
  8. Int.Internal.Linear.eq_of_core
  9. Int.Internal.Linear.eq_def
  10. Int.Internal.Linear.le_combine

### View D
  1. Or.imp
  2. congrArg
  3. Nat.ModEq.trans
  4. LT.lt.trans_le
  5. Nat.mul_succ
  6. Nat.mod_add_div
  7. Eq.symm
  8. Nat.mod_eq_of_lt
  9. Pell.eq_of_xn_modEq'
  10. add_comm

### View E
  - Dvd.dvd.modEq_zero_nat
  - Eq.symm
  - Eq.trans
  - LT.lt.le
  - LT.lt.trans_le
  - MulZeroClass.mul_zero
  - Nat.ModEq.add_right
  - Nat.ModEq.symm
  - Nat.ModEq.trans
  - Nat.mod_add_div
  - Nat.mod_eq_of_lt
  - Nat.mod_lt
  - Nat.mul_succ
  - Or.imp