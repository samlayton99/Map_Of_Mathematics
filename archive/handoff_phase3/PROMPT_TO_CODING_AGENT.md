# Prompt to the Coding Agent

You are continuing the existing MathMap / MathRecord repository that produced Gates 0–1 and Phase 2. Read this package in the order listed in `README.md`, then inspect the repository’s current implementation, reports, ADRs, and `NEXT_RECOMMENDATION` before changing anything.

Implement **Phase 3: Structural Role and Landmark Separability** as a bounded, reproducible study over the existing exact record.

The primary research questions are:

> **A. Can topology identify formal machinery or infrastructure without names or semantic content?**
>
> **B. Once machinery is treated as a probabilistic, context-sensitive role rather than simply deleted, can topology improve the ranking of mathematical landmarks in individual proofs?**

Important constraints:

- Do not perform an architectural reset.
- Preserve one heterogeneous, typed, relational verified mathematical structure beneath task-specific views.
- Formal applicability remains state-dependent and dynamically checked by Lean; do not create permanent global applicability edges.
- Derive the primary library graph from raw P1/P0 evidence. Use P2 as an ablation. Do not use P3-filtered topology as the main input.
- P3 classifications may be targets, strata, and baselines, but never feature leakage.
- Run a strict topology-only track and a separate typed-formal-structure track. No declaration names, namespace tokens, source text, docstrings, theorem-text embeddings, or semantic labels in either primary track.
- Treat P3 labels as existing deterministic classifications, not unquestionable ground truth. Report class-specific results and ambiguity.
- Distinguish global infrastructure-like role from theorem-local salience. A globally infrastructure-like declaration can still be a key local move.
- Never hard-delete raw evidence. Filtering and downweighting must remain reversible.
- Start with interpretable methods: descriptive distributions, simple thresholds, regularized logistic regression, and shallow decision trees. A stronger non-interpretable model may be included only as a clearly labeled ceiling, not as the main conclusion. Do not begin with a GNN.
- Control for extraction-boundary artifacts and evaluate generalization by file/domain, not only random node splits.
- Human expert review is not a hard gate. Prepare a small user vibe-check packet and provenance-preserving independent-agent review packets. Run independent agent reviews only if the environment genuinely supports them; otherwise leave the packets ready. Do not fabricate reviews.
- Preserve historical Gate and Phase 2 reports unchanged. Reconcile current-direction documentation, ADRs, and `NEXT_RECOMMENDATION`, and add an explicit Phase 2 errata/corrections note where appropriate.

Produce the datasets, code, tests, reports, review packets, and updated current-direction documentation specified in `core/07_DELIVERABLES_ACCEPTANCE_AND_REPO_RECONCILIATION.md`.

The final report must answer honestly:

1. Which existing P3 infrastructure classes are structurally separable, and which are not?
2. How much of any apparent separability is explained by degree alone, extraction coverage, domain, or imported-node status?
3. Which global and theorem-local structural features characterize reviewed landmarks?
4. Does soft machinery downweighting plus local structural salience outperform raw support, P3 filtering, global centrality, and P4-route on the reviewed set?
5. What failed, what remains ambiguous, and what should be done next?

Do not claim that topology discovers “the core of mathematics” or that it identifies human conceptual importance unless the evidence supports that exact statement.
