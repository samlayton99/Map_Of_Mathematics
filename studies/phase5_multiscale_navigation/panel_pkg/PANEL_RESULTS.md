# Semantic Keyness Panel — results

2026-08-20. Design fixed in `src/panel_prep.py` before any brief was
generated. 25 proofs, 4–5 per depth band, universe U1D, three independent
Opus raters all rating the same 25.

**The raters never saw a ranking.** Each was shown a proof's citations in
random order and asked which are the key moves. One annotation therefore
scores every ranking — present and future — with no anchoring. This is the
only place in the program a `Semantic*` metric may be computed, because it is
the only place graded labels exist.

---

## Headline: the panel overturns the SourceHit ordering

| ranking | SemanticCoreHit@1 (majority) | SemanticCoreHit@4 | SourceHit@1 (for contrast) |
|---|---|---|---|
| **R_v8_faithful** | **0.857** (18/21) | 0.952 | 0.587 |
| R_introduced_depth | 0.762 (16/21) | 0.905 | **0.603** |
| R_phase5_composite | 0.714 | 0.905 | 0.561 |
| R_v8_all_kinds | 0.714 | 0.810 | 0.591 |
| **O_source (SourceOracle)** | **0.619** | 0.857 | *1.000 by construction* |
| R_depth | 0.619 | 0.857 | 0.570 |
| B0_random | 0.143 | 0.190 | 0.243 |
| B3_term_order | 0.095 | 0.238 | 0.225 |
| B2_popularity | 0.048 | 0.190 | 0.120 |
| B1_reverse_depth | 0.000 | 0.095 | 0.128 |

Two things flip relative to what I reported earlier, and both were predicted
by the external audit.

### 1. Source alignment is NOT keyness — proved, not argued

**The SourceOracle scores 0.619 on semantic keyness and is beaten by four
candidate rankings.** A ranking that perfectly orders "what the author wrote"
is mediocre at "what the key move is." That is the audit's central correction,
now measured: 13 of 21 versus 18 of 21 for the best candidate.

Every `SourceHit@1` number in this program's history is therefore an
authorship-alignment diagnostic, never a keyness claim.

### 2. My recommendation was based on the wrong metric

I recommended promoting `R_introduced_depth` because it led on `SourceHit@1`
(0.603 vs 0.587). On the semantic panel the order reverses: **V8-faithful
0.857, introduced+depth 0.762.**

**But the difference is not significant.** 18/21 versus 16/21, four discordant
proofs (3 favouring V8, 1 favouring introduced+depth), exact McNemar
two-sided **p = 0.625**. At n=21 a two-proof gap is noise.

The honest conclusion is *not* "V8 wins". It is: **the metric I used to
recommend a promotion does not measure the thing we care about, and on the
metric that does, the two are indistinguishable at this sample size.**

Where they differ:

| proof | band | theorem | V8 | intro+depth |
|---|---|---|---|---|
| 06 | 11–25 | `CategoryTheory.Limits.Types.instHasImage` | miss | hit |
| 09 | 26–50 | `CategoryTheory.unop_tensorObj` | hit | miss |
| 10 | 26–50 | `USize.toBitVec_neg` | hit | miss |
| 25 | 126+ | `SpecialLinearGroup.toLinearEquiv_eq_coe` | hit | miss |

---

## The task is meaningful: baselines collapse

Random scores 0.143, term-order 0.095, popularity 0.048, reverse-depth 0.000 —
against 0.62–0.86 for every real candidate. The separation between signal and
noise is large and unambiguous, which is the main thing a vibes check needs to
establish.

Note popularity at 0.048: as a *local keyness* score it is worse than random.
This is now confirmed on semantic labels, not only on source agreement.

## Inter-rater agreement

Mean pairwise Jaccard **0.791** across all proofs — high for a task with free
selection from a dozen candidates.

By depth band: 0–10 = 0.61, 11–25 = 0.75, 26–50 = 0.83, 51–75 = **1.00**,
76–125 = 0.83, 126+ = 0.73.

**Registered prediction P3 — agreement lower at shallow depth — is
SUPPORTED.** Raters agree perfectly in the 51–75 band and least near the
foundations, which is consistent with the earlier finding that glue is
genuinely the content at shallow depth and therefore harder to call.

## NONE_LISTED: the coverage gap, measured semantically

A majority of raters said the real key move was **absent from the candidate
list** in **4 of 25 proofs (16%)**.

Per-rater: R1 = 6, R2 = 4, R3 = 1. That spread is itself informative — raters
differ substantially in willingness to declare a proof's content unlistable,
so 16% should be read as an estimate with wide uncertainty.

This is the semantic counterpart of the coverage measurements: some proofs
work by manipulating local hypotheses, exhibiting witnesses, or splitting into
cases, and no citation list can express that. It is evidence for the local
typed-move layer, not a rating failure.

## Registered predictions

| prediction | outcome |
|---|---|
| P1 `R_introduced_depth` leads on SemanticCoreHit@1 | **FALSIFIED** (V8-faithful leads, though not significantly) |
| P2 NONE_LISTED more common in the two shallowest bands | not supported cleanly; the 4 majority-NONE proofs are spread, not concentrated shallow |
| P3 inter-rater agreement lower at shallow depth | **SUPPORTED** (0.61 at 0–10 vs 1.00 at 51–75) |

## What this does and does not license

**Does:** retire `SourceHit@1` as a promotion criterion. Confirm the task and
the apparatus produce separable signal. Confirm popularity is dead as a local
keyness score. Establish that ~16% of proofs cannot be explained by citations
at all.

**Does not:** promote any ranking. n = 21 scored proofs, three agent raters,
one panel, and the top two candidates are two proofs apart. A promotion needs
the larger pre-registered panel from the constitution package (TEST-R at 360
proofs, sealed, with the graded 0–4 rubric rather than binary picks).
