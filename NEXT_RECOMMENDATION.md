# Next Recommendation (2026-08-27)

Prior gates closed: G1 80/80 audit-clean; semantic ladder run (see README and `docs/CURRENT_RESEARCH_DIRECTION.md`). The next cycle, in priority order:

1. **Semantic-grain decision dataset + hierarchical policy.** Convert reference traces (`bigdata/semtrace{80b,300,3k}.jsonl`) into per-decision training examples at the semantic grain: π(family|state) · π(parameter|family,state). The certificate-grain ranker v3 (top-1 0.645) is not the final surface; rewrite-set selection is.
2. **Close the Gate C mechanical gap (67→80).** Failure modes are enumerated in the cycle report: `simp made no progress` (direction/conditional-rewrite cases), residual-goal/continuation mismatches, 7 uncaptured. Each is an executor defect, not search difficulty.
3. **Remaining invisible action classes**: `congr` (119), `Eq.ndrec` (78), `id` (63), `Exists.casesOn` (51), `And.casesOn` (33), `Eq.rec` (31) — extend the mechanical operator family.
4. **Connect ranker to best-first search** only after per-decision metrics exist on the semantic action space; then measure end-to-end at fixed budget vs the A″/G3 controls.
5. **Durability** (not yet executed): second Lean/Mathlib snapshot, metamorphic source refactorings, per-family semantic branching-factor measurement.

Do not start value learning / MCTS / expert iteration before 1–4.
