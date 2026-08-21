# Separating LEGIT_GLUE (2) from BAD_GLUE/JUNK (<=1)

Sealed R1 labels, 552 proofs, 7,531 graded candidates (every U1D candidate of
every sampled proof is graded, so per-proof features are complete).

**Split discipline.** Every rule was chosen and every threshold set on
DEV = CAL + TEST-C (192 proofs, 2,731 candidates). TEST-R (360 proofs,
4,800 candidates) was read once, after the rule was fixed. Both columns are
shown throughout so the replication is visible.

Base rate P(grade 2 | grade <= 2): **0.213** DEV, **0.202** TEST-R.

---

## 1. The prize is real

Under the base model (`role_rebucketed x frozen_rarity`), TEST-R still has
1,116 inverted pairs (a grade <=1 item ranked above a useful item inside the
same proof). By the grade of the useful item:

| useful item | inverted pairs | share |
|---|---|---|
| 2 LEGIT_GLUE | 972 | **0.871** |
| 3 MAJOR | 113 | 0.101 |
| 4 CORE | 31 | 0.028 |

87% of what is left to fix is grade 2. The failure analysis was right about
where the gain is.

---

## 2. Rules tested

`precision` = n(2) / n(2 + <=1) among fired items. `recall` = share of all
grade-2 items fired. `collateral` = share of all grade >=3 items fired.

### 2a. Proof-relative signals (the primary hypothesis) — all null

| rule | prec DEV | prec TR | recall TR | collateral TR |
|---|---|---|---|---|
| proof has no theorem candidate | 0.264 | 0.235 | 0.294 | 0.211 |
| n_candidates <= 8 (short proof) | 0.333 | 0.278 | 0.157 | 0.193 |
| n_nonglue_candidates <= 6 | 0.276 | 0.250 | 0.355 | 0.379 |
| glue_share >= 0.5 | 0.232 | 0.230 | 0.472 | 0.468 |
| cited_depth >= proof median | 0.244 | 0.268 | 0.729 | 0.952 |
| rel_depth = d_cite/(proof max d_cite) >= 0.5 | 0.287 | 0.352 | 0.214 | 0.654 |
| depth rank in proof <= 3 | 0.332 | 0.375 | 0.317 | 0.725 |
| deepest candidate in proof (depth_gap == 0) | 0.333 | 0.612 | 0.062 | 0.453 |
| rarity >= proof median | 0.304 | 0.312 | 0.690 | 0.957 |

Nothing beats the 0.21 base rate by enough to matter. The two that look
strong on TEST-R (`deepest`, `depth_gap == 0`) do not replicate on DEV
(0.333 vs 0.612) and catch 45% of all grade 3/4 items — they are *deep move*
detectors, not glue detectors, and they are already what the base model does.

**Sharper test.** Restrict to the population where the confusion actually
lives (cited_depth <= 3 and frozen rarity <= 5; n = 3,123, p2 = 0.147) and
compute AUC for grade 2 vs <=1 on each proof-relative signal:

| signal | AUC DEV | AUC TEST-R |
|---|---|---|
| depth_gap (proof best minus this item) | 0.382 | 0.480 |
| delta_depth (target minus cited) | 0.383 | 0.481 |
| proof max cited depth | 0.385 | 0.484 |
| deepest theorem candidate depth | 0.352 | 0.381 |
| rarity gap to proof best | 0.349 | 0.402 |
| n_candidates | 0.423 | 0.434 |
| n_theorem_candidates | 0.432 | 0.387 |
| glue_share | 0.527 | 0.530 |
| in_statement | 0.409 | 0.457 |
| **applied role** | **0.647** | **0.685** |
| rel_depth | 0.661 | 0.634 |
| frozen rarity | 0.652 | 0.597 |

Every proof-relative signal is near 0.5 or flips sign between the two splits.
**"Grade 2 concentrates in proofs where there is no deeper content" is false
in this corpus.** At proof level: proofs containing no grade >=3 item have
P(2 | <=2) = 0.206; proofs containing one have 0.206.

Only three signals replicate, and two of them (rarity, depth) are already in
or adjacent to the base model. The one that is not is the role.

### 2b. Target-relative signals

| rule | prec DEV | prec TR | recall TR | collateral TR |
|---|---|---|---|---|
| delta_depth <= 1 (immediately below target) | 0.353 | 0.615 | 0.058 | 0.436 |
| delta_depth <= 3 | 0.331 | 0.429 | 0.127 | 0.525 |

`delta_depth <= 1` fires 376 times on TEST-R and 298 of those (79%) are grade
3/4. It is a good CORE detector and a bad LEGIT_GLUE detector.

### 2c. Role x own-cone-depth — the one that works

Sweep of `role bucket & cited_depth <= k`. Only the applied row separates:

| rule | prec DEV | prec TR | recall TR | collateral TR |
|---|---|---|---|---|
| **applied & d_cite <= 2** | **0.873** | **0.882** | 0.116 | **0.028** |
| applied & d_cite <= 3 | 0.872 | 0.856 | 0.128 | 0.038 |
| applied & d_cite <= 1 | 0.795 | 0.859 | 0.073 | 0.009 |
| applied & d_cite <= 5 | 0.640 | 0.670 | 0.142 | 0.057 |
| applied (any depth) | 0.648 | 0.683 | 0.152 | 0.238 |
| explicit/let & d_cite <= 2 | 0.363 | 0.287 | 0.227 | 0.089 |
| implicit & d_cite <= 2 | 0.175 | 0.127 | 0.080 | 0.010 |
| type-ann & d_cite <= 2 | 0.146 | 0.095 | 0.090 | 0.009 |
| instance-slot & d_cite <= 2 | 0.000 | 0.009 | 0.005 | 0.003 |

Widening attempts, all rejected (precision halves, NavAP does not improve):

| rule | prec DEV | prec TR | recall TR | NavAP TR (floor 4) |
|---|---|---|---|---|
| (applied \| is_claim) & d <= 3 | 0.463 | 0.446 | 0.162 | 0.9112 |
| is_claim & d <= 3 & not instance-slot | 0.400 | 0.353 | 0.101 | 0.9033 |
| applied & d <= 2 & not in_statement | 0.917 | 0.880 | 0.026 | 0.9033 |

---

## 3. The rule

> **A declaration applied in head position whose own dependency cone is at
> most 2 deep is legitimate glue.**

`inc_roles[:, 0] > 0 and node_depth[cited] <= 2`.

Fires 193 / 7,531 times. Grade composition:

| split | 0 | 1 | **2** | 3 | 4 | precision | recall | collateral |
|---|---|---|---|---|---|---|---|---|
| DEV | 1 | 3 | **55** | 0 | 1 | 0.873 | 0.113 | 0.002 (1 item) |
| TEST-R | 7 | 6 | **97** | 7 | 12 | 0.882 | 0.116 | 0.028 (19 items) |

4.3x the base rate, replicated. Collateral is the point: on DEV a single
grade >=3 item fires; on TEST-R, 19 of 686. The rule cannot demote real
mathematics because it barely touches it — and the intervention only raises
scores, never lowers them.

What it is picking up, by construction rather than by name: `rfl`, `Eq.refl`,
`Iff.intro`, `Iff.mpr`, `And.intro`, `Exists.intro`, `<Class>.mk`. Failure B
of `FAILURE_ANALYSIS.md` verbatim — "for an `_apply` lemma whose proof is
literally `rfl`, reflexivity *is* the argument, and rarity guarantees we bury
it." Under the base model these grade-2 items sit at mean rank 5.6 of 13.4.

The one systematic false positive is `id` (14 fires, all graded <=1). No name
rule was used to remove it.

### Append-safety

| ingredient | scope |
|---|---|
| `inc_roles[:,0]` | per incidence |
| `node_depth[cited]` | the cited declaration's own dependency cone |
| threshold 2, floor 4 | fixed constants, not data-derived quantiles |

No library-wide count, no in-degree, no global max/mean/quantile, no `dmax`
normaliser, no name string. Adding a theorem to the library cannot change any
existing score. Scores are only raised, never lowered, so nothing is deleted.

---

## 4. Ranking effect

Intervention: floor the frozen-rarity factor at 4 for fired items.

```
score = role_rebucketed(i) * ( rarity_frozen(i) if not FIRE(i)
                               else max(rarity_frozen(i), 4.0) )
```

The floor level was chosen on DEV as the largest value that improves NavAP
without regressing MajorAP or major-recall@4. Deltas are per-proof paired,
2,000-replicate bootstrap, 95% CI.

**DEV (192 proofs, used for selection)**

| | base | +rule | delta [95% CI] |
|---|---|---|---|
| NavigationAP | 0.8766 | 0.8829 | **+0.0063 [+0.0028, +0.0099]** |
| MajorAP | 0.8552 | 0.8536 | -0.0016 [-0.0040, -0.0001] |
| clean@1 | 0.8750 | 0.8750 | +0.0000 |
| major-recall@4 | 0.8716 | 0.8716 | +0.0000 |

**TEST-R (360 proofs, held out, read once)**

| | base | +rule | delta [95% CI] |
|---|---|---|---|
| NavigationAP | 0.9017 | 0.9131 | **+0.0115 [+0.0080, +0.0152]** |
| MajorAP | 0.8947 | 0.8967 | +0.0020 [-0.0015, +0.0058] |
| clean@1 (precision@1) | 0.9750 | 0.9750 | +0.0000 |
| major-recall@4 | 0.9258 | 0.9263 | +0.0005 [-0.0054, +0.0069] |

54 proofs improved, 8 hurt, 297 unchanged. Positive in every depth band, and
largest in the two bands that have been hardest in every previous round:

| band | base NavAP | +rule | delta |
|---|---|---|---|
| 0-10 | 0.9193 | 0.9290 | +0.0097 |
| 11-25 | 0.9166 | 0.9260 | +0.0094 |
| **26-50** | 0.8665 | 0.8849 | **+0.0184** |
| 51-75 | 0.9335 | 0.9411 | +0.0076 |
| **76-125** | 0.8909 | 0.9107 | **+0.0198** |
| 126+ | 0.8835 | 0.8873 | +0.0038 |

### How much of the available gain is this?

Oracle: apply the identical floor-at-4 to the *true* grade-2 set on TEST-R.

| | NavAP | MajorAP | clean@1 | major-rec@4 |
|---|---|---|---|---|
| base | 0.9017 | 0.8947 | 0.9750 | 0.9258 |
| **rule (recall 0.116)** | **0.9131** | 0.8967 | 0.9750 | 0.9263 |
| oracle, same floor | 0.9196 | 0.8925 | 0.9750 | 0.9233 |
| oracle, floor 8 | 0.9588 | 0.8342 | 0.9861 | 0.8887 |

At 11.6% recall the rule captures **64%** of what a perfect grade-2 detector
buys at the same intervention strength. It does so because the items it
catches are precisely the badly-mis-ranked ones: maximal role weight, minimal
rarity.

A stronger floor extracts more NavAP but starts paying in MajorAP
(floor 8 oracle: NavAP +0.057, MajorAP -0.061). That trade is a policy
decision, not a detector question, and floor 4 is the free part of it.

---

## 5. Recommendation

**Adopt the rule; it clears part of the bar, not all of it.**

- NavigationAP improves, replicated, CI excludes zero on both splits.
- precision@1 is **unchanged** (0.9750 -> 0.9750). It is already 0.975; a
  grade-2 promoter has almost nothing to fix at rank 1.
- major-recall@4 is **unchanged within noise** (+0.0005, CI spans zero).

So the honest statement is: *one of three named metrics improves, the other
two do not move in either direction.* If the bar was "all three improve", it
is not cleared. If the bar was "improve navigation without paying for it
anywhere", it is cleared cleanly — 54 proofs better, 8 worse, no metric down.

**The clean negative is the more important result.** The task's leading
hypothesis — that grade 2 is identifiable from proof-relative context (no
deeper content available, short proof, few non-glue candidates, small depth
gap) — is false in this corpus. Nine proof-relative rules and twelve
proof-relative AUCs were tested; none replicates across DEV and TEST-R. The
premise that "the same declaration is a 2 in one proof and a 1 in another" is
true, but the proof-level features we can compute do not know which.

The signal that works is not contextual at all. It is intrinsic: *head
position plus a shallow own-cone*. Applying something is a claim that it
carries the step; being two levels above the foundations means there is no
deeper thing it could be standing in for. The base model already gives
applied role its full weight — the entire contribution here is refusing to
let rarity bury it, which is exactly the failure the cross-method analysis
identified.

**Remaining gap.** 87% of inversions are grade 2 and this rule addresses
12% of grade-2 items. The other 88% are shallow, common declarations in
explicit/implicit/type-annotation positions (`LE.le`, `Subtype.mk`,
`CategoryStruct.comp`, `Eq.symm`, `congrArg`) whose grade genuinely flips
between proofs. On the evidence here, nothing in the current record separates
those. Closing that gap needs a signal the corpus does not currently carry —
term-level structure (how many times the citation occurs, where in the term
tree), not another combination of the existing per-incidence fields.
