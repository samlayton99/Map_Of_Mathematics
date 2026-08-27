# 02 — Research Questions and Decision Logic

## Central distinction

The word “machinery” can refer to at least two things:

1. a declaration’s **global formal role** in the library, such as coercion, generated helper, typeclass plumbing, recursor, or equality transport;
2. a declaration occurrence’s **local salience** in one proof.

These are not identical. A recursor or equality theorem can be globally infrastructure-like yet locally be the central mathematical move.

The study must model both levels.

## Question A — Structural role separability

### A1. Broad P3 separability

Can no-name graph features predict whether a declaration receives any existing P3 infrastructure classification?

This is a test of recoverability of an existing deterministic labeling scheme, not proof that the scheme equals human truth.

### A2. Class-specific separability

Which overlapping P3 classes are structurally distinctive?

- typeclass instance;
- recursor;
- structure projection;
- generated;
- internal detail;
- equality machinery;
- logic core;
- coercion.

Report each class separately. Do not collapse them without also showing class-wise results.

### A3. Beyond degree and extraction artifacts

Does separability remain after controlling for:

- unique and weighted degree;
- stored versus shallow declaration coverage;
- imported-node status or equivalent extraction boundary;
- file/domain;
- highly repeated generated declaration families?

### A4. Disagreement audit

What do high-confidence topology/P3 disagreements reveal?

Possibilities include:

- classifier errors;
- label ambiguity;
- topology identifying a distinct structural role;
- extraction artifacts;
- mathematically important infrastructure.

Produce a small disagreement packet rather than silently forcing a label.

## Question B — Landmark separability

### B1. Landmark is not the complement of machinery

Among declarations involved in a theorem’s proof, can theorem-local and global structural features distinguish:

- key mathematical landmarks;
- useful supporting mathematics;
- formal scaffolding/noise;
- unclear or context-dependent items?

### B2. Does soft downweighting help?

Compare raw support and existing projections with a score that combines:

- probability of global infrastructure-like role;
- theorem-local salience;
- exact occurrence role;
- local/global importance.

A simple schematic is acceptable:

\[
\operatorname{score}(v,T)
=
\operatorname{localSalience}(v,T)
-
\lambda\operatorname{machineryProbability}(v),
\]

but do not assume this exact linear form is optimal. Preserve interpretable components and report them separately.

### B3. What structural signatures do landmarks have?

Test hypotheses such as:

- high local but moderate global centrality;
- bridge position between communities;
- low distance from the proof root or a major branch point;
- high proof-subgraph coverage;
- occurrence in statement/type relationships rather than only certificate plumbing;
- explicit application-head role;
- high local/global centrality ratio.

These are candidate hypotheses, not required findings.

## Decision rules

### Continue topology as a serious map component if

- structure-only models outperform degree-only and prevalence baselines under grouped, cross-domain evaluation;
- the effect is not explained primarily by extraction coverage;
- and soft structural ranking improves landmark quality or noise reduction on the reviewed set relative to P3/P4 baselines.

### Retain topology only as an infrastructure diagnostic if

- Question A succeeds but Question B does not.

In that case topology may help clean or characterize formal records without identifying mathematical landmarks.

### De-emphasize topology as a primary signal if

- separability collapses under domain holdout or coverage controls;
- or landmark ranking shows no consistent gain over simpler projections.

The exact record still remains valuable.

### Change the conceptual model if

- reviewers consistently identify globally “infrastructure-like” nodes as key local moves;
- or landmark labels have low agreement because different tasks require different maps.

That would favor task-conditioned structural roles rather than one global machinery/content partition.
