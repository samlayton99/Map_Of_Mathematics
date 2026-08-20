# ADR-0004 — Epistemic Layers (constitution amendment, Phase 4)

Date: 2026-08-19. Status: accepted (external judge ruling + owner direction).

## The change

The prior working constitution — "everything must be exact, name-free, kernel-invariant" — is narrowed to:

**Everything in the canonical verified structure must be exact and provenance-preserving. Derived views must explicitly declare what information they use and at which epistemic level.**

The levels:

1. **kernel** — facts of the type theory: statement/body, Prop/Type sorts, term positions and binder roles, the citation graph. Survive any Lean version by definition.
2. **library-relative** — measured quantities over a pinned snapshot: depth, in-degree, single-use status, concept universality, statement cones. Exact, but *expected to evolve* as mathematics grows; versioned, never claimed stable.
3. **elaboration-provenance** — what the source, as resolved by the elaborator, did: written citations, tactic invocations, intent. Recorded in a sidecar (`mathrecord provenance`), never mixed into the kernel record.
4. **semantic/experience** — human or model judgments (keyness, ratings). Clearly labeled; never inputs to levels 1–3.

## Why

The kernel can answer "this proof performs a classical-negation elimination here." It cannot answer "the mathematician chose proof by contradiction" — that fact existed at the source level and vanished in elaboration. Refusing to record it does not purify the map; it discards evidence (measured: the strategy channel scored near zero on intent-level strategies from kernel data alone). Conversely, letting provenance leak into the kernel structure would surrender exactness. Separation preserves both.

## Consequences adopted with this ADR

1. "Future-proof" is redefined: **the meaning of each relation must survive library evolution; its values at level 2 legitimately change.** Cross-version testing distinguishes extractor instability (level-1 outputs must be identical for identical proof terms) from map-geometry drift (level-2 change is expected and is itself data).
2. Single-use is a level-2 attribute and a zoom hint, never a semantic "container": named theorems are abstraction boundaries; `T -> L` is preserved, and `L`'s proof expands *beneath* it on zoom.
3. Prop-valued claim moves are one *view* of the heterogeneous structure, not the ontology of moves; construction/representation moves (Type-valued) remain a first-class future channel.
4. Every report states, per metric, which levels it consumed; proxy metrics carry proxy names (`top1_nonmachinery_proxy`, not "precision").
