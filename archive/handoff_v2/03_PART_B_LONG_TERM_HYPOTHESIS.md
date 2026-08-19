# Part B — The Long-Term Hypothesis

This document preserves the larger idea without pretending that it has been validated.

## 1. The enduring vision

The desired end state is not merely a theorem database.

It is a living mathematical record that can support:

- exact verification;
- local proof construction;
- alternative routes and failed attempts;
- definitions and abstractions;
- statement synthesis and refutation;
- curation and importance;
- multiscale navigation;
- human and agent collaboration.

The intuition is that formal mathematics contains global accumulated structure and recurring local typed activity. The research hypothesis is that a learner operating on this structure can transfer reasoning patterns, compress mathematical knowledge, and navigate it more effectively than systems based only on surface text.

## 2. The long-term single object

If the immediate core succeeds, extend it to

\[
\boxed{\mathcal W_t=(\mathcal R_t,\mathcal O_t,\mathcal V_t)}.
\]

- \(\mathcal R_t\): the exact formal core from Part A.
- \(\mathcal O_t\): an epistemic and activity overlay.
- \(\mathcal V_t\): a system of task-specific views and coarse-grainings.

This is still one versioned object. The layers are separated by trust, not stored as unrelated products.

### Exact core \(\mathcal R_t\)

Lean-checked or Lean-derived declarations, expressions, states, transitions, environments, and certificates.

### Epistemic/activity overlay \(\mathcal O_t\)

Records such as:

- conjectures;
- computational observations;
- counterexamples;
- failed attempts;
- alternative formalizations;
- informal explanations;
- provenance and historical sequence;
- candidate equivalences and analogies;
- novelty and utility estimates.

Every edge has a relation type, source, time, and confidence/trust class.

### View system \(\mathcal V_t\)

Maps the exact object to task-specific representations:

\[
C_q:\mathcal W_t\longrightarrow\mathcal W_{t,q}^{(k)},
\]

where \(q\) is a task and \(k\) is a resolution budget.

Examples:

- five conceptual units for a high-level explanation;
- 100 units for premise retrieval;
- 1,000 units for semantic auditing;
- full expression detail for kernel checking.

This is the rigorous version of the Google Maps idea: one territory, multiple resolutions, with explicit knowledge of what was collapsed.

## 3. The mathematical activity loop

A mature system would support:

\[
\boxed{
\text{Explore}
\rightarrow
\text{Represent/Propose}
\rightarrow
\text{Solve or Refute}
\rightarrow
\text{Verify}
\rightarrow
\text{Curate}
\rightarrow
\text{Explore again}.
}
\]

### Explore

Compute examples, search finite models, inspect failed proofs, compare analogous structures, and seek counterexamples. Exploratory evidence is not proof.

### Represent

Introduce useful definitions, interfaces, invariants, or intermediate lemmas. A transparent definition is a verified representation change; an abstraction is useful only if it reduces future work or exposes reusable structure.

### Propose

Synthesize a candidate theorem type. Hypotheses and conclusions are parts of one formal statement, though the system may separately model the discovery of a pattern and its precise formalization.

### Solve or refute

Construct a proof term, a certified counterexample, or a partial result.

### Verify

Lean checks formal validity. The learned system does not replace this function.

### Curate

Decide whether the artifact deserves explicit status in the library or map. Validity does not imply novelty, nonredundancy, clarity, or importance.

## 4. Shared-representation hypothesis

The long-term ML hypothesis is:

\[
z=F_\theta(\Sigma,\Gamma,A,\text{relevant neighborhood}),
\]

with different conditional policies operating over \(z\):

\[
\pi_{\mathrm{proof}},\quad
\pi_{\mathrm{statement}},\quad
\pi_{\mathrm{abstraction}},\quad
V_{\mathrm{utility}}.
\]

Lean supplies validity, not the learned value function.

This architecture is plausible because all activities manipulate typed mathematical objects in shared environments. It is not established. The immediate gates are designed to determine whether the shared structural representation has any measurable advantage.

## 5. Long-term gates, in order

These gates are conditional. Do not begin one because it is exciting; begin it only because the preceding evidence supports it.

### Gate 6 — Cross-domain next-step transfer

**Question:** Is there reusable local “physics” of proof construction?

Task:

\[
(\Sigma,\Gamma,A)\longrightarrow\text{next proof action}.
\]

Train on selected domains and test on held-out domains. Compare token, structural, and hybrid representations with matched budgets.

**Positive evidence:** statistically credible improvement on held-out domains and either at least 5% relative improvement on the primary action metric or a meaningful reduction in end-to-end proof-search cost.

**Strong evidence:** roughly 10% or more relative improvement, materially better sample efficiency, or at least 20% fewer search nodes at matched success.

### Gate 7 — Learned zoom

**Question:** Can the system discard formal detail in a task-dependent way without losing what matters?

Construct views at several budgets and measure downstream performance.

**Positive evidence:** a view using no more than 20% of the exact units retains at least 95% of the full representation's performance on a predeclared task, or materially improves human navigation while preserving verifiable expansion links.

The learned view must record what was collapsed and remain connected to exact core IDs.

### Gate 8 — Abstraction invention

**Question:** Can repeated proof structure be converted into a useful definition or lemma?

A candidate abstraction must:

- be expressible and verifiable in Lean;
- avoid merely memorizing one proof;
- apply to held-out tasks;
- reduce future proof-search or description cost.

A simple utility target is

\[
\Delta C=
C(\text{held-out proofs without abstraction})-
C(\text{held-out proofs with abstraction}).
\]

**Positive evidence:** verified, nontrivial abstractions reduce aggregate held-out proof cost by at least 10% in several independent motifs or domains.

### Gate 9 — Statement synthesis and refutation

**Question:** Can the system propose statements that are resolvable, nontrivial, nonredundant, and structurally useful?

Do not evaluate by raw theorem count.

Require:

- proof or certified counterexample rate;
- redundancy checks against the existing library;
- controls for vacuity and trivial reformulation;
- downstream utility or expert judgment on a bounded benchmark.

The system should be rewarded for informative false conjectures as well as true ones when their counterexamples reveal useful boundaries.

### Gate 10 — Curation and value

**Question:** Can the system predict what deserves explicit memory?

Possible targets include:

- realized future reuse;
- reduction in future proof cost;
- compression of later declarations;
- bridge value across modules;
- novelty and redundancy;
- expert-maintainer decisions.

A useful initial test is retrodictive: using only information available when a declaration was introduced, predict its future load-bearing role better than citation count, degree, length, and text baselines.

### Gate 11 — Theory-level transport and applications

**Question:** Can the system find structure-preserving maps between mathematical regions and use them to transfer results?

This is closer to deep cross-field discovery than ordinary graph proximity. It should only be attempted after structural transfer and abstraction learning have worked at smaller scales.

## 6. What the final object would represent

If the program succeeds, the object would represent at least four aspects of mathematics:

1. **Products:** definitions, statements, proofs, counterexamples, algorithms.
2. **States:** contexts, goals, available constructions, partial terms.
3. **Processes:** successful and failed transitions, alternative routes, discovery history.
4. **Views:** human- and task-specific abstractions at multiple resolutions.

It would not identify formal validity with human meaning. Instead, it would anchor every semantic or conceptual view to an exact formal substrate and expose the trust boundary.

## 7. Why this could be important

The powerful possibility is not merely better search.

If local structure transfers, zoom can be learned, and abstractions can be scored by future utility, then the same record could become:

- a map for humans;
- a state space for proof agents;
- a replay buffer for learning;
- a curriculum generated from reachable frontiers;
- a substrate for abstraction discovery;
- a curation system for proof abundance.

That would be a substantial change in mathematical infrastructure.

But the program earns this conclusion only by passing the gates. Coherence is not evidence.

## 8. The honest end-state claim

The long-term goal is not to prove that one data structure is metaphysically identical to mathematics.

It is to build one extensible record that is expressive enough to host exact formal mathematics, mathematical activity, and multiple justified views without conflating them.

That is a strong and achievable notion of “an object that represents mathematics.”
