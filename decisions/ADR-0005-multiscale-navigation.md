# ADR-0005 — Multiscale Navigation: the certificate-support hypergraph

Date: 2026-08-20. Status: accepted (external judge ruling, Trial 3 disposition).
Supersedes nothing; extends ADR-0004. Historical reports are preserved unchanged.

## The change

The research objective moves from **"improve rank 1"** to **"test whether the
verified relational record supports useful multiscale navigation across
mathematics."**

V8 is **frozen** as a reproducible citation/decluttering baseline. There is no
V9. Apparatus thresholds are not tuned further. The V8 ordering, the apparatus
heuristic, and the Prop-only claim list are **not promoted into the ontology**;
they are derived views, explicitly labelled as such.

## What a proof hyperedge means, and what it does not

For a proof artifact `p` certifying theorem `T`, with `C_p` the set of
declarations cited under a declared projection, the derived hyperedge is

    e_p : C_p ==> T

and it means exactly this:

> These declarations occur in this particular checked certificate for `T`.

It is **not** a claim that every tail declaration is logically necessary, that
the set is minimal, or that it is a canonical AND-decomposition. This is the
central semantic commitment of the phase, and it is what the trial's
prosecution correctly attacked in the previous framing: a support set observed
in one certificate is evidence, not entailment.

Consequences:

- **Proof-artifact identity is preserved.** Alternative proofs of the same
  theorem are distinct hyperedges, never merged.
- **No silent clique expansion.** Algorithms use a bipartite incidence
  representation (declaration nodes on one side, proof-artifact nodes on the
  other). Replacing a hyperedge by a clique among its citations would
  manufacture relations that the record does not contain.
- **Named theorem boundaries survive.** A theorem with exactly one user is
  still an abstraction boundary, not an inlining opportunity.

## Projections are reversible views, never edits

No projection may delete evidence from the backing record. Every view declares
its epistemic level (ADR-0004), its inclusion rule, its coverage, and its known
omissions, and every view must be regenerable from the exact record.

Two controls answer different questions and neither replaces the other:

- **top-k** bounds visual density and produces slices comparable across
  theorems;
- **the content boundary** (V8's glue/machinery cut, or any successor) tracks
  variable proof complexity, so a theorem with fifty substantive citations may
  keep all fifty while a short one keeps two.

## Depth is altitude, not importance

Depth remains a level-2 library-relative coordinate: map altitude and zoom, not
a truth label and not sophistication. Every citation incidence retains the
depth gap `Δd = d(T) − d(c)` together with both endpoint depths, so long
vertical jumps are visible and traceable.

Depth-band filtering provides two modes, because they answer different
questions: an **induced band** (only declarations inside the window, for
studying within-layer geometry) and a **portal band** (the window plus
summarized links to what it cites above and below, so a slice is not falsely
disconnected).

## Definitions and constructions remain first-class

A claim-only citation view may hide definitions, witnesses and constructions
for display, but they remain in the underlying object and must be exposed by at
least one view. The Trial 3 evidence appendix left open (item E2) whether
`Exists.intro` is pair-assembly or the exhibition of a witness; under this ADR
the question stops being a filter-tuning matter, because the local typed-move
layer represents witness construction directly rather than as a cited name.

## Persistence over one-cut storytelling

No structure is called important because it appears at one threshold. Claims
about communities, landmarks, bridges and routes must report whether they
persist across a declared range of projections, using simple statistics first
(rank correlation, partition agreement, component births and merges, bridge
survival, route survival). Advanced machinery is admitted only after a stable
phenomenon is found by simple means.

## Negative results are outcomes, not failures

The phase declares in advance that any of these is a legitimate conclusion:
the hypergraph is a genuine map projection; it is a useful index but shows no
robust deeper geometry; the local expansion carries most of the value; the
current ranking adds little relative to simple exact views; or depth is useful
only as a filter. Each has a pre-registered decision rule.

## Relationship to the rest of the program

    exact verified relations
      -> multiscale certificate-support hypergraph      (global atlas)
      -> expandable local typed moves                   (street level)
      -> later state-conditioned and semantic maps      (route planner)

The hypergraph is one projection of a single heterogeneous typed relational
record, not a replacement for it and not the only map the project needs.
Semantic, historical and pedagogical overlays attach as sidecars and never
enter the verified core; cross-proof "same move" identification is
conservative — the same global interface used in the same typed role — and
model-judged analogy is excluded from the verified layer entirely.
