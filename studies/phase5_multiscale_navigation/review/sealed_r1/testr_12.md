# Grading batch `testr_12` — 24 proofs

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

### proof_0265  (target depth 75, band 51-75)

THEOREM PROVED: `Std.DTreeMap.containsThenInsertIfNew_fst`

Grade all 6 candidates.

   1. `Std.DTreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]
   2. `Std.DTreeMap.Internal.Impl.containsThenInsertIfNew_fst`
      [theorem, depth 74, introduced-by-proof, role applied]
   3. `Std.DTreeMap.wf`
      [theorem, depth 17, in-statement, role explicit-arg]
   4. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Std.DTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]

### proof_0266  (target depth 67, band 51-75)

THEOREM PROVED: `TopologicalSpace.Opens.coe_inf`

Grade all 12 candidates.

   1. `SetLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   2. `SemilatticeInf.toMin`
      [def, depth 2, in-statement, role instance-slot]
   3. `Min.min`
      [def, depth 1, in-statement, role explicit-arg]
   4. `TopologicalSpace.Opens`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `TopologicalSpace.Opens.instSetLike`
      [def, depth 8, in-statement, role instance-slot]
   6. `rfl`
      [def, depth 2, in-statement, role applied]
   7. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   8. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `ConditionallyCompleteLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  10. `CompleteLattice.toConditionallyCompleteLattice`
      [def, depth 9, in-statement, role instance-slot]
  11. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  12. `TopologicalSpace.Opens.instCompleteLattice`
      [def, depth 66, in-statement, role instance-slot]

### proof_0267  (target depth 73, band 51-75)

THEOREM PROVED: `Std.HashSet.get!_union_of_not_mem_left`

Grade all 12 candidates.

   1. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Unit`
      [def, depth 1, in-statement, role implicit-arg]
   3. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.HashMap.getKey!_union_of_not_mem_left`
      [theorem, depth 72, introduced-by-proof, role applied]
   5. `Std.HashSet.instMembership`
      [def, depth 70, in-statement, role instance-slot]
   6. `Std.HashSet.inner`
      [def, depth 2, in-statement, role implicit-arg]
   7. `Not`
      [def, depth 1, in-statement, role type-annotation]
   8. `Std.HashSet`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
  12. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0268  (target depth 64, band 51-75)

THEOREM PROVED: `SimplexCategoryGenRel.instHasFactorizationP_σP_δ`

Grade all 18 candidates.

   1. `Exists.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   2. `CategoryTheory.MorphismProperty.MapFactorizationData.mk`
      [constructor, depth 9, introduced-by-proof, role explicit-arg]
   3. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   5. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `instCategorySimplexCategoryGenRel`
      [def, depth 15, in-statement, role instance-slot]
   7. `CategoryTheory.MorphismProperty.HasFactorization.mk`
      [constructor, depth 4, introduced-by-proof, role applied]
   8. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   9. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  10. `CategoryTheory.MorphismProperty.MapFactorizationData`
      [inductive, depth 3, introduced-by-proof, role explicit-arg]
  11. `SimplexCategoryGenRel`
      [def, depth 14, in-statement, role implicit-arg]
  12. `Nonempty`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  13. `Nonempty.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  14. `SimplexCategoryGenRel.P_δ`
      [def, depth 17, in-statement, role implicit-arg]
  15. `SimplexCategoryGenRel.P_σ`
      [def, depth 17, in-statement, role implicit-arg]
  16. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  17. `SimplexCategoryGenRel.exists_P_σ_P_δ_factorization`
      [theorem, depth 63, introduced-by-proof, role explicit-arg]
  18. `Exists`
      [inductive, depth 0, introduced-by-proof, role explicit-arg]

### proof_0269  (target depth 67, band 51-75)

THEOREM PROVED: `Uniform.tendsto_congr`

Grade all 11 candidates.

   1. `uniformity`
      [def, depth 2, in-statement, role explicit-arg]
   2. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   3. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Filter.Tendsto.congr_uniformity`
      [theorem, depth 66, introduced-by-proof, role explicit-arg]
   5. `Prod.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
   6. `Filter`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Filter.Tendsto.uniformity_symm`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
   8. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
   9. `UniformSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `nhds`
      [def, depth 18, in-statement, role explicit-arg]
  11. `Filter.Tendsto`
      [def, depth 13, in-statement, role type-annotation]

### proof_0270  (target depth 55, band 51-75)

THEOREM PROVED: `Filter.eventually_ne_atTop`

Grade all 10 candidates.

   1. `Filter.Eventually.mono`
      [theorem, depth 9, introduced-by-proof, role applied]
   2. `Ne`
      [def, depth 2, in-statement, role implicit-arg]
   3. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   5. `NoTopOrder`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Filter.atTop`
      [def, depth 15, in-statement, role implicit-arg]
   7. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `ne_of_gt`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   9. `Filter.eventually_gt_atTop`
      [theorem, depth 54, introduced-by-proof, role explicit-arg]
  10. `Preorder.toLT`
      [def, depth 1, introduced-by-proof, role instance-slot]

### proof_0271  (target depth 60, band 51-75)

THEOREM PROVED: `Finset.apply_sup_eq_sup_comp_of_linearOrder`

Grade all 18 candidates.

   1. `Bot.bot`
      [def, depth 1, in-statement, role explicit-arg]
   2. `SemilatticeSup`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Finset`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
   5. `SemilatticeSup.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   6. `OrderBot.toBot`
      [def, depth 2, in-statement, role instance-slot]
   7. `Lattice.toSemilatticeSup`
      [def, depth 1, in-statement, role instance-slot]
   8. `Preorder.toLE`
      [def, depth 1, in-statement, role implicit-arg]
   9. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  10. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  11. `OrderBot`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  14. `Monotone.map_sup`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
  15. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  16. `Finset.apply_sup_eq_sup_comp`
      [theorem, depth 59, introduced-by-proof, role applied]
  17. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `Monotone`
      [def, depth 2, in-statement, role type-annotation]

### proof_0272  (target depth 63, band 51-75)

THEOREM PROVED: `Finset.subset_compl_comm`

Grade all 7 candidates.

   1. `BooleanAlgebra.toBiheytingAlgebra`
      [def, depth 53, introduced-by-proof, role instance-slot]
   2. `BiheytingAlgebra.toHeytingAlgebra`
      [def, depth 1, introduced-by-proof, role instance-slot]
   3. `le_compl_iff_le_compl`
      [theorem, depth 8, introduced-by-proof, role applied]
   4. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Finset.booleanAlgebra`
      [def, depth 62, in-statement, role instance-slot]
   6. `Finset`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]

### proof_0273  (target depth 70, band 51-75)

THEOREM PROVED: `CoalgEquiv.trans_toCoalgHom`

Grade all 12 candidates.

   1. `CoalgHomClass.toCoalgHom`
      [def, depth 58, in-statement, role implicit-arg]
   2. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CoalgHom`
      [inductive, depth 3, in-statement, role implicit-arg]
   4. `rfl`
      [def, depth 2, in-statement, role applied]
   5. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CoalgebraStruct`
      [inductive, depth 2, in-statement, role type-annotation]
   7. `CoalgEquiv.trans`
      [def, depth 69, in-statement, role explicit-arg]
   8. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   9. `CoalgEquiv.instEquivLike`
      [def, depth 66, in-statement, role implicit-arg]
  10. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `CoalgEquiv`
      [inductive, depth 3, in-statement, role type-annotation]
  12. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]

### proof_0274  (target depth 67, band 51-75)

THEOREM PROVED: `PresentedGroup.mk_surjective`

Grade all 5 candidates.

   1. `FreeGroup.instGroup`
      [def, depth 18, in-statement, role instance-slot]
   2. `Subgroup.normalClosure`
      [def, depth 66, in-statement, role implicit-arg]
   3. `FreeGroup`
      [def, depth 2, in-statement, role explicit-arg]
   4. `QuotientGroup.mk_surjective`
      [theorem, depth 66, introduced-by-proof, role applied]
   5. `Set`
      [def, depth 0, in-statement, role type-annotation]

### proof_0275  (target depth 58, band 51-75)

THEOREM PROVED: `Finset.sup_insert`

Grade all 12 candidates.

   1. `Bot.bot`
      [def, depth 1, in-statement, role implicit-arg]
   2. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   3. `Preorder.toLE`
      [def, depth 1, in-statement, role implicit-arg]
   4. `SemilatticeSup.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   5. `SemilatticeSup.toMax`
      [def, depth 2, in-statement, role instance-slot]
   6. `SemilatticeSup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Finset.fold_insert_idem`
      [theorem, depth 57, introduced-by-proof, role applied]
   8. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   9. `Max.max`
      [def, depth 1, in-statement, role implicit-arg]
  10. `Finset`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `OrderBot.toBot`
      [def, depth 2, in-statement, role instance-slot]
  12. `OrderBot`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0276  (target depth 63, band 51-75)

THEOREM PROVED: `instDiscreteTopologyPUnit`

Grade all 5 candidates.

   1. `DiscreteTopology.mk`
      [constructor, depth 62, introduced-by-proof, role applied]
   2. `instTopologicalSpacePUnit`
      [def, depth 62, in-statement, role implicit-arg]
   3. `PUnit`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
   5. `TopologicalSpace`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0277  (target depth 72, band 51-75)

THEOREM PROVED: `Std.HashMap.getElem!_union_of_not_mem_right`

Grade all 11 candidates.

   1. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.HashMap`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Std.HashMap.instMembership`
      [def, depth 69, in-statement, role instance-slot]
   6. `Std.HashMap.inner`
      [def, depth 2, in-statement, role implicit-arg]
   7. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Std.DHashMap.Const.get!_union_of_not_mem_right`
      [theorem, depth 71, introduced-by-proof, role applied]
  10. `Not`
      [def, depth 1, in-statement, role type-annotation]
  11. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0278  (target depth 52, band 51-75)

THEOREM PROVED: `lowerHemicontinuousOn_iff`

Grade all 4 candidates.

   1. `LowerHemicontinuousOn`
      [def, depth 51, in-statement, role implicit-arg]
   2. `Set`
      [def, depth 0, in-statement, role type-annotation]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Iff.rfl`
      [theorem, depth 3, in-statement, role applied]

### proof_0279  (target depth 60, band 51-75)

THEOREM PROVED: `Finset.support_prod_subset`

Grade all 21 candidates.

   1. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   4. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   5. `MonoidWithZero.toMulZeroOneClass`
      [def, depth 5, in-statement, role instance-slot]
   6. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
   7. `CommMonoidWithZero.toMonoidWithZero`
      [def, depth 5, in-statement, role instance-slot]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `CommMonoidWithZero.toCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
  10. `Set.mem_iInter₂`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
  11. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
  12. `Finset.prod`
      [def, depth 13, in-statement, role explicit-arg]
  13. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  15. `CommMonoidWithZero`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  17. `Finset.prod_eq_zero`
      [theorem, depth 59, introduced-by-proof, role explicit-arg]
  18. `MulZeroOneClass.toMulZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  19. `Function.support`
      [def, depth 4, in-statement, role explicit-arg]
  20. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  21. `Set.iInter`
      [def, depth 5, in-statement, role explicit-arg]

### proof_0280  (target depth 62, band 51-75)

THEOREM PROVED: `Set.image_single_Ico`

Grade all 7 candidates.

   1. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   2. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Pi.instZero`
      [def, depth 4, in-statement, role instance-slot]
   5. `Set.image_update_Ico`
      [theorem, depth 61, introduced-by-proof, role applied]
   6. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   7. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0281  (target depth 51, band 51-75)

THEOREM PROVED: `IsRetrocompact.inter_isOpen`

Grade all 12 candidates.

   1. `IsOpen`
      [def, depth 2, in-statement, role type-annotation]
   2. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `Set`
      [def, depth 0, in-statement, role type-annotation]
   4. `IsOpen.inter`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Set.inter_assoc`
      [theorem, depth 6, in-statement, role explicit-arg]
   6. `Eq.rec`
      [recursor, depth 2, in-statement, role applied]
   7. `Inter.inter`
      [def, depth 1, in-statement, role explicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Set.instInter`
      [def, depth 5, in-statement, role instance-slot]
  10. `IsRetrocompact`
      [def, depth 50, in-statement, role type-annotation]
  11. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `IsCompact`
      [def, depth 49, in-statement, role implicit-arg]

### proof_0282  (target depth 65, band 51-75)

THEOREM PROVED: `Partition.IsRepFun.image_subset`

Grade all 23 candidates.

   1. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
   2. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   3. `Classical.propDecidable`
      [def, depth 11, in-statement, role instance-slot]
   4. `Partition.IsRepFun.apply_mem`
      [theorem, depth 64, introduced-by-proof, role explicit-arg]
   5. `Not`
      [def, depth 1, in-statement, role type-annotation]
   6. `Set.instCompleteAtomicBooleanAlgebra`
      [def, depth 58, in-statement, role instance-slot]
   7. `And`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   9. `And.casesOn`
      [def, depth 3, in-statement, role explicit-arg]
  10. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `dite`
      [def, depth 5, in-statement, role explicit-arg]
  12. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
  13. `Eq.rec`
      [recursor, depth 2, in-statement, role explicit-arg]
  14. `Set.image`
      [def, depth 4, in-statement, role explicit-arg]
  15. `Partition`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`
      [def, depth 1, in-statement, role instance-slot]
  17. `Partition.IsRepFun.apply_of_notMem`
      [theorem, depth 60, introduced-by-proof, role explicit-arg]
  18. `Partition.IsRepFun`
      [inductive, depth 59, in-statement, role type-annotation]
  19. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]
  20. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  21. `Exists.casesOn`
      [def, depth 3, in-statement, role applied]
  22. `CompleteBooleanAlgebra.toCompleteLattice`
      [def, depth 1, in-statement, role instance-slot]
  23. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0283  (target depth 68, band 51-75)

THEOREM PROVED: `Nat.Prime.not_perfect`

Grade all 5 candidates.

   1. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Nat.Perfect.pseudoperfect`
      [theorem, depth 59, introduced-by-proof, role explicit-arg]
   3. `Nat.Prime.not_pseudoperfect`
      [theorem, depth 67, introduced-by-proof, role applied]
   4. `Nat.Perfect`
      [def, depth 58, in-statement, role type-annotation]
   5. `Nat.Prime`
      [def, depth 19, in-statement, role type-annotation]

### proof_0284  (target depth 74, band 51-75)

THEOREM PROVED: `Std.ExtHashMap.isEmpty_inter_left`

Grade all 11 candidates.

   1. `Std.ExtHashMap.isEmpty`
      [def, depth 69, in-statement, role explicit-arg]
   2. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Std.ExtHashMap`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Std.ExtDHashMap.isEmpty_inter_left`
      [theorem, depth 73, introduced-by-proof, role applied]
   9. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `Std.ExtHashMap.inner`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0285  (target depth 73, band 51-75)

THEOREM PROVED: `DirichletCharacter.primitive_mul_isPrimitive`

Grade all 6 candidates.

   1. `DirichletCharacter`
      [def, depth 57, in-statement, role type-annotation]
   2. `Nat.lcm`
      [def, depth 25, in-statement, role implicit-arg]
   3. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `DirichletCharacter.primitiveCharacter_isPrimitive`
      [theorem, depth 72, introduced-by-proof, role applied]
   5. `CommMonoidWithZero`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `DirichletCharacter.mul`
      [def, depth 64, in-statement, role explicit-arg]

### proof_0286  (target depth 69, band 51-75)

THEOREM PROVED: `Std.DHashMap.Const.get_eq_getD`

Grade all 21 candidates.

   1. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   2. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.DHashMap.instMembership`
      [def, depth 68, in-statement, role instance-slot]
   4. `Std.DHashMap.Internal.Raw₀.Const.get_eq_getD`
      [theorem, depth 66, introduced-by-proof, role applied]
   5. `_private.Std.Data.DHashMap.Basic.0.Std.DHashMap.Const.get?._proof_1`
      [theorem, depth 66, in-statement, role explicit-arg]
   6. `Std.DHashMap.Raw.buckets`
      [def, depth 1, in-statement, role explicit-arg]
   7. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   8. `Std.DHashMap`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `Std.DHashMap.wf`
      [theorem, depth 2, in-statement, role explicit-arg]
  10. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Subtype.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  13. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
  15. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  16. `Array.size`
      [def, depth 10, in-statement, role explicit-arg]
  17. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  19. `Std.DHashMap.inner`
      [def, depth 2, in-statement, role explicit-arg]
  20. `Std.DHashMap.Internal.AssocList`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `Std.DHashMap.Raw`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0287  (target depth 71, band 51-75)

THEOREM PROVED: `Std.HashMap.not_mem_emptyWithCapacity`

Grade all 4 candidates.

   1. `Std.DHashMap.not_mem_emptyWithCapacity`
      [theorem, depth 70, introduced-by-proof, role applied]
   2. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0288  (target depth 60, band 51-75)

THEOREM PROVED: `Sum.Ioo_inr_inl`

Grade all 10 candidates.

   1. `Sum.inr`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Sum`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `rfl`
      [def, depth 2, in-statement, role applied]
   4. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Finset.Ioo`
      [def, depth 3, in-statement, role implicit-arg]
   6. `LocallyFiniteOrder`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Sum.inl`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Sum.instPreorderSum`
      [def, depth 13, in-statement, role instance-slot]
  10. `Sum.instLocallyFiniteOrder`
      [def, depth 59, in-statement, role instance-slot]
