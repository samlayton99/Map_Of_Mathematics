# Grading batch `testr_09` — 24 proofs

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

### proof_0193  (target depth 36, band 26-50)

THEOREM PROVED: `Int.mul_ediv_cancel_left`

Grade all 14 candidates.

   1. `HDiv.hDiv`
      [def, depth 2, in-statement, role explicit-arg]
   2. `instOfNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `instHDiv`
      [def, depth 3, in-statement, role instance-slot]
   4. `HMul.hMul`
      [def, depth 2, in-statement, role implicit-arg]
   5. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
   7. `Int.instDiv`
      [def, depth 21, in-statement, role instance-slot]
   8. `Int.mul_ediv_cancel`
      [theorem, depth 35, introduced-by-proof, role explicit-arg]
   9. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  10. `Int.mul_comm`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
  11. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Ne`
      [def, depth 2, in-statement, role type-annotation]
  13. `Eq.rec`
      [recursor, depth 2, in-statement, role applied]
  14. `Int.instMul`
      [def, depth 11, in-statement, role instance-slot]

### proof_0194  (target depth 26, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.colimit.ι_inv_pre`

Grade all 22 candidates.

   1. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   2. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   3. `CategoryTheory.IsIso.comp_inv_eq._simp_1`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   6. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   7. `CategoryTheory.inv`
      [def, depth 8, in-statement, role explicit-arg]
   8. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
  10. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  11. `CategoryTheory.Limits.colimit.ι`
      [def, depth 22, in-statement, role explicit-arg]
  12. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  13. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `CategoryTheory.Limits.colimit.ι_pre`
      [theorem, depth 25, introduced-by-proof, role explicit-arg]
  15. `CategoryTheory.IsIso`
      [inductive, depth 2, in-statement, role type-annotation]
  16. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `CategoryTheory.Limits.HasColimit`
      [inductive, depth 2, in-statement, role type-annotation]
  19. `CategoryTheory.Limits.colimit.pre`
      [def, depth 24, in-statement, role explicit-arg]
  20. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  21. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  22. `CategoryTheory.Limits.colimit`
      [def, depth 6, in-statement, role implicit-arg]

### proof_0195  (target depth 39, band 26-50)

THEOREM PROVED: `PointedCone.isFaceOf_map_iff`

Grade all 18 candidates.

   1. `PointedCone.IsFaceOf.of_map_injective`
      [theorem, depth 38, introduced-by-proof, role explicit-arg]
   2. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `LinearMap`
      [inductive, depth 11, in-statement, role implicit-arg]
   4. `LinearMap.instFunLike`
      [def, depth 20, in-statement, role instance-slot]
   5. `PointedCone.map`
      [def, depth 34, in-statement, role explicit-arg]
   6. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
  10. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  11. `IsOrderedRing`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  13. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
  14. `PointedCone.IsFaceOf`
      [inductive, depth 34, in-statement, role implicit-arg]
  15. `Function.Injective`
      [def, depth 1, in-statement, role type-annotation]
  16. `PointedCone.IsFaceOf.map`
      [theorem, depth 36, introduced-by-proof, role explicit-arg]
  17. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]
  18. `PointedCone`
      [def, depth 33, in-statement, role type-annotation]

### proof_0196  (target depth 44, band 26-50)

THEOREM PROVED: `NNRat.commute_cast`

Grade all 9 candidates.

   1. `DivisionSemiring.toNNRatCast`
      [def, depth 1, in-statement, role instance-slot]
   2. `NNRat`
      [def, depth 39, in-statement, role type-annotation]
   3. `DivisionSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `NNRat.cast_commute`
      [theorem, depth 43, introduced-by-proof, role explicit-arg]
   5. `Commute.symm`
      [theorem, depth 6, introduced-by-proof, role applied]
   6. `Distrib.toMul`
      [def, depth 1, in-statement, role instance-slot]
   7. `DivisionSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   8. `NNRat.cast`
      [def, depth 2, in-statement, role implicit-arg]
   9. `instDistribOfSemiring`
      [def, depth 11, in-statement, role instance-slot]

### proof_0197  (target depth 39, band 26-50)

THEOREM PROVED: `Int.gcd_add_left_left_of_dvd`

Grade all 16 candidates.

   1. `Int.instDvd`
      [def, depth 12, in-statement, role instance-slot]
   2. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
   5. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   6. `Int.gcd_mul_left_add_left`
      [theorem, depth 38, introduced-by-proof, role explicit-arg]
   7. `Int.instMul`
      [def, depth 11, in-statement, role instance-slot]
   8. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Int.gcd`
      [def, depth 25, in-statement, role explicit-arg]
  11. `Exists.casesOn`
      [def, depth 3, introduced-by-proof, role applied]
  12. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
  13. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `Int.instAdd`
      [def, depth 11, in-statement, role instance-slot]
  16. `Dvd.dvd`
      [def, depth 1, in-statement, role type-annotation]

### proof_0198  (target depth 34, band 26-50)

THEOREM PROVED: `zpow_iterate`

Grade all 14 candidates.

   1. `Nat.iterate`
      [def, depth 6, in-statement, role explicit-arg]
   2. `instHPow`
      [def, depth 3, in-statement, role instance-slot]
   3. `HPow.hPow`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Int.instNatPow`
      [def, depth 22, in-statement, role instance-slot]
   5. `ZPow.toPow`
      [def, depth 2, in-statement, role instance-slot]
   6. `Nat.brecOn`
      [def, depth 5, in-statement, role applied]
   7. `zpow_iterate._f`
      [def, depth 33, introduced-by-proof, role explicit-arg]
   8. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `DivInvMonoid.toZPow`
      [def, depth 1, in-statement, role instance-slot]
  10. `instPowNat`
      [def, depth 2, in-statement, role instance-slot]
  11. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
  13. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0199  (target depth 31, band 26-50)

THEOREM PROVED: `USize.toBitVec32_mod`

Grade all 22 candidates.

   1. `id`
      [def, depth 0, in-statement, role explicit-arg]
   2. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   4. `USize.toBitVec32`
      [def, depth 15, in-statement, role explicit-arg]
   5. `USize.toBitVec`
      [def, depth 1, in-statement, role explicit-arg]
   6. `HMod.hMod`
      [def, depth 2, in-statement, role explicit-arg]
   7. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   8. `USize`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  10. `instModUSize`
      [def, depth 29, in-statement, role instance-slot]
  11. `instHMod`
      [def, depth 3, in-statement, role instance-slot]
  12. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `BitVec.cast`
      [def, depth 14, in-statement, role explicit-arg]
  14. `System.Platform.numBits`
      [def, depth 6, in-statement, role explicit-arg]
  15. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  16. `USize.toBitVec_mod`
      [theorem, depth 30, introduced-by-proof, role explicit-arg]
  17. `Eq.rec`
      [recursor, depth 2, in-statement, role explicit-arg]
  18. `BitVec.cast.congr_simp`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
  19. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
  20. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  22. `BitVec.instMod`
      [def, depth 27, in-statement, role instance-slot]

### proof_0200  (target depth 33, band 26-50)

THEOREM PROVED: `Std.Tactic.BVDecide.Frontend.Normalize.BitVec.add_right_inj`

Grade all 24 candidates.

   1. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `BEq.beq`
      [def, depth 1, in-statement, role explicit-arg]
   3. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   6. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `instBEqOfDecidableEq`
      [def, depth 6, in-statement, role instance-slot]
   8. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `BitVec.add_right_inj._simp_1`
      [theorem, depth 32, introduced-by-proof, role explicit-arg]
  10. `beq_iff_eq._simp_1`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
  11. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `instDecidableEqBitVec`
      [def, depth 19, in-statement, role instance-slot]
  14. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  15. `Bool.eq_iff_iff`
      [theorem, depth 10, introduced-by-proof, role explicit-arg]
  16. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  17. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  18. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  19. `BitVec.instAdd`
      [def, depth 25, in-statement, role instance-slot]
  20. `id`
      [def, depth 0, in-statement, role explicit-arg]
  21. `iff_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  22. `propext`
      [axiom, depth 1, introduced-by-proof, role explicit-arg]
  23. `Iff`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  24. `BitVec`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0201  (target depth 28, band 26-50)

THEOREM PROVED: `UInt32.ofNatTruncate_finVal`

Grade all 3 candidates.

   1. `Fin`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `UInt32.size`
      [def, depth 4, in-statement, role explicit-arg]
   3. `UInt32.ofNatClamp_finVal`
      [theorem, depth 27, introduced-by-proof, role applied]

### proof_0202  (target depth 26, band 26-50)

THEOREM PROVED: `CategoryTheory.Iso.conjAut_apply`

Grade all 24 candidates.

   1. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   3. `CategoryTheory.Aut`
      [def, depth 2, in-statement, role implicit-arg]
   4. `MulEquiv`
      [inductive, depth 1, in-statement, role implicit-arg]
   5. `id`
      [def, depth 0, in-statement, role explicit-arg]
   6. `CategoryTheory.Aut.ext`
      [theorem, depth 15, introduced-by-proof, role applied]
   7. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
   8. `CategoryTheory.Iso.symm`
      [def, depth 15, in-statement, role explicit-arg]
   9. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  11. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  12. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  13. `MulEquiv.instEquivLike`
      [def, depth 16, in-statement, role instance-slot]
  14. `CategoryTheory.Iso.conjAut`
      [def, depth 25, in-statement, role explicit-arg]
  15. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  17. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  18. `CategoryTheory.Iso.trans`
      [def, depth 15, in-statement, role explicit-arg]
  19. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  20. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  21. `CategoryTheory.Aut.instGroup`
      [def, depth 19, in-statement, role instance-slot]
  22. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  23. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  24. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]

### proof_0203  (target depth 44, band 26-50)

THEOREM PROVED: `CategoryTheory.coalgebraToOver_map`

Grade all 20 candidates.

   1. `CategoryTheory.Over.mk`
      [def, depth 24, in-statement, role explicit-arg]
   2. `CategoryTheory.Over`
      [def, depth 24, in-statement, role implicit-arg]
   3. `CategoryTheory.Limits.prod.fst`
      [def, depth 23, in-statement, role explicit-arg]
   4. `CategoryTheory.Comonad.toFunctor`
      [def, depth 2, in-statement, role explicit-arg]
   5. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role implicit-arg]
   6. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   8. `CategoryTheory.prodComonad`
      [def, depth 40, in-statement, role explicit-arg]
   9. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  10. `CategoryTheory.Comonad.Coalgebra.eilenbergMoore`
      [def, depth 16, in-statement, role instance-slot]
  11. `CategoryTheory.instCategoryOver`
      [def, depth 26, in-statement, role instance-slot]
  12. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  13. `CategoryTheory.Limits.HasBinaryProducts`
      [def, depth 11, in-statement, role type-annotation]
  14. `CategoryTheory.Comonad.Coalgebra`
      [inductive, depth 2, in-statement, role implicit-arg]
  15. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  16. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `CategoryTheory.Functor.map`
      [def, depth 2, in-statement, role explicit-arg]
  18. `CategoryTheory.Comonad.Coalgebra.A`
      [def, depth 3, in-statement, role explicit-arg]
  19. `CategoryTheory.coalgebraToOver`
      [def, depth 43, in-statement, role explicit-arg]
  20. `CategoryTheory.Comonad.Coalgebra.a`
      [def, depth 3, in-statement, role explicit-arg]

### proof_0204  (target depth 33, band 26-50)

THEOREM PROVED: `CategoryTheory.MonoidalOpposite.mopMopEquivalenceInverseMonoidal_η_unmop_unmop`

Grade all 18 candidates.

   1. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   4. `CategoryTheory.MonoidalOpposite.unmop`
      [def, depth 1, in-statement, role explicit-arg]
   5. `CategoryTheory.Equivalence.inverse`
      [def, depth 2, in-statement, role explicit-arg]
   6. `CategoryTheory.MonoidalOpposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `CategoryTheory.Functor.Monoidal.toOplaxMonoidal`
      [def, depth 3, in-statement, role instance-slot]
   8. `CategoryTheory.Functor.OplaxMonoidal.η`
      [def, depth 3, in-statement, role explicit-arg]
   9. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `CategoryTheory.monoidalCategoryMop`
      [def, depth 25, in-statement, role implicit-arg]
  12. `CategoryTheory.MonoidalCategoryStruct.tensorUnit`
      [def, depth 2, in-statement, role explicit-arg]
  13. `CategoryTheory.MonoidalOpposite.monoidalOppositeCategory`
      [def, depth 10, in-statement, role instance-slot]
  14. `CategoryTheory.MonoidalOpposite.mopMopEquivalenceInverseMonoidal`
      [def, depth 32, in-statement, role instance-slot]
  15. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  16. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  17. `CategoryTheory.MonoidalOpposite.mopMopEquivalence`
      [def, depth 30, in-statement, role explicit-arg]
  18. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]

### proof_0205  (target depth 43, band 26-50)

THEOREM PROVED: `Int64.toBitVec64_toISize`

Grade all 22 candidates.

   1. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   2. `ISize.toBitVec`
      [def, depth 2, in-statement, role explicit-arg]
   3. `id`
      [def, depth 0, in-statement, role explicit-arg]
   4. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   5. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   7. `System.Platform.numBits`
      [def, depth 6, in-statement, role explicit-arg]
   8. `Int64.toBitVec_toISize`
      [theorem, depth 42, introduced-by-proof, role explicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Int64.toISize`
      [def, depth 41, in-statement, role explicit-arg]
  11. `ISize.toBitVec64`
      [def, depth 15, in-statement, role explicit-arg]
  12. `Int64`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `BitVec.cast`
      [def, depth 14, in-statement, role explicit-arg]
  14. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  15. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
  16. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  17. `BitVec.cast.congr_simp`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
  18. `Int64.toBitVec`
      [def, depth 2, in-statement, role explicit-arg]
  19. `Eq.rec`
      [recursor, depth 2, in-statement, role explicit-arg]
  20. `BitVec.signExtend`
      [def, depth 40, in-statement, role explicit-arg]
  21. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  22. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0206  (target depth 30, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.hasLimitsOfSize_opposite_iff`

Grade all 8 candidates.

   1. `Opposite`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.Limits.HasColimitsOfSize`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
   5. `CategoryTheory.Limits.hasColimits_of_hasLimits_op`
      [theorem, depth 28, introduced-by-proof, role explicit-arg]
   6. `inferInstance`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   7. `CategoryTheory.Limits.HasLimitsOfSize`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]

### proof_0207  (target depth 30, band 26-50)

THEOREM PROVED: `Frm.Iso.mk_hom`

Grade all 17 candidates.

   1. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Frm`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   4. `CompleteLattice.toCompleteSemilatticeInf`
      [def, depth 8, in-statement, role instance-slot]
   5. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   6. `Frm.instCategory`
      [def, depth 19, in-statement, role instance-slot]
   7. `CompleteSemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   8. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   9. `Frm.carrier`
      [def, depth 1, in-statement, role explicit-arg]
  10. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  11. `OrderIso`
      [def, depth 2, in-statement, role type-annotation]
  12. `Frm.Iso.mk`
      [def, depth 29, in-statement, role explicit-arg]
  13. `Frm.of`
      [constructor, depth 1, in-statement, role explicit-arg]
  14. `Order.Frame.toCompleteLattice`
      [def, depth 1, in-statement, role instance-slot]
  15. `Frm.str`
      [def, depth 1, in-statement, role instance-slot]
  16. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  17. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]

### proof_0208  (target depth 32, band 26-50)

THEOREM PROVED: `Int.lt_min`

Grade all 7 candidates.

   1. `HAdd.hAdd`
      [def, depth 2, in-statement, role implicit-arg]
   2. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `instOfNat`
      [def, depth 3, in-statement, role instance-slot]
   5. `Int.le_min`
      [theorem, depth 31, introduced-by-proof, role applied]
   6. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Int.instAdd`
      [def, depth 11, in-statement, role instance-slot]

### proof_0209  (target depth 36, band 26-50)

THEOREM PROVED: `Mathlib.Meta.NormNum.isNat_ordinalMul`

Grade all 18 candidates.

   1. `Ordinal.natCast_mul`
      [theorem, depth 35, introduced-by-proof, role explicit-arg]
   2. `Mathlib.Meta.NormNum.IsNat.mk`
      [constructor, depth 3, introduced-by-proof, role explicit-arg]
   3. `MulZeroClass.toMul`
      [def, depth 1, in-statement, role instance-slot]
   4. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Nat.cast`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   7. `_private.Mathlib.Tactic.NormNum.Ordinal.0.Mathlib.Meta.NormNum.isNat_ordinalMul.match_1_1`
      [def, depth 31, introduced-by-proof, role applied]
   8. `Mathlib.Meta.NormNum.IsNat`
      [inductive, depth 1, in-statement, role explicit-arg]
   9. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  10. `Ordinal.addMonoidWithOne`
      [def, depth 30, in-statement, role instance-slot]
  11. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  12. `AddMonoidWithOne.toNatCast`
      [def, depth 1, introduced-by-proof, role instance-slot]
  13. `Ordinal.monoidWithZero`
      [def, depth 32, in-statement, role instance-slot]
  14. `MonoidWithZero.toMulZeroOneClass`
      [def, depth 5, in-statement, role instance-slot]
  15. `MulZeroOneClass.toMulZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  16. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  17. `Ordinal`
      [def, depth 25, in-statement, role implicit-arg]
  18. `instMulNat`
      [def, depth 9, in-statement, role instance-slot]

### proof_0210  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.coprod.inl_fst_assoc`

Grade all 21 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `CategoryTheory.Limits.HasZeroMorphisms`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   4. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]
   5. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `CategoryTheory.Limits.coprod.inl_fst`
      [theorem, depth 26, introduced-by-proof, role explicit-arg]
   7. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   8. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   9. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role explicit-arg]
  10. `CategoryTheory.Category.assoc`
      [theorem, depth 1, in-statement, role explicit-arg]
  11. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  12. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  13. `id`
      [def, depth 0, in-statement, role applied]
  14. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  15. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  16. `CategoryTheory.Limits.HasBinaryCoproduct`
      [def, depth 14, in-statement, role type-annotation]
  17. `CategoryTheory.Limits.coprod`
      [def, depth 15, in-statement, role implicit-arg]
  18. `CategoryTheory.Limits.coprod.inl`
      [def, depth 23, in-statement, role explicit-arg]
  19. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `CategoryTheory.Category.id_comp`
      [theorem, depth 1, in-statement, role explicit-arg]
  21. `CategoryTheory.Limits.coprod.fst`
      [def, depth 25, in-statement, role explicit-arg]

### proof_0211  (target depth 32, band 26-50)

THEOREM PROVED: `CategoryTheory.SimplicialObject.whiskering_obj_obj_δ`

Grade all 24 candidates.

   1. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   2. `SimplexCategory`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   6. `CategoryTheory.SimplicialObject`
      [def, depth 30, in-statement, role explicit-arg]
   7. `Fin`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   9. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  11. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  12. `CategoryTheory.SimplicialObject.whiskering`
      [def, depth 30, in-statement, role explicit-arg]
  13. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
  14. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  15. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  16. `rfl`
      [def, depth 2, in-statement, role applied]
  17. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  18. `CategoryTheory.SimplicialObject.δ`
      [def, depth 31, in-statement, role implicit-arg]
  19. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `Opposite.op`
      [constructor, depth 1, in-statement, role explicit-arg]
  21. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  22. `SimplexCategory.smallCategory`
      [def, depth 29, in-statement, role instance-slot]
  23. `SimplexCategory.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  24. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]

### proof_0212  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.LaxMonoidalFunctor.id_hom`

Grade all 13 candidates.

   1. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   2. `CategoryTheory.LaxMonoidalFunctor.instCategory`
      [def, depth 26, in-statement, role instance-slot]
   3. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role explicit-arg]
   5. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CategoryTheory.LaxMonoidalFunctor.Hom.hom`
      [def, depth 4, in-statement, role implicit-arg]
   7. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   8. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  10. `CategoryTheory.LaxMonoidalFunctor.toFunctor`
      [def, depth 3, in-statement, role explicit-arg]
  11. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  12. `CategoryTheory.LaxMonoidalFunctor`
      [inductive, depth 2, in-statement, role implicit-arg]
  13. `rfl`
      [def, depth 2, in-statement, role applied]

### proof_0213  (target depth 26, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.Types.jointly_surjective`

Grade all 7 candidates.

   1. `CategoryTheory.Limits.Cocone`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `CategoryTheory.Limits.IsColimit`
      [inductive, depth 3, in-statement, role type-annotation]
   3. `CategoryTheory.types`
      [def, depth 10, in-statement, role instance-slot]
   4. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `CategoryTheory.Limits.Types.jointly_surjective_of_isColimit`
      [theorem, depth 25, introduced-by-proof, role applied]
   6. `CategoryTheory.Limits.Cocone.pt`
      [def, depth 3, in-statement, role type-annotation]
   7. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0214  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.Discrete.equivalence_counitIso`

Grade all 18 candidates.

   1. `CategoryTheory.Discrete.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `CategoryTheory.Discrete.equivalence`
      [def, depth 26, in-statement, role explicit-arg]
   3. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   4. `CategoryTheory.Functor.id`
      [def, depth 10, in-statement, role explicit-arg]
   5. `Equiv.symm`
      [def, depth 10, in-statement, role explicit-arg]
   6. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   8. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `CategoryTheory.discreteCategory`
      [def, depth 10, in-statement, role instance-slot]
  10. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  11. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  12. `CategoryTheory.Discrete.functor`
      [def, depth 12, in-statement, role explicit-arg]
  13. `CategoryTheory.Discrete`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  15. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  16. `CategoryTheory.Equivalence.counitIso`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
  18. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]

### proof_0215  (target depth 41, band 26-50)

THEOREM PROVED: `CategoryTheory.ShortComplex.Homotopy.symm_h₂`

Grade all 14 candidates.

   1. `CategoryTheory.ShortComplex.Homotopy`
      [inductive, depth 18, in-statement, role type-annotation]
   2. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   3. `CategoryTheory.ShortComplex.instCategory`
      [def, depth 15, in-statement, role instance-slot]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.ShortComplex.X₃`
      [def, depth 3, in-statement, role explicit-arg]
   6. `CategoryTheory.Preadditive`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `CategoryTheory.ShortComplex.Homotopy.h₂`
      [def, depth 19, in-statement, role explicit-arg]
   8. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   9. `CategoryTheory.ShortComplex.Homotopy.symm`
      [def, depth 40, in-statement, role explicit-arg]
  10. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  11. `CategoryTheory.ShortComplex.X₂`
      [def, depth 3, in-statement, role explicit-arg]
  12. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `CategoryTheory.ShortComplex`
      [inductive, depth 2, in-statement, role implicit-arg]
  14. `CategoryTheory.Preadditive.preadditiveHasZeroMorphisms`
      [def, depth 17, in-statement, role instance-slot]

### proof_0216  (target depth 31, band 26-50)

THEOREM PROVED: `DirectLimit.Ring.lift_of`

Grade all 18 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   5. `DirectedSystem`
      [inductive, depth 2, in-statement, role type-annotation]
   6. `DirectLimit.Ring.of`
      [def, depth 30, in-statement, role explicit-arg]
   7. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `RingHom.instFunLike`
      [def, depth 15, in-statement, role instance-slot]
   9. `RingHom`
      [inductive, depth 1, in-statement, role implicit-arg]
  10. `IsDirectedOrder`
      [def, depth 2, in-statement, role type-annotation]
  11. `RingHomClass`
      [inductive, depth 3, in-statement, role type-annotation]
  12. `DirectLimit`
      [def, depth 8, in-statement, role implicit-arg]
  13. `FunLike`
      [def, depth 2, in-statement, role type-annotation]
  14. `Nonempty`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `DirectLimit.Ring.lift`
      [def, depth 30, in-statement, role explicit-arg]
  16. `DirectLimit.instNonAssocSemiringOfRingHomClass`
      [def, depth 28, in-statement, role implicit-arg]
  17. `NonAssocSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
