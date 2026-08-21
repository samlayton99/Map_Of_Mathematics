# Grading batch `testr_10` — 24 proofs

You are one of three independent raters. You will never see any
ranking our system produces and must not try to guess one. Your
grades are the ground truth those rankings are scored against.
Do not look at any other file in this repository.

## Stage 1 — say what the proof does, BEFORE judging the list

For each proof, first write `moves`: in your own words, one or two sentences,
what the key mathematical steps of this proof are. Write this from the theorem
statement and your own understanding.

Do this before you weigh the candidate list. If the real content of the proof
is something no citation could name -- a case split, exhibiting a witness,
manipulating a local hypothesis, pure rewriting -- say so plainly. That is a
genuine measurement, not a failure.

## Stage 2 — grade every candidate 0-4

Grade **every** candidate. Do not pick a top few. The grade is about THIS
proof, not about the declaration in general.

| grade | name | meaning |
|---|---|---|
| **4** | `CORE` | A core move. If asked "how does this proof go?", you would name it. |
| **3** | `MAJOR` | Real mathematical content, genuinely used, but secondary. |
| **2** | `LEGIT_GLUE` | Logical or structural plumbing that **is genuinely the content of this proof**. Near the foundations, assembling equalities really can be the whole argument. |
| **1** | `BAD_GLUE` | Plumbing or background that carries no idea here. A person explaining the proof would never mention it. |
| **0** | `JUNK` | Irrelevant machinery: automation residue, instance/typeclass resolution, universe or decidability bookkeeping, notation unfolding. |

The 2-versus-1 line is the important one. **Do not grade something 1 just
because it looks like plumbing.** Ask whether a mathematician explaining *this
specific theorem* would mention it. If yes, it is 2 even if its name looks
like machinery. If the theorem is a deep result and the item is `Eq.mpr`,
that is 1.

Candidates are in RANDOM order. Position means nothing. `depth` is context so
you can tell a deep theorem from a primitive -- it is NOT a hint, and you must
not grade something high merely because it is deep.

## Output format

Return **only** a JSON object, no commentary:

```json
{
  "proof_0007": {
    "moves": "Rewrites along commutativity of addition, then closes by reflexivity.",
    "grades": {"1": 1, "2": 4, "3": 0, "4": 3, "5": 2},
    "missing_key": false,
    "confidence": "high"
  }
}
```

Every proof id in your batch must appear exactly once, and every candidate
number of that proof must appear exactly once in its `grades` map.


---

### proof_0217  (target depth 30, band 26-50)

THEOREM PROVED: `AffineEquiv.toEquiv_symm`

Grade all 12 candidates.

   1. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `AffineEquiv.symm`
      [def, depth 29, in-statement, role explicit-arg]
   3. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   5. `AddTorsor`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   7. `AffineEquiv.toEquiv`
      [def, depth 7, in-statement, role implicit-arg]
   8. `AffineEquiv`
      [inductive, depth 6, in-statement, role type-annotation]
   9. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `rfl`
      [def, depth 2, in-statement, role applied]
  11. `AddCommGroup.toAddGroup`
      [def, depth 1, in-statement, role instance-slot]
  12. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0218  (target depth 46, band 26-50)

THEOREM PROVED: `SeminormedSpace.Core.norm_triangle`

Grade all 10 candidates.

   1. `Norm`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   4. `SeminormedSpace.Core`
      [inductive, depth 45, in-statement, role type-annotation]
   5. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `NormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   8. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
   9. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
  10. `NormedField.toField`
      [def, depth 1, in-statement, role instance-slot]

### proof_0219  (target depth 40, band 26-50)

THEOREM PROVED: `CochainComplex.cm5b.I_X`

Grade all 21 candidates.

   1. `AddRightCancelMonoid.toAddRightCancelSemigroup`
      [def, depth 3, in-statement, role instance-slot]
   2. `CochainComplex`
      [def, depth 8, in-statement, role type-annotation]
   3. `HomologicalComplex.X`
      [def, depth 3, in-statement, role explicit-arg]
   4. `CochainComplex.cm5b.I`
      [def, depth 39, in-statement, role explicit-arg]
   5. `AddGroup.toAddCancelMonoid`
      [def, depth 12, in-statement, role instance-slot]
   6. `CategoryTheory.Abelian.toPreadditive`
      [def, depth 2, in-statement, role instance-slot]
   7. `ComplexShape.up`
      [def, depth 7, in-statement, role implicit-arg]
   8. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  10. `CategoryTheory.EnoughInjectives`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Int.instRing`
      [def, depth 37, in-statement, role instance-slot]
  12. `AddMonoidWithOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
  13. `Ring.toAddGroupWithOne`
      [def, depth 10, in-statement, role instance-slot]
  14. `AddRightCancelSemigroup.toAddSemigroup`
      [def, depth 1, in-statement, role instance-slot]
  15. `Int.instAddGroup`
      [def, depth 30, in-statement, role instance-slot]
  16. `AddGroupWithOne.toAddMonoidWithOne`
      [def, depth 1, in-statement, role instance-slot]
  17. `AddCancelMonoid.toAddRightCancelMonoid`
      [def, depth 3, in-statement, role instance-slot]
  18. `Int`
      [inductive, depth 0, in-statement, role explicit-arg]
  19. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`
      [def, depth 17, in-statement, role instance-slot]
  20. `AddSemigroup.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  21. `CategoryTheory.Abelian`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0220  (target depth 44, band 26-50)

THEOREM PROVED: `nnratCast_smul_eq`

Grade all 12 candidates.

   1. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   2. `AddMonoidHom`
      [inductive, depth 1, introduced-by-proof, role implicit-arg]
   3. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   4. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `AddCommMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
   7. `AddMonoidHom.instFunLike`
      [def, depth 10, introduced-by-proof, role instance-slot]
   8. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   9. `NNRat`
      [def, depth 39, in-statement, role type-annotation]
  10. `AddMonoidHom.id`
      [def, depth 5, introduced-by-proof, role explicit-arg]
  11. `DivisionSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `map_nnratCast_smul`
      [theorem, depth 43, introduced-by-proof, role applied]

### proof_0221  (target depth 30, band 26-50)

THEOREM PROVED: `CategoryTheory.Sieve.functorPullback_functorPushforward_overForget`

Grade all 25 candidates.

   1. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
   2. `CategoryTheory.Sieve.functorPullback_apply`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   3. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `CategoryTheory.Sieve.functorPushforward_apply`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Sieve.functorPushforward`
      [def, depth 6, in-statement, role explicit-arg]
   6. `CategoryTheory.Presieve.map`
      [inductive, depth 3, introduced-by-proof, role explicit-arg]
   7. `CategoryTheory.Presieve.functorPullback_map_overForget`
      [theorem, depth 29, introduced-by-proof, role explicit-arg]
   8. `CategoryTheory.Over`
      [def, depth 24, in-statement, role implicit-arg]
   9. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  10. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  11. `CategoryTheory.Sieve.functorPullback`
      [def, depth 6, in-statement, role explicit-arg]
  12. `CategoryTheory.Presieve.functorPushforward`
      [def, depth 3, in-statement, role implicit-arg]
  13. `CategoryTheory.Sieve.arrows_ext`
      [theorem, depth 6, introduced-by-proof, role applied]
  14. `CategoryTheory.Sieve`
      [inductive, depth 1, in-statement, role type-annotation]
  15. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `CategoryTheory.Sieve.arrows`
      [def, depth 2, in-statement, role explicit-arg]
  17. `CategoryTheory.Sieve.functorPushforward_overForget_arrows`
      [theorem, depth 28, introduced-by-proof, role explicit-arg]
  18. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  19. `CategoryTheory.instCategoryOver`
      [def, depth 26, in-statement, role instance-slot]
  20. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `CategoryTheory.Presieve`
      [def, depth 2, in-statement, role implicit-arg]
  22. `CategoryTheory.Presieve.functorPullback`
      [def, depth 3, in-statement, role implicit-arg]
  23. `CategoryTheory.Over.forget`
      [def, depth 23, in-statement, role explicit-arg]
  24. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  25. `True`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0222  (target depth 33, band 26-50)

THEOREM PROVED: `Nat.modEq_three_digits_sum`

Grade all 7 candidates.

   1. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   2. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `Nat.modEq_digits_sum`
      [theorem, depth 32, introduced-by-proof, role applied]
   4. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   6. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]

### proof_0223  (target depth 39, band 26-50)

THEOREM PROVED: `Action.preservesLimits_forget`

Grade all 18 candidates.

   1. `Action.forget`
      [def, depth 19, in-statement, role implicit-arg]
   2. `CategoryTheory.Functor.category`
      [def, depth 19, introduced-by-proof, role instance-slot]
   3. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `CategoryTheory.Functor.comp`
      [def, depth 15, introduced-by-proof, role implicit-arg]
   5. `CategoryTheory.Functor.obj`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   6. `CategoryTheory.Limits.HasLimits`
      [def, depth 2, in-statement, role type-annotation]
   7. `CategoryTheory.Equivalence.functor`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   8. `CategoryTheory.Limits.preservesLimits_of_natIso`
      [theorem, depth 38, introduced-by-proof, role applied]
   9. `PUnit.unit`
      [constructor, depth 1, in-statement, role explicit-arg]
  10. `CategoryTheory.evaluation`
      [def, depth 23, introduced-by-proof, role explicit-arg]
  11. `CategoryTheory.SingleObj`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  12. `Action.functorCategoryEquivalence`
      [def, depth 27, introduced-by-proof, role explicit-arg]
  13. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Action`
      [inductive, depth 1, in-statement, role implicit-arg]
  15. `CategoryTheory.SingleObj.category`
      [def, depth 10, introduced-by-proof, role instance-slot]
  16. `Action.functorCategoryEquivalenceCompEvaluation`
      [def, depth 28, introduced-by-proof, role explicit-arg]
  17. `Action.instCategory`
      [def, depth 17, in-statement, role instance-slot]
  18. `Monoid`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0224  (target depth 33, band 26-50)

THEOREM PROVED: `_private.Std.Data.Internal.List.Associative.0.Std.Internal.List.min_apply`

Grade all 24 candidates.

   1. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   3. `Sigma.fst`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Sigma`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `Ordering`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `ite`
      [def, depth 5, in-statement, role implicit-arg]
   9. `instDecidableEqBool`
      [def, depth 7, in-statement, role explicit-arg]
  10. `ite_congr`
      [theorem, depth 8, in-statement, role explicit-arg]
  11. `_private.Std.Data.Internal.List.Associative.0.Std.Internal.List.minSigmaOfOrd`
      [def, depth 32, in-statement, role instance-slot]
  12. `Ord`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `apply_ite`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
  14. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
  15. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `Decidable`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  18. `Ordering.isLE`
      [def, depth 31, in-statement, role explicit-arg]
  19. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  21. `Min.min`
      [def, depth 1, in-statement, role explicit-arg]
  22. `Ord.compare`
      [def, depth 1, in-statement, role explicit-arg]
  23. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  24. `Not`
      [def, depth 1, in-statement, role type-annotation]

### proof_0225  (target depth 26, band 26-50)

THEOREM PROVED: `Nat.sum_le_ofDigits`

Grade all 17 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `instLENat`
      [def, depth 2, in-statement, role instance-slot]
   3. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Nat.instMulZeroClass`
      [def, depth 17, in-statement, role instance-slot]
   5. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
   7. `Nat.instSemiring`
      [def, depth 24, in-statement, role instance-slot]
   8. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
   9. `Nat.ofDigits_one`
      [theorem, depth 25, introduced-by-proof, role explicit-arg]
  10. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
  11. `List.sum`
      [def, depth 7, in-statement, role implicit-arg]
  12. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
  13. `Nat.ofDigits_monotone`
      [theorem, depth 25, introduced-by-proof, role explicit-arg]
  14. `Eq.rec`
      [recursor, depth 2, in-statement, role applied]
  15. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  16. `Nat.ofDigits`
      [def, depth 13, in-statement, role explicit-arg]
  17. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]

### proof_0226  (target depth 38, band 26-50)

THEOREM PROVED: `CategoryTheory.CosimplicialObject.Augmented.toArrow_obj_right`

Grade all 10 candidates.

   1. `CategoryTheory.Comma.right`
      [def, depth 3, in-statement, role explicit-arg]
   2. `CategoryTheory.CosimplicialObject.Augmented.toArrow`
      [def, depth 37, in-statement, role explicit-arg]
   3. `CategoryTheory.instCategoryArrow`
      [def, depth 14, in-statement, role instance-slot]
   4. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   5. `CategoryTheory.Arrow`
      [def, depth 11, in-statement, role implicit-arg]
   6. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `CategoryTheory.CosimplicialObject.Augmented`
      [def, depth 32, in-statement, role implicit-arg]
   8. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   9. `CategoryTheory.Functor.id`
      [def, depth 10, in-statement, role implicit-arg]
  10. `CategoryTheory.CosimplicialObject.instCategoryAugmented`
      [def, depth 33, in-statement, role instance-slot]

### proof_0227  (target depth 28, band 26-50)

THEOREM PROVED: `UInt64.toFin_sub`

Grade all 8 candidates.

   1. `UInt64.toFin`
      [def, depth 4, in-statement, role implicit-arg]
   2. `UInt64.size`
      [def, depth 4, in-statement, role explicit-arg]
   3. `HSub.hSub`
      [def, depth 2, in-statement, role explicit-arg]
   4. `rfl`
      [def, depth 2, in-statement, role applied]
   5. `instHSub`
      [def, depth 3, in-statement, role instance-slot]
   6. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `instSubUInt64`
      [def, depth 27, in-statement, role instance-slot]
   8. `UInt64`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0228  (target depth 28, band 26-50)

THEOREM PROVED: `Equiv.transPartialEquiv_apply`

Grade all 5 candidates.

   1. `Equiv`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   3. `PartialEquiv.toFun`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Equiv.transPartialEquiv`
      [def, depth 27, in-statement, role explicit-arg]
   5. `PartialEquiv`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0229  (target depth 26, band 26-50)

THEOREM PROVED: `ByteArray.empty_append`

Grade all 19 candidates.

   1. `ByteArray.instAppend`
      [def, depth 9, in-statement, role instance-slot]
   2. `HAppend.hAppend`
      [def, depth 2, in-statement, role implicit-arg]
   3. `ByteArray.data_append`
      [theorem, depth 25, introduced-by-proof, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   6. `ByteArray.empty`
      [def, depth 6, in-statement, role explicit-arg]
   7. `UInt8`
      [inductive, depth 0, in-statement, role explicit-arg]
   8. `Array.empty_append`
      [theorem, depth 25, introduced-by-proof, role explicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `ByteArray`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Array`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `instHAppendOfAppend`
      [def, depth 3, in-statement, role instance-slot]
  13. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  14. `Array.instAppend`
      [def, depth 22, introduced-by-proof, role instance-slot]
  15. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  16. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  17. `ByteArray.ext`
      [theorem, depth 6, introduced-by-proof, role applied]
  18. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  19. `ByteArray.data`
      [def, depth 1, in-statement, role explicit-arg]

### proof_0230  (target depth 42, band 26-50)

THEOREM PROVED: `RootPairing.Equiv.inv_coweightMap`

Grade all 15 candidates.

   1. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
   2. `LinearMap`
      [inductive, depth 11, in-statement, role implicit-arg]
   3. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `RootPairing.Equiv`
      [inductive, depth 7, in-statement, role type-annotation]
   5. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   6. `rfl`
      [def, depth 2, in-statement, role applied]
   7. `RootPairing`
      [inductive, depth 6, in-statement, role type-annotation]
   8. `RootPairing.Equiv.toHom`
      [def, depth 8, in-statement, role explicit-arg]
   9. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  11. `RootPairing.Equiv.symm`
      [def, depth 41, in-statement, role explicit-arg]
  12. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
  13. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  15. `RootPairing.Hom.coweightMap`
      [def, depth 8, in-statement, role implicit-arg]

### proof_0231  (target depth 50, band 26-50)

THEOREM PROVED: `Lean.Grind.instDivUInt8UintOfNatNat`

Grade all 25 candidates.

   1. `Nat.instDiv`
      [def, depth 19, in-statement, role instance-slot]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   3. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `UInt8`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `instDivUInt8`
      [def, depth 25, in-statement, role instance-slot]
   8. `Nat.cast`
      [def, depth 2, in-statement, role explicit-arg]
   9. `instHDiv`
      [def, depth 3, in-statement, role instance-slot]
  10. `UInt8.toNat_div`
      [theorem, depth 26, introduced-by-proof, role explicit-arg]
  11. `Lean.Grind.IntInterval.uint`
      [def, depth 23, in-statement, role implicit-arg]
  12. `Lean.Grind.instToIntUInt8UintOfNatNat`
      [def, depth 49, in-statement, role instance-slot]
  13. `UInt8.toNat`
      [def, depth 13, in-statement, role explicit-arg]
  14. `Lean.Grind.ToInt.toInt`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  15. `instNatCastInt`
      [def, depth 2, in-statement, role instance-slot]
  16. `Int.instDiv`
      [def, depth 21, in-statement, role instance-slot]
  17. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  18. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  19. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
  20. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  22. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  23. `HDiv.hDiv`
      [def, depth 2, in-statement, role explicit-arg]
  24. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  25. `Lean.Grind.ToInt.Div.mk`
      [constructor, depth 22, introduced-by-proof, role applied]

### proof_0232  (target depth 34, band 26-50)

THEOREM PROVED: `MonCat.forget_preservesLimitsOfSize`

Grade all 18 candidates.

   1. `CategoryTheory.forget`
      [def, depth 19, in-statement, role explicit-arg]
   2. `MonCat.carrier`
      [def, depth 1, in-statement, role implicit-arg]
   3. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   4. `CategoryTheory.Limits.PreservesLimit`
      [inductive, depth 2, introduced-by-proof, role implicit-arg]
   5. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `MonCat.instConcreteCategoryMonoidHomCarrier`
      [def, depth 17, in-statement, role instance-slot]
   7. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   9. `MonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
  10. `MonCat.str`
      [def, depth 1, in-statement, role instance-slot]
  11. `UnivLE`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `CategoryTheory.types`
      [def, depth 10, in-statement, role implicit-arg]
  13. `inferInstance`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  14. `CategoryTheory.Limits.PreservesLimitsOfSize.mk`
      [constructor, depth 9, introduced-by-proof, role applied]
  15. `MonCat`
      [inductive, depth 0, in-statement, role explicit-arg]
  16. `MonCat.instCategory`
      [def, depth 15, in-statement, role implicit-arg]
  17. `CategoryTheory.Limits.PreservesLimitsOfShape.mk`
      [constructor, depth 9, introduced-by-proof, role explicit-arg]
  18. `MonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0233  (target depth 41, band 26-50)

THEOREM PROVED: `Int.eq_of_mul_eq_one`

Grade all 16 candidates.

   1. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Int.instNegInt`
      [def, depth 7, introduced-by-proof, role instance-slot]
   4. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Int.eq_one_or_neg_one_of_mul_eq_one'`
      [theorem, depth 40, introduced-by-proof, role explicit-arg]
   6. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `And`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   8. `and_imp`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   9. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  10. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  11. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  12. `Int.instMul`
      [def, depth 11, in-statement, role instance-slot]
  13. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  14. `instOfNat`
      [def, depth 3, in-statement, role instance-slot]
  15. `Or.elim`
      [theorem, depth 5, introduced-by-proof, role applied]
  16. `Neg.neg`
      [def, depth 1, introduced-by-proof, role explicit-arg]

### proof_0234  (target depth 32, band 26-50)

THEOREM PROVED: `Int.rel_of_forall_rel_succ_of_le`

Grade all 21 candidates.

   1. `Std.Refl`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `instOfNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   4. `Int.instLinearOrder`
      [def, depth 31, introduced-by-proof, role instance-slot]
   5. `LE.le.eq_or_lt`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
   6. `Eq.rec`
      [recursor, depth 2, introduced-by-proof, role explicit-arg]
   7. `refl`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   8. `Or.elim`
      [theorem, depth 5, introduced-by-proof, role applied]
   9. `Int.rel_of_forall_rel_succ_of_lt`
      [theorem, depth 27, introduced-by-proof, role explicit-arg]
  10. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `PartialOrder.toPreorder`
      [def, depth 1, introduced-by-proof, role instance-slot]
  12. `Eq`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
  13. `HAdd.hAdd`
      [def, depth 2, in-statement, role type-annotation]
  14. `IsTrans`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `LT.lt`
      [def, depth 1, introduced-by-proof, role implicit-arg]
  16. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  17. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
  18. `Int.instAdd`
      [def, depth 11, in-statement, role instance-slot]
  19. `Preorder.toLT`
      [def, depth 1, introduced-by-proof, role instance-slot]
  20. `Int.instLEInt`
      [def, depth 15, in-statement, role instance-slot]
  21. `LinearOrder.toPartialOrder`
      [def, depth 1, introduced-by-proof, role instance-slot]

### proof_0235  (target depth 29, band 26-50)

THEOREM PROVED: `Std.DTreeMap.Internal.Impl.toList_keysArray`

Grade all 18 candidates.

   1. `Std.DTreeMap.Internal.Impl.keysArray_eq_toArray_keys`
      [theorem, depth 28, introduced-by-proof, role explicit-arg]
   2. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
   3. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   4. `Std.DTreeMap.Internal.Impl.keysArray`
      [def, depth 8, in-statement, role explicit-arg]
   5. `Std.DTreeMap.Internal.Impl.keys`
      [def, depth 8, in-statement, role explicit-arg]
   6. `Array.toList`
      [def, depth 1, in-statement, role explicit-arg]
   7. `Std.DTreeMap.Internal.Impl.keys_eq_keys`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
   8. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   9. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  10. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  11. `Array`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `Std.Internal.List.keys`
      [def, depth 6, introduced-by-proof, role explicit-arg]
  14. `Std.DTreeMap.Internal.Impl.toListModel`
      [def, depth 9, introduced-by-proof, role explicit-arg]
  15. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `List.toArray`
      [def, depth 2, introduced-by-proof, role implicit-arg]
  17. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  18. `Std.DTreeMap.Internal.Impl`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0236  (target depth 37, band 26-50)

THEOREM PROVED: `Std.Internal.List.getKey!_filter_key`

Grade all 23 candidates.

   1. `Sigma`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `Std.Internal.List.DistinctKeys`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Sigma.fst`
      [def, depth 1, in-statement, role explicit-arg]
   4. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   6. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
   7. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `Std.Internal.List.getKey?_filter_key`
      [theorem, depth 19, introduced-by-proof, role explicit-arg]
  11. `Bool`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Option.get!`
      [def, depth 34, in-statement, role explicit-arg]
  13. `Std.Internal.List.getKey?`
      [def, depth 7, in-statement, role explicit-arg]
  14. `Option.filter`
      [def, depth 8, in-statement, role explicit-arg]
  15. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `Std.Internal.List.getKey!`
      [def, depth 35, in-statement, role explicit-arg]
  17. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  18. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  19. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  20. `Std.Internal.List.getKey!_eq_getKey?`
      [theorem, depth 36, introduced-by-proof, role explicit-arg]
  21. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  22. `List.filter`
      [def, depth 6, in-statement, role explicit-arg]
  23. `List`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0237  (target depth 29, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.initialMul_hom`

Grade all 12 candidates.

   1. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   2. `CategoryTheory.Limits.prod`
      [def, depth 15, in-statement, role explicit-arg]
   3. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CategoryTheory.Limits.HasInitial`
      [def, depth 11, in-statement, role type-annotation]
   7. `CategoryTheory.Limits.initialMul`
      [def, depth 28, in-statement, role explicit-arg]
   8. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   9. `CategoryTheory.Limits.initial`
      [def, depth 15, in-statement, role explicit-arg]
  10. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  11. `CategoryTheory.Limits.HasBinaryProduct`
      [def, depth 14, in-statement, role type-annotation]
  12. `CategoryTheory.Limits.HasStrictInitialObjects`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0238  (target depth 41, band 26-50)

THEOREM PROVED: `CategoryTheory.Functor.isRightKanExtension_iff_of_iso₂`

Grade all 25 candidates.

   1. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   2. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   3. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
   4. `CategoryTheory.Functor.isUniversalOfIsRightKanExtension`
      [def, depth 28, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
   6. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   7. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   8. `CategoryTheory.Functor.RightExtension.isUniversalEquivOfIso₂`
      [def, depth 40, introduced-by-proof, role let-value]
   9. `CategoryTheory.Functor.whiskeringLeft`
      [def, depth 26, introduced-by-proof, role explicit-arg]
  10. `CategoryTheory.CostructuredArrow.IsUniversal`
      [def, depth 25, introduced-by-proof, role explicit-arg]
  11. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Equiv.invFun`
      [def, depth 1, introduced-by-proof, role explicit-arg]
  13. `CategoryTheory.Functor.IsRightKanExtension.mk`
      [constructor, depth 28, introduced-by-proof, role explicit-arg]
  14. `CategoryTheory.Functor.whiskerLeft`
      [def, depth 21, in-statement, role explicit-arg]
  15. `CategoryTheory.Functor.IsRightKanExtension`
      [inductive, depth 20, in-statement, role implicit-arg]
  16. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
  17. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role implicit-arg]
  18. `CategoryTheory.Functor.RightExtension.mk`
      [def, depth 27, introduced-by-proof, role explicit-arg]
  19. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  21. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  22. `Equiv.toFun`
      [def, depth 1, introduced-by-proof, role explicit-arg]
  23. `Nonempty.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
  24. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  25. `Equiv`
      [inductive, depth 0, introduced-by-proof, role type-annotation]

### proof_0239  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.Discrete.equivalence_unitIso`

Grade all 18 candidates.

   1. `Equiv.symm`
      [def, depth 10, in-statement, role explicit-arg]
   2. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   3. `CategoryTheory.Discrete`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
   5. `CategoryTheory.Discrete.equivalence`
      [def, depth 26, in-statement, role explicit-arg]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   7. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   9. `CategoryTheory.Equivalence.unitIso`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CategoryTheory.Discrete.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `CategoryTheory.Functor.id`
      [def, depth 10, in-statement, role explicit-arg]
  12. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  13. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `CategoryTheory.discreteCategory`
      [def, depth 10, in-statement, role instance-slot]
  16. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
  17. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role implicit-arg]
  18. `CategoryTheory.Discrete.functor`
      [def, depth 12, in-statement, role explicit-arg]

### proof_0240  (target depth 31, band 26-50)

THEOREM PROVED: `AlgHom.toLinearMap_toOpposite`

Grade all 21 candidates.

   1. `Semiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
   2. `Distrib.toMul`
      [def, depth 1, in-statement, role instance-slot]
   3. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
   5. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   8. `Algebra.toModule`
      [def, depth 18, in-statement, role instance-slot]
   9. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  10. `rfl`
      [def, depth 2, in-statement, role applied]
  11. `AlgHom`
      [inductive, depth 2, in-statement, role implicit-arg]
  12. `AlgHom.toLinearMap`
      [def, depth 23, in-statement, role implicit-arg]
  13. `LinearMap`
      [inductive, depth 11, in-statement, role implicit-arg]
  14. `MulOpposite`
      [def, depth 1, in-statement, role explicit-arg]
  15. `AlgHom.funLike`
      [def, depth 20, in-statement, role instance-slot]
  16. `AlgHom.toOpposite`
      [def, depth 30, in-statement, role explicit-arg]
  17. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `MulOpposite.instSemiring`
      [def, depth 25, in-statement, role implicit-arg]
  19. `MulOpposite.instAlgebra`
      [def, depth 28, in-statement, role instance-slot]
  20. `instDistribOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
  21. `Commute`
      [def, depth 5, in-statement, role type-annotation]
