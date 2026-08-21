# Grading batch `testc_22` — 24 proofs

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

## Stage 3 — for this batch only: why is it a defect?

For every candidate you graded **0 or 1**, add a cause code:

| code | meaning |
|---|---|
| `A` | Generated proof obligation or private/internal helper |
| `B` | Wrapper/forwarder that just routes to a more useful boundary |
| `C` | Irrelevant instance / typeclass / interface plumbing |
| `D` | Tactic or certificate machinery (explains Lean's automation, not the maths) |
| `E` | Incidental logic/equality assembly (context-dependent) |
| `F` | Depth-inflated: looks deep structurally, but its mathematical role here is background |
| `G` | Other — name it in one short phrase |

Put these in a `causes` map from candidate number to code.

## Output format

Return **only** a JSON object, no commentary:

```json
{
  "proof_0007": {
    "moves": "Rewrites along commutativity of addition, then closes by reflexivity.",
    "grades": {"1": 1, "2": 4, "3": 0, "4": 3, "5": 2},
    "missing_key": false,
    "confidence": "high",
    "causes": {"1": "C", "3": "A"}
  }
}
```

Every proof id in your batch must appear exactly once, and every candidate
number of that proof must appear exactly once in its `grades` map.


---

### proof_0505  (target depth 132, band 126+)

THEOREM PROVED: `Algebra.IsAlgebraic.trans_isIntegral`

Grade all 19 candidates.

   1. `Algebra.IsIntegral`
      [inductive, depth 6, in-statement, role type-annotation]
   2. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
   4. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   5. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
   6. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Distrib.toMul`
      [def, depth 1, in-statement, role instance-slot]
   8. `Algebra.IsIntegral.isIntegral`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   9. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  10. `IsScalarTower`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Algebra.IsAlgebraic`
      [inductive, depth 6, in-statement, role type-annotation]
  12. `NoZeroDivisors`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `instMulZeroClassOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
  15. `CommRing.toRing`
      [def, depth 1, in-statement, role instance-slot]
  16. `Algebra.toSMul`
      [def, depth 2, in-statement, role instance-slot]
  17. `Algebra.IsAlgebraic.mk`
      [constructor, depth 103, introduced-by-proof, role applied]
  18. `IsIntegral.trans_isAlgebraic`
      [theorem, depth 131, introduced-by-proof, role explicit-arg]
  19. `instDistribOfSemiring`
      [def, depth 11, in-statement, role instance-slot]

### proof_0506  (target depth 16, band 11-25)

THEOREM PROVED: `SimpleGraph.IsVertexCover.subset`

Grade all 6 candidates.

   1. `Set`
      [def, depth 0, in-statement, role type-annotation]
   2. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   3. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]
   4. `_private.Mathlib.Combinatorics.SimpleGraph.VertexCover.0.SimpleGraph.IsVertexCover.subset._proof_1_2`
      [theorem, depth 15, introduced-by-proof, role applied]
   5. `SimpleGraph.IsVertexCover`
      [def, depth 4, in-statement, role type-annotation]
   6. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0507  (target depth 79, band 76-125)

THEOREM PROVED: `QuotientAddGroup.quotientKerEquivRange._proof_2`

Grade all 25 candidates.

   1. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   2. `AddSubgroup.instSetLike`
      [def, depth 16, in-statement, role instance-slot]
   3. `Function.Injective`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   5. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   6. `SubNegMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
   7. `QuotientAddGroup.instHasQuotientAddSubgroup`
      [def, depth 66, in-statement, role instance-slot]
   8. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   9. `HasQuotient.Quotient`
      [def, depth 2, in-statement, role explicit-arg]
  10. `QuotientAddGroup.rangeKerLift_injective`
      [theorem, depth 78, introduced-by-proof, role explicit-arg]
  11. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
  12. `And.intro`
      [constructor, depth 1, in-statement, role applied]
  13. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  14. `AddMonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]
  15. `AddMonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
  16. `QuotientAddGroup.rangeKerLift`
      [def, depth 77, in-statement, role explicit-arg]
  17. `QuotientAddGroup.Quotient.addGroup`
      [def, depth 69, in-statement, role instance-slot]
  18. `Function.Surjective`
      [def, depth 1, in-statement, role implicit-arg]
  19. `AddSubgroup`
      [inductive, depth 1, in-statement, role implicit-arg]
  20. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  21. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
  22. `AddMonoidHom.range`
      [def, depth 22, in-statement, role explicit-arg]
  23. `QuotientAddGroup.rangeKerLift_surjective`
      [theorem, depth 78, introduced-by-proof, role explicit-arg]
  24. `AddSubgroup.toAddGroup`
      [def, depth 18, in-statement, role instance-slot]
  25. `AddMonoidHom.ker`
      [def, depth 17, in-statement, role explicit-arg]

### proof_0508  (target depth 194, band 126+)

THEOREM PROVED: `MeasureTheory.vaddInvariantMeasure_map_vadd`

Grade all 11 candidates.

   1. `MeasurableConstVAdd.measurable_const_vadd`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   2. `HVAdd.hVAdd`
      [def, depth 2, in-statement, role explicit-arg]
   3. `MeasurableConstVAdd`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `VAdd`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `VAddCommClass.vadd_comm`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   7. `instHVAdd`
      [def, depth 3, in-statement, role instance-slot]
   8. `MeasureTheory.vaddInvariantMeasure_map`
      [theorem, depth 193, introduced-by-proof, role applied]
   9. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `MeasureTheory.VAddInvariantMeasure`
      [inductive, depth 2, in-statement, role type-annotation]
  11. `VAddCommClass`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0509  (target depth 67, band 51-75)

THEOREM PROVED: `tendsto_nhds_bot_mono'`

Grade all 14 candidates.

   1. `nhds`
      [def, depth 18, in-statement, role explicit-arg]
   2. `OrderBot`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `tendsto_nhds_bot_mono`
      [theorem, depth 66, introduced-by-proof, role applied]
   5. `Pi.hasLe`
      [def, depth 2, in-statement, role instance-slot]
   6. `Filter.Tendsto`
      [def, depth 13, in-statement, role type-annotation]
   7. `OrderTopology`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  10. `Bot.bot`
      [def, depth 1, in-statement, role explicit-arg]
  11. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
  12. `Filter`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `OrderBot.toBot`
      [def, depth 2, in-statement, role instance-slot]
  14. `Filter.Eventually.of_forall`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]

### proof_0510  (target depth 32, band 26-50)

THEOREM PROVED: `CategoryTheory.CartesianMonoidalCategory.lift_snd_comp_fst_comp_assoc`

Grade all 25 candidates.

   1. `CategoryTheory.CartesianMonoidalCategory.lift`
      [def, depth 26, in-statement, role explicit-arg]
   2. `CategoryTheory.SemiCartesianMonoidalCategory.fst`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `CategoryTheory.CartesianMonoidalCategory.toSemiCartesianMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
   5. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]
   6. `CategoryTheory.BraidedCategory.braiding`
      [def, depth 3, in-statement, role explicit-arg]
   7. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   8. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   9. `CategoryTheory.Category.assoc`
      [theorem, depth 1, in-statement, role explicit-arg]
  10. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  11. `id`
      [def, depth 0, in-statement, role applied]
  12. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  13. `CategoryTheory.SemiCartesianMonoidalCategory.toMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
  14. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
  15. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  16. `CategoryTheory.SemiCartesianMonoidalCategory.snd`
      [def, depth 2, in-statement, role explicit-arg]
  17. `CategoryTheory.CartesianMonoidalCategory.lift_snd_comp_fst_comp`
      [theorem, depth 31, introduced-by-proof, role explicit-arg]
  18. `CategoryTheory.MonoidalCategoryStruct.tensorObj`
      [def, depth 2, in-statement, role implicit-arg]
  19. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  20. `CategoryTheory.MonoidalCategoryStruct.tensorHom`
      [def, depth 2, in-statement, role explicit-arg]
  21. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  22. `CategoryTheory.CartesianMonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
  23. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  24. `CategoryTheory.BraidedCategory`
      [inductive, depth 2, in-statement, role type-annotation]
  25. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]

### proof_0511  (target depth 21, band 11-25)

THEOREM PROVED: `CategoryTheory.Bicategory.Pith.comp₂_iso_inv_assoc`

Grade all 23 candidates.

   1. `CategoryTheory.CoreHom.iso`
      [def, depth 2, in-statement, role explicit-arg]
   2. `CategoryTheory.Groupoid.toCategory`
      [def, depth 1, in-statement, role instance-slot]
   3. `CategoryTheory.Bicategory.Pith.categoryStruct`
      [def, depth 3, in-statement, role instance-slot]
   4. `CategoryTheory.Bicategory.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.Bicategory.homCategory`
      [def, depth 1, in-statement, role instance-slot]
   6. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   7. `CategoryTheory.Bicategory.Pith.as`
      [def, depth 1, in-statement, role explicit-arg]
   8. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   9. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  10. `CategoryTheory.Core.of`
      [def, depth 1, in-statement, role implicit-arg]
  11. `CategoryTheory.Category.assoc`
      [theorem, depth 1, in-statement, role explicit-arg]
  12. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `CategoryTheory.Bicategory`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  15. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
  16. `CategoryTheory.Bicategory.Pith`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  18. `CategoryTheory.Bicategory.Pith.homGroupoid`
      [def, depth 19, in-statement, role instance-slot]
  19. `CategoryTheory.Bicategory.Pith.comp₂_iso_inv`
      [theorem, depth 20, introduced-by-proof, role explicit-arg]
  20. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `id`
      [def, depth 0, in-statement, role applied]
  22. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  23. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]

### proof_0512  (target depth 64, band 51-75)

THEOREM PROVED: `Filter.Tendsto.inv_inv`

Grade all 25 candidates.

   1. `MonoidHomClass`
      [inductive, depth 3, in-statement, role type-annotation]
   2. `Filter.inv_le_inv`
      [theorem, depth 63, introduced-by-proof, role explicit-arg]
   3. `DivisionMonoid.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
   4. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   5. `Filter.instPartialOrder`
      [def, depth 12, in-statement, role instance-slot]
   6. `DivisionMonoid.toDivInvOneMonoid`
      [def, depth 9, in-statement, role instance-slot]
   7. `Eq.trans_le`
      [theorem, depth 5, introduced-by-proof, role applied]
   8. `DivInvOneMonoid.toInvOneClass`
      [def, depth 5, in-statement, role instance-slot]
   9. `InvOneClass.toInv`
      [def, depth 1, in-statement, role instance-slot]
  10. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  12. `Filter.map_inv'`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
  13. `FunLike`
      [def, depth 2, in-statement, role type-annotation]
  14. `Filter.map`
      [def, depth 8, in-statement, role implicit-arg]
  15. `Group.toDivisionMonoid`
      [def, depth 11, in-statement, role instance-slot]
  16. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Filter.instInv`
      [def, depth 9, in-statement, role instance-slot]
  18. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  19. `Filter.Tendsto`
      [def, depth 13, in-statement, role type-annotation]
  20. `Inv.inv`
      [def, depth 1, in-statement, role implicit-arg]
  21. `DivisionMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  22. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  23. `Filter`
      [inductive, depth 0, in-statement, role implicit-arg]
  24. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  25. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]

### proof_0513  (target depth 82, band 76-125)

THEOREM PROVED: `NNRat.coe_one`

Grade all 13 candidates.

   1. `Rat`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `rfl`
      [def, depth 2, in-statement, role applied]
   3. `Rat.instNNRatCast`
      [def, depth 41, in-statement, role instance-slot]
   4. `NNRat`
      [def, depth 39, in-statement, role implicit-arg]
   5. `NonAssocSemiring.toAddCommMonoidWithOne`
      [def, depth 10, in-statement, role instance-slot]
   6. `AddCommMonoidWithOne.toAddMonoidWithOne`
      [def, depth 1, in-statement, role instance-slot]
   7. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
   8. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   9. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  10. `NNRat.cast`
      [def, depth 2, in-statement, role implicit-arg]
  11. `AddMonoidWithOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
  12. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  13. `instCommSemiringNNRat`
      [def, depth 81, in-statement, role instance-slot]

### proof_0514  (target depth 100, band 76-125)

THEOREM PROVED: `String.Pos.skip?_eq_skip?_toSlice`

Grade all 6 candidates.

   1. `String.Pos`
      [inductive, depth 1, in-statement, role explicit-arg]
   2. `String.Slice.Pattern.ForwardPattern`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `String.Pos.skip?`
      [def, depth 99, in-statement, role implicit-arg]
   5. `rfl`
      [def, depth 2, in-statement, role applied]
   6. `String`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0515  (target depth 110, band 76-125)

THEOREM PROVED: `ENNReal.ofReal_le_ofReal_iff`

Grade all 25 candidates.

   1. `Real.instZero`
      [def, depth 85, in-statement, role instance-slot]
   2. `id`
      [def, depth 0, in-statement, role explicit-arg]
   3. `NNReal`
      [def, depth 95, in-statement, role implicit-arg]
   4. `Real.toNNReal_le_toNNReal_iff`
      [theorem, depth 108, introduced-by-proof, role explicit-arg]
   5. `Iff.rfl`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   8. `Real.toNNReal`
      [def, depth 107, in-statement, role explicit-arg]
   9. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
  10. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  11. `ENNReal.instLE`
      [def, depth 104, in-statement, role instance-slot]
  12. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `NNReal.instPartialOrder`
      [def, depth 102, in-statement, role instance-slot]
  14. `ENNReal.ofReal.eq_1`
      [theorem, depth 109, introduced-by-proof, role explicit-arg]
  15. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
  16. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  17. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  18. `Iff`
      [inductive, depth 0, in-statement, role explicit-arg]
  19. `ENNReal.ofReal`
      [def, depth 108, in-statement, role explicit-arg]
  20. `ENNReal.ofNNReal`
      [def, depth 96, in-statement, role explicit-arg]
  21. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
  22. `Real.instLE`
      [def, depth 94, in-statement, role instance-slot]
  23. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  24. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  25. `ENNReal.coe_le_coe`
      [theorem, depth 103, introduced-by-proof, role explicit-arg]

### proof_0516  (target depth 84, band 76-125)

THEOREM PROVED: `Equiv.Perm.SameCycle.mem_support_iff`

Grade all 18 candidates.

   1. `Iff.mpr`
      [theorem, depth 1, in-statement, role explicit-arg]
   2. `Equiv.Perm`
      [def, depth 1, in-statement, role type-annotation]
   3. `Equiv.Perm.instDecidableRelSameCycle`
      [def, depth 82, introduced-by-proof, role instance-slot]
   4. `Equiv.Perm.cycleOf`
      [def, depth 34, introduced-by-proof, role explicit-arg]
   5. `Equiv.Perm.support`
      [def, depth 26, in-statement, role explicit-arg]
   6. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
   7. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   8. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   9. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `And.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Equiv.Perm.mem_support_cycleOf_iff`
      [theorem, depth 83, introduced-by-proof, role explicit-arg]
  13. `Equiv.Perm.support_cycleOf_le`
      [theorem, depth 83, introduced-by-proof, role explicit-arg]
  14. `Equiv.Perm.SameCycle`
      [def, depth 21, in-statement, role explicit-arg]
  15. `Equiv.Perm.SameCycle.symm`
      [theorem, depth 23, introduced-by-proof, role explicit-arg]
  16. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  17. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
  18. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0517  (target depth 76, band 76-125)

THEOREM PROVED: `Finset.seqRight_def`

Grade all 7 candidates.

   1. `SeqRight.seqRight`
      [def, depth 1, in-statement, role implicit-arg]
   2. `Applicative.toSeqRight`
      [def, depth 1, in-statement, role instance-slot]
   3. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Unit`
      [def, depth 1, in-statement, role type-annotation]
   5. `rfl`
      [def, depth 2, in-statement, role applied]
   6. `Decidable`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Finset.applicative`
      [def, depth 75, in-statement, role instance-slot]

### proof_0518  (target depth 79, band 76-125)

THEOREM PROVED: `Std.ExtDTreeMap.get?_insert`

Grade all 20 candidates.

   1. `Std.DTreeMap.get?_insert`
      [theorem, depth 76, introduced-by-proof, role explicit-arg]
   2. `Std.ExtDTreeMap.inductionOn`
      [theorem, depth 27, introduced-by-proof, role applied]
   3. `Not`
      [def, depth 1, in-statement, role type-annotation]
   4. `Std.ExtDTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   5. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `cast`
      [def, depth 3, in-statement, role explicit-arg]
   7. `Std.DTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   8. `dite`
      [def, depth 5, in-statement, role explicit-arg]
   9. `Std.ExtDTreeMap.get?`
      [def, depth 77, in-statement, role explicit-arg]
  10. `Ordering`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Std.LawfulEqCmp.compare_eq_iff_eq`
      [theorem, depth 3, in-statement, role explicit-arg]
  12. `Option.some`
      [constructor, depth 1, in-statement, role explicit-arg]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `instDecidableEqOrdering`
      [def, depth 12, in-statement, role instance-slot]
  15. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
  17. `Std.LawfulEqCmp`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `Ordering.eq`
      [constructor, depth 1, in-statement, role explicit-arg]
  19. `Std.ExtDTreeMap.insert`
      [def, depth 78, in-statement, role explicit-arg]
  20. `Iff.mp`
      [theorem, depth 1, in-statement, role explicit-arg]

### proof_0519  (target depth 176, band 126+)

THEOREM PROVED: `condensedSetToTopCat_map`

Grade all 21 candidates.

   1. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   2. `CompHausLike.category`
      [def, depth 20, in-statement, role instance-slot]
   3. `CompHaus`
      [def, depth 2, in-statement, role explicit-arg]
   4. `TopCat.instCategory`
      [def, depth 18, in-statement, role instance-slot]
   5. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   6. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   8. `CondensedSet.toTopCat`
      [def, depth 171, in-statement, role explicit-arg]
   9. `Opposite`
      [inductive, depth 0, in-statement, role explicit-arg]
  10. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  11. `CategoryTheory.types`
      [def, depth 10, in-statement, role instance-slot]
  12. `CondensedSet`
      [def, depth 167, in-statement, role implicit-arg]
  13. `condensedSetToTopCat`
      [def, depth 175, in-statement, role explicit-arg]
  14. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  15. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  16. `CategoryTheory.Functor.map`
      [def, depth 2, in-statement, role explicit-arg]
  17. `TopCat`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `CategoryTheory.ObjectProperty.FullSubcategory.category`
      [def, depth 10, in-statement, role instance-slot]
  19. `True`
      [inductive, depth 0, in-statement, role explicit-arg]
  20. `CategoryTheory.Presheaf.IsSheaf`
      [def, depth 28, in-statement, role explicit-arg]
  21. `CategoryTheory.coherentTopology`
      [def, depth 30, in-statement, role explicit-arg]

### proof_0520  (target depth 93, band 76-125)

THEOREM PROVED: `Subfield.relrank_comap_comap_eq_relrank_of_le`

Grade all 23 candidates.

   1. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   2. `Subfield`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   4. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   5. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   6. `Eq.mp`
      [def, depth 3, in-statement, role applied]
   7. `Cardinal.lift`
      [def, depth 21, in-statement, role explicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
  10. `Subfield.relrank`
      [def, depth 83, in-statement, role explicit-arg]
  11. `Subfield.instPartialOrder`
      [def, depth 50, in-statement, role instance-slot]
  12. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `Subfield.comap`
      [def, depth 54, in-statement, role explicit-arg]
  14. `Cardinal`
      [def, depth 18, in-statement, role implicit-arg]
  15. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  17. `RingHom.fieldRange`
      [def, depth 54, in-statement, role explicit-arg]
  18. `RingHom`
      [inductive, depth 1, in-statement, role type-annotation]
  19. `Field`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
  21. `Field.toDivisionRing`
      [def, depth 44, in-statement, role instance-slot]
  22. `Subfield.lift_relrank_comap_comap_eq_lift_relrank_of_le`
      [theorem, depth 92, introduced-by-proof, role explicit-arg]
  23. `Cardinal.lift_id`
      [theorem, depth 23, introduced-by-proof, role explicit-arg]

### proof_0521  (target depth 94, band 76-125)

THEOREM PROVED: `Computable.option_bind`

Grade all 16 candidates.

   1. `Option.casesOn`
      [def, depth 3, in-statement, role explicit-arg]
   2. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `Primcodable`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
   5. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Computable`
      [def, depth 11, in-statement, role type-annotation]
   7. `Computable.of_eq`
      [theorem, depth 12, introduced-by-proof, role applied]
   8. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `Computable₂`
      [def, depth 76, in-statement, role type-annotation]
  10. `Primcodable.option`
      [def, depth 71, in-statement, role instance-slot]
  11. `Option.none`
      [constructor, depth 1, in-statement, role explicit-arg]
  12. `Computable.const`
      [theorem, depth 89, introduced-by-proof, role explicit-arg]
  13. `Option.bind`
      [def, depth 5, in-statement, role explicit-arg]
  14. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `Computable.option_casesOn`
      [theorem, depth 93, introduced-by-proof, role explicit-arg]
  16. `Option.some`
      [constructor, depth 1, in-statement, role explicit-arg]

### proof_0522  (target depth 80, band 76-125)

THEOREM PROVED: `ContinuousMap.zsmul_apply`

Grade all 11 candidates.

   1. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `HSMul.hSMul`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `ContinuousMap.instFunLike`
      [def, depth 13, in-statement, role instance-slot]
   5. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `ContinuousMap`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `rfl`
      [def, depth 2, in-statement, role applied]
   8. `instHSMul`
      [def, depth 3, in-statement, role instance-slot]
   9. `IsTopologicalAddGroup`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `ContinuousMap.instZSMul`
      [def, depth 79, in-statement, role instance-slot]
  11. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0523  (target depth 177, band 126+)

THEOREM PROVED: `AnalyticOn.comp`

Grade all 11 candidates.

   1. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   2. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `AnalyticWithinAt.comp`
      [theorem, depth 176, introduced-by-proof, role applied]
   5. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   6. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Set`
      [def, depth 0, in-statement, role type-annotation]
   8. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   9. `Set.MapsTo`
      [def, depth 4, in-statement, role type-annotation]
  10. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  11. `AnalyticOn`
      [def, depth 160, in-statement, role type-annotation]

### proof_0524  (target depth 81, band 76-125)

THEOREM PROVED: `CategoryTheory.LocalizerMorphism.guitartExact_of_isRightDerivabilityStructure'`

Grade all 16 candidates.

   1. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   2. `Eq.mp`
      [def, depth 3, in-statement, role applied]
   3. `CategoryTheory.LocalizerMorphism.isRightDerivabilityStructure_iff`
      [theorem, depth 80, introduced-by-proof, role explicit-arg]
   4. `CategoryTheory.LocalizerMorphism.functor`
      [def, depth 4, in-statement, role explicit-arg]
   5. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
   6. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `CategoryTheory.Functor.IsLocalization`
      [inductive, depth 3, in-statement, role type-annotation]
   8. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  10. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
  11. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  12. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  13. `CategoryTheory.TwoSquare.GuitartExact`
      [inductive, depth 21, in-statement, role implicit-arg]
  14. `CategoryTheory.LocalizerMorphism`
      [inductive, depth 3, in-statement, role type-annotation]
  15. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `CategoryTheory.LocalizerMorphism.IsRightDerivabilityStructure`
      [inductive, depth 4, in-statement, role implicit-arg]

### proof_0525  (target depth 77, band 76-125)

THEOREM PROVED: `AddSubsemigroup.separatelyContinuousAdd`

Grade all 21 candidates.

   1. `instTopologicalSpaceSubtype`
      [def, depth 64, in-statement, role implicit-arg]
   2. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
   3. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   4. `SeparatelyContinuousAdd`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `AddHom.mk`
      [constructor, depth 4, introduced-by-proof, role explicit-arg]
   6. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   7. `AddSemigroup`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Topology.IsInducing.mk`
      [constructor, depth 64, introduced-by-proof, role explicit-arg]
   9. `AddSemigroup.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  10. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
  11. `AddMemClass.toAddSemigroup`
      [def, depth 9, in-statement, role instance-slot]
  12. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
  13. `AddSubsemigroup.instSetLike`
      [def, depth 8, in-statement, role instance-slot]
  14. `AddSubsemigroup`
      [inductive, depth 1, in-statement, role implicit-arg]
  15. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  16. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `AddHom.funLike`
      [def, depth 8, introduced-by-proof, role instance-slot]
  18. `TopologicalSpace`
      [inductive, depth 0, in-statement, role implicit-arg]
  19. `AddHom`
      [inductive, depth 1, introduced-by-proof, role implicit-arg]
  20. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  21. `Topology.IsInducing.separatelyContinuousAdd`
      [theorem, depth 76, introduced-by-proof, role applied]

### proof_0526  (target depth 87, band 76-125)

THEOREM PROVED: `Polynomial.eval_finsetSum`

Grade all 6 candidates.

   1. `Finset`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   4. `Polynomial`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Polynomial.eval₂_finsetSum`
      [theorem, depth 86, introduced-by-proof, role applied]
   6. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]

### proof_0527  (target depth 115, band 76-125)

THEOREM PROVED: `String.Slice.Pattern.Char.instLawfulBackwardPatternChar`

Grade all 14 candidates.

   1. `String.Slice.Pattern.LawfulBackwardPattern.mk`
      [constructor, depth 13, introduced-by-proof, role applied]
   2. `String.Slice.isEmpty`
      [def, depth 12, in-statement, role explicit-arg]
   3. `String.Slice.Pattern.LawfulBackwardPattern.endsWith_eq`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   4. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Char`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `instDecidableEqChar`
      [def, depth 22, in-statement, role instance-slot]
   7. `String.Slice`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `String.Slice.Pattern.Char.instBackwardPatternChar`
      [def, depth 114, in-statement, role instance-slot]
   9. `BEq.beq`
      [def, depth 1, in-statement, role implicit-arg]
  10. `instBEqOfDecidableEq`
      [def, depth 6, in-statement, role instance-slot]
  11. `String.Slice.Pattern.CharPred.instBackwardPatternForallCharBool`
      [def, depth 113, in-statement, role implicit-arg]
  12. `Bool.false`
      [constructor, depth 1, in-statement, role explicit-arg]
  13. `String.Slice.Pattern.LawfulBackwardPattern.skipSuffixOfNonempty?_eq`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  14. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0528  (target depth 190, band 126+)

THEOREM PROVED: `LSeriesHasSum_congr`

Grade all 22 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `LSeriesSummable`
      [def, depth 186, introduced-by-proof, role explicit-arg]
   3. `iff_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   4. `LSeriesHasSum`
      [def, depth 186, in-statement, role explicit-arg]
   5. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   6. `Complex`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
   9. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `_private.Mathlib.NumberTheory.LSeries.Basic.0.LSeriesHasSum_congr._simp_1_1`
      [theorem, depth 189, introduced-by-proof, role explicit-arg]
  12. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  13. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  14. `LSeriesSummable_congr`
      [theorem, depth 187, introduced-by-proof, role explicit-arg]
  15. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `LSeries_congr`
      [theorem, depth 187, introduced-by-proof, role explicit-arg]
  17. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  19. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  20. `Ne`
      [def, depth 2, in-statement, role type-annotation]
  21. `LSeries`
      [def, depth 186, introduced-by-proof, role explicit-arg]
  22. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
