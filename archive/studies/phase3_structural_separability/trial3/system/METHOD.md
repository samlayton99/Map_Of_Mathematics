# THE METHOD (V8) — complete, reproducible, no jargon

## The nine definitions everything uses

1. Entry: any named thing in compiled Mathlib (771,129). Each has a statement
   (what it asserts / what kind of object it is) and usually a body (proof or
   construction). Both are walkable data structures.
2. Claim: an entry whose statement is a true/false assertion (Lean records
   this: type lives in Prop), excluding entries Lean marks constructor or
   recursor (rules for building/taking apart logical shapes -- the form of
   goals, not steps of arguments). claim = Prop-typed, not ctor, not recursor.
3. Depth: 0 if the body (or statement, when bodyless) mentions no other
   entries; else 1 + max depth over everything mentioned. One library pass.
4. Statement-world of T: names in T's statement; add everything their
   definitions mention; repeat to closure. "What stating T already needs."
5. Logic-only: measure every concept's commonness = fraction of all theorem
   statements mentioning it; >2% = everywhere-words (measured, not chosen:
   equality, naturals, sets, <=, membership). An entry's ingredients are the
   concepts in its statement under the 2% line. An entry is logic-only if it
   has no ingredients, or all of them are bare propositions (def. 8).
6. Machine-generated: no recorded source-file location (Lean logs locations
   for human-written declarations only; verified to separate cleanly).
7. Used-once: exactly one entry in the library mentions it in a body.
8. Bare proposition: a concept that IS a proposition rather than one ABOUT
   something -- Lean's own sort test says its statement is `Prop`, and it
   takes no arguments. Exactly five exist in Mathlib (True, False, UnivLE,
   FermatLastTheorem, RiemannHypothesis). A predicate like `Function.Injective`
   is Prop-sorted but takes arguments, so it is not bare.
9. Apparatus: a concept that is used far more than it is stated. Count, per
   concept, (a) how many human theorem statements mention it, inherited down
   the definition graph (a statement about Ring states everything Ring's
   definition contains), and (b) how many proofs in the library cite a claim
   having it as an ingredient. Apparatus = not bare, under the 2% line,
   (b) > 200, and (b) > 20x(a+1). This is what a decision procedure's private
   vocabulary looks like: 102 concepts, all of them encoding machinery
   (omega's Constraint and Coeffs, grind's Poly, NormNum's IsNat, the
   internal linear-arithmetic types). Nothing is named; the test is a ratio.

## The recipe for one theorem T

1. Walk T's body recording, per mentioned entry, its positions:
   (a) applied as a step, (b) explicit argument, (c) let-value,
   (d) implicit argument, (e) typeclass slot, (f) type annotation,
   (g) unresolvable slot. KEEP entries occurring in {a,b,c,g}; set aside
   those only in {d,e,f} (kept in the record, not moves).
2. Keep only claims (def. 2).
3. Resolve machine names: for each kept machine-generated item, run steps
   1-2 on ITS body, drop logic-only results; if exactly one claim remains,
   replace the item by it (a derived form proves itself from its original,
   so the original is in its body). Up to 3 hops, never revisit.
4. Mark machinery: an item is machinery for T when one of its ingredients is
   apparatus (def. 9) AND none of its ingredients appear in T's own
   statement. The second half is what keeps the measure honest -- a theorem
   ABOUT omega's Constraint keeps its constraint lemmas as real moves.
5. Verdict: if every item is logic-only or machinery, output "holds by
   definition/logic" (all logic-only) or "discharged by automation" and stop.
6. Rank by three keys: (i) items that are neither logic-only nor machinery
   first; (ii) NOT in T's statement-world first; (iii) deeper first.
7. Zoom (display): while the top item is used-once and unopened, replace it
   by its own kept-claims (name kept as group label), re-sort; max 8 opens.
8. Label (display only): a machine-generated item is shown as what it is
   part of -- the single substantive claim in its own proof, else the single
   definition whose construction cites it, else the subject of its own
   statement. Unresolved ones keep their raw name. The record is unchanged.

Constants: the measured 2% line, the apparatus thresholds (200 uses, 20x
ratio), 3 attribution hops, 8 zoom opens, "unresolvable slot counts as kept"
(conservative), a 4-of-8 selection of load-bearing binder roles, and a
minimum of 3 distinct citations for a proof to be scored. Sensitivity of the
apparatus thresholds is measured (data/apparatus_sensitivity.json): across a
4x swing in the size of the apparatus set, top-1 moves 0.06 points and the
tactic-blame and verdict counts do not move at all.

Evaluation caveat, stated plainly: the ranking rules read no names, but the
CERTIFICATION does. Every sample is drawn from theorems carrying no
classification flag, and those flags come from a name-based classifier
(mathrecord/Mathrecord/Study.lean), which excludes about 46% of Mathlib's
theorems from every round ever run. The grader is name-based too. Both are
evaluation scaffolding, both are discarded with the grader, and neither
touches the system's output -- but no certified number describes the
excluded half.

Certified (round 9, seed 20260831, run once, data/phase4_holdout9_results.json):
V8 = 94.80% top-1 non-machinery proxy against V6's 94.38 on the same sample --
a gain of 0.42 points, eight theorems. (A stricter grader was introduced in
the same round and reports 94.52 vs 93.18; because an instrument change
shipped alongside the treatment, the STANDING-metric gain of +0.42 is the
honest headline, not the +1.34. The anchor's own seed-to-seed spread is 0.87,
so this gain is within the noise of the baseline it is measured against.) tactic-internal rank-1 blames
cut 18 -> 13; real moves lost to the new rule: 2 in 1,826. Earlier rounds:
V6 certified 94.84 (round 6), replicated 93.97 (round 7).

Round 8 (seed 20260830) ran this same design and was FALSIFIED by its own
declared bar: "bare proposition" was tested as "mentions no constants",
which a predicate over abstract types also satisfies, so `Function.Injective`
and `Nonempty` were misfiled as bare and real moves ("an equivalence is
injective") collapsed into definitional verdicts -- 31 such losses against a
ceiling of 5. The extractor now reads arity from the kernel telescope
(dump v7 field `ar`) and round 9 re-ran the corrected spec on a fresh seed.

Longevity of the apparatus measure: it names nothing and knows nothing about
omega, grind, or any particular tactic. It measures a relation -- used far
more than stated -- that any decision procedure must exhibit, because a
procedure works by encoding goals into its own vocabulary and proving
denotation lemmas about that vocabulary, which is therefore cited by
thousands of proofs and stated in almost no theorems. A replacement for
omega would be caught the day it lands, with no edit. Per ADR-0004 the
MEANING is fixed; the 102 concepts it currently selects are a level-2
library-relative value that legitimately changes as the library changes.

Verdict certification: "holds by definition" outputs are now positively
checkable by the kernel (`mathrecord defcheck`: are the statement's sides
definitionally equal?). On the audited sample: 58/80 kernel-certified.
