# mathrecord

Lean 4.33.0 extractor/validator for the MathRecord core (E,X,D,S + T spike). See `../SCHEMA.md`, `../reports/GATE_1.md`.

```
lake build
./.lake/build/bin/mathrecord extract  corpus/Adversarial.lean records/adversarial.json --spike
./.lake/build/bin/mathrecord validate corpus/Adversarial.lean records/adversarial.json adversarial
./.lake/build/bin/mathrecord alpha    records/adversarial.json records/adversarial_renamed.json
./.lake/build/bin/mathrecord inspect  records/adversarial.json Corpus.letTactic
./.lake/build/bin/mathrecord study  <file.lean> out.json --mathlib   # Phase 2 projections
./.lake/build/bin/gate0 spikes                # Gate 0 audit spike

# Proof-search program (run from ../corpusenv via ../tools/run_prover.sh):
./.lake/build/bin/mathrecord prove    <ImportMathlib.lean> <tasks.json> <out.jsonl> <banks> <budget>
./.lake/build/bin/mathrecord replay   <ImportMathlib.lean> <tasks.json> <out.jsonl> [neg]   # replay / legality traces
./.lake/build/bin/mathrecord semtrace <ImportMathlib.lean> <tasks.json> <out.jsonl>         # semantic action traces
```

Search modules: `Prover.lean` (best-first + guided descent + oracle modes), `Replay.lean` (replay, shadow tiers, legality probe), `Ho.lean` (mechanical higher-order application), `Semantic.lean` (certificate-region compression + simp execution).

One source file per process invocation (ADR-0001). `records/` are canonical sample outputs; regenerating them must be byte-identical.
