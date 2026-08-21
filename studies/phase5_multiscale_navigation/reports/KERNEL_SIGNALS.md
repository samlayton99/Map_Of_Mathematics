# Kernel-local declaration signals

Append-safe substitutes for `decl_logic_only`. Pipeline work only: no ranking
was added, changed, or re-run.

## Status

Lean was NOT re-run. `pr`, `ps`, `ar` were already emitted by
`mathrecord/Mathrecord/DepDump.lean` and already present in the dump on disk
(`scratchpad/mathlib_deps7.jsonl`, 771,129 rows), and `src/build_incidence.py`
already carried all three into `data/nodes.npz`. The only change needed was
exposure on `Corpus`.

## What was already available

`data/nodes.npz` keys, unchanged: `kind, pr, ps, ar, gen, depth, in_degree, stated`.
All 771,129 long, one row per declaration, aligned with `data/names.json`.

Definitions (from the DepDump docstring, all kernel checks, no name strings):

| field | meaning |
|---|---|
| `pr` | the constant's type IS a Prop -- the constant is a proof (`Meta.isProp`, not the kind proxy) |
| `ps` | the type telescopes to `Sort 0` -- the constant is a proposition or a predicate, not data |
| `ar` | arity: binders the type telescopes through (`forallTelescopeReducing`) |

Each is a function of the declaration's own type alone. No usage counts, no
library-wide thresholds, no neighbourhood. Adding theorems to Mathlib cannot
change a value already recorded for an existing declaration -- append-safe by
construction. Contrast `decl_logic_only` in `src/build_v8_mask.py`, which is
gated on `univ[k] < THETA`, a library-wide statement-frequency threshold, and
therefore shifts as the library grows.

Verification that the on-disk arrays match the dump: stride sample of the full
1.3 GB dump, every 13th row, 59,317 rows checked against `nodes.npz` via
`names.json` -- 0 mismatches, 0 dump rows missing from `names.json`, dump row
count exactly equal to `n_nodes`.

## What was added

`mathmap_eval/corpus.py` only:

- `load()` reads `nodes["pr"] / ["ps"] / ["ar"]` into `_node_pr / _node_ps / _node_ar`.
- Three documented properties: `node_is_proof`, `node_is_prop`, `node_arity`.
  Each calls `load()` on access, like `universe()`.

No existing array was touched. `nodes.npz` was not rewritten. `python -m
mathmap_eval.tests` passes all invariants (T1-T8), and all 17 previously
exposed corpus arrays load with unchanged shape and dtype.

Gap, for the record: DepDump does not emit the binder-info telescope of a
declaration's OWN type, so "does this declaration take instance-implicit
binders" is not derivable from the current dump. Role 4 in `vo` is
instance-implicit *argument position in a citing proof*, a different fact.
Getting the former needs a Lean re-run; it was not required for the signals
requested here.

## Distributions

Per declaration (n = 771,129):

| signal | value |
|---|---|
| `is_proof` true | 553,433 (0.7177) |
| `is_prop` true | 5,811 (0.0075) |
| `arity` | min 0, max 106, mean 6.34, median 5, p90 12, p99 23 |

Arity bands, per declaration: 0 -> 36,356 (0.047); 1-2 -> 99,907 (0.130);
3-5 -> 257,261 (0.334); 6-9 -> 229,703 (0.298); 10+ -> 147,902 (0.192).

By kind:

| kind | n | is_proof | is_prop | bare | mean arity |
|---|---|---|---|---|---|
| theorem | 533,320 | 1.000 | 0.000 | 0.0000 | 6.91 |
| def | 211,455 | 0.079 | 0.017 | 0.0000 | 5.08 |
| inductive | 6,790 | 0.000 | 0.337 | 0.0004 | 2.96 |
| constructor | 9,571 | 0.323 | 0.000 | 0.0000 | 4.69 |
| recursor | 6,913 | 0.045 | 0.000 | 0.0000 | 6.97 |
| opaque | 3,061 | 0.000 | 0.000 | 0.0000 | 4.01 |
| quot | 4 | 0.250 | 0.000 | 0.0000 | 4.00 |
| axiom | 15 | 0.400 | 0.000 | 0.0000 | 1.87 |

`is_proof` agrees with kind=theorem on every theorem but also fires on 7.9% of
`def`s (proof-valued definitions) and 32.3% of constructors -- it is not a kind
proxy.

Incidence-weighted over universe U1D (18,081,920 incidences): `is_proof` 0.177,
`is_prop` 0.090, bare 0.0065, mean arity 3.26. Arity bands 0/1-2/3-5/6-9/10+ =
0.111 / 0.420 / 0.293 / 0.139 / 0.036. Cited declarations are far shallower in
arity than the library average -- what proofs cite skews to low-arity constants.

## Bare-proposition sanity check: PASS

`is_prop AND arity == 0` fires on exactly 5 declarations in all of Mathlib:

    False (inductive), True (inductive), UnivLE (inductive),
    FermatLastTheorem (def), RiemannHypothesis (def)

Expected order of magnitude, expected membership: the two logical constants and
three named conjectures stated as closed propositions. Nothing anomalous.

## Against the graded labels

Labels from `review/sealed_r1/`, loaded the way `src/mine_failures.py` does
(keymap + `grades_*.json`, median over raters). 7,531 graded incidences across
552 proofs (TEST-R 4,800 / TEST-C 1,769 / CAL 962). Grade counts:
0 -> 2,291, 1 -> 2,793, 2 -> 1,319, 3 -> 556, 4 -> 572.

Fraction of each grade carrying each signal (all splits):

| grade | n | is_proof | is_prop | bare | logic_only | ar 0 | ar 1-2 | ar 3-5 | ar 6-9 | ar 10+ | med ar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 JUNK | 2,291 | 0.064 | 0.038 | 0.016 | 0.272 | 0.112 | 0.678 | 0.161 | 0.045 | 0.004 | 2 |
| 1 BAD_GLUE | 2,793 | 0.107 | 0.179 | 0.002 | 0.702 | 0.099 | 0.425 | 0.339 | 0.131 | 0.006 | 2 |
| 2 LEGIT_GLUE | 1,319 | 0.244 | 0.200 | 0.001 | 0.494 | 0.035 | 0.288 | 0.472 | 0.174 | 0.032 | 4 |
| 3 MAJOR | 556 | 0.286 | 0.176 | 0.004 | 0.230 | 0.022 | 0.180 | 0.487 | 0.252 | 0.059 | 4 |
| 4 CORE | 572 | 0.879 | 0.005 | 0.000 | 0.042 | 0.003 | 0.121 | 0.344 | 0.337 | 0.194 | 6 |

The three splits agree on every column; see the per-split tables below for the
TEST-R / TEST-C / CAL breakdown of the same quantities.

AUC against `useful = grade >= 2`, all splits (`rarity_live` and `d_cite` shown
as already-known reference points, `rarity_live` is not append-safe):

| signal | AUC | append-safe |
|---|---|---|
| arity | 0.742 | yes |
| is_proof | 0.657 | yes |
| is_prop | 0.517 | yes |
| decl_logic_only | 0.410 | no |
| rarity_live (ref) | 0.817 | no |
| d_cite (ref) | 0.722 | yes |

Per split, arity 0.751 / 0.716 / 0.759 and is_proof 0.669 / 0.604 / 0.700
(TEST-R / TEST-C / CAL). Stable.

Conditional usefulness rates, all splits (base rate 0.325):

| condition | n | useful rate | mean grade |
|---|---|---|---|
| is_proof | 1,431 | 0.688 | 2.40 |
| not is_proof | 6,100 | 0.240 | 0.98 |
| is_prop | 953 | 0.383 | 1.40 |
| not is_prop | 6,578 | 0.317 | 1.22 |
| arity 0 | 594 | 0.101 | 0.70 |
| arity >= 10 | 214 | 0.869 | 3.01 |
| bare proposition | 44 | 0.068 | 0.30 |
| decl_logic_only | 3,388 | 0.237 | 1.11 |
| not decl_logic_only | 4,143 | 0.397 | 1.36 |

## Are they predictive

Yes for `arity` and `is_proof`; no for `is_prop` on its own.

- **arity** is the strongest append-safe per-declaration signal measured here.
  It is monotone in grade (median 2, 2, 4, 4, 6) and its AUC (0.742) beats the
  incumbent `decl_logic_only` and matches `d_cite` (0.722). It does not reach
  `rarity_live` (0.817), which is count-based and not append-safe.
- **is_proof** separates the top grade sharply: 0.879 of CORE candidates are
  proofs versus 0.064 of JUNK. Useful rate 0.688 vs 0.240. As a binary its AUC
  is capped at 0.657, but as a factor it is clean.
- **is_prop alone is not predictive** (AUC 0.517; useful rate 0.383 vs 0.317,
  in the wrong direction for a plumbing detector). It peaks at grades 1-3 and
  collapses at grade 4 (0.005). Do not use it as a drop-in for
  `decl_logic_only`. Its value is inside conjunctions.

Plumbing detectors compared, on all 7,531 graded incidences. Defect = grade <= 1,
base rate 0.675:

| predicate | n | coverage | P(defect \| T) | P(defect \| ~T) | append-safe |
|---|---|---|---|---|---|
| `decl_logic_only` (incumbent) | 3,388 | 0.450 | 0.763 | 0.603 | no |
| `~is_proof & arity <= 2` | 3,518 | 0.467 | 0.888 | 0.489 | yes |
| `arity <= 2` | 3,882 | 0.515 | 0.843 | 0.496 | yes |
| `arity == 0` | 594 | 0.079 | 0.899 | 0.656 | yes |
| `~is_proof` | 6,100 | 0.810 | 0.760 | 0.312 | yes |
| `is_prop & arity <= 2` | 263 | 0.035 | 0.722 | 0.673 | yes |
| bare prop (`is_prop & arity == 0`) | 44 | 0.006 | 0.932 | 0.674 | yes |
| `is_prop` | 953 | 0.127 | 0.617 | 0.683 | yes |

The headline for the next round: **`~is_proof & arity <= 2` dominates
`decl_logic_only` on this data at matched coverage** -- 0.467 vs 0.450 coverage,
0.888 vs 0.763 defect rate -- and it is append-safe where the incumbent is not.
Bare-proposition is a near-pure defect flag (0.932) but reaches only 0.6% of
candidates, so it is a tiebreaker, not a detector.

These are descriptive statistics measured on already-graded data. No ranking
consumes them yet, and any round that adopts them owes a fresh seal.

## Per-split tables

TEST-R (4,800 graded incidences, 360 proofs):

| grade | n | is_proof | is_prop | bare | logic_only | ar 0 | ar 1-2 | ar 3-5 | ar 6-9 | ar 10+ | med ar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1,432 | 0.079 | 0.034 | 0.014 | 0.273 | 0.106 | 0.679 | 0.155 | 0.054 | 0.005 | 2 |
| 1 | 1,851 | 0.072 | 0.172 | 0.001 | 0.702 | 0.100 | 0.425 | 0.343 | 0.124 | 0.008 | 2 |
| 2 | 833 | 0.228 | 0.224 | 0.001 | 0.475 | 0.023 | 0.293 | 0.459 | 0.186 | 0.040 | 4 |
| 3 | 302 | 0.348 | 0.093 | 0.000 | 0.205 | 0.026 | 0.166 | 0.434 | 0.298 | 0.076 | 5 |
| 4 | 382 | 0.872 | 0.003 | 0.000 | 0.050 | 0.003 | 0.128 | 0.348 | 0.322 | 0.199 | 6 |

TEST-C (1,769 graded incidences, 120 proofs):

| grade | n | is_proof | is_prop | bare | logic_only | ar 0 | ar 1-2 | ar 3-5 | ar 6-9 | ar 10+ | med ar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 567 | 0.037 | 0.037 | 0.021 | 0.261 | 0.108 | 0.705 | 0.157 | 0.026 | 0.004 | 2 |
| 1 | 555 | 0.238 | 0.200 | 0.005 | 0.688 | 0.110 | 0.405 | 0.328 | 0.153 | 0.004 | 2 |
| 2 | 327 | 0.248 | 0.177 | 0.000 | 0.529 | 0.076 | 0.287 | 0.462 | 0.168 | 0.006 | 3 |
| 3 | 200 | 0.180 | 0.300 | 0.000 | 0.270 | 0.010 | 0.210 | 0.560 | 0.200 | 0.020 | 4 |
| 4 | 120 | 0.883 | 0.017 | 0.000 | 0.017 | 0.008 | 0.133 | 0.300 | 0.358 | 0.200 | 6 |

CAL (962 graded incidences, 72 proofs):

| grade | n | is_proof | is_prop | bare | logic_only | ar 0 | ar 1-2 | ar 3-5 | ar 6-9 | ar 10+ | med ar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 292 | 0.045 | 0.065 | 0.014 | 0.288 | 0.151 | 0.616 | 0.199 | 0.031 | 0.003 | 2 |
| 1 | 387 | 0.088 | 0.183 | 0.000 | 0.726 | 0.078 | 0.452 | 0.333 | 0.132 | 0.005 | 2 |
| 2 | 159 | 0.321 | 0.119 | 0.000 | 0.516 | 0.013 | 0.264 | 0.560 | 0.119 | 0.044 | 4 |
| 3 | 54 | 0.333 | 0.185 | 0.037 | 0.222 | 0.037 | 0.148 | 0.519 | 0.185 | 0.111 | 4 |
| 4 | 70 | 0.914 | 0.000 | 0.000 | 0.043 | 0.000 | 0.057 | 0.400 | 0.386 | 0.157 | 6 |
