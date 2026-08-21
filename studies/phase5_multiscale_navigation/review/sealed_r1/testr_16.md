# Grading batch `testr_16` — 24 proofs

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

### proof_0361  (target depth 97, band 76-125)

THEOREM PROVED: `Polynomial.X_mem_lifts`

Grade all 18 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `RingHom.instFunLike`
      [def, depth 15, in-statement, role instance-slot]
   5. `Polynomial.map_X`
      [theorem, depth 93, introduced-by-proof, role explicit-arg]
   6. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   7. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   8. `Polynomial.semiring`
      [def, depth 84, in-statement, role instance-slot]
   9. `Exists.intro`
      [constructor, depth 1, in-statement, role applied]
  10. `RingHom`
      [inductive, depth 1, in-statement, role implicit-arg]
  11. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  12. `Polynomial.X`
      [def, depth 90, in-statement, role explicit-arg]
  13. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  14. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  16. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
  17. `Polynomial.mapRingHom`
      [def, depth 96, in-statement, role explicit-arg]
  18. `Polynomial`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0362  (target depth 76, band 76-125)

THEOREM PROVED: `Homeomorph.smulConst_symm_apply`

Grade all 11 candidates.

   1. `Homeomorph.symm`
      [def, depth 11, in-statement, role explicit-arg]
   2. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   3. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   4. `Homeomorph.instEquivLike`
      [def, depth 15, in-statement, role instance-slot]
   5. `Homeomorph`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `IsTopologicalTorsor`
      [inductive, depth 2, in-statement, role type-annotation]
   7. `Torsor`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Homeomorph.smulConst`
      [def, depth 75, in-statement, role explicit-arg]
  11. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]

### proof_0363  (target depth 96, band 76-125)

THEOREM PROVED: `SimpleGraph.IsEdgeConnected.connected`

Grade all 9 candidates.

   1. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Nonempty`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `SimpleGraph.IsEdgeConnected`
      [def, depth 91, in-statement, role type-annotation]
   5. `SimpleGraph.IsEdgeConnected.preconnected`
      [theorem, depth 95, introduced-by-proof, role explicit-arg]
   6. `SimpleGraph.Connected.mk`
      [constructor, depth 4, introduced-by-proof, role applied]
   7. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   8. `Ne`
      [def, depth 2, in-statement, role type-annotation]
   9. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0364  (target depth 101, band 76-125)

THEOREM PROVED: `MvPolynomial.uniqueAlgEquiv_symm_apply`

Grade all 22 candidates.

   1. `AddMonoidAlgebra.semiring`
      [def, depth 80, in-statement, role instance-slot]
   2. `Finsupp.instAddMonoid`
      [def, depth 65, in-statement, role instance-slot]
   3. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   4. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   6. `Finsupp`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `Unique`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Nat.instAddMonoid`
      [def, depth 16, in-statement, role instance-slot]
   9. `Polynomial.algebraOfAlgebra`
      [def, depth 96, in-statement, role instance-slot]
  10. `AlgEquiv.symm`
      [def, depth 18, in-statement, role explicit-arg]
  11. `Algebra.id`
      [def, depth 20, in-statement, role instance-slot]
  12. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
  13. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  14. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `AlgEquiv.instFunLike`
      [def, depth 21, in-statement, role instance-slot]
  16. `Nat.instMulZeroClass`
      [def, depth 17, in-statement, role instance-slot]
  17. `MvPolynomial`
      [def, depth 18, in-statement, role implicit-arg]
  18. `AddMonoidAlgebra.algebra`
      [def, depth 82, in-statement, role instance-slot]
  19. `Polynomial`
      [inductive, depth 1, in-statement, role type-annotation]
  20. `MvPolynomial.uniqueAlgEquiv`
      [def, depth 100, in-statement, role explicit-arg]
  21. `AlgEquiv`
      [inductive, depth 2, in-statement, role implicit-arg]
  22. `Polynomial.semiring`
      [def, depth 84, in-statement, role instance-slot]

### proof_0365  (target depth 78, band 76-125)

THEOREM PROVED: `IsAddTorsion.module_of_finite`

Grade all 9 candidates.

   1. `IsAddTorsion.module_of_torsion`
      [theorem, depth 27, introduced-by-proof, role applied]
   2. `Ring.toAddGroupWithOne`
      [def, depth 10, introduced-by-proof, role instance-slot]
   3. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Finite`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   7. `AddGroupWithOne.toAddGroup`
      [def, depth 10, introduced-by-proof, role instance-slot]
   8. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `isAddTorsion_of_finite`
      [theorem, depth 77, introduced-by-proof, role explicit-arg]

### proof_0366  (target depth 77, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.Const.minKey!_alter_eq_self`

Grade all 14 candidates.

   1. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   2. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   3. `Std.DTreeMap.Raw.Const.alter`
      [def, depth 40, in-statement, role explicit-arg]
   4. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Bool.false`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `Std.DTreeMap.Raw.isEmpty`
      [def, depth 18, in-statement, role explicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
  10. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Option`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
  14. `Std.DTreeMap.Internal.Impl.Const.minKey!_alter!_eq_self`
      [theorem, depth 76, introduced-by-proof, role applied]

### proof_0367  (target depth 76, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.getD_modify`

Grade all 8 candidates.

   1. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   2. `Std.LawfulEqCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
   4. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   6. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   7. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Std.DTreeMap.Internal.Impl.getD_modify`
      [theorem, depth 75, introduced-by-proof, role applied]

### proof_0368  (target depth 77, band 76-125)

THEOREM PROVED: `Std.ExtHashSet.size_insertMany_list`

Grade all 13 candidates.

   1. `BEq.beq`
      [def, depth 1, in-statement, role explicit-arg]
   2. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.ExtHashSet`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `List.Pairwise`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Std.ExtHashSet.inner`
      [def, depth 2, in-statement, role implicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  10. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `Bool.false`
      [constructor, depth 1, in-statement, role explicit-arg]
  13. `Std.ExtHashMap.size_insertManyIfNewUnit_list`
      [theorem, depth 76, introduced-by-proof, role applied]

### proof_0369  (target depth 77, band 76-125)

THEOREM PROVED: `HasSumUniformlyOn.mono`

Grade all 16 candidates.

   1. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   3. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   4. `TendstoUniformlyOn`
      [def, depth 6, introduced-by-proof, role implicit-arg]
   5. `HasSumUniformlyOn`
      [def, depth 72, in-statement, role implicit-arg]
   6. `HasSumUniformlyOn.tendstoUniformlyOn`
      [theorem, depth 76, introduced-by-proof, role explicit-arg]
   7. `Finset.instPartialOrder`
      [def, depth 54, in-statement, role instance-slot]
   8. `Finset.sum`
      [def, depth 13, in-statement, role explicit-arg]
   9. `Set`
      [def, depth 0, in-statement, role type-annotation]
  10. `UniformSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `hasSumUniformlyOn_iff_tendstoUniformlyOn`
      [theorem, depth 75, introduced-by-proof, role explicit-arg]
  12. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  13. `Filter.atTop`
      [def, depth 15, in-statement, role explicit-arg]
  14. `TendstoUniformlyOn.mono`
      [theorem, depth 66, introduced-by-proof, role explicit-arg]
  15. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]
  16. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0370  (target depth 87, band 76-125)

THEOREM PROVED: `EReal.toReal_coe`

Grade all 4 candidates.

   1. `EReal.toReal`
      [def, depth 86, in-statement, role implicit-arg]
   2. `Real.toEReal`
      [def, depth 3, in-statement, role explicit-arg]
   3. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `rfl`
      [def, depth 2, in-statement, role applied]

### proof_0371  (target depth 94, band 76-125)

THEOREM PROVED: `SimpleGraph.ConnectedComponent.card_le_card_of_le`

Grade all 9 candidates.

   1. `Nat.card_le_card_of_surjective`
      [theorem, depth 93, introduced-by-proof, role applied]
   2. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   3. `Finite`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `SimpleGraph.ConnectedComponent`
      [def, depth 3, in-statement, role implicit-arg]
   6. `SimpleGraph.ConnectedComponent.map`
      [def, depth 31, introduced-by-proof, role explicit-arg]
   7. `SimpleGraph.ConnectedComponent.surjective_map_ofLE`
      [theorem, depth 32, introduced-by-proof, role explicit-arg]
   8. `SimpleGraph.instLE`
      [def, depth 2, in-statement, role instance-slot]
   9. `SimpleGraph.Hom.ofLE`
      [def, depth 3, introduced-by-proof, role explicit-arg]

### proof_0372  (target depth 80, band 76-125)

THEOREM PROVED: `TopologicalSpace.Closeds.coe_prod`

Grade all 10 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `SProd.sprod`
      [def, depth 2, in-statement, role explicit-arg]
   4. `TopologicalSpace.Closeds.instSetLike`
      [def, depth 6, in-statement, role instance-slot]
   5. `TopologicalSpace.Closeds.instSProdProd`
      [def, depth 79, in-statement, role instance-slot]
   6. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   7. `SetLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   8. `TopologicalSpace.Closeds`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
  10. `instTopologicalSpaceProd`
      [def, depth 64, in-statement, role instance-slot]

### proof_0373  (target depth 197, band 126+)

THEOREM PROVED: `ContinuousOn.aestronglyMeasurable_of_isCompact`

Grade all 11 candidates.

   1. `ContinuousOn`
      [def, depth 50, in-statement, role type-annotation]
   2. `MeasurableSet`
      [def, depth 2, in-statement, role type-annotation]
   3. `Set`
      [def, depth 0, in-statement, role type-annotation]
   4. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `ContinuousOn.aestronglyMeasurable_of_subset_isCompact`
      [theorem, depth 196, introduced-by-proof, role applied]
   6. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `OpensMeasurableSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `IsCompact`
      [def, depth 49, in-statement, role type-annotation]
   9. `Set.Subset.rfl`
      [theorem, depth 5, in-statement, role explicit-arg]
  10. `TopologicalSpace.PseudoMetrizableSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0374  (target depth 151, band 126+)

THEOREM PROVED: `TendstoLocallyUniformly.mul₀`

Grade all 12 candidates.

   1. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `PseudoMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Filter`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `TendstoLocallyUniformly.smul₀`
      [theorem, depth 150, introduced-by-proof, role applied]
   5. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   6. `Continuous`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `instSMulOfMul`
      [def, depth 2, in-statement, role instance-slot]
   8. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `TendstoLocallyUniformly`
      [def, depth 19, in-statement, role type-annotation]
  10. `IsBoundedSMul`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Mul`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]

### proof_0375  (target depth 130, band 126+)

THEOREM PROVED: `MeasureTheory.inter_ae_eq_right_of_ae_eq_univ`

Grade all 19 candidates.

   1. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   2. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
   3. `id`
      [def, depth 0, in-statement, role explicit-arg]
   4. `Inter.inter`
      [def, depth 1, in-statement, role explicit-arg]
   5. `Iff`
      [inductive, depth 0, in-statement, role explicit-arg]
   6. `Set`
      [def, depth 0, in-statement, role type-annotation]
   7. `Filter.EventuallyEq`
      [def, depth 6, in-statement, role explicit-arg]
   8. `MeasureTheory.ae_eq_set_inter`
      [theorem, depth 129, introduced-by-proof, role explicit-arg]
   9. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  10. `Set.instInter`
      [def, depth 5, in-statement, role instance-slot]
  11. `ENNReal`
      [def, depth 96, in-statement, role explicit-arg]
  12. `Iff.rfl`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `MeasureTheory.OuterMeasureClass`
      [inductive, depth 97, in-statement, role type-annotation]
  14. `MeasureTheory.ae`
      [def, depth 128, in-statement, role explicit-arg]
  15. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `Set.univ_inter`
      [theorem, depth 20, in-statement, role explicit-arg]
  17. `Set.univ`
      [def, depth 2, in-statement, role explicit-arg]
  18. `FunLike`
      [def, depth 2, in-statement, role type-annotation]
  19. `MeasureTheory.ae_eq_refl`
      [theorem, depth 129, introduced-by-proof, role explicit-arg]

### proof_0376  (target depth 159, band 126+)

THEOREM PROVED: `IsIntegralCurve.isIntegralCurveOn`

Grade all 12 candidates.

   1. `IsIntegralCurve`
      [def, depth 155, in-statement, role type-annotation]
   2. `DenselyNormedField.toNontriviallyNormedField`
      [def, depth 111, in-statement, role instance-slot]
   3. `Real.normedField`
      [def, depth 150, in-statement, role instance-slot]
   4. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   5. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  10. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Real.denselyNormedField`
      [def, depth 153, in-statement, role instance-slot]
  12. `HasDerivAt.hasDerivWithinAt`
      [theorem, depth 158, introduced-by-proof, role applied]

### proof_0377  (target depth 198, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.restrict_sUnion_congr`

Grade all 18 candidates.

   1. `Set.Countable`
      [def, depth 5, in-statement, role type-annotation]
   2. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
   3. `Set.sUnion`
      [def, depth 5, in-statement, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `Iff`
      [inductive, depth 0, in-statement, role explicit-arg]
   6. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   7. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   9. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  10. `MeasureTheory.Measure.restrict`
      [def, depth 185, in-statement, role explicit-arg]
  11. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  12. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
  13. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  14. `MeasureTheory.Measure.restrict_biUnion_congr`
      [theorem, depth 197, introduced-by-proof, role explicit-arg]
  15. `Iff.rfl`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `Set.iUnion`
      [def, depth 5, in-statement, role explicit-arg]
  17. `id`
      [def, depth 0, in-statement, role explicit-arg]
  18. `Set.sUnion_eq_biUnion`
      [theorem, depth 60, in-statement, role explicit-arg]

### proof_0378  (target depth 155, band 126+)

THEOREM PROVED: `ClosedSubmodule.mem_orthogonal_toSubmodule_iff`

Grade all 25 candidates.

   1. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   2. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   3. `ClosedSubmodule`
      [inductive, depth 2, in-statement, role type-annotation]
   4. `ClosedSubmodule.toSubmodule`
      [def, depth 3, in-statement, role explicit-arg]
   5. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
   7. `NormedField.toField`
      [def, depth 1, in-statement, role instance-slot]
   8. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   9. `Iff.rfl`
      [theorem, depth 3, in-statement, role applied]
  10. `DenselyNormedField.toNormedField`
      [def, depth 1, in-statement, role implicit-arg]
  11. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  12. `Submodule.orthogonal`
      [def, depth 154, in-statement, role explicit-arg]
  13. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  14. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
  15. `InnerProductSpace`
      [inductive, depth 2, in-statement, role type-annotation]
  16. `NormedSpace.toModule`
      [def, depth 2, in-statement, role instance-slot]
  17. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
  18. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  19. `InnerProductSpace.toNormedSpace`
      [def, depth 3, in-statement, role instance-slot]
  20. `RCLike`
      [inductive, depth 1, in-statement, role type-annotation]
  21. `Submodule.setLike`
      [def, depth 12, in-statement, role instance-slot]
  22. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
  23. `RCLike.toDenselyNormedField`
      [def, depth 2, in-statement, role instance-slot]
  24. `Submodule`
      [inductive, depth 2, in-statement, role implicit-arg]
  25. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]

### proof_0379  (target depth 152, band 126+)

THEOREM PROVED: `NNReal.agm_pos`

Grade all 15 candidates.

   1. `lt_min`
      [theorem, depth 13, in-statement, role explicit-arg]
   2. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
   3. `NNReal.min_le_agm`
      [theorem, depth 151, introduced-by-proof, role explicit-arg]
   4. `LinearOrder.toMin`
      [def, depth 1, in-statement, role instance-slot]
   5. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   6. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   7. `NNReal.instLinearOrder`
      [def, depth 108, in-statement, role instance-slot]
   8. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   9. `NNReal`
      [def, depth 95, in-statement, role implicit-arg]
  10. `NNReal.instZero`
      [def, depth 103, in-statement, role instance-slot]
  11. `LT.lt.trans_le`
      [theorem, depth 5, in-statement, role applied]
  12. `Min.min`
      [def, depth 1, in-statement, role implicit-arg]
  13. `NNReal.instPartialOrder`
      [def, depth 102, in-statement, role instance-slot]
  14. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  15. `NNReal.agm`
      [def, depth 124, in-statement, role implicit-arg]

### proof_0380  (target depth 157, band 126+)

THEOREM PROVED: `Polynomial.natSepDegree_mul_of_isCoprime`

Grade all 25 candidates.

   1. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
   2. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
   3. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   4. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   5. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Polynomial.instZero`
      [def, depth 81, in-statement, role instance-slot]
   7. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   8. `Or.inr`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `Field`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
  11. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
  12. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  13. `And`
      [inductive, depth 0, in-statement, role explicit-arg]
  14. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
  15. `Polynomial.instMul`
      [def, depth 71, in-statement, role instance-slot]
  16. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Polynomial.natSepDegree`
      [def, depth 135, in-statement, role explicit-arg]
  18. `Semifield.toCommSemiring`
      [def, depth 1, in-statement, role instance-slot]
  19. `Or`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `Polynomial.natSepDegree_mul_eq_iff`
      [theorem, depth 156, introduced-by-proof, role explicit-arg]
  21. `Polynomial`
      [inductive, depth 1, in-statement, role implicit-arg]
  22. `IsCoprime`
      [def, depth 12, in-statement, role explicit-arg]
  23. `Polynomial.commSemiring`
      [def, depth 85, in-statement, role instance-slot]
  24. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  25. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]

### proof_0381  (target depth 148, band 126+)

THEOREM PROVED: `Metric.ball_infDist_compl_subset`

Grade all 11 candidates.

   1. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]
   2. `Set.instCompl`
      [def, depth 4, in-statement, role instance-slot]
   3. `Set.instBooleanAlgebra`
      [def, depth 56, in-statement, role instance-slot]
   4. `LE.le.trans_eq`
      [theorem, depth 4, in-statement, role applied]
   5. `Metric.infDist`
      [def, depth 142, in-statement, role explicit-arg]
   6. `Metric.ball`
      [def, depth 90, in-statement, role implicit-arg]
   7. `Metric.ball_infDist_subset_compl`
      [theorem, depth 147, introduced-by-proof, role explicit-arg]
   8. `PseudoMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Compl.compl`
      [def, depth 1, in-statement, role implicit-arg]
  10. `compl_compl`
      [theorem, depth 54, in-statement, role explicit-arg]
  11. `Set`
      [def, depth 0, in-statement, role implicit-arg]

### proof_0382  (target depth 163, band 126+)

THEOREM PROVED: `Topology.RelCWComplex.Subcomplex.finiteType_subcomplex_of_finiteType`

Grade all 18 candidates.

   1. `Topology.RelCWComplex.Subcomplex.instSetLike`
      [def, depth 151, in-statement, role instance-slot]
   2. `Topology.RelCWComplex.Subcomplex.instRelCWComplex`
      [def, depth 162, in-statement, role instance-slot]
   3. `T2Space`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Topology.RelCWComplex.FiniteType.mk`
      [constructor, depth 3, introduced-by-proof, role applied]
   6. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   7. `Subtype.finite`
      [theorem, depth 62, introduced-by-proof, role explicit-arg]
   8. `Topology.RelCWComplex.FiniteType.finite_cell`
      [theorem, depth 3, introduced-by-proof, role let-value]
   9. `Topology.RelCWComplex.FiniteType`
      [inductive, depth 2, in-statement, role type-annotation]
  10. `Finite`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  12. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `SetLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
  14. `Set`
      [def, depth 0, in-statement, role type-annotation]
  15. `Topology.RelCWComplex.Subcomplex.I`
      [def, depth 3, in-statement, role explicit-arg]
  16. `Topology.RelCWComplex.cell`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Topology.RelCWComplex`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `Topology.RelCWComplex.Subcomplex`
      [inductive, depth 2, in-statement, role implicit-arg]

### proof_0383  (target depth 198, band 126+)

THEOREM PROVED: `MeasureTheory.Measure.add_left_inj`

Grade all 19 candidates.

   1. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   2. `MeasureTheory.SigmaFinite`
      [inductive, depth 2, in-statement, role type-annotation]
   3. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   5. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `MeasureTheory.Measure.add_right_inj`
      [theorem, depth 197, introduced-by-proof, role explicit-arg]
   7. `add_comm`
      [theorem, depth 2, in-statement, role explicit-arg]
   8. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
  10. `id`
      [def, depth 0, in-statement, role explicit-arg]
  11. `MeasureTheory.Measure.instAdd`
      [def, depth 167, in-statement, role instance-slot]
  12. `AddCommMonoid.toAddCommSemigroup`
      [def, depth 5, in-statement, role instance-slot]
  13. `AddCommMagma.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  14. `Iff`
      [inductive, depth 0, in-statement, role explicit-arg]
  15. `MeasureTheory.Measure.instAddCommMonoid`
      [def, depth 170, introduced-by-proof, role instance-slot]
  16. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  17. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  18. `AddCommSemigroup.toAddCommMagma`
      [def, depth 5, in-statement, role instance-slot]
  19. `Iff.rfl`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_0384  (target depth 150, band 126+)

THEOREM PROVED: `Filter.Tendsto.norm`

Grade all 13 candidates.

   1. `Filter.Tendsto`
      [def, depth 13, in-statement, role type-annotation]
   2. `nhds`
      [def, depth 18, in-statement, role implicit-arg]
   3. `Norm.norm`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Filter.Tendsto.comp`
      [theorem, depth 14, introduced-by-proof, role applied]
   5. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   6. `tendsto_norm`
      [theorem, depth 149, introduced-by-proof, role explicit-arg]
   7. `Real.pseudoMetricSpace`
      [def, depth 113, in-statement, role instance-slot]
   8. `Filter`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `SeminormedAddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
  12. `SeminormedAddGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  13. `SeminormedAddGroup.toNorm`
      [def, depth 1, in-statement, role instance-slot]
