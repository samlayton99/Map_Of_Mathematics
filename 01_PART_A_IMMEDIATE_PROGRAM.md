# Part A — The Honest Immediate Program

## 1. The immediate problem

The immediate project is not “build the representation of all mathematics.”

It is:

> **Determine whether a small, exact Lean-derived record can faithfully represent representative formal mathematical objects and local construction states.**

The current coding run ends after that question is answered.

Only if the object passes should the project scale it, turn it into a storefront, or test it against token and graph baselines.

## 2. What is established versus hypothesized

### Established enough to build on

- Lean represents mathematical objects, propositions, definitions, and proofs as typed expressions in environments.
- A local formal task can be described as
  \[
  \Sigma;\Gamma\vdash ?e:A.
  \]
- Lean has exact declarations, local contexts, metavariables, proof terms, and a trusted checker.
- Multiple graph-like views can in principle be derived from those objects.

### Still hypotheses

- A new stable observation layer is needed rather than existing tooling being sufficient.
- Explicit structural representations improve premise selection or next-step prediction.
- Local proof structure transfers across mathematical domains.
- Useful abstraction levels can be learned.
- Definitions can be scored by future proof-cost reduction.
- One shared representation can support proving, statement synthesis, abstraction, and curation.

The first coding run tests only the first hypothesis.

## 3. The smallest coherent object

Use the provisional record

\[
\mathcal R=(E,X,D,S,T).
\]

This is one object with five components, not five independent ontologies.

- \(E\): pinned environment snapshots.
- \(X\): immutable typed expression and universe structure.
- \(D\): declarations pointing into \(X\).
- \(S\): local construction states pointing into \(E\) and \(X\).
- \(T\): observed actions connecting states.

For the current run, implement `E`, `X`, `D`, and `S` fully enough for the conformance corpus. For `T`, only prove through a spike that transition information can be obtained. Full transition recording is the next gate, not part of the current build.

## 4. Why this object is plausibly expressive

From the same typed core:

| Mathematical artifact or activity | Representation |
|---|---|
| Mathematical object | term `e : A` |
| Proposition | type `P : Prop` |
| Proof | term `p : P` |
| Definition | named declaration with type and body |
| Theorem | named proposition-valued declaration with proof term |
| Local assumptions | ordered context `Γ` |
| Goal | target `A` |
| Unfinished proof | metavariable or hole `?e : A` |
| Dependency | constants occurring in type or body/proof expressions |
| Alternative proof | distinct proof term with the same target |
| Exact zoom | declaration → term → expression structure |

This is enough to claim possible adequacy for **formalized mathematics in the pinned Lean environment**.

It is not enough to claim that the object captures:

- informal meaning;
- motivation;
- mathematical importance;
- conceptual sameness;
- historical discovery;
- applications;
- all possible proofs;
- all mathematical foundations.

Those must remain separate future layers.

## 5. Current execution: Gate 0 and Gate 1

### Gate 0 — Audit before schema

**Question:** What does Lean and maintained tooling already provide, and what is genuinely missing?

**Work:**

- pin the toolchain;
- inspect expressions, declarations, contexts, metavariables, proof terms, and proof states;
- test existing exporters or trace tools;
- capture several small examples;
- map each desired field to its source;
- revise the provisional schema.

**Pass:**

- exact declarations, expressions, local contexts, and targets are accessible;
- completed terms remain connected to Lean checking;
- unstable identifiers are understood;
- the custom layer has a clear, narrow purpose.

**Fail:**

- the required data is inaccessible or available only through fragile display parsing;
- existing tooling already solves the problem and no distinct research layer remains;
- the proposed object adds complexity without stable identity or query value.

### Gate 1 — Lossless micro-corpus

**Question:** Does the reduced object faithfully represent difficult representative Lean constructs?

**Work:**

- create an adversarial conformance corpus;
- extract and serialize it;
- validate terms, targets, contexts, references, and determinism;
- inspect one theorem end to end.

**Pass:**

- all supported cases preserve exact structure;
- all completed terms check;
- contexts and binders remain well scoped;
- extraction is deterministic after documented normalization;
- unsupported cases fail loudly;
- the result is inspectable and clearly tied back to Lean.

**Fail:**

- fidelity depends on pretty-printed text;
- identity is unstable;
- context or binder structure is lost;
- unsupported constructs are silently omitted;
- recorded terms cannot be related back to Lean verification.

### Required stopping point

After Gate 1, stop and decide:

1. proceed to dynamic traces;
2. revise the object;
3. abandon or wrap an existing representation instead.

Do not automatically continue.

## 6. The next evidence gates, not part of the current run

These gates are included so the object has a disciplined path forward.

### Gate 2 — Dynamic activity

**Question:** Can the same core represent successful and failed proof-state transitions and replay completed routes?

**Success:** observed transitions preserve exact before/after states, completed routes reconstruct checked terms, and alternative proofs remain distinct.

### Gate 3 — Real-corpus survival

**Question:** Does the object remain deterministic and queryable on a bounded but genuine Mathlib slice?

**Success:** high-coverage extraction, classified failures, stable hashes, and no manual repair.

### Gate 4 — Exact map/storefront

**Question:** Can declaration, dependency, proof-route, context, and expression views all be generated from the same exact core while preserving identity and provenance?

**Success:** users can expand and collapse one formal artifact without switching to a second manually curated truth store.

### Gate 5 — Does structure matter?

**Question:** Does the representation improve premise selection or local proof prediction beyond strong token and flat-graph baselines on held-out mathematics?

**Success:** a preregistered, statistically credible, practically meaningful held-out gain.

A negative result here should stop the grand learned-substrate thesis, even if the exact map remains useful software.

## 7. Why this order is important

The project needs three separate achievements:

1. **Faithfulness:** the object correctly represents the formal source.
2. **Usefulness:** the object supports better navigation or tools.
3. **Scientific value:** the object improves learning or transfer beyond existing representations.

These are different claims.

The earlier handoff tried to pursue all three at once. This program forces them to be earned in order.
