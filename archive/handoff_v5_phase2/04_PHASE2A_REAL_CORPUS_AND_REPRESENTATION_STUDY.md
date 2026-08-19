# Phase 2A — Real Corpus and Representation Study

## 1. Purpose

Move from the adversarial micro-corpus to real Mathlib and compare candidate proof representations before choosing a permanent MathMap ontology.

## 2. Corpus design

Select 500–2,000 declarations across at least four areas and 40–80 showcase proof artifacts.

The showcase set should deliberately include:

- short and long proofs;
- tactic and term proofs;
- explicit theorem applications;
- `simp`/automation-heavy proofs;
- typeclass-heavy proofs;
- rewrites;
- structural/constructor proofs;
- recursive and inductive proofs;
- proofs with recognizable mathematical lemmas;
- proofs dominated by infrastructure;
- a small number of exact same-statement alternative proofs where available.

## 3. Extraction invariants

- Preserve Gates 0–1 exact data.
- Preserve raw reference occurrences.
- Never overwrite raw data with filtered views.
- Record completeness and derivation method.
- Link every derived item to an exact expression/source location.

## 4. Per-proof outputs

For each showcase proof produce:

1. theorem type;
2. source excerpt;
3. exact proof-term size and structure summary;
4. type-reference list;
5. body-reference occurrence multiset;
6. deduplicated support set;
7. infrastructure-classified support view;
8. named application occurrence tree/DAG if recoverable;
9. explicit tactic/source use events if present;
10. one-level selective expansion examples;
11. all trust/completeness labels.

## 5. Quantitative characterization

Report by domain and proof style:

- exact extraction coverage;
- support-set size distribution;
- occurrence multiplicity;
- infrastructure fraction under each documented classifier;
- named-application extraction coverage;
- source-use-event coverage;
- term-size compression ratios;
- disagreement between support, applications, and source actions;
- number of candidate nodes after each projection;
- runtime and storage cost.

## 6. Human review

Automated metrics cannot establish whether a view is a good mathematical summary.

Create a blinded or at least structured review worksheet. For each proof, ask the reviewer to rate candidate views on:

- inclusion of the most helpful named hint;
- noise;
- missing key ideas;
- usefulness for reconstructing the proof;
- usefulness for understanding the proof;
- need for ordering/grouping;
- value of selective expansion.

Recommended rating scale: 1–5 plus free-text corrections.

If possible use at least two reviewers on a subset to assess agreement.

If human review is not available, explicitly leave usefulness unresolved.

## 7. Natural-language evidence

Docstrings, comments, textbook statements, blueprints, and future tagging-agent output may be used as auxiliary evidence, but not as unquestioned gold labels.

Record provenance and confidence.

## 8. Result

The output of Phase 2A is a comparison among candidate representations, not a declaration that one is the map.
