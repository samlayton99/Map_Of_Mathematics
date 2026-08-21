# P0 — Audit of what the SEALED-R1 raters actually saw

Audited: `src/sealed_sample.py` (brief generator), `src/label_prep.py` (dev-round generator, same format),
`src/sealed_analysis.py`, `PREREGISTRATION_SEALED_R1.md`, `SEALED_R1_MANIFEST.json`,
actual brief files in `review/sealed_r1/*.md` (spot-checked against code; they match).

## What one graded item looked like

Per proof: `THEOREM PROVED: \`name\`` + target depth + depth band. **No theorem statement, no proof source.**
Per candidate: `` `name` [kind, depth N, in-statement|introduced-by-proof, role X]``, shuffled per-proof
(seed `20260824 + 7919*n`). No score, rank, rarity, in-degree, or gen flag anywhere. TEST-C batches
additionally carried the defect-cause taxonomy (A generated / C instance / F depth-inflated ...) for grades <= 1.

## Verdict table

| signal | rater visibility | conclusions affected |
|---|---|---|
| **depth** (candidate + target) | **VISIBLE** — integer printed on every candidate and in every proof header. "Not a hint" instruction is the only mitigation. | Any grade-vs-depth correlation is partly self-fulfilling. Depth-conditional glue results (S5/S6, glue-by-depth) doubly so — see below. |
| **role** | **VISIBLE** — exact 8-way label (`instance-slot`, `let-value`, ...) printed on every candidate; same vocabulary the role-tier voter uses. | Claim (a) role-bucket usefulness: contaminated (see below). |
| **in-statement** | **VISIBLE** — binary tag on every candidate ("either can be key" is the mitigation). | `stmt` voter's grade-correlation partly circular; modest, since the tag is symmetric-worded. |
| **kind / is_proof** | **VISIBLE** — `theorem`/`def`/... printed; directly reveals the `isproof` voter's bit. | `isproof` voter correlations (CORE 0.879 vs JUNK 0.064 is_proof) partly circular. |
| **rarity (IDF50)** | **HIDDEN** — no counts shown, not computable from a brief. (LLM background familiarity with common Mathlib lemmas is world knowledge, not brief leakage.) | Grade-vs-rarity correlations are genuine evidence. |
| **gen flag** | **HIDDEN as a coordinate.** Inferable only via names (`.eq_1`, `_proof_`, `match_`), which is sanctioned name-visibility. TEST-C S1 selection used the flag, but raters never saw stratum labels. | S1 defect-rate results stand. |
| **composite score / rank** | **HIDDEN** — no ranking shown, candidates shuffled per proof, briefs generated before analysis, order carries no information. | Ranking-vs-grade endpoints (NavigationAP etc.) are not order-leaked. Clean. |
| **arity, in-degree** | **HIDDEN.** | Arity-voter correlations are evidence. |

## Two rubric-text contaminations (worse than the tags)

1. **JUNK is defined as the signal.** Grade-0 text: "instance/typeclass resolution, universe or decidability
   bookkeeping" — printed next to candidates tagged `role instance-slot`. The mapping instance-slot -> 0/1 is
   nearly instructed. Consistent tell: instance-slot has the *lowest* rater disagreement in the dataset (0.11
   vs 0.22–0.43 elsewhere, FAILURE_BANK_M1 §4.3) — certainty that cheap usually means rule-following, not judgment.
2. **The depth-conditional glue hypothesis is written into the rubric.** "Near the foundations, assembling
   equalities really can be the whole argument" + "If the theorem is a deep result and the item is `Eq.mpr`,
   that is 1" — with target depth printed in each proof header. Prediction S6 (shallow glue legit, deep glue bad)
   could not have failed; its confirmation is not evidence.

## Downstream claims

| claim | verdict |
|---|---|
| (a) Role-bucket usefulness ordering (applied/let-value ~0.83–1.00 useful ... instance-slot 0.038; the "let-value 92% ... 1.6%" figures are variants of the same conditioning) | **Undermined in magnitude, probably right in direction.** Computed as P(grade >= 2 \| role tag), where the tag was on the page and the rubric keyed JUNK to it. The extreme instance-slot separation and its 0.11 disagreement are inflated by circularity. Direction is independently plausible (instance decls are recognizable by name), but the percentages cannot be quoted as independent human judgment. Needs one re-grade round with role/depth/in-statement tags stripped. |
| (b) HYB_copeland_first KeyMove@1 0.897 vs 0.825 (REF_weighted_role_x_rarity) | **Mostly survives as a relative claim.** Both sides are scored against the *same* fixed label set; the comparison is rule-vs-rule, paired per proof (McNemar). Leakage inflates all role/depth/stmt-using voters together, so it moves absolute Key@1 levels more than the ordering of aggregation rules. Caveat: leakage adds shared correlation between voters and grades, so the pairwise-majority margin (+0.033, CI [+0.006,+0.061]) could shrink on clean labels; treat the delta as fragile, the mechanism (Condorcet-winner promotion) as real. |
| (c) Glue/junk composition metrics (BadGlue@1, cleanliness, defect-cause mix) | **Split verdict.** Junk-share and cleanliness at k for rankings that do NOT use role (depth, popularity, term-order, random baselines) are evidence. For role-using rankings (V8, composite) the "junk demoted" numbers are partly the rater and the ranking reading the same printed tag. The depth-conditional glue composition (glue-by-depth, S5 vs S6) is rubric-instructed and should be treated as unmeasured. |

## Sampling frame (question 5)

**Theorem-only, by construction.** Eligibility in both rounds: `node_kind[d] == 0` (theorem targets only),
`not node_gen[d]`, human-written, U1D, 3–25 candidates. Definitions, constructions, instances, inductives were
**never graded as targets** — they appear only as candidates. Also excluded: proofs with >25 candidates (large
proofs) and <3 (trivial ones). So all 552 graded proofs are mid-sized human theorem proofs; nothing measured
here transfers to navigating definition/construction nodes, and the pre-registration says so ("human-written
theorem targets") — this is a declared scope limit, not a hidden bias.

## What is clean

Shuffle blinding is real (per-proof seeded permutation, no rank/score anywhere); dev/sealed disjointness enforced
by declaration id; seed and prereg hashed before sampling; rarity/arity/in-degree/gen/composite never printed.
The alpha 0.881 gate is honest about agreement but agreement partly measures shared tag-following (all raters were
the same model family — disclosed in prereg §9.3), so it cannot certify independence from the leaked signals.
