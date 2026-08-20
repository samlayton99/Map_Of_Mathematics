# HYPERGRAPH_SCHEMA — nodes, artifacts, incidences, projections

The certificate-support hypergraph is **derived**, never primary. Everything
below is regenerable from the MathRecord dump; nothing here is a new source of
truth. Epistemic levels per ADR-0004 are marked on every field.

## Nodes

**Declaration nodes `D`** — one per constant in the compiled environment
(771,129). Fields:

| field | level | meaning |
|---|---|---|
| `id` | kernel | integer index, stable within a dump version |
| `name` | kernel | full name; used for display and joins, never for classification |
| `kind` | kernel | theorem / def / inductive / constructor / recursor / opaque / quot / axiom |
| `is_proof` (`pr`) | kernel | the constant's type is a Prop — it IS a proof |
| `is_prop_sorted` (`ps`) | kernel | its type telescopes to `Prop` — it IS a proposition or predicate |
| `arity` (`ar`) | kernel | binders the type telescopes through |
| `machine_generated` (`gen`) | elaboration | no recorded source declaration range |
| `depth` | library-relative | 1 + max over cited declarations; primitives 0 |
| `in_degree` | library-relative | distinct declarations citing it in a body |
| `stated_count` | library-relative | human theorem statements mentioning it |
| `module` | kernel | owning module, from the environment's own record |

**Proof-artifact nodes `P`** — one per declaration that has a body. A theorem's
own body is one artifact; each machine-generated helper it spawns
(`_proof_N`, `match_N`, `_unary`, equation lemmas) is a **separate** artifact,
so alternative and auxiliary certificates stay distinguishable.

| field | level | meaning |
|---|---|---|
| `id` | kernel | artifact index |
| `certifies` | kernel | the declaration this artifact is the body of |
| `is_generated` | elaboration | whether the artifact is compiler-emitted |
| `parent_boundary` | derived | for generated artifacts, the named declaration it belongs to (ADR-0005 label rules) |
| `n_incidences` | kernel | number of distinct declarations occurring in it |

`certifies(p, T)` is a function here — one artifact certifies one declaration.
Alternative proofs of the same theorem, when Mathlib carries them under
different names, are different declarations and therefore different artifacts;
the hypergraph keeps them separate and a later equivalence layer may relate
them. It must never merge them silently.

## Incidences

The bipartite incidence relation is the primary derived object. **Algorithms
operate on this**; clique expansion of a hyperedge is prohibited (ADR-0005).

`proof_occurs(p, d, roles)` — declaration `d` occurs in artifact `p`:

| field | level | meaning |
|---|---|---|
| `artifact` | kernel | `p` |
| `decl` | kernel | `d` |
| `roles[8]` | kernel | occurrence counts by role: 0 applied, 1 let-value, 2 explicit arg, 3 implicit arg, 4 instance slot, 5 strict-implicit, 6 type annotation, 7 unresolved |
| `load_bearing` | kernel | any occurrence in roles {0,1,2,7} |
| `in_statement_world` | library-relative | `d` is reachable from the certified theorem's statement closure |
| `delta_depth` | library-relative | `depth(certified) − depth(d)` |
| `d_target`, `d_cite` | library-relative | both endpoint depths, kept explicitly |

`statement_occurs(T, d)` — declaration `d` occurs in `T`'s **statement**. Kept
as a separate relation so the statement/proof distinction is never inferred.

`body_occurs(x, d, roles)` — the same relation for non-theorem declarations
(definitions, constructions, instances), so the definition layer is present in
the record even when a claim-only view hides it.

## Derived hyperedges

For artifact `p` certifying `T` under projection `π`:

    e_p^π : C_p^π ==> T,   C_p^π = { d : proof_occurs(p, d, ·) satisfies π }

Semantics fixed by ADR-0005: **observed support in one checked certificate**.
Not necessity, not minimality, not a canonical AND-set.

## The projection family (fixed in advance)

Each is an inclusion rule over incidences. All are monotone in evidence except
where noted, and all are reversible — the backing record is untouched.

| # | projection | inclusion rule | level |
|---|---|---|---|
| P1 | full certificate support | every occurrence, any role | kernel |
| P2 | load-bearing | roles {0,1,2,7} | kernel |
| P3 | claim citations | P2 ∧ is_proof ∧ kind ∉ {constructor, recursor} | kernel |
| P4 | frozen V8 content boundary | P3 minus logic-only and minus machinery, V8 rules frozen as of round 9 | library-relative (derived heuristic view, labelled) |
| P5 | statement-relative: proof-introduced | P2 ∧ ¬in_statement_world | library-relative |
| P6 | statement-relative: statement-world | P2 ∧ in_statement_world | library-relative |
| P7 | top-k | first k of P4's frozen order, k ∈ {1,2,4,8,16,all} | library-relative |
| P8 | definition/construction layer | `body_occurs` for non-theorem declarations | kernel |

P4 and P7 answer different questions and both ship: P7 bounds density and makes
slices comparable across theorems; P4 preserves variable proof complexity.

## Navigation controls (independent, never fused into one score)

1. **evidence tier** — core (P4) / support (P3) / background (P2) / all (P1).
2. **per-proof rank limit** — top 1, 2, 4, 8, 16, all, within the enabled tier.
3. **declaration-depth window** — arbitrary band, with the 50–75 band called
   out; two modes, *induced* (band only) and *portal* (band plus summarized
   links out of it).
4. **proof-expansion depth** — direct citations, one theorem boundary opened,
   two levels, or expand-on-demand.

Increasing any control **adds** evidence. No control may relabel or replace a
node that was already visible.

## Storage

Column-oriented arrays keyed by incidence, written once per dump version:

    nodes.npz       id, kind codes, pr/ps/ar/gen flags, depth, in_degree, stated
    artifacts.npz   id, certifies, is_generated, n_incidences
    incid.npz       artifact, decl, roles[8], load_bearing, in_stmt_world,
                    d_target, d_cite, delta_depth

Every projection is a boolean mask over `incid`, computed on demand. This is
what makes the family reversible by construction: a view is a mask, not a
rebuild, so no view can lose evidence the record holds.
