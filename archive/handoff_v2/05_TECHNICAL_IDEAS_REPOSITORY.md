# Technical Ideas Repository
## Mathematical hypotheses and conceptual machinery for MathMap / MathRecord

**Status:** non-authoritative research notes. This document is a direct synthesis of the strongest mathematical and technical ideas developed in the design conversation. It is intentionally richer and more speculative than the implementation handoff. Use it as a source of hypotheses, representations, invariances, objective functions, and future experiment ideas. Do **not** interpret every object below as something the current MVP must implement.

The immediate handoff documents define what to build now. This document tries to preserve **why the object might be interesting if the early gates succeed**.

---

# 1. The central intuition

The recurring intuition is that mathematics may have two separable aspects:

1. a **global accumulated substrate** of objects, definitions, theorems, constructions, proofs, and transformations; and
2. a relatively small amount of **local reasoning machinery** that repeatedly operates on a small part of that substrate.

A local mathematical task can be represented by the judgment

\[
\Sigma;\Gamma \vdash ?e : A.
\]

Interpretation:

- \(\Sigma\): the global Lean environment or library currently available;
- \(\Gamma\): the local context — variables, assumptions, structures, local definitions;
- \(A\): the target type or proposition;
- \(?e\): the unknown term, construction, witness, or proof to synthesize.

This should be treated as an **experimental primitive**, not as a metaphysical claim that all mathematical intelligence is reducible to one tuple.

The main research hypothesis is stronger:

> There may exist a representation of \((\Sigma,\Gamma,A)\) in which useful mathematical reasoning becomes sufficiently local, reusable, invariant, and multiscale that learned policies transfer across problems and mathematical domains better than policies learned from surface syntax alone.

That hypothesis is falsifiable and should ultimately be tested against strong token-based and hybrid baselines.

---

# 2. Why Curry–Howard makes this substrate unusually coherent

Dependent type theory gives a remarkably uniform language for mathematical entities.

At a simplified level:

\[
\text{proposition} \leftrightarrow \text{type},
\]

\[
\text{proof of }P \leftrightarrow \text{term }p:P.
\]

Ordinary mathematical objects have the same typed form:

\[
x:\mathbb R,
\qquad
f:\mathbb R\to\mathbb R,
\qquad
p:P.
\]

Implication becomes a function type:

\[
P\Rightarrow Q
\quad\leftrightarrow\quad
P\to Q.
\]

A proof of implication is therefore a function taking proofs of \(P\) to proofs of \(Q\):

\[
f:P\to Q,
\qquad
p:P
\quad\Rightarrow\quad
f(p):Q.
\]

Dependent products and sums unify quantification with typed construction:

\[
\forall x:A,\;B(x)
\quad\leftrightarrow\quad
\Pi_{x:A} B(x),
\]

\[
\exists x:A,\;B(x)
\quad\leftrightarrow\quad
\Sigma_{x:A} B(x).
\]

This matters because proofs, objects, functions, propositions, witnesses, definitions, and theorem applications need not live in unrelated data systems. Lean already represents them through a common typed expression language.

The practical consequence is that one exact record can plausibly anchor many different mathematical activities without inventing five unrelated ontologies.

---

# 3. Context is part of the mathematical object

A theorem node by itself is too impoverished. Mathematical expressions are meaningful relative to a context.

Compare

\[
\Gamma_1\vdash x:\mathbb R
\]

with

\[
\Gamma_2\vdash x:G.
\]

The symbol `x` is not a globally meaningful node. Its identity and type depend on scope, binders, assumptions, and local declarations.

For this reason, a faithful representation must preserve at least:

- ordered local declarations;
- binder dependencies;
- local definitions;
- types of local variables;
- target type;
- universe information where relevant;
- enough identity information to distinguish scope while ignoring irrelevant generated names.

This suggests a useful slogan:

> The substrate should be **context-indexed but domain-agnostic**, not context-free.

The same machinery should operate whether the context contains real numbers, groups, topological spaces, matrices, measures, or functions.

---

# 4. The local “physics” of mathematical reasoning

Across domains, many proof transformations are instances of a small collection of typed operations. The exact kernel rules are more precise than this list, but conceptually the recurring moves include:

### Introduce structure

To prove an implication

\[
\Gamma\vdash A\to B,
\]

enter the extended context

\[
\Gamma,h:A\vdash B.
\]

To prove a conjunction, generate two subgoals.

### Eliminate or apply structure

Given

\[
f:A\to B
\quad\text{and}\quad
a:A,
\]

construct

\[
f(a):B.
\]

### Substitute / instantiate

A general theorem can be instantiated in a particular context. Substitution is one of the most fundamental transport operations in formal mathematics.

### Rewrite / normalize

Replace expressions using definitional equality, proved equality, simplification, or a structure-preserving equivalence.

### Construct witnesses

To prove an existential, synthesize both a witness and evidence that it satisfies the desired property.

### Recurse / induct

Use the structure of an inductive object to reduce a goal to recursively smaller or structurally simpler cases.

### Compose

Build new constructions from existing ones. Function composition and cut-like proof composition are ubiquitous.

### Abstract

Convert a successful local construction into a reusable theorem, function, lemma, or definition by discharging local variables and assumptions.

### Extend the library

Introduce a verified new declaration that future states can use as a primitive action.

The research question is not whether these operations exist — they do. It is whether their **statistical use**, after normalizing away superficial notation, is reusable enough to support strong cross-domain learning.

---

# 5. Exact recursive self-similarity

A useful formal observation is that proving frequently turns one state into smaller states of the same form.

Start with

\[
(\Sigma,\Gamma,A).
\]

A legal refinement may create

\[
(\Sigma,\Gamma_1,A_1),\ldots,(\Sigma,\Gamma_k,A_k).
\]

Each child is again a context plus target.

Example:

\[
\Gamma\vdash A\to(B\land C)
\]

may refine to

\[
\Gamma,h:A\vdash B
\]

and

\[
\Gamma,h:A\vdash C.
\]

The same type of state reappears recursively.

This is one rigorous sense in which mathematics is self-similar. It should **not** be confused with the stronger empirical claim that theorem networks follow a perfect power law or that every field has identical statistical proof structure.

The exact claim is structural recursion. The statistical claim is a hypothesis to test.

---

# 6. Definitions as representation changes, interfaces, and compression

A transparent definition has a form such as

\[
c:A := t,
\]

where \(t:A\) was already constructible.

At one level, this is repackaging: a complex term becomes accessible through a short name and interface. But useful definitions do more than save characters.

They can:

- expose a recurring invariant;
- make statements shorter;
- align multiple constructions under one interface;
- reduce future search depth;
- create a natural induction or recursion principle;
- make analogy with another area visible;
- provide a stable API while hiding implementation detail.

Inductive definitions are especially important because they introduce constructors and elimination/recursion principles. They therefore alter the effective reasoning vocabulary, not merely the pretty-printing.

A productive working analogy is:

> Definitions are learned coordinates, reusable APIs, or dictionary atoms for mathematics.

A theorem or lemma can similarly be viewed as a cached verified computation:

\[
A\leadsto E
\]

may initially require a long proof path, but once packaged as

\[
L:A\to E,
\]

future reasoning can invoke \(L\) as one reusable move.

This motivates treating **library design as representation design**.

---

# 7. Mathematical discovery is not only path search; it can change the search space

A fixed-goal theorem prover can be described as searching for a term

\[
p:P
\]

inside a fixed environment \(\Sigma\).

But mathematicians often succeed by changing the representation first:

- introduce an auxiliary lemma;
- strengthen the induction hypothesis;
- define an invariant;
- change coordinates;
- pass to a quotient;
- use a transform;
- introduce a generating function;
- move into an equivalent theory or representation.

Thus open-ended mathematics is closer to

\[
\text{modify the effective library/representation}
\quad+\quad
\text{search locally}.
\]

This is the deepest limitation of the chess analogy. The inner proof problem is game-like; the outer mathematical process can create new reusable moves and change the effective board.

A useful conceptual decomposition is therefore:

### Inner game

Fix \(\Sigma,\Gamma,A\). Find

\[
p:A.
\]

Lean supplies the legal semantics and terminal validity check.

### Outer game

Change the environment or research target:

\[
\Sigma_t\to\Sigma_{t+1}.
\]

Possible moves include defining objects, proving reusable lemmas, formulating statements, discovering counterexamples, and promoting useful artifacts into the library.

The inner game has a crisp success signal. The outer game requires a theory of value.

---

# 8. One joint generative object, several conditional activities

A particularly promising synthesis from the conversation is to treat mathematical declarations as structured tuples and view different activities as different conditional-generation problems.

Let a declaration-like object be

\[
D=(k,\Gamma,A,e),
\]

where

- \(k\) is a declaration/activity kind;
- \(\Gamma\) is the parameter/context structure;
- \(A\) is a type or proposition;
- \(e\) is a body, construction, witness, or proof.

A conceptual joint model might be

\[
p_\theta(k,\Gamma,A,e\mid\Sigma,\mathcal O),
\]

where \(\mathcal O\) denotes observations, examples, previous searches, computations, or other exploratory evidence.

Different mathematical activities correspond to revealing some fields and synthesizing others.

### Proof discovery

Clamp \(\Sigma,\Gamma,A\), synthesize \(e\):

\[
p_\theta(e\mid\Sigma,\Gamma,A).
\]

### Statement / hypothesis generation

Clamp the environment and exploratory evidence, synthesize a proposition or type:

\[
p_\theta(A\mid\Sigma,\mathcal O).
\]

### Goal shaping / formalization

Transform an informal or approximate hypothesis into an exact context and proposition:

\[
H\mapsto(\Gamma\vdash A).
\]

### Definition / abstraction generation

Propose a reusable interface and body:

\[
p_\theta(A,e\mid\Sigma,k=\mathrm{definition}).
\]

### Verification

This should **not** be a learned head. Use Lean:

\[
K(\Sigma;\Gamma\vdash e:A)\in\{0,1\}.
\]

This architecture suggests that proof learning, statement synthesis, and abstraction learning may benefit from one shared structural representation even if they require different decoders or constraints.

That transfer hypothesis is not established and should not drive the MVP until basic structural value is demonstrated.

---

# 9. Exploration should be distinguished from deduction

Mathematical conjectures do not arise only from statistical pattern recognition. They may arise from:

- computation;
- random or exhaustive examples;
- symmetry;
- analogy;
- failed proof attempts;
- generalization of a known theorem;
- special cases;
- counterexamples to stronger claims;
- invariants;
- transformed representations;
- theory transport.

It is useful to distinguish an uncertain exploratory relationship from a deductively verified edge.

Possible epistemic relation types include:

- `proves`;
- `refutes`;
- `implies-conditionally`;
- `suggests`;
- `motivates`;
- `is-consistent-with`;
- `generalizes`;
- `specializes`;
- `is-equivalent-to` when certified;
- `appears-analogous-to` when learned or human-supplied.

A computational observation generally does not imply a universal theorem:

\[
\mathcal O\not\vdash P.
\]

It changes the posterior plausibility or priority of testing \(P\):

\[
\Pr(P\mid\mathcal O)>\Pr(P)
\]

in an informal Bayesian sense.

Keeping epistemic status explicit is critical if the long-term record eventually mixes proof, experimentation, conjecture, failed searches, and semantic annotations.

---

# 10. Hypothesis creation and goal construction are related but not identical

The conversation initially separated:

1. noticing or proposing a mathematical pattern; and
2. constructing the exact formal theorem to attempt.

That distinction remains useful even if an implementation later merges them.

A semantic hypothesis might be:

> “This quantity appears invariant under the transformation.”

The formal goal designer must choose:

- the precise objects being quantified over;
- assumptions;
- definitions;
- conclusion;
- strength and generality;
- edge cases;
- exact universe/structure level.

Thus one can view the process as

\[
\text{pattern / research idea}
\to
\text{candidate statement family}
\to
\Gamma\vdash A.
\]

The second arrow is mathematically significant. Bad theorem statements can be vacuous, overspecified, unnecessarily weak, unnecessarily strong, or tied to an unnatural representation.

---

# 11. Theorem shaping as movement in a partially ordered space of statements

There is a useful formal way to compare nearby propositions.

For propositions \(P,Q\), define

\[
P\preceq Q
\quad\Longleftrightarrow\quad
\Sigma\vdash Q\to P.
\]

Then \(Q\) is at least as strong as \(P\).

Goal construction can therefore be interpreted partly as navigation through a space of nearby statements:

- remove assumptions;
- add necessary assumptions after finding a counterexample;
- strengthen or weaken the conclusion;
- generalize constants to variables;
- specialize to tractable cases;
- replace a formulation by an equivalent one;
- alter the ambient algebraic/topological structure;
- search for a sharp boundary between true and false.

A candidate assumption-minimization objective is

\[
\Gamma^*
=
\arg\min_{\Delta}
\operatorname{Cost}(\Delta)
\quad
\text{s.t.}
\quad
\Delta\vdash P.
\]

But logical minimality is not the same as mathematical naturalness. A useful theorem statement may retain a redundant-looking assumption because it exposes the right conceptual interface or aligns with a standard structure.

Therefore theorem shaping should eventually optimize a vector of properties rather than only proof-theoretic strength.

Possible dimensions:

\[
V_{\mathrm{statement}}=
(
\text{generality},
\text{sharpness},
\text{novelty},
\text{tractability},
\text{naturalness},
\text{downstream utility}
).
\]

---

# 12. Abstraction quality as held-out compression and future proof utility

One of the richest ideas from the conversation is that useful definitions and lemmas should be judged by what they do to **future mathematics**, not merely by whether they shorten the examples from which they were extracted.

Suppose a candidate abstraction \(d\) is added to a library \(\Sigma\).

A retrospective compression score is

\[
\Delta_{\mathrm{train}}(d)
=
L(\mathcal C\mid\Sigma)
-
\left[
L(d)+L(\mathcal C\mid\Sigma\cup\{d\})
\right].
\]

But this can overfit. A bizarre macro might memorize one proof.

A stronger score measures held-out future benefit:

\[
U_{\mathrm{def}}(d)
=
\mathbb E_{q\sim\mathcal D_{\mathrm{future}}}
\left[
C(q\mid\Sigma)-C(q\mid\Sigma\cup\{d\})
\right]
-
\lambda L(d).
\]

Here:

- \(C(q\mid\Sigma)\) is proof-search, retrieval, or description cost for future task \(q\);
- \(L(d)\) is the complexity or maintenance cost of adding the abstraction.

This makes definition invention analogous to dictionary learning or feature learning:

> A good mathematical abstraction is a compact reusable latent feature that reduces expected future reasoning cost.

Potential additional rewards include:

- transfer across domains;
- invariance under natural equivalence;
- creation of clean closure properties;
- reduction in proof-search branching;
- interpretability;
- ability to expose further conjectures;
- ability to connect previously separate regions.

This is a long-term hypothesis, not a current MVP objective.

---

# 13. The explicit library as a dictionary, not the full deductive closure

Let

\[
\operatorname{Cl}(\Sigma)
\]

be the deductive closure of the current library: all consequences that can in principle be proved from it.

That set is far too large, often infinite, and contains endless trivial reformulations.

Therefore an explicit mathematical library should not attempt to name every true consequence. It should contain a useful **generating dictionary**:

- definitions;
- canonical lemmas;
- high-value theorems;
- important counterexamples;
- useful algorithms/constructions;
- multiple genuinely informative proof routes;
- translations between theories.

A conceptual library-design objective is

\[
L^*
=
\arg\min_L
\left[
\operatorname{DL}(L)
+
\mathbb E_{q\sim\mathcal D}C(q\mid L)
\right].
\]

The first term penalizes an enormous library. The second penalizes a library that makes future reasoning expensive.

This formalizes the intuition that statements like repeated conjunctions of an already known theorem are valid but not worth naming.

Verification answers:

> Is this artifact formally valid?

Curation answers:

> Does this artifact deserve explicit memory, status, and navigational prominence?

Those are fundamentally different questions.

---

# 14. Conjecture value should include information gain, not only probability of truth

A conjecture generator that simply maximizes the probability that a statement is true will produce large amounts of trivial mathematics.

A valuable conjecture may be uncertain or even false if resolving it reveals a sharp structural boundary.

A conceptual value-of-information score is

\[
\operatorname{VOI}(P)
=
\mathbb E_r
\left[
U(\mathfrak M_{t+1}\mid r)-U(\mathfrak M_t)
\right]
-
C_{\mathrm{resolve}}(P),
\]

where outcomes may include

\[
r\in
\{
\text{proved},
\text{refuted},
\text{partially resolved},
\text{independent},
\text{unresolved}
\}.
\]

A practical approximation is to temporarily assume the conjecture and examine the valuable region it unlocks:

\[
\Sigma,h:P\vdash Q.
\]

If assuming \(P\) allows many important consequences, then resolving \(P\) may have high value. The same analysis can be performed under \(\neg P\).

This resembles influence analysis on the mathematical substrate, but conditional dependencies must remain explicitly marked as conditional rather than verified facts.

---

# 15. The shared-backbone hypothesis

If proving, statement construction, and abstraction discovery all operate over related typed objects, one could imagine a shared structural encoder

\[
z
=
F_\theta(\Sigma,\Gamma,A,\text{local/global neighborhood}).
\]

Task-specific policies then operate on the same representation:

\[
\pi_{\mathrm{proof}}(z),
\qquad
\pi_{\mathrm{statement}}(z),
\qquad
\pi_{\mathrm{abstraction}}(z),
\qquad
V_{\mathrm{utility}}(z).
\]

Lean supplies formal validity rather than a neural `validity head`.

This model should not be built until the representation shows value on simpler experiments. But the reason it is attractive is that the tasks are mutually recursive in real mathematics:

- proof attempts suggest missing lemmas;
- repeated subproofs suggest definitions;
- counterexamples modify theorem statements;
- successful proofs reveal generalizations;
- new abstractions make new conjectures visible;
- conjectures create targets that produce proof-search experience.

The learned representation might therefore benefit from multi-task training if the substrate genuinely captures reusable structure.

---

# 16. Structural invariances a good representation should respect

A mathematically meaningful learned representation should ideally avoid relearning distinctions that are syntactically arbitrary.

Candidate invariances/equivariances include:

### Alpha-renaming invariance

Renaming a bound or local variable should not alter the mathematical state representation except through a corresponding identity map.

### Permutation invariance for independent context entries

If two hypotheses do not depend on one another, harmless reordering should not materially alter the semantic representation.

### Substitution equivariance

If a state is transported through a valid substitution \(f\), recommended structural actions should transport correspondingly:

\[
\pi(f^*s)
\approx
f^*\pi(s).
\]

This may be one of the most important formal expressions of “the same local machinery everywhere.”

### Definitional fold/unfold consistency

Replacing a named transparent definition by its body should change representation resolution without destroying core meaning.

### Equivalence transport

If structures are related by a certified equivalence, the representation should make corresponding transported reasoning accessible rather than treating the two regions as unrelated strings.

### Irrelevance robustness

Adding syntactically present but logically irrelevant context should have limited effect on the policy when the target does not depend on it.

These are useful sources of augmentations, evaluation tests, or architectural constraints.

---

# 17. Hypergraph structure: why ordinary dependency edges are insufficient

A proof step often consumes several premises jointly:

\[
\{A,B\}\to C.
\]

Representing this with independent edges

\[
A\to C,
\qquad
B\to C
\]

incorrectly suggests that either premise suffices.

Thus derivation structure is naturally hypergraphic or operation-centric: a rule instance has multiple typed inputs and one or more outputs.

However, even a hypergraph must preserve:

- binding;
- local context;
- substitutions;
- theorem instantiations;
- expression structure;
- provenance;
- rule/action identity.

This is why “a theorem dependency graph” is a useful projection but probably not the primitive substrate.

The current project should not become obsessed with whether the implementation is literally called a graph, hypergraph, term graph, or compiler IR. The mathematical requirement is preservation of the typed incidence and context information.

---

# 18. Alternative proofs are first-class routes

A theorem generally has no unique dependency set. Different proofs of the same proposition can expose radically different mathematics.

If

\[
p:P
\qquad\text{and}\qquad
q:P,
\]

then the final theorem interface is shared, but the derivational routes may differ in:

- dependencies;
- proof length;
- abstraction structure;
- conceptual explanation;
- computational content;
- portability to another theory;
- downstream usefulness.

Therefore a useful record should not identify “the theorem” with “one chosen proof path.”

Conceptually distinguish:

1. the statement/interface \(P\);
2. individual derivations \(p,q,\ldots\);
3. the dependencies and local states occurring along each derivation.

A future navigation system may show several routes to the same destination, much like a map offers different paths with different properties.

---

# 19. One exact core, many derived projections

The conversation initially spoke of several different graphs: theorem dependencies, proof states, concept graphs, theory graphs, applications, literature, and so on.

The refined view is:

> It may be possible to maintain one exact typed core and derive multiple **projections** or overlays from it, rather than maintaining unrelated truth stores.

Examples:

### Declaration dependency projection

For each declaration, project the constants occurring in its type or selected proof/body.

### Proof-state projection

Project observed states and transitions during proof construction.

### Expression projection

Expand a declaration into its typed term structure.

### Module / namespace projection

Aggregate declarations according to source organization.

### Conceptual projection

Later, collapse exact structures into human-scale concepts. This projection may be learned or curated rather than kernel-certified.

### Provenance / literature overlay

Attach source, author, timestamp, paper, project, or historical metadata to exact artifacts.

### Application overlay

Attach models, algorithms, assumptions, software, or empirical interpretations. These are not derivable purely from Lean logic.

The important design principle is that inferred semantic layers should remain anchored to exact IDs and explicitly labeled by trust status.

---

# 20. Google Maps: two distinct forms of zoom

The map analogy yielded one of the strongest ideas in the conversation. “Zoom” should be separated into two operations.

## 20.1 Certified structural zoom

A declaration can be viewed as one opaque node or expanded into its exact implementation/proof term.

A theorem may support resolutions like:

\[
1\text{ theorem}
\to
10\text{ named lemmas}
\to
100\text{ proof-state steps}
\to
10^4\text{ expression nodes}.
\]

Every collapse/expansion at this layer should be mechanically related to the exact formal artifact.

Definitions and lemmas naturally provide existing abstraction boundaries.

## 20.2 Learned or human semantic zoom

A human may summarize a 100-step proof as:

1. reduce to a compactness claim;
2. obtain a finite subcover;
3. derive a uniform bound;
4. conclude.

Those four concepts may not correspond to literal contiguous term subtrees. They are semantic interpretations.

Thus a future map should distinguish:

- **certified zoom**: exact expansion/collapse backed by formal structure;
- **semantic zoom**: task-conditioned abstraction with confidence/provenance.

A general task-conditioned map can be written

\[
C_q:G_{\mathrm{exact}}\to G_{\mathrm{task},q},
\]

where \(q\) might be:

- proof search;
- human explanation;
- prerequisite learning;
- semantic audit;
- application discovery.

The scientific question becomes:

> Which formal information can be discarded for which task without materially harming performance?

That is measurable and more useful than arguing abstractly that mathematics “has scales.”

---

# 21. Mathematical importance as marginal future utility

Graph centrality, citation count, and theorem usage are crude proxies for importance.

A more structural idea is to define the importance of an artifact \(T\) through its marginal reduction of future mathematical cost:

\[
I(T)
=
\mathbb E_{Q\sim\mathcal D}
\left[
C(Q\mid\Sigma\setminus\{T\})
-
C(Q\mid\Sigma)
\right].
\]

Interpretation:

> How much harder would future mathematics become if this theorem/definition were unavailable as a reusable interface?

Possible cost functions include:

- proof-search nodes;
- proof length;
- retrieval difficulty;
- model compute;
- human time;
- description length;
- number of auxiliary abstractions required.

This creates a direct connection among:

- theorem importance;
- abstraction quality;
- library curation;
- compression;
- curriculum design.

It is difficult to estimate but conceptually powerful.

---

# 22. The library as environment, curriculum, and replay buffer

If the representation eventually records not only final theorems but also local states and search trajectories, the same substrate can play several roles.

### Environment

The current library determines the reusable actions and objects available to the agent.

### Dataset

Verified declarations and proof traces provide supervised learning examples.

### Replay buffer

Successful and failed search trajectories can be revisited for policy/value learning.

### Curriculum

Reachability from the existing library can help identify tasks near the current frontier of an agent's capability.

### Map

Humans and agents can navigate dependencies, proof routes, and abstraction levels.

### Historical process record

A temporal layer can preserve failed branches, alternative proofs, conjecture revisions, and discovery order.

This is one reason better storage and better learning may eventually become tightly coupled: the organization of the library determines the environment in which future mathematical search occurs.

---

# 23. Temporal mathematics: products versus process

Traditional mathematical artifacts preserve successful products much better than process.

A richer future record could distinguish:

### Products

- definitions;
- theorem statements;
- proofs;
- counterexamples;
- algorithms.

### States

- local contexts;
- goals;
- partial terms;
- available declarations.

### Processes

- successful transitions;
- failed proof actions;
- backtracking;
- alternative routes;
- conjecture revisions;
- experiments and observations.

### Views

- human summaries;
- learned abstractions;
- domain maps;
- prerequisite paths.

The exact MVP currently focuses on products and states. The process layer becomes valuable if the project reaches dynamic tracing.

---

# 24. Theory transport may matter more than graph proximity

Many important cross-field connections are not merely “nearby subgraphs.” They arise because one mathematical structure can be mapped into another in a way that preserves relevant operations or truths.

Schematically,

\[
F:\mathcal T_1\to\mathcal T_2.
\]

Examples in ordinary mathematics include transforms, representations, dualities, equivalences, reductions, and functorial constructions.

A hard problem in \(\mathcal T_1\) may become easy after transport to \(\mathcal T_2\), after which the result is transported back.

This suggests a long-term distinction:

- **local retrieval:** find useful nearby declarations;
- **structural transport:** find a map that moves the entire problem into a better representation.

If agents ever discover deep cross-field connections, learned theory-level transport may be more important than ordinary graph distance or spectral proximity.

This is far beyond the current implementation gates, but it should remain visible as a reason not to overfit the substrate to declaration adjacency alone.

---

# 25. Power laws versus hierarchical compressibility

The original intuition included the possibility that mathematics has power-law graph structure.

That may or may not be statistically accurate depending on the projection and edge type. It should not be an architectural assumption.

The stronger and more useful hypothesis is:

> Mathematics may be **hierarchically compressible**.

That means useful abstractions repeatedly collapse large detailed constructions into smaller reusable interfaces, producing structure at multiple scales.

A possible future empirical test is a renormalization-style experiment:

1. begin with a fine proof representation;
2. repeatedly collapse verified reusable substructures;
3. measure proof motifs, action distributions, retrieval performance, or difficulty predictors across scales;
4. test whether useful statistical regularities remain approximately stable.

If so, there would be empirical evidence for scale-invariant reasoning structure rather than merely a visual resemblance to a power-law network.

---

# 26. What it should mean for an object to “represent mathematics”

The phrase should be scoped carefully.

A practical representation need not encode every aspect of human mathematical meaning in one primitive data structure.

A more defensible target is an object satisfying the following properties.

### Formal faithfulness

Every represented formal artifact can be related back to the exact Lean environment and checked term/type structure.

### Contextual completeness

Local meaning, binders, assumptions, and scope are preserved rather than flattened into global strings.

### Compositionality

Large mathematical objects are built from smaller typed objects in a way that can be expanded and recomposed.

### Extensibility

New declarations, proof traces, semantic annotations, provenance, and applications can be attached without changing the meaning of old certified records.

### Multiresolution access

The same artifact can be inspected at several useful scales while maintaining links to exact underlying structure.

### Multiple derivations

Alternative proofs or constructions can coexist without being collapsed into one dependency story.

### Trust separation

Kernel-certified facts, observed process data, heuristic relationships, and human/learned semantic claims remain distinguishable.

### Learnability

The representation supports experiments on retrieval, prediction, transfer, compression, abstraction, or navigation.

If one extensible object satisfies these properties, it may be reasonable to call it a useful **representation substrate for formal mathematics** even if it is not a philosophical foundation of all mathematical meaning.

---

# 27. A candidate expanded research state — only as a north-star model

The immediate record is intentionally small:

\[
\mathcal R=(E,X,D,S,T).
\]

For long-term thinking, one can imagine a richer state

\[
\mathfrak M_t
=
(\Sigma_t,
\mathcal S_t,
\mathcal T_t,
\mathcal O_t,
\mathcal A_t,
\mathcal V_t,
\mathcal P_t).
\]

Possible meanings:

- \(\Sigma_t\): verified library/environment;
- \(\mathcal S_t\): formal local states;
- \(\mathcal T_t\): observed transitions and derivations;
- \(\mathcal O_t\): experiments, examples, counterexamples, observations;
- \(\mathcal A_t\): abstraction hierarchy / zoom mappings;
- \(\mathcal V_t\): learned or curated utility/value annotations;
- \(\mathcal P_t\): provenance and temporal history.

This should **not** be treated as a schema proposal. Its purpose is to show that the exact core can remain the anchor while richer mathematical activities are layered around it.

---

# 28. A concise north-star loop

The complete conceptual process that emerged from the conversation is:

\[
\boxed{
\begin{aligned}
\text{Explore}
&\to
\text{Propose / shape statements}
\leftrightarrow
\text{Create abstractions}\\
&\to
\text{Solve / refute}
\to
\text{Verify with Lean}\\
&\to
\text{Curate}
\to
\text{larger verified library}
\to
\text{Explore again}.
\end{aligned}
}
\]

Or at the highest level:

\[
\boxed{
\text{global substrate}
\to
\text{local search}
\to
\text{verified construction}
\to
\text{compression / curation}
\to
\text{improved substrate}.
}
\]

This loop is more important than any particular graph terminology.

---

# 29. The strongest research hypotheses to preserve

The following are the ideas from the conversation most worth keeping alive. They are ordered roughly from nearest-term to most speculative.

## H1. Structural representation hypothesis

A normalized Lean-native representation of \((\Sigma,\Gamma,A)\) provides useful signal beyond tokens and flat declaration dependencies.

## H2. Local-transfer hypothesis

Proof policies trained on structural states transfer better across domains because substantial mathematical reasoning has reusable local structure.

## H3. Hybrid hypothesis

The best representation will likely combine exact formal structure with learned semantic/text embeddings rather than replacing language entirely.

## H4. Multiscale hypothesis

Different mathematical tasks require different resolutions of the same underlying formal object, and task-conditioned zoom can discard large amounts of detail without sacrificing performance.

## H5. Abstraction-as-compression hypothesis

Useful definitions and lemmas can be discovered by identifying recurring structures whose introduction reduces held-out future reasoning cost.

## H6. Shared-representation hypothesis

Proof discovery, statement synthesis, theorem shaping, and abstraction invention can share a learned mathematical backbone because they are conditional operations over related typed structures.

## H7. Utility-learning hypothesis

Mathematical importance can be approximated by future reuse, compression, influence, or proof-cost reduction sufficiently well to support automated curation.

## H8. Process-data hypothesis

Failed proof attempts, alternative routes, counterexamples, and discovery traces contain valuable training information not present in final proof corpora.

## H9. Theory-transport hypothesis

Some high-value cross-domain discoveries can be modeled as finding structure-preserving transformations between mathematical regions rather than simple graph proximity.

## H10. Hierarchical-compressibility hypothesis

Mathematics exhibits useful statistical regularities across abstraction scales because definitions and theorems repeatedly compress recurring structure.

None of H2–H10 should be assumed true merely because the formal picture is elegant.

---

# 30. Questions the coding agent should keep nearby — not requirements

While implementing the immediate core, these questions may help avoid choices that unnecessarily close future doors:

1. Can every derived view point back to exact expression/declaration/state identities?
2. Is local context represented richly enough to support substitution and binder-aware comparison later?
3. Can alternative proof routes be stored without forcing a theorem to have one canonical dependency set?
4. Can definitions be expanded and collapsed mechanically?
5. Can failed and successful dynamic states be added later without redesigning the static core?
6. Can trust status distinguish verified facts from inferred semantic relationships?
7. Can identifiers survive alpha-renaming, recompilation, and benign formatting changes where appropriate?
8. Does the representation make it possible to compare two states structurally after renaming locals?
9. Is text preserved as a useful modality rather than discarded in pursuit of structural purity?
10. Could a future task-conditioned projection select a small neighborhood without copying truth into another independent database?
11. Could proof-search cost be measured before and after adding a proposed lemma or definition?
12. Is provenance/version information sufficient to treat the mathematical environment as evolving over time?

These are design-pressure checks, not instructions to implement speculative functionality now.

---

# 31. What not to infer from this document

Do not infer that:

- dependent type theory is proven to be the optimal neural representation;
- mathematics has one canonical graph;
- mathematics follows a pure power law;
- local proof moves are sufficient for deep discovery;
- compression alone defines mathematical value;
- conjecturing is primarily statistical induction;
- a graph neural network is necessarily the right architecture;
- the final system should replace Lean;
- kernel validity implies semantic correctness, novelty, or importance;
- one chosen proof gives the intrinsic dependency structure of a theorem;
- an elegant formal ontology is evidence that the ML hypothesis works.

The purpose of the immediate experiments is precisely to distinguish attractive structure from useful structure.

---

# 32. Final conceptual picture

The most mature synthesis reached in the conversation is this:

> **Formal mathematics can be viewed as a growing typed environment in which local mathematical states have the form \(\Sigma;\Gamma\vdash ?e:A\). Lean supplies exact syntax, typing, local contexts, proof terms, computation, and verification. Mathematical activity repeatedly transforms these local states, packages successful constructions into reusable abstractions, and enlarges the environment. A useful future system would preserve this exact core while learning how to retrieve, navigate, compress, abstract, propose, and curate mathematics at multiple scales.**

In the Google Maps metaphor:

- Lean is the surveyed ground truth and coordinate system;
- exact expressions and declarations are the road geometry;
- proof traces are routes;
- definitions and lemmas are named highways and interchanges;
- alternative proofs are alternate routes;
- semantic zoom produces city/state/country-scale views;
- theory translations connect different map projections;
- conjectures are proposed destinations;
- exploration is reconnaissance;
- verification confirms that a claimed route really connects its endpoints;
- curation determines which roads and landmarks deserve to appear prominently on the map.

The near-term project only needs to establish that the ground-truth record is faithful and structurally useful. If that succeeds, the ideas above provide a mathematically rich set of directions for what the object might eventually become.
