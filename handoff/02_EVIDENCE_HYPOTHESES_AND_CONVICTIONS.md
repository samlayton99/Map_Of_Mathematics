# Evidence, Hypotheses, and Conviction Levels

## A. Reproduced or directly testable evidence

### E1. Lean exact objects are available

Lean exposes exact terms, types, declarations, local contexts, proof bodies, and elaborator information.

### E2. MathRecord v0.1 was faithful on its tested corpus

Gates 0–1 reported deterministic serialization, alpha-invariant structural identity, exact round trips, dependency reconstruction, and Lean checking on the adversarial micro-corpus.

### E3. Type and proof/body references differ

This follows directly from separate exact Lean expressions.

### E4. Named declarations occur in proof terms and source-level proof actions

Their occurrence is extractable to varying degrees.

## B. Strong design judgments

### J1. Keep Lean as the verifier

Very high conviction.

### J2. Keep exact and semantic data separate

Very high conviction.

### J3. Preserve raw evidence under all derived projections

Very high conviction.

### J4. Use stable IDs so future annotations can attach without mutating formal identity

High conviction.

## C. Central research hypotheses

### H1. Named declarations are a useful primary abstraction level

Plausible and central, but not yet validated as sufficient or optimal.

### H2. Direct certificate support contains useful human-scale proof information

Uncertain. It may be dominated by infrastructure or omit conceptual organization.

### H3. Application occurrences provide a better route representation than support sets

Plausible. Recoverability and usefulness are unknown.

### H4. Contextual declaration-use events capture transferable mathematical experience

Plausible and partially supported by premise-selection research, but the proposed event representation is untested.

### H5. Selective declaration expansion is useful zoom

Plausible. It is not guaranteed that formal expansion tracks conceptual explanation.

### H6. Alternative proof routes reveal bridge structure

High upside, low near-term evidence and sparse data.

### H7. Explicit structure improves learned navigation beyond strong text/retrieval baselines

Unknown and requires a controlled experiment.

## D. Long-term speculation

- one substrate supports proving, conjecturing, abstraction invention, and curation;
- global graph structure enables distant mathematical discovery;
- proof diversity reveals theory morphisms;
- value can be learned from future proof-cost reduction;
- the system becomes transformative mathematical infrastructure.

These ideas should remain in the research vision, not in the current acceptance criteria.

## E. Reporting discipline

Every claim must be labeled as one of:

- reproduced evidence;
- current implementation result;
- deterministic projection;
- human annotation;
- model inference;
- design judgment;
- future hypothesis.
