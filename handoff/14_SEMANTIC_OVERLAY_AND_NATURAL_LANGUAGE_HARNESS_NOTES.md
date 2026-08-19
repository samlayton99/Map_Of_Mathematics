# Semantic Overlay and Natural-Language Harness Research Notes
## Status: NON-AUTHORITATIVE FUTURE LAYER

The future natural-language tagging harness may become strategically important because Lean artifacts preserve formal validity but not all of the semantic information humans use.

---

# 1. Why a semantic overlay may be necessary

A final proof term does not reliably encode:

- the motivation for the theorem;
- which step was conceptually decisive;
- the author's intended proof method;
- the relationship to a textbook argument;
- pedagogical prerequisites;
- application areas;
- historical provenance;
- analogies or dualities;
- importance or elegance.

Therefore the eventual system may require a semantic layer attached to exact formal IDs.

The core principle is:

> Formal objects remain authoritative for formal truth.  
> Natural-language metadata is fallible evidence about meaning, use, and importance.

---

# 2. Attachment targets

Annotations should be able to attach to:

- declarations;
- theorem types;
- proof artifacts;
- reference/application occurrences;
- use events;
- selected subterms;
- source spans;
- groups/regions produced by a candidate map;
- natural-language papers or proof steps aligned to formal artifacts.

---

# 3. Candidate annotation types

Examples:

- informal theorem statement;
- proof sketch;
- key theorem hint;
- proof-method label;
- mathematical concepts;
- field/subfield;
- prerequisites;
- application domains;
- “why this definition exists”;
- common use cases;
- known equivalent formulations;
- analogy / duality / transport claim;
- difficulty estimate;
- importance estimate;
- historical citation;
- paper-to-Lean alignment;
- human-rated usefulness of a candidate projection.

---

# 4. Minimal provenance schema

Every semantic assertion should carry something like:

```text
target_id
annotation_type
payload
source_kind
source_reference
agent_or_author
method
confidence
review_status
created_at
version
supersedes?
retracted?
```

No semantic annotation should alter a formal object's identity.

---

# 5. Natural-language harness roles

A future harness could:

1. parse mathematical papers and textbooks;
2. identify theorem statements and proof steps;
3. align those steps to Lean declarations;
4. tag key named tools and conceptual moves;
5. attach explanation metadata;
6. identify application contexts;
7. collect human feedback;
8. produce supervision for semantic zoom and route ranking.

The harness should preserve uncertainty rather than force one ontology.

---

# 6. Potential training uses

The semantic overlay may support:

\[
P(d\mid\Gamma,A,\text{concept tags})
\]

for premise navigation;

\[
P(\text{concept block}\mid G_{\mathrm{formal}})
\]

for learned coarse-graining;

\[
P(\text{application}\mid d)
\]

for applied-mathematics navigation;

and comparison between formal route extraction and human proof summaries.

---

# 7. Evaluation discipline

Do not evaluate semantic tagging only by LLM self-agreement.

Use where possible:

- expert review;
- agreement with authored proof sketches;
- held-out document alignment;
- downstream retrieval/navigation benefit;
- consistency under paraphrase;
- explicit provenance.

The overlay can be extremely useful even if imperfect, provided confidence and provenance remain visible.

---

# 8. Relationship to the current study

Current Phase 2 should implement only a generic append-only annotation hook if useful.

It should not block candidate formal-representation characterization.

However, the study should record cases where exact Lean artifacts clearly fail to capture the concept a human reviewer considers important. Those cases are evidence for what the future semantic harness must supply.
