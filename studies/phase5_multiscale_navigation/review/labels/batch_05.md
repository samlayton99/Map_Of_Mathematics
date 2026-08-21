# Grading batch `batch_05` -- 20 proofs

You are one of several independent raters. You will never see any
ranking our system produces and must not try to guess one. Your
grades are the ground truth those rankings are scored against.

Candidates are listed in RANDOM order. Position means nothing.

`depth` = how much mathematics sits beneath a declaration in the
library. It is context so you can tell a deep theorem from a
primitive. It is NOT a hint and you must not grade something high
merely because it is deep, nor low because it is shallow.

`in-statement` = already implied by what the theorem says.
`introduced-by-proof` = the proof brought it in. Either can be key.

## The grade

Give **every** candidate a grade 0-4. Do not pick a top few -- grade all of
them. The grade is about THIS proof, not about the declaration in general.

| grade | name | meaning |
|---|---|---|
| **4** | `KEY` | A core move. If asked "how does this proof go?", you would name it. Removing it destroys the proof's central idea. |
| **3** | `SUPPORT` | Real mathematical content, genuinely used, but secondary -- a lemma the key move needs, a rewrite that does actual work. |
| **2** | `LEGIT_GLUE` | Logical or structural plumbing (`Eq.trans`, `congrArg`, `Iff.mpr`, coercions, instances) that **is genuinely the content of this proof**. Near the foundations, assembling equalities really can be the whole argument. |
| **1** | `BAD_GLUE` | Plumbing or background that is present but carries no idea here. A person explaining the proof would never mention it. Correct to demote. |
| **0** | `JUNK` | Irrelevant machinery: automation residue, instance/typeclass resolution, universe or decidability bookkeeping, notation unfolding. Noise. |

The 2-versus-1 line is the important one and it is the whole reason this
panel exists. **Do not grade something 1 just because it looks like plumbing.**
Ask whether a mathematician explaining *this specific theorem* would mention
it. If yes, it is 2 even if its name looks like machinery. If the theorem is a
deep result and the item is `Eq.mpr`, that is 1.

## Also required, per proof

`missing_key`: `true` if you believe this proof has a key move that is **not
in the list at all** -- it works by manipulating local hypotheses, exhibiting
a witness, splitting into cases, or pure rewriting, and no listed citation
captures that. This is a genuine measurement of our coverage gap, not a
failure to do the task. Otherwise `false`.

`confidence`: `high` / `medium` / `low` -- whether you understood the theorem
well enough to grade it.

## Output format

Return **only** a JSON object, no commentary. Every proof id in your batch
must appear exactly once, and every candidate number of that proof must
appear exactly once in its `grades` map.

```json
{
  "proof_007": {
    "grades": {"1": 1, "2": 4, "3": 0, "4": 3, "5": 2},
    "missing_key": false,
    "confidence": "high"
  }
}
```


---

### proof_081  (target depth 47, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.fiberwiseColimit_map`

Grade all 20 candidates below.

   1. `CategoryTheory.Limits.HasColimit`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.Limits.colimit`
      [def, depth 6, in-statement, role explicit-arg]
   4. `CategoryTheory.Limits.fiberwiseColimit`
      [def, depth 46, in-statement, role explicit-arg]
   5. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   6. `CategoryTheory.Grothendieck.ι`
      [def, depth 42, in-statement, role explicit-arg]
   7. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `CategoryTheory.Cat`
      [def, depth 1, in-statement, role explicit-arg]
   9. `CategoryTheory.Cat.Hom.toFunctor`
      [def, depth 3, in-statement, role explicit-arg]
  10. `CategoryTheory.Grothendieck`
      [inductive, depth 32, in-statement, role implicit-arg]
  11. `CategoryTheory.Cat.str`
      [def, depth 2, in-statement, role instance-slot]
  12. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  13. `CategoryTheory.Grothendieck.instCategory`
      [def, depth 39, in-statement, role instance-slot]
  14. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  15. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  16. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
  17. `CategoryTheory.Bundled.α`
      [def, depth 1, in-statement, role implicit-arg]
  18. `CategoryTheory.Cat.category`
      [def, depth 31, in-statement, role instance-slot]
  19. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  20. `CategoryTheory.Functor.map`
      [def, depth 2, in-statement, role explicit-arg]

### proof_082  (target depth 73, band 51-75)

THEOREM PROVED: `Std.ExtDHashMap.Const.getD_insertManyIfNewUnit_list`

Grade all 17 candidates below.

   1. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Id`
      [def, depth 0, in-statement, role implicit-arg]
   3. `Std.ExtDHashMap`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Id.instMonad`
      [def, depth 3, in-statement, role instance-slot]
   5. `List.instForIn'InferInstanceMembershipOfMonad`
      [def, depth 14, in-statement, role instance-slot]
   6. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Unit`
      [def, depth 1, in-statement, role explicit-arg]
   8. `Std.ExtDHashMap.Const.insertManyIfNewUnit`
      [def, depth 72, in-statement, role explicit-arg]
   9. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `List`
      [inductive, depth 0, in-statement, role explicit-arg]
  11. `List.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  12. `rfl`
      [def, depth 2, in-statement, role applied]
  13. `Std.ExtDHashMap.Const.getD`
      [def, depth 68, in-statement, role implicit-arg]
  14. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `inferInstance`
      [def, depth 0, in-statement, role implicit-arg]
  16. `instForInOfForIn'`
      [def, depth 4, in-statement, role instance-slot]
  17. `Membership`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_083  (target depth 81, band 76-125)

THEOREM PROVED: `Finset.card_le_card_sub_right`

Grade all 19 candidates below.

   1. `Finset.card`
      [def, depth 12, in-statement, role explicit-arg]
   2. `Finset.Nonempty`
      [def, depth 54, in-statement, role type-annotation]
   3. `instHSub`
      [def, depth 3, in-statement, role instance-slot]
   4. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
   5. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   6. `Finset.card_le_card_image₂_right`
      [theorem, depth 80, introduced-by-proof, role explicit-arg]
   7. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   8. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
   9. `SubNegMonoid.toSub`
      [def, depth 1, in-statement, role instance-slot]
  10. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `HSub.hSub`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  13. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `sub_left_injective`
      [theorem, depth 13, introduced-by-proof, role explicit-arg]
  15. `_private.Mathlib.Algebra.Group.Pointwise.Finset.Basic.0.Finset.card_le_card_sub_right.match_1_1`
      [def, depth 55, introduced-by-proof, role applied]
  16. `Finset`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `Finset.sub`
      [def, depth 75, in-statement, role instance-slot]
  18. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
  19. `instLENat`
      [def, depth 2, in-statement, role instance-slot]

### proof_084  (target depth 141, band 126+)

THEOREM PROVED: `FundamentalGroupoidFunctor.piToPiTop_obj_as`

Grade all 18 candidates below.

   1. `TopCat.instCategory`
      [def, depth 18, in-statement, role instance-slot]
   2. `CategoryTheory.Groupoid.toCategory`
      [def, depth 1, in-statement, role instance-slot]
   3. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   4. `CategoryTheory.Bundled.α`
      [def, depth 1, in-statement, role implicit-arg]
   5. `FundamentalGroupoid.as`
      [def, depth 1, in-statement, role explicit-arg]
   6. `TopCat`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `FundamentalGroupoid.fundamentalGroupoidFunctor`
      [def, depth 138, in-statement, role explicit-arg]
   8. `CategoryTheory.pi`
      [def, depth 10, in-statement, role instance-slot]
   9. `CategoryTheory.Grpd.category`
      [def, depth 17, in-statement, role instance-slot]
  10. `TopCat.str`
      [def, depth 1, in-statement, role instance-slot]
  11. `TopCat.carrier`
      [def, depth 1, in-statement, role implicit-arg]
  12. `Pi.topologicalSpace`
      [def, depth 64, in-statement, role instance-slot]
  13. `TopCat.of`
      [constructor, depth 1, in-statement, role explicit-arg]
  14. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  15. `CategoryTheory.Grpd.str'`
      [def, depth 2, in-statement, role instance-slot]
  16. `CategoryTheory.Grpd`
      [def, depth 1, in-statement, role implicit-arg]
  17. `FundamentalGroupoidFunctor.piToPiTop`
      [def, depth 140, in-statement, role explicit-arg]
  18. `CategoryTheory.Groupoid`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_085  (target depth 8, band 0-10)

THEOREM PROVED: `Relation.reflTransGen_eq_reflGen`

Grade all 12 candidates below.

   1. `Relation.transGen_eq_self`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   2. `Relation.ReflGen`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `Relation.ReflTransGen`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   5. `Relation.reflGen_transGen`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   6. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `Relation.TransGen`
      [inductive, depth 0, introduced-by-proof, role explicit-arg]
   8. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   9. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  10. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  11. `IsTrans`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]

### proof_086  (target depth 14, band 11-25)

THEOREM PROVED: `ULift.addCommMonoid._proof_3`

Grade all 15 candidates below.

   1. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `ULift.smul`
      [def, depth 4, in-statement, role instance-slot]
   3. `AddCommMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
   4. `ULift`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `NSMul.toSMul`
      [def, depth 2, in-statement, role instance-slot]
   6. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   7. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   8. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   9. `rfl`
      [def, depth 2, in-statement, role applied]
  10. `AddMonoid.toNSMul`
      [def, depth 1, in-statement, role instance-slot]
  11. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `Equiv.ulift`
      [def, depth 10, in-statement, role explicit-arg]
  14. `HSMul.hSMul`
      [def, depth 2, in-statement, role explicit-arg]
  15. `instHSMul`
      [def, depth 3, in-statement, role instance-slot]

### proof_087  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.LaxMonoidalFunctor.comp_hom`

Grade all 13 candidates below.

   1. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   2. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.LaxMonoidalFunctor.Hom.hom`
      [def, depth 4, in-statement, role implicit-arg]
   6. `CategoryTheory.LaxMonoidalFunctor.toFunctor`
      [def, depth 3, in-statement, role explicit-arg]
   7. `CategoryTheory.LaxMonoidalFunctor`
      [inductive, depth 2, in-statement, role implicit-arg]
   8. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   9. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  12. `rfl`
      [def, depth 2, in-statement, role applied]
  13. `CategoryTheory.LaxMonoidalFunctor.instCategory`
      [def, depth 26, in-statement, role instance-slot]

### proof_088  (target depth 64, band 51-75)

THEOREM PROVED: `Set.Finite.exists_finset_coe`

Grade all 17 candidates below.

   1. `Set.toFinset`
      [def, depth 27, introduced-by-proof, role explicit-arg]
   2. `Nonempty.casesOn`
      [def, depth 3, in-statement, role applied]
   3. `Nonempty`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Nonempty.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
   6. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role unresolved]
   8. `Fintype`
      [inductive, depth 0, introduced-by-proof, role explicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Exists.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `Exists`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Set.Finite.nonempty_fintype`
      [theorem, depth 63, introduced-by-proof, role explicit-arg]
  13. `Set.Finite`
      [def, depth 5, in-statement, role type-annotation]
  14. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
  16. `SetLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Set.coe_toFinset`
      [theorem, depth 56, introduced-by-proof, role explicit-arg]

### proof_089  (target depth 82, band 76-125)

THEOREM PROVED: `Matrix.mulVec_injective_of_isUnit`

Grade all 23 candidates below.

   1. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   2. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Matrix`
      [def, depth 0, in-statement, role implicit-arg]
   4. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `IsUnit.isRegular`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   6. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   7. `NonUnitalNonAssocSemiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
   8. `NonUnitalSemiring.toNonUnitalNonAssocSemiring`
      [def, depth 1, in-statement, role instance-slot]
   9. `IsRegular.left`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  10. `IsLeftRegular`
      [def, depth 4, introduced-by-proof, role implicit-arg]
  11. `Matrix.mulVec`
      [def, depth 15, in-statement, role explicit-arg]
  12. `Monoid.toMulOneClass`
      [def, depth 5, introduced-by-proof, role instance-slot]
  13. `Matrix.instMulOfFintypeOfAddCommMonoid`
      [def, depth 16, in-statement, role instance-slot]
  14. `Semiring.toNonUnitalSemiring`
      [def, depth 5, in-statement, role instance-slot]
  15. `Iff.mp`
      [theorem, depth 1, in-statement, role applied]
  16. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
  17. `NonUnitalNonAssocSemiring.toDistrib`
      [def, depth 5, in-statement, role instance-slot]
  18. `IsUnit`
      [def, depth 3, in-statement, role type-annotation]
  19. `Function.Injective`
      [def, depth 1, in-statement, role implicit-arg]
  20. `Matrix.semiring`
      [def, depth 81, in-statement, role instance-slot]
  21. `Distrib.toMul`
      [def, depth 1, in-statement, role instance-slot]
  22. `Matrix.isLeftRegular_iff_mulVec_injective`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
  23. `Semiring.toMonoid`
      [def, depth 1, in-statement, role instance-slot]

### proof_090  (target depth 152, band 126+)

THEOREM PROVED: `UpperHalfPlane.linear_ne_zero`

Grade all 13 candidates below.

   1. `Ne`
      [def, depth 2, in-statement, role type-annotation]
   2. `UpperHalfPlane.linear_ne_zero_of_im`
      [theorem, depth 151, introduced-by-proof, role applied]
   3. `Pi.instZero`
      [def, depth 4, in-statement, role instance-slot]
   4. `UpperHalfPlane`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Real.instZero`
      [def, depth 85, in-statement, role instance-slot]
   7. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   8. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `UpperHalfPlane.coe`
      [def, depth 1, in-statement, role implicit-arg]
  10. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  12. `UpperHalfPlane.im_ne_zero`
      [theorem, depth 102, introduced-by-proof, role explicit-arg]
  13. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]

### proof_091  (target depth 4, band 0-10)

THEOREM PROVED: `le_of_antisymmRel_of_le`

Grade all 6 candidates below.

   1. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
   2. `AntisymmRel`
      [def, depth 1, in-statement, role type-annotation]
   3. `AntisymmRel.le`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   4. `LE.le.trans`
      [theorem, depth 3, introduced-by-proof, role applied]
   5. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]

### proof_092  (target depth 12, band 11-25)

THEOREM PROVED: `Associated.neg_right_iff`

Grade all 14 candidates below.

   1. `HasDistribNeg`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `MulOne.toMul`
      [def, depth 1, in-statement, role implicit-arg]
   3. `Associated`
      [def, depth 6, in-statement, role implicit-arg]
   4. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   6. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   7. `Associated.neg_right`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
   8. `Monoid`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Eq.rec`
      [recursor, depth 2, introduced-by-proof, role explicit-arg]
  10. `neg_neg`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  11. `InvolutiveNeg.toNeg`
      [def, depth 1, in-statement, role instance-slot]
  12. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  13. `HasDistribNeg.toInvolutiveNeg`
      [def, depth 2, in-statement, role instance-slot]
  14. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]

### proof_093  (target depth 34, band 26-50)

THEOREM PROVED: `Int16.ofBitVec_xor`

Grade all 10 candidates below.

   1. `instHXorOfXorOp`
      [def, depth 3, in-statement, role instance-slot]
   2. `rfl`
      [def, depth 2, in-statement, role applied]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
   5. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   6. `HXor.hXor`
      [def, depth 2, in-statement, role explicit-arg]
   7. `Int16`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Int16.ofBitVec`
      [def, depth 5, in-statement, role implicit-arg]
   9. `BitVec.instXorOp`
      [def, depth 33, in-statement, role instance-slot]
  10. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_094  (target depth 59, band 51-75)

THEOREM PROVED: `Finset.set_biUnion_union`

Grade all 7 candidates below.

   1. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`
      [def, depth 1, introduced-by-proof, role instance-slot]
   2. `CompleteBooleanAlgebra.toCompleteLattice`
      [def, depth 1, introduced-by-proof, role instance-slot]
   3. `Finset.iSup_union`
      [theorem, depth 55, introduced-by-proof, role applied]
   4. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   5. `Finset`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Set.instCompleteAtomicBooleanAlgebra`
      [def, depth 58, introduced-by-proof, role instance-slot]
   7. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]

### proof_095  (target depth 78, band 76-125)

THEOREM PROVED: `Int.prime_three`

Grade all 12 candidates below.

   1. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Nat.prime_three`
      [theorem, depth 51, introduced-by-proof, role explicit-arg]
   4. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   5. `instOfNat`
      [def, depth 3, in-statement, role instance-slot]
   6. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   7. `Int.prime_ofNat_iff`
      [theorem, depth 77, introduced-by-proof, role explicit-arg]
   8. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Prime`
      [def, depth 6, in-statement, role implicit-arg]
  10. `CommSemiring.toCommMonoidWithZero`
      [def, depth 6, in-statement, role instance-slot]
  11. `Nat.Prime`
      [def, depth 19, introduced-by-proof, role implicit-arg]
  12. `Int.instCommSemiring`
      [def, depth 37, in-statement, role instance-slot]

### proof_096  (target depth 205, band 126+)

THEOREM PROVED: `Real.contDiffAt_rpow_const_of_le`

Grade all 20 candidates below.

   1. `Real.denselyNormedField`
      [def, depth 153, in-statement, role instance-slot]
   2. `WithTop.natCast`
      [def, depth 3, in-statement, role instance-slot]
   3. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   5. `Nat.cast`
      [def, depth 2, in-statement, role explicit-arg]
   6. `instHPow`
      [def, depth 3, in-statement, role instance-slot]
   7. `Real.instPow`
      [def, depth 186, in-statement, role instance-slot]
   8. `Real.normedAddCommGroup`
      [def, depth 148, in-statement, role instance-slot]
   9. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  10. `Real.instNatCast`
      [def, depth 82, in-statement, role instance-slot]
  11. `Real.instLE`
      [def, depth 94, in-statement, role instance-slot]
  12. `ENat.instNatCast`
      [def, depth 3, in-statement, role instance-slot]
  13. `NormedField.toNormedSpace`
      [def, depth 105, in-statement, role instance-slot]
  14. `Real.contDiff_rpow_const_of_le`
      [theorem, depth 204, introduced-by-proof, role explicit-arg]
  15. `WithTop`
      [def, depth 1, in-statement, role implicit-arg]
  16. `ENat`
      [def, depth 2, in-statement, role explicit-arg]
  17. `ContDiff.contDiffAt`
      [theorem, depth 190, introduced-by-proof, role applied]
  18. `HPow.hPow`
      [def, depth 2, in-statement, role implicit-arg]
  19. `DenselyNormedField.toNontriviallyNormedField`
      [def, depth 111, in-statement, role instance-slot]
  20. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_097  (target depth 6, band 0-10)

THEOREM PROVED: `Combinatorics.Subspace.coe_apply`

Grade all 3 candidates below.

   1. `Combinatorics.Subspace.toFun`
      [def, depth 5, in-statement, role implicit-arg]
   2. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   3. `Combinatorics.Subspace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_098  (target depth 21, band 11-25)

THEOREM PROVED: `List.zip_eq_zip_take_min`

Grade all 11 candidates below.

   1. `List.zip_eq_zip_take_min._f`
      [def, depth 20, introduced-by-proof, role explicit-arg]
   2. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `Min.min`
      [def, depth 1, in-statement, role explicit-arg]
   5. `List.brecOn`
      [def, depth 5, in-statement, role applied]
   6. `List.length`
      [def, depth 9, in-statement, role explicit-arg]
   7. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `List.take`
      [def, depth 6, in-statement, role explicit-arg]
  10. `List.zip`
      [def, depth 7, in-statement, role explicit-arg]
  11. `instMinNat`
      [def, depth 16, in-statement, role instance-slot]

### proof_099  (target depth 33, band 26-50)

THEOREM PROVED: `CategoryTheory.Under.equivalenceOfIsInitial_counitIso`

Grade all 23 candidates below.

   1. `CategoryTheory.instCategoryUnder`
      [def, depth 26, in-statement, role instance-slot]
   2. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   4. `CategoryTheory.Functor.mk`
      [constructor, depth 9, in-statement, role explicit-arg]
   5. `CategoryTheory.Under.homMk`
      [def, depth 27, in-statement, role explicit-arg]
   6. `CategoryTheory.Under.equivalenceOfIsInitial._proof_2`
      [theorem, depth 27, in-statement, role explicit-arg]
   7. `CategoryTheory.Under.mk`
      [def, depth 24, in-statement, role implicit-arg]
   8. `CategoryTheory.Limits.IsInitial`
      [def, depth 24, in-statement, role type-annotation]
   9. `CategoryTheory.Under.equivalenceOfIsInitial._proof_3`
      [theorem, depth 28, in-statement, role explicit-arg]
  10. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  11. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  12. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  13. `CategoryTheory.Equivalence.counitIso`
      [def, depth 2, in-statement, role explicit-arg]
  14. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  15. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  16. `CategoryTheory.Under.equivalenceOfIsInitial`
      [def, depth 32, in-statement, role explicit-arg]
  17. `CategoryTheory.Under`
      [def, depth 24, in-statement, role implicit-arg]
  18. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  19. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role implicit-arg]
  20. `CategoryTheory.Limits.IsInitial.to`
      [def, depth 25, in-statement, role explicit-arg]
  21. `CategoryTheory.Under.forget`
      [def, depth 23, in-statement, role explicit-arg]
  22. `CategoryTheory.Under.equivalenceOfIsInitial._proof_4`
      [theorem, depth 28, in-statement, role explicit-arg]
  23. `CategoryTheory.Functor.id`
      [def, depth 10, in-statement, role explicit-arg]

### proof_100  (target depth 70, band 51-75)

THEOREM PROVED: `Std.DHashMap.Const.get!_eq_default`

Grade all 25 candidates below.

   1. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Std.DHashMap.contains`
      [def, depth 67, in-statement, role explicit-arg]
   3. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `implies_congr`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.DHashMap.Const.get!`
      [def, depth 67, in-statement, role explicit-arg]
   8. `Std.DHashMap`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `Bool.false`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Std.DHashMap.instMembership`
      [def, depth 68, in-statement, role instance-slot]
  13. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
  14. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `Bool.not_eq_true`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
  16. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `Not`
      [def, depth 1, in-statement, role implicit-arg]
  18. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  19. `Std.DHashMap.Const.get!_eq_default_of_contains_eq_false`
      [theorem, depth 67, introduced-by-proof, role explicit-arg]
  20. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
  21. `Inhabited.default`
      [def, depth 1, in-statement, role explicit-arg]
  22. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  23. `id`
      [def, depth 0, in-statement, role explicit-arg]
  24. `_private.Std.Data.DHashMap.Lemmas.0.Std.DHashMap.Const.get!_eq_default._simp_1_1`
      [theorem, depth 69, introduced-by-proof, role explicit-arg]
  25. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
