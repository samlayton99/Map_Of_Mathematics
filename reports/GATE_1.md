# Gate 1 Report — Exactness on an Adversarial Micro-Corpus

Date: 2026-08-18. Decision: **PASS** (all 10 acceptance criteria; 40 automated checks, 0 failures).

## Setup

- Pinned toolchain: `leanprover/lean4:v4.33.0` (`mathrecord/lean-toolchain`), no external deps (`lake-manifest.json` empty). Reproduce: `cd mathrecord && lake build`.
- Corpus: `mathrecord/corpus/Adversarial.lean` (54 resulting declarations incl. auto-generated), `AdversarialRenamed.lean` (alpha-renamed twin), `FailingAction.lean`.
- Extractor/serializer/validator/CLI: `mathrecord/Mathrecord/{Record,Extract,Validate,Main}.lean`, exe `mathrecord`.
- Canonical sample records: `mathrecord/records/*.json`.
- Evidence: `reports/evidence/gate1_validation_output.txt`, `reports/evidence/gate1_inspect_letTactic.txt`.

Commands:

```
mathrecord extract  corpus/Adversarial.lean records/adversarial.json --spike
mathrecord validate corpus/Adversarial.lean records/adversarial.json adversarial
mathrecord validate corpus/FailingAction.lean records/failing.json failing
mathrecord alpha    records/adversarial.json records/adversarial_renamed.json
mathrecord inspect  records/adversarial.json Corpus.letTactic
```

## Corpus coverage (all 15 required constructs)

dependent functions (`depApply`), dependent products (`mkSigma`), local lets in term and tactic mode (`withLet`, `letTactic`), equality/rewriting (`rwDemo`), existential witness (`existsDemo`), recursion (`sumTo`), induction (`sumTo_ge`), structures/projections (`Point`, auto-projections with `Expr.proj` bodies), typeclass synthesis (`HasZero`/`getZero`), coercion (`natToInt`), all four binder kinds (`binders`), universe polymorphism (`constFun.{w,z}`), transparency spectrum (`@[reducible]`/`@[irreducible]`/`opaque`), theorem proof terms (all), branching proof state (`branching` via `constructor` → 2 goals), failing action (`FailingAction.lean` + programmatic `done`), two distinct proofs of one proposition (`twoProofsA`/`twoProofsB`).

## Acceptance criteria → evidence

1. **No silent loss.** `coverage:no-silent-loss`: 54 env declarations = 53 stored + 1 classified unsupported (`hasSorry`). Extraction is total over `Expr`/`Level` constructors by construction (compile-time exhaustive match); anything unencodable throws a classified `EncodeError`.
2. **Completed proofs still check in the pinned environment.** `kernel:stored-defs-theorems-recheck`: 45 defs/theorems re-added to the kernel via `Environment.addDeclCore` using only stored `(levelParams, type, value)` after JSON decode — the kernel, not string comparison, certifies fidelity. Remaining 8 kinds (inductives, ctors, recursors, opaque, unsafe aux) pass `Meta.check` + `isDefEq` (`meta:other-kinds-typecheck`).
3. **Stored targets well-formed in stored contexts.** `states:context-and-target-wellformed`: 13/13 states rebuilt from the record alone (fresh fvars, ordered `LocalContext` incl. let-values and `ldKind`), every hypothesis type, let-value, and target passes `Meta.check`. 0 skipped: no state in this corpus carries residual mvars.
4. **Binders, scopes, local definitions, universes, declaration kinds preserved.** `roundtrip:decode-equals-original`: decode(encode(e)) is `Expr`-equal (binder names, binder infos, let nonDep, universe levels included) to the mdata-stripped original for all 53 declarations. Kind coverage check confirms def/theorem/inductive/constructor/recursor/opaque all present; `constFun` retains 2 universe params.
5. **Dependencies recomputable.** `deps:recomputable-from-stored`: `getUsedConstants` over decoded exprs equals the originals for all 53; type-deps and value-deps kept separate.
6. **Deterministic identity.** Two clean extractor processes produced byte-identical 126KB records (`cmp` clean).
7. **Alpha-renaming invariance.** Renamed twin (every binder, hypothesis, let-name, pattern variable, and universe parameter renamed): all 53 paired declarations and all 13 paired states have identical sids (`alpha:*`). sids are full canonical strings, not hashes, so this is exact structural normalization, not visual similarity.
8. **Unsupported data fails loudly.** `hasSorry` classified with reason `contains sorryAx`; the failed theorem in `FailingAction.lean` is classified unsupported, never stored as a fact (`failing:failed-theorem-not-stored-as-fact`); encode errors (fvar/mvar out of scope) are typed classifications.
9. **End-to-end inspection of one theorem.** `inspect Corpus.letTactic` renders, from the stored record only: declaration metadata, exact structural statement, proof term, type/value references, and a recorded local state showing the auxDecl self-reference, the hypothesis `n : Nat`, and the exact target (`gate1_inspect_letTactic.txt`).
10. **Formal fidelity vs informal meaning** — see Final assessment below.

Transitions (spike, per plan): 32 observed transitions incl. one branching (`constructor`: `[s8] → [s9, s10]`) and closing steps (`after: []`); programmatic spike on a real recorded state: `skip` → success (1 successor), `done` → failure with before-state intact and diagnostic captured. Failure detection handles Lean's error-recovery path (goal admitted via `sorryAx` with logged error), which initially masqueraded as success — see Surprises.

## Failures and surprises (kept, per protocol)

- `Tactic.run` recovers from tactic errors by admitting the goal with `sorryAx` and logging; a naive "no exception = success" spike misclassified `done` as succeeding. Fixed by checking the goal assignment for `sorryAx`. This matters for Gate 2's transition recorder design.
- Tactic-proof local contexts contain the declaration-under-construction as an `auxDecl` hypothesis; state sid initially failed its fixpoint check because rebuilt contexts defaulted `LocalDeclKind`. Now stored (`ldKind`) and rebuilt faithfully.
- `induction ... with | zero | succ` exposes no branching in `goalsAfter` (cases close inside one syntax node) — observed transitions reflect syntax structure, not the logical branch tree. An explicit `constructor` proof supplies the branching case; Gate 2 must normalize this.
- `Corpus.sumTo._unsafe_rec` (equation-compiler artifact) is `safety=unsafe` and correctly refuses kernel re-addition as safe; routed to Meta checking by its stored safety field.

## Stop-condition check

None triggered: identity is deterministic (byte-identical runs); no pretty-print matching anywhere in the fidelity path (display strings exist only in labeled `d`/`actionText`/`diagnostic` fields); unsupported constructs classified loudly; contexts/binders/universes/local definitions round-trip exactly; stored artifacts re-verify through Lean's kernel.

## Final assessment (required questions)

1. **Does the minimal record faithfully represent the tested Lean mathematics?** Yes, for the tested Lean-native record in the pinned v4.33.0 environment: validated by kernel re-checking from stored data, exact round-trips, deterministic serialization, and alpha-invariant structural identity — over an adversarial corpus, not just friendly examples.
2. **What exact information is lost or unstable?** Lost by documented canonicalization: `mdata` payloads, raw `FVarId`/`MVarId` names. Unstable and excluded from identity: display names, `_uniq` numbering. Not yet handled: states with residual mvars (recorded, check-skipped, classified), state-scope universe-param sid uses names, 64-bit fingerprint hashes (labels only). Full list: SCHEMA.md "Known limitations".
3. **What already existed and was reused?** Lean's own `Expr`/`Level`/`ConstantInfo`/`MetavarContext`/`LocalContext`/InfoTree/`Elab.runTactic`/kernel `addDeclCore` are the entire substance — the record is a serialization of them, not a new IR (ADR-0001). No external tool was suitable as the record itself (audit §2), but lean4export's mdata-stripping convention was adopted.
4. **Useful observation layer or needless duplication?** Useful and narrow: no maintained tool serializes exact declarations + exact local states + transitions with environment fingerprints and canonical identity. The layer is ~1.2k lines of Lean and stays honest by construction (kernel re-check from stored bytes). It does not duplicate Lean's internals; it makes them addressable.
5. **Next: dynamic transitions, revise, or stop?** Proceed to dynamic traces (Gate 2) — see `NEXT_RECOMMENDATION.md`.

**Formal fidelity vs informal meaning:** everything validated here is fidelity to Lean's formal objects in one pinned environment. The record demonstrably does not capture informal meaning, motivation, importance, conceptual sameness, or proof-space completeness — e.g. `twoProofsA`/`twoProofsB` are distinct records with a shared statement sid, which says nothing about which proof matters or why; `Nat.add_comm`-style statements carry no semantics beyond their expression structure. Those remain future overlay layers (spec §10), and nothing in this gate licenses claims about them.
