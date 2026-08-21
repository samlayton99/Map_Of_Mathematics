# Global map structure: E4_flat vs E4 vs EL0

Run label: **FINAL - rebuilt phase5 arrays, corrected in_stmt_world flag**

Data: `/Users/sam/my-repos/research/Map_Of_Mathematics/studies/phase6_stable_local_geometry/../phase5_multiscale_navigation/data`
Modules: `/Users/sam/mathmap_data/all_modules.tsv` (present=True)

Areas are validation-only evidence of human organization. They never
enter the ordering or the admission rule.

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
| E4 | 1704084 | 442376 | 250287 | 464316 |
| EL0 | 1458344 | 340135 | 224212 | 383969 |

EL0 admission budget k per artifact (dem=0, lane=0, stmt=0):

| mean | median | p90 | p99 | max | k=0 share | mean given k>0 |
|---|---|---|---|---|---|---|
| 3.29 | 2 | 7 | 30 | 202 | 0.232 | 4.29 |

Where the EL0 budget comes from (same candidate pool, successively
dropping keys). The `stmt` key is the one whose input flag is being
rebuilt, so EL0's final size is the least settled number here:

| filter | edges | mean k | median | p90 | max | k=0 share |
|---|---|---|---|---|---|---|
| EL0 (dem0 lane0 stmt0) | 1458344 | 3.29 | 2 | 7 | 202 | 0.232 |
| dem0 lane0 (no stmt key) | 2564290 | 5.79 | 3 | 13 | 228 | 0.112 |
| dem0 (load-bearing only) | 5464116 | 12.34 | 7 | 29 | 328 | 0.038 |
| all candidates | 12008405 | 27.13 | 18 | 58 | 631 | 0.001 |

Candidate pool (12059181 rows): U1D-demoted 0.544; lane 0/1/2 = 0.250/0.428/0.322; stmt=1 0.664.

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
| edges | 1482782 | 1704084 | 1458344 |
| largest component (nodes) | 499909 | 463466 | 349876 |
| LCC share of active nodes | 0.989 | 0.998 | 0.911 |
| cross-area mass -> mathematics | 0.257 | 0.512 | 0.967 |
| cross-area mass -> transport | 0.650 | 0.336 | 0.000 |
| cross-area mass -> notation | 0.086 | 0.153 | 0.033 |
| cross-area mass -> generated | 0.007 | 0.000 | 0.000 |
| same-area mass -> mathematics | 0.561 | 0.732 | 0.986 |
| within-area edge share | 0.532 | 0.669 | 0.538 |
| edges landing in a meta area (Core/Tactic/...) | 0.543 | 0.398 | 0.316 |
| cross-area mass -> meta areas (Core/Tactic/...) | 0.678 | 0.487 | 0.357 |
| top-100 hubs' share of all links | 0.407 | 0.211 | 0.176 |
| top-100 hubs' share of cross-area links | 0.656 | 0.428 | 0.303 |
| AMI (communities vs areas) | 0.2117 | 0.3420 | 0.3354 |
| communities | 194 | 75 | 365 |
| modularity | 0.600 | 0.684 | 0.675 |
| distance AUC (same vs cross) | 0.5407 | 0.5743 | 0.5666 |
| mean dist same-area | 3.565 | 4.171 | 4.749 |
| mean dist cross-area | 3.712 | 4.433 | 5.029 |
| delta_depth median (all) | 27 | 12 | 35 |
| delta_depth median (cross-area) | 62 | 34 | 82 |

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
| all_edges | 1704084 | 0.659 | 0.278 | 0.063 | 0.000 |
| same_area | 1139551 | 0.732 | 0.249 | 0.018 | 0.000 |
| cross_area | 564533 | 0.512 | 0.336 | 0.153 | 0.000 |

Pooled class composition of the per-area top-15 lists:

| list | n | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| within_area_hubs | 465 | 0.583 | 0.409 | 0.009 | 0.000 |
| cross_area_mediators | 381 | 0.753 | 0.228 | 0.018 | 0.000 |

Global top hubs by total in-degree (top 15 of 100 scored):

| hub | in-degree | in-cross | class | area | areas citing |
|---|---|---|---|---|---|
| `OfNat.ofNat` | 40039 | 28184 | notation | Core | 30 |
| `rfl` | 22630 | 18894 | transport | Core | 29 |
| `Membership.mem` | 18506 | 16417 | notation | Core | 29 |
| `DFunLike.coe` | 18263 | 17135 | notation | Data | 28 |
| `HAdd.hAdd` | 11376 | 8665 | notation | Core | 30 |
| `Eq.refl` | 10722 | 8041 | transport | Core | 29 |
| `HMul.hMul` | 9878 | 8306 | notation | Core | 29 |
| `RingHom.id` | 7756 | 6150 | mathematics | Algebra | 19 |
| `Nat` | 6908 | 3538 | transport | Core | 30 |
| `Eq.mpr` | 6014 | 4647 | transport | Core | 27 |
| `Eq.ndrec` | 5633 | 2469 | transport | Core | 29 |
| `HSub.hSub` | 5177 | 3545 | notation | Core | 29 |
| `id` | 5039 | 1923 | transport | Core | 27 |
| `Lean.TSyntax.mk` | 5022 | 3781 | mathematics | Core | 28 |
| `Lean.TSyntax.raw` | 4682 | 3462 | mathematics | Core | 28 |

Top-100 hubs absorb 0.211 of all links and 0.428 of cross-area links; classes {'notation': 7, 'generated': 0, 'transport': 63, 'mathematics': 30}.

Cross-area link mass by hub AREA (area-based, independent of the lane construction):

| hub area | cross-links | share |
|---|---|---|
| Core | 266067 | 0.471 |
| Algebra | 85881 | 0.152 |
| Data | 79122 | 0.140 |
| Order | 36734 | 0.065 |
| CategoryTheory | 24312 | 0.043 |
| Topology | 16580 | 0.029 |
| Logic | 10847 | 0.019 |
| LinearAlgebra | 9398 | 0.017 |
| Tactic | 8399 | 0.015 |
| MeasureTheory | 6581 | 0.012 |
| Analysis | 5872 | 0.010 |
| RingTheory | 4382 | 0.008 |

**Core** (203227 decls, in-same 393826, in-cross 266067)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `OfNat.ofNat` | 11855 | notation | `OfNat.ofNat` | 28184 | notation |
| 2 | `rfl` | 3736 | transport | `rfl` | 18894 | transport |
| 3 | `Nat` | 3370 | transport | `Membership.mem` | 16417 | notation |
| 4 | `Eq.ndrec` | 3164 | transport | `HAdd.hAdd` | 8665 | notation |
| 5 | `id` | 3116 | transport | `HMul.hMul` | 8306 | notation |
| 6 | `HAdd.hAdd` | 2711 | notation | `Eq.refl` | 8041 | transport |
| 7 | `Eq.refl` | 2681 | transport | `Eq.mpr` | 4647 | transport |
| 8 | `HAppend.hAppend` | 2514 | mathematics | `HSMul.hSMul` | 4104 | notation |

**Algebra** (100743 decls, in-same 141563, in-cross 85881)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `RingHom.id` | 1606 | mathematics | `RingHom.id` | 6150 | mathematics |
| 2 | `MulOpposite` | 485 | transport | `Module` | 1105 | transport |
| 3 | `HVAdd.hVAdd` | 473 | mathematics | `Finset.sum_congr` | 938 | mathematics |
| 4 | `Units.val` | 434 | mathematics | `LinearMap` | 865 | mathematics |
| 5 | `HomologicalComplex.X` | 391 | mathematics | `Algebra.algebraMap` | 826 | mathematics |
| 6 | `CommRing` | 345 | transport | `Algebra` | 733 | transport |
| 7 | `Polynomial.C` | 344 | mathematics | `CommRing` | 693 | transport |
| 8 | `Submodule` | 335 | mathematics | `HVAdd.hVAdd` | 639 | mathematics |

**Data** (44522 decls, in-same 46943, in-cross 79122)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `DFunLike.coe` | 1128 | notation | `DFunLike.coe` | 17135 | notation |
| 2 | `Set` | 963 | transport | `SetLike.coe` | 3093 | mathematics |
| 3 | `Finset` | 698 | transport | `Real` | 2325 | transport |
| 4 | `Set.ext` | 320 | mathematics | `Set` | 1929 | transport |
| 5 | `Multiset` | 318 | transport | `ENat` | 1165 | transport |
| 6 | `SetLike.coe` | 271 | mathematics | `Set.ext` | 1084 | mathematics |
| 7 | `NNReal` | 239 | transport | `Opposite` | 837 | transport |
| 8 | `Finset.ext` | 238 | mathematics | `Set.ofPred` | 732 | transport |

**Order** (33258 decls, in-same 46704, in-cross 36734)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `Preorder` | 735 | transport | `Top.top` | 918 | transport |
| 2 | `OrderDual` | 522 | transport | `OrderDual` | 593 | transport |
| 3 | `Filter` | 502 | transport | `LE.le.trans` | 580 | mathematics |
| 4 | `Bot.bot` | 318 | transport | `Bot.bot` | 564 | transport |
| 5 | `OrderDual.toDual` | 280 | transport | `Disjoint` | 529 | mathematics |
| 6 | `LinearOrder` | 276 | transport | `le_rfl` | 475 | mathematics |
| 7 | `Preorder.toLE` | 255 | transport | `Preorder` | 370 | transport |
| 8 | `Top.top` | 247 | transport | `LT.lt.le` | 337 | mathematics |

**CategoryTheory** (76896 decls, in-same 154072, in-cross 24312)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `CategoryTheory.Category.assoc` | 3095 | mathematics | `CategoryTheory.Category.assoc` | 1543 | mathematics |
| 2 | `CategoryTheory.Functor.obj` | 2957 | mathematics | `CategoryTheory.Functor.obj` | 1063 | mathematics |
| 3 | `CategoryTheory.Functor.comp` | 2732 | mathematics | `CategoryTheory.ConcreteCategory.hom` | 895 | mathematics |
| 4 | `CategoryTheory.Category` | 2230 | transport | `CategoryTheory.Functor.comp` | 688 | mathematics |
| 5 | `CategoryTheory.Functor` | 1493 | transport | `CategoryTheory.Functor.map` | 490 | mathematics |
| 6 | `CategoryTheory.Functor.map` | 1362 | mathematics | `CategoryTheory.CategoryStruct.comp` | 387 | mathematics |
| 7 | `CategoryTheory.CategoryStruct.comp` | 1298 | mathematics | `CategoryTheory.forget` | 369 | mathematics |
| 8 | `CategoryTheory.Functor.const` | 1051 | mathematics | `CategoryTheory.forget₂` | 356 | mathematics |

**Topology** (48040 decls, in-same 63702, in-cross 16580)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `TopologicalSpace` | 1913 | transport | `ContinuousLinearMap` | 547 | mathematics |
| 2 | `nhds` | 601 | transport | `TopologicalSpace` | 286 | transport |
| 3 | `ContinuousMap` | 386 | transport | `nhds` | 284 | transport |
| 4 | `TopCat.carrier` | 272 | transport | `tsum` | 189 | mathematics |
| 5 | `PartialHomeomorph.toPartialEquiv` | 257 | mathematics | `nhdsWithin` | 160 | transport |
| 6 | `Homeomorph.symm` | 245 | mathematics | `ContinuousLinearMap.ext` | 159 | mathematics |
| 7 | `ContinuousMap.mk` | 240 | mathematics | `ContinuousLinearMap.comp` | 156 | mathematics |
| 8 | `UniformSpace` | 239 | transport | `TopologicalSpace.Opens.map` | 130 | mathematics |

### EL0

| link population | links | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| all_edges | 1458344 | 0.977 | 0.000 | 0.023 | 0.000 |
| same_area | 784377 | 0.986 | 0.000 | 0.014 | 0.000 |
| cross_area | 673967 | 0.967 | 0.000 | 0.033 | 0.000 |

Pooled class composition of the per-area top-15 lists:

| list | n | mathematics | transport | notation | generated |
|---|---|---|---|---|---|
| within_area_hubs | 463 | 0.994 | 0.000 | 0.006 | 0.000 |
| cross_area_mediators | 390 | 0.990 | 0.000 | 0.010 | 0.000 |

Global top hubs by total in-degree (top 15 of 100 scored):

| hub | in-degree | in-cross | class | area | areas citing |
|---|---|---|---|---|---|
| `OfNat.ofNat` | 17307 | 9124 | notation | Core | 30 |
| `Exists.casesOn` | 14988 | 14327 | mathematics | Core | 29 |
| `And.casesOn` | 9357 | 8924 | mathematics | Core | 28 |
| `CategoryTheory.Category.assoc` | 6735 | 2209 | mathematics | CategoryTheory | 12 |
| `Or.casesOn` | 6530 | 6067 | mathematics | Core | 28 |
| `Eq.casesOn` | 6019 | 5737 | mathematics | Core | 29 |
| `DFunLike.coe` | 5736 | 5336 | notation | Data | 27 |
| `Lean.TSyntax.mk` | 5324 | 3911 | mathematics | Core | 28 |
| `Lean.TSyntax.raw` | 5244 | 3735 | mathematics | Core | 28 |
| `Mathlib.Tactic.Reassoc.eq_whisker'` | 4372 | 4368 | mathematics | Tactic | 10 |
| `MonadExcept.throw` | 4239 | 3198 | mathematics | Core | 28 |
| `mul_one` | 4116 | 3392 | mathematics | Algebra | 25 |
| `Eq.rec` | 4054 | 3416 | mathematics | Core | 26 |
| `HAppend.hAppend` | 4013 | 834 | mathematics | Core | 25 |
| `one_mul` | 3028 | 2513 | mathematics | Algebra | 25 |

Top-100 hubs absorb 0.176 of all links and 0.303 of cross-area links; classes {'notation': 6, 'generated': 0, 'transport': 0, 'mathematics': 94}.

Cross-area link mass by hub AREA (area-based, independent of the lane construction):

| hub area | cross-links | share |
|---|---|---|
| Algebra | 160154 | 0.238 |
| Core | 135416 | 0.201 |
| Tactic | 104441 | 0.155 |
| Data | 94954 | 0.141 |
| Order | 69612 | 0.103 |
| CategoryTheory | 27945 | 0.041 |
| Topology | 27048 | 0.040 |
| LinearAlgebra | 11107 | 0.016 |
| Analysis | 10278 | 0.015 |
| MeasureTheory | 10207 | 0.015 |
| Logic | 7916 | 0.012 |
| RingTheory | 6500 | 0.010 |

**Algebra** (100743 decls, in-same 101751, in-cross 160154)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `mul_one` | 724 | mathematics | `mul_one` | 3392 | mathematics |
| 2 | `add_zero` | 614 | mathematics | `one_mul` | 2513 | mathematics |
| 3 | `zero_add` | 574 | mathematics | `add_zero` | 2229 | mathematics |
| 4 | `one_mul` | 515 | mathematics | `Finset.sum_congr` | 2047 | mathematics |
| 5 | `add_comm` | 467 | mathematics | `mul_comm` | 1997 | mathematics |
| 6 | `mul_comm` | 444 | mathematics | `zero_add` | 1880 | mathematics |
| 7 | `map_zero` | 432 | mathematics | `one_ne_zero` | 1537 | mathematics |
| 8 | `mul_assoc` | 432 | mathematics | `mul_assoc` | 1365 | mathematics |

**Core** (203227 decls, in-same 215637, in-cross 135416)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `OfNat.ofNat` | 8183 | notation | `Exists.casesOn` | 14327 | mathematics |
| 2 | `HAppend.hAppend` | 3179 | mathematics | `OfNat.ofNat` | 9124 | notation |
| 3 | `Lean.TSyntax.raw` | 1509 | mathematics | `And.casesOn` | 8924 | mathematics |
| 4 | `Lean.TSyntax.mk` | 1413 | mathematics | `Or.casesOn` | 6067 | mathematics |
| 5 | `GetElem.getElem` | 1391 | mathematics | `Eq.casesOn` | 5737 | mathematics |
| 6 | `HAdd.hAdd` | 1121 | notation | `Lean.TSyntax.mk` | 3911 | mathematics |
| 7 | `Std.DTreeMap.wf` | 1121 | mathematics | `Lean.TSyntax.raw` | 3735 | mathematics |
| 8 | `ForIn.forIn` | 1098 | mathematics | `Eq.rec` | 3416 | mathematics |

**Tactic** (16138 decls, in-same 4377, in-cross 104441)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `Mathlib.Meta.NormNum.NormNumExt.mk` | 76 | mathematics | `Mathlib.Tactic.Reassoc.eq_whisker'` | 4368 | mathematics |
| 2 | `Mathlib.Meta.NormNum.Result` | 76 | mathematics | `Mathlib.Meta.NormNum.isNat_ofNat` | 2839 | mathematics |
| 3 | `Mathlib.Meta.NormNum.IsNat.mk` | 65 | mathematics | `Mathlib.Meta.NormNum.IsNat.of_raw` | 2321 | mathematics |
| 4 | `Mathlib.Meta.NormNum.Result.isNat` | 54 | mathematics | `Mathlib.Tactic.Ring.Common.atom_pf` | 2298 | mathematics |
| 5 | `Mathlib.Meta.NormNum.derive` | 42 | mathematics | `Mathlib.Tactic.Ring.Common.add_pf_add_zero` | 2277 | mathematics |
| 6 | `Mathlib.Meta.NormNum.deriveNat` | 37 | mathematics | `Mathlib.Meta.NormNum.IsNat.to_raw_eq` | 2095 | mathematics |
| 7 | `Mathlib.Meta.Positivity.Strictness.positive` | 37 | mathematics | `Mathlib.Tactic.Ring.Common.add_pf_zero_add` | 1977 | mathematics |
| 8 | `Mathlib.Meta.Positivity.Strictness` | 34 | mathematics | `Mathlib.Tactic.Ring.Common.zero_mul` | 1969 | mathematics |

**Data** (44522 decls, in-same 32582, in-cross 94954)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `DFunLike.coe` | 400 | notation | `DFunLike.coe` | 5336 | notation |
| 2 | `Set.ext` | 356 | mathematics | `Nat.cast_one` | 2665 | mathematics |
| 3 | `Finset.ext` | 256 | mathematics | `Set.ext` | 2006 | mathematics |
| 4 | `Nat.cast_one` | 123 | mathematics | `Nat.cast_zero` | 1756 | mathematics |
| 5 | `Finsupp.ext` | 123 | mathematics | `SetLike.coe` | 1148 | mathematics |
| 6 | `Nat.cast_zero` | 115 | mathematics | `SetLike.mem_coe` | 918 | mathematics |
| 7 | `SetLike.coe` | 106 | mathematics | `Set.mem_singleton_iff` | 905 | mathematics |
| 8 | `Finset.mem_univ` | 106 | mathematics | `Set.mem_univ` | 809 | mathematics |

**Order** (33258 decls, in-same 32545, in-cross 69612)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `LE.le.trans` | 356 | mathematics | `LE.le.trans` | 2296 | mathematics |
| 2 | `le_rfl` | 282 | mathematics | `LT.lt.le` | 2141 | mathematics |
| 3 | `le_antisymm` | 224 | mathematics | `le_refl` | 1690 | mathematics |
| 4 | `LT.lt.le` | 188 | mathematics | `le_antisymm` | 1571 | mathematics |
| 5 | `bot_le` | 151 | mathematics | `Filter.mp_mem` | 1564 | mathematics |
| 6 | `le_top` | 134 | mathematics | `LT.lt.ne'` | 1523 | mathematics |
| 7 | `le_refl` | 133 | mathematics | `le_rfl` | 1313 | mathematics |
| 8 | `Filter.Eventually.mono` | 127 | mathematics | `le_of_lt` | 1200 | mathematics |

**CategoryTheory** (76896 decls, in-same 107994, in-cross 27945)

| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |
|---|---|---|---|---|---|---|
| 1 | `CategoryTheory.Category.assoc` | 4526 | mathematics | `CategoryTheory.Category.assoc` | 2209 | mathematics |
| 2 | `CategoryTheory.Category.comp_id` | 1913 | mathematics | `CategoryTheory.Category.comp_id` | 578 | mathematics |
| 3 | `CategoryTheory.Category.id_comp` | 1757 | mathematics | `CategoryTheory.Category.id_comp` | 539 | mathematics |
| 4 | `CategoryTheory.Iso.hom` | 1037 | mathematics | `CategoryTheory.Functor.obj` | 418 | mathematics |
| 5 | `CategoryTheory.Iso.symm` | 913 | mathematics | `CategoryTheory.Functor.mk` | 345 | mathematics |
| 6 | `CategoryTheory.Functor.comp` | 909 | mathematics | `CategoryTheory.Iso.symm` | 314 | mathematics |
| 7 | `CategoryTheory.Iso.refl` | 902 | mathematics | `CategoryTheory.Functor.comp` | 303 | mathematics |
| 8 | `CategoryTheory.Functor.obj` | 883 | mathematics | `CategoryTheory.Iso.hom` | 261 | mathematics |

## 2. Community emergence

| set | method | nodes | undirected edges | subsampled | communities | >=100 | largest frac | modularity | AMI vs areas |
|---|---|---|---|---|---|---|---|---|---|
| E4_flat | louvain | 499909 | 1479524 | False | 194 | 36 | 0.205 | 0.600 | **0.2117** |
| E4 | louvain | 463466 | 1703375 | False | 75 | 33 | 0.176 | 0.684 | **0.3420** |
| EL0 | louvain | 349876 | 1436263 | False | 365 | 33 | 0.167 | 0.675 | **0.3354** |

Cross-check with a second community algorithm (vectorised weighted
label propagation, same graphs, same seed):

| set | method | communities | modularity | AMI vs areas |
|---|---|---|---|---|
| E4_flat | lpa | 26348 | 0.444 | **0.1445** |
| E4 | lpa | 11254 | 0.612 | **0.2751** |
| EL0 | lpa | 14456 | 0.429 | **0.2148** |

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
| E4 | 1500 | 4.171 | 4.433 | 4 | 4 | 0.000 | 0.000 | **0.5743** |
| EL0 | 1500 | 4.749 | 5.029 | 5 | 5 | 0.000 | 0.000 | **0.5666** |

E4_flat distance histogram (same / cross):

| d | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| same | 0 | 1 | 272 | 338 | 702 | 152 | 24 | 11 | 0 | 0 | 0 | 0 | 0 |
| cross | 0 | 0 | 198 | 313 | 765 | 179 | 38 | 6 | 1 | 0 | 0 | 0 | 0 |

E4 distance histogram (same / cross):

| d | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| same | 0 | 1 | 55 | 230 | 690 | 451 | 70 | 3 | 0 | 0 | 0 | 0 | 0 |
| cross | 0 | 0 | 26 | 137 | 666 | 513 | 149 | 8 | 1 | 0 | 0 | 0 | 0 |

EL0 distance histogram (same / cross):

| d | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| same | 0 | 0 | 46 | 142 | 519 | 431 | 221 | 101 | 26 | 7 | 7 | 0 | 0 |
| cross | 0 | 0 | 15 | 95 | 432 | 478 | 315 | 119 | 33 | 8 | 3 | 2 | 0 |

## 4. Verticality (delta_depth = depth[src] - depth[dst])

**all_edges**

| set | n | mean | p1 | p5 | p25 | p50 | p75 | p90 | p99 | frac <= 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| E4_flat | 1482782 | 49.2 | 1 | 1 | 5 | 27 | 74 | 127 | 250 | 0.000 |
| E4 | 1704084 | 32.2 | 1 | 1 | 2 | 12 | 50 | 89 | 193 | 0.001 |
| EL0 | 1458344 | 59.5 | 1 | 1 | 5 | 35 | 89 | 159 | 277 | 0.001 |

**same_area**

| set | n | mean | p1 | p5 | p25 | p50 | p75 | p90 | p99 | frac <= 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| E4_flat | 789557 | 27.7 | 1 | 1 | 1 | 11 | 43 | 78 | 150 | 0.000 |
| E4 | 1139551 | 21.2 | 1 | 1 | 1 | 6 | 28 | 65 | 136 | 0.002 |
| EL0 | 784377 | 26.8 | 1 | 1 | 1 | 10 | 41 | 76 | 158 | 0.001 |

**cross_area**

| set | n | mean | p1 | p5 | p25 | p50 | p75 | p90 | p99 | frac <= 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| E4_flat | 693225 | 73.6 | 1 | 3 | 20 | 62 | 102 | 170 | 277 | 0.000 |
| E4 | 564533 | 54.2 | 1 | 1 | 11 | 34 | 79 | 138 | 230 | 0.000 |
| EL0 | 673967 | 97.5 | 1 | 4 | 38 | 82 | 146 | 199 | 289 | 0.000 |

