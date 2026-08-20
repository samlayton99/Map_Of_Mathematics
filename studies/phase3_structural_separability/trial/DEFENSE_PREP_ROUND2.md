# Defense Preparation — Second Trial (2026-08-20)

State of the system and complete evidence inventory, prepared before the second adversarial review. Everything below is committed; file references inline.

## The certified system (V6)

Substrate: position-aware occurrence roles (dump v5, adds `gen` flag), exact Prop check, claims = Prop ∧ kind ∉ {constructor, recursor}, single-use as attribute with zoom display, bookkeeping-aware verdicts, and **forwarder attribution**: a machine-generated constant (gen = no source declaration range — recorded environment fact) whose own substantive move-set is exactly one non-bookkeeping claim P is displayed and scored as P. Human-named corollaries are never dissolved (gen=false gates it).

Attribution provenance was verified empirically, not assumed (`/tmp/regprobe*.lean`, results recorded here):
- Lean's matcher registry does NOT recognize `match_1_1` splitters; the simp registry holds ZERO `._simp_N` twins — the registry hypothesis from the first prep was **falsified by probe** and abandoned.
- What holds instead, verified: (a) machine-generated constants have no source declaration range (probe: 5/5 correct separation on twins/matchers/unary vs human lemmas); (b) a twin's own proof term cites its parent at the root (`Finset.mem_product._simp_1` root chain = `[propext, Finset.mem_product]`) — a kernel necessity: derived forms prove themselves from their originals.

## Certification chain (every round registered before running, run once)

| round | seed | result |
|---|---|---|
| dev | 20260819 | development only |
| 1 | 20260820 | V4hist 89.85 replicates; exact variants regress — diagnosis begins |
| 2 | 20260821 | claims-filter correction; V5pz 80.75 |
| 3 | 20260822 | bookkeeping-demotion hypothesis FALSIFIED (+0.09) |
| 4 | 20260824 | breadth-zoom hypothesis FALSIFIED (81.3); case-reading finds denominator artifact |
| 5 | 20260825 | verdict semantics; V5v 91.59; matched-denominator parity with historical |
| 6 | 20260828 | attribution; **V6 94.84** (bar 93); V5v anchor 92.29; matched +2.6 |

Anchor replication count: 8 disjoint samples, spread 89.85–92.29 across formulations' anchors. Seeds 20260819–27 are all burned as development data (including descriptive accounting samples 26/27).

## The 100% failure accounting (owner requirement)

Rank-1 failures fully enumerated and read (`data/phase4_ledger.json`, 160 cases from round 5; glue-in-top-10 partition residual 0 on two samples, `data/glue_accounting.json`). Judged inventory of the 160:

- ~70 machine-named derivations of real lemmas (`X._simp_N`, `X.eq_N`, neighbor `._proof_N`) — real content, machine name. V6 attribution converted the simple-forwarder majority (generated blames 92 → 44 measured).
- ~42 grader mislabels of real moves: interface/structure-field facts (`NatTrans.naturality`, `AddMemClass.add_mem`, ~20), `Classical.byContradiction` (6), Prop-valued instance theorems applied as steps (`Finite.instSigma`, "sigma of finite types is finite" — 8 of the 9 instance cases read as real facts), misc projections (~8).
- ~15 tactic internals (omega `coordinate_eval_*`, grind, abel) — TRUE automation junk (~0.9% of proofs); awaiting the seclusion measure; known, bounded.
- ~12 Prop-eliminators (`Exists.casesOn`, `Nonempty.casesOn`) and thin-list plumbing — owner-ruled fine (trivial proofs where glue IS the proof).
- ~5 own-helpers (zoom handles; 2 remain in V6).

Post-V6 residual (~5.2% of live proofs): ~half grader mislabels of real moves; true junk-at-rank-1 ≈ 2–2.5%, dominated by tactic internals and non-forwarder byproducts. Every case is named; nothing unaccounted.

## Verdict audit (the first trial's sharpest anticipated charge)

449 "holds by definition" verdicts in round 5; 80 sampled and source-checked (`data/phase4_ledger.json` verdict_audit_sample). Of the 39 with verified sources: 30 literal `rfl`, 6 one-line trivial, 3 "substantial-looking" — of which 2 were shortname-resolution collisions (wrong source fetched; verified) and 1 was literally `rfl`. **Zero confirmed false verdicts.** Disclosed weakness: 41/80 could not be source-verified (shortname resolution failure); their candidate lists are uniformly `Eq.symm`/`funext`-style, consistent with ext-lemma one-liners, but unverified is unverified. Fix path: verify via provenance-channel declaration names (exact, no shortnames).

## Open items, declared (do not let the defense overclaim)

1. Cross-version test: still unexecuted (requires extractor build on an older toolchain). Longevity remains a structural argument plus the falsified-and-replaced registry episode as evidence the program tests its own assumptions.
2. Keyness: n=23, one panel, Opus raters (owner-directed), 3/26 briefs excluded for a caught source-collision bug. Strong signal (zoom 4.33/5, 92.8% exact-or-partial), thin base. Human raters and provenance-based brief sources are the scale path.
3. 41 unverified verdicts (above).
4. Tactic-internal pollution ~1% (seclusion measure designed, untested; raw-exposure version already falsified honestly).
5. The grader (diagnosis labeler) is imperfect and used for proxy metrics only; per owner ruling, improving it is explicitly out of scope — keyness panels are the semantic instrument instead.

## Verdict audit v2 (implemented 2026-08-20, closes the disclosed gap as far as tooling allows)

New `mathrecord modules` command resolves any declaration to its true source module from the environment's own records (no name-based search — the collision bug cannot recur). All 80 sampled verdicts re-audited through the provenance channel: 28 positively confirmed, 2 flagged-then-read (statement-side citations, proofs literally `rfl` — audit artifacts, verdicts correct), 14 machine-generated (auto-ext family), 36 human theorems with zero written identifiers (consistent with definitional proofs; not positively certifiable). Combined with audit v1 (39/39 source-verified): **zero false verdicts found by any channel.** See reports/ACCOUNTING_STATUS.md.

## Anticipated prosecution lines and answers

- "Six formulation iterations = garden of forking paths." Every iteration pre-registered, fresh-seeded, run once; two hypotheses were falsified and reported as such; the anchor replicated 8 times. The chain is the opposite of forking: it is falsification with receipts.
- "Attribution is name-matching in disguise." No: gating fact = absence of source range (recorded env metadata); target = the unique substantive claim in the twin's own proof term (kernel). Both probed; registry alternative tested and rejected on evidence.
- "The 94.8 is graded by a name-based labeler." Correct, and it is called a proxy everywhere; the semantic instrument is the blind panel, where rank-1 matched independent raters' key move 93% (exact-or-partial). Also the ledger shows the proxy's residual errors run AGAINST us (real moves counted as failures).
- "Verdicts hide moves." Audited twice: 39/39 source-verified + 28 provenance-confirmed; the 2 flags raised by the second audit were read and are statement-side artifacts; zero false verdicts in any channel; residual = 36 identifier-free proofs, disclosed.
- "n=23 keyness." Acknowledged; scale path stated; the result's direction is corroborated by three independent raters converging on key moves unprompted.
