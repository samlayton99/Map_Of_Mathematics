# Conditional structure: regimes, trees, cascades, semiorders

Family premise: the signals are not symmetric. Role tier behaves like a
near-deterministic filter, depth and rarity like graded evidence. So role should
*condition* the ordering rather than vote in it.

Everything here is reproduced by `src/scheme_conditional.py`
(`battery | tiers | escape | tree | sweep | gradient | bands | nav | regimes | all`).

## Headline answers

1. **Per-tier secondary signals do NOT genuinely differ.** Frozen rarity, or the
   depth+rarity Borda, is best-or-tied inside every tier on every split. The one
   apparent exception (tier 2 prefers `arity` on TEST-R) does not replicate.
2. **The escape hatch does rescue lexicographic, decisively.** Pure lex: P@1
   0.836, KeyMove@1 0.500, 58 precision failures. A one-tier jump for
   `rarity >= 8`: P@1 0.983, KeyMove@1 0.831, 5 precision failures. The jump
   crosses a real tier boundary at rank 1 in 165/360 TEST-R proofs and turns a
   defect into a useful item 55 times against 2 breakages.
3. **Most of lexicographic's damage is over-resolution, not hardness.** Merging
   the 5 tiers into 3 (`{4,3} {2,1} {0}`) recovers P@1 0.836 -> 0.972 with no
   escape at all. The tier signal carries roughly one bit and a bit, not five levels.
4. Every gain comes with a loss. See the trades at the bottom; nothing here
   dominates the Borda reference outright.

## Reproduction caveat, stated up front

The scripts that produced the quoted reference numbers were not committed
(commit 72959d3 added only `battery.py`). This harness reproduces the quoted
pure-lexicographic result **exactly** (KeyMove@1 0.500, 58 precision failures vs
8), which is the check that matters, but the two positive references are
re-implemented, not recovered:

| reference | quoted | re-implemented here |
|---|---|---|
| weighted decimal model | P@1 0.975, P@4 0.712, KM@1 0.825, core@4 0.974, pf 8 | `role{1.0/0.7/0.5} x frozen rarity`: P@1 0.975, P@4 0.679, KM@1 0.825, core@4 0.963, pf 8 |
| Borda | P@1 0.975, KM@1 0.864, P@4 0.663 | `Borda(tier,depth,rarity,not-in-stmt)`, average ranks: P@1 0.975, KM@1 0.872, P@4 0.693 |

P@1, KeyMove@1 and the precision-failure count line up; P@4 and core@4 differ by
0.02-0.03, presumably a tie-handling or transform detail. **All comparisons below
are against the re-implemented references measured in the same harness**, so they
are internally consistent. Read the quoted numbers as approximate.

## Signals and every constant

Signals (all append-safe, no name matching):

- `tier` — ordinal 0-4 from the strongest role present in the proof term.
  `4` applied, `3` let-value or explicit-arg, `2` implicit-arg or
  strict-implicit, `1` type-annotation or unresolved, `0` instance-slot.
- `depth` — `inc_d_cite`, integer.
- `rarity` — frozen IDF over the pinned depth<=50 foundation, as in
  `src/mine_failures.py`.
- `in_stmt`, `arity`, `is_proof`, `is_prop` — booleans / kernel integers.
- `ev-rank` — within-proof rank of `rank(depth) + rank(rarity)`; 1 = strongest
  evidence in this proof. Proof-local, hence append-safe.

Constants, complete list. All integers, all stated:

| constant | value | meaning |
|---|---|---|
| frozen foundation depth | 50 | pinned rarity table (inherited, not fitted here) |
| escape rarity | 8 | nats of frozen rarity that buy a one-tier jump |
| escape ev-rank | 2 | alternative escape: top-2 evidence item in the proof |
| tier merge map | {4,3}->2, {2,1}->1, {0}->0 | integer coarsening |
| tree max depth | 3 | interpretability cap |
| tree min leaf | 100 | candidates per leaf |
| cascade rarity gates | 8, 10 | integer thresholds inside cascade predicates |

The reference weighted model's decimals (1.0 / 0.7 / 0.5) appear only in the
comparator, never in a scheme proposed here.

## 1. Per-tier evidence — does each tier want a different secondary signal?

Concordance `C` over pairs that are (same proof, same tier, different grade) —
exactly the pairs a within-tier secondary ordering decides. `C = 0.5` is chance.

| tier | split | pairs | rarity | borda(d,r) | depth | arity | is_prop |
|---|---|---|---|---|---|---|---|
| 4 | TEST-R | **1** | 1.000 | 1.000 | 0.500 | 1.000 | 0.500 |
| 4 | CAL / TEST-C | **0** | — | — | — | — | — |
| 3 | TEST-R | 4335 | **0.866** | 0.855 | 0.773 | 0.608 | 0.466 |
| 3 | CAL | 1075 | 0.832 | **0.850** | 0.798 | 0.639 | 0.441 |
| 3 | TEST-C | 2095 | **0.846** | 0.814 | 0.703 | 0.573 | 0.473 |
| 2 | TEST-R | 319 | 0.749 | 0.776 | 0.718 | **0.799** | 0.511 |
| 2 | CAL | 83 | 0.801 | **0.843** | 0.753 | 0.789 | 0.470 |
| 2 | TEST-C | 160 | **0.806** | 0.778 | 0.656 | 0.675 | 0.463 |
| 1 | TEST-R | 520 | 0.833 | **0.838** | 0.822 | 0.801 | 0.759 |
| 1 | CAL | 55 | **0.827** | 0.818 | 0.782 | 0.791 | 0.755 |
| 1 | TEST-C | 236 | 0.852 | **0.881** | 0.873 | 0.869 | 0.756 |
| 0 | TEST-R | 381 | 0.883 | **0.909** | 0.827 | 0.612 | 0.500 |
| 0 | CAL | 99 | 0.879 | **0.914** | 0.864 | 0.778 | 0.500 |
| 0 | TEST-C | 110 | 0.805 | **0.818** | 0.791 | 0.527 | 0.500 |

Read-out:

- **Tier 4 has essentially no within-tier decisions.** `applied` is the head of
  the proof term; there is at most one per proof. One decidable pair on TEST-R,
  zero on CAL and TEST-C. Any claim about "what the applied tier wants" is
  unmeasurable. More generally, **the highest occupied tier of a proof is a
  singleton in 539 of 552 proofs (97.6%)** — which is why a tier primary decides
  rank 1 on its own and no secondary signal can rescue it.
- **Rarity or the depth+rarity Borda is top-or-within-noise in every tier on
  every split.** The two are within 0.03 of each other everywhere.
- **Depth is never the best signal in any tier**, and its deficit is largest
  exactly where the pairs are (tier 3: 0.773 vs rarity's 0.866).
- The one genuine-looking difference — tier 2 wanting `arity` (0.799 vs rarity
  0.749 on TEST-R) — **fails to replicate**: CAL 0.789 vs 0.801, TEST-C 0.675 vs
  0.806. It is a 319-pair artefact.

**Verdict: no. Conditioning the secondary signal on the tier buys nothing.** The
scheme `C1d` that does exactly that (per-tier fitted signal) is indistinguishable
from `C1a` (rarity everywhere) at rank 1, and differs by 0.004 in P@4.

## 2. The schemes, as rules

**C1 role-conditioned ordering.** `sort by tier descending; within a tier by <signal>`.
Variants: rarity (C1a), depth (C1b), borda(depth,rarity) (C1c), per-tier fitted
signal (C1d: tier 4/3 rarity, tier 2 arity, tier 1/0 borda).

**C2 tier coarsening.** `sort by merged tier descending; within by ev-rank`.
C2a merges `{4,3} {2,1} {0}`; C2b `{4,3} {2,1,0}`; C2c `{4,3,2,1} {0}`.

**C3 semiorder / lexicographic with escape.**
```
effective_tier = tier + 1  if <escape predicate>  else tier
sort by effective_tier descending, then by ev-rank ascending
```
Escape predicates tested: `ev-rank <= 1 / 2 / 3`, `rarity >= 8`,
`rarity >= 8 and tier >= 1`, `rarity >= 8 and is_proof`, and a two-tier jump.

**C4 cascade.** First matching predicate assigns the class; unmatched fall to the
bottom class; within class order by ev-rank.
```
C4a  1: tier>=3 and rarity>=8      C4b  1: tier>=3 and rarity>=8 and not in_stmt
     2: tier>=3                         2: tier>=3
     3: tier>=1 and rarity>=10           3: tier>=1 and rarity>=10
     4: tier==2                         4: everything else
     5: tier==1
     6: everything else
```

**C5 decision tree** (section 4). **C6** = C2a's merged tiers plus C3's
`rarity>=8` escape. **C7** = tree class plus the same escape.

## 3. Full battery, all three splits

TEST-R 360 proofs (fitting split), CAL 72, TEST-C 120. `inv` = gradient
inversions over 10 equal-mass position bins; `pf/rf/gf` = precision / recall /
gradient failure counts from `battery.failures`.

| scheme | split | P@1 | P@4 | KeyMove@1 | core@4 | major@4 | useful@4 | monotone | inv | prec fail | rec fail | grad fail |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF-W  role x frozen rarity | TEST-R | 0.975 | 0.679 | 0.825 | 0.963 | 0.864 | 0.641 | True | 0 | 8 | 6 | 1 |
| REF-W  role x frozen rarity | CAL | 0.903 | 0.632 | 0.722 | 0.943 | 0.839 | 0.636 | False | 2 | 7 | 1 | 0 |
| REF-W  role x frozen rarity | TEST-C | 0.850 | 0.713 | 0.675 | 0.975 | 0.766 | 0.526 | False | 1 | 18 | 0 | 3 |
| REF-B  Borda tier+depth+rarity+stmt | TEST-R | 0.975 | 0.693 | 0.872 | 0.982 | 0.892 | 0.655 | True | 0 | 8 | 4 | 0 |
| REF-B  Borda tier+depth+rarity+stmt | CAL | 0.944 | 0.670 | 0.833 | 1.000 | 0.863 | 0.675 | True | 0 | 4 | 0 | 0 |
| REF-B  Borda tier+depth+rarity+stmt | TEST-C | 0.842 | 0.719 | 0.750 | 0.983 | 0.753 | 0.530 | True | 0 | 19 | 0 | 2 |
| REF-LEX tier -> rarity | TEST-R | 0.836 | 0.689 | 0.500 | 0.961 | 0.822 | 0.651 | True | 0 | 58 | 2 | 0 |
| REF-LEX tier -> rarity | CAL | 0.806 | 0.663 | 0.375 | 0.914 | 0.798 | 0.668 | True | 0 | 14 | 2 | 0 |
| REF-LEX tier -> rarity | TEST-C | 0.742 | 0.721 | 0.350 | 0.917 | 0.681 | 0.532 | False | 2 | 31 | 1 | 1 |
| C1a tier -> rarity | TEST-R | 0.836 | 0.689 | 0.500 | 0.961 | 0.822 | 0.651 | True | 0 | 58 | 2 | 0 |
| C1a tier -> rarity | CAL | 0.806 | 0.663 | 0.375 | 0.914 | 0.798 | 0.668 | True | 0 | 14 | 2 | 0 |
| C1a tier -> rarity | TEST-C | 0.742 | 0.721 | 0.350 | 0.917 | 0.681 | 0.532 | False | 2 | 31 | 1 | 1 |
| C1b tier -> depth | TEST-R | 0.836 | 0.678 | 0.500 | 0.948 | 0.816 | 0.640 | True | 0 | 58 | 4 | 0 |
| C1b tier -> depth | CAL | 0.806 | 0.656 | 0.375 | 0.929 | 0.774 | 0.661 | True | 0 | 14 | 2 | 0 |
| C1b tier -> depth | TEST-C | 0.742 | 0.702 | 0.350 | 0.942 | 0.678 | 0.518 | True | 0 | 31 | 0 | 2 |
| C1c tier -> borda(depth,rarity) | TEST-R | 0.836 | 0.691 | 0.500 | 0.969 | 0.841 | 0.653 | True | 0 | 58 | 1 | 0 |
| C1c tier -> borda(depth,rarity) | CAL | 0.806 | 0.667 | 0.375 | 0.943 | 0.798 | 0.671 | False | 1 | 14 | 1 | 0 |
| C1c tier -> borda(depth,rarity) | TEST-C | 0.742 | 0.715 | 0.350 | 0.950 | 0.681 | 0.527 | False | 1 | 31 | 0 | 1 |
| C1d tier -> per-tier signal | TEST-R | 0.836 | 0.693 | 0.500 | 0.958 | 0.819 | 0.655 | True | 0 | 58 | 3 | 0 |
| C1d tier -> per-tier signal | CAL | 0.806 | 0.663 | 0.375 | 0.914 | 0.798 | 0.668 | False | 1 | 14 | 2 | 0 |
| C1d tier -> per-tier signal | TEST-C | 0.742 | 0.715 | 0.350 | 0.917 | 0.678 | 0.527 | False | 1 | 31 | 1 | 1 |
| C2a merge {4,3}{2,1}{0} | TEST-R | 0.972 | 0.707 | 0.850 | 0.979 | 0.868 | 0.668 | True | 0 | 9 | 1 | 0 |
| C2a merge {4,3}{2,1}{0} | CAL | 0.917 | 0.660 | 0.819 | 0.943 | 0.831 | 0.664 | True | 0 | 6 | 1 | 0 |
| C2a merge {4,3}{2,1}{0} | TEST-C | 0.858 | 0.746 | 0.725 | 0.942 | 0.756 | 0.550 | False | 1 | 17 | 1 | 1 |
| C2b merge {4,3}{2,1,0} | TEST-R | 0.972 | 0.705 | 0.850 | 0.976 | 0.882 | 0.665 | True | 0 | 9 | 2 | 0 |
| C2b merge {4,3}{2,1,0} | CAL | 0.917 | 0.653 | 0.819 | 0.957 | 0.839 | 0.657 | False | 1 | 6 | 0 | 0 |
| C2b merge {4,3}{2,1,0} | TEST-C | 0.858 | 0.727 | 0.725 | 0.950 | 0.756 | 0.536 | False | 1 | 17 | 1 | 1 |
| C2c merge {4,3,2,1}{0} | TEST-R | 0.967 | 0.698 | 0.842 | 0.955 | 0.851 | 0.659 | True | 0 | 11 | 7 | 1 |
| C2c merge {4,3,2,1}{0} | CAL | 0.944 | 0.649 | 0.847 | 0.929 | 0.823 | 0.654 | False | 1 | 4 | 1 | 0 |
| C2c merge {4,3,2,1}{0} | TEST-C | 0.850 | 0.744 | 0.767 | 0.950 | 0.784 | 0.549 | True | 0 | 18 | 1 | 1 |
| C3a escape ev-rank<=1 | TEST-R | 0.967 | 0.696 | 0.806 | 0.969 | 0.851 | 0.657 | True | 0 | 11 | 1 | 0 |
| C3a escape ev-rank<=1 | CAL | 0.972 | 0.670 | 0.833 | 0.943 | 0.806 | 0.675 | True | 0 | 2 | 1 | 0 |
| C3a escape ev-rank<=1 | TEST-C | 0.858 | 0.719 | 0.708 | 0.950 | 0.688 | 0.530 | False | 1 | 17 | 0 | 1 |
| C3b escape ev-rank<=2 | TEST-R | 0.981 | 0.700 | 0.842 | 0.963 | 0.852 | 0.661 | True | 0 | 6 | 1 | 0 |
| C3b escape ev-rank<=2 | CAL | 0.958 | 0.670 | 0.764 | 0.943 | 0.798 | 0.675 | True | 0 | 3 | 1 | 0 |
| C3b escape ev-rank<=2 | TEST-C | 0.858 | 0.719 | 0.692 | 0.950 | 0.694 | 0.530 | True | 0 | 17 | 0 | 1 |
| C3c escape ev-rank<=3 | TEST-R | 0.975 | 0.706 | 0.847 | 0.966 | 0.855 | 0.666 | False | 1 | 8 | 1 | 0 |
| C3c escape ev-rank<=3 | CAL | 0.931 | 0.677 | 0.722 | 0.943 | 0.806 | 0.682 | True | 0 | 5 | 1 | 0 |
| C3c escape ev-rank<=3 | TEST-C | 0.858 | 0.721 | 0.675 | 0.950 | 0.706 | 0.532 | True | 0 | 17 | 0 | 1 |
| C3d escape rarity>=8 | TEST-R | 0.983 | 0.718 | 0.831 | 0.984 | 0.864 | 0.678 | False | 1 | 5 | 1 | 0 |
| C3d escape rarity>=8 | CAL | 0.944 | 0.688 | 0.778 | 0.957 | 0.823 | 0.693 | False | 2 | 4 | 1 | 0 |
| C3d escape rarity>=8 | TEST-C | 0.867 | 0.746 | 0.683 | 0.950 | 0.744 | 0.550 | True | 0 | 16 | 0 | 1 |
| **C3e escape rarity>=8 & tier>=1** | TEST-R | 0.983 | 0.716 | 0.831 | 0.984 | 0.860 | 0.676 | True | 0 | 5 | 1 | 0 |
| **C3e escape rarity>=8 & tier>=1** | CAL | 0.944 | 0.688 | 0.778 | 0.957 | 0.823 | 0.693 | True | 0 | 4 | 1 | 0 |
| **C3e escape rarity>=8 & tier>=1** | TEST-C | 0.867 | 0.742 | 0.683 | 0.950 | 0.738 | 0.547 | True | 0 | 16 | 0 | 1 |
| C3f escape rarity>=8 & is_proof | TEST-R | 0.983 | 0.691 | 0.717 | 0.979 | 0.851 | 0.653 | True | 0 | 5 | 1 | 0 |
| C3f escape rarity>=8 & is_proof | CAL | 0.944 | 0.667 | 0.694 | 0.971 | 0.823 | 0.671 | False | 1 | 4 | 1 | 0 |
| C3f escape rarity>=8 & is_proof | TEST-C | 0.842 | 0.717 | 0.608 | 0.967 | 0.681 | 0.529 | True | 0 | 19 | 0 | 1 |
| C3g escape two tiers, ev-rank<=1 | TEST-R | 0.961 | 0.699 | 0.822 | 0.963 | 0.857 | 0.660 | True | 0 | 13 | 3 | 0 |
| C3g escape two tiers, ev-rank<=1 | CAL | 0.958 | 0.670 | 0.861 | 0.957 | 0.815 | 0.675 | True | 0 | 3 | 0 | 0 |
| C3g escape two tiers, ev-rank<=1 | TEST-C | 0.858 | 0.719 | 0.742 | 0.950 | 0.691 | 0.530 | False | 1 | 17 | 0 | 1 |
| C4a cascade 6-class | TEST-R | 0.972 | 0.705 | 0.853 | 0.979 | 0.865 | 0.665 | False | 1 | 9 | 1 | 0 |
| C4a cascade 6-class | CAL | 0.917 | 0.656 | 0.819 | 0.943 | 0.831 | 0.661 | True | 0 | 6 | 1 | 0 |
| C4a cascade 6-class | TEST-C | 0.858 | 0.748 | 0.725 | 0.942 | 0.747 | 0.552 | True | 0 | 17 | 1 | 1 |
| C4b cascade 4-class | TEST-R | 0.972 | 0.703 | 0.875 | 0.976 | 0.882 | 0.663 | True | 0 | 9 | 2 | 0 |
| C4b cascade 4-class | CAL | 0.917 | 0.656 | 0.847 | 0.986 | 0.863 | 0.661 | False | 1 | 6 | 0 | 0 |
| C4b cascade 4-class | TEST-C | 0.858 | 0.730 | 0.733 | 0.967 | 0.747 | 0.538 | True | 0 | 17 | 1 | 1 |
| C5  tree d3 -> rarity+depth | TEST-R | 0.969 | 0.700 | 0.881 | 0.963 | 0.857 | 0.661 | True | 0 | 10 | 6 | 0 |
| C5  tree d3 -> rarity+depth | CAL | 0.958 | 0.656 | 0.889 | 0.943 | 0.855 | 0.661 | True | 0 | 3 | 2 | 0 |
| C5  tree d3 -> rarity+depth | TEST-C | 0.850 | 0.748 | 0.775 | 0.967 | 0.784 | 0.552 | True | 0 | 18 | 1 | 1 |
| C5b tree d3 -> rarity | TEST-R | 0.950 | 0.691 | 0.817 | 0.953 | 0.841 | 0.653 | False | 1 | 17 | 7 | 0 |
| C5b tree d3 -> rarity | CAL | 0.931 | 0.642 | 0.750 | 0.957 | 0.855 | 0.647 | True | 0 | 5 | 2 | 0 |
| C5b tree d3 -> rarity | TEST-C | 0.842 | 0.751 | 0.717 | 0.958 | 0.775 | 0.553 | True | 0 | 19 | 2 | 1 |
| **C6  merge{4,3}{2,1}{0} + escape rarity>=8** | TEST-R | 0.975 | 0.706 | 0.867 | 0.974 | 0.867 | 0.666 | True | 0 | 8 | 3 | 0 |
| **C6  merge{4,3}{2,1}{0} + escape rarity>=8** | CAL | 0.931 | 0.677 | 0.861 | 0.943 | 0.847 | 0.682 | True | 0 | 5 | 1 | 0 |
| **C6  merge{4,3}{2,1}{0} + escape rarity>=8** | TEST-C | 0.850 | 0.757 | 0.758 | 0.942 | 0.769 | 0.558 | True | 0 | 18 | 1 | 1 |
| C7  tree class + escape rarity>=8 | TEST-R | 0.969 | 0.698 | 0.878 | 0.963 | 0.855 | 0.659 | True | 0 | 10 | 6 | 0 |
| C7  tree class + escape rarity>=8 | CAL | 0.958 | 0.649 | 0.889 | 0.943 | 0.855 | 0.654 | True | 0 | 3 | 2 | 0 |
| C7  tree class + escape rarity>=8 | TEST-C | 0.850 | 0.751 | 0.775 | 0.967 | 0.775 | 0.553 | True | 0 | 18 | 1 | 1 |

Scale: TEST-R has 360 proofs, so 0.003 in P@1 or KeyMove@1 is one proof. CAL has
72 (0.014 per proof) and TEST-C 120 (0.008 per proof). Differences below about
0.02 on CAL should not be read as real.

## 4. The tree, in full

Fitted on TEST-R only. Regression on the median grade, max depth 3, min leaf 100,
splits restricted to `feature <= integer` (booleans are `<= 0`). Rarity is real
valued but only integer thresholds were offered. Leaf means are shown to justify
the class ORDER; the deployed rule is the integer order, not the means.

```
class 1: tier > 0 and rarity > 9 and in_stmt <= 0      n=403   mean grade 3.61
class 2: tier > 0 and rarity > 9 and in_stmt >  0      n=459   mean grade 2.11
class 3: tier > 0 and rarity <= 9 and depth > 0        n=1840  mean grade 1.37
class 4: tier > 0 and rarity <= 9 and depth <= 0       n=903   mean grade 0.91
class 5: tier <= 0 and rarity > 8 and rarity <= 12     n=107   mean grade 0.62
class 6: tier <= 0 and rarity > 12                     n=153   mean grade 0.39
class 7: tier <= 0 and rarity <= 8 and depth > 6       n=266   mean grade 0.15
class 8: tier <= 0 and rarity <= 8 and depth <= 6      n=669   mean grade 0.03
within class: order by rank(rarity) + rank(depth)
```

Two things the tree says that matter more than its score:

- **Its root is `tier > 0`, not the 5-level tier.** With eight leaves to spend it
  never buys a second tier split. The instance-slot/everything-else boundary is
  the only part of the role signal that pays.
- **`in_stmt` splits the top class in two** (3.61 vs 2.11): among tier>0, very
  rare citations, the ones the proof *introduces* are the content and the ones
  already implied by the statement are plumbing.

Class-order transfer (mean grade per class, per split):

| split | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 |
|---|---|---|---|---|---|---|---|---|
| TEST-R | 3.61 | 2.11 | 1.37 | 0.91 | 0.62 | 0.39 | 0.15 | 0.03 |
| CAL | 3.61 | 1.65 | 1.38 | 0.89 | 0.47 | **0.50** | 0.17 | 0.04 |
| TEST-C | 3.16 | 2.38 | 1.51 | 0.92 | 0.33 | **0.40** | 0.04 | 0.04 |

The fitted order holds out of sample everywhere except the c5/c6 pair, which
inverts on both held-out splits — the rarity>12 vs 8-12 distinction inside
instance-slot is noise (n=107 and 153 on the fitting split).

Refits, as an overfitting check:

- Fit on TEST-C (min leaf 50): same shape — `tier > 0`, then `rarity > 7`, then
  depth. Agrees with the TEST-R tree up to the rarity threshold moving 9 -> 7.
- Fit on CAL (min leaf 30, 1,099 candidates): splits on `in_stmt` at the root
  instead, then `rarity > 7`, then `arity > 4`. Different root, same vocabulary.
- Fit on TEST-R with min leaf 300: top four classes identical; only the
  instance-slot subtree changes.

So the recurring predicates — `tier > 0`, `rarity > 7..9`, `depth > 0`,
`in_stmt` — are stable; the exact thresholds and the bottom of the tree are not.

## 5. Does the escape hatch actually escape?

Escape predicate `rarity >= 8 and tier >= 1`. It is selective *within* every
tier, which is what licenses it as an override rather than a re-weighting.
P(useful | fires) vs P(useful | does not), same tier:

| split | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|
| TEST-R | 0.48 vs 0.09 | 0.60 vs 0.15 | 0.91 vs 0.32 | 0.99 vs 0.70 |
| CAL | 0.39 vs 0.06 | 0.50 vs 0.11 | 0.79 vs 0.30 | 1.00 vs 0.70 |
| TEST-C | 0.64 vs 0.21 | 0.82 vs 0.23 | 0.86 vs 0.40 | 0.92 vs 0.60 |

What it does at rank 1, against pure lexicographic:

| split | proofs | rank-1 crossed a tier | defect -> useful | useful -> defect |
|---|---|---|---|---|
| TEST-R | 360 | 165 | 55 | 2 |
| CAL | 72 | 38 | 13 | 3 |
| TEST-C | 120 | 57 | 19 | 4 |

The jump is real (it changes which tier rank 1 comes from in ~46% of proofs) and
the trade is 27:1 favourable on TEST-R, 4-5:1 on the held-out splits.

Threshold sweep — the escape constant is a plateau, not a knife edge:

| rarity >= | TEST-R P@1 / P@4 / KM | CAL P@1 / P@4 / KM | TEST-C P@1 / P@4 / KM |
|---|---|---|---|
| 5 | 0.981 / 0.712 / 0.822 | 0.931 / 0.684 / 0.750 | 0.883 / 0.759 / 0.675 |
| 6 | 0.981 / 0.716 / 0.822 | 0.944 / 0.691 / 0.764 | 0.883 / 0.757 / 0.675 |
| 7 | 0.981 / 0.714 / 0.819 | 0.944 / 0.684 / 0.764 | 0.867 / 0.757 / 0.692 |
| **8** | **0.983 / 0.716 / 0.831** | 0.944 / 0.688 / 0.778 | 0.867 / 0.742 / 0.683 |
| 9 | 0.981 / 0.712 / 0.825 | 0.944 / 0.677 / 0.750 | 0.858 / 0.740 / 0.692 |
| 10 | 0.972 / 0.707 / 0.811 | 0.944 / 0.670 / 0.722 | 0.842 / 0.736 / 0.675 |
| 11 | 0.953 / 0.705 / 0.789 | 0.931 / 0.667 / 0.694 | 0.833 / 0.734 / 0.633 |
| 12 | 0.942 / 0.704 / 0.756 | 0.903 / 0.667 / 0.667 | 0.817 / 0.734 / 0.600 |

5-9 is flat; the scheme only degrades past 10, where the predicate stops firing.
Honestly: 8 is the TEST-R argmax, and 5-6 would be picked on the held-out splits.
All three sit inside the plateau, so the choice is not load bearing, but the
constant *was* fitted on TEST-R and should be read that way.

## 6. Gradient

P(useful) over 10 equal-mass within-proof position bins.

| scheme | split | bin rates | inversions |
|---|---|---|---|
| REF-W | TEST-R | 0.94 0.65 0.49 0.33 0.25 0.15 0.12 0.10 0.07 0.06 | 0 |
| REF-W | CAL | 0.87 0.64 0.38 0.30 0.22 0.17 0.19 0.03 0.08 0.06 | 2 |
| REF-W | TEST-C | 0.83 0.75 0.59 0.47 0.28 0.27 0.18 0.15 0.07 0.07 | 1 |
| REF-B | TEST-R | 0.93 0.68 0.49 0.34 0.29 0.19 0.14 0.06 0.03 0.01 | 0 |
| REF-B | CAL | 0.91 0.69 0.38 0.28 0.21 0.20 0.16 0.06 0.05 0.00 | 0 |
| REF-B | TEST-C | 0.82 0.72 0.54 0.46 0.34 0.25 0.23 0.15 0.08 0.06 | 0 |
| REF-LEX | TEST-C | 0.76 0.80 0.66 0.45 0.31 0.23 0.17 0.18 0.07 0.03 | 2 |
| C2a | TEST-C | 0.85 0.77 0.62 0.37 0.37 0.28 0.21 0.10 0.06 0.03 | 1 |
| C3e | TEST-R | 0.94 0.73 0.54 0.33 0.26 0.16 0.07 0.07 0.04 0.02 | 0 |
| C3e | CAL | 0.91 0.70 0.42 0.29 0.20 0.18 0.09 0.06 0.05 0.03 | 0 |
| C3e | TEST-C | 0.85 0.75 0.61 0.47 0.33 0.25 0.19 0.12 0.06 0.03 | 0 |
| C5 | TEST-R | 0.94 0.69 0.50 0.35 0.28 0.19 0.08 0.07 0.04 0.02 | 0 |
| C5 | CAL | 0.89 0.66 0.36 0.35 0.26 0.19 0.08 0.07 0.03 0.03 | 0 |
| C5 | TEST-C | 0.82 0.80 0.67 0.46 0.37 0.22 0.18 0.07 0.05 0.03 | 0 |
| C6 | TEST-R | 0.94 0.72 0.50 0.35 0.30 0.14 0.08 0.07 0.03 0.03 | 0 |
| C6 | CAL | 0.87 0.70 0.40 0.32 0.23 0.18 0.11 0.05 0.05 0.02 | 0 |
| C6 | TEST-C | 0.84 0.76 0.71 0.42 0.32 0.25 0.17 0.08 0.06 0.03 | 0 |

C3e, C5, C6 and C7 are monotone on all three splits — the only schemes here that
are, and better than both references (REF-W is non-monotone on CAL and TEST-C).
`REF-LEX`, `C2a`, `C2b`, `C4a` and `C3d` each break monotonicity somewhere.
Note that the `& tier >= 1` guard on the escape is what fixes `C3d`'s inversions:
promoting instance-slot candidates on rarity alone re-injects junk mid-list.

## 7. Navigability, whole corpus, k = 4

Junk proxy: not-a-proof AND arity <= 2 (the append-safe kernel proxy used in the
committed result).

| scheme | junk edge share | giant | giant without junk | retained |
|---|---|---|---|---|
| REF-W role x frozen rarity | 0.293 | 1.000 | 0.945 | 0.945 |
| REF-B Borda | 0.248 | 1.000 | 0.956 | 0.956 |
| REF-LEX tier -> rarity | 0.243 | 1.000 | 0.958 | 0.958 |
| C2a merge {4,3}{2,1}{0} | 0.230 | 1.000 | 0.956 | 0.956 |
| C3e escape rarity>=8 & tier>=1 | 0.231 | 1.000 | 0.956 | 0.956 |
| C6 merge + escape | 0.238 | 1.000 | 0.954 | 0.954 |

Reproduces the committed finding: navigability barely discriminates (0.945-0.958
across everything, including the worst per-proof ranking) and is mildly
*anti*-correlated with per-proof quality. The conditional schemes do cut the junk
edge share (0.293 -> 0.231, against 0.230 for C2a and 0.248 for Borda), which is a real
if small win: fewer machinery edges enter the top-4 graph at all.

## 8. By target depth (TEST-R)

| scheme | 0-10 | 11-25 | 26-50 | 51-75 | 76-125 | 126+ |
|---|---|---|---|---|---|---|
| REF-W P@1 | 0.983 | 0.983 | 0.950 | 1.000 | 0.967 | 0.967 |
| REF-B P@1 | 0.950 | 0.983 | 0.950 | 1.000 | 0.983 | 0.983 |
| REF-LEX P@1 | 0.850 | 0.783 | 0.783 | 0.867 | 0.883 | 0.850 |
| C3e P@1 | 0.967 | 0.983 | 0.967 | 1.000 | 1.000 | 0.983 |
| C5 P@1 | 0.933 | 0.967 | 0.967 | 0.967 | 0.983 | 1.000 |
| C3e P@4 | 0.624 | 0.736 | 0.741 | 0.683 | 0.754 | 0.754 |
| REF-B P@4 | 0.645 | 0.741 | 0.707 | 0.675 | 0.692 | 0.700 |

C3e's advantage over the references is concentrated in deep targets (76+), where
it gains 0.06 P@4; it loses 0.02 P@4 at the shallowest band. n = 60 per band, so
each band's P@1 moves 0.017 per proof.

## 9. Verdict

**Best two.**

`C3e` — lexicographic on role tier with a one-tier escape for
`rarity >= 8 and tier >= 1`, ties by depth+rarity Borda rank:

```
TEST-R  P@1 0.983  P@4 0.716  KeyMove@1 0.831  core@4 0.984  major@4 0.860
        useful@4 0.676  monotone (0 inv)  failures: prec 5, recall 1, grad 0
CAL     P@1 0.944  P@4 0.688  KeyMove@1 0.778  core@4 0.957  major@4 0.823
        useful@4 0.693  monotone (0 inv)  failures: prec 4, recall 1, grad 0
TEST-C  P@1 0.867  P@4 0.742  KeyMove@1 0.683  core@4 0.950  major@4 0.738
        useful@4 0.547  monotone (0 inv)  failures: prec 16, recall 0, grad 1
navigability k=4: junk share 0.231, giant 1.000 -> 0.956 (95.6% retained)
```

`C6` — the same escape on top of the merged tiers `{4,3} {2,1} {0}`:

```
TEST-R  P@1 0.975  P@4 0.706  KeyMove@1 0.867  core@4 0.974  major@4 0.867
        useful@4 0.666  monotone (0 inv)  failures: prec 8, recall 3, grad 0
CAL     P@1 0.931  P@4 0.677  KeyMove@1 0.861  core@4 0.943  major@4 0.847
        useful@4 0.682  monotone (0 inv)  failures: prec 5, recall 1, grad 0
TEST-C  P@1 0.850  P@4 0.757  KeyMove@1 0.758  core@4 0.942  major@4 0.769
        useful@4 0.558  monotone (0 inv)  failures: prec 18, recall 1, grad 1
navigability k=4: junk share 0.238, giant 1.000 -> 0.954 (95.4% retained)
```

**The trades, stated.**

- C3e vs the weighted reference: wins P@1 (0.983 vs 0.975), P@4 (0.716 vs 0.679),
  KeyMove@1 (0.831 vs 0.825), core@4 (0.984 vs 0.963), precision failures (5 vs
  8), and is monotone on all three splits where the reference is not. The only
  TEST-R metric it loses on is major@4 (0.860 vs 0.864, about one item). On TEST-C it gains P@1 (0.867 vs 0.850) and P@4
  (0.742 vs 0.713) but **loses core@4 (0.950 vs 0.975)** — the reference buries
  fewer CORE moves on the harder split.
- C3e vs the Borda reference: **loses KeyMove@1 everywhere** (0.831 vs 0.872
  TEST-R, 0.778 vs 0.833 CAL, 0.683 vs 0.750 TEST-C) and loses core@4 on TEST-C
  (0.950 vs 0.983). It wins P@1 and P@4 on every split and halves the precision
  failures on TEST-R. This is the same trade the Borda/weighted comparison
  already showed, in the same direction: **schemes that sharpen rank 1 against
  defects lose key-move accuracy.**
- C6 vs C3e: buys KeyMove@1 (+0.036 TEST-R, +0.083 CAL, +0.075 TEST-C) and P@4
  on TEST-C (+0.015), pays P@1 (-0.008 to -0.017), core@4 (-0.010 to -0.014) and
  3 more precision failures on TEST-R. If key-move accuracy is the objective,
  C6 or the tree; if rank-1 cleanliness is, C3e.
- The tree C5 has the best KeyMove@1 of anything tested (0.881 / 0.889 / 0.775)
  and the best TEST-C major@4, at the cost of P@1 (0.969 / 0.958 / 0.850) and
  6 recall failures on TEST-R against C3e's 1.

**Negatives, reported.**

- Role-conditioned ordering (C1) is a dead end, and the mechanism is now exact:
  **in 539 of 552 proofs (97.6%) the highest occupied tier contains exactly one
  candidate**, so under a tier primary rank 1 is a foregone conclusion and no
  secondary signal can touch it. Verified directly — all four C1 variants select
  the *same* rank-1 item in every proof, hence identical P@1 0.836, KeyMove@1
  0.500 and 58 precision failures on TEST-R. That forced item is useful only 81%
  of the time and is the proof's best move at most half the time (KeyMove@1
  0.500 TEST-R, 0.375 CAL, 0.350 TEST-C). Choosing the
  secondary per tier (C1d) changes P@4 by 0.004 and nothing else. This is also
  why the escape is the right repair: the only way to fix rank 1 under a tier
  primary is to let something cross the boundary.
- No tier genuinely wants a different secondary signal (section 1).
- `is_proof` as an escape gate (C3f) actively hurts KeyMove@1 (0.717 TEST-R,
  0.608 TEST-C) — it promotes lemmas over the definitions and constructions that
  raters call CORE.
- A two-tier escape (C3g) is worse than a one-tier escape on TEST-R.
- Proof-level regimes (choose the ordering RULE from a proof-local fact, keeping
  C3e as the default rule) buy nothing. `src/scheme_conditional.py regimes`:

  | regime | TEST-R P@1 / P@4 / KM / mono | CAL | TEST-C |
  |---|---|---|---|
  | R1 proofs <= 8 candidates -> evidence only | 0.978 / 0.711 / 0.825 / **no** | 0.944 / 0.677 / 0.833 | 0.850 / 0.738 / 0.733 |
  | R2 proofs without tier-4 -> evidence only | 0.983 / 0.716 / 0.831 / yes | 0.944 / 0.688 / 0.778 | 0.867 / 0.742 / 0.683 |
  | R3 proofs with tier-4 -> evidence only | 0.950 / 0.628 / 0.817 / **no** | 0.944 / 0.604 / 0.875 | 0.817 / 0.639 / 0.750 |

  R2 is a near-no-op: only 12 of 552 proofs lack a tier-4 candidate. R1 trades
  monotonicity for +0.003 KeyMove@1 on CAL. R3 — dropping role entirely on the
  540 proofs that *do* have an applied-position candidate — is clearly worse
  (P@4 0.628 vs 0.716, 17 precision failures vs 5, 11 recall failures vs 1),
  which is the informative half: role structure matters most exactly where the
  applied position is occupied.
- Everything is worse on TEST-C than on TEST-R by roughly 0.10 P@1 for every
  scheme including both references, so TEST-C is a harder distribution, not a
  transfer failure of these schemes specifically. The relative ordering of
  schemes on TEST-C matches TEST-R for P@1, P@4 and monotonicity; it does **not**
  match for core@4, where both references beat every conditional scheme.
