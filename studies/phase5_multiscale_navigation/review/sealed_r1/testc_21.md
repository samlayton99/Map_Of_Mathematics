# Grading batch `testc_21` — 24 proofs

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

### proof_0481  (target depth 112, band 76-125)

THEOREM PROVED: `String.Slice.contains_char_eq_contains_beq`

Grade all 13 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `Char`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `String.Slice.Pattern.ToForwardSearcher.DefaultForwardSearcher.instIteratorLoopIdSearchStep`
      [def, depth 111, in-statement, role instance-slot]
   4. `instBEqOfDecidableEq`
      [def, depth 6, in-statement, role instance-slot]
   5. `String.Slice.Pattern.Char.instToForwardSearcherCharDefaultForwardSearcherForallBoolBeq`
      [def, depth 111, in-statement, role instance-slot]
   6. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `String.Slice.contains`
      [def, depth 31, in-statement, role implicit-arg]
   8. `instDecidableEqChar`
      [def, depth 22, in-statement, role instance-slot]
   9. `String.Slice.Pattern.ToForwardSearcher.DefaultForwardSearcher.instIteratorIdSearchStepOfForwardPattern`
      [def, depth 110, in-statement, role instance-slot]
  10. `String.Slice.Pattern.ToForwardSearcher.DefaultForwardSearcher`
      [inductive, depth 1, in-statement, role implicit-arg]
  11. `String.Slice.Pattern.CharPred.instForwardPatternForallCharBool`
      [def, depth 109, in-statement, role instance-slot]
  12. `BEq.beq`
      [def, depth 1, in-statement, role explicit-arg]
  13. `String.Slice`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0482  (target depth 65, band 51-75)

THEOREM PROVED: `SimpleGraph.ComponentCompl.hom_infinite`

Grade all 11 candidates.

   1. `Set.Infinite`
      [def, depth 6, in-statement, role type-annotation]
   2. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]
   3. `Set.Infinite.mono`
      [theorem, depth 64, introduced-by-proof, role applied]
   4. `SimpleGraph.ComponentCompl.setLike`
      [def, depth 18, in-statement, role instance-slot]
   5. `SimpleGraph.ComponentCompl.hom`
      [def, depth 59, in-statement, role explicit-arg]
   6. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   7. `SimpleGraph.ComponentCompl`
      [def, depth 12, in-statement, role implicit-arg]
   8. `Set`
      [def, depth 0, in-statement, role type-annotation]
   9. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `SimpleGraph.ComponentCompl.subset_hom`
      [theorem, depth 60, introduced-by-proof, role explicit-arg]
  11. `SetLike.coe`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0483  (target depth 117, band 76-125)

THEOREM PROVED: `RingHom.FormallyEtale.of_comp`

Grade all 16 candidates.

   1. `RingHom.FormallyUnramified`
      [def, depth 19, in-statement, role type-annotation]
   2. `RingHom.toAlgebra`
      [def, depth 18, in-statement, role let-value]
   3. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role implicit-arg]
   4. `Algebra.toSMul`
      [def, depth 2, introduced-by-proof, role instance-slot]
   5. `Algebra.algebraMap`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   6. `RingHom`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   8. `RingHom.comp`
      [def, depth 18, in-statement, role explicit-arg]
   9. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `IsScalarTower`
      [inductive, depth 1, introduced-by-proof, role type-annotation]
  11. `Algebra.FormallyEtale.of_restrictScalars`
      [theorem, depth 116, introduced-by-proof, role applied]
  12. `IsScalarTower.of_algebraMap_eq'`
      [theorem, depth 19, introduced-by-proof, role let-value]
  13. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
  15. `RingHom.FormallyEtale`
      [def, depth 19, in-statement, role type-annotation]
  16. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]

### proof_0484  (target depth 64, band 51-75)

THEOREM PROVED: `NonUnitalSubsemiring.subset_closure`

Grade all 13 candidates.

   1. `NonUnitalNonAssocSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   3. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   4. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   5. `NonUnitalSubsemiring.instSetLike`
      [def, depth 12, in-statement, role instance-slot]
   6. `NonUnitalSubsemiring.closure`
      [def, depth 63, in-statement, role explicit-arg]
   7. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   8. `NonUnitalSubsemiring`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  10. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  11. `NonUnitalSubsemiring.mem_closure`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
  12. `SetLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]

### proof_0485  (target depth 8, band 0-10)

THEOREM PROVED: `Std.Iter.isPlausibleSuccessorOf_eq_invImage`

Grade all 5 candidates.

   1. `Std.Iter.IsPlausibleSuccessorOf`
      [def, depth 7, in-statement, role implicit-arg]
   2. `Std.Iter`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   4. `Std.Iterator`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Id`
      [def, depth 0, in-statement, role explicit-arg]

### proof_0486  (target depth 28, band 26-50)

THEOREM PROVED: `FirstOrder.Language.Theory.Iff.mpr`

Grade all 10 candidates.

   1. `And.right`
      [theorem, depth 1, introduced-by-proof, role applied]
   2. `FirstOrder.Language.Theory.Imp`
      [def, depth 22, in-statement, role explicit-arg]
   3. `FirstOrder.Language`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Iff.mp`
      [theorem, depth 1, in-statement, role explicit-arg]
   5. `FirstOrder.Language.Theory`
      [def, depth 6, in-statement, role type-annotation]
   6. `FirstOrder.Language.BoundedFormula`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `FirstOrder.Language.Theory.Iff`
      [def, depth 22, in-statement, role implicit-arg]
   9. `And`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  10. `FirstOrder.Language.Theory.iff_iff_imp_and_imp`
      [theorem, depth 27, introduced-by-proof, role explicit-arg]

### proof_0487  (target depth 21, band 11-25)

THEOREM PROVED: `Set.Pairwise.subsingleton`

Grade all 9 candidates.

   1. `Iff.mp`
      [theorem, depth 1, in-statement, role applied]
   2. `Set.Subsingleton`
      [def, depth 4, in-statement, role implicit-arg]
   3. `Set.Pairwise`
      [def, depth 4, in-statement, role implicit-arg]
   4. `Set.pairwise_bot_iff`
      [theorem, depth 20, introduced-by-proof, role explicit-arg]
   5. `Set`
      [def, depth 0, in-statement, role type-annotation]
   6. `BooleanAlgebra.toBot`
      [def, depth 1, in-statement, role instance-slot]
   7. `Prop.instBooleanAlgebra`
      [def, depth 19, in-statement, role instance-slot]
   8. `Bot.bot`
      [def, depth 1, in-statement, role explicit-arg]
   9. `Pi.instBotForall`
      [def, depth 2, in-statement, role instance-slot]

### proof_0488  (target depth 10, band 0-10)

THEOREM PROVED: `Codisjoint.eq_top_of_le`

Grade all 12 candidates.

   1. `OrderTop.toTop`
      [def, depth 2, in-statement, role instance-slot]
   2. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   3. `le_rfl`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   4. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Codisjoint`
      [def, depth 3, in-statement, role type-annotation]
   6. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
   7. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
   8. `eq_top_iff`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   9. `Top.top`
      [def, depth 1, in-statement, role explicit-arg]
  10. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  11. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `OrderTop`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0489  (target depth 143, band 126+)

THEOREM PROVED: `instIsIsometricVAddAddOpposite`

Grade all 19 candidates.

   1. `HVAdd.hVAdd`
      [def, depth 2, in-statement, role explicit-arg]
   2. `instHVAdd`
      [def, depth 3, in-statement, role instance-slot]
   3. `PseudoEMetricSpace.toUniformSpace`
      [def, depth 1, in-statement, role instance-slot]
   4. `EDist.edist`
      [def, depth 1, in-statement, role explicit-arg]
   5. `AddOpposite.unop`
      [def, depth 2, in-statement, role explicit-arg]
   6. `UniformSpace.toTopologicalSpace`
      [def, depth 1, in-statement, role implicit-arg]
   7. `AddOpposite.instPseudoEMetricSpace`
      [def, depth 136, in-statement, role instance-slot]
   8. `ENNReal`
      [def, depth 96, in-statement, role implicit-arg]
   9. `WeakPseudoEMetricSpace.toEDist`
      [def, depth 2, introduced-by-proof, role instance-slot]
  10. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `edist_vadd_left`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  12. `PseudoEMetricSpace.toWeakPseudoEMetricSpace`
      [def, depth 140, introduced-by-proof, role instance-slot]
  13. `AddOpposite`
      [def, depth 1, in-statement, role implicit-arg]
  14. `IsIsometricVAdd.mk`
      [constructor, depth 142, introduced-by-proof, role applied]
  15. `PseudoEMetricSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `AddOpposite.instVAdd`
      [def, depth 4, in-statement, role instance-slot]
  17. `VAdd`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `id`
      [def, depth 0, in-statement, role explicit-arg]
  19. `IsIsometricVAdd`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0490  (target depth 41, band 26-50)

THEOREM PROVED: `Std.DTreeMap.Internal.Impl.minEntry?_eq_minEntry?`

Grade all 17 candidates.

   1. `Ord`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Std.DTreeMap.Internal.Impl.minEntry?ₘ_eq_minEntry?`
      [theorem, depth 39, introduced-by-proof, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `Std.DTreeMap.Internal.Impl.Ordered`
      [def, depth 10, in-statement, role type-annotation]
   6. `id`
      [def, depth 0, in-statement, role explicit-arg]
   7. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Std.DTreeMap.Internal.Impl.minEntry?_eq_minEntry?ₘ`
      [theorem, depth 40, introduced-by-proof, role explicit-arg]
   9. `Std.TransOrd`
      [def, depth 2, in-statement, role type-annotation]
  10. `Std.DTreeMap.Internal.Impl.toListModel`
      [def, depth 9, in-statement, role explicit-arg]
  11. `Std.DTreeMap.Internal.Impl.minEntry?ₘ`
      [def, depth 15, introduced-by-proof, role explicit-arg]
  12. `Std.DTreeMap.Internal.Impl.minEntry?`
      [def, depth 36, in-statement, role explicit-arg]
  13. `Std.DTreeMap.Internal.Impl`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Std.Internal.List.minEntry?`
      [def, depth 33, in-statement, role explicit-arg]
  15. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  16. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  17. `Sigma`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0491  (target depth 67, band 51-75)

THEOREM PROVED: `isLocallyClosed_Ico`

Grade all 24 candidates.

   1. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `Set.Iio_inter_Ici`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   7. `Inter.inter`
      [def, depth 1, in-statement, role explicit-arg]
   8. `isLocallyClosed_Iio`
      [theorem, depth 66, introduced-by-proof, role explicit-arg]
   9. `Set.instInter`
      [def, depth 5, in-statement, role instance-slot]
  10. `IsLocallyClosed.inter`
      [theorem, depth 62, introduced-by-proof, role explicit-arg]
  11. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  12. `isLocallyClosed_Ici`
      [theorem, depth 22, introduced-by-proof, role explicit-arg]
  13. `Set.Iio`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  14. `IsLocallyClosed`
      [def, depth 6, in-statement, role explicit-arg]
  15. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  16. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
  17. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  18. `Set.Ici`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  19. `ClosedIciTopology`
      [inductive, depth 1, in-statement, role type-annotation]
  20. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  21. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  22. `id`
      [def, depth 0, in-statement, role explicit-arg]
  23. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  24. `Set.Ico`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0492  (target depth 58, band 51-75)

THEOREM PROVED: `IntermediateField.mem_toSubfield`

Grade all 14 candidates.

   1. `IntermediateField.toSubfield`
      [def, depth 57, in-statement, role explicit-arg]
   2. `Semifield.toDivisionSemiring`
      [def, depth 44, in-statement, role instance-slot]
   3. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   4. `Subfield.instSetLike`
      [def, depth 49, in-statement, role instance-slot]
   5. `Field`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Subfield`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   8. `Field.toSemifield`
      [def, depth 44, in-statement, role instance-slot]
   9. `Field.toDivisionRing`
      [def, depth 44, in-statement, role instance-slot]
  10. `Semifield.toCommSemiring`
      [def, depth 1, in-statement, role instance-slot]
  11. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `IntermediateField`
      [inductive, depth 45, in-statement, role type-annotation]
  13. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  14. `Iff.rfl`
      [theorem, depth 3, in-statement, role applied]

### proof_0493  (target depth 12, band 11-25)

THEOREM PROVED: `Array.Perm.mem_iff`

Grade all 19 candidates.

   1. `List.mem_toArray._simp_1`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
   2. `Eq`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   3. `Array.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   4. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `List.Perm`
      [inductive, depth 1, introduced-by-proof, role implicit-arg]
   7. `List.instMembership`
      [def, depth 3, introduced-by-proof, role instance-slot]
   8. `Array.Perm`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  10. `Array.mk`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  11. `Array`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  13. `List`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
  14. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  15. `Array.casesOn`
      [def, depth 3, introduced-by-proof, role applied]
  16. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
  17. `_private.Init.Data.Array.Perm.0.Array.Perm.mem_iff._simp_1_1`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  18. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
  19. `List.Perm.mem_iff`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]

### proof_0494  (target depth 17, band 11-25)

THEOREM PROVED: `Set.Iio_inj`

Grade all 10 candidates.

   1. `Set.Iio_injective`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
   2. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   3. `Function.Injective.eq_iff`
      [theorem, depth 4, introduced-by-proof, role applied]
   4. `Set.Iio`
      [def, depth 2, in-statement, role implicit-arg]
   5. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
   6. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   8. `Lattice.toSemilatticeSup`
      [def, depth 1, in-statement, role instance-slot]
   9. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
  10. `SemilatticeSup.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]

### proof_0495  (target depth 12, band 11-25)

THEOREM PROVED: `Zsqrtd.nonnegg_cases_right`

Grade all 18 candidates.

   1. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   2. `Zsqrtd.SqLe`
      [def, depth 10, in-statement, role type-annotation]
   3. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Nat.cast`
      [def, depth 2, in-statement, role explicit-arg]
   5. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `_private.Mathlib.NumberTheory.Zsqrtd.Basic.0.Zsqrtd.nonnegg_cases_right.match_1_1`
      [def, depth 11, introduced-by-proof, role applied]
   7. `Int.instNegInt`
      [def, depth 7, in-statement, role instance-slot]
   8. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
   9. `Int.negSucc`
      [constructor, depth 1, in-statement, role explicit-arg]
  10. `instNatCastInt`
      [def, depth 2, in-statement, role instance-slot]
  11. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  13. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Zsqrtd.Nonnegg`
      [def, depth 11, in-statement, role explicit-arg]
  15. `rfl`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  16. `trivial`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  17. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]
  18. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0496  (target depth 77, band 76-125)

THEOREM PROVED: `Std.DTreeMap.Raw.get!_erase`

Grade all 9 candidates.

   1. `Std.DTreeMap.Internal.Impl.get!_erase!`
      [theorem, depth 76, introduced-by-proof, role applied]
   2. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role implicit-arg]
   4. `Std.LawfulEqCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Std.DTreeMap.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   6. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   7. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   8. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0497  (target depth 66, band 51-75)

THEOREM PROVED: `closed_nhdsSet_basis`

Grade all 17 candidates.

   1. `Filter.HasBasis`
      [inductive, depth 1, in-statement, role implicit-arg]
   2. `Filter.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   3. `Filter`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `IsClosed`
      [inductive, depth 1, in-statement, role explicit-arg]
   5. `exists_mem_nhdsSet_isClosed_subset`
      [theorem, depth 65, introduced-by-proof, role explicit-arg]
   6. `And`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `nhdsSet`
      [def, depth 19, in-statement, role explicit-arg]
   8. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Exists`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `NormalSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
  12. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
  13. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Filter.hasBasis_self`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]
  15. `id`
      [def, depth 0, in-statement, role explicit-arg]
  16. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  17. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]

### proof_0498  (target depth 86, band 76-125)

THEOREM PROVED: `SimpleGraph.IsAcyclic.eq_snd_of_adj_start`

Grade all 18 candidates.

   1. `SimpleGraph.Path.singleton`
      [def, depth 27, introduced-by-proof, role explicit-arg]
   2. `SimpleGraph.IsAcyclic`
      [def, depth 3, in-statement, role type-annotation]
   3. `SimpleGraph.Walk.support`
      [def, depth 7, in-statement, role explicit-arg]
   4. `SimpleGraph.Walk.takeUntil`
      [def, depth 15, introduced-by-proof, role explicit-arg]
   5. `_private.Mathlib.Combinatorics.SimpleGraph.Acyclic.0.SimpleGraph.IsAcyclic.eq_snd_of_adj_start._proof_1_6`
      [theorem, depth 65, introduced-by-proof, role applied]
   6. `List.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   7. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `SimpleGraph.Walk.IsPath.takeUntil`
      [theorem, depth 23, introduced-by-proof, role explicit-arg]
   9. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `SimpleGraph.Walk`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Classical.propDecidable`
      [def, depth 11, introduced-by-proof, role instance-slot]
  12. `SimpleGraph.Adj`
      [def, depth 1, in-statement, role type-annotation]
  13. `SimpleGraph.Walk.IsPath`
      [inductive, depth 2, in-statement, role implicit-arg]
  14. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  15. `Subtype.mk`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  16. `Subsingleton.elim`
      [theorem, depth 2, introduced-by-proof, role let-value]
  17. `SimpleGraph.Path`
      [def, depth 3, introduced-by-proof, role implicit-arg]
  18. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0499  (target depth 15, band 11-25)

THEOREM PROVED: `CategoryTheory.MorphismProperty.equivalenceRightFractionRel`

Grade all 10 candidates.

   1. `CategoryTheory.MorphismProperty.RightFractionRel.symm`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
   2. `CategoryTheory.MorphismProperty.HasRightCalculusOfFractions`
      [inductive, depth 3, in-statement, role type-annotation]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
   5. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   6. `Equivalence.mk`
      [constructor, depth 1, introduced-by-proof, role applied]
   7. `CategoryTheory.MorphismProperty.RightFractionRel.refl`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
   8. `CategoryTheory.MorphismProperty.RightFractionRel`
      [def, depth 5, in-statement, role implicit-arg]
   9. `CategoryTheory.MorphismProperty.RightFractionRel.trans`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
  10. `CategoryTheory.MorphismProperty.RightFraction`
      [inductive, depth 3, in-statement, role type-annotation]

### proof_0500  (target depth 89, band 76-125)

THEOREM PROVED: `ZFSet.subset_vonNeumann_self`

Grade all 14 candidates.

   1. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   2. `ZFSet.instPartialOrder`
      [def, depth 22, in-statement, role instance-slot]
   3. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `Std.le_refl._simp_1`
      [theorem, depth 6, in-statement, role explicit-arg]
   5. `Ordinal.partialOrder`
      [def, depth 30, in-statement, role instance-slot]
   6. `ZFSet.vonNeumann`
      [def, depth 40, in-statement, role explicit-arg]
   7. `Ordinal`
      [def, depth 25, in-statement, role implicit-arg]
   8. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   9. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
  10. `ZFSet.rank`
      [def, depth 41, in-statement, role explicit-arg]
  11. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `_private.Mathlib.SetTheory.ZFC.VonNeumann.0.ZFSet.subset_vonNeumann_self._simp_1_1`
      [theorem, depth 88, introduced-by-proof, role explicit-arg]
  13. `ZFSet`
      [def, depth 14, in-statement, role implicit-arg]
  14. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]

### proof_0501  (target depth 53, band 51-75)

THEOREM PROVED: `UInt8.sub_eq_add_mul`

Grade all 22 candidates.

   1. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   2. `id`
      [def, depth 0, in-statement, role explicit-arg]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   6. `instAddUInt8`
      [def, depth 27, in-statement, role instance-slot]
   7. `instSubUInt8`
      [def, depth 27, in-statement, role instance-slot]
   8. `UInt8.sub_eq_add_neg`
      [theorem, depth 30, introduced-by-proof, role explicit-arg]
   9. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
  10. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  11. `UInt8.neg_one_eq`
      [theorem, depth 28, introduced-by-proof, role explicit-arg]
  12. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  13. `Neg.neg`
      [def, depth 1, introduced-by-proof, role explicit-arg]
  14. `UInt8.neg_eq_neg_one_mul`
      [theorem, depth 52, introduced-by-proof, role explicit-arg]
  15. `HSub.hSub`
      [def, depth 2, in-statement, role explicit-arg]
  16. `instNegUInt8`
      [def, depth 27, introduced-by-proof, role instance-slot]
  17. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  18. `instHSub`
      [def, depth 3, in-statement, role instance-slot]
  19. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  20. `UInt8`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `UInt8.instOfNat`
      [def, depth 25, in-statement, role instance-slot]
  22. `instMulUInt8`
      [def, depth 27, in-statement, role instance-slot]

### proof_0502  (target depth 45, band 26-50)

THEOREM PROVED: `Int.modEq_and_modEq_iff_modEq_lcm`

Grade all 20 candidates.

   1. `iff_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   2. `Int.ModEq`
      [def, depth 23, in-statement, role explicit-arg]
   3. `instNatCastInt`
      [def, depth 2, in-statement, role instance-slot]
   4. `Int.lcm`
      [def, depth 26, in-statement, role explicit-arg]
   5. `Nat.cast`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `_private.Mathlib.Data.Int.ModEq.0.Int.modEq_and_modEq_iff_modEq_lcm._simp_1_2`
      [theorem, depth 39, introduced-by-proof, role explicit-arg]
   8. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `_private.Mathlib.Data.Int.ModEq.0.Int.modEq_and_modEq_iff_modEq_lcm._simp_1_1`
      [theorem, depth 44, introduced-by-proof, role explicit-arg]
  10. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  11. `instHSub`
      [def, depth 3, in-statement, role instance-slot]
  12. `Int.instDvd`
      [def, depth 12, introduced-by-proof, role instance-slot]
  13. `Int.instSub`
      [def, depth 13, introduced-by-proof, role instance-slot]
  14. `HSub.hSub`
      [def, depth 2, in-statement, role explicit-arg]
  15. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  17. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  18. `Dvd.dvd`
      [def, depth 1, introduced-by-proof, role implicit-arg]
  19. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]

### proof_0503  (target depth 143, band 126+)

THEOREM PROVED: `Complex.exp_nat_mul`

Grade all 17 candidates.

   1. `Nat.cast`
      [def, depth 2, in-statement, role explicit-arg]
   2. `HPow.hPow`
      [def, depth 2, in-statement, role explicit-arg]
   3. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
   4. `NPow.toPow`
      [def, depth 2, in-statement, role instance-slot]
   5. `Semiring.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
   6. `instHPow`
      [def, depth 3, in-statement, role instance-slot]
   7. `Monoid.toNPow`
      [def, depth 1, in-statement, role instance-slot]
   8. `Complex.instNatCast`
      [def, depth 87, in-statement, role instance-slot]
   9. `Complex`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Complex.exp`
      [def, depth 139, in-statement, role explicit-arg]
  13. `Complex.instSemiring`
      [def, depth 103, in-statement, role instance-slot]
  14. `Complex.exp_nat_mul._f`
      [def, depth 142, introduced-by-proof, role explicit-arg]
  15. `Complex.instMul`
      [def, depth 92, in-statement, role instance-slot]
  16. `Nat.brecOn`
      [def, depth 5, in-statement, role applied]
  17. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0504  (target depth 8, band 0-10)

THEOREM PROVED: `covBy_iff_wcovBy_and_ne`

Grade all 14 candidates.

   1. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
   2. `CovBy`
      [def, depth 2, in-statement, role implicit-arg]
   3. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   4. `CovBy.wcovBy`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   5. `And.left`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   6. `WCovBy.covBy_of_ne`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   7. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Ne`
      [def, depth 2, in-statement, role explicit-arg]
   9. `CovBy.ne`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  10. `And.right`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  11. `WCovBy`
      [def, depth 2, in-statement, role explicit-arg]
  12. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  14. `And.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
