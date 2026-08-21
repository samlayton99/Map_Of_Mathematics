# Grading batch `testr_14` — 24 proofs

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

### proof_0313  (target depth 110, band 76-125)

THEOREM PROVED: `Real.iInter_Iic_rat`

Grade all 23 candidates.

   1. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   2. `Not`
      [def, depth 1, in-statement, role implicit-arg]
   3. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   4. `Real`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `Set.iInter`
      [def, depth 5, in-statement, role explicit-arg]
   6. `iInter_Iic_eq_empty_iff`
      [theorem, depth 24, introduced-by-proof, role explicit-arg]
   7. `Real.instRatCast`
      [def, depth 82, in-statement, role instance-slot]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `Set.instEmptyCollection`
      [def, depth 2, in-statement, role instance-slot]
  10. `BddBelow`
      [def, depth 5, introduced-by-proof, role explicit-arg]
  11. `EmptyCollection.emptyCollection`
      [def, depth 1, in-statement, role explicit-arg]
  12. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
  13. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  14. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  15. `Real.linearOrder`
      [def, depth 105, introduced-by-proof, role instance-slot]
  16. `Rat`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `Set.range`
      [def, depth 2, in-statement, role explicit-arg]
  18. `Rat.cast`
      [def, depth 2, in-statement, role explicit-arg]
  19. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  20. `Real.not_bddBelow_coe`
      [theorem, depth 109, introduced-by-proof, role explicit-arg]
  21. `Set.Iic`
      [def, depth 2, in-statement, role explicit-arg]
  22. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  23. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]

### proof_0314  (target depth 119, band 76-125)

THEOREM PROVED: `PseudoMetricSpace.replaceTopology_eq`

Grade all 13 candidates.

   1. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `PseudoMetricSpace.replaceTopology`
      [def, depth 118, in-statement, role instance-slot]
   3. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Dist.dist`
      [def, depth 1, in-statement, role implicit-arg]
   5. `Dist.ext`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   6. `PseudoMetricSpace.ext`
      [theorem, depth 112, introduced-by-proof, role applied]
   7. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `PseudoMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
  10. `PseudoMetricSpace.toDist`
      [def, depth 1, in-statement, role instance-slot]
  11. `TopologicalSpace`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role explicit-arg]
  13. `funext`
      [theorem, depth 4, in-statement, role explicit-arg]

### proof_0315  (target depth 76, band 76-125)

THEOREM PROVED: `Matrix.diagonalRingHom_apply`

Grade all 11 candidates.

   1. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   2. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Matrix.nonAssocSemiring`
      [def, depth 73, in-statement, role implicit-arg]
   4. `Matrix.diagonalRingHom`
      [def, depth 75, in-statement, role explicit-arg]
   5. `Pi.nonAssocSemiring`
      [def, depth 14, in-statement, role implicit-arg]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   7. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   8. `Matrix`
      [def, depth 0, in-statement, role implicit-arg]
   9. `NonAssocSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `RingHom.instFunLike`
      [def, depth 15, in-statement, role instance-slot]
  11. `RingHom`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0316  (target depth 85, band 76-125)

THEOREM PROVED: `MeasureTheory.SimpleFunc.map_const`

Grade all 5 candidates.

   1. `MeasureTheory.SimpleFunc.map`
      [def, depth 84, in-statement, role implicit-arg]
   2. `MeasureTheory.SimpleFunc.const`
      [def, depth 65, in-statement, role explicit-arg]
   3. `rfl`
      [def, depth 2, in-statement, role applied]
   4. `MeasureTheory.SimpleFunc`
      [inductive, depth 1, in-statement, role implicit-arg]
   5. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0317  (target depth 102, band 76-125)

THEOREM PROVED: `Polynomial.aeval_one`

Grade all 20 candidates.

   1. `Polynomial.instOne`
      [def, depth 62, in-statement, role instance-slot]
   2. `AlgHom.funLike`
      [def, depth 20, in-statement, role implicit-arg]
   3. `AddCommMonoidWithOne.toAddMonoidWithOne`
      [def, depth 1, in-statement, role instance-slot]
   4. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `map_one`
      [theorem, depth 5, in-statement, role applied]
   6. `Polynomial.semiring`
      [def, depth 84, in-statement, role implicit-arg]
   7. `Algebra.id`
      [def, depth 20, in-statement, role instance-slot]
   8. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   9. `NonAssocSemiring.toAddCommMonoidWithOne`
      [def, depth 10, in-statement, role instance-slot]
  10. `AddMonoidWithOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
  11. `MulZeroOneClass.toMulOneClass`
      [def, depth 1, in-statement, role instance-slot]
  12. `Polynomial.aeval`
      [def, depth 101, in-statement, role explicit-arg]
  13. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Polynomial`
      [inductive, depth 1, in-statement, role explicit-arg]
  15. `Polynomial.algebraOfAlgebra`
      [def, depth 96, in-statement, role implicit-arg]
  16. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `NonAssocSemiring.toMulZeroOneClass`
      [def, depth 5, in-statement, role implicit-arg]
  18. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role implicit-arg]
  19. `AlgHom`
      [inductive, depth 2, in-statement, role implicit-arg]
  20. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]

### proof_0318  (target depth 78, band 76-125)

THEOREM PROVED: `CategoryTheory.IsCardinalFiltered.exists_cardinal_directed.functorMap_comp_assoc`

Grade all 23 candidates.

   1. `LE.le.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `CategoryTheory.IsCardinalFiltered.exists_cardinal_directed.DiagramWithUniqueTerminal.top`
      [def, depth 20, in-statement, role implicit-arg]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   4. `CategoryTheory.Category.assoc`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.IsCardinalFiltered.exists_cardinal_directed.DiagramWithUniqueTerminal`
      [inductive, depth 19, in-statement, role implicit-arg]
   6. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   7. `id`
      [def, depth 0, in-statement, role applied]
   8. `CategoryTheory.IsCardinalFiltered.exists_cardinal_directed.instPartialOrderDiagramWithUniqueTerminal`
      [def, depth 75, in-statement, role instance-slot]
   9. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  10. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  12. `Cardinal`
      [def, depth 18, in-statement, role type-annotation]
  13. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  14. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  15. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  16. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  17. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]
  18. `forall_congr`
      [theorem, depth 5, in-statement, role explicit-arg]
  19. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  20. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  21. `CategoryTheory.IsCardinalFiltered.exists_cardinal_directed.functorMap_comp`
      [theorem, depth 77, introduced-by-proof, role explicit-arg]
  22. `CategoryTheory.IsCardinalFiltered.exists_cardinal_directed.functorMap`
      [def, depth 77, in-statement, role explicit-arg]
  23. `CategoryTheory.SmallCategory`
      [def, depth 1, in-statement, role type-annotation]

### proof_0319  (target depth 89, band 76-125)

THEOREM PROVED: `CategoryTheory.Triangulated.TStructure.spectralObjectFunctor_obj`

Grade all 25 candidates.

   1. `Preorder.smallCategory`
      [def, depth 10, in-statement, role instance-slot]
   2. `CategoryTheory.Preadditive`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `CategoryTheory.IsTriangulated`
      [inductive, depth 32, in-statement, role type-annotation]
   5. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   6. `WithTop.instPreorder`
      [def, depth 16, in-statement, role instance-slot]
   7. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   8. `Int.instAddMonoid`
      [def, depth 30, in-statement, role instance-slot]
   9. `CategoryTheory.Triangulated.TStructure.spectralObjectFunctor`
      [def, depth 88, in-statement, role explicit-arg]
  10. `WithBot.instPreorder`
      [def, depth 18, in-statement, role instance-slot]
  11. `CategoryTheory.Functor.Additive`
      [inductive, depth 2, in-statement, role type-annotation]
  12. `instLatticeInt`
      [def, depth 32, in-statement, role instance-slot]
  13. `CategoryTheory.shiftFunctor`
      [def, depth 20, in-statement, role explicit-arg]
  14. `CategoryTheory.HasShift`
      [inductive, depth 1, in-statement, role type-annotation]
  15. `CategoryTheory.Limits.HasZeroObject`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `CategoryTheory.Pretriangulated`
      [inductive, depth 31, in-statement, role type-annotation]
  17. `WithTop`
      [def, depth 1, in-statement, role implicit-arg]
  18. `CategoryTheory.Triangulated.SpectralObject`
      [inductive, depth 32, in-statement, role implicit-arg]
  19. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  20. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  21. `CategoryTheory.Triangulated.SpectralObject.instCategory`
      [def, depth 63, in-statement, role instance-slot]
  22. `CategoryTheory.Triangulated.TStructure`
      [inductive, depth 32, in-statement, role type-annotation]
  23. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  24. `EInt`
      [def, depth 3, in-statement, role explicit-arg]
  25. `Int`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0320  (target depth 80, band 76-125)

THEOREM PROVED: `Finset.Nonempty.of_vsub_right`

Grade all 5 candidates.

   1. `VSub`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Finset`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `VSub.vsub`
      [def, depth 2, in-statement, role implicit-arg]
   4. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   5. `Finset.Nonempty.of_image₂_right`
      [theorem, depth 79, introduced-by-proof, role applied]

### proof_0321  (target depth 80, band 76-125)

THEOREM PROVED: `Finset.singleton_vadd_singleton`

Grade all 5 candidates.

   1. `HVAdd.hVAdd`
      [def, depth 2, in-statement, role implicit-arg]
   2. `instHVAdd`
      [def, depth 3, in-statement, role instance-slot]
   3. `VAdd`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   5. `Finset.image₂_singleton`
      [theorem, depth 79, introduced-by-proof, role applied]

### proof_0322  (target depth 79, band 76-125)

THEOREM PROVED: `Std.ExtTreeMap.getKey?_eq_some_getKey!_of_contains`

Grade all 6 candidates.

   1. `Std.ExtDTreeMap.getKey?_eq_some_getKey!_of_contains`
      [theorem, depth 78, introduced-by-proof, role applied]
   2. `Std.ExtTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   3. `Std.ExtTreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]
   4. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0323  (target depth 78, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.mem_filter`

Grade all 23 candidates.

   1. `id`
      [def, depth 0, in-statement, role explicit-arg]
   2. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.DTreeMap.Raw.get?`
      [def, depth 18, in-statement, role explicit-arg]
   4. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `Std.DTreeMap.Raw.filter`
      [def, depth 42, in-statement, role explicit-arg]
   6. `Std.LawfulEqCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   9. `Std.DTreeMap.Raw.contains`
      [def, depth 18, in-statement, role explicit-arg]
  10. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
  11. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role implicit-arg]
  12. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  14. `Option.any`
      [def, depth 5, in-statement, role explicit-arg]
  15. `Std.DTreeMap.Raw.contains_filter`
      [theorem, depth 77, introduced-by-proof, role explicit-arg]
  16. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  17. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  18. `_private.Std.Data.DTreeMap.Raw.Lemmas.0.Std.DTreeMap.Raw.mem_filter._simp_1_2`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
  19. `Std.DTreeMap.Raw.instMembership`
      [def, depth 19, in-statement, role instance-slot]
  20. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  21. `_private.Std.Data.DTreeMap.Raw.Lemmas.0.Std.DTreeMap.Raw.mem_filter._simp_1_1`
      [theorem, depth 20, introduced-by-proof, role explicit-arg]
  22. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  23. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0324  (target depth 77, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Const.getD_alter_self`

Grade all 7 candidates.

   1. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Std.DTreeMap.Internal.Impl.Const.getD_alter_self`
      [theorem, depth 76, introduced-by-proof, role applied]
   3. `Std.DTreeMap.wf`
      [theorem, depth 17, in-statement, role explicit-arg]
   4. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Std.DTreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]
   6. `Option`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.DTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]

### proof_0325  (target depth 84, band 76-125)

THEOREM PROVED: `mem_doublyStochastic`

Grade all 15 candidates.

   1. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   2. `instMulZeroOneClassOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
   3. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Submonoid.instSetLike`
      [def, depth 10, in-statement, role instance-slot]
   5. `Submonoid`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `MulZeroOneClass.toMulOneClass`
      [def, depth 1, in-statement, role instance-slot]
   7. `IsOrderedRing`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   9. `Matrix`
      [def, depth 0, in-statement, role explicit-arg]
  10. `Iff.rfl`
      [theorem, depth 3, in-statement, role applied]
  11. `Matrix.semiring`
      [def, depth 81, in-statement, role instance-slot]
  12. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  13. `doublyStochastic`
      [def, depth 83, in-statement, role explicit-arg]
  14. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0326  (target depth 86, band 76-125)

THEOREM PROVED: `Cardinal.mk_set_nat`

Grade all 22 candidates.

   1. `Cardinal.mk_set`
      [theorem, depth 68, introduced-by-proof, role explicit-arg]
   2. `Cardinal.instPowCardinal`
      [def, depth 21, in-statement, role instance-slot]
   3. `Cardinal.mk_eq_aleph0`
      [theorem, depth 85, introduced-by-proof, role explicit-arg]
   4. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   5. `Cardinal.instNatCast`
      [def, depth 22, in-statement, role instance-slot]
   6. `HPow.hPow`
      [def, depth 2, in-statement, role implicit-arg]
   7. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
   8. `Set`
      [def, depth 0, in-statement, role explicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Cardinal.aleph0`
      [def, depth 22, in-statement, role explicit-arg]
  11. `Cardinal.mk`
      [def, depth 18, in-statement, role explicit-arg]
  12. `instOfNatAtLeastTwo`
      [def, depth 3, in-statement, role instance-slot]
  13. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  14. `instHPow`
      [def, depth 3, in-statement, role instance-slot]
  15. `Cardinal.continuum`
      [def, depth 23, in-statement, role explicit-arg]
  16. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
  17. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  18. `Cardinal`
      [def, depth 18, in-statement, role implicit-arg]
  19. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  20. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  21. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  22. `True`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0327  (target depth 77, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.getD_erase`

Grade all 8 candidates.

   1. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   2. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Std.DTreeMap.Internal.Impl.getD_erase!`
      [theorem, depth 76, introduced-by-proof, role applied]
   4. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
   5. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Std.LawfulEqCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   8. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]

### proof_0328  (target depth 95, band 76-125)

THEOREM PROVED: `Ordinal.lift_eq_omega_ofNat`

Grade all 4 candidates.

   1. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Ordinal.lift_eq_omega_natCast`
      [theorem, depth 94, introduced-by-proof, role applied]
   3. `Nat.AtLeastTwo`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Ordinal`
      [def, depth 25, in-statement, role type-annotation]

### proof_0329  (target depth 92, band 76-125)

THEOREM PROVED: `finsuppTensorFinsupp'_symm_single_mul`

Grade all 6 candidates.

   1. `Semiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
   2. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   4. `Prod`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `finsuppTensorFinsuppLid_symm_single_smul`
      [theorem, depth 91, introduced-by-proof, role applied]
   6. `Semiring.toModule`
      [def, depth 13, in-statement, role instance-slot]

### proof_0330  (target depth 77, band 76-125)

THEOREM PROVED: `Equiv.toEquiv_toHomeomorphOfIsInducing`

Grade all 9 candidates.

   1. `Equiv.toHomeomorphOfIsInducing`
      [def, depth 76, in-statement, role explicit-arg]
   2. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Topology.IsInducing`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   5. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   7. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   8. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Homeomorph.toEquiv`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0331  (target depth 80, band 76-125)

THEOREM PROVED: `Std.TreeMap.getKey?_inter_of_not_mem_left`

Grade all 8 candidates.

   1. `Std.TreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   2. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.TreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]
   5. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Std.DTreeMap.getKey?_inter_of_not_mem_left`
      [theorem, depth 79, introduced-by-proof, role applied]
   7. `Std.TreeMap.instMembership`
      [def, depth 20, in-statement, role instance-slot]
   8. `Not`
      [def, depth 1, in-statement, role type-annotation]

### proof_0332  (target depth 110, band 76-125)

THEOREM PROVED: `ENNReal.le_of_add_le_add_right`

Grade all 17 candidates.

   1. `NNReal.instAddCancelCommMonoid`
      [def, depth 107, introduced-by-proof, role instance-slot]
   2. `NNReal.instSemiring`
      [def, depth 106, in-statement, role instance-slot]
   3. `NNReal.instPartialOrder`
      [def, depth 102, in-statement, role instance-slot]
   4. `Distrib.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   5. `AddCancelCommMonoid.toAddCancelMonoid`
      [def, depth 8, introduced-by-proof, role instance-slot]
   6. `WithTop.le_of_add_le_add_right`
      [theorem, depth 16, introduced-by-proof, role applied]
   7. `AddRightCancelMonoid.toAddRightCancelSemigroup`
      [def, depth 3, introduced-by-proof, role instance-slot]
   8. `AddCommMonoid.toAddCommSemigroup`
      [def, depth 5, in-statement, role instance-slot]
   9. `NNReal`
      [def, depth 95, in-statement, role explicit-arg]
  10. `instDistribOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
  11. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  12. `AddCancelMonoid.toAddRightCancelMonoid`
      [def, depth 3, introduced-by-proof, role instance-slot]
  13. `LT.lt`
      [def, depth 1, in-statement, role explicit-arg]
  14. `Semiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
  15. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
  16. `ENNReal`
      [def, depth 96, in-statement, role type-annotation]
  17. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]

### proof_0333  (target depth 77, band 76-125)

THEOREM PROVED: `UniformEquiv.piCongrLeft_toEquiv`

Grade all 9 candidates.

   1. `UniformEquiv.toEquiv`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   4. `UniformEquiv.piCongrLeft`
      [def, depth 76, in-statement, role explicit-arg]
   5. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   6. `UniformSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Pi.uniformSpace`
      [def, depth 71, in-statement, role instance-slot]
   8. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]

### proof_0334  (target depth 100, band 76-125)

THEOREM PROVED: `Set.Nonempty.ncard_pos`

Grade all 13 candidates.

   1. `Set.ncard`
      [def, depth 90, in-statement, role explicit-arg]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   3. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   4. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
   6. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   7. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   8. `Set`
      [def, depth 0, in-statement, role type-annotation]
   9. `Set.Finite`
      [def, depth 5, in-statement, role explicit-arg]
  10. `Set.ncard_pos._auto_1`
      [def, depth 8, in-statement, role explicit-arg]
  11. `Set.ncard_pos`
      [theorem, depth 99, introduced-by-proof, role explicit-arg]
  12. `Set.Nonempty`
      [def, depth 4, in-statement, role implicit-arg]
  13. `autoParam`
      [def, depth 1, in-statement, role type-annotation]

### proof_0335  (target depth 77, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.Const.get!_eq_default`

Grade all 8 candidates.

   1. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Std.DTreeMap.Internal.Impl.Const.get!_eq_default`
      [theorem, depth 76, introduced-by-proof, role applied]
   3. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   4. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   6. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   8. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]

### proof_0336  (target depth 80, band 76-125)

THEOREM PROVED: `Std.ExtTreeMap.contains_of_contains_filter`

Grade all 6 candidates.

   1. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.ExtDTreeMap.contains_of_contains_filter`
      [theorem, depth 79, introduced-by-proof, role applied]
   3. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.ExtTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   5. `Bool`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Std.ExtTreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]
