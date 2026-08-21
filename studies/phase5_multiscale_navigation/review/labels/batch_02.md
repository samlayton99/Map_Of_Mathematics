# Grading batch `batch_02` -- 20 proofs

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

### proof_021  (target depth 27, band 26-50)

THEOREM PROVED: `Set.image_mul_right_Ioo`

Grade all 15 candidates below.

   1. `OrderIso.mulRight₀`
      [def, depth 20, introduced-by-proof, role explicit-arg]
   2. `MulPosReflectLT`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   4. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   5. `MulZeroClass.toMul`
      [def, depth 1, in-statement, role instance-slot]
   6. `MonoidWithZero.toMulZeroOneClass`
      [def, depth 5, in-statement, role instance-slot]
   7. `MulZeroOneClass.toMulZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   8. `OrderIso.image_Ioo`
      [theorem, depth 26, introduced-by-proof, role applied]
   9. `GroupWithZero.toMonoidWithZero`
      [def, depth 1, in-statement, role instance-slot]
  10. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  11. `GroupWithZero`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
  13. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  14. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
  15. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_022  (target depth 74, band 51-75)

THEOREM PROVED: `Std.ExtDHashMap.getD_union_of_not_mem_right`

Grade all 15 candidates below.

   1. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.DHashMap`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.ExtDHashMap.inductionOn₂`
      [theorem, depth 21, introduced-by-proof, role applied]
   5. `Std.ExtDHashMap.getD`
      [def, depth 68, in-statement, role explicit-arg]
   6. `Std.ExtDHashMap.mk`
      [def, depth 19, in-statement, role explicit-arg]
   7. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   8. `Union.union`
      [def, depth 1, in-statement, role explicit-arg]
   9. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Std.ExtDHashMap.instMembershipOfEquivBEqOfLawfulHashable`
      [def, depth 69, in-statement, role instance-slot]
  11. `Not`
      [def, depth 1, in-statement, role type-annotation]
  12. `LawfulBEq`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `Std.ExtDHashMap`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `Std.ExtDHashMap.instUnionOfEquivBEqOfLawfulHashable`
      [def, depth 73, in-statement, role instance-slot]
  15. `Std.DHashMap.getD_union_of_not_mem_right`
      [theorem, depth 71, introduced-by-proof, role explicit-arg]

### proof_023  (target depth 77, band 76-125)

THEOREM PROVED: `Std.TreeMap.getKey?_modify_self`

Grade all 5 candidates below.

   1. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.TreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   3. `Std.DTreeMap.Const.getKey?_modify_self`
      [theorem, depth 76, introduced-by-proof, role applied]
   4. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Std.TreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]

### proof_024  (target depth 198, band 126+)

THEOREM PROVED: `Real.analyticAt_sinh`

Grade all 14 candidates below.

   1. `Real.normedAddCommGroup`
      [def, depth 148, in-statement, role instance-slot]
   2. `Top.top`
      [def, depth 1, in-statement, role implicit-arg]
   3. `WithTop`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Real.sinh`
      [def, depth 141, in-statement, role implicit-arg]
   5. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   6. `ENat`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   7. `NormedField.toNormedSpace`
      [def, depth 105, in-statement, role instance-slot]
   8. `DenselyNormedField.toNontriviallyNormedField`
      [def, depth 111, in-statement, role instance-slot]
   9. `ContDiffAt.analyticAt`
      [theorem, depth 184, introduced-by-proof, role applied]
  10. `ContDiff.contDiffAt`
      [theorem, depth 190, introduced-by-proof, role explicit-arg]
  11. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Real.denselyNormedField`
      [def, depth 153, in-statement, role instance-slot]
  13. `WithTop.top`
      [def, depth 2, in-statement, role instance-slot]
  14. `Real.contDiff_sinh`
      [theorem, depth 197, introduced-by-proof, role explicit-arg]

### proof_025  (target depth 3, band 0-10)

THEOREM PROVED: `CategoryTheory.Limits.MulticospanShape.prod_fst`

Grade all 4 candidates below.

   1. `CategoryTheory.Limits.MulticospanShape.fst`
      [def, depth 1, in-statement, role explicit-arg]
   2. `CategoryTheory.Limits.MulticospanShape.prod`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Prod`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role applied]

### proof_026  (target depth 18, band 11-25)

THEOREM PROVED: `Function.isMinimalFor_argminOn`

Grade all 18 candidates below.

   1. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   2. `Function.argminOn_le`
      [theorem, depth 17, introduced-by-proof, role explicit-arg]
   3. `Function.argminOn_mem`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
   4. `And.intro`
      [constructor, depth 1, in-statement, role applied]
   5. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
   6. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
  10. `Set.Nonempty`
      [def, depth 4, in-statement, role type-annotation]
  11. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  12. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  13. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
  14. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  15. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
  16. `WellFoundedLT`
      [def, depth 2, in-statement, role type-annotation]
  17. `Function.argminOn`
      [def, depth 15, in-statement, role explicit-arg]
  18. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]

### proof_027  (target depth 34, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.mkIso_inv_snd`

Grade all 23 candidates below.

   1. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.mkIso._auto_1`
      [def, depth 8, in-statement, role explicit-arg]
   2. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   5. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.mkIso`
      [def, depth 33, in-statement, role explicit-arg]
   6. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.snd`
      [def, depth 3, in-statement, role explicit-arg]
   8. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.instCategory`
      [def, depth 30, in-statement, role instance-slot]
  10. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.iso`
      [def, depth 3, in-statement, role explicit-arg]
  11. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  12. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role implicit-arg]
  13. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.fst`
      [def, depth 3, in-statement, role explicit-arg]
  14. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
  15. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  16. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  18. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
  19. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.Hom.snd`
      [def, depth 4, in-statement, role explicit-arg]
  20. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  21. `autoParam`
      [def, depth 1, in-statement, role type-annotation]
  22. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver`
      [inductive, depth 2, in-statement, role type-annotation]
  23. `CategoryTheory.Functor.whiskerRight`
      [def, depth 21, in-statement, role explicit-arg]

### proof_028  (target depth 69, band 51-75)

THEOREM PROVED: `AddGroup.addCommGroupOfCenterEqTop._proof_1`

Grade all 22 candidates below.

   1. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   2. `AddSubgroup.instTop`
      [def, depth 13, in-statement, role instance-slot]
   3. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]
   4. `AddSubgroup.eq_top_iff'`
      [theorem, depth 68, introduced-by-proof, role explicit-arg]
   5. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   6. `Iff.mp`
      [theorem, depth 1, in-statement, role applied]
   7. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   8. `AddSubgroup.center`
      [def, depth 19, in-statement, role explicit-arg]
   9. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  10. `Top.top`
      [def, depth 1, in-statement, role explicit-arg]
  11. `SetLike.instMembership`
      [def, depth 4, introduced-by-proof, role instance-slot]
  12. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  13. `AddSubgroup`
      [inductive, depth 1, in-statement, role implicit-arg]
  14. `SubNegMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  15. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  16. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  17. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
  18. `AddSubgroup.instSetLike`
      [def, depth 16, introduced-by-proof, role instance-slot]
  19. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  21. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  22. `AddSubgroup.mem_center_iff`
      [theorem, depth 20, introduced-by-proof, role explicit-arg]

### proof_029  (target depth 78, band 76-125)

THEOREM PROVED: `Std.TreeMap.Raw.minKey!_insert`

Grade all 8 candidates below.

   1. `Std.TreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
   2. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.DTreeMap.Raw.minKey!_insert`
      [theorem, depth 77, introduced-by-proof, role applied]
   4. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Std.TreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   6. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.TreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   8. `Std.TreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]

### proof_030  (target depth 169, band 126+)

THEOREM PROVED: `NormedSpace.eq_iff_forall_dual_eq`

Grade all 19 candidates below.

   1. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
   2. `RCLike.toDenselyNormedField`
      [def, depth 2, in-statement, role instance-slot]
   3. `NormedCommRing.toSeminormedCommRing`
      [def, depth 96, in-statement, role instance-slot]
   4. `SeminormedCommRing.toSeminormedRing`
      [def, depth 1, in-statement, role instance-slot]
   5. `DivisionRing.toRing`
      [def, depth 1, in-statement, role instance-slot]
   6. `DenselyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   7. `SeparatingDual.eq_iff_forall_dual_eq`
      [theorem, depth 25, introduced-by-proof, role applied]
   8. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   9. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  11. `NormedSpace.toModule`
      [def, depth 2, in-statement, role instance-slot]
  12. `RCLike`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  14. `NormedField.toField`
      [def, depth 1, in-statement, role instance-slot]
  15. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  17. `NormedField.toNormedCommRing`
      [def, depth 103, in-statement, role instance-slot]
  18. `SeminormedRing.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  19. `Field.toDivisionRing`
      [def, depth 44, in-statement, role instance-slot]

### proof_031  (target depth 4, band 0-10)

THEOREM PROVED: `ExceptT.run_liftM`

Grade all 10 candidates below.

   1. `Except`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `ExceptT.run`
      [def, depth 2, in-statement, role implicit-arg]
   3. `liftM`
      [def, depth 2, in-statement, role explicit-arg]
   4. `instMonadLiftTOfMonadLift`
      [def, depth 3, in-statement, role instance-slot]
   5. `ExceptT`
      [def, depth 1, in-statement, role explicit-arg]
   6. `instMonadLiftT`
      [def, depth 2, in-statement, role instance-slot]
   7. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   8. `ExceptT.instMonadLift`
      [def, depth 3, in-statement, role instance-slot]
   9. `Monad`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `LawfulMonad`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_032  (target depth 21, band 11-25)

THEOREM PROVED: `List.NodupKeys.nodup`

Grade all 4 candidates below.

   1. `Sigma`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `List.Nodup.of_map`
      [theorem, depth 20, introduced-by-proof, role applied]
   3. `Sigma.fst`
      [def, depth 1, in-statement, role explicit-arg]
   4. `List`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_033  (target depth 39, band 26-50)

THEOREM PROVED: `CategoryTheory.associator_inv_apply_2`

Grade all 16 candidates below.

   1. `CategoryTheory.ConcreteCategory.hom`
      [def, depth 4, in-statement, role explicit-arg]
   2. `CategoryTheory.MonoidalCategoryStruct.tensorObj`
      [def, depth 2, in-statement, role explicit-arg]
   3. `CategoryTheory.typesCartesianMonoidalCategory`
      [def, depth 38, in-statement, role instance-slot]
   4. `Prod.snd`
      [def, depth 1, in-statement, role implicit-arg]
   5. `CategoryTheory.CartesianMonoidalCategory.toSemiCartesianMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
   6. `CategoryTheory.types`
      [def, depth 10, in-statement, role implicit-arg]
   7. `rfl`
      [def, depth 2, in-statement, role applied]
   8. `TypeCat.instFunLikeFun`
      [def, depth 7, in-statement, role implicit-arg]
   9. `TypeCat.Fun`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `CategoryTheory.SemiCartesianMonoidalCategory.toMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
  11. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
  13. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  14. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
  15. `CategoryTheory.MonoidalCategoryStruct.associator`
      [def, depth 2, in-statement, role explicit-arg]
  16. `instConcreteCategoryTypeFun`
      [def, depth 12, in-statement, role instance-slot]

### proof_034  (target depth 51, band 51-75)

THEOREM PROVED: `Fin.xor_comm`

Grade all 3 candidates below.

   1. `_private.Mathlib.Data.Fin.Init.0.Fin.xor_comm._proof_1_1`
      [theorem, depth 50, introduced-by-proof, role applied]
   2. `Fin`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_035  (target depth 83, band 76-125)

THEOREM PROVED: `CategoryTheory.Localization.lift₂_iso_hom_app_app₁`

Grade all 18 candidates below.

   1. `CategoryTheory.Localization.instLifting₂Lift₂`
      [def, depth 82, in-statement, role instance-slot]
   2. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   4. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   5. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   6. `CategoryTheory.MorphismProperty.ContainsIdentities`
      [inductive, depth 3, in-statement, role type-annotation]
   7. `CategoryTheory.Functor.whiskeringLeft₂`
      [def, depth 31, in-statement, role explicit-arg]
   8. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
  10. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  11. `CategoryTheory.MorphismProperty.IsInvertedBy₂`
      [def, depth 24, in-statement, role type-annotation]
  12. `CategoryTheory.Localization.lift₂`
      [def, depth 81, in-statement, role explicit-arg]
  13. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role explicit-arg]
  14. `CategoryTheory.Functor.IsLocalization`
      [inductive, depth 3, in-statement, role type-annotation]
  15. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  16. `CategoryTheory.Localization.Lifting₂.iso`
      [def, depth 21, in-statement, role explicit-arg]
  17. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  18. `rfl`
      [def, depth 2, in-statement, role applied]

### proof_036  (target depth 216, band 126+)

THEOREM PROVED: `MeasureTheory.AEStronglyMeasurable.prod_swap`

Grade all 16 candidates below.

   1. `MeasureTheory.Measure.map`
      [def, depth 188, in-statement, role explicit-arg]
   2. `Prod.instMeasurableSpace`
      [def, depth 67, in-statement, role implicit-arg]
   3. `MeasureTheory.AEStronglyMeasurable`
      [def, depth 165, in-statement, role implicit-arg]
   4. `MeasureTheory.Measure.prod_swap`
      [theorem, depth 215, introduced-by-proof, role explicit-arg]
   5. `MeasureTheory.SFinite`
      [inductive, depth 2, in-statement, role type-annotation]
   6. `MeasureTheory.AEStronglyMeasurable.comp_measurable`
      [theorem, depth 198, introduced-by-proof, role applied]
   7. `MeasureTheory.Measure.prod`
      [def, depth 206, in-statement, role explicit-arg]
   8. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  10. `measurable_swap`
      [theorem, depth 69, in-statement, role explicit-arg]
  11. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Prod.swap`
      [def, depth 2, in-statement, role explicit-arg]
  13. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]
  15. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_037  (target depth 9, band 0-10)

THEOREM PROVED: `Function.Exact.of_comp_of_mem_range`

Grade all 16 candidates below.

   1. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   2. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   3. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
   5. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   6. `Exists.rec`
      [recursor, depth 2, introduced-by-proof, role explicit-arg]
   7. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   8. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   9. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
  11. `congrFun`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  12. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  13. `forall_apply_eq_imp_iff`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
  14. `Pi.instZero`
      [def, depth 4, in-statement, role instance-slot]
  15. `Exists`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `Set.range`
      [def, depth 2, in-statement, role explicit-arg]

### proof_038  (target depth 13, band 11-25)

THEOREM PROVED: `CategoryTheory.MorphismProperty.RightFraction.unop_f`

Grade all 15 candidates below.

   1. `CategoryTheory.MorphismProperty.RightFraction`
      [inductive, depth 3, in-statement, role type-annotation]
   2. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
   4. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   5. `CategoryTheory.CategoryStruct.opposite`
      [def, depth 4, in-statement, role instance-slot]
   6. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
   7. `Opposite.unop`
      [def, depth 1, in-statement, role explicit-arg]
   8. `CategoryTheory.MorphismProperty.RightFraction.X'`
      [def, depth 4, in-statement, role explicit-arg]
   9. `CategoryTheory.MorphismProperty.LeftFraction.f`
      [def, depth 4, in-statement, role explicit-arg]
  10. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `CategoryTheory.MorphismProperty.RightFraction.unop`
      [def, depth 12, in-statement, role explicit-arg]
  12. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  13. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  14. `CategoryTheory.MorphismProperty.unop`
      [def, depth 5, in-statement, role implicit-arg]
  15. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]

### proof_039  (target depth 40, band 26-50)

THEOREM PROVED: `HomologicalComplex.extend.homologyData'_left_K`

Grade all 18 candidates below.

   1. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   2. `HomologicalComplex`
      [inductive, depth 2, in-statement, role type-annotation]
   3. `ComplexShape.Embedding.f`
      [def, depth 2, in-statement, role explicit-arg]
   4. `CategoryTheory.Limits.HasZeroMorphisms`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `CategoryTheory.ShortComplex.LeftHomologyData.K`
      [def, depth 4, in-statement, role explicit-arg]
   6. `CategoryTheory.ShortComplex.HomologyData`
      [inductive, depth 3, in-statement, role type-annotation]
   7. `HomologicalComplex.extend`
      [def, depth 17, in-statement, role explicit-arg]
   8. `HomologicalComplex.sc`
      [def, depth 22, in-statement, role implicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `HomologicalComplex.sc'`
      [def, depth 21, in-statement, role explicit-arg]
  12. `CategoryTheory.Limits.HasZeroObject`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `ComplexShape.prev`
      [def, depth 12, in-statement, role explicit-arg]
  14. `ComplexShape`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `HomologicalComplex.extend.homologyData'`
      [def, depth 39, in-statement, role explicit-arg]
  16. `CategoryTheory.ShortComplex.HomologyData.left`
      [def, depth 4, in-statement, role explicit-arg]
  17. `ComplexShape.Embedding`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `ComplexShape.next`
      [def, depth 12, in-statement, role explicit-arg]

### proof_040  (target depth 69, band 51-75)

THEOREM PROVED: `List.SortedGE.map_ofDual`

Grade all 14 candidates below.

   1. `List.sortedGE_map_ofDual`
      [theorem, depth 68, introduced-by-proof, role explicit-arg]
   2. `List.SortedLE`
      [def, depth 25, in-statement, role implicit-arg]
   3. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   4. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `OrderDual.ofDual`
      [def, depth 11, in-statement, role explicit-arg]
   6. `Iff.mp`
      [theorem, depth 1, in-statement, role applied]
   7. `OrderDual`
      [def, depth 0, in-statement, role explicit-arg]
   8. `List.map`
      [def, depth 6, in-statement, role explicit-arg]
   9. `List.SortedGE`
      [def, depth 25, in-statement, role implicit-arg]
  10. `List`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
  12. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `OrderDual.instPreorder`
      [def, depth 10, in-statement, role instance-slot]
  14. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
