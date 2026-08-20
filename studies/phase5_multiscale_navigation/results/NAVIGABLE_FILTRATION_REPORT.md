# Navigable Filtration — first working construction

2026-08-20. Answers the owner's specification: connected at every level, a
slider from everything down to a backbone, plumbing judged relatively, purity
stratified by depth. Design follows an independent graph-theory consult.

## Why independent per-proof truncation cannot work (arithmetic, not tuning)

Top-1 per proof touches 487,735 declarations with 462,505 edges. A one-parent
structure is a forest, so components = nodes − edges = **25,230**, which is
exactly the measured component count. Top-1 is a spanning forest **25,229
edges short of a spanning tree**. No re-ranking fixes this; the deficit is a
counting fact. Connectivity has to be supplied by construction.

## The construction

**Backbone — maximum-weight anti-arborescence, plus a virtual root.**
Every citation points strictly downward in depth, so a per-node argmax over
its citations can never form a cycle: greedy per-node selection is provably
optimal and Chu-Liu/Edmonds is vacuous here. Each proof keeps its
highest-weight citation (728,753 edges). Every sink is then grounded at a
**virtual root** representing the ambient logical framework — without this the
structure is a forest of trees rooted at sinks and is never connected.

**Weight — depth first, then measured commonness.**

    w  =  m_role · m_stmt · m_depth · idf(cited)

- `m_depth` is driven by the **absolute depth of the cited declaration**. This
  is the program's validated keyness signal: the depth key was the largest
  single contributor in the V8 ablation (+3.45 points). A mild secondary term
  favours citations nearly as deep as their target (the last big step rather
  than a descent into foundations). The raw depth **gap** is deliberately
  unused — measured median 22 and p99 268 means it barely discriminates.
- `idf(c) = log(N_proofs / #proofs citing c)` carries "globally common implies
  probably plumbing" as a measured quantity, naming nothing.
- `m_role` favours citations applied as proof steps over argument positions;
  `m_stmt` favours citations the proof introduces over those already implied
  by the statement.

**Filter — configuration-null score, both endpoints.** The disparity filter is
locally normalised, which matches "plumbing is relative", but it is one-sided:
it cannot see that a lemma is cited 200,000 times library-wide, and global
commonness is our central plumbing signal. A configuration null conditions on
both endpoint strengths, so a hub lemma's edges must be exceptional to
survive.

**Nesting — structural, not tested.** One score per edge, computed once on the
full graph, never recomputed on a filtered graph. Edges are sorted once and
stored as a rank array; every slider level is a **prefix of that array**, and
backbone edges hold rank 0. Nesting and connectivity are therefore properties
the implementation cannot violate.

## Result

| level | edges | components (with root) | giant | components (mathematics only) | giant |
|---|---|---|---|---|---|
| backbone only | 728,753 | 64 | 99.98% | 34,337 | 6.44% |
| top 10% by score | 848,534 | 25 | 99.99% | 22,471 | 88.08% |
| top 25% | 2,121,337 | **1** | 100% | 1,716 | 98.90% |
| top 50% | 4,242,674 | **1** | 100% | 895 | 99.66% |
| top 75% | 6,364,011 | **1** | 100% | 598 | 99.77% |
| everything | 8,485,349 | **1** | 100% | 569 | 99.78% |

Nesting verified monotone. The 64 residual components at the closed end are
the mutual-recursion cycles (543 declarations), whose chains never reach a
sink to be grounded; grounding cycle participants would remove them.

**The honest reading of two columns.** With the virtual root the family is
literally connected everywhere, which is the specification. Without it —
counting only connectivity earned through mathematics — even the *full* graph
has 569 components. Total connectivity through mathematics alone does not
exist at any level, so the virtual root is not a trick to rescue the closed
end; it is required at every level, including the open one.

**The navigable regime is around the top 25%** (2.1M edges): mathematics-only
connectivity reaches 98.9% and literal connectivity is exactly 1.

## Does the backbone distort the statistics?

**No: 91.0% of backbone edges would pass the top-25% filter on their own
merits.** The consult predicted above 80% for an arborescence backbone (and
poor overlap for a spanning-tree backbone, whose edges are chosen globally and
are locally meaningless). Forcing the backbone in costs almost nothing.

## Stratified purity — the owner's requirement, and it emerged rather than being imposed

Fraction of backbone edges whose cited endpoint is content (a claim that is
not logic-only), by depth of the citing theorem:

| depth band | backbone edges | cited is content |
|---|---|---|
| 0–10 | 130,039 | 27.7% |
| 10–25 | 148,294 | 54.9% |
| 25–50 | 129,184 | 50.9% |
| 50–75 | 103,109 | **75.2%** |
| 75–125 | 132,525 | 66.7% |
| 125–350 | 85,602 | **70.2%** |

Glue dominates the base, content dominates the upper tree. Nothing imposed
this; it falls out of the weights. Independently, rank-1 content purity of the
frozen ranking rises the same way: 48.9% at depth 0–10 to 78.6% at 125+.

## Definitions are back in the structure

The base graph applies no proposition filter, so constructions are first-class
again — the layer every citation view before this phase hid completely.

- **57.2%** of all edges cite a definition, inductive type, or construction.
- **34.7%** of backbone edges land on one.
- **140,008 distinct definitions** are present as nodes.

## Disclosed weaknesses

1. **The configuration null is not calibrated.** Median z is 9.1 and the
   maximum is 3,237: on a graph this sparse the null expectation is tiny, so
   nearly every edge is nominally "significant". The score is therefore used
   as a **ranking**, cut by percentile, not as a hypothesis test. Calling a
   level "the significant edges" would be overselling; it is "the top x% by
   score". A Pólya-urn null would be better calibrated for heavy tails.
2. **Free stratification is weaker than hoped.** The consult's mechanism-1
   requires deeper theorems to have larger proofs; measured
   Spearman(depth, citation count) = **0.351** — positive but only moderate.
   The purity gradient above is therefore partly carried by the weights
   themselves rather than by the null's degree dependence. A depth-stratified
   null is the stronger route and has not been built.
3. **Deletion cannot remove plumbing from a connected graph.** Connecting
   546,576 nodes needs at least 546,575 edges regardless of significance, and
   the owner's own rule keeps an all-plumbing proof's backbone edge forever.
   This is a counting fact. The resolution is a second dial —
   **node contraction**, collapsing a retained subtree below a depth threshold
   into its root, which preserves connectivity by construction (a quotient of
   a connected graph is connected) while genuinely removing plumbing from
   view. Not yet built.

## Not yet done

The diagnostics that would show the family is *good* rather than merely
connected: shortest-path stretch against the full graph, depth-gradient
preservation along retained routes, backbone stability under weight
perturbation with the argmax margin per node, and a held-out test of whether
the score predicts the citations of proofs it never saw. That last one is the
only diagnostic that tests keyness rather than topology.
