# Real.one_sub_inv_le_log_of_pos

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* term · *proof-term size:* 1553 nodes

## Statement and source  [lean-exact]

```lean
lemma one_sub_inv_le_log_of_pos (hx : 0 < x) : 1 - x⁻¹ ≤ log x := by
  simpa [add_comm] using log_le_sub_one_of_pos (inv_pos.2 hx)
```

Exact proof reference: record decl `d122` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x17638`, value `x17746`).

## P2 — support set (body)  [deterministic-derived]

**Domain (8):** `Real`, `Real.log`, `Eq`, `add_comm`, `congrFun'`, `Real.log_inv`, `Real.log_le_sub_one_of_pos`, `inv_pos`

**Classified infrastructure (67):** `LT.lt` (structure-projection), `Real.instLT` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `Eq.mpr` (eq-machinery), `LE.le` (structure-projection), `Real.instLE` (typeclass-instance), `HSub.hSub` (structure-projection), `instHSub` (typeclass-instance), `Real.instSub` (typeclass-instance), `One.toOfNat1` (typeclass-instance), `Real.instOne` (typeclass-instance), `Inv.inv` (structure-projection), `Real.instInv` (typeclass-instance), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `AddCommMagma.toAdd` (structure-projection,typeclass-instance), `AddCommSemigroup.toAddCommMagma` (typeclass-instance), `Real.instAddCommSemigroup` (typeclass-instance), `id` (eq-machinery), `Eq.trans` (eq-machinery), `Real.instAdd` (typeclass-instance), `tsub_le_iff_right._simp_1` (internal-detail), `AddGroup.toOrderedSub` (typeclass-instance), `Real.instAddGroup` (typeclass-instance), `covariant_swap_add_of_covariant_add` (typeclass-instance), `IsOrderedAddMonoid.toAddLeftMono` (typeclass-instance), `Real.instAddCommMonoid` (typeclass-instance), `Real.instPreorder` (typeclass-instance), `Real.instIsOrderedAddMonoid` (typeclass-instance), `congrArg` (eq-machinery), `Eq.mp` (eq-machinery), `InvOneClass.toInv` (structure-projection,typeclass-instance), `DivInvOneMonoid.toInvOneClass` (typeclass-instance), `DivisionMonoid.toDivInvOneMonoid` (typeclass-instance), `GroupWithZero.toDivisionMonoid` (typeclass-instance), `DivisionSemiring.toGroupWithZero` (typeclass-instance), `Semifield.toDivisionSemiring` (typeclass-instance), `Field.toSemifield` (typeclass-instance), `Real.instField` (typeclass-instance), `AddZero.toAdd` (structure-projection,typeclass-instance), `AddZeroClass.toAddZero` (structure-projection,typeclass-instance), `AddMonoid.toAddZeroClass` (typeclass-instance), `SubNegMonoid.toAddMonoid` (structure-projection,typeclass-instance), `AddGroup.toSubNegMonoid` (structure-projection,typeclass-instance), `AddCommGroup.toAddGroup` (structure-projection,typeclass-instance), `Real.instAddCommGroup` (typeclass-instance), `Neg.neg` (structure-projection), `Real.instNeg` (typeclass-instance), `neg_le_sub_iff_le_add._simp_1` (internal-detail), `Iff.mpr` (logic-core,structure-projection), `Preorder.toLT` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `Real.partialOrder` (typeclass-instance), `MulZeroClass.toZero` (structure-projection,typeclass-instance), `MulZeroOneClass.toMulZeroClass` (typeclass-instance), `MonoidWithZero.toMulZeroOneClass` (typeclass-instance), `GroupWithZero.toMonoidWithZero` (structure-projection,typeclass-instance), `PosMulReflectLE.toPosMulReflectLT` (typeclass-instance), `instMulZeroClassOfSemiring` (typeclass-instance), `Real.semiring` (typeclass-instance), `PosMulStrictMono.toPosMulReflectLE` (typeclass-instance), `MulZeroClass.toMul` (structure-projection,typeclass-instance), `Real.linearOrder` (typeclass-instance), `IsStrictOrderedRing.toPosMulStrictMono` (structure-projection,typeclass-instance), `Real.instIsStrictOrderedRing` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `LT.lt` (4 args) : <sort>
  - `Real` (0 args)
  - `Real.instLT` (0 args)
  - `OfNat.ofNat` (3 args) : Real
    - `Real` (0 args)
    - `Zero.toOfNat0` (2 args) : OfNat
      - `Real` (0 args)
      - `Real.instZero` (0 args)
- `Eq.mpr` (4 args) : LE.le [Prop]
  - `LE.le` (4 args) : <sort>
    - `Real` (0 args)
    - `Real.instLE` (0 args)
    - `HSub.hSub` (6 args) : Real
      - `Real` (0 args)
      - `Real` (0 args)
      - `Real` (0 args)
      - `instHSub` (2 args) : HSub
        - `Real` (0 args)
        - `Real.instSub` (0 args)
      - `OfNat.ofNat` (3 args) : Real
        - `Real` (0 args)
        - `One.toOfNat1` (2 args) : OfNat
          - `Real` (0 args)
          - `Real.instOne` (0 args)
      - `Inv.inv` (3 args) : Real
        - `Real` (0 args)
        - `Real.instInv` (0 args)
    - `Real.log` (1 args) : Real
  - `LE.le` (4 args) : <sort>
  ... (704 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `add_comm` (4 args) : Eq (depth 4)
- `congrFun'` (6 args) : Eq (depth 3)
- `Real.log_inv` (1 args) : Eq (depth 5)
- `Real.log_le_sub_one_of_pos` (2 args) : LE.le (depth 2)
- `inv_pos` (5 args) : Iff (depth 4)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `Real.log` — def, module `Basic`
- `Eq` — inductive, module `Init.Prelude`
- `add_comm` — axiom, module `Mathlib.Algebra.Group.Defs`
- `congrFun'` — axiom, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
