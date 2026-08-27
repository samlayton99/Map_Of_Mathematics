#!/bin/bash
# Run the Phase 2A study pass over the pinned Mathlib corpus.
# One extractor process per file (ADR-0001). LEAN_PATH comes from `lake env`
# inside the mathlib workspace so imports resolve to the pinned oleans.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ML="$ROOT/corpusenv/mathlib"
BIN="$ROOT/mathrecord/.lake/build/bin/mathrecord"
OUT="$ROOT/studies"
export PATH="$HOME/.elan/bin:$PATH"

FILES=(
  "Mathlib/Algebra/Group/Basic.lean"
  "Mathlib/Order/Lattice.lean"
  "Mathlib/Topology/Basic.lean"
  "Mathlib/Data/Nat/GCD/Basic.lean"
  "Mathlib/Logic/Function/Basic.lean"
  "Mathlib/Analysis/SpecialFunctions/Log/Basic.lean"
)

mkdir -p "$OUT"
cd "$ML"
for f in "${FILES[@]}"; do
  stem="$(echo "$f" | sed 's|Mathlib/||; s|/|_|g; s|\.lean$||')"
  out="$OUT/$stem.study.json"
  if [ -f "$out" ] && [ "${FORCE:-0}" != "1" ]; then
    echo "skip (exists): $stem"
    continue
  fi
  echo "== studying $f -> $out"
  /usr/bin/time lake env "$BIN" study "$f" "$out" --mathlib
done
echo "corpus study complete: $(ls "$OUT" | wc -l) files in $OUT"
