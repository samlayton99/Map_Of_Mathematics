# 02 — Formal Theory

## 1. Four layers, not one score

### Layer A — Canonical local move object

For a checked proof artifact

\[
p:T,
\]

construct a rooted typed DAG/hypergraph \(P(p)\).

Its nodes are occurrence-level objects such as:

- named application occurrences;
- constructors and witnesses;
- definition folds/unfolds;
- rewrites/transports;
- local hypotheses;
- generated helpers;
- exact subterms.

Its relations preserve:

- expression path;
- parent application;
- argument index and binder role;
- local context;
- substitution/instantiation;
- resulting type/subgoal;
- generated-owner relation.

If \(p\) is unchanged, \(P(p)\) is unchanged under unrelated library growth.

### Layer B — Intrinsic local descriptors

For an occurrence \(e\) of declaration \(c\) in proof \(p:T\), retain a stable vector

\[
x(e)=
(
\text{move kind},
\text{nesting},
\text{occurrence role},
\text{statement relation},
d_T,
d_c,
\Delta d,
\text{arity},
\text{isProof},
\text{generated/owner},
\text{interface anchoring},
\text{local contribution}
).
\]

Do not immediately compress this vector to one scalar.

### Layer C — Global atlas

Aggregate local move objects while retaining artifact and occurrence identity:

\[
A_t=\operatorname{colim}_{p\in M_t} P(p).
\]

Informally, this is a union of local proof structures with declaration interfaces identified but local occurrences preserved.

Append-only growth gives an embedding

\[
A_t\hookrightarrow A_{t+1}
\]

that leaves the old induced structure unchanged.

### Layer D — Dynamic global fields

At version \(t\), attach sidecars such as:

\[
g_t(v,e)=
(
\text{usage},
\text{rarity},
\text{centrality},
\text{community},
\text{branch relevance},
\text{learned utility}
).
\]

These may change as mathematics grows.

They are not canonical local edges.

## 2. Why exact append-safe universality is impossible

Suppose \(f(T,c)\) depends only on:

- the unchanged proof occurrence;
- \(T\) and \(c\);
- their types, bodies, and down-sets.

Now take two declarations with identical local/down-set structure. Extend the library by adding many new proofs citing only the first.

Their future/global universality differs, while every input to \(f\) remains identical.

Therefore:

> No append-invariant local/down-set statistic can exactly equal a future/use-based universality statistic in general.

This is not an engineering failure. It is an information limitation.

Consequences:

- `delta_depth` cannot be universality.
- arity cannot be universality.
- cone size cannot be universality.
- a pinned count table is a historical field, not an intrinsic property.

## 3. What `delta_depth` actually is

Define

\[
\Delta d(T,c)=d(T)-d(c).
\]

This measures **vertical abstraction span**.

It tells us how far a direct certificate reference drops in the depth stratification.

It does not tell us by itself whether the edge is:

- a false shortcut to universal plumbing;
- a legitimate descent to foundations;
- or a valuable long-range mathematical bridge.

Use the two-dimensional geometry:

\[
(d(c),\Delta d(T,c)).
\]

Interpretation:

- low cited depth, large drop: likely vertical foundational support;
- high cited depth, small drop: local high-level neighbour;
- high cited depth, large drop: candidate long-range bridge;
- low cited depth, shallow target: legitimate foundational mathematics.

This is more informative than a single “bad edge” score.

Also test:

\[
\Delta_{\mathrm{rel}}=\frac{d(T)-d(c)}{1+d(T)}
\]

and within-proof rank of \(\Delta d\) as candidate scale-normalized coordinates.

## 4. Vertical versus lateral navigation

A depth-200 theorem citing `Eq` should not necessarily be rendered as a lateral neighbour of `Eq`.

It is better interpreted as a **vertical support portal**.

At a given zoom/abstraction level:

- same-scale edges support lateral exploration;
- large-drop edges support drill-down;
- high-depth long-span edges are explicit bridge candidates.

This avoids deleting exact support while preventing foundational nodes from collapsing horizontal map distance.

## 5. Multifiltration rather than weighted sum

Let:

- \(q(e)\) be intrinsic local salience/layer;
- \(s(e)\) be abstraction span;
- \(\ell(e)\) be relation lane.

Define views

\[
V_{\alpha,\beta,L}(A_t)
=
\{e:
q(e)\succeq \alpha,\;
s(e)\preceq\beta,\;
\ell(e)\in L
\}.
\]

This is a multi-parameter filtration.

Examples:

- show the first two local move layers;
- show definitions/constructions but hide instance support;
- show same-scale neighbours;
- show long-range bridge candidates;
- show all exact support.

Do not collapse \((q,s,\ell)\) to one weighted sum unless a particular downstream policy requires it.

## 6. The likely root error: flattening

The current hyperedge

\[
\{c_1,\ldots,c_n\}\Rightarrow T
\]

puts every cited declaration at one level.

But in the exact proof term:

- one citation may be the head of a major application;
- another may prove one premise of that application;
- a third may fill an implicit type parameter;
- a fourth may be an instance generated inside that premise.

Flattening turns descendants into siblings and gives every occurrence a direct edge from \(T\).

Two observed phenomena may be consequences:

1. Global rarity is needed to push ubiquitous descendants down the flat list.
2. Universal constants become direct hubs and collapse global distances.

The hierarchy-restoration hypothesis is therefore prior to another scoring search.

## 7. Definitions need typed lanes

A definition can appear as:

- a concept in the theorem statement;
- a type annotation;
- an implicit interface parameter;
- a construction used by the proof;
- an unfolding/folding action;
- an instance implementation.

These are not interchangeable.

At minimum separate:

1. **move lane** — active construction/unfolding/application;
2. **concept lane** — vocabulary/type/interface;
3. **infrastructure lane** — instance/generated/elaboration support.

Definitions remain first-class in all lanes.

## 8. Coherence conditions between local and global layers

A split local/global architecture is principled if it satisfies:

1. **Faithfulness:** every global edge traces to an exact occurrence or an explicitly derived relation.
2. **Local naturality:** unchanged proofs retain identical local objects under extension.
3. **Monotone expansion:** opening a view reveals hidden exact structure; it never invents support.
4. **Refinement consistency:** expanding a global edge lands on the corresponding local move.
5. **Typed transparency:** theorem, definition, construction, instance, and generated relations remain distinguishable.
6. **Versioned dynamics:** changing global centrality or rarity does not mutate the canonical local object.
7. **Route honesty:** synthetic roots, collapsed owners, and portal edges are visibly derived.
