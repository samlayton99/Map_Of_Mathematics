# Grading batch `batch_06` -- 20 proofs

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

### proof_101  (target depth 89, band 76-125)

THEOREM PROVED: `AdjoinRoot.isScalarTower_right`

Grade all 19 candidates below.

   1. `IsScalarTower`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `_private.Mathlib.RingTheory.AdjoinRoot.0.AdjoinRoot.isScalarTower_right._proof_1`
      [theorem, depth 88, introduced-by-proof, role applied]
   3. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   4. `AddGroupWithOne.toAddMonoidWithOne`
      [def, depth 1, in-statement, role instance-slot]
   5. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   6. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `instDistribOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
   8. `SMulZeroClass.toSMul`
      [def, depth 2, in-statement, role instance-slot]
   9. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
  10. `Ring.toAddGroupWithOne`
      [def, depth 10, in-statement, role instance-slot]
  11. `DistribSMul.toSMulZeroClass`
      [def, depth 2, in-statement, role instance-slot]
  12. `Polynomial`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `CommRing.toRing`
      [def, depth 1, in-statement, role instance-slot]
  14. `DistribSMul`
      [inductive, depth 1, in-statement, role type-annotation]
  15. `AddZero.toZero`
      [def, depth 1, in-statement, role implicit-arg]
  16. `AddMonoidWithOne.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  17. `Distrib.toMul`
      [def, depth 1, in-statement, role instance-slot]
  18. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  19. `instSMulOfMul`
      [def, depth 2, in-statement, role instance-slot]

### proof_102  (target depth 133, band 126+)

THEOREM PROVED: `AlgebraicGeometry.instHasTerminalScheme`

Grade all 16 candidates below.

   1. `CommRingCat`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `AlgebraicGeometry.Scheme`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Fintype.instPEmpty`
      [def, depth 56, introduced-by-proof, role instance-slot]
   4. `PEmpty`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role implicit-arg]
   6. `AlgebraicGeometry.Scheme.Spec`
      [def, depth 124, introduced-by-proof, role explicit-arg]
   7. `CategoryTheory.finCategoryDiscreteOfFintype`
      [def, depth 60, introduced-by-proof, role instance-slot]
   8. `CommRingCat.instCategory`
      [def, depth 20, in-statement, role instance-slot]
   9. `AlgebraicGeometry.Spec.reflective`
      [def, depth 132, introduced-by-proof, role instance-slot]
  10. `CategoryTheory.Functor.empty`
      [def, depth 13, introduced-by-proof, role implicit-arg]
  11. `CategoryTheory.Limits.hasTerminal_of_hasTerminal_of_preservesLimit`
      [theorem, depth 35, introduced-by-proof, role applied]
  12. `CategoryTheory.Discrete`
      [inductive, depth 0, in-statement, role explicit-arg]
  13. `AlgebraicGeometry.Scheme.instCategory`
      [def, depth 89, in-statement, role implicit-arg]
  14. `Opposite`
      [inductive, depth 0, in-statement, role explicit-arg]
  15. `CategoryTheory.monadicOfReflective`
      [def, depth 31, introduced-by-proof, role instance-slot]
  16. `CategoryTheory.discreteCategory`
      [def, depth 10, in-statement, role implicit-arg]

### proof_103  (target depth 10, band 0-10)

THEOREM PROVED: `CoheytingHom.ext_iff`

Grade all 13 candidates below.

   1. `HEq`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
   2. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
   3. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `CoheytingHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `CoheytingHom.instFunLike`
      [def, depth 8, in-statement, role instance-slot]
   7. `HEq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
   8. `CoheytingAlgebra`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Eq.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  10. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
  11. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  13. `CoheytingHom.ext`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]

### proof_104  (target depth 25, band 11-25)

THEOREM PROVED: `CategoryTheory.ShortComplex.SnakeInput.id_f₀`

Grade all 15 candidates below.

   1. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`
      [def, depth 17, in-statement, role instance-slot]
   2. `CategoryTheory.ShortComplex.SnakeInput.L₀`
      [def, depth 3, in-statement, role explicit-arg]
   3. `CategoryTheory.ShortComplex.SnakeInput.Hom.f₀`
      [def, depth 4, in-statement, role implicit-arg]
   4. `CategoryTheory.ShortComplex.SnakeInput.instCategory`
      [def, depth 24, in-statement, role instance-slot]
   5. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   6. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role explicit-arg]
   8. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   9. `rfl`
      [def, depth 2, in-statement, role applied]
  10. `CategoryTheory.ShortComplex`
      [inductive, depth 2, in-statement, role implicit-arg]
  11. `CategoryTheory.Abelian.toPreadditive`
      [def, depth 2, in-statement, role instance-slot]
  12. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `CategoryTheory.ShortComplex.SnakeInput`
      [inductive, depth 2, in-statement, role implicit-arg]
  14. `CategoryTheory.ShortComplex.instCategory`
      [def, depth 15, in-statement, role instance-slot]
  15. `CategoryTheory.Abelian`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_105  (target depth 34, band 26-50)

THEOREM PROVED: `CategoryTheory.MonoidalCategory.IsPushout.inr_isoPushout_hom_whiskerRight`

Grade all 25 candidates below.

   1. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   3. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
   4. `_private.Mathlib.CategoryTheory.Monoidal.Limits.Shapes.Pullback.0.CategoryTheory.MonoidalCategory.IsPushout.inr_isoPushout_hom_whiskerRight._simp_1_1`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.MonoidalCategoryStruct.whiskerRight`
      [def, depth 2, in-statement, role explicit-arg]
   6. `congrFun`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   8. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   9. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CategoryTheory.Limits.pushout.inr`
      [def, depth 23, in-statement, role explicit-arg]
  11. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  12. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  13. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  15. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `CategoryTheory.IsPushout`
      [inductive, depth 2, in-statement, role type-annotation]
  19. `CategoryTheory.MonoidalCategoryStruct.tensorObj`
      [def, depth 2, in-statement, role explicit-arg]
  20. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
  21. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  22. `CategoryTheory.IsPushout.isoPushout`
      [def, depth 31, in-statement, role explicit-arg]
  23. `CategoryTheory.Limits.pushout`
      [def, depth 18, in-statement, role explicit-arg]
  24. `CategoryTheory.IsPushout.inr_isoPushout_hom`
      [theorem, depth 33, introduced-by-proof, role explicit-arg]
  25. `CategoryTheory.Limits.HasPushout`
      [def, depth 17, in-statement, role type-annotation]

### proof_106  (target depth 73, band 51-75)

THEOREM PROVED: `addCommutator_eq_bot`

Grade all 14 candidates below.

   1. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   2. `addCommutator`
      [def, depth 67, in-statement, role explicit-arg]
   3. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   4. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   5. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
   6. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   7. `AddSubgroup.instBot`
      [def, depth 13, in-statement, role instance-slot]
   8. `Bot.bot`
      [def, depth 1, in-statement, role explicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `SubNegMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  11. `addCommutator_eq_bot_iff`
      [theorem, depth 72, introduced-by-proof, role explicit-arg]
  12. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `AddSubgroup`
      [inductive, depth 1, in-statement, role implicit-arg]
  14. `IsAddCommutative`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_107  (target depth 86, band 76-125)

THEOREM PROVED: `Ordinal.card_lt_ofNat`

Grade all 4 candidates below.

   1. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Ordinal`
      [def, depth 25, in-statement, role type-annotation]
   3. `Ordinal.card_lt_nat`
      [theorem, depth 85, introduced-by-proof, role applied]
   4. `Nat.AtLeastTwo`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_108  (target depth 178, band 126+)

THEOREM PROVED: `MeasureTheory.AEEqFun.toGermAddMonoidHom_apply`

Grade all 19 candidates below.

   1. `MeasureTheory.AEEqFun`
      [def, depth 168, in-statement, role type-annotation]
   2. `MeasureTheory.AEEqFun.toGermAddMonoidHom`
      [def, depth 177, in-statement, role explicit-arg]
   3. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `MeasureTheory.AEEqFun.instAddMonoid`
      [def, depth 176, in-statement, role instance-slot]
   5. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   6. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   8. `Filter.Germ.instAddZeroClass`
      [def, depth 19, in-statement, role instance-slot]
   9. `MeasureTheory.ae`
      [def, depth 128, in-statement, role explicit-arg]
  10. `AddMonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
  11. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
  12. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Filter.Germ`
      [def, depth 15, in-statement, role implicit-arg]
  14. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
  15. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  16. `ContinuousAdd`
      [inductive, depth 1, in-statement, role type-annotation]
  17. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `MeasureTheory.Measure.instFunLike`
      [def, depth 163, in-statement, role instance-slot]
  19. `AddMonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_109  (target depth 9, band 0-10)

THEOREM PROVED: `SimpleGraph.Hom.coe_comp`

Grade all 7 candidates below.

   1. `RelHom.instFunLike`
      [def, depth 5, in-statement, role instance-slot]
   2. `SimpleGraph.Hom.comp`
      [def, depth 8, in-statement, role explicit-arg]
   3. `rfl`
      [def, depth 2, in-statement, role applied]
   4. `SimpleGraph.Hom`
      [def, depth 2, in-statement, role type-annotation]
   5. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `SimpleGraph.Adj`
      [def, depth 1, in-statement, role implicit-arg]
   7. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]

### proof_110  (target depth 17, band 11-25)

THEOREM PROVED: `Function.IsPeriodicPt.right_of_add`

Grade all 12 candidates below.

   1. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   2. `AddCommSemigroup.toAddCommMagma`
      [def, depth 5, introduced-by-proof, role instance-slot]
   3. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
   4. `Nat.instAddCommSemigroup`
      [def, depth 16, introduced-by-proof, role instance-slot]
   5. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   6. `Function.IsPeriodicPt.left_of_add`
      [theorem, depth 11, introduced-by-proof, role applied]
   7. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   8. `add_comm`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   9. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  10. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `AddCommMagma.toAdd`
      [def, depth 1, introduced-by-proof, role instance-slot]
  12. `Function.IsPeriodicPt`
      [def, depth 7, in-statement, role implicit-arg]

### proof_111  (target depth 29, band 26-50)

THEOREM PROVED: `UInt64.toFin_mod`

Grade all 8 candidates below.

   1. `instHMod`
      [def, depth 3, in-statement, role instance-slot]
   2. `UInt64.size`
      [def, depth 4, in-statement, role explicit-arg]
   3. `HMod.hMod`
      [def, depth 2, in-statement, role explicit-arg]
   4. `instModUInt64`
      [def, depth 28, in-statement, role instance-slot]
   5. `UInt64`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `rfl`
      [def, depth 2, in-statement, role applied]
   7. `UInt64.toFin`
      [def, depth 4, in-statement, role implicit-arg]
   8. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_112  (target depth 59, band 51-75)

THEOREM PROVED: `MvPolynomial.coeff_add`

Grade all 23 candidates below.

   1. `MvPolynomial`
      [def, depth 18, in-statement, role type-annotation]
   2. `AddZero.toZero`
      [def, depth 1, in-statement, role instance-slot]
   3. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   4. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `NonAssocSemiring.toAddCommMonoidWithOne`
      [def, depth 10, in-statement, role instance-slot]
   6. `Nat.instMulZeroClass`
      [def, depth 17, in-statement, role instance-slot]
   7. `Finsupp`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `AddMonoidWithOne.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
   9. `AddMonoidAlgebra.coeff`
      [def, depth 2, in-statement, role explicit-arg]
  10. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
  11. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  12. `AddCommMonoidWithOne.toAddMonoidWithOne`
      [def, depth 1, in-statement, role instance-slot]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  15. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  17. `Finsupp.instFunLike`
      [def, depth 58, in-statement, role instance-slot]
  18. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  19. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  20. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  21. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  22. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  23. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]

### proof_113  (target depth 82, band 76-125)

THEOREM PROVED: `Submodule.spanRank_map_eq_of_injective`

Grade all 21 candidates below.

   1. `Cardinal.lift`
      [def, depth 21, in-statement, role explicit-arg]
   2. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Cardinal.lift_id`
      [theorem, depth 23, introduced-by-proof, role explicit-arg]
   5. `Submodule.lift_spanRank_map_eq_of_injective`
      [theorem, depth 81, introduced-by-proof, role explicit-arg]
   6. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   7. `Submodule.map`
      [def, depth 24, in-statement, role explicit-arg]
   8. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  10. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `RingHomSurjective`
      [inductive, depth 11, in-statement, role type-annotation]
  12. `Submodule.spanRank`
      [def, depth 75, in-statement, role explicit-arg]
  13. `Function.Injective`
      [def, depth 1, in-statement, role type-annotation]
  14. `Submodule`
      [inductive, depth 2, in-statement, role type-annotation]
  15. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `LinearMap`
      [inductive, depth 11, in-statement, role implicit-arg]
  17. `Eq.mp`
      [def, depth 3, in-statement, role applied]
  18. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  19. `RingHom`
      [inductive, depth 1, in-statement, role type-annotation]
  20. `LinearMap.instFunLike`
      [def, depth 20, in-statement, role instance-slot]
  21. `Cardinal`
      [def, depth 18, in-statement, role implicit-arg]

### proof_114  (target depth 199, band 126+)

THEOREM PROVED: `ProbabilityTheory.iIndepFun.iIndepFun_process`

Grade all 17 candidates below.

   1. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `ProbabilityTheory.Kernel.const`
      [def, depth 166, in-statement, role implicit-arg]
   3. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
   4. `ProbabilityTheory.iIndepFun`
      [def, depth 173, in-statement, role type-annotation]
   5. `ProbabilityTheory.Kernel.iIndepFun.iIndepFun_process`
      [theorem, depth 198, introduced-by-proof, role applied]
   6. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   7. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   8. `Measurable`
      [def, depth 5, in-statement, role type-annotation]
   9. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
  10. `MeasurableSpace.pi`
      [def, depth 66, in-statement, role instance-slot]
  11. `Subtype`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `Unit.unit`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Unit`
      [def, depth 1, in-statement, role explicit-arg]
  15. `PUnit.instMeasurableSpace`
      [def, depth 66, in-statement, role implicit-arg]
  16. `MeasureTheory.Measure.dirac`
      [def, depth 163, in-statement, role implicit-arg]
  17. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_115  (target depth 3, band 0-10)

THEOREM PROVED: `MeasurableSet.neg`

Grade all 6 candidates below.

   1. `Neg`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `MeasurableNeg.measurable_neg`
      [theorem, depth 2, introduced-by-proof, role applied]
   4. `MeasurableSet`
      [def, depth 2, in-statement, role type-annotation]
   5. `MeasurableNeg`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Set`
      [def, depth 0, in-statement, role type-annotation]

### proof_116  (target depth 15, band 11-25)

THEOREM PROVED: `IsMinOn.dual`

Grade all 14 candidates below.

   1. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   2. `IsMaxOn`
      [def, depth 8, in-statement, role implicit-arg]
   3. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
   5. `isMaxOn_dual_iff`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
   6. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
   7. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   8. `OrderDual`
      [def, depth 0, in-statement, role implicit-arg]
   9. `Set`
      [def, depth 0, in-statement, role type-annotation]
  10. `OrderDual.toDual`
      [def, depth 11, in-statement, role explicit-arg]
  11. `IsMinOn`
      [def, depth 8, in-statement, role implicit-arg]
  12. `OrderDual.instPreorder`
      [def, depth 10, in-statement, role instance-slot]
  13. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]

### proof_117  (target depth 36, band 26-50)

THEOREM PROVED: `CategoryTheory.Precoverage.toPretopology_toPrecoverage`

Grade all 9 candidates below.

   1. `CategoryTheory.Precoverage.IsStableUnderComposition`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `CategoryTheory.Precoverage`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `CategoryTheory.Precoverage.IsStableUnderBaseChange`
      [inductive, depth 2, in-statement, role type-annotation]
   4. `CategoryTheory.Precoverage.HasIsos`
      [inductive, depth 2, in-statement, role type-annotation]
   5. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   6. `CategoryTheory.Precoverage.toPretopology`
      [def, depth 35, in-statement, role explicit-arg]
   7. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `CategoryTheory.Pretopology.toPrecoverage`
      [def, depth 16, in-statement, role explicit-arg]
   9. `CategoryTheory.Limits.HasPullbacks`
      [def, depth 14, in-statement, role type-annotation]

### proof_118  (target depth 55, band 51-75)

THEOREM PROVED: `Function.updateFinset_def`

Grade all 9 candidates below.

   1. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Function.updateFinset`
      [def, depth 54, in-statement, role implicit-arg]
   3. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   4. `rfl`
      [def, depth 2, in-statement, role applied]
   5. `Subtype`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Subtype.val`
      [def, depth 1, in-statement, role type-annotation]
   7. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   8. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]

### proof_119  (target depth 107, band 76-125)

THEOREM PROVED: `CategoryTheory.instPreservesFilteredColimitsOfSizeObjOppositeFunctorTypeCoyonedaOpOfIsFinitelyPresentable`

Grade all 19 candidates below.

   1. `CategoryTheory.types`
      [def, depth 10, in-statement, role instance-slot]
   2. `id`
      [def, depth 0, in-statement, role explicit-arg]
   3. `Opposite.op`
      [constructor, depth 1, in-statement, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `CategoryTheory.isFinitelyPresentable_iff_preservesFilteredColimitsOfSize`
      [theorem, depth 106, introduced-by-proof, role explicit-arg]
   6. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   7. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   8. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   9. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  11. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  12. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `CategoryTheory.Limits.PreservesFilteredColimitsOfSize`
      [inductive, depth 2, in-statement, role explicit-arg]
  14. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  16. `CategoryTheory.IsFinitelyPresentable`
      [def, depth 103, in-statement, role explicit-arg]
  17. `inferInstance`
      [def, depth 0, in-statement, role explicit-arg]
  18. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  19. `CategoryTheory.coyoneda`
      [def, depth 27, in-statement, role explicit-arg]

### proof_120  (target depth 174, band 126+)

THEOREM PROVED: `iteratedDeriv_neg`

Grade all 25 candidates below.

   1. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `SubtractionMonoid.toSubNegZeroMonoid`
      [def, depth 9, in-statement, role instance-slot]
   3. `id`
      [def, depth 0, in-statement, role explicit-arg]
   4. `_private.Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas.0.iteratedDeriv_neg._simp_1_1`
      [theorem, depth 172, introduced-by-proof, role explicit-arg]
   5. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]
   6. `Pi.instNeg`
      [def, depth 2, in-statement, role instance-slot]
   7. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `AddCommGroup.toDivisionAddCommMonoid`
      [def, depth 12, in-statement, role instance-slot]
   9. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  11. `iteratedDerivWithin`
      [def, depth 169, introduced-by-proof, role implicit-arg]
  12. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  14. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `SubNegZeroMonoid.toNegZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  16. `congrFun`
      [theorem, depth 3, in-statement, role explicit-arg]
  17. `Set.univ`
      [def, depth 2, in-statement, role explicit-arg]
  18. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  19. `iteratedDerivWithin_neg`
      [theorem, depth 173, introduced-by-proof, role explicit-arg]
  20. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
  21. `iteratedDeriv`
      [def, depth 169, in-statement, role implicit-arg]
  22. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  23. `SubtractionCommMonoid.toSubtractionMonoid`
      [def, depth 1, in-statement, role instance-slot]
  24. `NegZeroClass.toNeg`
      [def, depth 1, in-statement, role instance-slot]
  25. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
