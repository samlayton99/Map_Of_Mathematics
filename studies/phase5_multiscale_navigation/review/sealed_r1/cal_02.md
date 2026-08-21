# Grading batch `cal_02` — 24 proofs

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

### proof_0025  (target depth 26, band 26-50)

THEOREM PROVED: `CategoryTheory.PreZeroHypercover.sieve₀_eq_of_iso`

Grade all 15 candidates.

   1. `CategoryTheory.PreZeroHypercover`
      [inductive, depth 1, in-statement, role implicit-arg]
   2. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.PreZeroHypercover.instCategory`
      [def, depth 15, in-statement, role instance-slot]
   4. `CompleteLattice.toConditionallyCompleteLattice`
      [def, depth 9, introduced-by-proof, role instance-slot]
   5. `CategoryTheory.Sieve`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `CategoryTheory.Iso.inv`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   8. `ConditionallyCompletePartialOrder.toConditionallyCompletePartialOrderSup`
      [def, depth 1, introduced-by-proof, role instance-slot]
   9. `CategoryTheory.PreZeroHypercover.Hom.sieve₀_le_sieve₀`
      [theorem, depth 25, introduced-by-proof, role explicit-arg]
  10. `CategoryTheory.Iso.hom`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  11. `le_antisymm`
      [theorem, depth 2, introduced-by-proof, role applied]
  12. `CategoryTheory.Sieve.instCompleteLattice`
      [def, depth 21, introduced-by-proof, role instance-slot]
  13. `ConditionallyCompletePartialOrderSup.toPartialOrder`
      [def, depth 1, introduced-by-proof, role instance-slot]
  14. `ConditionallyCompleteLattice.toConditionallyCompletePartialOrder`
      [def, depth 8, introduced-by-proof, role instance-slot]
  15. `CategoryTheory.PreZeroHypercover.sieve₀`
      [def, depth 8, in-statement, role implicit-arg]

### proof_0026  (target depth 34, band 26-50)

THEOREM PROVED: `SSet.instNonemptySOfNonempty`

Grade all 17 candidates.

   1. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   2. `SimplexCategory.smallCategory`
      [def, depth 29, in-statement, role instance-slot]
   3. `CategoryTheory.types`
      [def, depth 10, in-statement, role instance-slot]
   4. `SSet.S.mk`
      [constructor, depth 33, introduced-by-proof, role explicit-arg]
   5. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `SimplexCategory`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
   8. `SSet.Nonempty`
      [def, depth 32, in-statement, role type-annotation]
   9. `Opposite.op`
      [constructor, depth 1, in-statement, role explicit-arg]
  10. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  11. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  12. `Classical.arbitrary`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  13. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `Nonempty.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
  15. `SSet`
      [def, depth 31, in-statement, role type-annotation]
  16. `SimplexCategory.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  17. `SSet.S`
      [inductive, depth 32, in-statement, role implicit-arg]

### proof_0027  (target depth 26, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.ConeMorphism.inv_hom_id`

Grade all 22 candidates.

   1. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role implicit-arg]
   2. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   5. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
   6. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  10. `CategoryTheory.Iso.inv_hom_id`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  11. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
  12. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role implicit-arg]
  13. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  14. `CategoryTheory.Limits.ConeMorphism.hom`
      [def, depth 4, in-statement, role explicit-arg]
  15. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  17. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  18. `CategoryTheory.Limits.Cone.category`
      [def, depth 25, in-statement, role instance-slot]
  19. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `CategoryTheory.Limits.Cone.pt`
      [def, depth 3, in-statement, role implicit-arg]
  22. `CategoryTheory.Limits.Cone`
      [inductive, depth 2, in-statement, role implicit-arg]

### proof_0028  (target depth 35, band 26-50)

THEOREM PROVED: `instSubsingletonQuaternion`

Grade all 5 candidates.

   1. `Neg`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `_private.Mathlib.Algebra.Quaternion.0.instSubsingletonQuaternion._proof_1`
      [theorem, depth 34, introduced-by-proof, role applied]
   3. `Subsingleton`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `One`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0029  (target depth 29, band 26-50)

THEOREM PROVED: `UInt8.toFin_mod`

Grade all 8 candidates.

   1. `UInt8.toFin`
      [def, depth 4, in-statement, role implicit-arg]
   2. `UInt8.size`
      [def, depth 4, in-statement, role explicit-arg]
   3. `instModUInt8`
      [def, depth 28, in-statement, role instance-slot]
   4. `rfl`
      [def, depth 2, in-statement, role applied]
   5. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]
   6. `instHMod`
      [def, depth 3, in-statement, role instance-slot]
   7. `HMod.hMod`
      [def, depth 2, in-statement, role explicit-arg]
   8. `UInt8`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0030  (target depth 31, band 26-50)

THEOREM PROVED: `Nat.mul_div_cancel_left'`

Grade all 16 candidates.

   1. `instMulNat`
      [def, depth 9, in-statement, role instance-slot]
   2. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `HDiv.hDiv`
      [def, depth 2, in-statement, role explicit-arg]
   4. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
   5. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
   8. `Nat.instDiv`
      [def, depth 19, in-statement, role instance-slot]
   9. `Nat.instDvd`
      [def, depth 10, in-statement, role instance-slot]
  10. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `Nat.div_mul_cancel`
      [theorem, depth 30, introduced-by-proof, role explicit-arg]
  12. `Nat.mul_comm`
      [theorem, depth 15, introduced-by-proof, role explicit-arg]
  13. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  14. `Dvd.dvd`
      [def, depth 1, in-statement, role type-annotation]
  15. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  16. `instHDiv`
      [def, depth 3, in-statement, role instance-slot]

### proof_0031  (target depth 29, band 26-50)

THEOREM PROVED: `CategoryTheory.MonoOver.lift_obj_arrow`

Grade all 19 candidates.

   1. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.Over.isMono`
      [def, depth 26, in-statement, role explicit-arg]
   3. `CategoryTheory.Over`
      [def, depth 24, in-statement, role implicit-arg]
   4. `CategoryTheory.MonoOver.arrow`
      [def, depth 28, in-statement, role implicit-arg]
   5. `CategoryTheory.MonoOver.lift`
      [def, depth 28, in-statement, role explicit-arg]
   6. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.MonoOver`
      [def, depth 27, in-statement, role implicit-arg]
   8. `CategoryTheory.MonoOver.forget`
      [def, depth 27, in-statement, role explicit-arg]
   9. `CategoryTheory.ObjectProperty.FullSubcategory.obj`
      [def, depth 3, in-statement, role explicit-arg]
  10. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  11. `CategoryTheory.instCategoryOver`
      [def, depth 26, in-statement, role instance-slot]
  12. `CategoryTheory.Over.hom`
      [def, depth 25, in-statement, role explicit-arg]
  13. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  14. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  15. `CategoryTheory.Over.left`
      [def, depth 25, in-statement, role explicit-arg]
  16. `CategoryTheory.ObjectProperty.FullSubcategory.category`
      [def, depth 10, in-statement, role instance-slot]
  17. `CategoryTheory.Mono`
      [inductive, depth 2, in-statement, role type-annotation]
  18. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  19. `rfl`
      [def, depth 2, in-statement, role applied]

### proof_0032  (target depth 26, band 26-50)

THEOREM PROVED: `Fin.natAdd_inj`

Grade all 12 candidates.

   1. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
   2. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Fin.strictMono_natAdd`
      [theorem, depth 25, introduced-by-proof, role explicit-arg]
   5. `StrictMono.injective`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
   6. `Function.Injective.eq_iff`
      [theorem, depth 4, introduced-by-proof, role applied]
   7. `Fin.instPartialOrder`
      [def, depth 24, introduced-by-proof, role instance-slot]
   8. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   9. `Fin.natAdd`
      [def, depth 17, in-statement, role implicit-arg]
  10. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Fin.instLinearOrder`
      [def, depth 23, introduced-by-proof, role instance-slot]
  12. `PartialOrder.toPreorder`
      [def, depth 1, introduced-by-proof, role instance-slot]

### proof_0033  (target depth 27, band 26-50)

THEOREM PROVED: `SimpleGraph.Iso.induce_comp_induce`

Grade all 12 candidates.

   1. `SimpleGraph.Iso.induce`
      [def, depth 26, in-statement, role explicit-arg]
   2. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   3. `SimpleGraph.Adj`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Set.BijOn`
      [def, depth 7, in-statement, role type-annotation]
   5. `Set`
      [def, depth 0, in-statement, role type-annotation]
   6. `RelIso.instFunLike`
      [def, depth 20, in-statement, role instance-slot]
   7. `SimpleGraph.Iso.comp`
      [def, depth 23, in-statement, role explicit-arg]
   8. `Set.Elem`
      [def, depth 4, in-statement, role implicit-arg]
   9. `SimpleGraph.induce`
      [def, depth 11, in-statement, role implicit-arg]
  10. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  11. `SimpleGraph.Iso`
      [def, depth 2, in-statement, role implicit-arg]
  12. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0034  (target depth 39, band 26-50)

THEOREM PROVED: `CategoryTheory.Limits.Pi.equivalenceOfEquivCompPointwiseProduct_inv_app`

Grade all 21 candidates.

   1. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   2. `CategoryTheory.Equivalence.inverse`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   4. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
   6. `CategoryTheory.Limits.pointwiseProduct`
      [def, depth 36, in-statement, role explicit-arg]
   7. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
   8. `CategoryTheory.Limits.HasProductsOfShape`
      [def, depth 11, in-statement, role type-annotation]
   9. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role explicit-arg]
  10. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  11. `CategoryTheory.pi`
      [def, depth 10, in-statement, role instance-slot]
  12. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role explicit-arg]
  13. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  14. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
  15. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  16. `CategoryTheory.Limits.Pi.equivalenceOfEquivCompPointwiseProduct`
      [def, depth 38, in-statement, role explicit-arg]
  17. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  19. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  20. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `CategoryTheory.Pi.equivalenceOfEquiv`
      [def, depth 29, in-statement, role explicit-arg]

### proof_0035  (target depth 29, band 26-50)

THEOREM PROVED: `Std.Sat.CNF.relabel_empty`

Grade all 22 candidates.

   1. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Std.Sat.CNF.mk`
      [constructor, depth 3, in-statement, role explicit-arg]
   3. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `Array`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `List.map`
      [def, depth 6, in-statement, role explicit-arg]
   6. `Std.Sat.CNF.clauses`
      [def, depth 1, in-statement, role explicit-arg]
   7. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   8. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `Array.map`
      [def, depth 23, in-statement, role implicit-arg]
  10. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `Std.Sat.CNF.Clause.relabel`
      [def, depth 7, in-statement, role explicit-arg]
  12. `List.map_nil`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  13. `Std.Sat.CNF.relabel`
      [def, depth 24, in-statement, role explicit-arg]
  14. `Std.Sat.CNF.empty`
      [def, depth 4, in-statement, role explicit-arg]
  15. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  16. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `Std.Sat.CNF.Clause`
      [def, depth 2, in-statement, role implicit-arg]
  18. `List.map_toArray`
      [theorem, depth 28, introduced-by-proof, role explicit-arg]
  19. `List.toArray`
      [def, depth 2, in-statement, role explicit-arg]
  20. `Std.Sat.CNF`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  22. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_0036  (target depth 30, band 26-50)

THEOREM PROVED: `CategoryTheory.Presheaf.isLocallySurjective_of_isLocallySurjective_fac`

Grade all 16 candidates.

   1. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   2. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.ConcreteCategory`
      [inductive, depth 3, in-statement, role type-annotation]
   4. `Opposite`
      [inductive, depth 0, in-statement, role explicit-arg]
   5. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   6. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   7. `CategoryTheory.Presheaf.IsLocallySurjective`
      [inductive, depth 20, in-statement, role type-annotation]
   8. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `FunLike`
      [def, depth 2, in-statement, role type-annotation]
  10. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Eq.ndrec`
      [def, depth 3, in-statement, role applied]
  12. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  13. `CategoryTheory.GrothendieckTopology`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  15. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  16. `CategoryTheory.Presheaf.isLocallySurjective_of_isLocallySurjective`
      [theorem, depth 29, introduced-by-proof, role explicit-arg]

### proof_0037  (target depth 69, band 51-75)

THEOREM PROVED: `Ideal.mul_left_self_sup`

Grade all 23 candidates.

   1. `Ideal.mul_le_right`
      [theorem, depth 68, introduced-by-proof, role explicit-arg]
   2. `Semiring.toModule`
      [def, depth 13, in-statement, role instance-slot]
   3. `sup_eq_right`
      [theorem, depth 7, in-statement, role explicit-arg]
   4. `SemilatticeSup.toMax`
      [def, depth 2, in-statement, role instance-slot]
   5. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   6. `CompleteLattice.toConditionallyCompleteLattice`
      [def, depth 9, in-statement, role instance-slot]
   7. `Monoid.toMulAction`
      [def, depth 7, in-statement, role instance-slot]
   8. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]
  10. `Semiring.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  11. `Lattice.toSemilatticeSup`
      [def, depth 1, in-statement, role instance-slot]
  12. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  13. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  14. `ConditionallyCompleteLattice.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  15. `Submodule.mul`
      [def, depth 67, in-statement, role instance-slot]
  16. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  17. `Ideal`
      [def, depth 14, in-statement, role type-annotation]
  18. `Max.max`
      [def, depth 1, in-statement, role explicit-arg]
  19. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `Submodule.completeLattice`
      [def, depth 62, in-statement, role instance-slot]
  21. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  22. `SemilatticeSup.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  23. `Semiring.toAddCommMonoid`
      [def, depth 1, in-statement, role instance-slot]

### proof_0038  (target depth 59, band 51-75)

THEOREM PROVED: `Set.smul_set_inter`

Grade all 12 candidates.

   1. `Monoid.toSemigroup`
      [def, depth 1, in-statement, role implicit-arg]
   2. `MulAction.injective`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
   3. `instHSMul`
      [def, depth 3, in-statement, role instance-slot]
   4. `SemigroupAction.toSMul`
      [def, depth 2, in-statement, role instance-slot]
   5. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
   6. `Set.image_inter`
      [theorem, depth 58, introduced-by-proof, role applied]
   7. `MulAction`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
   9. `HSMul.hSMul`
      [def, depth 2, in-statement, role implicit-arg]
  10. `Set`
      [def, depth 0, in-statement, role type-annotation]
  11. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `MulAction.toSemigroupAction`
      [def, depth 2, in-statement, role instance-slot]

### proof_0039  (target depth 70, band 51-75)

THEOREM PROVED: `Std.ExtHashMap.getKeyD_eq_getD_getKey?`

Grade all 7 candidates.

   1. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Std.ExtHashMap`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Std.ExtDHashMap.getKeyD_eq_getD_getKey?`
      [theorem, depth 69, introduced-by-proof, role applied]
   7. `Std.ExtHashMap.inner`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0040  (target depth 66, band 51-75)

THEOREM PROVED: `List.length_eq_succ_iff`

Grade all 3 candidates.

   1. `_private.Mathlib.Data.List.Basic.0.List.length_eq_succ_iff._proof_1_1`
      [theorem, depth 65, introduced-by-proof, role applied]
   2. `List`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Nat`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0041  (target depth 64, band 51-75)

THEOREM PROVED: `SSet.StrictSegalCore.spineToSimplex_zero`

Grade all 16 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   3. `SimplexCategory`
      [inductive, depth 0, in-statement, role explicit-arg]
   4. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `SSet`
      [def, depth 31, in-statement, role type-annotation]
   6. `Opposite.op`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   8. `SSet.Path`
      [def, depth 55, in-statement, role type-annotation]
   9. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role implicit-arg]
  10. `SSet.StrictSegalCore`
      [inductive, depth 32, in-statement, role type-annotation]
  11. `SimplexCategory.smallCategory`
      [def, depth 29, in-statement, role instance-slot]
  12. `CategoryTheory.Category.opposite`
      [def, depth 10, in-statement, role instance-slot]
  13. `SimplexCategory.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  14. `SSet.StrictSegalCore.spineToSimplex`
      [def, depth 63, in-statement, role implicit-arg]
  15. `CategoryTheory.types`
      [def, depth 10, in-statement, role instance-slot]
  16. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0042  (target depth 52, band 51-75)

THEOREM PROVED: `wbtw_rotate_iff`

Grade all 23 candidates.

   1. `wbtw_swap_right_iff`
      [theorem, depth 51, introduced-by-proof, role explicit-arg]
   2. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
   3. `Ring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   4. `AddCommGroup.toAddCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   5. `id`
      [def, depth 0, in-statement, role explicit-arg]
   6. `AddCommGroup`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `IsOrderedRing`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Wbtw`
      [def, depth 46, in-statement, role explicit-arg]
   9. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  10. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Ring`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `propext`
      [axiom, depth 1, in-statement, role explicit-arg]
  13. `AddTorsor`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
  15. `Iff`
      [inductive, depth 0, in-statement, role explicit-arg]
  16. `wbtw_comm`
      [theorem, depth 50, introduced-by-proof, role explicit-arg]
  17. `Iff.rfl`
      [theorem, depth 3, in-statement, role explicit-arg]
  18. `eq_comm`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  19. `AddCommGroup.toAddGroup`
      [def, depth 1, in-statement, role instance-slot]
  20. `And`
      [inductive, depth 0, in-statement, role explicit-arg]
  21. `IsDomain`
      [inductive, depth 1, in-statement, role type-annotation]
  22. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  23. `Module.IsTorsionFree`
      [inductive, depth 2, in-statement, role type-annotation]

### proof_0043  (target depth 72, band 51-75)

THEOREM PROVED: `ContinuousAt.inf`

Grade all 5 candidates.

   1. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Min`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `ContinuousAt`
      [def, depth 19, in-statement, role type-annotation]
   4. `ContinuousAt.inf'`
      [theorem, depth 71, introduced-by-proof, role applied]
   5. `ContinuousInf`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0044  (target depth 71, band 51-75)

THEOREM PROVED: `Std.HashMap.Raw.getElem_map'`

Grade all 12 candidates.

   1. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Std.HashMap.Raw.WF`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `Std.HashMap.Raw.instMembershipOfBEqOfHashable`
      [def, depth 54, in-statement, role instance-slot]
   4. `Std.HashMap.Raw`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Std.DHashMap.Raw.Const.get_map'`
      [theorem, depth 70, introduced-by-proof, role applied]
   6. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Std.HashMap.Raw.map`
      [def, depth 48, in-statement, role explicit-arg]
   9. `Std.HashMap.Raw.inner`
      [def, depth 1, in-statement, role implicit-arg]
  10. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Std.HashMap.Raw.WF.out`
      [theorem, depth 2, in-statement, role explicit-arg]
  12. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]

### proof_0045  (target depth 61, band 51-75)

THEOREM PROVED: `CategoryTheory.ComposableArrows.threeδ₃Toδ₂_app_zero`

Grade all 22 candidates.

   1. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role implicit-arg]
   2. `Fin.instPartialOrder`
      [def, depth 24, in-statement, role instance-slot]
   3. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   4. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
   5. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   7. `CategoryTheory.ComposableArrows.threeδ₃Toδ₂`
      [def, depth 60, in-statement, role explicit-arg]
   8. `Fin.instOfNat`
      [def, depth 24, in-statement, role instance-slot]
   9. `rfl`
      [def, depth 2, in-statement, role applied]
  10. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  11. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
  12. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Fin`
      [inductive, depth 1, in-statement, role explicit-arg]
  14. `Preorder.smallCategory`
      [def, depth 10, in-statement, role instance-slot]
  15. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  17. `CategoryTheory.ComposableArrows.mk₂`
      [def, depth 58, in-statement, role explicit-arg]
  18. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  19. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  20. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  21. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
  22. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]

### proof_0046  (target depth 54, band 51-75)

THEOREM PROVED: `Array.flatMapM_unattach`

Grade all 24 candidates.

   1. `Array.flatMapM`
      [def, depth 23, in-statement, role implicit-arg]
   2. `Array`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `binderNameHint`
      [def, depth 0, in-statement, role explicit-arg]
   4. `Array.flatMapM_subtype`
      [theorem, depth 53, introduced-by-proof, role explicit-arg]
   5. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   6. `Array.foldlM_unattach.match_1`
      [def, depth 4, in-statement, role explicit-arg]
   7. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `wfParam`
      [def, depth 0, in-statement, role explicit-arg]
   9. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
  10. `Unit.unit`
      [def, depth 2, in-statement, role explicit-arg]
  11. `Array.flatMapM_congr`
      [theorem, depth 52, introduced-by-proof, role explicit-arg]
  12. `Array.unattach`
      [def, depth 24, in-statement, role explicit-arg]
  13. `LawfulMonad`
      [inductive, depth 1, in-statement, role type-annotation]
  14. `Monad`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
  16. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  17. `True`
      [inductive, depth 0, in-statement, role implicit-arg]
  18. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
  19. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
  20. `Unit`
      [def, depth 1, in-statement, role implicit-arg]
  21. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  22. `Subtype.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  23. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
  24. `Subtype`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0047  (target depth 67, band 51-75)

THEOREM PROVED: `Std.DHashMap.Raw.map_id_equiv`

Grade all 25 candidates.

   1. `Array.size`
      [def, depth 10, in-statement, role explicit-arg]
   2. `Std.DHashMap.Internal.Raw₀.map_id_equiv`
      [theorem, depth 50, introduced-by-proof, role explicit-arg]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
   5. `Std.DHashMap.Raw`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Subtype.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `Std.DHashMap.Raw.buckets`
      [def, depth 1, in-statement, role explicit-arg]
   8. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   9. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  10. `Std.DHashMap.Raw.WF`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
  12. `Std.DHashMap.Internal.AssocList`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `Std.DHashMap.Raw.WF.size_buckets_pos`
      [theorem, depth 65, introduced-by-proof, role explicit-arg]
  15. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
  16. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  17. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  19. `id`
      [def, depth 0, in-statement, role explicit-arg]
  20. `Std.DHashMap.Internal.Raw₀.map`
      [def, depth 30, in-statement, role explicit-arg]
  21. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
  22. `Std.DHashMap.Internal.Raw.map_eq`
      [theorem, depth 66, introduced-by-proof, role explicit-arg]
  23. `Std.DHashMap.Raw.Equiv`
      [inductive, depth 1, in-statement, role implicit-arg]
  24. `Std.DHashMap.Raw.map`
      [def, depth 47, in-statement, role explicit-arg]
  25. `Eq.mpr`
      [def, depth 4, in-statement, role applied]

### proof_0048  (target depth 52, band 51-75)

THEOREM PROVED: `Fin.removeNth_removeNth_heq_swap`

Grade all 24 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `instAddNat`
      [def, depth 7, in-statement, role instance-slot]
   3. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
   4. `implies_congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `Fin.predAbove`
      [def, depth 27, in-statement, role explicit-arg]
   6. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   7. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Fin.succAbove`
      [def, depth 18, in-statement, role explicit-arg]
   9. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
  10. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  11. `HEq`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `Function.hfunext`
      [theorem, depth 16, introduced-by-proof, role applied]
  13. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  14. `_private.Mathlib.Data.Fin.Tuple.Basic.0.Fin.removeNth_removeNth_heq_swap._simp_1_1`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  15. `Fin.removeNth`
      [def, depth 19, in-statement, role explicit-arg]
  16. `Eq.ndrec`
      [def, depth 3, in-statement, role explicit-arg]
  17. `Fin.succAbove_succAbove_succAbove_predAbove`
      [theorem, depth 51, introduced-by-proof, role explicit-arg]
  18. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  19. `id`
      [def, depth 0, in-statement, role explicit-arg]
  20. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  21. `congr_arg_heq`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
  22. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  23. `Fin`
      [inductive, depth 1, in-statement, role type-annotation]
  24. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
