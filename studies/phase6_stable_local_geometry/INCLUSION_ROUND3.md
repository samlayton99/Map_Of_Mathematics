# Inclusion round 3: the instrument is exhausted (2026-08-21)

The lead challenged the round-2 "oracle ceiling" on two grounds: (a) is
it actually computed correctly, (b) what is it even a ceiling OF, given
that math-vs-formality is genuinely gray. Both challenges answered.

## (a) Verified

Independent reimplementation reproduces the oracles exactly
(depth-threshold 0.799, order-prefix 0.825, per-proof distribution: a
perfect prefix exists for 57.1% of proofs). Concrete interleaved
examples printed with names and grades (`src/verify_oracle.py`).

## (b) The ceiling is the LABEL instrument's, not mathematics'

F1 here = agreement with median LLM-rater grades (useful = median >= 3)
on the 522-proof sealed corpus. New measurement: one rater judged
against the median of the OTHER raters scores **F1 0.856** (n = 1,603
rater-proof comparisons) — the resolution limit of the labels
themselves, i.e. the gray area, quantified.

| | F1 |
|---|---|
| rater vs rest (label resolution) | 0.856 |
| pool oracle | 0.879 |
| cut oracle | 0.825 |
| gap or move-lane | 0.719 |
| gap_all | 0.653 |

The cut-oracle sits AT the label noise floor. Verdict: **the graded
corpus is exhausted as an optimization target for inclusion and
ordering.** Remaining differences at this scale are disagreement about
what counts as mathematics, not recoverable structure.

## Supporting closures from this round

- **Ordering is at its information limit**: within-block inversion
  mining (159 inverted vs 803 correct graded pairs) shows every
  available signal (multiplicity, arity, statement depth, pr, ps)
  breaks far more correctly-ordered pairs than it fixes (best net +14).
- **Pool decomposition**: of the 0.121 pool loss, 130/147 missing
  useful items are the theorem's own statement concepts. Promoting them
  naively fails (stmt-def junk ratio 26:1, F1 craters to 0.654).
- **New substrate: statement trees** (`mathrecord hierdumpt` walks the
  TYPE's occurrence forest). Useful statement concepts sit at statement
  nesting <= 1 (median 1) vs junk median 51; the combined rule
  (nesting <= 1 AND relative depth >= 1/2) reaches precision 0.53
  (46 useful vs 41 junk) — the best separator found, still marginal
  under noisy labels. Held for the definition-target blind regrade.

## Where the frontier actually is now

Better inclusion requires better INSTRUMENTS, not better rules:
1. the grade-free instruments already built (metamorphic invariance;
   held-out co-use prediction at 23x) become the primary yardsticks;
2. a blind regrade (no tags, definition targets included) would create
   a fresh label instrument and unlock the statement-concept harvest
   (pool oracle with stmt-defs: 0.970);
3. helper expansion in the extractor remains the one purely structural
   unlock (26 universe exclusions + the metamorphic wrapper failure).
