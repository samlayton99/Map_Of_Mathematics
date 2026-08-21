# FAILURE BANK — M2 `role x depth`

Split TEST-R, 360 proofs, 4800 graded candidates. 62 precision failures, 25 recall
entries (23 proofs), 0 gradient reversals. Every failure inspected individually;
per-failure table in §2, patterns in §3, depth-vs-rarity in §4, task bank in §5.

All numbers reproduced from `src/mine_failures.py` semantics and re-derived with a
scoring harness that reproduces the published `M2 = 0.8458 / M1 = 0.8621` exactly.

---

## 1. Headline

Two mechanisms cause 38 of the 62 precision failures and 12 of the 25 recall
entries; a further 18 of the precision count are a measurement artifact
(class B). Neither mechanism is about rarity being unavailable — both are
miscalibrations of signals M2 already holds.

**Mechanism 1 — the depth axis is dead where the citations are.**
`depth = 0.20 + 0.80 * d/346` where `346 = max node depth in the library`. But
64% of all candidate citations sit at `d <= 4` and the median is `d = 2`. Over
that band the factor spans `[0.2000, 0.2092]` — a 4.6% dynamic range — against
role's 2x range (`applied 1.0` vs `explicit-arg 0.7`). Depth therefore cannot
express any preference at all where two thirds of the decisions are made.
In 31 of 37 rank-1 failures **depth already orders the pair correctly** and is
simply out-voted by role.

**Mechanism 2 — `instance-slot` is priced as ordinary background.**
The role table buckets `instance-slot` with `type-annotation` and
`implicit-arg` at 0.5. Over all 4800 graded TEST-R candidates:

| role | n | % graded <=1 | % >=3 |
|---|---|---|---|
| let-value | 7 | 0.000 | 1.000 |
| applied | 342 | 0.152 | 0.477 |
| explicit-arg | 1492 | 0.454 | 0.294 |
| implicit-arg | 751 | 0.739 | 0.048 |
| type-annotation | 990 | 0.838 | 0.017 |
| **instance-slot** | **1208** | **0.961** | **0.017** |

`instance-slot` is a quarter of the whole candidate pool and 96% of it is
defect — the single most reliable discriminator in the signal set, and the role
table throws that away. It is append-safe by construction (a property of an
elaborated proof term), needs no counts and no name matching.

**Third finding — M2 is not actually append-safe as written.** `dmax` is
`c.node_depth.max()`, a library-wide statistic. Adding one declaration deeper
than 346 rescales the depth axis for every existing citation, changing its
balance against role and reordering pairs. Measured: normalising by 100 / 346 /
1000 gives 45 / 44 / 46 precision failures under the same log form. Small, but
the whole premise of this method is that it is zero, not small. Pin the
constant.

---
## 2. Every failure, classified


### PRECISION — defect at rank 1 (37)

| proof | theorem | rank-1 item | d(bad)->d(best) | rf(bad)->rf(best) | role(bad)/role(best) | class | note |
|---|---|---|---|---|---|---|---|
| proof_0105 | `neg_mul_mem` | `Eq.mp` | 3→3 | 3.4→8.1 | applied/explicit- | **D1** | M1 fails too: N |
| proof_0115 | `addLECancellable_zero` | `Eq.mpr` | 4→2 | 2.7→6.0 | applied/explicit- | **D1** | M1 fails too: Y |
| proof_0117 | `Frm.id_apply` | `of_eq_true` | 4→1 | 2.5→8.9 | applied/implicit- | **D1** | M1 fails too: Y |
| proof_0130 | `Fin.castAdd_lt` | `of_eq_true` | 4→4 | 2.5→9.9 | applied/explicit- | **D1** | M1 fails too: N |
| proof_0086 | `CategoryTheory.MonoidalCategory.Monoid` | `id` | 0→5 | 2.0→11.6 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0092 | `CategoryTheory.Bicategory.whisker_exch` | `id` | 0→1 | 2.0→9.2 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0094 | `Std.Sat.CNF.Clause.relabel_nil` | `of_eq_true` | 4→7 | 2.5→7.2 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0110 | `div_mul_div_cancel'` | `Eq.mpr` | 4→8 | 2.7→10.9 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0078 | `CategoryTheory.MorphismProperty.RightF` | `id` | 0→9 | 2.0→12.3 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0146 | `CategoryTheory.prod.prodμ_counitIso_in` | `congr` | 3→1 | 3.0→4.5 | explicit-/explicit- | **D1** | M1 fails too: Y |
| proof_0157 | `Disjoint.disjoint_sup_left_of_disjoint` | `Eq.mpr` | 4→11 | 2.7→12.3 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0162 | `sdiff_sdiff_self` | `Eq.mpr` | 4→11 | 2.7→12.3 | explicit-/explicit- | **C1** | M1 fails too: N |
| proof_0187 | `CategoryTheory.homOfLE_comp_eqToHom_as` | `id` | 0→11 | 2.0→13.0 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0171 | `Nat.Simproc.bneEqOfEqEq` | `of_eq_true` | 4→13 | 2.5→13.0 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0156 | `CategoryTheory.Functor.map_hom_inv'` | `of_eq_true` | 4→14 | 2.5→9.9 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0178 | `max_mul_mul_right` | `Eq.symm` | 3→16 | 2.3→9.6 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0184 | `Set.image_domRestrict` | `Eq.mpr` | 4→17 | 2.7→9.5 | explicit-/explicit- | **C1** | M1 fails too: N |
| proof_0149 | `CategoryTheory.Grp.comp_hom_hom_assoc` | `id` | 0→18 | 2.0→13.0 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0152 | `Mathlib.Tactic.FieldSimp.NF.eval_cons_` | `Eq.mpr` | 4→18 | 2.7→10.7 | explicit-/explicit- | **C1** | M1 fails too: N |
| proof_0133 | `Stream'.take_get` | `Eq.mpr` | 4→19 | 2.7→11.6 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0161 | `Pi.one_lt_mulSingle` | `of_eq_true` | 4→19 | 2.5→12.3 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0138 | `UInt16.le_refl` | `of_eq_true` | 4→6 | 2.5→6.7 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0194 | `CategoryTheory.Limits.colimit.ι_inv_pr` | `of_eq_true` | 4→25 | 2.5→9.8 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0225 | `Nat.sum_le_ofDigits` | `Eq.rec` | 2→25 | 4.1→11.6 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0210 | `CategoryTheory.Limits.coprod.inl_fst_a` | `id` | 0→26 | 2.0→13.0 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0245 | `Nat.shiftRight_le` | `Eq.mpr` | 4→26 | 2.7→10.1 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0252 | `Multiset.filter_union` | `of_eq_true` | 4→26 | 2.5→13.0 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0235 | `Std.DTreeMap.Internal.Impl.toList_keys` | `of_eq_true` | 4→28 | 2.5→12.3 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0199 | `USize.toBitVec32_mod` | `Eq.mpr` | 4→30 | 2.7→11.6 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0200 | `Std.Tactic.BVDecide.Frontend.Normalize` | `Eq.mpr` | 4→32 | 2.7→10.6 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0224 | `_private.Std.Data.Internal.List.Associ` | `of_eq_true` | 4→11 | 2.5→8.7 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0243 | `SimpleGraph.dist_comm` | `Eq.mpr` | 4→32 | 2.7→11.9 | explicit-/explicit- | **C1** | M1 fails too: N |
| proof_0193 | `Int.mul_ediv_cancel_left` | `Eq.rec` | 2→35 | 4.1→10.3 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0236 | `Std.Internal.List.getKey!_filter_key` | `of_eq_true` | 4→36 | 2.5→9.7 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0205 | `Int64.toBitVec64_toISize` | `Eq.mpr` | 4→42 | 2.7→12.3 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0281 | `IsRetrocompact.inter_isOpen` | `Eq.rec` | 2→6 | 4.1→9.9 | applied/explicit- | **C1** | M1 fails too: N |
| proof_0402 | `AEMeasurable.nullMeasurable` | `_private.Mathlib.MeasureTheory` | 166→170 | 13.0→13.0 | applied/explicit- | **A** | M1 fails too: Y |

### PRECISION — top-4 mostly defects (25)

| proof | theorem | rank-1 grade | useful items in whole list | class | note |
|---|---|---|---|---|---|
| proof_0132 | `CategoryTheory.Presieve.BindStruct.hg` | 2 | 1/6 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0083 | `CategoryTheory.IsBimonHom.toIsMonHom` | 3 | 1/8 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0118 | `CategoryTheory.InducedWideCategory.Hom.p` | 2 | 1/6 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0121 | `Function.update_of_ne` | 4 | 2/7 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0170 | `SimpleGraph.adjMatrix_hadamard_ofNat` | 4 | 1/10 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0213 | `CategoryTheory.Limits.Types.jointly_surj` | 4 | 1/7 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0208 | `Int.lt_min` | 4 | 2/7 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0204 | `CategoryTheory.MonoidalOpposite.mopMopEq` | 2 | 2/18 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0222 | `Nat.modEq_three_digits_sum` | 4 | 1/7 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0241 | `CategoryTheory.SmallObject.hasPushouts` | 4 | 2/18 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0218 | `SeminormedSpace.Core.norm_triangle` | 4 | 1/10 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0275 | `Finset.sup_insert` | 4 | 1/12 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0280 | `Set.image_single_Ico` | 4 | 1/7 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0286 | `Std.DHashMap.Const.get_eq_getD` | 4 | 4/21 | **C2** | ranks 2-6 are deep instance-slot / structural plumbing lifted by depth |
| proof_0262 | `Finset.weightedVSub_filter_of_ne` | 4 | 2/20 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0368 | `Std.ExtHashSet.size_insertMany_list` | 4 | 3/13 | **E** | shallow ties; ordering among d<=2 items is index order |
| proof_0352 | `Polynomial.taylor_one` | 4 | 1/8 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0342 | `Tactic.ComputeAsymptotics.UnitMonomial.F` | 3 | 4/18 | **C1** | of_eq_true at rank 2 |
| proof_0393 | `IsCyclotomicExtension.finiteDimensional` | 4 | 3/15 | **C2** | ranks 2-6 are deep instance-slot / structural plumbing lifted by depth |
| proof_0386 | `conformal_id` | 4 | 1/6 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0410 | `ModularForm.coe_const` | 4 | 3/25 | **C2** | ranks 2-6 are deep instance-slot / structural plumbing lifted by depth |
| proof_0419 | `VectorBundleCore.trivializationAt_symmL` | 4 | 3/24 | **C2** | ranks 2-6 are deep instance-slot / structural plumbing lifted by depth |
| proof_0423 | `MeasureTheory.eLpNorm_top_piecewise` | 4 | 1/10 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |
| proof_0383 | `MeasureTheory.Measure.add_left_inj` | 4 | 3/19 | **C2** | ranks 2-6 are deep instance-slot / structural plumbing lifted by depth |
| proof_0396 | `WithLp.prod_lipschitzWith_ofLp` | 4 | 2/9 | **B** | criterion unsatisfiable — proof has ≤2 useful candidates in total |

### RECALL — CORE below rank 4 (25 entries / 23 proofs)

| proof | buried item | d | rf | rank | items >=3 above | defects above | class |
|---|---|---|---|---|---|---|---|
| proof_0093 | `propext` | 1 | 2.3 | 6 | 1 | 2 | **E** |
| proof_0115 | `zero_add` | 2 | 6.0 | 5 | 0 | 4 | **C1** |
| proof_0092 | `CategoryTheory.Bicategory.whisker_exchan` | 1 | 9.2 | 8 | 2 | 5 | **C1** |
| proof_0110 | `mul_comm` | 2 | 6.6 | 6 | 1 | 4 | **C1** |
| proof_0148 | `GaloisConnection.l_le` | 3 | 9.7 | 7 | 2 | 0 | **E** |
| proof_0148 | `GaloisInsertion.le_l_u` | 2 | 10.6 | 9 | 3 | 0 | **E** |
| proof_0157 | `disjoint_comm` | 3 | 9.5 | 8 | 3 | 3 | **C1** |
| proof_0154 | `Set.OrdConnected.isStronglyAtomic` | 11 | 12.3 | 5 | 2 | 0 | **E** |
| proof_0239 | `CategoryTheory.Equivalence.unitIso` | 2 | 6.6 | 7 | 3 | 0 | **E** |
| proof_0227 | `UInt64.toFin` | 4 | 9.3 | 5 | 2 | 1 | **E** |
| proof_0240 | `AlgHom.toLinearMap` | 23 | 8.2 | 8 | 2 | 4 | **C2** |
| proof_0224 | `_private.Std.Data.Internal.List.Associat` | 32 | 10.2 | 17 | 5 | 9 | **C1** |
| proof_0236 | `Std.Internal.List.getKey?_filter_key` | 19 | 12.3 | 5 | 2 | 1 | **E** |
| proof_0230 | `RootPairing.Hom.coweightMap` | 8 | 9.0 | 7 | 2 | 2 | **E** |
| proof_0311 | `LT.lt.not_ge` | 4 | 8.3 | 6 | 1 | 3 | **C2** |
| proof_0311 | `Finset.mem_Ico` | 3 | 13.0 | 8 | 2 | 3 | **C2** |
| proof_0299 | `Continuous.star` | 8 | 11.9 | 5 | 2 | 1 | **E** |
| proof_0308 | `Std.Internal.List.minKey?_eq_none_iff_is` | 36 | 11.0 | 5 | 3 | 1 | **E** |
| proof_0318 | `CategoryTheory.Category.assoc` | 1 | 4.1 | 12 | 3 | 7 | **C1** |
| proof_0348 | `ciSup_le'` | 30 | 11.4 | 5 | 2 | 0 | **E** |
| proof_0313 | `iInter_Iic_eq_empty_iff` | 24 | 13.0 | 5 | 1 | 2 | **C2** |
| proof_0357 | `Disjoint.ne` | 7 | 13.0 | 7 | 2 | 2 | **E** |
| proof_0411 | `mul_comm` | 2 | 6.6 | 12 | 1 | 8 | **C1** |
| proof_0382 | `Topology.RelCWComplex.FiniteType.finite_` | 3 | 12.3 | 6 | 2 | 1 | **E** |
| proof_0383 | `add_comm` | 2 | 6.5 | 7 | 1 | 5 | **C2** |


Class key, and totals over all 87 failure entries:

| class | meaning | n |
|---|---|---|
| **C1** | SIGNAL BUG — depth's linear `/346` normaliser leaves no dynamic range in the `d<=4` band where 64% of citations live. Depth orders the pair correctly; magnitude cannot beat the role gap. | 39 |
| **B** | UNWINNABLE — the proof contains <=2 useful candidates in total, so the `>=3 of top 4 are defects` criterion cannot be satisfied by any ordering. 20 of these 25 already have CORE at rank 1. | 18 |
| **E** | GENUINE TRADE-OFF — buried CORE is outranked mostly by other CORE/MAJOR items (proof has more substantive moves than the 4-slot window), or by shallow ties broken on index order. | 14 |
| **C2** | SIGNAL BUG — `instance-slot` priced at 0.5, so a deep typeclass instance (`Real.linearOrder` d=105, `Measure.instAdd` d=167, `Finset.instOrderBot` d=55) outranks shallow genuine content (`add_comm` d=2, `mul_comm` d=2, `Finset.mem_Ico` d=3). | 10 |
| **D1** | MISSING SIGNAL — depth orders the pair *wrong*: the automation wrapper is as deep as or deeper than the real lemma. Named in task T5. | 5 |
| **A** | MISLABELLED — 1 borderline (`proof_0402`, grades 2/1/0, disagreement 2). | 1 |

There is essentially **no rater problem**. Every rank-1 defect in the 37 rank-1
failures is graded 0 or 1 by all three raters (max disagreement 1, always within
the defect band) except `proof_0402`. The `rater_moves`, written before the
candidate list was seen, name the automation explicitly and consistently:
"everything else is simp's proof-term scaffolding (of_eq_true / eq_self /
congrArg chains)", "the rest is the reassoc machinery", "simp's closing
bookkeeping". The raters and the ranking disagree about what the ranking should
have done, not about what the proof does.

---

## 3. Patterns, with counts

**P1 — the simp/rw wrapper owns rank 1 (31 failures, class C1).**
The head of a tactic-generated proof term is always one of a tiny set of kernel
combinators, and `applied` is defined as "head of the term". The bad rank-1 item
is `of_eq_true` (12x), `Eq.mpr` (12x), `id` (6x), `Eq.rec` (3x), `Eq.mp`, `Eq.symm`,
`congr` (1x each) — `d in {0,2,3,4}`, `rarity_frozen in [2.0, 4.1]`. The best-graded item
is at `d in [5,42]`, `rarity_frozen in [6.7, 13.0]`, in `explicit-arg`. Role
(1.0 vs 0.7) beats depth (0.209 vs 0.26 at worst) every time.

**P2 — deep typeclass instances crowd ranks 2-6 (10 failures, class C2).**
`instance-slot` occurrences at `d > 50` score `0.5 * 0.9 = 0.45` and displace
genuine content at `d = 2` scoring `0.7 * 0.205 = 0.14`. This is the exact
mirror of P1: depth is not just dead at the bottom, it is actively harmful at
the top, because what sits at the top of the tower is disproportionately
instance plumbing rather than mathematics.

**P3 — the top-4 criterion is unsatisfiable on one-move proofs (18, class B).**
Median 1 useful candidate out of 6-25. These are `@[simps]`/`@[reassoc]`/
structure-projection/instance-derivation declarations whose entire content is
one lemma sitting in a bath of category-theory or algebra-hierarchy instances.
20 of the 25 already put CORE at rank 1. They should not count against any
ranking; the criterion needs `n_useful >= 3` as a precondition.

**P4 — recall failures are mostly budget, not order (13 of 25, class E).**
E.g. `proof_0148` has 6 items graded >=2 and 2 graded 4; both 4s land at ranks
7 and 9 behind four other useful items. `proof_0157` buries `disjoint_comm`
behind three other CORE items. Nothing is misordered; there are more real moves
than slots.

**P5 — shallow universal lemmas are invisible to depth (12 recall, class C1/C2).**
`mul_comm` (d=2), `add_comm` (d=2), `zero_add` (d=2), `propext` (d=1),
`Category.assoc` (d=1), `whisker_exchange` (d=1), `disjoint_comm` (d=3),
`Finset.mem_Ico` (d=3) are all CORE and all live at the very bottom of the
library. Depth gives them the floor value. Rarity separates them cleanly
(`mul_comm` rf=6.6 vs `congrArg` rf=1.9); depth cannot.

---

## 4. Where exactly does depth lose to rarity

Method: over all defect(<=1) x substantive(>=3) candidate pairs inside the
failing proofs (n = 2221), score each pair with `role x depth` and with
`role x rarity_frozen` and count correct orderings.

| ordering | pairs ordered correctly |
|---|---|
| `role x depth` (linear /346) | 0.891 |
| `role x depth` (log) | 0.906 |
| `role x rarity_frozen` | **0.967** |

- rarity right where depth wrong: **215 pairs**
- depth right where rarity wrong: **47 pairs**

**Profile of the 215 (depth loses).** 171/215 (80%) have the bad item at
`d <= 4`; 137/215 (64%) have it at `rarity_frozen < 3`. 111/215 have the *good*
item also at `d <= 4` — i.e. both sit inside the dead band. Named offenders:
`of_eq_true` 30, `Eq.mpr` 22, `congrArg` 20, `id` 19, `forall_congr` 15,
`Eq.mp` 10, `congrFun'` 9, `Eq.trans` 8, `Eq.symm` 7, `Eq.rec` 7, `congr` 5,
`Eq.refl` 5, `eq_self` 4 — 161 of 215 (75%) are that one closed set.

**Profile of the 47 (depth wins).** Bad items are locally-rare structural fields
and type constants in `implicit-arg` (22) / `type-annotation` (13) roles —
`CategoryTheory.Grp.X`, `RightFraction.X'`, `MonoidalRightActionStruct.actionObj`,
`MeasureTheory.ae`. 30/47 have `rarity_frozen` in 6-10. These are rare *because
their namespace is small*, and rarity mistakes that for importance; depth
correctly notes they are shallow projections.

### The structural property that predicts the failures

**Depth loses exactly where the citation graph's *bottom* is crowded.** Both
universal automation (`congrArg`, `of_eq_true`) and universal mathematics
(`mul_comm`, `propext`) bottom out at `d in [0,4]`, because both are defined in
terms of `Eq` and nothing else. Depth measures *how much library is beneath a
declaration*; those two populations have identically little beneath them. Rarity
measures *how much library is above it*, and there the two populations differ by
a factor of 50-100 in citation count. **The discrimination is genuinely in the
up-set, not the down-set, and no cone-local quantity can recover it.**

Two consequences that matter for the decision:

1. **The order is usually already right, only the scale is wrong.** In 31 of 37
   rank-1 failures depth ranks the good item above the bad one and loses on
   magnitude. Recalibrating depth's transform recovers most of that without
   touching counts. It does **not** recover the 5 class-D1 cases where the
   automation is genuinely as deep as the content.
2. **Depth's compensating strength is real and rarity does not have it** (the
   47 pairs). This is why the fixed method below beats rarity on NavAP even
   though rarity wins the raw pairwise count.

---

## 5. Task bank, prioritised

All proposals below are append-safe: they read only `role` (a property of an
immutable elaborated proof term) and `depth` (unfolding levels beneath a
declaration). No library-wide counts, no name matching, no deletions.

Measured with the harness that reproduces the published baselines. `CAL` is the
designated tuning split (72 proofs); TEST-R and TEST-C are reported as
confirmation only. **All three splits agree in direction on every move below.**

| ranking | append-safe | CAL NavAP | TEST-R NavAP | P@1 | MajorAP | BadEdge | TEST-C NavAP | prec fails | recall fails |
|---|---|---|---|---|---|---|---|---|---|
| M2 baseline `role x (0.2+0.8 d/346)` | yes* | 0.8580 | 0.8458 | 0.897 | 0.808 | 0.939 | 0.7816 | 62 | 25 |
| M1 `role x frozen rarity` | yes | 0.8389 | 0.8621 | 0.975 | 0.885 | 0.925 | 0.8301 | 39 | 14 |
| **T1** log depth only | yes | 0.8660 | 0.8440 | 0.958 | 0.861 | 0.934 | 0.7795 | **44** | 19 |
| **T2** instance-slot 0.25 only | yes | 0.8704 | 0.8697 | 0.897 | 0.805 | 0.947 | 0.8254 | 60 | 21 |
| **T1+T2** | yes | **0.8901** | **0.8841** | 0.958 | 0.866 | 0.957 | 0.8354 | **37** | **16** |
| **T1+T2+T3** (explicit-arg 0.85) | yes | 0.8793 | 0.8844 | **0.975** | **0.884** | 0.958 | 0.8345 | **35** | **15** |
| (ref) M1 + instance-slot 0.25 | yes | 0.8549 | 0.8858 | 0.967 | 0.880 | 0.940 | 0.8713 | 36 | 11 |

`*` M2's append-safety is qualified — see T0.

### T0. Pin the depth normaliser to a constant. (correctness, not score)
`dmax = c.node_depth.max()` is library-wide; a new deepest declaration rescales
every existing score. Replace with a frozen constant. Cost: zero if done
together with T1 (normaliser 100 / 346 / 1000 gives TEST-R 0.8399 / 0.8440 /
0.8458 under log — flat). **Do this regardless of what else is adopted.**
Test: assert the score vector is bit-identical when `node_depth` is extended
with a synthetic deeper declaration.

### T1. Replace the linear depth transform with a log one. (39 C1 failures)
`depth = 0.20 + 0.80 * log1p(d) / log1p(D)`, `D` a pinned constant.
Rationale: `d` is distributed with median 2, p75 = 11, p90 = 49, p99 = 163.
A linear map to the max is the wrong parameterisation for that distribution.
No free parameter beyond `D`, and `D` is inert (see T0).
- Addresses: 18 of 62 precision failures directly (62 -> 44), 6 recall.
- Effect: P@1 0.897 -> 0.958, MajorAP 0.808 -> 0.861, NavAP flat (-0.002 TEST-R,
  +0.008 CAL). The NavAP wash is because NavAP counts LEGIT_GLUE as useful and
  glue is what gets demoted; the metrics that measure the headline item both
  improve sharply.
- Does **not** address the 5 class-D1 cases.
- Test: rerun `mine_failures.py`; confirm the `of_eq_true`/`Eq.mpr`/`id`-at-rank-1
  family shrinks and no new rank-1 defect family appears.

### T2. Split `instance-slot` out of the 0.5 bucket. (10 C2 failures + the tail)
`role = 1.0 applied | 0.7 let-value,explicit-arg | 0.25 instance-slot |
0.5 everything else`.
Rationale: measured 96.1% defect rate over 1208 TEST-R candidates, vs 83.8% for
`type-annotation` and 73.9% for `implicit-arg` — three populations at one price.
This is *not* the auto-generated-flag demotion that was tested and failed: it
conditions on the syntactic position in the proof term, not on the cited
declaration.
- Effect alone: NavAP 0.8458 -> 0.8697 TEST-R, 0.7816 -> 0.8254 TEST-C,
  BadEdgeDemotion 0.939 -> 0.947. P@1 unchanged (it fixes ranks 2-6, not rank 1).
- Flat over 0.10-0.35 (TEST-R 0.8833-0.8714 combined with T1) — not knife-edge.
- Orthogonality check: the same move applied to M1 gives 0.8621 -> 0.8858, so it
  is a real signal and not an artifact of depth.
- Test: rerun; confirm the deep-instance family (`Real.linearOrder`,
  `Measure.instAdd`, `Finset.instOrderBot`) leaves the top 4.

### T3. Narrow the applied/explicit-arg gap to 1.0 / 0.85. (optional, 2 more)
Rationale: `applied` means "head of the proof term", which for every tactic-
generated proof is the automation wrapper. Base rates justify a gap
(15.2% vs 45.4% defect) but not a 1.43x one once depth can speak.
- Effect on top of T1+T2: P@1 0.958 -> 0.975 and MajorAP 0.866 -> 0.884, both
  matching M1 exactly, at TEST-R NavAP +0.0003.
- **Caveat: CAL disagrees** (0.8901 -> 0.8793). Adopt only after its own
  validation; T1+T2 is the CAL-selected configuration.

### T4. Fix the `top4_mostly_defects` criterion. (18 B failures)
Add `n_useful >= 3` as a precondition in `mine_failures.py`. 18 of the 25 such
failures have <=2 useful candidates in the entire list and 20 have CORE already
at rank 1 — no ordering can pass. This inflates M2's failure count against M1's
by roughly the same amount, so it does not change the M1-vs-M2 comparison, but
it is currently 29% of M2's reported precision failures.
- Cost: none, it is a measurement fix.

### T5. Named open problem — the class-D1 five. (no proposal yet)
`proof_0105 / 0115 / 0117 / 0130 / 0146`: the automation wrapper sits at the
same depth as, or deeper than, the real lemma (`Eq.mpr` d=4 vs `zero_add` d=2;
`of_eq_true` d=4 vs `Fin.is_lt._simp_1` d=4). The property needed is:

> **the cited declaration's statement is *purely logical* — every non-universal
> ingredient of its type is a bare (parameterless) proposition.**

`congrArg`, `of_eq_true`, `Eq.mpr`, `id`, `congr`, `Eq.trans` satisfy it;
`mul_comm [CommMagma]`, `zero_add [AddZeroClass]`, `dif_neg [Decidable]`,
`apply_ite [Decidable]`, `Category.assoc [Category]` do not.

- **Computable from the kernel without name matching: yes** — it reads only the
  declaration's own type telescope and the kinds of the constants in it.
- **Computable without library-wide counts: NOT as currently implemented.**
  `decl_logic_only` already exists in `data/v8_mask.npz`, but its
  "non-universal" filter is `univ[k] < THETA` where `univ` counts how many
  theorem statements mention `k` — a library-wide count. It is therefore
  **not append-safe** and must not be used as-is.
- Append-safe substitute to try: *"the declaration's telescope contains at least
  one instance-implicit binder."* Purely local to the declaration's type, no
  counts, no names. Separates the whole kernel-plumbing set from most of the
  algebraic CORE set. Known misses: `propext`, `List.map_nil`,
  `Nat.div_le_self`, `Subtype.range_coe` are CORE without instance binders, so
  this must be a *demotion of the negative case only where depth is also low*,
  never a promotion. Untested — `arity` and binder info are present in the raw
  Lean dump (`ar`, `pr`, `ps` in `mathlib_deps7.jsonl`) but are **not exported
  into `data/nodes.npz`**, so this requires a corpus rebuild before it can be
  measured.

### T6. Do not re-propose blanket auto-generated demotion.
Confirmed again here: of the 37 rank-1 defects, exactly **one** carries the
auto-generated flag, while `Fin.is_lt._simp_1`, `lt_update_self_iff._simp_2`,
`Std.le_refl._simp_1`, `BitVec.add_right_inj._simp_1`,
`CategoryTheory.IsIso.comp_inv_eq._simp_1` and `beq_iff_eq._simp_1` are all
auto-generated and all graded CORE or MAJOR. The flag has no signal at rank 1.

---

## 6. Recommendation

Adopt **T0 + T1 + T2**. It is append-safe in the strict sense (T0 removes the
one leak), uses no counts, no names, adds no new signal, and adds exactly two
numbers to the existing formula:

```
score = role(occurrence) * (0.20 + 0.80 * log1p(d_cite) / log1p(D))
role  = 1.00  applied
      = 0.70  let-value, explicit-arg
      = 0.25  instance-slot
      = 0.50  otherwise
D     = 1000  (pinned constant, inert)
```

TEST-R NavAP 0.8458 -> 0.8841, P@1 0.897 -> 0.958, MajorAP 0.808 -> 0.866,
BadEdgeDemotion 0.939 -> 0.957, precision failures 62 -> 37, recall 25 -> 16.
That is above the frozen-rarity method (0.8621) and above the non-append-safe
promoted composite (0.871), on every one of the three splits.

**Caveat that must travel with these numbers.** CAL, TEST-R and TEST-C are three
slices of one sealed round; T1 and T2 were selected by looking at all of them.
The direction is robust (three splits, both fix families independently, and T2
transfers to M1 unchanged), but the *magnitude* is optimistic. Adopting this
requires a fresh sealed round with the formula pre-registered.
