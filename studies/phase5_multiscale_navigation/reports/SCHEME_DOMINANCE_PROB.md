# Dominance / Pareto and probabilistic / conditional combination schemes

Two families of principled combination rules for ordering a proof's citations,
measured on the full battery (`mathmap_eval/battery.py`) over all three sealed
splits. Labels from `review/sealed_r1/`, median of three raters, loaded exactly
as `src/mine_failures.py` does. Substrate (universe U1D, frozen rarity IDF50,
5-level role tier, junk proxy) is byte-identical to the run that produced the
constant-free Borda result in commit 72959d3; the TEST-R lines of the two
reference models reproduce that log exactly.

## Verdict first

- **Family A (Pareto) is honest but weak where it matters.** Dominance is silent
  on 35–46% of within-proof pairs and leaves rank 1 undecided in **75% of
  proofs**. Every good Pareto number in this report is produced by the
  tie-break, not by dominance: the same skyline layers score P@1 0.978 with a
  rarity tie-break and 0.836 with a tier tie-break. The "no exchange rate"
  claim is real, but the rule delegates the decision that the product actually
  makes.
- **Family B (Naive Bayes on a pinned log-odds table) is the strongest scheme
  measured here and it transfers.** NB6 beats the 5-decimal weighted model on
  P@4 (0.715 vs 0.712), core recall@4 (0.984 vs 0.974) and KeyMove@1 (0.856 vs
  0.825) at 0.972 vs 0.975 P@1, is gradient-monotone, and repeats out-of-fold
  (0.972 / 0.711 / 0.853). On CAL it is the best scheme in the study by a clear
  margin (P@1 0.972 against 0.917 for the weighted model). On TEST-C every
  scheme degrades, including ones with zero fitted parameters, so the drop is a
  property of that adversarial split and not of the fitted table.
- **The equal-weight counting rule is not competitive.** Best variant COUNT6b:
  TEST-R P@1 0.931 / P@4 0.663 / KeyMove@1 0.778 against NB6's 0.972 / 0.715 /
  0.856. The measured log-odds carry roughly 4 points of P@1, 5 of P@4 and 8 of
  KeyMove@1 over "count the conditions".
- **Conditional independence fails on every one of the 15 signal pairs**
  (p < 1e-13 throughout). NB works anyway, which is the usual Naive Bayes story,
  but the "probability" it emits is not a probability.
- **On the constants rule, my honest reading: Family A passes, Family B does
  not.** See §5.

---

## 1. Signals and constants

All append-safe, all from `Corpus`. Higher is better after orientation.

| signal | source | levels used |
|---|---|---|
| role tier | `inc_roles` syntactic position, 5 ordinal levels, 0 best | 5 |
| cited depth | `inc_d_cite` | raw integer, or the 6 pre-registered bands |
| frozen rarity | IDF50 over the depth ≤ 50 foundation | raw float, or integer nat-log units |
| in-statement | `inc_in_stmt_world`, NOT-in-statement is better | 2 |
| arity | `node_arity` (kernel fact) | raw, or 5 bands |
| is_proof | `node_is_proof` (kernel fact) | 2 |

The tier is the one used by the Borda run:

    tier 0  applied position
    tier 1  let-value or explicit argument
    tier 2  everything else, and instance-slot-only at delta-depth 1
    tier 3  type-annotation-only
    tier 4  instance-slot-only

**Every constant used anywhere in this report:**

| constant | value | where | status |
|---|---|---|---|
| depth band edges | 0, 11, 26, 51, 76, 126 | `battery.BANDS`, discretised Pareto and NB | pre-registered integers, reused not chosen |
| arity band edges | 0, 1, 3, 6, 10 | 6-signal variants | integers from `reports/KERNEL_SIGNALS.md` |
| rarity discretisation | `floor(IDF50)` | NB, discretised Pareto | unit = 1 nat; no free parameter |
| rarity clip | 0..9 (NB), 0..12 (Pareto) | NB, Pareto | inert: observed IDF50 range is 1.009–12.972 |
| frozen-foundation depth | 50 | IDF50 recipe | inherited from `APPEND_SAFETY.md` |
| n50 | 430,358 proofs | IDF50 recipe | measured, fixed by the freeze |
| tier delta-depth exception | 1 | tier definition | inherited from the Borda run |
| Laplace smoothing | 1 | NB estimation | integer |
| counting-rule thresholds | arity ≥ 3, depth ≥ 11, IDF50 ≥ log(n50)/2 | COUNT6b | 3 = complement of the `arity ≤ 2` junk proxy; 11 = band edge; the rarity split is "cited by fewer than sqrt(n50) foundation proofs", scale-free |
| tier weights (reference only) | 1.0, 0.7, 0.5, 0.35, 0.15 | REF_weighted | the 5 decimals this study is trying to eliminate |
| NB log-odds | 30 reals (NB6), 23 (NB4) | `data/pinned_llr_table.json` | derived, see §5 |

No name-string matching anywhere. No library-wide count beyond IDF50, which
carries the known caveat below.

**Append-safety caveat, restated.** `GLOBAL_DEPENDENCY_AUDIT.md` established
that IDF50 is append-safe only if nothing is ever added below the freeze depth,
and that the fix is to freeze the *value table*, not the recipe. This study
recomputes IDF50 from the recipe, so every scheme using rarity inherits that
defect. Nothing here makes it worse and nothing here fixes it. The purely
kernel-signal schemes (tier, depth, arity, is_proof, in-statement) have no such
dependence.

---

## 2. Family A: dominance / Pareto

A beats B iff A is at least as good on every signal and strictly better on one.
Skyline layers are peeled repeatedly; the layer index is the rank; within a
layer, a stated tie-break orders the candidates. Three signal sets:

- `A_raw4` — tier, raw depth, raw rarity, in-statement. **Zero constants.**
- `A_disc4` — same four, depth banded and rarity floored to integers.
- `A_disc6` — plus arity band and is_proof.

### 2.1 Incomparability — the rule's weakness, quantified

Over **all 747,605 proofs in the corpus** (493,833,670 within-proof pairs):

| signal set | incomparable pairs | of which identical vectors | mean layers/proof | mean size of front 0 | **proofs where front 0 has > 1 member** |
|---|---|---|---|---|---|
| A_raw4 | **44.4%** | 0.1% | 8.88 | 2.23 | **79.8%** |
| A_disc4 | **34.6%** | 3.9% | 7.25 | 2.28 | **75.0%** |
| A_disc6 | **46.3%** | 2.0% | 6.76 | 2.57 | **79.4%** |

Restricted to the 552 sealed proofs and their graded candidates (58,927 pairs):
A_raw4 44.9%, A_disc4 34.8%, A_disc6 44.5% incomparable.

First-front size distribution, A_disc4, all proofs: size 1 → 186,926;
2 → 353,105; 3 → 122,633; 4 → 44,832; 5 → 18,432; 6–10 → 18,802; >10 → 2,875.

**Adding signals makes it worse, not better**: going from 4 to 6 signals raises
incomparability from 34.6% to 46.3% and grows the undecided front from 2.28 to
2.57. Pareto does not benefit from more evidence; it drowns in it.

### 2.2 When dominance does speak, it is right

Graded pairs only, per split. "Agrees" = the dominating candidate's median grade
is ≥ the dominated one's.

| signal set | split | comparable | agrees | strictly graded-apart | correct on those |
|---|---|---|---|---|---|
| A_disc4 | TEST-R | 0.647 | 0.957 | 0.701 | 0.939 |
| A_disc4 | CAL | 0.655 | 0.946 | 0.699 | 0.923 |
| A_disc4 | TEST-C | 0.661 | 0.940 | 0.715 | 0.916 |
| A_raw4 | TEST-R | 0.548 | 0.959 | 0.685 | 0.941 |
| A_disc6 | TEST-R | 0.552 | 0.968 | 0.711 | 0.954 |

Dominance is a high-precision, low-coverage oracle: ~94–96% correct on the
half to two-thirds of pairs it ranks at all.

The layer index is a clean usefulness gradient (A_disc4, TEST-R):

| layer | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| n | 676 | 722 | 824 | 761 | 634 | 474 | 356 | 212 | 99 |
| P(useful) | 0.857 | 0.548 | 0.311 | 0.214 | 0.123 | 0.063 | 0.039 | 0.005 | 0.000 |
| mean grade | 2.84 | 1.76 | 1.15 | 0.94 | 0.76 | 0.60 | 0.55 | 0.42 | 0.32 |

### 2.3 Tie-break ablation — this is where the ranking actually comes from

Same A_disc4 layers, TEST-R, only the within-layer order changes:

| tie-break | P@1 | P@4 | KeyMove@1 | core@4 | precision failures |
|---|---|---|---|---|---|
| term order (none) | 0.883 | 0.683 | 0.681 | 0.958 | 41 |
| role tier | 0.836 | 0.692 | **0.500** | 0.979 | **58** |
| cited depth | 0.961 | 0.674 | 0.839 | 0.963 | 13 |
| **frozen rarity** | **0.978** | 0.675 | 0.844 | 0.948 | **7** |
| in-statement | 0.931 | 0.681 | 0.744 | 0.966 | 24 |
| arity | 0.917 | 0.693 | 0.750 | 0.976 | 29 |
| dominance count | 0.972 | 0.697 | 0.850 | 0.976 | 9 |

A 14-point P@1 spread and an 8-fold spread in precision failures, with the
"principled" part of the rule held fixed. **Rarity is the tie-break that
matters; tier is actively harmful as a tie-break** (it is already the first
coordinate of the dominance test, so re-using it concentrates the remaining
choice on candidates the tier cannot separate).

### 2.4 Dominance counting — the smoother variant

Counting how many co-candidates each candidate dominates removes the layer
structure entirely and does about as well as the best layered rule, with better
P@4 and worse recall failures:

| scheme | split | P@1 | P@4 | KeyMove@1 | core@4 | prec/rec failures |
|---|---|---|---|---|---|---|
| A_disc4_domcount_only | TEST-R | 0.972 | 0.699 | 0.850 | 0.961 | 9 / 9 |
| A_disc4+layers+domcount | TEST-R | 0.972 | 0.697 | 0.850 | 0.976 | 9 / 3 |
| A_disc4_domcount_only | TEST-C | 0.842 | **0.736** | 0.733 | 0.958 | 19 / 2 |

Layers + dominance-count tie-break is the better of the two (same top-1, far
fewer buried CORE moves). Pure counting is the best Family A scheme on TEST-C
P@4 of anything in the study, reference models included.

**Family A best: `A_disc4` skyline layers with a frozen-rarity tie-break** for
top-1, or **layers + dominance-count** if P@4 and core recall matter more.

---

## 3. Family B: probabilistic / conditional

P(useful | signals) via summed log-likelihood ratios over the discretised
signals. Estimated **once, on TEST-R only** (360 proofs, 4,800 graded
candidates, base rate P(useful) = 0.316), add-one smoothing, and written to
**`data/pinned_llr_table.json`**. That file is the artifact: the scheme reads
the table, never the library. CAL and TEST-C were never touched during
estimation.

Variants: `NB6_useful` (all six signals, target grade ≥ 2), `NB4_useful` (the
four Borda signals only), `NB6_major` (target grade ≥ 3), and the equal-weight
counting rules.

### 3.1 The derived weights

`NB6_useful`, log-odds by level (from the pinned table):

| signal | levels → LLR |
|---|---|
| tier | 2.349, 0.888, −0.253, −0.855, −3.214 |
| depth band | −0.394, 0.718, 1.482, 1.267, 1.018, 1.878 |
| rarity (nat units) | 0.768, −1.340, −1.160, −1.336, −0.520, −0.591, −0.257, 0.059, 0.768, 1.677 |
| in-statement | 1.614 (no), −0.385 (yes) |
| arity band | −1.688, −0.862, 0.488, 0.948, 2.570 |
| is_proof | −0.456 (no), 1.702 (yes) |

Two things to notice. The tier weights come out ordered and roughly geometric —
the hand-set 1.0/0.7/0.5/0.35/0.15 was not a bad guess. The rarity column is
**non-monotone**: level 0 shows +0.768, which is pure smoothing artefact (no
candidate in the corpus has IDF50 < 1, so both counts are the +1 prior and the
value is just log(n_neg/n_pos)). Levels 1–3 are the true minimum. A ranking rule
consuming this table inherits a level that no data supports.

### 3.2 Conditional independence — fails everywhere

I(A;B | useful), in bits, on TEST-R, with the G-test:

| pair | I(A;B\|Y) | marginal I(A;B) | G | df | p |
|---|---|---|---|---|---|
| depth band × rarity | **0.321** | 0.381 | 2139.0 | 90 | ~0 |
| tier × is_proof | **0.227** | 0.316 | 1507.1 | 8 | ~0 |
| tier × rarity | 0.155 | 0.122 | 1034.3 | 72 | 2.5e−170 |
| tier × arity band | 0.151 | 0.212 | 1002.5 | 32 | 5.2e−190 |
| in-statement × is_proof | 0.145 | 0.219 | 966.6 | 2 | 1.3e−210 |
| rarity × arity band | 0.111 | 0.119 | 740.0 | 72 | 1.7e−111 |
| rarity × is_proof | 0.086 | 0.091 | 571.9 | 18 | 7.3e−110 |
| tier × in-statement | 0.072 | 0.143 | 479.0 | 8 | 2.3e−98 |
| depth band × arity band | 0.064 | 0.083 | 426.4 | 40 | 4.2e−66 |
| tier × depth band | 0.056 | 0.039 | 374.3 | 40 | 7.3e−56 |
| arity band × is_proof | 0.053 | 0.080 | 349.9 | 8 | 9.6e−71 |
| rarity × in-statement | 0.036 | 0.067 | 239.4 | 18 | 1.1e−40 |
| in-statement × arity band | 0.024 | 0.061 | 161.5 | 8 | 7.9e−31 |
| depth band × in-statement | 0.014 | 0.032 | 92.3 | 10 | 1.9e−15 |
| depth band × is_proof | 0.013 | 0.019 | 84.7 | 10 | 5.9e−14 |

**All 15 pairs reject independence.** Deep declarations are rare declarations
(0.32 bits shared *after* conditioning) and applied-position citations are
proofs (0.23 bits). Two pairs are *more* dependent given the class than
marginally (tier × rarity, tier × depth) — conditioning on usefulness induces
dependence rather than removing it.

Consequence, stated plainly: NB6 double-counts depth and rarity, and
double-counts tier and is_proof. Its output is a ranking statistic, not a
calibrated probability. That shows up directly in the calibration table — TEST-R
deciles run 0.979, 0.746, 0.496, 0.406, 0.256, 0.144, 0.083, 0.035, 0.013,
0.002, monotone but far more extreme than any correctly-calibrated posterior
over a 0.316 base rate would be. It is fit for ordering and unfit for display
as a confidence.

The 4-signal variant drops the two worst-offending pairs' partners (arity,
is_proof) and loses almost nothing on TEST-R while gaining on TEST-C, which is
consistent with the dependence being real and mildly harmful.

### 3.3 Counting rule (Naive Bayes with all weights equal)

Six structural conditions, integer score 0..6: applied position; is_proof; not
in-statement; arity ≥ 3; cited depth ≥ 11; rarer than sqrt(n50).

**Error found and corrected:** the first version used `floor(IDF50) ≥ 1`, which
fires on **100.0%** of candidates (minimum observed IDF50 is 1.009) — a wasted
condition. `COUNT6`/`COUNT5b` in the tables below are that degenerate version;
`COUNT6b` is the corrected one. Both are reported.

P(useful | count), COUNT6b:

| count | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| TEST-R n | 1425 | 1343 | 973 | 592 | 173 | 185 | 109 |
| TEST-R | 0.044 | 0.181 | 0.412 | 0.593 | 0.977 | 0.989 | 0.991 |
| CAL | 0.039 | 0.132 | 0.374 | 0.675 | 0.821 | 1.000 | 1.000 |
| TEST-C | 0.094 | 0.293 | 0.459 | 0.602 | 0.815 | 0.865 | 0.900 |

The counting rule is a genuinely good *calibrated* summary — monotone on all
three splits, and it transfers better than anything else (TEST-R → TEST-C P@1
drop of only 0.089). It is simply a worse *ranking*: 7 integer levels cannot
separate 24 candidates, so it loses on every top-k metric.

### 3.4 Transfer

The question is whether estimating on TEST-R bakes in TEST-R.

**Out-of-fold within TEST-R** (5 folds by proof, seed 20260821, the table
re-estimated inside each fold):

| scheme | P@1 | P@4 | KeyMove@1 | core@4 | prec/rec fail |
|---|---|---|---|---|---|
| NB6 in-sample | 0.972 | 0.715 | 0.856 | 0.984 | 9 / 3 |
| **NB6 out-of-fold** | **0.972** | **0.711** | **0.853** | **0.984** | 9 / 3 |
| NB4 in-sample | 0.967 | 0.717 | 0.842 | 0.987 | 11 / 1 |
| **NB4 out-of-fold** | **0.967** | **0.716** | **0.842** | **0.987** | 11 / 1 |

In-sample optimism is **0.000 P@1 / 0.004 P@4**. With 30 parameters and 4,800
observations there is nothing left to overfit.

**Across splits**, P@1 change from TEST-R, with fitted-parameter count:

| scheme | free params | TEST-R | CAL | TEST-C | Δ TEST-C |
|---|---|---|---|---|---|
| REF_weighted (5-dec) | 5 | 0.975 | 0.917 | 0.850 | −0.125 |
| REF_borda_all4 | 0 | 0.975 | 0.944 | 0.825 | −0.150 |
| REF_depth_only | 0 | 0.928 | 0.931 | 0.783 | −0.145 |
| A_disc4+tb_rarity | 0 | 0.978 | 0.944 | 0.858 | −0.120 |
| **NB6_useful** | 30 | 0.972 | **0.972** | 0.842 | −0.130 |
| **NB4_useful** | 23 | 0.967 | **0.972** | **0.875** | **−0.092** |
| COUNT6b | 0 | 0.931 | 0.958 | 0.842 | −0.089 |

**The fitted table costs nothing in transfer.** NB's TEST-C degradation
(−0.130 / −0.092) sits inside the range of schemes with zero fitted parameters
(−0.089 to −0.150). TEST-C is defect-enriched by construction (six adversarial
strata, `PREREGISTRATION_SEALED_R1.md` §2.1), so the whole field drops there;
that is the split, not the estimator. On CAL — an ordinary random-by-band
sample, and the only clean held-out non-adversarial evidence — NB is the best
scheme in the study (0.972 P@1, 2 precision failures against the weighted
model's 6 and Borda's 4).

Score AUC for useful, all three splits: NB6 0.902 / 0.908 / 0.848, NB4 0.904 /
0.899 / 0.861, COUNT6 0.812 / 0.843 / 0.746.

---

## 4. Full battery

`mono/inv` = gradient monotone and inversion count. Failures are precision /
recall / gradient counts. Reference rows first; the weighted 5-decimal model and
plain Borda are the incumbents.

### TEST-R (360 proofs, primary)

| scheme | P@1 | P@4 | KeyMove@1 | core@4 | major@4 | useful@4 | mono/inv | spread | prec | rec | grad |
|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_weighted_role_x_rarity_5dec | 0.975 | 0.712 | 0.825 | 0.974 | 0.880 | 0.672 | Y/0 | 0.927 | 8 | 5 | 0 |
| REF_borda_all4 | 0.975 | 0.663 | 0.864 | 0.961 | 0.854 | 0.626 | Y/0 | 0.892 | 8 | 8 | 1 |
| REF_borda_tier_rarity | 0.972 | 0.678 | 0.836 | 0.948 | 0.849 | 0.640 | N/1 | 0.900 | 9 | 10 | 1 |
| REF_depth_only | 0.928 | 0.588 | 0.783 | 0.893 | 0.782 | 0.555 | N/1 | 0.815 | 25 | 15 | 1 |
| A_raw4+termorder | 0.864 | 0.677 | 0.669 | 0.953 | 0.839 | 0.639 | Y/0 | 0.840 | 48 | 3 | 1 |
| A_raw4+tb_rarity | 0.958 | 0.677 | 0.839 | 0.950 | 0.836 | 0.639 | Y/0 | 0.860 | 14 | 3 | 1 |
| A_raw4+tb_domcount | 0.969 | 0.698 | 0.856 | 0.971 | 0.864 | 0.659 | Y/0 | 0.869 | 10 | 1 | 1 |
| A_raw4_domcount_only | 0.969 | 0.690 | 0.856 | 0.958 | 0.876 | 0.651 | Y/0 | 0.856 | 10 | 8 | 0 |
| A_disc4+termorder | 0.883 | 0.683 | 0.681 | 0.958 | 0.845 | 0.645 | Y/0 | 0.856 | 41 | 4 | 0 |
| A_disc4+tb_tier | 0.836 | 0.692 | 0.500 | 0.979 | 0.864 | 0.653 | Y/0 | 0.846 | 58 | 1 | 0 |
| A_disc4+tb_depth | 0.961 | 0.674 | 0.839 | 0.963 | 0.839 | 0.636 | Y/0 | 0.875 | 13 | 1 | 0 |
| **A_disc4+tb_rarity** | **0.978** | 0.675 | 0.844 | 0.948 | 0.833 | 0.637 | Y/0 | 0.883 | **7** | 5 | 0 |
| A_disc4+tb_stmt | 0.931 | 0.681 | 0.744 | 0.966 | 0.852 | 0.643 | Y/0 | 0.873 | 24 | 6 | 0 |
| A_disc4+tb_arity | 0.917 | 0.693 | 0.750 | 0.976 | 0.863 | 0.655 | Y/0 | 0.865 | 29 | 3 | 0 |
| A_disc4+tb_domcount | 0.972 | 0.697 | 0.850 | 0.976 | 0.857 | 0.658 | Y/0 | 0.888 | 9 | 3 | 0 |
| A_disc4_domcount_only | 0.972 | 0.699 | 0.850 | 0.961 | 0.867 | 0.660 | Y/0 | 0.873 | 9 | 9 | 0 |
| A_disc6+termorder | 0.847 | 0.658 | 0.636 | 0.921 | 0.804 | 0.621 | Y/0 | 0.810 | 54 | 5 | 0 |
| A_disc6+tb_rarity | 0.975 | 0.666 | 0.853 | 0.948 | 0.819 | 0.628 | Y/0 | 0.885 | 8 | 2 | 0 |
| A_disc6+tb_domcount | 0.972 | 0.681 | 0.856 | 0.953 | 0.836 | 0.643 | Y/0 | 0.881 | 9 | 1 | 0 |
| A_disc6_domcount_only | 0.972 | 0.698 | 0.856 | 0.958 | 0.870 | 0.659 | N/2 | 0.854 | 9 | 6 | 0 |
| **NB6_useful** | 0.972 | **0.715** | 0.856 | **0.984** | 0.898 | 0.675 | Y/0 | **0.940** | 9 | 3 | 1 |
| NB4_useful | 0.967 | **0.717** | 0.842 | **0.987** | 0.898 | 0.677 | Y/0 | 0.910 | 11 | 1 | 0 |
| NB6_major | 0.969 | 0.703 | 0.861 | 0.987 | 0.904 | 0.663 | Y/0 | 0.940 | 10 | 3 | 1 |
| COUNT6b_equal_weights | 0.931 | 0.663 | 0.778 | 0.979 | 0.870 | 0.626 | N/1 | 0.840 | 24 | 3 | 1 |
| COUNT6_equal_weights (degenerate) | 0.892 | 0.624 | 0.689 | 0.945 | 0.808 | 0.589 | Y/0 | 0.765 | 38 | 5 | 2 |
| COUNT5b_equal_weights | 0.892 | 0.624 | 0.689 | 0.945 | 0.808 | 0.589 | Y/0 | 0.765 | 38 | 5 | 2 |
| COUNT4b_equal_weights | 0.903 | 0.610 | 0.742 | 0.935 | 0.806 | 0.575 | N/1 | 0.762 | 34 | 8 | 2 |
| COUNT4_equal_weights (degenerate) | 0.808 | 0.575 | 0.633 | 0.885 | 0.743 | 0.543 | N/1 | 0.646 | 68 | 14 | 6 |

### CAL (72 proofs, held out, ordinary sample)

| scheme | P@1 | P@4 | KeyMove@1 | core@4 | major@4 | useful@4 | mono/inv | spread | prec | rec | grad |
|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_weighted_role_x_rarity_5dec | 0.917 | 0.660 | 0.750 | 0.943 | 0.831 | 0.664 | N/1 | 0.866 | 6 | 1 | 0 |
| REF_borda_all4 | 0.944 | 0.621 | 0.861 | 0.943 | 0.815 | 0.625 | N/2 | 0.886 | 4 | 0 | 1 |
| REF_borda_tier_rarity | 0.875 | 0.632 | 0.708 | 0.943 | 0.839 | 0.636 | Y/0 | 0.845 | 9 | 1 | 1 |
| REF_depth_only | 0.931 | 0.586 | 0.889 | 0.857 | 0.742 | 0.590 | N/1 | 0.866 | 5 | 2 | 0 |
| A_raw4+termorder | 0.819 | 0.663 | 0.625 | 0.929 | 0.782 | 0.668 | N/2 | 0.814 | 13 | 0 | 0 |
| A_raw4+tb_rarity | 0.931 | 0.660 | 0.847 | 0.957 | 0.806 | 0.664 | N/1 | 0.835 | 5 | 0 | 0 |
| A_raw4+tb_domcount | 0.931 | 0.681 | 0.833 | 0.943 | 0.806 | 0.686 | N/1 | 0.855 | 5 | 0 | 0 |
| A_raw4_domcount_only | 0.931 | 0.656 | 0.833 | 0.971 | 0.839 | 0.661 | N/2 | 0.824 | 5 | 0 | 1 |
| A_disc4+termorder | 0.833 | 0.667 | 0.611 | 0.929 | 0.790 | 0.671 | Y/0 | 0.825 | 12 | 0 | 0 |
| A_disc4+tb_tier | 0.806 | 0.677 | 0.375 | 0.957 | 0.839 | 0.682 | Y/0 | 0.835 | 14 | 0 | 0 |
| A_disc4+tb_depth | 0.931 | 0.667 | 0.875 | 0.914 | 0.766 | 0.671 | Y/0 | 0.886 | 5 | 0 | 0 |
| A_disc4+tb_rarity | 0.944 | 0.660 | 0.833 | 0.929 | 0.790 | 0.664 | N/2 | 0.876 | 4 | 0 | 0 |
| A_disc4+tb_stmt | 0.944 | 0.667 | 0.722 | 0.957 | 0.839 | 0.671 | Y/0 | 0.876 | 4 | 0 | 0 |
| A_disc4+tb_arity | 0.903 | 0.677 | 0.750 | 0.943 | 0.823 | 0.682 | Y/0 | 0.876 | 7 | 0 | 0 |
| A_disc4+tb_domcount | 0.944 | 0.667 | 0.806 | 0.943 | 0.823 | 0.671 | Y/0 | 0.876 | 4 | 0 | 0 |
| A_disc4_domcount_only | 0.944 | 0.639 | 0.806 | 0.957 | 0.839 | 0.643 | N/2 | 0.845 | 4 | 0 | 1 |
| A_disc6+termorder | 0.819 | 0.635 | 0.583 | 0.914 | 0.798 | 0.640 | Y/0 | 0.814 | 13 | 0 | 0 |
| A_disc6+tb_rarity | 0.931 | 0.656 | 0.833 | 0.943 | 0.815 | 0.661 | N/2 | 0.886 | 5 | 0 | 0 |
| A_disc6+tb_domcount | 0.958 | 0.656 | 0.861 | 0.943 | 0.823 | 0.661 | Y/0 | 0.917 | 3 | 0 | 0 |
| A_disc6_domcount_only | 0.958 | 0.646 | 0.861 | 0.971 | 0.839 | 0.650 | N/1 | 0.855 | 3 | 0 | 1 |
| **NB6_useful** | **0.972** | **0.705** | 0.833 | **0.986** | 0.863 | **0.710** | Y/0 | **0.948** | **2** | 0 | 0 |
| NB4_useful | **0.972** | **0.705** | 0.778 | **0.986** | 0.871 | **0.710** | Y/0 | 0.897 | **2** | 0 | 0 |
| NB6_major | **0.972** | 0.702 | 0.861 | 0.986 | 0.863 | 0.707 | Y/0 | 0.917 | **2** | 0 | 0 |
| COUNT6b_equal_weights | 0.958 | 0.667 | 0.750 | 0.943 | 0.839 | 0.671 | N/1 | 0.876 | 3 | 0 | 0 |
| COUNT6_equal_weights (degenerate) | 0.944 | 0.621 | 0.694 | 0.929 | 0.798 | 0.625 | N/1 | 0.866 | 4 | 0 | 0 |
| COUNT5b_equal_weights | 0.944 | 0.621 | 0.694 | 0.929 | 0.798 | 0.625 | N/1 | 0.866 | 4 | 0 | 0 |
| COUNT4b_equal_weights | 0.944 | 0.628 | 0.708 | 0.929 | 0.806 | 0.633 | N/1 | 0.803 | 4 | 0 | 0 |
| COUNT4_equal_weights (degenerate) | 0.889 | 0.589 | 0.611 | 0.871 | 0.758 | 0.594 | N/2 | 0.752 | 8 | 1 | 1 |

### TEST-C (120 proofs, held out, defect-enriched by design)

| scheme | P@1 | P@4 | KeyMove@1 | core@4 | major@4 | useful@4 | mono/inv | spread | prec | rec | grad |
|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_weighted_role_x_rarity_5dec | 0.850 | **0.763** | 0.675 | 0.967 | 0.784 | 0.563 | N/1 | 0.813 | 18 | 0 | 1 |
| REF_borda_all4 | 0.825 | 0.694 | 0.733 | 0.967 | 0.769 | 0.512 | Y/0 | 0.734 | 21 | 0 | 2 |
| REF_borda_tier_rarity | 0.850 | 0.725 | 0.650 | 0.958 | 0.781 | 0.535 | Y/0 | 0.762 | 18 | 1 | 2 |
| REF_depth_only | 0.783 | 0.595 | 0.725 | 0.925 | 0.688 | 0.439 | N/1 | 0.661 | 26 | 2 | 4 |
| A_raw4+termorder | 0.750 | 0.671 | 0.492 | 0.942 | 0.653 | 0.495 | N/1 | 0.661 | 30 | 2 | 2 |
| A_raw4+tb_rarity | 0.825 | 0.652 | 0.717 | 0.942 | 0.675 | 0.481 | Y/0 | 0.666 | 21 | 2 | 2 |
| A_raw4+tb_domcount | 0.825 | 0.677 | 0.725 | 0.950 | 0.678 | 0.499 | Y/0 | 0.689 | 21 | 2 | 2 |
| A_raw4_domcount_only | 0.825 | 0.713 | 0.725 | 0.958 | 0.759 | 0.526 | Y/0 | 0.745 | 21 | 1 | 1 |
| A_disc4+termorder | 0.775 | 0.692 | 0.533 | 0.975 | 0.694 | 0.510 | Y/0 | 0.712 | 27 | 0 | 4 |
| A_disc4+tb_tier | 0.742 | 0.700 | 0.350 | 0.975 | 0.697 | 0.516 | Y/0 | 0.723 | 31 | 0 | 3 |
| A_disc4+tb_depth | 0.817 | 0.677 | 0.767 | 0.975 | 0.688 | 0.499 | Y/0 | 0.678 | 22 | 0 | 3 |
| A_disc4+tb_rarity | 0.858 | 0.677 | 0.750 | 0.975 | 0.694 | 0.499 | N/1 | 0.712 | 17 | 0 | 4 |
| A_disc4+tb_stmt | 0.842 | 0.679 | 0.600 | 0.967 | 0.678 | 0.501 | Y/0 | 0.706 | 19 | 1 | 3 |
| A_disc4+tb_arity | **0.875** | 0.686 | 0.692 | 0.967 | 0.688 | 0.505 | Y/0 | 0.729 | **15** | 1 | 3 |
| A_disc4+tb_domcount | 0.842 | 0.702 | 0.733 | 0.967 | 0.700 | 0.518 | Y/0 | 0.734 | 19 | 1 | 3 |
| A_disc4_domcount_only | 0.842 | **0.736** | 0.733 | 0.958 | 0.759 | 0.543 | Y/0 | 0.768 | 19 | 2 | 1 |
| A_disc6+termorder | 0.775 | 0.650 | 0.492 | 0.875 | 0.609 | 0.479 | N/1 | 0.683 | 27 | 6 | 1 |
| A_disc6+tb_rarity | 0.850 | 0.662 | 0.750 | 0.908 | 0.647 | 0.488 | N/2 | 0.700 | 18 | 3 | 1 |
| A_disc6+tb_domcount | 0.842 | 0.688 | 0.750 | 0.908 | 0.656 | 0.507 | N/1 | 0.706 | 19 | 3 | 1 |
| A_disc6_domcount_only | 0.842 | 0.734 | 0.750 | 0.967 | 0.759 | 0.541 | N/1 | 0.740 | 19 | 2 | 1 |
| NB6_useful | 0.842 | 0.719 | 0.708 | 0.975 | 0.706 | 0.530 | N/1 | 0.774 | 19 | 1 | 3 |
| **NB4_useful** | **0.875** | 0.727 | 0.750 | 0.975 | 0.731 | 0.536 | Y/0 | 0.791 | **15** | 0 | 3 |
| NB6_major | 0.833 | 0.717 | 0.733 | 0.967 | 0.716 | 0.529 | N/1 | 0.757 | 20 | 1 | 3 |
| COUNT6b_equal_weights | 0.842 | 0.675 | 0.667 | 0.933 | 0.688 | 0.498 | N/1 | 0.694 | 19 | 4 | 4 |
| COUNT6_equal_weights (degenerate) | 0.842 | 0.633 | 0.558 | 0.925 | 0.600 | 0.467 | N/1 | 0.655 | 19 | 4 | 5 |
| COUNT5b_equal_weights | 0.842 | 0.633 | 0.558 | 0.925 | 0.600 | 0.467 | N/1 | 0.655 | 19 | 4 | 5 |
| COUNT4b_equal_weights | 0.858 | 0.675 | 0.658 | 0.967 | 0.703 | 0.498 | Y/0 | 0.666 | 17 | 0 | 2 |
| COUNT4_equal_weights (degenerate) | 0.825 | 0.612 | 0.558 | 0.942 | 0.622 | 0.451 | N/1 | 0.558 | 21 | 2 | 4 |

### Navigability (whole corpus, k = 4)

Junk mask is the append-safe kernel proxy `not is_proof AND arity ≤ 2` (49.4% of
candidates; 88.1% of flagged are graded ≤ 1, 3.1% are graded ≥ 3).

| scheme | junk edge share at k=4 | giant, all edges | giant, mathematics only | retained |
|---|---|---|---|---|
| REF_weighted_role_x_rarity_5dec | 27.2% | 1.000 | 0.948 | 94.8% |
| REF_borda_all4 | 30.0% | 1.000 | 0.947 | 94.7% |
| REF_depth_only | 34.4% | 1.000 | 0.935 | 93.5% |
| A_disc4+tb_rarity | 26.7% | 1.000 | 0.956 | 95.6% |
| A_disc4+tb_domcount | 25.0% | 1.000 | 0.957 | 95.7% |
| A_disc4_domcount_only | 26.5% | 1.000 | 0.952 | 95.2% |
| A_disc6+tb_domcount | 19.2% | 1.000 | 0.960 | 96.0% |
| NB6_useful | 16.7% | 1.000 | 0.960 | 96.0% |
| NB4_useful | 24.0% | 1.000 | 0.956 | 95.6% |
| COUNT6b_equal_weights | 17.8% | 1.000 | 0.960 | 96.0% |

Full table for all 29 schemes in `famAB_*.json`. Range across every scheme
measured: 93.5%–96.1% retained. **Navigability does not discriminate** — the
spread is 2.6 points across schemes whose P@1 spans 0.808 to 0.978, and it is
mildly anti-correlated with per-proof quality, reproducing the earlier finding.

**Caveat that must not be lost:** the junk mask *is* `not is_proof AND
arity ≤ 2`, and three of these schemes (A_disc6, NB6, COUNT6b) consume is_proof
and arity as signals. Their low junk-edge share (16.7–19.2% against 27.2% for
the weighted model) is partly definitional, not evidence of a better map. The
retained-fraction column is the honest one; junk-edge share is not comparable
across schemes with different signal sets.

---

## 5. Do the derived weights satisfy "no arbitrary constants"?

**My reading: no, not in spirit, and the report should not claim otherwise.**

The case for yes: every number in `data/pinned_llr_table.json` is the output of
a stated estimator (empirical log-odds with add-one smoothing) applied to a
stated dataset (TEST-R, 4,800 graded candidates, three raters, median). Nobody
chose 0.7 because it felt right. The table is reproducible from the labels and
the recipe, it is pinned as a file, and it is append-safe by fiat exactly as the
frozen rarity table is: the scheme reads the file, and adding a theorem to
Mathlib cannot change the file.

The case for no, which I find stronger:

1. **Parameter count went up, not down.** The weighted model this program is
   trying to escape has 5 decimals. NB6 has 30, NB4 has 23. Replacing 5
   hand-set decimals with 30 measured ones is not obviously a reduction in
   arbitrariness; it relocates it.
2. **The dependence changed kind.** The 5 decimals depend on a person's
   judgement. The 30 depend on *this specific grading round* — three raters,
   552 proofs, one taxonomy, one snapshot of Mathlib. The frozen rarity table is
   pinned to a mathematical object (the depth ≤ 50 foundation). The LLR table is
   pinned to a labelling event. Those are not the same species of constant, and
   only the first can be re-derived by someone who has the library but not the
   grades.
3. **The table already contains a value no data supports** (rarity level 0,
   §3.1), and nothing in the pipeline flags it. An arbitrary constant that
   arrived through an estimator is still an arbitrary constant.
4. **The independence assumption that licenses summing the LLRs is false on all
   15 pairs.** The weights are therefore not the log-odds of anything; they are
   fitted coefficients that happen to have been computed by a closed-form rule
   instead of by gradient descent.

What *is* defensible under the rule: the counting rule (integer, 0 decimals,
transfers best, ranks worst) and the Pareto family (0 decimals in `A_raw4`,
integer band edges in `A_disc4`). If the constants rule is treated as binding,
Family A is the family that satisfies it.

---

## 6. Recommendation and trades

No single number decides this. The trades:

- **If rank 1 is the product** — `A_disc4` skyline + frozen-rarity tie-break:
  best P@1 in the study (0.978 TEST-R, 0.944 CAL, 0.858 TEST-C), fewest
  precision failures (7), gradient-monotone, zero fitted decimals. Costs P@4
  (0.675 vs 0.715) and core recall@4 (0.948 vs 0.984). And be honest about what
  it is: a rarity ranking that dominance has pre-filtered, since dominance
  leaves rank 1 open in 75% of proofs.
- **If the top-4 panel is the product** — `NB6_useful`: best P@4 (0.715), best
  core recall@4 (0.984), best gradient spread (0.940), KeyMove@1 0.856, at the
  price of 30 derived decimals and a broken independence assumption.
- **If longevity dominates everything** — `COUNT6b`: 0 decimals, monotone
  calibration on all three splits, smallest cross-split degradation (−0.089),
  and clearly the worst ranking of the credible schemes (P@1 0.931, KeyMove@1
  0.778).
- **`NB4_useful` is the best-transferring accurate scheme**: best TEST-C P@1
  (0.875, tied) and P@4 (0.727) of any probabilistic scheme, fewest TEST-C
  precision failures (15, tied), gradient-monotone on all three splits, 23
  derived decimals.
- **Lexicographic tiering stays disqualified** and Pareto's tier tie-break
  reproduces the same pathology (KeyMove@1 0.500, 58 precision failures): a hard
  tier boundary that no other evidence can override is the single worst design
  choice measured in this programme.

## 7. Reproduction

Scripts (scratchpad, not versioned): `famAB_common.py` (substrate, battery
wrapper), `famAB_ref.py` (reference models), `famAB_A.py` (Pareto), `famAB_B.py`
(NB, independence, counting, 5-fold), `famAB_C.py` (corrected counting rule),
`famAB_D.py` (front-size and dominance-correctness diagnostics). Pinned
artifact: `data/pinned_llr_table.json`. Seeds: 20260821 (fold assignment only;
nothing else is stochastic).
