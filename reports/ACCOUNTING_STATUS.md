# ACCOUNTING STATUS — every flagged case, marked (2026-08-20)

Latest certified run: **round 9, seed 20260831, V8, run once**
(data/phase4_holdout9_results.json). 2,400 theorems -> 280 verdicts
("holds by definition"), 239 EMPTY (the filters left nothing at all -- a
FAILURE MODE, not a designed output; it is excluded from the precision
denominator, which flatters the headline and is disclosed here for the first
time), 55 too small, 1,826 scored. Rank-1 pass 94.80% on the standing proxy, 94.52% under a
stricter grader (two measured blind spots closed for evaluation only:
core-internal arithmetic namespaces, and the True-twin normalization
family). Same-sample V6 baseline: 94.38 / 93.18. Markers:

| at #1 | n | marker | cause | fix status |
|---|---|---|---|---|
| machine-generated, several claims inside | 43 | OK-mislabel (mostly; ledger-read) | multi-parent derivations; attribution cannot pick one | **display label IMPLEMENTED** (src/parent_labels.py): 77.1% of 239,625 machine-generated claims now resolve to what they are part of (attribution 108k / definition-user 43k / statement-subject 34k); the rest keep their raw name |
| grader-stamped glue | 42 | 2/3 OK-mislabel (interface facts, byContradiction), 1/3 OK-by-owner-ruling (thin lists) | grader stamps structure fields / logic ops | none needed (grader work ruled out) |
| automation internals | 13 | NOT OK, but **halved** (1.1% -> 0.71%, and 5 of the 13 are correct answers on theorems that are themselves part of a tactic's own development, leaving ~0.44% true junk) | tactic certificates are genuine claims | **apparatus measure IMPLEMENTED and CERTIFIED** (round 9); residual is logic-shaped bridge lemmas (`Lean.Grind.forall_forall_or`, `Lean.Omega.Int.lt_of_not_le`) whose statements contain no apparatus vocabulary because they restate pure logic — the measure cannot see them and arguably should not: they are real, shallow facts, so what is left is a depth/generality ranking question, not a machinery question |
| Prop-typed instances | 1 | OK-mislabel (read: real facts) | grader | none needed |
| own compiled helpers | 1 | OK (zoom opens) | kept by design | implemented |

## The apparatus measure (this round's fix, certified)

A concept is **apparatus** when it is used far more than it is stated:
proofs citing it > 200, and > 20x the number of human theorem statements
that mention it (inherited down the definition graph). 102 concepts qualify,
every one of them a decision procedure's encoding vocabulary. An item is
**machinery for T** when one of its ingredients is apparatus and none of its
ingredients appear in T's own statement; machinery ranks below real moves,
and a list that is entirely machinery yields "discharged by automation".

It names nothing. The longevity argument is mechanical: a decision procedure
works by encoding goals into private vocabulary and proving denotation
lemmas about it, so that vocabulary is cited by thousands of proofs and
stated in almost no theorems. Any replacement for omega exhibits the same
signature the day it lands.

Cost, measured: 2 real moves lost in 1,826 proofs (bar was 5).

## Falsifications this round (recorded, not hidden)

- **Round 8 (seed 20260830) FALSIFIED by its own bar.** Same design, but
  "bare proposition" was tested as "mentions no constants" — which a
  predicate over abstract types also satisfies. `Function.Injective` and
  `Nonempty` were misfiled, and real moves ("an equivalence is injective")
  collapsed into definitional verdicts: 31 losses against a ceiling of 5.
  Fixed by reading arity from the kernel telescope (dump v7, field `ar`);
  exactly five bare propositions exist in Mathlib. Round 9 re-ran corrected.
- **Capsule atomization falsified twice on dev data.** Closing a
  machine-generated block when any inner claim is machinery, and when the
  top-ranked inner claim is machinery, both hide real moves (6 cases). No
  capsule rule ships; zoom is unchanged.
- **Audience test falsified on dev data.** "Cited only by machine-generated
  proofs" measures whether a block got outlined, not whether it is
  automation (`ring` emits inline into human theorems; `byContradiction`
  blocks get outlined). Dropped.

Earlier falsified detector designs, still recorded: raw statement-exposure,
root-grain strategy signatures, Lean registries, co-mention islands,
weighted islands, author-written priority at file and declaration grain.

## The empty bucket (disclosed, not yet fixed)

239 of 2,400 sampled theorems (12.8% library-wide) produce NO output: after
the position and claims filters nothing survives, so there is no list to rank
and no verdict to issue. The scoring code drops them from the denominator
(`live = a[a > 0]`), so they cost the reported precision nothing. They were
previously reported together with verdicts, which was wrong: a verdict is a
statement about every candidate being demoted, and requires candidates. This
is the single largest unmeasured failure mode in the system.

## Verdicts (280; 80 sampled from the earlier round, audited THREE ways)

- v1 (source text): 39/39 resolvable verified correct (30 literal rfl).
- v2 (exact-module + provenance channel via `mathrecord modules`): 28
  confirmed; 2 flags read as statement-side artifacts (proofs := rfl).
- v3 (KERNEL CERTIFICATION, `mathrecord defcheck`): 58/80 POSITIVELY
  KERNEL-CERTIFIED definitionally equal. Union with v1: 64/80 certified by
  at least one hard channel; of the 16 remaining, 10 are machine-generated
  congruence/injectivity lemmas (correct by construction), 6 named
  individually with no evidence of error. ZERO false verdicts, any channel.

The new "discharged by automation" verdict is a separate output from "holds
by definition" precisely so this audit stays meaningful.

Below rank 1: 97% of visible glue sits below the real moves (OK by owner
ruling). Plumbing-boundary display cut: floated, NOT implemented, cosmetic.

Recall (CORRECTED 2026-08-20; the previous claim was an artifact):
the old harness applied the claims filter to its own answer key, so its
"zero filter losses" was arithmetically forced. Rebuilt with an unfiltered
answer key (src/recall_loss_split.py): mean recall 0.317 / median 0.25
against EVERY elaborator-resolved source identifier. Loss taxonomy over 146
losses: 51 statement vocabulary (the theorem's own nouns -- not moves), 60
background slots (same vocabulary in implicit positions), 24 erased by
compilation before any term exists, 8 constructors assembling pairs, and
THREE genuine "unfold this definition" moves the claims filter cannot
express. That last class is the architecture's real recall cost and matches
the documented Type-valued gap (ADR-0004 s3). n=39; the rate at scale is
unknown.

Implemented and certified: position filter; claims filter; attribution;
verdict semantics; logic-only demotion; statement-world priority; depth
ranking; zoom; provenance sidecar; exact-module resolver + verdict audit v2;
kernel verdict certifier; **apparatus measure; machine-generated display
labels**.

Floated, NOT implemented (all non-blocking): plumbing display cut;
cross-version run; larger/human keyness panel; merging the provenance
channel into the views (the path to ~100% end-to-end recall).

Remaining goal posts, in order: (1) residual ~0.44% logic-shaped bridge
lemmas — reclassified: a ranking question, not a machinery question;
(2) cross-version run; (3) keyness at scale; (4) provenance merge for
end-to-end recall.
