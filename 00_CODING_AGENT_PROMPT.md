# Coding-Agent Prompt: Validate the Minimal MathRecord

You are the lead research engineer for a narrowly scoped Lean 4 investigation.

Your job is not to build a universal mathematical platform or instantiate a philosophy of mathematics. Your job is to determine whether the smallest proposed Lean-native record is technically coherent, faithful, and worth building on.

Read every document in this package. `01_PART_A_IMMEDIATE_PROGRAM.md` defines the current work. `02_MATH_RECORD_CORE_SPEC.md` defines the provisional object. `03_PART_B_LONG_TERM_HYPOTHESIS.md` is context only. `04_DECISIONS_AND_STOP_RULES.md` is binding.

## Current question

> Can a minimal observation layer over Lean faithfully preserve the formal objects and local states needed for later navigation and learning?

Do not test ML value yet. First establish that the object itself is exact and nonredundant.

## Provisional exact core

The working record is

\[
\mathcal R=(E,X,D,S,T).
\]

- `E`: pinned environment snapshots.
- `X`: exact typed Lean expressions and universe levels.
- `D`: declarations.
- `S`: local states of the form \(\Sigma;\Gamma\vdash ?e:A\).
- `T`: observed state transitions.

Do not assume this schema is final. Gate 0 must determine how much is already available through Lean and maintained tooling. Reuse or wrap existing exact representations before writing a competing one.

## Execute only Gate 0 and Gate 1

After Gate 1, stop. Do not continue into scale testing, a storefront, or model training.

After each gate:

1. run every acceptance test;
2. write `reports/GATE_<n>.md` with evidence, commands, failures, and a pass/fail decision;
3. snapshot the exact code, toolchain, and configuration;
4. stop immediately if the gate fails.

## Gate 0 — Tool and representation audit

Audit the pinned Lean version and current ecosystem before fixing storage or schema.

Inspect and spike-test access to:

- environments and imports;
- `Expr` and universe structure;
- declaration types and values/proof terms;
- local contexts, binder scope, and local definitions;
- metavariables and targets;
- tactic/proof states;
- at least one successful and one failing action when accessible;
- source spans and provenance;
- definition transparency/unfolding;
- exact declaration references.

Candidate sources may include Lean's metaprogramming APIs, maintained exporters, and existing trace tools. Do not assume any named third-party tool is current or sufficient. Pin and test whatever is selected.

### Gate 0 deliverables

- a working extraction spike on at least three small proofs;
- one captured local proof state;
- one transition-access spike, without building a full trace dataset;
- a field-by-field source/gap matrix;
- `LEAN_REPRESENTATION_AUDIT.md`;
- one short architecture decision record;
- a reduced v0.1 schema containing only fields justified by the audit;
- an explicit list of unavailable, unstable, or redundant fields.

### Gate 0 passes only if

- exact declarations, expression structure, local contexts, and targets are accessible without scraping pretty-printed text as the formal source;
- completed terms/proofs can be connected to Lean checking;
- the agent can explain what custom layer is genuinely missing;
- there is a plausible path to stable serialization and canonical identity.

### Gate 0 stop conditions

Stop and report failure or pivot if:

- exact local states cannot be obtained reliably;
- the necessary information requires fragile parsing of display output;
- an existing maintained tool already supplies the complete required record and the project has no distinct experimental need;
- the proposed record would merely duplicate Lean internals without adding stable serialization, provenance, or query value.

## Gate 1 — Exactness on an adversarial micro-corpus

Proceed only if Gate 0 passes.

Create a small Lean corpus designed to expose representation failures. It must include at least:

- dependent functions and dependent products;
- local `let` declarations;
- equality and rewriting;
- existential witnesses;
- induction or recursion;
- structures and projections;
- typeclass synthesis;
- coercions;
- implicit and explicit binders;
- universe polymorphism;
- transparent and opaque declarations;
- theorem proof terms;
- one branching proof state;
- one failing action;
- two distinct proofs of the same proposition.

Implement extraction into the reduced MathRecord core.

### Gate 1 deliverables

- pinned, reproducible Lean project;
- adversarial conformance corpus;
- extractor and canonical serializer;
- validator and tests;
- canonical sample records;
- a minimal CLI or static inspector for one theorem;
- `SCHEMA.md`;
- `reports/GATE_1.md`;
- `NEXT_RECOMMENDATION.md` containing exactly one recommendation:
  - proceed to dynamic traces;
  - revise the static object;
  - abandon this representation in favor of an existing tool or a different approach.

### Gate 1 passes only if

1. every supported case is extracted without silent loss;
2. every completed proof or term still checks in the pinned Lean environment;
3. every stored target is well-formed in its stored ordered context;
4. binders, scopes, local definitions, universes, and declaration kinds are preserved;
5. type dependencies and body/proof dependencies can be recomputed from stored expressions;
6. two clean extractions produce identical semantic identities after documented canonicalization;
7. alpha-renaming of display names does not change structural identity;
8. unsupported data fails loudly and is classified;
9. one theorem can be inspected through its declaration, exact statement, body/proof, direct references, and one local state;
10. the final report distinguishes formal fidelity from informal mathematical meaning.

Do not count matching pretty-printed strings as structural fidelity.

## Hard non-goals for this run

Do not implement:

- representative or all-Mathlib extraction;
- a full transition/replay dataset;
- graph database infrastructure;
- a polished web storefront;
- premise-selection or next-step models;
- embeddings or required cloud APIs;
- conjecture generation;
- definition invention;
- semantic ontology or concept clustering;
- learned zoom;
- curation or importance models;
- categorical or higher-dimensional reformulations.

## Required final assessment

Stop after Gate 1 and write an evidence-based assessment answering:

1. Does the minimal record faithfully represent the tested Lean mathematics?
2. What exact information is lost or unstable?
3. What already existed and was reused?
4. Is `MathRecord` a useful observation layer or needless duplication?
5. Should the next project capture dynamic transitions, revise the object, or stop?

The correct outcome may be a negative result. Do not add scope to make the project look successful.
