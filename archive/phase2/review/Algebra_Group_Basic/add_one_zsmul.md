# add_one_zsmul

*file:* `Mathlib/Algebra/Group/Basic.lean` · *style (derived):* term · *proof-term size:* 11877 nodes

## Statement and source  [lean-exact]

```lean
@[to_additive add_one_zsmul]
```

Exact proof reference: record decl `d79` in `studies/Algebra_Group_Basic.study.json` (type `x5124`, value `x5594`).

## P2 — support set (body)  [deterministic-derived]

**Domain (27):** `AddGroup`, `Int`, `Eq`, `Nat`, `of_eq_true`, `Nat.cast`, `True`, `Nat.succ`, `natCast_zsmul`, `succ_nsmul`, `congrFun'`, `eq_self`, `Unit`, `Int.add_left_neg`, `ofNat_zsmul`, `zero_nsmul`, `neg_zsmul`, `one_nsmul`, `neg_add_cancel`, `Int.negSucc`, `negSucc_zsmul`, `succ_nsmul'`, `neg_add_rev`, `neg_add_cancel_right`, `Int.negSucc_eq`, `Int.neg_add`, `Int.neg_add_cancel_right`

**Classified infrastructure (35):** `_private.Basic.0.add_one_zsmul.match_1` (internal-detail,generated), `HSMul.hSMul` (structure-projection), `instHSMul` (typeclass-instance), `ZSMul.toSMul` (typeclass-instance), `SubNegMonoid.toZSMul` (structure-projection,typeclass-instance), `AddGroup.toSubNegMonoid` (structure-projection,typeclass-instance), `HAdd.hAdd` (structure-projection), `instHAdd` (typeclass-instance), `Int.instAdd` (typeclass-instance), `OfNat.ofNat` (structure-projection), `instOfNat` (typeclass-instance), `AddZero.toAdd` (structure-projection,typeclass-instance), `AddZeroClass.toAddZero` (structure-projection,typeclass-instance), `AddMonoid.toAddZeroClass` (typeclass-instance), `SubNegMonoid.toAddMonoid` (structure-projection,typeclass-instance), `instNatCastInt` (typeclass-instance), `Eq.trans` (eq-machinery), `NSMul.toSMul` (typeclass-instance), `AddMonoid.toNSMul` (structure-projection,typeclass-instance), `congr` (eq-machinery), `congrArg` (eq-machinery), `Neg.neg` (structure-projection), `Int.instNegInt` (typeclass-instance), `Zero.toOfNat0` (typeclass-instance), `AddZero.toZero` (structure-projection,typeclass-instance), `instOfNatNat` (typeclass-instance), `NegZeroClass.toNeg` (structure-projection,typeclass-instance), `SubNegZeroMonoid.toNegZeroClass` (typeclass-instance), `SubtractionMonoid.toSubNegZeroMonoid` (typeclass-instance), `AddGroup.toSubtractionMonoid` (typeclass-instance), `SubtractionMonoid.toSubNegMonoid` (structure-projection,typeclass-instance), `Eq.mpr` (eq-machinery), `instAddNat` (typeclass-instance), `SubNegMonoid.toNeg` (structure-projection,typeclass-instance), `id` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `AddGroup` (1 args) : <sort>
- `Int` (0 args)
- `_private.Basic.0.add_one_zsmul.match_1` (5 args) : Eq [Prop]
  - `Int` (0 args)
  - `Eq` (3 args) : <sort>
    - `HSMul.hSMul` (6 args) : <local>
      - `Int` (0 args)
      - `instHSMul` (3 args) : HSMul
        - `Int` (0 args)
        - `ZSMul.toSMul` (2 args) : SMul
          - `SubNegMonoid.toZSMul` (2 args) : ZSMul
            - `AddGroup.toSubNegMonoid` (2 args) : SubNegMonoid
      - `HAdd.hAdd` (6 args) : Int
        - `Int` (0 args)
        - `Int` (0 args)
        - `Int` (0 args)
        - `instHAdd` (2 args) : HAdd
          - `Int` (0 args)
          - `Int.instAdd` (0 args)
        - `OfNat.ofNat` (3 args) : Int
          - `Int` (0 args)
          - `instOfNat` (1 args) : OfNat
    - `HAdd.hAdd` (6 args) : <local>
      - `instHAdd` (2 args) : HAdd
        - `AddZero.toAdd` (2 args) : Add
          - `AddZeroClass.toAddZero` (2 args) : AddZero
            - `AddMonoid.toAddZeroClass` (2 args) : AddZeroClass
              - `SubNegMonoid.toAddMonoid` (2 args) : AddMonoid
                - `AddGroup.toSubNegMonoid` (2 args) : SubNegMonoid
      - `HSMul.hSMul` (6 args) : <local>
  ... (3415 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `of_eq_true` (2 args) : Eq (depth 1)
- `natCast_zsmul` (4 args) : Eq (depth 6)
- `succ_nsmul` (4 args) : Eq (depth 6)
- `congrFun'` (6 args) : Eq (depth 4)
- `eq_self` (2 args) : Eq (depth 3)
- `Int.add_left_neg` (1 args) : Eq (depth 8)
- `ofNat_zsmul` (4 args) : Eq (depth 7)
- `zero_nsmul` (3 args) : Eq (depth 6)
- `congrFun'` (6 args) : Eq (depth 5)
- `neg_zsmul` (4 args) : Eq (depth 8)
- `ofNat_zsmul` (4 args) : Eq (depth 10)
- `one_nsmul` (3 args) : Eq (depth 10)
- `neg_add_cancel` (3 args) : Eq (depth 5)
- `negSucc_zsmul` (4 args) : Eq (depth 4)
- `succ_nsmul'` (4 args) : Eq (depth 5)
- `neg_add_rev` (4 args) : Eq (depth 6)
- `neg_add_cancel_right` (4 args) : Eq (depth 7)
- `Int.negSucc_eq` (1 args) : Eq (depth 8)
- `Int.neg_add` (2 args) : Eq (depth 9)
- `Int.neg_add_cancel_right` (2 args) : Eq (depth 10)
- `negSucc_zsmul` (4 args) : Eq (depth 8)

## P5 — source-level use events  [observed]

(term-mode proof: no tactic events)

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `AddGroup` — inductive, module `Mathlib.Algebra.Group.Defs`
- `Int` — inductive, module `Init.Data.Int.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Nat` — inductive, module `Init.Prelude`
- `of_eq_true` — axiom, module `Init.SimpLemmas`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
