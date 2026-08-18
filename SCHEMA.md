# MathRecord Schema v0.1 (`mathrecord-0.1`)

As implemented and validated at Gate 1. One JSON record per source file per extractor process (ADR-0001). Toolchain-coupled by design: records are only meaningful relative to their environment fingerprint.

## Top level

```json
{
  "schema": "mathrecord-0.1",
  "source": {"file": "...", "contentHash": "hex64"},
  "environment": E,
  "expressions": [X...],
  "declarations": [D...],
  "states": [S...],
  "transitions": [T...],
  "programmaticTransitions": [...],
  "failures": [...],
  "unsupported": [{"name", "reason"}]
}
```

Trust classes (spec §8): every record carries `trust`. `lean-exact` = extracted from Lean objects and re-checkable; `observed` = real event from tooling; `observed-programmatic` = event produced by the extractor driving Lean. Derived data (dependencies, graphs) is never stored — recompute from X.

## E — environment

`environment_id`, `lean_version`, `lean_githash`, `ordered_imports` (deduped), `module_count`, `module_names_hash`, `extractor`, `fingerprint` (hash over all of the above). Records with different fingerprints are never comparable silently.

## X — expressions

Append-only table; id `x<n>` in deterministic DFS-postorder interning order; structurally identical nodes (including display names) are shared. Node kinds mirror Lean 4.33's `Expr` constructors verbatim:

| kind | fields |
|---|---|
| `bvar` | `i` (de Bruijn, Lean-native) |
| `lvar` | `i` — canonical local ordinal (replaces unstable `FVarId`; states only) |
| `mvar` | `i` — first-occurrence ordinal within one state (states only) |
| `sort` | `u` (level) |
| `const` | `n`, `us` (levels) |
| `app` | `f`, `a` |
| `lam` / `pi` | `d` (display name), `bi`, `t`, `b` |
| `let` | `d`, `nd` (nonDep), `t`, `v`, `b` |
| `lit` | `lt` (`nat`\|`str`), `v` (nat as decimal string) |
| `proj` | `s` (struct name), `i`, `b` |

Levels: `zero`, `succ u`, `max u v`, `imax u v`, `param n`, `lmvar i` — Lean's `Level` verbatim.

**Canonicalization (documented, validated):** `mdata` stripped recursively before encoding (elaborator annotations only; kernel-irrelevant; matches lean4export default). Raw `FVarId`/`MVarId` (`_uniq.N`) never serialized. Assigned mvars instantiated against the state's `MetavarContext` before encoding.

**Structural identity (`sid`):** full canonical name-free encoding string (not a hash) — binder display names dropped, universe params replaced by index into the declaration's `levelParams`, lvars/mvars by canonical ordinals. Two exprs are structurally identical iff their sid strings are equal; alpha-renaming of display names provably does not change sid (validated over 53 decls + 13 states).

## D — declarations

`id`, `name`, `kind` (`axiom|def|theorem|opaque|quot|inductive|constructor|recursor`), `levelParams`, `type` (expr id), `typeSid`, `value`/`valueSid` (def/theorem/opaque; theorem values require `allowOpaque := true` at extraction), `module`, `span` (start/end line-col), `reducibility` (5 values in Lean 4.33), `extras` (kind-specific structural fields: hints/safety, inductive numbers+ctors, recursor rules with encoded rhs, quot kind), `trust`.

TypeDeps/ValueDeps are derived (recompute by walking stored exprs); never stored, never conflated.

## S — local states  (Σ;Γ ⊢ ?e : A)

`id`, `decl` (enclosing declaration), `goalUserName`, `ctx` (ordered; each entry: `i`, `d` display name, `bi`, `ldKind` (`default|implDetail|auxDecl`), `t`, optional `v`+`nonDep` for local lets), `target` (expr id), `sid` (state-level canonical string over ctx entry sids + target sid), `src` span, `status`, `hasMVars`, `trust`.

States are deduplicated by sid; a raw goal mvar maps to the state materialized at its first observation. `hasMVars: true` marks states whose exprs contain residual unassigned mvars — these are recorded but excluded from context/target re-checking (classified, not silent).

## T — transitions (spike shape; Gate 2 will normalize)

Observed (from InfoTrees): `id`, `actionKind` (syntax kind), `actionText` (display-only), `src`, `before[]`, `after[]` (state ids; ≥2 = branching, 0 = closing), `outcome`, `trust`, `note`. Nested syntax nodes each produce a transition (documented; not a clean linear trace).

Programmatic (`--spike`): `actionText`, `before`, `afterCount`, `outcome` (`success|failure`), `diagnostic` (display-only). Failure detection covers both thrown exceptions and Lean's recovery path (goal admitted via `sorryAx` + logged error).

`failures`: in-file error events (severity, position, display diagnostic).

## Known limitations (explicit)

- `mdata` payloads dropped (canonicalization; recoverable only by re-elaboration).
- States containing residual mvars are stored but not re-checked (classified via `hasMVars`).
- State-scope universe params keep names in sid (declaration-scope uses indices); corpus states are universe-monomorphic so this is untested surface.
- `hex64` fingerprints use Lean's 64-bit string hash — fine for provenance labels; identity claims rest on full canonical strings only. Swap for SHA-256 before any scaled corpus.
- Exotic name atoms (needing `«»`) round-trip via `toString`/`toName` untested.
- One source file per extractor process (double `importModules` corrupts the parser token table).
