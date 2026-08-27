# Map_Of_Mathematics — agent notes

Start with `README.md` (layout + how to run), `docs/CURRENT_RESEARCH_DIRECTION.md` (program state), `NEXT_RECOMMENDATION.md` (current step).

Operational essentials:
- Python: `~/venv/general_ml/bin/python` (never system python; venvs live outside iCloud).
- Lean: `cd mathrecord && lake build` (toolchain 4.33.0). Runs go through `tools/run_prover.sh` and execute inside `corpusenv/` via `lake env`.
- Max TWO concurrent `lake env` processes (~10GB each, 16GB machine). A background run killed with an empty log = OS memory pressure; check `memory_pressure -Q` and retry.
- `bigdata/` is gitignored and regenerable (`tools/extract_full_mathlib.sh`, ~15 min) — but traces (`traces_*`, `semtrace*`) took hours to extract; do not delete them.
- Results discipline: kernel-verify + `tools/proof_audit.py` every solved-count claim; budget-matched controls for search comparisons; historical reports are never rewritten (corrections via errata in `reports/`).
- Cycle reports are delivered to `~/Downloads/<name>-results.md` with accurate numbers and minimal interpretation.
