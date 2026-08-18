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
