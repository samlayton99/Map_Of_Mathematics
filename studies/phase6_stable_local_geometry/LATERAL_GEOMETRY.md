# Lateral geometry: the traversal round (2026-08-21)

The lead's principle: mathematicians navigate laterally. Going down to
shared foundations and back up (linear algebra -> addition -> number
theory) is expensive; connections at a field's own altitude are the
valuable moves. The round formalized this two ways, falsified one, and
validated the other against held-out mathematical practice.

## Formalization 1: undirected superlevel merge height — FAILS as
a kinship measure

Filter the graph by depth from the top; merge height of a pair = highest
level at which any path connects them. Measured (12k depth-matched
theorem pairs):

- The GAP graph transforms the geometry: median dip below the pair's own
  level 21 -> 1; connections forced through the foundations 40% -> 11%;
  median merge altitude 13 -> 35.
- But same-area vs cross-area AUC is ~0.50: paths through DEEPER nodes
  are free in this filtration, and deep proofs citing both endpoints
  connect everything from above. Also, random pairs within a Mathlib
  area are mostly genuinely unrelated, so random-pair AUC is the wrong
  instrument regardless.

## Formalization 2: V-kinship (downward shared substance) — WORKS

sig(T) = T's GAP move set, two hops down (tiny: median 1, p90 5 moves
per hop). Kinship = sig(A) and sig(B) intersect; V-dip = how far below
min(depth) the deepest shared node sits. This is "what do these two
proofs share, mathematically."

- The move graph is SPARSE: 97.3% of random theorem pairs share nothing
  within two hops — which is what makes it navigable.
- Kinship rate: 4.6% same-area vs 0.9% cross-area (5x).
- When kinship exists: median V-dip 14 (same-area) vs 28 (cross-area).
  Same-field kinship lives near the theorems' own altitude; cross-field
  kinship is forced twice as deep. Both halves of the lateral principle,
  measured.

## The validation: held-out co-use prediction (non-circular)

Hold out 10% of proofs; delete their edges; ask whether the blind map's
kinship predicts which theorem pairs those proofs actually co-cite,
versus depth-matched random pairs. FIXED positive pairs, all three
graphs asked the same question:

| graph | kinship on co-used pairs | on random pairs | lift |
|---|---|---|---|
| flat top-4 | 0.553 | 0.341 | 1.6x |
| ordered top-4 | 0.586 | 0.154 | 3.8x |
| GAP | 0.368 | 0.016 | **23.0x** (36.9x on second seed) |

And the V-dip of actually co-used pairs is **2** vs 22 for random —
real mathematical practice is lateral, exactly as the principle claims.
The flat graph's kinship is near-saturated noise; the constructed map's
kinship is meaning. This is the strongest non-circular validation the
project has: the map forecasts mathematical practice it never saw.

## Lateral bridges (qualitative)

Cross-area kinships at dip <= 5 occur at ~0.09% of cross-area pairs
(rare, as "genius connections" should be). Mined examples
(data/lateral_bridges.json): Algebra<->Geometry via `Module.finrank`;
Probability<->MeasureTheory via `MeasureTheory.integral`;
Data<->RingTheory via `Fintype.equivFin`; GroupTheory<->LinearAlgebra
via `Nat.card`. No `Eq.mpr`, no `HAdd.hAdd`, no definition-of-addition
routing anywhere in the list.

## The traversal signal (deliverable)

`data/traversal_geometry.npz`: per GAP edge (src, dst, span) and per
node (depth, lane 0 math / 1 transport / 2 generated, area id).
Span quantiles 1/4/17/67 (q25/50/75/95). A traversal agent gets the
vertical-cost geometry as input without us fixing an exchange rate:
cost of a step = any monotone function of its span; cost of a route =
its dip profile. No fitted weights anywhere (principles 2 and 14).

## Cautious interpretations

- The two geometries answer different questions: V-kinship = "share
  substance" (association); the failed undirected merge = allows "used
  together by something deeper" (co-use from above). A traversal cost
  combining both is future work, not settled here.
- Kinship measured at radius 2 only; radius sensitivity untested.
- Area labels are coarse validation-only human organization.
- Co-use positives are pairs of GAP-included citations of held-out
  proofs; the fixed-pair control removes the definitional asymmetry
  between graphs, but a fully construction-independent pair source
  (e.g. textbook co-occurrence) remains desirable.
- The graded corpus contributed nothing here — this round is free of
  the brief-contamination caveat.
