# Candidate Representation Definitions (as implemented)

Phase 2A operational definitions. Every projection is a computed view over the exact Gate-1 record; raw data is never replaced by a filtered view. Extraction: `mathrecord study <file.lean> <out.json>` (one file per process). Trust classes: `lean-exact`, `observed`, `deterministic-derived`; semantic judgment is explicitly absent (P7 hook only).

## P0 — exact proof-term expression graph  [lean-exact]

The Gate-1 record itself: deduplicated expression table (`record.expressions`), declaration type/value roots, canonical sids. Sizes reported as `Expr.sizeWithoutSharing` per declaration (`declStudies[].sizes`).

## P1 — direct named reference occurrences  [lean-exact]

Every `const` occurrence in a declaration's type (`p1_typeRefs`) and body/proof (`p1_bodyRefs`), with the expression path (child-edge string, e.g. `r.f.a.b`) preserving position and multiplicity. Derivation: total recursive walk of the mdata-stripped `Expr`; no filtering.

## P2 — deduplicated support set  [deterministic-derived]

`p2_supportType` / `p2_supportBody`: first-occurrence-ordered dedup of P1 per layer. Never merged across layers; never labeled as necessary logical premises.

## P3 — infrastructure-classified support  [deterministic-derived, reversible]

Each referenced declaration gets `classification[]` from documented deterministic classifiers (`referencedDecls`): `typeclass-instance` (env instance table), `recursor` (kind), `structure-projection` (env projection table), `generated` (suffix list: rec/casesOn/brecOn/…/match_*/proof_*), `internal-detail` (`Name.isInternalDetail`), `eq-machinery` (fixed list: `Eq.mpr`, `congrArg`, …), `logic-core` (fixed list: `And.intro`, …), `coercion` (name-root list). Empty list = unclassified = presumed domain mathematics. Filtering means hiding classified items in a view; the raw set always remains (P2), every exclusion carries its class as reason.

## P4 — named application occurrences  [deterministic-derived]

Maximal application spines `d a₁ … aₖ` with `const` heads, from a binder-instantiating walk of the proof term (`p4_apps`): head, arg count, per-arg head tags, per-arg is-proof (Meta), inferred result-type head and is-Prop (`Meta.inferType` under the live telescope; `resultOk=false` marks failures loudly), parent-occurrence nesting, depth, expression path. Zero-arg constant uses are recorded as spines of arity 0. `p4_completeness` marks failure or absence per declaration.

## P5 — source/elaborator use route  [observed]

`useEvents`: for explicit tactic families only (`apply`, `exact`, `refine`, `rw`/`rewrite`, `unfold`, `simp`/`simp_all`, `constructor`, `exacts`, `induction`, `cases`, `have`, `specialize`, `calc`), one event per TacticInfo node with: role, source span, action text (display-only label), before/after state ids (linked to the Gate-1 state store), and attributions. Attribution = head constants of the topmost elaborated terms (`TermInfo.expr`) under the nearest substantive enclosing tactic — resolved elaborator objects, never parsed display text. `completeness = no-named-attribution` when a family tactic has no const-headed elaborated term (e.g. rewriting with a local hypothesis, bare `constructor`, closed-term automation). Nested duplicates (`rw` wrapping `rewrite`) are deduplicated at analysis time by source span, keeping the attributed inner node. `nonFamilyTacticKinds` tallies everything outside the families for coverage accounting.

## P6 — one-level selective expansion  [deterministic-derived]

For a chosen declaration: its P2 support (direct backing) joined with each supporting declaration's shallow record (kind, typeSid, module, classification). Computed at analysis time from `declStudies` + `referencedDecls`; no assumption that this is the right zoom model.

## P7 — semantic/human route  [hook only, no data in this run]

Append-only annotation attachment keyed by stable ids (decl name + env fingerprint, state id, event index). Schema per `handoff/00` §11. Not synthesized in this run; the reviewer worksheet is the designated entry path.

## Use events (Phase 2B)

The P5 events are the Phase 2B feasibility dataset. Tier mapping: role from an explicit family with elaborator attribution = Tier A/B (explicit role, deterministic attribution); `no-named-attribution` = classified unavailable; multiple attributions on one event are stored, not resolved (Tier C preserved). Instantiation completeness = arg/universe counts recorded from the elaborated term; full σ extraction is not claimed.
