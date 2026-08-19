# ADR-0002: Characterize candidate representations before committing to a map ontology

Date: 2026-08-18. Status: accepted. Supersedes the recommendation in `NEXT_RECOMMENDATION.md` (Gate 1, same date).

## Context

Gate 1 closed with "proceed to dynamic traces (Gate 2)". The Balanced Research Handoff v5 (`handoff/`) supersedes that: intermediate proposals (v3 activity layer, v4 declaration-centered AND–OR map with selective zoom) moved from a compelling intuition to a prescribed ontology without evidence — ontology before measurement, support sets mistaken for explanations, human-scale routes assumed recoverable, zoom assumed useful (`handoff/01_INDEPENDENT_REASSESSMENT.md`).

## Decision

Before recording large-scale dynamic traces or committing any map schema, run a bounded study on real Mathlib that derives and compares candidate projections (P0 exact term graph, P1 reference occurrences, P2 support set, P3 filtered support, P4 named application occurrences, P5 source/elaborator use route, P6 selective expansion) of the same proofs, plus a use-event feasibility measurement. Only evidence from that comparison may promote a projection to persistent schema (each promotion needs its own ADR).

Dynamic traces are not rejected — deferred. The Gate 2 entry conditions listed in the superseded document (transition normalization, `sorryAx` failure semantics, mvar-state tables, SHA-256) remain valid engineering notes for whenever transition recording is authorized.

## Consequences

- The exact MathRecord core (ADR-0001) is unchanged and remains the substrate; all projections are computed views over it with provenance and trust classes.
- `NEXT_RECOMMENDATION.md` carries a supersession banner; content preserved as history.
- The v2 handoff documents are archived (`archive/handoff_v2/`); `handoff/00`–`10` are current authority, `handoff/11`–`15` are a non-authoritative research notebook.
- This run ends with exactly one of: select a representation and proceed to a navigation experiment; run another bounded study; or stop the map-centered program while preserving MathRecord as tooling.
