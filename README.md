# Map of Mathematics — MathRecord / MathMap

Research program: determine which representation of formal (Lean) mathematics, if any, deserves to become a navigable "map of mathematics". Lean is the verifier and source of formal truth.

## State

- **Gates 0–1 (PASS):** exact Lean-backed record (E,X,D,S + T spike) validated on an adversarial corpus. Evidence: `reports/`, `SCHEMA.md`, `LEAN_REPRESENTATION_AUDIT.md`. Code: `mathrecord/`.
- **Phase 2A/2B (executed):** six-file Mathlib candidate-representation study + use-event feasibility. Results: `reports/REPRESENTATION_CHARACTERIZATION.md`, `reports/USE_EVENT_FEASIBILITY.md`, `reports/HONEST_ASSESSMENT.md`. Recommendation: `NEXT_RECOMMENDATION.md` (another bounded study: human review of `review/`).
- Authority: `handoff/00`–`10`. Direction: `docs/CURRENT_RESEARCH_DIRECTION.md`.

## Layout

- `handoff/` — Balanced Research Handoff v5. `00`–`10` authoritative; `11`–`15` non-authoritative research notebook.
- `mathrecord/` — Lean 4.33.0 extractor/validator/projections (see its README).
- `reports/` — gate and phase reports with evidence (historical reports never rewritten).
- `decisions/` — ADRs. ADR-0001 wrap-Lean-not-new-IR; ADR-0002 characterize-before-ontology.
- `docs/` — current direction and phase docs.
- `sources/` — ecosystem audit, vision conversation source.
- `archive/` — superseded handoffs (v2) and pre-project material.

Superseded Gate 1 recommendation: `reports/NEXT_RECOMMENDATION_gate1_superseded.md`.
