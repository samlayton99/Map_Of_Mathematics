# Explain these 6 Lean proofs in English -- part 1

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

### proof_031  (target depth 4, band 0-10)

THEOREM: `ExceptT.run_liftM`

Candidates:

   1. `Except`
      [inductive, depth 0, in-statement]
   2. `ExceptT.run`
      [def, depth 2, in-statement]
   3. `liftM`
      [def, depth 2, in-statement]
   4. `instMonadLiftTOfMonadLift`
      [def, depth 3, in-statement]
   5. `ExceptT`
      [def, depth 1, in-statement]
   6. `instMonadLiftT`
      [def, depth 2, in-statement]
   7. `rfl`
      [def, depth 2, introduced-by-proof]
   8. `ExceptT.instMonadLift`
      [def, depth 3, in-statement]
   9. `Monad`
      [inductive, depth 0, in-statement]
  10. `LawfulMonad`
      [inductive, depth 1, in-statement]

### proof_067  (target depth 5, band 0-10)

THEOREM: `Relation.TransGen.head`

Candidates:

   1. `Relation.TransGen.head'`
      [theorem, depth 4, introduced-by-proof]
   2. `Relation.TransGen.to_reflTransGen`
      [theorem, depth 4, introduced-by-proof]
   3. `Relation.TransGen`
      [inductive, depth 0, in-statement]

### proof_176  (target depth 15, band 11-25)

THEOREM: `List.Sublist.flatten`

Candidates:

   1. `List`
      [inductive, depth 0, in-statement]
   2. `List.Sublist.rec`
      [recursor, depth 3, introduced-by-proof]
   3. `_private.Mathlib.Data.List.Flatten.0.List.Sublist.flatten._proof_1_2`
      [theorem, depth 13, introduced-by-proof]
   4. `List.flatten`
      [def, depth 8, in-statement]
   5. `_private.Mathlib.Data.List.Flatten.0.List.Sublist.flatten._proof_1_1`
      [theorem, depth 13, introduced-by-proof]
   6. `List.Sublist`
      [inductive, depth 1, in-statement]
   7. `_private.Mathlib.Data.List.Flatten.0.List.Sublist.flatten._proof_1_3`
      [theorem, depth 14, introduced-by-proof]

### proof_098  (target depth 21, band 11-25)

THEOREM: `List.zip_eq_zip_take_min`

Candidates:

   1. `List.zip_eq_zip_take_min._f`
      [def, depth 20, introduced-by-proof]
   2. `Nat`
      [inductive, depth 0, in-statement]
   3. `Prod`
      [inductive, depth 0, in-statement]
   4. `Min.min`
      [def, depth 1, in-statement]
   5. `List.brecOn`
      [def, depth 5, in-statement]
   6. `List.length`
      [def, depth 9, in-statement]
   7. `List`
      [inductive, depth 0, in-statement]
   8. `Eq`
      [inductive, depth 0, in-statement]
   9. `List.take`
      [def, depth 6, in-statement]
  10. `List.zip`
      [def, depth 7, in-statement]
  11. `instMinNat`
      [def, depth 16, in-statement]

### proof_135  (target depth 27, band 26-50)

THEOREM: `CategoryTheory.Functor.whiskerRight_id`

Candidates:

   1. `CategoryTheory.Functor.category`
      [def, depth 19, in-statement]
   2. `CategoryTheory.Functor.map_id`
      [theorem, depth 2, in-statement]
   3. `CategoryTheory.Functor.whiskeringRight`
      [def, depth 26, introduced-by-proof]
   4. `CategoryTheory.Functor.obj`
      [def, depth 2, in-statement]
   5. `CategoryTheory.Category`
      [inductive, depth 0, in-statement]
   6. `CategoryTheory.Functor`
      [inductive, depth 1, in-statement]

### proof_147  (target depth 31, band 26-50)

THEOREM: `Matrix.cons_head_tail`

Candidates:

   1. `Nat`
      [inductive, depth 0, in-statement]
   2. `Nat.succ`
      [constructor, depth 1, in-statement]
   3. `Fin.cons_self_tail`
      [theorem, depth 30, introduced-by-proof]
   4. `Fin`
      [inductive, depth 1, in-statement]
