# Phase 5 Pre-Registration — questions fixed before any results are seen

Written 2026-08-20, **before** the incidence structure was built. The judge's
handoff requires the questions and the projection family to be registered in
advance; this document is that registration. Nothing below may be edited after
results are examined. Corrections go in a dated addendum with the reason.

The projection family P1-P8 and the four navigation controls are fixed in
`reports/HYPERGRAPH_SCHEMA.md` and are part of this registration by reference.

---

## Q1 — Geometry across projections

**Q1.1** How do node count, hyperedge count, and hyperedge-size distribution
change from P1 (full support) through P2, P3, P4, and each top-k cut?
*Reported as: a table plus the size distribution's median, p90, p99, max.*

**Q1.2** Which weak components, communities, central declarations, and
cross-domain bridges persist as resolution changes?
*Persistence statistic declared in advance:* for centrality, Spearman
correlation of the top-1000 ranking between adjacent projections; for
communities, adjusted Rand index between partitions; for components, the count
of births and merges as evidence is added.

**Q1.3** Which apparent landmarks exist **only** in glue-rich views?
*Operationalized:* declarations in the top-100 by centrality under P1/P2 that
fall below rank 1000 under P4.

**Prediction registered:** centrality ranking will be substantially more stable
between P3 and P4 (both claim-level) than between P2 and P3 (crossing the
Prop boundary). If instead P2->P3 is the stable transition and P3->P4 is not,
the V8 content boundary is doing more violence to the geometry than the claims
filter, and that is evidence against keeping P4 as the default view.

---

## Q2 — Depth and long-distance structure

**Q2.1** What is the distribution of citation depth gaps `Δd` under each
projection?

**Q2.2** Which proofs have unusually large depth span, and which have
unusually broad cross-community reach? Are they the same proofs?
*Registered threshold:* "unusually large" = span above the 99th percentile.

**Q2.3** Which declarations or artifacts repeatedly bridge distant depth bands
or mathematical domains?

**Q2.4** Does opening a theorem boundary expose intelligible intermediate
routes behind a large depth jump?
*Operationalized:* for the largest-`Δd` incidences, does one level of
expansion produce intermediate declarations whose depths fall strictly inside
the gap? Report the fraction where it does, and the median number of
intermediate steps recovered.

**Prediction registered:** the 50-75 depth band will be dominated by analysis
and algebra rather than foundations, and the portal mode will be necessary —
the induced band will show a component count at least 2x the portal mode's,
because the band is knit together through declarations outside it.

---

## Q3 — Abstraction and compression

**Q3.1** For each theorem, compare direct citation count, filtered citation
count (P4), and recursively expanded support size.

**Q3.2** Which named theorem boundaries compress the largest underlying region
into the smallest reusable interface?
*Operationalized:* compression ratio = |recursive support| / |direct citations|,
reported with both endpoints so a large ratio driven by a single deep chain is
distinguishable from one driven by genuine breadth.

**Q3.3** Does the variable-size content boundary (P4) preserve this abstraction
structure better than a fixed top-k cut (P7)?
*Operationalized:* correlation between a theorem's compression ratio and its
retained citation count under each; a fixed k destroys the signal by
construction if proof complexity varies, so the question is how much.

---

## Q4 — Persistence, stated as the phase's central test

**Q4.1** Do the structures identified in Q1-Q3 persist across the declared
projection range, or are they artifacts of one cut?

**Decision rule, registered:** a structure is called *persistent* if it
survives every projection from P2 through P4 and every top-k with k >= 4. A
structure appearing only under a single projection is reported as
projection-specific and explicitly not offered as map geometry.

---

## Q5 — Local typed-move expansion (24-30 selected proofs)

**Q5.1** For proofs deliberately selected to include local hypotheses,
witnesses, case splits, induction, definition unfolding, rewriting/transport,
representation changes, tactic-heavy certificates, definitional proofs, and
**current V8 empty-output cases**: what fraction of the human-visible argument
can be represented as exact typed moves?

**Q5.2** For the V8 empty-output cases specifically — 12.8% of the library
produces no output today — does the local move layer explain the proof where
the citation layer had nothing to say?
*This is the registered test of whether the empty bucket is a representational
gap or a genuine absence of content.*

**Q5.3** Under conservative cross-proof aggregation (same global interface,
same typed role, differing substitutions), how often does the "same move"
recur across the pilot set?

---

## Decision rules (one must be selected at phase end)

1. **Global hypergraph succeeds as a map projection** — structures and routes
   persist across reasonable slices and navigation tasks improve. Scale it.
2. **Succeeds mainly as an index** — useful for browsing citations and depth,
   no robust deeper geometry. Preserve without overclaiming; prioritize local
   moves and semantic overlays.
3. **Local expansion carries most of the value** — prioritize exact typed move
   extraction and cross-proof aggregation; keep the hypergraph as entry layer.
4. **Current ranking adds little** — if P2 or P3 perform as well as P4 for
   navigation, freeze V8 for historical comparison and simplify the default.
5. **Depth is useful only as a filter** — if depth bands do not form coherent
   navigational layers, retain depth as a coordinate and stop interpreting it
   as structural hierarchy.

## Gates

**Formal faithfulness.** Every incidence traces to an exact declaration
occurrence, artifact, role and path. Every projection regenerates from the
backing record. Empty and unsupported cases are reported, never silently
dropped from a denominator — the specific failure this program committed in
Trial 3 and must not repeat. Alternative proofs stay distinguishable.

**Map geometry.** Structures must be robust across projections. If communities,
bridges or central nodes collapse under small changes, the honest finding is
that the hypergraph is a useful index and not evidence of deep global geometry.

**Navigation.** 10-12 concrete tasks, answered against at least: raw support,
exact load-bearing, frozen V8 boundary, fixed top-k, and hypergraph plus local
expansion. Reviewers answer task-specific questions, not aesthetic ratings.

## What this phase will not do

No V9. No apparatus tuning. No calling a support hyperedge a necessary AND-set.
No erasing theorem boundaries for single-user theorems. No Prop-only view that
removes definitions or witnesses from the underlying object. No single scalar
as the ontology of importance. No model-judged semantic merging in the verified
layer. No production interface before the navigation questions are answered.
