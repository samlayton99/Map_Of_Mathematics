# Pre-registration — Sealed Round 1 (navigation cleanliness)

**Written and hashed before any sample was drawn or any brief generated.**
Implements the v2 experiment constitution (docs 01–08 and 06A).

Round id: `SEALED-R1`
Sampling seed: `20260824` (fresh; not reused from any prior round)
Rating seed offset: `+7919 * proof_index`

---

## 0. Why this round exists

The development panel (180 proofs, 2,419 graded candidates) produced one
result that would change the standing ranking:

> On the v2 primary objective (navigation average precision, positives =
> grade ≥ 2), `R_phase5_composite` scored 0.865 against 0.801 for
> `R_v8_faithful` and 0.756 for `R_depth`, with a paired bootstrap CI of
> [+0.041, +0.087] versus V8 and wins in all six depth bands.

That contradicts the standing position that the composite is a weak comparator
to be frozen. **It was measured on development data and may not survive.** This
round exists to confirm or kill it on data never previously examined.

Mitigating fact, recorded now: the development labels were collected *before*
the v2 objective existed, so they were not tuned toward it. This round removes
the remaining risk that the 180 proofs are idiosyncratic.

---

## 1. Frozen objects

### 1.1 Candidate rankings — FROZEN, no additions after this file

`B0_random`, `B1_reverse_depth`, `B2_popularity`, `B3_term_order`,
`O_source`, `R_depth`, `R_introduced_depth`, `R_v8_faithful`,
`R_v8_all_kinds`, `R_phase5_composite`.

No ranking may be added, edited, or tuned after this file is hashed. A new
ranking begins a new round.

### 1.2 Evidence universe

Primary: **U1D**. Secondary reported: U1, U0. The universe is part of the
experiment's identity, not a display control.

### 1.3 Inclusion policies (display only)

top-k (k ∈ 1,2,4,8), per-proof percentile, global score quantile,
`cluster_split`, lanes. These may never move a ranking-quality number.

---

## 2. Sample design

All samples drawn from human-written theorem targets in U1D with 3–25
candidates, **disjoint from the 180 development proofs** (enforced by
declaration id).

| set | size | design | purpose |
|---|---|---|---|
| **CAL** | 72 | 12 per target-depth band | reliability gate + protocol check. Analysed FIRST and alone. |
| **TEST-R** | 360 | 60 per target-depth band | primary sealed endpoint |
| **TEST-C** | 120 | defect-enriched strata (below) | navigation-defect challenge |

Depth bands: 0–10, 11–25, 26–50, 51–75, 76–125, 126+.

### 2.1 TEST-C strata (20 proofs each)

Selected by **structural** signals only — no name matching anywhere.

1. proofs containing ≥1 candidate with the kernel auto-generated flag
   (`node_gen`);
2. proofs whose candidates are ≥50% instance-slot-only occurrences;
3. proofs containing a candidate occurring only in type-annotation position;
4. proofs containing a single-user cited declaration (library in-degree ≤ 1);
5. proofs at target depth ≥ 76 containing logic-only glue candidates;
6. proofs at target depth ≤ 25 containing logic-only glue candidates.

Strata 5 and 6 are the direct test of the depth-conditional glue hypothesis.

---

## 3. Annotation protocol

**Three independent raters per proof.** Raters are isolated reasoning agents;
they see no ranking, no score, no depth-derived hint beyond the depth integer
already shown as context, and no other rater's output.

**Two stages, in order, in one pass:**

1. **Free recall (before the candidate list is shown in the grading task).**
   The rater writes, in their own words, what the key moves of the proof are.
   This is recorded verbatim and is the instrument for measuring moves that
   *no citation can express*.
2. **Graded scoring.** The rater then grades **every** candidate 0–4 on the
   scale already fixed in the development round:
   4 CORE · 3 MAJOR/SUPPORT · 2 LEGITIMATE GLUE · 1 BAD GLUE · 0 JUNK.

Candidates are shuffled per proof with a per-proof seed.

Also recorded per proof: `missing_key` (a key move is absent from the list),
`confidence`, and for TEST-C only, a **defect cause** from the 06A taxonomy
(A generated obligation, B wrapper/forwarder, C irrelevant instance,
D tactic/certificate, E incidental logic, F depth-inflated, G other/named)
for each candidate graded ≤ 1.

**Aggregation:** median grade across the three raters. Spread is reported, not
hidden.

---

## 4. Reliability gate — evaluated on CAL, before TEST is analysed

Compute **Krippendorff's alpha with ordinal weights** over the 3 x 72 graded
candidate set.

- **alpha ≥ 0.67** → proceed to analyse TEST-R and TEST-C.
- **alpha < 0.67** → **no ranking may be promoted in this round.** Report the
  failure, and the round ends with outcome INSUFFICIENT RELIABILITY.

Also reported on CAL: exact agreement, adjacent agreement, per-band alpha, and
the share of proofs where raters disagree about `missing_key`.

CAL is not pooled into the primary endpoint.

---

## 5. Endpoints

### 5.1 Primary

**NavigationAP** — macro-averaged per-proof average precision on TEST-R,
positives = median grade ≥ 2, ranked by each frozen ranking within proof.

### 5.2 Secondary (all pre-specified)

- MajorAP (positives = grade ≥ 3) — guards against a clean-but-bland ranking
- BadEdgeDemotionAP (reverse order, positives = grade ≤ 1)
- NavigationCleanliness at top-k, k ∈ 1,2,4,8
- LegitimateCoverage and MajorMathCoverage at each k
- Cleanliness at legitimate-coverage 50/75/90/95%
- Coverage at defect-rate budgets 1/2.5/5/10%
- SemanticKeyMoveAt1 (the old primary, retained for continuity)
- SourceHit@1 (authorship diagnostic only — **may not promote**)
- Gradient quality: violation rate, spread, cross-depth calibration gap
- All of the above stratified by the six target-depth bands

### 5.3 TEST-C endpoints

- NavigationDefectRate at top-k per stratum
- Defect-cause composition at rank 1
- Depth-conditional glue: P(grade ≥ 2 | logic-only glue, target depth band),
  strata 5 vs 6

---

## 6. Statistical protocol

- **Hierarchical bootstrap**, resampling proofs (and raters within proof),
  **2,000 replicates minimum**, paired across rankings on the same proofs.
- **Holm correction** across the 9 pairwise comparisons against the leader.
- **Practical-equivalence margin: 0.02 AP.** A difference whose CI lies
  entirely within ±0.02 is declared equivalent, and simplicity decides.
- **Catastrophic-stratum rule:** a ranking is disqualified from promotion if
  its NavigationAP in any single depth band is more than 0.10 below the best
  ranking in that band, even if it leads overall.
- Every denominator, empty case, tie, missing judgment and failed prediction
  is reported.

---

## 7. Decision rule

Outcome is exactly one of:

1. **PROMOTE** — leader wins the primary endpoint with Holm-corrected CI
   excluding zero and the equivalence margin, passes the catastrophic-stratum
   rule, and does not lose MajorAP.
2. **NON-INFERIOR / SIMPLER** — a simpler ranking is within the equivalence
   margin of the leader; the simpler one is adopted.
3. **PARETO / TASK-SPECIFIC** — no single ranking dominates across
   cleanliness, major coverage and depth strata; multiple retained.
4. **REJECT** — no candidate beats the baselines meaningfully.
5. **INSUFFICIENT RELIABILITY** — the CAL alpha gate failed.

Outcome 1 is not to be forced.

---

## 8. Registered predictions (falsifiable; recorded so they can fail)

| id | prediction |
|---|---|
| **S1** | `R_phase5_composite` leads NavigationAP on TEST-R, replicating development. |
| **S2** | Its margin over `R_v8_faithful` is smaller on sealed data than the development +0.064, but the CI still excludes zero. |
| **S3** | Lift over `B0_random` rises with target depth, as on development (1.49x shallow → 2.06x deep). |
| **S4** | Band 26–50 is the worst band for every candidate ranking (third independent replication). |
| **S5** | On TEST-C stratum 1 (auto-generated candidates present), every ranking's defect rate at rank 1 exceeds its TEST-R rate. |
| **S6** | Depth-conditional glue: P(grade ≥ 2 \| logic-only glue) is higher in stratum 6 (shallow) than stratum 5 (deep). |
| **S7** | `SourceHit@1` ordering disagrees with NavigationAP ordering — source alignment again fails to track navigation quality. |

---

## 9. Declared deviations from the v2 constitution

Stated in advance rather than discovered afterwards.

1. **Cross-proof comparison pairs: 600, not 2,400.** Scoped to what this
   round can execute. Global calibration is therefore measured with reduced
   power and its result is reported as indicative, not decisive.
2. **Island/component panel (120 instances + controls): out of scope.** It
   tests the subject-atlas hypothesis, which is independent of ranking
   promotion. Deferred to its own round.
3. **Raters are all the same model family.** The constitution prefers multiple
   families; only one is available here. Disclosed as a threat to validity:
   correlated rater error cannot be excluded by agreement statistics alone.
4. **Free recall and grading occur in one agent pass**, with the recall
   written before the grades. A true sequential seal would need two calls;
   ordering within one pass is the available approximation and is disclosed.

---

## 10. Sealing

This file is hashed before sampling. The hash, the sample manifests, the
rater briefs and the analysis code are recorded in `SEALED_R1_MANIFEST.json`.
The analysis is run **once**. No ranking is tuned on the result. Any successor
hypothesis begins a new registered round.
