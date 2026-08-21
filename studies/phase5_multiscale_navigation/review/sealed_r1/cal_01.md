# Grading batch `cal_01` — 24 proofs

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

### proof_0001  (target depth 6, band 0-10)

THEOREM PROVED: `Sum.isLeft_inl`

Grade all 4 candidates.

   1. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   3. `Sum.inl`
      [constructor, depth 1, in-statement, role explicit-arg]
   4. `Sum.isLeft`
      [def, depth 5, in-statement, role implicit-arg]

### proof_0002  (target depth 5, band 0-10)

THEOREM PROVED: `instNontrivialProp`

Grade all 7 candidates.

   1. `Exists`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
   2. `Ne`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   3. `true_ne_false`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   4. `False`
      [inductive, depth 0, introduced-by-proof, role explicit-arg]
   5. `Exists.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   6. `Nontrivial.mk`
      [constructor, depth 3, introduced-by-proof, role applied]
   7. `True`
      [inductive, depth 0, introduced-by-proof, role explicit-arg]

### proof_0003  (target depth 3, band 0-10)

THEOREM PROVED: `le_of_lt`

Grade all 10 candidates.

   1. `lt_iff_le_not_ge`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   2. `Iff.mp`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   3. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   4. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
   5. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
   6. `And.left`
      [theorem, depth 1, introduced-by-proof, role applied]
   7. `LT.lt`
      [def, depth 1, in-statement, role implicit-arg]
   8. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `Not`
      [def, depth 1, introduced-by-proof, role explicit-arg]
  10. `And`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]

### proof_0004  (target depth 3, band 0-10)

THEOREM PROVED: `ApplicativeTransformation.app_eq_coe`

Grade all 4 candidates.

   1. `ApplicativeTransformation`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Applicative`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `ApplicativeTransformation.app`
      [def, depth 2, in-statement, role implicit-arg]
   4. `rfl`
      [def, depth 2, introduced-by-proof, role applied]

### proof_0005  (target depth 4, band 0-10)

THEOREM PROVED: `Derivation.map_one_eq_zero`

Grade all 7 candidates.

   1. `Derivation`
      [inductive, depth 2, in-statement, role type-annotation]
   2. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Derivation.map_one_eq_zero'`
      [theorem, depth 3, introduced-by-proof, role applied]
   4. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   5. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Algebra`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0006  (target depth 7, band 0-10)

THEOREM PROVED: `Decidable.not_and_iff_not_or_not`

Grade all 10 candidates.

   1. `And`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `not_and_of_not_or_not`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   3. `And.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   4. `Or.inr`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   5. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   6. `Or.inl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   7. `Decidable`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `dite`
      [def, depth 5, introduced-by-proof, role explicit-arg]
   9. `Not`
      [def, depth 1, in-statement, role explicit-arg]
  10. `Or`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0007  (target depth 8, band 0-10)

THEOREM PROVED: `Std.Internal.Do.Triple.iff`

Grade all 10 candidates.

   1. `Std.Internal.Do.Triple.intro`
      [constructor, depth 4, introduced-by-proof, role explicit-arg]
   2. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   3. `Std.Internal.Do.WP`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `_private.Std.Internal.Do.Triple.Basic.0.Std.Internal.Do.Triple.iff.match_1_1`
      [def, depth 7, introduced-by-proof, role explicit-arg]
   5. `Std.Internal.Do.Triple`
      [inductive, depth 2, in-statement, role type-annotation]
   6. `Std.Internal.Do.Assertion.toCompleteLattice`
      [def, depth 1, in-statement, role instance-slot]
   7. `Lean.Order.PartialOrder.rel`
      [def, depth 1, in-statement, role type-annotation]
   8. `Lean.Order.CompleteLattice.toPartialOrder`
      [def, depth 1, in-statement, role instance-slot]
   9. `Std.Internal.Do.WP.wp`
      [def, depth 3, in-statement, role explicit-arg]
  10. `Std.Internal.Do.Assertion`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0008  (target depth 3, band 0-10)

THEOREM PROVED: `Pi.sup_def`

Grade all 4 candidates.

   1. `Max.max`
      [def, depth 1, in-statement, role implicit-arg]
   2. `Pi.instMaxForall_mathlib`
      [def, depth 2, in-statement, role instance-slot]
   3. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   4. `Max`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0009  (target depth 4, band 0-10)

THEOREM PROVED: `Set.zero_mem_zero`

Grade all 4 candidates.

   1. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role applied]
   2. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   3. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   4. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0010  (target depth 10, band 0-10)

THEOREM PROVED: `TopologicalSpace.OpenNhds.op_map_id_obj`

Grade all 7 candidates.

   1. `TopCat.carrier`
      [def, depth 1, in-statement, role type-annotation]
   2. `TopologicalSpace.OpenNhds`
      [def, depth 9, in-statement, role explicit-arg]
   3. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   4. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Opposite`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `TopCat`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]

### proof_0011  (target depth 4, band 0-10)

THEOREM PROVED: `Std.Internal.Do.WPMonad.wp_monadLift_refl_apply_eq`

Grade all 9 candidates.

   1. `Pure`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Monad`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.Internal.Do.WPMonad`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.Internal.Do.instWPOfWPMonad`
      [def, depth 3, in-statement, role instance-slot]
   5. `MonadLiftT.monadLift`
      [def, depth 1, in-statement, role explicit-arg]
   6. `Std.Internal.Do.WP.wp`
      [def, depth 3, in-statement, role implicit-arg]
   7. `instMonadLiftT`
      [def, depth 2, in-statement, role instance-slot]
   8. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   9. `Std.Internal.Do.Assertion`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0012  (target depth 5, band 0-10)

THEOREM PROVED: `Unitization.fst_inr`

Grade all 5 candidates.

   1. `Unitization.inr`
      [def, depth 4, in-statement, role explicit-arg]
   2. `Zero`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Unitization.toProd`
      [def, depth 1, in-statement, role explicit-arg]
   4. `Prod.fst`
      [def, depth 1, in-statement, role implicit-arg]
   5. `rfl`
      [def, depth 2, introduced-by-proof, role applied]

### proof_0013  (target depth 20, band 11-25)

THEOREM PROVED: `CategoryTheory.ObjectProperty.instContainsZeroTopOfHasZeroObject`

Grade all 18 candidates.

   1. `And.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `CategoryTheory.Limits.IsZero`
      [inductive, depth 1, introduced-by-proof, role explicit-arg]
   3. `CategoryTheory.ObjectProperty.ContainsZero.mk`
      [constructor, depth 3, introduced-by-proof, role applied]
   4. `CategoryTheory.Limits.HasZeroObject`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   6. `CategoryTheory.Limits.isZero_zero`
      [theorem, depth 9, introduced-by-proof, role explicit-arg]
   7. `CategoryTheory.Limits.HasZeroObject.zero'`
      [def, depth 9, introduced-by-proof, role instance-slot]
   8. `True.intro`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Prop.instBooleanAlgebra`
      [def, depth 19, in-statement, role instance-slot]
  11. `Pi.instTopForall`
      [def, depth 2, in-statement, role instance-slot]
  12. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  13. `Top.top`
      [def, depth 1, in-statement, role implicit-arg]
  14. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `Zero.toOfNat0`
      [def, depth 3, introduced-by-proof, role instance-slot]
  16. `CategoryTheory.ObjectProperty`
      [def, depth 1, in-statement, role implicit-arg]
  17. `BooleanAlgebra.toTop`
      [def, depth 1, in-statement, role instance-slot]
  18. `Exists.intro`
      [constructor, depth 1, in-statement, role explicit-arg]

### proof_0014  (target depth 11, band 11-25)

THEOREM PROVED: `Sum.Lex.inl_le_inl_iff`

Grade all 3 candidates.

   1. `LE`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Sum.lex_inl_inl`
      [theorem, depth 10, introduced-by-proof, role applied]
   3. `LE.le`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0015  (target depth 16, band 11-25)

THEOREM PROVED: `Topology.WithUpperSet.map_id`

Grade all 7 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `OrderHom.id`
      [def, depth 4, in-statement, role explicit-arg]
   3. `Topology.WithUpperSet.map`
      [def, depth 15, in-statement, role implicit-arg]
   4. `Topology.WithUpperSet`
      [def, depth 0, in-statement, role explicit-arg]
   5. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `ContinuousMap`
      [inductive, depth 1, in-statement, role implicit-arg]
   7. `Topology.WithUpperSet.instTopologicalSpace`
      [def, depth 9, in-statement, role instance-slot]

### proof_0016  (target depth 16, band 11-25)

THEOREM PROVED: `SubMulAction.compl_def`

Grade all 13 candidates.

   1. `MulAction`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
   3. `Monoid.toSemigroup`
      [def, depth 1, in-statement, role implicit-arg]
   4. `MulAction.toSemigroupAction`
      [def, depth 2, in-statement, role instance-slot]
   5. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
   6. `rfl`
      [def, depth 2, in-statement, role applied]
   7. `SemigroupAction.toSMul`
      [def, depth 2, in-statement, role instance-slot]
   8. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `SubMulAction`
      [inductive, depth 1, in-statement, role implicit-arg]
  10. `Compl.compl`
      [def, depth 1, in-statement, role explicit-arg]
  11. `SubMulAction.instCompl`
      [def, depth 15, in-statement, role instance-slot]
  12. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  13. `SubMulAction.carrier`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0017  (target depth 12, band 11-25)

THEOREM PROVED: `Fin.sigma_eq_iff_eq_comp_cast`

Grade all 20 candidates.

   1. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   2. `Fin.rec`
      [recursor, depth 5, introduced-by-proof, role explicit-arg]
   3. `Fin.mk`
      [constructor, depth 4, in-statement, role unresolved]
   4. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Eq.rec`
      [recursor, depth 2, in-statement, role explicit-arg]
   6. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   7. `_private.Mathlib.Data.Fin.Tuple.Basic.0.Fin.sigma_eq_iff_eq_comp_cast.match_1_1`
      [def, depth 6, introduced-by-proof, role explicit-arg]
   8. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   9. `Fin`
      [inductive, depth 1, in-statement, role implicit-arg]
  10. `Sigma.snd`
      [def, depth 1, in-statement, role explicit-arg]
  11. `rfl`
      [def, depth 2, introduced-by-proof, role explicit-arg]
  12. `Exists.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  13. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `Sigma`
      [inductive, depth 0, in-statement, role implicit-arg]
  15. `funext`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  16. `Exists`
      [inductive, depth 0, in-statement, role implicit-arg]
  17. `Fin.sigma_eq_of_eq_comp_cast`
      [theorem, depth 11, introduced-by-proof, role explicit-arg]
  18. `Function.comp`
      [def, depth 0, in-statement, role explicit-arg]
  19. `Sigma.fst`
      [def, depth 1, in-statement, role explicit-arg]
  20. `Fin.cast`
      [def, depth 5, in-statement, role explicit-arg]

### proof_0018  (target depth 21, band 11-25)

THEOREM PROVED: `Monotone.withBot_map`

Grade all 7 candidates.

   1. `Monotone`
      [def, depth 2, in-statement, role implicit-arg]
   2. `WithBot.monotone_map_iff`
      [theorem, depth 20, introduced-by-proof, role explicit-arg]
   3. `WithBot.instPreorder`
      [def, depth 18, in-statement, role instance-slot]
   4. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Iff.mpr`
      [theorem, depth 1, in-statement, role applied]
   6. `WithBot.map`
      [def, depth 6, in-statement, role explicit-arg]
   7. `WithBot`
      [def, depth 1, in-statement, role implicit-arg]

### proof_0019  (target depth 13, band 11-25)

THEOREM PROVED: `List.rdropWhile_concat_neg`

Grade all 19 candidates.

   1. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `instHAppendOfAppend`
      [def, depth 3, in-statement, role instance-slot]
   3. `id`
      [def, depth 0, introduced-by-proof, role explicit-arg]
   4. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   6. `List.cons`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `List.rdropWhile_concat`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]
   8. `HAppend.hAppend`
      [def, depth 2, in-statement, role explicit-arg]
   9. `List.instAppend`
      [def, depth 7, in-statement, role instance-slot]
  10. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  11. `List.rdropWhile`
      [def, depth 8, in-statement, role explicit-arg]
  12. `ite`
      [def, depth 5, introduced-by-proof, role explicit-arg]
  13. `Not`
      [def, depth 1, in-statement, role type-annotation]
  14. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  15. `Bool.true`
      [constructor, depth 1, in-statement, role explicit-arg]
  16. `Eq.mpr`
      [def, depth 4, introduced-by-proof, role applied]
  17. `instDecidableEqBool`
      [def, depth 7, introduced-by-proof, role implicit-arg]
  18. `if_neg`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
  19. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0020  (target depth 13, band 11-25)

THEOREM PROVED: `Subrel.coe_inclusionEmbedding`

Grade all 12 candidates.

   1. `RelEmbedding`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   3. `Subrel.inclusionEmbedding`
      [def, depth 12, in-statement, role explicit-arg]
   4. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   5. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   6. `rfl`
      [def, depth 2, in-statement, role applied]
   7. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   8. `RelEmbedding.instFunLike`
      [def, depth 11, in-statement, role instance-slot]
   9. `Set.instLE`
      [def, depth 5, in-statement, role instance-slot]
  10. `Subrel`
      [def, depth 2, in-statement, role explicit-arg]
  11. `Subtype`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0021  (target depth 15, band 11-25)

THEOREM PROVED: `String.Pos.Raw.byteIdx_addString`

Grade all 3 candidates.

   1. `String.Pos.Raw.byteIdx_add_string`
      [theorem, depth 14, introduced-by-proof, role applied]
   2. `String`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `String.Pos.Raw`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0022  (target depth 13, band 11-25)

THEOREM PROVED: `AddSubmonoid.add._proof_1`

Grade all 9 candidates.

   1. `AddSubmonoid`
      [inductive, depth 1, in-statement, role implicit-arg]
   2. `AddSubmonoid.add_mem`
      [theorem, depth 12, introduced-by-proof, role applied]
   3. `Membership.mem`
      [def, depth 2, in-statement, role explicit-arg]
   4. `AddZeroClass`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Subtype.property`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
   6. `AddSubmonoid.instSetLike`
      [def, depth 10, in-statement, role instance-slot]
   7. `SetLike.instMembership`
      [def, depth 4, in-statement, role instance-slot]
   8. `Subtype.val`
      [def, depth 1, in-statement, role implicit-arg]
   9. `Subtype`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0023  (target depth 22, band 11-25)

THEOREM PROVED: `isAntichain_and_least_iff`

Grade all 24 candidates.

   1. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
   2. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   3. `Set.eq_singleton_iff_unique_mem`
      [theorem, depth 21, introduced-by-proof, role explicit-arg]
   4. `IsAntichain.singleton`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   5. `Singleton.singleton`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Iff.intro`
      [constructor, depth 1, introduced-by-proof, role applied]
   7. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `IsLeast`
      [def, depth 5, in-statement, role implicit-arg]
   9. `isLeast_singleton`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
  10. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  11. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  12. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  13. `And.right`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  14. `And.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  15. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  16. `And.left`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  17. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  18. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  19. `lowerBounds`
      [def, depth 4, in-statement, role explicit-arg]
  20. `Set.instSingletonSet`
      [def, depth 3, in-statement, role instance-slot]
  21. `IsAntichain`
      [def, depth 5, in-statement, role implicit-arg]
  22. `IsAntichain.eq'`
      [theorem, depth 17, introduced-by-proof, role explicit-arg]
  23. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  24. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0024  (target depth 12, band 11-25)

THEOREM PROVED: `Int.cast_ite`

Grade all 5 candidates.

   1. `Decidable`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Int`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `apply_ite`
      [theorem, depth 11, introduced-by-proof, role applied]
   4. `Int.cast`
      [def, depth 2, in-statement, role explicit-arg]
   5. `IntCast`
      [inductive, depth 0, in-statement, role type-annotation]
