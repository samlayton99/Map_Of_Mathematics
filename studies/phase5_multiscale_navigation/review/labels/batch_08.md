# Grading batch `batch_08` -- 20 proofs

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

### proof_141  (target depth 27, band 26-50)

THEOREM PROVED: `IsManifold.instLEInftyOfNatWithTopENat`

Grade all 3 candidates below.

   1. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Nat.AtLeastTwo`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `_private.Mathlib.Geometry.Manifold.IsManifold.Basic.0.IsManifold.instLEInftyOfNatWithTopENat._proof_1`
      [theorem, depth 26, introduced-by-proof, role applied]

### proof_142  (target depth 72, band 51-75)

THEOREM PROVED: `IsClosedMap.eventually_nhds_fiber`

Grade all 21 candidates below.

   1. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   2. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `IsClosedMap.comap_nhds_le`
      [theorem, depth 71, introduced-by-proof, role explicit-arg]
   5. `Eq.mp`
      [def, depth 3, introduced-by-proof, role applied]
   6. `IsClosedMap`
      [def, depth 5, in-statement, role type-annotation]
   7. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   8. `Filter.eventually_comap`
      [theorem, depth 61, introduced-by-proof, role explicit-arg]
   9. `Set.preimage`
      [def, depth 4, in-statement, role explicit-arg]
  10. `Set.instSingletonSet`
      [def, depth 3, in-statement, role instance-slot]
  11. `Singleton.singleton`
      [def, depth 2, in-statement, role explicit-arg]
  12. `eventually_nhdsSet_iff_forall`
      [theorem, depth 21, introduced-by-proof, role explicit-arg]
  13. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  14. `Filter.comap`
      [def, depth 58, introduced-by-proof, role explicit-arg]
  15. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  16. `Filter.Eventually.filter_mono`
      [theorem, depth 13, introduced-by-proof, role let-value]
  17. `Filter.Eventually`
      [def, depth 5, in-statement, role implicit-arg]
  18. `nhdsSet`
      [def, depth 19, introduced-by-proof, role explicit-arg]
  19. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  21. `nhds`
      [def, depth 18, in-statement, role explicit-arg]

### proof_143  (target depth 78, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.getKey!_filterMap`

Grade all 10 candidates below.

   1. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, in-statement, role explicit-arg]
   3. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   4. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
   5. `Option`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Std.DTreeMap.Internal.Impl.getKey!_filterMap!`
      [theorem, depth 77, introduced-by-proof, role applied]
   7. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   9. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Std.LawfulEqCmp`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_144  (target depth 203, band 126+)

THEOREM PROVED: `Manifold.IsImmersionAt.contMDiffOn`

Grade all 16 candidates below.

   1. `WithTop`
      [def, depth 1, in-statement, role type-annotation]
   2. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
   3. `ModelWithCorners`
      [inductive, depth 11, in-statement, role type-annotation]
   4. `Manifold.IsImmersionAt.instNormedSpaceComplement`
      [def, depth 70, in-statement, role instance-slot]
   5. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
   7. `Manifold.IsImmersionAt.isImmersionAtOfComplement_complement`
      [theorem, depth 68, in-statement, role explicit-arg]
   8. `Manifold.IsImmersionAtOfComplement.contMDiffOn`
      [theorem, depth 202, introduced-by-proof, role applied]
   9. `ChartedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Manifold.IsImmersionAt.complement`
      [def, depth 68, in-statement, role implicit-arg]
  12. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `Manifold.IsImmersionAt`
      [def, depth 67, in-statement, role type-annotation]
  14. `ENat`
      [def, depth 2, in-statement, role explicit-arg]
  15. `Manifold.IsImmersionAt.instNormedAddCommGroupComplement`
      [def, depth 69, in-statement, role instance-slot]
  16. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_145  (target depth 3, band 0-10)

THEOREM PROVED: `CategoryTheory.MonoidalCategory.MonoidalRightAction.actionHom_def`

Grade all 3 candidates below.

   1. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.MonoidalCategory.MonoidalRightAction`
      [inductive, depth 2, in-statement, role type-annotation]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_146  (target depth 23, band 11-25)

THEOREM PROVED: `CategoryTheory.RightExactFunctor.ofExact_map_hom`

Grade all 18 candidates below.

   1. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   2. `CategoryTheory.rightExactFunctor`
      [def, depth 3, in-statement, role explicit-arg]
   3. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   4. `CategoryTheory.RightExactFunctor.ofExact`
      [def, depth 22, in-statement, role explicit-arg]
   5. `CategoryTheory.InducedCategory.Hom.hom`
      [def, depth 2, in-statement, role implicit-arg]
   6. `CategoryTheory.ExactFunctor`
      [def, depth 21, in-statement, role implicit-arg]
   7. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   8. `CategoryTheory.ObjectProperty.FullSubcategory.category`
      [def, depth 10, in-statement, role instance-slot]
   9. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  10. `CategoryTheory.ObjectProperty.FullSubcategory`
      [inductive, depth 2, in-statement, role implicit-arg]
  11. `CategoryTheory.RightExactFunctor`
      [def, depth 20, in-statement, role implicit-arg]
  12. `CategoryTheory.ObjectProperty.FullSubcategory.obj`
      [def, depth 3, in-statement, role explicit-arg]
  13. `CategoryTheory.Functor.map`
      [def, depth 2, in-statement, role explicit-arg]
  14. `CategoryTheory.exactFunctor`
      [def, depth 20, in-statement, role explicit-arg]
  15. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `rfl`
      [def, depth 2, in-statement, role applied]
  17. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  18. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]

### proof_147  (target depth 31, band 26-50)

THEOREM PROVED: `Matrix.cons_head_tail`

Grade all 4 candidates below.

   1. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Nat.succ`
      [constructor, depth 1, in-statement, role explicit-arg]
   3. `Fin.cons_self_tail`
      [theorem, depth 30, introduced-by-proof, role applied]
   4. `Fin`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_148  (target depth 68, band 51-75)

THEOREM PROVED: `CoalgEquiv.refl_apply`

Grade all 10 candidates below.

   1. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   2. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   4. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CoalgEquiv.instFunLike`
      [def, depth 67, in-statement, role instance-slot]
   7. `CoalgEquiv.refl`
      [def, depth 63, in-statement, role explicit-arg]
   8. `CoalgebraStruct`
      [inductive, depth 2, in-statement, role type-annotation]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CoalgEquiv`
      [inductive, depth 3, in-statement, role implicit-arg]

### proof_149  (target depth 78, band 76-125)

THEOREM PROVED: `ContinuousSMul.measurableSMul₂`

Grade all 17 candidates below.

   1. `SMul`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `SecondCountableTopologyEither`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `MeasurableSMul₂.mk`
      [constructor, depth 68, introduced-by-proof, role applied]
   4. `Prod`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   5. `instTopologicalSpaceProd`
      [def, depth 64, introduced-by-proof, role instance-slot]
   6. `OpensMeasurableSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Prod.fst`
      [def, depth 1, introduced-by-proof, role explicit-arg]
   8. `ContinuousSMul`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Prod.snd`
      [def, depth 1, introduced-by-proof, role explicit-arg]
  11. `ContinuousSMul.continuous_smul`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  12. `instHSMul`
      [def, depth 3, introduced-by-proof, role instance-slot]
  13. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `BorelSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  15. `Prod.instMeasurableSpace`
      [def, depth 67, introduced-by-proof, role instance-slot]
  16. `Continuous.measurable`
      [theorem, depth 63, introduced-by-proof, role explicit-arg]
  17. `HSMul.hSMul`
      [def, depth 2, introduced-by-proof, role implicit-arg]

### proof_150  (target depth 133, band 126+)

THEOREM PROVED: `ENNReal.mul_lt_of_lt_div'`

Grade all 20 candidates below.

   1. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
   2. `ENNReal.instCommSemiring`
      [def, depth 110, in-statement, role instance-slot]
   3. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
   5. `CommMagma.toMul`
      [def, depth 1, in-statement, role instance-slot]
   6. `NonUnitalNonAssocCommSemiring.toCommMagma`
      [def, depth 5, in-statement, role instance-slot]
   7. `instHDiv`
      [def, depth 3, in-statement, role instance-slot]
   8. `ENNReal.instPartialOrder`
      [def, depth 105, in-statement, role instance-slot]
   9. `ENNReal.instDivInvMonoid`
      [def, depth 123, in-statement, role instance-slot]
  10. `DivInvMonoid.toDiv`
      [def, depth 1, in-statement, role instance-slot]
  11. `mul_comm`
      [theorem, depth 2, in-statement, role explicit-arg]
  12. `HDiv.hDiv`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
  14. `CommSemiring.toNonUnitalCommSemiring`
      [def, depth 7, in-statement, role instance-slot]
  15. `ENNReal.mul_lt_of_lt_div`
      [theorem, depth 132, introduced-by-proof, role explicit-arg]
  16. `Eq.rec`
      [recursor, depth 2, in-statement, role applied]
  17. `HMul.hMul`
      [def, depth 2, in-statement, role implicit-arg]
  18. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  19. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  20. `NonUnitalCommSemiring.toNonUnitalNonAssocCommSemiring`
      [def, depth 7, in-statement, role instance-slot]

### proof_151  (target depth 6, band 0-10)

THEOREM PROVED: `Lean.Omega.LinearCombo.ext`

Grade all 11 candidates below.

   1. `Lean.Omega.LinearCombo.coeffs`
      [def, depth 1, in-statement, role explicit-arg]
   2. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   3. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   4. `Lean.Omega.LinearCombo`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
   7. `Lean.Omega.LinearCombo.const`
      [def, depth 1, in-statement, role explicit-arg]
   8. `Lean.Omega.Coeffs`
      [def, depth 2, in-statement, role implicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Lean.Omega.LinearCombo.mk`
      [constructor, depth 3, introduced-by-proof, role explicit-arg]
  11. `Lean.Omega.LinearCombo.casesOn`
      [def, depth 5, introduced-by-proof, role applied]

### proof_152  (target depth 17, band 11-25)

THEOREM PROVED: `Equiv.constSMul_mul`

Grade all 17 candidates below.

   1. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Equiv.Perm.instMul`
      [def, depth 16, in-statement, role instance-slot]
   3. `Torsor`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Equiv.ext`
      [theorem, depth 14, introduced-by-proof, role applied]
   5. `SemigroupAction.mul_smul`
      [theorem, depth 2, in-statement, role explicit-arg]
   6. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `MulAction.toSemigroupAction`
      [def, depth 2, in-statement, role instance-slot]
   8. `Equiv.constSMul`
      [def, depth 10, in-statement, role explicit-arg]
   9. `Monoid.toSemigroup`
      [def, depth 1, in-statement, role implicit-arg]
  10. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  11. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  12. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  13. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
  14. `Torsor.toMulAction`
      [def, depth 2, in-statement, role instance-slot]
  15. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role implicit-arg]
  16. `Equiv.Perm`
      [def, depth 1, in-statement, role implicit-arg]
  17. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]

### proof_153  (target depth 40, band 26-50)

THEOREM PROVED: `CategoryTheory.Functor.ranCompIsoOfPreserves_hom_app`

Grade all 16 candidates below.

   1. `CategoryTheory.Functor.ran`
      [def, depth 33, in-statement, role explicit-arg]
   2. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   3. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
   5. `CategoryTheory.Functor.ranCompIsoOfPreserves`
      [def, depth 39, in-statement, role explicit-arg]
   6. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `CategoryTheory.Functor.HasRightKanExtension`
      [def, depth 28, in-statement, role type-annotation]
   8. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   9. `CategoryTheory.Functor.whiskeringRight`
      [def, depth 26, in-statement, role explicit-arg]
  10. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  11. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  12. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role explicit-arg]
  13. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  14. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  15. `CategoryTheory.Functor.PreservesRightKanExtensions`
      [def, depth 3, in-statement, role type-annotation]
  16. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]

### proof_154  (target depth 63, band 51-75)

THEOREM PROVED: `IsLUB.iUnion_Iio_eq`

Grade all 18 candidates below.

   1. `IsGLB.iUnion_Ioi_eq`
      [theorem, depth 62, introduced-by-proof, role applied]
   2. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   3. `DFunLike.coe`
      [def, depth 2, introduced-by-proof, role implicit-arg]
   4. `Equiv.instEquivLike`
      [def, depth 13, introduced-by-proof, role instance-slot]
   5. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
   6. `Equiv`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   7. `IsLUB.dual`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   8. `OrderDual.instLinearOrder`
      [def, depth 13, introduced-by-proof, role instance-slot]
   9. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  10. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  12. `Set.range`
      [def, depth 2, in-statement, role explicit-arg]
  13. `IsLUB`
      [def, depth 6, in-statement, role type-annotation]
  14. `OrderDual`
      [def, depth 0, introduced-by-proof, role implicit-arg]
  15. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
  16. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  17. `OrderDual.toDual`
      [def, depth 11, introduced-by-proof, role explicit-arg]
  18. `EquivLike.toFunLike`
      [def, depth 8, introduced-by-proof, role instance-slot]

### proof_155  (target depth 90, band 76-125)

THEOREM PROVED: `isLindelof_iff_countable`

Grade all 8 candidates below.

   1. `IsLindelof.countable_of_discrete`
      [theorem, depth 89, introduced-by-proof, role explicit-arg]
   2. `DiscreteTopology`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Set.Countable`
      [def, depth 5, in-statement, role implicit-arg]
   4. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `IsLindelof`
      [def, depth 49, in-statement, role implicit-arg]
   6. `Set`
      [def, depth 0, in-statement, role type-annotation]
   7. `Set.Countable.isLindelof`
      [theorem, depth 88, introduced-by-proof, role explicit-arg]
   8. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]

### proof_156  (target depth 201, band 126+)

THEOREM PROVED: `ProbabilityTheory.IdentDistrib.coe_nnreal_ennreal`

Grade all 10 candidates below.

   1. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `NNReal.measurableSpace`
      [def, depth 116, in-statement, role instance-slot]
   3. `WithTop.some`
      [def, depth 2, in-statement, role implicit-arg]
   4. `ProbabilityTheory.IdentDistrib.comp`
      [theorem, depth 200, introduced-by-proof, role applied]
   5. `measurable_coe_nnreal_ennreal`
      [theorem, depth 124, introduced-by-proof, role explicit-arg]
   6. `ENNReal.measurableSpace`
      [def, depth 107, in-statement, role instance-slot]
   7. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `ProbabilityTheory.IdentDistrib`
      [inductive, depth 9, in-statement, role type-annotation]
   9. `NNReal`
      [def, depth 95, in-statement, role implicit-arg]
  10. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]

### proof_157  (target depth 3, band 0-10)

THEOREM PROVED: `Opposite.op_unop`

Grade all 3 candidates below.

   1. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   2. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Opposite.unop`
      [def, depth 1, in-statement, role explicit-arg]

### proof_158  (target depth 20, band 11-25)

THEOREM PROVED: `FreeAddGroup.ext_hom_iff`

Grade all 20 candidates below.

   1. `FreeAddGroup`
      [def, depth 2, in-statement, role explicit-arg]
   2. `AddMonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   5. `HEq`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   7. `HEq.refl`
      [constructor, depth 1, in-statement, role unresolved]
   8. `FreeAddGroup.instAddGroup`
      [def, depth 18, in-statement, role instance-slot]
   9. `Eq.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  10. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
  12. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
  14. `AddMonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
  15. `SubNegMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  16. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `FreeAddGroup.ext_hom`
      [theorem, depth 19, introduced-by-proof, role explicit-arg]
  18. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  19. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
  20. `FreeAddGroup.of`
      [def, depth 3, in-statement, role explicit-arg]

### proof_159  (target depth 41, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.CategoricalPullback.functorEquiv_counitIso_hom_app_fst_app`

Grade all 22 candidates below.

   1. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.fst`
      [def, depth 3, in-statement, role explicit-arg]
   5. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role explicit-arg]
   7. `CategoryTheory.Limits.CategoricalPullback.instCategory`
      [def, depth 12, in-statement, role instance-slot]
   8. `CategoryTheory.Limits.CategoricalPullback.functorEquiv`
      [def, depth 40, in-statement, role explicit-arg]
   9. `CategoryTheory.Equivalence.counitIso`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CategoryTheory.Functor.id`
      [def, depth 10, in-statement, role explicit-arg]
  11. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.instCategory`
      [def, depth 30, in-statement, role instance-slot]
  12. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.Hom.fst`
      [def, depth 4, in-statement, role explicit-arg]
  13. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  14. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  15. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver`
      [inductive, depth 2, in-statement, role explicit-arg]
  16. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  17. `CategoryTheory.Limits.CategoricalPullback.toCatCommSqOver`
      [def, depth 33, in-statement, role explicit-arg]
  18. `CategoryTheory.Limits.CategoricalPullback.CatCommSqOver.toFunctorToCategoricalPullback`
      [def, depth 35, in-statement, role explicit-arg]
  19. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  20. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  21. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  22. `CategoryTheory.Limits.CategoricalPullback`
      [inductive, depth 2, in-statement, role explicit-arg]

### proof_160  (target depth 57, band 51-75)

THEOREM PROVED: `SSet.Path.congr_vertex`

Grade all 23 candidates below.

   1. `SimplexCategory`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `SSet.Path`
      [def, depth 55, in-statement, role type-annotation]
   3. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   4. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role implicit-arg]
   5. `SimplexCategory.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
   6. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `id`
      [def, depth 0, in-statement, role explicit-arg]
   9. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
  10. `Fin`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `CategoryTheory.types`
      [def, depth 10, in-statement, role instance-slot]
  12. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  13. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  14. `SSet.Path.vertex`
      [def, depth 56, in-statement, role explicit-arg]
  15. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  16. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  19. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  20. `Opposite.op`
      [constructor, depth 1, in-statement, role explicit-arg]
  21. `SimplexCategory.smallCategory`
      [def, depth 29, in-statement, role instance-slot]
  22. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  23. `SSet`
      [def, depth 31, in-statement, role type-annotation]
