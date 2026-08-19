# Consolidated MathMap / MathRecord Handoff


---

# FILE: README.md

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


---

# FILE: 00_CODING_AGENT_PROMPT.md

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


---

# FILE: 01_PART_A_IMMEDIATE_PROGRAM.md

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


---

# FILE: 02_MATH_RECORD_CORE_SPEC.md

# Minimal MathRecord Core Specification

Status: provisional, deliberately small, and subject to revision after Gate 0.

## 1. Formal object

The exact core is

\[
\boxed{\mathcal R=(E,X,D,S,T)}.
\]

It is a versioned record of a pinned Lean environment and formal activity observed within it.

## 2. Environment snapshots \(E\)

An environment snapshot identifies the formal world in which every other record is meaningful.

Minimum fields:

```text
environment_id
lean_version
lean_revision, if available
mathlib_revision
project_revision
ordered_imports
relevant_options
extractor_name_and_version
fingerprint
```

Invariant:

> Records from different environment fingerprints are never silently treated as identical.

## 3. Expression store \(X\)

The expression store preserves Lean's typed expression and universe structure. It must retain enough information to distinguish binders, scopes, constants, applications, lambdas, dependent function types, lets, projections, literals, metadata when semantically required, metavariables, and universe levels.

The exact constructor list must be derived from the pinned Lean version during Gate 0.

### Identity

Expression identity must not depend on pretty-printing or unstable generated names.

Use documented canonicalization for:

- bound variables;
- free/local variable identities;
- metavariable identities within a trace;
- universe parameters where alpha-renaming is irrelevant.

The safest initial identity is a deterministic structural encoding plus the environment fingerprint.

### Invariant

> If two encoded expressions have the same semantic identity, the project must be able to justify that equivalence through exact structural normalization, not visual similarity.

## 4. Declarations \(D\)

A declaration record points into the expression store.

Minimum fields:

```text
declaration_id
fully_qualified_name
kind
environment_id
universe_parameters
type_expression_id
value_expression_id, optional
module
source_span, optional
transparency_or_reducibility, when available
trust/provenance
```

Examples:

- A transparent definition has a type and body.
- A theorem has a proposition-valued type and a proof term/value when available.
- An axiom has a type but no proof body.
- Constructors, recursors, and projections remain distinct declarations.

Do not collapse theorem type dependencies and chosen-proof dependencies.

Derived sets:

\[
\operatorname{TypeDeps}(d)=\{c: c\text{ occurs in the type expression of }d\},
\]

\[
\operatorname{ValueDeps}(d)=\{c: c\text{ occurs in the body/proof expression of }d\}.
\]

These describe one declaration in one environment, not an intrinsic dependency set of the abstract theorem.

## 5. Local states \(S\)

A local state represents a formal construction problem:

\[
\Sigma;\Gamma\vdash ?e:A.
\]

Minimum fields:

```text
state_id
environment_id
ordered_local_context
target_expression_id
metavariable_or_partial_term_id, optional
source_location, optional
trace_id
status
```

Each local declaration in \(\Gamma\) should preserve:

```text
local_id
binder_info
type_expression_id
value_expression_id, optional   # local let/definition
user_name_for_display
implementation_detail_flag, when available
```

The ordered context and exact local identities are part of the state. A state is not identified by its pretty-printed goal text.

### Invariants

- Every local type is well-formed relative to preceding local declarations.
- The target is well-formed in the stored context.
- Free-variable references resolve to stored local declarations.
- State identity is stable under irrelevant pretty-printer choices.

## 6. Transitions \(T\)

A transition records an observed attempt to transform one state into successor states.

Minimum fields:

```text
transition_id
trace_id
before_state_id
action_source_text, optional
action_kind_or_structured_form, optional
after_state_ids[]
outcome: success | failure | timeout | unsupported
diagnostic, optional
elapsed_time, optional
provenance
```

One successful action may create zero, one, or many successor states.

Failures are first-class data. They are not part of the trusted theorem library, but they are part of the activity record.

### Invariant

> The record must distinguish an observed transition from a logically necessary implication.

A tactic transition is a historical route, not the only possible proof route.

## 7. What is derived rather than stored as a second truth source

The following should be computed from \(E,X,D,S,T\):

- declaration dependency graph;
- expression DAG/tree views;
- module aggregation;
- proof-state trajectories;
- definition expansion/collapse;
- theorem-to-proof routes;
- type-only versus proof-only dependencies;
- candidate training examples for premise selection and next-step prediction.

A cache or index may store derived results for speed, but it must be reproducible from the exact core and labeled as derived.

## 8. Trust classes

Every record or relation should belong to one of these classes:

1. **Lean-exact:** directly extracted from, reconstructed in, or checked by Lean.
2. **Observed:** a real trace/action/event produced by tooling, but not a theorem of the logic.
3. **Deterministic-derived:** mechanically computed from exact or observed records.
4. **Human-authored:** annotation or concept label supplied by a person.
5. **Model-inferred:** similarity, abstraction, importance, or alignment proposed by a model.

The UI and APIs must never present classes 4 or 5 as if they were class 1.

## 9. Sufficiency claims the core may earn

After Gates 1–4, the project may claim that the record is sufficient to represent, for the tested Lean environment:

- formal declarations;
- theorem statements;
- proof certificates;
- exact local contexts and goals;
- observed proof construction trajectories;
- explicit definition bodies;
- chosen-proof dependencies;
- alternative observed routes;
- exact multilevel inspection.

It may not claim that the record captures:

- all mathematical meaning;
- mathematical importance;
- informal theorem identity;
- every possible proof;
- all foundations;
- the complete process by which humans discover mathematics.

## 10. Extension points for the long-term object

Future records may refer to exact core IDs without changing their meaning:

- candidate statements;
- computational observations;
- counterexamples;
- failed proof searches;
- informal descriptions;
- theorem alignments;
- semantic concepts;
- learned abstractions;
- task-specific coarse-grainings;
- utility and curation scores;
- theory translations;
- application models.

This is how one record can grow into a broad mathematical substrate without pretending that inferred semantics are kernel facts.

## 11. Non-normative illustrative shape

```json
{
  "environment": {"id": "env:...", "fingerprint": "..."},
  "expressions": {"expr:...": {"kind": "forall", "...": "..."}},
  "declarations": {
    "decl:...": {
      "name": "Example.theorem",
      "kind": "theorem",
      "type": "expr:type",
      "value": "expr:proof"
    }
  },
  "states": {
    "state:0": {
      "context": ["local:x", "local:h"],
      "target": "expr:goal"
    }
  },
  "transitions": {
    "transition:0": {
      "before": "state:0",
      "action": "exact ...",
      "after": [],
      "outcome": "success"
    }
  }
}
```

The coding agent must revise this shape after Gate 0 rather than treating it as a frozen JSON contract.


---

# FILE: 03_PART_B_LONG_TERM_HYPOTHESIS.md

# Part B — The Long-Term Hypothesis

This document preserves the larger idea without pretending that it has been validated.

## 1. The enduring vision

The desired end state is not merely a theorem database.

It is a living mathematical record that can support:

- exact verification;
- local proof construction;
- alternative routes and failed attempts;
- definitions and abstractions;
- statement synthesis and refutation;
- curation and importance;
- multiscale navigation;
- human and agent collaboration.

The intuition is that formal mathematics contains global accumulated structure and recurring local typed activity. The research hypothesis is that a learner operating on this structure can transfer reasoning patterns, compress mathematical knowledge, and navigate it more effectively than systems based only on surface text.

## 2. The long-term single object

If the immediate core succeeds, extend it to

\[
\boxed{\mathcal W_t=(\mathcal R_t,\mathcal O_t,\mathcal V_t)}.
\]

- \(\mathcal R_t\): the exact formal core from Part A.
- \(\mathcal O_t\): an epistemic and activity overlay.
- \(\mathcal V_t\): a system of task-specific views and coarse-grainings.

This is still one versioned object. The layers are separated by trust, not stored as unrelated products.

### Exact core \(\mathcal R_t\)

Lean-checked or Lean-derived declarations, expressions, states, transitions, environments, and certificates.

### Epistemic/activity overlay \(\mathcal O_t\)

Records such as:

- conjectures;
- computational observations;
- counterexamples;
- failed attempts;
- alternative formalizations;
- informal explanations;
- provenance and historical sequence;
- candidate equivalences and analogies;
- novelty and utility estimates.

Every edge has a relation type, source, time, and confidence/trust class.

### View system \(\mathcal V_t\)

Maps the exact object to task-specific representations:

\[
C_q:\mathcal W_t\longrightarrow\mathcal W_{t,q}^{(k)},
\]

where \(q\) is a task and \(k\) is a resolution budget.

Examples:

- five conceptual units for a high-level explanation;
- 100 units for premise retrieval;
- 1,000 units for semantic auditing;
- full expression detail for kernel checking.

This is the rigorous version of the Google Maps idea: one territory, multiple resolutions, with explicit knowledge of what was collapsed.

## 3. The mathematical activity loop

A mature system would support:

\[
\boxed{
\text{Explore}
\rightarrow
\text{Represent/Propose}
\rightarrow
\text{Solve or Refute}
\rightarrow
\text{Verify}
\rightarrow
\text{Curate}
\rightarrow
\text{Explore again}.
}
\]

### Explore

Compute examples, search finite models, inspect failed proofs, compare analogous structures, and seek counterexamples. Exploratory evidence is not proof.

### Represent

Introduce useful definitions, interfaces, invariants, or intermediate lemmas. A transparent definition is a verified representation change; an abstraction is useful only if it reduces future work or exposes reusable structure.

### Propose

Synthesize a candidate theorem type. Hypotheses and conclusions are parts of one formal statement, though the system may separately model the discovery of a pattern and its precise formalization.

### Solve or refute

Construct a proof term, a certified counterexample, or a partial result.

### Verify

Lean checks formal validity. The learned system does not replace this function.

### Curate

Decide whether the artifact deserves explicit status in the library or map. Validity does not imply novelty, nonredundancy, clarity, or importance.

## 4. Shared-representation hypothesis

The long-term ML hypothesis is:

\[
z=F_\theta(\Sigma,\Gamma,A,\text{relevant neighborhood}),
\]

with different conditional policies operating over \(z\):

\[
\pi_{\mathrm{proof}},\quad
\pi_{\mathrm{statement}},\quad
\pi_{\mathrm{abstraction}},\quad
V_{\mathrm{utility}}.
\]

Lean supplies validity, not the learned value function.

This architecture is plausible because all activities manipulate typed mathematical objects in shared environments. It is not established. The immediate gates are designed to determine whether the shared structural representation has any measurable advantage.

## 5. Long-term gates, in order

These gates are conditional. Do not begin one because it is exciting; begin it only because the preceding evidence supports it.

### Gate 6 — Cross-domain next-step transfer

**Question:** Is there reusable local “physics” of proof construction?

Task:

\[
(\Sigma,\Gamma,A)\longrightarrow\text{next proof action}.
\]

Train on selected domains and test on held-out domains. Compare token, structural, and hybrid representations with matched budgets.

**Positive evidence:** statistically credible improvement on held-out domains and either at least 5% relative improvement on the primary action metric or a meaningful reduction in end-to-end proof-search cost.

**Strong evidence:** roughly 10% or more relative improvement, materially better sample efficiency, or at least 20% fewer search nodes at matched success.

### Gate 7 — Learned zoom

**Question:** Can the system discard formal detail in a task-dependent way without losing what matters?

Construct views at several budgets and measure downstream performance.

**Positive evidence:** a view using no more than 20% of the exact units retains at least 95% of the full representation's performance on a predeclared task, or materially improves human navigation while preserving verifiable expansion links.

The learned view must record what was collapsed and remain connected to exact core IDs.

### Gate 8 — Abstraction invention

**Question:** Can repeated proof structure be converted into a useful definition or lemma?

A candidate abstraction must:

- be expressible and verifiable in Lean;
- avoid merely memorizing one proof;
- apply to held-out tasks;
- reduce future proof-search or description cost.

A simple utility target is

\[
\Delta C=
C(\text{held-out proofs without abstraction})-
C(\text{held-out proofs with abstraction}).
\]

**Positive evidence:** verified, nontrivial abstractions reduce aggregate held-out proof cost by at least 10% in several independent motifs or domains.

### Gate 9 — Statement synthesis and refutation

**Question:** Can the system propose statements that are resolvable, nontrivial, nonredundant, and structurally useful?

Do not evaluate by raw theorem count.

Require:

- proof or certified counterexample rate;
- redundancy checks against the existing library;
- controls for vacuity and trivial reformulation;
- downstream utility or expert judgment on a bounded benchmark.

The system should be rewarded for informative false conjectures as well as true ones when their counterexamples reveal useful boundaries.

### Gate 10 — Curation and value

**Question:** Can the system predict what deserves explicit memory?

Possible targets include:

- realized future reuse;
- reduction in future proof cost;
- compression of later declarations;
- bridge value across modules;
- novelty and redundancy;
- expert-maintainer decisions.

A useful initial test is retrodictive: using only information available when a declaration was introduced, predict its future load-bearing role better than citation count, degree, length, and text baselines.

### Gate 11 — Theory-level transport and applications

**Question:** Can the system find structure-preserving maps between mathematical regions and use them to transfer results?

This is closer to deep cross-field discovery than ordinary graph proximity. It should only be attempted after structural transfer and abstraction learning have worked at smaller scales.

## 6. What the final object would represent

If the program succeeds, the object would represent at least four aspects of mathematics:

1. **Products:** definitions, statements, proofs, counterexamples, algorithms.
2. **States:** contexts, goals, available constructions, partial terms.
3. **Processes:** successful and failed transitions, alternative routes, discovery history.
4. **Views:** human- and task-specific abstractions at multiple resolutions.

It would not identify formal validity with human meaning. Instead, it would anchor every semantic or conceptual view to an exact formal substrate and expose the trust boundary.

## 7. Why this could be important

The powerful possibility is not merely better search.

If local structure transfers, zoom can be learned, and abstractions can be scored by future utility, then the same record could become:

- a map for humans;
- a state space for proof agents;
- a replay buffer for learning;
- a curriculum generated from reachable frontiers;
- a substrate for abstraction discovery;
- a curation system for proof abundance.

That would be a substantial change in mathematical infrastructure.

But the program earns this conclusion only by passing the gates. Coherence is not evidence.

## 8. The honest end-state claim

The long-term goal is not to prove that one data structure is metaphysically identical to mathematics.

It is to build one extensible record that is expressive enough to host exact formal mathematics, mathematical activity, and multiple justified views without conflating them.

That is a strong and achievable notion of “an object that represents mathematics.”


---

# FILE: 04_DECISIONS_AND_STOP_RULES.md

# Decisions, Non-Goals, and Stop Rules

## 1. Decisions

### Lean remains the verifier

The project builds on Lean's kernel and environment. It does not create a replacement logic or trusted checker.

### Audit before schema

The v0.1 schema must be reduced or modified after inspecting current Lean APIs and trace tools. Existing exact representations should be wrapped or indexed rather than duplicated without reason.

### One exact core, many projections

Dependencies, proof routes, and map views must be reproducible from the exact core. Caches are permitted; contradictory truth stores are not.

### Static fidelity before dynamic tracing

The current run validates declarations, expressions, contexts, and goals before building a large transition dataset. A transition-access spike is required, but replay infrastructure is Gate 2.

### Structural plus text is a first-class baseline

The project should not assume that structure replaces language. The likely strongest system may be hybrid.

### Held-out transfer matters more than random-split gains

Random splits can reward local memorization. The central learning hypothesis concerns reusable structure, so held-out module, domain, and time tests are required.

### Negative results are deliverables

A faithful representation that fails to improve learning is still a useful finding. It should prevent premature expansion.

## 2. Immediate non-goals

Do not build in the current Gate 0–1 run:

- a full proof-transition or replay dataset;
- representative or all-Mathlib extraction;
- a universal ontology of mathematical concepts;
- autonomous conjecture generation;
- definition invention;
- learned curation;
- theory-morphism mining;
- informal-math alignment at web scale;
- a production graph platform;
- a polished public UI;
- a premise-selection or theorem-proving model;
- a new theorem prover kernel;
- a claim that the object represents all human mathematical meaning.

## 3. Stop rules

### Stop after Gate 0 if

- exact declarations, local contexts, or targets cannot be accessed reliably;
- necessary data requires fragile parsing of display strings;
- completed terms cannot be connected back to Lean checking;
- existing tooling already provides the complete needed object and the project has no distinct experiment.

In the last case, pivot to using the existing representation rather than rebuilding it.

### Stop after Gate 1 if

- exact expression/context identity cannot be made deterministic;
- fidelity depends on pretty-print matching;
- unsupported constructs are silently dropped;
- context, binder, universe, or local-definition information is lost;
- completed artifacts cannot be related back to Lean verification.

### Stop after Gate 2 if

- state transitions depend on unstable process state that cannot be normalized;
- successful routes cannot be replayed or related to checked terms;
- failure traces cannot be represented honestly;
- the tracing layer requires changing Lean's trusted semantics.

### Stop after Gate 3 if

- the object only works on toy examples;
- real-corpus failures are widespread or unclassifiable;
- environment/version sensitivity makes records uninterpretable;
- extraction cost makes later experiments infeasible.

### Stop or reframe after Gate 4 if

- useful views require a separate hand-built ontology rather than projections of the core;
- expand/collapse loses identity or provenance;
- the object adds no navigational value beyond existing Lean tools.

### Stop the grand ML thesis after Gate 5 if

- structural and hybrid models do not beat a well-tuned text baseline on held-out mathematics;
- gains appear only under random splits;
- gains vanish under leakage controls or anonymization;
- the effect is too small to justify the representation cost.

A negative Gate 5 does not forbid a useful navigation product. It blocks confident claims about a new mathematical learning substrate.

## 4. Anti-goals

The project should actively avoid:

- naming a speculative architecture as if the name proves it is correct;
- building storage before understanding the source data;
- measuring graph centrality and interpreting it as mathematical importance without validation;
- treating one chosen proof's dependencies as the theorem's intrinsic dependencies;
- treating model similarity as theorem equivalence;
- treating kernel validity as semantic fidelity or importance;
- using the number of generated theorems as success;
- adding features because they fit the vision rather than because a gate requires them;
- continuing after a failed gate by adding complexity.

## 5. Evidence language

Use these terms consistently:

- **Implemented:** code exists and was run.
- **Validated:** written acceptance tests passed.
- **Positive evidence:** a predeclared experiment materially supports a hypothesis.
- **Strong evidence:** the effect is large, robust, and survives held-out evaluation.
- **Speculation:** plausible but not empirically established.

Do not write “the representation of mathematics” in technical reports. Write “the tested Lean-native record” unless the claim has been carefully scoped.


---

# FILE: WHAT_CHANGED_FROM_V1.md

# What Changed from the Previous Handoff

The previous handoff was thoughtful but premature. It specified a large versioned IR, tracing system, storefront, medium-scale extraction, and ML experiments before proving that the minimal record was exact or needed.

This revision makes six changes.

1. **The project is split in two.** Part A validates the exact core. Part B preserves the conditional long-term research program.
2. **The current coding run executes only Gates 0 and 1.** It audits Lean and validates the object on a micro-corpus, then stops.
3. **The core object is reduced to \((E,X,D,S,T)\).** Full transition infrastructure is deferred until the static core passes.
4. **Existing Lean representations are audited before a schema is frozen.** Reuse is preferred over reimplementation.
5. **Every expansion is gated.** Real-corpus extraction, the storefront, and ML tests come later and can be abandoned independently.
6. **The end-state claim is narrowed.** The goal is one extensible record that can anchor exact formal mathematics and justified views—not a claim that one data structure is metaphysically identical to all mathematics.

The long-term vision has not been discarded. It has been removed from the critical path until evidence supports it.


---

# FILE: PROMPT_TO_PASTE.md

# Paste this into the coding agent

Read the attached MathMap / MathRecord handoff, beginning with `00_CODING_AGENT_PROMPT.md`.

Execute **only Gate 0 and Gate 1**.

First audit the current Lean ecosystem and determine what exact objects and maintained tools already exist. Avoid inventing a new intermediate representation where Lean or existing tooling already provides the required data.

Then build and validate the smallest coherent record

\[
\mathcal R=(E,X,D,S,T)
\]

of Lean environments, typed expressions, declarations, and local states, with only a transition-access spike for `T`. Lean remains the verifier and source of formal truth.

After Gate 1, stop. Produce the gate reports and one evidence-based recommendation: proceed to dynamic traces, revise the object, or abandon/wrap an existing representation.

Do not build a large Mathlib extraction, polished storefront, graph platform, model, conjecture generator, abstraction inventor, or curation system in this run.

Negative results are acceptable. The goal is to discover whether the smallest exact object is coherent and worth building on.
