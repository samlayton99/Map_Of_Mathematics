#!/bin/zsh
# Run a sequence of prover configs: run_prover.sh <tag:tasks:banks[:budget]> ...
set -e
export PATH="$HOME/.elan/bin:$PATH"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/corpusenv"
for spec in "$@"; do
  tag="${spec%%:*}"; rest="${spec#*:}"
  tasks="${rest%%:*}"; rest2="${rest#*:}"
  banks="${rest2%%:*}"
  budget="${rest2#*:}"
  [ "$budget" = "$banks" ] && budget=300
  lake env "$ROOT/mathrecord/.lake/build/bin/mathrecord" prove \
    "$ROOT/bigdata/ImportMathlib.lean" \
    "$ROOT/bigdata/$tasks" \
    "$ROOT/bigdata/prover_out_v2_$tag.jsonl" "$banks" "$budget" \
    > "$ROOT/bigdata/pv2_$tag.log" 2>&1
  echo "$tag: $(tail -1 "$ROOT/bigdata/pv2_$tag.log")"
done
