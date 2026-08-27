# Move-Ranking Forensics (2026-08-19)

Question (Sam): does the ranking put the most mathematically useful ideas on top *every time*? If ranks 1–2 are glue and rank 3 is the real move, the ranking is broken.

Method: ranking under test = a theorem's direct proof references ordered by (new-to-statement, then global depth). Stage A: 2,355 random unclassified theorems (seed 20260819), ranks 1–3 auto-classified as content / instance / self-helper / generated / glue / tactic (`src/forensics.py`, `data/forensics_results.json`; categories used for diagnosis only, never inside the ranking). Stage B: manual reading of ~50 broken exemplars plus all 20 ground-truth proofs (`review/ui/review_data.json`).

## Headline rates (2,355 theorems)

| variant | top-1 is content | top-2 contains content | broken (content exists, ranks 1–2 both junk) |
|---|---|---|---|
| depth only | 77.1% | 88.4% | 8.2% |
| new-then-depth | 79.2% | 88.3% | 8.3% |
| + self-helpers unfolded one level | 82.2% | 90.4% | 6.6% |

By depth tercile (new-then-depth, top-1 content): shallow (depth 2–33) **66.1%**, mid (34–80) **84.5%**, deep (81–323) **87.1%**. The ranking is good where the library is deep and degrades toward the axioms. Manual read of the 20 ground-truth proofs matches: all 8 with depth ≥ 34 had correct or near-perfect top lists; the failures concentrate below depth ~15.

## The five failure modes (with top-1 blame counts / 2,355)

**1. Instance towers — 158 (6.7%), the largest.** Example: `Matrix.isHermitian_add_transpose_self` ranks `Matrix.instStarAddMonoid` and `Matrix.addCommMonoid` above the actual move `IsSelfAdjoint.add_star_self`; `cfc_re_id`'s entire top-5 is the ℂ-is-a-C*-algebra instance stack. Why the score cannot see this: instances are deep (constructions, median relDepth 9), and they are genuinely "new" (a statement uses notation; the specific instances materialize only in the elaborated proof). Both ranking criteria pass. The category error: an instance is *how the statement's notation gets its meaning*, not a step of the argument. Caveat found in the exemplars: rarely the instances ARE the argument (`preservesFiniteCoproducts_of_reflects_of_preserves` works by instance resolution) — so instances should be displayed as a separate "setting" group, not deleted.

**2. Neighbor compiler byproducts — 100 (4.2%).** Auto-derived variants of real lemmas (`slope.eq_1` = slope's defining equation; `WithTop.coe_covBy_coe._simp_2` = a simp-normal form of a real lemma) outrank the real thing while *being* the real thing in disguise. Fix is attribution: each byproduct names its parent structurally; credit the parent.

**3. Self-helpers — 86 (3.7%), solved.** The theorem's own `._unary`/`._simp_1_1`/`._f` helper carries the whole proof (`PowerSeries.order_eq`, `List.Perm.eq_of_pairwise`, and `Nat.pow_sub_one_gcd_pow_sub_one` in the 20). Unfolding one level removes 82 of 86 (86→4) and is a pure graph operation.

**4. Shallow-region glue ties — 41 (1.7% overall, concentrated in the shallow tercile).** Two distinct subspecies. (a) *Definitional theorems*: the proof is literally `rfl` — `Part.mul_def`, `Language.one_def`, `LieSubmodule.mem_carrier`. There are no moves; "no content found" is the *correct* answer and the display should say "holds by definition." (b) *Genuine ties*: `AddUnits.add_neg_cancel_right` ranks `Eq.mpr`(d4), `congrArg`(d3) above the real moves `add_neg`/`add_assoc`(d2–3); ditto `Function.Bijective.existsUnique_iff` in the 20 (glue at 1–3, real moves at 4–5). Root cause: at the bottom of the library everything — glue and content alike — sits within a few levels of the axioms, so a max-over-chain measure has no resolution left. **This is the one mode with no known fix inside the depth family**; it needs an orthogonal signal (candidate's topical overlap with the statement, or use-side evidence).

**5. Prover-internal theorems — ~30 sampled rows + 10 top-1 blames.** The sample includes Lean's own tactic support library (`Lean.Grind.*`, `Lean.Order.*`); content-rate there is 6.7% because those declarations aren't mathematics at all. Separately, tactic *certificates* pollute real proofs (`Nat.pow_sub_one_mod_pow_sub_one` ranks 2–5 are omega internals) — and pollute the ground truth too: the P4-route answer key for that proof contains 20 omega lemmas. Any evaluation against route overstates tactic-internal "content."

## The cohesive picture

Depth = mathematical importance holds **except where something non-mathematical is deep**, and the deep non-mathematics comes in exactly three families — instances (deep by construction), compiler byproducts (inherit their parent's depth), tactic machinery (deep code) — plus one region where depth is too coarse (the shallow floor, where it has no dynamic range). None of these are noise: all five modes are *categories of declaration whose depth does not mean what depth means for theorems*. All three deep families are detectable from deterministic environment facts already in the dump (instance flag, generated/internal flags, byproduct-parent structure) — no name heuristics, no learned classifier.

Projected ceiling from stacking the deterministic fixes (helper unfolding measured, others estimated from blame counts): top-1 content ≈ 92–95%, with the shallow floor as the honest residue.

## Recommended next step

One re-run: (1) unfold self-helpers (measured win), (2) attribute neighbor byproducts to their parents, (3) group instances/generated into a labeled "setting" section below the moves instead of interleaving, (4) mark `rfl`-proof theorems "holds by definition". Then re-measure the same three headline rates on the same 2,355 sample — target is top-1 content ≥ 90% overall and the shallow tercile pulled above 80%. The shallow-floor residue gets its own experiment afterward (statement-overlap relevance signal).
