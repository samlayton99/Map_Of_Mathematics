# Grading batch `batch_03` -- 20 proofs

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

### proof_041  (target depth 98, band 76-125)

THEOREM PROVED: `String.Pos.copy_ofCopy`

Grade all 18 candidates below.

   1. `String.Pos`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `String.Pos.offset_ofCopy`
      [theorem, depth 97, introduced-by-proof, role explicit-arg]
   3. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   4. `String.Slice.copy`
      [def, depth 89, in-statement, role explicit-arg]
   5. `String.Pos.Raw`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `String.Pos.ofCopy`
      [def, depth 96, in-statement, role explicit-arg]
   7. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
   8. `String.Slice`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `String.Slice.Pos.copy`
      [def, depth 96, in-statement, role explicit-arg]
  12. `String.Slice.Pos.offset_copy`
      [theorem, depth 97, introduced-by-proof, role explicit-arg]
  13. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  14. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  15. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `String.Slice.Pos.offset`
      [def, depth 2, in-statement, role implicit-arg]
  17. `String.Pos.offset`
      [def, depth 2, in-statement, role explicit-arg]
  18. `String.Pos.ext`
      [theorem, depth 6, introduced-by-proof, role applied]

### proof_042  (target depth 152, band 126+)

THEOREM PROVED: `LinearIsometryEquiv.symm_symm`

Grade all 11 candidates below.

   1. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   3. `RingHomInvPair`
      [inductive, depth 11, in-statement, role type-annotation]
   4. `LinearIsometryEquiv.symm`
      [def, depth 151, in-statement, role explicit-arg]
   5. `SeminormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
   6. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   7. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `LinearIsometryEquiv`
      [inductive, depth 12, in-statement, role implicit-arg]
   9. `SeminormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `RingHom`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `rfl`
      [def, depth 2, in-statement, role applied]

### proof_043  (target depth 7, band 0-10)

THEOREM PROVED: `FunLike.addMonoid._proof_3`

Grade all 8 candidates below.

   1. `FunLike`
      [def, depth 2, in-statement, role type-annotation]
   2. `AddMonoid.toNSMul`
      [def, depth 1, in-statement, role instance-slot]
   3. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `NSMul.toSMul`
      [def, depth 2, in-statement, role instance-slot]
   5. `SMul`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `FunLike.coe_smul`
      [theorem, depth 6, introduced-by-proof, role applied]
   7. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `IsSMulApply`
      [inductive, depth 3, in-statement, role type-annotation]

### proof_044  (target depth 21, band 11-25)

THEOREM PROVED: `AddMonoidHom.mul_op_ext_iff`

Grade all 18 candidates below.

   1. `AddZeroClass`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `AddEquiv.toAddMonoidHom`
      [def, depth 19, in-statement, role explicit-arg]
   3. `AddMonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `AddMonoidHom.mul_op_ext`
      [theorem, depth 20, introduced-by-proof, role explicit-arg]
   5. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `MulOpposite.opAddEquiv`
      [def, depth 12, in-statement, role explicit-arg]
   8. `HEq`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
   9. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
  10. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `MulOpposite.instAddZeroClass`
      [def, depth 17, in-statement, role instance-slot]
  12. `MulOpposite`
      [def, depth 1, in-statement, role implicit-arg]
  13. `AddMonoidHom.comp`
      [def, depth 13, in-statement, role explicit-arg]
  14. `Eq.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  15. `HEq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
  16. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
  17. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  18. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]

### proof_045  (target depth 37, band 26-50)

THEOREM PROVED: `Representation.IntertwiningMap.comp_def`

Grade all 9 candidates below.

   1. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `rfl`
      [def, depth 2, in-statement, role applied]
   3. `Monoid`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Representation`
      [def, depth 31, in-statement, role type-annotation]
   5. `Representation.IntertwiningMap.comp`
      [def, depth 36, in-statement, role implicit-arg]
   6. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   8. `Representation.IntertwiningMap`
      [inductive, depth 32, in-statement, role type-annotation]
   9. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_046  (target depth 62, band 51-75)

THEOREM PROVED: `IsPreconnected.union'`

Grade all 13 candidates below.

   1. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Exists.casesOn`
      [def, depth 3, introduced-by-proof, role applied]
   3. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   4. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   5. `Set.instUnion`
      [def, depth 5, in-statement, role instance-slot]
   6. `And.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   7. `Union.union`
      [def, depth 1, in-statement, role explicit-arg]
   8. `IsPreconnected`
      [def, depth 6, in-statement, role implicit-arg]
   9. `Set.instInter`
      [def, depth 5, in-statement, role instance-slot]
  10. `Inter.inter`
      [def, depth 1, in-statement, role explicit-arg]
  11. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  12. `IsPreconnected.union`
      [theorem, depth 61, introduced-by-proof, role explicit-arg]
  13. `Set.Nonempty`
      [def, depth 4, in-statement, role type-annotation]

### proof_047  (target depth 80, band 76-125)

THEOREM PROVED: `CoalgCat.tensorObj_instCoalgebra`

Grade all 18 candidates below.

   1. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `ModuleCat.isModule`
      [def, depth 2, in-statement, role instance-slot]
   3. `Coalgebra`
      [inductive, depth 2, in-statement, role implicit-arg]
   4. `CoalgCat.instCoalgebra`
      [def, depth 2, in-statement, role explicit-arg]
   5. `CoalgCat.toModuleCat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `TensorProduct`
      [def, depth 39, in-statement, role explicit-arg]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   8. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
   9. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
  10. `CoalgCat.instMonoidalCategoryStruct`
      [def, depth 79, in-statement, role instance-slot]
  11. `ModuleCat.isAddCommGroup`
      [def, depth 2, in-statement, role instance-slot]
  12. `CommRing.toRing`
      [def, depth 1, in-statement, role instance-slot]
  13. `CoalgCat.category`
      [def, depth 66, in-statement, role implicit-arg]
  14. `TensorProduct.instModule`
      [def, depth 53, in-statement, role instance-slot]
  15. `CategoryTheory.MonoidalCategoryStruct.tensorObj`
      [def, depth 2, in-statement, role explicit-arg]
  16. `ModuleCat.carrier`
      [def, depth 2, in-statement, role explicit-arg]
  17. `CoalgCat`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `TensorProduct.addCommGroup`
      [def, depth 60, in-statement, role instance-slot]

### proof_048  (target depth 194, band 126+)

THEOREM PROVED: `MeasureTheory.MeasurePreserving.map_of_comp`

Grade all 10 candidates below.

   1. `MeasureTheory.MeasurePreserving.map_eq`
      [theorem, depth 10, introduced-by-proof, role explicit-arg]
   2. `MeasureTheory.MeasurePreserving.mk`
      [constructor, depth 189, introduced-by-proof, role applied]
   3. `MeasureTheory.Measure.map`
      [def, depth 188, in-statement, role implicit-arg]
   4. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
   5. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `MeasureTheory.MeasurePreserving`
      [inductive, depth 9, in-statement, role type-annotation]
   8. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Measurable`
      [def, depth 5, in-statement, role type-annotation]
  10. `MeasureTheory.Measure.map_map`
      [theorem, depth 193, introduced-by-proof, role explicit-arg]

### proof_049  (target depth 7, band 0-10)

THEOREM PROVED: `AddMonoidHom.map_exists_left_neg`

Grade all 15 candidates below.

   1. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   2. `AddZero`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   5. `map_add_eq_zero`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   6. `AddMonoidHomClass`
      [inductive, depth 3, in-statement, role type-annotation]
   7. `AddZero.toZero`
      [def, depth 1, in-statement, role instance-slot]
   8. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   9. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  10. `Exists`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  12. `FunLike`
      [def, depth 2, in-statement, role type-annotation]
  13. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  14. `_private.Mathlib.Algebra.Group.Hom.Defs.0.AddMonoidHom.map_exists_left_neg.match_1_1`
      [def, depth 4, introduced-by-proof, role applied]
  15. `Exists.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]

### proof_050  (target depth 18, band 11-25)

THEOREM PROVED: `Equiv.sigmaProdDistrib_apply`

Grade all 8 candidates below.

   1. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   2. `Sigma`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   5. `Equiv.sigmaProdDistrib`
      [def, depth 17, in-statement, role explicit-arg]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   7. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]

### proof_051  (target depth 50, band 26-50)

THEOREM PROVED: `Lean.Grind.ToInt.add_congr.wl`

Grade all 22 candidates below.

   1. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `Lean.Grind.IntInterval.nonEmpty`
      [def, depth 18, introduced-by-proof, role explicit-arg]
   3. `Lean.Grind.IntInterval`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role let-value]
   5. `Lean.Grind.ToInt.toInt`
      [def, depth 2, in-statement, role explicit-arg]
   6. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   7. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `_private.Init.Grind.ToIntLemmas.0.Lean.Grind.ToInt.isNonempty`
      [theorem, depth 47, introduced-by-proof, role let-value]
  10. `Lean.Grind.ToInt`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Add`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Lean.Grind.ToInt.Add`
      [inductive, depth 2, in-statement, role type-annotation]
  13. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `Lean.Grind.IntInterval.isFinite`
      [def, depth 5, in-statement, role explicit-arg]
  15. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
  16. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  17. `Lean.Grind.ToInt.toInt_mem`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  18. `Lean.Grind.ToInt.add_congr.ww`
      [theorem, depth 48, introduced-by-proof, role applied]
  19. `Membership.mem`
      [def, depth 2, introduced-by-proof, role implicit-arg]
  20. `Lean.Grind.IntInterval.wrap`
      [def, depth 23, in-statement, role explicit-arg]
  21. `Lean.Grind.IntInterval.instMembershipInt`
      [def, depth 19, introduced-by-proof, role instance-slot]
  22. `Lean.Grind.IntInterval.wrap_eq_self_iff`
      [theorem, depth 49, introduced-by-proof, role explicit-arg]

### proof_052  (target depth 53, band 51-75)

THEOREM PROVED: `instLawfulCommIdentityISizeHXorOfNat`

Grade all 10 candidates below.

   1. `instHXorOfXorOp`
      [def, depth 3, in-statement, role instance-slot]
   2. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `Std.LawfulCommIdentity.mk`
      [constructor, depth 2, introduced-by-proof, role applied]
   4. `ISize.xor_zero`
      [theorem, depth 51, introduced-by-proof, role explicit-arg]
   5. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Std.Commutative.comm`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   7. `instXorOpISize`
      [def, depth 35, in-statement, role instance-slot]
   8. `ISize.instOfNat`
      [def, depth 25, in-statement, role instance-slot]
   9. `ISize`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `HXor.hXor`
      [def, depth 2, in-statement, role implicit-arg]

### proof_053  (target depth 76, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Internal.Impl.Equiv.getEntryGE!_eq`

Grade all 19 candidates below.

   1. `Sigma`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `Std.TransOrd`
      [def, depth 2, in-statement, role type-annotation]
   3. `Option.get!`
      [def, depth 34, in-statement, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   7. `Std.DTreeMap.Internal.Impl.Equiv`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Std.DTreeMap.Internal.Impl.WF`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Std.DTreeMap.Internal.Impl.getEntryGE?`
      [def, depth 7, in-statement, role implicit-arg]
  10. `Std.DTreeMap.Internal.Impl.Equiv.getEntryGE?_eq`
      [theorem, depth 75, introduced-by-proof, role explicit-arg]
  11. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  14. `Std.DTreeMap.Internal.Impl`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `Ord`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  17. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
  19. `Std.DTreeMap.Internal.Impl.getEntryGE!`
      [def, depth 35, in-statement, role explicit-arg]

### proof_054  (target depth 135, band 126+)

THEOREM PROVED: `Complex.isBigO_im_sub_im`

Grade all 19 candidates below.

   1. `Complex.instSub`
      [def, depth 91, in-statement, role instance-slot]
   2. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
   3. `Complex.im`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Complex`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `HSub.hSub`
      [def, depth 2, in-statement, role implicit-arg]
   6. `NormedCommRing.toSeminormedCommRing`
      [def, depth 96, in-statement, role instance-slot]
   7. `SeminormedCommRing.toSeminormedRing`
      [def, depth 1, in-statement, role instance-slot]
   8. `Complex.instNormedField`
      [def, depth 134, in-statement, role instance-slot]
   9. `Complex.instNorm`
      [def, depth 124, in-statement, role instance-slot]
  10. `Real.instSub`
      [def, depth 90, in-statement, role instance-slot]
  11. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `NormedField.toNormedCommRing`
      [def, depth 103, in-statement, role instance-slot]
  13. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
  14. `Complex.abs_im_le_norm`
      [theorem, depth 130, introduced-by-proof, role explicit-arg]
  15. `instHSub`
      [def, depth 3, in-statement, role instance-slot]
  16. `Asymptotics.isBigO_of_le`
      [theorem, depth 105, introduced-by-proof, role applied]
  17. `nhds`
      [def, depth 18, in-statement, role explicit-arg]
  18. `Real.norm`
      [def, depth 105, in-statement, role instance-slot]
  19. `SeminormedRing.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]

### proof_055  (target depth 6, band 0-10)

THEOREM PROVED: `Set.Icc_subset_Icc_iff`

Grade all 16 candidates below.

   1. `Set.Icc`
      [def, depth 2, in-statement, role explicit-arg]
   2. `And.right`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   3. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]
   4. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   5. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
   6. `And.left`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   7. `_private.Mathlib.Order.Interval.Set.Basic.0.Set.Icc_subset_Icc_iff.match_1_1`
      [def, depth 4, introduced-by-proof, role explicit-arg]
   8. `And`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `LE.le.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  10. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  11. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  13. `And.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  14. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
  15. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  16. `le_rfl`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]

### proof_056  (target depth 16, band 11-25)

THEOREM PROVED: `NonUnitalRingHom.id_comp`

Grade all 8 candidates below.

   1. `NonUnitalRingHom.instFunLike`
      [def, depth 10, introduced-by-proof, role instance-slot]
   2. `NonUnitalRingHom.ext`
      [theorem, depth 11, introduced-by-proof, role applied]
   3. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
   4. `NonUnitalRingHom.id`
      [def, depth 7, in-statement, role explicit-arg]
   5. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   6. `NonUnitalRingHom.comp`
      [def, depth 15, in-statement, role explicit-arg]
   7. `NonUnitalNonAssocSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `NonUnitalRingHom`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_057  (target depth 28, band 26-50)

THEOREM PROVED: `Mathlib.Tactic.ENatToNat.coe_zero`

Grade all 8 candidates below.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `instMulZeroClassOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
   3. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
   4. `ENat`
      [def, depth 2, in-statement, role implicit-arg]
   5. `instCommSemiringENat`
      [def, depth 27, in-statement, role instance-slot]
   6. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   7. `OfNat.ofNat`
      [def, depth 2, in-statement, role implicit-arg]
   8. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]

### proof_058  (target depth 62, band 51-75)

THEOREM PROVED: `TwoSidedIdeal.matrix_monotone`

Grade all 13 candidates below.

   1. `TwoSidedIdeal.instPartialOrder`
      [def, depth 41, in-statement, role instance-slot]
   2. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `TwoSidedIdeal.matrix`
      [def, depth 61, in-statement, role explicit-arg]
   4. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   5. `TwoSidedIdeal`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `NonUnitalNonAssocRing`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Matrix.nonUnitalNonAssocRing`
      [def, depth 60, in-statement, role instance-slot]
   8. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   9. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  10. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  11. `Matrix`
      [def, depth 0, in-statement, role explicit-arg]
  12. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  13. `TwoSidedIdeal.setLike`
      [def, depth 40, in-statement, role instance-slot]

### proof_059  (target depth 101, band 76-125)

THEOREM PROVED: `SimpleGraph.Walk.IsTrail.not_mem_edges_of_not_isEdgeReachable_two`

Grade all 14 candidates below.

   1. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   2. `Not`
      [def, depth 1, in-statement, role type-annotation]
   3. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   4. `List.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   5. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `SimpleGraph.Walk`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `SimpleGraph.Walk.support`
      [def, depth 7, in-statement, role explicit-arg]
   8. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `mt`
      [theorem, depth 2, in-statement, role applied]
  10. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  12. `_private.Mathlib.Combinatorics.SimpleGraph.Connectivity.EdgeConnectivity.0.SimpleGraph.Walk.IsTrail.isEdgeReachable_two_of_isEdgeReachable_two_aux`
      [theorem, depth 100, introduced-by-proof, role explicit-arg]
  13. `SimpleGraph.IsEdgeReachable`
      [def, depth 90, in-statement, role explicit-arg]
  14. `SimpleGraph.Walk.IsTrail`
      [inductive, depth 2, in-statement, role type-annotation]

### proof_060  (target depth 175, band 126+)

THEOREM PROVED: `Set.EqOn.iteratedDeriv_of_isOpen`

Grade all 25 candidates below.

   1. `SeminormedRing.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   2. `id`
      [def, depth 0, in-statement, role explicit-arg]
   3. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   5. `IsOpen.mem_nhds`
      [theorem, depth 59, in-statement, role explicit-arg]
   6. `IsOpen`
      [def, depth 2, in-statement, role type-annotation]
   7. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Filter.EventuallyEq.iteratedDeriv_eq`
      [theorem, depth 174, introduced-by-proof, role applied]
   9. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  10. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  11. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  12. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `SeminormedCommRing.toSeminormedRing`
      [def, depth 1, in-statement, role instance-slot]
  14. `NormedField.toNormedCommRing`
      [def, depth 103, in-statement, role instance-slot]
  15. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
  16. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  17. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  18. `Set.ofPred`
      [def, depth 1, in-statement, role explicit-arg]
  19. `Filter.mp_mem`
      [theorem, depth 7, in-statement, role explicit-arg]
  20. `Set.EqOn`
      [def, depth 4, in-statement, role type-annotation]
  21. `nhds`
      [def, depth 18, in-statement, role implicit-arg]
  22. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  23. `NormedCommRing.toSeminormedCommRing`
      [def, depth 96, in-statement, role instance-slot]
  24. `Filter.univ_mem'`
      [theorem, depth 7, in-statement, role explicit-arg]
  25. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
