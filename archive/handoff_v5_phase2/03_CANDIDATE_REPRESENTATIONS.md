# Candidate Representations of Mathematical Structure

## 1. Exact starting object

Fix a Lean environment \(\Sigma\).

A declaration has approximately:

\[
d : \tau_d := \beta_d,
\]

where \(\tau_d\) is its exact type/interface and \(\beta_d\) is its body or proof when available.

MathRecord already stores exact representations of these objects.

No human-scale map is assumed yet.

## 2. Candidate projection P0 — Exact term graph

For a proof term \(p:T\), retain the exact Lean expression DAG.

Advantages:

- formally complete;
- reconstructible/checkable;
- no semantic guesswork.

Limitations:

- enormous;
- implementation-shaped;
- poor default human view;
- may obscure named mathematical structure.

## 3. Candidate projection P1 — Direct reference occurrences

Record every named declaration occurrence in the theorem type or proof body, preserving multiplicity and expression location.

This is exact as occurrence data.

It does not encode importance, necessity, or conceptual role.

## 4. Candidate projection P2 — Deduplicated support set

\[
\operatorname{Supp}(p)=\{d\mid d\text{ occurs in }p\}.
\]

Advantages:

- simple;
- highly compressed;
- easy to compute;
- useful premise-selection target.

Limitations:

- loses multiplicity, order, nesting, and local role;
- includes infrastructure;
- not a set of minimal logical premises;
- not automatically an AND inference edge.

Treat it as a candidate proof summary, not a settled map.

## 5. Candidate projection P3 — Filtered support

Apply deterministic infrastructure classifications while retaining the raw support set.

Possible classes include:

- typeclass machinery;
- coercions;
- generated recursors;
- basic logical constructors;
- implementation details;
- domain declarations.

Filtering is a view, not formal truth. Every exclusion needs a reason and must be reversible.

## 6. Candidate projection P4 — Named application occurrences

Extract maximal application spines headed by named declarations:

\[
d\;a_1\cdots a_k.
\]

Preserve:

- head declaration;
- arguments;
- inferred result type when available;
- local binder dependencies;
- nesting/parent relation;
- expression path.

This may better represent “how a theorem was used,” but it still does not reveal the author's conceptual intent.

## 7. Candidate projection P5 — Source/elaborator use route

Use explicit tactic/source events such as:

- `apply L`;
- `rw [L]`;
- `exact L ...`;
- `unfold D`.

Advantages:

- closer to author action;
- role often explicit;
- naturally contextual.

Limitations:

- source-style dependent;
- unavailable for many term proofs;
- automation can hide many uses;
- one tactic may generate complex term structure.

## 8. Candidate projection P6 — Human or natural-language route

A human or future tagging agent identifies conceptual moves:

- “apply compactness”;
- “pass to the dual space”;
- “use Jensen's inequality”;
- “reduce to the finite case.”

This may be the most useful map level, but it is not kernel-certified and may not be recoverable from formal syntax alone.

## 9. Candidate interface view

A theorem type

\[
\Pi (x_1:A_1)\cdots(x_n:A_n),R
\]

can be exposed as a typed telescope.

Classifying binders as parameters, premises, instances, witnesses, or outputs is a derived interpretation. The exact telescope is formal; the role labels are not always unambiguous.

## 10. AND–OR interpretation

Alternative proof artifacts do create OR structure in the weak sense that several certificates inhabit the same exact theorem type.

Within one proof, the support set may be displayed jointly, but it should not be called a set of logically necessary premises.

The AND–OR hypergraph is therefore one candidate visualization of certificate structure, not a proven ontology of mathematics.

## 11. What the study must determine

- Which projection gives the shortest useful proof hint?
- Which retains enough structure for navigation?
- Which survives automation and different proof styles?
- Which can be extracted at scale?
- Which requires semantic annotation?
- Which is best treated as a stored entity versus a computed view?
