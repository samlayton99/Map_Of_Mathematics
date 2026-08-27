#!/bin/zsh
# Full-Mathlib dependency extraction: toolchain -> Mathlib olean cache ->
# mathrecord exe -> depdump over `import Mathlib` (771k constants).
# Output: bigdata/mathlib_deps.jsonl (gitignored; multi-GB).
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$HOME/.elan/bin:$PATH"

mkdir -p "$ROOT/bigdata"

echo "=== [1/4] corpusenv: fetch deps + Mathlib olean cache ==="
cd "$ROOT/corpusenv"
lake exe cache get
echo "=== corpusenv: lake build ==="
lake build

echo "=== [2/4] mathrecord: lake build ==="
cd "$ROOT/mathrecord"
lake build

echo "=== [3/4] depdump over import Mathlib ==="
echo "import Mathlib" > "$ROOT/bigdata/ImportMathlib.lean"
cd "$ROOT/corpusenv"
time lake env "$ROOT/mathrecord/.lake/build/bin/mathrecord" depdump \
  "$ROOT/bigdata/ImportMathlib.lean" "$ROOT/bigdata/mathlib_deps.jsonl"

echo "=== [4/4] done ==="
ls -lh "$ROOT/bigdata/mathlib_deps.jsonl"
wc -l "$ROOT/bigdata/mathlib_deps.jsonl"
