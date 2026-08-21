# 03 — Answers to the Four Review Questions

## Q1. Is `delta_depth` an acceptable proxy for universality?

**No, not as stated.**

Universality is an up-set/time-dependent property. No strictly append-safe local/down-set statistic can recover it exactly in general.

`delta_depth` is nevertheless highly valuable as:

- an abstraction-span coordinate;
- a vertical-versus-lateral rendering signal;
- a multiscale filtration axis;
- a self-similarity candidate.

Do not call it universality, junk probability, or shortcut badness.

### What to do with counts

Live rarity/in-degree may be used in a **versioned global sidecar**.

For reproducibility, persist each version’s values.

Do not use live counts to redefine an existing proof’s canonical local rank.

A pinned count table is acceptable only as:

- a historical snapshot;
- a teacher/upper-bound signal;
- or an explicit “global state at version \(t\)” field.

It is not an intrinsic local relation.

### A third exact append-safe up-set quantity?

No, absent additional assumptions. The impossibility argument in `02_FORMAL_THEORY.md` rules it out.

The correct response is architectural separation, not a more ingenious proxy.

## Q2. Filter or weight?

**Neither should be canonical. Use a multifiltration.**

Weights force an exchange rate between:

- local salience;
- abstraction span;
- relation type;
- possibly global current use.

A single hard filter discards legitimate long-range bridges.

Preserve the vector and expose monotone views.

For a specific route planner:

- constrained or lexicographic paths are preferable to an arbitrary weighted sum;
- interactive expansion/click cost is a better primary model than all-pairs shortest path;
- a learned policy may combine features dynamically.

Use `delta_depth` to distinguish vertical drill-down from lateral traversal, not to erase edges.

## Q3. Must local ranking and global map use the same rule?

**No. They should not.**

Local proof explanation and global route selection solve different conditional problems.

### Local

\[
L(e\mid p)
\]

asks how an occurrence functions in one immutable proof.

### Global

\[
G_t(e\mid\text{task, region, version})
\]

asks how useful that occurrence/declaration is for navigation now.

The split is not an excuse if the coherence conditions in `02_FORMAL_THEORY.md` are enforced.

Recommended structure:

- stable local move hierarchy and intrinsic coordinates;
- dynamic global sidecars;
- task-conditioned navigator over both.

## Q4. How do we validate without scoring our own definition?

### Strongest internal validation: metamorphic invariance

Create formally equivalent or near-equivalent proof variants and test whether the high-level navigational skeleton is stable under:

- alpha-renaming;
- explicit versus implicit instances;
- wrapper insertion/removal;
- inline versus named `have`;
- tactic versus term proof;
- `simpa` versus explicit rewrite;
- fold versus unfold;
- generated-helper extraction.

This directly tests whether the map follows mathematics rather than compilation accidents.

### Exact expansion/reconstruction

Every collapsed or hidden occurrence must be recoverable by expansion, and the expanded structure must reconstruct the exact checked term.

### Alternative-proof/refactoring comparison

High-level landmarks should be more stable than low-level machinery across harmless refactorings. Genuinely different proofs may diverge and should remain distinct.

### Held-out citation prediction

Useful as a retrieval test, not a complete map-quality test. It rewards the recorded proof route and may reward common tools.

### Module co-location

Legitimate only as a weak external proxy. Mathlib files encode human organization but also engineering convenience.

### Pairwise mathematical relatedness

The strongest direct global test, but expensive. Use it on a small, discriminating set after the representation is frozen.

### Navigation tasks

Ultimately measure:

- clicks/expansions;
- irrelevant landmarks inspected;
- success finding the key definition/theorem;
- ability to compare proof routes;
- depth-band navigation;
- route explanation quality.
