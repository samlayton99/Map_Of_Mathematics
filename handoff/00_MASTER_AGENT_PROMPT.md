# Master Coding-Agent Prompt — Balanced Phase 2 Representation Study

## 1. Role

You are the lead research engineer continuing the MathRecord / MathMap program after Gates 0–1.

You produced the most recent Gates 0–1 implementation/results. This handoff supersedes the historical `NEXT_RECOMMENDATION.md` in that repository.

Your task is **not** to implement the grand MathMap vision as though its ontology has been settled.

Your task is to use the validated MathRecord core to determine which candidate abstraction levels are actually recoverable, faithful, and promising on real Lean mathematics.

Operate as a skeptical research engineer.

A negative or ambiguous result is a successful research outcome.

---

## 2. Epistemic hierarchy of this package

This package contains three kinds of documents.

### Authoritative execution documents: `00`–`10`

These define what you should build now.

### Non-authoritative research notebook: `11`–`15`

These preserve mathematically rich hypotheses and long-term ideas.

Read them. Use them to understand the motivation and to suggest candidate analyses. Do not treat them as requirements or settled ontology.

If they conflict with `00`–`10`, the authoritative documents win.

### Historical/evidence sources: `source/`

Preserve them unchanged.

---

## 3. Starting point

Use:

`source/mathrecord_gates0-1_results.zip`

as the starting repository.

Before feature work:

1. reproduce the pinned Lean build;
2. rerun Gate 1 validation;
3. preserve the original reports and code state;
4. report any discrepancy before continuing;
5. create an ADR documenting that the prior direct-to-dynamic-traces recommendation is superseded by representation characterization.

Do not rewrite Gates 0–1 reports to make them match the new direction. They are historical evidence.

---

## 4. What Gates 0–1 established

Treat only the following as established by the prior run:

> The tested MathRecord representation faithfully serialized and reconstructed a bounded set of Lean-native formal objects in one pinned environment.

The run supplied evidence for deterministic serialization, alpha-invariant identity, exact term/type round trips, dependency reconstruction, local-state reconstruction on the tested examples, and Lean checking.

It did **not** establish:

- a correct human-scale mathematical map;
- usefulness for theorem proving;
- usefulness for humans;
- a unique best node/edge ontology;
- learnability;
- semantic meaning;
- importance;
- conceptual proof structure;
- long-range mathematical discovery.

Do not allow successful implementation to inflate those claims.

---

## 5. Immediate research questions

The current stage asks:

1. **Which projections of Lean proof artifacts best preserve reusable named mathematical structure?**
2. **Which candidate views are exact, which are deterministic-derived, and which require semantic judgment?**
3. **How much of contextual named-tool use can be recovered reliably from real proofs?**
4. **Which proposed objects deserve to become persistent schema, and which should remain computed views?**
5. **Is there enough evidence to choose a primary representation for a later navigation experiment?**

---

## 6. Strongly supported constraints

Keep these unless real evidence contradicts them:

1. Lean remains the formal source of truth.
2. Reuse Lean's exact `Expr`, types, declarations, contexts, and proof bodies.
3. Preserve Gates 0–1 exactness and provenance.
4. Keep theorem/type dependencies separate from proof/body dependencies.
5. Keep certified, observed, deterministic-derived, human-annotated, and model-inferred data distinct.
6. Never recover formal content by parsing pretty-printed text.
7. Unsupported or ambiguous cases must classify loudly.
8. Every candidate view must retain provenance to the exact Lean artifacts from which it was derived.
9. Preserve raw data underneath every filter.
10. Do not create a speculative parallel formal language.

---

## 7. Central hypotheses — not architecture

Read files `11`–`15` for the full research ideas, but do not assume any of the following:

- named declarations are sufficient or optimal primary map nodes;
- direct certificate-support sets are good human proof summaries;
- a support set is logically AND-like;
- an AND–OR hypergraph is the final map;
- named application spines recover human proof steps;
- theorem-use roles are recoverable reliably from proof terms;
- selective declaration expansion is the useful notion of zoom;
- alternative proofs exist at useful scale;
- graph structure will outperform strong text/retrieval models;
- a common representation will support proving, conjecturing, definition invention, and curation;
- compression or future proof cost is the right value model;
- the final system will be transformative.

These are hypotheses to preserve and eventually test.

---

# 8. Phase 2A — Real-corpus candidate representation study

## 8.1 Select a bounded heterogeneous Mathlib corpus

Pin a Mathlib revision compatible with the existing Lean toolchain.

Target approximately:

- 500–2,000 declarations in the exact backing record;
- at least four meaningfully different mathematical areas;
- 40–80 showcase proof artifacts for close inspection.

Include:

- tactic proofs;
- term proofs;
- explicit theorem applications;
- rewriting;
- simplification;
- structures;
- typeclasses;
- recursion/induction;
- automation-heavy examples;
- generated declarations as a measured minority rather than the dominant corpus.

Before extraction, write `CORPUS_SELECTION.md` explaining the sample and why it is representative enough for this stage.

## 8.2 Derive candidate projections

For each showcase proof, derive when possible:

### P0 — exact proof-term expression graph

Keep the full exact Lean structure.

### P1 — direct named reference occurrences

Preserve multiplicity and expression position.

### P2 — deduplicated support set

\[
\operatorname{Supp}(p)=\{d:d\text{ occurs in }p\}.
\]

Never label this as a set of necessary logical premises.

### P3 — infrastructure-filtered support view

Preserve P2 and attach reversible classifications/filter reasons.

### P4 — named application occurrences

Extract maximal application spines headed by named declarations, with arguments, position, nesting, and resulting type where available.

### P5 — source/elaborator use view

Recover explicit named uses such as `apply`, `exact`, `refine`, `rw`, `unfold`, constructors, and explicit simp lemmas when defensible.

### P6 — one-level selective declaration expansion

For chosen declarations, show their direct formal backing/dependencies without assuming this is the correct final zoom model.

### P7 — future semantic/human route

Do not synthesize this as formal truth. Reserve hooks/worksheet fields for human or future natural-language tags indicating conceptual proof steps.

For every projection record:

- derivation method;
- exact provenance;
- trust class;
- completeness;
- ambiguity;
- known failure modes.

## 8.3 Characterize representations quantitatively

For each projection measure:

- number of nodes/edges/items;
- compression relative to exact term size;
- named mathematical declarations retained;
- fraction attributable to likely infrastructure;
- overlap/disagreement with other projections;
- coverage across proof styles;
- automation sensitivity;
- rate of ambiguous/partial extraction;
- determinism and alpha-stability where applicable.

Do not select a representation because a graph looks visually clean.

## 8.4 Human-review bundle

For 40–80 showcase proofs, produce side-by-side review artifacts containing:

- theorem statement/source;
- exact proof reference;
- P1–P6 candidate views;
- trust/completeness labels;
- one-branch expansion examples;
- notes about hidden automation/infrastructure.

Produce a worksheet asking a mathematically competent reviewer:

- Which items are actually useful as a short proof hint?
- Which are noise/infrastructure?
- Which important conceptual tools are missing?
- Does order/grouping matter?
- Which candidate view is the best coarse summary?
- Does selective formal expansion help?
- Where would natural-language tagging be required?

If no human review is performed in this run, say so. Do not claim human usefulness.

---

# 9. Phase 2B — Contextual named-use event feasibility

This is a feasibility study, not a full event ontology.

Start only with attribution that is explicit or mechanically defensible:

- `apply L`;
- `exact L ...`;
- `refine L ...`;
- `rw [L]`;
- `unfold D`;
- constructors;
- explicit simplification lemmas when attribution is available.

Attempt to record minimally:

\[
u=
(C_{\mathrm{before}},
 d,
 \mathrm{role},
 \sigma?,
 C_{\mathrm{after}},
 \mathrm{provenance},
 \mathrm{completeness}).
\]

Where:

- `C_before` is canonical context + goal content;
- `d` is the attributable named declaration;
- `role` is explicit/deterministic/ambiguous/unavailable;
- `sigma` is included only where exact instantiation can be recovered honestly;
- `C_after` is the successor goal-content collection;
- provenance links back to syntax, InfoTree, and/or proof term.

Measure:

- manual precision;
- coverage;
- ambiguity;
- instantiation completeness;
- proof-style dependence;
- agreement/disagreement between source syntax, elaborator trace, and proof term;
- automation cases where no single named declaration can be assigned honestly.

Do not build a comprehensive replay engine unless a narrow validation check requires one.

---

# 10. Diagnostic viewer

A small viewer is allowed only as an experimental instrument.

It should let a reviewer switch among P0–P6 for the same proof and inspect provenance.

Do not build a polished MathMap storefront.

Do not make the UI itself evidence that the representation is useful.

---

# 11. Natural-language annotation hook

Because a future agent harness may tag formal objects from papers, textbooks, proof sketches, or natural-language explanations, implement at most a generic append-only annotation attachment keyed by stable exact IDs if useful.

Do not define a comprehensive ontology now.

Suggested minimal fields:

```text
target_id
annotation_type
payload
source
method
confidence
review_status
version
supersedes?
```

The semantic overlay never changes formal identity or Lean validity.

Read `14_SEMANTIC_OVERLAY_AND_NATURAL_LANGUAGE_HARNESS_NOTES.md` for the speculative future direction.

---

# 12. Provisional data-model discipline

Store exact Lean data once.

Prefer derived views over permanent entities.

Do not add a permanent schema entity merely because an idea is appealing.

New permanent entities require an ADR explaining:

- evidence for necessity;
- why a computed view is insufficient;
- trust semantics;
- compatibility with exact provenance.

---

# 13. Deliverables

Produce:

1. `REPRODUCTION_REPORT.md`
2. `CORPUS_SELECTION.md`
3. `CURRENT_RESEARCH_DIRECTION.md`
4. `REPRESENTATION_DEFINITIONS.md`
5. deterministic extraction/derivation code
6. candidate-projection datasets
7. `REPRESENTATION_CHARACTERIZATION.md`
8. human-review bundle
9. reviewer worksheet
10. `USE_EVENT_FEASIBILITY.md`
11. raw validation outputs
12. optional diagnostic viewer
13. `HONEST_ASSESSMENT.md`
14. `NEXT_RECOMMENDATION.md`
15. ADR updating the old direct-to-dynamic-traces recommendation

Update repository documentation so no current document presents a speculative ontology as settled fact.

Do not erase historical documents.

---

# 14. Required honest assessment

Explicitly answer:

- Which projections are exact?
- Which are deterministic views?
- Which require semantic judgment?
- Does raw support look like meaningful mathematics or mostly compiler/library machinery?
- Does filtering help without hiding important structure?
- Does multiplicity/order/nesting matter?
- Can named application routes be recovered beyond toy proofs?
- How much explicit use-event coverage exists?
- How accurately can theorem instantiation be recovered?
- What information appears irretrievably lost after elaboration?
- Which candidate views work across proof styles?
- Which proposed schema entities turned out unnecessary?
- Does selective expansion appear informative or merely verbose?
- Where would the future natural-language harness add indispensable information?
- Is there enough evidence to select a primary map representation?

---

# 15. Decision rules

Choose exactly one final recommendation.

## Outcome 1 — Select representation and proceed

Only if one representation or hybrid:

- is recoverable over a substantial heterogeneous sample;
- has understood failure modes;
- retains useful named mathematical information;
- appears better than raw dependency output under review;
- yields a plausible next learning target.

Recommendation:

**Select a representation and proceed to a controlled navigation experiment.**

## Outcome 2 — Another bounded study

If results are promising but ambiguous:

**Run another bounded representation study.**

Specify exactly what uncertainty remains and the smallest experiment that resolves it.

## Outcome 3 — Stop map-centered program

If candidate maps are mostly dependency restatements/noise, meaningful routes require unsustainably heavy semantic reconstruction, or use-event coverage is too poor:

**Preserve MathRecord as exact tooling but stop pursuing the map-centered representation program.**

Do not recommend continuation merely because implementation succeeded.

---

# 16. Hard scope exclusions

Do not build in this run:

- production MathMap;
- universal graph database;
- full alternative-proof registry;
- large custom GNN;
- theorem prover training;
- conjecture generation;
- definition invention;
- learned semantic zoom;
- bridge discovery;
- curation/value models;
- general autonomous mathematical agent;
- comprehensive replay/state engine unless narrowly required for validation.

---

# 17. Research discipline

The appendices preserve a much larger mathematical vision.

Do not delete those ideas.

Do not implement them simply because they are exciting.

The governing rule is:

> Preserve exact evidence.  
> Compare candidate abstractions.  
> Promote an ontology only after evidence.
