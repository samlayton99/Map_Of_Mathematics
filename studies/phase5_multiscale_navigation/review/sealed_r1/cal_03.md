# Grading batch `cal_03` — 24 proofs

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

### proof_0049  (target depth 95, band 76-125)

THEOREM PROVED: `compact_exists_isClopen_in_isOpen`

Grade all 21 candidates.

   1. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   2. `TopologicalSpace.IsTopologicalBasis.mem_nhds_iff`
      [theorem, depth 64, introduced-by-proof, role explicit-arg]
   3. `Filter.instMembership`
      [def, depth 4, introduced-by-proof, role instance-slot]
   4. `IsClopen`
      [def, depth 3, in-statement, role explicit-arg]
   5. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   7. `IsOpen`
      [def, depth 2, in-statement, role type-annotation]
   8. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Exists`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `T2Space`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `TotallyDisconnectedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `CompactSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `Iff.mp`
      [theorem, depth 1, introduced-by-proof, role applied]
  14. `isTopologicalBasis_isClopen`
      [theorem, depth 94, introduced-by-proof, role explicit-arg]
  15. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
  16. `Filter`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  17. `IsOpen.mem_nhds`
      [theorem, depth 59, introduced-by-proof, role explicit-arg]
  18. `nhds`
      [def, depth 18, introduced-by-proof, role explicit-arg]
  19. `Set.ofPred`
      [def, depth 1, introduced-by-proof, role explicit-arg]
  20. `And`
      [inductive, depth 0, in-statement, role explicit-arg]
  21. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]

### proof_0050  (target depth 80, band 76-125)

THEOREM PROVED: `Finset.prod_set_coe`

Grade all 14 candidates.

   1. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
   2. `Finset.univ`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   4. `Set.mem_toFinset`
      [theorem, depth 55, introduced-by-proof, role explicit-arg]
   5. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   6. `CommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Finset.prod`
      [def, depth 13, in-statement, role implicit-arg]
   8. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
  10. `Eq.symm`
      [theorem, depth 3, in-statement, role applied]
  11. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  12. `Set.toFinset`
      [def, depth 27, in-statement, role explicit-arg]
  13. `Finset.prod_subtype`
      [theorem, depth 79, introduced-by-proof, role explicit-arg]
  14. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0051  (target depth 81, band 76-125)

THEOREM PROVED: `Std.ExtTreeMap.ordCompare_minKey!_modify_eq`

Grade all 6 candidates.

   1. `Std.TransOrd`
      [def, depth 2, in-statement, role type-annotation]
   2. `Ord.compare`
      [def, depth 1, in-statement, role explicit-arg]
   3. `Std.ExtTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   4. `Ord`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Std.ExtTreeMap.compare_minKey!_modify_eq`
      [theorem, depth 80, introduced-by-proof, role applied]
   6. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0052  (target depth 95, band 76-125)

THEOREM PROVED: `ModuleCat.free_δ_freeMk`

Grade all 8 candidates.

   1. `CategoryTheory.types`
      [def, depth 10, in-statement, role implicit-arg]
   2. `CategoryTheory.MonoidalCategoryStruct.tensorObj`
      [def, depth 2, in-statement, role type-annotation]
   3. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `CategoryTheory.CartesianMonoidalCategory.toSemiCartesianMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
   5. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
   6. `CategoryTheory.typesCartesianMonoidalCategory`
      [def, depth 38, in-statement, role instance-slot]
   7. `ModuleCat.FreeMonoidal.μIso_inv_freeMk`
      [theorem, depth 94, in-statement, role applied]
   8. `CategoryTheory.SemiCartesianMonoidalCategory.toMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]

### proof_0053  (target depth 80, band 76-125)

THEOREM PROVED: `Continuous.piecewise`

Grade all 9 candidates.

   1. `frontier`
      [def, depth 7, in-statement, role explicit-arg]
   2. `Continuous`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   4. `Decidable`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   6. `Continuous.if`
      [theorem, depth 79, introduced-by-proof, role applied]
   7. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   8. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0054  (target depth 89, band 76-125)

THEOREM PROVED: `Polynomial.supp_subset_range`

Grade all 17 candidates.

   1. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   2. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Polynomial.natDegree`
      [def, depth 25, in-statement, role explicit-arg]
   4. `Polynomial.le_natDegree_of_mem_supp`
      [theorem, depth 88, introduced-by-proof, role explicit-arg]
   5. `Polynomial.support`
      [def, depth 12, in-statement, role explicit-arg]
   6. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
   8. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
   9. `Nat.instPreorder`
      [def, depth 20, introduced-by-proof, role instance-slot]
  10. `Finset.mem_range`
      [theorem, depth 22, introduced-by-proof, role explicit-arg]
  11. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  12. `Polynomial`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Finset.range`
      [def, depth 53, in-statement, role explicit-arg]
  15. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
  16. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  17. `LE.le.trans_lt`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]

### proof_0055  (target depth 78, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.contains_ofList`

Grade all 15 candidates.

   1. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Std.DTreeMap.Internal.Impl.contains_insertMany_empty_list`
      [theorem, depth 77, introduced-by-proof, role explicit-arg]
   4. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Std.DTreeMap.Raw.ofList`
      [def, depth 64, in-statement, role explicit-arg]
   8. `Sigma`
      [inductive, depth 0, in-statement, role explicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Std.DTreeMap.Raw.contains`
      [def, depth 18, in-statement, role explicit-arg]
  11. `List.contains`
      [def, depth 7, in-statement, role explicit-arg]
  12. `id`
      [def, depth 0, in-statement, role applied]
  13. `Std.LawfulBEqCmp`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `List.map`
      [def, depth 6, in-statement, role explicit-arg]
  15. `Sigma.fst`
      [def, depth 1, in-statement, role explicit-arg]

### proof_0056  (target depth 78, band 76-125)

THEOREM PROVED: `ContinuousWithinAt.nsmul`

Grade all 11 candidates.

   1. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `nhdsWithin`
      [def, depth 48, in-statement, role implicit-arg]
   4. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   5. `ContinuousAdd`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Set`
      [def, depth 0, in-statement, role type-annotation]
   7. `Filter.Tendsto.nsmul`
      [theorem, depth 77, introduced-by-proof, role applied]
   8. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   9. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  10. `ContinuousWithinAt`
      [def, depth 49, in-statement, role type-annotation]
  11. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0057  (target depth 82, band 76-125)

THEOREM PROVED: `LocallyConstant.congrRightₗ_symm_apply_apply`

Grade all 17 candidates.

   1. `LocallyConstant.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
   2. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
   3. `LocallyConstant`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `LocallyConstant.instAddCommMonoid`
      [def, depth 74, in-statement, role instance-slot]
   5. `LocallyConstant.congrRightₗ`
      [def, depth 81, in-statement, role explicit-arg]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   7. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   9. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  12. `LinearEquiv`
      [inductive, depth 12, in-statement, role implicit-arg]
  13. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  14. `LocallyConstant.instModule`
      [def, depth 78, in-statement, role implicit-arg]
  15. `LinearEquiv.instEquivLike`
      [def, depth 25, in-statement, role instance-slot]
  16. `LinearEquiv.symm`
      [def, depth 26, in-statement, role explicit-arg]
  17. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0058  (target depth 82, band 76-125)

THEOREM PROVED: `Std.ExtTreeMap.getElem_eq_get_getElem?`

Grade all 7 candidates.

   1. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.ExtTreeMap.instMembershipOfTransCmp`
      [def, depth 79, in-statement, role instance-slot]
   3. `Std.ExtTreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]
   4. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Std.ExtDTreeMap.Const.get_eq_get_get?`
      [theorem, depth 81, introduced-by-proof, role applied]
   6. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   7. `Std.ExtTreeMap`
      [inductive, depth 16, in-statement, role implicit-arg]

### proof_0059  (target depth 86, band 76-125)

THEOREM PROVED: `QuaternionAlgebra.instFinite`

Grade all 20 candidates.

   1. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
   2. `CommRing.toNonAssocCommRing`
      [def, depth 11, in-statement, role instance-slot]
   3. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   4. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `AddCommGroupWithOne.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
   6. `QuaternionAlgebra.instRing`
      [def, depth 41, in-statement, role instance-slot]
   7. `NonAssocRing.toAddCommGroupWithOne`
      [def, depth 10, in-statement, role instance-slot]
   8. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   9. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  10. `Fin.fintype`
      [def, depth 55, introduced-by-proof, role instance-slot]
  11. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Semiring.toModule`
      [def, depth 13, in-statement, role instance-slot]
  13. `QuaternionAlgebra`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `QuaternionAlgebra.basisOneIJK`
      [def, depth 75, introduced-by-proof, role explicit-arg]
  15. `Fin`
      [inductive, depth 1, introduced-by-proof, role explicit-arg]
  16. `QuaternionAlgebra.instModule`
      [def, depth 21, in-statement, role instance-slot]
  17. `Semiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
  18. `NonAssocCommRing.toNonAssocRing`
      [def, depth 1, in-statement, role instance-slot]
  19. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  20. `Module.Finite.of_basis`
      [theorem, depth 85, introduced-by-proof, role applied]

### proof_0060  (target depth 103, band 76-125)

THEOREM PROVED: `String.Slice.posGT_eq_posGE`

Grade all 8 candidates.

   1. `String.Slice.Pos`
      [inductive, depth 1, in-statement, role implicit-arg]
   2. `String.instLTRaw`
      [def, depth 4, in-statement, role instance-slot]
   3. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   4. `String.Pos.Raw`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `String.Slice.posGT`
      [def, depth 102, in-statement, role implicit-arg]
   6. `rfl`
      [def, depth 2, in-statement, role applied]
   7. `String.Slice`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `String.Slice.rawEndPos`
      [def, depth 11, in-statement, role explicit-arg]

### proof_0061  (target depth 151, band 126+)

THEOREM PROVED: `RCLike.ofReal_neg`

Grade all 15 candidates.

   1. `DivisionRing.toRing`
      [def, depth 1, in-statement, role instance-slot]
   2. `RCLike.toNormedAlgebra`
      [def, depth 2, in-statement, role instance-slot]
   3. `Real.commRing`
      [def, depth 92, in-statement, role instance-slot]
   4. `RCLike.toDenselyNormedField`
      [def, depth 2, in-statement, role instance-slot]
   5. `algebraMap.coe_neg`
      [theorem, depth 17, introduced-by-proof, role applied]
   6. `DenselyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   7. `Field.toDivisionRing`
      [def, depth 44, in-statement, role instance-slot]
   8. `Real.normedField`
      [def, depth 150, in-statement, role implicit-arg]
   9. `NormedCommRing.toSeminormedCommRing`
      [def, depth 96, in-statement, role instance-slot]
  10. `NormedAlgebra.toAlgebra`
      [def, depth 2, in-statement, role instance-slot]
  11. `RCLike`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `NormedField.toField`
      [def, depth 1, in-statement, role instance-slot]
  14. `NormedField.toNormedCommRing`
      [def, depth 103, in-statement, role instance-slot]
  15. `SeminormedCommRing.toSeminormedRing`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0062  (target depth 158, band 126+)

THEOREM PROVED: `extChartAt_model_space_eq_id`

Grade all 21 candidates.

   1. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   2. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   3. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   4. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   6. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `extChartAt`
      [def, depth 24, in-statement, role explicit-arg]
   8. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `modelWithCornersSelf`
      [def, depth 157, in-statement, role explicit-arg]
  11. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  12. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  14. `PartialEquiv`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `PartialEquiv.refl`
      [def, depth 26, in-statement, role explicit-arg]
  16. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  17. `PartialEquiv.trans_refl`
      [theorem, depth 27, introduced-by-proof, role explicit-arg]
  18. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  19. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `chartedSpaceSelf`
      [def, depth 79, in-statement, role instance-slot]
  21. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]

### proof_0063  (target depth 138, band 126+)

THEOREM PROVED: `AlgebraicGeometry.Scheme.PartialIso.ext`

Grade all 19 candidates.

   1. `AlgebraicGeometry.Scheme.isoOfEq`
      [def, depth 131, in-statement, role explicit-arg]
   2. `AlgebraicGeometry.Scheme.PartialIso.ext_iff`
      [theorem, depth 137, introduced-by-proof, role explicit-arg]
   3. `Exists`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `AlgebraicGeometry.Scheme.PartialIso.target`
      [def, depth 2, in-statement, role explicit-arg]
   6. `CategoryTheory.Iso.trans`
      [def, depth 15, in-statement, role explicit-arg]
   7. `id`
      [def, depth 0, in-statement, role explicit-arg]
   8. `AlgebraicGeometry.Scheme`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `AlgebraicGeometry.Scheme.PartialIso.source`
      [def, depth 2, in-statement, role explicit-arg]
  10. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `AlgebraicGeometry.Scheme.PartialIso`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `AlgebraicGeometry.Scheme.Opens`
      [def, depth 21, in-statement, role implicit-arg]
  13. `AlgebraicGeometry.Scheme.PartialIso.iso`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  15. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role implicit-arg]
  16. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  17. `Exists.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
  18. `AlgebraicGeometry.Scheme.Opens.toScheme`
      [def, depth 128, in-statement, role implicit-arg]
  19. `AlgebraicGeometry.Scheme.instCategory`
      [def, depth 89, in-statement, role instance-slot]

### proof_0064  (target depth 202, band 126+)

THEOREM PROVED: `IsometryEquiv.measurePreserving_hausdorffMeasure`

Grade all 16 candidates.

   1. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   2. `IsometryEquiv`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   4. `IsometryEquiv.instEquivLike`
      [def, depth 148, in-statement, role instance-slot]
   5. `IsometryEquiv.continuous`
      [theorem, depth 149, introduced-by-proof, role explicit-arg]
   6. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `EMetricSpace.toPseudoEMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   8. `Continuous.measurable`
      [theorem, depth 63, introduced-by-proof, role explicit-arg]
   9. `IsometryEquiv.map_hausdorffMeasure`
      [theorem, depth 201, introduced-by-proof, role explicit-arg]
  10. `EMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `MeasureTheory.MeasurePreserving.mk`
      [constructor, depth 189, introduced-by-proof, role applied]
  12. `MeasureTheory.Measure.hausdorffMeasure`
      [def, depth 194, in-statement, role implicit-arg]
  13. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
  14. `Real`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `BorelSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `PseudoEMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]

### proof_0065  (target depth 166, band 126+)

THEOREM PROVED: `deriv_const_add'`

Grade all 19 candidates.

   1. `funext`
      [theorem, depth 4, in-statement, role applied]
   2. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
   3. `deriv`
      [def, depth 104, in-statement, role implicit-arg]
   4. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   5. `AddCommMagma.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   6. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   7. `AddCommMonoid.toAddCommSemigroup`
      [def, depth 5, in-statement, role instance-slot]
   8. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   9. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  10. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role implicit-arg]
  11. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  12. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
  13. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `deriv_const_add`
      [theorem, depth 165, introduced-by-proof, role explicit-arg]
  16. `AddCommSemigroup.toAddCommMagma`
      [def, depth 5, in-statement, role instance-slot]
  17. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
  19. `NormedSpace.toModule`
      [def, depth 2, in-statement, role instance-slot]

### proof_0066  (target depth 274, band 126+)

THEOREM PROVED: `ProbabilityTheory.CondIndepSets.union_iff`

Grade all 10 candidates.

   1. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Set`
      [def, depth 0, in-statement, role explicit-arg]
   3. `MeasureTheory.Measure.trim`
      [def, depth 184, in-statement, role implicit-arg]
   4. `ProbabilityTheory.Kernel.IndepSets.union_iff`
      [theorem, depth 172, introduced-by-proof, role applied]
   5. `MeasureTheory.IsFiniteMeasure`
      [inductive, depth 2, in-statement, role type-annotation]
   6. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `StandardBorelSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `ProbabilityTheory.condExpKernel`
      [def, depth 273, in-statement, role implicit-arg]
   9. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
  10. `MeasurableSpace.instLE`
      [def, depth 3, in-statement, role instance-slot]

### proof_0067  (target depth 146, band 126+)

THEOREM PROVED: `Real.cosh_sq'`

Grade all 21 candidates.

   1. `Real.instMonoid`
      [def, depth 95, in-statement, role instance-slot]
   2. `HPow.hPow`
      [def, depth 2, in-statement, role explicit-arg]
   3. `NPow.toPow`
      [def, depth 2, in-statement, role instance-slot]
   4. `Eq.trans`
      [theorem, depth 3, in-statement, role applied]
   5. `instHPow`
      [def, depth 3, in-statement, role instance-slot]
   6. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
   7. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   8. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Real.instAdd`
      [def, depth 89, in-statement, role instance-slot]
  10. `Real.sinh`
      [def, depth 141, in-statement, role explicit-arg]
  11. `add_comm`
      [theorem, depth 2, in-statement, role explicit-arg]
  12. `HAdd.hAdd`
      [def, depth 2, in-statement, role implicit-arg]
  13. `Real.cosh`
      [def, depth 141, in-statement, role explicit-arg]
  14. `Real.instOne`
      [def, depth 85, in-statement, role instance-slot]
  15. `AddCommSemigroup.toAddCommMagma`
      [def, depth 5, in-statement, role instance-slot]
  16. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  17. `Real.instAddCommSemigroup`
      [def, depth 96, in-statement, role instance-slot]
  18. `Monoid.toNPow`
      [def, depth 1, in-statement, role instance-slot]
  19. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `Real.cosh_sq`
      [theorem, depth 145, introduced-by-proof, role explicit-arg]
  21. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]

### proof_0068  (target depth 167, band 126+)

THEOREM PROVED: `deriv_one`

Grade all 24 candidates.

   1. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   2. `deriv`
      [def, depth 104, in-statement, role implicit-arg]
   3. `NegZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
   4. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   5. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
   7. `Pi.instZero`
      [def, depth 4, in-statement, role instance-slot]
   8. `One`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `deriv_const`
      [theorem, depth 166, introduced-by-proof, role explicit-arg]
  10. `AddCommGroup.toDivisionAddCommMonoid`
      [def, depth 12, in-statement, role instance-slot]
  11. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `SubNegZeroMonoid.toNegZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  14. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  15. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role implicit-arg]
  16. `funext`
      [theorem, depth 4, in-statement, role applied]
  17. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  18. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
  19. `SubtractionCommMonoid.toSubtractionMonoid`
      [def, depth 1, in-statement, role instance-slot]
  20. `Pi.instOne`
      [def, depth 4, in-statement, role instance-slot]
  21. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  22. `SubtractionMonoid.toSubNegZeroMonoid`
      [def, depth 9, in-statement, role instance-slot]
  23. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
  24. `NormedSpace.toModule`
      [def, depth 2, in-statement, role instance-slot]

### proof_0069  (target depth 248, band 126+)

THEOREM PROVED: `intervalIntegral.abs_intervalIntegral_eq`

Grade all 9 candidates.

   1. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `Real.normedAddCommGroup`
      [def, depth 148, in-statement, role instance-slot]
   3. `Real.measurableSpace`
      [def, depth 114, in-statement, role instance-slot]
   4. `Real.instRCLike`
      [def, depth 155, in-statement, role implicit-arg]
   5. `RCLike.toInnerProductSpaceReal`
      [def, depth 158, in-statement, role instance-slot]
   6. `InnerProductSpace.toNormedSpace`
      [def, depth 3, in-statement, role instance-slot]
   7. `intervalIntegral.norm_intervalIntegral_eq`
      [theorem, depth 247, introduced-by-proof, role applied]
   8. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role implicit-arg]

### proof_0070  (target depth 192, band 126+)

THEOREM PROVED: `MeasureTheory.isAddLeftInvariant_smul`

Grade all 25 candidates.

   1. `id`
      [def, depth 0, in-statement, role explicit-arg]
   2. `MeasureTheory.Measure.IsAddLeftInvariant.mk`
      [constructor, depth 189, introduced-by-proof, role applied]
   3. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
   4. `MeasureTheory.Measure.map`
      [def, depth 188, introduced-by-proof, role explicit-arg]
   5. `HSMul.hSMul`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Add`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   8. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   9. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
  10. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  12. `ENNReal`
      [def, depth 96, in-statement, role explicit-arg]
  13. `Algebra.id`
      [def, depth 20, in-statement, role instance-slot]
  14. `MeasureTheory.Measure.IsAddLeftInvariant`
      [inductive, depth 2, in-statement, role type-annotation]
  15. `MeasureTheory.map_add_left_eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  16. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  17. `MeasureTheory.Measure.map_smul`
      [theorem, depth 191, introduced-by-proof, role explicit-arg]
  18. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  19. `Distrib.toMul`
      [def, depth 1, in-statement, role instance-slot]
  20. `MeasureTheory.Measure.instSMul`
      [def, depth 167, in-statement, role instance-slot]
  21. `ENNReal.instCommSemiring`
      [def, depth 110, in-statement, role instance-slot]
  22. `instHSMul`
      [def, depth 3, in-statement, role instance-slot]
  23. `instDistribOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
  24. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  25. `instSMulOfMul`
      [def, depth 2, in-statement, role instance-slot]

### proof_0071  (target depth 155, band 126+)

THEOREM PROVED: `Dilation.ratioHom_apply`

Grade all 14 candidates.

   1. `Dilation`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   3. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   4. `PseudoEMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `MulZeroOneClass.toMulOneClass`
      [def, depth 1, in-statement, role instance-slot]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   7. `MonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `MonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
   9. `instMulZeroOneClassOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
  10. `Dilation.instMonoid`
      [def, depth 152, in-statement, role instance-slot]
  11. `NNReal`
      [def, depth 95, in-statement, role explicit-arg]
  12. `Dilation.ratioHom`
      [def, depth 154, in-statement, role explicit-arg]
  13. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  14. `NNReal.instSemiring`
      [def, depth 106, in-statement, role instance-slot]

### proof_0072  (target depth 141, band 126+)

THEOREM PROVED: `IsSimplyConnected.isPathConnected`

Grade all 14 candidates.

   1. `SimplyConnectedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   3. `instTopologicalSpaceSubtype`
      [def, depth 64, in-statement, role instance-slot]
   4. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   5. `IsSimplyConnected.simplyConnectedSpace`
      [theorem, depth 66, introduced-by-proof, role let-value]
   6. `isPathConnected_iff_pathConnectedSpace`
      [theorem, depth 130, introduced-by-proof, role explicit-arg]
   7. `inferInstance`
      [def, depth 0, in-statement, role explicit-arg]
   8. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   9. `PathConnectedSpace`
      [inductive, depth 1, introduced-by-proof, role implicit-arg]
  10. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `IsPathConnected`
      [def, depth 120, in-statement, role implicit-arg]
  12. `IsSimplyConnected`
      [def, depth 65, in-statement, role type-annotation]
  13. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
  14. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
