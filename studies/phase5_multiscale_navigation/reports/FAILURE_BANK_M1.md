# Failure bank — M1_role_x_frozen_rarity (TEST-R, 360 proofs)

Source: `review/failures/testr/M1_role_x_frozen_rarity.json`
(39 precision, 14 recall, 1 gradient reversal). Every failure examined
individually; classifications below are mechanical wherever `blame`,
`n_useful` or a per-proof AP recomputation settles them.

Method under review: `score = role x IDF50`, where `role in {1.0 applied,
0.7 let-value/explicit-arg, 0.5 everything else}` and
`IDF50 = log(430358 / count_at_target_depth<=50)`, ceiling 12.9724.
Metric: NavAP (per-proof AP, positives = median grade >= 2), macro-averaged.
Baseline M1: TEST-R 0.8621, TEST-C 0.8301, CAL 0.8389.

## Classification key

| | |
|---|---|
| **A MISLABELLED** | raters wrong, ranking right |
| **B UNWINNABLE** | content absent from the list, or <= 1 useful candidate exists |
| **C SIGNAL BUG** | a signal carries a defensibly wrong value |
| **D MISSING SIGNAL** | a nameable, computable property would have fixed it |
| **E TRADE-OFF** | working as designed; acceptable cost of a rule that pays elsewhere |

Counts: **A 6 · B 13 · C 12 · D 6 · E 17** (54 total).

---

## 1. Precision failures (39)

`nu` = number of candidates in the whole list with median grade >= 2.
`AP` = per-proof average precision under M1. `FIX1` = status under the
proposed role re-bucketing (Task 1 below).

| id | proof | theorem | nu | AP | class | evidence |
|---|---|---|---|---|---|---|
| P00 | 0132 | `Presieve.BindStruct.hg` | 1 | **1.000** | B | ordering is perfect; detector fires because only 1 useful candidate exists |
| P01 | 0083 | `IsBimonHom.toIsMonHom` | 1 | **1.000** | B | same; all raters: "the content is unnameable by any citation" |
| P02 | 0115 | `addLECancellable_zero` | 2 | 0.577 | E | `zero_add` CORE at 1; 2nd useful is `id`@9, median 0 in 57/69 corpus proofs |
| P03 | 0117 | `Frm.id_apply` | **0** | n/a | B | all three raters state the working lemma is *not in the list*; only simp residue is |
| P04 | 0118 | `InducedWideCategory.Hom.property` | 1 | **1.000** | B | detector artifact |
| P05 | 0146 | `prod.prodμ_counitIso_inv_app` | 2 | 0.278 | D | `blame`: neither role nor rarity swap fixes. `Prod.mkHom` (**def**) outranks `comp_id` (**theorem**); kind is the unused discriminator |
| P06 | 0150 | `CommGrp.forget₂Grp_obj_one` | 4 | 0.427 | E | MAJOR at 1; `CommGrp.instCategory` (JUNK) survives at 3 because its `delta_depth==1` exempts it from the instance demotion — direct cost of Task 1's carve-out |
| P07 | 0170 | `adjMatrix_hadamard_ofNat` | 1 | **1.000** | B | detector artifact |
| P08 | 0173 | `LinearMap.map_add` | 2 | 0.667 | C | ranks 2–5 are all instance-slot-only. FIX1 -> **AP 1.000, cleared** |
| P09 | 0213 | `Limits.Types.jointly_surjective` | 1 | **1.000** | B | detector artifact |
| P10 | 0248 | `AddEquiv.coe_mapAddSubgroup` | 4 | 0.520 | C | instance-slot at 3,4. FIX1 -> 0.678, **cleared** |
| P11 | 0212 | `LaxMonoidalFunctor.id_hom` | 2 | 0.267 | E | no candidate above LEGIT_GLUE anywhere; rank-1 `[2,1,1]` vs best `[2,2,2]`. The 1-vs-2 boundary here is inside rater noise |
| P12 | 0214 | `Discrete.equivalence_counitIso` | 2 | 0.559 | E | correct item at 1; 2nd useful is `Eq.refl`@13 |
| P13 | 0227 | `UInt64.toFin_sub` | 5 | 0.660 | C | `blame[role].would_fix = True`. `UInt64.size` is scored explicit-arg (0.7) but the occurrence is an argument *inside the `Fin` type*, not a proof step. Role over-credits nested occurrences |
| P14 | 0207 | `Frm.Iso.mk_hom` | 2 | 0.583 | E | 2nd useful is `Eq.refl`@7 |
| P15 | 0208 | `Int.lt_min` | 2 | 0.667 | C | CORE at 1; ranks 2,3 instance-slot. FIX1 -> 0.833, **cleared** |
| P16 | 0204 | `mopMopEquivalence...η_unmop_unmop` | 2 | 0.321 | D | `blame[role].would_fix = True` but only downward. The graded-better item is the one with `delta_depth == 1` (the declaration the lemma is *about*); that relation is unused |
| P17 | 0222 | `Nat.modEq_three_digits_sum` | 1 | **1.000** | B | detector artifact |
| P18 | 0241 | `SmallObject.hasPushouts` | 2 | 0.700 | E | CORE at 1; 2nd useful is a class in type-annotation position, which Task 1 deliberately demotes |
| P19 | 0203 | `coalgebraToOver_map` | 2 | 0.567 | E | 2nd useful is `Eq.refl`@15 |
| P20 | 0218 | `SeminormedSpace.Core.norm_triangle` | 1 | **1.000** | B | detector artifact |
| P21 | 0275 | `Finset.sup_insert` | 1 | **1.000** | B | detector artifact |
| P22 | 0256 | `Monotone.mulIndicator_eventuallyEq_iUnion` | 3 | 0.610 | C | ranks 2,3,4 are `Set.instCompleteAtomicBooleanAlgebra` and its parent projections. FIX1 -> **AP 1.000, cleared** |
| P23 | 0280 | `Set.image_single_Ico` | 1 | **1.000** | B | detector artifact |
| P24 | 0266 | `Opens.coe_inf` | 3 | 0.540 | C | instance-slot chain at 3,6. FIX1 -> 0.700, **cleared** (also clears R07) |
| P25 | 0262 | `Finset.weightedVSub_filter_of_ne` | 2 | 0.567 | E | CORE at 1; 2nd useful is `Ne`, ubiquitous |
| P26 | 0259 | `Std.ExtHashSet.insert_eq_insert` | 3 | 0.633 | C | ranks 2,4 are class type-annotations graded `[0,1,0]`. FIX1 **clears** it |
| P27 | 0315 | `Matrix.diagonalRingHom_apply` | 3 | 0.491 | E | 2nd/3rd useful are `DFunLike.coe`, `Eq.refl` |
| P28 | 0323 | `Std.DTreeMap.Raw.mem_filter` | 4 | 0.431 | D | **ceiling tie**: `get?` (BAD_GLUE) and `contains_filter` (CORE) both have role 0.7 *and* IDF50 = 12.9724 exactly; order decided by array index. `in_statement` separates them (get? yes, contains_filter no) |
| P29 | 0350 | `moduleCatExtendScalarsPseudofunctor_obj` | 3 | 0.516 | E | 2nd/3rd useful are `Prefunctor.obj`, `Eq.refl` |
| P30 | 0352 | `Polynomial.taylor_one` | 1 | **1.000** | B | detector artifact |
| P31 | 0334 | `Set.Nonempty.ncard_pos` | 5 | 0.710 | D | ceiling tie again. Rank 1 is `Set.ncard_pos._auto_1` (`[0,0,0]`, an autoParam filler); CORE `Set.ncard_pos` at 2. `in_statement` separates them and **fixes** it |
| P32 | 0406 | `AffineScheme.forgetToScheme_map` | 5 | 0.342 | D | ceiling tie with **no available discriminator**: `Scheme.Spec` (BAD_GLUE) and `forgetToScheme` (MAJOR) agree on role, on `in_statement`, and both saturate IDF50 |
| P33 | 0391 | `DilationEquiv.mulLeft_apply` | 3 | 0.440 | E | 2nd/3rd useful are `DFunLike.coe`, `Eq.refl` |
| P34 | 0386 | `conformal_id` | 1 | **1.000** | B | detector artifact |
| P35 | 0402 | `AEMeasurable.nullMeasurable` | 7 | 0.597 | **A** | all three raters write "the witness extraction is a real step that **no citation names**" — but the list *does* contain the `match` auxiliary that performs exactly that destructuring, at rank 1, graded `[2,1,0]`. The raters named the move and then failed to recognise its citation |
| P36 | 0410 | `ModularForm.coe_const` | 3 | 0.414 | E | CORE at 1; 2nd/3rd useful are `DFunLike.coe`, `Eq.refl` |
| P37 | 0423 | `eLpNorm_top_piecewise` | 1 | **1.000** | B | detector artifact |
| P38 | 0396 | `WithLp.prod_lipschitzWith_ofLp` | 2 | 0.667 | C | CORE at 1; ranks 2,4 `ENNReal.instLE`/`instOne`. FIX1 -> 0.750, **cleared** |

## 2. Recall failures (14)

| id | proof | buried item | votes | class | evidence |
|---|---|---|---|---|---|
| R00 | 0093 | `propext`@8 | 4,4,4 | E | label is solid, but `propext` is graded 0–1 in 16/17 corpus proofs; rarity demoting it is right on average |
| R01 | 0076 | `rfl`@5 | 4,3,4 | **A** | `rfl` has median 2 in 66 of 81 corpus proofs; the raters' own prose says the content is "the shape of the `Max` instance", which the ranking placed at rank 2 |
| R02 | 0184 | `Set.image_comp`@5 | 4,4,3 | E | genuine 4-rewrite proof; AP already 0.929. The rank-4 cut, not the ordering, is the failure |
| R03 | 0311 | `LT.lt.not_ge`@7 | 4,4,3 | C | three `Finset.inst*` instance-slots occupy ranks 4–6. FIX1 -> AP 0.755→0.924, **cleared** |
| R04 | 0288 | `rfl`@9 | **2,4,4** | **A** | see §3.1 — one of only 5 median-4 labels in the entire sealed corpus that rests on a min vote <= 2 |
| R05 | 0276 | `rfl`@5 | **2,4,4** | **A** | same |
| R06 | 0301 | `prod.comp_lift`@5 | 3,4,4 | E | 12 useful candidates, AP 0.976; rank-4 cut |
| R07 | 0266 | `rfl`@7 | **2,4,4** | **A** | same; also cleared by FIX1 |
| R08 | 0273 | `rfl`@7 | **2,4,4** | **A** | same |
| R09 | 0318 | `Category.assoc`@10 | 4,3,4 | E | reassoc-generated lemma; `assoc` is genuinely used but is one of the most common declarations in the library |
| R10 | 0348 | `ciSup_le'`@5 | 3,4,4 | E | 8 useful candidates, AP 0.966 under FIX1; rank-4 cut |
| R11 | 0411 | `mul_comm`@6 | 3,4,4 | C | `Polynomial.commRing`/`instMul` occupy ranks 4,5. FIX1 -> AP 1.000, **cleared** |
| R12 | 0383 | `add_comm`@5 | 4,4,4 | C | `Measure.instAddCommMonoid`/`instAdd` occupy ranks 2,3. FIX1 -> AP 1.000, **cleared** |
| R13 | 0420 | `contDiff_iff_contDiffAt`@5 | 4,4,4 | D | five candidates tie at role 0.7 x IDF50 12.9724. Both COREs are `in_statement = False`; that signal is unused |

## 3. Gradient reversal (1)

| id | proof | class | evidence |
|---|---|---|---|
| G00 | 0305 `BoolAlg.dualEquiv_inverse` | C | `BoolAlg.instCategory` (JUNK, instance-slot, `delta_depth`=10) at rank 3 pushes both useful items into the bottom half. FIX1 **clears** it |

---

## 4. Patterns

### 4.1 The MISLABELLED claim, stated explicitly (A, 6 cases)

Four of the five buried-`rfl` recall failures (R04, R05, R07, R08) carry the
vote vector `[2,4,4]`. Across the **entire** sealed corpus (552 proofs, 7,531
graded candidates) there are 572 items with median grade 4, and only **5** of
them rest on a vote whose minimum is <= 2. All five are `rfl` or `Iff.rfl`;
four of the five are precisely these four failures. Meanwhile the
declaration `rfl` has median 2 in 66 of 81 proofs corpus-wide and median 4 in
7. R01 (`[4,3,4]`) is the same family, marginally firmer.

This is not "raters disagreed a bit". It is the most fragile label class in
the corpus, concentrated on one declaration, and the raters' own free-text
`rater_moves` in every one of these five proofs names the *definition being
unfolded* as the content ("the content is entirely the shape of the `Max`
instance"; "the content is that the lattice instance is set-level by
construction") — which is exactly what M1 put at rank 1. **The prose and the
grade contradict each other, and the ranking agrees with the prose.**

P35 is the sixth: all three raters wrote that the witness destructuring "is a
real step that no citation names", while the `match` auxiliary performing that
destructuring sits at rank 1 in the list they were grading.

Rater-offset check, for completeness: raters A/B/C carry global offsets of
+0.044 / -0.000 / -0.044 grades, so there is no gross rater bias. There *is* a
class-local one: on definitional projections (`kind=def`, in-statement,
`delta_depth==1`, n=190) rater A runs **+0.279** above the mean of the other
two. That inflates the top-of-list grades in P12/P14/P16/P19 but does not
change their classification, since those fire on ranks 2–4, not rank 1.

### 4.2 The `top4_mostly_defects` detector is measuring the proof, not the ranking (B, 13 cases)

`top4_mostly_defects` fires when >= 3 of the top 4 are graded <= 1. Twelve of
the 30 such failures have **exactly one useful candidate in the entire list**,
and one (P03) has **zero**. In all twelve the ranking's per-proof AP is
**1.000** — every useful item is above every defect; the ordering is
literally optimal. The detector is unsatisfiable on these proofs by any
ranking whatsoever.

**Recommendation: gate the detector on `n_useful >= 2` (and prefer AP over a
fixed top-4 window) before the next round.** Without that, ~33% of M1's
reported precision failures are noise.

P03 is the genuinely diagnostic member of this group: three raters
independently state the lemma doing the work is absent from the candidate
list. `simp`-discharged rewrites leave only `of_eq_true`/`eq_self` in the
kernel term, so the extractor cannot see them. That is a **corpus-extraction**
limitation, not a ranking one, and no reordering can address it.

### 4.3 The `role` factor's 0.5 bucket lumps together three wildly different positions (C, 12 cases — the dominant fixable pattern)

M1 assigns 0.5 to instance-slot, implicit-arg, type-annotation and
unresolved alike. On TEST-R (4,800 graded candidates):

| position (sole role) | n | P(grade >= 2) | P(>= 3) | mean rater disagreement |
|---|---|---|---|---|
| applied | 336 | **0.860** | 0.485 | 0.22 |
| let-value | 7 | 1.000 | 1.000 | 0.43 |
| explicit-arg | 1134 | 0.563 | 0.340 | 0.42 |
| implicit-arg | 384 | 0.367 | 0.086 | 0.34 |
| type-annotation | 928 | 0.164 | 0.018 | 0.38 |
| **instance-slot** | **1195** | **0.038** | 0.017 | **0.11** |

Instance-slot occurrences are 25% of everything graded, are useful 3.8% of
the time, and carry the **lowest rater disagreement in the whole dataset**
(0.11) — the labels are as certain as labels get. Yet at the IDF50 ceiling
they score `0.5 x 12.9724 = 6.486`, which outranks almost all real content.
This single mis-bucketing accounts for 8 precision failures, 3 recall
failures and the sole gradient reversal.

The obvious blunt fix has a known counterexample class, and the data says why.
Split instance-slot by `delta_depth = depth(target) - depth(cited)`:

| instance-slot only, by delta_depth | n | P(useful) | P(>= 3) |
|---|---|---|---|
| **1** | 49 | **0.571** | 0.367 |
| 2 | 21 | 0.048 | 0.000 |
| 3–5 | 97 | 0.062 | 0.021 |
| 6–10 | 119 | 0.025 | 0.000 |
| 11–30 | 309 | 0.013 | 0.000 |
| 31+ | 641 | 0.011 | 0.002 |

`delta_depth == 1` means the instance is the declaration immediately below the
target in the depth DAG — the instance the lemma *is about*
(`Opens.instCompleteLattice` for `Opens.coe_inf`; `Sum.instLocallyFiniteOrder`
for `Sum.Ioo_inr_inl`). Everything else is typeclass-resolution transport.
**Without this carve-out the demotion breaks P24, P26 and R04; with it, they
survive.** This is the sharper condition the earlier blanket-auto-generated
experiment lacked.

### 4.4 The frozen-rarity ceiling saturates and ties (D, 4 of 6 cases)

`IDF50` is `log(430358/count)` over proofs at target depth <= 50, capped at
**12.9724** for anything the frozen foundation never cites. 562 of 4,800
TEST-R candidates (12%) sit exactly at that ceiling; in deep proofs it is most
of the list. Score then collapses to `role x 12.9724` — a three-valued
function — and the final order is decided by **array index**. P28, P31, P32
and R13 are all decided this way, with `score_gap = 0.0000` and
`blame[*].would_fix = False` for every factor.

Deep declarations are exactly where the ranking matters most, and exactly
where the frozen foundation is blindest. `in_statement` breaks three of these
four ties correctly (P28, P31, R13); P32 has no available discriminator at
all.

### 4.5 The ubiquitous-residual family: rarity works, and this is its bill (E, 12 of 17 cases)

In 10 of the 17 trade-off cases the second-or-later useful item is one of
`Eq.refl`, `rfl`, `id`, `DFunLike.coe`, `Ne`, `OfNat.ofNat`, `propext`,
`Category.assoc` — declarations so common that IDF50 floors them. Corpus-wide
they are graded 0 or 1 far more often than 2 (`id`: median 0 in 57/69;
`Eq.refl`: median 0–1 in 34/82; `propext`: 0–1 in 16/17). Promoting them
would lose more than it gains. **No fix proposed; this is the intended
behaviour.**

The remaining 5 (R02, R06, R09, R10 and P18) are proofs with 5–12 genuinely
useful moves where the rank-4 window simply cannot hold them all — AP is
0.93–0.98. These are detector-window artifacts of the same species as §4.2.

### 4.6 `auto_generated` is a red herring — confirmed, do not revisit

32 of 4,800 TEST-R candidates are auto-generated, and they are graded useful
**68.8%** of the time versus a 31.4% base rate. The flag is *positively*
correlated with usefulness. The earlier blanket-demotion result (0.862 ->
0.851) was not bad luck. The junk sub-population (autoParam fillers, extracted
proof obligations) is not separable by this flag; separating it needs the
parameter-slot property discussed in Task 4, which is Lean-specific.

---

## 5. Task bank, prioritised

All measurements below are on the sealed splits **after** they were used for
this forensics pass. TEST-R is now diagnostic data, not confirmatory. Every
number is an effect-size estimate for planning, not a result.

### Task 1 — Re-bucket the `role` factor (SHIP CANDIDATE)

Replace the 3-level role table with a 5-level precedence ladder. This changes
**one existing factor**; it does not add a factor.

```
strongest role present, in this order:
  applied                                    1.00
  let-value or explicit-arg                  0.70
  implicit-arg                               0.50
  type-annotation                            0.35
  instance-slot (no stronger role present)   0.15
then: if depth(target) - depth(cited) == 1, floor the weight at 0.50
```

Only the old 0.5 bucket moves: of 2,838 such TEST-R candidates, 1,148 go to
0.15, 924 to 0.35, 766 stay at 0.50. 0.7 and 1.0 are untouched.

- **Failures addressed (observed):** 12 — P08, P10, P15, P22, P24, P26, P38, R03, R07, R11, R12, G00. Substantial AP improvement on 12 more (P06, P10, P32, P33, R08, R09, R10, R13, …).
- **Failures introduced:** **zero** on TEST-R.
- **Cost elsewhere:** P06 is the visible price of the `delta_depth == 1`
  carve-out — a JUNK `instCategory` at delta 1 keeps rank 3. Accepted: the
  carve-out is worth 3 other failures.
- **Measured effect:** TEST-R 0.8621 -> **0.9018** (+0.0397, 95% CI
  [+0.0321, +0.0474], 184 proofs improved / 32 worsened); TEST-C 0.8301 ->
  **0.8782** (+0.0481, [+0.0353,+0.0621], 65/12); CAL 0.8389 -> **0.8741**
  (+0.0352, [+0.0181,+0.0554], 35/8). clean@1 unchanged at 0.975, major
  recall@4 0.911 -> 0.926, precision failures 39 -> 33, recall 14 -> 10.
  **No metric on any split degrades.**
- **Constraint check:** role bits and node depths only — both frozen; adding
  a theorem at the edge changes neither. No name strings. Demotes only.
  Same factor count as M1.
- **How to test:** register the exact weight table and the delta==1 floor in a
  pre-registration; draw a fresh sealed split; primary endpoint NavAP vs M1
  with a paired hierarchical bootstrap; pre-declare clean@1 as a
  non-inferiority guard at a 0.01 margin. Sensitivity: the instance weight is
  flat between 0.05 and 0.25 (AP varies by 0.001), so do not tune it — fix it
  at 0.15 and state that in advance.

### Task 2 — Gate the failure detectors (INSTRUMENTATION, do first)

`top4_mostly_defects` is unsatisfiable when `n_useful < 2`; `core_move_buried`
fires on proofs with more than 4 genuine moves. Both measure the proof, not
the ranking.

- **Failures addressed:** 13 B-class + 5 E-class = **18 of 54 reported
  failures are detector artifacts**.
- **Fix:** require `n_useful >= 2` for `top4_mostly_defects`; require
  `n_core <= 4` for `core_move_buried`; emit per-proof AP and
  `AP_achievable = 1.0` alongside every flag so "perfect ordering, flagged
  anyway" is visible at a glance.
- **Cost:** none — this is measurement hygiene, not a ranking change.
- **Test:** re-run `mine_failures.py`; the 12 AP=1.000 precision failures
  must vanish and P03 must be reclassified as an extraction gap.

### Task 3 — Add the `in_statement` factor (HOLD, needs a sealed round)

`x1.5` when the citation is **not** reachable from the statement closure.
P(useful | not in statement) = 0.700 vs 0.239 in statement; the split survives
conditioning on role (within explicit-arg: 0.723 vs 0.449).

- **Failures addressed on top of Task 1:** 5 — P31, R01, R02, R10, R13; P28
  degrades from a rank-1 defect to a top-4 defect.
- **Cost:** it promotes not-in-statement *junk* too. One new rank-1 failure on
  TEST-R (`proof_0342`: a match-arm `ctorIdx` graded `[0,1,0]` rises to rank 1).
  More seriously, on **TEST-C it costs AP**: 0.8782 -> 0.8715 and clean@1
  0.850 -> 0.842, while gaining on TEST-R (0.9018 -> 0.9059) and CAL
  (0.8741 -> 0.8877). The gain is split-dependent; Task 1's is not.
- **Recommendation:** do not bundle with Task 1. Ship Task 1, then test this
  alone on a fresh split as a second factor that must earn its place.

### Task 4 — Resolve the frozen-rarity ceiling (RESEARCH)

12% of graded candidates saturate IDF50 at 12.9724, and in deep proofs that is
most of the list; order then falls to array index (P28, P31, P32, R13, all
with `score_gap = 0.0000`).

- **Failures addressed:** 4 directly, plus an unknown tail of index-order
  luck across the 360 proofs.
- **Options, all append-safe:**
  (a) deepen the frozen foundation (depth <= 100 instead of <= 50) — cheapest,
      but only moves the ceiling, does not remove it;
  (b) add a deterministic tie-break on `delta_depth` — cheap, and the data
      supports it (non-instance `delta_depth == 1` has P(useful) = 0.972 vs
      0.300 at delta >= 31), but the multiplicative form was tested here and
      did **not** pay (TEST-R flat, TEST-C -0.005), so it belongs as a
      *tie-break*, not a factor;
  (c) accept the tie and report it — ties are honest, index order is not.
- **Cost:** (a) weakens the append-safety story slightly (a larger frozen
  foundation is still frozen, but must be re-frozen and re-sealed).
- **Test:** measure the number of exact score ties per proof before and after;
  that is the direct endpoint, not AP.

### Task 5 — Fix the nested-occurrence role attribution (RESEARCH)

P13 is the clean instance: `UInt64.size` is credited explicit-arg (0.7)
because it occurs as an argument, but the enclosing application sits inside a
*type*, so the occurrence is not a proof step. `blame[role].would_fix = True`
confirms the mis-attribution mechanically.

- **Failures addressed:** 1 observed (P13); likely a small systematic tail —
  `only explicit-arg` has P(useful) 0.563 with the highest disagreement of any
  bucket (0.42), consistent with it being a mixture of two populations.
- **Property needed:** for each occurrence, whether any enclosing application
  along the spine is itself in a type/instance position. Computable from the
  kernel term traversal already run by `build_incidence.py`; **no name-string
  matching**. It is one extra bit per occurrence in the `vo` role vector.
- **Cost:** requires re-extracting the incidence table (the `vo` role rows are
  the source of truth and do not carry nesting context today).
- **Test:** re-derive roles with the extra bit, confirm the `explicit-arg`
  bucket splits into two populations with materially different P(useful),
  and only then propose a weight.

### Task 6 — Recover simp-discharged citations (CORPUS, out of scope for ranking)

P03 (`Frm.id_apply`) is unwinnable because the lemmas that do the work never
appear in the kernel term — `simp` leaves `of_eq_true`/`eq_self` residue.
All three raters flagged this independently and unprompted.

- **Failures addressed:** 1 observed, but this is a *ceiling* on the whole
  method: no ranking can surface content the extractor cannot see.
- **Test:** measure how many TEST-R proofs contain `of_eq_true` or `eq_self`
  in the candidate list *and* have `n_useful <= 1` — that is the size of the
  blind spot.

### Not proposed, explicitly

- **Blanket auto-generated demotion.** Re-checked against this data: 68.8%
  useful vs a 31.4% base rate. The earlier negative result stands and is
  explained.
- **Promoting `rfl` / `Eq.refl` / `id`.** They drive 10 of the 17 trade-off
  cases, but corpus-wide they are graded 0–1 more often than 2. Their low rank
  is correct on average; §4.1 argues the CORE labels on them are the error.
- **Any live-popularity or in-degree signal.** Forbidden by append-safety, and
  nothing in this bank needs it.
