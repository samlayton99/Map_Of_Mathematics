# Technical Mathematical Ideas Repository
## Status: NON-AUTHORITATIVE RESEARCH NOTEBOOK

This document preserves the mathematically richest ideas that motivated MathRecord / MathMap.

It is intentionally **not** an implementation specification. Nothing in this file becomes architecture merely because it is mathematically elegant. The authoritative current assignment is in `00_MASTER_AGENT_PROMPT.md`.

The purpose of this notebook is to keep promising ideas from being forgotten while the project subjects them to empirical tests.

---

# 1. The core formal object Lean already gives us

Fix a Lean environment \(\Sigma\).

A local formal judgment has the form

\[
\Sigma;\Gamma \vdash t : A.
\]

Here:

- \(\Sigma\) is the global environment: declarations, definitions, theorems, inductive types, axioms, reducibility information, etc.
- \(\Gamma\) is the ordered local context: variables, hypotheses, local definitions, typeclass assumptions, and other scoped objects.
- \(A\) is a target type.
- \(t\) is a term inhabiting that type.

Under Curry–Howard, propositions are types and proofs are terms:

\[
P : \mathrm{Prop}, \qquad p : P.
\]

Function types encode implication and dependent products encode quantified statements. A theorem such as

\[
L : \Pi x:A,\; P(x)\to Q(x)\to R(x)
\]

is simultaneously:

1. a proposition with a proof certificate;
2. a reusable typed function;
3. a parameterized inference schema.

This is the exact formal substrate. We do not need to invent a new foundation.

---

# 2. The working abstraction hypothesis

The central human-scale hypothesis is different from the foundational fact above.

Mathematicians usually reason with **named abstractions**:

- definitions;
- lemmas;
- theorems;
- structures;
- constructors;
- equivalences;
- recursors and induction principles;
- named constructions and algorithms.

A declaration has approximately

\[
d : \tau_d := \beta_d,
\]

where \(\tau_d\) is its interface/type and \(\beta_d\) is its body or proof when available.

Once a result has been proved and named, a potentially large derivation becomes a reusable one-step tool. This motivates the claim:

> A mathematical library is not merely a set of true statements; it is an accumulated vocabulary of certified reusable actions.

This is a strong working hypothesis, not a proven theorem about optimal mathematical representation.

---

# 3. One declaration has several potentially useful faces

A named theorem \(L\) may be represented at several resolutions.

## 3.1 Interface / use schema

If

\[
L : \Pi x:A,\; P(x)\to Q(x)\to R(x),
\]

then a use of \(L\) can be understood as an instantiated rule

\[
\{P(a),Q(a)\} \xrightarrow{L(a)} R(a).
\]

Backward search attempts to match the conclusion \(R(a)\) to the current goal. Forward search attempts to satisfy the premises from the current context.

This interface view may be useful for navigation because it says **how a theorem can attach to a local proof state**.

## 3.2 Certificate support

For one registered proof term \(p_L:L\), let

\[
\operatorname{Supp}(p_L)
\]

denote the named declarations occurring in the certificate.

This is exact occurrence/support data, but it must not be overinterpreted:

- it is proof-relative;
- it is not necessarily minimal;
- it may include compiler or elaboration infrastructure;
- it does not imply logical necessity;
- it loses order and local role if deduplicated.

Nevertheless, it may be an excellent compressed proof hint.

## 3.3 Named application route

A richer candidate view records actual application occurrences such as

\[
K\,a_1\cdots a_n
\]

inside the proof term, along with nesting, local context, result type, and provenance.

This may recover more of the human-scale proof route than a support set, but whether it does so reliably is an empirical question.

## 3.4 Exact proof term

The complete Lean term remains the authoritative certificate.

Any coarser representation should retain provenance back to this exact artifact.

---

# 4. Proofs as typed construction structure

A proof term is built compositionally.

For example, application has the form

\[
\frac{
\Gamma\vdash f:\Pi x:A\,B(x)
\qquad
\Gamma\vdash a:A
}{
\Gamma\vdash f(a):B(a)
}.
\]

This can be displayed as a typed directed hyperedge

\[
\{\Gamma\vdash f:\Pi x:A\,B(x),\;
  \Gamma\vdash a:A\}
\longrightarrow
\Gamma\vdash f(a):B(a).
\]

Conjunction construction, existential construction, induction, rewriting, structure construction, and many other inference/construction steps have multi-input structure of the same general kind.

This motivates a **typed contextual hypergraph** view of exact term construction.

Important caution: this is one mathematically natural projection of Lean syntax/typing, not automatically the best learned or human-facing representation.

---

# 5. Alternative proofs and proof families

For theorem \(T\), conceptually define

\[
\mathcal P_\Sigma(T)=\{p\mid \Sigma\vdash p:T\}.
\]

Each proof may induce different dependencies and a different route through the library.

If two known proofs have supports

\[
\operatorname{Supp}(p_1)=\{A,B,C\},
\qquad
\operatorname{Supp}(p_2)=\{X,Y\},
\]

they expose two distinct certificate routes to the same theorem type.

This suggests a weak AND–OR interpretation:

- OR across alternative certificates for the same statement;
- joint support inside one chosen certificate.

But **do not assume** the support set is a set of logically necessary AND-premises. The AND–OR ontology is a candidate map formalism only.

Structurally diverse alternative proofs may eventually be valuable because they connect distant regions of mathematics. Ten tactic variants of the same proof are likely much less informative than two proofs using fundamentally different theories.

---

# 6. Selective opacity and exact zoom

Named declarations are natural candidate abstraction boundaries.

Let \(D\) be declarations and choose an opacity set

\[
O\subseteq D.
\]

A view may leave declarations in \(O\) collapsed and expand selected declarations outside \(O\) into bodies, dependencies, or named application routes.

If a theorem \(T\) has selected proof route \(\rho\), denote a partially expanded view schematically by

\[
H_{O,\rho}(T).
\]

This formalizes the Google Maps intuition:

- familiar tools remain black boxes;
- the region where the user is stuck can be opened;
- expansion can be branch-specific rather than global.

But formal expansion is not automatically conceptual explanation. Whether selective declaration expansion is a useful human or machine zoom operation must be tested.

---

# 7. Local mathematical navigation

A local state is

\[
C=(\Sigma;\Gamma\vdash A).
\]

A central candidate learning target is

\[
P(d\text{ useful}\mid \Gamma,A),
\]

where \(d\) is a declaration.

This captures a large part of the original intuition: mathematical experience includes learning which reusable tools tend to become relevant in which local situations.

A theorem-use event may be represented minimally as

\[
u=(C_{\mathrm{before}},d,r,\sigma?,C_{\mathrm{after}},\pi),
\]

where:

- \(d\) is the named declaration;
- \(r\) is a use role such as application, rewrite, unfold, constructor, etc.;
- \(\sigma\) is an exact instantiation if recoverable;
- \(\pi\) is provenance.

The important conceptual distinction is:

> The global map records what tools and routes exist.  
> Use events record when mathematicians took which roads.

Proof states therefore may be most useful as **experience data**, not as the primary global map.

---

# 8. Forward and backward traversal

Given current goal

\[
\Gamma\vdash A
\]

and theorem

\[
L:\Pi x,\;P_1(x)\to\cdots\to P_k(x)\to Q(x),
\]

backward reasoning seeks \(\sigma\) with

\[
Q(\sigma x)\approx A
\]

and replaces the current goal by subgoals

\[
P_1(\sigma x),\ldots,P_k(\sigma x).
\]

Forward reasoning starts from facts in \(\Gamma\) matching the premises and derives \(Q(\sigma x)\).

Rewriting, unfolding, changing coordinates, proving equivalent targets, strengthening lemmas, and introducing intermediate statements modify the representation until useful declarations become attachable.

A recurring proof-search loop is therefore:

\[
\text{inspect state}
\to
\text{retrieve candidate tools}
\to
\text{instantiate / apply / rewrite / unfold}
\to
\text{new state}
\to
\text{repeat}.
\]

This is one reason graph/navigation language is appealing.

---

# 9. Definitions as representation changes

Definitions are not merely collections of propositions.

A definition can package:

- an object;
- a predicate;
- a function;
- a structure;
- an invariant;
- a family;
- a construction.

A transparent definition

\[
d:A:=t
\]

introduces a reusable interface around a construction.

Operationally, definitions can be viewed as **representation-changing abstractions**:

- folding hides lower-level detail behind a useful concept;
- unfolding exposes detail when the abstraction blocks progress.

This motivates the compression hypothesis:

> Good mathematical abstractions reduce future reasoning cost by creating useful reusable interfaces.

A possible long-term utility measure is

\[
U(d)
=
\mathbb E_{q\sim\mathcal D}
\left[
C(q\mid\Sigma)-C(q\mid\Sigma\cup\{d\})
\right]
-\lambda\,\mathrm{Cost}(d),
\]

where \(C\) is proof/search cost.

This is speculative but concrete and falsifiable.

---

# 10. Importance should be conditional

Raw citation count is a poor universal importance measure.

A more meaningful quantity may be regional or task-conditional:

\[
I_R(L)=P(L\text{ useful}\mid q\in R).
\]

A stronger counterfactual notion is

\[
I_R(L)
=
\mathbb E_{q\sim R}
\left[
C(q\mid\Sigma\setminus\{L\})
-
C(q\mid\Sigma)
\right].
\]

Interpretation:

> How much harder would future work in region \(R\) become if theorem \(L\) were unavailable as a named black-box tool?

This may provide a route toward measuring load-bearing lemmas, abstraction quality, and curation value.

It is not yet validated.

---

# 11. The library changes the search geometry

Suppose a long route exists:

\[
A\to B\to C\to D\to T.
\]

A new theorem

\[
L:A\to D
\]

turns that recurring path into a shorter reusable action.

A new definition may similarly expose a representation in which many results become shorter or more discoverable.

A structurally different alternative proof may connect distant regions.

This motivates a central long-term idea:

> Doing mathematics changes the effective map on which future mathematics is done.

That links theorem proving, abstraction invention, alternative proofs, and curation.

---

# 12. The long-term multi-role loop

The larger vision remains:

\[
\text{Explore}
\to
\text{Define}
\to
\text{Conjecture}
\to
\text{Shape}
\to
\text{Prove/Refute}
\to
\text{Verify}
\to
\text{Curate}.
\]

Potential roles:

- **Explore:** compute examples, search counterexamples, inspect neighboring structure.
- **Define:** propose useful abstractions/representations.
- **Conjecture:** propose potentially valuable statements.
- **Shape:** choose assumptions, generality, formulation, and target.
- **Prove/Refute:** navigate and synthesize routes.
- **Verify:** Lean checks exact formal validity.
- **Curate:** decide what deserves durable prominence.

A shared learned representation across these roles is plausible but unproven.

---

# 13. Category/type theory as structural plumbing

The project does not need category theory as its primary UI or immediate data model.

Still, the deeper formal picture is useful.

Contexts and substitutions organize local mathematics:

\[
\sigma:\Delta\to\Gamma.
\]

A judgment in \(\Gamma\) transports along substitution to one in \(\Delta\).

This is the mathematical basis for expecting the local machinery—application, substitution, abstraction, rewriting, composition—to recur across domains.

A desirable learned policy may respect substitution or renaming equivariance approximately:

\[
\pi(\sigma^*C)\approx \sigma^*\pi(C).
\]

This is a candidate inductive bias, not an established architecture.

---

# 14. Structural self-similarity and power laws

Two claims must be separated.

## Exact recursive form

Proof-state refinement repeatedly produces new states of the same broad form

\[
\Gamma\vdash A.
\]

Named abstractions can also be recursively expanded.

This is real structural recursion.

## Statistical self-similarity

Claims that mathematics has a power-law or scale-free structure are empirical and projection-dependent.

Do not build the project around a power-law assumption.

A more defensible hypothesis is:

> Formal mathematics may be hierarchically compressible and may contain reusable motifs across abstraction scales.

This can be tested.

---

# 15. Natural-language semantic information

Lean certifies syntax and semantics internal to the formal system. It does not certify:

- motivation;
- conceptual proof method;
- intended informal meaning;
- historical context;
- pedagogical prerequisites;
- applications;
- novelty;
- importance;
- analogy;
- elegance.

A future natural-language tagging harness may attach such information to stable exact IDs.

This creates a potential hierarchy:

\[
\text{exact Lean core}
\longleftrightarrow
\text{derived formal views}
\longleftrightarrow
\text{observed usage}
\longleftrightarrow
\text{semantic annotations}.
\]

The overlay can eventually supervise semantic zoom or concept-conditioned navigation, but it must remain provenance-aware and fallible.

---

# 16. Candidate unified vision

If the empirical studies support it, a future mathematical substrate might be described as

\[
\mathcal M_t
=
(\text{exact corpus},
 \text{map},
 \text{experience},
 \text{semantic overlay},
 \text{evolution}).
\]

Where:

- the exact corpus comes from Lean;
- the map contains useful reusable abstractions and proof-route projections;
- experience records which moves were useful in which contexts;
- semantic overlays connect formal artifacts to human concepts and natural language;
- evolution adds new statements, definitions, proofs, counterexamples, routes, and curation decisions.

This is the motivating vision.

It is **not** the current architecture.

---

# 17. Research discipline

The following distinctions must remain explicit:

\[
\text{formal validity}
\neq
\text{semantic fidelity}
\neq
\text{human usefulness}
\neq
\text{novelty}
\neq
\text{importance}.
\]

Likewise:

\[
\text{beautiful formalization}
\neq
\text{validated representation}.
\]

Use this notebook to generate hypotheses, diagnostics, candidate projections, and future experiments—not to override evidence.
