# Map of Mathematics — MathRecord / MathMap

Research program: determine which representation of formal (Lean) mathematics, if any, deserves to become a navigable "map of mathematics". Lean is the verifier; one heterogeneous, typed, relational verified structure underlies all task-specific views (ADR-0003 invariants).

## State

- **Gates 0–1 (PASS):** exact Lean-backed record validated on an adversarial corpus. `reports/GATE_0.md`, `reports/GATE_1.md`, `SCHEMA.md`.
- **Phase 2A/2B (executed):** six-file Mathlib representation study + use-event feasibility. `reports/REPRESENTATION_CHARACTERIZATION.md`, `reports/USE_EVENT_FEASIBILITY.md` — read with `reports/PHASE2_ERRATA.md`.
- **Phase 3 (current):** structural role & landmark separability — can no-name topology identify machinery, and does soft downweighting improve landmark ranking? Authority: `handoff/phase3/`. Direction: `docs/CURRENT_RESEARCH_DIRECTION.md`. Work: `studies/phase3_structural_separability/`.

## Layout

- `handoff/phase3/` — current authoritative handoff; `handoff/notebook/` — non-authoritative research ideas.
- `mathrecord/` — Lean 4.33.0 extractor/validator/projections; `corpusenv/` — pinned Mathlib checkout (gitignored).
- `studies/` — extraction datasets (large JSONs gitignored, regenerable via `analysis/run_corpus.sh`) and analysis outputs.
- `reports/` — gate/phase reports and evidence (historical reports never rewritten; corrections via errata).
- `decisions/` — ADR-0001 wrap-Lean; ADR-0002 characterize-before-ontology; ADR-0003 structural-separability phase.
- `analysis/`, `review/` — Phase 2 tooling and review bundle.
- `archive/` — superseded handoffs (v2, v5) and pre-project material.

`NEXT_RECOMMENDATION.md` always holds the current approved step or the latest evidence-based recommendation; superseded ones live in `reports/`.
