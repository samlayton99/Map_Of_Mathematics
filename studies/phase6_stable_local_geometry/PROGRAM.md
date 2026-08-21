# Phase 6 — Stable Local Geometry

Adopted 2026-08-21 from the GPT review (`gpt_handoff/`), endorsed by Sam.
This file is the single source of truth for what is alive, what is dead, and
what runs next. Historical reports in `../phase5_multiscale_navigation/reports/`
are preserved unchanged.

## Central hypothesis (H1)

Phase 5 treated a proof as a flat bag of citations and searched for a ranking
over that bag. The exact proof term is a rooted typed graph; flattening it
turns nested descendants (implicit args, instance support, generated
obligations) into direct siblings of the theorem. Two chronic problems are
predicted consequences:

1. Global rarity looked indispensable because it statistically pushes
   flattened descendants back down.
2. Universal constants became direct hubs and collapsed map distance
   (junk = 9% of declarations but 49-70% of top hubs).

H1: restoring the hierarchy reduces both, at equal recall, without a new
score. Falsifiable — see `gpt_handoff/04_HYPOTHESES.md`.

## Architecture

- **Layer A** canonical local move object per proof: typed occurrence DAG
  (expression path, parent application, argument index, role, nesting).
  Immutable under library growth.
- **Layer B** intrinsic descriptors per occurrence: role, nesting, d_target,
  d_cited, span, arity, isProof, generated/owner. A vector; never collapsed
  to one canonical scalar.
- **Layer C** global atlas: union of local objects with declaration
  interfaces identified. Append = embedding.
- **Layer D** dynamic global fields (rarity, centrality, communities,
  learned navigation) as VERSIONED SIDECARS. Legal again under refined
  principle 1; never rewrite A/B.

Proven impossibility (gpt_handoff/02, sec 2): no append-safe local statistic
can equal future-use universality. Stop hunting for a proxy; separate layers.

## Status ledger

### Dead / void
- `R_phase5_composite` promotion — void (live rarity in canonical layer).
- `battery.navigability` — measured connectivity, wrong question. DELETED.
- Junk-mask as primary validator — circular, inadmissible (principle 15).
- `delta_depth` as universality/junk classifier — refuted; it is abstraction
  span only.
- Single weighted score over salience x span x lane — replaced by
  multifiltration.
- 3-pass cycle relaxation depth (`src/build_incidence.py`) — replaced by
  exact SCC condensation.

### Alive, carried forward
- Occurrence roles (all 8), depth, in-statement, arity, isProof, gen flag —
  the Layer B vocabulary.
- Instance-slot forensics (25% of candidates, 96.5% junk) — becomes the
  infrastructure LANE.
- Condorcet/Copeland-first result (KeyMove@1 0.897) — carried as H5/H10 but
  MUST BE RE-MEASURED without the live-rarity voter; the measured gain
  included it.
- Tier merge 5->3 (P@1 0.972) — sibling-ordering baseline within hierarchy.
- Rarity — demoted to versioned sidecar / teacher / upper-bound comparator.
- Sealed-round grades (552 proofs, alpha 0.881) — development data;
  the grading briefs are audited in P0 before further reuse.
- Design constraints on record: lexicographic fails (97.6% single-occupied
  top tier); Pareto front >1 in 75-80%; role primacy falsified twice;
  ordinal rules lose P@4 (tail needs magnitude — H6 candidates).
- Eval apparatus: dashboard, plugins landing port, shortcuts.py,
  composition.py, reliability.py.

### Re-opened
- "Append-safety audit violations" (29) — reinterpreted: violations are
  banned from Layer A/B but may return as Layer D sidecars.

## Stages

- **P0 substrate corrections** -> `SUBSTRATE_CORRECTIONS.md`
  exact SCC depth; type-vs-value depth separated; statement-world closure
  audit; occurrence-level extraction (`hierdump`); generated-owner; grading
  brief audit.
- **P1 hierarchy pilot (48 proofs)** -> `HIERARCHY_VS_FLAT_RESULTS.md`
  four views: flat / owner-collapse / named-application hierarchy /
  hierarchy+lanes. Metrics: useful-recall at budget 1/2/4/8,
  artificial-jump rate, generated exposure, expansion completeness. No new
  fitted weights.
- **P2 metamorphic benchmark** -> `METAMORPHIC_BENCHMARK.md`
  Lean proof-variant pairs per gpt_handoff/06; skeleton invariance under
  harmless refactors, divergence under genuine change.
- **P3 stable local ordering** — baselines + compliant Copeland-first +
  hierarchy sibling ordering; publish signals, tie semantics, failures.
- **P4 edge-scale / self-similarity** -> `EDGE_SCALE_AND_SELF_SIMILARITY.md`
  span normalizations across depth bands; the hard 26-50 band.
- **P5 multifiltration views** -> `MULTIFILTRATION_REPORT.md`
- **P6 independent validation** -> `INDEPENDENT_NAVIGATION_VALIDATION.md`
  metamorphic + expansion completeness + artificial-jump + navigation tasks;
  co-location and held-out prediction secondary only.

## Standing exceptions, stated once

- Generated-owner uses the elaborator's auxiliary-declaration provenance
  (recorded via name prefix of `gen`-flagged declarations). Authority: the
  elaborator, not human naming. This is provenance metadata, not a semantic
  name, and is immutable once created.
- Learned navigators contain fitted parameters — allowed as versioned Layer D
  artifacts over stable Layer A/B features, never in the canonical structure.
