# Sealed Round 1 — results

> **THE PROMOTION IN THIS REPORT IS VOID.** `R_phase5_composite` violates
> append-safety / the canonical-layer principle (library-wide citation counts,
> `dmax` normaliser). See `../../phase6_stable_local_geometry/PROGRAM.md`.
> The measurements below remain valid as data.

Pre-registration `PREREGISTRATION_SEALED_R1.md`, sha256 `8765ace1fa4aa115…`,
written and hashed **before** any sample was drawn. Analysis run **once**, in
the pre-registered order. No ranking was tuned on these results.

| | |
|---|---|
| proofs | 552 (CAL 72, TEST-R 360, TEST-C 120) |
| graded candidates | 7,531 |
| grades collected | 22,593 |
| rating tasks | 69 (23 batches x 3 independent raters) |
| validation problems | **0** |
| disjoint from development set | yes, enforced by declaration id |

---

## 1. Reliability gate — PASSED

Krippendorff's alpha with ordinal weights over the 72 CAL proofs, 962
multi-rated candidates, 2,886 pairs.

| | |
|---|---|
| **alpha (ordinal)** | **0.881** (pre-registered gate 0.67) |
| alpha (nominal) | 0.732 |
| exact agreement | 0.809 |
| adjacent agreement | 0.995 |
| pairs differing by >1 grade | 14 of 2,886 |

Per band: 0.941, 0.941, 0.856, 0.890, 0.799, 0.796. TEST was unblocked only
after this passed.

---

## 2. Primary endpoint — TEST-R, 360 unseen proofs

NavigationAP: per-proof average precision, positives = median grade ≥ 2
(a useful visible landmark), macro-averaged.

| ranking | **NavAP** | MajorAP | BadDemAP | clean@1 | major recall@4 |
|---|---|---|---|---|---|
| **R_phase5_composite** | **0.871** | 0.918 | 0.939 | 0.983 | 0.893 |
| R_v8_faithful | 0.807 | 0.872 | 0.904 | 0.981 | 0.842 |
| R_introduced_depth | 0.806 | 0.864 | 0.912 | 0.956 | 0.833 |
| R_v8_all_kinds | 0.784 | 0.867 | 0.895 | 0.947 | 0.819 |
| O_source *(oracle)* | 0.784 | 0.821 | 0.905 | 0.928 | 0.784 |
| R_depth | 0.783 | 0.820 | 0.905 | 0.928 | 0.782 |
| B3_term_order | 0.492 | 0.356 | 0.757 | 0.375 | 0.341 |
| B0_random | 0.470 | 0.341 | 0.724 | 0.361 | 0.333 |
| B2_popularity | 0.322 | 0.162 | 0.556 | 0.167 | 0.076 |
| B1_reverse_depth | 0.305 | 0.159 | 0.568 | 0.058 | 0.086 |

Paired hierarchical bootstrap, 2,000 replicates, Holm-corrected across nine
comparisons:

| vs | ΔAP | 95% CI | p (Holm) |
|---|---|---|---|
| R_v8_faithful | +0.064 | [+0.048, +0.080] | <0.0001 |
| R_introduced_depth | +0.065 | [+0.052, +0.079] | <0.0001 |
| R_v8_all_kinds | +0.087 | [+0.072, +0.102] | <0.0001 |
| O_source | +0.088 | [+0.074, +0.102] | <0.0001 |
| R_depth | +0.088 | [+0.074, +0.103] | <0.0001 |
| B3_term_order | +0.379 | [+0.356, +0.404] | <0.0001 |
| B0_random | +0.401 | [+0.379, +0.424] | <0.0001 |
| B2_popularity | +0.549 | [+0.524, +0.574] | <0.0001 |
| B1_reverse_depth | +0.567 | [+0.548, +0.588] | <0.0001 |

Every interval excludes zero **and** exceeds the 0.02 practical-equivalence
margin. No ranking is disqualified by the catastrophic-stratum rule.

### DECISION: **PROMOTE `R_phase5_composite`**

**The replication is near-exact.** The development estimate of the margin over
V8 was +0.064; the sealed estimate on 360 proofs never previously examined is
+0.064. That is the strongest evidence this program has produced for anything.

---

## 3. Registered predictions — as they actually landed

| id | prediction | outcome |
|---|---|---|
| S1 | composite leads NavAP on TEST-R | **SUPPORTED** |
| S2 | its margin over V8 is *smaller* when sealed, but still excludes zero | **FALSIFIED in its main claim** — the margin was *identical* (0.064 both), not smaller. The CI-excludes-zero half held. |
| S3 | lift over random rises with target depth | **SUPPORTED** — 1.61x shallow to 2.07x deep, though not monotone (dips at 76–125) |
| S4 | band 26–50 is worst for every candidate ranking | **PARTIAL** — worst for 3 of 4; `R_introduced_depth`'s worst band is 11–25, by 0.009 |
| S5 | the auto-generated stratum has a higher rank-1 defect rate | **SUPPORTED strongly** — 0.400 against 0.017 on TEST-R overall, a 23x rate |
| S6 | shallow glue is more often legitimate than deep glue | **SUPPORTED** — defect@1 0.100 shallow vs 0.150 deep |
| S7 | SourceHit ordering disagrees with NavigationAP ordering | **SUPPORTED** — composite ranks **3rd** on SourceHit@1 (0.611) and **1st** on NavigationAP |

S7 is worth dwelling on: had we still been promoting on source agreement, we
would have promoted `R_v8_faithful` (SourceHit 0.635) and rejected the ranking
that is decisively better at the actual task.

---

## 4. Depth

| band | composite | random | lift | n |
|---|---|---|---|---|
| 0–10 | 0.914 | 0.566 | 1.61x | 60 |
| 11–25 | 0.886 | 0.455 | 1.95x | 60 |
| 26–50 | **0.834** | 0.440 | 1.89x | 60 |
| 51–75 | 0.892 | 0.481 | 1.85x | 60 |
| 76–125 | 0.843 | 0.464 | 1.82x | 60 |
| 126+ | 0.858 | 0.414 | **2.07x** | 60 |

Absolute score is highest at shallow depth, but so is random's — half of a
shallow proof's candidates are useful, so you cannot miss. **Corrected for
that, the ranking contributes most at depth**, which is the right shape for a
map: deep theorems are where a reader cannot eyeball the list themselves.

Band 26–50 is again the hardest, now for the fifth independent time.

---

## 5. Recall

| top k | core moves (grade 4) | major (≥3) | useful (≥2) |
|---|---|---|---|
| 1 | 0.652 | 0.456 | 0.233 |
| 2 | 0.882 | 0.702 | 0.405 |
| 4 | **0.987** | 0.893 | 0.651 |
| 8 | **1.000** | 0.978 | 0.873 |
| 12 | 1.000 | 0.994 | 0.955 |

**Every core move is visible by k=8, and 98.7% by k=4.** Recall is not the
binding constraint; precision in the middle depth bands is.

Grade distribution over TEST-R: KEY 382, SUPPORT 302, LEGIT_GLUE 833,
BAD_GLUE 1851, JUNK 1432. Two thirds of the candidate universe is plumbing or
noise — the floor any ranking must beat.

---

## 6. TEST-C — the defect challenge

Leader's rank-1 defect rate by stratum, against 0.017 on TEST-R overall:

| stratum | defect@1 | NavAP | n |
|---|---|---|---|
| **S1 auto-generated present** | **0.400** | 0.716 | 20 |
| S4 single-user cited declaration | 0.300 | 0.782 | 20 |
| S5 deep target + logic-only glue | 0.150 | 0.818 | 20 |
| S6 shallow target + logic-only glue | 0.100 | 0.885 | 20 |
| S3 type-position-only occurrence | 0.050 | 0.848 | 20 |
| S2 instance-heavy | **0.000** | 0.882 | 20 |

**Auto-generated declarations are confirmed as the dominant navigation
defect** — a 23x elevated failure rate, exactly the mechanism traced in
`FAILURE_ANALYSIS.md`: they are rarer than the core mathematics (mean idf
12.70 against 11.37), and the leading score is essentially a rarity score.

**Instance-heavy proofs are not a problem at rank 1 (0.000).** This
contradicts my reading of the development data, where instances appeared among
the named failures. Rater cause codes explain why: `C` (irrelevant instance
plumbing) is by far the most common defect cause overall — 2,187 of 3,282 —
but instances almost never reach rank 1. **The ranking already demotes them
correctly.** They are a tail problem, not a top problem.

Defect causes: C 2187, E incidental logic 380, D tactic/certificate 349,
G other 225, **A generated 99**, F depth-inflated 40, B wrapper 2.

---

## 7. Corrections to earlier claims

**The 12.5% missing-key figure was wrong.** I reported it from CAL and
attributed it to the two-stage protocol exposing coverage gaps. TEST-R, using
the identical protocol on 360 proofs, gives **1.9% (7/360)** — close to the
development round's 3.3%. The CAL figure was a sample artifact. The case for
an urgent local typed-move layer is correspondingly weaker, not stronger.

**Instances are not a rank-1 failure mode.** See §6.

---

## 8. What this does and does not license

**Does.** Promote `R_phase5_composite` as the standing ranking for the
citation branch, on a pre-registered sealed test with a passed reliability
gate, Holm-corrected intervals excluding zero by more than the equivalence
margin, and a near-exact replication of the development estimate. Retire
`SourceHit@1` permanently — it would have selected the wrong ranking here.
Confirm auto-generated declarations as the priority defect.

**Does not.** Resolve the longevity objection in `FAILURE_ANALYSIS.md`. The
promoted ranking is ~90% driven by `idf`, a library-wide citation count that
shifts with every Mathlib change, and whose most extreme values come from
compiler-generated declarations whose existence depends on the elaborator
version. **The winner on this objective is the least version-stable
candidate.** That conflict is unresolved and is registered as H4.

It also does not touch cross-proof calibration (measured at reduced power and
reported as indicative), the island/subject-atlas question (declared out of
scope), or the definition of a good *map* as opposed to a good ranking — which
remains the largest open problem in the program.
