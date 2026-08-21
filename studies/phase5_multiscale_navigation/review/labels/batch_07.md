# Grading batch `batch_07` -- 20 proofs

You are one of several independent raters. You will never see any
ranking our system produces and must not try to guess one. Your
grades are the ground truth those rankings are scored against.

Candidates are listed in RANDOM order. Position means nothing.

`depth` = how much mathematics sits beneath a declaration in the
library. It is context so you can tell a deep theorem from a
primitive. It is NOT a hint and you must not grade something high
merely because it is deep, nor low because it is shallow.

`in-statement` = already implied by what the theorem says.
`introduced-by-proof` = the proof brought it in. Either can be key.

## The grade

Give **every** candidate a grade 0-4. Do not pick a top few -- grade all of
them. The grade is about THIS proof, not about the declaration in general.

| grade | name | meaning |
|---|---|---|
| **4** | `KEY` | A core move. If asked "how does this proof go?", you would name it. Removing it destroys the proof's central idea. |
| **3** | `SUPPORT` | Real mathematical content, genuinely used, but secondary -- a lemma the key move needs, a rewrite that does actual work. |
| **2** | `LEGIT_GLUE` | Logical or structural plumbing (`Eq.trans`, `congrArg`, `Iff.mpr`, coercions, instances) that **is genuinely the content of this proof**. Near the foundations, assembling equalities really can be the whole argument. |
| **1** | `BAD_GLUE` | Plumbing or background that is present but carries no idea here. A person explaining the proof would never mention it. Correct to demote. |
| **0** | `JUNK` | Irrelevant machinery: automation residue, instance/typeclass resolution, universe or decidability bookkeeping, notation unfolding. Noise. |

The 2-versus-1 line is the important one and it is the whole reason this
panel exists. **Do not grade something 1 just because it looks like plumbing.**
Ask whether a mathematician explaining *this specific theorem* would mention
it. If yes, it is 2 even if its name looks like machinery. If the theorem is a
deep result and the item is `Eq.mpr`, that is 1.

## Also required, per proof

`missing_key`: `true` if you believe this proof has a key move that is **not
in the list at all** -- it works by manipulating local hypotheses, exhibiting
a witness, splitting into cases, or pure rewriting, and no listed citation
captures that. This is a genuine measurement of our coverage gap, not a
failure to do the task. Otherwise `false`.

`confidence`: `high` / `medium` / `low` -- whether you understood the theorem
well enough to grade it.

## Output format

Return **only** a JSON object, no commentary. Every proof id in your batch
must appear exactly once, and every candidate number of that proof must
appear exactly once in its `grades` map.

```json
{
  "proof_007": {
    "grades": {"1": 1, "2": 4, "3": 0, "4": 3, "5": 2},
    "missing_key": false,
    "confidence": "high"
  }
}
```


---

### proof_121  (target depth 3, band 0-10)

THEOREM PROVED: `Relation.ReflTransGen.trans`

Grade all 3 candidates below.

   1. `Relation.ReflTransGen.tail`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
   2. `Relation.ReflTransGen.rec`
      [recursor, depth 2, introduced-by-proof, role applied]
   3. `Relation.ReflTransGen`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_122  (target depth 23, band 11-25)

THEOREM PROVED: `OrderIso.toRelIsoLT_ofRelIsoLT`

Grade all 13 candidates below.

   1. `eq_self`
      [theorem, depth 4, introduced-by-proof, role explicit-arg]
   2. `Preorder.toLT`
      [def, depth 1, in-statement, role instance-slot]
   3. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   4. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   5. `RelIso`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `of_eq_true`
      [theorem, depth 4, in-statement, role explicit-arg]
   8. `LT.lt`
      [def, depth 1, in-statement, role explicit-arg]
   9. `OrderIso.ofRelIsoLT`
      [def, depth 22, in-statement, role explicit-arg]
  10. `OrderIso.toRelIsoLT`
      [def, depth 19, in-statement, role strict-implicit]
  11. `RelIso.instFunLike`
      [def, depth 20, in-statement, role instance-slot]
  12. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `RelIso.ext`
      [theorem, depth 21, introduced-by-proof, role applied]

### proof_123  (target depth 27, band 26-50)

THEOREM PROVED: `HomologicalComplex₂.flip_d_f`

Grade all 19 candidates below.

   1. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `Not`
      [def, depth 1, in-statement, role type-annotation]
   3. `CategoryTheory.Limits.HasZeroMorphisms`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `HomologicalComplex₂.flip`
      [def, depth 26, in-statement, role explicit-arg]
   5. `HomologicalComplex.X`
      [def, depth 3, in-statement, role explicit-arg]
   6. `HomologicalComplex.instCategory`
      [def, depth 17, in-statement, role instance-slot]
   7. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   8. `HomologicalComplex.instHasZeroMorphisms`
      [def, depth 20, in-statement, role instance-slot]
   9. `HomologicalComplex₂`
      [def, depth 21, in-statement, role type-annotation]
  10. `HomologicalComplex₂.shape_f`
      [theorem, depth 22, in-statement, role explicit-arg]
  11. `ComplexShape.Rel`
      [def, depth 1, in-statement, role explicit-arg]
  12. `HomologicalComplex`
      [inductive, depth 2, in-statement, role implicit-arg]
  13. `HomologicalComplex.Hom.f`
      [def, depth 4, in-statement, role explicit-arg]
  14. `HomologicalComplex.d`
      [def, depth 3, in-statement, role explicit-arg]
  15. `ComplexShape`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
  17. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  18. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  19. `HomologicalComplex₂.flip._proof_2`
      [theorem, depth 23, in-statement, role explicit-arg]

### proof_124  (target depth 66, band 51-75)

THEOREM PROVED: `List.utf8DecodeChar?_utf8Encode_singleton`

Grade all 21 candidates below.

   1. `instHAppendOfAppend`
      [def, depth 3, in-statement, role instance-slot]
   2. `Option`
      [inductive, depth 0, in-statement, role implicit-arg]
   3. `ByteArray.empty`
      [def, depth 6, in-statement, role explicit-arg]
   4. `List.cons`
      [constructor, depth 1, in-statement, role explicit-arg]
   5. `ByteArray`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Char`
      [inductive, depth 0, in-statement, role explicit-arg]
   7. `OfNat.ofNat`
      [def, depth 2, in-statement, role explicit-arg]
   8. `congrArg`
      [theorem, depth 3, in-statement, role explicit-arg]
   9. `List.utf8Encode`
      [def, depth 26, in-statement, role explicit-arg]
  10. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
  11. `congrFun'`
      [theorem, depth 3, in-statement, role explicit-arg]
  12. `Eq.mp`
      [def, depth 3, in-statement, role applied]
  13. `ByteArray.instAppend`
      [def, depth 9, introduced-by-proof, role instance-slot]
  14. `HAppend.hAppend`
      [def, depth 2, in-statement, role explicit-arg]
  15. `List.utf8DecodeChar?_utf8Encode_singleton_append`
      [theorem, depth 65, introduced-by-proof, role explicit-arg]
  16. `ByteArray.append_empty`
      [theorem, depth 26, introduced-by-proof, role explicit-arg]
  17. `List.nil`
      [constructor, depth 1, in-statement, role explicit-arg]
  18. `Option.some`
      [constructor, depth 1, in-statement, role explicit-arg]
  19. `Eq`
      [inductive, depth 0, in-statement, role implicit-arg]
  20. `ByteArray.utf8DecodeChar?`
      [def, depth 59, in-statement, role implicit-arg]
  21. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]

### proof_125  (target depth 80, band 76-125)

THEOREM PROVED: `Std.ExtTreeMap.self_le_maxKey!_insert`

Grade all 6 candidates below.

   1. `Std.ExtTreeMap.inner`
      [def, depth 17, in-statement, role implicit-arg]
   2. `Std.ExtDTreeMap.self_le_maxKey!_insert`
      [theorem, depth 79, introduced-by-proof, role applied]
   3. `Std.ExtTreeMap`
      [inductive, depth 16, in-statement, role type-annotation]
   4. `Inhabited`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_126  (target depth 156, band 126+)

THEOREM PROVED: `measurable_of_tendsto_metrizable`

Grade all 21 candidates below.

   1. `Filter.Tendsto`
      [def, depth 13, in-statement, role type-annotation]
   2. `Nat.instMetricSpace`
      [def, depth 147, introduced-by-proof, role instance-slot]
   3. `EMetricSpace.toPseudoEMetricSpace`
      [def, depth 1, introduced-by-proof, role instance-slot]
   4. `MetricSpace.toEMetricSpace`
      [def, depth 145, introduced-by-proof, role instance-slot]
   5. `Measurable`
      [def, depth 5, in-statement, role type-annotation]
   6. `nhds`
      [def, depth 18, in-statement, role explicit-arg]
   7. `Nat`
      [inductive, depth 0, in-statement, role explicit-arg]
   8. `BorelSpace`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `Nat.instLinearOrder`
      [def, depth 19, in-statement, role instance-slot]
  10. `Pi.topologicalSpace`
      [def, depth 64, in-statement, role instance-slot]
  11. `Filter.atTop`
      [def, depth 15, in-statement, role explicit-arg]
  12. `MeasurableSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  13. `instInhabitedNat`
      [def, depth 2, introduced-by-proof, role instance-slot]
  14. `Nat.instLocallyFiniteOrder`
      [def, depth 56, introduced-by-proof, role instance-slot]
  15. `Nat.instPartialOrder`
      [def, depth 20, introduced-by-proof, role instance-slot]
  16. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]
  17. `Nat.instPreorder`
      [def, depth 20, in-statement, role instance-slot]
  18. `instTopologicalSpaceNat`
      [def, depth 62, introduced-by-proof, role instance-slot]
  19. `Nat.instSemiring`
      [def, depth 24, introduced-by-proof, role instance-slot]
  20. `TopologicalSpace.PseudoMetrizableSpace`
      [inductive, depth 1, in-statement, role type-annotation]
  21. `measurable_of_tendsto_metrizable'`
      [theorem, depth 155, introduced-by-proof, role applied]

### proof_127  (target depth 2, band 0-10)

THEOREM PROVED: `FiberBundle.mem_baseSet_trivializationAt'`

Grade all 3 candidates below.

   1. `Bundle.TotalSpace`
      [inductive, depth 0, in-statement, role explicit-arg]
   2. `FiberBundle`
      [inductive, depth 1, in-statement, role type-annotation]
   3. `TopologicalSpace`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_128  (target depth 23, band 11-25)

THEOREM PROVED: `LieHom.fst_apply`

Grade all 11 candidates below.

   1. `LieAlgebra.Prod.instLieAlgebra`
      [def, depth 21, in-statement, role instance-slot]
   2. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
   3. `LieRing`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `LieHom.fst`
      [def, depth 22, in-statement, role explicit-arg]
   5. `LieAlgebra.Prod.instLieRing`
      [def, depth 19, in-statement, role instance-slot]
   6. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Prod`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `LieAlgebra`
      [inductive, depth 1, in-statement, role type-annotation]
   9. `rfl`
      [def, depth 2, in-statement, role applied]
  10. `LieHom.instFunLike`
      [def, depth 22, in-statement, role instance-slot]
  11. `LieHom`
      [inductive, depth 2, in-statement, role implicit-arg]

### proof_129  (target depth 30, band 26-50)

THEOREM PROVED: `ofBoolAlg_bot`

Grade all 11 candidates below.

   1. `Equiv`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `rfl`
      [def, depth 2, in-statement, role applied]
   3. `ofBoolAlg`
      [def, depth 11, in-statement, role explicit-arg]
   4. `AsBoolAlg`
      [def, depth 0, in-statement, role explicit-arg]
   5. `Equiv.instEquivLike`
      [def, depth 13, in-statement, role instance-slot]
   6. `instBooleanAlgebraAsBoolAlg`
      [def, depth 29, in-statement, role instance-slot]
   7. `EquivLike.toFunLike`
      [def, depth 8, in-statement, role instance-slot]
   8. `Bot.bot`
      [def, depth 1, in-statement, role explicit-arg]
   9. `BooleanAlgebra.toBot`
      [def, depth 1, in-statement, role instance-slot]
  10. `DFunLike.coe`
      [def, depth 2, in-statement, role implicit-arg]
  11. `BooleanRing`
      [inductive, depth 0, in-statement, role type-annotation]

### proof_130  (target depth 70, band 51-75)

THEOREM PROVED: `Std.HashSet.mem_of_mem_toList`

Grade all 8 candidates below.

   1. `EquivBEq`
      [inductive, depth 1, in-statement, role type-annotation]
   2. `Std.HashMap.mem_of_mem_keys`
      [theorem, depth 69, introduced-by-proof, role applied]
   3. `LawfulHashable`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `Std.HashSet.inner`
      [def, depth 2, in-statement, role implicit-arg]
   5. `Hashable`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `BEq`
      [inductive, depth 0, in-statement, role type-annotation]
   7. `Std.HashSet`
      [inductive, depth 1, in-statement, role type-annotation]
   8. `Unit`
      [def, depth 1, in-statement, role implicit-arg]

### proof_131  (target depth 94, band 76-125)

THEOREM PROVED: `SSet.Subcomplex.N.opEquiv_apply`

Grade all 14 candidates below.

   1. `SSet.Subcomplex.N.opEquiv`
      [def, depth 93, in-statement, role explicit-arg]
   2. `RelIso.instFunLike`
      [def, depth 20, in-statement, role instance-slot]
   3. `Preorder.toLE`
      [def, depth 1, in-statement, role instance-slot]
   4. `SSet`
      [def, depth 31, in-statement, role type-annotation]
   5. `PartialOrder.toPreorder`
      [def, depth 1, in-statement, role instance-slot]
   6. `SSet.Subcomplex`
      [def, depth 32, in-statement, role type-annotation]
   7. `SSet.Subcomplex.op`
      [def, depth 38, in-statement, role explicit-arg]
   8. `DFunLike.coe`
      [def, depth 2, in-statement, role explicit-arg]
   9. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
  10. `SSet.Subcomplex.N`
      [inductive, depth 33, in-statement, role implicit-arg]
  11. `SSet.Subcomplex.N.instPartialOrder`
      [def, depth 91, in-statement, role instance-slot]
  12. `RelIso`
      [inductive, depth 0, in-statement, role implicit-arg]
  13. `SSet.op`
      [def, depth 37, in-statement, role implicit-arg]
  14. `LE.le`
      [def, depth 1, in-statement, role explicit-arg]

### proof_132  (target depth 126, band 126+)

THEOREM PROVED: `RingHom.IsIntegralElem.neg_iff`

Grade all 17 candidates below.

   1. `SubtractionMonoid.toSubNegZeroMonoid`
      [def, depth 9, in-statement, role instance-slot]
   2. `CommSemiring.toSemiring`
      [def, depth 1, in-statement, role instance-slot]
   3. `SubNegZeroMonoid.toNegZeroClass`
      [def, depth 5, in-statement, role instance-slot]
   4. `CommRing`
      [inductive, depth 0, in-statement, role type-annotation]
   5. `RingHom`
      [inductive, depth 1, in-statement, role type-annotation]
   6. `Semiring.toNonAssocSemiring`
      [def, depth 10, in-statement, role instance-slot]
   7. `RingHom.IsIntegralElem`
      [def, depth 65, in-statement, role implicit-arg]
   8. `Neg.neg`
      [def, depth 1, in-statement, role explicit-arg]
   9. `Iff.intro`
      [constructor, depth 1, in-statement, role applied]
  10. `NegZeroClass.toNeg`
      [def, depth 1, in-statement, role instance-slot]
  11. `CommRing.toCommSemiring`
      [def, depth 5, in-statement, role instance-slot]
  12. `RingHom.IsIntegralElem.neg`
      [theorem, depth 124, introduced-by-proof, role explicit-arg]
  13. `AddCommGroup.toDivisionAddCommMonoid`
      [def, depth 12, in-statement, role instance-slot]
  14. `RingHom.IsIntegralElem.of_neg`
      [theorem, depth 125, introduced-by-proof, role explicit-arg]
  15. `SubtractionCommMonoid.toSubtractionMonoid`
      [def, depth 1, in-statement, role instance-slot]
  16. `Ring.toAddCommGroup`
      [def, depth 10, in-statement, role instance-slot]
  17. `CommRing.toRing`
      [def, depth 1, in-statement, role instance-slot]

### proof_133  (target depth 3, band 0-10)

THEOREM PROVED: `ValuativeRel.RankLeOneStruct.strictMono`

Grade all 3 candidates below.

   1. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   2. `ValuativeRel.RankLeOneStruct`
      [inductive, depth 2, in-statement, role type-annotation]
   3. `ValuativeRel`
      [inductive, depth 1, in-statement, role type-annotation]

### proof_134  (target depth 22, band 11-25)

THEOREM PROVED: `CategoryTheory.Comma.isoMk_inv_left`

Grade all 22 candidates below.

   1. `Quiver.Hom`
      [def, depth 1, in-statement, role implicit-arg]
   2. `CategoryTheory.Comma.hom`
      [def, depth 3, in-statement, role explicit-arg]
   3. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role type-annotation]
   4. `CategoryTheory.Functor.map`
      [def, depth 2, in-statement, role explicit-arg]
   5. `autoParam`
      [def, depth 1, in-statement, role type-annotation]
   6. `Eq.refl`
      [constructor, depth 1, in-statement, role applied]
   7. `CategoryTheory.Comma.right`
      [def, depth 3, in-statement, role explicit-arg]
   8. `CategoryTheory.Comma`
      [inductive, depth 2, in-statement, role type-annotation]
   9. `CategoryTheory.Iso.hom`
      [def, depth 2, in-statement, role explicit-arg]
  10. `CategoryTheory.commaCategory`
      [def, depth 12, in-statement, role instance-slot]
  11. `CategoryTheory.CommaMorphism.left`
      [def, depth 4, in-statement, role explicit-arg]
  12. `CategoryTheory.Iso.inv`
      [def, depth 2, in-statement, role explicit-arg]
  13. `CategoryTheory.Comma.isoMk._auto_1`
      [def, depth 8, in-statement, role explicit-arg]
  14. `CategoryTheory.Comma.left`
      [def, depth 3, in-statement, role explicit-arg]
  15. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
  16. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role implicit-arg]
  17. `CategoryTheory.Iso`
      [inductive, depth 1, in-statement, role type-annotation]
  18. `CategoryTheory.CategoryStruct.toQuiver`
      [def, depth 1, in-statement, role instance-slot]
  19. `CategoryTheory.Category.toCategoryStruct`
      [def, depth 1, in-statement, role instance-slot]
  20. `CategoryTheory.Comma.isoMk`
      [def, depth 21, in-statement, role explicit-arg]
  21. `Eq`
      [inductive, depth 0, in-statement, role explicit-arg]
  22. `CategoryTheory.CategoryStruct.comp`
      [def, depth 1, in-statement, role explicit-arg]

### proof_135  (target depth 27, band 26-50)

THEOREM PROVED: `CategoryTheory.Functor.whiskerRight_id`

Grade all 6 candidates below.

   1. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement, role instance-slot]
   2. `CategoryTheory.Functor.map_id`
      [theorem, depth 2, in-statement, role applied]
   3. `CategoryTheory.Functor.whiskeringRight`
      [def, depth 26, introduced-by-proof, role explicit-arg]
   4. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement, role explicit-arg]
   5. `CategoryTheory.Category`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement, role implicit-arg]

### proof_136  (target depth 75, band 51-75)

THEOREM PROVED: `Std.TreeSet.Raw.toList_rci`

Grade all 13 candidates below.

   1. `Unit`
      [def, depth 1, in-statement, role implicit-arg]
   2. `Std.DTreeMap.Raw.inner`
      [def, depth 17, in-statement, role explicit-arg]
   3. `Std.DTreeMap.Internal.Unit.toList_rci`
      [theorem, depth 36, introduced-by-proof, role applied]
   4. `Std.TreeSet.Raw.WF`
      [inductive, depth 17, in-statement, role type-annotation]
   5. `Std.DTreeMap.Internal.Impl.WF.ordered`
      [theorem, depth 74, introduced-by-proof, role explicit-arg]
   6. `Std.TreeSet.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   7. `Std.TreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   8. `Std.DTreeMap.Raw.WF.out`
      [theorem, depth 18, introduced-by-proof, role explicit-arg]
   9. `Std.TreeSet.Raw.inner`
      [def, depth 17, in-statement, role explicit-arg]
  10. `Std.TreeSet.Raw`
      [inductive, depth 16, in-statement, role type-annotation]
  11. `Ordering`
      [inductive, depth 0, in-statement, role type-annotation]
  12. `Std.TransCmp`
      [inductive, depth 1, in-statement, role type-annotation]
  13. `Std.TreeMap.Raw.inner`
      [def, depth 17, in-statement, role explicit-arg]

### proof_137  (target depth 93, band 76-125)

THEOREM PROVED: `Polynomial.natDegree_X`

Grade all 8 candidates below.

   1. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   2. `Polynomial.degree_X`
      [theorem, depth 92, introduced-by-proof, role explicit-arg]
   3. `instOfNatNat`
      [def, depth 3, in-statement, role instance-slot]
   4. `Polynomial.natDegree_eq_of_degree_eq_some`
      [theorem, depth 27, introduced-by-proof, role applied]
   5. `Semiring`
      [inductive, depth 0, in-statement, role type-annotation]
   6. `Polynomial.X`
      [def, depth 90, in-statement, role implicit-arg]
   7. `Nontrivial`
      [inductive, depth 0, in-statement, role type-annotation]
   8. `OfNat.ofNat`
      [def, depth 2, in-statement, role implicit-arg]

### proof_138  (target depth 311, band 126+)

THEOREM PROVED: `CStarAlgebra.inr_mem_Icc_iff_nnnorm_le`

Grade all 8 candidates below.

   1. `NonUnitalRing.toNonUnitalSemiring`
      [def, depth 5, in-statement, role instance-slot]
   2. `NonUnitalCStarAlgebra`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `PartialOrder`
      [inductive, depth 0, in-statement, role type-annotation]
   4. `StarOrderedRing`
      [inductive, depth 2, in-statement, role type-annotation]
   5. `NonUnitalNormedRing.toNonUnitalRing`
      [def, depth 1, in-statement, role instance-slot]
   6. `NonUnitalCStarAlgebra.toStarRing`
      [def, depth 1, in-statement, role instance-slot]
   7. `NonUnitalCStarAlgebra.toNonUnitalNormedRing`
      [def, depth 1, in-statement, role instance-slot]
   8. `CStarAlgebra.inr_mem_Icc_iff_norm_le`
      [theorem, depth 310, introduced-by-proof, role applied]

### proof_139  (target depth 6, band 0-10)

THEOREM PROVED: `Sum.bnot_isLeft`

Grade all 12 candidates below.

   1. `Eq.symm`
      [theorem, depth 3, introduced-by-proof, role explicit-arg]
   2. `Sum.inl`
      [constructor, depth 1, in-statement, role explicit-arg]
   3. `Sum`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `Sum.casesOn`
      [def, depth 3, in-statement, role applied]
   5. `Bool`
      [inductive, depth 0, in-statement, role implicit-arg]
   6. `Bool.not`
      [def, depth 5, in-statement, role explicit-arg]
   7. `Eq.ndrec`
      [def, depth 3, introduced-by-proof, role explicit-arg]
   8. `Sum.isRight`
      [def, depth 5, in-statement, role explicit-arg]
   9. `Eq.refl`
      [constructor, depth 1, introduced-by-proof, role explicit-arg]
  10. `Eq`
      [inductive, depth 0, in-statement, role type-annotation]
  11. `Sum.inr`
      [constructor, depth 1, in-statement, role explicit-arg]
  12. `Sum.isLeft`
      [def, depth 5, in-statement, role explicit-arg]

### proof_140  (target depth 17, band 11-25)

THEOREM PROVED: `Nat.find_spec`

Grade all 11 candidates below.

   1. `instLTNat`
      [def, depth 3, in-statement, role instance-slot]
   2. `Exists`
      [inductive, depth 0, in-statement, role type-annotation]
   3. `Nat`
      [inductive, depth 0, in-statement, role implicit-arg]
   4. `DecidablePred`
      [def, depth 1, in-statement, role type-annotation]
   5. `Not`
      [def, depth 1, in-statement, role type-annotation]
   6. `And`
      [inductive, depth 0, in-statement, role implicit-arg]
   7. `Subtype.val`
      [def, depth 1, in-statement, role explicit-arg]
   8. `LT.lt`
      [def, depth 1, in-statement, role type-annotation]
   9. `And.left`
      [theorem, depth 1, introduced-by-proof, role applied]
  10. `Subtype.property`
      [theorem, depth 1, introduced-by-proof, role explicit-arg]
  11. `Nat.findX`
      [def, depth 16, in-statement, role explicit-arg]
