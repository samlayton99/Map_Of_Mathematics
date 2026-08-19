# Phase 3 — Disagreement Audit

High-information failure and disagreement cases (`data/disagreements.json`, reviewer notes). These are more instructive than the successes.

## 1. Topology says machinery, P3 says nothing — a real P3 label gap

Top high-confidence cases are **structure constructors** (`Lattice.mk`, `Preorder.mk`, `SemilatticeSup.mk`, `LE.mk`, …, machinery-prob 0.76–0.84) plus core logic inductives (`True`, `Iff`). P3 classifies structure *projections* and *instances* but never the `.mk` constructors, and its logic-core list holds ctors/eliminators but not the inductive types themselves. Topology found a coherent hole in the deterministic labeling. Recommended P3 amendment (needs its own ADR, not applied silently): classify constructors of typeclass/order structures and core logic inductives.

## 2. P3 says machinery, topology says content — the boundary is context-dependent

Top cases are **instances defined inside the corpus files themselves** (`OrderDual.instDistribLattice`, `Pi.instSemilatticeInf`, …, prob 0.12–0.19) and `_proof_1` auxiliary theorems. A file-local instance has full body structure and modest in-degree — structurally it *is* content of that file, even though its global role is plumbing. This directly supports the handoff's central distinction: machinery is a **role relative to a context**, not a permanent node class. (`_proof_N` internals are name-detectable only — topology legitimately cannot see them.)

## 3. The worst reviewed case: `Nat.pow_sub_one_gcd_pow_sub_one`

Every view — including the winner — surfaced only well-founded-recursion artifacts (`Nat.pow_sub_one_gcd_pow_sub_one._unary`, `PSigma.mk`, `WellFounded` machinery). The entire Euclidean-descent argument is invisible: it lives inside the `_unary` auxiliary's body, which is a *stored* declaration but not the reviewed one. Declaration-level ranking fails structurally when the equation compiler moves the mathematics into a generated twin. Fix direction: follow `_unary`/`match_` indirections to their bodies before ranking (deterministic, one level).

## 4. Blind spots common to every view (both reviewers, independently)

- local hypotheses, witnesses, and `h ▸`-substitutions;
- `simpa`/`suffices` transports and identity bridges;
- case-split/induction structure beyond private match names;
- representation-change lemmas (`isOpen_compl_iff`-style pivots).

These are theorem-local *moves*, not declarations; no declaration ranking can express them. They mark the exact boundary where the P5-event/state layer (and eventually semantic annotation) becomes necessary rather than optional.

## 5. Packet defects (kept as evidence)

`add_one_zsmul`, `sup_eq_and_inf_eq_iff` (and partially `DistribLattice.le_sup_inf`) had truncated Part 2 sources: their `declarationRanges` spans start at an attribute/`instance` line and my statement-vs-proof splitter mis-cut. Reviewers rated with lowered confidence and said so — provenance worked as designed. Fix in a future packet build; responses for these three carry reduced weight in the summary.
