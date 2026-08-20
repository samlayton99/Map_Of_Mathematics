# Trial 3 — Package for the External Judge

Date: 2026-08-20. Prior rulings by this judge (accept-with-conditions, Phase 4
certification program) were executed; see `CASE_HISTORY_ADDENDUM.md` §0.

## What you are ruling on

Two questions, put by the program owner:

**Q1.** Is this the right structure/procedure to move forward on, to produce
the best and cleanest ranking of the statements/citations in a proof?
"Best and cleanest" means: most reflecting how a mathematician would think of
the proof, and how simple it is. Everything is relative to the complexity of
the proof — **a rudimentary proof that is only glue, reported as glue, is not
a failure.**

**Q2.** Is this the right structure/procedure to move forward on, to achieve
the project's actual stated goal — a navigable map of mathematics?

## The owner's standing constraints (these bind the answer)

1. No naming conventions, no string/namespace rules, no learned or
   probabilistic scoring anywhere in the measure.
2. Fixes must be robust to all future Lean versions, must approach 100% as
   the library deepens, and must never be patchwork.
3. At this stage, **filtering out a key move is more damaging than admitting
   junk.**
4. Precision and recall must not drift as Lean evolves.
5. Simplicity is a design principle, not a preference: it is the operational
   proxy for auditability and drift-resistance (Occam).

## The owner's stated suspicions, which the prosecution was told to press

- The current solution may be patchwork; longevity is the primary worry.
- Arbitrary hardcoded constants are suspect.
- He is not convinced of the recall.
- He is not convinced of the precision.

## Ground rule imposed on the prosecution

The grader is an automated name/namespace-based labeler used **only for
evaluation** and will be discarded when the work is done. Attacks whose entire
content is "the proxy metric is a proxy" were ruled weak. This did not exempt
the grader from scrutiny where it distorts a conclusion.

## How to read this package

Read in this order:

1. `CASE_HISTORY_ADDENDUM.md` — everything learned since the last handoff,
   including the full certification chain and every falsified design.
2. `METHOD.md` — the system on trial (V8), stated so it can be reproduced
   from scratch.
3. `briefs/1_DEFENSE_OPENING.md`
4. `briefs/2_PROSECUTION_OPENING.md`
5. `briefs/3_DEFENSE_REBUTTAL.md`
6. `briefs/4_PROSECUTION_REBUTTAL.md`
7. `EVIDENCE.md` — every load-bearing claim from either side, checked against
   the code by the defense during the trial, with file:line receipts, marked
   VERIFIED / REFUTED / CORRECTED.
8. `ACCOUNTING_STATUS.md` — the current marked ledger of every failure class.

## Procedural facts you should know

- The prosecution was an **independent agent** with full repository access,
  instructed to verify claims against code rather than trust prose. It was
  not shown a preferred conclusion.
- The defense **conceded five charges outright** and fixed three of them
  during the trial; the corrections are in this package and in the git
  history, not merely promised.
- The prosecution **withdrew one charge** on the merits after the defense
  produced contrary evidence.
- The defense **retracted one of its own rebuttal claims** after diagnosing a
  case that contradicted it. That retraction is in `EVIDENCE.md` item E7.

## The specific rulings requested

1. On Q1 and Q2 as stated.
2. Whether the apparatus measure (METHOD.md definition 9) is a legitimate
   answer to the longevity constraint, or a tuned artifact. The parties agree
   the *mechanism* argument is sound and disagree about whether the
   *implementation* — a two-threshold ratio over a max-propagated statedness
   count — inherits that soundness.
3. Whether the corrected recall picture (mean 0.317 against an unfiltered
   answer key, with 3-to-11 of 146 losses being genuine inexpressible moves)
   satisfies constraint 3 above, or violates it.
4. Whether the certification chain (nine rounds, seeds burned, specification
   changed between rounds, two rounds falsified and reported) constitutes
   genuine falsification or a garden of forking paths.
5. What the next unit of work should be. The parties agree the current
   accounting's remaining goal posts do not contain the item the map needs.
