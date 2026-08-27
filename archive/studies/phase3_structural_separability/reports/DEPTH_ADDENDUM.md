# Addendum — Recursive Unfolding Depth over the Full Library (user proposal, 2026-08-19)

Proposal (Sam): `depth(n) = 1 + max(depth of everything in n's proof term)`, primitives at 0, computed over the **complete** library closure; use depth cutoffs as a resolution dial and a machinery filter. This measure was not computable on the Phase 3 corpus graph (extraction boundary: imported nodes had no out-edges); it required the full-environment expansion the handoff licensed (`core/03` §5) and Phase 3 did not take. Correcting that: `mathrecord depdump` dumps every constant in `import Mathlib` (771,129 constants, 78s); `src/depth.py` computes depth (16s). Results: `data/depth_results.json`.

## Headline results

- Well-defined at scale: 771,129 constants, 543 cyclic stragglers (0.07%, unsafe-rec artifacts, fixpoint-resolved). Depth percentiles: median 33, p90 132, max 346.
- **Depth orders mathematical sophistication remarkably well** (anchors): `Nat.add_comm` 11 → `Nat.gcd_comm` 32 → `norm_add_le` 95 → `Real.exp` 140 → `Real.log` 162 → `Real.exp_log` 164 → `MeasureTheory.integral_add` 243.
- **The resolution dial works**: unclassified theorems at depth ≥50: 170k; ≥100: 67k; ≥150: 40k — a smooth, absolute, name-free coarse-graining knob.
- **Machinery-is-shallow holds for logical glue, inverts for tower machinery** (median depth / shallow-detects AUC): structure-projection 1 / 0.93 · eq-machinery 3 / 0.96 · coercion 3 / 0.95 · recursor 5 / 0.79 — versus **typeclass-instance 35 / 0.56 (coin flip)** and internal-detail 28 / 0.61 (both inherit the towers they sit on). Unclassified theorems: median 64.
- Depth alone gives p3_any AUC 0.64 over the full 771k population — weaker than the Phase 3 typed track (0.80) but with zero training and one interpretable number; Spearman with the learned machinery probability is **−0.24**: the two measures are complementary, not redundant.
- Calibration surprise: `dist_triangle` has depth **2** — in Mathlib the triangle inequality is a *structure field* (wrapper over the projection `PseudoMetricSpace.dist_triangle`); its mathematical depth lives in each metric-space instance that proves the field. Interface lemmas are shallow by design; their depth migrated into the instances — the same phenomenon that makes instances deep.

## Consequence

Adopt depth as a standing exact-derived feature: (1) a resolution dial for certified zoom with an absolute scale; (2) a zero-training detector for glue machinery; (3) a complement to the learned typed-track probability (instances are exactly where depth fails and the typed track excels). Candidate refinement to evaluate next: relative depth = depth(proof) − depth(statement), which should discount the pervasive-tower effect (max-brittleness).
