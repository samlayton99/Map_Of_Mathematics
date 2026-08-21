# Grading batch `testr_04` — 24 proofs

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

### proof_0073  (target depth 10, band 0-10)

THEOREM PROVED: `Std.Do.SVal.uncurry_cons`

Grade all 7 candidates.

   1. `List.cons`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Std.Do.SVal.StateTuple`
      [def, depth 6, in-statement, role implicit-arg]
   3. `Prod.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
   4. `Std.Do.SVal.uncurry`
      [def, depth 9, in-statement, role implicit-arg]
   5. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   6. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.Do.SVal`
      [def, depth 6, in-statement, role type-annotation]

### proof_0074  (target depth 5, band 0-10)

THEOREM PROVED: `CategoryTheory.ShortComplex.HasHomology.mk'`

Grade all 6 candidates.

   1. `CategoryTheory.ShortComplex`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `CategoryTheory.Limits.HasZeroMorphisms`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.ShortComplex.HomologyData`
      [inductive, depth 3, in-statement, role implicit-arg]
   4. `Nonempty.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CategoryTheory.ShortComplex.HasHomology.mk`
      [constructor, depth 4, introduced-by-proof, role applied]

### proof_0075  (target depth 3, band 0-10)

THEOREM PROVED: `Equivalence.isEquiv`

Grade all 8 candidates.

   1. `Equivalence`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `IsEquiv.mk`
      [constructor, depth 1, introduced-by-proof, role applied]
   3. `Std.Refl`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
   4. `Equivalence.stdSymm`
      [theorem, depth 2, introduced-by-proof, role let-value]
   5. `Equivalence.isTrans`
      [theorem, depth 2, introduced-by-proof, role let-value]
   6. `Std.Symm`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
   7. `Equivalence.stdRefl`
      [theorem, depth 2, introduced-by-proof, role let-value]
   8. `IsTrans`
      [inductive, depth 0, introduced-by-proof, role type-annotation]

### proof_0076  (target depth 6, band 0-10)

THEOREM PROVED: `NonemptyInterval.snd_sup`

Grade all 11 candidates.

   1. `NonemptyInterval`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   3. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   4. `NonemptyInterval.instMax`
      [def, depth 5, in-statement, role instance-slot]
   5. `Lattice`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `NonemptyInterval.toProd`
      [def, depth 2, in-statement, role explicit-arg]
   7. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   8. `Prod.snd`
      [def, depth 1, in-statement, role implicit-arg]
   9. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  10. `Max.max`
      [def, depth 1, in-statement, role explicit-arg]
  11. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]

### proof_0077  (target depth 6, band 0-10)

THEOREM PROVED: `decide_false`

Grade all 10 candidates.

   1. `Bool.false`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Not`
      [def, depth 1, in-statement, role type-annotation]
   4. `False`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `Decidable.decide`
      [def, depth 5, in-statement, role explicit-arg]
   6. `_private.Init.Core.0.decide_false.match_1_1`
      [def, depth 5, introduced-by-proof, role applied]
   7. `False.elim`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   8. `Decidable`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `rfl`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  10. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0078  (target depth 10, band 0-10)

THEOREM PROVED: `CategoryTheory.MorphismProperty.RightFraction.leftFraction_fac_assoc`

Grade all 24 candidates.

   1. `CategoryTheory.MorphismProperty.RightFraction.leftFraction`
      [def, depth 9, in-statement, role explicit-arg]
   2. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   3. `id`
      [def, depth 0, introduced-by-proof, role applied]
   4. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.MorphismProperty.RightFraction`
      [inductive, depth 3, in-statement, role type-annotation]
   6. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `CategoryTheory.Category.assoc`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   8. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   9. `CategoryTheory.MorphismProperty.RightFraction.X'`
      [def, depth 4, in-statement, role implicit-arg]
  10. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  11. `CategoryTheory.MorphismProperty.RightFraction.s`
      [def, depth 4, in-statement, role explicit-arg]
  12. `CategoryTheory.MorphismProperty.RightFraction.f`
      [def, depth 4, in-statement, role explicit-arg]
  13. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  14. `CategoryTheory.MorphismProperty.RightFraction.leftFraction_fac`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
  15. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  16. `CategoryTheory.MorphismProperty.LeftFraction.f`
      [def, depth 4, in-statement, role explicit-arg]
  17. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  18. `CategoryTheory.MorphismProperty.HasLeftCalculusOfFractions`
      [inductive, depth 3, in-statement, role type-annotation]
  19. `CategoryTheory.MorphismProperty.LeftFraction.s`
      [def, depth 4, in-statement, role explicit-arg]
  20. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  21. `CategoryTheory.MorphismProperty.LeftFraction.Y'`
      [def, depth 4, in-statement, role implicit-arg]
  22. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  23. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  24. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]

### proof_0079  (target depth 4, band 0-10)

THEOREM PROVED: `Mathlib.Tactic.LinearCombinationPrime.pf_add_c`

Grade all 6 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   3. `rfl`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   4. `Add`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Eq.rec`
      [recursor, depth 2, introduced-by-proof, role applied]
   6. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]

### proof_0080  (target depth 4, band 0-10)

THEOREM PROVED: `Prefunctor.id_map`

Grade all 5 candidates.

   1. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role applied]
   2. `Prefunctor.map`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Quiver`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Prefunctor.id`
      [def, depth 3, in-statement, role explicit-arg]

### proof_0081  (target depth 9, band 0-10)

THEOREM PROVED: `ModuleFilterBasis.smul_right`

Grade all 10 candidates.

   1. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   3. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   5. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   7. `ModuleFilterBasis.GroupFilterBasis.hasMem`
      [def, depth 8, in-statement, role instance-slot]
   8. `ModuleFilterBasis.smul_right'`
      [theorem, depth 7, introduced-by-proof, role applied]
   9. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `ModuleFilterBasis`
      [inductive, depth 6, in-statement, role implicit-arg]

### proof_0082  (target depth 7, band 0-10)

THEOREM PROVED: `Right.add_nonneg`

Grade all 11 candidates.

   1. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   2. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `le_add_of_nonneg_of_le`
      [theorem, depth 6, introduced-by-proof, role applied]
   5. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   6. `AddZero.toZero`
      [def, depth 1, in-statement, role instance-slot]
   7. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   8. `AddRightMono`
      [def, depth 4, in-statement, role type-annotation]
   9. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  11. `AddZeroClass`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0083  (target depth 5, band 0-10)

THEOREM PROVED: `CategoryTheory.IsBimonHom.toIsMonHom`

Grade all 8 candidates.

   1. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.BraidedCategory`
      [inductive, depth 2, in-statement, role type-annotation]
   6. `CategoryTheory.IsBimonHom`
      [inductive, depth 4, in-statement, role type-annotation]
   7. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   8. `CategoryTheory.BimonObj`
      [inductive, depth 3, in-statement, role type-annotation]

### proof_0084  (target depth 10, band 0-10)

THEOREM PROVED: `AddSubmonoidClass.toAddMonoid._proof_2`

Grade all 21 candidates.

   1. `SetLike`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
   3. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
   4. `AddZeroClass.add_zero`
      [theorem, depth 1, introduced-by-proof, role applied]
   5. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   6. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   7. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   8. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  10. `AddSubmonoidClass`
      [inductive, depth 2, in-statement, role type-annotation]
  11. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
  12. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Function.Injective.addZeroClass`
      [def, depth 7, introduced-by-proof, role instance-slot]
  15. `AddSubmonoidClass.toAddZeroClass`
      [def, depth 9, introduced-by-proof, role instance-slot]
  16. `Subtype.val`
      [def, depth 1, in-statement, role implicit-arg]
  17. `Subtype.coe_injective`
      [theorem, depth 7, in-statement, role explicit-arg]
  18. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  19. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
  20. `ZeroMemClass.zero`
      [def, depth 5, in-statement, role instance-slot]
  21. `AddZero.toZero`
      [def, depth 1, in-statement, role instance-slot]

### proof_0085  (target depth 3, band 0-10)

THEOREM PROVED: `CategoryTheory.Abelian.SpectralObject.exact₃'`

Grade all 3 candidates.

   1. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `CategoryTheory.Abelian`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.Abelian.SpectralObject`
      [inductive, depth 2, in-statement, role type-annotation]

### proof_0086  (target depth 6, band 0-10)

THEOREM PROVED: `CategoryTheory.MonoidalCategory.MonoidalRightAction.unit_actionHomRight_assoc`

Grade all 24 candidates.

   1. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   2. `CategoryTheory.MonoidalCategoryStruct.tensorUnit`
      [def, depth 2, in-statement, role explicit-arg]
   3. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   6. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   7. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
   8. `id`
      [def, depth 0, introduced-by-proof, role applied]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `CategoryTheory.MonoidalCategory.MonoidalRightAction`
      [inductive, depth 2, in-statement, role type-annotation]
  11. `CategoryTheory.MonoidalCategory.MonoidalRightAction.toMonoidalRightActionStruct`
      [def, depth 3, in-statement, role instance-slot]
  12. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  13. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  14. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  16. `CategoryTheory.MonoidalCategory.MonoidalRightActionStruct.actionHomLeft`
      [def, depth 3, in-statement, role explicit-arg]
  17. `CategoryTheory.MonoidalCategory.MonoidalRightActionStruct.actionObj`
      [def, depth 3, in-statement, role implicit-arg]
  18. `CategoryTheory.Category.assoc`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  19. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  20. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role implicit-arg]
  21. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  22. `CategoryTheory.MonoidalCategory.MonoidalRightActionStruct.actionUnitIso`
      [def, depth 3, in-statement, role explicit-arg]
  23. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  24. `CategoryTheory.MonoidalCategory.MonoidalRightAction.unit_actionHomRight`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]

### proof_0087  (target depth 5, band 0-10)

THEOREM PROVED: `Hypergraph.IsNonempty.of_nonempty_vertexSet`

Grade all 6 candidates.

   1. `Hypergraph.vertexSet`
      [def, depth 1, in-statement, role explicit-arg]
   2. `Set.Nonempty`
      [def, depth 4, in-statement, role implicit-arg]
   3. `Hypergraph`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Or.inl`
      [constructor, depth 1, introduced-by-proof, role applied]
   5. `Hypergraph.edgeSet`
      [def, depth 1, in-statement, role explicit-arg]
   6. `Set`
      [def, depth 0, in-statement, role implicit-arg]

### proof_0088  (target depth 7, band 0-10)

THEOREM PROVED: `AddOreLocalization.AddOreSet.ore_right_cancel`

Grade all 4 candidates.

   1. `AddOreLocalization.AddOreSet`
      [inductive, depth 6, in-statement, role type-annotation]
   2. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   3. `AddSubmonoid`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `AddMonoid`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0089  (target depth 4, band 0-10)

THEOREM PROVED: `CategoryTheory.Functor.HasPointwiseLeftDerivedFunctorAt.hasLimit'`

Grade all 5 candidates.

   1. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `CategoryTheory.MorphismProperty`
      [def, depth 2, in-statement, role type-annotation]
   3. `CategoryTheory.Functor.HasPointwiseLeftDerivedFunctorAt`
      [inductive, depth 3, in-statement, role type-annotation]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0090  (target depth 10, band 0-10)

THEOREM PROVED: `SemiconjBy.units_inv_symm_left_iff`

Grade all 11 candidates.

   1. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   2. `SemiconjBy.units_inv_symm_left`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   3. `Inv.inv`
      [def, depth 1, in-statement, role explicit-arg]
   4. `SemiconjBy`
      [def, depth 4, in-statement, role implicit-arg]
   5. `Units`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
   7. `Units.instInv`
      [def, depth 7, in-statement, role instance-slot]
   8. `Monoid`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
  10. `Units.val`
      [def, depth 2, in-statement, role explicit-arg]
  11. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]

### proof_0091  (target depth 9, band 0-10)

THEOREM PROVED: `Std.Rxo.Iterator.instLawfulDeterministicIterator`

Grade all 14 candidates.

   1. `Std.IterM`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `Std.LawfulDeterministicIterator.mk`
      [constructor, depth 4, introduced-by-proof, role applied]
   3. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Id`
      [def, depth 0, in-statement, role explicit-arg]
   5. `Std.IterStep`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Std.Rxo.instIteratorIteratorIdOfUpwardEnumerableOfDecidableLT`
      [def, depth 8, in-statement, role instance-slot]
   7. `Std.Rxo.Iterator.Monadic.step`
      [def, depth 6, in-statement, role explicit-arg]
   8. `Std.Rxo.Iterator`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Exists.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  10. `Std.PRange.UpwardEnumerable`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  12. `DecidableLT`
      [def, depth 2, in-statement, role type-annotation]
  13. `LT`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Std.IterM.IsPlausibleStep`
      [def, depth 3, introduced-by-proof, role explicit-arg]

### proof_0092  (target depth 6, band 0-10)

THEOREM PROVED: `CategoryTheory.Bicategory.whisker_exchange_assoc`

Grade all 18 candidates.

   1. `CategoryTheory.Bicategory.whiskerRight`
      [def, depth 1, in-statement, role explicit-arg]
   2. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   3. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   4. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Bicategory.whisker_exchange`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   6. `CategoryTheory.Bicategory`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   8. `CategoryTheory.Bicategory.homCategory`
      [def, depth 1, in-statement, role instance-slot]
   9. `CategoryTheory.Category.assoc`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  10. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  11. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  12. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  14. `id`
      [def, depth 0, introduced-by-proof, role applied]
  15. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role implicit-arg]
  16. `CategoryTheory.Bicategory.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  17. `CategoryTheory.Bicategory.whiskerLeft`
      [def, depth 1, in-statement, role explicit-arg]
  18. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]

### proof_0093  (target depth 4, band 0-10)

THEOREM PROVED: `propext_iff`

Grade all 11 candidates.

   1. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   2. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   3. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Iff.rfl`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   6. `HEq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
   7. `HEq`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
   8. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   9. `propext`
      [axiom, depth 1, introduced-by-proof, role explicit-arg]
  10. `Iff`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Eq.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]

### proof_0094  (target depth 8, band 0-10)

THEOREM PROVED: `Std.Sat.CNF.Clause.relabel_nil`

Grade all 16 candidates.

   1. `Std.Sat.CNF.Clause`
      [def, depth 2, in-statement, role implicit-arg]
   2. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   3. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Prod.snd`
      [def, depth 1, introduced-by-proof, role explicit-arg]
   5. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
   8. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
   9. `List.map_nil`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  10. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  12. `Std.Sat.Literal`
      [def, depth 1, in-statement, role implicit-arg]
  13. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  14. `Std.Sat.CNF.Clause.relabel`
      [def, depth 7, in-statement, role explicit-arg]
  15. `Prod.fst`
      [def, depth 1, introduced-by-proof, role explicit-arg]
  16. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]

### proof_0095  (target depth 10, band 0-10)

THEOREM PROVED: `Stream'.Seq.get?_mem`

Grade all 12 candidates.

   1. `Stream'.IsSeq`
      [def, depth 8, in-statement, role implicit-arg]
   2. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Stream'`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Option.some`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `Exists.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   6. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Stream'.Seq.get?`
      [def, depth 9, in-statement, role explicit-arg]
   8. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   9. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
  10. `Stream'.Seq`
      [def, depth 9, in-statement, role type-annotation]
  11. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Stream'.get`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0096  (target depth 4, band 0-10)

THEOREM PROVED: `PFun.prodLift_apply`

Grade all 5 candidates.

   1. `PFun`
      [def, depth 1, in-statement, role type-annotation]
   2. `Part`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   4. `PFun.prodLift`
      [def, depth 3, in-statement, role implicit-arg]
   5. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
