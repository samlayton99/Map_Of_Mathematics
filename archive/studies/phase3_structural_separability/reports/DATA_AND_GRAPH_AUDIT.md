# Phase 3 — Data and Graph Audit

Source: Phase 2 study JSONs (six Mathlib v4.33.0 files), raw P1 occurrence evidence. Construction: `src/build_graph.py` (deterministic, tested). Numbers: `data/audit.json`.

## Graph

`G_decl_raw`: **3,662 nodes** (unique declarations; the Phase 2 "5,204 backing declarations" counted per-file rows — 369 nodes appear in several files), **31,287 unique directed pairs** carried by 44,366 typed edge rows (type-layer 15,064 / body-layer 29,302) and **640,860 raw occurrences**. Orientation u→v = "u refers to v". The graph is a **true DAG** (zero nontrivial SCCs) and a single weakly connected component.

## Coverage strata and the boundary artifact

- 1,711 stored (full bodies) vs 1,951 shallow (type-only, imported).
- **Shallow nodes have out-degree 0 by construction (100%)** — the dominant extraction-boundary artifact. Stored: 0.4% out-degree-0.
- Degree: stored median 15 (mean 20.7); shallow median 2 (mean 13.9).
- PageRank rank correlation between full graph and stored-only subgraph: 0.92 — global centrality is moderately but not fully robust to the boundary.

Consequences implemented: the **primary population** for Question A is stored ∧ P3-evaluated (n=876, prevalence 0.448); the all-evaluated population (n=2,827, prevalence 0.376) is sensitivity-only; coverage status is never a feature.

## Labels

P3 evaluation exists for 2,827 nodes (those referenced by some stored declaration). 835 stored-but-never-referenced nodes are unlabeled and excluded from Question A. Class prevalence (evaluated): typeclass-instance 533, internal-detail 363, structure-projection 229, generated 102, eq-machinery 19, logic-core 15, recursor 10, coercion 1. The last four are underpowered in the primary population (0–5 stored positives) — reported as skipped, not silently pooled.

## Documented feature limitations

- Pivot-sampled betweenness is order-sensitive under identifier renaming (rank corr ≈ 0.50); model weight is small (|coef| 0.16). All other strict features are exactly renaming-invariant (tested, `tests/test_phase3.py`).
- Greedy-modularity communities can shift under exact modularity ties (rank corr > 0.5 required by test); the without-community ablation bounds their influence (removing them *raises* grouped AUC 0.677→0.691).
- Multi-file nodes are assigned their first file for grouped splits (369 nodes; noted, group leakage direction is conservative).

## Fair-comparison population for Question B

24 stratified proofs (fixed seed, manifest in `data/landmark_sample_manifest.json`, selected from the committed Phase 2 review bundle before any model output was inspected); 845 candidate declaration-occurrences with explicit P4-inference missingness (114 candidates with `result_ok_frac` < 1 kept in-band).
