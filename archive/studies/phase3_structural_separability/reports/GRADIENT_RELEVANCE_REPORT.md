# Subject-Matter Relevance + Abstraction Gradient (2026-08-19)

Goal (Sam): attack the V4 residue without patchwork, and check the *gradient* — do depth cutoffs reveal sensible abstraction layers? Code `src/relevance.py`, data `data/relevance_results.json`.

## The one-axis design

One new measure instead of three patches. **Universality** u(k) = fraction of theorem statements directly mentioning concept k (measured stop-words; θ = 2% ⇒ 149 universal concepts: Eq, OfNat, Nat, Membership, DFunLike, Set, LE, Category… — sensible, and stable under θ ∈ {1%, 5%}). **Subject** of a candidate = the non-universal concepts in its own statement. Verdict against the theorem's statement cone A_S(T):

- **bookkeeping** — no non-universal subject at all (pure logic vocabulary);
- **relevant** — some subject concept lies in A_S(T);
- **alien** — has subject, none of it in A_S(T).

All kernel facts (direct type refs + measured frequency + cone membership).

## Results — honest reading

1. **Zero loss**: no ground-truth route item across the 20 reviewed proofs is ever tagged alien or bookkeeping (`route_items_demoted = 0`).
2. **Headline unmoved**: V5 (relevant > alien > bookkeeping regrouping) scores 90.45% top-1 vs V4's 90.25% — relevance is a *structuring* axis, not a precision booster. Partly a measurement artifact: 1,694 "content"-labeled candidates land in bookkeeping, and reading them shows they are `of_eq_true`/`eq_self`-style logic that the P3 labels miscount as content, so correct demotions score as losses.
3. **Tactic residue splits in two**. Data-structure internals (`LinearCombo` lemmas: 198 items) are caught as alien. But 1,096 tactic-library items land *relevant* — and inspection shows why: omega's `Int` helper lemmas are *ordinary arithmetic facts* that happen to live in a tactic library. Kernel-invariantly they ARE mathematics; no honest structural measure will exclude them, and that is the correct verdict, not a failure.
4. **Known leak, bounded**: logic constants like `True` have low *direct-mention* universality but sit in every statement *cone*, so `of_eq_true` occasionally sneaks into "relevant" at list tails (never displacing real moves). The universality grain (direct mention vs cone presence) is the open design question.

## The discovery: alien = imported, and imports are sometimes the point

In `Nat.exists_infinite_primes`, the verdict tags `Nat.dvd_factorial` alien — factorial is not in the statement's world. But *considering n!+1 is Euclid's creative move.* The alien tag cannot distinguish machinery pollution from a proof's creative import, because structurally they are the same event: the proof reaches outside the problem's vocabulary. Consequence: **alien is a display dimension ("imported"), never a filter.** A proof view should show: moves within the problem's world, then imports labeled as such — where an import is either automation residue or the idea worth reading the proof for. This upgrades, rather than repairs, the map design.

## The gradient — layers are real

Recursive relevant-move trees, two levels, with depth-cutoff slices (all six anchors coherent):

- `MeasureTheory.integral_add` (d 243): cutoff 194 → the integral/setToFun layer (6 items: integral_def, setToFun_add/eq…); cutoff 121 adds the L1/Integrable layer; cutoff 60 adds functional analysis (`ContinuousLinearMap.map_add`). Reads as: *the Bochner integral is setToFun of weightedSMul; setToFun is additive for dominated additive set functions; weightedSMul is one.*
- `Real.exp_add` (d 144): cutoff 115 → the complex-exponential layer; cutoff 72 adds the ofReal transport and the series layer (`add_pow`, `Finset.sum_range_sub_sum_range` — the binomial/Cauchy-product mechanics under `Complex.exp_add`).
- `Nat.gcd_comm` (d 32): antisymmetry layer → gcd divisibility lemmas → `gcd_rec` (Euclid's algorithm) at the bottom.
- `deriv_add`, `Real.exp_log`: equally clean (HasDerivAt layer → HasFDerivAt layer; exp_log_eq_abs → log_of_ne_zero).

Verdict: raising the depth cutoff over the recursive move tree produces *nested, mathematically sensible summaries* — the resolution-dial behavior originally hoped for, now on move trees instead of raw dependency cones. (The computed layer-coherence stat printed 1.0 but covers few pairs by construction — treat the qualitative trees, not that number, as the evidence.)

## Standing residue after this round

1. Shallow floor glue ties (bounded below depth ~15; relative weight shrinks as the library grows).
2. Universality grain for logic constants (design question, small effect).
3. Trivial-but-real arithmetic living in tactic libraries — correctly kept by structural measures; if the map wants them hidden it must be by *provenance display choice*, not by structure, and should be labeled as exactly that.
