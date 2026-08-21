# Global map structure: E4_flat vs E4 vs EL0

Run label: **SMOKE — v7_backup frozen arrays, OLD (buggy, inflated) in_stmt_world flag**

Data: `/Users/sam/my-repos/research/Map_Of_Mathematics/studies/phase6_stable_local_geometry/data/v7_backup`
Modules: `/Users/sam/mathmap_data/all_modules.tsv` (present=True)

Areas are validation-only evidence of human organization. They never
enter the ordering or the admission rule.

Code: `src/map_graph.py` (Task 1), `src/map_analysis.py` (Tasks 2-3),
`src/map_report.py` (this file), `src/check_map_graph.py` (brute-force
reference check), `src/el0_sensitivity.py`, `src/run_final.sh`.
Artifacts: `data/map/` (Louvain run), `data/map_lpa/` (label-propagation
cross-check), `logs/map_analysis*.log`.

## Method

Edges run `target_decl -> candidate_decl`, one block of candidates per
artifact, restricted to artifacts whose `is_generated` is False.
Candidates are ordered by `(dem, lane, stmt, -depth, position)`:

- `dem` 0 for load-bearing occurrences (roles applied / let-value /
  explicit-arg / unresolved), 1 for the U1D demoted entry (non-Prop
  declarations cited only through non-load roles).
- `lane` 2 when the candidate's minimum role tier is instance-only,
  else 1 when `depth_stmt <= 1` (transport), else 0 (move).
- `stmt` the incidence's `in_stmt_world` flag; proof-introduced (0) first.
- `depth` the cited declaration's value depth (`d_cite`, verified equal
  to `nodes.depth[decl]`); deepest first.
- `position` the incidence's index inside its artifact row block. Row
  blocks are NOT sorted by declaration id (checked: 35/2931 sampled
  blocks are ascending), so this approximates extractor term order.

Generated candidates are redirected to the longest proper dot-prefix
that is an existing non-generated declaration; a generated candidate
owned by the artifact's own target is internal and dropped, as is one
with no owner. Redirected candidates take the owner's `depth_stmt` and
node depth and never receive lane 2. Candidates are deduplicated after
redirect, keeping the best key. Self-loops are dropped.

`E4_flat` is the control: top-4 by `(role tier, position)` over
load-bearing candidates only, no lanes, no redirect.

The admission code was checked against a brute-force Python
reimplementation on 400 random artifacts: 0 mismatches for E4 and EL0.

### Reading the class shares honestly

Hub classes are assigned with precedence
`notation > generated > transport > mathematics`, where `transport` is
`depth_stmt <= 1`, `notation` is a lookup in the seven-name observed
interface set, and `mathematics` is the residual.

**The transport share of EL0 is zero by construction**: EL0 is defined
as lane 0, and lane 1 is exactly `depth_stmt <= 1`. So EL0's
"mathematics" share is not independent evidence. Two diagnostics that
are independent of the construction are reported alongside it: the
notation share (all seven interface constants have `depth_stmt = 2`, so
they are lane 0 and survive EL0), and the share of cross-area link mass
landing in the infrastructure AREAS (Core, Tactic, Util, Lean, ...),
which is a pure human-organization label.

## Admitted edge sets

| set | edges | source decls | target decls | nodes |
|---|---|---|---|---|
| E4_flat | 1482782 | 427780 | 208164 | 505561 |
| E4 | 1704084 | 442376 | 251369 | 464320 |
| EL0 | 1155016 | 333079 | 223091 | 381396 |

EL0 admission budget k per artifact (dem=0, lane=0, stmt=0):

| mean | median | p90 | p99 | max | k=0 share | mean given k>0 |
|---|---|---|---|---|---|---|
| 2.61 | 1 | 6 | 20 | 143 | 0.248 | 3.47 |

Where the EL0 budget comes from (same candidate pool, successively
dropping keys). The `stmt` key is the one whose input flag is being
rebuilt, so EL0's final size is the least settled number here:

| filter | edges | mean k | median | p90 | max | k=0 share |
|---|---|---|---|---|---|---|
| EL0 (dem0 lane0 stmt0) | 1155016 | 2.61 | 1 | 6 | 143 | 0.248 |
| dem0 lane0 (no stmt key) | 2564290 | 5.79 | 3 | 13 | 228 | 0.112 |
| dem0 (load-bearing only) | 5464116 | 12.34 | 7 | 29 | 328 | 0.038 |
| all candidates | 12008405 | 27.13 | 18 | 58 | 631 | 0.001 |

Candidate pool (12059181 rows): U1D-demoted 0.544; lane 0/1/2 = 0.250/0.428/0.322; stmt=1 0.768.

## Area distribution (validation labels)

33 areas over 771129 declarations.

| area | decls |
|---|---|
| Core | 203227 |
| Algebra | 100743 |
| CategoryTheory | 76896 |
| Analysis | 50546 |
| Topology | 48040 |
| Data | 44522 |
| RingTheory | 38328 |
| Order | 33258 |
| LinearAlgebra | 22078 |
| MeasureTheory | 19381 |
| GroupTheory | 17060 |
| Tactic | 16138 |
| Combinatorics | 15857 |
| NumberTheory | 14262 |
| AlgebraicGeometry | 10573 |
| Geometry | 10220 |
| AlgebraicTopology | 9712 |
| Probability | 6436 |
| FieldTheory | 5568 |
| SetTheory | 5550 |
| (13 smaller areas) | 22734 |

## Headline three-way comparison

| metric | E4_flat | E4 | EL0 |
|---|---|---|---|
| edges | 1482782 | 1704084 | 1155016 |
| largest component (nodes) | 499909 | 463478 | 345393 |
| LCC share of active nodes | 0.989 | 0.998 | 0.906 |
| cross-area mass -> mathematics | 0.257 | 0.502 | 0.954 |
| cross-area mass -> transport | 0.650 | 0.337 | 0.000 |
| cross-area mass -> notation | 0.086 | 0.160 | 0.046 |
| cross-area mass -> generated | 0.007 | 0.000 | 0.000 |
| same-area mass -> mathematics | 0.561 | 0.732 | 0.985 |
| within-area edge share | 0.532 | 0.681 | 0.627 |
| edges landing in a meta area (Core/Tactic/...) | 0.543 | 0.390 | 0.296 |
| cross-area mass -> meta areas (Core/Tactic/...) | 0.678 | 0.478 | 0.320 |
| top-100 hubs' share of all links | 0.407 | 0.202 | 0.119 |
| top-100 hubs' share of cross-area links | 0.656 | 0.420 | 0.222 |
| AMI (communities vs areas) | 0.2117 | 0.3664 | 0.3775 |
| communities | 194 | 65 | 376 |
| modularity | 0.600 | 0.697 | 0.740 |
| distance AUC (same vs cross) | 0.5407 | 0.6024 | 0.5954 |
| mean dist same-area | 3.565 | 4.185 | 5.451 |
| mean dist cross-area | 3.712 | 4.519 | 5.920 |
| delta_depth median (all) | 27 | 12 | 22 |
| delta_depth median (cross-area) | 62 | 31 | 62 |

## What the numbers say

Every structural metric orders the three admissions the same way, and the
gap between the control and the laned admissions is large:

1. **Hub cleanliness.** Under the flat control, 65% of cross-area link mass
   lands on transport and another 9% on the seven interface constants; only
   26% reaches anything else. E4 halves that (50% mathematics), EL0 removes
   transport by construction and leaves 4.6% notation. The
   construction-independent version of the same statement: the share of
   admitted edges whose destination sits in an infrastructure AREA falls
   0.543 -> 0.390 -> 0.296, and the share of all link mass absorbed by the
   top-100 hubs falls 0.407 -> 0.202 -> 0.119. That third number is the
   important one — the flat map is a star graph around `Eq.mpr`, `congrArg`
   and `rfl`; EL0 is not.
2. **Communities recover areas.** AMI 0.2117 -> 0.3664 -> 0.3775 under
   Louvain, and 0.1445 -> 0.2631 -> 0.2476 under label propagation. Both
   algorithms agree that the laned admissions roughly double the agreement
   with human area labels, and both put E4 and EL0 close together. Modularity
   rises monotonically as well (0.600 -> 0.697 -> 0.740).
3. **Distance stops being fake.** In the flat map every theorem pair is 3-4
   hops apart whether or not it shares an area (AUC 0.5407, and the same-area
   and cross-area histograms are nearly identical). E4 and EL0 stretch the
   metric — mean 4.2/5.5 same-area against 4.5/5.9 cross-area — and separate
   the two populations at AUC ~0.60. Re-draws put the sampling noise around
   +/-0.02, so E4 and EL0 are not distinguishable here; both clearly beat flat.
4. **Verticality.** E4 makes the smallest abstraction jumps (median
   delta_depth 12 overall, 31 across areas) against flat's 27/62. EL0 sits in
   between at 22/62 — dropping transport and statement vocabulary leaves the
   proof-plumbing recursors (`Exists.casesOn`, `Eq.rec`), which are shallow,
   so EL0's cross-area edges span as much depth as the flat control's. No
   edge set produces meaningful negative jumps (frac <= 0 is ~0.001).

### The surprise, and the limit of the notation set

The seven-name interface set is too narrow. All seven constants have
`depth_stmt = 2`, so the transport lane does not catch them and they survive
into EL0 — `OfNat.ofNat` alone is EL0's largest hub at 17178 in-links, cited
from 30 of the 32 areas. Worse, EL0's next-largest hubs are
`Lean.TSyntax.mk`, `Lean.TSyntax.raw`, `MonadExcept.throw`, `Exists.casesOn`,
`HAppend.hAppend`, `And.casesOn`, `Eq.rec` — all scored "mathematics" by the
residual rule, none of it mathematics. Two things are mixed in here:
Lean metaprogramming (Mathlib's own tactic sources are human-written
declarations and so are admitted as artifacts — the Tactic area absorbs 14%
of EL0's cross-area mass) and the `casesOn`/`rec` eliminator family. The
"mathematics" share of EL0 is therefore an upper bound, not a measurement.

Against that, the per-area tables are genuinely encouraging: Algebra's
top cross-area mediators under EL0 are `Finset.sum_congr`, `RingHom.id`,
`mul_one`, `one_ne_zero`, `Algebra.algebraMap`, `LinearEquiv.symm`. Those are
the real interfaces between algebra and everything else. Under the flat
control the same slot is filled with `Eq.mpr` and `congrArg`.

Answering the question as posed — do cross-area mediators differ from
within-area hubs? Under E4 they do, and in the good direction: pooled over
areas, the top-15 within-area hubs are 41.5% transport / 57.4% mathematics
while the top-15 cross-area mediators are 24.1% transport / 74.0%
mathematics. Under the flat control the two lists are indistinguishable
(54.8% vs 59.5% mathematics) — the flat ordering gives no signal about what
mediates between areas. Under EL0 both lists are ~98% "mathematics", which
mostly says the classification has run out of resolution.

Note the two levels do not agree, and both are worth keeping. Per-area
top-15 lists say cross-area mediators are *more* mathematical than
within-area hubs (under E4). Global cross-area link *mass* says the opposite
(50.2% mathematics cross-area vs 73.2% same-area). Both are true: a handful
of universal Core constants (`OfNat.ofNat`, `rfl`, `Membership.mem`,
`DFunLike.coe`) absorb 42% of E4's cross-area mass and never appear in a
mathematical area's own top-15. Cross-area traffic is bimodal — a plumbing
trunk plus a thin layer of genuine interfaces — and the admission rule
controls the ratio, not the existence of the trunk.

## 1. Relative hubs

### E4_flat

| link population | links | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| all_edges | 1482782 | 0.419 | 0.487 | 0.047 | 0.047 |
| same_area | 789557 | 0.561 | 0.344 | 0.013 | 0.082 |
| cross_area | 693225 | 0.257 | 0.650 | 0.086 | 0.007 |

Pooled class composition of the per-area top-15 lists:

| list | n | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| within_area_hubs | 465 | 0.548 | 0.398 | 0.006 | 0.047 |
| cross_area_mediators | 373 | 0.595 | 0.383 | 0.013 | 0.008 |

Global top hubs by total in-degree (top 15 of 100 scored):

| hub | in-degree | in-cross | class | area | areas citing |
|---|---|---|---|---|---|
| `Eq.mpr` | 76339 | 63841 | transport | Core | 30 |
| `congrArg` | 74949 | 58323 | transport | Core | 29 |
| `rfl` | 26488 | 22852 | transport | Core | 29 |
| `id` | 24836 | 18617 | transport | Core | 31 |
| `of_eq_true` | 22261 | 15632 | transport | Core | 28 |
| `Eq.refl` | 20891 | 19023 | transport | Core | 29 |
| `HMul.hMul` | 20387 | 18212 | notation | Core | 28 |
| `Iff.mpr` | 16879 | 15437 | transport | Core | 28 |
| `Membership.mem` | 16300 | 14590 | notation | Core | 27 |
| `OfNat.ofNat` | 13326 | 10163 | notation | Core | 30 |
| `Pure.pure` | 12779 | 5256 | transport | Core | 29 |
| `Real` | 12140 | 11893 | transport | Data | 19 |
| `Iff.intro` | 10888 | 9826 | transport | Core | 28 |
| `Eq.mp` | 7024 | 5736 | transport | Core | 28 |
| `Eq.ndrec` | 6439 | 3422 | transport | Core | 29 |

Top-100 hubs absorb 0.407 of all links and 0.656 of cross-area links; classes {'notation': 7, 'generated': 0, 'transport': 67, 'mathematics': 26}.

Cross-area link mass by hub AREA (area-based, independent of the lane construction):

| hub area | cross-links | share |
|---|---|---|
| Core | 464641 | 0.670 |
| Data | 70528 | 0.102 |
| Algebra | 52527 | 0.076 |
| Order | 33456 | 0.048 |
| CategoryTheory | 20760 | 0.030 |
| Topology | 11695 | 0.017 |
| Logic | 11479 | 0.017 |
| Tactic | 5245 | 0.008 |
| LinearAlgebra | 4699 | 0.007 |
| Analysis | 3808 | 0.005 |
| Combinatorics | 3357 | 0.005 |
| MeasureTheory | 3138 | 0.005 |

**Core** (203227 decls, in-same 328400, in-cross 464641)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `congrArg` | 16626 | transport | `Eq.mpr` | 63841 | transport |
| 2 | `Eq.mpr` | 12498 | transport | `congrArg` | 58323 | transport |
| 3 | `Pure.pure` | 7523 | transport | `rfl` | 22852 | transport |
| 4 | `of_eq_true` | 6629 | transport | `Eq.refl` | 19023 | transport |
| 5 | `id` | 6219 | transport | `id` | 18617 | transport |
| 6 | `Bind.bind` | 4513 | transport | `HMul.hMul` | 18212 | notation |
| 7 | `rfl` | 3636 | transport | `of_eq_true` | 15632 | transport |
| 8 | `OfNat.ofNat` | 3163 | notation | `Iff.mpr` | 15437 | transport |

**Data** (44522 decls, in-same 30457, in-cross 70528)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `Finset.univ` | 359 | transport | `Real` | 11893 | transport |
| 2 | `Set.ext` | 353 | mathematics | `DFunLike.coe` | 6005 | notation |
| 3 | `DFunLike.coe` | 319 | notation | `Opposite` | 5832 | transport |
| 4 | `Set.ofPred` | 304 | transport | `Set.ofPred` | 3372 | transport |
| 5 | `Real` | 247 | transport | `Set.univ` | 1999 | transport |
| 6 | `Multiset.map` | 240 | transport | `Set.ext` | 1879 | mathematics |
| 7 | `Set.Elem` | 240 | transport | `Finset.univ` | 1812 | transport |
| 8 | `Finset.ext` | 237 | mathematics | `SetLike.coe` | 1707 | mathematics |

**Algebra** (100743 decls, in-same 87158, in-cross 52527)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `Polynomial.C` | 752 | mathematics | `RingHom.id` | 2509 | mathematics |
| 2 | `Units.val` | 669 | mathematics | `Algebra.algebraMap` | 2417 | mathematics |
| 3 | `RingHom.id` | 614 | mathematics | `Units.val` | 1222 | mathematics |
| 4 | `Algebra.algebraMap` | 605 | mathematics | `LinearEquiv.symm` | 1126 | mathematics |
| 5 | `MulOpposite` | 581 | transport | `LinearMap` | 853 | mathematics |
| 6 | `HomologicalComplex.Hom.f` | 467 | mathematics | `Polynomial.C` | 751 | mathematics |
| 7 | `CategoryTheory.ShortComplex.X₁` | 434 | mathematics | `Submodule` | 593 | mathematics |
| 8 | `ModuleCat` | 368 | transport | `CommRingCat.carrier` | 557 | transport |

**Order** (33258 decls, in-same 32141, in-cross 33456)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `Bot.bot` | 491 | transport | `le_antisymm` | 1210 | mathematics |
| 2 | `iInf` | 413 | transport | `le_refl` | 1125 | mathematics |
| 3 | `OrderDual` | 407 | transport | `Bot.bot` | 1085 | transport |
| 4 | `OrderDual.toDual` | 406 | transport | `Compl.compl` | 1052 | transport |
| 5 | `Set.Ici` | 320 | transport | `Top.top` | 1021 | transport |
| 6 | `iSup` | 313 | transport | `iInf` | 972 | transport |
| 7 | `lowerBounds` | 287 | transport | `iSup` | 781 | transport |
| 8 | `OrderDual.ofDual` | 286 | transport | `Set.Ioi` | 764 | transport |

**CategoryTheory** (76896 decls, in-same 105891, in-cross 20760)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `CategoryTheory.Category.assoc` | 4279 | mathematics | `CategoryTheory.Category.assoc` | 2049 | mathematics |
| 2 | `CategoryTheory.Functor.comp` | 3676 | mathematics | `CategoryTheory.ConcreteCategory.hom` | 1469 | mathematics |
| 3 | `CategoryTheory.Functor` | 2876 | transport | `CategoryTheory.Functor.comp` | 1040 | mathematics |
| 4 | `CategoryTheory.CategoryStruct.id` | 2039 | mathematics | `CategoryTheory.Functor.op` | 552 | mathematics |
| 5 | `CategoryTheory.Functor.map` | 1354 | mathematics | `CategoryTheory.CategoryStruct.id` | 516 | mathematics |
| 6 | `CategoryTheory.Functor.obj` | 1326 | mathematics | `CategoryTheory.Functor.map` | 488 | mathematics |
| 7 | `CategoryTheory.CategoryStruct.comp` | 1230 | mathematics | `CategoryTheory.CategoryStruct.comp` | 481 | mathematics |
| 8 | `CategoryTheory.Functor.id` | 1014 | mathematics | `CategoryTheory.Functor.mk` | 466 | mathematics |

**Topology** (48040 decls, in-same 40417, in-cross 11695)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `nhds` | 912 | transport | `nhds` | 599 | transport |
| 2 | `TopCat.carrier` | 486 | transport | `ContinuousLinearMap.comp` | 516 | mathematics |
| 3 | `Continuous` | 374 | transport | `ContinuousLinearMap` | 510 | mathematics |
| 4 | `uniformity` | 372 | transport | `TopologicalSpace.Opens` | 415 | transport |
| 5 | `TopologicalSpace.Opens` | 329 | transport | `nhdsWithin` | 310 | transport |
| 6 | `nhdsWithin` | 306 | transport | `ContinuousLinearEquiv.symm` | 184 | mathematics |
| 7 | `ContinuousMap.mk` | 297 | mathematics | `ContinuousMultilinearMap` | 158 | mathematics |
| 8 | `PartialHomeomorph.toPartialEquiv` | 292 | mathematics | `Continuous` | 157 | transport |

### E4

| link population | links | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| all_edges | 1704084 | 0.658 | 0.278 | 0.064 | 0.000 |
| same_area | 1159917 | 0.732 | 0.250 | 0.018 | 0.000 |
| cross_area | 544167 | 0.502 | 0.337 | 0.160 | 0.000 |

Pooled class composition of the per-area top-15 lists:

| list | n | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| within_area_hubs | 465 | 0.574 | 0.415 | 0.011 | 0.000 |
| cross_area_mediators | 381 | 0.740 | 0.241 | 0.018 | 0.000 |

Global top hubs by total in-degree (top 15 of 100 scored):

| hub | in-degree | in-cross | class | area | areas citing |
|---|---|---|---|---|---|
| `OfNat.ofNat` | 40167 | 28299 | notation | Core | 30 |
| `rfl` | 22283 | 18572 | transport | Core | 29 |
| `Membership.mem` | 18740 | 16641 | notation | Core | 29 |
| `DFunLike.coe` | 18193 | 17061 | notation | Data | 28 |
| `HAdd.hAdd` | 11447 | 8722 | notation | Core | 30 |
| `HMul.hMul` | 10428 | 8850 | notation | Core | 29 |
| `Eq.refl` | 9512 | 6847 | transport | Core | 29 |
| `RingHom.id` | 8114 | 6431 | mathematics | Algebra | 19 |
| `Nat` | 6908 | 3538 | transport | Core | 30 |
| `Eq.ndrec` | 5474 | 2300 | transport | Core | 29 |
| `HSub.hSub` | 5257 | 3619 | notation | Core | 29 |
| `Lean.TSyntax.mk` | 5022 | 3781 | mathematics | Core | 28 |
| `Lean.TSyntax.raw` | 4682 | 3462 | mathematics | Core | 28 |
| `id` | 4648 | 1738 | transport | Core | 27 |
| `LE.le` | 4342 | 3685 | transport | Core | 27 |

Top-100 hubs absorb 0.202 of all links and 0.420 of cross-area links; classes {'notation': 7, 'generated': 0, 'transport': 63, 'mathematics': 30}.

Cross-area link mass by hub AREA (area-based, independent of the lane construction):

| hub area | cross-links | share |
|---|---|---|
| Core | 253428 | 0.466 |
| Algebra | 83299 | 0.153 |
| Data | 78606 | 0.144 |
| Order | 35863 | 0.066 |
| CategoryTheory | 21905 | 0.040 |
| Topology | 16535 | 0.030 |
| Logic | 10891 | 0.020 |
| LinearAlgebra | 9732 | 0.018 |
| MeasureTheory | 6728 | 0.012 |
| Tactic | 6433 | 0.012 |
| Analysis | 5736 | 0.011 |
| RingTheory | 4436 | 0.008 |

**Core** (203227 decls, in-same 393824, in-cross 253428)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `OfNat.ofNat` | 11868 | notation | `OfNat.ofNat` | 28299 | notation |
| 2 | `rfl` | 3711 | transport | `rfl` | 18572 | transport |
| 3 | `Nat` | 3370 | transport | `Membership.mem` | 16641 | notation |
| 4 | `Eq.ndrec` | 3174 | transport | `HMul.hMul` | 8850 | notation |
| 5 | `id` | 2910 | transport | `HAdd.hAdd` | 8722 | notation |
| 6 | `HAdd.hAdd` | 2725 | notation | `Eq.refl` | 6847 | transport |
| 7 | `Eq.refl` | 2665 | transport | `HSMul.hSMul` | 4133 | notation |
| 8 | `HAppend.hAppend` | 2508 | mathematics | `Lean.TSyntax.mk` | 3781 | mathematics |

**Algebra** (100743 decls, in-same 144669, in-cross 83299)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `RingHom.id` | 1683 | mathematics | `RingHom.id` | 6431 | mathematics |
| 2 | `MulOpposite` | 521 | transport | `Module` | 1106 | transport |
| 3 | `HVAdd.hVAdd` | 473 | mathematics | `LinearMap` | 882 | mathematics |
| 4 | `Units.val` | 444 | mathematics | `Algebra.algebraMap` | 828 | mathematics |
| 5 | `Polynomial.C` | 422 | mathematics | `Algebra` | 733 | transport |
| 6 | `HomologicalComplex.X` | 404 | mathematics | `CommRing` | 693 | transport |
| 7 | `CommRing` | 345 | transport | `HVAdd.hVAdd` | 639 | mathematics |
| 8 | `Algebra.algebraMap` | 337 | mathematics | `Finset.sum_congr` | 604 | mathematics |

**Data** (44522 decls, in-same 48247, in-cross 78606)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `DFunLike.coe` | 1132 | notation | `DFunLike.coe` | 17061 | notation |
| 2 | `Set` | 963 | transport | `SetLike.coe` | 3101 | mathematics |
| 3 | `Finset` | 699 | transport | `Real` | 2328 | transport |
| 4 | `Multiset` | 321 | transport | `Set` | 1923 | transport |
| 5 | `Set.ext` | 302 | mathematics | `ENat` | 1202 | transport |
| 6 | `SetLike.coe` | 273 | mathematics | `Set.ext` | 873 | mathematics |
| 7 | `ENNReal` | 251 | transport | `Opposite` | 847 | transport |
| 8 | `NNReal` | 249 | transport | `Set.Elem` | 787 | transport |

**Order** (33258 decls, in-same 47317, in-cross 35863)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `Preorder` | 735 | transport | `Top.top` | 925 | transport |
| 2 | `OrderDual` | 515 | transport | `Bot.bot` | 601 | transport |
| 3 | `Filter` | 502 | transport | `OrderDual` | 578 | transport |
| 4 | `Bot.bot` | 324 | transport | `Disjoint` | 556 | mathematics |
| 5 | `LinearOrder` | 281 | transport | `LE.le.trans` | 516 | mathematics |
| 6 | `OrderDual.toDual` | 280 | transport | `le_rfl` | 413 | mathematics |
| 7 | `Preorder.toLE` | 255 | transport | `Preorder` | 370 | transport |
| 8 | `Top.top` | 248 | transport | `LT.lt.le` | 331 | mathematics |

**CategoryTheory** (76896 decls, in-same 155615, in-cross 21905)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `CategoryTheory.Functor.obj` | 2987 | mathematics | `CategoryTheory.Functor.obj` | 1077 | mathematics |
| 2 | `CategoryTheory.Functor.comp` | 2957 | mathematics | `CategoryTheory.ConcreteCategory.hom` | 928 | mathematics |
| 3 | `CategoryTheory.Category` | 2230 | transport | `CategoryTheory.Functor.comp` | 733 | mathematics |
| 4 | `CategoryTheory.Functor` | 1564 | transport | `CategoryTheory.Functor.map` | 501 | mathematics |
| 5 | `CategoryTheory.Functor.map` | 1457 | mathematics | `CategoryTheory.forget` | 409 | mathematics |
| 6 | `CategoryTheory.CategoryStruct.comp` | 1304 | mathematics | `CategoryTheory.CategoryStruct.comp` | 387 | mathematics |
| 7 | `CategoryTheory.Functor.const` | 1122 | mathematics | `CategoryTheory.forget₂` | 356 | mathematics |
| 8 | `CategoryTheory.NatTrans.app` | 1035 | mathematics | `CategoryTheory.Iso.hom` | 317 | mathematics |

**Topology** (48040 decls, in-same 65435, in-cross 16535)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `TopologicalSpace` | 1914 | transport | `ContinuousLinearMap` | 577 | mathematics |
| 2 | `nhds` | 771 | transport | `nhds` | 323 | transport |
| 3 | `ContinuousMap` | 404 | transport | `TopologicalSpace` | 286 | transport |
| 4 | `nhdsWithin` | 338 | transport | `tsum` | 222 | mathematics |
| 5 | `TopCat.carrier` | 293 | transport | `nhdsWithin` | 184 | transport |
| 6 | `PartialHomeomorph.toPartialEquiv` | 261 | mathematics | `ContinuousLinearMap.comp` | 165 | mathematics |
| 7 | `UniformSpace` | 253 | transport | `TopologicalSpace.Opens.map` | 161 | mathematics |
| 8 | `Homeomorph.symm` | 245 | mathematics | `ContinuousMultilinearMap` | 126 | mathematics |

### EL0

| link population | links | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| all_edges | 1155016 | 0.974 | 0.000 | 0.026 | 0.000 |
| same_area | 724410 | 0.985 | 0.000 | 0.015 | 0.000 |
| cross_area | 430606 | 0.954 | 0.000 | 0.046 | 0.000 |

Pooled class composition of the per-area top-15 lists:

| list | n | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| within_area_hubs | 463 | 0.991 | 0.000 | 0.009 | 0.000 |
| cross_area_mediators | 390 | 0.982 | 0.000 | 0.018 | 0.000 |

Global top hubs by total in-degree (top 15 of 100 scored):

| hub | in-degree | in-cross | class | area | areas citing |
|---|---|---|---|---|---|
| `OfNat.ofNat` | 17178 | 9041 | notation | Core | 30 |
| `Lean.TSyntax.mk` | 5324 | 3911 | mathematics | Core | 28 |
| `Lean.TSyntax.raw` | 5244 | 3735 | mathematics | Core | 28 |
| `DFunLike.coe` | 4742 | 4358 | notation | Data | 27 |
| `MonadExcept.throw` | 4239 | 3198 | mathematics | Core | 28 |
| `Exists.casesOn` | 3881 | 3489 | mathematics | Core | 27 |
| `HAppend.hAppend` | 3782 | 770 | mathematics | Core | 22 |
| `And.casesOn` | 2591 | 2357 | mathematics | Core | 25 |
| `HAdd.hAdd` | 2435 | 1341 | notation | Core | 30 |
| `Membership.mem` | 2316 | 2087 | notation | Core | 26 |
| `Mathlib.Tactic.Reassoc.eq_whisker'` | 1846 | 1842 | mathematics | Tactic | 8 |
| `Eq.casesOn` | 1820 | 1624 | mathematics | Core | 27 |
| `HSub.hSub` | 1719 | 950 | notation | Core | 29 |
| `Singleton.singleton` | 1529 | 1522 | mathematics | Core | 26 |
| `Eq.rec` | 1527 | 1124 | mathematics | Core | 24 |

Top-100 hubs absorb 0.119 of all links and 0.222 of cross-area links; classes {'notation': 7, 'generated': 0, 'transport': 0, 'mathematics': 93}.

Cross-area link mass by hub AREA (area-based, independent of the lane construction):

| hub area | cross-links | share |
|---|---|---|
| Algebra | 100576 | 0.234 |
| Core | 77334 | 0.180 |
| Data | 69256 | 0.161 |
| Tactic | 60228 | 0.140 |
| Order | 38728 | 0.090 |
| Topology | 19975 | 0.046 |
| CategoryTheory | 18914 | 0.044 |
| LinearAlgebra | 9719 | 0.023 |
| Analysis | 8244 | 0.019 |
| MeasureTheory | 8104 | 0.019 |
| Logic | 6386 | 0.015 |
| RingTheory | 5709 | 0.013 |

**Algebra** (100743 decls, in-same 91733, in-cross 100576)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `mul_one` | 417 | mathematics | `Finset.sum_congr` | 891 | mathematics |
| 2 | `mul_comm` | 348 | mathematics | `RingHom.id` | 783 | mathematics |
| 3 | `Finset.sum_congr` | 300 | mathematics | `mul_one` | 636 | mathematics |
| 4 | `add_comm` | 279 | mathematics | `one_ne_zero` | 561 | mathematics |
| 5 | `one_mul` | 269 | mathematics | `Algebra.algebraMap` | 556 | mathematics |
| 6 | `add_zero` | 262 | mathematics | `LinearEquiv.symm` | 510 | mathematics |
| 7 | `mul_assoc` | 259 | mathematics | `mul_comm` | 509 | mathematics |
| 8 | `zero_add` | 255 | mathematics | `zero_add` | 412 | mathematics |

**Core** (203227 decls, in-same 199252, in-cross 77334)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `OfNat.ofNat` | 8137 | notation | `OfNat.ofNat` | 9041 | notation |
| 2 | `HAppend.hAppend` | 3012 | mathematics | `Lean.TSyntax.mk` | 3911 | mathematics |
| 3 | `Lean.TSyntax.raw` | 1509 | mathematics | `Lean.TSyntax.raw` | 3735 | mathematics |
| 4 | `Lean.TSyntax.mk` | 1413 | mathematics | `Exists.casesOn` | 3489 | mathematics |
| 5 | `GetElem.getElem` | 1281 | mathematics | `MonadExcept.throw` | 3198 | mathematics |
| 6 | `ForIn.forIn` | 1098 | mathematics | `And.casesOn` | 2357 | mathematics |
| 7 | `HAdd.hAdd` | 1094 | notation | `Membership.mem` | 2087 | notation |
| 8 | `MonadExcept.throw` | 1041 | mathematics | `Eq.casesOn` | 1624 | mathematics |

**Data** (44522 decls, in-same 31460, in-cross 69256)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `DFunLike.coe` | 384 | notation | `DFunLike.coe` | 4358 | notation |
| 2 | `Set.ext` | 292 | mathematics | `SetLike.coe` | 997 | mathematics |
| 3 | `Finset.ext` | 208 | mathematics | `Set.ext` | 931 | mathematics |
| 4 | `Finsupp.ext` | 89 | mathematics | `Set.mem_singleton_iff` | 516 | mathematics |
| 5 | `Set.mem_univ` | 89 | mathematics | `SetLike.mem_coe` | 511 | mathematics |
| 6 | `Finset.mem_univ` | 89 | mathematics | `Nat.cast_one` | 498 | mathematics |
| 7 | `Nat.cast_one` | 88 | mathematics | `Set.mem_preimage` | 472 | mathematics |
| 8 | `SetLike.coe` | 85 | mathematics | `Nat.cast_zero` | 414 | mathematics |

**Tactic** (16138 decls, in-same 4173, in-cross 60228)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `Mathlib.Meta.NormNum.Result` | 76 | mathematics | `Mathlib.Tactic.Reassoc.eq_whisker'` | 1842 | mathematics |
| 2 | `Mathlib.Meta.NormNum.NormNumExt.mk` | 76 | mathematics | `Mathlib.Meta.NormNum.isNat_ofNat` | 1225 | mathematics |
| 3 | `Mathlib.Meta.NormNum.IsNat.mk` | 61 | mathematics | `Mathlib.Meta.NormNum.IsNat.of_raw` | 1199 | mathematics |
| 4 | `Mathlib.Meta.NormNum.Result.isNat` | 54 | mathematics | `Mathlib.Tactic.Ring.Common.add_pf_add_zero` | 1183 | mathematics |
| 5 | `Mathlib.Meta.NormNum.derive` | 42 | mathematics | `Mathlib.Tactic.Ring.Common.atom_pf` | 1182 | mathematics |
| 6 | `Mathlib.Meta.NormNum.deriveNat` | 37 | mathematics | `Mathlib.Meta.NormNum.IsNat.to_raw_eq` | 1115 | mathematics |
| 7 | `Mathlib.Meta.Positivity.Strictness.positive` | 37 | mathematics | `Mathlib.Tactic.Ring.Common.add_mul` | 1074 | mathematics |
| 8 | `Mathlib.Meta.Positivity.Strictness` | 34 | mathematics | `Mathlib.Tactic.Ring.Common.zero_mul` | 1074 | mathematics |

**Order** (33258 decls, in-same 30872, in-cross 38728)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `LE.le.trans` | 308 | mathematics | `LE.le.trans` | 803 | mathematics |
| 2 | `le_rfl` | 208 | mathematics | `LT.lt.le` | 724 | mathematics |
| 3 | `LT.lt.le` | 181 | mathematics | `LT.lt.ne'` | 533 | mathematics |
| 4 | `le_antisymm` | 137 | mathematics | `not_le` | 470 | mathematics |
| 5 | `Filter.Eventually.mono` | 114 | mathematics | `not_lt` | 463 | mathematics |
| 6 | `bot_le` | 111 | mathematics | `le_antisymm` | 380 | mathematics |
| 7 | `le_top` | 104 | mathematics | `LE.le.trans_lt` | 315 | mathematics |
| 8 | `RelIso.mk` | 102 | mathematics | `LT.lt.trans_le` | 300 | mathematics |

**Topology** (48040 decls, in-same 46364, in-cross 19975)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `Continuous.comp` | 244 | mathematics | `ContinuousLinearMap.comp` | 239 | mathematics |
| 2 | `IsOpen.mem_nhds` | 198 | mathematics | `OpenPartialHomeomorph.toFun'` | 143 | mathematics |
| 3 | `Homeomorph.symm` | 185 | mathematics | `Continuous.continuousOn` | 127 | mathematics |
| 4 | `subset_closure` | 161 | mathematics | `OpenPartialHomeomorph.symm` | 122 | mathematics |
| 5 | `ContinuousMap.mk` | 156 | mathematics | `tsum` | 109 | mathematics |
| 6 | `continuous_id` | 155 | mathematics | `ContinuousLinearMap.ext` | 106 | mathematics |
| 7 | `Continuous.continuousAt` | 141 | mathematics | `ContinuousLinearEquiv.toContinuousLinearMap` | 102 | mathematics |
| 8 | `Homeomorph.mk` | 134 | mathematics | `tendsto_const_nhds` | 102 | mathematics |

## 2. Community emergence

| set | method | nodes | undirected edges | subsampled | communities | >=100 | largest frac | modularity | AMI vs areas |
|---|---|---|---|---|---|---|---|---|---|
| E4_flat | louvain | 499909 | 1479524 | False | 194 | 36 | 0.205 | 0.600 | **0.2117** |
| E4 | louvain | 463478 | 1703381 | False | 65 | 29 | 0.144 | 0.697 | **0.3664** |
| EL0 | louvain | 345393 | 1131789 | False | 376 | 40 | 0.132 | 0.740 | **0.3775** |

Cross-check with a second community algorithm (vectorised weighted
label propagation, same graphs, same seed):

| set | method | communities | modularity | AMI vs areas |
|---|---|---|---|---|
| E4_flat | lpa | 26348 | 0.444 | **0.1445** |
| E4 | lpa | 11773 | 0.544 | **0.2631** |
| EL0 | lpa | 22571 | 0.566 | **0.2476** |

## 3. Distance honesty

Non-generated theorem declarations (`kind == 0`) in the largest
component with a known area. The source is drawn uniformly from that
pool; the partner is drawn uniformly from the source's own area
(same-area) or uniformly from the pool with rejection (cross-area).
Sampling the source uniformly rather than sampling pairs uniformly
keeps the large areas (Core, Algebra) from dominating the same-area
sample. Undirected BFS, capped at 12; unreachable counts as 12.

| set | pairs each | same mean | cross mean | same median | cross median | same capped | cross capped | AUC |
|---|---|---|---|---|---|---|---|---|
| E4_flat | 1500 | 3.565 | 3.712 | 4 | 4 | 0.000 | 0.000 | **0.5407** |
| E4 | 1500 | 4.185 | 4.519 | 4 | 5 | 0.000 | 0.000 | **0.6024** |
| EL0 | 1500 | 5.451 | 5.920 | 5 | 6 | 0.000 | 0.001 | **0.5954** |

E4_flat distance histogram (same / cross):

| d | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| same | 0 | 1 | 272 | 338 | 702 | 152 | 24 | 11 | 0 | 0 | 0 | 0 | 0 |
| cross | 0 | 0 | 198 | 313 | 765 | 179 | 38 | 6 | 1 | 0 | 0 | 0 | 0 |

E4 distance histogram (same / cross):

| d | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| same | 0 | 0 | 47 | 224 | 703 | 458 | 66 | 2 | 0 | 0 | 0 | 0 | 0 |
| cross | 0 | 0 | 28 | 110 | 595 | 600 | 157 | 10 | 0 | 0 | 0 | 0 | 0 |

EL0 distance histogram (same / cross):

| d | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| same | 0 | 1 | 8 | 61 | 302 | 451 | 383 | 178 | 89 | 16 | 7 | 4 | 0 |
| cross | 0 | 0 | 2 | 19 | 174 | 422 | 441 | 252 | 133 | 37 | 15 | 4 | 1 |

Sampling noise on the AUC: two independent re-draws of 750+750
pairs per edge set.

| set | re-draw 1 | re-draw 2 |
|---|---|---|
| E4_flat | 0.5345 | 0.5426 | 
| E4 | 0.6124 | 0.6196 | 
| EL0 | 0.6178 | 0.5980 | 

## 4. Verticality (delta_depth = depth[src] - depth[dst])

**all_edges**

| set | n | mean | p1 | p5 | p25 | p50 | p75 | p90 | p99 | frac <= 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| E4_flat | 1482782 | 49.2 | 1 | 1 | 5 | 27 | 74 | 127 | 250 | 0.000 |
| E4 | 1704084 | 31.1 | 1 | 1 | 2 | 12 | 48 | 86 | 190 | 0.001 |
| EL0 | 1155016 | 41.8 | 1 | 1 | 2 | 22 | 66 | 113 | 210 | 0.001 |

**same_area**

| set | n | mean | p1 | p5 | p25 | p50 | p75 | p90 | p99 | frac <= 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| E4_flat | 789557 | 27.7 | 1 | 1 | 1 | 11 | 43 | 78 | 150 | 0.000 |
| E4 | 1159917 | 21.1 | 1 | 1 | 1 | 6 | 28 | 65 | 136 | 0.002 |
| EL0 | 724410 | 24.7 | 1 | 1 | 1 | 8 | 36 | 72 | 150 | 0.001 |

**cross_area**

| set | n | mean | p1 | p5 | p25 | p50 | p75 | p90 | p99 | frac <= 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| E4_flat | 693225 | 73.6 | 1 | 3 | 20 | 62 | 102 | 170 | 277 | 0.000 |
| E4 | 544167 | 52.4 | 1 | 1 | 10 | 31 | 77 | 135 | 221 | 0.000 |
| EL0 | 430606 | 70.6 | 1 | 2 | 24 | 62 | 99 | 150 | 256 | 0.000 |


## Caveats

- **This is a SMOKE run.** It uses the frozen `data/v7_backup` copy, whose
  `in_stmt_world` flag is the old buggy one (inflated on rewriting
  machinery): 76.8% of the candidate pool is marked statement-vocabulary.
  That flag is the sole input to the `stmt` key, which more than halves EL0
  (2.56M edges without it, 1.16M with it). EL0's size, its 24.8% empty-proof
  share, and everything downstream of its graph will move on the rebuild.
  E4 and E4_flat are much less exposed: the `stmt` key is the third of five
  in E4 and absent from E4_flat.
- Areas were used only for validation. The admission code never reads them,
  and `data/map/areas.npz` is written after the edges.
- Community detection ran at full scale, no subsampling. Louvain took
  578s / 96s / 34s for the three sets; the label-propagation cross-check took
  3-7s each.
- Distance AUCs carry about +/-0.02 of sampling noise (see the re-draw table),
  so E4 vs EL0 is not resolved by this measurement.
- The "mathematics" class is a residual, and it absorbs Lean metaprogramming
  and the `casesOn`/`rec` eliminator family. Treat every "mathematics" share
  as an upper bound. The area-based diagnostics (within-area edge share,
  meta-area destination share, top-100 hub mass) do not have this problem.
- Row position within an artifact's incidence block is used as the final
  tiebreak. It is deterministic and is not a decl-id sort (verified), but it
  is the extractor's row order, not a proven term order.
