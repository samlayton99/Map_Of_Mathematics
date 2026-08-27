# Case History — Everything Learned Since the Phase 3 Handoff

This is the complete narrative from the last results handoff (Phase 3 structural-separability zip, 2026-08-19 morning) to this trial package (same day, evening). Each stage names its finding, the evidence file, and what it killed or established. Reports in `reports/`, data in `data/`, code in `src/`.

## 0. Where the last handoff left off (context)

Phase 3 had established: no-name topology detects machinery moderately well (learned typed track AUC 0.80), but topology-based landmark ranking LOST a blinded review to the exact "route" view (lemmas actually applied in the proof term, 3.9/5 vs 2.7/5); verdict: topology = soft prior + diagnostic only. Known ceiling: local hypotheses, case structure invisible to any declaration ranking. The program owner then proposed a new direction: recursive unfolding depth over the *complete* library, as a machinery filter and resolution dial — which Phase 3's slice-based graph structurally could not compute.

## 1. Depth at full scale (DEPTH_ADDENDUM.md, data/depth_results.json)

Built a full-environment extractor (`mathrecord depdump`): every constant in `import Mathlib` — 771,129 constants, dump in ~96s. depth(n) = 1 + max(depth of proof-term references), primitives 0.

- Depth orders sophistication: Nat.add_comm 11 → Nat.gcd_comm 32 → norm_add_le 95 → Real.exp 140 → Real.exp_log 164 → MeasureTheory.integral_add 243 (max 346).
- The resolution dial works: unclassified theorems at depth ≥50: 170k; ≥100: 67k; ≥150: 40k.
- **Two kinds of machinery discovered**: logical glue is shallow (projections/coercions/eq-machinery median depth 1–3, detectable by shallowness at AUC 0.93–0.96); typeclass instances are DEEP (median 35, AUC 0.56 = invisible to depth). "Machinery is shallow" is half-true.
- Interface phenomenon: `dist_triangle` has depth 2 — in Mathlib the triangle inequality is a structure field; its depth lives in the instances.

## 2. Size, combinations, and early failures (data/measures_results.json, reports/CONES_REPORT.md §1)

- Proof SIZE (fully-unfolded tree size, log scale) is a near-duplicate of depth (per-class AUCs within 0.01; later Spearman 0.992). The owner's "combine depth and size" question is answered: **they are one coordinate**; combinations dead (measured).
- The exact ancestor-SET size is also the same coordinate (Spearman 0.98). Depth ≈ log(volume of prerequisite mathematics). Sharing factor: the unfolded tree is ~10^8× the distinct-fact set.
- **Automation pollution discovered** (data/gateway_hubs.json): the most frequent "deepest ingredient" across all of Mathlib are omega/grind certificate lemmas (instOfNatNat 5958×, omega coordinate_eval 1980× at depth 45) — trivial lemmas proved by tactics LOOK deep.
- **Critical-path navigation fails**: following each theorem's deepest ingredient walks into the ℝ-construction instance tower, not the mathematical story.
- Name/namespace cutting tried (data/depth_mathonly.json): improved one metric but silently severed `_private.*` real mathematics → rejected, and the owner then constitutionally banned name-based and probabilistic filtering.

## 3. Statement cone vs proof cone (CONES_REPORT.md, data/cones_results.json)

For theorem T: A_S = all ancestors of the statement; A_P = all ancestors of the proof; N(T) = A_P \ A_S = mathematics the proof introduced beyond what stating the problem required. Computed exactly for 524 roots by bitmask propagation.

- 19% of proofs have empty N (stay inside the statement's world); median share-new 12%; 35% of theorems add ≤0 depth beyond their statement — the interface layer is a third of the library.
- relDepth (proof depth − statement depth) is a **construction-vs-assertion axis**: definitions 7, instances 9, theorems 2 — the first single coordinate that "sees" instances.
- Ranking a proof's ingredients by (new-to-statement, then depth) recovered 77.5% of the Phase 3 route skeleton vs 70.8% for raw depth — never hurting any of 20 ground-truth proofs.
- Reuse count (in-degree) as importance: **0.0** at move-finding; the most-cited constants are glue.

## 4. Forensics at scale (FORENSICS_REPORT.md, data/forensics_results.json)

The owner demanded: stop looking at averages; map exactly where the ranking breaks. 2,355 random theorems, ranks 1–3 auto-classified, ~50 failures hand-read. Five failure modes: instances 6.7% (largest), neighbor compiler byproducts 4.2%, self-helpers 3.7%, shallow glue ties 1.7%, prover-internal declarations. Rank-1 correctness: 66% shallow / 84% mid / 87% deep. The route "ground truth" itself was found polluted by omega certificates.

## 5. The kernel constitution and first invariant rules (INVARIANT_RANK_REPORT.md)

The owner set the constitution: fixes must approach 100% as the library deepens, survive Lean's evolution, and not be patchwork. Adopted principle: only kernel-calculus facts (statement/body, Prop/Type, citation graph). Two rules tested:
- **Moves must be Props** (instances are constructions): rank-1 79.2%→82.5%, shallow 66%→77%.
- **Inline single-use citations** (private helpers are cited exactly once, by construction): →85.3%, self-helper mode 96→6 blames. 360 theorems correctly reclassified "holds by definition."
- **Negative result, kept**: raw statement-mention counts to detect tactic vocabulary scored AUC 0.40 (tactic libraries state hundreds of internal lemmas); the correct form must be directional seclusion (designed, untested).
- Reading the survivors identified the final gap: Prop-valued instances pass the Prop rule; what distinguishes them is *how the proof uses them* — occurrence position in the term.

## 6. Position-aware extraction — the formulation on trial (MOVES_REPORT.md, lean/DepDump.lean, data/moves_results.json)

Extended the extractor: purely syntactic walk of every proof term; every reference classified load-bearing (applied step / let value / explicit argument) vs background (instance-implicit, implicit, type annotations). Full library in 96s.

- Precision: rank-1 genuine lemma 90.3% overall, 94.6% deep tercile; error now DECREASES with depth. Instance failure mode: 99 → 1 blames.
- Recall vs human source citations (130 random proofs): mean 92.5%, median 100%. Loss forensics: 28/30 misses were self-inflicted by the inlining rule dissolving once-used real lemmas → **container semantics** adopted (open for ranking, keep the label) → ~97–99% by construction.
- Loss accounting vs the previous ranking: 2.2% of theorems lose a top-3 item; examined: predominantly background side-conditions (correct drops).
- Vibe: `Nat.exists_infinite_primes` reads as Euclid's argument verbatim; `Real.exp_add` exposes the via-ℂ strategy; `dist_triangle` correctly reports "interface, no content".

## 7. Residue attack and the gradient (GRADIENT_RELEVANCE_REPORT.md, data/relevance_results.json)

One measure instead of three patches: **subject-matter relevance** — universality of a concept = measured fraction of theorem statements mentioning it (the stop-word principle; the universal list comes out as Eq, Nat, Set, ≤ …); a candidate is *bookkeeping* (no non-universal subject), *relevant* (subject overlaps the statement cone), or *alien* (subject unrelated).

- Zero measured loss (no ground-truth move ever demoted).
- Headline precision unchanged (90.45 vs 90.25) — relevance is a structuring axis, not a booster.
- **Discovery**: alien = *imported* — structurally identical events cover automation residue AND a proof's creative import (Euclid's n!+1 via `dvd_factorial` is tagged alien). Therefore a labeled display group, never a filter.
- Tactic residue splits: data-structure internals caught; omega's Int helper lemmas are ordinary arithmetic that happens to live in a tactic library — no structural measure can (or should) exclude them.
- **Gradient verdict**: recursive relevant-move trees under depth cutoffs give nested, coherent abstraction layers on all six anchors (integral_add: setToFun layer → L1 layer → functional analysis).

## 8. Proof strategies (STRATEGIES_REPORT.md, data/strategies{,2}_results.json)

- v1 (fingerprint constants anywhere in the term): failed — contradiction precision 0.095, induction recall 0.0. Kept as the argument for grain.
- v2 (root shape of the proof term; extractor extended with root head-chains and the kernel isRec flag; recursion-combinator closure instead of name lists): induction, case-split, extensionality work (all anchor recursion proofs correct; ext precision 0.75).
- **Finding**: strategies split into *term-visible* (induction/cases/ext — structural events, recoverable forever) and *intent-level* (by_contra/contrapose/choose/decide — tactic-layer human intent that compiles away; every contradiction false-positive was a term doing classical reasoning whose author never chose contradiction). Intent is not recoverable at kernel grain; if wanted, it must come from the tactic layer as labeled provenance.

## 9. Standing state at trial time

Current pipeline and measured trade-offs are in `briefs/DEFENSE.md` §1–2 and MOVES_REPORT. Admitted gaps: ranking *keyness* (vs genuineness) unproven at scale; shallow floor (83% rank-1, no depth-family fix); yardstick imperfections (auto-labels; source-citation ceiling); single-snapshot validation (no cross-version test yet); universality grain leak for logic constants; mid-proof strategy events invisible to root chains. Queued with designs: directional seclusion, occurrence-prominence strategy grain, cross-version transfer test, spectral pass on a symmetrized statement graph (raw DAG adjacency is provably degenerate).
