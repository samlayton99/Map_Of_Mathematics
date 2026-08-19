# Phase 2A — Representation Characterization

> *Erratum 2026-08-19: three claims in the Phase 2 reports are corrected in [`PHASE2_ERRATA.md`](PHASE2_ERRATA.md) (non-universal P5-in-P2 containment; 68.9% term-proof fraction; 61.4% P4 result-inference success). Body below unchanged.*


Date: 2026-08-18. Corpus: 6 Mathlib files (v4.33.0), six areas — see `docs/CORPUS_SELECTION.md`. Definitions: `docs/REPRESENTATION_DEFINITIONS.md`. Data: `studies/*.study.json` (310MB, regenerate deterministically with `analysis/run_corpus.sh`), aggregates in `studies/characterization.json`. Claim labels per `handoff/02` §E.

## Corpus scale (implementation result)

1,711 stored declarations with proof bodies + 3,493 referenced shallow declarations = **5,204 backing declarations** (target was 500–2,000; exceeded because reference closures are large — bounded but generous). 1,233 showcase-candidate theorems/defs; 1,303 exact local states (8 = 0.6% classified unsupported, all "fvar outside goal context" from delayed assignments); 4,827 observed transitions; 0 elaboration errors; 0 P4 walker failures. Runtime 2–13s per file. Determinism: two clean study runs of a Mathlib file are byte-identical (deterministic projection, verified).

Proof styles (derived from observed events): term 850, automation 168, rewrite 180, tactic-other 27, induction 8. Mathlib's showcase population is term-proof-dominant; per-style medians are reported so this doesn't silently bias conclusions.

## Headline table (medians per file; deterministic-derived)

| file | stored | showcase | ref-infra% | P2 med (infra%) | P4 med | P4-route med | P5 ev (attr) | c(P2) | c(P4) |
|---|---|---|---|---|---|---|---|---|---|
| Algebra_Group_Basic | 530 | 445 | 37% | 24 (71%) | 228 | 3 | 234 (164) | 0.022 | 0.192 |
| Analysis_…_Log_Basic | 178 | 119 | 42% | 34 (65%) | 265 | 4 | 184 (142) | 0.052 | 0.432 |
| Data_Nat_GCD_Basic | 76 | 52 | 39% | 18 (64%) | 151 | 2 | 69 (55) | 0.037 | 0.344 |
| Logic_Function_Basic | 347 | 270 | 32% | 6 (29%) | 7 | 1 | 101 (73) | 0.055 | 0.095 |
| Order_Lattice | 514 | 300 | 48% | 11 (60%) | 23 | 1 | 136 (83) | 0.082 | 0.155 |
| Topology_Basic | 66 | 47 | 36% | 10 (35%) | 22 | 2 | 36 (32) | 0.068 | 0.183 |

c(Pi) = median projection size / proof-term node count. P4-route = P4 filtered to Prop-resulting spines with unclassified (domain) heads.

## Findings

**F1. Raw support (P2) is substantially infrastructure, and it varies by domain 2.5×.** Median infrastructure fraction of body support ranges from 29% (logic) to 71% (algebra) — the algebra/analysis files pay a heavy typeclass/coercion/`OfNat` tax. The "support may be dominated by machinery" concern (`handoff/01` §2) is confirmed for algebraic domains and refuted for plain-logic domains. [deterministic projection]

**F2. The filtered classifications are cheap and effective.** Eight deterministic, reversible classifiers (instance table, projection table, recursors, generated suffixes, internal details, eq-machinery, logic-core, coercion roots) separate the support sets cleanly: in the showcase bundle the P3 "domain" residue reads as mathematical content (e.g. `Nat.Coprime.mul_add_mul_ne_mul`: 23 domain lemmas vs 42 classified infrastructure, and the domain list is a plausible proof hint). [implementation result + design judgment; usefulness not human-validated]

**F3. Raw P4 is huge; filtered P4-route is small and route-shaped.** Raw application occurrences (median 7–265 per proof) are dominated by type-level scaffolding. Filtering to Prop-resulting spines with domain heads collapses this to a median of **1–4 named steps** per proof, and on inspected examples the result is ordered, nested, relation-labeled (`Dvd.dvd`, `Iff`, `Eq`, `False`) and reads like the proof's skeleton (see `review/Data_Nat_GCD_Basic/Nat.Coprime.mul_add_mul_ne_mul.md`). This filtered view is the strongest new candidate to emerge: it exists for term proofs (82% of showcase candidates), where P5 is empty by definition. [deterministic projection; "route-shaped" is engineer judgment pending human review]

**F4. Projections are mutually consistent.** Every P5-attributed declaration and every P4 head occurs in the P2 support of the same proof (containment 1.0 across all six files) — the three views are refinements of one another, not competing stories. Disagreement lives only in *granularity* (multiplicity, order, nesting, roles). [deterministic-derived]

**F5. Compression.** P2 compresses proof terms to 2–8% (set of names), P4 to 10–43% (occurrence structure), P4-route to well under 1% in large proofs. All views keep exact provenance (expr ids, paths) back to the record. [deterministic-derived]

**F6. Automation sensitivity is real but classified.** Automation-heavy styles show the highest infra fractions and the lowest P5 attribution (simp 57%, simp_all 20%); `nonFamilyTacticKinds` tallies the uncovered tactic volume per file. Nothing is silently dropped. [deterministic-derived]

**F7. What is not recoverable.** Conceptual grouping ("reduce to the finite case"), motivation, and step boundaries of the author's mental proof are absent from every projection — P4-route gives the formal skeleton, not the narrative. One concrete loss surfaced: rewrite-rule attribution inside structure-literal `where`-proofs loses its TermInfo (classified `no-named-attribution`, ~29 events). [reproduced evidence for the loss; the "narrative" gap is design judgment]

## Human review status

**No human review was performed in this run.** The 76-proof review bundle (`review/`, stratified small/median/large × style × file) and worksheet (`review/WORKSHEET.md`) are ready; usefulness claims are explicitly deferred until it is filled in. The optional diagnostic viewer was skipped — the markdown bundle covers side-by-side inspection for this bounded run.
