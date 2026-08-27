# Brief 2 — Prosecution Opening

*Written by an independent agent with full repository access, instructed to
verify every claim against code and data rather than trust prose, and to go
beyond the owner's stated suspicions. Reproduced verbatim.*

---

## I. The lead charge: the recall number is circular, and the filter that deletes the most has never been tested

The defense's third pillar is "the filters lose ZERO human-written citations." That sentence is not a measurement. It is an artifact of how the answer key is built.

`src/phase4_provenance_recall.py`, lines 113–122. The ground truth `gt` is assembled from the elaborator's resolved source identifiers — and then, before anything is compared, the script applies the system's own claims filter to the answer key:

```python
if c is None or c == r or not pr[c]:      continue   # line 113
if kinds[c] in ("constructor", "recursor"): continue   # line 115
...
moves = {c for c in loadbearing(r)
         if pr[c] and kinds[c] not in ("constructor", "recursor")}   # 121–122
```

The predicate on line 122 is the predicate on lines 113–115. Any human-written citation the claims filter would drop is deleted from the denominator *first*. That is why `loss_taxonomy.not-prop-flag = 0` in `phase4_provenance_recall.json` — it is arithmetically impossible for that bucket to be non-zero. Definition 2 of METHOD.md has never had its recall measured, not once, on any sample.

How much does that filter delete? I counted it over the full dump (771,129 constants, 533,312 theorems with bodies): of 15,223,133 load-bearing citations in theorem proofs, **6,844,261 survive the position filter (45.0%), and of those only 2,799,265 survive the claims filter (40.9%)**. Compound survival: **18.4%**. The architecture deletes better than four out of five cited constants before ranking begins, and the defense describes this as "never delete."

The deleted 59% is not noise. It is every `def`, every instance, every construction — the Type-valued half of mathematics. ADR-0004 §3 concedes exactly this ("construction/representation moves (Type-valued) remain a first-class future channel"). For a proof that builds a scheme, defines a functor, or exhibits a witness, the system's ontology has no place to put the move at all.

And it shows in the output. `phase4_holdout9_results.json` reports `verdicts: {definitional: 280, empty: 239}`. That second bucket is 239 theorems where, after the two filters, **nothing at all is left** — no ranked list, no verdict, no output. Over the whole library the rate is 12.8% (68,219 of 533,312 theorems have zero surviving load-bearing claims). `phase4_holdout9.py` line ~397 counts these as `fcr.append(0)`, and line 412 drops zeros from the denominator: `live = a[a > 0]`. So 239 total extraction failures are invisible to the precision metric. ACCOUNTING_STATUS.md then folds them into "519 verdicts" — but METHOD.md step 5 defines a verdict as *every item being demoted*, which requires items. There is no ninth definition for "we found nothing." A silent failure mode is being reported as a designed output.

Two further gaps in the same measurement: line 118, `if len(gt) < 2: continue`, structurally excludes every proof with exactly one written citation — precisely the case where a miss costs 100% of the moves. And `moves` on line 121 tests only position and claims. The demotion tier, the machinery rule, the verdict rule, zoom, and attribution — six of the eight steps — are not in the recall harness at all. n=29, from 4,522 available provenance declarations.

Then look at what *is* lost, in `loss_examples`. `csSup_union_le` loses `csSup_union`, `bddAbove_union`, and `csSup_of_not_bddAbove`. `norm_lt_of_mem_ball'` loses `norm_lt_of_mem_ball`. `norm_mul_sub_norm_div_le_two_mul` loses `norm_add_sub_norm_sub_le_two_mul`. These are not incidental glue erased by `simp`. In each case the lost citation *is the key move* — the unprimed source lemma, the union lemma for the union theorem. Median recall 1.0 is doing heavy lifting for a distribution where the failures are concentrated on the one citation that mattered. "Mean 86%" understates the damage because the loss is not uniformly distributed across a proof's moves.

## II. Certification: the treatment and the instrument moved together

Round 9's headline is +1.34 points (0.9318 → 0.9452) on `top1_extended_grader`, and bar 1 is defined on that grader. The extended grader was introduced *in round 9*, and it consists of hardcoded names: `EXTRA_TACTIC_NS` (2 namespaces) and `TRUE_TWINS` (17 literal names), `phase4_holdout9.py` lines 84–88.

Its effect is not symmetric. From the results JSON: the extension moves **22** V6 rank-1s from content to non-content (glue 35→55, tactic 16→18) and only **5** of V8's (glue 38→42, tactic 12→13). On the project's own standing metric, `top1_nonmachinery_proxy`, V8's gain over V6 is **+0.42 points — eight theorems out of 1,826**. Roughly three-quarters of the certified improvement comes from a grader change shipped in the same file as the treatment, differentially penalizing the control.

Bar 2 is worse. It requires V8 tactic blames ≤ 0.8 × V6's. On the standing proxy: 16 × 0.8 = 12.8, V8 = 12. **The bar passes by 0.8 of one theorem.** One more tactic rank-1 and round 9 is a falsification.

Bar 1 — "V8 ≥ V6" — has no statistical content; any positive difference passes. The relevant scale is V6's own between-seed variance: 94.84 (round 6), 93.97 (round 7), 94.38 (round 9). Spread 0.87 points. The certified effect (0.42) is half the noise of the anchor it is measured against.

Denominators moved too. Round 4's post-hoc reading (PHASE4_CERTIFICATION.md §2) found "the gap was substantially a **denominator accounting artifact**" — proofs whose entire list is `rfl`. Round 5's fix was to adopt verdict semantics, which moves those proofs out of the denominator, and scored 91.59. The score rose because the hard cases left the sample. Today 574 of 2,400 (24%) are outside the reported denominator.

Finally, the population itself. Every holdout draws from `pool = thm & ~has_class & ...` (line 294). `has_class` comes from `mathrecord/Mathrecord/Study.lean:46–63`, which is name-based: `n.isInternalDetail`, `genSuffixes`, `startsWith "match_"`, and the hardcoded `logicCore`/`eqMachinery`/`coeRoots` sets. **245,837 of 533,320 theorems — 46% of Mathlib — are excluded from every sample the system has ever been certified on**, by a name filter. "Nothing in the system reads a name" is true of the ranking rules and false of the certification.

## III. The apparatus measure is not stable — measured, not asserted

I ran the repository's own `stability.py` (it had never been executed; no numeric output existed). Results:

**Threshold sensitivity.** Jaccard of the apparatus set against the shipped (λ=20, floor=200) set: λ=15 → 0.850; λ=30 → 0.873; floor=500 → 0.647; floor=50 → 0.650. There is no plateau. A genuine structural cliff read off a bimodal distribution would be flat under ±50% perturbation. This one moves 13–35%. (20, 200) is a tuned point.

**Margin.** For the 102 concepts, the ratio `used/(stated+1)` has p0 = 20.4, p5 = 24.0, p10 = 28.5. **Twenty of 102 sit within 2× of the line.** The defense concedes grind's `Poly` at 12.7 falls below it. That concession is load-bearing: three of the thirteen residual tactic rank-1 failures in `round9.log` are `Poly` denotation lemmas (`Lean.Grind.CommRing.Poly.denote_insert`, `Lean.Grind.Linarith.Poly.denote'_eq_denote`, `Int.Internal.Linear.Poly.denote'_eq_denote`). The one concept the measure misses causes 23% of the failures the measure exists to prevent.

**Refactor simulation.** If Mathlib states K theorems reaching each internal type: K=50 → 44 of 102 survive; K=100 → **20 of 102**; K=500 → zero.

And the mechanism is worse than "someone states a theorem." `inherited` (lines 171–189) is a **max** propagated down the definition graph, not a sum or a count. It is a step function. A single new, widely-stated definition that transitively contains an internal type flips that type *and everything beneath it* in one commit, with no gradual degradation and no warning signal. Note also that the propagation graph is `deps = deps_v if deps_v else deps_t` (line 123): for a `def` with a body, the definition's *type* is dropped from the inheritance graph entirely. That asymmetry is undocumented.

This is the direct answer to "caught the day it lands, with no edit." The mechanism argument — decision procedures encode into private vocabulary — is sound. The *implementation* of that argument is a two-threshold ratio over a max-propagated statedness count, and it is one Mathlib refactor from collapsing.

## IV. Occam's razor: the complexity is accidental, and I can show it

A system meant to outlive several Lean versions should be the simplest rule that does the job, because simplicity is the only operational proxy for auditability and drift-resistance. Every threshold is a surface that can rot silently.

Count the shipped parts: nine definitions, eight procedural steps, five declared constants. But METHOD.md line 66–68 says "Nothing else," and that is false. In `phase4_holdout9.py` alone: `LOAD_ROLES = (0,1,2,7)` (a 4-of-8 selection over binder roles); `len(set(deps_v[r]) - {r}) < 3` (line 388, an undocumented minimum-citations gate that removes 55 theorems from scoring); `indeg_v[c] <= 1 or gen[c]` in candidate expansion; three separate `range(3)` / `* 2` cycle-relaxation constants; a five-member `CONCEPT_KINDS`; a three-key sort tuple; `len(subst) == 1` in attribution. In `parent_labels.py`: `cov >= 0.49`. And a genuine spec/code divergence: METHOD.md declares "Up to 3 hops, never revisit," but `make_attr` in the certified round-9 script (lines 245–256) has **no hop cap at all** — only cycle detection. `parent_labels.py` line 175 does have `len(seen) >= 3`. The certified system and the shipped display labeler implement different attribution rules, and the canonical method document describes neither exactly.

So: has the complexity earned itself? I ran the ablation the project never ran. Using `phase4_holdout9.py` unmodified except for the sort key, on the certified seed 20260831, run once (`top1_nonmachinery_proxy`, same 1,826 denominator):

| ranking | score |
|---|---|
| V8 (demote + statement-world + depth) | **0.9480** |
| V8 minus depth key | 0.9135 |
| V8 minus statement-world key | 0.9387 |
| demotion tier only | 0.8943 |
| V6 (no apparatus) | 0.9438 |
| depth alone, no demotion, no verdicts (n=2,106) | 0.8186 |
| statement-world alone (n=2,106) | 0.7474 |

Read the marginal contributions. **Depth is worth +3.45 points. Statement-world is worth +0.93. The apparatus measure — 102 derived concepts, two thresholds, an inheritance fixpoint, and one falsified round — is worth +0.42.** The single largest contributor to the ranking is `depth`, which ADR-0004 §1 classifies as level-2, "expected to evolve," "versioned, never claimed stable," and which CONES_REPORT.md establishes is Spearman ≥0.98 with prerequisite cone size — i.e. it is a measure of library volume, the *most* refactor-sensitive quantity in the system. The rule carrying the ranking is the one the constitution says will drift, and it has never been ablated until now.

Meanwhile the bookkeeping/universality rule (definitions 5 and 8) was tested once on its own — round 3, "**Falsified**: 83.24 → 83.33 (+0.09; bar was 88)" — and shipped anyway. Round 8's entire falsification lived inside that same rule's extension.

Trajectory: V4 → V5 → V5p → V5pz → V5pzb → V5v → V6 → V8. Every round added a definition; none removed one. The gains: V5v→V6 +2.56 (matched), V6→V8 +0.42. Complexity monotone up, marginal return monotone down. That is the signature of accidental complexity accreting around a primitive that cannot express the thing being measured — not of essential complexity in the domain.

The stripped baseline has never been on a holdout. Every comparator across nine rounds (`grep "variants ="`) is a full-system variant. There is no round in which the question "does this component beat one simple rule?" was asked.

## V. The primitive is wrong for a map, and the project has already proved it

`reports/HONEST_ASSESSMENT.md`, "What failed": *"Declaration ranking hit a structural ceiling: both reviewers independently identified move-level blind spots (local hypotheses, witnesses, case structure, representation changes) that no declaration list can express."* Those four things are what a mathematician calls the move. The V5→V8 line has spent nine rounds optimizing rank-1 inside a representation the project itself has documented as unable to express the answer.

The map needs three things this architecture does not produce: typed edges (does this proof *specialize*, *dualize*, or *instantiate* the cited theorem?), cross-proof identification (the same move in 500 proofs is one map edge, not 500 list entries), and node-level salience. On the third, the project's one pre-registered test **failed**: *"the pre-registered landmark condition failed: salience − machinery-prob (2.7/5) lost to global PageRank (3.3)"*, and *"reuse-count marks glue, not importance."* An ordered list per proof is not a map; it is 533,312 unlinked lists.

And the semantic evidence, honestly stated: KEYNESS_REPORT.md's own table gives the **ranked** view — the thing METHOD.md step 6 produces — **37.7% exact, 71.0% exact-or-partial**. The defense's 56.5 / 92.8 is the *zoom* view, a display transform (step 7), evaluated on **V5v** — two versions before the system on trial. The one semantic measurement in the project does not measure the certified ranking.

## VI. What is sound

Three things, and I will not contest them. The **position filter** is a real kernel fact and its recall *was* honestly measured: `background-slot = 0` across the provenance sample means no human citation hid in an implicit or instance slot. (Caveat: role 2, "explicit argument," carries 3,981,002 of 4,130,073 kept occurrences — the filter is nearly all "not implicit," which is a weaker claim than "load-bearing.") The **kernel verdict certifier** (`defcheck`, 58/80 positively definitionally-equal) is the strongest instrument in the repository — a positive check, not a proxy. And the **falsification discipline** is genuine: round 8 was reported, eleven detector designs are recorded as dead. That culture is the project's real asset.

## What would have to be true

For the defense to be right: (1) the claims filter would have to lose nothing a mathematician would call a move — untested, and untestable by the harness as built; (2) the apparatus set would have to be stable under library evolution — measured today, and it is not; (3) round 9's gain would have to exceed the system's own seed-to-seed noise — it does not, on the standing metric; (4) declaration-level citation ranking would have to be able to express the move — the project's own reviewers say it cannot; (5) the added machinery would have to beat a stripped baseline — never asked until this morning, and the answer is that the simplest key in the system is also the biggest one.

The recommendation is not "start over." It is: stop adding definitions. Fix the recall harness so the answer key does not apply the filter under test. Publish a stripped baseline. Decide whether the unit of output is a ranked list per proof or an edge in a map — because those are different projects, and only one of them is being built.
