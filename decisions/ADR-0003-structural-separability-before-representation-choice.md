# ADR-0003: Phase 3 tests structural separability; no human-review gate; invariants adopted

Date: 2026-08-19. Status: accepted. Supersedes the Phase 2 recommendation (now `reports/NEXT_RECOMMENDATION_phase2_superseded.md`) — the human-review pass it required will not be staffed with independent experts and is replaced, not skipped silently.

## Decision

Execute the Phase 3 handoff (`handoff/phase3/`): a bounded, reproducible study over the existing exact record asking (A) whether **no-name graph topology** can identify P3-classified infrastructure, controlling for degree, extraction boundary, and domain; and (B) whether a **soft machinery probability + theorem-local salience** score improves landmark ranking over raw support, P3 filtering, global centrality, and P4-route. Review evidence comes from a compact user packet, genuinely independent agent review passes where the environment supports them, and clearly-marked formal proxies — not a human expert gate.

Key methodological commitments: primary graphs derive from raw P1/P0 (never P3-filtered topology); P3 classes are labels/strata/baselines only; strict topology-only and typed-structure tracks with automated leakage tests; interpretable models first (no GNN); grouped file/domain holdouts and degree/boundary-matched controls; nothing hard-deleted; negative results are results.

## Architectural invariants adopted into current direction (handoff/phase3/core/01)

1. One heterogeneous, typed, relational verified structure underlies all task-specific views; graphs in this study are derived projections of it.
2. Formal applicability is state-dependent and dynamically checked by Lean — no permanent global applicability edges.
3. Workspace (conjectures, failed searches) and experience corpus are separate from the verified core; semantic labels are optional sidecars.
4. Definition generation is broader than graph-internal compression (external inspiration and applications count).
5. The map is time-indexed: new verified objects change future navigation geometry.
6. Linking formal mathematics to application domains remains a long-term goal.
7. Raw evidence survives every view; all filtering is reversible, scored, attributable.

## Consequences

- `reports/PHASE2_ERRATA.md` records three verified corrections (non-universal P5⊆P2, 68.9% term fraction, 61.4% P4 result-inference success); erratum banners point to it from the affected historical reports, whose bodies are unchanged.
- v5 execution docs move to `archive/handoff_v5_phase2/`; the research notebook stays live at `handoff/notebook/`.
- Study outputs are derived artifacts under `studies/phase3_structural_separability/`; nothing is promoted to core schema without a further ADR.
