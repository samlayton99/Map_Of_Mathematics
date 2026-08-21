# Grading batch `testc_23` — 24 proofs

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

### proof_0529  (target depth 159, band 126+)

THEOREM PROVED: `AlgebraicGeometry.instHasFiniteLimitsScheme`

Grade all 3 candidates.

   1. `CategoryTheory.Limits.hasFiniteLimits_of_hasTerminal_and_pullbacks`
      [theorem, depth 69, introduced-by-proof, role applied]
   2. `AlgebraicGeometry.Scheme.instCategory`
      [def, depth 89, in-statement, role instance-slot]
   3. `AlgebraicGeometry.Scheme`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_0530  (target depth 201, band 126+)

THEOREM PROVED: `ProbabilityTheory.Kernel.IsZeroOrMarkovKernel.fst`

Grade all 14 candidates.

   1. `Prod`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Eq.mpr`
      [def, depth 4, in-statement, role applied]
   3. `ProbabilityTheory.Kernel.map`
      [def, depth 196, introduced-by-proof, role explicit-arg]
   4. `inferInstance`
      [def, depth 0, in-statement, role explicit-arg]
   5. `ProbabilityTheory.Kernel.fst_eq`
      [theorem, depth 198, introduced-by-proof, role explicit-arg]
   6. `id`
      [def, depth 0, in-statement, role explicit-arg]
   7. `ProbabilityTheory.IsZeroOrMarkovKernel`
      [inductive, depth 2, in-statement, role explicit-arg]
   8. `ProbabilityTheory.Kernel`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  10. `Prod.instMeasurableSpace`
      [def, depth 67, in-statement, role implicit-arg]
  11. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `Prod.fst`
      [def, depth 1, in-statement, role explicit-arg]
  14. `ProbabilityTheory.Kernel.fst`
      [def, depth 196, in-statement, role explicit-arg]

### proof_0531  (target depth 88, band 76-125)

THEOREM PROVED: `Matrix.SpecialLinearGroup.instDiscreteTopology`

Grade all 6 candidates.

   1. `_private.Mathlib.Topology.Algebra.Group.Matrix.0.Matrix.SpecialLinearGroup.instDiscreteTopology._proof_1`
      [theorem, depth 87, introduced-by-proof, role applied]
   2. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `Fintype`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `DecidableEq`
      [def, depth 1, in-statement, role type-annotation]
   6. `DiscreteTopology`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_0532  (target depth 83, band 76-125)

THEOREM PROVED: `Std.ExtTreeMap.inter_eq`

Grade all 7 candidates.

   1. `of_eq_true`
      [theorem, depth 4, in-statement, role applied]
   2. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `eq_self`
      [theorem, depth 4, in-statement, role explicit-arg]
   4. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   5. `Std.ExtTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   6. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.ExtTreeMap.inter`
      [def, depth 82, in-statement, role explicit-arg]

### proof_0533  (target depth 9, band 0-10)

THEOREM PROVED: `Function.Injective.isWellOrder`

Grade all 6 candidates.

   1. `IsWellOrder.mk`
      [constructor, depth 1, introduced-by-proof, role applied]
   2. `IsWellOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Std.Trichotomous`
      [inductive, depth 0, introduced-by-proof, role type-annotation]
   4. `Function.Injective.trichotomous_onFun`
      [theorem, depth 3, introduced-by-proof, role let-value]
   5. `Function.Injective`
      [def, depth 1, in-statement, role type-annotation]
   6. `Function.onFun`
      [def, depth 0, in-statement, role explicit-arg]

### proof_0534  (target depth 6, band 0-10)

THEOREM PROVED: `Int32.ofBitVec_uInt32ToBitVec`

Grade all 5 candidates.

   1. `UInt32`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Int32`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `Int32.ofBitVec`
      [def, depth 5, in-statement, role implicit-arg]
   4. `rfl`
      [def, depth 2, introduced-by-proof, role applied]
   5. `UInt32.toBitVec`
      [def, depth 1, in-statement, role explicit-arg]

### proof_0535  (target depth 6, band 0-10)

THEOREM PROVED: `exists_nonneg_add_of_le`

Grade all 24 candidates.

   1. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   2. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
   3. `ExistsAddOfLE.exists_add_of_le`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   4. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
   5. `Exists`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]
   8. `rfl`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   9. `nonneg_of_le_add_right`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  10. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
  11. `AddZero.toZero`
      [def, depth 1, in-statement, role instance-slot]
  12. `Exists.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  13. `And.intro`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  14. `And`
      [inductive, depth 0, in-statement, role explicit-arg]
  15. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]
  16. `AddZeroClass`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `ExistsAddOfLE`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `Exists.casesOn`
      [def, depth 3, introduced-by-proof, role applied]
  19. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
  20. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
  21. `AddLeftReflectLE`
      [inductive, depth 1, in-statement, role type-annotation]
  22. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  23. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  24. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0536  (target depth 25, band 11-25)

THEOREM PROVED: `Int16.toBitVec_ofNat'`

Grade all 7 candidates.

   1. `rfl`
      [def, depth 2, in-statement, role applied]
   2. `BitVec`
      [inductive, depth 1, in-statement, role implicit-arg]
   3. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Int16.ofNat`
      [def, depth 24, in-statement, role explicit-arg]
   5. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `Int16.toBitVec`
      [def, depth 2, in-statement, role implicit-arg]
   7. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]

### proof_0537  (target depth 8, band 0-10)

THEOREM PROVED: `Turing.ToPartrec.Code.succ_eval`

Grade all 16 candidates.

   1. `HAdd.hAdd`
      [def, depth 2, introduced-by-proof, role explicit-arg]
   2. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   3. `instHAdd`
      [def, depth 3, introduced-by-proof, role instance-slot]
   4. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
   5. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   6. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   7. `PFun`
      [def, depth 1, in-statement, role implicit-arg]
   8. `instInhabitedNat`
      [def, depth 2, in-statement, role instance-slot]
   9. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
  10. `List.cons`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `Part.some`
      [def, depth 2, in-statement, role explicit-arg]
  12. `instAddNat`
      [def, depth 7, introduced-by-proof, role instance-slot]
  13. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  14. `List.headI`
      [def, depth 5, in-statement, role explicit-arg]
  15. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
  16. `List`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0538  (target depth 15, band 11-25)

THEOREM PROVED: `Graph.isLoopAt_iff_inc_not_isNonloopAt`

Grade all 23 candidates.

   1. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   2. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   3. `implies_congr_ctx`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
   4. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
   5. `Graph.Inc`
      [def, depth 2, in-statement, role explicit-arg]
   6. `imp_self._simp_1`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   7. `True`
      [inductive, depth 0, introduced-by-proof, role explicit-arg]
   8. `not_and._simp_1`
      [theorem, depth 7, introduced-by-proof, role explicit-arg]
   9. `Graph.IsNonloopAt`
      [def, depth 3, in-statement, role explicit-arg]
  10. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  11. `implies_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  12. `Not`
      [def, depth 1, in-statement, role explicit-arg]
  13. `Graph`
      [inductive, depth 0, in-statement, role type-annotation]
  14. `Classical.not_not._simp_1`
      [theorem, depth 13, introduced-by-proof, role explicit-arg]
  15. `_private.Mathlib.Combinatorics.Graph.Basic.0.Graph.isLoopAt_iff_inc_not_isNonloopAt._simp_1_3`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  16. `Graph.IsLoopAt`
      [def, depth 2, in-statement, role implicit-arg]
  17. `and_self`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  18. `eq_true`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  19. `Iff`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `_private.Mathlib.Combinatorics.Graph.Basic.0.Graph.isLoopAt_iff_inc_not_isNonloopAt._simp_1_1`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
  21. `_private.Mathlib.Combinatorics.Graph.Basic.0.Graph.isLoopAt_iff_inc_not_isNonloopAt._simp_1_2`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  22. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role applied]
  23. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]

### proof_0539  (target depth 14, band 11-25)

THEOREM PROVED: `FreeMonoid.toList_cons`

Grade all 9 candidates.

   1. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `FreeMonoid.toList`
      [def, depth 11, in-statement, role explicit-arg]
   3. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   4. `List.cons`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   6. `rfl`
      [def, depth 2, in-statement, role applied]
   7. `FreeMonoid`
      [def, depth 1, in-statement, role type-annotation]
   8. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]

### proof_0540  (target depth 7, band 0-10)

THEOREM PROVED: `Option.any_attach`

Grade all 21 candidates.

   1. `congrFun'`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   2. `Option.some`
      [constructor, depth 1, in-statement, role explicit-arg]
   3. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   4. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   5. `Option.attach`
      [def, depth 6, in-statement, role explicit-arg]
   6. `Option.any`
      [def, depth 5, in-statement, role explicit-arg]
   7. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   8. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   9. `Subtype`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Subtype.mk`
      [constructor, depth 1, in-statement, role explicit-arg]
  11. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
  12. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  14. `Option.none`
      [constructor, depth 1, in-statement, role explicit-arg]
  15. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
  16. `Eq.trans`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  17. `Option.casesOn`
      [def, depth 3, in-statement, role applied]
  18. `True`
      [inductive, depth 0, introduced-by-proof, role implicit-arg]
  19. `Bool.false`
      [constructor, depth 1, in-statement, role explicit-arg]
  20. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
  21. `Eq.refl`
      [constructor, depth 1, in-statement, role unresolved]

### proof_0541  (target depth 6, band 0-10)

THEOREM PROVED: `CategoryTheory.MonoidalCategory.id_tensor_associator_naturality_assoc`

Grade all 21 candidates.

   1. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `CategoryTheory.MonoidalCategory`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `id`
      [def, depth 0, introduced-by-proof, role applied]
   4. `forall_congr`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
   5. `Eq.mp`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   6. `CategoryTheory.MonoidalCategoryStruct.tensorObj`
      [def, depth 2, in-statement, role implicit-arg]
   7. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   8. `CategoryTheory.MonoidalCategory.toMonoidalCategoryStruct`
      [def, depth 2, in-statement, role instance-slot]
   9. `CategoryTheory.Category.assoc`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  10. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  11. `Quiver.Hom`
      [def, depth 1, in-statement, role type-annotation]
  12. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `congrArg`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  14. `CategoryTheory.MonoidalCategoryStruct.associator`
      [def, depth 2, in-statement, role explicit-arg]
  15. `CategoryTheory.MonoidalCategoryStruct.tensorHom`
      [def, depth 2, in-statement, role explicit-arg]
  16. `congr`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
  17. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  18. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  19. `CategoryTheory.CategoryStruct.id`
      [def, depth 1, in-statement, role explicit-arg]
  20. `CategoryTheory.MonoidalCategory.id_tensor_associator_naturality`
      [theorem, depth 5, introduced-by-proof, role explicit-arg]
  21. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]

### proof_0542  (target depth 15, band 11-25)

THEOREM PROVED: `IsLowerSet.ofDual`

Grade all 14 candidates.

   1. `Set.preimage`
      [def, depth 4, in-statement, role explicit-arg]
   2. `IsUpperSet`
      [def, depth 4, in-statement, role implicit-arg]
   3. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   4. `OrderDual`
      [def, depth 0, in-statement, role explicit-arg]
   5. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   6. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   7. `Set`
      [def, depth 0, in-statement, role type-annotation]
   8. `IsLowerSet`
      [def, depth 4, in-statement, role implicit-arg]
   9. `Iff.mpr`
      [theorem, depth 1, introduced-by-proof, role applied]
  10. `OrderDual.instLE`
      [def, depth 2, in-statement, role instance-slot]
  11. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
  12. `isUpperSet_preimage_toDual_iff`
      [theorem, depth 14, introduced-by-proof, role explicit-arg]
  13. `OrderDual.toDual`
      [def, depth 11, in-statement, role explicit-arg]
  14. `LE`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0543  (target depth 20, band 11-25)

THEOREM PROVED: `_private.Batteries.Data.UnionFind.Basic.0.Batteries.UnionFind.rank'_lt_rankMax.go`

Grade all 15 candidates.

   1. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   2. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `instLENat`
      [def, depth 2, in-statement, role instance-slot]
   4. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   5. `Membership.mem`
      [def, depth 2, in-statement, role type-annotation]
   6. `List`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   8. `List.brecOn`
      [def, depth 5, in-statement, role applied]
   9. `List.instMembership`
      [def, depth 3, in-statement, role instance-slot]
  10. `Batteries.UFNode`
      [inductive, depth 0, in-statement, role explicit-arg]
  11. `Nat.instMax`
      [def, depth 16, in-statement, role instance-slot]
  12. `Max.max`
      [def, depth 1, in-statement, role explicit-arg]
  13. `Batteries.UFNode.rank`
      [def, depth 1, in-statement, role explicit-arg]
  14. `List.foldr`
      [def, depth 6, in-statement, role explicit-arg]
  15. `_private.Batteries.Data.UnionFind.Basic.0.Batteries.UnionFind.rank'_lt_rankMax.go._f`
      [def, depth 19, introduced-by-proof, role explicit-arg]

### proof_0544  (target depth 7, band 0-10)

THEOREM PROVED: `le_of_le_add_of_nonpos_left`

Grade all 14 candidates.

   1. `LE.le`
      [def, depth 1, in-statement, role type-annotation]
   2. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   3. `Preorder`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `AddLeftMono`
      [def, depth 4, in-statement, role type-annotation]
   5. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   6. `instHAdd`
      [def, depth 3, in-statement, role instance-slot]
   7. `AddZero.toZero`
      [def, depth 1, in-statement, role instance-slot]
   8. `AddZeroClass`
      [inductive, depth 0, in-statement, role type-annotation]
   9. `AddZero.toAdd`
      [def, depth 1, in-statement, role instance-slot]
  10. `add_le_of_nonpos_right`
      [theorem, depth 6, introduced-by-proof, role explicit-arg]
  11. `AddZeroClass.toAddZero`
      [def, depth 1, in-statement, role instance-slot]
  12. `LE.le.trans`
      [theorem, depth 3, introduced-by-proof, role applied]
  13. `HAdd.hAdd`
      [def, depth 2, in-statement, role explicit-arg]
  14. `Zero.toOfNat0`
      [def, depth 3, in-statement, role instance-slot]

### proof_0545  (target depth 5, band 0-10)

THEOREM PROVED: `Coalgebra.comm_comp_comul`

Grade all 7 candidates.

   1. `Coalgebra.IsCocomm`
      [inductive, depth 3, in-statement, role type-annotation]
   2. `AddCommMonoid`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Module`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `CommSemiring`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Coalgebra.IsCocomm.comm_comp_comul`
      [theorem, depth 4, introduced-by-proof, role applied]
   6. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   7. `Coalgebra`
      [inductive, depth 2, in-statement, role type-annotation]

### proof_0546  (target depth 6, band 0-10)

THEOREM PROVED: `Set.op_mem_op`

Grade all 7 candidates.

   1. `Set.op`
      [def, depth 5, in-statement, role explicit-arg]
   2. `Iff.rfl`
      [theorem, depth 3, introduced-by-proof, role applied]
   3. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]
   4. `Set`
      [def, depth 0, in-statement, role implicit-arg]
   5. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   6. `Opposite.op`
      [constructor, depth 1, in-statement, role explicit-arg]
   7. `Opposite`
      [inductive, depth 0, in-statement, role explicit-arg]

### proof_0547  (target depth 17, band 11-25)

THEOREM PROVED: `Subgroup.instSubgroupClass`

Grade all 16 candidates.

   1. `Submonoid.one_mem'`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   2. `MulOneClass.toMulOne`
      [def, depth 1, in-statement, role instance-slot]
   3. `Group.toDivInvMonoid`
      [def, depth 1, in-statement, role instance-slot]
   4. `SubgroupClass.mk`
      [constructor, depth 6, introduced-by-proof, role applied]
   5. `Monoid.toMulOneClass`
      [def, depth 5, in-statement, role instance-slot]
   6. `Subgroup.instSetLike`
      [def, depth 16, in-statement, role instance-slot]
   7. `DivInvMonoid.toInv`
      [def, depth 1, in-statement, role instance-slot]
   8. `Subgroup.toSubmonoid`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Submonoid.toSubsemigroup`
      [def, depth 2, in-statement, role explicit-arg]
  10. `Subgroup.inv_mem'`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  11. `Subsemigroup.mul_mem'`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
  12. `MulOne.toOne`
      [def, depth 1, in-statement, role instance-slot]
  13. `MulOne.toMul`
      [def, depth 1, in-statement, role instance-slot]
  14. `Group`
      [inductive, depth 0, in-statement, role type-annotation]
  15. `DivInvMonoid.toMonoid`
      [def, depth 1, in-statement, role instance-slot]
  16. `Subgroup`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_0548  (target depth 11, band 11-25)

THEOREM PROVED: `Function.Fiber.mk_image`

Grade all 14 candidates.

   1. `Set.range`
      [def, depth 2, in-statement, role explicit-arg]
   2. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
   3. `Function.Fiber.mkSelf`
      [def, depth 9, introduced-by-proof, role explicit-arg]
   4. `Membership.mem`
      [def, depth 2, in-statement, role implicit-arg]
   5. `Function.Fiber.image`
      [def, depth 9, in-statement, role implicit-arg]
   6. `Function.Fiber.mk`
      [def, depth 8, in-statement, role explicit-arg]
   7. `Singleton.singleton`
      [def, depth 2, in-statement, role explicit-arg]
   8. `Function.Fiber.map_eq_image`
      [theorem, depth 10, introduced-by-proof, role explicit-arg]
   9. `Set.preimage`
      [def, depth 4, in-statement, role explicit-arg]
  10. `Eq.symm`
      [theorem, depth 3, in-statement, role applied]
  11. `Set.Elem`
      [def, depth 4, in-statement, role implicit-arg]
  12. `Set`
      [def, depth 0, in-statement, role implicit-arg]
  13. `Set.instSingletonSet`
      [def, depth 3, in-statement, role instance-slot]
  14. `Set.instMembership`
      [def, depth 3, in-statement, role instance-slot]

### proof_0549  (target depth 13, band 11-25)

THEOREM PROVED: `CategoryTheory.Bicategory.Comonad.comul_assoc_assoc`

Grade all 24 candidates.

   1. `CategoryTheory.Bicategory.Comonad.comul_assoc`
      [theorem, depth 12, introduced-by-proof, role explicit-arg]
   2. `CategoryTheory.Bicategory.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
   3. `CategoryTheory.Bicategory.Comonad.comul`
      [def, depth 12, in-statement, role explicit-arg]
   4. `CategoryTheory.Bicategory.whiskerLeft`
      [def, depth 1, in-statement, role explicit-arg]
   5. `CategoryTheory.Bicategory.whiskerRight`
      [def, depth 1, in-statement, role explicit-arg]
   6. `CategoryTheory.Bicategory.Comonad`
      [def, depth 11, in-statement, role type-annotation]
   7. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   8. `Eq.trans`
      [theorem, depth 3, in-statement, role explicit-arg]
   9. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  10. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  11. `Mathlib.Tactic.Reassoc.eq_whisker'`
      [theorem, depth 5, in-statement, role explicit-arg]
  12. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  13. `CategoryTheory.Bicategory.homCategory`
      [def, depth 1, in-statement, role instance-slot]
  14. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  15. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]
  16. `forall_congr`
      [theorem, depth 5, in-statement, role explicit-arg]
  17. `id`
      [def, depth 0, in-statement, role applied]
  18. `congr`
      [theorem, depth 3, in-statement, role explicit-arg]
  19. `Eq.mp`
      [def, depth 3, in-statement, role explicit-arg]
  20. `CategoryTheory.Category.assoc`
      [theorem, depth 1, in-statement, role explicit-arg]
  21. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
  22. `CategoryTheory.Bicategory.associator`
      [def, depth 1, in-statement, role explicit-arg]
  23. `CategoryTheory.instCategoryEndMonoidal`
      [def, depth 2, in-statement, role instance-slot]
  24. `CategoryTheory.Bicategory`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0550  (target depth 7, band 0-10)

THEOREM PROVED: `Option.foldl_toList`

Grade all 13 candidates.

   1. `Option.some`
      [constructor, depth 1, in-statement, role explicit-arg]
   2. `Option`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `of_eq_true`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   4. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   5. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   6. `Option.casesOn`
      [def, depth 3, in-statement, role applied]
   7. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
   8. `Option.none`
      [constructor, depth 1, in-statement, role explicit-arg]
   9. `Option.elim`
      [def, depth 5, in-statement, role explicit-arg]
  10. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role unresolved]
  11. `List.foldl`
      [def, depth 6, in-statement, role explicit-arg]
  12. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
  13. `Option.toList`
      [def, depth 5, in-statement, role explicit-arg]

### proof_0551  (target depth 5, band 0-10)

THEOREM PROVED: `Quiver.Hom.cast_rfl_rfl`

Grade all 4 candidates.

   1. `Quiver.Hom.cast`
      [def, depth 4, in-statement, role implicit-arg]
   2. `rfl`
      [def, depth 2, in-statement, role explicit-arg]
   3. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   4. `Quiver`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_0552  (target depth 23, band 11-25)

THEOREM PROVED: `Order.IsPredLimit.lt_sub_one`

Grade all 10 candidates.

   1. `One`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   3. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   4. `Order.IsPredPrelimit.lt_sub_one`
      [theorem, depth 22, introduced-by-proof, role applied]
   5. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Order.IsPredLimit.isPredPrelimit`
      [theorem, depth 2, introduced-by-proof, role explicit-arg]
   7. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
   8. `PredSubOrder`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Sub`
      [inductive, depth 0, in-statement, role type-annotation]
  10. `Order.IsPredLimit`
      [inductive, depth 1, in-statement, role type-annotation]
