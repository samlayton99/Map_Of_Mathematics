# Phase 3 — Honest Assessment

## What was established

1. **A modest, real, cross-domain no-name structural signal for machinery exists.** Strict topology on the simple dedup graph: AUC 0.757 vs degree-only 0.693 under leave-one-domain-out; survives degree matching (0.72 vs 0.64). The typed occurrence profile (statement-vs-body reference structure) is the strongest formal signal: 0.802, degree-matched 0.86 vs 0.66.
2. **Separability is class-specific, not uniform.** Typeclass-instance is genuinely structurally recognizable (0.97); internal-detail needs typed relations (0.85); generated and structure-projection separability is degree in disguise; four classes have no stored positives and remain untested in the fair population.
3. **Occurrence multiplicity is noise for role identification and near-useless for landmark ranking** — the unweighted graph beat the weighted one, and multiplicity ranked worst in review (2.1/5). This contradicts a natural assumption and is double-evidenced.
4. **Landmark ranking: the pre-registered soft-downweighting success condition failed.** salience − λ·machineryProb (2.7/5) lost to global PageRank (3.3), P3 filtering (3.2), and P4-route (3.9). The hybrid that puts exact route/event evidence first and uses topology only as tie-breaker won (4.1/5, 19/48 best-view votes) — the win belongs mostly to the exact P4/P5 evidence, not topology.
5. **The machinery/content boundary is context-dependent**, exactly as hypothesized: file-local instances read as content, structure constructors read as machinery (and expose a genuine P3 label gap). A global binary partition is the wrong object; a calibrated role probability conditioned on context is the right one.

## What was only reproduced from P3

All Question A numbers measure recoverability of P3's deterministic labeling, not human truth. High AUC on typeclass-instance means instances have a distinctive formal role — which was already plausible; the value is the calibrated probability and the disagreement analysis, not the label parroting.

## What remains a proxy

- The proxy landmark labels (P4/P5-derived) are circular and were used descriptively only.
- Both completed review passes are Claude-based reasoning agents (independent contexts and blinded packets, but shared model priors; agreement ρ=0.97 partly reflects that). The 12-proof user packet is built and unreviewed. No human validation is claimed.

## What failed

- Strict topology on the weighted graph *underperformed* degree-only (0.677 vs 0.693).
- The linear soft-downweight ranker failed its success condition outright.
- Declaration ranking hit a structural ceiling: both reviewers independently identified move-level blind spots (local hypotheses, witnesses, case structure, representation changes) that no declaration list can express, and one proof where equation-compiler indirection (`_unary`) hid the entire argument from every view.
- Three review packets had truncated sources (span/attribute bug) — a packet-generation defect, documented, responses down-weighted.

## Verdict on topology's role

**Use topology as a calibrated soft infrastructure prior and diagnostic, not as a primary map signal.** (Decision rule: Question A succeeds / Question B fails in its strict form → "retain topology as an infrastructure diagnostic".) Its diagnostic value is proven twice over: it cleans candidate views (hybrid tie-breaking), and it audits the labeling scheme itself (constructor gap, context-dependence).

## The single recommended next step

Fix the two mechanical blockers that capped every view — follow `_unary`/`match_` indirection before ranking, and repair the three packet spans — then put the **existing 12-proof user packet** in front of the user. That is the cheapest decisive evidence on whether the hybrid view (exact route/events first, topology prior as tie-breaker) is good enough to seed a navigation experiment, and it requires no new infrastructure.
