# ADR-0001: Wrap Lean's own objects; do not invent an intermediate representation

Date: 2026-08-18. Status: accepted (Gate 0).

## Decision

MathRecord's X is a verbatim serialization of Lean 4.33.0's `Expr` (12 constructors) and `Level` (6 constructors). D wraps `ConstantInfo`, S wraps `MetavarDecl`+`LocalContext` from InfoTree `TacticInfo` nodes, E wraps the environment header, T (spike) wraps InfoTree tactic steps / `Elab.runTactic` results. Extraction runs in-process against the pinned toolchain, one source file per process.

The only custom machinery is: canonical JSON serialization, structural identity hashing after documented canonicalization (renumber `FVarId`/`MVarId`, drop display names and `mdata` from the hash), environment fingerprinting, and trust-class provenance labels.

## Why

- Gate 0 spike (`mathrecord/`, exe `gate0`) verified every required field is accessible as structured objects — no display parsing anywhere.
- No maintained external tool provides the whole record: lean4export lacks S/T/spans; REPL and InfoTree training-data tools serialize goals as pretty-printed strings; Pantograph is an interaction protocol pinned ~2 versions behind with no canonical identity or environment fingerprinting (see `LEAN_REPRESENTATION_AUDIT.md`).
- A new IR would duplicate Lean internals and violate the handoff's reuse rule; a thin serializer cannot drift from the verifier because the verifier's objects are the schema.

## Consequences

- Schema is version-coupled to the pinned toolchain by design; environment fingerprint makes that explicit rather than hidden.
- Extractor is a Lean program (not Python), so records stay connected to kernel re-checking (`Environment.addDeclCore`) in the same process.
- Per-file process isolation is a hard rule until the double-`importModules` parser corruption is understood upstream.
