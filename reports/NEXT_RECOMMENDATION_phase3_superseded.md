# Next Recommendation — Phase 3 results (2026-08-19)

**Update 2026-08-19 (full-library cone study, `studies/phase3_structural_separability/reports/CONES_REPORT.md`):** the recommended user review should include a third view per proof — the proof-introduced set N(T) = A_P \ A_S ranked by depth (name-free, zero training; recovers 77.5% of the P4-route skeleton, vs 70.8% for raw depth). Established alongside: depth ≈ log prerequisite volume (depth/cone-size/tree-size are one coordinate, Spearman ≥ 0.98, so "combine depth and size" is a dead end); relDepth is a construction-vs-assertion axis (defs 7, instances 9, theorems 2); 35% of theorems are pure interface (proof no deeper than statement); reuse-count marks glue, not importance. The rest of this document stands.

**Adopt topology as a calibrated soft infrastructure prior and diagnostic — not a primary map signal — and run the small decisive follow-up: fix the two mechanical blockers, then collect the prepared 12-proof user review.**

Per the pre-registered decision rules (`handoff/phase3/core/02`): **Question A succeeded, Question B failed in its strict form** → "retain topology as an infrastructure diagnostic".

## Evidence (details in `studies/phase3_structural_separability/reports/`)

- No-name machinery detection under leave-one-domain-out: typed track AUC 0.80 (degree-matched 0.86 vs 0.66), strict topology 0.76 on the simple graph vs 0.69 degree-only. Class-specific: typeclass-instance 0.97 (real), internal-detail 0.85 (typed only), generated/projection = degree in disguise.
- The pre-registered landmark condition failed: salience − machinery-prob (2.7/5) lost to global PageRank (3.3), P3 filter (3.2), and P4-route (3.9) in blinded review by two independent agent reviewers (ρ=0.97). The hybrid — exact P4-route/P5 evidence first, topology as tie-breaker — won at 4.1/5 with 19/48 best-view votes.
- The machinery/content boundary is context-dependent (file-local instances read as content; structure constructors exposed a genuine P3 label gap), supporting probabilistic, context-sensitive roles over a global binary partition.
- Structural ceiling identified: local hypotheses, witnesses, case structure, and representation changes are invisible to every declaration ranking; and equation-compiler `_unary` indirection can hide an entire proof from all views.

## The follow-up (small, no new infrastructure)

1. Follow `_unary`/`match_` indirection to bodies before ranking (deterministic, one level).
2. Repair the three truncated packet spans (attribute-line span bug).
3. Rebuild the 12-proof user packet and have the user complete it (`studies/phase3_structural_separability/review/user_packet/`) — the only missing evidence class is a human judgment on the hybrid view.

If the user review confirms the agent verdict, the pre-specified next stage is the controlled navigation experiment (`archive/handoff_v5_phase2/06` §7) seeded with: hybrid view as the candidate representation, machinery probability as a soft feature, and multiplicity excluded (double-evidenced as noise). If it contradicts the agents, that disagreement itself becomes the next study object.

Superseded predecessors: `reports/NEXT_RECOMMENDATION_gate1_superseded.md`, `reports/NEXT_RECOMMENDATION_phase2_superseded.md`.
