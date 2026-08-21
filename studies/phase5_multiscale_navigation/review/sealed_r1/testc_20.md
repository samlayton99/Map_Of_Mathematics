# Grading batch `testc_20` — 24 proofs

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

### proof_0457  (target depth 22, band 11-25)

THEOREM PROVED: `Valuation.leAddSubgroup_monotone`

Grade all 15 candidates.

   1. `LinearOrderedCommGroupWithZero`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   3. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   4. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   5. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
   6. `LinearOrderedCommGroupWithZero.toLinearOrderedCommMonoidWithZero`
      [def, depth 1, in-statement, role instance-slot]
   7. `Valuation.instFunLike`
      [def, depth 21, in-statement, role instance-slot]
   8. `Valuation`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  10. `LinearOrderedCommMonoidWithZero.toLinearOrder`
      [def, depth 1, in-statement, role instance-slot]
  11. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  13. `LE.le.trans'`
      [theorem, depth 4, introduced-by-proof, role applied]
  14. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
  15. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]

### proof_0458  (target depth 173, band 126+)

THEOREM PROVED: `Submodule.norm_starProjection_apply`

Grade all 20 candidates.

   1. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   2. `NormedField.toField`
      [def, depth 1, in-statement, role instance-slot]
   3. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
   4. `Submodule.norm_orthogonalProjectionOnto_apply`
      [theorem, depth 172, introduced-by-proof, role applied]
   5. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   6. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   7. `InnerProductSpace`
      [inductive, depth 2, in-statement, role type-annotation]
   8. `NormedSpace.toModule`
      [def, depth 2, in-statement, role instance-slot]
   9. `Submodule.HasOrthogonalProjection`
      [inductive, depth 45, in-statement, role type-annotation]
  10. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
  11. `RCLike`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role implicit-arg]
  13. `Submodule`
      [inductive, depth 2, in-statement, role implicit-arg]
  14. `RCLike.toDenselyNormedField`
      [def, depth 2, in-statement, role instance-slot]
  15. `Submodule.setLike`
      [def, depth 12, in-statement, role instance-slot]
  16. `DenselyNormedField.toNormedField`
      [def, depth 1, in-statement, role implicit-arg]
  17. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  18. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  19. `InnerProductSpace.toNormedSpace`
      [def, depth 3, in-statement, role instance-slot]
  20. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]

### proof_0459  (target depth 296, band 126+)

THEOREM PROVED: `ProbabilityTheory.variance_continuousLinearMap_gaussianReal`

Grade all 13 candidates.

   1. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   3. `ContinuousLinearMap.toLinearMap`
      [def, depth 12, in-statement, role explicit-arg]
   4. `Real.pseudoMetricSpace`
      [def, depth 113, in-statement, role instance-slot]
   5. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   6. `Real.instAddCommMonoid`
      [def, depth 95, in-statement, role instance-slot]
   7. `NNReal`
      [def, depth 95, in-statement, role type-annotation]
   8. `Semiring.toModule`
      [def, depth 13, in-statement, role instance-slot]
   9. `Real.semiring`
      [def, depth 94, in-statement, role instance-slot]
  10. `ProbabilityTheory.variance_linearMap_gaussianReal`
      [theorem, depth 295, introduced-by-proof, role applied]
  11. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
  12. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  13. `ContinuousLinearMap`
      [inductive, depth 11, in-statement, role type-annotation]

### proof_0460  (target depth 15, band 11-25)

THEOREM PROVED: `neg_of_neg_pos`

Grade all 19 candidates.

   1. `SubtractionMonoid.toSubNegZeroMonoid`
      [def, depth 9, in-statement, role instance-slot]
   2. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   3. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   4. `NegZeroClass.toNeg`
      [def, depth 1, in-statement, role instance-slot]
   5. `Left.neg_pos_iff`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
   6. `NegZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
   7. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   8. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   9. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
  10. `AddLeftStrictMono`
      [def, depth 4, in-statement, role type-annotation]
  11. `LT`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
  13. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]
  14. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  15. `SubNegMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  16. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `AddGroup.toSubtractionMonoid`
      [def, depth 11, in-statement, role instance-slot]
  18. `Iff.mp`
      [theorem, depth 1, introduced-by-proof, role applied]
  19. `SubNegZeroMonoid.toNegZeroClass`
      [def, depth 5, in-statement, role instance-slot]

### proof_0461  (target depth 6, band 0-10)

THEOREM PROVED: `Set.Icc_subset_uIcc`

Grade all 12 candidates.

   1. `Lattice.toSemilatticeSup`
      [def, depth 1, in-statement, role instance-slot]
   2. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   3. `Lattice`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Set.Icc_subset_Icc`
      [theorem, depth 5, introduced-by-proof, role applied]
   5. `Min.min`
      [def, depth 1, in-statement, role implicit-arg]
   6. `le_sup_right`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   7. `inf_le_left`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   8. `SemilatticeInf.toMin`
      [def, depth 2, in-statement, role instance-slot]
   9. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  10. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  11. `Max.max`
      [def, depth 1, in-statement, role implicit-arg]
  12. `SemilatticeSup.toMax`
      [def, depth 2, in-statement, role instance-slot]

### proof_0462  (target depth 7, band 0-10)

THEOREM PROVED: `IsCompl.inf_eq_bot`

Grade all 10 candidates.

   1. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   2. `Preorder.toLE`
      [def, depth 1, in-statement, role implicit-arg]
   3. `IsCompl`
      [inductive, depth 2, in-statement, role type-annotation]
   4. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   5. `Lattice`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Disjoint.eq_bot`
      [theorem, depth 6, introduced-by-proof, role applied]
   7. `IsCompl.disjoint`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   8. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   9. `BoundedOrder.toOrderBot`
      [def, depth 2, in-statement, role instance-slot]
  10. `BoundedOrder`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0463  (target depth 57, band 51-75)

THEOREM PROVED: `Maximal.eq_of_superset`

Grade all 12 candidates.

   1. `SemilatticeInf.toPartialOrder`
      [def, depth 1, introduced-by-proof, role instance-slot]
   2. `GeneralizedCoheytingAlgebra.toLattice`
      [def, depth 1, introduced-by-proof, role instance-slot]
   3. `Set.instBooleanAlgebra`
      [def, depth 56, introduced-by-proof, role instance-slot]
   4. `BooleanAlgebra.toBiheytingAlgebra`
      [def, depth 53, introduced-by-proof, role instance-slot]
   5. `Maximal`
      [def, depth 2, in-statement, role type-annotation]
   6. `Lattice.toSemilatticeInf`
      [def, depth 3, introduced-by-proof, role instance-slot]
   7. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `BiheytingAlgebra.toCoheytingAlgebra`
      [def, depth 4, introduced-by-proof, role instance-slot]
  10. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]
  11. `CoheytingAlgebra.toGeneralizedCoheytingAlgebra`
      [def, depth 1, introduced-by-proof, role instance-slot]
  12. `Maximal.eq_of_ge`
      [theorem, depth 6, introduced-by-proof, role applied]

### proof_0464  (target depth 106, band 76-125)

THEOREM PROVED: `IsIntegral.isAlmostIntegral`

Grade all 16 candidates.

   1. `IsIntegral.isAlmostIntegral_of_isLocalization`
      [theorem, depth 105, introduced-by-proof, role applied]
   2. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `instMulZeroOneClassOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
   5. `Semiring.toMonoidWithZero`
      [def, depth 5, in-statement, role instance-slot]
   6. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   7. `IsIntegral`
      [def, depth 66, in-statement, role type-annotation]
   8. `Submonoid.instPartialOrder`
      [def, depth 22, introduced-by-proof, role instance-slot]
   9. `MulZeroOneClass.toMulOneClass`
      [def, depth 1, in-statement, role instance-slot]
  10. `IsFractionRing`
      [def, depth 16, in-statement, role type-annotation]
  11. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  12. `le_rfl`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `Submonoid`
      [inductive, depth 1, in-statement, role implicit-arg]
  14. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
  15. `CommRing.toRing`
      [def, depth 1, in-statement, role instance-slot]
  16. `nonZeroDivisors`
      [def, depth 15, in-statement, role explicit-arg]

### proof_0465  (target depth 15, band 11-25)

THEOREM PROVED: `isRelPrime_one_right`

Grade all 9 candidates.

   1. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role implicit-arg]
   3. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   4. `MulOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
   5. `CommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CommMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
   7. `IsUnit.isRelPrime_right`
      [theorem, depth 14, introduced-by-proof, role applied]
   8. `isUnit_one`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
   9. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]

### proof_0466  (target depth 145, band 126+)

THEOREM PROVED: `Isometry.mapRingHom_coe`

Grade all 21 candidates.

   1. `UniformSpace.Completion.mapRingHom_coe`
      [theorem, depth 123, introduced-by-proof, role applied]
   2. `RingHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   4. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   5. `NonAssocRing.toNonUnitalNonAssocRing`
      [def, depth 1, in-statement, role instance-slot]
   6. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `PseudoEMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   8. `Isometry`
      [def, depth 141, in-statement, role type-annotation]
   9. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  10. `IsTopologicalRing`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Isometry.uniformContinuous`
      [theorem, depth 144, introduced-by-proof, role explicit-arg]
  12. `RingHom.instFunLike`
      [def, depth 15, in-statement, role instance-slot]
  13. `IsUniformAddGroup`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `PseudoMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `Ring.toAddGroupWithOne`
      [def, depth 10, in-statement, role instance-slot]
  16. `UniformContinuous.continuous`
      [theorem, depth 71, in-statement, role explicit-arg]
  17. `PseudoMetricSpace.toPseudoEMetricSpace`
      [def, depth 115, in-statement, role instance-slot]
  18. `AddGroupWithOne.toAddGroup`
      [def, depth 10, in-statement, role instance-slot]
  19. `Ring.toNonAssocRing`
      [def, depth 10, in-statement, role instance-slot]
  20. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  21. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0467  (target depth 152, band 126+)

THEOREM PROVED: `Complex.isLittleO_ofReal_left`

Grade all 14 candidates.

   1. `Norm`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Complex.instNormedField`
      [def, depth 134, introduced-by-proof, role instance-slot]
   3. `Complex.isTheta_ofReal`
      [theorem, depth 151, introduced-by-proof, role explicit-arg]
   4. `Filter`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `NonUnitalSeminormedCommRing.toNonUnitalSeminormedRing`
      [def, depth 1, introduced-by-proof, role instance-slot]
   6. `NormedField.toNormedCommRing`
      [def, depth 103, introduced-by-proof, role instance-slot]
   7. `Asymptotics.IsTheta.isLittleO_congr_left`
      [theorem, depth 118, introduced-by-proof, role applied]
   8. `Complex.ofReal`
      [def, depth 86, in-statement, role implicit-arg]
   9. `Complex`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `NonUnitalSeminormedRing.toSeminormedAddCommGroup`
      [def, depth 10, introduced-by-proof, role instance-slot]
  11. `SeminormedCommRing.toNonUnitalSeminormedCommRing`
      [def, depth 96, introduced-by-proof, role instance-slot]
  12. `Real.normedCommRing`
      [def, depth 150, introduced-by-proof, role instance-slot]
  13. `NormedCommRing.toSeminormedCommRing`
      [def, depth 96, introduced-by-proof, role instance-slot]
  14. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0468  (target depth 74, band 51-75)

THEOREM PROVED: `QuotientGroup.con_mono`

Grade all 17 candidates.

   1. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
   2. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   3. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
   4. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   5. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `QuotientGroup.con`
      [def, depth 68, in-statement, role explicit-arg]
   7. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   8. `Con.instLE`
      [def, depth 9, in-statement, role instance-slot]
   9. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  10. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  11. `Con`
      [inductive, depth 1, in-statement, role implicit-arg]
  12. `Subgroup`
      [inductive, depth 1, in-statement, role implicit-arg]
  13. `QuotientGroup.con_le_iff`
      [theorem, depth 73, introduced-by-proof, role explicit-arg]
  14. `Subgroup.Normal`
      [inductive, depth 2, in-statement, role type-annotation]
  15. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
  16. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  17. `Subgroup.instPartialOrder`
      [def, depth 22, in-statement, role instance-slot]

### proof_0469  (target depth 18, band 11-25)

THEOREM PROVED: `Set.Ioo_succ_right_eq_Ioc`

Grade all 11 candidates.

   1. `SuccOrder`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
   3. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   4. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
   5. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `NoMaxOrder`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   8. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   9. `not_isMax`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
  10. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  11. `Set.Ioo_succ_right_eq_Ioc_of_not_isMax`
      [theorem, depth 17, introduced-by-proof, role applied]

### proof_0470  (target depth 82, band 76-125)

THEOREM PROVED: `eventually_const_le_iff_forall_lt_eventually_const_lt`

Grade all 16 candidates.

   1. `OrderTopology`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `LinearOrder.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `OrderDual.instLinearOrder`
      [def, depth 13, introduced-by-proof, role instance-slot]
   5. `OrderDual.instTopologicalSpace`
      [def, depth 1, introduced-by-proof, role instance-slot]
   6. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   7. `OrderDual`
      [def, depth 0, introduced-by-proof, role implicit-arg]
   8. `FirstCountableTopology`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  10. `CountableInterFilter`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Filter`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  14. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  15. `eventually_le_const_iff_forall_gt_eventually_lt_const`
      [theorem, depth 81, introduced-by-proof, role applied]
  16. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]

### proof_0471  (target depth 18, band 11-25)

THEOREM PROVED: `AddEquiv.map_sub`

Grade all 12 candidates.

   1. `SubtractionMonoid.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
   2. `map_sub`
      [theorem, depth 15, introduced-by-proof, role applied]
   3. `SubNegMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
   4. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
   5. `SubtractionMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   8. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   9. `AddEquiv`
      [inductive, depth 1, in-statement, role explicit-arg]
  10. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  11. `AddEquiv.instEquivLike`
      [def, depth 16, in-statement, role instance-slot]
  12. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]

### proof_0472  (target depth 29, band 26-50)

THEOREM PROVED: `DirectSum.map_id`

Grade all 4 candidates.

   1. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   2. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `AddCommMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
   4. `DFinsupp.mapRange.addMonoidHom_id`
      [theorem, depth 28, introduced-by-proof, role applied]

### proof_0473  (target depth 86, band 76-125)

THEOREM PROVED: `coplanar_empty`

Grade all 13 candidates.

   1. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Set.instEmptyCollection`
      [def, depth 2, in-statement, role instance-slot]
   3. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   4. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   5. `EmptyCollection.emptyCollection`
      [def, depth 1, in-statement, role implicit-arg]
   6. `AddCommGroup.toAddGroup`
      [def, depth 1, in-statement, role instance-slot]
   7. `collinear_empty`
      [theorem, depth 85, introduced-by-proof, role explicit-arg]
   8. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   9. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `DivisionRing`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Collinear.coplanar`
      [theorem, depth 84, introduced-by-proof, role applied]
  12. `DivisionRing.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
  13. `AddTorsor`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0474  (target depth 29, band 26-50)

THEOREM PROVED: `HomotopicalAlgebra.FibrantObject.homMk_surjective`

Grade all 18 candidates.

   1. `HomotopicalAlgebra.CategoryWithFibrations`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.ObjectProperty.FullSubcategory.category`
      [def, depth 10, in-statement, role instance-slot]
   3. `HomotopicalAlgebra.FibrantObject.mk`
      [def, depth 27, in-statement, role explicit-arg]
   4. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   5. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.InducedCategory.Hom.hom`
      [def, depth 2, in-statement, role explicit-arg]
   8. `HomotopicalAlgebra.fibrantObjects`
      [def, depth 26, in-statement, role explicit-arg]
   9. `HomotopicalAlgebra.FibrantObject`
      [def, depth 27, in-statement, role implicit-arg]
  10. `CategoryTheory.ObjectProperty.FullSubcategory`
      [inductive, depth 2, in-statement, role implicit-arg]
  11. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
  13. `CategoryTheory.ObjectProperty.FullSubcategory.obj`
      [def, depth 3, in-statement, role implicit-arg]
  14. `HomotopicalAlgebra.IsFibrant`
      [def, depth 25, in-statement, role type-annotation]
  15. `CategoryTheory.Limits.HasTerminal`
      [def, depth 11, in-statement, role type-annotation]
  16. `HomotopicalAlgebra.FibrantObject.homMk`
      [def, depth 28, in-statement, role explicit-arg]
  17. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  18. `Exists.intro`
      [constructor, depth 1, in-statement, role applied]

### proof_0475  (target depth 15, band 11-25)

THEOREM PROVED: `Function.mulSupport_fun_curry`

Grade all 3 candidates.

   1. `Function.mulSupport_curry`
      [theorem, depth 14, introduced-by-proof, role applied]
   2. `Prod`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `One`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0476  (target depth 66, band 51-75)

THEOREM PROVED: `PowerSeries.X_apply`

Grade all 4 candidates.

   1. `PowerSeries`
      [def, depth 19, in-statement, role implicit-arg]
   2. `PowerSeries.X`
      [def, depth 65, in-statement, role implicit-arg]
   3. `rfl`
      [def, depth 2, in-statement, role applied]
   4. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0477  (target depth 148, band 126+)

THEOREM PROVED: `TopologicalSpace.Compacts.isometry_singleton`

Grade all 3 candidates.

   1. `Metric.hausdorffEDist_singleton`
      [theorem, depth 147, introduced-by-proof, role applied]
   2. `EMetricSpace.toPseudoEMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   3. `EMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0478  (target depth 55, band 51-75)

THEOREM PROVED: `OpenPartialHomeomorph.bijOn`

Grade all 12 candidates.

   1. `OpenPartialHomeomorph.mapsTo_symm`
      [theorem, depth 54, introduced-by-proof, role explicit-arg]
   2. `PartialHomeomorph.toPartialEquiv`
      [def, depth 2, in-statement, role explicit-arg]
   3. `OpenPartialHomeomorph.toPartialHomeomorph`
      [def, depth 2, in-statement, role explicit-arg]
   4. `OpenPartialHomeomorph.mapsTo`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   5. `OpenPartialHomeomorph.toFun'`
      [def, depth 3, in-statement, role implicit-arg]
   6. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `OpenPartialHomeomorph.symm`
      [def, depth 53, introduced-by-proof, role explicit-arg]
   8. `PartialEquiv.source`
      [def, depth 1, in-statement, role implicit-arg]
   9. `OpenPartialHomeomorph.invOn`
      [theorem, depth 54, introduced-by-proof, role explicit-arg]
  10. `Set.InvOn.bijOn`
      [theorem, depth 7, introduced-by-proof, role applied]
  11. `OpenPartialHomeomorph`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `PartialEquiv.target`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0479  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.IsColimit.ofIsoColimit._proof_1`

Grade all 21 candidates.

   1. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   2. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
   3. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   4. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `id`
      [def, depth 0, in-statement, role explicit-arg]
   6. `CategoryTheory.Iso.hom`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   7. `CategoryTheory.Limits.IsColimit`
      [inductive, depth 3, in-statement, role type-annotation]
   8. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `CategoryTheory.Limits.Cocone`
      [inductive, depth 2, in-statement, role implicit-arg]
  10. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  12. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `CategoryTheory.Limits.IsColimit.descCoconeMorphism`
      [def, depth 23, in-statement, role explicit-arg]
  15. `CategoryTheory.Limits.IsColimit.uniq_cocone_morphism`
      [theorem, depth 26, introduced-by-proof, role explicit-arg]
  16. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
  17. `CategoryTheory.Iso.comp_inv_eq._to_dual_1`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  18. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  19. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
  20. `CategoryTheory.Limits.Cocone.category`
      [def, depth 24, in-statement, role instance-slot]
  21. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_0480  (target depth 78, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.le_maxKey?_of_mem`

Grade all 7 candidates.

   1. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   3. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, in-statement, role explicit-arg]
   5. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
   6. `Std.DTreeMap.Internal.Impl.le_maxKey?_of_mem`
      [theorem, depth 77, introduced-by-proof, role applied]
   7. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
