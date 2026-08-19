# Long-Term Research Hypotheses and Falsifiers
## Status: NON-AUTHORITATIVE

This document turns the project's speculative ideas into falsifiable hypotheses. It exists to preserve ambition without confusing ambition with evidence.

---

## H1. Named declarations form a useful working abstraction level

### Claim

Definitions, lemmas, theorems, structures, and related declarations are more useful navigation units than kernel-level expression nodes for a substantial fraction of mathematical tasks.

### Evidence today

Plausible from mathematical practice; partially reflected in premise-selection systems and library APIs.

### Falsifiers / weakening evidence

- human reviewers consistently prefer a different projection;
- named-declaration views are dominated by implementation details;
- text-only or learned latent representations outperform declaration structure with no incremental value;
- important conceptual moves frequently have no recoverable named-declaration correlate.

---

## H2. Direct proof support contains useful compressed proof information

### Claim

For many proofs,

\[
\operatorname{Supp}(p)
\]

or a filtered refinement provides a useful short hint about how the proof works.

### Falsifiers

- support is mostly typeclass/coercion/compiler infrastructure;
- key human-recognized moves are absent;
- ordering/grouping is essential and cannot be recovered;
- support adds no value beyond theorem text.

---

## H3. Named application occurrences recover a useful middle layer

### Claim

Maximal applications headed by named declarations encode enough local structure to approximate meaningful proof routes.

### Falsifiers

- application occurrence graphs are too dense or low-level;
- automation erases attribution;
- term-style and tactic-style proofs produce incompatible representations;
- human reviewers do not find the result more informative than support sets.

---

## H4. Contextual use history is transferable mathematical experience

### Claim

A dataset of events such as

\[
(\Gamma,A,d,\mathrm{role},\sigma,\mathrm{result})
\]

supports useful prediction of which declarations/actions matter in new proof states.

### Core target

\[
P(d\mid\Gamma,A).
\]

### Falsifiers

- events cannot be recovered with adequate precision/coverage;
- gains disappear under module/domain holdouts;
- text representations capture all incremental signal;
- attribution to named tools is too ambiguous.

---

## H5. Selective formal expansion provides useful zoom

### Claim

Keeping most declarations opaque and expanding only selected branches helps navigation or understanding.

### Falsifiers

- users gain little from dependency/body expansion;
- conceptual explanations consistently require semantic information absent from formal expansion;
- alternative coarse-graining methods dominate.

---

## H6. Structural representation improves generalization

### Claim

Exact typed structure contributes signal beyond strong text and flat dependency baselines, especially out of domain.

### Key experiment

Compare text, flat graph, structural, and hybrid representations under module/domain holdout.

### Falsifiers

- no robust incremental gain;
- gains come only from leaked names/namespaces;
- hybrid structure adds negligible value after strong retrieval.

---

## H7. Structurally diverse alternative proofs expose bridges

### Claim

Theorems with proof routes using distant regions can reveal analogies, transports, or useful long-range connections.

### Falsifiers / limitations

- alternative proofs are too sparse;
- route diversity mostly reflects superficial implementation choices;
- graph distance does not correlate with useful conceptual transfer.

---

## H8. Useful abstractions reduce future mathematical cost

### Claim

Definitions and lemmas can be scored by future search/compression benefit:

\[
U(a)
=
\mathbb E_q[
C(q\mid\Sigma)-C(q\mid\Sigma+a)
]
-\lambda \operatorname{Cost}(a).
\]

### Falsifiers

- historical utility cannot be measured robustly;
- search-cost metrics reward pathological abstractions;
- human usefulness disagrees systematically with measured savings.

---

## H9. Learned semantic zoom can map exact structure to human-scale concepts

### Claim

Natural-language proofs, blueprints, textbooks, or human annotations can supervise mappings from exact Lean artifacts to conceptual units.

### Falsifiers

- alignments are too ambiguous;
- conceptual decompositions are too task/user dependent for stable learning;
- exact formal structure contributes little compared with raw language models.

---

## H10. One shared representation supports multiple mathematical roles

### Claim

Proving, statement synthesis, abstraction invention, and curation benefit from a common learned mathematical representation.

### Falsifiers

- transfer across roles is weak or negative;
- role-specific representations consistently dominate;
- curation/value signals remain fundamentally external.

---

## H11. The mathematical map is dynamically improved by new named abstractions

### Claim

New lemmas/definitions change future search geometry in measurable ways.

### Falsifiers

- new named intermediates do not improve held-out search;
- library growth increases branching more than it reduces path length;
- strong models synthesize needed intermediates on demand and gain little from durable registration.

---

## H12. Global structure helps long-range mathematical discovery

### Claim

Beyond local premise selection, global map structure enables useful cross-domain transfer or discovery.

### Falsifiers

- global graph features add no signal beyond local retrieval;
- discovered crosslinks are mostly already captured by embeddings/language;
- structural similarity fails to correspond to mathematical analogy.

---

# Conviction guide

Approximate current status:

### High conviction / engineering facts

- Lean should remain the verifier.
- Exact and semantic information must remain separated.
- Stable provenance and IDs are valuable.
- Type and body dependencies should not be conflated.

### Medium conviction / research bets

- named declarations matter strongly;
- local context is critical for useful theorem retrieval;
- use-event history is valuable;
- hybrid text + formal structure is more promising than either alone.

### Low-to-medium conviction / high-upside bets

- AND–OR structure is the right main map;
- selective declaration expansion is the right zoom;
- global structural bridge mining works;
- future proof-cost gives a good abstraction/value metric;
- a common representation supports the whole mathematical loop.

### Low conviction / visionary

- one explicit map becomes a universal mathematical operating substrate;
- the system supports autonomous open-ended research mathematics at scale;
- structural self-similarity supplies an AlphaZero-like general solution.

None of the low-conviction ideas should be hidden. None should be implemented merely because they are exciting.
