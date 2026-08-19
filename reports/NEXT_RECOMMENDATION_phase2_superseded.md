# Next Recommendation — Phase 2A/2B (2026-08-18)

**Run another bounded representation study** (Outcome 2 of `handoff/00` §15) — specifically, the human-review pass over the already-built 76-proof bundle, plus two classified attribution-gap fixes. Exactly one recommendation, per protocol.

## Why not Outcome 1 (select and proceed)

Every *technical* criterion for selection is met, and a front-runner exists: the hybrid of **P3-filtered support + P4-route skeleton + P5 use events** is recoverable across the heterogeneous corpus, deterministic (byte-identical reruns), style-covering (P4-route works on the 76% of proofs that are term-mode, P5 covers 82.5% of tactic proofs with exact states), compressive (median 1–4 route steps vs 10⁲–10⁴-node terms), mutually consistent (P5 ⊆ P4-heads ⊆ P2 containment 1.0), and provenance-complete. But the pre-registered decision rules (`handoff/06` §3–4) make human review a hard gate for "more useful than raw dependency output", and **no human review was performed in this run**. Recommending selection now would be exactly the construction-equals-success error the handoff warns against.

## Why not Outcome 3 (stop)

None of the stop signals fired: the candidate views are not mere dependency restatements (P4-route adds order/nesting/relation labels that P2 lacks; P5 adds roles and exact before/after states); recovery required no heavy semantic reconstruction (everything is deterministic extraction); use-event coverage is high-precision and honestly partial rather than too poor (32/32 manual precision, 82.5% tactic-theorem coverage, all gaps classified).

## The smallest experiment that resolves the uncertainty

1. **Human review** of `review/` (76 stratified proofs, worksheet included): one or ideally two mathematically competent reviewers rate P2/P3/P4-route/P5 per proof. This directly decides "useful vs noise", "does order matter", "does expansion help", and where natural-language tagging is indispensable.
2. **Fix the two classified attribution gaps** before the next measurement so they don't contaminate it: rewrite-rule TermInfo inside structure-literal proofs (follow delayed-assignment InfoTree branches), and case-alternative vs eliminator attribution for `cases`/`induction`.
3. Optionally re-measure P5 coverage after the fixes (one command; the pipeline is deterministic).

Then re-enter the decision with human evidence. If review favors the hybrid, the pre-specified next step is the controlled navigation experiment of `handoff/06` §7 — `(Γ, A) ↦ rank useful declarations` against text/flat-dependency baselines with module holdouts. If review says the views are noise, Outcome 3 becomes the honest choice and MathRecord remains exact tooling.

## Evidence

`reports/REPRESENTATION_CHARACTERIZATION.md`, `reports/USE_EVENT_FEASIBILITY.md`, `reports/HONEST_ASSESSMENT.md`, datasets `studies/` (regenerable via `analysis/run_corpus.sh`), review bundle `review/`. Negative/limiting findings are recorded and count as results: algebraic-domain support is up to 71% infrastructure; automation and structure-literal elaboration lose attribution; conceptual grouping is absent from every purely formal view.
