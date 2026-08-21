# 05 — Applied Experiment Program

## Phase 0 — Correct the substrate before more ranking work

Required:

1. Replace cycle depth relaxation with exact SCC condensation and DAG depth.
2. Separate:
   - direct type/interface dependencies;
   - transparent definition expansion;
   - theorem proof/certificate dependencies.
3. Rebuild `statement-world` so it never silently traverses another theorem’s proof body.
4. Persist stable declaration/artifact/occurrence identifiers, not array positions.
5. Recover expression paths and application-parent relations.
6. Extract or reconstruct generated-owner/provenance relations.
7. Preserve every occurrence role, not only the strongest or most frequent.
8. Audit the 552-proof grading briefs:
   - exactly what theorem/proof context was visible;
   - whether depth/role/system cues were shown;
   - which conclusions remain valid.

Deliverable: `SUBSTRATE_CORRECTIONS.md`.

## Phase 1 — Local hierarchy pilot

### Sample

Use 48 proofs:

- 8 per target-depth band;
- at least 12 definition/construction heavy;
- at least 12 generated/private/instance heavy;
- at least 12 with local hypotheses/witnesses/cases;
- at least 12 long proofs.

### Build four views

1. flat current candidate list;
2. generated-owner collapse only;
3. named-application/term hierarchy;
4. hierarchy plus typed lanes.

### Required metrics

- visible useful/core recall at budgets 1, 2, 4, 8;
- artificial-jump rate;
- generated/private exposure;
- exact expansion completeness;
- number of vertical versus lateral edges;
- rater explanation quality;
- click/expansion count.

Do not fit new weights.

## Phase 2 — Metamorphic benchmark

Build the formal proof pairs in `06_METAMORPHIC_VALIDATION.md`.

Compare exact records and high-level views.

Primary criterion:

> The exact certificate may change; the high-level navigational skeleton should remain equivalent under declared harmless transformations.

## Phase 3 — Stable local ordering

Freeze candidates:

### Baselines

- depth only;
- proof-introduced then depth;
- append-safe role × raw depth;
- current live-rarity composite as a noncompliant upper bound.

### Principled candidates

- stable Copeland/Condorcet-first;
- normalized dominance count;
- hierarchy order with ordinal sibling ranking;
- hierarchy plus one local magnitude from H6.

Every candidate must publish:

- exact signals;
- append-safety proof;
- tie semantics;
- global score resolution;
- failure cases.

Use existing grades for development. Grade a fresh sample only after the hierarchy and candidate formulas are frozen.

## Phase 4 — Edge-scale and self-similarity study

For every edge compute:

\[
d_T,\quad d_c,\quad \Delta d,\quad
\frac{\Delta d}{1+d_T},\quad
\frac{d_c}{1+d_T},\quad
\operatorname{rank}_{p}(\Delta d).
\]

Across depth bands and at least two Mathlib snapshots:

- compare distributions;
- compare usefulness calibration;
- compare role composition;
- compute Wasserstein/KS distances;
- test whether one normalization yields approximate data collapse;
- inspect the persistent hard band around depth 26–50.

If no representation is stable, retain explicit depth regimes.

Do not manufacture self-similarity.

## Phase 5 — Global multifiltration

Build views over:

- local hierarchy level/salience;
- abstraction span;
- relation lane.

At minimum expose:

- high-level proof moves;
- concepts/definitions;
- same-scale neighbours;
- vertical drill-down;
- long-range bridge candidates;
- exact full support.

Analyze component and hub persistence across the parameter lattice.

Do not use one junk mask as the primary validator.

## Phase 6 — Independent map validation

### Cheap standing checks

- append invariance on fresh sublibraries;
- metamorphic invariance;
- exact expansion;
- held-out citation prediction;
- module co-location sensitivity;
- graph statistics on fresh samples.

### Expensive checks

- 100–200 pairwise relatedness judgments;
- 24 navigation tasks;
- owner review of 12 discriminating cases.

### Navigation tasks

1. find the main theorem/definition used;
2. distinguish a vertical foundational dependency from a lateral neighbour;
3. find another proof with the same high-level move;
4. trace toward foundations;
5. identify a long-range mathematical bridge;
6. compare two proofs;
7. recover hidden exact machinery;
8. navigate a selected depth band.

## Decision rules

### Promote hierarchy if

- artificial jumps fall materially;
- refactoring invariance rises;
- core/major recall is non-inferior;
- exact expansion remains complete.

### Promote `delta_depth` as a map axis if

- it is stable and useful for vertical/lateral rendering.

Never promote it as “universality” without independent evidence.

### Keep dynamic rarity if

- it adds current navigation value after hierarchy restoration.

Keep it as a versioned field, not a canonical local edge.

### Stop local ranking research if

- hierarchy plus a simple stable policy lies within practical equivalence of the best dynamic score.

Move effort to local typed moves, state-conditioned navigation, and actual tasks.
