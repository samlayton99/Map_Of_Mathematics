#!/bin/bash
# Final global-map run against the REBUILT phase5 arrays.
# Re-runs Task 1 (edge admission) and Task 3 (analyses), then writes the report.
#
# DO NOT RUN until the phase5 rebuild has finished writing all of
#   nodes.npz incid.npz artifacts.npz depth_scc.npz names.json
# The guard below only checks that the files exist, not that they are complete.
#
#   bash src/run_final.sh                  # default: rebuilt phase5 data
#   bash src/run_final.sh /path/to/data    # explicit data directory
#   SKIP_LPA=1 bash src/run_final.sh       # skip the second community algorithm
#
# Runtime on the smoke data: ~4s edges, ~23min analyses (Louvain dominates),
# ~11min for the LPA cross-check. Everything logs to logs/final_*.log.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA="${1:-$ROOT/../phase5_multiscale_navigation/data}"
PY="$HOME/venv/general_ml/bin/python"
OUT="$ROOT/data/map_final"

export MAPGRAPH_DATA_DIR="$DATA"
export MAPGRAPH_OUT_DIR="$OUT"
export MAPGRAPH_MODULES_TSV="${MAPGRAPH_MODULES_TSV:-/Users/sam/mathmap_data/all_modules.tsv}"

mkdir -p "$ROOT/logs" "$OUT"

for f in nodes.npz incid.npz artifacts.npz depth_scc.npz names.json; do
  [ -f "$DATA/$f" ] || { echo "MISSING $DATA/$f -- rebuild not complete"; exit 1; }
done
[ -f "$MAPGRAPH_MODULES_TSV" ] || echo "WARN: no module table; all areas will be Unknown"

echo "data dir : $DATA"
echo "out dir  : $OUT"
echo "modules  : $MAPGRAPH_MODULES_TSV"

echo "=== Task 1: edge admission"
"$PY" "$ROOT/src/map_graph.py" 2>&1 | tee "$ROOT/logs/final_map_graph.log"

echo "=== Task 1 check: brute-force reference on 400 random artifacts"
"$PY" "$ROOT/src/check_map_graph.py" 2>&1 | tee "$ROOT/logs/final_check.log"

echo "=== EL0 budget sensitivity"
"$PY" "$ROOT/src/el0_sensitivity.py" 2>&1 | tee "$ROOT/logs/final_el0_sens.log"

echo "=== Task 3: analyses (Louvain communities)"
"$PY" "$ROOT/src/map_analysis.py" 2>&1 | tee "$ROOT/logs/final_map_analysis.log"

ALT=""
if [ "${SKIP_LPA:-0}" != "1" ]; then
  echo "=== Task 3 cross-check: same analyses with label-propagation communities"
  mkdir -p "$ROOT/data/map_final_lpa"
  cp "$OUT"/edges_*.npz "$OUT/owner.npy" "$ROOT/data/map_final_lpa/"
  MAPGRAPH_OUT_DIR="$ROOT/data/map_final_lpa" MAP_COMMUNITY_METHOD=lpa \
    "$PY" "$ROOT/src/map_analysis.py" 2>&1 | tee "$ROOT/logs/final_map_analysis_lpa.log"
  ALT="$ROOT/data/map_final_lpa/map_analysis.json"
fi

echo "=== report"
MAP_ALT_ANALYSIS_JSON="$ALT" "$PY" "$ROOT/src/map_report.py" \
  "$OUT/map_analysis.json" "$OUT/edge_stats.json" \
  "FINAL - rebuilt phase5 arrays, corrected in_stmt_world flag" \
  > "$ROOT/MAP_STRUCTURE_RESULTS_FINAL.md"

echo "=== done"
echo "edges     : $OUT/edges_{E4,EL0,E4_flat}.npz"
echo "edge stats: $OUT/edge_stats.json"
echo "analyses  : $OUT/map_analysis.json"
echo "report    : $ROOT/MAP_STRUCTURE_RESULTS_FINAL.md"
echo
echo "The report's 'What the numbers say' / 'Caveats' prose is NOT regenerated;"
echo "MAP_STRUCTURE_RESULTS.md (smoke) keeps the hand-written interpretation."
