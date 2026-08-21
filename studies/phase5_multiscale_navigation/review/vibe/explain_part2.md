# Explain these 6 Lean proofs in English -- part 2

The reader cannot read Lean. For EVERY proof below, and EVERY
candidate citation of that proof, write a short plain-English
explanation of what that declaration actually is and what it does.

Also write, for each proof, a 1-3 sentence explanation of what the
THEOREM says in English, and a 1-2 sentence sketch of how the proof
plausibly goes.

Be concrete. `Eq.mpr` is 'rewrites the goal along an equality', not
'a fundamental equality operation'. Name the mathematical object
when there is one. If a declaration is pure machinery, say so and
say what machinery.

Keep each candidate explanation to 1-2 sentences. This is a quick
orientation aid, not a treatise.

## Output

Write ONLY a JSON object to the path given at the end, shaped:

```json
{"proof_012": {
   "statement_en": "...", "proof_sketch_en": "...",
   "candidates": {"1": "...", "2": "..."}
}}
```

Every proof id and every candidate number must appear.

---

### proof_034  (target depth 51, band 51-75)

THEOREM: `Fin.xor_comm`

Candidates:

   1. `_private.Mathlib.Data.Fin.Init.0.Fin.xor_comm._proof_1_1`
      [theorem, depth 50, introduced-by-proof]
   2. `Fin`
      [inductive, depth 1, in-statement]
   3. `Nat`
      [inductive, depth 0, in-statement]

### proof_076  (target depth 68, band 51-75)

THEOREM: `Graph.isClosedSubgraph_bot_iff`

Candidates:

   1. `Eq.rec`
      [recursor, depth 2, in-statement]
   2. `PartialOrder.toPreorder`
      [def, depth 1, in-statement]
   3. `Bot.bot`
      [def, depth 1, in-statement]
   4. `Graph.IsClosedSubgraph`
      [inductive, depth 1, in-statement]
   5. `Graph.instPartialOrder`
      [def, depth 58, in-statement]
   6. `Iff.intro`
      [constructor, depth 1, in-statement]
   7. `le_bot_iff`
      [theorem, depth 8, in-statement]
   8. `Graph`
      [inductive, depth 0, in-statement]
   9. `Eq`
      [inductive, depth 0, in-statement]
  10. `LE.le`
      [def, depth 1, in-statement]
  11. `Graph.IsInducedSubgraph.le`
      [theorem, depth 2, introduced-by-proof]
  12. `Graph.IsClosedSubgraph.rfl`
      [theorem, depth 67, introduced-by-proof]
  13. `Preorder.toLE`
      [def, depth 1, in-statement]
  14. `Graph.IsClosedSubgraph.isInducedSubgraph`
      [theorem, depth 2, introduced-by-proof]
  15. `Iff.mp`
      [theorem, depth 1, in-statement]
  16. `Graph.instOrderBot`
      [def, depth 59, in-statement]
  17. `OrderBot.toBot`
      [def, depth 2, in-statement]

### proof_005  (target depth 77, band 76-125)

THEOREM: `Rat.ofNat_add_den`

Candidates:

   1. `Rat.natCast_add_den`
      [theorem, depth 76, introduced-by-proof]
   2. `Rat`
      [inductive, depth 0, in-statement]
   3. `Nat`
      [inductive, depth 0, in-statement]

### proof_041  (target depth 98, band 76-125)

THEOREM: `String.Pos.copy_ofCopy`

Candidates:

   1. `String.Pos`
      [inductive, depth 1, in-statement]
   2. `String.Pos.offset_ofCopy`
      [theorem, depth 97, introduced-by-proof]
   3. `eq_self`
      [theorem, depth 4, in-statement]
   4. `String.Slice.copy`
      [def, depth 89, in-statement]
   5. `String.Pos.Raw`
      [inductive, depth 0, in-statement]
   6. `String.Pos.ofCopy`
      [def, depth 96, in-statement]
   7. `of_eq_true`
      [theorem, depth 4, in-statement]
   8. `String.Slice`
      [inductive, depth 0, in-statement]
   9. `Eq`
      [inductive, depth 0, in-statement]
  10. `True`
      [inductive, depth 0, in-statement]
  11. `String.Slice.Pos.copy`
      [def, depth 96, in-statement]
  12. `String.Slice.Pos.offset_copy`
      [theorem, depth 97, introduced-by-proof]
  13. `Eq.trans`
      [theorem, depth 3, in-statement]
  14. `congrFun'`
      [theorem, depth 3, in-statement]
  15. `congrArg`
      [theorem, depth 3, in-statement]
  16. `String.Slice.Pos.offset`
      [def, depth 2, in-statement]
  17. `String.Pos.offset`
      [def, depth 2, in-statement]
  18. `String.Pos.ext`
      [theorem, depth 6, introduced-by-proof]

### proof_048  (target depth 194, band 126+)

THEOREM: `MeasureTheory.MeasurePreserving.map_of_comp`

Candidates:

   1. `MeasureTheory.MeasurePreserving.map_eq`
      [theorem, depth 10, introduced-by-proof]
   2. `MeasureTheory.MeasurePreserving.mk`
      [constructor, depth 189, introduced-by-proof]
   3. `MeasureTheory.Measure.map`
      [def, depth 188, in-statement]
   4. `Function.comp`
      [def, depth 0, in-statement]
   5. `Eq.trans`
      [theorem, depth 3, in-statement]
   6. `MeasurableSpace`
      [inductive, depth 0, in-statement]
   7. `MeasureTheory.MeasurePreserving`
      [inductive, depth 9, in-statement]
   8. `MeasureTheory.Measure`
      [inductive, depth 1, in-statement]
   9. `Measurable`
      [def, depth 5, in-statement]
  10. `MeasureTheory.Measure.map_map`
      [theorem, depth 193, introduced-by-proof]

### proof_138  (target depth 311, band 126+)

THEOREM: `CStarAlgebra.inr_mem_Icc_iff_nnnorm_le`

Candidates:

   1. `NonUnitalRing.toNonUnitalSemiring`
      [def, depth 5, in-statement]
   2. `NonUnitalCStarAlgebra`
      [inductive, depth 0, in-statement]
   3. `PartialOrder`
      [inductive, depth 0, in-statement]
   4. `StarOrderedRing`
      [inductive, depth 2, in-statement]
   5. `NonUnitalNormedRing.toNonUnitalRing`
      [def, depth 1, in-statement]
   6. `NonUnitalCStarAlgebra.toStarRing`
      [def, depth 1, in-statement]
   7. `NonUnitalCStarAlgebra.toNonUnitalNormedRing`
      [def, depth 1, in-statement]
   8. `CStarAlgebra.inr_mem_Icc_iff_norm_le`
      [theorem, depth 310, introduced-by-proof]
