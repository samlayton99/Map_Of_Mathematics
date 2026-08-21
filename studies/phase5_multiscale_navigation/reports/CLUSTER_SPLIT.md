# Adaptive per-proof cut (`cluster_split`)

**Headline: the adaptive methods that genuinely vary per proof are WORSE than fixed
top-k at the same mean view size. The two that beat it, beat it by about one
graded candidate out of 154 — inside the Wilson interval. `cluster_split` is a
defensible policy, not a demonstrated improvement over `top_k`.**

Code: `mathmap_eval/cluster_split.py`. Registered as the `cluster_split`
inclusion policy (the module must be imported for registration to take effect).
Default method: `tie_two`.

## The scalar

A ranking's score is a lexicographic key tuple, so break-finding needs a number
first. We use the **dense lexicographic level** of the key tuple over the whole
universe, normalised to [0,1]: `s = level_index / (n_levels - 1)`. It is
strictly monotone in the ranking's own order and preserves ties exactly. Key
columns are dense-coded and bit-packed into one int64 (lexsort fallback if the
tuple needs more than 62 bits). `scale="mass"` (share of the universe ranked
strictly ahead) is also implemented; it is uniformly worse and is not default.

Everything is segment arithmetic over the sorted-by-artifact record: one
lexsort plus `reduceat`. No Python loop over proofs. 18.1M candidates (U1D):
4.3 s to build the shared segment structure, 0.2–0.4 s per method after that.

## Methods tried

| method | rule |
|---|---|
| `tie_first` | first tie-block of the lexicographic key |
| `tie_first_capped` | ... capped at `min(8, ceil(L/2))` |
| `tie_two` | first two tie-blocks |
| `max_gap` | cut after the largest jump in the score sequence |
| `max_gap_half` | ... restricted to the first half of the proof |
| `max_gap_rel` | largest multiplicative jump `g_i / max(s_i, one level)` |
| `otsu` | 1-D two-class Otsu (identical to 2-class Jenks on sorted data) |
| `kneedle` | max normalised distance below the chord (convex branch) |
| `curvature` | max discrete second difference |

All guarantee `1 <= admitted <= proof size`. A fully tied proof admits
everything (`tied_all=True`): any prefix would be an arbitrary tie-break.

## Comparison

Universe U1D, 180 labelled proofs, 2419 graded candidates, 154 graded KEY.
Averaged over the five candidate rankings. `matched` = the fixed top-k curve
(k = 1..24) linearly interpolated to the method's own mean admitted size — the
only fair baseline, since a bigger view buys recall for free.

```
policy                     size  KeyRec  Prec>=3  Bad<=1  MeanG   | matched fixed-k at same size:
                                                                     KeyRec  Prec>=3  Bad<=1
--------------------------------------------------------------------------------------------------
top_k=1                    1.00   0.657    0.782   0.063   3.26
top_k=2                    2.00   0.862    0.588   0.200   2.67
top_k=4                    3.94   0.956    0.372   0.393   2.01
top_k=8                    7.32   0.996    0.226   0.533   1.55
tie_first                  1.04   0.671    0.774   0.069   3.23   |   0.665    0.773   0.070
tie_first_capped           1.04   0.671    0.774   0.069   3.23   |   0.665    0.773   0.070
tie_two                    2.16   0.882    0.568   0.220   2.61   |   0.873    0.567   0.220
max_gap_half               2.42   0.904    0.531   0.267   2.45   |   0.882    0.533   0.253
max_gap_rel                2.70   0.890    0.498   0.309   2.33   |   0.877    0.513   0.278
kneedle                    3.21   0.861    0.484   0.337   2.27   |   0.865    0.494   0.302
max_gap                    3.24   0.910    0.456   0.338   2.21   |   0.909    0.464   0.316
otsu                       3.88   0.929    0.410   0.378   2.06   |   0.939    0.413   0.359
curvature                  4.85   0.948    0.323   0.448   1.82   |   0.965    0.334   0.431
max_gap_rel[mass]          3.29   0.912    0.410   0.369   2.10   |   0.931    0.449   0.327
max_gap_half[mass]         3.68   0.958    0.394   0.378   2.04   |   0.949    0.398   0.369
otsu[mass]                 6.53   0.987    0.249   0.514   1.58   |   0.990    0.252   0.505
kneedle[mass]              7.02   0.969    0.225   0.558   1.47   |   0.992    0.240   0.519
max_gap[mass]              7.21   0.983    0.227   0.540   1.52   |   0.993    0.234   0.524
curvature[mass]            8.00   0.986    0.211   0.561   1.46   |   0.999    0.214   0.544
```

`size` = mean admitted per labelled proof. `KeyRec` = share of graded-KEY
admitted. `Prec>=3` = share of admitted graded candidates graded KEY or
SUPPORT. `Bad<=1` = share graded BAD_GLUE or JUNK. `MeanG` = mean grade of
admitted graded candidates.

Reading it:

- `otsu`, `kneedle`, `curvature` and every `[mass]` variant **lose** to matched
  fixed-k on KEY recall. The natural-breaks family does not work here.
- `max_gap` / `max_gap_rel` buy recall with junk: recall up, precision down,
  `Bad<=1` up. Net neutral at best.
- `max_gap_half` gains +2.2 pt recall at flat precision but +1.4 pt junk, and
  it is the most ranking-dependent method (below).
- `tie_first`, `tie_first_capped`, `tie_two` beat matched fixed-k on recall and
  precision, by 0.6–0.9 pt and 0.1 pt respectively.

Per candidate ranking (`beats_matched` = strictly better recall AND precision):

| method | R_depth | R_introduced_depth | R_phase5_composite | R_v8_all_kinds | R_v8_faithful |
|---|---|---|---|---|---|
| `tie_first`(_capped) | no | **yes** | tie | no | **yes** |
| `tie_two` | no (prec -0.002) | **yes** | tie | **yes** | **yes** |
| `max_gap_half` | no | no | **yes** | **yes** | no |
| `max_gap` | no | no | **yes** | no | no |
| `otsu` | no | no | **yes** | no | no |
| `kneedle` | **yes** | no | **yes** | no | no |
| `curvature` | no | **yes** | no | no | no |

## Chosen default: `tie_two`

1. It is the only method whose KEY recall is >= the matched fixed-k baseline
   for **every** candidate ranking, at flat precision.
2. It never breaks a tie arbitrarily. Cutting inside a tie-block means the
   displayed list depends on a stable-ID tie-break, which is reproducible but
   meaningless (the standing audit position on ties).
3. It sits at a mean size of ~2.2, the region where "how many real moves does
   this proof have" is genuinely uncertain — top-1 is too tight for multi-move
   proofs and top-4 is mostly plumbing (precision 0.372).

## How it fails

- **The win is not resolvable.** +0.9 pt KEY recall on n = 154 graded KEY is
  ~1.4 candidates; the Wilson half-width at p = 0.88, n = 154 is ±5.1 pt. Do
  not quote `cluster_split` as better than `top_k=2`.
- **It barely adapts.** Corpus-wide over U1D, `tie_two` admits exactly 2 in the
  large majority of proofs; p90 = 3, p99 = 6, max 65. The tie-block idea is
  principled but the rankings' last key (cited depth, 346 distinct values)
  breaks nearly every tie, so there is little tie structure left to exploit.
  `tie_first` is worse in this respect: it admits exactly 1 in 90–98% of
  proofs, i.e. it is `top_k=1` wearing a different name.

  Mean / p90 / p99 / max admitted per proof, U1D, whole corpus:

  | ranking | `tie_first` | `tie_two` | `max_gap_half` |
  |---|---|---|---|
  | R_depth | 1.15 / 1 / 3 / 64 | 2.42 / 3 / 7 / 65 | 3.36 / 7 / 21 / 112 |
  | R_introduced_depth | 1.12 / 1 / 3 / 64 | 2.32 / 3 / 6 / 65 | 3.77 / 8 / 26 / 212 |
  | R_phase5_composite | 1.04 / 1 / 2 / 64 | 2.04 / 2 / 4 / 65 | 2.57 / 5 / 17 / 186 |
  | R_v8_all_kinds | 1.10 / 1 / 3 / 64 | 2.28 / 3 / 6 / 65 | 4.38 / 10 / 29 / 187 |
  | R_v8_faithful | 1.10 / 1 / 3 / 63 | 2.26 / 3 / 6 / 65 | 4.31 / 10 / 31 / 296 |

  The genuinely adaptive method is `max_gap_half` (35–55% of proofs get one
  item, 27–47% get three or more) — and that is exactly the method the labels
  do not support.
- **Uncapped.** A proof whose ranking cannot separate 65 candidates gets all 65.
  That is the honest reading of a tie, but it makes the view size long-tailed.
  `cap_abs` / `cap_frac` exist and are used by `tie_first_capped`; `tie_two` does
  not use them.
- **Ranking-dependent by construction.** `tie_two` on a ranking with a
  continuous score (R_phase5_composite) is exactly `top_k=2`. It only does
  something different when the ranking has genuine ties, so it cannot rescue a
  ranking that over-discriminates.
- **Measured on 180 proofs.** All of the above is Channel B; n is small and only
  U1D contains every graded candidate (U1 holds 989 of 2419).

## Reproducing

```python
from mathmap_eval import cluster_split as CS
res = CS.evaluate_methods(universe="U1D", scales=("level", "mass"))
print(res["table"])
```

Runtime ~3 min over all 10 rankings.
