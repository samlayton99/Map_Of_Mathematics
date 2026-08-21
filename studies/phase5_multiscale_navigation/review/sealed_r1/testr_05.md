# Grading batch `testr_05` — 24 proofs

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

### proof_0097  (target depth 7, band 0-10)

THEOREM PROVED: `String.Slice.Pattern.SearchStep.endPos_matched`

Grade all 5 candidates.

   1. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   2. `String.Slice.Pattern.SearchStep.matched`
      [constructor, depth 2, in-statement, role explicit-arg]
   3. `String.Slice.Pos`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `String.Slice`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `String.Slice.Pattern.SearchStep.endPos`
      [def, depth 6, in-statement, role implicit-arg]

### proof_0098  (target depth 8, band 0-10)

THEOREM PROVED: `BddBelow.inter_of_left`

Grade all 8 candidates.

   1. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   2. `BddBelow`
      [def, depth 5, in-statement, role type-annotation]
   3. `Inter.inter`
      [def, depth 1, in-statement, role strict-implicit]
   4. `Set.inter_subset_left`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   5. `BddBelow.mono`
      [theorem, depth 7, introduced-by-proof, role applied]
   6. `Set`
      [def, depth 0, in-statement, role type-annotation]
   7. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Set.instInter`
      [def, depth 5, in-statement, role instance-slot]

### proof_0099  (target depth 5, band 0-10)

THEOREM PROVED: `forall_prop_congr_dom`

Grade all 3 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `Eq.rec`
      [recursor, depth 2, in-statement, role applied]
   3. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0100  (target depth 6, band 0-10)

THEOREM PROVED: `Option.forM_eq_forM`

Grade all 7 candidates.

   1. `Monad`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Applicative.toPure`
      [def, depth 1, in-statement, role instance-slot]
   3. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   4. `PUnit`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Option.forM`
      [def, depth 5, in-statement, role implicit-arg]
   6. `Monad.toApplicative`
      [def, depth 1, in-statement, role instance-slot]
   7. `Option`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0101  (target depth 3, band 0-10)

THEOREM PROVED: `CategoryTheory.Monad.PreservesColimitOfIsReflexivePair.out`

Grade all 3 candidates.

   1. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.Monad.PreservesColimitOfIsReflexivePair`
      [inductive, depth 2, in-statement, role type-annotation]

### proof_0102  (target depth 3, band 0-10)

THEOREM PROVED: `QuaternionAlgebra.imI_neg`

Grade all 6 candidates.

   1. `Neg`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role applied]
   3. `QuaternionAlgebra`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]
   5. `QuaternionAlgebra.instNeg`
      [def, depth 2, in-statement, role instance-slot]
   6. `QuaternionAlgebra.imI`
      [def, depth 1, in-statement, role explicit-arg]

### proof_0103  (target depth 3, band 0-10)

THEOREM PROVED: `InnerProductSpace.add_left`

Grade all 3 candidates.

   1. `InnerProductSpace`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `SeminormedAddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `RCLike`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0104  (target depth 6, band 0-10)

THEOREM PROVED: `One.gOne_one`

Grade all 5 candidates.

   1. `One`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `GradedMonoid.GOne.one`
      [def, depth 2, in-statement, role explicit-arg]
   3. `One.gOne`
      [def, depth 5, in-statement, role instance-slot]
   4. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role applied]

### proof_0105  (target depth 5, band 0-10)

THEOREM PROVED: `neg_mul_mem`

Grade all 15 candidates.

   1. `HasDistribNeg.toInvolutiveNeg`
      [def, depth 2, in-statement, role instance-slot]
   2. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   3. `MulMemClass`
      [inductive, depth 2, in-statement, role type-annotation]
   4. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   5. `neg_mul`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   6. `MulMemClass.mul_mem`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]
   8. `InvolutiveNeg.toNeg`
      [def, depth 1, in-statement, role instance-slot]
   9. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  10. `Eq.mp`
      [def, depth 3, introduced-by-proof, role applied]
  11. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  12. `HasDistribNeg`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  14. `Mul`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `SetLike`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0106  (target depth 4, band 0-10)

THEOREM PROVED: `LatticeHomClass.toInfHomClass`

Grade all 3 candidates.

   1. `Lattice`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `FunLike`
      [def, depth 2, in-statement, role type-annotation]
   3. `LatticeHomClass`
      [inductive, depth 3, in-statement, role type-annotation]

### proof_0107  (target depth 5, band 0-10)

THEOREM PROVED: `Set.elem_mem`

Grade all 5 candidates.

   1. `Set.ofPred`
      [def, depth 1, in-statement, role explicit-arg]
   2. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Set.Elem`
      [def, depth 4, in-statement, role implicit-arg]
   4. `Membership`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `rfl`
      [def, depth 2, introduced-by-proof, role applied]

### proof_0108  (target depth 7, band 0-10)

THEOREM PROVED: `List.intersperse_singleton`

Grade all 5 candidates.

   1. `List.intersperse`
      [def, depth 6, in-statement, role implicit-arg]
   2. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   3. `List.cons`
      [constructor, depth 1, in-statement, role explicit-arg]
   4. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]

### proof_0109  (target depth 5, band 0-10)

THEOREM PROVED: `TwoP.coe_toBipointed`

Grade all 4 candidates.

   1. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   2. `Bipointed.X`
      [def, depth 1, in-statement, role implicit-arg]
   3. `TwoP`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `TwoP.toBipointed`
      [def, depth 4, in-statement, role explicit-arg]

### proof_0110  (target depth 9, band 0-10)

THEOREM PROVED: `div_mul_div_cancel'`

Grade all 22 candidates.

   1. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
   2. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   3. `CommMagma.toMul`
      [def, depth 1, introduced-by-proof, role instance-slot]
   4. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `div_mul_div_cancel`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
   6. `CommMonoid.toCommSemigroup`
      [def, depth 5, introduced-by-proof, role instance-slot]
   7. `CommGroup.toCommMonoid`
      [def, depth 5, introduced-by-proof, role instance-slot]
   8. `CommSemigroup.toCommMagma`
      [def, depth 5, introduced-by-proof, role instance-slot]
   9. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
  10. `HDiv.hDiv`
      [def, depth 2, in-statement, role explicit-arg]
  11. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
  12. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  13. `CommGroup.toGroup`
      [def, depth 1, in-statement, role instance-slot]
  14. `CommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `mul_comm`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  16. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  17. `instHDiv`
      [def, depth 3, in-statement, role instance-slot]
  18. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  19. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  20. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  21. `DivInvMonoid.toDiv`
      [def, depth 1, in-statement, role instance-slot]
  22. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0111  (target depth 10, band 0-10)

THEOREM PROVED: `List.cons_subset_of_subset_of_mem`

Grade all 10 candidates.

   1. `List.cons_subset`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   2. `And.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   3. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
   4. `HasSubset.Subset`
      [def, depth 1, in-statement, role implicit-arg]
   5. `List.cons`
      [constructor, depth 1, in-statement, role explicit-arg]
   6. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   7. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `And`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   9. `List.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  10. `List.instHasSubset`
      [def, depth 5, in-statement, role instance-slot]

### proof_0112  (target depth 6, band 0-10)

THEOREM PROVED: `Option.all_bind`

Grade all 15 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Option.bind`
      [def, depth 5, in-statement, role explicit-arg]
   3. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   5. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   6. `Option.casesOn`
      [def, depth 3, in-statement, role applied]
   7. `Option.none`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `Option.some`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  10. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  11. `Option.all`
      [def, depth 5, in-statement, role explicit-arg]
  12. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
  14. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
  15. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]

### proof_0113  (target depth 5, band 0-10)

THEOREM PROVED: `OrderDual.mulRightReflectLE`

Grade all 13 candidates.

   1. `OrderDual`
      [def, depth 0, in-statement, role type-annotation]
   2. `MulRightReflectLE.le_of_mul_le_mul_right'`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   3. `OrderDual.instLE`
      [def, depth 2, in-statement, role instance-slot]
   4. `Mul`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `instHMul`
      [def, depth 3, introduced-by-proof, role instance-slot]
   6. `LE`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `HMul.hMul`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   8. `MulRightReflectLE`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `MulRightReflectLE.mk`
      [constructor, depth 4, introduced-by-proof, role applied]
  10. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
  11. `Function.swap`
      [def, depth 0, introduced-by-proof, role implicit-arg]
  12. `OrderDual.instMul`
      [def, depth 1, in-statement, role instance-slot]
  13. `Contravariant.flip`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]

### proof_0114  (target depth 5, band 0-10)

THEOREM PROVED: `CategoryTheory.PreOneHypercover.multicospanShape_snd`

Grade all 8 candidates.

   1. `CategoryTheory.PreOneHypercover`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role applied]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `CategoryTheory.PreOneHypercover.multicospanShape`
      [def, depth 4, in-statement, role explicit-arg]
   5. `CategoryTheory.PreZeroHypercover.I₀`
      [def, depth 2, in-statement, role implicit-arg]
   6. `CategoryTheory.Limits.MulticospanShape.snd`
      [def, depth 1, in-statement, role explicit-arg]
   7. `CategoryTheory.PreOneHypercover.I₁'`
      [def, depth 3, in-statement, role type-annotation]
   8. `CategoryTheory.PreOneHypercover.toPreZeroHypercover`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0115  (target depth 5, band 0-10)

THEOREM PROVED: `addLECancellable_zero`

Grade all 18 candidates.

   1. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   2. `AddZeroClass`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   4. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   6. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `AddZero.toZero`
      [def, depth 1, in-statement, role instance-slot]
   8. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
   9. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  10. `Eq`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  11. `zero_add`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  12. `LE`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  15. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  16. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  17. `implies_congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  18. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]

### proof_0116  (target depth 5, band 0-10)

THEOREM PROVED: `AddUnits.vaddCommClass_left`

Grade all 8 candidates.

   1. `VAddCommClass.mk`
      [constructor, depth 4, introduced-by-proof, role applied]
   2. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `AddUnits`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `AddUnits.val`
      [def, depth 2, in-statement, role explicit-arg]
   5. `VAddCommClass.vadd_comm`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   6. `VAddCommClass`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `AddUnits.instVAdd`
      [def, depth 4, in-statement, role instance-slot]
   8. `VAdd`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0117  (target depth 5, band 0-10)

THEOREM PROVED: `Frm.id_apply`

Grade all 5 candidates.

   1. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   2. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   3. `Frm`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Frm.carrier`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0118  (target depth 6, band 0-10)

THEOREM PROVED: `CategoryTheory.InducedWideCategory.Hom.property`

Grade all 6 candidates.

   1. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
   2. `CategoryTheory.MorphismProperty.IsMultiplicative`
      [inductive, depth 3, in-statement, role type-annotation]
   3. `CategoryTheory.InducedWideCategory.Hom`
      [inductive, depth 5, in-statement, role type-annotation]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.InducedWideCategory`
      [def, depth 4, in-statement, role type-annotation]
   6. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0119  (target depth 4, band 0-10)

THEOREM PROVED: `Set.Ioi_subset_Ici_self`

Grade all 6 candidates.

   1. `le_of_lt`
      [theorem, depth 3, introduced-by-proof, role applied]
   2. `Set.Ioi`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   4. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   6. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]

### proof_0120  (target depth 7, band 0-10)

THEOREM PROVED: `Option.join_map_eq_map_join`

Grade all 12 candidates.

   1. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   2. `Option.some`
      [constructor, depth 1, in-statement, role explicit-arg]
   3. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   4. `Option.join`
      [def, depth 6, in-statement, role explicit-arg]
   5. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
   6. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   7. `Option.none`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Option.casesOn`
      [def, depth 3, in-statement, role applied]
  10. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  11. `Option.map`
      [def, depth 5, in-statement, role explicit-arg]
  12. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
