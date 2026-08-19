# Evaluation and Decision Rules

## 1. Why construction is not success

The project can always create a graph from Lean constants. The research question is whether any candidate projection corresponds to a useful and recoverable mathematical abstraction level.

## 2. Pre-registered decision dimensions

### Formal fidelity

Can every displayed exact item be traced to Lean?

### Recoverability

What fraction of real proofs support the candidate representation without ambiguity?

### Human usefulness

Do competent reviewers find the view informative as a proof hint or explanation?

### Compression

Does the view reduce complexity without discarding the named tools judged important?

### Robustness

Does it work across domains, tactic styles, term proofs, and automation?

### Incremental value

Does it add information beyond a plain direct dependency set or source text?

## 3. No fake precision

Do not set arbitrary numerical thresholds and then treat them as laws. Report confidence intervals and qualitative failure classes.

However, the following are hard constraints:

- exact-labeled data must have zero known silent provenance errors;
- unsupported and ambiguous cases must be explicit;
- use events labeled explicit/deterministic must have very high manual precision;
- human usefulness cannot be claimed without human evaluation;
- semantic labels cannot be treated as Lean-certified.

## 4. Outcome A — choose a candidate representation

Recommend proceeding only if:

- one or a hybrid of the candidate views is recoverable on a substantial and diverse portion of the corpus;
- its limitations are understood;
- human review indicates it is more useful than raw dependency output;
- use-event extraction or theorem-level labels provide a plausible next learning task.

## 5. Outcome B — another bounded study

Choose this if:

- candidate views are promising but human evidence is sparse;
- filtering or attribution requires refinement;
- one proof style dominates the result;
- the best representation appears hybrid but is not yet characterized.

## 6. Outcome C — stop the map-centered program

Choose this if:

- candidate maps are mostly restatements of existing dependency extraction;
- human-scale routes cannot be recovered without heavy semantic annotation;
- selective expansion adds little;
- use-event coverage is too low to support navigation;
- the proposed ontology creates more complexity than information.

MathRecord may remain useful exact tooling even under this outcome.

## 7. Future navigation experiment

Only after selecting a candidate representation should the project test:

\[
(\Gamma,A)\mapsto \text{rank useful declarations}.
\]

Compare:

- text;
- flat dependencies;
- selected structural representation;
- usage history;
- hybrid.

Use cross-domain and module-separated splits.
