# Nat.Coprime.mul_add_mul_ne_mul

*file:* `Mathlib/Data/Nat/GCD/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 10925 nodes

## Statement and source  [lean-exact]

```lean
theorem Coprime.mul_add_mul_ne_mul {m n a b : ℕ} (cop : Coprime m n) (ha : a ≠ 0) (hb : b ≠ 0) :
    a * m + b * n ≠ m * n := by
  intro h
  obtain ⟨x, rfl⟩ : n ∣ a :=
    cop.symm.dvd_of_dvd_mul_right
      ((Nat.dvd_add_iff_left (Nat.dvd_mul_left n b)).mpr
        ((congr_arg _ h).mpr (Nat.dvd_mul_left n m)))
  obtain ⟨y, rfl⟩ : m ∣ b :=
    cop.dvd_of_dvd_mul_right
      ((Nat.dvd_add_iff_right (Nat.dvd_mul_left m (n * x))).mpr
        ((congr_arg _ h).mpr (Nat.dvd_mul_right m n)))
  rw [mul_comm, mul_ne_zero_iff, ← one_le_iff_ne_zero] at ha hb
  refine mul_ne_zero hb.2 ha.2 (eq_zero_of_mul_eq_self_left (ne_of_gt (add_le_add ha.1 hb.1)) ?_)
  rw [← mul_assoc, ← h, Nat.add_mul, Nat.add_mul, mul_comm _ n, ← mul_assoc, mul_comm y]
```

Exact proof reference: record decl `d5` in `studies/Data_Nat_GCD_Basic.study.json` (type `x395`, value `x1080`).

## P2 — support set (body)  [deterministic-derived]

**Domain (21):** `Nat`, `Nat.Coprime`, `Ne`, `Eq`, `False`, `Nat.Coprime.dvd_of_dvd_mul_right`, `Nat.Coprime.symm`, `Nat.dvd_add_iff_left`, `Nat.dvd_mul_left`, `Nat.dvd_add_iff_right`, `Nat.dvd_mul_right`, `mul_ne_zero`, `And`, `Nat.one_le_iff_ne_zero`, `mul_ne_zero_iff`, `mul_comm`, `eq_zero_of_mul_eq_self_left`, `ne_of_gt`, `Nat.add_le_add`, `mul_assoc`, `Nat.add_mul`

**Classified infrastructure (44):** `OfNat.ofNat` (structure-projection), `instOfNatNat` (typeclass-instance), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `instAddNat` (typeclass-instance), `HMul.hMul` (structure-projection), `instHMul` (typeclass-instance), `instMulNat` (typeclass-instance), `Exists.casesOn` (generated), `Dvd.dvd` (structure-projection), `Nat.instDvd` (typeclass-instance), `Iff.mpr` (logic-core,structure-projection), `Eq.mpr` (eq-machinery), `congr_arg` (eq-machinery), `Eq.ndrec` (eq-machinery,generated), `MulZeroClass.toZero` (structure-projection,typeclass-instance), `Nat.instMulZeroClass` (typeclass-instance), `IsRightCancelMulZero.to_noZeroDivisors` (typeclass-instance), `IsCancelMulZero.toIsRightCancelMulZero` (structure-projection,typeclass-instance), `MulZeroClass.toMul` (structure-projection,typeclass-instance), `Nat.instIsCancelMulZero` (typeclass-instance), `And.right` (logic-core,structure-projection), `LE.le` (structure-projection), `instLENat` (typeclass-instance), `Zero.toOfNat0` (typeclass-instance), `Eq.mp` (eq-machinery), `congrArg` (eq-machinery), `Eq.symm` (eq-machinery), `propext` (eq-machinery), `CommMagma.toMul` (structure-projection,typeclass-instance), `CommSemigroup.toCommMagma` (typeclass-instance), `Nat.instCommSemigroup` (typeclass-instance), `Nat.instMulZeroOneClass` (typeclass-instance), `MulZeroOneClass.toMulZeroClass` (typeclass-instance), `Nat.instPreorder` (typeclass-instance), `One.toOfNat1` (typeclass-instance), `MulOne.toOne` (structure-projection,typeclass-instance), `MulOneClass.toMulOne` (structure-projection,typeclass-instance), `MulZeroOneClass.toMulOneClass` (structure-projection,typeclass-instance), `And.left` (logic-core,structure-projection), `Semigroup.toMul` (structure-projection,typeclass-instance), `Nat.instSemigroup` (typeclass-instance), `id` (eq-machinery), `Eq.refl` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Nat` (0 args)
- `Nat` (0 args)
- `Nat` (0 args)
- `Nat` (0 args)
- `Nat.Coprime` (2 args) : <sort>
- `Ne` (3 args) : <sort>
  - `Nat` (0 args)
  - `OfNat.ofNat` (3 args) : Nat
    - `Nat` (0 args)
    - `instOfNatNat` (1 args) : OfNat
- `Ne` (3 args) : <sort>
  - `Nat` (0 args)
  - `OfNat.ofNat` (3 args) : Nat
    - `Nat` (0 args)
    - `instOfNatNat` (1 args) : OfNat
- `Eq` (3 args) : <sort>
  - `Nat` (0 args)
  - `HAdd.hAdd` (6 args) : Nat
    - `Nat` (0 args)
    - `Nat` (0 args)
    - `Nat` (0 args)
    - `instHAdd` (2 args) : HAdd
      - `Nat` (0 args)
      - `instAddNat` (0 args)
    - `HMul.hMul` (6 args) : Nat
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `Nat` (0 args)
      - `instHMul` (2 args) : HMul
        - `Nat` (0 args)
  ... (4472 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `Nat.Coprime.dvd_of_dvd_mul_right` (5 args) : Dvd.dvd (depth 1)
- `Nat.Coprime.symm` (3 args) : Nat.Coprime (depth 2)
- `Nat.dvd_add_iff_left` (4 args) : Iff (depth 3)
- `Nat.dvd_mul_left` (2 args) : Dvd.dvd (depth 4)
- `Nat.Coprime.dvd_of_dvd_mul_right` (5 args) : Dvd.dvd (depth 3)
- `Nat.dvd_add_iff_right` (4 args) : Iff (depth 5)
- `Nat.dvd_mul_left` (2 args) : Dvd.dvd (depth 6)
- `Nat.dvd_mul_right` (2 args) : Dvd.dvd (depth 6)
- `mul_ne_zero` (9 args) : False (depth 4)
- `Nat.one_le_iff_ne_zero` (1 args) : Iff (depth 10)
- `mul_ne_zero_iff` (5 args) : Iff (depth 10)
- `mul_comm` (4 args) : Eq (depth 10)
- `eq_zero_of_mul_eq_self_left` (7 args) : Eq (depth 5)
- `ne_of_gt` (5 args) : Ne (depth 6)
- `Nat.add_le_add` (6 args) : LE.le (depth 7)
- `Nat.one_le_iff_ne_zero` (1 args) : Iff (depth 13)
- `mul_ne_zero_iff` (5 args) : Iff (depth 13)
- `mul_comm` (4 args) : Eq (depth 13)
- `mul_assoc` (5 args) : Eq (depth 10)
- `Nat.add_mul` (3 args) : Eq (depth 11)
- `Nat.add_mul` (3 args) : Eq (depth 12)
- `mul_assoc` (5 args) : Eq (depth 15)
- `mul_comm` (4 args) : Eq (depth 15)
  ... (31 occurrences total)

## P5 — source-level use events  [observed]

- `rewrite` → `mul_comm`, `mul_comm`, `mul_ne_zero_iff`, `mul_ne_zero_iff`, `Nat.one_le_iff_ne_zero`, `Nat.one_le_iff_ne_zero` — `rewrite  [ mul_comm, mul_ne_zero_iff, ← one_le_iff_ne_zero ] at ha hb`
- `rewrite` → `mul_assoc`, `Nat.add_mul`, `Nat.add_mul`, `mul_comm`, `mul_assoc`, `mul_comm` — `rewrite  [ ← mul_assoc, ← h, Nat.add_mul, Nat.add_mul, mul_comm _ n, ← mul_assoc`
- `refine` → `mul_ne_zero` — `refine mul_ne_zero hb.2 ha.2 (eq_zero_of_mul_eq_self_left (ne_of_gt (add_le_add `

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Nat` — inductive, module `Init.Prelude`
- `Nat.Coprime` — def, module `Init.Data.Nat.Coprime`
- `Ne` — def, module `Init.Core`
- `Eq` — inductive, module `Init.Prelude`
- `False` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
