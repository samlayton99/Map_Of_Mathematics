# Evidence Appendix — every load-bearing claim, checked

Each item states the claim, who made it, what was done to check it, and the
outcome. "VERIFIED" means the defense confirmed a prosecution charge against
the code. Nothing here is argument; it is the record of what was run.

All new code and data in this package were produced DURING the trial, after
the charge that prompted them. Git history carries the timestamps.

---

## E1. The recall harness applied the filter under test to its own answer key

**Claimed by:** prosecution (opening §I).
**Check:** read `src/phase4_provenance_recall.py` lines 105-124.

```python
for cn in refs:
    c = idx.get(cn)
    if c is None or c == r or not pr[c]:            # <- claims filter
        continue
    if kinds[c] in ("constructor", "recursor"):     # <- claims filter
        continue
    gt.add(c)
...
moves = {c for c in loadbearing(r)
         if pr[c] and kinds[c] not in ("constructor", "recursor")}
```

The answer key `gt` and the system output `moves` are filtered by the same
predicate, so the `not-prop-flag` loss bucket could not be non-zero.

**Outcome: VERIFIED.** The defense withdrew the claim "the filters lose zero
human-written citations." It was not a measurement.

---

## E2. The corrected recall measurement

**Action:** rebuilt the harness with an UNFILTERED answer key —
every identifier the elaborator resolved from the human's source text, with no
predicate applied — in `src/recall_loss_split.py`. Loss taxonomy refined to
separate the causes. Output: `data/phase4_recall_loss_split.json`.

**Result (n=39 declarations):** mean recall **0.317**, median **0.25**.
The previously reported 0.859 / 1.0 is withdrawn.

**Loss taxonomy, 146 losses:**

| cause | n | reading |
|---|---|---|
| statement vocabulary (`Set`, `Iff`, `Nat`, `Finset.prod`, `Norm.norm`) | 51 | the theorem's own nouns; the elaborator resolves the statement too. Not moves. |
| background slot | 60 | same vocabulary in implicit/instance positions |
| erased by compilation before any term existed | 24 | unreachable by any kernel-term method; provenance channel only |
| constructors (`And.intro`, `Exists.intro`) | 8 | **disputed** — defense read as pair-assembly, prosecution as *exhibiting a witness*, which the project's own HONEST_ASSESSMENT lists as a move class |
| genuine "unfold this definition" moves | 3 | `ProbabilityTheory.iIndepSets`, `Ideal.radical`, `Int.fract` — entering through the proof, not the statement |

**Contested conclusion:** the claims filter's irreducible cost is **3 of 146**
on the defense's reading of the constructor bucket, **11 of 146** on the
prosecution's. The judge is asked to rule on the constructor bucket.

**Both sides agree:** n=39 is too small, 4,522 provenance declarations are
available, and the classification protocol should be fixed in advance before
scaling. Neither side claims this is settled.

---

## E3. The "empty" bucket is a failure mode reported as an output

**Claimed by:** prosecution (opening §I).
**Check:** `phase4_holdout9.py` — theorems with no surviving candidates append
`0`; the scorer then computes `live = a[a > 0]`, removing them from the
denominator. `ACCOUNTING_STATUS.md` reported "519 verdicts" = 280 definitional
+ 239 empty.

**Outcome: VERIFIED and FIXED.** 239 of 2,400 (12.8% library-wide) produce no
output at all. They cost the reported precision nothing. ACCOUNTING_STATUS now
carries them as a separate, named failure mode with its own section. The
defense conceded this was a reporting error, not a subtlety.

---

## E4. Attribution: specification and code diverge

**Claimed by:** prosecution (opening §IV).
**Check:** `make_attr` in the certified round-9 script had
`if not gen[c] or c in seen: return c` — cycle detection, no hop cap.
METHOD.md step 3 declares "Up to 3 hops, never revisit."
`parent_labels.py:175` enforces `len(seen) >= 3`.

**Outcome: VERIFIED and FIXED.** Hop cap added to the certified script so all
three artifacts agree with the specification.

---

## E5. The grader changed in the same round as the treatment

**Claimed by:** prosecution (opening §II).
**Check:** `EXTRA_TACTIC_NS` (2 namespaces) and `TRUE_TWINS` (17 literal
names) were introduced in `phase4_holdout9.py`, the same file as the V8
treatment. From `phase4_holdout9_results.json`, the extension reclassifies 22
of V6's rank-1s and only 5 of V8's.

| metric | V6 | V8 | gain |
|---|---|---|---|
| `top1_nonmachinery_proxy` (standing metric) | 0.9438 | 0.9480 | **+0.42** |
| `top1_extended_grader` (introduced this round) | 0.9318 | 0.9452 | +1.34 |

V6 anchor across rounds: 94.84, 93.97, 94.38 — spread **0.87**.

**Outcome: VERIFIED.** The defense adopted **+0.42 points (eight theorems)** as
the honest headline and recorded in METHOD.md that this is inside the
seed-to-seed noise of the anchor it is measured against. The bars were
declared in the file before the run, but shipping an instrument change with a
treatment is conceded as bad practice.

---

## E6. Certification samples exclude 46% of Mathlib by a name-based rule

**Claimed by:** prosecution (opening §II).
**Check:** every round draws from `pool = thm & ~has_class & ...`; `has_class`
derives from `classify` in `mathrecord/Mathrecord/Study.lean:46-63`, which
tests `n.isInternalDetail`, `genSuffixes`, `startsWith "match_"`, and
hardcoded `logicCore` / `eqMachinery` / `coeRoots` name sets.

**Outcome: VERIFIED.** METHOD.md now states plainly: the ranking rules read no
names, the CERTIFICATION does, and no certified number describes the excluded
half. Both the sampling filter and the grader are evaluation scaffolding that
is discarded with the grader, and neither touches system output — but the
defense's unqualified "nothing reads a name" was wrong as stated.

---

## E7. Threshold sensitivity — claim, counter-claim, and the defense's retraction

**Prosecution (opening §III):** ran the repository's never-executed
`stability.py`. Jaccard of the apparatus set vs the shipped (20, 200) point:
λ=15 → 0.850, λ=30 → 0.873, floor=500 → 0.647, floor=50 → 0.650. No plateau;
20 of 102 concepts sit within 2x of the line. Refactor simulation: at +100
statements per internal type, 20 of 102 survive; at +500, zero.

**Defense (rebuttal §7):** ran `src/apparatus_sensitivity.py`, 15
configurations. Across a 4x swing of the apparatus set (53 to 216 concepts),
top-1 moved 0.9339 → 0.9333, and tactic blames (20) and verdict counts (245)
were **identical in every configuration**. Argued: set identity churns,
output does not.

**Prosecution (rebuttal):** identical integers across a 4x swing is not
robustness but *inertness* — you cannot claim both "thresholds are not
load-bearing" and "the measure halved automation junk"; also, the sweep ran on
the dev seed, never on the certified seed.

**Defense's own follow-up check (post-rebuttal):** diagnosed the two residuals
the prosecution flagged, by ingredient:

```
Mathlib.Tactic.Abel.subst_into_negg
   NegZeroClass.toNeg            used=11017 stated=9292 ratio=1.2   apparatus=False

Mathlib.Tactic.FieldSimp.NF.pow_eq_eval
   Mathlib.Tactic.FieldSimp.NF        used=545 stated=29 ratio=18.2 apparatus=False
   Mathlib.Tactic.FieldSimp.NF.eval   used=545 stated=29 ratio=18.2 apparatus=False
   Mathlib.Tactic.FieldSimp.NF.instPowNat used=129 stated=3 ratio=32.2 apparatus=False
```

The second case clears the 20x ratio and fails only the **200-use floor**
(129 uses). On the certified seed, that constant decides an outcome.

**Outcome: DEFENSE RETRACTED its own claim.** The dev-sample invariance is
real but sample-specific and was over-read. The corrected statement, now in
METHOD.md and ACCOUNTING_STATUS.md: the thresholds are not load-bearing for
the concepts that carry the effect (ratios 100-2400x), while boundary
concepts near the floor do change individual outcomes. The sweep has still not
been run on the certified seed.

---

## E8. The `Poly` charge — prosecution withdrew

**Prosecution (opening §III):** grind's `Poly` falling below the ratio line
"causes 23% of the failures the measure exists to prevent," citing three
residual rank-1s.

**Defense (rebuttal §6):** all three — `Int.Internal.Linear.dvd_solve_combine`,
`Lean.Grind.CommRing.Poly.denote_cancelVar`, `Lean.Grind.Linarith.eq_coeff` —
carry `root_in_tactic_ns: True` in the round-9 log. They are theorems inside a
tactic's own development, where citing that tactic's denotation lemmas is
correct and the goal-relevance clause spares them deliberately.

**Outcome: REFUTED. Prosecution withdrew the charge on the merits.**

---

## E9. The residual taxonomy was partly false

**Claimed by:** prosecution (rebuttal), arising from checking E8.
ACCOUNTING_STATUS had described the whole automation residual as
"logic-shaped bridge lemmas ... the measure cannot see them and arguably
should not."

**Check:** two of the eight genuine residuals are not logic-shaped —
`AlgebraicTopology.DoldKan.Q_succ` ← `Mathlib.Tactic.Abel.subst_into_negg`,
and `WeierstrassCurve.exists_variableChange_isCharThreeNF` ←
`Mathlib.Tactic.FieldSimp.NF.pow_eq_eval` — both tactic normal-form
vocabulary applied to real mathematics.

**Outcome: VERIFIED and CORRECTED.** Diagnosed by ingredient (see E7) into
three distinct classes: a **structural blind spot** (a tactic's substitution
lemma written entirely in ordinary algebraic vocabulary carries no apparatus
fingerprint; no threshold fixes it), a **threshold miss** (fails the 200-use
floor), and **genuine logic restatements** (a ranking question, not a
machinery question). ACCOUNTING_STATUS rewritten accordingly.

---

## E10. The `inherited` statedness count is a max, not a sum

**Claimed by:** prosecution (rebuttal).
**Check:** the propagation loop takes, for each concept, the maximum
statement-count over every concept whose definition transitively contains it.

**Consequence, as argued and not contested by the defense:** the retirement
trigger is not "the community wrote 500 theorems about `Constraint`." It is
*one* wrapper definition containing `Constraint` that someone states 500
theorems about — which retires `Constraint` and every concept beneath it
simultaneously, in one commit, with no intermediate state. A sum would degrade
smoothly.

**Outcome: STANDS AGAINST THE DEFENSE.** This is the sharpest surviving
longevity charge and is untouched by any threshold sweep. The defense's
"the measure retires a concept once people talk about it" reading requires a
sum and the code has a max.

---

## E11. Component ablation — what the complexity buys

**Both sides ran one.** Neither had existed before this trial.

**Defense** (`src/v8_ablation.py`, dev seed 20260819, extended grader,
14 configurations, `data/v8_ablation.json`):

| config | top-1 | tactic junk |
|---|---|---|
| V8 full | 0.9344 | 20 |
| − position filter | 0.8863 | 20 |
| − claims filter | 0.9034 | 32 |
| − logic-only demotion | 0.8260 | 23 |
| − apparatus demotion | 0.9307 | 26 |
| − attribution | 0.9113 | 20 |
| − zoom | 0.9288 | **12** |
| − statement-world key | 0.9286 | 20 |
| − depth key | 0.9055 | 21 |
| depth only, no filters, no tiers | 0.7707 | 15 |
| position+claims+depth | 0.7639 | 17 |
| V5v-like (no apparatus) | 0.8697 | 13 |

**Prosecution** (certified seed 20260831, standing metric, same 1,826
denominator): V8 0.9480; − depth 0.9135; − statement-world 0.9387; demotion
tier only 0.8943; V6 0.9438; depth alone 0.8186; statement-world alone 0.7474.

**Contested:** the defense's "logic-only demotion +10.8" is, per the
prosecution, a denominator artifact — removing the rule also removes verdict
semantics, returning ~280 all-bookkeeping proofs to the denominator, which is
the same artifact round 4 diagnosed and round 5 fixed. The prosecution's
controlled comparison puts **depth** first at +3.45.

**Agreed by both sides:**
- Stripped baselines land at **0.73-0.82**; the full system at **0.93-0.95**.
  The complexity is not decorative.
- The apparatus measure is worth **+0.42** on the standing metric.
- **Zoom costs junk**: it buys +0.56 top-1 while raising tactic blames from
  12 to 20. Never measured before this trial.
- Marginal return is falling: V5v→V6 +2.56, V6→V8 +0.42, with complexity
  monotonically increasing across every round.

---

## E12. The semantic measurement does not measure the certified ranking

**Claimed by:** prosecution (opening §V). **Check:** `keyness_results.json`,
primary 23-proof panel, three blind raters:

| view | rank-1 is the key move, exactly | exactly or nearly |
|---|---|---|
| **ranked** (METHOD.md step 6 — the ranking itself) | **37.7%** | **71.0%** |
| **zoom** (step 7 — the shipped display) | 56.5% | 92.8% |

Measured on V5v, two formulations before the system on trial.

**Outcome: VERIFIED.** The defense conceded that quoting 56.5/92.8 as the
ranking's semantic score, as its opening did, was wrong; it is the display's
score, on an older system.

---

## E13. What the project's own documents already concede about the goal

`reports/HONEST_ASSESSMENT.md`: *"Declaration ranking hit a structural
ceiling: both reviewers independently identified move-level blind spots
(local hypotheses, witnesses, case structure, representation changes) that no
declaration list can express."*

The same report records that the pre-registered landmark-salience test
**failed** (2.7/5, losing to global PageRank at 3.3), and that "reuse-count
marks glue, not importance."

**Outcome: UNCONTESTED BY BOTH SIDES.** The defense did not contest question
two. Both parties agree the architecture produces neither typed edges nor
cross-proof identification, and that the remaining goal posts in
ACCOUNTING_STATUS contain no item for either.

---

## Summary of the trial's effect on the system

Fixed during the trial: the recall harness (E1/E2), the empty-bucket
accounting (E3), the attribution hop cap (E4), the residual taxonomy (E9),
the headline metric (E5), and the name-based-certification disclosure (E6).

Retracted by the defense: the threshold-inertness claim (E7).

Withdrawn by the prosecution: the `Poly` charge (E8).

Still open and unresolved: the constructor/witness bucket (E2), the max-vs-sum
propagation defect (E10), scaling the corrected recall harness, and the
question of what primitive the map actually requires (E13).
