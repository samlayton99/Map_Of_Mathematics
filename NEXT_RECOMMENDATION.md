# Next Recommendation

**Proceed to dynamic traces (Gate 2).**

One recommendation, per protocol. Not "revise the object": every Gate 1 acceptance criterion passed without weakening, and the revisions listed below are additive hardening inside the same object, not changes to its shape. Not "abandon/wrap": the live audit (2026-08-18) found no maintained tool that provides exact serialized declarations + exact local states + transitions under one fingerprinted identity — the closest (Pantograph: interaction protocol, v4.31-pinned; lean4export: kernel declarations only; REPL/ntp-toolkit: pretty-printed states) each miss a load-bearing part, and the validated layer is small enough (~1.2k lines over Lean's own objects) that wrapping would cost more than it saves.

## Evidence base

- E, X, D, S validated on an adversarial corpus: kernel re-check from stored bytes (45 decls), exact round-trips (53), rebuilt-context well-formedness (13 states), byte-identical determinism, alpha-invariant identity (53 decls + 13 states). `reports/GATE_1.md`.
- Transition access proven three ways: InfoTree observation (32 transitions incl. branching `[s8]→[s9,s10]` and closing steps), programmatic execution on a recorded state (`skip` success / `done` failure with diagnostic), and in-file failure capture with prior states intact.

## Gate 2 entry conditions (fold in before or during)

1. Normalize T: derive the logical branch tree from nested syntax observations (the `induction ... with` case shows syntax nesting ≠ branch structure); one canonical transition per logical step, nesting kept as provenance.
2. Failure semantics: a transition recorder must treat Lean's error-recovery path (`sorryAx`-admitted goal + logged error) as failure — already demonstrated in the spike; make it the recorder's invariant.
3. Represent mvar-carrying states fully (per-state mvar declaration table) so no state is check-skipped.
4. Replace 64-bit fingerprint hashes with SHA-256 before any corpus larger than toys.
5. Keep one-file-per-process isolation until the double-`importModules` parser corruption is resolved upstream.

## Risk to carry forward

Gate 1 establishes faithfulness only. It says nothing about usefulness (Gate 4) or learning value (Gate 5); do not let the clean pass inflate claims beyond "the tested Lean-native record is exact for the pinned environment".
