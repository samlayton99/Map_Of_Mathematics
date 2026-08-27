# MathMap / MathRecord — Coding-Agent Handoff

## Phase 3: Structural Role and Landmark Separability

This package specifies the next bounded empirical study for the existing MathRecord repository.

It is for the coding agent that implemented Gates 0–1 and Phase 2. It is not an invitation to redesign the architecture or start a new implementation.

## Objective

Use the existing exact, unfiltered MathRecord evidence to test two linked questions:

1. **Can graph structure identify formal machinery or infrastructure without using declaration names, source text, documentation, or semantic embeddings?**
2. **After machinery is treated as a soft structural role rather than blindly removed, can graph structure help rank the mathematical landmarks that matter in individual proofs?**

The point is to learn whether topology contains useful signal. A coherent graph-theoretic story is not itself a result.

## Reading order

1. `core/00_ROLE_AND_SCOPE.md`
2. `core/01_ARCHITECTURAL_INVARIANTS.md`
3. `core/02_RESEARCH_QUESTIONS_AND_DECISION_LOGIC.md`
4. `core/03_GRAPH_CONSTRUCTIONS_AND_DATA_AUDIT.md`
5. `core/04_FEATURES_LABELS_AND_LEAKAGE_CONTROLS.md`
6. `core/05_MODELS_EVALUATION_AND_ABLATIONS.md`
7. `core/06_LANDMARK_REVIEW_WITHOUT_A_HUMAN_GATE.md`
8. `core/07_DELIVERABLES_ACCEPTANCE_AND_REPO_RECONCILIATION.md`

Then consult:

- `reference/PHASE2_FACTS_AND_CORRECTIONS.md`
- `reference/REASONING_DECISION_CONTEXT.md`

The exact task prompt is in `PROMPT_TO_CODING_AGENT.md`.

## Core instruction

Do not use P3-filtered output as the graph on which the primary topology test is run. Derive graph features from the raw exact record—primarily P1/P0—and use P3 classifications only as labels, strata, or baselines.

Do not hard-delete predicted machinery. Preserve the raw graph and test reversible filtering or soft downweighting.
