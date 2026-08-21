# Grading batch `testr_18` — 24 proofs

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

### proof_0409  (target depth 169, band 126+)

THEOREM PROVED: `NumberField.mixedEmbedding.fundamentalCone.expMap_apply`

Grade all 12 candidates.

   1. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Field`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `NumberField`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `NumberField.InfinitePlace`
      [def, depth 135, in-statement, role type-annotation]
   5. `OpenPartialHomeomorph.toFun'`
      [def, depth 3, in-statement, role implicit-arg]
   6. `Real.pseudoMetricSpace`
      [def, depth 113, in-statement, role instance-slot]
   7. `Pi.topologicalSpace`
      [def, depth 64, in-statement, role instance-slot]
   8. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   9. `rfl`
      [def, depth 2, in-statement, role applied]
  10. `NumberField.mixedEmbedding.realSpace`
      [def, depth 136, in-statement, role implicit-arg]
  11. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  12. `NumberField.mixedEmbedding.fundamentalCone.expMap`
      [def, depth 168, in-statement, role explicit-arg]

### proof_0410  (target depth 180, band 126+)

THEOREM PROVED: `ModularForm.coe_const`

Grade all 25 candidates.

   1. `Matrix.GeneralLinearGroup`
      [def, depth 82, in-statement, role explicit-arg]
   2. `Semiring.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
   3. `Real.semiring`
      [def, depth 94, in-statement, role instance-slot]
   4. `ModularForm.const`
      [def, depth 177, in-statement, role explicit-arg]
   5. `Real.commRing`
      [def, depth 92, in-statement, role instance-slot]
   6. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   7. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
   8. `instDecidableEqFin`
      [def, depth 12, in-statement, role instance-slot]
   9. `Subgroup.HasDetOne`
      [inductive, depth 83, in-statement, role type-annotation]
  10. `UpperHalfPlane`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Units.instGroup`
      [def, depth 20, in-statement, role instance-slot]
  12. `Matrix.semiring`
      [def, depth 81, in-statement, role instance-slot]
  13. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  14. `instOfNat`
      [def, depth 3, in-statement, role instance-slot]
  15. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  16. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `ModularForm.funLike`
      [def, depth 179, in-statement, role instance-slot]
  19. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  20. `Subgroup`
      [inductive, depth 1, in-statement, role type-annotation]
  21. `Matrix`
      [def, depth 0, in-statement, role implicit-arg]
  22. `Fin.fintype`
      [def, depth 55, in-statement, role instance-slot]
  23. `Complex`
      [inductive, depth 0, in-statement, role implicit-arg]
  24. `ModularForm`
      [inductive, depth 95, in-statement, role implicit-arg]
  25. `Fin`
      [inductive, depth 1, in-statement, role explicit-arg]

### proof_0411  (target depth 137, band 126+)

THEOREM PROVED: `Polynomial.splits_mul_X`

Grade all 25 candidates.

   1. `NonUnitalNonAssocCommRing.toNonUnitalNonAssocCommSemiring`
      [def, depth 5, introduced-by-proof, role instance-slot]
   2. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Polynomial.commRing`
      [def, depth 87, introduced-by-proof, role instance-slot]
   4. `NonUnitalCommRing.toNonUnitalNonAssocCommRing`
      [def, depth 5, introduced-by-proof, role instance-slot]
   5. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `Polynomial.splits_X_mul._simp_1`
      [theorem, depth 136, introduced-by-proof, role explicit-arg]
   7. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   8. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  10. `CommRing.toNonUnitalCommRing`
      [def, depth 10, introduced-by-proof, role instance-slot]
  11. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
  12. `mul_comm`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  13. `Polynomial.Splits`
      [def, depth 93, in-statement, role explicit-arg]
  14. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `Polynomial.X`
      [def, depth 90, in-statement, role explicit-arg]
  17. `NonUnitalNonAssocCommSemiring.toCommMagma`
      [def, depth 5, introduced-by-proof, role instance-slot]
  18. `Polynomial`
      [inductive, depth 1, in-statement, role implicit-arg]
  19. `CommMagma.toMul`
      [def, depth 1, introduced-by-proof, role instance-slot]
  20. `IsDomain`
      [inductive, depth 1, in-statement, role type-annotation]
  21. `Polynomial.instMul`
      [def, depth 71, in-statement, role instance-slot]
  22. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
  23. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  24. `iff_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  25. `instHMul`
      [def, depth 3, in-statement, role instance-slot]

### proof_0412  (target depth 201, band 126+)

THEOREM PROVED: `ProbabilityTheory.IdentDistrib.const_add`

Grade all 9 candidates.

   1. `ProbabilityTheory.IdentDistrib.comp`
      [theorem, depth 200, introduced-by-proof, role applied]
   2. `MeasurableAdd`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `MeasurableAdd.measurable_const_add`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   4. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `HAdd.hAdd`
      [def, depth 2, in-statement, role implicit-arg]
   6. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   7. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Add`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `ProbabilityTheory.IdentDistrib`
      [inductive, depth 9, in-statement, role type-annotation]

### proof_0413  (target depth 196, band 126+)

THEOREM PROVED: `Real.contDiff_exp`

Grade all 10 candidates.

   1. `Complex.instDenselyNormedField`
      [def, depth 137, introduced-by-proof, role instance-slot]
   2. `Complex.contDiff_exp`
      [theorem, depth 192, introduced-by-proof, role explicit-arg]
   3. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   4. `Complex.exp`
      [def, depth 139, in-statement, role implicit-arg]
   5. `ENat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `ContDiff.real_of_complex`
      [theorem, depth 195, introduced-by-proof, role applied]
   7. `DenselyNormedField.toNontriviallyNormedField`
      [def, depth 111, in-statement, role instance-slot]
   8. `Complex`
      [inductive, depth 0, in-statement, role explicit-arg]
   9. `NormedAlgebra.id`
      [def, depth 107, introduced-by-proof, role instance-slot]
  10. `WithTop`
      [def, depth 1, in-statement, role type-annotation]

### proof_0414  (target depth 141, band 126+)

THEOREM PROVED: `isConjRoot_iff_exists_algEquiv`

Grade all 24 candidates.

   1. `Semifield.toCommSemiring`
      [def, depth 1, in-statement, role instance-slot]
   2. `Eq.rec`
      [recursor, depth 2, in-statement, role explicit-arg]
   3. `Normal`
      [inductive, depth 45, in-statement, role type-annotation]
   4. `isConjRoot_of_algEquiv`
      [theorem, depth 108, introduced-by-proof, role explicit-arg]
   5. `Field`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `_private.Mathlib.FieldTheory.Minpoly.IsConjRoot.0.isConjRoot_iff_exists_algEquiv.match_1_1`
      [def, depth 45, introduced-by-proof, role explicit-arg]
   7. `Field.toCommRing`
      [def, depth 1, in-statement, role instance-slot]
   8. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `IsConjRoot.symm`
      [theorem, depth 84, introduced-by-proof, role explicit-arg]
  10. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
  11. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  12. `Exists`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `AlgEquiv.instFunLike`
      [def, depth 21, in-statement, role instance-slot]
  14. `IsConjRoot.exists_algEquiv`
      [theorem, depth 140, introduced-by-proof, role explicit-arg]
  15. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
  16. `AlgEquiv`
      [inductive, depth 2, in-statement, role implicit-arg]
  17. `Field.toDivisionRing`
      [def, depth 44, in-statement, role instance-slot]
  18. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
  19. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  20. `IsConjRoot`
      [def, depth 83, in-statement, role implicit-arg]
  21. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  22. `DivisionRing.toRing`
      [def, depth 1, in-statement, role instance-slot]
  23. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
  24. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0415  (target depth 168, band 126+)

THEOREM PROVED: `AEMeasurable.neg`

Grade all 8 candidates.

   1. `MeasurableNeg.measurable_neg`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   2. `AEMeasurable`
      [def, depth 165, in-statement, role type-annotation]
   3. `Measurable.comp_aemeasurable`
      [theorem, depth 167, introduced-by-proof, role applied]
   4. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `MeasurableNeg`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Neg.neg`
      [def, depth 1, in-statement, role implicit-arg]
   8. `Neg`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0416  (target depth 128, band 126+)

THEOREM PROVED: `BoxIntegral.BoxAdditiveMap.ext_iff`

Grade all 15 candidates.

   1. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
   2. `HEq.refl`
      [constructor, depth 1, in-statement, role unresolved]
   3. `BoxIntegral.BoxAdditiveMap.instFunLikeBox`
      [def, depth 126, in-statement, role instance-slot]
   4. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `BoxIntegral.Box`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Eq.casesOn`
      [def, depth 3, in-statement, role explicit-arg]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   9. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `BoxIntegral.BoxAdditiveMap`
      [inductive, depth 2, in-statement, role implicit-arg]
  11. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
  12. `WithTop`
      [def, depth 1, in-statement, role type-annotation]
  13. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `HEq`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `BoxIntegral.BoxAdditiveMap.ext`
      [theorem, depth 127, introduced-by-proof, role explicit-arg]

### proof_0417  (target depth 129, band 126+)

THEOREM PROVED: `AlgebraicGeometry.IsOpenImmersion.instPreservesLimitSchemeTopCatWalkingCospanCospanForgetToTop_1`

Grade all 10 candidates.

   1. `AlgebraicGeometry.Scheme`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `AlgebraicGeometry.IsOpenImmersion`
      [def, depth 90, in-statement, role type-annotation]
   3. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   4. `AlgebraicGeometry.Scheme.forgetToTop`
      [def, depth 92, in-statement, role explicit-arg]
   5. `TopCat`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `TopCat.instCategory`
      [def, depth 18, in-statement, role instance-slot]
   7. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   8. `AlgebraicGeometry.Scheme.instCategory`
      [def, depth 89, in-statement, role instance-slot]
   9. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  10. `CategoryTheory.Limits.preservesPullback_symmetry`
      [theorem, depth 36, introduced-by-proof, role applied]

### proof_0418  (target depth 188, band 126+)

THEOREM PROVED: `Meromorphic.div`

Grade all 12 candidates.

   1. `NonUnitalNormedCommRing.toNonUnitalNormedRing`
      [def, depth 1, in-statement, role instance-slot]
   2. `SeminormedCommRing.toSeminormedRing`
      [def, depth 1, in-statement, role instance-slot]
   3. `Meromorphic`
      [def, depth 161, in-statement, role type-annotation]
   4. `NormedField.toNormedCommRing`
      [def, depth 103, in-statement, role instance-slot]
   5. `MeromorphicAt.div`
      [theorem, depth 187, introduced-by-proof, role applied]
   6. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   8. `NormedCommRing.toSeminormedCommRing`
      [def, depth 96, in-statement, role instance-slot]
   9. `NormedAlgebra`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `NormedCommRing.toNonUnitalNormedCommRing`
      [def, depth 96, in-statement, role instance-slot]
  11. `NormedAlgebra.toNormedSpace`
      [def, depth 97, in-statement, role instance-slot]
  12. `NonUnitalNormedRing.toNormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]

### proof_0419  (target depth 180, band 126+)

THEOREM PROVED: `VectorBundleCore.trivializationAt_symmL`

Grade all 24 candidates.

   1. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `FiberBundleCore.indexAt`
      [def, depth 2, in-statement, role implicit-arg]
   5. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   7. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   8. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   9. `VectorBundleCore.Fiber`
      [def, depth 175, in-statement, role explicit-arg]
  10. `Bundle.TotalSpace.proj`
      [def, depth 1, in-statement, role implicit-arg]
  11. `VectorBundleCore.toTopologicalSpace`
      [def, depth 177, in-statement, role instance-slot]
  12. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  13. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
  14. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  15. `VectorBundleCore.localTriv_symmL`
      [theorem, depth 179, introduced-by-proof, role applied]
  16. `Bundle.Trivialization.baseSet`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Bundle.TotalSpace`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  19. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  20. `VectorBundleCore`
      [inductive, depth 11, in-statement, role type-annotation]
  21. `VectorBundleCore.toFiberBundleCore`
      [def, depth 174, in-statement, role explicit-arg]
  22. `FiberBundle.trivializationAt`
      [def, depth 3, in-statement, role explicit-arg]
  23. `VectorBundleCore.topologicalSpaceFiber`
      [def, depth 176, in-statement, role instance-slot]
  24. `VectorBundleCore.fiberBundle`
      [def, depth 178, in-statement, role instance-slot]

### proof_0420  (target depth 198, band 126+)

THEOREM PROVED: `ContDiff.prodMap`

Grade all 22 candidates.

   1. `contDiff_iff_contDiffAt`
      [theorem, depth 189, introduced-by-proof, role explicit-arg]
   2. `_private.Mathlib.Analysis.Calculus.ContDiff.Operations.0.ContDiff.prodMap.match_1_1`
      [def, depth 4, introduced-by-proof, role explicit-arg]
   3. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
   4. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   5. `ContDiff`
      [def, depth 165, in-statement, role implicit-arg]
   6. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   7. `Prod.normedSpace`
      [def, depth 151, in-statement, role instance-slot]
   8. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   9. `WithTop`
      [def, depth 1, in-statement, role type-annotation]
  10. `ContDiffAt.prodMap`
      [theorem, depth 197, introduced-by-proof, role explicit-arg]
  11. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `ContDiffAt`
      [def, depth 166, introduced-by-proof, role type-annotation]
  13. `Prod.normedAddCommGroup`
      [def, depth 149, in-statement, role instance-slot]
  14. `ENat`
      [def, depth 2, in-statement, role explicit-arg]
  15. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]
  16. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `id`
      [def, depth 0, in-statement, role explicit-arg]
  18. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  19. `Prod.map`
      [def, depth 5, in-statement, role explicit-arg]
  20. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  21. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  22. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0421  (target depth 161, band 126+)

THEOREM PROVED: `ProbabilityTheory.stieltjesOfMeasurableRat_nonneg`

Grade all 9 candidates.

   1. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `ProbabilityTheory.IsMeasurableRatCDF.stieltjesFunction_nonneg`
      [theorem, depth 160, introduced-by-proof, role applied]
   4. `Rat`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Measurable`
      [def, depth 5, in-statement, role type-annotation]
   6. `Real.measurableSpace`
      [def, depth 114, in-statement, role instance-slot]
   7. `ProbabilityTheory.isMeasurableRatCDF_toRatCDF`
      [theorem, depth 160, in-statement, role explicit-arg]
   8. `MeasurableSpace.pi`
      [def, depth 66, in-statement, role instance-slot]
   9. `ProbabilityTheory.toRatCDF`
      [def, depth 87, in-statement, role implicit-arg]

### proof_0422  (target depth 140, band 126+)

THEOREM PROVED: `AlgebraicGeometry.Scheme.RationalMap.toRationalMap_representative`

Grade all 7 candidates.

   1. `Exists.choose_spec`
      [theorem, depth 8, in-statement, role applied]
   2. `AlgebraicGeometry.Scheme`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `AlgebraicGeometry.Scheme.PartialMap`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `AlgebraicGeometry.Scheme.PartialMap.toRationalMap`
      [def, depth 138, in-statement, role explicit-arg]
   6. `AlgebraicGeometry.Scheme.RationalMap.exists_rep`
      [theorem, depth 139, in-statement, role explicit-arg]
   7. `AlgebraicGeometry.Scheme.RationalMap`
      [def, depth 138, in-statement, role implicit-arg]

### proof_0423  (target depth 192, band 126+)

THEOREM PROVED: `MeasureTheory.eLpNorm_top_piecewise`

Grade all 10 candidates.

   1. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   4. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `ESeminormedAddMonoid`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `MeasureTheory.eLpNormEssSup_piecewise`
      [theorem, depth 191, introduced-by-proof, role applied]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `DecidablePred`
      [def, depth 1, in-statement, role type-annotation]
  10. `MeasurableSet`
      [def, depth 2, in-statement, role type-annotation]

### proof_0424  (target depth 168, band 126+)

THEOREM PROVED: `AEMeasurable.coe_real_ereal`

Grade all 10 candidates.

   1. `measurable_coe_real_ereal`
      [theorem, depth 122, introduced-by-proof, role explicit-arg]
   2. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `EReal`
      [def, depth 2, in-statement, role implicit-arg]
   5. `Measurable.comp_aemeasurable`
      [theorem, depth 167, introduced-by-proof, role applied]
   6. `Real.measurableSpace`
      [def, depth 114, in-statement, role instance-slot]
   7. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Real.toEReal`
      [def, depth 3, in-statement, role implicit-arg]
   9. `AEMeasurable`
      [def, depth 165, in-statement, role type-annotation]
  10. `EReal.measurableSpace`
      [def, depth 104, in-statement, role instance-slot]

### proof_0425  (target depth 166, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.mem_support_iff_forall`

Grade all 11 candidates.

   1. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   2. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `id`
      [def, depth 0, in-statement, role implicit-arg]
   4. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   5. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Filter.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   7. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Filter`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Filter.basis_sets`
      [theorem, depth 8, in-statement, role explicit-arg]
  10. `Filter.HasBasis.mem_measureSupport`
      [theorem, depth 165, introduced-by-proof, role applied]
  11. `nhds`
      [def, depth 18, in-statement, role explicit-arg]

### proof_0426  (target depth 161, band 126+)

THEOREM PROVED: `CircleDeg1Lift.lt_map_of_nat_lt_translationNumber`

Grade all 11 candidates.

   1. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   2. `CircleDeg1Lift.translationNumber`
      [def, depth 114, in-statement, role explicit-arg]
   3. `CircleDeg1Lift.lt_map_of_int_lt_translationNumber`
      [theorem, depth 160, introduced-by-proof, role applied]
   4. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `CircleDeg1Lift`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `instNatCastInt`
      [def, depth 2, in-statement, role instance-slot]
   7. `Real.instNatCast`
      [def, depth 82, in-statement, role instance-slot]
   8. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Real.instLT`
      [def, depth 89, in-statement, role instance-slot]
  10. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Nat.cast`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0427  (target depth 171, band 126+)

THEOREM PROVED: `MeasureTheory.ProbabilityMeasure.coeFn_toFiniteMeasure`

Grade all 9 candidates.

   1. `MeasureTheory.ProbabilityMeasure`
      [def, depth 3, in-statement, role type-annotation]
   2. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `rfl`
      [def, depth 2, in-statement, role applied]
   4. `MeasureTheory.FiniteMeasure.instFunLike`
      [def, depth 170, in-statement, role instance-slot]
   5. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   6. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   7. `NNReal`
      [def, depth 95, in-statement, role implicit-arg]
   8. `MeasureTheory.FiniteMeasure`
      [def, depth 3, in-statement, role implicit-arg]
   9. `MeasureTheory.ProbabilityMeasure.toFiniteMeasure`
      [def, depth 168, in-statement, role explicit-arg]

### proof_0428  (target depth 133, band 126+)

THEOREM PROVED: `Quotient.instPathConnectedSpace`

Grade all 9 candidates.

   1. `continuous_coinduced_rng`
      [theorem, depth 64, introduced-by-proof, role explicit-arg]
   2. `Quotient.mk'_surjective`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   3. `PathConnectedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `instTopologicalSpaceQuotient`
      [def, depth 64, in-statement, role instance-slot]
   5. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Quotient`
      [def, depth 2, in-statement, role implicit-arg]
   7. `Quotient.mk'`
      [def, depth 3, in-statement, role implicit-arg]
   8. `Function.Surjective.pathConnectedSpace`
      [theorem, depth 132, introduced-by-proof, role applied]
   9. `Setoid`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0429  (target depth 161, band 126+)

THEOREM PROVED: `ContinuousLinearMap.normOneClass`

Grade all 22 candidates.

   1. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
   2. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   4. `ContinuousLinearMap`
      [inductive, depth 11, in-statement, role implicit-arg]
   5. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `ContinuousLinearMap.norm_id`
      [theorem, depth 160, introduced-by-proof, role explicit-arg]
   7. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   8. `ContinuousLinearMap.one`
      [def, depth 19, in-statement, role instance-slot]
   9. `SeminormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
  10. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  11. `SeminormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `NormedField.toField`
      [def, depth 1, in-statement, role instance-slot]
  13. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  14. `ContinuousLinearMap.hasOpNorm`
      [def, depth 115, in-statement, role instance-slot]
  15. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
  16. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  17. `NormOneClass.mk`
      [constructor, depth 86, introduced-by-proof, role applied]
  18. `NontrivialTopology`
      [inductive, depth 1, in-statement, role type-annotation]
  19. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
  20. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
  21. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  22. `NormedSpace.toModule`
      [def, depth 2, in-statement, role instance-slot]

### proof_0430  (target depth 168, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.interior_eq_empty_of_null`

Grade all 17 candidates.

   1. `interior`
      [def, depth 6, in-statement, role implicit-arg]
   2. `ENNReal.instZero`
      [def, depth 104, in-statement, role instance-slot]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `MeasureTheory.Measure.instFunLike`
      [def, depth 163, in-statement, role instance-slot]
   6. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   7. `isOpen_interior`
      [theorem, depth 6, in-statement, role explicit-arg]
   8. `interior_subset`
      [theorem, depth 60, in-statement, role explicit-arg]
   9. `IsOpen.eq_empty_of_measure_zero`
      [theorem, depth 167, introduced-by-proof, role applied]
  10. `Set`
      [def, depth 0, in-statement, role type-annotation]
  11. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
  13. `MeasureTheory.Measure.IsOpenPosMeasure`
      [inductive, depth 2, in-statement, role type-annotation]
  14. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  15. `MeasureTheory.measure_mono_null`
      [theorem, depth 108, introduced-by-proof, role explicit-arg]
  16. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
  17. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0431  (target depth 196, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.comap_swap`

Grade all 6 candidates.

   1. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `MeasurableEquiv.prodComm`
      [def, depth 71, introduced-by-proof, role explicit-arg]
   5. `Prod.instMeasurableSpace`
      [def, depth 67, in-statement, role implicit-arg]
   6. `MeasurableEquiv.comap_symm`
      [theorem, depth 195, introduced-by-proof, role applied]

### proof_0432  (target depth 196, band 126+)

THEOREM PROVED: `MeasureTheory.MeasurePreserving.setLIntegral_comp_preimage_emb`

Grade all 19 candidates.

   1. `MeasureTheory.Measure.map`
      [def, depth 188, introduced-by-proof, role explicit-arg]
   2. `id`
      [def, depth 0, in-statement, role explicit-arg]
   3. `MeasurableEmbedding`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `MeasurableEmbedding.restrict_map`
      [theorem, depth 194, introduced-by-proof, role explicit-arg]
   5. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `MeasurableEmbedding.lintegral_map`
      [theorem, depth 195, introduced-by-proof, role explicit-arg]
   7. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
   9. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
  10. `MeasureTheory.MeasurePreserving.map_eq`
      [theorem, depth 10, introduced-by-proof, role explicit-arg]
  11. `MeasureTheory.lintegral`
      [def, depth 168, in-statement, role explicit-arg]
  12. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  14. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  15. `MeasureTheory.MeasurePreserving`
      [inductive, depth 9, in-statement, role type-annotation]
  16. `Set.preimage`
      [def, depth 4, in-statement, role explicit-arg]
  17. `Set`
      [def, depth 0, in-statement, role type-annotation]
  18. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  19. `MeasureTheory.Measure.restrict`
      [def, depth 185, in-statement, role explicit-arg]
