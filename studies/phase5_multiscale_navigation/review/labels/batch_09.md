# Grading batch `batch_09` -- 20 proofs

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

### proof_161  (target depth 78, band 76-125)

THEOREM PROVED: `isSeqCompact_iff_seqCompactSpace`

Grade all 12 candidates below.

   1. `isSeqCompact_univ_iff`
      [theorem, depth 23, introduced-by-proof, role explicit-arg]
   2. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   3. `Iff.trans`
      [theorem, depth 2, in-statement, role applied]
   4. `isSeqCompact_iff_isSeqCompact_univ`
      [theorem, depth 77, introduced-by-proof, role explicit-arg]
   5. `Set.univ`
      [def, depth 2, in-statement, role explicit-arg]
   6. `instTopologicalSpaceSubtype`
      [def, depth 64, in-statement, role instance-slot]
   7. `IsSeqCompact`
      [def, depth 21, in-statement, role implicit-arg]
   8. `SeqCompactSpace`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
  10. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  12. `Set`
      [def, depth 0, in-statement, role implicit-arg]

### proof_162  (target depth 185, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.comap_preimage`

Grade all 24 candidates below.

   1. `Set.preimage`
      [def, depth 4, in-statement, role explicit-arg]
   2. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Measurable`
      [def, depth 5, in-statement, role type-annotation]
   4. `MeasurableSet`
      [def, depth 2, in-statement, role type-annotation]
   5. `Set.instInter`
      [def, depth 5, in-statement, role instance-slot]
   6. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `Set`
      [def, depth 0, in-statement, role type-annotation]
   8. `MeasureTheory.Measure.comap_apply₀`
      [theorem, depth 184, introduced-by-proof, role explicit-arg]
   9. `Set.image`
      [def, depth 4, in-statement, role explicit-arg]
  10. `MeasureTheory.Measure.comap`
      [def, depth 182, in-statement, role explicit-arg]
  11. `Inter.inter`
      [def, depth 1, in-statement, role explicit-arg]
  12. `MeasureTheory.NullMeasurableSet`
      [def, depth 167, in-statement, role type-annotation]
  13. `Function.Injective`
      [def, depth 1, in-statement, role type-annotation]
  14. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  15. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  16. `Set.range`
      [def, depth 2, in-statement, role explicit-arg]
  17. `MeasureTheory.Measure.instFunLike`
      [def, depth 163, in-statement, role instance-slot]
  18. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
  19. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  20. `MeasurableSet.nullMeasurableSet`
      [theorem, depth 165, in-statement, role explicit-arg]
  21. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  22. `id`
      [def, depth 0, in-statement, role explicit-arg]
  23. `Set.image_preimage_eq_inter_range`
      [theorem, depth 16, in-statement, role explicit-arg]
  24. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]

### proof_163  (target depth 3, band 0-10)

THEOREM PROVED: `Matrix.vec_eq_uncurry`

Grade all 4 candidates below.

   1. `Matrix.vec`
      [def, depth 2, in-statement, role implicit-arg]
   2. `Prod`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   4. `Matrix`
      [def, depth 0, in-statement, role type-annotation]

### proof_164  (target depth 20, band 11-25)

THEOREM PROVED: `AddSubmonoid.LocalizationMap.instAddMonoidHomClass`

Grade all 14 candidates below.

   1. `AddZero.toZero`
      [def, depth 1, in-statement, role instance-slot]
   2. `AddHom.map_add`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   3. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   4. `AddSubmonoid.LocalizationMap.instFunLike`
      [def, depth 19, in-statement, role instance-slot]
   5. `AddMonoidHomClass.mk`
      [constructor, depth 4, introduced-by-proof, role applied]
   6. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   7. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   8. `AddSubmonoid`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `AddMonoidHom.map_zero`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  10. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `AddCommMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  12. `AddSubmonoid.LocalizationMap.toAddMonoidHom`
      [def, depth 16, in-statement, role explicit-arg]
  13. `AddSubmonoid.LocalizationMap.toAddHom`
      [def, depth 7, in-statement, role explicit-arg]
  14. `AddSubmonoid.LocalizationMap`
      [inductive, depth 6, in-statement, role implicit-arg]

### proof_165  (target depth 26, band 26-50)

THEOREM PROVED: `Matrix.uniqueLinearEquiv_apply`

Grade all 15 candidates below.

   1. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   3. `LinearEquiv.instEquivLike`
      [def, depth 25, in-statement, role instance-slot]
   4. `Matrix`
      [def, depth 0, in-statement, role type-annotation]
   5. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   6. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
   7. `LinearEquiv`
      [inductive, depth 12, in-statement, role implicit-arg]
   8. `Matrix.uniqueLinearEquiv`
      [def, depth 21, in-statement, role explicit-arg]
   9. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  10. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  11. `Matrix.addCommMonoid`
      [def, depth 13, in-statement, role instance-slot]
  12. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `Unique`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `Matrix.module`
      [def, depth 16, in-statement, role implicit-arg]

### proof_166  (target depth 61, band 51-75)

THEOREM PROVED: `Set.kernImage_preimage_union`

Grade all 12 candidates below.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Set`
      [def, depth 0, in-statement, role type-annotation]
   3. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   4. `Union.union`
      [def, depth 1, in-statement, role explicit-arg]
   5. `Set.union_comm`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   6. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
   7. `Set.kernImage`
      [def, depth 4, in-statement, role explicit-arg]
   8. `Set.preimage`
      [def, depth 4, in-statement, role explicit-arg]
   9. `Set.kernImage_union_preimage`
      [theorem, depth 60, introduced-by-proof, role explicit-arg]
  10. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  11. `Set.instUnion`
      [def, depth 5, in-statement, role instance-slot]
  12. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]

### proof_167  (target depth 84, band 76-125)

THEOREM PROVED: `Finsupp.isAffineMap_eval`

Grade all 19 candidates below.

   1. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   2. `Finsupp`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   4. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   5. `NonAssocSemiring.toAddCommMonoidWithOne`
      [def, depth 10, in-statement, role instance-slot]
   6. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Convexity.ConvexSpace`
      [inductive, depth 2, in-statement, role type-annotation]
   8. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Semiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
  10. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  11. `Finsupp.sConvexComb_apply`
      [theorem, depth 83, introduced-by-proof, role explicit-arg]
  12. `Finsupp.instFunLike`
      [def, depth 58, in-statement, role instance-slot]
  13. `Finsupp.instConvexSpace`
      [def, depth 82, in-statement, role instance-slot]
  14. `AddCommMonoidWithOne.toAddMonoidWithOne`
      [def, depth 1, in-statement, role instance-slot]
  15. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `Convexity.StdSimplex`
      [inductive, depth 1, in-statement, role type-annotation]
  17. `Convexity.IsAffineMap.mk`
      [constructor, depth 76, introduced-by-proof, role applied]
  18. `AddMonoidWithOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
  19. `IsStrictOrderedRing`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_168  (target depth 157, band 126+)

THEOREM PROVED: `EuclideanGeometry.inversion_def`

Grade all 10 candidates below.

   1. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `MetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Real.instRCLike`
      [def, depth 155, in-statement, role instance-slot]
   4. `InnerProductSpace`
      [inductive, depth 2, in-statement, role type-annotation]
   5. `rfl`
      [def, depth 2, in-statement, role applied]
   6. `EuclideanGeometry.inversion`
      [def, depth 156, in-statement, role implicit-arg]
   7. `NormedAddTorsor`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   9. `MetricSpace.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  10. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_169  (target depth 8, band 0-10)

THEOREM PROVED: `CategoryTheory.MonoidalCategory.leftUnitor_inv_naturality_assoc`

Grade all 21 candidates below.

   1. `CategoryTheory.MonoidalCategoryStruct.leftUnitor`
      [def, depth 2, in-statement, role explicit-arg]
   2. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   4. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   6. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
   7. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   8. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   9. `CategoryTheory.MonoidalCategoryStruct.tensorObj`
      [def, depth 2, in-statement, role implicit-arg]
  10. `CategoryTheory.MonoidalCategoryStruct.tensorUnit`
      [def, depth 2, in-statement, role explicit-arg]
  11. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
  12. `CategoryTheory.Category.assoc`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  13. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  14. `CategoryTheory.MonoidalCategory.leftUnitor_inv_naturality`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  15. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  16. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
  17. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  18. `CategoryTheory.MonoidalCategoryStruct.whiskerLeft`
      [def, depth 2, in-statement, role explicit-arg]
  19. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  20. `id`
      [def, depth 0, introduced-by-proof, role applied]
  21. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_170  (target depth 19, band 11-25)

THEOREM PROVED: `List.kinsert_nodupKeys`

Grade all 18 candidates below.

   1. `List.NodupKeys`
      [def, depth 8, in-statement, role implicit-arg]
   2. `Sigma.fst`
      [def, depth 1, in-statement, role explicit-arg]
   3. `List.nodupKeys_cons`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
   4. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `List.kerase`
      [def, depth 8, in-statement, role explicit-arg]
   6. `List.notMem_keys_kerase`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   7. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   8. `Not`
      [def, depth 1, in-statement, role explicit-arg]
   9. `List.NodupKeys.kerase`
      [theorem, depth 17, introduced-by-proof, role explicit-arg]
  10. `List.cons`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `Membership.mem`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  12. `And.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  13. `List.instMembership`
      [def, depth 3, introduced-by-proof, role instance-slot]
  14. `And`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  15. `Sigma`
      [inductive, depth 0, in-statement, role explicit-arg]
  16. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
  17. `Sigma.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  18. `List.keys`
      [def, depth 7, in-statement, role explicit-arg]

### proof_171  (target depth 35, band 26-50)

THEOREM PROVED: `CategoryTheory.Center.ofBraided_ε_f`

Grade all 20 candidates below.

   1. `CategoryTheory.BraidedCategory`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `Sigma.fst`
      [def, depth 1, in-statement, role explicit-arg]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   4. `CategoryTheory.Center.instCategory`
      [def, depth 12, in-statement, role implicit-arg]
   5. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   7. `rfl`
      [def, depth 2, in-statement, role applied]
   8. `CategoryTheory.Center.instMonoidalCategory`
      [def, depth 30, in-statement, role implicit-arg]
   9. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  10. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `CategoryTheory.Center.instMonoidalOfBraided`
      [def, depth 34, in-statement, role instance-slot]
  12. `CategoryTheory.Functor.Monoidal.toLaxMonoidal`
      [def, depth 3, in-statement, role instance-slot]
  13. `CategoryTheory.Center.Hom.f`
      [def, depth 5, in-statement, role implicit-arg]
  14. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
  15. `CategoryTheory.HalfBraiding`
      [inductive, depth 2, in-statement, role implicit-arg]
  16. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  17. `CategoryTheory.Center`
      [def, depth 3, in-statement, role explicit-arg]
  18. `CategoryTheory.Functor.LaxMonoidal.ε`
      [def, depth 3, in-statement, role explicit-arg]
  19. `CategoryTheory.MonoidalCategoryStruct.tensorUnit`
      [def, depth 2, in-statement, role explicit-arg]
  20. `CategoryTheory.Center.ofBraided`
      [def, depth 15, in-statement, role explicit-arg]

### proof_172  (target depth 68, band 51-75)

THEOREM PROVED: `Set.Nonempty.ofIntrinsicClosure`

Grade all 13 candidates below.

   1. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   2. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Set.Nonempty`
      [def, depth 4, in-statement, role implicit-arg]
   4. `intrinsicClosure`
      [def, depth 65, in-statement, role explicit-arg]
   5. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   6. `AddTorsor`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `AddCommGroup.toAddGroup`
      [def, depth 1, in-statement, role instance-slot]
   8. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `intrinsicClosure_nonempty`
      [theorem, depth 67, introduced-by-proof, role explicit-arg]
  10. `Set`
      [def, depth 0, in-statement, role type-annotation]
  11. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Iff.mp`
      [theorem, depth 1, in-statement, role applied]
  13. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_173  (target depth 112, band 76-125)

THEOREM PROVED: `ENNReal.cancel_of_lt`

Grade all 9 candidates below.

   1. `Top.top`
      [def, depth 1, in-statement, role explicit-arg]
   2. `ENNReal.cancel_of_ne`
      [theorem, depth 111, introduced-by-proof, role applied]
   3. `ENNReal.instTop`
      [def, depth 97, in-statement, role instance-slot]
   4. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   5. `ENNReal.instPartialOrder`
      [def, depth 105, in-statement, role instance-slot]
   6. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
   7. `LT.lt.ne`
      [theorem, depth 6, in-statement, role explicit-arg]
   8. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
   9. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]

### proof_174  (target depth 216, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.dirac_prod_dirac`

Grade all 16 candidates below.

   1. `MeasureTheory.Measure.map_dirac'`
      [theorem, depth 193, introduced-by-proof, role explicit-arg]
   2. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   4. `MeasureTheory.Measure.dirac`
      [def, depth 163, in-statement, role explicit-arg]
   5. `MeasureTheory.Measure.prod_dirac`
      [theorem, depth 215, introduced-by-proof, role explicit-arg]
   6. `MeasureTheory.Measure.prod`
      [def, depth 206, in-statement, role explicit-arg]
   7. `MeasureTheory.Measure.map`
      [def, depth 188, in-statement, role explicit-arg]
   8. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   9. `Prod.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  10. `id`
      [def, depth 0, in-statement, role explicit-arg]
  11. `Prod.instMeasurableSpace`
      [def, depth 67, in-statement, role instance-slot]
  12. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  16. `measurable_prodMk_right`
      [theorem, depth 70, introduced-by-proof, role explicit-arg]

### proof_175  (target depth 4, band 0-10)

THEOREM PROVED: `CategoryTheory.Limits.hasFilteredColimitsOfSize_of_hasColimitsOfSize`

Grade all 6 candidates below.

   1. `CategoryTheory.Limits.HasFilteredColimitsOfSize.mk`
      [constructor, depth 2, introduced-by-proof, role applied]
   2. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.IsFiltered`
      [inductive, depth 1, introduced-by-proof, role type-annotation]
   4. `inferInstance`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Limits.HasColimitsOfShape`
      [inductive, depth 1, introduced-by-proof, role implicit-arg]
   6. `CategoryTheory.Limits.HasColimitsOfSize`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_176  (target depth 15, band 11-25)

THEOREM PROVED: `List.Sublist.flatten`

Grade all 7 candidates below.

   1. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `List.Sublist.rec`
      [recursor, depth 3, introduced-by-proof, role applied]
   3. `_private.Mathlib.Data.List.Flatten.0.List.Sublist.flatten._proof_1_2`
      [theorem, depth 13, introduced-by-proof, role explicit-arg]
   4. `List.flatten`
      [def, depth 8, in-statement, role explicit-arg]
   5. `_private.Mathlib.Data.List.Flatten.0.List.Sublist.flatten._proof_1_1`
      [theorem, depth 13, introduced-by-proof, role explicit-arg]
   6. `List.Sublist`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `_private.Mathlib.Data.List.Flatten.0.List.Sublist.flatten._proof_1_3`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]

### proof_177  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.Iso.conjAut_trans`

Grade all 4 candidates below.

   1. `CategoryTheory.Iso.conjAut_mul`
      [theorem, depth 26, introduced-by-proof, role applied]
   2. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `CategoryTheory.Aut`
      [def, depth 2, in-statement, role type-annotation]

### proof_178  (target depth 72, band 51-75)

THEOREM PROVED: `Continuous.mapPullback`

Grade all 22 candidates below.

   1. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   2. `Function.Pullback.fst`
      [def, depth 3, in-statement, role implicit-arg]
   3. `Prod.fst`
      [def, depth 1, in-statement, role explicit-arg]
   4. `continuous_subtype_val`
      [theorem, depth 69, introduced-by-proof, role explicit-arg]
   5. `Function.Pullback.snd`
      [def, depth 3, in-statement, role implicit-arg]
   6. `Continuous`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `Function.Pullback`
      [def, depth 2, in-statement, role implicit-arg]
   8. `Continuous.prodMk`
      [theorem, depth 71, introduced-by-proof, role explicit-arg]
   9. `instTopologicalSpaceProd`
      [def, depth 64, in-statement, role instance-slot]
  10. `TopologicalSpace.induced`
      [def, depth 63, in-statement, role instance-slot]
  11. `Continuous.comp`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  12. `continuous_fst`
      [theorem, depth 71, introduced-by-proof, role explicit-arg]
  13. `Function.mapPullback`
      [def, depth 6, in-statement, role explicit-arg]
  14. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
  15. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `continuous_induced_rng`
      [theorem, depth 69, introduced-by-proof, role explicit-arg]
  17. `Prod.snd`
      [def, depth 1, in-statement, role explicit-arg]
  18. `continuous_snd`
      [theorem, depth 71, introduced-by-proof, role explicit-arg]
  19. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `Subtype.val`
      [def, depth 1, in-statement, role implicit-arg]
  21. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
  22. `instTopologicalSpaceSubtype`
      [def, depth 64, in-statement, role implicit-arg]

### proof_179  (target depth 98, band 76-125)

THEOREM PROVED: `RingHom.finitePresentation_isStableUnderBaseChange`

Grade all 23 candidates below.

   1. `Algebra.TensorProduct.leftAlgebra`
      [def, depth 73, introduced-by-proof, role instance-slot]
   2. `RingHom.FinitePresentation`
      [def, depth 19, in-statement, role implicit-arg]
   3. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   4. `inferInstance`
      [def, depth 0, in-statement, role explicit-arg]
   5. `Algebra`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `Semiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
   7. `TensorProduct`
      [def, depth 39, introduced-by-proof, role explicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `_private.Mathlib.RingTheory.RingHom.FinitePresentation.0.RingHom.finitePresentation_isStableUnderBaseChange._simp_1_1`
      [theorem, depth 22, introduced-by-proof, role explicit-arg]
  10. `RingHom.finitePresentation_respectsIso`
      [theorem, depth 97, introduced-by-proof, role explicit-arg]
  11. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  12. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
  13. `Algebra.id`
      [def, depth 20, introduced-by-proof, role instance-slot]
  14. `implies_congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  15. `Algebra.algebraMap`
      [def, depth 2, in-statement, role explicit-arg]
  16. `CommRing`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `Algebra.FinitePresentation`
      [inductive, depth 2, in-statement, role implicit-arg]
  18. `Algebra.TensorProduct.instSemiring`
      [def, depth 71, introduced-by-proof, role implicit-arg]
  19. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  20. `RingHom.IsStableUnderBaseChange.mk`
      [theorem, depth 80, introduced-by-proof, role applied]
  21. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
  22. `Algebra.TensorProduct.instCommRing`
      [def, depth 75, introduced-by-proof, role instance-slot]
  23. `Algebra.toModule`
      [def, depth 18, introduced-by-proof, role instance-slot]

### proof_180  (target depth 162, band 126+)

THEOREM PROVED: `BoundedContinuousFunction.coe_sup`

Grade all 18 candidates below.

   1. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   2. `BoundedContinuousFunction`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
   4. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   5. `rfl`
      [def, depth 2, in-statement, role applied]
   6. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   7. `HasSolidNorm`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `IsOrderedAddMonoid`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Lattice`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  12. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  14. `BoundedContinuousFunction.instFunLike`
      [def, depth 99, in-statement, role instance-slot]
  15. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  16. `BoundedContinuousFunction.instSup`
      [def, depth 161, in-statement, role instance-slot]
  17. `Max.max`
      [def, depth 1, in-statement, role explicit-arg]
  18. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
