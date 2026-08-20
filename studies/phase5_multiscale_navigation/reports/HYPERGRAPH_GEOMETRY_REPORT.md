# Hypergraph Geometry Report — Phase 5, first results

Built 2026-08-20 from dump v7 (771,129 declarations). Questions and
projections were fixed in `PRE_REGISTRATION.md` before any of this was seen.

**Scale.** 747,644 proof artifacts, **18,721,317 incidences**, of which
8,485,349 are load-bearing and 14,207,730 lie inside the certified theorem's
own statement world.

## Q1.1 — Geometry across projections

| projection | incidences | hyperedges | empty | distinct decls | size p50 / p90 / p99 / max |
|---|---|---|---|---|---|
| P1 full support | 18,721,317 | 747,605 | 39 | 546,576 | 16 / 55 / 142 / 699 |
| P2 load-bearing | 8,485,349 | 728,753 | 18,891 | 502,906 | 6 / 28 / 72 / 401 |
| P3 claims | 2,924,084 | 519,600 | 228,044 | 360,595 | 2 / 13 / 41 / 231 |
| P4 V8 boundary | 1,573,630 | 462,505 | 285,139 | 347,492 | 2 / 7 / 25 / 176 |
| P5 proof-introduced | 3,163,125 | 621,200 | 126,444 | 487,423 | 2 / 11 / 43 / 193 |
| P6 statement-world | 5,322,224 | 597,702 | 149,942 | **104,016** | 5 / 21 / 54 / 279 |
| P8 definition layer | 1,641,088 | 200,886 | 546,758 | 201,796 | 5 / 18 / 51 / 197 |

The filtration is steep: **P4 retains 8.4% of the evidence P1 carries.**

### The finding worth keeping from this table

Compare P5 and P6. Proving theorems reaches **487,423 distinct declarations**
across 3.2M incidences. Stating them uses **104,016** across 5.3M incidences.
Statement vocabulary is small and reused constantly; proof vocabulary is large
and used thinly. That asymmetry is a fact about the shape of mathematics as
recorded, not about any filter, and it is the first structural result this
program has produced that is about mathematics rather than about our pipeline.

The **definition layer** (P8) carries 1.64M incidences over 200,886
construction artifacts. Under every citation view shipped before this phase it
was invisible.

### Top-k over the frozen P4 order

| k | incidences | mean edge size |
|---|---|---|
| 1 | 462,505 | 1.00 |
| 2 | 709,619 | 1.53 |
| 4 | 991,923 | 2.14 |
| 8 | 1,253,430 | 2.71 |
| 16 | 1,437,530 | 3.11 |

Mean size saturates well below k, confirming that top-k and the content
boundary answer different questions: past k=8 the cut stops binding for most
theorems while still truncating the citation-rich ones.

## Q1.3 — Landmarks that exist only in glue-rich views

**All 100** of the top-100 declarations by raw citation count vanish from the
P4 ranking (every one falls below rank 1000; most to exactly zero citations):
`Eq` (301,634 raw citations), `OfNat.ofNat`, `Nat`, `congrArg`, `Eq.refl`,
`id`, `Membership.mem`, `Eq.trans`, `instOfNatNat`, `DFunLike.coe`, `Set`,
`Eq.mpr`, `Eq.symm`, `True`, `LE.le`, `of_eq_true`, `HAdd.hAdd`, `propext`.

A citation-count map built on raw support would be a map of Lean's plumbing.
That is the clearest evidence so far that *some* content boundary is
necessary for navigation, independent of whether V8's is the right one.

What survives into P4's top 20, reported honestly as three kinds:

- **real mathematical identities** — `CategoryTheory.Category.comp_id` (5,977),
  `Category.id_comp`, `mul_one`, `add_zero`, `zero_add`, `one_mul`,
  `le_of_le_of_eq`, `Int.add_one_le_of_lt`;
- **decision-procedure bridge lemmas** — `Lean.Omega.Int.sub_congr` (4,725),
  `Int.add_congr`, `Int.ofNat_lt_of_lt`, `Int.sub_nonneg_of_le`;
- **kernel plumbing that survived the boundary** — `eq_of_heq` (13,119, the
  single most-cited P4 declaration), `heq_of_eq`, `Or.casesOn`,
  `of_decide_eq_true`, `noConfusion_of_Nat`, `ite_congr`.

Roughly half the persistent landmark set is not mathematics. `eq_of_heq`
topping the content view is a standing indictment of using citation frequency
as importance, and it is exactly why ADR-0005 forbids promoting any single
scalar into an ontology of importance.

## Q2.1 — Citation depth gaps

| projection | mean Δd | p1 | p50 | p99 | max |
|---|---|---|---|---|---|
| P1 full support | 70.20 | 1 | 55 | 279 | 346 |
| P2 load-bearing | 61.10 | 1 | 44 | 272 | 346 |
| P4 V8 boundary | 47.68 | 1 | 22 | 268 | 341 |
| P5 proof-introduced | 39.42 | 1 | 23 | 184 | 343 |

**Long-distance citation is the norm, not the exception.** Under the content
view the median citation still crosses 22 levels of library depth, and the top
percentile crosses 268. Any navigation interface that assumes a proof cites
its neighbours is modelling the wrong object.

Filtering shortens the median jump (55 → 22) far more than it shortens the
extreme (279 → 268): glue is mostly local, and the genuinely long jumps are
made by content citations.

## Q2.2 — Unusually large depth span

p99 span = **242 levels**; 4,663 artifacts at or above it. The largest:
`CompletelyPositiveMap.mk.inj` (341), `CompletelyPositiveMap.instFunLike._proof_1`
(340), `CStarMatrix.instCStarAlgebra._proof_{3..8}` (337),
`NumberField.Ideal.tendsto_norm_le_div_atTop` (337).

Note what these are: the extreme-span artifacts are dominated by **instance
and structure-construction obligations**, not by human theorem proofs. This
corroborates the Phase 3 finding that typeclass instances are deep, and it
means the "longest routes on the map" are mostly assembly of algebraic
structure rather than mathematical argument. A navigation demonstrator that
sorts by span without saying so would surface plumbing at the top.

## Q3.1 — Direct vs filtered citation counts (theorem artifacts only)

| projection | mean | p50 | p90 | theorems with NOTHING |
|---|---|---|---|---|
| P1 full support | 28.54 | 18 | 62 | 0 (0.0%) |
| P2 load-bearing | 12.83 | 6 | 31 | 5,445 (1.0%) |
| P3 claims | 5.25 | 2 | 13 | 68,219 (12.8%) |
| P4 V8 boundary | 2.75 | 1 | 7 | **116,581 (21.9%)** |

This is the gate number, reported first and not buried. **The frozen V8
boundary leaves 21.9% of all theorem proofs in Mathlib with nothing to
display** — nearly double the claims filter alone, and far above the 12.8%
figure previously quoted from a 2,400-theorem sample. Under P2 the same
proofs have a median of 6 load-bearing citations, so the evidence exists in
the record; the content boundary is what removes it.

Whether those 116,581 proofs are genuinely contentless or merely
inexpressible in a citation view is exactly registered question Q5.2, and the
local typed-move layer is the instrument that will answer it.

## Q1.2 / Q4 — Persistence, and the registered prediction

Centrality is bipartite PageRank on the incidence structure — a random walk
declaration → artifact → certified declaration. No clique expansion anywhere
(ADR-0005). Spearman is computed over the union of each pair's top-1000.

| transition | Spearman | top-1000 overlap |
|---|---|---|
| P1 → P2 | **−0.122** | 38.3% |
| P2 → P3 | **−0.384** | 24.0% |
| P3 → P4 | +0.208 | 64.7% |
| P4 → top16 | 0.999 | 99.3% |
| top16 → top4 | 0.924 | 92.7% |
| top4 → top1 | **0.026** | 48.3% |

**Registered prediction: CONFIRMED.** P3→P4 (+0.208) is more stable than
P2→P3 (−0.384), so the V8 content boundary does less violence to the geometry
than the claims filter does.

**But the result that matters is the absolute scale, and it is bad.**
Centrality rankings do not merely shift between evidence tiers — they
*invert*. A negative Spearman between P1→P2 and P2→P3 means the most central
declarations under one tier are systematically not central under the next.
Under this report's own pre-registered persistence rule — a structure counts
as persistent only if it survives P2 through P4 and every top-k with k ≥ 4 —
**centrality-derived landmarks fail the test and must not be offered as map
geometry.** They are projection artifacts. This corroborates Q1.3 from a
second direction: there is no single citation-frequency notion of importance
that survives changing how much evidence you admit.

The PageRank leaders make the point concretely: P1 leads with `Eq`, `Nat`,
`Eq.refl`; P3 with `rfl`, `congrArg`, `propext`; P4 with `eq_of_heq`,
`Or.casesOn`, `noConfusion_of_Nat`. Three different tiers, three disjoint
notions of "most important declaration in mathematics", none of them
mathematics.

### Component structure across the filtration

| projection | touched nodes | components | giant fraction |
|---|---|---|---|
| P1 full support | 771,054 | 2 | 100.00% |
| P2 load-bearing | 763,027 | 569 | 99.78% |
| P3 claims | 548,509 | 1,934 | 98.82% |
| P4 V8 boundary | 514,560 | 8,024 | 96.01% |
| top16 | 513,709 | 8,096 | 95.93% |
| top4 | 506,445 | 8,884 | 95.25% |
| **top1** | 487,735 | **25,230** | **8.87%** |

At full support the record is a single connected object. Content filtering
fragments it gently — P4 still holds 96% of touched nodes in one component.
**Top-1 destroys it**: 25,230 components and no giant component at all, just
shards averaging 19 nodes.

This is the sharpest strike yet against the program's previous direction. The
rank-1 metric that nine certification rounds optimized produces, when taken as
a map, a disconnected rubble field. Navigability appears somewhere between
k=4 and k=16, and the connectivity that makes the object a *map* lives in
evidence the rank-1 view discards. The judge's instruction to stop optimizing
rank 1 is confirmed by measurement, not merely by argument.

## Status against the pre-registered questions

Answered: Q1.1, Q1.2, Q1.3, Q2.1, Q2.2, Q3.1, and Q4 for centrality and
components.
Not yet started: Q2.3 (repeat bridges), Q2.4 (route expansion behind large
jumps), Q3.2/Q3.3 (compression), and all of Q5 (local typed-move layer).

No decision rule is invoked yet — rules 1 through 5 require the navigation
tasks and the local move layer. But two findings already constrain the
outcome: citation-frequency centrality is not persistent and cannot serve as
map salience, and top-1 is not a connected map.
