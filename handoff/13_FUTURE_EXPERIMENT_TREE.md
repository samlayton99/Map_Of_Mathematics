# Future Experiment Tree
## Status: CONDITIONAL RESEARCH ROADMAP

This is not a committed schedule. It is a branching decision tree designed to stop the project from building ahead of evidence.

---

# Stage A — Exact core
**Status:** Gates 0–1 passed on a bounded adversarial corpus.

Question:

> Can exact Lean artifacts be serialized, identified, and traced without silent loss?

If no: stop/revise.

If yes: continue.

---

# Stage B — Candidate representation study
**Current authorized stage.**

Questions:

1. Which projections are recoverable on real Mathlib?
2. Which are exact versus derived?
3. Which contain named mathematical information rather than infrastructure?
4. Can human reviewers identify a useful coarse proof view?
5. Can meaningful named-tool use events be recovered at adequate precision?

Candidate projections:

\[
P_0=\text{exact term graph}
\]
\[
P_1=\text{reference occurrences}
\]
\[
P_2=\text{support set}
\]
\[
P_3=\text{filtered support}
\]
\[
P_4=\text{named application occurrences}
\]
\[
P_5=\text{source/elaborator use route}
\]
\[
P_6=\text{future semantic/human route}.
\]

### Outcomes

**B1 — Clear winner/hybrid:** proceed to navigation test.

**B2 — Promising but ambiguous:** run one more bounded characterization iteration.

**B3 — Mostly noise/redundancy:** preserve MathRecord tooling and stop the map-centered program.

---

# Stage C — Navigation usefulness
Only after Stage B selects a representation.

Primary tasks:

\[
(\Gamma,A)\mapsto \text{rank useful declarations}
\]

and possibly theorem-level premise retrieval.

Compare:

- text;
- flat dependency graph;
- selected structural representation;
- usage history;
- hybrid.

Use cross-domain/module holdouts and name-ablation controls.

### Outcomes

**C1 — Strong out-of-domain gain:** invest in richer activity traces and representation learning.

**C2 — Small incremental gain:** treat as useful engineering; investigate feature attribution before expanding vision.

**C3 — No gain:** weaken or abandon explicit-structure ML thesis.

---

# Stage D — Next-action / local physics
Only after Stage C.

Task:

\[
R(\Gamma\vdash A)\mapsto \text{next useful action}.
\]

Test whether proof policies transfer across mathematical domains.

Potential invariance tests:

- alpha-renaming;
- context permutation where valid;
- substitution;
- definition fold/unfold;
- equivalent formulations.

A strong result here is the first meaningful evidence for reusable domain-independent local machinery.

---

# Stage E — Semantic zoom
Only if exact projections plus navigation prove useful.

Use natural-language proofs, human review, blueprints, or a tagging harness to learn:

\[
C_q:G_{\mathrm{exact}}\to G_{\mathrm{task},q}.
\]

Questions:

- what information can be discarded for premise retrieval?
- what resolution supports explanation?
- what resolution supports theorem reuse?
- can conceptual blocks be predicted from exact structure?

---

# Stage F — Alternative proof diversity and bridges
Only if enough alternative proof data exists.

Measure structural diversity between proof routes.

Look for theorems joining distant regions.

Test whether bridge candidates yield useful analogy/transfer rather than only graph novelty.

---

# Stage G — Abstraction / lemma invention
Only after navigation and evaluation are reliable.

Propose candidate lemmas/definitions.

Measure held-out utility:

\[
\Delta C
=
C(\text{future tasks without abstraction})
-
C(\text{future tasks with abstraction}).
\]

Reject abstractions that compress only training proofs but do not improve future tasks.

---

# Stage H — Statement synthesis and refutation
Only after a meaningful utility model exists.

Generate candidate statements from:

- computation;
- analogy;
- generalization;
- failed proof traces;
- structural gaps;
- transferred patterns.

Evaluate through proof/refutation plus value/novelty filters.

---

# Stage I — Curation
Develop models that distinguish:

\[
\text{valid}
\neq
\text{worth retaining}.
\]

Potential signals:

- future proof savings;
- generality;
- proof connectivity;
- semantic novelty;
- explanatory value;
- human expert judgment.

---

# Stage J — Shared multi-role system
Only after several preceding roles show compatible representations.

Test whether one backbone helps:

- navigate;
- prove;
- define;
- conjecture;
- shape;
- curate.

Do not assume shared representation is optimal.

---

# Stage K — Long-range mathematical exploration
Highest-risk vision.

Test whether accumulated map + experience + semantic overlays enable discoveries unavailable to equally capable text/retrieval systems.

This is the point at which “mathematical operating substrate” would become evidence-backed rather than aspirational.
