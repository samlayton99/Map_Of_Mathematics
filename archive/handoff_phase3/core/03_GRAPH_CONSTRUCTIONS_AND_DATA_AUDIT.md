# 03 — Graph Constructions and Data Audit

## 1. Primary library graph

Construct a directed, typed, weighted declaration graph from raw exact occurrence evidence, preferably P1.

Use the orientation:

\[
u\to v
\]

when declaration `u` refers to declaration `v` in its type, definition body, or proof certificate.

Preserve, at minimum:

- unique versus repeated occurrences;
- type/statement versus body/certificate occurrence;
- declaration kind when available, but keep it out of the strict topology-only feature set;
- occurrence path or depth where already stored;
- source declaration and referenced declaration identity;
- whether the referenced declaration is fully stored or shallow/boundary-only.

Call this graph `G_decl_raw` or the repository’s equivalent.

## 2. Required graph variants

### Strict untyped declaration graph

Collapse edge types but preserve direction and optional multiplicity.

This answers the strongest “topology alone” question.

### Typed declaration graph

Retain exact relation categories such as statement/type occurrence versus definition/proof-body occurrence.

This tests whether formal relational structure adds signal without names or natural-language semantics.

### P2 simple-support ablation

Use the deduplicated support graph as a lower-information comparison.

### P0-derived theorem-local graph

For individual proof landmark analysis, use the exact proof-term graph or a faithful local projection that preserves:

- application heads and arguments;
- nesting/depth;
- local hypotheses when available;
- term-construction branching;
- named declaration occurrences;
- relation to the theorem root.

P4/P5 may be joined as additional exact or observed views, but they must not replace P0 as the evidence source.

## 3. Do not use P3 as the primary graph

P3 already encodes the classification being tested. It may supply labels and baseline filters, but no P3 classification or filtered topology may enter feature construction for Question A.

## 4. Coverage and boundary audit before modeling

The Phase 2 corpus contains fully stored declarations and shallow referenced declarations. This can create false structural signatures—for example, imported nodes may have many observed incoming uses but missing outgoing dependencies.

Before fitting models, report:

- node and edge counts for each graph variant;
- number of fully stored versus shallow nodes;
- P3 class prevalence within each coverage stratum;
- in/out degree distributions by coverage stratum;
- connected components and strongly connected components;
- whether the expected declaration dependency graph is acyclic, and any exceptions;
- how much centrality changes when shallow nodes are included or excluded;
- how many targets have enough observed structure for fair comparison.

## 5. Primary and sensitivity populations

Use at least two analyses:

1. **Coverage-controlled primary analysis:** nodes with comparable observed structure, normally fully stored declarations or another defensible matched population.
2. **All-backing-node sensitivity analysis:** all available declarations, with explicit boundary caveats and stratification.

Do not let a `body_available`, imported, file, or shallow-status feature drive the strict topology result.

If the boundary audit shows that global graph measures are uninterpretable on the existing extraction, perform only the minimum additional expansion needed to make the test valid. Document and justify it; do not automatically scale to all of Mathlib.

## 6. Reproducibility

- Fix random seeds.
- Record graph construction parameters and software versions.
- Serialize graph summaries and feature matrices deterministically where feasible.
- Add invariance tests showing that renaming declaration identifiers does not change topology-only features.
- Confirm that raw Phase 2 artifacts are not modified.
