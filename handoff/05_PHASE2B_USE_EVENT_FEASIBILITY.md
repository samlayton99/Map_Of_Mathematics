# Phase 2B — Contextual Use-Event Feasibility

## 1. Research question

Can Lean artifacts supply reliable training examples of the form:

\[
P(d\text{ useful}\mid \Gamma\vdash A)
\]

without fabricating author intent?

## 2. Minimal event

Use a deliberately small provisional record:

```text
UseEvent {
  before_state_content
  before_state_occurrence?
  named_declaration
  explicit_role?
  instantiation?
  after_state_contents[]
  source_span?
  proof_term_occurrence?
  raw_event_reference
  outcome
  completeness
  trust
}
```

Do not create a large permanent event ontology yet.

## 3. Confidence tiers

### Tier A — explicit

The source syntax names the declaration and role directly, such as `apply L` or `rw [L]`.

### Tier B — deterministic-derived

A named head application can be aligned between elaborator/proof term and a local transition, but the source role is not explicit.

### Tier C — ambiguous

Several declarations or automation steps could explain the result.

Store ambiguity rather than choosing one.

### Tier D — semantic

A human or model asserts the conceptual role. Keep this in the annotation layer.

## 4. Initial coverage

Focus on explicit or highly reliable families:

- `apply`;
- `exact`;
- `refine` with named head;
- `rw`;
- `unfold`;
- constructor use;
- explicitly listed simp lemmas.

Do not claim comprehensive proof experience.

## 5. Evaluation

Manually inspect a stratified sample and report:

- named-declaration precision;
- role precision;
- before/after state fidelity;
- instantiation completeness;
- ambiguity rate;
- coverage across proof styles;
- fraction of proofs with at least one reliable use event;
- fraction of named applications not attributable to a local source event;
- automation failure modes.

## 6. Decision significance

A high-precision but partial event set may still be valuable for supervised navigation.

Low coverage would imply one or more of:

- use proof-term applications as weak labels;
- instrument future interactive proving sessions;
- rely on natural-language tagging;
- use theorem-level premise prediction first;
- abandon the rich use-event hypothesis.

The phase must report which conclusion is supported.
