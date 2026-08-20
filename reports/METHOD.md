# THE METHOD (V6) — complete, reproducible, no jargon

## The seven definitions everything uses

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
   equality, naturals, sets, <=, membership). An entry is logic-only if its
   statement mentions no concept under the 2% line.
6. Machine-generated: no recorded source-file location (Lean logs locations
   for human-written declarations only; verified to separate cleanly).
7. Used-once: exactly one entry in the library mentions it in a body.

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
4. Verdict: if the list is empty or entirely logic-only, output
   "holds by definition/logic" and stop.
5. Rank by three keys: (i) non-logic-only first; (ii) NOT in T's
   statement-world first; (iii) deeper first.
6. Zoom (display): while the top item is used-once and unopened, replace it
   by its own kept-claims (name kept as group label), re-sort; max 8 opens.

Constants: the measured 2% line, 3 attribution hops, 8 zoom opens,
"unresolvable slot counts as kept" (conservative). Nothing else.

Certified: 94.84% top-1 non-machinery proxy, fresh pre-registered sample,
run once (data/phase4_holdout6_results.json); replication on a further
fresh sample: 93.97% (round 7, data/phase4_holdout7_results.json — which
also falsified an author-written-priority sort key: it provably cannot
fire on automation-heavy proofs, where nothing is author-written).

Verdict certification: "holds by definition" outputs are now positively
checkable by the kernel (`mathrecord defcheck`: are the statement's sides
definitionally equal?). On the audited sample: 58/80 kernel-certified.
