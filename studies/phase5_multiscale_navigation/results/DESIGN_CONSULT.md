# Design Consultation — graph sparsification for a connected citation map

An independent graph-theory consultation was run on the construction problem.
Its recommendations are recorded here because they drove the implementation
and because the reasoning matters more than the conclusions. Condensed from
the full response; the load-bearing arguments are reproduced faithfully.

## (a) The backbone: a spanning anti-arborescence, not a spanning tree

The key structural fact: because every citation points strictly downward in
depth, a functional graph with one out-edge per certified declaration is
**automatically acyclic** — a forest of in-trees rooted at the sinks. The
25,230 components measured for top-1 are exactly its 25,230 distinct sinks.
That is not fragmentation damage; it is a forest with too many roots.

So the fix is not a different backbone family, it is **a root**. Add a virtual
root (the ambient logical framework) and attach every sink to it. The closed
state is then a maximum-weight spanning anti-arborescence: every declaration
points to exactly one parent, its highest-keyness prerequisite; every sink
points to the root. Exactly *n* edges, one component always, by construction —
no union-find, no post-hoc repair.

The algorithmic payoff is large. In general, maximum-weight spanning
arborescence needs Chu-Liu/Edmonds (Chu & Liu 1965; Edmonds 1967; Tarjan 1977)
because cycles among candidate parent choices must be contracted. **On a DAG
that machinery is vacuous**: the per-node argmax can never form a cycle, so
greedy independent selection is provably optimal. That is a single segmented
maximum over incidences sorted by target — seconds on 18.7M rows.

Alternatives rejected:

- **Maximum spanning tree (Kruskal/Prim).** Globally competitive, so an edge's
  fate depends on far-away edges — this violates the locality requirement at
  the structural level. It also leaves some declarations with no chosen parent
  at all, which is semantically incoherent for a citation graph.
- **Steiner tree.** Every node is a terminal, so it degenerates to a spanning
  tree.
- **k-core / degeneracy.** Deletes nodes, not edges, and gives no connectivity
  guarantee.
- **Chow-Liu.** Requires a joint distribution and pairwise mutual information
  over ~1.5 x 10^11 pairs. No natural distribution, no compute.

**Hypergraph fidelity.** The arborescence selects one *incidence* and never
expands a proof into a clique. Two variants: one parent per *declaration*
(a literal tree) or one parent per *proof* (preserves "every proof is
represented"). The proof-faithful variant is the honest default, and the two
nest.

## (b) The continuum: judge both endpoints

The **disparity filter** (Serrano, Boguñá, Vespignani, PNAS 2009) keeps edge
(i,j) when (1 − p_ij)^(k_i − 1) < α, where p_ij is the edge's share of node
i's strength. It is locally normalised — which matches "plumbing is relative"
exactly — has one monotone parameter, and is O(E).

Its failure modes all bite here:

1. **k = 1 and k = 2.** At k=1 the expression is undefined. The corpus is full
   of 1-3 citation proofs, which are exactly the "trivial proof of a trivial
   lemma" case the specification says must be kept.
2. **Degree-dependent stringency.** For large k the threshold behaves like
   −ln α/(k−1). This is the mechanism that would give stratified purity for
   free, but it means very large proofs can be reduced to nearly nothing.
3. **One-sidedness.** Disparity never sees that a lemma is cited 200,000 times
   library-wide. **Global commonness is the central plumbing signal, and
   disparity discards it.**

Because of (3) the recommendation is a **noise-corrected backbone** (Coscia &
Neffke, ICDE 2017): score each edge against a configuration/gravity null built
from *both* endpoint strengths, keeping edges whose weight exceeds expectation
by δ standard deviations. A hub lemma's edges must then be exceptional to
survive — plumbing detection falls out of the null instead of a blacklist.

The **Pólya urn filter** (Marcaccioli & Livan, Nature Communications 2019) is
the more principled version, with a self-reinforcing null whose p-values come
from the incomplete beta function; it handles heavy tails better. **LANS**
(Foti, Hurme & Rockmore 2011) is essentially "top x% per proof" — what was
already tried. **h-backbone** is parameter-free, which is a defect when a
slider is required. **Effective-resistance spectral sparsification** (Spielman
& Srivastava 2011) provably preserves all cuts, but it *reweights* surviving
edges — violating "never relabel" — and optimises spectral fidelity rather
than semantics. Use it as a diagnostic, not as the filter.

## (c) Monotonicity and nesting — one invariant makes it free

> Compute **one static real score per edge, once, on the full graph.** The
> slider is a threshold on that score. Nothing is ever recomputed on a
> filtered graph.

Under this rule disparity, noise-corrected, Pólya and LANS are all exactly
nested. What breaks nesting is recomputing node strengths on the
already-filtered graph, doubly-stochastic normalisation, and any randomised
sampler that redraws per level.

Implementation: sort the edges once by score and store a rank. Every level is
a **prefix of one array**. Nesting is then not a property to verify, it is a
property that cannot be violated.

## (d) Guaranteeing connectivity

`kept(t) = backbone ∪ {e : score(e) ≤ t}`, implemented by giving backbone
edges rank 0. This does **not** distort the statistics, because scores are
computed on the full graph before the backbone is chosen.

It is also nearly free with an arborescence backbone, which is the real
argument against an MST: the backbone edge for each proof is the per-proof
argmax, precisely the edge the filter is most likely to retain anyway. Expect
overlap above 0.8. (Measured here: **91%**.) An MST backbone would inject
globally-chosen, locally-meaningless edges and the overlap would be poor.

On the cycle-space alternative — "only ever remove edges that are not bridges,
in increasing score order" — that is the reverse-delete formulation, and it is
**provably identical to Kruskal on decreasing weight**. It buys nothing beyond
(a) and costs decremental connectivity maintenance.

## (e) Edge weights

Use a log-linear raw weight and let the null do the normalising:

    w(T <- c) = m_role · m_stmt · g(depth) · idf(c),
    idf(c) = log(N_proofs / #proofs citing c)

**idf is the workhorse**: measured, not tuned, and it encodes "globally common
implies probably plumbing" without a blacklist.

**Do not use the raw depth gap.** The measurement (median 22, p99 268) says
long-range citation is normal, so the gap has almost no discriminating power
globally. Use the within-proof z-score of the gap, or the ratio
depth(c)/depth(T).

**Per-proof normalisation pitfall.** Thresholding a per-proof share globally
is a document-length bias: a 2-citation proof gives each edge mass 0.5 and
always survives, while a 500-citation proof gives each 0.002 and is
annihilated. Since large proofs correlate with deep theorems, that **inverts
the stratification requirement**. Threshold the p-value, which conditions on
the number of citations, instead.

## (f) Stratification

**Mechanism 1 (free).** Purity at great depth falls out of the null's degree
dependence: deep theorems have large proofs, so the null is stringent and only
exceptional edges survive; shallow declarations have 1-3 citation proofs, the
null cannot reject anything, and glue is kept — as specified. **Prerequisite:
Spearman(depth(T), |citations|) must be strongly positive. Measure it first.**
(Measured here: **0.351** — positive but only moderate, so this mechanism
fires weakly and mechanism 2 is needed for a strong effect.)

**Mechanism 2 (explicit).** Bin edges by depth into quantile strata, estimate
the null *within* stratum, and convert to a within-stratum p-value.

**Warning that matters:** stratify the *null*, not the *acceptance rate*. If
survival fractions are forced equal per depth stratum, the very signal being
sought — that deep strata are purer — is destroyed by construction. Estimate
null parameters per stratum, apply **one global threshold**, and report the
survival-versus-depth curve as a finding.

## (g) Diagnostics beyond connectivity

1. Components = 1 at every level (assert). Then the sharper version: the
   fraction of retained edges that are **bridges** — a rising bridge fraction
   quantifies "the family is collapsing to a tree".
2. **Shortest-path stretch**: sample 10^5 pairs, report median and p99 of
   d_kept/d_full. The full graph is shallow (long-range edges); the backbone
   is deep. This curve is the honest cost of the slider and should be the
   headline plot.
3. **Depth-gradient preservation**: minimum retained hops from a deep theorem
   to a primitive, versus the full-graph value. If it explodes, the filter is
   keeping sideways edges and deleting descent edges.
4. **Cone retention**: retained ancestor-cone size over full cone size — does
   the retained cone read like a syllabus?
5. **Backbone stability**: jitter the weights and measure how many nodes
   change parent, by depth. Report the argmax margin per node; nodes with a
   tiny margin have essentially arbitrary parents and should be flagged in the
   interface rather than presented as canonical.
6. **Edge betweenness of survivors**: exact Brandes is infeasible (~10^13);
   use sampled-source approximation with a compiled library.
7. **Spectral distortion**: smallest nonzero Laplacian eigenvalues and
   effective resistances, kept versus full.
8. **Held-out semantic check**: hide 1% of proofs and test whether their
   citations rank high under the score. This is the only diagnostic that tests
   whether keyness means anything, rather than testing topology.

## Where the specification is subtly wrong

**"Connected at every level" and "removes all plumbing" are in genuine
tension, and the tension is exactly quantifiable.** Connecting 546,576 nodes
requires at least 546,575 retained edges *regardless of significance*. At the
closed end roughly half a million edges are present for topological reasons
alone. Worse, the relativity requirement makes this permanent: an all-plumbing
proof of an all-plumbing lemma is *correct*, so it keeps its backbone edge at
every level.

**Edge deletion can never remove plumbing from a connected graph.** No filter
fixes this; it is a counting fact.

The resolution is that two operations have been conflated:

- **Dial 1 (as specified): edge filtering with a connectivity floor.** Nested,
  monotone, connected, O(E) to build, O(1) to slide.
- **Dial 2 (what "remove plumbing" actually means): node contraction.**
  Contract each retained subtree whose nodes all fall below a depth threshold
  into its root, forming a quotient graph. Contraction preserves connectivity
  **by construction** — a quotient of a connected graph is connected — while
  genuinely removing plumbing from view, and it composes with the nested edge
  family since contracting a subtree of E(t1) ⊆ E(t2) respects the inclusion.

Deletion cannot give what was asked for; contraction can. Ship Dial 1 as the
slider and Dial 2 as the zoom, and the specification becomes consistent.
