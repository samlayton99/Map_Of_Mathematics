# Current Research Direction

As of 2026-08-19, governed by the Phase 3 handoff (`handoff/phase3/`, ADR-0003). The research notebook (`handoff/notebook/`) remains non-authoritative reference; v5 execution docs are archived (`archive/handoff_v5_phase2/`).

## Current phase — Phase 3: Structural Role and Landmark Separability

- **Question A:** can graph structure — no declaration names, source text, docstrings, or semantic content — identify formal machinery (the existing P3 classes) in the raw exact record? Class-by-class, after controlling for degree, extraction boundary, and domain.
- **Question B:** treating machinery as a probabilistic, context-sensitive role (not deleted), does topology improve ranking of the mathematical landmarks inside individual proofs?
- Review evidence: compact user vibe-check packet + independent agent review passes + explicitly-marked formal proxies. **No human expert gate.**
- Methods discipline: primary graphs from raw P1/P0 (P3 only as labels/strata/baselines); strict topology-only and typed-structure tracks; automated leakage tests; interpretable models first, no GNN; grouped file/domain holdouts; degree-matched controls; reversible filtering only.

## Architectural invariants (settled for this phase)

One heterogeneous typed relational verified structure beneath all task-specific views; dynamic Lean-checked applicability (no permanent global applicability edges); workspace / experience-corpus / semantic sidecars kept separate from the verified core; definition generation broader than internal compression; time-indexed evolving map; long-term application-domain navigation preserved; raw evidence survives every view.

## Status ledger

- Gates 0–1 (PASS, 2026-08-18): exact record validated; kernel-recheckable, deterministic, alpha-invariant.
- Phase 2A/2B (executed 2026-08-18): six-file Mathlib corpus characterized; use events 72% attribution / 82.5% tactic-theorem coverage. **Three corrections apply: `reports/PHASE2_ERRATA.md`** (P5⊆P2 not universal; 68.9% term proofs, not 76%; P4 result-inference 61.4%, not overwhelming). No human validation occurred; no primary representation was selected.
- Phase 3 (current): structural separability study; outputs land in `studies/phase3_structural_separability/`; nothing promoted to schema without a further ADR.
