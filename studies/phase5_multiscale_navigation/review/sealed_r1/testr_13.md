# Grading batch `testr_13` — 24 proofs

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

### proof_0289  (target depth 66, band 51-75)

THEOREM PROVED: `CategoryTheory.LocalizerMorphism.RightResolution.unopFunctor_obj`

Grade all 16 candidates.

   1. `CategoryTheory.LocalizerMorphism.LeftResolution`
      [inductive, depth 4, in-statement, role implicit-arg]
   2. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Opposite.unop`
      [def, depth 1, in-statement, role explicit-arg]
   4. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   5. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   7. `CategoryTheory.LocalizerMorphism.RightResolution.instCategory`
      [def, depth 15, in-statement, role instance-slot]
   8. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `CategoryTheory.MorphismProperty.op`
      [def, depth 5, in-statement, role implicit-arg]
  10. `CategoryTheory.LocalizerMorphism.LeftResolution.instCategory`
      [def, depth 15, in-statement, role instance-slot]
  11. `CategoryTheory.LocalizerMorphism.RightResolution.unopFunctor`
      [def, depth 65, in-statement, role explicit-arg]
  12. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  13. `CategoryTheory.LocalizerMorphism`
      [inductive, depth 3, in-statement, role type-annotation]
  14. `CategoryTheory.LocalizerMorphism.RightResolution`
      [inductive, depth 4, in-statement, role explicit-arg]
  15. `CategoryTheory.LocalizerMorphism.op`
      [def, depth 61, in-statement, role explicit-arg]
  16. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]

### proof_0290  (target depth 64, band 51-75)

THEOREM PROVED: `Nat.setGcd_dvd_of_mem_closure`

Grade all 21 candidates.

   1. `Nat.instAddMonoid`
      [def, depth 16, in-statement, role instance-slot]
   2. `Nat.setGcd`
      [def, depth 43, in-statement, role explicit-arg]
   3. `dvd_add`
      [theorem, depth 7, in-statement, role explicit-arg]
   4. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   5. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   6. `AddSubmonoid.closure`
      [def, depth 15, in-statement, role explicit-arg]
   7. `Nat.instSemigroup`
      [def, depth 19, introduced-by-proof, role instance-slot]
   8. `AddSubmonoid`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `Nat.setGcd_dvd_of_mem`
      [theorem, depth 52, introduced-by-proof, role explicit-arg]
  10. `Set`
      [def, depth 0, in-statement, role type-annotation]
  11. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  12. `AddSubmonoid.instSetLike`
      [def, depth 10, in-statement, role instance-slot]
  13. `Nat.instDistrib`
      [def, depth 17, introduced-by-proof, role instance-slot]
  14. `Nat.instSemigroupWithZero`
      [def, depth 20, introduced-by-proof, role instance-slot]
  15. `Dvd.dvd`
      [def, depth 1, in-statement, role implicit-arg]
  16. `AddSubmonoid.closure_induction`
      [theorem, depth 63, introduced-by-proof, role applied]
  17. `dvd_zero`
      [theorem, depth 6, in-statement, role explicit-arg]
  18. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
  19. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  20. `Nat.instDvd`
      [def, depth 10, in-statement, role instance-slot]
  21. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]

### proof_0291  (target depth 75, band 51-75)

THEOREM PROVED: `ContinuousMultilinearMap.ofSubsingleton_apply_toMultilinearMap`

Grade all 17 candidates.

   1. `Subsingleton`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   3. `ContinuousMultilinearMap.ofSubsingleton`
      [def, depth 74, in-statement, role explicit-arg]
   4. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `ContinuousMultilinearMap`
      [inductive, depth 2, in-statement, role implicit-arg]
   8. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  10. `MultilinearMap`
      [inductive, depth 2, in-statement, role implicit-arg]
  11. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  12. `ContinuousMultilinearMap.toMultilinearMap`
      [def, depth 3, in-statement, role explicit-arg]
  13. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  14. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
  15. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  17. `ContinuousLinearMap`
      [inductive, depth 11, in-statement, role type-annotation]

### proof_0292  (target depth 75, band 51-75)

THEOREM PROVED: `Std.DTreeMap.Raw.isEmpty_eq_size_eq_zero`

Grade all 6 candidates.

   1. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   2. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
   3. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   4. `Std.DTreeMap.Internal.Impl.isEmpty_eq_size_eq_zero`
      [theorem, depth 74, introduced-by-proof, role applied]
   5. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   6. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0293  (target depth 54, band 51-75)

THEOREM PROVED: `Finset.nonempty_coe_sort`

Grade all 5 candidates.

   1. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   2. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
   3. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   5. `nonempty_subtype`
      [theorem, depth 5, introduced-by-proof, role applied]

### proof_0294  (target depth 68, band 51-75)

THEOREM PROVED: `Std.HashMap.containsThenInsert_fst`

Grade all 5 candidates.

   1. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.DHashMap.containsThenInsert_fst`
      [theorem, depth 67, introduced-by-proof, role applied]
   3. `Std.HashMap.inner`
      [def, depth 2, in-statement, role implicit-arg]
   4. `Std.HashMap`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0295  (target depth 54, band 51-75)

THEOREM PROVED: `Subarray.forIn_toArray`

Grade all 12 candidates.

   1. `Id.instMonad`
      [def, depth 3, in-statement, role instance-slot]
   2. `SubarrayIterator`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `LawfulMonad`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.Slice.Internal.SubarrayData`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `ForInStep`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `instIteratorSubarrayIteratorId`
      [def, depth 50, in-statement, role instance-slot]
   7. `Std.Slice.forIn_toArray`
      [theorem, depth 52, introduced-by-proof, role applied]
   8. `Monad`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Subarray.instToIterator`
      [def, depth 4, in-statement, role instance-slot]
  10. `Id`
      [def, depth 0, in-statement, role explicit-arg]
  11. `Subarray`
      [def, depth 1, in-statement, role type-annotation]
  12. `instIteratorLoopSubarrayIteratorIdOfMonad`
      [def, depth 51, in-statement, role instance-slot]

### proof_0296  (target depth 68, band 51-75)

THEOREM PROVED: `Std.HashMap.Raw.getKeyD_insertIfNew`

Grade all 9 candidates.

   1. `Std.HashMap.Raw.inner`
      [def, depth 1, in-statement, role implicit-arg]
   2. `Std.HashMap.Raw.WF`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Std.DHashMap.Raw.getKeyD_insertIfNew`
      [theorem, depth 67, introduced-by-proof, role applied]
   6. `Std.HashMap.Raw`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.HashMap.Raw.WF.out`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   8. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0297  (target depth 61, band 51-75)

THEOREM PROVED: `CategoryTheory.ComposableArrows.threeδ₂Toδ₁_app_zero`

Grade all 22 candidates.

   1. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   2. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   4. `Fin.instPartialOrder`
      [def, depth 24, in-statement, role instance-slot]
   5. `CategoryTheory.ComposableArrows.threeδ₂Toδ₁`
      [def, depth 60, in-statement, role explicit-arg]
   6. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role implicit-arg]
   7. `Preorder.smallCategory`
      [def, depth 10, in-statement, role instance-slot]
   8. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   9. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  11. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  12. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
  13. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  14. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  15. `rfl`
      [def, depth 2, in-statement, role applied]
  16. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  18. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  19. `Fin`
      [inductive, depth 1, in-statement, role explicit-arg]
  20. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
  21. `Fin.instOfNat`
      [def, depth 24, in-statement, role instance-slot]
  22. `CategoryTheory.ComposableArrows.mk₂`
      [def, depth 58, in-statement, role explicit-arg]

### proof_0298  (target depth 68, band 51-75)

THEOREM PROVED: `Std.DHashMap.getKey_insert_self`

Grade all 19 candidates.

   1. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `_private.Std.Data.DHashMap.Basic.0.Std.DHashMap.insert._proof_1`
      [theorem, depth 66, in-statement, role explicit-arg]
   3. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.DHashMap.Raw`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Std.DHashMap.Internal.Raw₀.getKey_insert_self`
      [theorem, depth 67, introduced-by-proof, role applied]
   6. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.DHashMap.Raw.buckets`
      [def, depth 1, in-statement, role explicit-arg]
   8. `Std.DHashMap`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Subtype.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  10. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
  12. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
  13. `Std.DHashMap.wf`
      [theorem, depth 2, in-statement, role explicit-arg]
  14. `Std.DHashMap.Internal.AssocList`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `Std.DHashMap.inner`
      [def, depth 2, in-statement, role explicit-arg]
  16. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Array.size`
      [def, depth 10, in-statement, role explicit-arg]
  18. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  19. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0299  (target depth 71, band 51-75)

THEOREM PROVED: `instContinuousStarMulOpposite`

Grade all 14 candidates.

   1. `MulOpposite.op`
      [def, depth 2, in-statement, role implicit-arg]
   2. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `MulOpposite.unop`
      [def, depth 2, in-statement, role explicit-arg]
   4. `MulOpposite.instTopologicalSpaceMulOpposite`
      [def, depth 64, in-statement, role instance-slot]
   5. `Continuous.comp`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   6. `MulOpposite.instStar`
      [def, depth 3, in-statement, role instance-slot]
   7. `ContinuousStar.mk`
      [constructor, depth 2, introduced-by-proof, role applied]
   8. `MulOpposite`
      [def, depth 1, in-statement, role implicit-arg]
   9. `MulOpposite.continuous_unop`
      [theorem, depth 69, introduced-by-proof, role explicit-arg]
  10. `Star.star`
      [def, depth 1, in-statement, role implicit-arg]
  11. `MulOpposite.continuous_op`
      [theorem, depth 70, introduced-by-proof, role explicit-arg]
  12. `ContinuousStar`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `Star`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Continuous.star`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]

### proof_0300  (target depth 57, band 51-75)

THEOREM PROVED: `ValuationSubring.toLocalSubring_injective`

Grade all 14 candidates.

   1. `Field`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `ValuationSubring`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `id`
      [def, depth 0, in-statement, role explicit-arg]
   4. `ValuationSubring.toSubring`
      [def, depth 2, in-statement, role explicit-arg]
   5. `LocalSubring.toSubring`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   6. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `LocalSubring`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `ValuationSubring.toSubring_injective`
      [theorem, depth 48, introduced-by-proof, role applied]
   9. `NonAssocCommRing.toNonAssocRing`
      [def, depth 1, in-statement, role instance-slot]
  10. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `Field.toCommRing`
      [def, depth 1, in-statement, role instance-slot]
  12. `Subring`
      [inductive, depth 1, in-statement, role implicit-arg]
  13. `CommRing.toNonAssocCommRing`
      [def, depth 11, in-statement, role instance-slot]
  14. `ValuationSubring.toLocalSubring`
      [def, depth 56, in-statement, role explicit-arg]

### proof_0301  (target depth 64, band 51-75)

THEOREM PROVED: `CategoryTheory.Dial.leftUnitor_hom_F`

Grade all 24 candidates.

   1. `CategoryTheory.Limits.terminal`
      [def, depth 15, in-statement, role explicit-arg]
   2. `CategoryTheory.Dial.tensorObjImpl`
      [def, depth 62, in-statement, role implicit-arg]
   3. `CategoryTheory.Dial.tgt`
      [def, depth 3, in-statement, role explicit-arg]
   4. `CategoryTheory.Limits.prod.lift`
      [def, depth 24, in-statement, role implicit-arg]
   5. `CategoryTheory.Category.comp_id`
      [theorem, depth 1, in-statement, role explicit-arg]
   6. `CategoryTheory.Limits.prod.comp_lift`
      [theorem, depth 27, in-statement, role explicit-arg]
   7. `CategoryTheory.Limits.terminal.comp_from`
      [theorem, depth 29, in-statement, role explicit-arg]
   8. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role implicit-arg]
   9. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role explicit-arg]
  10. `CategoryTheory.Dial`
      [inductive, depth 2, in-statement, role type-annotation]
  11. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  12. `CategoryTheory.Limits.terminal.from`
      [def, depth 24, in-statement, role explicit-arg]
  13. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  15. `CategoryTheory.Dial.tensorUnitImpl`
      [def, depth 62, in-statement, role explicit-arg]
  16. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  17. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  18. `CategoryTheory.Limits.prod`
      [def, depth 15, in-statement, role explicit-arg]
  19. `CategoryTheory.Dial.src`
      [def, depth 3, in-statement, role explicit-arg]
  20. `CategoryTheory.Limits.prod.snd`
      [def, depth 23, in-statement, role explicit-arg]
  21. `Eq.trans`
      [theorem, depth 3, in-statement, role applied]
  22. `CategoryTheory.Limits.HasPullbacks`
      [def, depth 14, in-statement, role type-annotation]
  23. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  24. `CategoryTheory.Limits.HasFiniteProducts`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0302  (target depth 51, band 51-75)

THEOREM PROVED: `List.rotate'_length`

Grade all 25 candidates.

   1. `List.rotate'`
      [def, depth 9, in-statement, role explicit-arg]
   2. `List.rotate'_eq_drop_append_take`
      [theorem, depth 50, introduced-by-proof, role explicit-arg]
   3. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   4. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `List.take_length`
      [theorem, depth 17, introduced-by-proof, role explicit-arg]
   6. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `List.length`
      [def, depth 9, in-statement, role explicit-arg]
   8. `instHAppendOfAppend`
      [def, depth 3, in-statement, role instance-slot]
   9. `List.instAppend`
      [def, depth 7, in-statement, role instance-slot]
  10. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  11. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  12. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `le_rfl`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  15. `List.drop_length`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
  16. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  17. `Nat.instPreorder`
      [def, depth 20, introduced-by-proof, role instance-slot]
  18. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  19. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `List`
      [inductive, depth 0, in-statement, role type-annotation]
  21. `List.take`
      [def, depth 6, introduced-by-proof, role explicit-arg]
  22. `HAppend.hAppend`
      [def, depth 2, in-statement, role implicit-arg]
  23. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
  24. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  25. `List.drop`
      [def, depth 6, introduced-by-proof, role explicit-arg]

### proof_0303  (target depth 68, band 51-75)

THEOREM PROVED: `continuousWithinAt_const`

Grade all 4 candidates.

   1. `Continuous.continuousWithinAt`
      [theorem, depth 66, introduced-by-proof, role applied]
   2. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Set`
      [def, depth 0, in-statement, role type-annotation]
   4. `continuous_const`
      [theorem, depth 67, introduced-by-proof, role explicit-arg]

### proof_0304  (target depth 65, band 51-75)

THEOREM PROVED: `Finset.subset_powersetCard_univ_iff`

Grade all 22 candidates.

   1. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `forall_congr'`
      [theorem, depth 2, introduced-by-proof, role applied]
   4. `Finset.powersetCard`
      [def, depth 62, in-statement, role explicit-arg]
   5. `Iff.rfl`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `Finset.mem_powersetCard_univ`
      [theorem, depth 64, introduced-by-proof, role explicit-arg]
   7. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   8. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   9. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
  10. `Finset.mem_coe`
      [theorem, depth 54, introduced-by-proof, role explicit-arg]
  11. `Finset.univ`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `id`
      [def, depth 0, in-statement, role explicit-arg]
  14. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `SetLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  16. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  17. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
  19. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  20. `Finset.card`
      [def, depth 12, in-statement, role explicit-arg]
  21. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  22. `Iff`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0305  (target depth 66, band 51-75)

THEOREM PROVED: `BoolAlg.dualEquiv_inverse`

Grade all 6 candidates.

   1. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   2. `BoolAlg`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `CategoryTheory.Equivalence.inverse`
      [def, depth 2, in-statement, role explicit-arg]
   4. `BoolAlg.dualEquiv`
      [def, depth 65, in-statement, role explicit-arg]
   5. `BoolAlg.instCategory`
      [def, depth 56, in-statement, role instance-slot]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]

### proof_0306  (target depth 70, band 51-75)

THEOREM PROVED: `CategoryTheory.Comma.hasFiniteLimits`

Grade all 11 candidates.

   1. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.Limits.PreservesFiniteLimits`
      [inductive, depth 2, in-statement, role type-annotation]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `inferInstance`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Comma`
      [inductive, depth 2, in-statement, role explicit-arg]
   6. `CategoryTheory.commaCategory`
      [def, depth 12, in-statement, role instance-slot]
   7. `CategoryTheory.SmallCategory`
      [def, depth 1, introduced-by-proof, role type-annotation]
   8. `CategoryTheory.Limits.HasFiniteLimits.mk`
      [constructor, depth 3, introduced-by-proof, role applied]
   9. `CategoryTheory.FinCategory`
      [inductive, depth 2, introduced-by-proof, role type-annotation]
  10. `CategoryTheory.Limits.HasFiniteLimits`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `CategoryTheory.Limits.HasLimitsOfShape`
      [inductive, depth 1, introduced-by-proof, role implicit-arg]

### proof_0307  (target depth 69, band 51-75)

THEOREM PROVED: `List.countBefore_zero`

Grade all 4 candidates.

   1. `BEq.beq`
      [def, depth 1, in-statement, role implicit-arg]
   2. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `List.countPBefore_zero`
      [theorem, depth 68, introduced-by-proof, role applied]
   4. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0308  (target depth 75, band 51-75)

THEOREM PROVED: `Std.DTreeMap.Internal.Impl.minKey?_eq_none_iff`

Grade all 25 candidates.

   1. `Option.none`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Std.TransOrd`
      [def, depth 2, in-statement, role type-annotation]
   3. `List.isEmpty`
      [def, depth 5, introduced-by-proof, role explicit-arg]
   4. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   7. `Std.DTreeMap.Internal.Impl.isEmpty_eq_isEmpty`
      [theorem, depth 13, introduced-by-proof, role explicit-arg]
   8. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Std.DTreeMap.Internal.Impl.minKey?`
      [def, depth 36, in-statement, role explicit-arg]
  11. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  12. `Std.Internal.List.minKey?`
      [def, depth 34, introduced-by-proof, role explicit-arg]
  13. `Std.DTreeMap.Internal.Impl.WF.ordered`
      [theorem, depth 74, introduced-by-proof, role explicit-arg]
  14. `Std.DTreeMap.Internal.Impl.toListModel`
      [def, depth 9, introduced-by-proof, role explicit-arg]
  15. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
  16. `Sigma`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  17. `Ord`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  19. `id`
      [def, depth 0, in-statement, role explicit-arg]
  20. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  21. `Std.DTreeMap.Internal.Impl.WF`
      [inductive, depth 1, in-statement, role type-annotation]
  22. `Std.DTreeMap.Internal.Impl.minKey?_eq_minKey?`
      [theorem, depth 42, introduced-by-proof, role explicit-arg]
  23. `Std.DTreeMap.Internal.Impl.isEmpty`
      [def, depth 5, in-statement, role explicit-arg]
  24. `Std.DTreeMap.Internal.Impl`
      [inductive, depth 0, in-statement, role type-annotation]
  25. `Std.Internal.List.minKey?_eq_none_iff_isEmpty`
      [theorem, depth 36, introduced-by-proof, role explicit-arg]

### proof_0309  (target depth 65, band 51-75)

THEOREM PROVED: `vadd_uniformity`

Grade all 11 candidates.

   1. `UniformSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `IsAddUnit.vadd_uniformity`
      [theorem, depth 64, introduced-by-proof, role applied]
   3. `AddMonoid.toAddSemigroup`
      [def, depth 1, in-statement, role implicit-arg]
   4. `UniformContinuousConstVAdd`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `AddAction.toAddSemigroupAction`
      [def, depth 2, in-statement, role instance-slot]
   6. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `AddAction`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `SubNegMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
   9. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
  10. `AddGroup.isAddUnit`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
  11. `AddSemigroupAction.toVAdd`
      [def, depth 2, in-statement, role instance-slot]

### proof_0310  (target depth 70, band 51-75)

THEOREM PROVED: `Std.HashSet.Raw.get?_empty`

Grade all 4 candidates.

   1. `Unit`
      [def, depth 1, in-statement, role implicit-arg]
   2. `Std.HashMap.Raw.getKey?_empty`
      [theorem, depth 69, introduced-by-proof, role applied]
   3. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0311  (target depth 59, band 51-75)

THEOREM PROVED: `Finset.Ico_disjoint_Ico_consecutive`

Grade all 24 candidates.

   1. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   2. `Finset.instPartialOrder`
      [def, depth 54, in-statement, role instance-slot]
   3. `Finset.disjoint_left`
      [theorem, depth 58, introduced-by-proof, role explicit-arg]
   4. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   5. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
   6. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   7. `Not`
      [def, depth 1, in-statement, role type-annotation]
   8. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   9. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `And.left`
      [theorem, depth 1, in-statement, role explicit-arg]
  11. `And.right`
      [theorem, depth 1, in-statement, role explicit-arg]
  12. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  14. `LT.lt.not_ge`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  15. `Finset.mem_Ico`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  16. `LT.lt`
      [def, depth 1, in-statement, role explicit-arg]
  17. `Finset.instOrderBot`
      [def, depth 55, in-statement, role instance-slot]
  18. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
  19. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
  20. `Iff.mp`
      [theorem, depth 1, in-statement, role explicit-arg]
  21. `LocallyFiniteOrder`
      [inductive, depth 1, in-statement, role type-annotation]
  22. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
  23. `Disjoint`
      [def, depth 3, in-statement, role implicit-arg]
  24. `Finset.Ico`
      [def, depth 3, in-statement, role explicit-arg]

### proof_0312  (target depth 54, band 51-75)

THEOREM PROVED: `List.drop_take_self`

Grade all 21 candidates.

   1. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   3. `List.drop_take`
      [theorem, depth 53, introduced-by-proof, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   7. `List.take`
      [def, depth 6, in-statement, role explicit-arg]
   8. `Nat.sub_self`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]
   9. `List.drop`
      [def, depth 6, in-statement, role explicit-arg]
  10. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  11. `instSubNat`
      [def, depth 8, introduced-by-proof, role instance-slot]
  12. `HSub.hSub`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  15. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  16. `List`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
  18. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  19. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  20. `instHSub`
      [def, depth 3, introduced-by-proof, role instance-slot]
  21. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
