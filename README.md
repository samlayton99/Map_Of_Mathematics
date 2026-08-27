# Map of Mathematics — MathRecord / MathMap

Research program: a navigable, verified map of formal (Lean/Mathlib) mathematics. Lean is the verifier; one typed relational structure underlies all views (ADR-0003). Current focus: **typed proof search over live Lean proof states**, measured against reference proofs.

## Current program (branch `study-paths`)

Best-first search inside the elaborator (`mathrecord/Mathrecord/Prover.lean`), with reference-proof-guided oracle ladders that attribute failures to specific engine components. State as of 2026-08-27:

- **Exact replay** of reference proofs through the engine's unification: 380/380 theorems, 8,252/8,252 nodes.
- **G1 (exact route oracle)**: 80/80 on the held-out benchmark, audit-clean.
- **Higher-order application operator** (`Ho.lean`): reference-action visibility 71.8% → 88.4%; legal-action set stays ~5/state (conditional sparsity).
- **Semantic action layer** (`Semantic.lean`): simp/congruence certificate regions compressed to single rewrite actions (3k-set: 29,393 actions vs 66,940 certificate nodes). Semantic ladder: representability 80/80; mechanical execution 64–73/80; free search + semantic hint 65/80 vs 30 control.
- **Ranker v3** (`tools/assembler_v3.py`): 29,585/1,046 decisions, top-1 0.645, MRR 0.786 vs 0.353 best hand rule.

Direction and next step: `docs/CURRENT_RESEARCH_DIRECTION.md`, `NEXT_RECOMMENDATION.md`. Detailed cycle reports are delivered to `~/Downloads/*-results.md` (not tracked here).

## Running

```bash
cd mathrecord && lake build                                   # build engine (Lean 4.33.0)
tools/extract_full_mathlib.sh                                 # regenerate bigdata/ dumps (~15 min)
tools/run_prover.sh <tag>:<tasks.json>:<banks>[:<budget>]     # prover runs -> bigdata/prover_out_v2_<tag>.jsonl
~/venv/general_ml/bin/python tools/proof_audit.py <out.jsonl>:<tasks.json>   # source-cleanliness audit
```

Bank chars: free banks `s`tructural `b`ackward `r`ewrite `h`yp `p` simp; guided modes `1`=G1 `2`=G2 `3`=G3 `c`=data-oracle `S`=sem-exact `X`/`Y`=sem-simp with/without data oracle `Z`=free+sem-hint; `f`=fallback, `o`=residual oracle. Max TWO concurrent `lake env` runs (~10GB each; OOM-killed under memory pressure — just retry).

## Layout

- `mathrecord/` — Lean engine: `Extract/Validate/Study` (Gates 0–1 record), `Prover/Replay/Ho/Semantic` (search program), CLI in `Main.lean`.
- `tools/` — Python pipeline: `atlas.py` (shared lib) + task generation (`support_tasks`, `train_tasks`, `rolodex2`), analysis (`replay_analysis`, `semtrace_analysis`, `semladder_analysis`, `prover_analysis`), audit (`proof_audit`), ranker (`assembler_v3`).
- `bigdata/` (gitignored, regenerable) — Mathlib dumps, task files, traces, run outputs, models.
- `corpusenv/` (gitignored) — pinned Mathlib checkout; runs execute via `lake env` here.
- `docs/` — definitions, corpus selection, current direction, `notebook/` long-term ideas.
- `decisions/` — ADR-0001 wrap-Lean; ADR-0002 characterize-before-ontology; ADR-0003 structural invariants.
- `reports/` — historical gate/phase reports (never rewritten; corrections via errata) + superseded recommendations.
- `sources/` — original vision conversation and ecosystem audit.
- `studies/phase5_multiscale_navigation/` — parallel line of work (from `main`): multiscale navigation, connected filtration, evaluation suite, keyness panels; its phase-3/4 predecessors live in `archive/studies/`.
- `viz/` — WebGL corpus-map prototype (reads archived phase-3 data; `build_data.py` regenerates `data.js`).
- `archive/` — superseded phases: phase-2 tooling/review, phase-3 handoff and studies, old handoffs, one-off tool outputs.
- `learning/` (untracked) — personal scratch, unrelated to the program.

`NEXT_RECOMMENDATION.md` always holds the current approved step; superseded ones move to `reports/`.
