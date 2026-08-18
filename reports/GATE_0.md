# Gate 0 Report — Tool and Representation Audit

Date: 2026-08-18. Decision: **PASS**.

## Setup

- Toolchain: `leanprover/lean4:v4.33.0` (stable, 2026-08-10, githash `d8b18978322de05a8f3dba51ef03cf5461676c17`), pinned in `mathrecord/lean-toolchain`, installed via elan 4.2.3.
- Spike: `mathrecord/` lake package, exe `gate0` (`Mathrecord/Frontend.lean`, `Mathrecord/Gate0.lean`), corpus `mathrecord/spikes/{SampleProofs,FailingProof}.lean` (3 proofs + 1 failing proof).
- Commands: `lake build && ./.lake/build/bin/gate0 spikes` and `./.lake/build/bin/gate0 spikes --only-fail`.
- Evidence: `reports/evidence/gate0_spike_output.txt`, `reports/evidence/gate0_failing_file_output.txt`.
- Ecosystem survey: `sources/ecosystem_audit_2026-08-18.md` (live-verified). Audit: `LEAN_REPRESENTATION_AUDIT.md`. ADR: `decisions/ADR-0001-wrap-lean-not-new-ir.md`.

## Acceptance criteria

1. **Exact declarations, expression structure, local contexts, and targets accessible without scraping pretty-printed text** — PASS. All dumps in the evidence files are constructor-level walks of `Expr`/`Level`/`LocalDecl`/`MetavarDecl` objects (e.g. `(forallE n def (const Nat []) …)`, `ldecl` with let-value, mvar targets). The pretty printer is never invoked for formal content.
2. **Completed terms/proofs connect to Lean checking** — PASS. `Environment.addDeclCore` (the kernel) re-checked the stored `(levelParams, type, value)` of `Gate0Spike.double_eq_two_mul` under a fresh name; a negative control with a swapped type was rejected by the kernel.
3. **The custom layer that is genuinely missing is explained** — PASS. Canonical serialization + stable identity + environment-fingerprinted provenance; nothing else (audit §5, ADR-0001).
4. **Plausible path to stable serialization and canonical identity** — PASS. `Expr` uses de Bruijn indices natively; the unstable parts are enumerated (`_uniq` fvar/mvar names, display names, `mdata`) with documented canonicalization planned (audit §4, §6).

## Deliverables

- Extraction spike on 3 small proofs (def + 2 tactic theorems + 1 term-mode theorem): done, evidence file sections A–F.
- One captured local proof state: done — state before `refine ⟨m, ?_⟩` in `exists_gt`, including a `cdecl`, an `ldecl` with its value, and the exact target (section G).
- Transition-access spike, no full trace dataset: done — (H1) 48 `TacticInfo` nodes with before/after goal mvars from InfoTrees; (H2) programmatic `Elab.runTactic`: `decide` closes a constructed goal, an ill-typed `exact` fails with a catchable exception and intact before-state; (H3) a failing file still yields 33 recorded tactic steps plus the exact error span.
- Field-by-field source/gap matrix: audit §3.
- `LEAN_REPRESENTATION_AUDIT.md`: written.
- ADR: `decisions/ADR-0001-wrap-lean-not-new-ir.md`.
- Reduced v0.1 schema: audit §6 (drops `lean_revision`, `mathlib_revision`, general `relevant_options`; defers full T).
- Unavailable/unstable/redundant field list: audit §4.

## Failures and surprises (kept, per protocol)

- `ConstantInfo.value?` silently returns `none` for theorems unless `allowOpaque := true` — first kernel-recheck attempt reported "no value".
- Processing a second file in one process corrupts the parser token table (spurious `unexpected token '+'`). Resolved by one-file-per-process; recorded as a hard extractor constraint.
- First "failing action" spike accidentally elaborated successfully (coercion swallowed it); replaced with an unambiguous type mismatch.
- `env.header.imports` lists `Init` twice; dedupe before fingerprinting.

## Stop-condition check

No stop condition triggered: exact states are reliable; no display parsing is needed; no existing maintained tool supplies the complete record (closest are Pantograph — interaction-oriented, version-lagged — and lean4export — declarations only); the layer adds serialization/identity/provenance rather than duplicating Lean internals.

**Proceed to Gate 1.**
