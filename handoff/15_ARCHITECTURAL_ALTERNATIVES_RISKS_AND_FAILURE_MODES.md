# Architectural Alternatives, Risks, and Failure Modes
## Status: RESEARCH SAFETY NOTE

This document exists to prevent the project from becoming attached to one elegant ontology.

---

# 1. Alternative representation families

The eventual best representation may be:

- declaration graph + text;
- proof-state text + retrieval;
- typed expression graph;
- named application DAG;
- source-level tactic sequence;
- semantic concept graph;
- learned latent representation with little explicit graph structure;
- hybrid formal graph + language model;
- dynamic retrieval over exact Lean objects without a persistent global map.

The current study should be open to all of these.

---

# 2. Ontological lock-in

Risk:

> A compelling conceptual model becomes a permanent schema before its utility is tested.

Mitigation:

- store exact Lean data;
- compute projections;
- treat map entities as views until evidence warrants permanence;
- use ADRs for promotion.

---

# 3. Compiler-artifact contamination

Raw dependencies may be dominated by:

- typeclass instances;
- coercions;
- recursors;
- equality infrastructure;
- generated declarations;
- elaborator necessities.

Mitigation:

- never delete raw evidence;
- classify/filter only in derived views;
- measure how much filtering changes conclusions.

---

# 4. Human-route reconstruction may be impossible from proof terms alone

A proof term can be formally exact while losing:

- author intent;
- tactical grouping;
- conceptual step boundaries;
- motivation.

Possible response:

- source-level traces;
- natural-language tagging;
- human annotations;
- learned grouping.

If heavy semantic annotation is required for every useful route, the value proposition of an automatically derived map weakens.

---

# 5. Support is not necessity

\[
d\in\operatorname{Supp}(p)
\]

means the selected certificate references \(d\).

It does not mean:

- \(d\) is necessary for theorem \(T\);
- every proof uses \(d\);
- \(d\) was conceptually central.

Never conflate certificate provenance with extensional logical dependence.

---

# 6. Formal zoom may not be semantic zoom

Opening a declaration into its body may produce more detail without more understanding.

A successful “Google Maps” experience may ultimately require learned or human conceptual boundaries rather than simple recursive dependency expansion.

---

# 7. Alternative proofs may be too sparse

The vision assigns high value to multiple proof routes.

Existing formal libraries often store only one certificate per named theorem.

The project may need:

- explicit alternative-proof registries;
- generated alternative proofs;
- paper/formalization alignments.

Do not make alternative-proof abundance an early prerequisite.

---

# 8. Strong language models may already learn the latent structure

A major null hypothesis is:

> A sufficiently capable transformer over text/Lean syntax already internalizes the useful relationships, and explicit graph structure adds little.

This must be tested fairly.

A hybrid model winning is not a failure; it may show that formal structure is complementary rather than primary.

---

# 9. Local navigation may not imply global discovery

Successful premise selection does not establish:

- good conjecture generation;
- useful definition invention;
- deep theory transport;
- curation judgment.

Treat every expansion of capability as a new empirical hypothesis.

---

# 10. Curation may be the hardest problem

Lean can verify:

\[
p:P.
\]

It cannot decide that \(P\) is:

- interesting;
- new;
- explanatory;
- worth naming;
- appropriately general;
- useful to future mathematics.

An autonomous generator without curation can create a formal junkyard.

---

# 11. Power-law / self-similarity overclaim

Heavy-tailed citation structure is plausible.

A pure universal power law is not established and is representation-dependent.

Do not use spectral or power-law rhetoric as evidence of the project's central thesis.

---

# 12. Building the platform before the result

Historical universal-math-repository projects show the danger of demanding expensive curation before delivering immediate value.

The current program should produce falsifiable results on borrowed Lean/Mathlib substrate before attempting a platform-scale ecosystem.

---

# 13. Success can still be incremental

Possible outcomes:

### Transformative
Explicit structure yields large transfer/search gains and supports learned abstraction/zoom.

### Important but incremental
MathRecord/MathMap becomes excellent theorem-navigation and training infrastructure but not a new paradigm.

### Tooling-only
Exact serialization/provenance is useful, but map/learning hypotheses fail.

All three outcomes are legitimate research outcomes.
