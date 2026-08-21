# Grading batch `testr_15` — 24 proofs

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

### proof_0337  (target depth 100, band 76-125)

THEOREM PROVED: `WithLp.toLp_fst`

Grade all 5 candidates.

   1. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `WithLp.fst`
      [def, depth 99, in-statement, role implicit-arg]
   3. `WithLp.toLp`
      [constructor, depth 98, in-statement, role explicit-arg]
   4. `rfl`
      [def, depth 2, in-statement, role applied]
   5. `ENNReal`
      [def, depth 96, in-statement, role type-annotation]

### proof_0338  (target depth 84, band 76-125)

THEOREM PROVED: `MvPolynomial.isEmptyRingEquiv_apply`

Grade all 24 candidates.

   1. `Finsupp.instAddMonoid`
      [def, depth 65, in-statement, role instance-slot]
   2. `AddMonoidAlgebra.semiring`
      [def, depth 80, in-statement, role instance-slot]
   3. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   4. `MvPolynomial.isEmptyRingEquiv`
      [def, depth 83, in-statement, role explicit-arg]
   5. `AddMonoidAlgebra`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Nat.instAddMonoid`
      [def, depth 16, in-statement, role instance-slot]
   7. `IsEmpty`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `RingEquiv.instEquivLike`
      [def, depth 16, in-statement, role instance-slot]
   9. `Nat.instMulZeroClass`
      [def, depth 17, in-statement, role instance-slot]
  10. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  11. `Distrib.toMul`
      [def, depth 1, in-statement, role instance-slot]
  12. `RingEquiv`
      [inductive, depth 1, in-statement, role implicit-arg]
  13. `AddMonoidAlgebra.instMul`
      [def, depth 70, in-statement, role instance-slot]
  14. `Finsupp.instAdd`
      [def, depth 62, in-statement, role instance-slot]
  15. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  16. `Finsupp`
      [inductive, depth 1, in-statement, role explicit-arg]
  17. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
  19. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
  20. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  21. `MvPolynomial`
      [def, depth 18, in-statement, role explicit-arg]
  22. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  23. `Distrib.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  24. `instDistribOfSemiring`
      [def, depth 11, in-statement, role instance-slot]

### proof_0339  (target depth 114, band 76-125)

THEOREM PROVED: `CommRingCat.Opposite.effectiveEpi_of_faithfullyFlat`

Grade all 24 candidates.

   1. `Iff.mp`
      [theorem, depth 1, introduced-by-proof, role applied]
   2. `CommRingCat.Hom.hom`
      [def, depth 23, in-statement, role explicit-arg]
   3. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `CommRingCat`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `CategoryTheory.Limits.WalkingPair`
      [inductive, depth 0, introduced-by-proof, role explicit-arg]
   6. `CommRingCat.instCommRingObjForgetRingHomCarrier`
      [def, depth 2, in-statement, role instance-slot]
   7. `CategoryTheory.Limits.WalkingCospan`
      [def, depth 2, introduced-by-proof, role implicit-arg]
   8. `CommRingCat.Opposite.regularEpiOfFaithfullyFlat`
      [theorem, depth 113, introduced-by-proof, role explicit-arg]
   9. `RingHom.FaithfullyFlat`
      [def, depth 19, in-statement, role type-annotation]
  10. `Quiver.Hom.unop`
      [def, depth 3, in-statement, role explicit-arg]
  11. `CommRingCat.carrier`
      [def, depth 1, in-statement, role implicit-arg]
  12. `CategoryTheory.IsRegularEpi`
      [inductive, depth 2, introduced-by-proof, role implicit-arg]
  13. `CategoryTheory.isRegularEpi_iff_effectiveEpi`
      [theorem, depth 31, introduced-by-proof, role explicit-arg]
  14. `CategoryTheory.Limits.fintypeWalkingPair`
      [def, depth 56, introduced-by-proof, role instance-slot]
  15. `Quiver.opposite`
      [def, depth 2, in-statement, role instance-slot]
  16. `CategoryTheory.Limits.WidePullbackShape.category`
      [def, depth 13, introduced-by-proof, role instance-slot]
  17. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
  18. `Opposite.unop`
      [def, depth 1, in-statement, role explicit-arg]
  19. `CommRingCat.instCategory`
      [def, depth 20, in-statement, role instance-slot]
  20. `CategoryTheory.Limits.cospan`
      [def, depth 16, introduced-by-proof, role explicit-arg]
  21. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  22. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  23. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  24. `CategoryTheory.EffectiveEpi`
      [inductive, depth 2, in-statement, role implicit-arg]

### proof_0340  (target depth 125, band 76-125)

THEOREM PROVED: `EReal.coe_ennreal_ne_one`

Grade all 10 candidates.

   1. `EReal`
      [def, depth 2, in-statement, role implicit-arg]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   3. `instOneEReal`
      [def, depth 87, in-statement, role instance-slot]
   4. `ENNReal.toEReal`
      [def, depth 98, in-statement, role explicit-arg]
   5. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
   6. `EReal.coe_ennreal_eq_one`
      [theorem, depth 124, introduced-by-proof, role explicit-arg]
   7. `ENNReal.instOne`
      [def, depth 104, in-statement, role instance-slot]
   8. `Iff.not`
      [theorem, depth 4, in-statement, role applied]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]

### proof_0341  (target depth 119, band 76-125)

THEOREM PROVED: `String.Slice.dropEndWhile_char_eq_dropEndWhile_beq`

Grade all 16 candidates.

   1. `String.Slice.Pattern.Char.instBackwardPatternChar`
      [def, depth 114, in-statement, role instance-slot]
   2. `id`
      [def, depth 0, in-statement, role applied]
   3. `BEq.beq`
      [def, depth 1, in-statement, role explicit-arg]
   4. `String.Slice.skipSuffixWhile_char_eq_skipSuffixWhile_beq`
      [theorem, depth 118, introduced-by-proof, role explicit-arg]
   5. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `String.Slice`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Char`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `String.Slice.Pos`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `instBEqOfDecidableEq`
      [def, depth 6, in-statement, role instance-slot]
  10. `Bool`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `String.Slice.Pattern.CharPred.instBackwardPatternForallCharBool`
      [def, depth 113, in-statement, role instance-slot]
  12. `String.Slice.dropEndWhile`
      [def, depth 23, in-statement, role explicit-arg]
  13. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  14. `String.Slice.skipSuffixWhile`
      [def, depth 22, in-statement, role implicit-arg]
  15. `String.Slice.sliceTo`
      [def, depth 12, in-statement, role explicit-arg]
  16. `instDecidableEqChar`
      [def, depth 22, in-statement, role instance-slot]

### proof_0342  (target depth 110, band 76-125)

THEOREM PROVED: `Tactic.ComputeAsymptotics.UnitMonomial.FirstNonzeroIsPos.not_nil`

Grade all 18 candidates.

   1. `Tactic.ComputeAsymptotics.UnitMonomial.FirstNonzeroIsPos`
      [def, depth 109, in-statement, role explicit-arg]
   2. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `noConfusion_of_Nat`
      [theorem, depth 9, in-statement, role explicit-arg]
   5. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Tactic.ComputeAsymptotics.UnitMonomial.Sign.zero`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `not_false_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
  10. `Tactic.ComputeAsymptotics.UnitMonomial.Sign`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `eq_false'`
      [theorem, depth 4, in-statement, role explicit-arg]
  12. `Tactic.ComputeAsymptotics.UnitMonomial.Sign.pos`
      [constructor, depth 1, in-statement, role explicit-arg]
  13. `Not`
      [def, depth 1, in-statement, role implicit-arg]
  14. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
  15. `Tactic.ComputeAsymptotics.UnitMonomial.Sign.ctorIdx`
      [def, depth 4, introduced-by-proof, role explicit-arg]
  16. `False.elim`
      [def, depth 2, in-statement, role explicit-arg]
  17. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  18. `False`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0343  (target depth 87, band 76-125)

THEOREM PROVED: `CartanMatrix.G₂_det`

Grade all 19 candidates.

   1. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `id`
      [def, depth 0, in-statement, role explicit-arg]
   3. `instOfNat`
      [def, depth 3, in-statement, role instance-slot]
   4. `Int.instDecidableEq`
      [def, depth 13, in-statement, role instance-slot]
   5. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `CartanMatrix.G₂`
      [def, depth 31, in-statement, role explicit-arg]
   8. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  10. `instDecidableEqFin`
      [def, depth 12, in-statement, role instance-slot]
  11. `Int.instCommRing`
      [def, depth 36, in-statement, role instance-slot]
  12. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]
  13. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  15. `Matrix.det`
      [def, depth 86, in-statement, role explicit-arg]
  16. `of_decide_eq_true`
      [theorem, depth 7, in-statement, role applied]
  17. `Fin.fintype`
      [def, depth 55, in-statement, role instance-slot]
  18. `Decidable.decide`
      [def, depth 5, in-statement, role explicit-arg]
  19. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0344  (target depth 106, band 76-125)

THEOREM PROVED: `FormalGroup.zero_apply`

Grade all 10 candidates.

   1. `FormalGroup`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `MvPowerSeries`
      [def, depth 18, in-statement, role implicit-arg]
   3. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `FormalGroup.instZeroPoint`
      [def, depth 105, in-statement, role instance-slot]
   5. `FormalGroup.Point`
      [def, depth 93, in-statement, role implicit-arg]
   6. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   7. `rfl`
      [def, depth 2, in-statement, role applied]
   8. `PowerSeries.HasSubst`
      [def, depth 92, in-statement, role implicit-arg]
   9. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  10. `Subtype.val`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0345  (target depth 108, band 76-125)

THEOREM PROVED: `unitInterval.le_symm_comm`

Grade all 20 candidates.

   1. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
   2. `Iff.rfl`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   5. `unitInterval.symm_le_symm`
      [theorem, depth 107, introduced-by-proof, role explicit-arg]
   6. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `Real.instLE`
      [def, depth 94, in-statement, role instance-slot]
   8. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   9. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  10. `Set.Elem`
      [def, depth 4, in-statement, role implicit-arg]
  11. `unitInterval.symm`
      [def, depth 106, in-statement, role explicit-arg]
  12. `Iff`
      [inductive, depth 0, in-statement, role explicit-arg]
  13. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  14. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  15. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  16. `id`
      [def, depth 0, in-statement, role explicit-arg]
  17. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `unitInterval.symm_symm`
      [theorem, depth 107, introduced-by-proof, role explicit-arg]
  19. `unitInterval`
      [def, depth 102, in-statement, role explicit-arg]
  20. `Subtype.instLE`
      [def, depth 2, in-statement, role instance-slot]

### proof_0346  (target depth 115, band 76-125)

THEOREM PROVED: `Real.HolderConjugate.toNNReal`

Grade all 13 candidates.

   1. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   3. `NNReal.HolderTriple`
      [inductive, depth 96, in-statement, role implicit-arg]
   4. `Eq.mp`
      [def, depth 3, in-statement, role applied]
   5. `Real.instOne`
      [def, depth 85, in-statement, role instance-slot]
   6. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `NNReal.instOne`
      [def, depth 103, in-statement, role instance-slot]
   8. `Real.HolderConjugate`
      [def, depth 86, in-statement, role type-annotation]
   9. `NNReal`
      [def, depth 95, in-statement, role implicit-arg]
  10. `Real.toNNReal_one`
      [theorem, depth 108, introduced-by-proof, role explicit-arg]
  11. `Real.toNNReal`
      [def, depth 107, in-statement, role explicit-arg]
  12. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
  13. `Real.HolderTriple.toNNReal`
      [theorem, depth 114, introduced-by-proof, role explicit-arg]

### proof_0347  (target depth 96, band 76-125)

THEOREM PROVED: `Set.Finite.ecard_strictMonoOn`

Grade all 6 candidates.

   1. `Set.ofPred`
      [def, depth 1, in-statement, role explicit-arg]
   2. `Set.Finite.ecard_lt_ecard`
      [theorem, depth 95, introduced-by-proof, role applied]
   3. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   4. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   5. `Set.Finite`
      [def, depth 5, in-statement, role explicit-arg]
   6. `Set`
      [def, depth 0, in-statement, role implicit-arg]

### proof_0348  (target depth 84, band 76-125)

THEOREM PROVED: `rank_le_card`

Grade all 24 candidates.

   1. `Cardinal.instLE`
      [def, depth 20, in-statement, role instance-slot]
   2. `Module.rank_def`
      [theorem, depth 83, introduced-by-proof, role explicit-arg]
   3. `ConditionallyCompleteLinearOrderBot.toConditionallyCompleteLinearOrder`
      [def, depth 1, in-statement, role instance-slot]
   4. `id`
      [def, depth 0, in-statement, role explicit-arg]
   5. `iSup`
      [def, depth 3, in-statement, role implicit-arg]
   6. `Module.rank`
      [def, depth 82, in-statement, role implicit-arg]
   7. `ConditionallyCompletePartialOrderSup.toSupSet`
      [def, depth 1, in-statement, role instance-slot]
   8. `Cardinal.mk_set_le`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   9. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Eq.trans_le`
      [theorem, depth 5, in-statement, role applied]
  11. `ConditionallyCompleteLattice.toConditionallyCompletePartialOrder`
      [def, depth 8, in-statement, role instance-slot]
  12. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
  14. `Cardinal.mk`
      [def, depth 18, in-statement, role implicit-arg]
  15. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `LinearIndepOn`
      [def, depth 78, in-statement, role explicit-arg]
  17. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  18. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
  19. `Cardinal.instConditionallyCompleteLinearOrderBot`
      [def, depth 74, in-statement, role instance-slot]
  20. `ConditionallyCompletePartialOrder.toConditionallyCompletePartialOrderSup`
      [def, depth 1, in-statement, role instance-slot]
  21. `Cardinal`
      [def, depth 18, in-statement, role implicit-arg]
  22. `ciSup_le'`
      [theorem, depth 30, introduced-by-proof, role explicit-arg]
  23. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  24. `ConditionallyCompleteLinearOrder.toConditionallyCompleteLattice`
      [def, depth 1, in-statement, role instance-slot]

### proof_0349  (target depth 76, band 76-125)

THEOREM PROVED: `Homeomorph.uniqueProd_symm_apply_snd`

Grade all 12 candidates.

   1. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   3. `Homeomorph.instEquivLike`
      [def, depth 15, in-statement, role instance-slot]
   4. `Homeomorph.uniqueProd`
      [def, depth 75, in-statement, role explicit-arg]
   5. `Homeomorph.symm`
      [def, depth 11, in-statement, role explicit-arg]
   6. `Prod.snd`
      [def, depth 1, in-statement, role explicit-arg]
   7. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `instTopologicalSpaceProd`
      [def, depth 64, in-statement, role instance-slot]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  10. `Unique`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  12. `Homeomorph`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0350  (target depth 89, band 76-125)

THEOREM PROVED: `CommRingCat.moduleCatExtendScalarsPseudofunctor_obj`

Grade all 17 candidates.

   1. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   2. `CategoryTheory.locallyDiscreteBicategory`
      [def, depth 14, in-statement, role instance-slot]
   3. `CommRingCat.instCategory`
      [def, depth 20, in-statement, role instance-slot]
   4. `CategoryTheory.Bicategory.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.Pseudofunctor.toPrelaxFunctor`
      [def, depth 2, in-statement, role explicit-arg]
   6. `CommRingCat`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   8. `Prefunctor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   9. `CategoryTheory.PrelaxFunctor.toPrelaxFunctorStruct`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CategoryTheory.LocallyDiscrete`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  12. `CategoryTheory.Cat`
      [def, depth 1, in-statement, role implicit-arg]
  13. `CommRingCat.moduleCatExtendScalarsPseudofunctor`
      [def, depth 88, in-statement, role explicit-arg]
  14. `CategoryTheory.PrelaxFunctorStruct.toPrefunctor`
      [def, depth 3, in-statement, role explicit-arg]
  15. `CategoryTheory.Cat.bicategory`
      [def, depth 29, in-statement, role instance-slot]
  16. `CategoryTheory.Bicategory.homCategory`
      [def, depth 1, in-statement, role instance-slot]
  17. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]

### proof_0351  (target depth 76, band 76-125)

THEOREM PROVED: `CompletelyNormalSpace.of_forall_normalSpace`

Grade all 10 candidates.

   1. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   3. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   4. `NormalSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `instTopologicalSpaceSubtype`
      [def, depth 64, in-statement, role instance-slot]
   6. `CompletelyNormalSpace`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
  10. `completelyNormalSpace_iff_forall_normalSpace`
      [theorem, depth 75, introduced-by-proof, role explicit-arg]

### proof_0352  (target depth 96, band 76-125)

THEOREM PROVED: `Polynomial.taylor_one`

Grade all 8 candidates.

   1. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
   3. `AddCommMonoidWithOne.toAddMonoidWithOne`
      [def, depth 1, in-statement, role instance-slot]
   4. `Polynomial.taylor_C`
      [theorem, depth 95, introduced-by-proof, role applied]
   5. `AddMonoidWithOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
   6. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   7. `NonAssocSemiring.toAddCommMonoidWithOne`
      [def, depth 10, in-statement, role instance-slot]
   8. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]

### proof_0353  (target depth 80, band 76-125)

THEOREM PROVED: `HasCompactMulSupport.comp_homeomorph`

Grade all 9 candidates.

   1. `HasCompactMulSupport`
      [def, depth 50, in-statement, role type-annotation]
   2. `Homeomorph.isClosedEmbedding`
      [theorem, depth 76, introduced-by-proof, role explicit-arg]
   3. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   4. `Homeomorph.instEquivLike`
      [def, depth 15, in-statement, role instance-slot]
   5. `One`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `HasCompactMulSupport.comp_isClosedEmbedding`
      [theorem, depth 79, introduced-by-proof, role applied]
   7. `Homeomorph`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   9. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0354  (target depth 79, band 76-125)

THEOREM PROVED: `Finset.vsub_inter_subset`

Grade all 5 candidates.

   1. `Finset`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Finset.image₂_inter_subset_right`
      [theorem, depth 78, introduced-by-proof, role applied]
   3. `VSub.vsub`
      [def, depth 2, in-statement, role implicit-arg]
   4. `VSub`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]

### proof_0355  (target depth 78, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.Const.getKeyD_filterMap`

Grade all 8 candidates.

   1. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, in-statement, role explicit-arg]
   4. `Option`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   6. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
   7. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   8. `Std.DTreeMap.Internal.Impl.Const.getKeyD_filterMap!`
      [theorem, depth 77, introduced-by-proof, role applied]

### proof_0356  (target depth 97, band 76-125)

THEOREM PROVED: `powCoprime_symm_apply`

Grade all 11 candidates.

   1. `Nat.card`
      [def, depth 89, in-statement, role explicit-arg]
   2. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   5. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   6. `Nat.Coprime`
      [def, depth 25, in-statement, role type-annotation]
   7. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Equiv.symm`
      [def, depth 10, in-statement, role explicit-arg]
  10. `powCoprime`
      [def, depth 96, in-statement, role explicit-arg]
  11. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]

### proof_0357  (target depth 121, band 76-125)

THEOREM PROVED: `BoxIntegral.Box.ne_of_disjoint_coe`

Grade all 22 candidates.

   1. `BoxIntegral.Box.coe_ne_empty`
      [theorem, depth 105, introduced-by-proof, role explicit-arg]
   2. `BoxIntegral.Box.coe_inj`
      [theorem, depth 120, introduced-by-proof, role explicit-arg]
   3. `ConditionallyCompletePartialOrderSup.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   4. `ConditionallyCompleteLattice.toConditionallyCompletePartialOrder`
      [def, depth 8, in-statement, role instance-slot]
   5. `Real`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `ConditionallyCompletePartialOrder.toConditionallyCompletePartialOrderSup`
      [def, depth 1, in-statement, role instance-slot]
   7. `Disjoint`
      [def, depth 3, in-statement, role type-annotation]
   8. `Order.Frame.toHeytingAlgebra`
      [def, depth 4, in-statement, role instance-slot]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `CompleteLattice.toConditionallyCompleteLattice`
      [def, depth 9, in-statement, role instance-slot]
  11. `CompleteBooleanAlgebra.toCompleteDistribLattice`
      [def, depth 55, in-statement, role instance-slot]
  12. `HeytingAlgebra.toOrderBot`
      [def, depth 1, in-statement, role instance-slot]
  13. `Disjoint.ne`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  14. `CompleteBooleanAlgebra.toCompleteLattice`
      [def, depth 1, in-statement, role instance-slot]
  15. `mt`
      [theorem, depth 2, in-statement, role applied]
  16. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`
      [def, depth 1, in-statement, role instance-slot]
  17. `BoxIntegral.Box.toSet`
      [def, depth 103, in-statement, role explicit-arg]
  18. `Iff.mpr`
      [theorem, depth 1, in-statement, role explicit-arg]
  19. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  20. `BoxIntegral.Box`
      [inductive, depth 0, in-statement, role type-annotation]
  21. `Set.instCompleteAtomicBooleanAlgebra`
      [def, depth 58, in-statement, role instance-slot]
  22. `CompleteDistribLattice.toFrame`
      [def, depth 1, in-statement, role instance-slot]

### proof_0358  (target depth 76, band 76-125)

THEOREM PROVED: `Continuous.units_map`

Grade all 24 candidates.

   1. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
   2. `Continuous.comp`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Inv.inv`
      [def, depth 1, in-statement, role explicit-arg]
   5. `Units`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `Units.instTopologicalSpaceUnits`
      [def, depth 65, in-statement, role instance-slot]
   7. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   8. `Units.inv`
      [def, depth 2, in-statement, role implicit-arg]
   9. `Monoid`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Units.val`
      [def, depth 2, in-statement, role explicit-arg]
  11. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Units.instMulOneClass`
      [def, depth 13, in-statement, role instance-slot]
  13. `And.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
  14. `Units.continuous_val`
      [theorem, depth 73, introduced-by-proof, role explicit-arg]
  15. `Units.map`
      [def, depth 22, in-statement, role explicit-arg]
  16. `Units.instInv`
      [def, depth 7, in-statement, role instance-slot]
  17. `MonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]
  18. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
  19. `MonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
  20. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  21. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  22. `Continuous`
      [inductive, depth 1, in-statement, role implicit-arg]
  23. `Units.continuous_iff`
      [theorem, depth 74, introduced-by-proof, role explicit-arg]
  24. `Units.continuous_coe_inv`
      [theorem, depth 75, introduced-by-proof, role explicit-arg]

### proof_0359  (target depth 79, band 76-125)

THEOREM PROVED: `Primrec.nat_rec'`

Grade all 12 candidates.

   1. `Prod.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Primrec₂`
      [def, depth 76, in-statement, role type-annotation]
   3. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Primcodable.prod`
      [def, depth 75, in-statement, role instance-slot]
   5. `Primrec.nat_rec`
      [theorem, depth 78, introduced-by-proof, role explicit-arg]
   6. `Denumerable.nat`
      [def, depth 6, in-statement, role instance-slot]
   7. `Primcodable`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Primrec₂.comp`
      [theorem, depth 77, introduced-by-proof, role applied]
   9. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
  10. `Primrec`
      [def, depth 8, in-statement, role type-annotation]
  11. `Primrec.id`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
  12. `Primcodable.ofDenumerable`
      [def, depth 18, in-statement, role instance-slot]

### proof_0360  (target depth 78, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.Const.getKey!_unitOfList_of_mem`

Grade all 11 candidates.

   1. `Ordering`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   3. `Not`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Ordering.eq`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   6. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `List.Pairwise`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `List.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  10. `Std.DTreeMap.Internal.Impl.Const.getKey!_insertManyIfNewUnit_empty_list_of_mem`
      [theorem, depth 77, introduced-by-proof, role applied]
  11. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
