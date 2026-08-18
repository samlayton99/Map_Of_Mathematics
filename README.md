# MathMap / MathRecord — Honest Two-Part Handoff

This package replaces the previous MathMap handoff. The earlier version tried to specify the platform, storage, storefront, and experiments before the core object had earned that complexity.

This version separates the work into two parts:

1. **Part A — Immediate validation.** Determine whether the smallest Lean-derived record is faithful and coherent on an adversarial micro-corpus.
2. **Part B — Conditional long-term hypothesis.** Preserve the larger idea—multiscale navigation and shared representations for proving, abstraction, statement synthesis, and curation—but make every extension conditional on evidence.

## The current coding run

The coding agent should execute only:

- **Gate 0:** audit what Lean and existing tools already provide;
- **Gate 1:** validate the minimal record on a deliberately difficult micro-corpus.

Then it must stop and report whether to proceed, revise, or abandon.

It should not yet extract a large Mathlib corpus, build a full storefront, or train a model.

## The minimal object

The provisional exact core is

\[
\mathcal R=(E,X,D,S,T),
\]

where:

- \(E\) contains pinned Lean environment snapshots;
- \(X\) contains exact typed Lean expressions and universe levels;
- \(D\) contains declarations such as definitions and theorems;
- \(S\) contains local states \(\Sigma;\Gamma\vdash ?e:A\);
- \(T\) contains observed proof-state transitions, including failures.

In the current run, `T` only needs an extraction spike proving that transitions are accessible. Full transition capture belongs to the next gate.

Dependencies, proof routes, expression views, and module views are derived projections of this one record. They are not separate truth stores.

## Why this can plausibly represent formal mathematics

Lean already represents mathematical objects, propositions, definitions, and proofs as typed expressions in an environment. The record is not a new foundation; it is a stable, inspectable observation layer over Lean's own formal objects.

If it preserves the environment, exact expressions, scoped contexts, targets, and terms, then it can represent formalized mathematics in that pinned Lean world. It does **not** thereby represent informal meaning, motivation, importance, analogy, or all mathematics outside Lean. Those are later overlays.

## Read in this order

1. `00_CODING_AGENT_PROMPT.md`
2. `01_PART_A_IMMEDIATE_PROGRAM.md`
3. `02_MATH_RECORD_CORE_SPEC.md`
4. `03_PART_B_LONG_TERM_HYPOTHESIS.md`
5. `04_DECISIONS_AND_STOP_RULES.md`

For agents that accept only one attachment, use `CONSOLIDATED_HANDOFF.md`.

## What success means now

A successful current run establishes only that:

1. the record faithfully captures representative Lean declarations and local mathematical states;
2. the serialization is deterministic and structurally meaningful;
3. completed artifacts remain connected to Lean verification;
4. the object is not merely a redundant reimplementation of an existing maintained tool.

It does not establish that the representation improves AI reasoning. That question comes later.
