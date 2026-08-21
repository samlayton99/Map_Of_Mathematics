# Grading batch `testr_11` — 24 proofs

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

### proof_0241  (target depth 41, band 26-50)

THEOREM PROVED: `CategoryTheory.SmallObject.hasPushouts`

Grade all 18 candidates.

   1. `OrderBot`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Cardinal.IsRegular`
      [inductive, depth 19, in-statement, role explicit-arg]
   5. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
   6. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   7. `DistribLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
   8. `Cardinal.ord`
      [def, depth 38, in-statement, role explicit-arg]
   9. `Fact`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `CategoryTheory.MorphismProperty.IsCardinalForSmallObjectArgument`
      [inductive, depth 39, in-statement, role type-annotation]
  11. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  12. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  13. `instDistribLatticeOfLinearOrder`
      [def, depth 15, in-statement, role instance-slot]
  14. `Ordinal.ToType`
      [def, depth 26, in-statement, role explicit-arg]
  15. `Cardinal`
      [def, depth 18, in-statement, role type-annotation]
  16. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  17. `CategoryTheory.MorphismProperty.IsCardinalForSmallObjectArgument.hasPushouts`
      [theorem, depth 40, introduced-by-proof, role applied]
  18. `linearOrder_toType`
      [def, depth 27, in-statement, role instance-slot]

### proof_0242  (target depth 36, band 26-50)

THEOREM PROVED: `Std.Tactic.BVDecide.Frontend.Normalize.BitVec.not_bif_eq_bif`

Grade all 18 candidates.

   1. `BitVec`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
   4. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   5. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `cond`
      [def, depth 5, in-statement, role explicit-arg]
   7. `Bool.false`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `BitVec.instComplement`
      [def, depth 35, in-statement, role instance-slot]
   9. `Complement.complement`
      [def, depth 1, in-statement, role explicit-arg]
  10. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `instBEqOfDecidableEq`
      [def, depth 6, in-statement, role instance-slot]
  13. `Bool.casesOn`
      [def, depth 3, in-statement, role applied]
  14. `instDecidableEqBitVec`
      [def, depth 19, in-statement, role instance-slot]
  15. `Eq.refl`
      [constructor, depth 1, in-statement, role unresolved]
  16. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
  17. `BEq.beq`
      [def, depth 1, in-statement, role explicit-arg]
  18. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]

### proof_0243  (target depth 33, band 26-50)

THEOREM PROVED: `SimpleGraph.dist_comm`

Grade all 13 candidates.

   1. `SimpleGraph.edist_comm`
      [theorem, depth 32, introduced-by-proof, role explicit-arg]
   2. `id`
      [def, depth 0, in-statement, role explicit-arg]
   3. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
   5. `ENat`
      [def, depth 2, in-statement, role implicit-arg]
   6. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   7. `SimpleGraph.edist`
      [def, depth 30, in-statement, role explicit-arg]
   8. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `SimpleGraph.dist`
      [def, depth 31, in-statement, role explicit-arg]
  10. `ENat.toNat`
      [def, depth 7, in-statement, role explicit-arg]
  11. `SimpleGraph.dist.eq_1`
      [theorem, depth 32, introduced-by-proof, role explicit-arg]
  12. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0244  (target depth 46, band 26-50)

THEOREM PROVED: `CategoryTheory.Functor.instIsDenseCompOfIsEquivalence`

Grade all 13 candidates.

   1. `CategoryTheory.Functor.IsDense`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.Functor.IsDense.mk`
      [constructor, depth 33, introduced-by-proof, role applied]
   4. `Nonempty.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `CategoryTheory.CostructuredArrow`
      [def, depth 23, introduced-by-proof, role implicit-arg]
   6. `CategoryTheory.Functor.IsEquivalence`
      [inductive, depth 2, in-statement, role type-annotation]
   7. `CategoryTheory.Functor.DenseAt.precompOfFinal`
      [def, depth 45, introduced-by-proof, role explicit-arg]
   8. `CategoryTheory.instCategoryCostructuredArrow_1`
      [def, depth 23, introduced-by-proof, role instance-slot]
   9. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  10. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `CategoryTheory.CostructuredArrow.pre`
      [def, depth 23, introduced-by-proof, role explicit-arg]
  12. `CategoryTheory.Functor.denseAt`
      [def, depth 32, introduced-by-proof, role explicit-arg]
  13. `CategoryTheory.Functor.DenseAt`
      [def, depth 31, introduced-by-proof, role implicit-arg]

### proof_0245  (target depth 27, band 26-50)

THEOREM PROVED: `Nat.shiftRight_le`

Grade all 22 candidates.

   1. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
   2. `instLENat`
      [def, depth 2, in-statement, role instance-slot]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `instNatPowNat`
      [def, depth 11, introduced-by-proof, role instance-slot]
   5. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   6. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   7. `HShiftRight.hShiftRight`
      [def, depth 2, in-statement, role explicit-arg]
   8. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
   9. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `Nat.div_le_self`
      [theorem, depth 21, introduced-by-proof, role explicit-arg]
  11. `instHShiftRightOfShiftRight`
      [def, depth 3, in-statement, role instance-slot]
  12. `instHPow`
      [def, depth 3, introduced-by-proof, role instance-slot]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `HPow.hPow`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  15. `Nat.instShiftRight`
      [def, depth 22, in-statement, role instance-slot]
  16. `HDiv.hDiv`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Nat.instDiv`
      [def, depth 19, in-statement, role instance-slot]
  18. `instHDiv`
      [def, depth 3, in-statement, role instance-slot]
  19. `Nat.shiftRight_eq_div_pow`
      [theorem, depth 26, introduced-by-proof, role explicit-arg]
  20. `instPowNat`
      [def, depth 2, introduced-by-proof, role instance-slot]
  21. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  22. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_0246  (target depth 50, band 26-50)

THEOREM PROVED: `List.twoStepInduction_cons_cons`

Grade all 4 candidates.

   1. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `List.twoStepInduction.eq_3`
      [theorem, depth 49, introduced-by-proof, role applied]
   3. `List.cons`
      [constructor, depth 1, in-statement, role type-annotation]
   4. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]

### proof_0247  (target depth 43, band 26-50)

THEOREM PROVED: `ONote.fundamentalSequenceProp_inl_none`

Grade all 7 candidates.

   1. `ONote.FundamentalSequenceProp`
      [def, depth 42, in-statement, role implicit-arg]
   2. `ONote`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Iff.rfl`
      [theorem, depth 3, in-statement, role applied]
   6. `Option.none`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `Sum.inl`
      [constructor, depth 1, in-statement, role explicit-arg]

### proof_0248  (target depth 26, band 26-50)

THEOREM PROVED: `AddEquiv.coe_mapAddSubgroup`

Grade all 16 candidates.

   1. `AddEquiv.mapAddSubgroup`
      [def, depth 25, in-statement, role explicit-arg]
   2. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   3. `AddGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `AddEquiv`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `instFunLikeOrderIso`
      [def, depth 21, in-statement, role instance-slot]
   6. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   7. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   8. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   9. `AddSubgroup.instPartialOrder`
      [def, depth 22, in-statement, role instance-slot]
  10. `AddGroup.toSubNegMonoid`
      [def, depth 1, in-statement, role instance-slot]
  11. `SubNegMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  12. `OrderIso`
      [def, depth 2, in-statement, role implicit-arg]
  13. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  14. `rfl`
      [def, depth 2, in-statement, role applied]
  15. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  16. `AddSubgroup`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0249  (target depth 36, band 26-50)

THEOREM PROVED: `LinearEquiv.congrRight₂_apply`

Grade all 23 candidates.

   1. `LinearMap.BilinMap`
      [def, depth 32, in-statement, role implicit-arg]
   2. `LinearEquiv.congrRight₂`
      [def, depth 35, in-statement, role explicit-arg]
   3. `LinearEquiv.instEquivLike`
      [def, depth 25, in-statement, role instance-slot]
   4. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   5. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   7. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   8. `Module.toDistribMulAction`
      [def, depth 2, in-statement, role instance-slot]
   9. `LinearEquiv`
      [inductive, depth 12, in-statement, role implicit-arg]
  10. `CommSemiring.toCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
  11. `LinearMap`
      [inductive, depth 11, in-statement, role implicit-arg]
  12. `LinearMap.module`
      [def, depth 31, in-statement, role instance-slot]
  13. `LinearMap.addCommMonoid`
      [def, depth 28, in-statement, role instance-slot]
  14. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  15. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
  16. `CommMonoid.toMonoid`
      [def, depth 1, in-statement, role implicit-arg]
  17. `DistribMulAction.toMulAction`
      [def, depth 2, in-statement, role instance-slot]
  18. `rfl`
      [def, depth 2, in-statement, role applied]
  19. `Semiring.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  20. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  21. `DistribMulAction.toDistribSMul`
      [def, depth 6, in-statement, role instance-slot]
  22. `AddCommMonoid.toAddMonoid`
      [def, depth 1, in-statement, role implicit-arg]
  23. `RingHom.id`
      [def, depth 12, in-statement, role explicit-arg]

### proof_0250  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.IsColimit.homEquiv_apply`

Grade all 18 candidates.

   1. `CategoryTheory.Limits.IsColimit`
      [inductive, depth 3, in-statement, role type-annotation]
   2. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   3. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `CategoryTheory.Limits.Cocone.pt`
      [def, depth 3, in-statement, role explicit-arg]
   5. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   6. `CategoryTheory.Functor.const`
      [def, depth 21, in-statement, role explicit-arg]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   8. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  11. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  12. `CategoryTheory.Limits.Cocone.extend`
      [def, depth 23, in-statement, role explicit-arg]
  13. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  14. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  15. `CategoryTheory.Limits.IsColimit.homEquiv`
      [def, depth 26, in-statement, role explicit-arg]
  16. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  17. `CategoryTheory.Limits.Cocone`
      [inductive, depth 2, in-statement, role type-annotation]
  18. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]

### proof_0251  (target depth 43, band 26-50)

THEOREM PROVED: `Std.DTreeMap.Raw.union_eq`

Grade all 6 candidates.

   1. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
   2. `Std.DTreeMap.Raw.union`
      [def, depth 42, in-statement, role explicit-arg]
   3. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Std.DTreeMap.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
   6. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]

### proof_0252  (target depth 27, band 26-50)

THEOREM PROVED: `Multiset.filter_union`

Grade all 21 candidates.

   1. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   2. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   3. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Multiset.filter`
      [def, depth 14, in-statement, role explicit-arg]
   5. `HSub.hSub`
      [def, depth 2, in-statement, role explicit-arg]
   6. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   7. `Multiset.instSub`
      [def, depth 24, in-statement, role instance-slot]
   8. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   9. `HAdd.hAdd`
      [def, depth 2, in-statement, role implicit-arg]
  10. `Multiset.filter_add`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
  11. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  12. `instHSub`
      [def, depth 3, in-statement, role instance-slot]
  13. `Multiset.filter_sub`
      [theorem, depth 26, introduced-by-proof, role explicit-arg]
  14. `Multiset.instUnion`
      [def, depth 26, in-statement, role instance-slot]
  15. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `Multiset.instAdd`
      [def, depth 13, in-statement, role instance-slot]
  17. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  18. `Multiset`
      [def, depth 9, in-statement, role type-annotation]
  19. `Union.union`
      [def, depth 1, in-statement, role explicit-arg]
  20. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `DecidablePred`
      [def, depth 1, in-statement, role type-annotation]

### proof_0253  (target depth 53, band 51-75)

THEOREM PROVED: `CategoryTheory.TwoSquare.GuitartExact.of_hComp'`

Grade all 18 candidates.

   1. `CategoryTheory.TwoSquare.GuitartExact.whiskerHorizontal_iff`
      [theorem, depth 52, introduced-by-proof, role explicit-arg]
   2. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
   3. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `CategoryTheory.TwoSquare.whiskerHorizontal`
      [def, depth 23, in-statement, role explicit-arg]
   5. `CategoryTheory.TwoSquare.hComp`
      [def, depth 24, in-statement, role explicit-arg]
   6. `CategoryTheory.Functor.EssSurj`
      [inductive, depth 2, in-statement, role type-annotation]
   7. `CategoryTheory.TwoSquare.hComp'`
      [def, depth 25, in-statement, role explicit-arg]
   8. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
   9. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  11. `CategoryTheory.TwoSquare`
      [def, depth 20, in-statement, role type-annotation]
  12. `CategoryTheory.TwoSquare.GuitartExact.of_hComp`
      [theorem, depth 49, introduced-by-proof, role applied]
  13. `CategoryTheory.TwoSquare.GuitartExact`
      [inductive, depth 21, in-statement, role implicit-arg]
  14. `Eq.mp`
      [def, depth 3, in-statement, role instance-slot]
  15. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  17. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  18. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0254  (target depth 73, band 51-75)

THEOREM PROVED: `CategoryTheory.Limits.FintypeCat.inclusion_preservesFiniteColimits`

Grade all 10 candidates.

   1. `FintypeCat.incl`
      [def, depth 14, in-statement, role explicit-arg]
   2. `CategoryTheory.SmallCategory`
      [def, depth 1, introduced-by-proof, role type-annotation]
   3. `CategoryTheory.preservesColimitOfShape_of_createsColimitsOfShape_and_hasColimitsOfShape`
      [theorem, depth 32, introduced-by-proof, role explicit-arg]
   4. `CategoryTheory.types`
      [def, depth 10, in-statement, role instance-slot]
   5. `CategoryTheory.Limits.PreservesFiniteColimits.mk`
      [constructor, depth 9, introduced-by-proof, role applied]
   6. `CategoryTheory.Limits.FintypeCat.inclusionCreatesFiniteColimits`
      [def, depth 72, introduced-by-proof, role instance-slot]
   7. `Finite`
      [inductive, depth 0, in-statement, role explicit-arg]
   8. `CategoryTheory.FinCategory`
      [inductive, depth 2, introduced-by-proof, role type-annotation]
   9. `FintypeCat`
      [def, depth 11, in-statement, role implicit-arg]
  10. `CategoryTheory.ObjectProperty.FullSubcategory.category`
      [def, depth 10, in-statement, role instance-slot]

### proof_0255  (target depth 72, band 51-75)

THEOREM PROVED: `Algebra.map_inf`

Grade all 23 candidates.

   1. `RingHomClass.toRingHom`
      [def, depth 13, in-statement, role explicit-arg]
   2. `SetLike.coe_injective`
      [theorem, depth 2, in-statement, role applied]
   3. `ConditionallyCompleteLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
   4. `Subalgebra`
      [inductive, depth 2, in-statement, role implicit-arg]
   5. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Function.Injective`
      [def, depth 1, in-statement, role type-annotation]
   7. `RingHom`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `Subalgebra.instSetLike`
      [def, depth 20, in-statement, role instance-slot]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  10. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Algebra.instCompleteLatticeSubalgebra`
      [def, depth 71, in-statement, role instance-slot]
  12. `AlgHom.funLike`
      [def, depth 20, in-statement, role instance-slot]
  13. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role implicit-arg]
  14. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
  15. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]
  16. `Subalgebra.map`
      [def, depth 25, in-statement, role explicit-arg]
  17. `SemilatticeInf.toMin`
      [def, depth 2, in-statement, role instance-slot]
  18. `CompleteLattice.toConditionallyCompleteLattice`
      [def, depth 9, in-statement, role instance-slot]
  19. `AlgHom`
      [inductive, depth 2, in-statement, role implicit-arg]
  20. `RingHom.instFunLike`
      [def, depth 15, in-statement, role instance-slot]
  21. `SetLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
  22. `Set.image_inter`
      [theorem, depth 58, introduced-by-proof, role explicit-arg]
  23. `Min.min`
      [def, depth 1, in-statement, role explicit-arg]

### proof_0256  (target depth 61, band 51-75)

THEOREM PROVED: `Monotone.mulIndicator_eventuallyEq_iUnion`

Grade all 20 candidates.

   1. `One`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Pi.instOne`
      [def, depth 4, introduced-by-proof, role instance-slot]
   5. `Set.instCompleteAtomicBooleanAlgebra`
      [def, depth 58, in-statement, role instance-slot]
   6. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
   7. `ConditionallyCompleteLattice.toConditionallyCompletePartialOrder`
      [def, depth 8, in-statement, role instance-slot]
   8. `ConditionallyCompletePartialOrderSup.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   9. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Monotone`
      [def, depth 2, in-statement, role type-annotation]
  11. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`
      [def, depth 1, in-statement, role instance-slot]
  12. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  14. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  15. `CompleteBooleanAlgebra.toCompleteLattice`
      [def, depth 1, in-statement, role instance-slot]
  16. `Set.iUnion`
      [def, depth 5, in-statement, role explicit-arg]
  17. `Monotone.piecewise_eventually_eq_iUnion`
      [theorem, depth 60, introduced-by-proof, role applied]
  18. `Classical.propDecidable`
      [def, depth 11, in-statement, role instance-slot]
  19. `ConditionallyCompletePartialOrder.toConditionallyCompletePartialOrderSup`
      [def, depth 1, in-statement, role instance-slot]
  20. `CompleteLattice.toConditionallyCompleteLattice`
      [def, depth 9, in-statement, role instance-slot]

### proof_0257  (target depth 66, band 51-75)

THEOREM PROVED: `Filter.tendsto_Ioc_Iic_Iic`

Grade all 7 candidates.

   1. `Filter.principal`
      [def, depth 7, in-statement, role implicit-arg]
   2. `Set.Ioc_subset_Icc_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   3. `Set.Icc`
      [def, depth 2, introduced-by-proof, role implicit-arg]
   4. `Set.Iic`
      [def, depth 2, in-statement, role explicit-arg]
   5. `Filter.tendstoIxxClass_of_subset`
      [theorem, depth 65, introduced-by-proof, role applied]
   6. `Set.Ioc`
      [def, depth 2, in-statement, role implicit-arg]
   7. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0258  (target depth 62, band 51-75)

THEOREM PROVED: `setOfPred_isOpen_sSup`

Grade all 20 candidates.

   1. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   2. `TopologicalSpace.instCompleteLattice`
      [def, depth 61, in-statement, role instance-slot]
   3. `OrderDual.ofDual`
      [def, depth 11, in-statement, role explicit-arg]
   4. `IsOpen`
      [def, depth 2, in-statement, role explicit-arg]
   5. `Set.ofPred`
      [def, depth 1, in-statement, role explicit-arg]
   6. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   8. `Set.instCompleteAtomicBooleanAlgebra`
      [def, depth 58, in-statement, role instance-slot]
   9. `OrderDual.toDual`
      [def, depth 11, in-statement, role explicit-arg]
  10. `Function.comp`
      [def, depth 0, in-statement, role implicit-arg]
  11. `TopologicalSpace.generateFrom`
      [def, depth 7, in-statement, role explicit-arg]
  12. `GaloisConnection.l_sSup`
      [theorem, depth 13, introduced-by-proof, role applied]
  13. `TopologicalSpace.gc_generateFrom`
      [theorem, depth 17, in-statement, role explicit-arg]
  14. `CompleteBooleanAlgebra.toCompleteLattice`
      [def, depth 1, in-statement, role instance-slot]
  15. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`
      [def, depth 1, in-statement, role instance-slot]
  16. `OrderDual.instCompleteLattice`
      [def, depth 15, in-statement, role instance-slot]
  17. `Set`
      [def, depth 0, in-statement, role explicit-arg]
  18. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
  19. `TopologicalSpace`
      [inductive, depth 0, in-statement, role explicit-arg]
  20. `OrderDual`
      [def, depth 0, in-statement, role implicit-arg]

### proof_0259  (target depth 74, band 51-75)

THEOREM PROVED: `Std.ExtHashSet.insert_eq_insert`

Grade all 8 candidates.

   1. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.ExtHashSet`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Insert.insert`
      [def, depth 2, in-statement, role implicit-arg]
   7. `rfl`
      [def, depth 2, in-statement, role applied]
   8. `Std.ExtHashSet.instInsertOfEquivBEqOfLawfulHashable`
      [def, depth 73, in-statement, role instance-slot]

### proof_0260  (target depth 61, band 51-75)

THEOREM PROVED: `SaturatedAddSubmonoid.instCompleteLattice._proof_8`

Grade all 6 candidates.

   1. `inferInstance`
      [def, depth 0, in-statement, role instance-slot]
   2. `CompleteSemilatticeInf.isGLB_sInf`
      [theorem, depth 1, in-statement, role applied]
   3. `AddZeroClass`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `SaturatedAddSubmonoid`
      [inductive, depth 1, in-statement, role explicit-arg]
   5. `SaturatedAddSubmonoid.instCompleteSemilatticeInf`
      [def, depth 60, in-statement, role instance-slot]
   6. `CompleteSemilatticeInf`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0261  (target depth 68, band 51-75)

THEOREM PROVED: `NonUnitalSubsemiring.closure_sUnion`

Grade all 17 candidates.

   1. `CompleteLattice.toCompleteSemilatticeInf`
      [def, depth 8, in-statement, role instance-slot]
   2. `SetLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   3. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   4. `NonUnitalSubsemiring.instCompleteLattice`
      [def, depth 65, in-statement, role instance-slot]
   5. `CompleteBooleanAlgebra.toCompleteLattice`
      [def, depth 1, in-statement, role instance-slot]
   6. `NonUnitalSubsemiring.closure`
      [def, depth 63, in-statement, role implicit-arg]
   7. `CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra`
      [def, depth 1, in-statement, role instance-slot]
   8. `NonUnitalSubsemiring`
      [inductive, depth 1, in-statement, role implicit-arg]
   9. `NonUnitalSubsemiring.gi`
      [def, depth 67, introduced-by-proof, role explicit-arg]
  10. `NonUnitalSubsemiring.instSetLike`
      [def, depth 12, in-statement, role instance-slot]
  11. `GaloisInsertion.gc`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  12. `CompleteSemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  13. `Set`
      [def, depth 0, in-statement, role explicit-arg]
  14. `NonUnitalSubsemiring.instPartialOrder`
      [def, depth 22, in-statement, role instance-slot]
  15. `NonUnitalNonAssocSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `GaloisConnection.l_sSup`
      [theorem, depth 13, introduced-by-proof, role applied]
  17. `Set.instCompleteAtomicBooleanAlgebra`
      [def, depth 58, in-statement, role instance-slot]

### proof_0262  (target depth 70, band 51-75)

THEOREM PROVED: `Finset.weightedVSub_filter_of_ne`

Grade all 20 candidates.

   1. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   2. `Finset.instSetLike`
      [def, depth 53, in-statement, role instance-slot]
   3. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   4. `DecidablePred`
      [def, depth 1, in-statement, role type-annotation]
   5. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   6. `Ne`
      [def, depth 2, in-statement, role type-annotation]
   7. `Classical.choice`
      [axiom, depth 1, in-statement, role explicit-arg]
   8. `instMulZeroClassOfSemiring`
      [def, depth 11, in-statement, role instance-slot]
   9. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
  10. `AddTorsor`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Finset.weightedVSubOfPoint_filter_of_ne`
      [theorem, depth 69, introduced-by-proof, role applied]
  13. `MulZeroClass.toZero`
      [def, depth 1, in-statement, role instance-slot]
  14. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  15. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
  16. `AddCommGroup.toAddGroup`
      [def, depth 1, in-statement, role instance-slot]
  17. `Finset`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]
  19. `Finset.weightedVSub._proof_1`
      [theorem, depth 3, in-statement, role explicit-arg]
  20. `Module`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0263  (target depth 55, band 51-75)

THEOREM PROVED: `List.mergeSort_nil`

Grade all 10 candidates.

   1. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   3. `Bool`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `_private.Init.Data.List.Sort.Lemmas.0.List.mergeSort.eq_1`
      [theorem, depth 54, introduced-by-proof, role explicit-arg]
   6. `id`
      [def, depth 0, in-statement, role explicit-arg]
   7. `List.mergeSort`
      [def, depth 51, in-statement, role explicit-arg]
   8. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_0264  (target depth 55, band 51-75)

THEOREM PROVED: `Lean.Grind.smul_int_eq_mul`

Grade all 19 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `instHSMul`
      [def, depth 3, in-statement, role instance-slot]
   3. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
   4. `Lean.Grind.Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   5. `Lean.Grind.IntModule.zsmul`
      [def, depth 1, in-statement, role instance-slot]
   6. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Lean.Grind.Ring.zsmul`
      [def, depth 1, in-statement, role instance-slot]
   8. `Lean.Grind.Ring`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  10. `Lean.Grind.Ring.intCast`
      [def, depth 1, in-statement, role instance-slot]
  11. `Lean.Grind.Semiring.toMul`
      [def, depth 1, in-statement, role instance-slot]
  12. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
  13. `Lean.Grind.Ring.toIntModule`
      [def, depth 54, in-statement, role instance-slot]
  14. `Int.cast`
      [def, depth 2, in-statement, role explicit-arg]
  15. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  16. `Lean.Grind.Ring.zsmul_eq_intCast_mul`
      [theorem, depth 52, in-statement, role explicit-arg]
  17. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  18. `HSMul.hSMul`
      [def, depth 2, in-statement, role explicit-arg]
  19. `id`
      [def, depth 0, in-statement, role explicit-arg]
