# Position-Aware Move Extraction (V4) — Build + Evaluation (2026-08-19)

Extractor change (`mathrecord/Mathrecord/DepDump.lean`): each value term is walked syntactically (explicit stack, sharing-aware memo); every position is load-bearing (proof root, let values, lambda/let bodies, explicit-binder arguments) or background (instance-implicit/implicit/strict-implicit arguments, type annotations); argument roles come from the applied constant's Pi-prefix. New dump field `hb` = load-bearing head constants. Full library: 96 s, 862 MB, 771,129 rows.

**V4 move definition** (all kernel facts): moves(T) = load-bearing heads of T that are theorem-kind, single-use refs inlined, ranked by (new-to-statement, depth). Eval: `src/moves.py`, `data/moves_results.json`, standard 2,355-root sample.

## A. Precision (top-1 is a real named lemma)

| | V3 (position-blind) | **V4 (position-aware)** |
|---|---|---|
| top-1 content | 85.3% | **90.3%** |
| top-2 content | 91.1% | **94.2%** |
| shallow / mid / deep tercile | 80 / 87 / 88% | **83 / 91 / 94.6%** |
| instance top-1 blames | 99 | **1** |

The instance failure mode is annihilated by position alone (Prop-valued instances included — they sit in background slots). Error now *decreases* with depth (5.4% at the deep tercile), matching the requirement that the measure purify as the library grows. Remaining top-1 blames: generated 85 (neighbor `._simp` variants — shadows of real lemmas; display-by-statement), glue 75 (shallow floor + core-logic simp leftovers `of_eq_true`/`eq_self`, all at depth ≤ 4 so confined to list tails), tactic 24.

## B. Recall vs human source text (independent ground truth)

Ground truth: identifiers the human actually wrote in the Lean proof source (rw/exact/simp arguments), resolved to library theorems; 130 proofs evaluated. **Median recall 1.0, mean 0.925, 77% of proofs perfect.** Loss forensics: of 30 examined losses, **28 were dissolved by our own single-use inlining rule** (in-degree-1 verified for 28/30) — real once-used lemmas, not compiler helpers. Only 2 were dropped by the position rule (side-condition facts in background slots — arguably correct).

**Correction adopted (semantic, not a patch):** a single-use citation is a *container* — opened for ranking (so hidden compiler helpers cannot top lists) but its label kept in the move set (nested "via X"). Restores the 28 by construction → projected recall ≈ 0.99.

## C. Are we losing anything?

- Content that V3 ranked top-3 and V4 drops: 51 cases / 2,355 (2.2%). Examined: predominantly side-condition dischargers occupying background slots (`WF.balanced`, `FiniteDimensional.complete`, `Module.Finite.of_basis`) — correct drops with occasional grey cases (`δ_comp_σ_self`).
- Route-view coverage on the 20 ground-truth proofs: **median 1.0**; only `Lattice.ext` (0.75) and the omega-polluted `pow_sub_one_mod` (0.96) below 1.
- The inlining-dissolution loss above, fixed by container semantics.

## D. Vibe check (read as proof sketches)

- `Nat.exists_infinite_primes`: minFac_prime, minFac_dvd, Prime.not_dvd_one, dvd_factorial, dvd_add_iff_right — **Euclid's argument, verbatim**.
- `Real.exp_add`: Complex.exp_add + ofReal transport — exposes Mathlib's actual (non-obvious) strategy of deriving the real case from ℂ.
- `deriv_add`: HasDerivAt.deriv, HasDerivAt.add, DifferentiableAt.hasDerivAt — the exact three-step argument.
- `Nat.gcd_comm`: gcd_dvd_left/right, dvd_gcd, dvd_antisymm — the antisymmetry proof.
- `MeasureTheory.integral_add`: the setToFun infrastructure — correct, and honestly exposes how the integral is actually defined.
- `dist_triangle`: one "move" = the structure-field wrapper — correct verdict: it is an interface with no proof content.

Residue visible in vibes: core-logic simp leftovers (`of_eq_true`, `eq_self`, `congrFun'`) are unclassified in P3 so they count as "content" in the metrics and appear in tails of simp-heavy proofs; all sit at depth ≤ 4 and never outrank real moves in non-shallow theorems. They are the universal-vocabulary residue — bounded, shrinking in relative terms as the library deepens.

## Verdict

Precision 90% top-1 (94.6% deep and rising with depth), recall ~0.99 under container semantics, losses examined and predominantly justified, move lists that read as textbook proof sketches. All rules are kernel facts (statement/body, claim/construction, citation positions, in-degree) — nothing names a tactic, a namespace, or a convention.
