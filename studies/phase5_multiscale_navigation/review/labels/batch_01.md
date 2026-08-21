# Grading batch `batch_01` -- 20 proofs

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

### proof_001  (target depth 4, band 0-10)

THEOREM PROVED: `CategoryTheory.MorphismProperty.IsStableUnderCobaseChange.of_isPushout`

Grade all 4 candidates below.

   1. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   3. `CategoryTheory.MorphismProperty.IsStableUnderCobaseChange`
      [inductive, depth 3, in-statement, role type-annotation]
   4. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]

### proof_002  (target depth 11, band 11-25)

THEOREM PROVED: `Submodule.mem_toAddSubmonoid`

Grade all 12 candidates below.

   1. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   2. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   4. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   6. `AddSubmonoid`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `Submodule`
      [inductive, depth 2, in-statement, role type-annotation]
   8. `AddSubmonoid.instSetLike`
      [def, depth 10, in-statement, role instance-slot]
   9. `Iff.rfl`
      [theorem, depth 3, introduced-by-proof, role applied]
  10. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Submodule.toAddSubmonoid`
      [def, depth 3, in-statement, role explicit-arg]
  12. `AddCommMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]

### proof_003  (target depth 27, band 26-50)

THEOREM PROVED: `Submonoid.saturation_toSubmonoid`

Grade all 10 candidates below.

   1. `Submonoid.saturation`
      [def, depth 23, in-statement, role implicit-arg]
   2. `SaturatedSubmonoid`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Submonoid`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `SaturatedSubmonoid.instPartialOrder`
      [def, depth 22, introduced-by-proof, role instance-slot]
   5. `GaloisInsertion.l_u_eq`
      [theorem, depth 5, introduced-by-proof, role applied]
   6. `Submonoid.instPartialOrder`
      [def, depth 22, in-statement, role instance-slot]
   7. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   8. `MulOneClass`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Submonoid.giSaturation`
      [def, depth 26, introduced-by-proof, role explicit-arg]
  10. `SaturatedSubmonoid.toSubmonoid`
      [def, depth 2, in-statement, role implicit-arg]

### proof_004  (target depth 75, band 51-75)

THEOREM PROVED: `Std.DTreeMap.toList_filter`

Grade all 6 candidates below.

   1. `Std.DTreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]
   2. `Bool`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.DTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   4. `Std.DTreeMap.wf`
      [theorem, depth 17, in-statement, role explicit-arg]
   5. `Std.DTreeMap.Internal.Impl.toList_filter`
      [theorem, depth 74, introduced-by-proof, role applied]
   6. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_005  (target depth 77, band 76-125)

THEOREM PROVED: `Rat.ofNat_add_den`

Grade all 3 candidates below.

   1. `Rat.natCast_add_den`
      [theorem, depth 76, introduced-by-proof, role applied]
   2. `Rat`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_006  (target depth 165, band 126+)

THEOREM PROVED: `ProbabilityTheory.IsKolmogorovProcess.IsAEKolmogorovProcess`

Grade all 18 candidates below.

   1. `MeasureTheory.ae`
      [def, depth 128, in-statement, role explicit-arg]
   2. `implies_true`
      [theorem, depth 4, in-statement, role explicit-arg]
   3. `MeasureTheory.Measure.instFunLike`
      [def, depth 163, in-statement, role instance-slot]
   4. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `forall_congr`
      [theorem, depth 5, in-statement, role explicit-arg]
   7. `ProbabilityTheory.IsKolmogorovProcess`
      [inductive, depth 96, in-statement, role explicit-arg]
   8. `Real`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Filter.EventuallyEq`
      [def, depth 6, in-statement, role type-annotation]
  10. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `PseudoEMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Filter.EventuallyEq.refl._simp_1`
      [theorem, depth 10, introduced-by-proof, role explicit-arg]
  13. `NNReal`
      [def, depth 95, in-statement, role type-annotation]
  14. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
  16. `And.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
  17. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role implicit-arg]
  18. `Exists.intro`
      [constructor, depth 1, in-statement, role applied]

### proof_007  (target depth 3, band 0-10)

THEOREM PROVED: `Bipointed.coe_of`

Grade all 4 candidates below.

   1. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   2. `Prod`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Bipointed.X`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Bipointed.of`
      [def, depth 2, in-statement, role explicit-arg]

### proof_008  (target depth 11, band 11-25)

THEOREM PROVED: `List.filterMapM_nil`

Grade all 6 candidates below.

   1. `List.filterMapM`
      [def, depth 10, in-statement, role implicit-arg]
   2. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
   3. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   5. `Monad`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Option`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_009  (target depth 43, band 26-50)

THEOREM PROVED: `CategoryTheory.Lax.LaxTrans.rightUnitor_hom_as_app`

Grade all 21 candidates below.

   1. `CategoryTheory.PrelaxFunctor.toPrelaxFunctorStruct`
      [def, depth 2, in-statement, role explicit-arg]
   2. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   3. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   4. `CategoryTheory.Lax.LaxTrans.Modification.app`
      [def, depth 29, in-statement, role explicit-arg]
   5. `CategoryTheory.Bicategory`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CategoryTheory.Bicategory.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.Lax.LaxTrans.rightUnitor`
      [def, depth 42, in-statement, role explicit-arg]
   8. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
   9. `CategoryTheory.LaxFunctor`
      [inductive, depth 1, in-statement, role implicit-arg]
  10. `CategoryTheory.Lax.LaxTrans.instCategoryStructLaxFunctor`
      [def, depth 27, in-statement, role instance-slot]
  11. `CategoryTheory.LaxFunctor.toPrelaxFunctor`
      [def, depth 2, in-statement, role explicit-arg]
  12. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role explicit-arg]
  13. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  14. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  15. `CategoryTheory.Lax.LaxTrans.Hom.as`
      [def, depth 29, in-statement, role explicit-arg]
  16. `CategoryTheory.Lax.LaxTrans.app`
      [def, depth 3, in-statement, role explicit-arg]
  17. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  18. `CategoryTheory.Lax.LaxTrans.homCategory`
      [def, depth 38, in-statement, role instance-slot]
  19. `Prefunctor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  20. `CategoryTheory.PrelaxFunctorStruct.toPrefunctor`
      [def, depth 3, in-statement, role explicit-arg]
  21. `CategoryTheory.Bicategory.homCategory`
      [def, depth 1, in-statement, role instance-slot]

### proof_010  (target depth 54, band 51-75)

THEOREM PROVED: `Nat.ModEq.sum`

Grade all 8 candidates below.

   1. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
   2. `Nat.ModEq`
      [def, depth 21, in-statement, role type-annotation]
   3. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   4. `Finset.val`
      [def, depth 1, in-statement, role implicit-arg]
   5. `Nat.ModEq.multisetSum_map`
      [theorem, depth 48, introduced-by-proof, role applied]
   6. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]

### proof_011  (target depth 76, band 76-125)

THEOREM PROVED: `CommBialgCat.bialgEquivOfIso_symm_apply`

Grade all 21 candidates below.

   1. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   2. `CommBialgCat.instCommRingObjForgetBialgHomCarrier`
      [def, depth 3, in-statement, role instance-slot]
   3. `CoalgEquiv.symm`
      [def, depth 69, in-statement, role explicit-arg]
   4. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   5. `CoalgEquiv.instFunLike`
      [def, depth 67, in-statement, role instance-slot]
   6. `BialgEquiv.toCoalgEquiv`
      [def, depth 20, in-statement, role explicit-arg]
   7. `Bialgebra.toAlgebra`
      [def, depth 2, in-statement, role instance-slot]
   8. `Bialgebra.toCoalgebra`
      [def, depth 2, in-statement, role instance-slot]
   9. `CommBialgCat.instCategory`
      [def, depth 70, in-statement, role instance-slot]
  10. `CommBialgCat.bialgEquivOfIso`
      [def, depth 75, in-statement, role explicit-arg]
  11. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Semiring.toAddCommMonoid`
      [def, depth 1, in-statement, role implicit-arg]
  13. `CoalgEquiv`
      [inductive, depth 3, in-statement, role implicit-arg]
  14. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role implicit-arg]
  15. `Algebra.toModule`
      [def, depth 18, in-statement, role implicit-arg]
  16. `CommBialgCat.carrier`
      [def, depth 2, in-statement, role implicit-arg]
  17. `CommBialgCat.instBialgebraObjForgetBialgHomCarrier`
      [def, depth 3, in-statement, role instance-slot]
  18. `CommBialgCat`
      [inductive, depth 1, in-statement, role type-annotation]
  19. `Coalgebra.toCoalgebraStruct`
      [def, depth 3, in-statement, role instance-slot]
  20. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
  21. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]

### proof_012  (target depth 295, band 126+)

THEOREM PROVED: `HurwitzZeta.hurwitzOddFEPair_f`

Grade all 11 candidates below.

   1. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role implicit-arg]
   2. `HurwitzZeta.hurwitzOddFEPair`
      [def, depth 294, in-statement, role explicit-arg]
   3. `Complex`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `RCLike.innerProductSpace`
      [def, depth 156, in-statement, role instance-slot]
   5. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   6. `WeakFEPair.f`
      [def, depth 136, in-statement, role explicit-arg]
   7. `InnerProductSpace.toNormedSpace`
      [def, depth 3, in-statement, role instance-slot]
   8. `UnitAddCircle`
      [def, depth 95, in-statement, role type-annotation]
   9. `Complex.instNormedAddCommGroup`
      [def, depth 132, in-statement, role instance-slot]
  10. `Real`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Complex.instRCLike`
      [def, depth 156, in-statement, role implicit-arg]

### proof_013  (target depth 5, band 0-10)

THEOREM PROVED: `Pi.isMulCommutative`

Grade all 9 candidates below.

   1. `Std.Commutative.mk`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   2. `Pi.instMul`
      [def, depth 4, in-statement, role instance-slot]
   3. `IsMulCommutative.mk`
      [constructor, depth 4, introduced-by-proof, role applied]
   4. `HMul.hMul`
      [def, depth 2, in-statement, role implicit-arg]
   5. `funext`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   6. `IsMulCommutative`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Mul`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
   9. `mul_comm'`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]

### proof_014  (target depth 22, band 11-25)

THEOREM PROVED: `Equiv.sigmaQuotFromRel_apply`

Grade all 21 candidates below.

   1. `Quot`
      [quot, depth 0, in-statement, role implicit-arg]
   2. `Std.Symm`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Equiv.sigmaQuotFromRel`
      [def, depth 21, in-statement, role explicit-arg]
   4. `RelHom`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
   6. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   7. `Function.onFun`
      [def, depth 0, in-statement, role implicit-arg]
   8. `Std.Symm.comap`
      [theorem, depth 4, in-statement, role explicit-arg]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  10. `Sigma`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Equiv.sigmaFiberFromRel._proof_4`
      [theorem, depth 5, in-statement, role explicit-arg]
  12. `Quot.mk`
      [quot, depth 1, in-statement, role explicit-arg]
  13. `Sym2.fromRel`
      [def, depth 14, in-statement, role explicit-arg]
  14. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  15. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  16. `Subtype`
      [inductive, depth 0, in-statement, role explicit-arg]
  17. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
  18. `RelHom.instFunLike`
      [def, depth 5, in-statement, role instance-slot]
  19. `Sym2`
      [def, depth 2, in-statement, role implicit-arg]
  20. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_015  (target depth 29, band 26-50)

THEOREM PROVED: `SemimoduleCat.hom_zero`

Grade all 17 candidates below.

   1. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
   2. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   3. `SemimoduleCat.Hom.hom`
      [def, depth 28, in-statement, role implicit-arg]
   4. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   5. `LinearMap`
      [inductive, depth 11, in-statement, role implicit-arg]
   6. `SemimoduleCat.isModule`
      [def, depth 2, in-statement, role instance-slot]
   7. `SemimoduleCat.instZeroHom`
      [def, depth 26, in-statement, role instance-slot]
   8. `SemimoduleCat.carrier`
      [def, depth 2, in-statement, role explicit-arg]
   9. `SemimoduleCat.moduleCategory`
      [def, depth 25, in-statement, role instance-slot]
  10. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  11. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  12. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  13. `SemimoduleCat.isAddCommMonoid`
      [def, depth 2, in-statement, role instance-slot]
  14. `SemimoduleCat`
      [inductive, depth 1, in-statement, role type-annotation]
  15. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  16. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `rfl`
      [def, depth 2, in-statement, role applied]

### proof_016  (target depth 73, band 51-75)

THEOREM PROVED: `Std.ExtHashSet.size_erase_le`

Grade all 8 candidates below.

   1. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.ExtHashSet`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Std.ExtHashMap.size_erase_le`
      [theorem, depth 72, introduced-by-proof, role applied]
   4. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Unit`
      [def, depth 1, in-statement, role implicit-arg]
   6. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Std.ExtHashSet.inner`
      [def, depth 2, in-statement, role implicit-arg]
   8. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_017  (target depth 111, band 76-125)

THEOREM PROVED: `Matroid.eRk_compl_union_add_eRk_compl_inter_le`

Grade all 24 candidates below.

   1. `Union.union`
      [def, depth 1, in-statement, role explicit-arg]
   2. `Set.instUnion`
      [def, depth 5, in-statement, role instance-slot]
   3. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   4. `Matroid`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Inter.inter`
      [def, depth 1, in-statement, role explicit-arg]
   6. `Matroid.eRk_submod`
      [theorem, depth 110, introduced-by-proof, role explicit-arg]
   7. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   8. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Set.sdiff_inter_sdiff`
      [theorem, depth 57, in-statement, role explicit-arg]
  10. `Matroid.E`
      [def, depth 1, in-statement, role explicit-arg]
  11. `instAddENat`
      [def, depth 9, in-statement, role instance-slot]
  12. `Set`
      [def, depth 0, in-statement, role type-annotation]
  13. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  14. `ENat`
      [def, depth 2, in-statement, role implicit-arg]
  15. `Set.sdiff_inter`
      [theorem, depth 57, introduced-by-proof, role explicit-arg]
  16. `instLEENat`
      [def, depth 22, in-statement, role instance-slot]
  17. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `id`
      [def, depth 0, in-statement, role explicit-arg]
  19. `SDiff.sdiff`
      [def, depth 1, in-statement, role explicit-arg]
  20. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
  21. `Set.instSDiff`
      [def, depth 5, in-statement, role instance-slot]
  22. `Matroid.eRk`
      [def, depth 91, in-statement, role explicit-arg]
  23. `Set.instInter`
      [def, depth 5, in-statement, role instance-slot]
  24. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_018  (target depth 152, band 126+)

THEOREM PROVED: `ContinuousWithinAt.nnnorm`

Grade all 9 candidates below.

   1. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   2. `ContinuousWithinAt`
      [def, depth 49, in-statement, role type-annotation]
   3. `Set`
      [def, depth 0, in-statement, role type-annotation]
   4. `Filter.Tendsto.nnnorm`
      [theorem, depth 151, introduced-by-proof, role applied]
   5. `SeminormedAddGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   6. `SeminormedAddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `nhdsWithin`
      [def, depth 48, in-statement, role implicit-arg]
   8. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   9. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_019  (target depth 6, band 0-10)

THEOREM PROVED: `Prod.map_snd`

Grade all 4 candidates below.

   1. `Prod`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Prod.snd`
      [def, depth 1, in-statement, role implicit-arg]
   3. `Prod.map`
      [def, depth 5, in-statement, role explicit-arg]
   4. `rfl`
      [def, depth 2, introduced-by-proof, role applied]

### proof_020  (target depth 21, band 11-25)

THEOREM PROVED: `Int32.le_iff_toBitVec_sle`

Grade all 4 candidates below.

   1. `Iff.rfl`
      [theorem, depth 3, introduced-by-proof, role applied]
   2. `instLEInt32`
      [def, depth 20, in-statement, role instance-slot]
   3. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Int32`
      [inductive, depth 0, in-statement, role implicit-arg]
