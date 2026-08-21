# Grading batch `testc_19` — 24 proofs

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

### proof_0433  (target depth 40, band 26-50)

THEOREM PROVED: `RBTree.RBNode.Ordered.ins`

Grade all 6 candidates.

   1. `RBTree.RBNode.brecOn`
      [def, depth 5, in-statement, role applied]
   2. `RBTree.RBNode.ins`
      [def, depth 33, in-statement, role explicit-arg]
   3. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `RBTree.RBNode.Ordered.ins._f`
      [def, depth 39, introduced-by-proof, role explicit-arg]
   5. `RBTree.RBNode`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `RBTree.RBNode.Ordered`
      [def, depth 8, in-statement, role type-annotation]

### proof_0434  (target depth 165, band 126+)

THEOREM PROVED: `Tactic.ComputeAsymptotics.WellFormedBasis.of_append_right`

Grade all 12 candidates.

   1. `List.Sublist`
      [inductive, depth 1, in-statement, role implicit-arg]
   2. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
   3. `List.sublist_append_of_sublist_right._simp_1`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
   4. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `HAppend.hAppend`
      [def, depth 2, in-statement, role explicit-arg]
   6. `List.instAppend`
      [def, depth 7, in-statement, role instance-slot]
   7. `instHAppendOfAppend`
      [def, depth 3, in-statement, role instance-slot]
   8. `List.Sublist.refl._simp_1`
      [theorem, depth 7, in-statement, role explicit-arg]
   9. `Real`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Tactic.ComputeAsymptotics.WellFormedBasis.of_sublist`
      [theorem, depth 164, introduced-by-proof, role applied]
  11. `Tactic.ComputeAsymptotics.Basis`
      [def, depth 1, in-statement, role implicit-arg]
  12. `Tactic.ComputeAsymptotics.WellFormedBasis`
      [def, depth 163, in-statement, role type-annotation]

### proof_0435  (target depth 29, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.hasPushout_of_epi_comp`

Grade all 22 candidates.

   1. `CategoryTheory.Limits.pushout.inl`
      [def, depth 23, introduced-by-proof, role explicit-arg]
   2. `CategoryTheory.Epi`
      [inductive, depth 2, in-statement, role type-annotation]
   3. `CategoryTheory.Limits.HasPushout`
      [def, depth 17, in-statement, role type-annotation]
   4. `CategoryTheory.Limits.pushoutIsPushoutOfEpiComp`
      [def, depth 28, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Limits.ColimitCocone`
      [inductive, depth 2, introduced-by-proof, role implicit-arg]
   6. `CategoryTheory.Limits.HasColimit.mk'`
      [constructor, depth 3, introduced-by-proof, role applied]
   7. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `CategoryTheory.Limits.pushout`
      [def, depth 18, introduced-by-proof, role explicit-arg]
   9. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  10. `CategoryTheory.Limits.pushoutIsPushoutOfEpiComp._proof_1`
      [theorem, depth 25, introduced-by-proof, role let-value]
  11. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  12. `CategoryTheory.Limits.pushout.inr`
      [def, depth 23, introduced-by-proof, role explicit-arg]
  13. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
  14. `CategoryTheory.Limits.ColimitCocone.mk`
      [constructor, depth 4, introduced-by-proof, role explicit-arg]
  15. `CategoryTheory.Limits.PushoutCocone.mk`
      [def, depth 23, introduced-by-proof, role explicit-arg]
  16. `CategoryTheory.Limits.WidePushoutShape.category`
      [def, depth 13, in-statement, role instance-slot]
  17. `CategoryTheory.Limits.span`
      [def, depth 16, in-statement, role explicit-arg]
  18. `Nonempty.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  19. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  20. `CategoryTheory.Limits.WalkingSpan`
      [def, depth 2, in-statement, role implicit-arg]
  21. `CategoryTheory.Limits.WalkingPair`
      [inductive, depth 0, in-statement, role implicit-arg]
  22. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0436  (target depth 67, band 51-75)

THEOREM PROVED: `semicontinuous_iff_isOpen`

Grade all 15 candidates.

   1. `Filter.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   2. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
   3. `IsOpen.mem_nhds`
      [theorem, depth 59, introduced-by-proof, role explicit-arg]
   4. `IsOpen`
      [def, depth 2, in-statement, role explicit-arg]
   5. `Filter`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   8. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
   9. `Set.ofPred`
      [def, depth 1, in-statement, role explicit-arg]
  10. `Semicontinuous`
      [def, depth 20, in-statement, role implicit-arg]
  11. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  12. `_private.Mathlib.Topology.Semicontinuity.Defs.0.semicontinuous_iff_isOpen._simp_1_1`
      [theorem, depth 66, introduced-by-proof, role explicit-arg]
  13. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `id`
      [def, depth 0, in-statement, role explicit-arg]
  15. `nhds`
      [def, depth 18, in-statement, role explicit-arg]

### proof_0437  (target depth 27, band 26-50)

THEOREM PROVED: `UInt16.toBitVec64_toUSize`

Grade all 21 candidates.

   1. `System.Platform.numBits`
      [def, depth 6, in-statement, role explicit-arg]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role implicit-arg]
   3. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `UInt16.toUSize`
      [def, depth 19, in-statement, role explicit-arg]
   5. `id`
      [def, depth 0, in-statement, role explicit-arg]
   6. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `UInt16`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  10. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `UInt16.toBitVec`
      [def, depth 1, in-statement, role explicit-arg]
  12. `Eq.rec`
      [recursor, depth 2, in-statement, role explicit-arg]
  13. `USize.toBitVec`
      [def, depth 1, in-statement, role explicit-arg]
  14. `BitVec.cast`
      [def, depth 14, in-statement, role explicit-arg]
  15. `UInt16.toBitVec_toUSize`
      [theorem, depth 26, introduced-by-proof, role explicit-arg]
  16. `USize.toBitVec64`
      [def, depth 15, in-statement, role explicit-arg]
  17. `BitVec.cast.congr_simp`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
  18. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
  19. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  21. `BitVec.setWidth`
      [def, depth 24, in-statement, role explicit-arg]

### proof_0438  (target depth 11, band 11-25)

THEOREM PROVED: `Nat.not_add_one_le_zero`

Grade all 10 candidates.

   1. `instLENat`
      [def, depth 2, in-statement, role instance-slot]
   2. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `_private.Init.Data.Nat.Basic.0.Nat.not_add_one_le_zero.match_1_1`
      [def, depth 10, introduced-by-proof, role applied]
   4. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   5. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   8. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   9. `False`
      [inductive, depth 0, in-statement, role explicit-arg]
  10. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]

### proof_0439  (target depth 66, band 51-75)

THEOREM PROVED: `SimpleGraph.Walk.adj_penultimate`

Grade all 5 candidates.

   1. `SimpleGraph.Walk.Nil`
      [inductive, depth 2, in-statement, role explicit-arg]
   2. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `_private.Mathlib.Combinatorics.SimpleGraph.Walk.Traversal.0.SimpleGraph.Walk.adj_penultimate._proof_1_1`
      [theorem, depth 65, introduced-by-proof, role applied]
   4. `SimpleGraph.Walk`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Not`
      [def, depth 1, in-statement, role type-annotation]

### proof_0440  (target depth 7, band 0-10)

THEOREM PROVED: `Std.IterM.forIn_congr`

Grade all 22 candidates.

   1. `Std.Iterator`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   4. `HEq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
   5. `Std.IterM`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Std.IteratorLoop`
      [inductive, depth 2, in-statement, role type-annotation]
   7. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
   8. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   9. `_private.Init.Data.Iterators.Lemmas.Consumers.Monadic.Loop.0.Std.IterM.forIn_congr._simp_1_1`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
  10. `MonadLiftT`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  12. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  13. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  14. `HEq`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
  15. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  16. `Std.IterM.instForInOfIteratorLoop`
      [def, depth 6, in-statement, role instance-slot]
  17. `Eq.casesOn`
      [def, depth 3, introduced-by-proof, role applied]
  18. `ForInStep`
      [inductive, depth 0, in-statement, role type-annotation]
  19. `ForIn.forIn`
      [def, depth 2, in-statement, role explicit-arg]
  20. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  21. `Monad`
      [inductive, depth 0, in-statement, role type-annotation]
  22. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]

### proof_0441  (target depth 67, band 51-75)

THEOREM PROVED: `Std.DHashMap.get!_eq_getD_default`

Grade all 19 candidates.

   1. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.DHashMap.Internal.AssocList`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Std.DHashMap.inner`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Std.DHashMap.Internal.Raw₀.get!_eq_getD_default`
      [theorem, depth 66, introduced-by-proof, role applied]
   5. `Array.size`
      [def, depth 10, in-statement, role explicit-arg]
   6. `Subtype.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `_private.Std.Data.DHashMap.Basic.0.Std.DHashMap.insert._proof_1`
      [theorem, depth 66, in-statement, role explicit-arg]
   8. `Std.DHashMap.wf`
      [theorem, depth 2, in-statement, role explicit-arg]
   9. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
  10. `Std.DHashMap.Raw.buckets`
      [def, depth 1, in-statement, role explicit-arg]
  11. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  13. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  16. `Std.DHashMap`
      [inductive, depth 1, in-statement, role type-annotation]
  17. `LawfulBEq`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
  19. `Std.DHashMap.Raw`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0442  (target depth 55, band 51-75)

THEOREM PROVED: `UInt8.not_eq_comm`

Grade all 21 candidates.

   1. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   2. `_private.Init.Data.UInt.Bitwise.0.UInt8.not_eq_comm._simp_1_2`
      [theorem, depth 54, introduced-by-proof, role explicit-arg]
   3. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `UInt8.toBitVec_not`
      [theorem, depth 38, introduced-by-proof, role explicit-arg]
   5. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   6. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   7. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   8. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `UInt8`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `UInt8.toBitVec`
      [def, depth 1, in-statement, role explicit-arg]
  13. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
  14. `Complement.complement`
      [def, depth 1, in-statement, role explicit-arg]
  15. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `BitVec.instComplement`
      [def, depth 35, in-statement, role instance-slot]
  18. `_private.Init.Data.UInt.Bitwise.0.UInt8.not_eq_comm._simp_1_1`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
  19. `instComplementUInt8`
      [def, depth 37, in-statement, role instance-slot]
  20. `iff_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  21. `True`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0443  (target depth 64, band 51-75)

THEOREM PROVED: `CategoryTheory.Abelian.SpectralObject.sc₁_X₂`

Grade all 21 candidates.

   1. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   2. `instOfNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `CategoryTheory.Abelian.SpectralObject.sc₁._auto_1`
      [def, depth 8, in-statement, role explicit-arg]
   4. `CategoryTheory.Abelian`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `autoParam`
      [def, depth 1, in-statement, role type-annotation]
   6. `CategoryTheory.Abelian.SpectralObject`
      [inductive, depth 2, in-statement, role type-annotation]
   7. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   9. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  10. `CategoryTheory.ShortComplex.X₂`
      [def, depth 3, in-statement, role explicit-arg]
  11. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  12. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`
      [def, depth 17, in-statement, role instance-slot]
  13. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  14. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  15. `CategoryTheory.Abelian.toPreadditive`
      [def, depth 2, in-statement, role instance-slot]
  16. `CategoryTheory.Abelian.SpectralObject.sc₁`
      [def, depth 63, in-statement, role explicit-arg]
  17. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  18. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
  19. `Int.instAdd`
      [def, depth 11, in-statement, role instance-slot]
  20. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  21. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0444  (target depth 113, band 76-125)

THEOREM PROVED: `nndist_eq_zero`

Grade all 20 candidates.

   1. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `MetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `MetricSpace.toPseudoMetricSpace`
      [def, depth 1, in-statement, role instance-slot]
   4. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   7. `NNReal.instZero`
      [def, depth 103, in-statement, role instance-slot]
   8. `iff_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   9. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  10. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `PseudoMetricSpace.toNNDist`
      [def, depth 112, in-statement, role instance-slot]
  12. `NNReal.toReal`
      [def, depth 95, introduced-by-proof, role explicit-arg]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `_private.Mathlib.Topology.MetricSpace.Defs.0.nndist_eq_zero._simp_1_1`
      [theorem, depth 98, introduced-by-proof, role explicit-arg]
  15. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
  17. `NNReal`
      [def, depth 95, in-statement, role implicit-arg]
  18. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  19. `dist_eq_zero._simp_1`
      [theorem, depth 87, introduced-by-proof, role explicit-arg]
  20. `NNDist.nndist`
      [def, depth 1, in-statement, role explicit-arg]

### proof_0445  (target depth 34, band 26-50)

THEOREM PROVED: `Int8.lt_of_lt_of_le`

Grade all 16 candidates.

   1. `implies_congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   2. `Int.instLTInt`
      [def, depth 17, in-statement, role instance-slot]
   3. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `instLEInt8`
      [def, depth 20, in-statement, role instance-slot]
   5. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   7. `Int.instLEInt`
      [def, depth 15, in-statement, role instance-slot]
   8. `Int8`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  10. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  11. `Int.lt_of_lt_of_le`
      [theorem, depth 33, introduced-by-proof, role explicit-arg]
  12. `instLTInt8`
      [def, depth 20, in-statement, role instance-slot]
  13. `Int8.toInt`
      [def, depth 18, introduced-by-proof, role explicit-arg]
  14. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
  15. `_private.Init.Data.SInt.Lemmas.0.Int8.lt_of_lt_of_le._simp_1_2`
      [theorem, depth 21, introduced-by-proof, role explicit-arg]
  16. `_private.Init.Data.SInt.Lemmas.0.Int8.lt_of_lt_of_le._simp_1_1`
      [theorem, depth 21, introduced-by-proof, role explicit-arg]

### proof_0446  (target depth 12, band 11-25)

THEOREM PROVED: `SimpleGraph.Subgraph.deleteVerts_adj`

Grade all 24 candidates.

   1. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   2. `SimpleGraph.Subgraph.induce_adj`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
   3. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   4. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Set.instSDiff`
      [def, depth 5, in-statement, role instance-slot]
   6. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   8. `SimpleGraph.Subgraph.Adj`
      [def, depth 2, in-statement, role implicit-arg]
   9. `Set.mem_sdiff._simp_1`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  10. `_private.Mathlib.Combinatorics.SimpleGraph.Subgraph.0.SimpleGraph.Subgraph.deleteVerts_adj._simp_1_1`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
  11. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
  12. `iff_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  13. `Not`
      [def, depth 1, in-statement, role explicit-arg]
  14. `SimpleGraph.Subgraph`
      [inductive, depth 1, in-statement, role type-annotation]
  15. `SDiff.sdiff`
      [def, depth 1, in-statement, role explicit-arg]
  16. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `SimpleGraph.Subgraph.verts`
      [def, depth 2, in-statement, role explicit-arg]
  18. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  19. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  20. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
  21. `SimpleGraph.Subgraph.induce`
      [def, depth 10, in-statement, role explicit-arg]
  22. `SimpleGraph.Subgraph.deleteVerts`
      [def, depth 11, in-statement, role explicit-arg]
  23. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
  24. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0447  (target depth 52, band 51-75)

THEOREM PROVED: `List.drop_eq_drop_min`

Grade all 18 candidates.

   1. `List.drop_eq_drop_iff._simp_1`
      [theorem, depth 51, introduced-by-proof, role explicit-arg]
   2. `instLENat`
      [def, depth 2, in-statement, role implicit-arg]
   3. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `instMinNat`
      [def, depth 16, in-statement, role instance-slot]
   6. `Std.le_refl._simp_1`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   7. `Nat.min_assoc`
      [theorem, depth 21, introduced-by-proof, role explicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
  12. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  13. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  14. `List.length`
      [def, depth 9, in-statement, role explicit-arg]
  15. `List.drop`
      [def, depth 6, in-statement, role explicit-arg]
  16. `Min.min`
      [def, depth 1, in-statement, role explicit-arg]
  17. `Nat.min_eq_left`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
  18. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0448  (target depth 56, band 51-75)

THEOREM PROVED: `USize.not_ne_self`

Grade all 25 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `BitVec.not_self_ne._simp_1`
      [theorem, depth 55, introduced-by-proof, role explicit-arg]
   3. `System.Platform.numBits_pos._simp_1`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]
   4. `False`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   7. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   8. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   9. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
  10. `Complement.complement`
      [def, depth 1, in-statement, role explicit-arg]
  11. `USize`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `USize.toBitVec`
      [def, depth 1, in-statement, role explicit-arg]
  13. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `BitVec.instComplement`
      [def, depth 35, in-statement, role instance-slot]
  16. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
  17. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
  18. `USize.toBitVec_not`
      [theorem, depth 38, introduced-by-proof, role explicit-arg]
  19. `_private.Init.Data.UInt.Bitwise.0.USize.not_ne_self._simp_1_1`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]
  20. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  21. `Not`
      [def, depth 1, in-statement, role implicit-arg]
  22. `System.Platform.numBits`
      [def, depth 6, in-statement, role explicit-arg]
  23. `not_false_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
  24. `instComplementUSize`
      [def, depth 37, in-statement, role instance-slot]
  25. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0449  (target depth 106, band 76-125)

THEOREM PROVED: `enorm_le_coe`

Grade all 20 candidates.

   1. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
   2. `NNNorm`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `iff_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   4. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   5. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
   6. `NNReal.instPartialOrder`
      [def, depth 102, in-statement, role instance-slot]
   7. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   8. `ENNReal.ofNNReal`
      [def, depth 96, in-statement, role explicit-arg]
   9. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  11. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  12. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `NNNorm.toENorm`
      [def, depth 98, in-statement, role instance-slot]
  14. `ENorm.enorm`
      [def, depth 1, in-statement, role explicit-arg]
  15. `ENNReal.coe_le_coe._simp_1`
      [theorem, depth 105, introduced-by-proof, role explicit-arg]
  16. `NNReal`
      [def, depth 95, in-statement, role implicit-arg]
  17. `NNNorm.nnnorm`
      [def, depth 1, in-statement, role explicit-arg]
  18. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
  19. `ENNReal.instLE`
      [def, depth 104, in-statement, role instance-slot]
  20. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0450  (target depth 67, band 51-75)

THEOREM PROVED: `Std.DHashMap.getD_eq_fallback_of_contains_eq_false`

Grade all 18 candidates.

   1. `Std.DHashMap.Raw`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Std.DHashMap.Raw.buckets`
      [def, depth 1, in-statement, role explicit-arg]
   3. `Array.size`
      [def, depth 10, in-statement, role explicit-arg]
   4. `Std.DHashMap.Internal.Raw₀.getD_eq_fallback`
      [theorem, depth 66, introduced-by-proof, role applied]
   5. `LawfulBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Std.DHashMap.inner`
      [def, depth 2, in-statement, role explicit-arg]
   7. `Std.DHashMap`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
  10. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
  11. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  12. `Std.DHashMap.wf`
      [theorem, depth 2, in-statement, role explicit-arg]
  13. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  15. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `_private.Std.Data.DHashMap.Basic.0.Std.DHashMap.insert._proof_1`
      [theorem, depth 66, in-statement, role explicit-arg]
  17. `Std.DHashMap.Internal.AssocList`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `Subtype.mk`
      [constructor, depth 1, in-statement, role explicit-arg]

### proof_0451  (target depth 108, band 76-125)

THEOREM PROVED: `String.Pos.le_prev_iff_lt`

Grade all 24 candidates.

   1. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   2. `String.Pos.offset`
      [def, depth 2, in-statement, role explicit-arg]
   3. `String.Pos.prev`
      [def, depth 103, in-statement, role explicit-arg]
   4. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `String.Pos.prev_eq_posLT._proof_1`
      [theorem, depth 56, introduced-by-proof, role explicit-arg]
   6. `String`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   8. `String.Pos`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `_private.Init.Data.String.Lemmas.FindPos.0.String.Pos.le_prev_iff_lt._simp_1_1`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  10. `String.instLTRaw`
      [def, depth 4, in-statement, role instance-slot]
  11. `String.instLEPos`
      [def, depth 4, in-statement, role instance-slot]
  12. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `String.startPos`
      [def, depth 54, in-statement, role explicit-arg]
  14. `Ne`
      [def, depth 2, in-statement, role type-annotation]
  15. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `String.instLTPos`
      [def, depth 5, in-statement, role instance-slot]
  17. `LT.lt`
      [def, depth 1, in-statement, role explicit-arg]
  18. `String.le_posLT_iff._simp_1`
      [theorem, depth 107, introduced-by-proof, role explicit-arg]
  19. `iff_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  20. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  21. `String.Pos.Raw`
      [inductive, depth 0, in-statement, role implicit-arg]
  22. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
  23. `String.posLT`
      [def, depth 102, introduced-by-proof, role explicit-arg]
  24. `String.Pos.prev_eq_posLT`
      [theorem, depth 105, introduced-by-proof, role explicit-arg]

### proof_0452  (target depth 86, band 76-125)

THEOREM PROVED: `FreeAbelianGroup.nonempty_support_iff`

Grade all 24 candidates.

   1. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `SubNegZeroMonoid.toNegZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   3. `NegZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
   4. `FreeAbelianGroup`
      [def, depth 69, in-statement, role implicit-arg]
   5. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `id`
      [def, depth 0, in-statement, role explicit-arg]
   7. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `SubtractionMonoid.toSubNegZeroMonoid`
      [def, depth 9, in-statement, role instance-slot]
   9. `SubtractionCommMonoid.toSubtractionMonoid`
      [def, depth 1, in-statement, role instance-slot]
  10. `EmptyCollection.emptyCollection`
      [def, depth 1, in-statement, role explicit-arg]
  11. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `FreeAbelianGroup.support_eq_empty`
      [theorem, depth 85, introduced-by-proof, role explicit-arg]
  13. `instAddCommGroupFreeAbelianGroup`
      [def, depth 77, in-statement, role instance-slot]
  14. `Finset.not_nonempty_iff_eq_empty._simp_1`
      [theorem, depth 61, introduced-by-proof, role explicit-arg]
  15. `Finset.instEmptyCollection`
      [def, depth 25, in-statement, role instance-slot]
  16. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  17. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `Mathlib.Tactic.Contrapose.contrapose_iff₃`
      [theorem, depth 13, introduced-by-proof, role applied]
  19. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
  20. `Finset.Nonempty`
      [def, depth 54, in-statement, role explicit-arg]
  21. `Not`
      [def, depth 1, in-statement, role explicit-arg]
  22. `AddCommGroup.toDivisionAddCommMonoid`
      [def, depth 12, in-statement, role instance-slot]
  23. `FreeAbelianGroup.support`
      [def, depth 81, in-statement, role explicit-arg]
  24. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_0453  (target depth 34, band 26-50)

THEOREM PROVED: `CategoryTheory.Grp.trivial_grp_one`

Grade all 14 candidates.

   1. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   2. `CategoryTheory.CartesianMonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   4. `CategoryTheory.MonObj.one`
      [def, depth 3, in-statement, role explicit-arg]
   5. `CategoryTheory.MonoidalCategoryStruct.tensorUnit`
      [def, depth 2, in-statement, role explicit-arg]
   6. `CategoryTheory.Grp.trivial`
      [def, depth 33, in-statement, role explicit-arg]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   8. `CategoryTheory.GrpObj.toMonObj`
      [def, depth 3, in-statement, role instance-slot]
   9. `CategoryTheory.CartesianMonoidalCategory.toSemiCartesianMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
  10. `CategoryTheory.Grp.grp`
      [def, depth 3, in-statement, role instance-slot]
  11. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
  12. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  13. `CategoryTheory.SemiCartesianMonoidalCategory.toMonoidalCategory`
      [def, depth 2, in-statement, role implicit-arg]
  14. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0454  (target depth 163, band 126+)

THEOREM PROVED: `ContinuousAffineMap.differentiableOn`

Grade all 21 candidates.

   1. `DivisionRing.toRing`
      [def, depth 1, in-statement, role instance-slot]
   2. `Differentiable.differentiableOn`
      [theorem, depth 159, introduced-by-proof, role applied]
   3. `NormedSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Field.toDivisionRing`
      [def, depth 44, in-statement, role instance-slot]
   5. `NormedField.toField`
      [def, depth 1, in-statement, role instance-slot]
   6. `NormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `ContinuousAffineMap`
      [inductive, depth 6, in-statement, role implicit-arg]
   8. `PseudoMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
  10. `NormedSpace.toModule`
      [def, depth 2, in-statement, role instance-slot]
  11. `SeminormedAddCommGroup.toPseudoMetricSpace`
      [def, depth 1, in-statement, role implicit-arg]
  12. `ContinuousAffineMap.differentiable`
      [theorem, depth 162, introduced-by-proof, role explicit-arg]
  13. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role instance-slot]
  14. `NontriviallyNormedField`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `NontriviallyNormedField.toNormedField`
      [def, depth 1, in-statement, role instance-slot]
  16. `ContinuousAffineMap.instFunLike`
      [def, depth 28, in-statement, role instance-slot]
  17. `NormedAddCommGroup.toSeminormedAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  18. `NormedAddCommGroup.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
  19. `Set`
      [def, depth 0, in-statement, role type-annotation]
  20. `NormedAddTorsor.toAddTorsor`
      [def, depth 2, in-statement, role instance-slot]
  21. `SeminormedAddCommGroup.toNormedAddTorsor`
      [def, depth 15, in-statement, role instance-slot]

### proof_0455  (target depth 25, band 11-25)

THEOREM PROVED: `Fin.sbtw_iff`

Grade all 8 candidates.

   1. `instCircularOrderFin`
      [def, depth 24, in-statement, role instance-slot]
   2. `CircularPartialOrder.toCircularPreorder`
      [def, depth 1, in-statement, role instance-slot]
   3. `Iff.rfl`
      [theorem, depth 3, in-statement, role applied]
   4. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `CircularOrder.toCircularPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   6. `Fin`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `CircularPreorder.toSBtw`
      [def, depth 1, in-statement, role instance-slot]
   8. `SBtw.sbtw`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0456  (target depth 29, band 26-50)

THEOREM PROVED: `Preorder.instHasTerminalOfOrderTop`

Grade all 12 candidates.

   1. `Top.top`
      [def, depth 1, introduced-by-proof, role explicit-arg]
   2. `Unique.instInhabited`
      [def, depth 2, introduced-by-proof, role instance-slot]
   3. `CategoryTheory.uniqueToTop`
      [def, depth 12, introduced-by-proof, role instance-slot]
   4. `Preorder.toLE`
      [def, depth 1, in-statement, role implicit-arg]
   5. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   6. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `CategoryTheory.Limits.hasTerminal_of_unique`
      [theorem, depth 28, introduced-by-proof, role applied]
   8. `OrderTop`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Preorder.smallCategory`
      [def, depth 10, in-statement, role instance-slot]
  10. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, introduced-by-proof, role instance-slot]
  11. `OrderTop.toTop`
      [def, depth 2, introduced-by-proof, role instance-slot]
  12. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
