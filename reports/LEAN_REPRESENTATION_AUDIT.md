# Lean Representation Audit (Gate 0)

Date: 2026-08-18. Toolchain: `leanprover/lean4:v4.33.0` (latest stable, released 2026-08-10, githash `d8b18978322de05a8f3dba51ef03cf5461676c17`). Spike code: `mathrecord/` (exe `gate0`).

## 1. Verdict

Everything the record needs is available **exactly** (as structured Lean objects, never parsed from display text) through Lean's own in-process metaprogramming API. No maintained external tool supplies the complete record (E,X,D,S,T); the genuinely missing layer is small: canonical serialization, stable identity, and environment-fingerprinted provenance over objects Lean already owns.

## 2. Ecosystem survey (verified against live repos, 2026-08-18)

| Tool | Maintained | Gives | Misses for MathRecord |
|---|---|---|---|
| Lean 4 core API (`Lean.Environment`, `Expr`, `InfoTree`, `Elab.runTactic`, kernel `addDeclCore`) | v4.33.0 stable | Everything below, in-process, structured | Serialization, stable IDs, provenance — the custom layer |
| lean4export (leanprover) | yes (tracks 4.34-rc) | Kernel decls + exprs as NDJSON | No source spans, no local states, no transitions |
| repl (leanprover-community) | yes (tracks 4.34-rc) | Tactic stepping, pickling | Goals are **pretty-printed strings**, not terms |
| Pantograph / PyPantograph | yes (pinned v4.31.0) | Structured goals, per-expr s-exps, save/load, failure messages | Interaction protocol, not a canonical record; no env fingerprinting/identity; lags Lean by ~2 versions |
| LeanDojo v1 | **deprecated** (Jan 2026) | — | — |
| LeanDojo-v2 | yes | Tracing + training stack over Pantograph | Heavy framework; states inherit Pantograph shape; not a minimal record |
| kim-em/lean-training-data | stale (pin v4.16.0) | InfoTree JSON export | Goals pretty-printed; stale |
| cmu-l3/ntp-toolkit | semi (pin v4.24.0) | state/tactic JSONL | States pretty-printed |
| LeanTree, LeanExplore, LeanSerde | new/niche | proof-tree factorization / search / serde lib | None is a fingerprinted exact record of E,X,D,S,T |

Full sourced table in `sources/ecosystem_audit_2026-08-18.md`.

## 3. Field-by-field source/gap matrix

Access path verified by running `gate0` unless noted. "Exact" = structured Lean objects, no display parsing.

| Record field | Source | Exact? | Spike evidence |
|---|---|---|---|
| E: lean version/revision | `Lean.versionString`, `Lean.githash` | yes | section A |
| E: imports, module list | `env.header.imports`, `env.header.moduleNames` | yes | section A (631 modules) |
| E: options | `Command.State.scopes` / elaborator options | yes | available; not yet recorded |
| E: fingerprint | derived (hash of the above + extractor version) | derived | to build (Gate 1) |
| X: expression structure | `Lean.Expr` — 12 ctors: bvar fvar mvar sort const app lam forallE letE lit mdata proj | yes | B–F dumps |
| X: universe levels | `Lean.Level` — zero succ max imax param mvar | yes | `Eq [(succ 0)]` in dumps |
| X: binder info | `BinderInfo` on lam/forallE + `LocalDecl` | yes | G dump |
| D: name, kind, levelParams | `ConstantInfo` (8 kinds: axiom def thm opaque quot induct ctor rec) | yes | B–F |
| D: type expr | `ConstantInfo.type` | yes | B–F |
| D: value/proof expr | `ConstantInfo.value? (allowOpaque := true)` — **theorems return `none` without the flag** | yes | B–F |
| D: module of origin | `env.getModuleIdxFor?` + `moduleNames` | yes | B–F |
| D: source span | `findDeclarationRanges?` | yes | `⟨8,0⟩–⟨11,18⟩` |
| D: transparency | `getReducibilityStatusCore`; unfolding via `Meta.unfoldDefinition?` | yes | B–F |
| D: TypeDeps/ValueDeps | `Expr.getUsedConstants` on type/value separately | yes | B–F |
| S: ordered local context | `TacticInfo.mctxBefore/.mctxAfter` → `MetavarDecl.lctx` → `LocalDecl` (cdecl/ldecl with index, fvarId, userName, binderInfo, type, let-value, implementation-detail flag) | yes | G dump incl. `ldecl` with value |
| S: target | `MetavarDecl.type` (an `Expr`) | yes | G dump |
| S: metavariable ids | `MVarId` | yes but **unstable** (`_uniq.N`) | G/H1 |
| S: source location | `TacticInfo.stx` ranges + `ContextInfo` file map | yes | available |
| T: observed steps | InfoTree `TacticInfo` (goalsBefore/goalsAfter + mctx pairs + tactic syntax) | yes | H1: 48 nodes/file |
| T: programmatic step | `Elab.runTactic mvarId stx : MetaM (List MVarId × State)` | yes | H2 success (`decide` closes goal) |
| T: failing action | `runTactic` throws catchable exception, before-state intact; in-file failures leave error message + all prior `TacticInfo` (33 nodes in failing spike file) | yes (diagnostic text is display-only, labeled) | H2, H3 |
| Verification link | `Environment.addDeclCore` (kernel) re-checks stored (levelParams, type, value) | yes | I: recheck OK; kernel rejected mistyped negative control |

## 4. Unavailable, unstable, or redundant fields

**Unstable (must be canonicalized, never used as identity):**
- `FVarId`/`MVarId`/`LMVarId` names (`_uniq.N`) — process-run-dependent. Canonicalize by position (context order / first-occurrence).
- Binder display names (`n`, `h`) — alpha-irrelevant; keep as display metadata, exclude from structural identity.
- `Expr.mdata` — elaborator annotations, not semantic content; record but exclude from identity by default.
- MessageData diagnostics — display text; store only as labeled `diagnostic`, never as formal source.

**Constraints discovered:**
- One source file per frontend process: a second `importModules` in the same process corrupts the parser token table (spurious `unexpected token '+'` errors). Extractor must run per-file (verified: same file processes cleanly when first).
- `ConstantInfo.value?` defaults to hiding theorem/opaque bodies; must pass `allowOpaque := true`.
- `env.header.imports` can duplicate `Init`; deduplicate before fingerprinting.

**Dropped/deferred from the provisional spec (not justified by audit):**
- `lean_revision` separate from `lean_version` — githash suffices.
- `mathlib_revision` — no Mathlib in Gates 0–1; field stays optional/absent.
- `relevant_options` — record only options explicitly set (none in spike).
- Full `T` schema (trace ids, timing, multi-successor bookkeeping) — deferred to Gate 2; spike shape only.

## 5. What the custom layer genuinely adds

1. Canonical, deterministic serialization of `Expr`/`Level`/`LocalContext`/`ConstantInfo` (Lean has no stable public serialization of these besides .olean, which is version-opaque).
2. Stable identity: structural hashing after documented canonicalization (bvar de Bruijn indices are native; fvar/mvar renumbering and name-stripping are ours) + environment fingerprint.
3. Provenance: every record tied to an environment fingerprint and trust class.
4. Cross-linking E–X–D–S–T in one queryable record.

Nothing else. The layer wraps Lean objects; it does not re-model them.

## 6. Reduced v0.1 schema (justified fields only)

- **E**: `environment_id`, `lean_version`, `lean_githash`, `ordered_imports` (deduped), `module_names_hash`, `extractor_version`, `fingerprint`.
- **X**: table `expr_id -> node` mirroring the 12 `Expr` ctors verbatim (with `Level` sub-table or inline); `expr_id` = canonical structural hash. Display names kept in a parallel `display` field outside the hash.
- **D**: `declaration_id`, `name`, `kind` (8 values), `level_params`, `type_expr`, `value_expr?`, `module`, `source_span?`, `reducibility`, `env`. TypeDeps/ValueDeps derived, not stored.
- **S**: `state_id`, `env`, `context` = ordered list of `{index, canonical_fvar, user_name(display), binder_info, type_expr, value_expr?, impl_detail}`, `target_expr`, `mvar(canonical)`, `source?`, `status`.
- **T (spike only)**: `{before_state, action_syntax_kind, action_text(display), after_states[], outcome, diagnostic(display)?}`.

Trust classes as in spec §8; everything above is class 1 (Lean-exact) except `T.outcome`/observed steps (class 2) and derived deps (class 3).
