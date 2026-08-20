# Phase 5 Results — connected filtration, first working construction

2026-08-20. This supersedes the earlier task handoff: the construction now
exists and is measured. Read `NAVIGABLE_FILTRATION_REPORT.md` first, then
`DESIGN_CONSULT.md` for why it is built this way.

## The headline

A nested family of graphs over the whole of Mathlib, connected at every
level, with a slider from the full citation record down to a backbone.

| level | edges | components (with root) | giant | components (mathematics only) | giant |
|---|---|---|---|---|---|
| backbone only | 728,753 | 64 | 99.98% | 34,337 | 6.44% |
| top 10% | 848,534 | 25 | 99.99% | 22,471 | 88.08% |
| **top 25%** | 2,121,337 | **1** | 100% | 1,716 | 98.90% |
| top 50% | 4,242,674 | **1** | 100% | 895 | 99.66% |
| everything | 8,485,349 | **1** | 100% | 569 | 99.78% |

Nesting is monotone. Nesting and connectivity are structural properties of
the implementation, not tested ones: one score per edge computed once on the
full graph, sorted once, stored as a rank array, so every level is a prefix
of that array and backbone edges hold rank 0.

## The result that killed the previous approach

Top-1 per proof touches 487,735 declarations with 462,505 edges. A
one-parent-per-node structure is a forest, so components = nodes − edges =
25,230 — exactly the measured count. **Top-1 is a spanning forest 25,229
edges short of a spanning tree.** No amount of re-ranking makes it connected.
This is why connectivity is now supplied by construction rather than hoped
for, and why nine rounds of rank-1 optimisation could not have produced a
navigable map.

## What is in here

- `NAVIGABLE_FILTRATION_REPORT.md` — the construction, the numbers, and three
  disclosed weaknesses.
- `HYPERGRAPH_GEOMETRY_REPORT.md` — the full geometry and persistence study
  across eight projections, against pre-registered questions.
- `DESIGN_CONSULT.md` — the independent graph-theory consultation that drove
  the design, including the proof that the owner's specification is
  impossible in one dial and what the second dial must be.
- `PRE_REGISTRATION.md` — questions, predictions and decision rules, fixed
  before results were seen.
- `ADR-0005-multiscale-navigation.md` — binding semantics for the hypergraph.
- `ADR-0004-epistemic-layers.md` — kernel vs library-relative vs provenance.
- `HYPERGRAPH_SCHEMA.md`, `METHOD.md` — the record's schema, and the frozen
  V8 ranking used only as a source of weights.
- `src/` — every builder. Run order: `build_incidence.py`,
  `build_v8_mask.py`, then `backbone.py`. `geometry.py`, `persistence.py`,
  `stratified_purity.py` are analyses.
- `data/*.json` — all measured results, including
  `filtration_sample.json`, which contains readable samples of the actual
  output (backbone edges by depth band, highest and lowest scoring edges)
  so quality can be judged without regenerating anything.

The large arrays (`incid.npz` 96MB, `filtration.npz` 97MB, `names.json` 36MB)
are excluded. Regenerate from the Mathlib dump with the builders in `src/`.

## Open work, in priority order

1. **The second dial: node contraction.** Edge deletion provably cannot
   remove plumbing from a connected graph — connecting 546,576 nodes needs at
   least 546,575 edges regardless of significance. Contraction (collapse a
   retained subtree below a depth threshold into its root) preserves
   connectivity by construction because a quotient of a connected graph is
   connected, and it composes with the nested edge family. This is the piece
   that actually delivers "remove the plumbing".
2. **Diagnostics that test goodness rather than connectivity**: shortest-path
   stretch against the full graph, depth-gradient preservation along retained
   routes, backbone stability under weight perturbation (with the argmax
   margin per node as a confidence flag), and a held-out test of whether the
   score predicts the citations of proofs it never saw. The last is the only
   one that tests keyness rather than topology.
3. **A better-calibrated null.** The configuration null is not calibrated on
   a graph this sparse (median z 9.1, max 3,237), so the score is currently a
   ranking cut by percentile, not a test. A Pólya-urn null handles heavy
   tails properly.
4. **Depth-stratified null.** Free stratification is weaker than hoped:
   Spearman(depth, citation count) = 0.351, only moderate. Stratify the null
   by depth band, then apply one global threshold, and report the
   survival-versus-depth curve as a finding rather than an input.

## Constraints that still bind

V8 is frozen — it supplies weights, nothing more; do not build V9 or retune
apparatus thresholds. A proof hyperedge is an observed support set for one
checked certificate, never a claim of logical necessity or minimality. Do not
clique-expand hyperedges. Definitions, witnesses and constructions stay
first-class. Every view must regenerate from the exact record, and empty or
unsupported cases are reported, never dropped from a denominator.
