# Grading batch `testr_07` — 24 proofs

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

### proof_0145  (target depth 14, band 11-25)

THEOREM PROVED: `CategoryTheory.Functor.map_dite`

Grade all 8 candidates.

   1. `Decidable`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Not`
      [def, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   4. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   5. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   6. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `_private.Mathlib.CategoryTheory.Functor.Basic.0.CategoryTheory.Functor.map_dite._proof_1_1`
      [theorem, depth 13, introduced-by-proof, role applied]

### proof_0146  (target depth 11, band 11-25)

THEOREM PROVED: `CategoryTheory.prod.prodμ_counitIso_inv_app`

Grade all 18 candidates.

   1. `Prod.snd`
      [def, depth 1, in-statement, role explicit-arg]
   2. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   3. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   4. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   5. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Prod`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `CategoryTheory.prod`
      [def, depth 3, in-statement, role instance-slot]
   8. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
   9. `Prod.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  10. `CategoryTheory.Prod.mkHom`
      [def, depth 2, in-statement, role implicit-arg]
  11. `CategoryTheory.Category.comp_id`
      [theorem, depth 1, in-statement, role explicit-arg]
  12. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role implicit-arg]
  13. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  14. `Prod.fst`
      [def, depth 1, in-statement, role explicit-arg]
  15. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  16. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  17. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role explicit-arg]
  18. `CategoryTheory.prod'`
      [def, depth 10, in-statement, role instance-slot]

### proof_0147  (target depth 22, band 11-25)

THEOREM PROVED: `Char.ltTrichotomous`

Grade all 10 candidates.

   1. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   2. `Char.not_lt._simp_1`
      [theorem, depth 21, introduced-by-proof, role explicit-arg]
   3. `Char.le_antisymm`
      [theorem, depth 20, introduced-by-proof, role explicit-arg]
   4. `LT.lt`
      [def, depth 1, in-statement, role explicit-arg]
   5. `Char.instLT`
      [def, depth 16, in-statement, role instance-slot]
   6. `LE.le`
      [def, depth 1, introduced-by-proof, role implicit-arg]
   7. `Char.instLE`
      [def, depth 16, introduced-by-proof, role instance-slot]
   8. `Std.Trichotomous.mk`
      [constructor, depth 2, introduced-by-proof, role applied]
   9. `Not`
      [def, depth 1, introduced-by-proof, role implicit-arg]
  10. `Char`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0148  (target depth 11, band 11-25)

THEOREM PROVED: `GaloisInsertion.isGLB_of_u_image`

Grade all 21 candidates.

   1. `GaloisInsertion.gc`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   2. `Set.image`
      [def, depth 4, in-statement, role explicit-arg]
   3. `And.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   4. `GaloisInsertion.le_l_u`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   5. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   6. `GaloisConnection.l_le`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   8. `LE.le.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   9. `IsGLB`
      [def, depth 6, in-statement, role type-annotation]
  10. `GaloisInsertion`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  12. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `Monotone.mem_lowerBounds_image`
      [theorem, depth 8, introduced-by-proof, role unresolved]
  14. `upperBounds`
      [def, depth 4, in-statement, role explicit-arg]
  15. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  16. `GaloisConnection.monotone_l`
      [theorem, depth 10, introduced-by-proof, role explicit-arg]
  17. `Set.mem_image_of_mem`
      [theorem, depth 4, introduced-by-proof, role unresolved]
  18. `lowerBounds`
      [def, depth 4, in-statement, role explicit-arg]
  19. `And.left`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  20. `And.right`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  21. `GaloisConnection.monotone_u`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]

### proof_0149  (target depth 19, band 11-25)

THEOREM PROVED: `CategoryTheory.Grp.comp_hom_hom_assoc`

Grade all 25 candidates.

   1. `CategoryTheory.Mon`
      [inductive, depth 2, in-statement, role implicit-arg]
   2. `CategoryTheory.Category.assoc`
      [theorem, depth 1, in-statement, role explicit-arg]
   3. `CategoryTheory.Mon.Hom.hom`
      [def, depth 4, in-statement, role explicit-arg]
   4. `CategoryTheory.Grp.toMon`
      [def, depth 4, in-statement, role implicit-arg]
   5. `CategoryTheory.Grp.comp_hom_hom`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   6. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   7. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `CategoryTheory.Grp`
      [inductive, depth 2, in-statement, role implicit-arg]
   9. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  10. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  11. `CategoryTheory.CartesianMonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
  12. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  13. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  14. `CategoryTheory.Grp.instCategory`
      [def, depth 17, in-statement, role instance-slot]
  15. `CategoryTheory.InducedCategory.Hom.hom`
      [def, depth 2, in-statement, role explicit-arg]
  16. `CategoryTheory.SemiCartesianMonoidalCategory.toMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
  17. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]
  18. `CategoryTheory.CartesianMonoidalCategory.toSemiCartesianMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
  19. `CategoryTheory.Mon.instCategory`
      [def, depth 15, in-statement, role instance-slot]
  20. `forall_congr`
      [theorem, depth 5, in-statement, role explicit-arg]
  21. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, in-statement, role explicit-arg]
  22. `id`
      [def, depth 0, in-statement, role applied]
  23. `CategoryTheory.Grp.X`
      [def, depth 3, in-statement, role implicit-arg]
  24. `CategoryTheory.Mon.X`
      [def, depth 3, in-statement, role implicit-arg]
  25. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0150  (target depth 20, band 11-25)

THEOREM PROVED: `CategoryTheory.CommGrp.forget₂Grp_obj_one`

Grade all 21 candidates.

   1. `CategoryTheory.CartesianMonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `CategoryTheory.SemiCartesianMonoidalCategory.toMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
   3. `CategoryTheory.CommGrp`
      [inductive, depth 3, in-statement, role implicit-arg]
   4. `CategoryTheory.CommGrp.instCategory`
      [def, depth 19, in-statement, role instance-slot]
   5. `CategoryTheory.Grp`
      [inductive, depth 2, in-statement, role implicit-arg]
   6. `CategoryTheory.CartesianMonoidalCategory.toSemiCartesianMonoidalCategory`
      [def, depth 2, in-statement, role instance-slot]
   7. `CategoryTheory.Grp.grp`
      [def, depth 3, in-statement, role instance-slot]
   8. `CategoryTheory.Grp.instCategory`
      [def, depth 17, in-statement, role instance-slot]
   9. `CategoryTheory.BraidedCategory`
      [inductive, depth 2, in-statement, role type-annotation]
  10. `CategoryTheory.GrpObj.toMonObj`
      [def, depth 3, in-statement, role instance-slot]
  11. `CategoryTheory.CommGrp.forget₂Grp`
      [def, depth 18, in-statement, role explicit-arg]
  12. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
  14. `rfl`
      [def, depth 2, in-statement, role applied]
  15. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  16. `CategoryTheory.MonObj.one`
      [def, depth 3, in-statement, role implicit-arg]
  17. `CategoryTheory.Grp.X`
      [def, depth 3, in-statement, role explicit-arg]
  18. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  19. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  20. `CategoryTheory.MonoidalCategoryStruct.tensorUnit`
      [def, depth 2, in-statement, role explicit-arg]
  21. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]

### proof_0151  (target depth 13, band 11-25)

THEOREM PROVED: `SimpleGraph.Walk.notNilRec_cons`

Grade all 9 candidates.

   1. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   2. `SimpleGraph.Walk.cons`
      [constructor, depth 2, in-statement, role explicit-arg]
   3. `SimpleGraph`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `SimpleGraph.Walk.Nil`
      [inductive, depth 2, in-statement, role explicit-arg]
   5. `Not`
      [def, depth 1, in-statement, role type-annotation]
   6. `SimpleGraph.Walk.notNilRec`
      [def, depth 12, in-statement, role explicit-arg]
   7. `SimpleGraph.Adj`
      [def, depth 1, in-statement, role type-annotation]
   8. `SimpleGraph.Walk`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `SimpleGraph.Walk.not_nil_cons`
      [theorem, depth 11, in-statement, role explicit-arg]

### proof_0152  (target depth 19, band 11-25)

THEOREM PROVED: `Mathlib.Tactic.FieldSimp.NF.eval_cons_eq_eval_of_eq_of_eq`

Grade all 23 candidates.

   1. `Mathlib.Tactic.FieldSimp.NF.cons`
      [def, depth 2, in-statement, role explicit-arg]
   2. `id`
      [def, depth 0, in-statement, role explicit-arg]
   3. `Prod.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
   4. `Eq.refl`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `Prod.fst`
      [def, depth 1, introduced-by-proof, role explicit-arg]
   6. `Mathlib.Tactic.FieldSimp.NF.eval_cons`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   7. `MonoidWithZero.toMulZeroOneClass`
      [def, depth 5, in-statement, role instance-slot]
   8. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
   9. `GroupWithZero.toMonoidWithZero`
      [def, depth 1, in-statement, role instance-slot]
  10. `Mathlib.Tactic.FieldSimp.NF.eval`
      [def, depth 17, in-statement, role explicit-arg]
  11. `Eq.mpr`
      [def, depth 4, in-statement, role explicit-arg]
  12. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `instHMul`
      [def, depth 3, in-statement, role instance-slot]
  14. `MulZeroClass.toMul`
      [def, depth 1, in-statement, role instance-slot]
  15. `Prod.snd`
      [def, depth 1, introduced-by-proof, role explicit-arg]
  16. `Eq.symm`
      [theorem, depth 3, in-statement, role explicit-arg]
  17. `CommGroupWithZero.toGroupWithZero`
      [def, depth 10, in-statement, role instance-slot]
  18. `MulZeroOneClass.toMulZeroClass`
      [def, depth 5, in-statement, role instance-slot]
  19. `Mathlib.Tactic.FieldSimp.zpow'`
      [def, depth 14, in-statement, role explicit-arg]
  20. `HMul.hMul`
      [def, depth 2, in-statement, role explicit-arg]
  21. `Mathlib.Tactic.FieldSimp.NF`
      [def, depth 1, in-statement, role type-annotation]
  22. `CommGroupWithZero`
      [inductive, depth 0, in-statement, role type-annotation]
  23. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]

### proof_0153  (target depth 16, band 11-25)

THEOREM PROVED: `PFun.preimage_comp`

Grade all 3 candidates.

   1. `Set`
      [def, depth 0, in-statement, role type-annotation]
   2. `_private.Mathlib.Data.PFun.0.PFun.preimage_comp._proof_1_1`
      [theorem, depth 15, introduced-by-proof, role applied]
   3. `PFun`
      [def, depth 1, in-statement, role type-annotation]

### proof_0154  (target depth 18, band 11-25)

THEOREM PROVED: `Set.OrdConnected.isStronglyCoatomic`

Grade all 21 candidates.

   1. `OrderDual.ofDual`
      [def, depth 11, introduced-by-proof, role explicit-arg]
   2. `Subtype.preorder`
      [def, depth 10, in-statement, role instance-slot]
   3. `isStronglyAtomic_dual_iff_is_stronglyCoatomic`
      [theorem, depth 16, introduced-by-proof, role explicit-arg]
   4. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   5. `IsStronglyAtomic`
      [inductive, depth 1, introduced-by-proof, role implicit-arg]
   6. `Set.preimage`
      [def, depth 4, introduced-by-proof, role implicit-arg]
   7. `Set.OrdConnected.dual`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
   8. `OrderDual`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   9. `Set.OrdConnected`
      [inductive, depth 1, in-statement, role type-annotation]
  10. `EquivLike.toFunLike`
      [def, depth 8, introduced-by-proof, role instance-slot]
  11. `DFunLike.coe`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  12. `Equiv.instEquivLike`
      [def, depth 13, introduced-by-proof, role instance-slot]
  13. `IsStronglyCoatomic`
      [inductive, depth 1, in-statement, role implicit-arg]
  14. `Set.OrdConnected.isStronglyAtomic`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
  15. `OrderDual.instPreorder`
      [def, depth 10, introduced-by-proof, role instance-slot]
  16. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  17. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
  18. `Set.Elem`
      [def, depth 4, in-statement, role explicit-arg]
  19. `Iff.mp`
      [theorem, depth 1, in-statement, role applied]
  20. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
  21. `Equiv`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]

### proof_0155  (target depth 21, band 11-25)

THEOREM PROVED: `small_set_zero`

Grade all 4 candidates.

   1. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   3. `small_single`
      [theorem, depth 20, introduced-by-proof, role applied]
   4. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0156  (target depth 15, band 11-25)

THEOREM PROVED: `CategoryTheory.Functor.map_hom_inv'`

Grade all 20 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role implicit-arg]
   3. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   4. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   5. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
   7. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   8. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   9. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  10. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
  11. `CategoryTheory.Iso.map_hom_inv_id`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
  12. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
  13. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  14. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role explicit-arg]
  15. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `CategoryTheory.Functor.map`
      [def, depth 2, in-statement, role explicit-arg]
  17. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  18. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  19. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  20. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0157  (target depth 12, band 11-25)

THEOREM PROVED: `Disjoint.disjoint_sup_left_of_disjoint_sup_right`

Grade all 21 candidates.

   1. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   2. `Lattice.toSemilatticeSup`
      [def, depth 1, in-statement, role instance-slot]
   3. `propext`
      [axiom, depth 1, introduced-by-proof, role explicit-arg]
   4. `Lattice.toSemilatticeInf`
      [def, depth 3, in-statement, role instance-slot]
   5. `disjoint_comm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   6. `Eq`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   7. `SemilatticeSup.toMax`
      [def, depth 2, in-statement, role instance-slot]
   8. `IsModularLattice`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `SemilatticeInf.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
  10. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  11. `Lattice`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Disjoint`
      [def, depth 3, in-statement, role implicit-arg]
  13. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  14. `sup_comm`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
  15. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  16. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  17. `Disjoint.disjoint_sup_right_of_disjoint_sup_left`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
  18. `Max.max`
      [def, depth 1, in-statement, role explicit-arg]
  19. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  20. `Disjoint.symm`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  21. `OrderBot`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0158  (target depth 23, band 11-25)

THEOREM PROVED: `CategoryTheory.Pi.comapComp_inv_app`

Grade all 15 candidates.

   1. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   2. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
   3. `CategoryTheory.Functor.comp`
      [def, depth 15, in-statement, role implicit-arg]
   4. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   6. `CategoryTheory.Pi.comapComp`
      [def, depth 22, in-statement, role explicit-arg]
   7. `CategoryTheory.pi`
      [def, depth 10, in-statement, role instance-slot]
   8. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
   9. `CategoryTheory.NatTrans.app`
      [def, depth 3, in-statement, role explicit-arg]
  10. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
  11. `CategoryTheory.Pi.comap`
      [def, depth 12, in-statement, role explicit-arg]
  12. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
  13. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]
  14. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  15. `CategoryTheory.Pi.instCategoryComp`
      [def, depth 2, in-statement, role instance-slot]

### proof_0159  (target depth 13, band 11-25)

THEOREM PROVED: `isUnit_gcd_one_right`

Grade all 13 candidates.

   1. `isUnit_of_dvd_one`
      [theorem, depth 12, introduced-by-proof, role applied]
   2. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   3. `MulOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
   4. `CommMonoidWithZero`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `CommMonoidWithZero.toCommMonoid`
      [def, depth 1, in-statement, role instance-slot]
   6. `GCDMonoid.gcd`
      [def, depth 2, in-statement, role implicit-arg]
   7. `MulZeroOneClass.toMulOneClass`
      [def, depth 1, in-statement, role instance-slot]
   8. `CommMonoidWithZero.toMonoidWithZero`
      [def, depth 5, in-statement, role instance-slot]
   9. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  10. `GCDMonoid`
      [inductive, depth 1, in-statement, role type-annotation]
  11. `MonoidWithZero.toMulZeroOneClass`
      [def, depth 5, in-statement, role instance-slot]
  12. `GCDMonoid.gcd_dvd_right`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  13. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]

### proof_0160  (target depth 14, band 11-25)

THEOREM PROVED: `Multiset.prod_map_inv'`

Grade all 12 candidates.

   1. `invMonoidHom`
      [def, depth 11, introduced-by-proof, role explicit-arg]
   2. `DivisionCommMonoid.toCommMonoid`
      [def, depth 5, in-statement, role instance-slot]
   3. `DivisionCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Multiset.prod_hom`
      [theorem, depth 13, introduced-by-proof, role applied]
   5. `MonoidHom`
      [inductive, depth 1, introduced-by-proof, role implicit-arg]
   6. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   7. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
   8. `DivisionCommMonoid.toDivisionMonoid`
      [def, depth 1, in-statement, role instance-slot]
   9. `MonoidHom.instFunLike`
      [def, depth 10, introduced-by-proof, role instance-slot]
  10. `DivisionMonoid.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
  11. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  12. `Multiset`
      [def, depth 9, in-statement, role type-annotation]

### proof_0161  (target depth 20, band 11-25)

THEOREM PROVED: `Pi.one_lt_mulSingle`

Grade all 18 candidates.

   1. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   2. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   3. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
   4. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `lt_update_self_iff._simp_2`
      [theorem, depth 19, introduced-by-proof, role explicit-arg]
   6. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   7. `LT.lt`
      [def, depth 1, in-statement, role explicit-arg]
   8. `iff_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   9. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
  10. `Pi.preorder`
      [def, depth 10, in-statement, role instance-slot]
  11. `One.toOfNat1`
      [def, depth 3, in-statement, role instance-slot]
  12. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
  14. `Pi.mulSingle`
      [def, depth 7, in-statement, role explicit-arg]
  15. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  16. `One`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  18. `Pi.instOne`
      [def, depth 4, in-statement, role instance-slot]

### proof_0162  (target depth 12, band 11-25)

THEOREM PROVED: `sdiff_sdiff_self`

Grade all 21 candidates.

   1. `Lattice.toSemilatticeInf`
      [def, depth 3, introduced-by-proof, role instance-slot]
   2. `Lattice.toSemilatticeSup`
      [def, depth 1, in-statement, role instance-slot]
   3. `SemilatticeSup.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   4. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   5. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role explicit-arg]
   6. `GeneralizedCoheytingAlgebra.toSDiff`
      [def, depth 1, in-statement, role instance-slot]
   7. `GeneralizedCoheytingAlgebra`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   9. `Preorder.toLE`
      [def, depth 1, in-statement, role implicit-arg]
  10. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
  11. `SDiff.sdiff`
      [def, depth 1, in-statement, role explicit-arg]
  12. `sdiff_self`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
  13. `OrderBot.toBot`
      [def, depth 2, in-statement, role instance-slot]
  14. `SemilatticeInf.toPartialOrder`
      [def, depth 1, introduced-by-proof, role instance-slot]
  15. `Bot.bot`
      [def, depth 1, in-statement, role explicit-arg]
  16. `GeneralizedCoheytingAlgebra.toLattice`
      [def, depth 1, in-statement, role instance-slot]
  17. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  18. `bot_sdiff`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
  19. `GeneralizedCoheytingAlgebra.toOrderBot`
      [def, depth 1, in-statement, role instance-slot]
  20. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `sdiff_sdiff_comm`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]

### proof_0163  (target depth 12, band 11-25)

THEOREM PROVED: `lt_or_eq_of_le'`

Grade all 6 candidates.

   1. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Classical.propDecidable`
      [def, depth 11, introduced-by-proof, role instance-slot]
   3. `Decidable.lt_or_eq_of_le'`
      [theorem, depth 6, introduced-by-proof, role applied]
   4. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   5. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
   6. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]

### proof_0164  (target depth 18, band 11-25)

THEOREM PROVED: `AddCancelMonoid.ext_iff`

Grade all 17 candidates.

   1. `AddCancelMonoid.toAddRightCancelMonoid`
      [def, depth 3, in-statement, role instance-slot]
   2. `AddCancelMonoid.ext`
      [theorem, depth 17, introduced-by-proof, role explicit-arg]
   3. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   4. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `AddCancelMonoid`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `HEq`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
   7. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   8. `AddMonoid.toAddZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   9. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
  10. `HEq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
  11. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  12. `AddRightCancelMonoid.toAddMonoid`
      [def, depth 1, in-statement, role instance-slot]
  13. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  14. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
  15. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  16. `Eq.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  17. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]

### proof_0165  (target depth 22, band 11-25)

THEOREM PROVED: `Subgroup.comap_toSubmonoid`

Grade all 15 candidates.

   1. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   2. `MonoidHomClass.toMonoidHom`
      [def, depth 7, in-statement, role explicit-arg]
   3. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `rfl`
      [def, depth 2, in-statement, role applied]
   5. `MulEquiv.instEquivLike`
      [def, depth 16, in-statement, role instance-slot]
   6. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   7. `Subgroup`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
   9. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
  10. `MulEquiv`
      [inductive, depth 1, in-statement, role explicit-arg]
  11. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
  12. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
  13. `Subgroup.comap`
      [def, depth 21, in-statement, role explicit-arg]
  14. `Subgroup.toSubmonoid`
      [def, depth 2, in-statement, role implicit-arg]
  15. `Submonoid`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0166  (target depth 16, band 11-25)

THEOREM PROVED: `DividedPowers.dpow_one`

Grade all 4 candidates.

   1. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   3. `Ideal`
      [def, depth 14, in-statement, role type-annotation]
   4. `DividedPowers`
      [inductive, depth 15, in-statement, role type-annotation]

### proof_0167  (target depth 13, band 11-25)

THEOREM PROVED: `Sigma.instTrichotomousLex`

Grade all 16 candidates.

   1. `Or.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   2. `rfl`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   3. `trichotomous_of`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]
   4. `Std.trichotomous_of_rel_or_eq_or_rel_swap`
      [theorem, depth 7, introduced-by-proof, role applied]
   5. `Or.inl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   6. `Or`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   7. `Sigma.Lex.left`
      [constructor, depth 2, introduced-by-proof, role explicit-arg]
   8. `Or.inr`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   9. `Sigma.casesOn`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  10. `Sigma`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Eq`
      [inductive, depth 0, introduced-by-proof, role explicit-arg]
  12. `Sigma.Lex`
      [inductive, depth 1, in-statement, role explicit-arg]
  13. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  14. `Sigma.mk`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  15. `Sigma.Lex.right`
      [constructor, depth 2, introduced-by-proof, role explicit-arg]
  16. `Std.Trichotomous`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0168  (target depth 18, band 11-25)

THEOREM PROVED: `Equiv.psigmaCongrRight_refl`

Grade all 5 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `PSigma`
      [inductive, depth 0, in-statement, role explicit-arg]
   3. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Equiv.psigmaCongrRight`
      [def, depth 17, in-statement, role implicit-arg]
   5. `Equiv.refl`
      [def, depth 10, in-statement, role explicit-arg]
