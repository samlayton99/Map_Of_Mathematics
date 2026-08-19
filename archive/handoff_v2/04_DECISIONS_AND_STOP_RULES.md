# Decisions, Non-Goals, and Stop Rules

## 1. Decisions

### Lean remains the verifier

The project builds on Lean's kernel and environment. It does not create a replacement logic or trusted checker.

### Audit before schema

The v0.1 schema must be reduced or modified after inspecting current Lean APIs and trace tools. Existing exact representations should be wrapped or indexed rather than duplicated without reason.

### One exact core, many projections

Dependencies, proof routes, and map views must be reproducible from the exact core. Caches are permitted; contradictory truth stores are not.

### Static fidelity before dynamic tracing

The current run validates declarations, expressions, contexts, and goals before building a large transition dataset. A transition-access spike is required, but replay infrastructure is Gate 2.

### Structural plus text is a first-class baseline

The project should not assume that structure replaces language. The likely strongest system may be hybrid.

### Held-out transfer matters more than random-split gains

Random splits can reward local memorization. The central learning hypothesis concerns reusable structure, so held-out module, domain, and time tests are required.

### Negative results are deliverables

A faithful representation that fails to improve learning is still a useful finding. It should prevent premature expansion.

## 2. Immediate non-goals

Do not build in the current Gate 0–1 run:

- a full proof-transition or replay dataset;
- representative or all-Mathlib extraction;
- a universal ontology of mathematical concepts;
- autonomous conjecture generation;
- definition invention;
- learned curation;
- theory-morphism mining;
- informal-math alignment at web scale;
- a production graph platform;
- a polished public UI;
- a premise-selection or theorem-proving model;
- a new theorem prover kernel;
- a claim that the object represents all human mathematical meaning.

## 3. Stop rules

### Stop after Gate 0 if

- exact declarations, local contexts, or targets cannot be accessed reliably;
- necessary data requires fragile parsing of display strings;
- completed terms cannot be connected back to Lean checking;
- existing tooling already provides the complete needed object and the project has no distinct experiment.

In the last case, pivot to using the existing representation rather than rebuilding it.

### Stop after Gate 1 if

- exact expression/context identity cannot be made deterministic;
- fidelity depends on pretty-print matching;
- unsupported constructs are silently dropped;
- context, binder, universe, or local-definition information is lost;
- completed artifacts cannot be related back to Lean verification.

### Stop after Gate 2 if

- state transitions depend on unstable process state that cannot be normalized;
- successful routes cannot be replayed or related to checked terms;
- failure traces cannot be represented honestly;
- the tracing layer requires changing Lean's trusted semantics.

### Stop after Gate 3 if

- the object only works on toy examples;
- real-corpus failures are widespread or unclassifiable;
- environment/version sensitivity makes records uninterpretable;
- extraction cost makes later experiments infeasible.

### Stop or reframe after Gate 4 if

- useful views require a separate hand-built ontology rather than projections of the core;
- expand/collapse loses identity or provenance;
- the object adds no navigational value beyond existing Lean tools.

### Stop the grand ML thesis after Gate 5 if

- structural and hybrid models do not beat a well-tuned text baseline on held-out mathematics;
- gains appear only under random splits;
- gains vanish under leakage controls or anonymization;
- the effect is too small to justify the representation cost.

A negative Gate 5 does not forbid a useful navigation product. It blocks confident claims about a new mathematical learning substrate.

## 4. Anti-goals

The project should actively avoid:

- naming a speculative architecture as if the name proves it is correct;
- building storage before understanding the source data;
- measuring graph centrality and interpreting it as mathematical importance without validation;
- treating one chosen proof's dependencies as the theorem's intrinsic dependencies;
- treating model similarity as theorem equivalence;
- treating kernel validity as semantic fidelity or importance;
- using the number of generated theorems as success;
- adding features because they fit the vision rather than because a gate requires them;
- continuing after a failed gate by adding complexity.

## 5. Evidence language

Use these terms consistently:

- **Implemented:** code exists and was run.
- **Validated:** written acceptance tests passed.
- **Positive evidence:** a predeclared experiment materially supports a hypothesis.
- **Strong evidence:** the effect is large, robust, and survives held-out evaluation.
- **Speculation:** plausible but not empirically established.

Do not write “the representation of mathematics” in technical reports. Write “the tested Lean-native record” unless the claim has been carefully scoped.
