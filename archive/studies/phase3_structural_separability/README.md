# Phase 3 — Structural Role and Landmark Separability

Bounded study per `handoff/phase3/` (ADR-0003). Raw evidence: the Phase 2 study JSONs (`../*.study.json`, regenerable via `analysis/run_corpus.sh`). Nothing here modifies the exact record.

## Reproduce

```
PY=~/venv/general_ml/bin/python           # numpy pandas scikit-learn networkx scipy pytest
cd src
$PY build_graph.py                        # data/node_inventory.csv, edge_inventory.csv
$PY features.py                           # strict + typed feature matrices
$PY audit.py                              # data/audit.json
$PY models_qa.py                          # data/qa_results.json  (Question A, ~4 min)
$PY ablations.py                          # data/ablations.json
$PY landmark.py                           # data/landmark_sample_manifest.json, rankings.json
$PY review_packets.py                     # review/{agent_packet,user_packet,prompts,...}
cd ../tests && $PY -m pytest -q           # 9 tests: determinism, reconciliation,
                                          # renaming invariance, leakage, split integrity,
                                          # historical-artifact immutability, missingness
```

Config: seed 20260819 everywhere; graph/model parameters at the top of each script; λ=1 in `landmark.py`.

## Outputs

- `data/` — inventories, feature matrices, QA results, ablations, rankings, disagreements.
- `reports/` — DATA_AND_GRAPH_AUDIT, MACHINERY_SEPARABILITY, LANDMARK_STRUCTURE_AND_RANKING, DISAGREEMENT_AUDIT, HONEST_ASSESSMENT.
- `review/` — blinded packets (24 agent / 12 user), reviewer prompt + response schema, two completed independent agent responses with provenance, method keymap (do not show reviewers), `review_summary.json`.

## Headline results

Typed-structure machinery detection AUC 0.80 under domain holdout (0.86 degree-matched); strict topology modest (0.76 best variant); typeclass-instance 0.97. Landmark ranking: hybrid (route/events first, topology tie-break) rated 4.1/5 by two independent agent reviewers; the pure soft-downweight score failed its pre-registered condition. Verdict: topology = calibrated soft infrastructure prior + diagnostic, not a primary map signal. Details and caveats in `reports/`.
