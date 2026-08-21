# Grading batch `testr_06` — 24 proofs

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

### proof_0121  (target depth 7, band 0-10)

THEOREM PROVED: `Function.update_of_ne`

Grade all 7 candidates.

   1. `Ne`
      [def, depth 2, in-statement, role type-annotation]
   2. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `Eq.ndrec`
      [def, depth 3, in-statement, role implicit-arg]
   4. `dif_neg`
      [theorem, depth 6, introduced-by-proof, role applied]
   5. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   6. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `Not`
      [def, depth 1, in-statement, role type-annotation]

### proof_0122  (target depth 10, band 0-10)

THEOREM PROVED: `LowerSet.instAddAction._proof_1`

Grade all 5 candidates.

   1. `SetLike.coe_injective`
      [theorem, depth 2, introduced-by-proof, role applied]
   2. `LowerSet.instSetLike`
      [def, depth 9, in-statement, role instance-slot]
   3. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   4. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `LowerSet`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0123  (target depth 9, band 0-10)

THEOREM PROVED: `Set.uIcc_of_gt`

Grade all 8 candidates.

   1. `LT.lt.le`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   2. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   3. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   4. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   5. `Lattice`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   7. `Set.uIcc_of_ge`
      [theorem, depth 8, introduced-by-proof, role applied]
   8. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]

### proof_0124  (target depth 4, band 0-10)

THEOREM PROVED: `Stream'.map_const`

Grade all 4 candidates.

   1. `Stream'`
      [def, depth 1, in-statement, role implicit-arg]
   2. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   3. `Stream'.const`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Stream'.map`
      [def, depth 3, in-statement, role implicit-arg]

### proof_0125  (target depth 7, band 0-10)

THEOREM PROVED: `Set.PairwiseDisjoint.range`

Grade all 22 candidates.

   1. `Set.range`
      [def, depth 2, in-statement, role explicit-arg]
   2. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   3. `Ne`
      [def, depth 2, in-statement, role type-annotation]
   4. `Disjoint`
      [def, depth 3, in-statement, role explicit-arg]
   5. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   6. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   7. `OrderBot`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   9. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  10. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Set.Elem`
      [def, depth 4, in-statement, role implicit-arg]
  12. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  13. `congr_arg`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  14. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  15. `Set.PairwiseDisjoint`
      [def, depth 5, in-statement, role type-annotation]
  16. `Subtype.ext`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
  17. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
  18. `Function.onFun`
      [def, depth 0, in-statement, role type-annotation]
  19. `Disjoint.mono`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  20. `Subtype.property`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  21. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  22. `Exists.casesOn`
      [def, depth 3, introduced-by-proof, role applied]

### proof_0126  (target depth 2, band 0-10)

THEOREM PROVED: `IsOrderedCancelSMul.toIsOrderedSMul`

Grade all 3 candidates.

   1. `LE`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `IsOrderedCancelSMul`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `SMul`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0127  (target depth 7, band 0-10)

THEOREM PROVED: `isDedekindFiniteMonoid_iff`

Grade all 12 candidates.

   1. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
   2. `IsDedekindFiniteMonoid.casesOn`
      [def, depth 6, introduced-by-proof, role explicit-arg]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   5. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   7. `IsDedekindFiniteMonoid`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `IsDedekindFiniteMonoid.mk`
      [constructor, depth 4, introduced-by-proof, role explicit-arg]
   9. `MulOne`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  11. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
  12. `MulOne.toOne`
      [def, depth 1, in-statement, role instance-slot]

### proof_0128  (target depth 6, band 0-10)

THEOREM PROVED: `CategoryTheory.ShortComplex.iCycles_g`

Grade all 6 candidates.

   1. `CategoryTheory.Limits.HasZeroMorphisms`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.ShortComplex.HasLeftHomology`
      [inductive, depth 3, in-statement, role type-annotation]
   3. `CategoryTheory.ShortComplex`
      [inductive, depth 2, in-statement, role type-annotation]
   4. `CategoryTheory.ShortComplex.LeftHomologyData.wi`
      [theorem, depth 4, introduced-by-proof, role applied]
   5. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CategoryTheory.ShortComplex.leftHomologyData`
      [def, depth 5, in-statement, role explicit-arg]

### proof_0129  (target depth 7, band 0-10)

THEOREM PROVED: `AntitoneOn.const_mul'`

Grade all 10 candidates.

   1. `mul_right_mono`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   2. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
   3. `Mul`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `AntitoneOn`
      [def, depth 4, in-statement, role type-annotation]
   5. `MulLeftMono`
      [def, depth 4, in-statement, role type-annotation]
   6. `Monotone.comp_antitoneOn`
      [theorem, depth 5, introduced-by-proof, role applied]
   7. `Set`
      [def, depth 0, in-statement, role type-annotation]
   8. `HMul.hMul`
      [def, depth 2, in-statement, role implicit-arg]
   9. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  10. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0130  (target depth 5, band 0-10)

THEOREM PROVED: `Fin.castAdd_lt`

Grade all 7 candidates.

   1. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
   2. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `Fin`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
   5. `Fin.val`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Fin.is_lt._simp_1`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]

### proof_0131  (target depth 5, band 0-10)

THEOREM PROVED: `Pairwise.pairwiseDisjoint`

Grade all 9 candidates.

   1. `Function.onFun`
      [def, depth 0, in-statement, role explicit-arg]
   2. `Pairwise`
      [def, depth 3, in-statement, role type-annotation]
   3. `Set`
      [def, depth 0, in-statement, role type-annotation]
   4. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   5. `OrderBot`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   8. `Pairwise.set_pairwise`
      [theorem, depth 4, introduced-by-proof, role applied]
   9. `Disjoint`
      [def, depth 3, in-statement, role explicit-arg]

### proof_0132  (target depth 4, band 0-10)

THEOREM PROVED: `CategoryTheory.Presieve.BindStruct.hg`

Grade all 6 candidates.

   1. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.Presieve`
      [def, depth 2, in-statement, role type-annotation]
   6. `CategoryTheory.Presieve.BindStruct`
      [inductive, depth 3, in-statement, role type-annotation]

### proof_0133  (target depth 20, band 11-25)

THEOREM PROVED: `Stream'.take_get`

Grade all 20 candidates.

   1. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   2. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `Stream'.get`
      [def, depth 2, in-statement, role explicit-arg]
   5. `Stream'.take`
      [def, depth 10, in-statement, role explicit-arg]
   6. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `List.length`
      [def, depth 9, in-statement, role explicit-arg]
   8. `List.instGetElemNatLtLength`
      [def, depth 13, in-statement, role instance-slot]
   9. `Stream'`
      [def, depth 1, in-statement, role type-annotation]
  10. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `Stream'.drop`
      [def, depth 8, introduced-by-proof, role explicit-arg]
  12. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
  13. `Stream'.appendStream'`
      [def, depth 7, introduced-by-proof, role explicit-arg]
  14. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  15. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  17. `GetElem.getElem`
      [def, depth 2, in-statement, role explicit-arg]
  18. `Stream'.get_append_left`
      [theorem, depth 19, introduced-by-proof, role explicit-arg]
  19. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `Stream'.append_take_drop`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]

### proof_0134  (target depth 16, band 11-25)

THEOREM PROVED: `Function.argminOn_mem`

Grade all 8 candidates.

   1. `LT.lt`
      [def, depth 1, in-statement, role explicit-arg]
   2. `LT`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Set.Nonempty`
      [def, depth 4, in-statement, role type-annotation]
   4. `Set`
      [def, depth 0, in-statement, role type-annotation]
   5. `Function.argmin._proof_1`
      [theorem, depth 7, in-statement, role explicit-arg]
   6. `WellFoundedLT`
      [def, depth 2, in-statement, role type-annotation]
   7. `InvImage`
      [def, depth 0, in-statement, role implicit-arg]
   8. `WellFounded.min_mem`
      [theorem, depth 15, introduced-by-proof, role applied]

### proof_0135  (target depth 15, band 11-25)

THEOREM PROVED: `norm_toDual`

Grade all 11 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Norm`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Norm.norm`
      [def, depth 1, in-statement, role implicit-arg]
   6. `OrderDual`
      [def, depth 0, in-statement, role implicit-arg]
   7. `OrderDual.toDual`
      [def, depth 11, in-statement, role explicit-arg]
   8. `OrderDual.toNorm`
      [def, depth 14, in-statement, role instance-slot]
   9. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
  10. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  11. `Real`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0136  (target depth 19, band 11-25)

THEOREM PROVED: `CategoryTheory.Iso.unop2_op2`

Grade all 15 candidates.

   1. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   2. `CategoryTheory.Bicategory.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   3. `Bicategory.Opposite.homCategory`
      [def, depth 10, in-statement, role instance-slot]
   4. `rfl`
      [def, depth 2, in-statement, role applied]
   5. `Quiver.Hom.unop`
      [def, depth 3, in-statement, role explicit-arg]
   6. `Opposite.op`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `CategoryTheory.Iso.unop2`
      [def, depth 18, in-statement, role explicit-arg]
   8. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Opposite.unop`
      [def, depth 1, in-statement, role explicit-arg]
  10. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role implicit-arg]
  11. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  12. `CategoryTheory.Iso.op2`
      [def, depth 18, in-statement, role implicit-arg]
  13. `Quiver.Hom.op`
      [def, depth 2, in-statement, role explicit-arg]
  14. `CategoryTheory.Bicategory`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `Quiver.opposite`
      [def, depth 2, in-statement, role instance-slot]

### proof_0137  (target depth 20, band 11-25)

THEOREM PROVED: `Localization.mk_one_eq_monoidOf_mk`

Grade all 14 candidates.

   1. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `CommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   4. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
   5. `Submonoid`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `CommMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
   7. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   8. `rfl`
      [def, depth 2, in-statement, role applied]
   9. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  10. `Submonoid.one`
      [def, depth 13, in-statement, role instance-slot]
  11. `Submonoid.instSetLike`
      [def, depth 10, in-statement, role instance-slot]
  12. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Localization`
      [def, depth 19, in-statement, role implicit-arg]
  14. `Localization.mk`
      [def, depth 19, in-statement, role implicit-arg]

### proof_0138  (target depth 21, band 11-25)

THEOREM PROVED: `UInt16.le_refl`

Grade all 14 candidates.

   1. `UInt16.toBitVec`
      [def, depth 1, in-statement, role explicit-arg]
   2. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
   3. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   5. `Std.le_refl._simp_1`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   6. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   8. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
   9. `_private.Init.Data.UInt.Lemmas.0.UInt16.le_refl._simp_1_1`
      [theorem, depth 17, introduced-by-proof, role explicit-arg]
  10. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  11. `UInt16`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `instLEBitVec`
      [def, depth 13, in-statement, role implicit-arg]
  14. `instLEUInt16`
      [def, depth 15, in-statement, role instance-slot]

### proof_0139  (target depth 25, band 11-25)

THEOREM PROVED: `LieSubalgebra.le_normalizer`

Grade all 16 candidates.

   1. `LieSubalgebra.instSetLike`
      [def, depth 12, in-statement, role instance-slot]
   2. `LieSubalgebra`
      [inductive, depth 2, in-statement, role implicit-arg]
   3. `LieSubalgebra.lieRingModule`
      [def, depth 22, in-statement, role instance-slot]
   4. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   5. `LieAlgebra.toModule`
      [def, depth 2, in-statement, role instance-slot]
   6. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   7. `lieRingSelfModule`
      [def, depth 7, in-statement, role instance-slot]
   8. `LieAlgebra`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `LieSubalgebra.toLieSubmodule`
      [def, depth 23, in-statement, role explicit-arg]
  10. `LieSubalgebra.lieAlgebra`
      [def, depth 23, in-statement, role instance-slot]
  11. `LieRing.toAddCommGroup`
      [def, depth 1, in-statement, role instance-slot]
  12. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `LieSubmodule.le_normalizer`
      [theorem, depth 21, introduced-by-proof, role applied]
  14. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `LieSubalgebra.lieRing`
      [def, depth 21, in-statement, role instance-slot]
  16. `LieRing`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0140  (target depth 19, band 11-25)

THEOREM PROVED: `Nat.max_le_of_le_of_le`

Grade all 17 candidates.

   1. `Or.casesOn`
      [def, depth 3, introduced-by-proof, role applied]
   2. `Nat.max_eq_left`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   3. `instLENat`
      [def, depth 2, in-statement, role instance-slot]
   4. `Or.inr`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   5. `Nat.le_total`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
   6. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Nat.instMax`
      [def, depth 16, in-statement, role instance-slot]
   8. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   9. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
  10. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
  12. `Nat.max_eq_right`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
  13. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  14. `Or`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  15. `Eq.refl`
      [constructor, depth 1, in-statement, role unresolved]
  16. `Or.inl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  17. `Max.max`
      [def, depth 1, in-statement, role explicit-arg]

### proof_0141  (target depth 16, band 11-25)

THEOREM PROVED: `MonotoneOn.monovaryOn`

Grade all 15 candidates.

   1. `MonotoneOn.reflect_lt`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   2. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
   3. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   4. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   5. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   6. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
   7. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   8. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  10. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  12. `MonotoneOn`
      [def, depth 4, in-statement, role type-annotation]
  13. `LT.lt.le`
      [theorem, depth 4, introduced-by-proof, role applied]
  14. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
  15. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]

### proof_0142  (target depth 12, band 11-25)

THEOREM PROVED: `Antitone.of_apply₂`

Grade all 5 candidates.

   1. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
   2. `Antitone`
      [def, depth 2, in-statement, role implicit-arg]
   3. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `antitone_iff_apply₂`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
   5. `Pi.preorder`
      [def, depth 10, in-statement, role instance-slot]

### proof_0143  (target depth 11, band 11-25)

THEOREM PROVED: `eq_top_of_bot_isCompl`

Grade all 12 candidates.

   1. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   2. `IsCompl.symm`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   3. `OrderBot.toBot`
      [def, depth 2, in-statement, role instance-slot]
   4. `Bot.bot`
      [def, depth 1, in-statement, role explicit-arg]
   5. `IsCompl`
      [inductive, depth 2, in-statement, role type-annotation]
   6. `eq_top_of_isCompl_bot`
      [theorem, depth 10, introduced-by-proof, role applied]
   7. `BoundedOrder`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `BoundedOrder.toOrderBot`
      [def, depth 2, in-statement, role instance-slot]
   9. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  10. `Preorder.toLE`
      [def, depth 1, in-statement, role implicit-arg]
  11. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  12. `Lattice`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0144  (target depth 19, band 11-25)

THEOREM PROVED: `Char.eq_of_val_eq`

Grade all 7 candidates.

   1. `_private.Init.Data.Char.Lemmas.0.Char.eq_of_val_eq.match_1_1`
      [def, depth 18, introduced-by-proof, role applied]
   2. `Char`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `UInt32.isValidChar`
      [def, depth 14, introduced-by-proof, role type-annotation]
   4. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `Char.val`
      [def, depth 1, in-statement, role explicit-arg]
   6. `UInt32`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `rfl`
      [def, depth 2, introduced-by-proof, role explicit-arg]
