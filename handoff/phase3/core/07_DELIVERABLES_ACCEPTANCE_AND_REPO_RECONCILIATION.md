# 07 — Deliverables, Acceptance Criteria, and Repository Reconciliation

## 1. Required repository outputs

Use the repository’s conventions, but create an equivalent of:

```text
studies/phase3_structural_separability/
  README.md
  config.*
  data/
    node_inventory.*
    edge_inventory.*
    feature_matrix_strict.*
    feature_matrix_typed.*
    labels_p3.*
    landmark_sample_manifest.*
    rankings.*
  scripts-or-src/
  tests/
  reports/
    DATA_AND_GRAPH_AUDIT.md
    MACHINERY_SEPARABILITY.md
    LANDMARK_STRUCTURE_AND_RANKING.md
    DISAGREEMENT_AUDIT.md
    HONEST_ASSESSMENT.md
  review/
    user_packet/
    agent_packet/
    response_schema.*
    prompts/
```

Exact filenames may differ, but every listed function must exist.

## 2. Minimum tests

- deterministic graph construction on repeated runs;
- counts reconcile with P1/P2 source data;
- identifier-renaming invariance for strict topology features;
- no P3 or name/text leakage into strict features;
- grouped split integrity;
- target-defining metadata excluded from corresponding class model;
- raw and historical Phase 2 artifacts unchanged;
- missing P4 result inference is explicit;
- every review and semantic judgment carries provenance.

## 3. Required final reports

### Data and graph audit

Explain graph construction, coverage, boundary effects, components, acyclicity/SCCs, and target populations.

### Machinery separability

Answer Question A with broad and class-specific metrics, grouped holdouts, degree/boundary controls, interpretable feature effects, and disagreement cases.

### Landmark structure and ranking

Answer Question B with theorem-local feature analysis, baseline comparisons, reviewed examples, and limitations.

### Honest assessment

State:

- what was established;
- what was only reproduced from P3;
- what remains a proxy;
- what failed;
- whether topology should be used as a primary map signal, a soft infrastructure prior, or only a diagnostic;
- the single recommended next step.

## 4. Acceptance criteria

The phase is complete when:

- the study is reproducible by one documented command or short sequence;
- raw exact evidence and historical reports remain intact;
- strict topology and typed-structure tracks are both present;
- extraction-boundary confounds are measured rather than ignored;
- results include domain/file holdouts and degree-matched controls;
- landmark evaluation includes at least prepared independent-agent packets and a compact user packet;
- no conclusion depends only on a random node split;
- no conclusion treats P3 as unquestionable ground truth;
- no model silently deletes nodes;
- negative and limiting results are reported.

## 5. Repository documentation reconciliation

Historical Gate 0–1 and Phase 2 reports are records of what was reported at the time. Do not rewrite them.

Instead:

1. Inventory the repository’s README/current-direction docs, ADRs, handoff files, and `NEXT_RECOMMENDATION`.
2. Add or update a clearly current direction document to state that Phase 3 is the structural role/landmark separability study.
3. Add a Phase 2 errata/corrections note containing the three known corrections.
4. Update `NEXT_RECOMMENDATION` before implementation to the approved Phase 3 study, then update it after results to the evidence-based next recommendation.
5. Preserve existing ADRs. Add a superseding/current ADR only where needed; do not rewrite history.
6. Ensure current docs preserve the architectural invariants in `core/01_ARCHITECTURAL_INVARIANTS.md`.
7. Remove or correct current prose that claims:
   - universal P5/P4/P2 containment;
   - a 76% term-proof fraction;
   - overwhelming P4 result-type inference success;
   - human validation that did not occur;
   - selection of a canonical primary map before this study.

## 6. No premature schema promotion

Graph features, learned machinery probabilities, community assignments, and landmark scores are derived study artifacts.

Do not promote them to permanent core schema without a separate decision and ADR after reviewing the evidence.
