# 01 — Architectural Invariants

These points are settled for this phase and should be reflected in current-direction documentation.

## 1. One underlying heterogeneous verified structure

Preserve the hypothesis that there is one heterogeneous, typed, relational structure of verified mathematics beneath task-specific maps.

“Not one flat graph” does not mean “no unified mathematical object.” Exact declarations, theorem interfaces, proof artifacts, expressions, contexts, and typed relations remain linked in one verified substrate.

Graph views used in this study are derived projections of that substrate.

## 2. Dynamic formal applicability

Whether a theorem or definition can be used is a property of a current Lean state and an elaborated substitution or action.

Do not store a permanent global edge meaning “declaration d is applicable to theorem T.” Applicability remains dynamically generated and checked by Lean.

## 3. Separate workspace and optional sidecars

- Candidate conjectures, generated definitions, failed searches, and incomplete proof attempts belong in the workspace.
- Raw failed attempts may be retained there, but the experience corpus should contain sparse selected evidence judged useful for future retrieval or learning—not every failure by default.
- The experience corpus and semantic labels are optional downstream sidecars, not the structural foundation.

## 4. Broad definition generation

Future definitions may arise from:

- internal abstraction, compression, recurring proof patterns, or representation changes;
- external conceptual inspiration, scientific modeling, empirical applications, or imported human ideas.

Do not narrow the long-term definition story to graph-internal compression.

## 5. Evolving geometry

Adding a definition, theorem, proof, equivalence, or transport relation changes later navigation possibilities. The mathematical map is time-indexed and evolves with curation.

## 6. Real-world and application navigation remains a long-term goal

The present study concerns formal structural signal. It should not erase the longer-term goal of linking formal mathematics to scientific, engineering, economic, and other application domains through provenance-aware semantic relations.

## 7. Raw evidence survives every view

No classifier or graph score may delete or overwrite the exact record. All filtering must be reversible, scored, and attributable.
