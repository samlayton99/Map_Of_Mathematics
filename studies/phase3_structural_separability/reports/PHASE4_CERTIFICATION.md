# Phase 4 — Exact Move Substrate Certification (2026-08-19)

Executed per the external judge's ruling (accept-with-conditions). Constitution amended first: ADR-0004 (epistemic layers). All metrics below are named `top1_nonmachinery_proxy` — agreement with an automated machinery-labeling proxy, not semantic precision. Development data (the seed-20260819 sample) is never quoted as validation below.

## 1. The substrate, implemented exactly

`mathrecord depdump` v3 (`lean/DepDump.lean`), full library (771,129 constants, 98 s, 1.3 GB):

- **True Prop check** (`Meta.isProp`, kernel) replaces the `kind == theorem` proxy. Zero check fallbacks. Measured proxy error: **20,113 constants** where kind and Prop-ness disagree.
- **Exact binder roles** via `forallBoundedTelescope` (definitional unfolding included), cached; unresolved roles instrumented: 57,741 rows carry at least one unresolved-role event (363,372 events total, counted in role 7 and kept load-bearing — conservative).
- **Occurrence roles preserved**: per reference, an 8-vector of occurrence counts by role (applied / let-value / explicit / implicit / instance / strict-implicit / type-annotation / unresolved), DAG multiplicity. The full positional stream (paths, argument indices) remains available through the per-file extractor.
- **Single-use is an attribute**, not a container: no inlining in the substrate; zoom expansion is display semantics (fixpoint, cycle-safe).
- Per-constant heartbeat budgets (a cumulative-budget overflow killed run 1 at 50k constants — fixed with `withCurrHeartbeats`, failures caught and counted).

## 2. Pre-registered holdout results (run once each)

Round 1 (seed 20260820, disjoint from dev; variants fixed in advance):

| variant | top-1 proxy | shallow/mid/deep | note |
|---|---|---|---|
| V4hist (historical) | **89.85%** | 83/91/93 | replicates dev's 90.25% — **no overfitting** (judge charge 10 answered) |
| V4b (exact Prop, else historical) | 73.3% | — | exact check ADMITS Prop-valued ctors/recursors the kind proxy hid |
| V5 (occurrence roles, no inlining) | 70.4% | — | single-use kept → self-helpers resurface (18% of rank-1s) |

Diagnosis on round 1 (post-hoc, so round 1 became development data too): the historical kind proxy was silently encoding "Prop-valued AND not constructor/recursor" — intro/elim rules of Prop inductives (`Iff.intro`, `List.Mem.rec`) are Prop-valued, usually new-to-statement, and topped lists. Constructor/recursor are kernel kinds, so the exact claims filter is `pr ∧ kind ∉ {constructor, recursor}`.

Round 2 (seed 20260821, disjoint from both prior samples; registered before running):

| variant | top-1 proxy | shallow/mid/deep | single-use at rank 1 |
|---|---|---|---|
| V4hist | **90.13%** | 85/90/95 | 0.1% |
| V5p (exact claims filter) | 76.7% | 66/77/86 | 19.9% |
| V5pz (V5p + zoom display semantics) | **80.75%** | 70/83/89 | 0 (opened) |

Replication: V4hist = 90.25 (dev) / 89.85 (holdout 1) / 90.13 (holdout 2). That number is real.

Rounds 3–5 (seeds 20260822/24/25, each disjoint from all prior samples, each registered before running, each run once):

- **Round 3** — hypothesis: bookkeeping demotion (measured universality) closes the gap. **Falsified**: 83.24 → 83.33 (+0.09; bar was 88). V4hist replicated a 4th time (90.93).
- **Round 4** — hypothesis: breadth zoom (expand every single-use candidate, not just rank-1 chains) closes it. **Falsified**: 81.3. V4hist replicated a 5th time (90.89). Lesson recorded: two mechanism guesses in a row failed because they were theorized instead of read from cases.
- Post-hoc case reading (400 roots): the "failures" are proofs whose ENTIRE candidate list is `rfl`/`Iff.rfl` — true-by-definition lemmas. The historical variant excludes `rfl` by kind, gets an empty list, and exits those proofs from the denominator as "definitional"; the exact substrate keeps `rfl` visible and is scored a failure *for reporting the correct fact as a candidate*. The gap was substantially a **denominator accounting artifact**.
- **Round 5** — verdict semantics fixed kernel-honestly (all-bookkeeping candidate list ⇒ holds-by-definition verdict, like empty), plus a matched-denominator comparison. **Certified**: V5v = **91.59%** (bar 88), glue blames 282 → 45 (below V4hist's 72), no-content 2.6%, shallow/deep 86/95.7. Matched denominator (1,899 proofs live in both): V4hist 91.63 vs **V5v 91.79**. V4hist replicated a 6th time (90.38).

**Certification conclusion**: the exact, kernel-honest substrate — occurrence roles, true Prop check, claims = Prop ∧ not constructor/recursor, single-use as attribute with zoom display, bookkeeping-aware verdicts — now matches the historical accidental system on identical proofs, with every component principled and every previously-mysterious gap explained by a named fact. Six replications of the anchor across disjoint samples close the overfitting charge; the substrate formulation (V5v) is the standing definition going forward.

## 3. Elaboration-provenance sidecar (built)

`mathrecord provenance <file> <out>`: per declaration, the global constants the source referenced *as resolved by the elaborator* (InfoTree TermInfo idents) plus tactic kinds — a separate channel, never mixed into the kernel record (ADR-0004 level 3). Smoke test: for `Real.le_exp_of_log_le` it returns exactly the human-written citations.

Extraction-independent recall (ground truth never passes through our extraction — the measurement the old benchmark structurally could not make):

40 files elaborated, 4,522 declarations with provenance; 29 holdout theorems qualified (≥2 Prop-valued elaborator-resolved citations — a small n, expandable by elaborating more files). Results:

- median recall **1.0**, mean **0.859**, 72.4% of proofs perfect;
- loss taxonomy: **not-in-term 15, background-slot 0, not-prop-flag 0**.

The taxonomy is the architectural verdict: **every single loss is a citation that never reached the kernel proof term** (erased during elaboration — simp closures, definitional rewrites; e.g. `tsub_le_iff_right` written in source, absent from the compiled term). The position filter and the claims filter lost *nothing* the human wrote. About 14% of human citations are elaboration-erased and therefore recoverable only through the provenance channel — measured justification for the two-channel architecture, and the number the old benchmark structurally could not see.

## 4. Judged interpretation

1. The **position signal survives certification**: V4hist's replication across three disjoint samples, with instance blames at 1–5 per 2,400, confirms the mechanism (the judge's 99% claim) on held-out data.
2. The **exact substrate is more faithful and currently scores lower on the proxy** — because the proxy rewards the historical variant's accidental filters. Both facts are now measured instead of conflated. The certified path forward: substrate = V5p (exact, occurrence-level, attribute-based); display = zoom semantics; the `rfl`/`propext`/bookkeeping residue goes to the next registered round.
3. **Single-use containers**: the judge's correction is implemented and vindicated — zoom semantics recovers most of the inlining benefit (70.4 → 80.75) without destroying abstraction boundaries or labels.
4. Still open, unchanged: keyness (deliberately untouched, per ruling), cross-version testing (needs an older-toolchain extractor build; next), the shallow floor.
