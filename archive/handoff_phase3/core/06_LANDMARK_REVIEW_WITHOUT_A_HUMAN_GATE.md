# 06 — Landmark Review Without a Human Gate

## 1. Review is evidence, not a hard gate

No independent human expert panel will be recruited.

Use a small, practical review protocol that combines:

- a compact user vibe-check;
- independent agent inspections where genuinely available;
- formal proxy labels from P4/P5/source evidence, clearly marked as proxies rather than human truth.

## 2. Preselected proof sample

Select a fixed, stratified sample from the existing 76-proof review bundle before inspecting topology-model outputs.

Recommended sample:

- 24 proofs total for machine/agent analysis, four per domain;
- a compact 12-proof user packet, two per domain, selected from the same manifest;
- the remaining proofs as reserve or disagreement cases.

Stratify across:

- term versus tactic proof;
- high versus low P3 infrastructure fraction;
- P4 result-inference success versus failure;
- simple versus large proof term;
- explicit named steps versus automation-heavy proof;
- examples with important local hypotheses or case/induction structure.

Record the seed, inclusion criteria, and exact manifest.

## 3. Two review questions

### Mathematical usefulness

Given the theorem statement and a candidate view, does the view surface the definitions, theorems, or constructions a mathematically informed reader would want to see?

### Certificate fidelity

After revealing the source proof and exact formal evidence, does the view preserve the important moves of this proof rather than merely plausible general mathematics?

These are different judgments and should not be collapsed.

## 4. Review presentation

For each proof, provide a compact packet containing:

- theorem statement and domain;
- proof-style metadata;
- raw P2 support;
- P3 classifications and residue;
- P4-route with explicit missing result-inference markers;
- P5 events when available;
- top-ranked nodes from each structural baseline and combined score;
- a concise local graph visualization or table only if it materially aids inspection;
- source proof revealed in the second section, not the first;
- a form for labels and missing conceptual/local moves.

Randomize or anonymize method names during pairwise usefulness rating where practical.

## 5. Reviewer provenance

Each review record must include:

- reviewer type: user, coding agent, reasoning agent, or proxy;
- model/agent identifier if available;
- prompt version;
- timestamp or run identifier;
- whether source proof was visible;
- confidence and free-text rationale.

Do not merge agent judgments into the verified core. Store them as review/semantic sidecar evidence.

## 6. Independent agent review

If the coding environment supports genuinely independent subagents or separate runs:

- run at least two independent review passes with identical blinded packets;
- prevent one reviewer from seeing the other’s outputs;
- preserve raw responses;
- compute agreement and disagreement.

If not supported, create ready-to-paste prompts and packets. Do not simulate or invent independent reviews.

## 7. Disagreement packet

Produce a short packet emphasizing:

- high-confidence structural machinery predictions that reviewers call landmarks;
- P3-unclassified declarations the structural model calls machinery;
- landmarks missed by every structural score;
- cases where P4-route is sparse because result inference failed;
- term proofs where P5 is absent;
- proofs whose key move is a local hypothesis, witness, case split, or representation change not captured by declaration ranking.

These cases are more informative than a gallery of successes.
