# Handoff — Navigable Connected Citation Graph (Phase 5, current task)

Date 2026-08-20. For an independent agent working this problem in parallel.
Everything here is measured, not assumed. Numbers come from the whole of
Mathlib (dump v7, 771,129 declarations).

---

# PART 1 — THE GOAL (this is the actual specification)

Build a **navigable graph of mathematics** from Lean proof citations, with:

1. **Connectivity at every filter level. No isolated islands, ever, by
   definition.** This is the hard requirement.
2. **A slider that filters edges.** Fully open = every citation. Fully closed
   = a **spanning tree** (still connected, minimal). Every level in between is
   nested: opening the slider only ADDS edges, never removes or relabels.
3. **A per-proof ranking of citations** correlating with how important or
   useful that step is ("keyness").
4. **Plumbing is a continuum, judged relatively.** What is trivial bookkeeping
   in a sophisticated proof may be the entire content of a simple proof. A
   proof that is entirely plumbing is CORRECT and not a failure **if the thing
   it proves is itself plumbing**. The filter must judge an edge against its
   local context, never against a global blacklist.
5. **Stratified purity.** High purity at the top of the tree (deep,
   sophisticated theorems); lower purity is fine at the base, because near the
   base glue genuinely is the content.

## Two approaches to compare

**Approach 1 — massage the existing per-proof ranking** so that it has the
connectivity property: total rank purity at the top of the tree, less purity
lower down, but everything truly connected.

**Approach 2 — start fully connected and remove edges strategically.** Take
the raw depth structure plus only the most defensible filters, i.e. very close
to the full graph, which IS connected. Then remove edges using the depth score
and the structure of the graph itself, so that it stays connected and
navigable while plumbing and glue are stripped out. Graph-theoretic
sparsification is the expected tool.

Same target in both cases.

---

# PART 2 — WHY THE OBVIOUS APPROACH FAILS (measured)

Filtering by "keep the top-k cited declarations per proof, independently per
proof" destroys connectivity. Weak-component structure of the resulting
declaration graph:

| filter | edges kept | components | largest component |
|---|---|---|---|
| everything (P1) | 18.7M | 2 | 100% |
| load-bearing occurrences (P2) | 8.5M | 569 | 99.78% |
| proposition-valued citations (P3) | 2.9M | 1,934 | 98.82% |
| content boundary V8 (P4) | 1.57M | 8,024 | 96.01% |
| top-16 per proof | 1.44M | 8,096 | 95.93% |
| top-4 per proof | 0.99M | 8,884 | 95.25% |
| **top-1 per proof** | **0.46M** | **25,230** | **8.87%** |

Diagnosis: one-out-edge-per-node produces a functional graph whose component
count equals the number of distinct sinks. Independent per-proof truncation
cannot preserve global connectivity — the choice has to be coordinated, or the
backbone has to be constructed globally.

A second measured fact in the same direction: **centrality is not stable
across filter levels — it inverts.** Spearman correlation of bipartite
PageRank between adjacent levels, over the union of each pair's top-1000:

| transition | Spearman | top-1000 overlap |
|---|---|---|
| P1 → P2 | −0.122 | 38.3% |
| P2 → P3 | −0.384 | 24.0% |
| P3 → P4 | +0.208 | 64.7% |
| P4 → top16 | 0.999 | 99.3% |
| top4 → top1 | 0.026 | 48.3% |

The three levels give three disjoint answers to "most central declaration":
`Eq`/`Nat`/`Eq.refl`, then `rfl`/`congrArg`/`propext`, then
`eq_of_heq`/`Or.casesOn`. None is mathematics. **Do not build salience on
citation frequency.**

---

# PART 3 — THE DATA YOU HAVE

Built by `src/build_incidence.py`, schema in `reports/HYPERGRAPH_SCHEMA.md`.
Regenerate from the dump; the arrays are ~134MB and are not in git.

- **546,576 declaration nodes** appearing in at least one proof (771,129 total
  declarations).
- **747,644 proof artifacts.** Each certifies exactly one declaration and
  cites a set. The natural object is a directed hypergraph `C_p ==> T`, one
  hyperedge per proof. **Hyperedges must not be clique-expanded** (ADR-0005).
- **18,721,317 citation incidences**, of which 8,485,349 are load-bearing.
- Essentially a DAG (543 declarations sit in small mutual-recursion cycles).

Per-node signals:
- `depth` — 1 + max depth of what it cites, primitives 0, max 346. Spearman
  ≥ 0.98 with prerequisite-cone size, so it is essentially log(volume of
  prerequisite mathematics). It is a **library-relative coordinate, not
  importance** (ADR-0004).
- `in_degree`, `stated_count` (how many human theorem statements mention it).

Per-incidence signals:
- occurrence roles (8-vector): applied as a step / let-value / explicit arg /
  implicit / instance slot / strict-implicit / type annotation / unresolved.
  Load-bearing = any occurrence in {applied, let-value, explicit, unresolved}.
- `in_stmt_world` — whether the cited declaration is already reachable from
  the certified theorem's own STATEMENT, as opposed to being introduced by the
  proof. 14,207,730 of 18.7M are in-statement-world.
- `d_target`, `d_cite`, `delta_depth`.

Measured depth-gap distribution (how far citations reach):

| projection | mean Δd | p50 | p99 | max |
|---|---|---|---|---|
| full support | 70.2 | 55 | 279 | 346 |
| load-bearing | 61.1 | 44 | 272 | 346 |
| content boundary | 47.7 | 22 | 268 | 341 |

**Long-range citation is the norm.** Any layout assuming proofs cite their
neighbours is modelling the wrong object.

A structural asymmetry worth knowing: **stating** theorems uses a small,
heavily reused vocabulary (104,016 distinct declarations over 5.3M
incidences); **proving** them reaches a large, thin one (487,423 over 3.2M).

---

# PART 4 — WHAT IS FROZEN, AND WHY

An external judge closed the previous phase. Binding constraints:

- **V8 (the current per-proof ranking) is FROZEN.** Do not build V9. Do not
  tune its thresholds. It is available as a derived, labelled view and as a
  source of edge weights, nothing more.
- **Do not promote any single scalar into an ontology of importance.**
- A proof hyperedge is an **observed support set for one checked
  certificate** — not logical necessity, not minimality, not a canonical
  AND-decomposition. Preserve proof-artifact identity so alternative proofs
  stay distinct.
- Definitions, witnesses and constructions stay first-class in the underlying
  object even when a claim-only view hides them.
- Every view must be regenerable from the exact record; nothing is deleted.
- Empty and unsupported cases are reported, never silently dropped from a
  denominator.

For reference, what V8 does (frozen): keep load-bearing occurrences; keep
proposition-valued citations that are not constructors/recursors; demote
"logic-only" citations (every non-universal ingredient is a bare proposition
like True/False); demote "machinery" (citations carrying decision-procedure
vocabulary — concepts used >200 times and >20x more often than they are
stated — unless that vocabulary appears in the target theorem's own
statement); rank the survivors by (not-demoted, proof-introduced, deeper
first).

Known cost of V8, reported honestly: it leaves **21.9% of all theorem proofs
(116,581) with nothing at all to display**, against 12.8% for the
proposition-filter alone. Those same proofs have a median of 6 load-bearing
citations underneath. The evidence exists; the boundary removes it.

---

# PART 5 — THE DESIGN QUESTIONS THAT MATTER

1. **What is the right "fully closed" state?** Maximum-weight spanning tree of
   the undirected projection? Maximum-weight spanning arborescence respecting
   the DAG (Chu-Liu/Edmonds)? Something that respects the hypergraph rather
   than the flattened edge list?
2. **What produces the continuum?** A locally-normalized significance filter
   is the natural fit for requirement 4 — judging each edge against a null
   model local to its own endpoint's weight distribution, so "plumbing" is
   relative. The disparity filter (Serrano, Boguñá, Vespignani 2009) is the
   canonical version; alternatives include the noise-corrected backbone
   (Coscia & Neffke 2017), the Pólya-urn filter (Marcaccioli & Livan 2019),
   LANS, and effective-resistance spectral sparsification. Each must be
   checked for: preserves connectivity, single monotone parameter, locally
   normalized, scales to 18.7M edges.
3. **How is connectivity guaranteed?** The obvious construction is
   `backbone ∪ {edges significant at level t}`, which is connected at every t
   by construction and nested by construction. Does forcing the backbone in
   distort the statistics, and is there a better way (e.g. only ever removing
   edges that are redundant in the cycle space)?
4. **What is the edge weight?** Candidate signals above. Should weight be
   normalized per-proof so each proof distributes one unit of importance among
   its citations, before any global filtering? Watch for pitfalls when node
   degrees vary by three orders of magnitude.
5. **How does stratified purity fall out rather than being imposed?** A
   depth-stratified null model — judging an edge against the distribution of
   edges at comparable depth — is one candidate.
6. **What diagnostics prove the family is good**, beyond connectivity?
   Shortest-path distortion against the full graph, preservation of the depth
   gradient along paths, backbone stability under weight perturbation,
   edge-betweenness of survivors.

## Tension to resolve explicitly

"Connected at every level" and "removes all plumbing" may be in genuine
tension: some glue edges may be the only thing holding a region on. If so,
say so and characterize which edges are load-bearing for connectivity — that
set is itself an interesting object (it would be the mathematics that cannot
be reached except through plumbing).

---

# PART 6 — WHAT IS IN THIS PACKAGE

- `reports/HYPERGRAPH_SCHEMA.md` — nodes, artifacts, incidence relations, the
  eight projections, storage layout.
- `reports/HYPERGRAPH_GEOMETRY_REPORT.md` — all measured geometry and
  persistence results, with the pre-registered questions they answer.
- `PRE_REGISTRATION.md` — the questions, predictions and decision rules, fixed
  before results were seen.
- `decisions/ADR-0005-multiscale-navigation.md` — binding semantics.
- `decisions/ADR-0004-epistemic-layers.md` — kernel vs library-relative vs
  provenance vs semantic; what "future-proof" means here.
- `reports/METHOD.md` — the frozen V8 definition, reproducible from scratch.
- `src/` — the builders: incidence, frozen V8 mask, geometry, persistence.
- `data/*.json` — geometry and persistence results.

To regenerate the arrays: run `src/build_incidence.py` then
`src/build_v8_mask.py` against the dump. Everything else reads those.
