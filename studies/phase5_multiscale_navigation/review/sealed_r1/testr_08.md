# Grading batch `testr_08` — 24 proofs

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

### proof_0169  (target depth 17, band 11-25)

THEOREM PROVED: `Stream'.WSeq.think_append`

Grade all 4 candidates.

   1. `Option.none`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Stream'.Seq.cons_append`
      [theorem, depth 16, introduced-by-proof, role applied]
   3. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Stream'.WSeq`
      [def, depth 10, in-statement, role type-annotation]

### proof_0170  (target depth 21, band 11-25)

THEOREM PROVED: `SimpleGraph.adjMatrix_hadamard_ofNat`

Grade all 10 candidates.

   1. `MulZeroOneClass`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Nat.cast`
      [def, depth 2, in-statement, role explicit-arg]
   3. `SimpleGraph.Adj`
      [def, depth 1, in-statement, role explicit-arg]
   4. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   6. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `NatCast`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `SimpleGraph.adjMatrix_hadamard_diagonal`
      [theorem, depth 20, introduced-by-proof, role applied]
   9. `DecidableRel`
      [def, depth 1, in-statement, role type-annotation]
  10. `Nat.AtLeastTwo`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0171  (target depth 14, band 11-25)

THEOREM PROVED: `Nat.Simproc.bneEqOfEqEq`

Grade all 15 candidates.

   1. `instBEqOfDecidableEq`
      [def, depth 6, in-statement, role instance-slot]
   2. `BEq.beq`
      [def, depth 1, in-statement, role implicit-arg]
   3. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Bool.not`
      [def, depth 5, in-statement, role explicit-arg]
   6. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   7. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  10. `bne`
      [def, depth 6, in-statement, role explicit-arg]
  11. `Nat.Simproc.beqEqOfEqEq`
      [theorem, depth 13, introduced-by-proof, role explicit-arg]
  12. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `instDecidableEqNat`
      [def, depth 11, in-statement, role instance-slot]
  14. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  15. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]

### proof_0172  (target depth 12, band 11-25)

THEOREM PROVED: `CategoryTheory.reflectsIsomorphisms_of_reflectsMonomorphisms_of_reflectsEpimorphisms`

Grade all 18 candidates.

   1. `CategoryTheory.IsIso`
      [inductive, depth 2, introduced-by-proof, role type-annotation]
   2. `CategoryTheory.Functor.obj`
      [def, depth 2, introduced-by-proof, role implicit-arg]
   3. `CategoryTheory.isIso_of_mono_of_epi`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   4. `CategoryTheory.Balanced`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, introduced-by-proof, role instance-slot]
   6. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, introduced-by-proof, role instance-slot]
   7. `CategoryTheory.Functor.mono_of_mono_map`
      [theorem, depth 4, introduced-by-proof, role let-value]
   8. `CategoryTheory.Functor.ReflectsIsomorphisms.mk`
      [constructor, depth 3, introduced-by-proof, role applied]
   9. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `CategoryTheory.Epi`
      [inductive, depth 2, introduced-by-proof, role implicit-arg]
  11. `inferInstance`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  12. `CategoryTheory.Functor.ReflectsEpimorphisms`
      [inductive, depth 2, in-statement, role type-annotation]
  13. `CategoryTheory.Mono`
      [inductive, depth 2, introduced-by-proof, role implicit-arg]
  14. `CategoryTheory.Functor.epi_of_epi_map`
      [theorem, depth 4, introduced-by-proof, role let-value]
  15. `CategoryTheory.Functor.map`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  16. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `Quiver.Hom`
      [def, depth 1, introduced-by-proof, role type-annotation]
  18. `CategoryTheory.Functor.ReflectsMonomorphisms`
      [inductive, depth 2, in-statement, role type-annotation]

### proof_0173  (target depth 22, band 11-25)

THEOREM PROVED: `LinearMap.map_add`

Grade all 11 candidates.

   1. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   2. `AddCommMagma.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   3. `AddCommMonoid.toAddCommSemigroup`
      [def, depth 5, in-statement, role instance-slot]
   4. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `LinearMap`
      [inductive, depth 11, in-statement, role implicit-arg]
   6. `RingHom`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `LinearMap.instFunLike`
      [def, depth 20, in-statement, role implicit-arg]
   9. `map_add`
      [theorem, depth 5, introduced-by-proof, role applied]
  10. `AddCommSemigroup.toAddCommMagma`
      [def, depth 5, in-statement, role instance-slot]
  11. `Module`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0174  (target depth 11, band 11-25)

THEOREM PROVED: `SimpleGraph.Connected.mono`

Grade all 7 candidates.

   1. `SimpleGraph.Connected.mk`
      [constructor, depth 4, introduced-by-proof, role applied]
   2. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `SimpleGraph.Connected.preconnected`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   4. `SimpleGraph.instLE`
      [def, depth 2, in-statement, role instance-slot]
   5. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   6. `SimpleGraph.Connected`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `SimpleGraph.Preconnected.mono`
      [theorem, depth 10, introduced-by-proof, role explicit-arg]

### proof_0175  (target depth 23, band 11-25)

THEOREM PROVED: `CategoryTheory.Functor.FullyFaithful.autMulEquivOfFullyFaithful_symm_apply_hom`

Grade all 23 candidates.

   1. `CategoryTheory.Aut.instGroup`
      [def, depth 19, in-statement, role instance-slot]
   2. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
   3. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   4. `CategoryTheory.Aut`
      [def, depth 2, in-statement, role implicit-arg]
   5. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   6. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   8. `MulEquiv`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `CategoryTheory.Functor.FullyFaithful`
      [inductive, depth 2, in-statement, role type-annotation]
  10. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  11. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `MulEquiv.symm`
      [def, depth 15, in-statement, role explicit-arg]
  13. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
  15. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  16. `MulEquiv.instEquivLike`
      [def, depth 16, in-statement, role instance-slot]
  17. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  18. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
  19. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  20. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  21. `CategoryTheory.Functor.FullyFaithful.autMulEquivOfFullyFaithful`
      [def, depth 22, in-statement, role explicit-arg]
  22. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
  23. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0176  (target depth 15, band 11-25)

THEOREM PROVED: `List.mem_rtakeWhile_imp`

Grade all 13 candidates.

   1. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Bool`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   4. `List.rtakeWhile`
      [def, depth 8, in-statement, role explicit-arg]
   5. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   6. `List.takeWhile`
      [def, depth 6, in-statement, role explicit-arg]
   7. `List.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   8. `propext`
      [axiom, depth 1, introduced-by-proof, role explicit-arg]
   9. `List.reverse`
      [def, depth 7, in-statement, role explicit-arg]
  10. `List.mem_reverse`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
  11. `List.mem_takeWhile_imp`
      [theorem, depth 13, introduced-by-proof, role applied]
  12. `List.rtakeWhile.eq_1`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
  13. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]

### proof_0177  (target depth 25, band 11-25)

THEOREM PROVED: `Fin.succ_one_eq_two'`

Grade all 20 candidates.

   1. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
   2. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `Fin.succ`
      [def, depth 10, in-statement, role explicit-arg]
   4. `Zero.ofOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   5. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
   7. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   8. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  10. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
  11. `Fin.instOfNat`
      [def, depth 24, in-statement, role instance-slot]
  12. `Nat.casesAuxOn`
      [def, depth 8, introduced-by-proof, role applied]
  13. `NeZero.ne`
      [theorem, depth 3, in-statement, role explicit-arg]
  14. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
  15. `NeZero`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `False.elim`
      [def, depth 2, in-statement, role explicit-arg]
  17. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  18. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  19. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_0178  (target depth 17, band 11-25)

THEOREM PROVED: `max_mul_mul_right`

Grade all 19 candidates.

   1. `Monotone.mul_const'`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   2. `Mul`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
   4. `MulRightMono`
      [def, depth 4, in-statement, role type-annotation]
   5. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Monotone.map_max`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
   7. `Max.max`
      [def, depth 1, in-statement, role explicit-arg]
   8. `Lattice.toSemilatticeSup`
      [def, depth 1, in-statement, role instance-slot]
   9. `monotone_id`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  10. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  11. `LinearOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `id`
      [def, depth 0, in-statement, role explicit-arg]
  13. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  14. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  15. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  16. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  17. `SemilatticeSup.toMax`
      [def, depth 2, in-statement, role instance-slot]
  18. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  19. `Eq.symm`
      [theorem, depth 3, in-statement, role applied]

### proof_0179  (target depth 18, band 11-25)

THEOREM PROVED: `MonoidHom.mem_ker`

Grade all 13 candidates.

   1. `MonoidHom`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   3. `Subgroup.instSetLike`
      [def, depth 16, in-statement, role instance-slot]
   4. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   6. `Subgroup`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   8. `MonoidHom.ker`
      [def, depth 17, in-statement, role explicit-arg]
   9. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
  10. `Iff.rfl`
      [theorem, depth 3, in-statement, role applied]
  11. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  12. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  13. `MulOneClass`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0180  (target depth 24, band 11-25)

THEOREM PROVED: `MonoidHom.mulExact_of_comp_of_mem_range`

Grade all 23 candidates.

   1. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
   2. `MonoidHom.mulExact_of_comp_eq_one_of_ker_le_range`
      [theorem, depth 23, introduced-by-proof, role applied]
   3. `MonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
   4. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
   5. `MonoidHom.range`
      [def, depth 22, in-statement, role explicit-arg]
   6. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   7. `Subgroup`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `DivisionMonoid.toDivInvOneMonoid`
      [def, depth 9, in-statement, role instance-slot]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  10. `instOneMonoidHom`
      [def, depth 5, in-statement, role instance-slot]
  11. `Subgroup.instSetLike`
      [def, depth 16, in-statement, role instance-slot]
  12. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  13. `Group.toDivisionMonoid`
      [def, depth 11, in-statement, role instance-slot]
  14. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  15. `MonoidHom.comp`
      [def, depth 13, in-statement, role explicit-arg]
  16. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  17. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  18. `DivInvOneMonoid.toInvOneClass`
      [def, depth 5, in-statement, role instance-slot]
  19. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `InvOneClass.toOne`
      [def, depth 1, in-statement, role instance-slot]
  21. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  22. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
  23. `MonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0181  (target depth 14, band 11-25)

THEOREM PROVED: `isRightRegular_toDual`

Grade all 13 candidates.

   1. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   2. `OrderDual.instMul`
      [def, depth 1, in-statement, role instance-slot]
   3. `OrderDual.toDual`
      [def, depth 11, in-statement, role explicit-arg]
   4. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   5. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `OrderDual`
      [def, depth 0, in-statement, role implicit-arg]
   7. `Monoid`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   9. `Iff.rfl`
      [theorem, depth 3, introduced-by-proof, role applied]
  10. `IsRightRegular`
      [def, depth 4, in-statement, role implicit-arg]
  11. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
  12. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  13. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]

### proof_0182  (target depth 21, band 11-25)

THEOREM PROVED: `CategoryTheory.Discrete.addMonoidalFunctor_δ`

Grade all 18 candidates.

   1. `CategoryTheory.Discrete.addMonoidalFunctorMonoidal`
      [def, depth 20, in-statement, role instance-slot]
   2. `CategoryTheory.Discrete.addMonoidalFunctor`
      [def, depth 13, in-statement, role explicit-arg]
   3. `CategoryTheory.MonoidalCategoryStruct.tensorObj`
      [def, depth 2, in-statement, role explicit-arg]
   4. `CategoryTheory.discreteCategory`
      [def, depth 10, in-statement, role implicit-arg]
   5. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   6. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   8. `CategoryTheory.Functor.OplaxMonoidal.δ`
      [def, depth 3, in-statement, role implicit-arg]
   9. `CategoryTheory.Discrete`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `CategoryTheory.Discrete.addMonoidal`
      [def, depth 14, in-statement, role implicit-arg]
  11. `AddMonoidHom`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
  13. `CategoryTheory.Functor.Monoidal.toOplaxMonoidal`
      [def, depth 3, in-statement, role instance-slot]
  14. `rfl`
      [def, depth 2, in-statement, role applied]
  15. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  16. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  18. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0183  (target depth 11, band 11-25)

THEOREM PROVED: `NonUnitalAlgHom.toFun_eq_coe`

Grade all 21 candidates.

   1. `NonUnitalAlgHom.toDistribMulActionHom`
      [def, depth 7, in-statement, role explicit-arg]
   2. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   3. `AddZero.toZero`
      [def, depth 1, in-statement, role implicit-arg]
   4. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   5. `DistribSMul.toSMulZeroClass`
      [def, depth 2, in-statement, role instance-slot]
   6. `MulActionHom.toFun`
      [def, depth 2, in-statement, role implicit-arg]
   7. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   8. `rfl`
      [def, depth 2, in-statement, role applied]
   9. `MonoidHom.instFunLike`
      [def, depth 10, in-statement, role instance-slot]
  10. `DistribMulActionHom.toMulActionHom`
      [def, depth 7, in-statement, role explicit-arg]
  11. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role implicit-arg]
  12. `NonUnitalNonAssocSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
  14. `AddCommMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  15. `DistribMulAction.toDistribSMul`
      [def, depth 6, in-statement, role instance-slot]
  16. `DistribMulAction`
      [inductive, depth 1, in-statement, role type-annotation]
  17. `MonoidHom`
      [inductive, depth 1, in-statement, role implicit-arg]
  18. `SMulZeroClass.toSMul`
      [def, depth 2, in-statement, role instance-slot]
  19. `Monoid`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `NonUnitalAlgHom`
      [inductive, depth 6, in-statement, role type-annotation]
  21. `NonUnitalNonAssocSemiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]

### proof_0184  (target depth 18, band 11-25)

THEOREM PROVED: `Set.image_domRestrict`

Grade all 22 candidates.

   1. `Set.instInter`
      [def, depth 5, in-statement, role instance-slot]
   2. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   3. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Set.image_preimage_eq_inter_range`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
   6. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   7. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
   8. `Set.range`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   9. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
  10. `Set.Elem`
      [def, depth 4, in-statement, role implicit-arg]
  11. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  12. `Set.domRestrict_eq`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
  13. `Inter.inter`
      [def, depth 1, in-statement, role explicit-arg]
  14. `Function.comp`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  15. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  16. `Set.preimage`
      [def, depth 4, in-statement, role explicit-arg]
  17. `Set.image_comp`
      [theorem, depth 8, introduced-by-proof, role explicit-arg]
  18. `Subtype.range_coe`
      [theorem, depth 17, introduced-by-proof, role explicit-arg]
  19. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `Set.image`
      [def, depth 4, in-statement, role explicit-arg]
  21. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
  22. `Set.domRestrict`
      [def, depth 5, in-statement, role explicit-arg]

### proof_0185  (target depth 14, band 11-25)

THEOREM PROVED: `Nat.one_add_sub_one`

Grade all 4 candidates.

   1. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   2. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Nat.add_sub_cancel_left`
      [theorem, depth 13, introduced-by-proof, role applied]

### proof_0186  (target depth 18, band 11-25)

THEOREM PROVED: `SimpleGraph.Subgraph.edgeSet_map`

Grade all 9 candidates.

   1. `SimpleGraph.Adj`
      [def, depth 1, in-statement, role implicit-arg]
   2. `SimpleGraph.Subgraph.symm`
      [theorem, depth 2, in-statement, role explicit-arg]
   3. `SimpleGraph.Subgraph`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `SimpleGraph.Hom`
      [def, depth 2, in-statement, role implicit-arg]
   5. `RelHom.instFunLike`
      [def, depth 5, in-statement, role instance-slot]
   6. `SimpleGraph.Subgraph.Adj`
      [def, depth 2, in-statement, role implicit-arg]
   7. `Sym2.fromRel_relationMap`
      [theorem, depth 17, introduced-by-proof, role applied]
   8. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0187  (target depth 12, band 11-25)

THEOREM PROVED: `CategoryTheory.homOfLE_comp_eqToHom_assoc`

Grade all 21 candidates.

   1. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   2. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.homOfLE`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   5. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   6. `LE.le.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   7. `CategoryTheory.eqToHom`
      [def, depth 5, in-statement, role explicit-arg]
   8. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   9. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  10. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  12. `le_of_eq`
      [theorem, depth 5, in-statement, role explicit-arg]
  13. `CategoryTheory.homOfLE_comp_eqToHom`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
  14. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  15. `id`
      [def, depth 0, in-statement, role applied]
  16. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  17. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  18. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  19. `Preorder.smallCategory`
      [def, depth 10, in-statement, role instance-slot]
  20. `CategoryTheory.Category.assoc`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  21. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]

### proof_0188  (target depth 14, band 11-25)

THEOREM PROVED: `MulActionHom.id_comp`

Grade all 14 candidates.

   1. `MulActionHom.comp`
      [def, depth 12, in-statement, role explicit-arg]
   2. `MulActionHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `MulActionHom.id_apply`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   4. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `id`
      [def, depth 0, in-statement, role explicit-arg]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
   8. `instFunLikeMulActionHom`
      [def, depth 8, in-statement, role instance-slot]
   9. `MulActionHom.id`
      [def, depth 5, in-statement, role explicit-arg]
  10. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  11. `SMul`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `MulActionHom.ext`
      [theorem, depth 9, introduced-by-proof, role applied]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `MulActionHom.comp_apply`
      [theorem, depth 13, introduced-by-proof, role explicit-arg]

### proof_0189  (target depth 23, band 11-25)

THEOREM PROVED: `OrderHom.withTopMap_coe`

Grade all 8 candidates.

   1. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   2. `OrderHom.withTopMap`
      [def, depth 22, in-statement, role explicit-arg]
   3. `OrderHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   4. `OrderHom.instFunLike`
      [def, depth 7, in-statement, role instance-slot]
   5. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `WithTop`
      [def, depth 1, in-statement, role implicit-arg]
   7. `WithTop.instPreorder`
      [def, depth 16, in-statement, role instance-slot]
   8. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0190  (target depth 15, band 11-25)

THEOREM PROVED: `CovBy.ofDual`

Grade all 11 candidates.

   1. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `CovBy`
      [def, depth 2, in-statement, role implicit-arg]
   4. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   5. `OrderDual.ofDual`
      [def, depth 11, in-statement, role explicit-arg]
   6. `OrderDual.instLT`
      [def, depth 2, in-statement, role instance-slot]
   7. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
   8. `LT`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  10. `OrderDual`
      [def, depth 0, in-statement, role type-annotation]
  11. `ofDual_covBy_ofDual_iff`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]

### proof_0191  (target depth 22, band 11-25)

THEOREM PROVED: `CategoryTheory.Bicategory.postcomposing_map_app`

Grade all 14 candidates.

   1. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   2. `CategoryTheory.Bicategory`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CategoryTheory.Bicategory.homCategory`
      [def, depth 1, in-statement, role instance-slot]
   4. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   5. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   6. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   8. `CategoryTheory.Functor.map`
      [def, depth 2, in-statement, role explicit-arg]
   9. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  10. `CategoryTheory.Bicategory.postcomposing`
      [def, depth 21, in-statement, role explicit-arg]
  11. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  12. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role explicit-arg]
  13. `CategoryTheory.Bicategory.postcomp`
      [def, depth 10, in-statement, role implicit-arg]
  14. `CategoryTheory.Bicategory.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]

### proof_0192  (target depth 24, band 11-25)

THEOREM PROVED: `OrderIso.instOrderIsoClass`

Grade all 6 candidates.

   1. `OrderIso.instEquivLike`
      [def, depth 23, in-statement, role instance-slot]
   2. `RelIso.map_rel_iff'`
      [theorem, depth 1, in-statement, role explicit-arg]
   3. `OrderIso`
      [def, depth 2, in-statement, role implicit-arg]
   4. `LE`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `OrderIsoClass.mk`
      [constructor, depth 9, introduced-by-proof, role applied]
   6. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
