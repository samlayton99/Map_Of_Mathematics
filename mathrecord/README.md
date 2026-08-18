# mathrecord

Lean 4.33.0 extractor/validator for the MathRecord core (E,X,D,S + T spike). See `../SCHEMA.md`, `../reports/GATE_1.md`.

```
lake build
./.lake/build/bin/mathrecord extract  corpus/Adversarial.lean records/adversarial.json --spike
./.lake/build/bin/mathrecord validate corpus/Adversarial.lean records/adversarial.json adversarial
./.lake/build/bin/mathrecord alpha    records/adversarial.json records/adversarial_renamed.json
./.lake/build/bin/mathrecord inspect  records/adversarial.json Corpus.letTactic
./.lake/build/bin/gate0 spikes                # Gate 0 audit spike
```

One source file per process invocation (ADR-0001). `records/` are canonical sample outputs; regenerating them must be byte-identical.
