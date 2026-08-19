# Reproduction Report — Gates 0–1 baseline before Phase 2

Date: 2026-08-18. Result: **fully reproduced, zero discrepancies.**

- Toolchain: `leanprover/lean4:v4.33.0` per `mathrecord/lean-toolchain`; `lake build` clean (17 jobs).
- Re-extraction of all three corpus files produced **byte-identical** outputs to the committed canonical records (`cmp` clean for `adversarial.json`, `adversarial_renamed.json`, `failing.json`) — reproduction and determinism confirmed in one step.
- `validate corpus/Adversarial.lean … adversarial`: 14/14 PASS, exit 0.
- `validate corpus/FailingAction.lean … failing`: all PASS.
- `alpha`: 53/53 declaration sids and 13/13 state sids invariant under renaming.

Note: this session runs on the same machine and elan installation as the original Gates 0–1 run; this is a same-environment reproduction, not a cross-machine one.

Baseline is intact. Phase 2A/2B feature work proceeds on top of it without modifying Gate 0–1 evidence (`reports/GATE_0.md`, `reports/GATE_1.md` unchanged).
