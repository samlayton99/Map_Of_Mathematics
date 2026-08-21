# Scheme family: social choice / rank aggregation

Each signal is a VOTER producing a within-proof ordering; a voting rule
aggregates the ballots. Split **TEST-R** (360 proofs, 4,800 graded
incidences, median of three raters, loaded exactly as `src/mine_failures.py`).
Universe U1D. TEST-R is diagnostic data, already inspected: these numbers
select what to pre-register, they promote nothing.

Code: `src/social_choice.py` (voters + rules), `src/run_social_choice.py`
(battery), `src/run_social_choice_nav.py` (whole-corpus navigability),
`src/social_choice_analysis.py` (Condorcet / Kemeny-exactness / IIA / ties),
`src/sc_paired.py` (paired tests), `src/test_social_choice.py` (correctness).

## 0. Headline, stated as a trade

| claim | evidence |
|---|---|
| **Every purely ordinal rule trades P@4 down for KeyMove@1 up.** | best ordinal P@4 is 0.703 (`borda6_rarityx2`); reference 0.712. No exception in 40 schemes. |
| **The one scheme that improves KeyMove@1 with no P@4 cost is a hybrid**: use the pairwise majority relation ONLY to pick rank 1, keep a cardinal score for the rest. | `HYB_copeland_first`: Key@1 0.897 vs 0.864 (Δ +0.033, 95% CI [+0.006,+0.061], McNemar p=0.023); P@4 0.712 vs 0.713 (Δ −0.0007, CI [−0.0021,+0.0000]). |
| **It is the Condorcet property doing the work, not "a second opinion".** | promoting the *Borda* winner instead is the control: Key@1 0.853, Δ −0.011, p=0.62. |
| **Cost of the hybrid**: core@4 0.984 → 0.982 (one core move moves out of the top 4), and it is NOT decimal-free — it inherits the anchor's weights. | see §7 |

## 1. Voters

Six signals, each an ascending within-proof key. All append-safe: role /
in-statement are properties of an immutable elaborated proof term; depth,
arity, is_proof are kernel facts about a declaration's own type; rarity is the
PINNED frozen-foundation table (proofs with target depth ≤ 50), the same table
`mine_failures.py` builds. No library-wide max/mean/quantile, no name strings.

| voter | key (lower = better) | direction justified by |
|---|---|---|
| `role` | −tier | tier is monotone in usefulness, measured below |
| `depth` | −cited depth | deeper cited declaration is more content |
| `rarity` | −IDF50 | frozen `log(N/count)` |
| `stmt` | in-statement | a citation the proof INTRODUCES is the move |
| `arity` | −arity | CORE median arity 6, JUNK 2 (`KERNEL_SIGNALS.md`) |
| `isproof` | −is_proof | CORE 0.879 is_proof, JUNK 0.064 (idem) |

### Role tier: five ordinal levels, from meaning

Assigned from what the syntactic position MEANS, then checked. A candidate
takes the highest tier of any position it occupies.

| tier | positions | n (TEST-R) | useful ≥2 | major ≥3 | core =4 |
|---|---|---|---|---|---|
| 5 | applied, let-value | 356 | 0.834 | 0.478 | 0.419 |
| 4 | explicit-arg, unresolved | 1,615 | 0.526 | 0.274 | 0.138 |
| 3 | implicit, strict-implicit | 706 | 0.245 | 0.050 | 0.010 |
| 2 | type-annotation | 928 | 0.164 | 0.018 | 0.001 |
| 1 | instance-slot | 1,195 | 0.038 | 0.017 | 0.002 |

Strictly monotone in all three columns. The tier labels 1–5 are ordinal
labels, never multiplied by anything.

## 2. Rules

| rule | definition | Kemeny/pairwise? |
|---|---|---|
| `borda` | sum of within-proof midranks | positional |
| `harmonic` | Dowdall: points 1/(1+rank) | positional |
| `median_rank` | median of the six ranks, Borda tie-break | order statistic |
| `minimax_rank` | WORST rank any voter gives it, Borda tie-break | order statistic |
| `best_rank` | BEST rank any voter gives it, Borda tie-break | order statistic |
| `copeland` | pairwise majority wins − losses | pairwise |
| `maximin_pairwise` | Simpson–Kramer: min over opponents of pairwise support | pairwise |
| `kemeny` | minimise total pairwise disagreement, HEURISTIC (§4) | pairwise |
| `black_condorcet` | Condorcet winner first if one exists, else Borda | pairwise |
| `veto_below_tN` | role tier < N ranked after everything else, Borda inside | asymmetric |
| `role_lex` | role as dictator, Borda tie-break | asymmetric |
| `*_Vx2 / *_Vx3` | voter V's ballot counted 2 or 3 times | asymmetric |
| `HYB_{condorcet,copeland,borda}_first` | promote that winner to rank 1, keep a cardinal anchor order otherwise | hybrid |

Panels: `*6` = all six voters, `*4` = the four the incumbent product model
uses (role, depth, rarity, stmt).

## 3. Constants — the complete list

| constant | value | why it is not a tuned decimal |
|---|---|---|
| role tiers | 1..5 | ordinal labels; never enter arithmetic as weights |
| ballot multiplicity | 1, 2, 3 | small integers; **tested for every voter, not just role** |
| veto threshold | tier 2, tier 3 | integer tier boundaries |
| rarity foundation | depth ≤ 50 | pre-existing pinned table (`APPEND_SAFETY.md` §3) |
| Kemeny pass cap | 64 | integer safety cap; convergence measured, never hit |
| battery k | 1,2,4,8; nav k=4 | pre-existing battery constants |
| bootstrap | 2000 reps, seed 20260821 | resampling, not a model parameter |
| tie-breaks | Borda, then term position | stated, and their effect measured (§6) |

**The hybrid is the exception and it is a real one.** `HYB_*` inherits its
anchor's decimals (role weights 1.0/0.85/0.5/0.25/0.1, depth transform
0.20+0.80·log1p(d)/log1p(346)). The social-choice part adds no constant, but
the scheme as a whole is not decimal-free.

## 4. The reference line could not be reproduced exactly

The quoted reference (P@1 0.975, P@4 0.712, Key@1 0.825, core@4 0.974, 8
precision failures) is not defined anywhere in the repo. A sweep of 5 tier
maps × 4 weight vectors × 9 factor products (`src/probe_reference.py`, 180
models) found none reproducing all five numbers. Two closest:

| model | P@1 | P@4 | Key@1 | core@4 | fail P |
|---|---|---|---|---|---|
| quoted reference | 0.975 | 0.712 | **0.825** | 0.974 | 8 |
| `REF*` = role5w × log-depth × frozen rarity | 0.975 | 0.713 | 0.864 | 0.984 | 8 |
| `REF` role5w × frozen rarity | 0.964 | 0.703 | **0.825** | 0.976 | 12 |

`REF*` is used as the in-repo comparator and as the hybrid anchor. It matches
the quoted line on P@1, P@4 and failure count but scores 0.864 on Key@1, not
0.825 — **so every "beats the reference on Key@1" claim below is stated
against the harder 0.864 bar, not the quoted 0.825.**

## 5. Full battery, TEST-R

`mono`/`inv` are `battery.gradient`; `fail P/R/G` are `battery.failures`
(1 unwinnable proof throughout). `junk@4` / `giant` / `retained` are
`battery.navigability` at k=4 over the **whole U1D corpus** (18,081,920
incidences, 747,605 proofs), junk_mask = `corpus.inc_glue`
(`decl_logic_only | machinery`) — the best corpus-wide junk estimate
available; graded labels exist for 552 proofs only. Junk share over all
candidate edges is 0.3986, so every entry below demotes junk.

| scheme | P@1 | P@4 | Key@1 | core@4 | major@4 | useful@4 | mono | inv | fail P | fail R | fail G | junk@4 | giant | retained |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `REF*_role5w_x_logdepth_x_rarity` | 0.975 | 0.713 | 0.864 | 0.984 | 0.882 | 0.673 | y | 0 | 8 | 2 | 1 | 0.267 | 1.000 | 0.960 |
| `REF_role5w_x_stmt_x_logdepth_x_rarity` | 0.975 | 0.711 | 0.883 | 0.984 | 0.890 | 0.671 | y | 0 | 8 | 2 | 1 | 0.267 | 1.000 | 0.960 |
| `REF_role5w_x_rarity` | 0.964 | 0.703 | 0.825 | 0.976 | 0.864 | 0.663 | y | 0 | 12 | 3 | 1 | 0.285 | 1.000 | 0.963 |
| `borda6` | 0.978 | 0.695 | 0.844 | 0.984 | 0.895 | 0.656 | y | 0 | 7 | 2 | 0 | 0.263 | 1.000 | 0.960 |
| `borda4` | 0.975 | 0.693 | 0.872 | 0.979 | 0.892 | 0.655 | y | 0 | 8 | 4 | 0 | - | - | - |
| `copeland6` | 0.981 | 0.688 | 0.897 | 0.987 | 0.892 | 0.649 | y | 0 | 6 | 3 | 0 | 0.258 | 1.000 | 0.959 |
| `copeland_bordatb6` | 0.981 | 0.690 | 0.886 | 0.987 | 0.893 | 0.651 | y | 0 | 6 | 3 | 0 | 0.258 | 1.000 | 0.959 |
| `copeland4` | 0.983 | 0.670 | 0.878 | 0.971 | 0.871 | 0.632 | y | 0 | 5 | 4 | 0 | - | - | - |
| `kemeny6` | 0.981 | 0.695 | 0.875 | 0.987 | 0.899 | 0.656 | y | 0 | 6 | 3 | 0 | 0.260 | 1.000 | 0.960 |
| `kemeny4` | 0.981 | 0.677 | 0.883 | 0.976 | 0.883 | 0.639 | y | 0 | 6 | 4 | 0 | - | - | - |
| `median_rank6` | 0.978 | 0.686 | 0.872 | 0.987 | 0.890 | 0.648 | y | 0 | 7 | 3 | 0 | 0.263 | 1.000 | 0.959 |
| `minimax_rank6` | 0.969 | 0.686 | 0.850 | 0.950 | 0.863 | 0.647 | **N** | 2 | 10 | 7 | 1 | 0.264 | 1.000 | 0.958 |
| `best_rank6` | 0.969 | 0.671 | 0.844 | 0.953 | 0.830 | 0.633 | y | 0 | 10 | 3 | 0 | 0.319 | 1.000 | 0.961 |
| `maximin_pairwise6` | 0.964 | 0.584 | 0.819 | 0.874 | 0.730 | 0.552 | **N** | 1 | 12 | 4 | 3 | 0.377 | 1.000 | 0.958 |
| `maximin_bordatb6` | 0.981 | 0.686 | 0.856 | 0.955 | 0.854 | 0.647 | y | 0 | 6 | 1 | 0 | 0.308 | 1.000 | 0.959 |
| `black_condorcet6` | 0.975 | 0.695 | 0.869 | 0.984 | 0.895 | 0.656 | y | 0 | 8 | 2 | 0 | 0.263 | 1.000 | 0.960 |
| `harmonic6` | 0.983 | 0.687 | 0.842 | 0.969 | 0.863 | 0.649 | **N** | 1 | 5 | 1 | 0 | 0.304 | 1.000 | 0.961 |
| `borda6_rolex2` | 0.975 | 0.701 | 0.856 | 0.984 | 0.882 | 0.662 | y | 0 | 8 | 2 | 0 | 0.281 | 1.000 | 0.959 |
| `borda6_rarityx2` | 0.981 | 0.703 | 0.883 | 0.987 | **0.911** | 0.663 | y | 0 | 6 | 4 | 0 | 0.244 | 1.000 | 0.962 |
| `borda6_depthx2` | 0.981 | 0.693 | 0.875 | 0.987 | 0.898 | 0.655 | y | 0 | 6 | 2 | 0 | - | - | - |
| `borda6_stmtx2` | 0.972 | 0.689 | 0.839 | 0.979 | 0.890 | 0.650 | y | 0 | 9 | 4 | 0 | - | - | - |
| `borda6_arityx2` | 0.967 | 0.684 | 0.847 | 0.976 | 0.882 | 0.646 | y | 0 | 11 | 3 | 0 | - | - | - |
| `borda6_isproofx2` | 0.969 | 0.693 | 0.833 | 0.984 | 0.885 | 0.654 | y | 0 | 10 | 2 | 0 | - | - | - |
| `copeland6_rolex2` | 0.975 | 0.700 | 0.822 | 0.987 | 0.885 | 0.661 | y | 0 | 8 | 2 | 0 | 0.282 | 1.000 | 0.959 |
| `copeland6_rarityx2` | **0.986** | 0.679 | 0.886 | 0.987 | 0.885 | 0.641 | y | 0 | **4** | 4 | 0 | **0.237** | 1.000 | **0.962** |
| `copeland6_depthx2` | 0.975 | 0.662 | 0.881 | 0.963 | 0.871 | 0.625 | y | 0 | 8 | 6 | 0 | - | - | - |
| `copeland6_stmtx2` | 0.975 | 0.682 | 0.878 | 0.982 | 0.889 | 0.643 | y | 0 | 8 | 5 | 0 | - | - | - |
| `copeland6_arityx2` | 0.947 | 0.670 | 0.806 | 0.966 | 0.861 | 0.632 | y | 0 | 18 | 4 | 0 | - | - | - |
| `copeland6_isproofx2` | 0.975 | 0.689 | 0.858 | **0.990** | 0.876 | 0.650 | y | 0 | 8 | 2 | 0 | - | - | - |
| `borda6_rolex3` | 0.969 | 0.697 | 0.833 | 0.984 | 0.871 | 0.658 | y | 0 | 10 | 1 | 0 | - | - | - |
| `copeland6_rolex3` | 0.961 | 0.697 | **0.661** | 0.984 | 0.863 | 0.658 | y | 0 | 13 | 2 | 0 | - | - | - |
| `kemeny6_rolex2` | 0.978 | 0.698 | 0.847 | 0.987 | 0.880 | 0.659 | y | 0 | 7 | 3 | 0 | - | - | - |
| `kemeny6_rolex3` | 0.972 | 0.700 | 0.697 | 0.984 | 0.868 | 0.661 | y | 0 | 9 | 2 | 0 | - | - | - |
| `veto_below_t26` | 0.978 | 0.693 | 0.847 | 0.982 | 0.874 | 0.655 | y | 0 | 7 | 2 | 0 | 0.289 | 1.000 | 0.959 |
| `veto_below_t36` | 0.978 | 0.688 | 0.847 | 0.982 | 0.877 | 0.649 | y | 0 | 7 | 2 | 0 | 0.287 | 1.000 | 0.959 |
| `role_lex6` | 0.836 | 0.675 | 0.508 | 0.969 | 0.841 | 0.637 | y | 0 | **58** | 2 | 0 | 0.345 | 1.000 | 0.958 |
| `HYB_condorcet_first(REF*)` | 0.981 | 0.713 | 0.892 | 0.982 | 0.880 | 0.673 | y | 0 | 6 | 3 | 1 | 0.266 | 1.000 | 0.960 |
| **`HYB_copeland_first(REF*)`** | **0.983** | **0.712** | **0.897** | 0.982 | 0.882 | 0.672 | y | 0 | **5** | 3 | 1 | 0.267 | 1.000 | 0.960 |
| `HYB_borda_first(REF*)` *(control)* | 0.975 | 0.712 | 0.853 | 0.984 | 0.882 | 0.672 | y | 0 | 8 | 2 | 1 | 0.267 | 1.000 | 0.960 |
| `HYB_condorcet_first_rolex2(REF*)` | 0.978 | **0.714** | 0.856 | 0.984 | 0.882 | 0.674 | y | 0 | 7 | 2 | 0 | - | - | - |
| `HYB_copeland_first_rolex2(REF*)` | 0.978 | **0.714** | 0.858 | 0.982 | 0.880 | 0.674 | y | 0 | 7 | 3 | 0 | - | - | - |
| `dictator_role` | 0.836 | 0.675 | 0.508 | 0.969 | 0.841 | 0.637 | y | 0 | 58 | 2 | 0 | - | - | - |
| `dictator_depth` | 0.931 | 0.597 | 0.803 | 0.911 | 0.797 | 0.564 | y | 0 | 24 | 13 | 0 | - | - | - |
| `dictator_rarity` | 0.967 | 0.633 | 0.861 | 0.921 | 0.820 | 0.598 | **N** | 1 | 11 | 12 | 4 | - | - | - |
| `dictator_stmt` | 0.972 | 0.686 | 0.836 | 0.979 | 0.885 | 0.647 | y | 0 | 9 | 4 | 1 | - | - | - |
| `dictator_arity` | 0.808 | 0.593 | 0.583 | 0.785 | 0.718 | 0.560 | y | 0 | 68 | 31 | 4 | - | - | - |
| `dictator_isproof` | 0.981 | 0.687 | 0.725 | 0.971 | 0.865 | 0.649 | y | 0 | 6 | 6 | 0 | - | - | - |

Navigability separates the schemes only through **junk edge share**: the giant
component is ~1.000 for every rule and 0.958–0.963 of it survives deleting
machinery edges, a 0.005 spread. The junk share at k=4 spans 0.237
(`copeland6_rarityx2`) to 0.377 (`maximin_pairwise6`) against 0.399 for the
unranked candidate set. **`copeland6_rarityx2` and `borda6_rarityx2` build the
cleanest map of anything tested, including the reference (0.237/0.244 vs
0.267)** — a genuine win for the family that the per-proof metrics do not show.

## 6. Paired tests (TEST-R, 2,000-replicate proof-level bootstrap, exact McNemar)

| comparison | ΔKey@1 | 95% CI | McNemar (fixed/broken) | p | ΔP@4 | 95% CI |
|---|---|---|---|---|---|---|
| `HYB_copeland_first` vs REF* | **+0.033** | [+0.006, +0.061] | 18 / 6 | **0.023** | −0.0007 | [−0.0021, +0.0000] |
| `HYB_condorcet_first` vs REF* | **+0.028** | [+0.006, +0.050] | 14 / 4 | **0.031** | **+0.0000** | [+0.0000, +0.0000] |
| `HYB_borda_first` vs REF* *(control)* | −0.011 | [−0.042, +0.019] | 16 / 20 | 0.62 | −0.0007 | [−0.0021, +0.0000] |
| `copeland6` vs `borda6` | +0.053 | [+0.028, +0.081] | 21 / 2 | 0.0001 | −0.0070 | [−0.0160, +0.0021] |
| `copeland6` vs REF* | +0.033 | [+0.003, +0.064] | 22 / 10 | 0.050 | **−0.025** | [−0.041, −0.010] |
| `kemeny6` vs `borda6` | +0.031 | [+0.014, +0.050] | 12 / 1 | 0.0034 | +0.0000 | [−0.0056, +0.0063] |
| `borda6_rarityx2` vs REF* | +0.019 | [−0.011, +0.050] | 19 / 12 | 0.28 | −0.0105 | [−0.0245, +0.0028] |
| `borda6_rarityx2` vs `borda6` | +0.039 | [+0.019, +0.061] | 15 / 1 | 0.0005 | +0.0077 | [−0.0028, +0.0189] |
| `borda6_rolex2` vs `borda6` | +0.011 | [−0.008, +0.031] | 8 / 4 | 0.39 | +0.0063 | [−0.0021, +0.0153] |

`HYB_condorcet_first`'s P@4 delta is **exactly zero with a degenerate CI**.
Direct check: promotion changes top-4 *membership* in 1 of 360 proofs
(3 of 360 for copeland-first), and the count of useful items inside the top 4
is unchanged in all 360 — so the promotion reorders the top of the list
essentially without changing what is visible at k=4.

## 7. Cross-split confirmation

The hybrid's direction is the same on all three labelled splits, and the
control's is not.

| scheme | CAL (72) Key@1 / P@4 | TEST-C (120) | TEST-R (360) |
|---|---|---|---|
| `REF*` anchor | 0.833 / 0.688 | 0.725 / 0.769 | 0.864 / 0.713 |
| `HYB_copeland_first` | **0.889** / 0.688 | **0.758** / 0.767 | **0.897** / 0.712 |
| `HYB_condorcet_first` | 0.833 / 0.688 | **0.767** / 0.769 | **0.892** / 0.713 |
| `HYB_borda_first` *(control)* | 0.875 / 0.688 | 0.725 / 0.767 | 0.853 / 0.712 |
| `copeland6` *(pure)* | 0.875 / 0.681 | 0.742 / **0.675** | 0.897 / **0.688** |

The pure ordinal rule's P@4 loss is worst on TEST-C, the defect challenge set:
0.675 against the anchor's 0.769. Discarding magnitude hurts exactly where the
candidates are adversarial.

## 8. Condorcet

| | 6 voters | 4 voters |
|---|---|---|
| a Condorcet winner exists | 299/360 (0.831) | 295/360 (0.819) |
| when it exists, it is a top-graded item | 273/299 (0.913) | 265/295 (0.898) |
| it coincides with the Borda winner | 287/299 (0.960) | 281/295 (0.953) |
| Borda Key@1 given a winner exists | 0.883 | 0.888 |
| Borda Key@1 given no winner exists | **0.656** | 0.800 |

**Condorcet existence is itself a confidence signal.** When the six signals
admit a majority winner, any sane rule finds the key move 88% of the time;
when they cycle, Borda drops to 0.656. That is a forensic hook worth exposing
in the UI regardless of which ranking ships: "the signals disagree here."

## 9. Kemeny: which heuristic, and how far off

Borda-seeded odd-even adjacent-transposition local search, swapping a
neighbouring pair only when the swap strictly reduces total pairwise
disagreement. Every accepted swap strictly decreases the objective, so it
terminates at a local optimum with respect to adjacent transpositions. Exact
Kemeny is NP-hard.

| check | result |
|---|---|
| 300 random 4-voter profiles, n ≤ 6, vs exhaustive optimum | optimal in 299/300, mean excess 0.0033 disagreements |
| TEST-R proofs with n ≤ 8 (104 of 360), vs exhaustive optimum | optimal in **102/104**, mean excess 0.0192 |
| Kemeny order differs from the Borda seed | 203/360 proofs |

So the heuristic is effectively exact at this scale, and it is not just
returning its seed.

## 10. Arrow

Arrow: with ≥3 alternatives no rule mapping ordinal profiles to a transitive
social ordering satisfies unrestricted domain + Pareto + IIA + non-dictatorship.

| rule | UD | Pareto | IIA | non-dictator | escapes Arrow by |
|---|---|---|---|---|---|
| `borda`, `harmonic` | y | y | **N** | y | dropping IIA |
| `median_rank`, `minimax_rank`, `best_rank` | y | y | **N** | y | dropping IIA |
| `copeland`, `maximin`, `kemeny`, `black` | y | y | **N** | y | dropping IIA |
| `veto_below_tN` | y | y | **N** | y | dropping IIA |
| `role_lex` / `dictator_*` | y | y | **y** | **N** | being a dictatorship |
| `REF*` product model | y | y | **y** | y | **not being an ordinal rule at all** |
| `HYB_*_first` | y | y* | **N** (measured 0.001) | y | mostly cardinal |

\* the hybrid's Pareto holds with respect to its anchor's factors; promotion
never violates it, because a candidate every voter ranks below another cannot
be a Condorcet or Copeland winner while that other is present.

**The cardinal model is not a counterexample to Arrow** — it reads magnitudes,
so it is outside Arrow's ordinal domain. That is the whole content of the
comparison: the product model buys IIA with cardinal information, and this
family sells IIA to buy scale-freeness.

### Does breaking IIA matter here? Measured, and yes — a little

Restrict the candidate universe U1D → U1 (4,800 → 1,971 candidates, dropping
definitions in non-load-bearing roles) and count how many of the 7,759
surviving graded pairs flip their relative order.

| rule | pair flips | rate | rank-1 item changed |
|---|---|---|---|
| `REF*` cardinal | 0 | **0.0000** | 0.0000 |
| `copeland_first_anchor` | 7 | 0.0009 | 0.0155 |
| `condorcet_first_anchor` | 9 | 0.0012 | 0.0217 |
| `maximin_pairwise` | 9 | 0.0012 | 0.0280 |
| `copeland` | 178 | 0.0229 | 0.0062 |
| `harmonic` | 211 | 0.0272 | 0.0652 |
| `kemeny` | 230 | 0.0296 | 0.0248 |
| `best_rank` | 254 | 0.0327 | 0.0807 |
| `black_condorcet` | 327 | 0.0421 | 0.0373 |
| `borda` | 333 | **0.0429** | 0.0559 |
| `median_rank` | 417 | 0.0537 | 0.0745 |
| `minimax_rank` | 689 | **0.0888** | **0.1118** |

`maximin_pairwise`'s low rate is an artifact of its degeneracy (§11), not a
virtue.

What this costs, precisely: **a rank-aggregated order is a property of the
candidate SET.** Change the extractor's universe and 4.3% of pairs that did
not themselves change are re-ordered anyway, and one proof in eighteen gets a
different headline item. Two things this is NOT:

- **It is not an append-safety violation.** Adding a theorem to Mathlib does
  not change any existing proof's candidate set, so every scheme here is
  append-safe. Whole-corpus navigability at k=4 was recomputed with no
  library-wide statistic anywhere.
- **It is not a correctness argument.** We have external ground truth, so a
  rule is judged by the battery, not by axioms. IIA failure is a
  reproducibility and forensic cost — "why did X move? because Y was added to
  the candidate list" is an answer a forensic agent has to accept — and it is
  a reason to prefer the hybrids (0.001) over pure Borda (0.043) at equal
  battery scores, not a reason to reject the family.

## 11. Rules that are worse, and why

| rule | verdict |
|---|---|
| `maximin_pairwise` | **Broken as specified.** With six voters, min pairwise support is 0 for almost every candidate: 91.4% of candidates sit in an exact tie and only 0.204 distinct scores per candidate remain, so the published order is essentially term order. P@4 0.584, core@4 0.874, gradient non-monotone, worst junk share (0.377). With a stated Borda tie-break (`maximin_bordatb6`) it recovers to 0.981/0.686/0.856 — i.e. **its earlier numbers measured the tie-break, not the rule.** "Only as good as your weakest pairwise showing" is too coarse a summary of six ballots. |
| `minimax_rank` ("weakest qualification") | **The conceptually attractive idea fails.** Non-monotone gradient (2 inversions), core@4 0.950 — worst of the non-degenerate rules — 7 recall failures, and the worst IIA sensitivity (0.089 pair flips, 0.112 top-1 changes). A key move genuinely does NOT qualify on every signal: CORE items are frequently rare-and-deep but sit in an implicit position, and one bad ballot buries them. The hypothesis is falsified on its own terms. |
| `best_rank` | The mirror also fails: P@4 0.671, core@4 0.953, junk 0.319. One good ballot is too easy to obtain. |
| `role_lex` / `dictator_role` | **Catastrophic**: P@1 0.836, Key@1 0.508, 58 precision failures. Role tier 5 contains only 356 of 4,800 candidates and 41.9% of them are CORE — but 58.1% are not, and with role deciding first, Borda cannot rescue those proofs. Arrow's dictatorship escape is available and useless. |
| `veto_below_tN` | Inert. Vetoing tier 1 or tiers 1–2 moves Borda by +0.003 Key@1 and −0.002/−0.007 P@4. Borda already ranks those candidates last; the veto has nothing left to do. |
| role multiplicity 3 | **Harmful and diagnostic**: `copeland6_rolex3` Key@1 0.661, `kemeny6_rolex3` 0.697. At weight 3 of 8 the role ballot decides most pairwise contests, and the rule degrades toward `role_lex`. |
| `harmonic` (Dowdall) | Best P@1 of the pure rules (0.983) but a non-monotone gradient and core@4 0.969: 1/(1+rank) concentrates everything on rank 1 and stops discriminating below rank 3. Wrong shape for a slider. |
| `copeland4` / `kemeny4` | The 4-voter panel is worse than the 6-voter panel on P@4 (0.670/0.677 vs 0.688/0.695) and core@4. `arity` and `is_proof` are weak alone (`dictator_arity` P@1 0.808) but they carry the middle of the list. |

## 12. The asymmetry hypothesis — tested and NOT supported as posed

The proposal was that role, being nearly a deterministic filter, should get a
veto or extra ballots. Multiplicity 2 was applied to **each of the six voters
in turn**, so the role result is read against its own controls:

| doubled voter | Borda ΔKey@1 | Borda ΔP@4 | Copeland ΔKey@1 | Copeland ΔP@4 |
|---|---|---|---|---|
| **rarity** | **+0.039** | **+0.008** | −0.011 | −0.009 |
| depth | +0.031 | −0.002 | −0.016 | −0.026 |
| role | +0.011 | +0.006 | **−0.075** | +0.012 |
| isproof | −0.011 | −0.002 | −0.039 | +0.001 |
| arity | +0.003 | −0.011 | −0.091 | −0.018 |
| stmt | −0.005 | −0.006 | −0.019 | −0.006 |

The best voter to double is **rarity**, not role — and doubling role is the
single worst move for Copeland (−0.075). The correct reading of the asymmetry
is the opposite of the hypothesis: role is already near-decisive *as one
ballot* because it is the most extreme voter, so amplifying it removes the
correction the graded evidence provides. The signal that deserves extra weight
is the one carrying magnitude, which rank aggregation throws away.

`borda6_rarityx2` is nonetheless **not** a win over the reference: ΔKey@1
+0.019 (CI crosses 0, p=0.28), ΔP@4 −0.011 (CI crosses 0). It is a wash on the
per-proof battery that buys a materially cleaner map (junk 0.244 vs 0.267).

## 13. Interpretability

| scheme | what a forensic agent reads off |
|---|---|
| `borda*` | "2nd on role, 1st on depth, 5th on rarity, 3rd on statement, 4th on arity, 2nd on is_proof → 17 points, second lowest in the proof." Six integers, fully auditable. |
| `copeland*` | "beat 7 of the 9 other candidates on a majority of the six signals, lost 1." One integer plus a 9-row pairwise table. |
| `kemeny` | Worst of the family: the position is justified only by a global permutation objective, and no per-candidate statement exists. |
| `HYB_*_first` | Two-line explanation: the cardinal score, plus "and it beat every other candidate on a majority of signals, so it was promoted to rank 1." The promotion is a discrete, checkable event affecting exactly one item per proof. |
| `maximin`, `minimax_rank` | Readable in principle, but the answer is usually "one bad ballot", which is not an explanation a reader accepts. |

## 14. Verdict

1. **Recommend pre-registering `HYB_copeland_first` (equivalently
   `HYB_condorcet_first`) over the standing cardinal model.** It is the only
   scheme tested that improves Key@1 with no measurable P@4 cost, the effect
   is significant (p=0.023), directionally consistent on all three splits, and
   the Borda-winner control rules out "any second opinion works". Cost to
   state: core@4 0.984 → 0.982, and it is not decimal-free.
   `HYB_condorcet_first` is the more conservative of the two — it touches only
   the 299/360 proofs with a Condorcet winner and changes top-4 membership in
   exactly 1 proof of 360.
2. **Do not ship a pure rank-aggregation rule.** Every one of them pays 0.010
   to 0.129 of P@4 for its Key@1, and the loss is worst on the adversarial
   TEST-C split. Rank aggregation discards the magnitude of the rarity signal,
   which is what orders positions 2–4.
3. **The family's real contribution is navigability, not per-proof precision.**
   `copeland6_rarityx2` and `borda6_rarityx2` cut the junk share of the top-4
   map from 0.267 to 0.237/0.244 — the cleanest whole-corpus map measured
   anywhere in this programme — while the per-proof battery calls them a wash.
   If the objective is the map rather than the headline item, that is the
   result to follow up.
4. **Two hypotheses falsified.** "A key move qualifies on every signal"
   (`minimax_rank`) and "role deserves multiplicity" both fail, the second
   with the sign reversed.
5. **Report Condorcet existence in the UI regardless of the ranking.** 83% of
   proofs have a majority winner; the other 17% are where every rule's Key@1
   collapses (0.883 → 0.656). It is a free, computable confidence flag.
