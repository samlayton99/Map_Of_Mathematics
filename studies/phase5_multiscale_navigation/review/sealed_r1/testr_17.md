# Grading batch `testr_17` — 24 proofs

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

### proof_0385  (target depth 172, band 126+)

THEOREM PROVED: `MeasureTheory.AEEqFun.smul_mk`

Grade all 12 candidates.

   1. `HSMul.hSMul`
      [def, depth 2, in-statement, role implicit-arg]
   2. `ContinuousConstSMul`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `MeasureTheory.AEEqFun.instSMul`
      [def, depth 171, in-statement, role instance-slot]
   5. `MeasureTheory.AEEqFun.mk`
      [def, depth 168, in-statement, role explicit-arg]
   6. `MeasureTheory.AEStronglyMeasurable`
      [def, depth 165, in-statement, role type-annotation]
   7. `instHSMul`
      [def, depth 3, in-statement, role instance-slot]
   8. `SMul`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `rfl`
      [def, depth 2, in-statement, role applied]
  10. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `MeasureTheory.AEEqFun`
      [def, depth 168, in-statement, role implicit-arg]

### proof_0386  (target depth 162, band 126+)

THEOREM PROVED: `conformal_id`

Grade all 6 candidates.

   1. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   4. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `conformalAt_id`
      [theorem, depth 161, introduced-by-proof, role applied]
   6. `Real.normedField`
      [def, depth 150, in-statement, role instance-slot]

### proof_0387  (target depth 167, band 126+)

THEOREM PROVED: `MDifferentiable.fst`

Grade all 20 candidates.

   1. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `ModelWithCorners.prod`
      [def, depth 158, in-statement, role explicit-arg]
   5. `MDifferentiable.comp`
      [theorem, depth 166, introduced-by-proof, role applied]
   6. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `instTopologicalSpaceModelProd`
      [def, depth 66, in-statement, role instance-slot]
   8. `ChartedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `ModelWithCorners`
      [inductive, depth 11, in-statement, role type-annotation]
  10. `Prod.fst`
      [def, depth 1, in-statement, role implicit-arg]
  11. `Prod.normedSpace`
      [def, depth 151, in-statement, role instance-slot]
  12. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  13. `ModelProd`
      [def, depth 1, in-statement, role implicit-arg]
  14. `instTopologicalSpaceProd`
      [def, depth 64, in-statement, role instance-slot]
  15. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  16. `mdifferentiable_fst`
      [theorem, depth 164, introduced-by-proof, role explicit-arg]
  17. `MDifferentiable`
      [def, depth 64, in-statement, role type-annotation]
  18. `prodChartedSpace`
      [def, depth 78, in-statement, role instance-slot]
  19. `Prod.normedAddCommGroup`
      [def, depth 149, in-statement, role instance-slot]
  20. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0388  (target depth 195, band 126+)

THEOREM PROVED: `NNReal.rpow_eq_rpow_iff`

Grade all 11 candidates.

   1. `Ne`
      [def, depth 2, in-statement, role type-annotation]
   2. `NNReal.instPowReal`
      [def, depth 191, in-statement, role instance-slot]
   3. `NNReal.rpow_left_injective`
      [theorem, depth 194, introduced-by-proof, role explicit-arg]
   4. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Real.instZero`
      [def, depth 85, in-statement, role instance-slot]
   6. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   7. `NNReal`
      [def, depth 95, in-statement, role implicit-arg]
   8. `Function.Injective.eq_iff`
      [theorem, depth 4, in-statement, role applied]
   9. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  10. `HPow.hPow`
      [def, depth 2, in-statement, role implicit-arg]
  11. `instHPow`
      [def, depth 3, in-statement, role instance-slot]

### proof_0389  (target depth 190, band 126+)

THEOREM PROVED: `ProbabilityTheory.cond_mul_eq_inter`

Grade all 7 candidates.

   1. `Set`
      [def, depth 0, in-statement, role type-annotation]
   2. `ProbabilityTheory.cond_mul_eq_inter'`
      [theorem, depth 189, introduced-by-proof, role applied]
   3. `MeasureTheory.measure_ne_top`
      [theorem, depth 166, introduced-by-proof, role explicit-arg]
   4. `MeasureTheory.IsFiniteMeasure`
      [inductive, depth 2, in-statement, role type-annotation]
   5. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `MeasurableSet`
      [def, depth 2, in-statement, role type-annotation]

### proof_0390  (target depth 198, band 126+)

THEOREM PROVED: `Meromorphic.logDeriv_zpow_eventuallyEq`

Grade all 17 candidates.

   1. `Int`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `NormedField.toNormedCommRing`
      [def, depth 103, in-statement, role instance-slot]
   3. `NormedAlgebra.toNormedSpace`
      [def, depth 97, in-statement, role instance-slot]
   4. `NormedCommRing.toNonUnitalNormedCommRing`
      [def, depth 96, in-statement, role instance-slot]
   5. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   6. `NonUnitalNormedCommRing.toNonUnitalNormedRing`
      [def, depth 1, in-statement, role instance-slot]
   7. `MeromorphicOn.logDeriv_zpow_eventuallyEq`
      [theorem, depth 197, introduced-by-proof, role applied]
   8. `Meromorphic`
      [def, depth 161, in-statement, role implicit-arg]
   9. `Set.univ`
      [def, depth 2, in-statement, role explicit-arg]
  10. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `meromorphicOn_univ`
      [theorem, depth 162, introduced-by-proof, role explicit-arg]
  12. `SeminormedCommRing.toSeminormedRing`
      [def, depth 1, in-statement, role instance-slot]
  13. `NormedAlgebra`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `Iff.mpr`
      [theorem, depth 1, in-statement, role explicit-arg]
  15. `NormedCommRing.toSeminormedCommRing`
      [def, depth 96, in-statement, role instance-slot]
  16. `MeromorphicOn`
      [def, depth 161, introduced-by-proof, role implicit-arg]
  17. `NonUnitalNormedRing.toNormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]

### proof_0391  (target depth 151, band 126+)

THEOREM PROVED: `DilationEquiv.mulLeft_apply`

Grade all 18 candidates.

   1. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   2. `instMulZeroClassOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
   3. `DivisionRing.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
   4. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   5. `EMetricSpace.toPseudoEMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   6. `DilationEquiv.instEquivLike`
      [def, depth 145, in-statement, role instance-slot]
   7. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   8. `NormedDivisionRing.toDivisionRing`
      [def, depth 1, in-statement, role instance-slot]
   9. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
  10. `MetricSpace.toEMetricSpace`
      [def, depth 145, in-statement, role instance-slot]
  11. `DilationEquiv`
      [inductive, depth 1, in-statement, role implicit-arg]
  12. `Ne`
      [def, depth 2, in-statement, role type-annotation]
  13. `DilationEquiv.mulLeft`
      [def, depth 150, in-statement, role explicit-arg]
  14. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  15. `NormedDivisionRing.toMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  16. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  17. `NormedDivisionRing`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]

### proof_0392  (target depth 129, band 126+)

THEOREM PROVED: `MeasureTheory.ae_eq_set_symmDiff`

Grade all 7 candidates.

   1. `Filter.EventuallyEq`
      [def, depth 6, in-statement, role type-annotation]
   2. `MeasureTheory.OuterMeasureClass`
      [inductive, depth 97, in-statement, role type-annotation]
   3. `MeasureTheory.ae`
      [def, depth 128, in-statement, role explicit-arg]
   4. `FunLike`
      [def, depth 2, in-statement, role type-annotation]
   5. `ENNReal`
      [def, depth 96, in-statement, role explicit-arg]
   6. `Set`
      [def, depth 0, in-statement, role type-annotation]
   7. `Filter.EventuallyEq.symmDiff`
      [theorem, depth 14, introduced-by-proof, role applied]

### proof_0393  (target depth 130, band 126+)

THEOREM PROVED: `IsCyclotomicExtension.finiteDimensional`

Grade all 15 candidates.

   1. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
   2. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Field`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Set`
      [def, depth 0, in-statement, role type-annotation]
   5. `IsDomain`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Semifield.toCommSemiring`
      [def, depth 1, in-statement, role instance-slot]
   7. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
   8. `IsCyclotomicExtension.finite`
      [theorem, depth 129, introduced-by-proof, role applied]
   9. `Finite`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `IsCyclotomicExtension`
      [inductive, depth 6, in-statement, role type-annotation]
  11. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
  13. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
  14. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  15. `Field.toCommRing`
      [def, depth 1, in-statement, role instance-slot]

### proof_0394  (target depth 162, band 126+)

THEOREM PROVED: `DifferentiableAt.fun_add`

Grade all 19 candidates.

   1. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   2. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   3. `AddCommSemigroup.toAddCommMagma`
      [def, depth 5, in-statement, role instance-slot]
   4. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   5. `AddCommMagma.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   6. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   9. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
  10. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role implicit-arg]
  11. `AddCommMonoid.toAddCommSemigroup`
      [def, depth 5, in-statement, role instance-slot]
  12. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
  13. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `DifferentiableAt`
      [def, depth 61, in-statement, role type-annotation]
  15. `id`
      [def, depth 0, in-statement, role applied]
  16. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  17. `NormedSpace.toModule`
      [def, depth 2, in-statement, role instance-slot]
  18. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  19. `DifferentiableAt.add`
      [theorem, depth 161, introduced-by-proof, role explicit-arg]

### proof_0395  (target depth 137, band 126+)

THEOREM PROVED: `FundamentalGroup.mapOfEq_apply`

Grade all 21 candidates.

   1. `CategoryTheory.End`
      [def, depth 2, in-statement, role implicit-arg]
   2. `FundamentalGroupoid.conj_eqToHom`
      [theorem, depth 134, introduced-by-proof, role applied]
   3. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `FundamentalGroupoid.as`
      [def, depth 1, in-statement, role implicit-arg]
   6. `MonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
   7. `ContinuousMap`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  10. `FundamentalGroup`
      [def, depth 134, in-statement, role type-annotation]
  11. `FundamentalGroup.map`
      [def, depth 136, in-statement, role explicit-arg]
  12. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  13. `FundamentalGroupoid`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `ContinuousMap.instFunLike`
      [def, depth 13, in-statement, role instance-slot]
  15. `CategoryTheory.Groupoid.toCategory`
      [def, depth 1, in-statement, role instance-slot]
  16. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `FundamentalGroupoid.instGroupoid`
      [def, depth 133, in-statement, role instance-slot]
  18. `FundamentalGroupoid.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  19. `MonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]
  20. `CategoryTheory.End.monoid`
      [def, depth 10, in-statement, role instance-slot]
  21. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]

### proof_0396  (target depth 209, band 126+)

THEOREM PROVED: `WithLp.prod_lipschitzWith_ofLp`

Grade all 9 candidates.

   1. `Fact`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   3. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
   4. `ENNReal.instOne`
      [def, depth 104, in-statement, role instance-slot]
   5. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
   6. `ENNReal.instLE`
      [def, depth 104, in-statement, role instance-slot]
   7. `PseudoEMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `_private.Mathlib.Analysis.Normed.Lp.ProdLp.0.WithLp.prod_lipschitzWith_ofLp_aux`
      [theorem, depth 208, in-statement, role applied]
   9. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]

### proof_0397  (target depth 150, band 126+)

THEOREM PROVED: `LipschitzOnWith.of_neg`

Grade all 17 candidates.

   1. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]
   2. `AddCommGroup.toDivisionAddCommMonoid`
      [def, depth 12, in-statement, role instance-slot]
   3. `SubtractionCommMonoid.toSubtractionMonoid`
      [def, depth 1, in-statement, role instance-slot]
   4. `SubNegZeroMonoid.toNegZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   5. `Set`
      [def, depth 0, in-statement, role type-annotation]
   6. `LipschitzOnWith`
      [def, depth 141, in-statement, role implicit-arg]
   7. `PseudoMetricSpace.toPseudoEMetricSpace`
      [def, depth 115, in-statement, role instance-slot]
   8. `NegZeroClass.toNeg`
      [def, depth 1, in-statement, role instance-slot]
   9. `lipschitzOnWith_neg_iff`
      [theorem, depth 149, introduced-by-proof, role explicit-arg]
  10. `NNReal`
      [def, depth 95, in-statement, role type-annotation]
  11. `SubtractionMonoid.toSubNegZeroMonoid`
      [def, depth 9, in-statement, role instance-slot]
  12. `Pi.instNeg`
      [def, depth 2, in-statement, role instance-slot]
  13. `SeminormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `SeminormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
  15. `Iff.mp`
      [theorem, depth 1, in-statement, role applied]
  16. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  17. `PseudoEMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0398  (target depth 156, band 126+)

THEOREM PROVED: `LinearIsometryEquiv.toContinuousLinearEquiv_symm`

Grade all 16 candidates.

   1. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   2. `SeminormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `RingHom`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   5. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   6. `LinearIsometryEquiv.toContinuousLinearEquiv`
      [def, depth 155, in-statement, role implicit-arg]
   7. `RingHomInvPair`
      [inductive, depth 11, in-statement, role type-annotation]
   8. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   9. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  10. `ContinuousLinearEquiv`
      [inductive, depth 12, in-statement, role implicit-arg]
  11. `SeminormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
  12. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `rfl`
      [def, depth 2, in-statement, role applied]
  15. `LinearIsometryEquiv.symm`
      [def, depth 151, in-statement, role explicit-arg]
  16. `LinearIsometryEquiv`
      [inductive, depth 12, in-statement, role type-annotation]

### proof_0399  (target depth 200, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.ext_of_sUnion_eq_univ`

Grade all 12 candidates.

   1. `MeasureTheory.Measure.restrict`
      [def, depth 185, in-statement, role explicit-arg]
   2. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   3. `MeasureTheory.Measure.ext_iff_of_sUnion_eq_univ`
      [theorem, depth 199, introduced-by-proof, role explicit-arg]
   4. `Set.sUnion`
      [def, depth 5, in-statement, role explicit-arg]
   5. `Set.Countable`
      [def, depth 5, in-statement, role type-annotation]
   6. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Set.univ`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  10. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
  11. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  12. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0400  (target depth 204, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.withDensity.instSigmaFinite`

Grade all 7 candidates.

   1. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `MeasureTheory.Measure.sigmaFinite_of_le`
      [theorem, depth 170, introduced-by-proof, role applied]
   3. `MeasureTheory.Measure.withDensity`
      [def, depth 195, in-statement, role implicit-arg]
   4. `MeasureTheory.Measure.withDensity_rnDeriv_le`
      [theorem, depth 203, introduced-by-proof, role explicit-arg]
   5. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `MeasureTheory.Measure.rnDeriv`
      [def, depth 199, in-statement, role explicit-arg]
   7. `MeasureTheory.SigmaFinite`
      [inductive, depth 2, in-statement, role type-annotation]

### proof_0401  (target depth 162, band 126+)

THEOREM PROVED: `HasFDerivWithinAt.congr'`

Grade all 19 candidates.

   1. `HasFDerivWithinAt`
      [def, depth 60, in-statement, role type-annotation]
   2. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
   4. `ContinuousLinearMap`
      [inductive, depth 11, in-statement, role type-annotation]
   5. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   6. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   7. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `NormedField.toField`
      [def, depth 1, in-statement, role instance-slot]
  10. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
  14. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  15. `Set.EqOn`
      [def, depth 4, in-statement, role type-annotation]
  16. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  17. `HasFDerivWithinAt.congr`
      [theorem, depth 161, introduced-by-proof, role applied]
  18. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
  19. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]

### proof_0402  (target depth 171, band 126+)

THEOREM PROVED: `AEMeasurable.nullMeasurable`

Grade all 12 candidates.

   1. `MeasureTheory.NullMeasurable.congr`
      [theorem, depth 170, introduced-by-proof, role explicit-arg]
   2. `Filter.EventuallyEq.symm`
      [theorem, depth 10, in-statement, role explicit-arg]
   3. `Measurable.nullMeasurable`
      [theorem, depth 165, introduced-by-proof, role explicit-arg]
   4. `MeasureTheory.NullMeasurable`
      [def, depth 168, in-statement, role explicit-arg]
   5. `MeasureTheory.ae`
      [def, depth 128, in-statement, role explicit-arg]
   6. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `AEMeasurable`
      [def, depth 165, in-statement, role type-annotation]
   8. `_private.Mathlib.MeasureTheory.Measure.MeasureSpace.0.AEMeasurable.nullMeasurable.match_1_1`
      [def, depth 166, introduced-by-proof, role applied]
   9. `Measurable`
      [def, depth 5, in-statement, role type-annotation]
  10. `Filter.EventuallyEq`
      [def, depth 6, in-statement, role type-annotation]
  11. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
  12. `MeasureTheory.Measure.instFunLike`
      [def, depth 163, in-statement, role instance-slot]

### proof_0403  (target depth 201, band 126+)

THEOREM PROVED: `ProbabilityTheory.Kernel.IsSFiniteKernel.fst`

Grade all 14 candidates.

   1. `ProbabilityTheory.Kernel.map`
      [def, depth 196, introduced-by-proof, role explicit-arg]
   2. `ProbabilityTheory.Kernel`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `ProbabilityTheory.IsSFiniteKernel`
      [inductive, depth 2, in-statement, role explicit-arg]
   5. `Prod.instMeasurableSpace`
      [def, depth 67, in-statement, role implicit-arg]
   6. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Prod.fst`
      [def, depth 1, in-statement, role explicit-arg]
   8. `ProbabilityTheory.Kernel.fst_eq`
      [theorem, depth 198, introduced-by-proof, role explicit-arg]
   9. `inferInstance`
      [def, depth 0, in-statement, role explicit-arg]
  10. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  12. `ProbabilityTheory.Kernel.fst`
      [def, depth 196, in-statement, role explicit-arg]
  13. `id`
      [def, depth 0, in-statement, role explicit-arg]
  14. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0404  (target depth 169, band 126+)

THEOREM PROVED: `LightCondMod.LocallyConstant.instFaithfulModuleCatLightCondensedDiscrete`

Grade all 23 candidates.

   1. `Opposite`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `And`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `LightCondensed.discrete`
      [def, depth 104, in-statement, role implicit-arg]
   5. `ModuleCat.moduleCategory`
      [def, depth 25, in-statement, role instance-slot]
   6. `SecondCountableTopology`
      [inductive, depth 1, in-statement, role explicit-arg]
   7. `ModuleCat`
      [inductive, depth 1, in-statement, role explicit-arg]
   8. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   9. `TopCat.carrier`
      [def, depth 1, in-statement, role explicit-arg]
  10. `LightCondMod.LocallyConstant.functorIsoDiscrete`
      [def, depth 165, introduced-by-proof, role explicit-arg]
  11. `LightProfinite`
      [def, depth 2, in-statement, role explicit-arg]
  12. `CategoryTheory.Presheaf.IsSheaf`
      [def, depth 28, in-statement, role explicit-arg]
  13. `CategoryTheory.Functor.Faithful.of_iso`
      [theorem, depth 25, introduced-by-proof, role applied]
  14. `LightCondensed`
      [def, depth 103, in-statement, role implicit-arg]
  15. `TopCat.str`
      [def, depth 1, in-statement, role instance-slot]
  16. `CategoryTheory.ObjectProperty.FullSubcategory.category`
      [def, depth 10, in-statement, role instance-slot]
  17. `CategoryTheory.coherentTopology`
      [def, depth 30, in-statement, role explicit-arg]
  18. `TotallyDisconnectedSpace`
      [inductive, depth 1, in-statement, role explicit-arg]
  19. `CompHausLike.category`
      [def, depth 20, in-statement, role instance-slot]
  20. `TopCat`
      [inductive, depth 0, in-statement, role type-annotation]
  21. `LightCondMod.LocallyConstant.functor`
      [def, depth 110, introduced-by-proof, role implicit-arg]
  22. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]
  23. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]

### proof_0405  (target depth 252, band 126+)

THEOREM PROVED: `ProbabilityTheory.Kernel.integral_integral_add'`

Grade all 21 candidates.

   1. `ProbabilityTheory.Kernel.instFunLike`
      [def, depth 169, in-statement, role instance-slot]
   2. `ProbabilityTheory.Kernel.integral_integral_add`
      [theorem, depth 251, introduced-by-proof, role applied]
   3. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   4. `Real.normedField`
      [def, depth 150, in-statement, role instance-slot]
   5. `SeminormedAddCommGroup.toSeminormedAddGroup`
      [def, depth 10, in-statement, role instance-slot]
   6. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   7. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
   8. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `MeasureTheory.Integrable`
      [def, depth 170, in-statement, role type-annotation]
  10. `Prod.instMeasurableSpace`
      [def, depth 67, in-statement, role instance-slot]
  11. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `ProbabilityTheory.Kernel.compProd`
      [def, depth 217, in-statement, role explicit-arg]
  13. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
  14. `SeminormedAddGroup.toContinuousENorm`
      [def, depth 152, in-statement, role instance-slot]
  15. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
  16. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  17. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  18. `ProbabilityTheory.Kernel`
      [inductive, depth 1, in-statement, role implicit-arg]
  19. `ProbabilityTheory.IsSFiniteKernel`
      [inductive, depth 2, in-statement, role type-annotation]
  20. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  21. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0406  (target depth 127, band 126+)

THEOREM PROVED: `AlgebraicGeometry.AffineScheme.forgetToScheme_map`

Grade all 20 candidates.

   1. `AlgebraicGeometry.AffineScheme`
      [def, depth 125, in-statement, role implicit-arg]
   2. `CategoryTheory.ObjectProperty.FullSubcategory`
      [inductive, depth 2, in-statement, role implicit-arg]
   3. `AlgebraicGeometry.AffineScheme.forgetToScheme`
      [def, depth 125, in-statement, role explicit-arg]
   4. `AlgebraicGeometry.Scheme.instCategory`
      [def, depth 89, in-statement, role instance-slot]
   5. `AlgebraicGeometry.instCategoryAffineScheme`
      [def, depth 126, in-statement, role instance-slot]
   6. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   7. `CategoryTheory.ObjectProperty.FullSubcategory.obj`
      [def, depth 3, in-statement, role explicit-arg]
   8. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  10. `CategoryTheory.Functor.essImage`
      [def, depth 3, in-statement, role explicit-arg]
  11. `AlgebraicGeometry.Scheme.Spec`
      [def, depth 124, in-statement, role explicit-arg]
  12. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  13. `CategoryTheory.Functor.map`
      [def, depth 2, in-statement, role explicit-arg]
  14. `CommRingCat`
      [inductive, depth 0, in-statement, role explicit-arg]
  15. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  16. `CommRingCat.instCategory`
      [def, depth 20, in-statement, role instance-slot]
  17. `CategoryTheory.InducedCategory.instCategory`
      [def, depth 10, in-statement, role instance-slot]
  18. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  19. `CategoryTheory.InducedCategory`
      [def, depth 0, in-statement, role implicit-arg]
  20. `AlgebraicGeometry.Scheme`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0407  (target depth 180, band 126+)

THEOREM PROVED: `HasGradientWithinAt.congr_of_mem`

Grade all 13 candidates.

   1. `InnerProductSpace`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   4. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   5. `HasGradientWithinAt`
      [def, depth 177, in-statement, role type-annotation]
   6. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   7. `CompleteSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `RCLike`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `HasGradientWithinAt.congr`
      [theorem, depth 179, introduced-by-proof, role applied]
  11. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  12. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  13. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]

### proof_0408  (target depth 199, band 126+)

THEOREM PROVED: `ContDiffBump.contDiff`

Grade all 19 candidates.

   1. `NormedField.toNormedSpace`
      [def, depth 105, in-statement, role instance-slot]
   2. `ContDiff.contDiffBump`
      [theorem, depth 198, introduced-by-proof, role applied]
   3. `ContDiffBump`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `ContDiffBump.rOut`
      [def, depth 1, in-statement, role implicit-arg]
   5. `contDiff_const`
      [theorem, depth 192, introduced-by-proof, role explicit-arg]
   6. `Real.denselyNormedField`
      [def, depth 153, in-statement, role instance-slot]
   7. `Real.normedAddCommGroup`
      [def, depth 148, in-statement, role instance-slot]
   8. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `HasContDiffBump`
      [inductive, depth 151, in-statement, role type-annotation]
  10. `WithTop.some`
      [def, depth 2, in-statement, role implicit-arg]
  11. `ContDiffBump.rIn`
      [def, depth 1, in-statement, role implicit-arg]
  12. `DenselyNormedField.toNontriviallyNormedField`
      [def, depth 111, in-statement, role instance-slot]
  13. `ENat`
      [def, depth 2, in-statement, role implicit-arg]
  14. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  15. `Real.normedField`
      [def, depth 150, in-statement, role instance-slot]
  16. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
  17. `contDiff_id`
      [theorem, depth 193, introduced-by-proof, role explicit-arg]
  18. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  19. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
