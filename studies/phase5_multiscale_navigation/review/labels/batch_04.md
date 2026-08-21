# Grading batch `batch_04` -- 20 proofs

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

### proof_061  (target depth 2, band 0-10)

THEOREM PROVED: `SlashAction.slash_one`

Grade all 3 candidates below.

   1. `Monoid`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `SlashAction`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_062  (target depth 15, band 11-25)

THEOREM PROVED: `neg_le_neg`

Grade all 16 candidates below.

   1. `AddCommMonoid.toAddCommSemigroup`
      [def, depth 5, introduced-by-proof, role instance-slot]
   2. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `SubtractionMonoid.toSubNegZeroMonoid`
      [def, depth 9, in-statement, role instance-slot]
   4. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   5. `AddCommGroup.toAddGroup`
      [def, depth 1, in-statement, role instance-slot]
   6. `NegZeroClass.toNeg`
      [def, depth 1, in-statement, role instance-slot]
   7. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `SubNegZeroMonoid.toNegZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   9. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  10. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
  11. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]
  12. `AddGroup.toSubtractionMonoid`
      [def, depth 11, in-statement, role instance-slot]
  13. `IsOrderedAddMonoid`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
  15. `neg_le_neg_iff`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
  16. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]

### proof_063  (target depth 30, band 26-50)

THEOREM PROVED: `CategoryTheory.ShortComplex.Splitting.leftHomologyData_H`

Grade all 9 candidates below.

   1. `CategoryTheory.ShortComplex`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `CategoryTheory.ShortComplex.Splitting.leftHomologyData`
      [def, depth 29, in-statement, role explicit-arg]
   3. `CategoryTheory.Limits.HasZeroObject`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   5. `CategoryTheory.ShortComplex.Splitting`
      [inductive, depth 18, in-statement, role type-annotation]
   6. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`
      [def, depth 17, in-statement, role instance-slot]
   7. `CategoryTheory.Preadditive`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `CategoryTheory.ShortComplex.LeftHomologyData.H`
      [def, depth 4, in-statement, role explicit-arg]
   9. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_064  (target depth 53, band 51-75)

THEOREM PROVED: `instLawfulCommIdentityUInt64HOrOfNat`

Grade all 10 candidates below.

   1. `UInt64.instOfNat`
      [def, depth 25, in-statement, role instance-slot]
   2. `UInt64.or_zero`
      [theorem, depth 51, introduced-by-proof, role explicit-arg]
   3. `Std.LawfulCommIdentity.mk`
      [constructor, depth 2, introduced-by-proof, role applied]
   4. `instHOrOfOrOp`
      [def, depth 3, in-statement, role instance-slot]
   5. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `UInt64`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `instOrOpUInt64`
      [def, depth 35, in-statement, role instance-slot]
   8. `Std.Commutative.comm`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   9. `HOr.hOr`
      [def, depth 2, in-statement, role implicit-arg]
  10. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_065  (target depth 95, band 76-125)

THEOREM PROVED: `instFullFintypeCatLightProfiniteToLightProfinite`

Grade all 15 candidates below.

   1. `TotallyDisconnectedSpace`
      [inductive, depth 1, in-statement, role explicit-arg]
   2. `CategoryTheory.types`
      [def, depth 10, in-statement, role instance-slot]
   3. `FintypeCat`
      [def, depth 11, in-statement, role implicit-arg]
   4. `FintypeCat.toLightProfinite`
      [def, depth 92, in-statement, role implicit-arg]
   5. `FintypeCat.toLightProfiniteFullyFaithful`
      [def, depth 94, introduced-by-proof, role explicit-arg]
   6. `Finite`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `LightProfinite`
      [def, depth 2, in-statement, role implicit-arg]
   8. `TopCat.str`
      [def, depth 1, in-statement, role instance-slot]
   9. `CategoryTheory.Functor.FullyFaithful.full`
      [theorem, depth 16, introduced-by-proof, role applied]
  10. `SecondCountableTopology`
      [inductive, depth 1, in-statement, role explicit-arg]
  11. `TopCat`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `CategoryTheory.ObjectProperty.FullSubcategory.category`
      [def, depth 10, in-statement, role instance-slot]
  13. `CompHausLike.category`
      [def, depth 20, in-statement, role instance-slot]
  14. `TopCat.carrier`
      [def, depth 1, in-statement, role explicit-arg]
  15. `And`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_066  (target depth 190, band 126+)

THEOREM PROVED: `Real.exp_one_rpow`

Grade all 25 candidates below.

   1. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
   2. `HPow.hPow`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Real.semiring`
      [def, depth 94, in-statement, role instance-slot]
   4. `Real.exp_mul`
      [theorem, depth 189, introduced-by-proof, role explicit-arg]
   5. `Real.exp`
      [def, depth 140, in-statement, role explicit-arg]
   6. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   7. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
   8. `instHPow`
      [def, depth 3, in-statement, role instance-slot]
   9. `MulOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
  10. `one_mul`
      [theorem, depth 2, in-statement, role explicit-arg]
  11. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Real.instOne`
      [def, depth 85, in-statement, role instance-slot]
  13. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  15. `Real.instMul`
      [def, depth 89, in-statement, role instance-slot]
  16. `id`
      [def, depth 0, in-statement, role explicit-arg]
  17. `Real.instPow`
      [def, depth 186, in-statement, role instance-slot]
  18. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  19. `instMulZeroOneClassOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
  20. `MulZeroOneClass.toMulOneClass`
      [def, depth 1, in-statement, role instance-slot]
  21. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  22. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  23. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  24. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  25. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_067  (target depth 5, band 0-10)

THEOREM PROVED: `Relation.TransGen.head`

Grade all 3 candidates below.

   1. `Relation.TransGen.head'`
      [theorem, depth 4, introduced-by-proof, role applied]
   2. `Relation.TransGen.to_reflTransGen`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   3. `Relation.TransGen`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_068  (target depth 22, band 11-25)

THEOREM PROVED: `CategoryTheory.prodOpEquiv_unitIso_hom_app`

Grade all 17 candidates below.

   1. `Opposite`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.prodOpEquiv`
      [def, depth 21, in-statement, role explicit-arg]
   6. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   7. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
   9. `CategoryTheory.Equivalence.unitIso`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  11. `CategoryTheory.Functor.id`
      [def, depth 10, in-statement, role explicit-arg]
  12. `CategoryTheory.prod'`
      [def, depth 10, in-statement, role instance-slot]
  13. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  14. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role explicit-arg]
  15. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  16. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  17. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]

### proof_069  (target depth 34, band 26-50)

THEOREM PROVED: `BitVec.ofBool_or_ofBool`

Grade all 17 candidates below.

   1. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Bool.false`
      [constructor, depth 1, in-statement, role explicit-arg]
   4. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   5. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
   6. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `BitVec.ofBool`
      [def, depth 25, in-statement, role explicit-arg]
  10. `instHOrOfOrOp`
      [def, depth 3, in-statement, role instance-slot]
  11. `Bool.casesOn`
      [def, depth 3, in-statement, role explicit-arg]
  12. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `Bool.or`
      [def, depth 5, in-statement, role explicit-arg]
  14. `BitVec.instOrOp`
      [def, depth 33, in-statement, role instance-slot]
  15. `HOr.hOr`
      [def, depth 2, in-statement, role explicit-arg]
  16. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
  17. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]

### proof_070  (target depth 69, band 51-75)

THEOREM PROVED: `Nat.find_pos`

Grade all 15 candidates below.

   1. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `Iff.trans`
      [theorem, depth 2, introduced-by-proof, role applied]
   4. `Exists`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Nat.pos_iff_ne_zero`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
   6. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   7. `Nat.find`
      [def, depth 17, in-statement, role explicit-arg]
   8. `DecidablePred`
      [def, depth 1, in-statement, role type-annotation]
   9. `Nat.find_eq_zero`
      [theorem, depth 68, introduced-by-proof, role explicit-arg]
  10. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
  11. `Not`
      [def, depth 1, in-statement, role implicit-arg]
  12. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `Iff.not`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  15. `Ne`
      [def, depth 2, introduced-by-proof, role implicit-arg]

### proof_071  (target depth 95, band 76-125)

THEOREM PROVED: `Subgroup.sq_mem_of_index_two`

Grade all 25 candidates below.

   1. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
   5. `NPow.toPow`
      [def, depth 2, in-statement, role instance-slot]
   6. `Subgroup`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `pow_two`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   8. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Subgroup.index`
      [def, depth 90, in-statement, role explicit-arg]
  10. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  11. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  12. `Monoid.toNPow`
      [def, depth 1, in-statement, role instance-slot]
  13. `Eq.rec`
      [recursor, depth 2, in-statement, role applied]
  14. `HPow.hPow`
      [def, depth 2, in-statement, role implicit-arg]
  15. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  16. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  17. `Subgroup.mul_self_mem_of_index_two`
      [theorem, depth 94, introduced-by-proof, role explicit-arg]
  18. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  19. `Subgroup.instSetLike`
      [def, depth 16, in-statement, role instance-slot]
  20. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
  21. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  22. `instHPow`
      [def, depth 3, in-statement, role instance-slot]
  23. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  24. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  25. `instHMul`
      [def, depth 3, in-statement, role instance-slot]

### proof_072  (target depth 199, band 126+)

THEOREM PROVED: `contMDiffWithinAt_congr_of_mem`

Grade all 18 candidates below.

   1. `StructureGroupoid.LocalInvariantProp.liftPropWithinAt_congr_iff_of_mem`
      [theorem, depth 78, introduced-by-proof, role applied]
   2. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   3. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `ModelWithCorners`
      [inductive, depth 11, in-statement, role type-annotation]
   5. `WithTop`
      [def, depth 1, in-statement, role type-annotation]
   6. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   9. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  11. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  12. `ENat`
      [def, depth 2, in-statement, role explicit-arg]
  13. `contDiffWithinAt_localInvariantProp`
      [theorem, depth 198, introduced-by-proof, role explicit-arg]
  14. `contDiffGroupoid`
      [def, depth 196, introduced-by-proof, role implicit-arg]
  15. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  17. `ChartedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `ContDiffWithinAtProp`
      [def, depth 166, in-statement, role implicit-arg]

### proof_073  (target depth 4, band 0-10)

THEOREM PROVED: `CategoryTheory.MorphismProperty.HasLeftCalculusOfFractions.exists_leftFraction`

Grade all 4 candidates below.

   1. `CategoryTheory.MorphismProperty.HasLeftCalculusOfFractions`
      [inductive, depth 3, in-statement, role type-annotation]
   2. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
   3. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   4. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_074  (target depth 21, band 11-25)

THEOREM PROVED: `RingEquiv.ofRingHom_symm`

Grade all 13 candidates below.

   1. `NonAssocSemiring.toNonUnitalNonAssocSemiring`
      [def, depth 1, in-statement, role instance-slot]
   2. `RingEquiv.ofRingHom`
      [def, depth 20, in-statement, role explicit-arg]
   3. `rfl`
      [def, depth 2, in-statement, role applied]
   4. `RingHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   5. `RingEquiv`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `Distrib.toMul`
      [def, depth 1, in-statement, role instance-slot]
   7. `NonUnitalNonAssocSemiring.toDistrib`
      [def, depth 5, in-statement, role instance-slot]
   8. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
   9. `Distrib.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  10. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `NonAssocSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `RingHom.comp`
      [def, depth 18, in-statement, role explicit-arg]
  13. `RingEquiv.symm`
      [def, depth 16, in-statement, role implicit-arg]

### proof_075  (target depth 43, band 26-50)

THEOREM PROVED: `Std.Internal.List.maxKeyD_modifyKey`

Grade all 12 candidates below.

   1. `Std.Internal.List.DistinctKeys`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Ord.compare`
      [def, depth 1, in-statement, role implicit-arg]
   3. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Std.Internal.List.minKeyD_modifyKey`
      [theorem, depth 42, introduced-by-proof, role applied]
   5. `Ord.opposite`
      [def, depth 2, in-statement, role instance-slot]
   6. `Std.TransOrd`
      [def, depth 2, in-statement, role type-annotation]
   7. `Std.LawfulBEqOrd`
      [def, depth 2, in-statement, role type-annotation]
   8. `inferInstance`
      [def, depth 0, in-statement, role explicit-arg]
   9. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Std.LawfulEqOrd`
      [def, depth 2, in-statement, role type-annotation]
  11. `Ord`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Sigma`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_076  (target depth 68, band 51-75)

THEOREM PROVED: `Graph.isClosedSubgraph_bot_iff`

Grade all 17 candidates below.

   1. `Eq.rec`
      [recursor, depth 2, in-statement, role explicit-arg]
   2. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   3. `Bot.bot`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Graph.IsClosedSubgraph`
      [inductive, depth 1, in-statement, role implicit-arg]
   5. `Graph.instPartialOrder`
      [def, depth 58, in-statement, role instance-slot]
   6. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
   7. `le_bot_iff`
      [theorem, depth 8, in-statement, role explicit-arg]
   8. `Graph`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
  11. `Graph.IsInducedSubgraph.le`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  12. `Graph.IsClosedSubgraph.rfl`
      [theorem, depth 67, introduced-by-proof, role explicit-arg]
  13. `Preorder.toLE`
      [def, depth 1, in-statement, role implicit-arg]
  14. `Graph.IsClosedSubgraph.isInducedSubgraph`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  15. `Iff.mp`
      [theorem, depth 1, in-statement, role explicit-arg]
  16. `Graph.instOrderBot`
      [def, depth 59, in-statement, role instance-slot]
  17. `OrderBot.toBot`
      [def, depth 2, in-statement, role instance-slot]

### proof_077  (target depth 82, band 76-125)

THEOREM PROVED: `Fin.le_of_surjective`

Grade all 12 candidates below.

   1. `Function.Surjective`
      [def, depth 1, in-statement, role type-annotation]
   2. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   3. `instLENat`
      [def, depth 2, in-statement, role instance-slot]
   4. `Eq.mp`
      [def, depth 3, introduced-by-proof, role applied]
   5. `Fintype.card_le_of_surjective`
      [theorem, depth 81, introduced-by-proof, role explicit-arg]
   6. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Fintype.card`
      [def, depth 13, introduced-by-proof, role explicit-arg]
  10. `Fin.fintype`
      [def, depth 55, introduced-by-proof, role instance-slot]
  11. `Fintype.card_fin`
      [theorem, depth 29, introduced-by-proof, role explicit-arg]
  12. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]

### proof_078  (target depth 163, band 126+)

THEOREM PROVED: `AlgebraicGeometry.instSurjectiveDescI₀SchemeF`

Grade all 12 candidates below.

   1. `AlgebraicGeometry.Scheme.Cover`
      [def, depth 90, in-statement, role type-annotation]
   2. `CategoryTheory.Precoverage.ZeroHypercover.toPreZeroHypercover`
      [def, depth 3, in-statement, role explicit-arg]
   3. `CategoryTheory.PreZeroHypercover.I₀`
      [def, depth 2, in-statement, role explicit-arg]
   4. `CategoryTheory.PreZeroHypercover.f`
      [def, depth 2, in-statement, role implicit-arg]
   5. `AlgebraicGeometry.Scheme.instCategory`
      [def, depth 89, in-statement, role instance-slot]
   6. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   7. `AlgebraicGeometry.Scheme.Cover.iUnion_range`
      [theorem, depth 93, introduced-by-proof, role explicit-arg]
   8. `AlgebraicGeometry.Scheme`
      [inductive, depth 0, in-statement, role explicit-arg]
   9. `CategoryTheory.PreZeroHypercover.X`
      [def, depth 2, in-statement, role implicit-arg]
  10. `AlgebraicGeometry.Surjective.sigmaDesc_of_union_range_eq_univ`
      [theorem, depth 162, introduced-by-proof, role applied]
  11. `AlgebraicGeometry.Scheme.precoverage`
      [def, depth 95, in-statement, role implicit-arg]
  12. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]

### proof_079  (target depth 9, band 0-10)

THEOREM PROVED: `isMinOn_iff`

Grade all 4 candidates below.

   1. `Set`
      [def, depth 0, in-statement, role type-annotation]
   2. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Iff.rfl`
      [theorem, depth 3, introduced-by-proof, role applied]
   4. `IsMinOn`
      [def, depth 8, in-statement, role implicit-arg]

### proof_080  (target depth 25, band 11-25)

THEOREM PROVED: `CategoryTheory.Limits.CokernelCofork.π_ofπ`

Grade all 17 candidates below.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   3. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   5. `CategoryTheory.Limits.WalkingParallelPair`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.Limits.walkingParallelPairHomCategory`
      [def, depth 13, in-statement, role instance-slot]
   8. `CategoryTheory.Limits.HasZeroMorphisms`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `CategoryTheory.Limits.Cofork.π`
      [def, depth 22, in-statement, role implicit-arg]
  10. `CategoryTheory.Limits.HasZeroMorphisms.zero`
      [def, depth 2, in-statement, role instance-slot]
  11. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `CategoryTheory.Limits.Cocone.pt`
      [def, depth 3, in-statement, role explicit-arg]
  13. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  14. `CategoryTheory.Limits.parallelPair`
      [def, depth 18, in-statement, role implicit-arg]
  15. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `CategoryTheory.Limits.CokernelCofork.ofπ`
      [def, depth 24, in-statement, role explicit-arg]
  17. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
