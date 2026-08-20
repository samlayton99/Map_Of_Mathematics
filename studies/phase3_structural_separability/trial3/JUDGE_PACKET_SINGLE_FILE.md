# MathMap Trial 3 — Complete Packet for the Judge

Single-file concatenation of the judge package. Section separators are
horizontal rules with the source filename. The full package, including the
raw data JSONs and the code for every measurement cited, accompanies this
file as a zip.

Everything below is verbatim from the repository at the close of the trial.

---


<!-- ==================== README_FOR_THE_JUDGE.md ==================== -->
# Trial 3 — Package for the External Judge

Date: 2026-08-20. Prior rulings by this judge (accept-with-conditions, Phase 4
certification program) were executed; see `CASE_HISTORY_ADDENDUM.md` §0.

## What you are ruling on

Two questions, put by the program owner:

**Q1.** Is this the right structure/procedure to move forward on, to produce
the best and cleanest ranking of the statements/citations in a proof?
"Best and cleanest" means: most reflecting how a mathematician would think of
the proof, and how simple it is. Everything is relative to the complexity of
the proof — **a rudimentary proof that is only glue, reported as glue, is not
a failure.**

**Q2.** Is this the right structure/procedure to move forward on, to achieve
the project's actual stated goal — a navigable map of mathematics?

## The owner's standing constraints (these bind the answer)

1. No naming conventions, no string/namespace rules, no learned or
   probabilistic scoring anywhere in the measure.
2. Fixes must be robust to all future Lean versions, must approach 100% as
   the library deepens, and must never be patchwork.
3. At this stage, **filtering out a key move is more damaging than admitting
   junk.**
4. Precision and recall must not drift as Lean evolves.
5. Simplicity is a design principle, not a preference: it is the operational
   proxy for auditability and drift-resistance (Occam).

## The owner's stated suspicions, which the prosecution was told to press

- The current solution may be patchwork; longevity is the primary worry.
- Arbitrary hardcoded constants are suspect.
- He is not convinced of the recall.
- He is not convinced of the precision.

## Ground rule imposed on the prosecution

The grader is an automated name/namespace-based labeler used **only for
evaluation** and will be discarded when the work is done. Attacks whose entire
content is "the proxy metric is a proxy" were ruled weak. This did not exempt
the grader from scrutiny where it distorts a conclusion.

## How to read this package

Read in this order:

1. `CASE_HISTORY_ADDENDUM.md` — everything learned since the last handoff,
   including the full certification chain and every falsified design.
2. `METHOD.md` — the system on trial (V8), stated so it can be reproduced
   from scratch.
3. `briefs/1_DEFENSE_OPENING.md`
4. `briefs/2_PROSECUTION_OPENING.md`
5. `briefs/3_DEFENSE_REBUTTAL.md`
6. `briefs/4_PROSECUTION_REBUTTAL.md`
7. `EVIDENCE.md` — every load-bearing claim from either side, checked against
   the code by the defense during the trial, with file:line receipts, marked
   VERIFIED / REFUTED / CORRECTED.
8. `ACCOUNTING_STATUS.md` — the current marked ledger of every failure class.

## Procedural facts you should know

- The prosecution was an **independent agent** with full repository access,
  instructed to verify claims against code rather than trust prose. It was
  not shown a preferred conclusion.
- The defense **conceded five charges outright** and fixed three of them
  during the trial; the corrections are in this package and in the git
  history, not merely promised.
- The prosecution **withdrew one charge** on the merits after the defense
  produced contrary evidence.
- The defense **retracted one of its own rebuttal claims** after diagnosing a
  case that contradicted it. That retraction is in `EVIDENCE.md` item E7.

## The specific rulings requested

1. On Q1 and Q2 as stated.
2. Whether the apparatus measure (METHOD.md definition 9) is a legitimate
   answer to the longevity constraint, or a tuned artifact. The parties agree
   the *mechanism* argument is sound and disagree about whether the
   *implementation* — a two-threshold ratio over a max-propagated statedness
   count — inherits that soundness.
3. Whether the corrected recall picture (mean 0.317 against an unfiltered
   answer key, with 3-to-11 of 146 losses being genuine inexpressible moves)
   satisfies constraint 3 above, or violates it.
4. Whether the certification chain (nine rounds, seeds burned, specification
   changed between rounds, two rounds falsified and reported) constitutes
   genuine falsification or a garden of forking paths.
5. What the next unit of work should be. The parties agree the current
   accounting's remaining goal posts do not contain the item the map needs.


---


<!-- ==================== CASE_HISTORY_ADDENDUM.md ==================== -->
# Case History Addendum — from the last judge ruling to this trial

Continues `CASE_HISTORY.md` (in the trial-2 package), which covers everything
from the Phase 3 handoff through the second trial. This addendum covers what
happened after the judge's accept-with-conditions ruling. Read this first if
you are the judge; it is the context the briefs assume.

## 0. The prior ruling, and how it was executed

The judge ruled ACCEPT WITH CONDITIONS and set a certification program:
implement the substrate exactly, run fresh pre-registered holdouts once each,
build a provenance sidecar, treat single-use as an attribute rather than a
container, run a cross-version test, convene a keyness panel of hard proofs,
and amend the constitution to distinguish epistemic layers.

Executed: all of it except the cross-version test, which remains unrun.
ADR-0004 (epistemic layers) was written first and governs everything since:
kernel facts / library-relative values / elaboration-provenance / semantic.
"Future-proof" was redefined to mean the RELATION's meaning survives, while
library-relative values legitimately evolve. Proxy metrics were renamed to
say they are proxies (`top1_nonmachinery_proxy`, never "precision").

## 1. The certification chain, complete

Every round was registered in the script's docstring before running, run once,
on a fresh seed disjoint from all prior samples.

| round | seed | outcome |
|---|---|---|
| dev | 20260819 | development only |
| 1 | 20260820 | V4hist 89.85 replicates dev's 90.25 — no overfitting |
| 2 | 20260821 | claims-filter correction; V5pz 80.75 |
| 3 | 20260822 | **FALSIFIED**: bookkeeping demotion, +0.09 against a bar of 88 |
| 4 | 20260824 | **FALSIFIED**: breadth zoom, 81.3 |
| 5 | 20260825 | **CERTIFIED** V5v 91.59 — verdict semantics |
| 6 | 20260828 | **CERTIFIED** V6 94.84 — forwarder attribution |
| 7 | 20260829 | **FALSIFIED**: author-written priority (V7 byte-identical to V6) |
| 8 | 20260830 | **FALSIFIED** by its own bar — see §3 |
| 9 | 20260831 | **CERTIFIED** V8 — apparatus measure |

Rounds 3 and 4 taught the program its most useful lesson: both were mechanism
guesses made from theory rather than from reading cases. After round 4 the
practice changed to reading failure cases first. Round 4's post-hoc reading
found that the apparent V4-vs-V5 gap was substantially a **denominator
accounting artifact** — proofs whose entire candidate list is `rfl` are
true-by-definition lemmas, which the historical variant silently exited from
the denominator. Round 5 fixed that honestly with verdict semantics. The
prosecution in this trial argues that fix also inflated the score by removing
hard cases; see brief 2 §II.

## 2. What V8 added (the system on trial)

Two kernel sort facts were added to the extractor (dump v6, then v7, 771,129
constants, ~140 s, zero fallbacks):

- `ps` — the constant's type telescopes to `Prop`; it IS a proposition or a
  predicate, as opposed to data.
- `ar` — arity, the number of binders the type telescopes through.

Together they define a **bare proposition** (Prop-sorted, arity 0). Exactly
five exist in Mathlib: `True`, `False`, `UnivLE`, `FermatLastTheorem`,
`RiemannHypothesis`.

The **apparatus measure**: a concept is apparatus when it is used far more
than it is stated — cited by more than 200 proofs, and more than 20x the
number of human theorem statements mentioning it (statement counts inherited
down the definition graph). 102 concepts qualify: omega's `Constraint` and
`Coeffs`, grind's `Expr`, NormNum's `IsNat`, the internal linear-arithmetic
types. An item is **machinery for T** when one of its ingredients is apparatus
and none of its ingredients appear in T's own statement — so a theorem *about*
omega's `Constraint` keeps its constraint lemmas. Machinery ranks below real
moves; an all-machinery list yields "discharged by automation".

Certified round 9: +0.42 points on the standing metric (the +1.34 figure
depends on a grader introduced in the same round — see EVIDENCE E5), tactic
rank-1 blames 18 → 13, two real moves lost in 1,826.

Also shipped: **machine-generated display labels**. 77.1% of 239,625 generated
constants now resolve to what they are part of, by three name-free rules
(the single substantive claim in their own proof; the single definition whose
construction cites them; the subject of their own statement). Display only.

## 3. Round 8, falsified, and why it matters to the judge

Round 8 ran the same design with one difference: "bare proposition" was tested
as "mentions no other constants" rather than "takes no arguments." A predicate
over abstract type variables mentions no constants either, so
`Function.Injective` and `Nonempty` were misfiled as bare propositions, and
real moves ("an equivalence is injective") collapsed into definitional
verdicts — 31 losses against a declared ceiling of 5.

It was reported as a falsification, the extractor was changed to read arity
from the kernel, and round 9 re-ran the corrected specification on a fresh
seed. The seed is burned and recorded as burned.

## 4. The falsification record — eleven designs, none shipped

Six automation detectors were tested and killed before the apparatus measure:
raw statement-exposure (AUC 0.40), root-grain strategy signatures, Lean's own
registries (probe: the simp registry holds zero `._simp_N` twins; the matcher
registry rejects splitters), rare-concept co-mention islands (giant component
99.9%), weighted islands, and author-written priority at both file and
declaration grain.

Three more died during V8's development: two capsule-atomization rules (close
a machine-generated block if any inner claim is machinery; close it if the
top-ranked inner claim is machinery) both hid real moves; and an audience test
("cited only by machine-generated proofs") which turned out to measure whether
a proof block got outlined, not whether it was automation — `ring` emits
inline into human theorems, while `byContradiction` blocks get outlined.

Two more were falsified as registered rounds (3, 4). Round 7 falsified an
author-written sort key by proving it cannot fire: in automation-heavy proofs
nothing is author-written, and V7 came out byte-identical to V6.

The defense offers this record as evidence the program does not ship
unverified detectors. The prosecution accepts it as the project's real asset
while arguing it does not license the parts that did ship.

## 5. Instruments built for auditing the system

- **Provenance sidecar** (`mathrecord provenance`): what Lean's elaborator
  resolved from the human's source text — an answer key that does not pass
  through this extraction. Measured but **not merged into the views**.
- **Exact module resolver** (`mathrecord modules`): kills a shortname
  collision bug class that had corrupted three earlier audits.
- **Kernel verdict certifier** (`mathrecord defcheck`): asks Lean itself
  whether a "holds by definition" verdict's two sides are definitionally
  equal. 58 of 80 positively certified; union with source reads 64/80; 10 of
  the remainder are machine congruence lemmas correct by construction; zero
  false verdicts found by any channel. The prosecution calls this the
  strongest instrument in the repository.

## 6. Standing owner rulings that constrain the answer

- Thin-list plumbing on trivial proofs is FINE, not a precision hit.
- Improving the grader is WASTED EFFORT; the semantic instrument is the blind
  keyness panel.
- No naming conventions, no probabilistic scoring, in the measure.
- Filtering out a key move is worse than admitting junk.

## 7. Where the numbers stand entering the trial

- Standing proxy: V8 94.80 vs V6 94.38 on the certified seed; anchor spread
  across rounds 0.87.
- Semantic, blind panel, n=23, on V5v: ranking 37.7% exact / 71.0% near;
  zoom display 56.5% / 92.8%.
- Recall: **withdrawn and re-measured during the trial.** See EVIDENCE E1/E2.
- Automation junk at rank 1: ~0.44% after V8, from ~1.1%.
- 12.8% of theorems library-wide produce no output at all (EVIDENCE E3).


---


<!-- ==================== system/METHOD.md ==================== -->

# THE SYSTEM ON TRIAL — METHOD.md (verbatim, current)

# THE METHOD (V8) — complete, reproducible, no jargon

## The nine definitions everything uses

1. Entry: any named thing in compiled Mathlib (771,129). Each has a statement
   (what it asserts / what kind of object it is) and usually a body (proof or
   construction). Both are walkable data structures.
2. Claim: an entry whose statement is a true/false assertion (Lean records
   this: type lives in Prop), excluding entries Lean marks constructor or
   recursor (rules for building/taking apart logical shapes -- the form of
   goals, not steps of arguments). claim = Prop-typed, not ctor, not recursor.
3. Depth: 0 if the body (or statement, when bodyless) mentions no other
   entries; else 1 + max depth over everything mentioned. One library pass.
4. Statement-world of T: names in T's statement; add everything their
   definitions mention; repeat to closure. "What stating T already needs."
5. Logic-only: measure every concept's commonness = fraction of all theorem
   statements mentioning it; >2% = everywhere-words (measured, not chosen:
   equality, naturals, sets, <=, membership). An entry's ingredients are the
   concepts in its statement under the 2% line. An entry is logic-only if it
   has no ingredients, or all of them are bare propositions (def. 8).
6. Machine-generated: no recorded source-file location (Lean logs locations
   for human-written declarations only; verified to separate cleanly).
7. Used-once: exactly one entry in the library mentions it in a body.
8. Bare proposition: a concept that IS a proposition rather than one ABOUT
   something -- Lean's own sort test says its statement is `Prop`, and it
   takes no arguments. Exactly five exist in Mathlib (True, False, UnivLE,
   FermatLastTheorem, RiemannHypothesis). A predicate like `Function.Injective`
   is Prop-sorted but takes arguments, so it is not bare.
9. Apparatus: a concept that is used far more than it is stated. Count, per
   concept, (a) how many human theorem statements mention it, inherited down
   the definition graph (a statement about Ring states everything Ring's
   definition contains), and (b) how many proofs in the library cite a claim
   having it as an ingredient. Apparatus = not bare, under the 2% line,
   (b) > 200, and (b) > 20x(a+1). This is what a decision procedure's private
   vocabulary looks like: 102 concepts, all of them encoding machinery
   (omega's Constraint and Coeffs, grind's Poly, NormNum's IsNat, the
   internal linear-arithmetic types). Nothing is named; the test is a ratio.

## The recipe for one theorem T

1. Walk T's body recording, per mentioned entry, its positions:
   (a) applied as a step, (b) explicit argument, (c) let-value,
   (d) implicit argument, (e) typeclass slot, (f) type annotation,
   (g) unresolvable slot. KEEP entries occurring in {a,b,c,g}; set aside
   those only in {d,e,f} (kept in the record, not moves).
2. Keep only claims (def. 2).
3. Resolve machine names: for each kept machine-generated item, run steps
   1-2 on ITS body, drop logic-only results; if exactly one claim remains,
   replace the item by it (a derived form proves itself from its original,
   so the original is in its body). Up to 3 hops, never revisit.
4. Mark machinery: an item is machinery for T when one of its ingredients is
   apparatus (def. 9) AND none of its ingredients appear in T's own
   statement. The second half is what keeps the measure honest -- a theorem
   ABOUT omega's Constraint keeps its constraint lemmas as real moves.
5. Verdict: if every item is logic-only or machinery, output "holds by
   definition/logic" (all logic-only) or "discharged by automation" and stop.
6. Rank by three keys: (i) items that are neither logic-only nor machinery
   first; (ii) NOT in T's statement-world first; (iii) deeper first.
7. Zoom (display): while the top item is used-once and unopened, replace it
   by its own kept-claims (name kept as group label), re-sort; max 8 opens.
8. Label (display only): a machine-generated item is shown as what it is
   part of -- the single substantive claim in its own proof, else the single
   definition whose construction cites it, else the subject of its own
   statement. Unresolved ones keep their raw name. The record is unchanged.

Constants: the measured 2% line, the apparatus thresholds (200 uses, 20x
ratio), 3 attribution hops, 8 zoom opens, "unresolvable slot counts as kept"
(conservative), a 4-of-8 selection of load-bearing binder roles, and a
minimum of 3 distinct citations for a proof to be scored. Sensitivity of the
apparatus thresholds is measured (data/apparatus_sensitivity.json): across a
4x swing in the size of the apparatus set, top-1 moves 0.06 points and the
tactic-blame and verdict counts do not move at all.

Evaluation caveat, stated plainly: the ranking rules read no names, but the
CERTIFICATION does. Every sample is drawn from theorems carrying no
classification flag, and those flags come from a name-based classifier
(mathrecord/Mathrecord/Study.lean), which excludes about 46% of Mathlib's
theorems from every round ever run. The grader is name-based too. Both are
evaluation scaffolding, both are discarded with the grader, and neither
touches the system's output -- but no certified number describes the
excluded half.

Certified (round 9, seed 20260831, run once, data/phase4_holdout9_results.json):
V8 = 94.80% top-1 non-machinery proxy against V6's 94.38 on the same sample --
a gain of 0.42 points, eight theorems. (A stricter grader was introduced in
the same round and reports 94.52 vs 93.18; because an instrument change
shipped alongside the treatment, the STANDING-metric gain of +0.42 is the
honest headline, not the +1.34. The anchor's own seed-to-seed spread is 0.87,
so this gain is within the noise of the baseline it is measured against.) tactic-internal rank-1 blames
cut 18 -> 13; real moves lost to the new rule: 2 in 1,826. Earlier rounds:
V6 certified 94.84 (round 6), replicated 93.97 (round 7).

Round 8 (seed 20260830) ran this same design and was FALSIFIED by its own
declared bar: "bare proposition" was tested as "mentions no constants",
which a predicate over abstract types also satisfies, so `Function.Injective`
and `Nonempty` were misfiled as bare and real moves ("an equivalence is
injective") collapsed into definitional verdicts -- 31 such losses against a
ceiling of 5. The extractor now reads arity from the kernel telescope
(dump v7 field `ar`) and round 9 re-ran the corrected spec on a fresh seed.

Longevity of the apparatus measure: it names nothing and knows nothing about
omega, grind, or any particular tactic. It measures a relation -- used far
more than stated -- that any decision procedure must exhibit, because a
procedure works by encoding goals into its own vocabulary and proving
denotation lemmas about that vocabulary, which is therefore cited by
thousands of proofs and stated in almost no theorems. A replacement for
omega would be caught the day it lands, with no edit. Per ADR-0004 the
MEANING is fixed; the 102 concepts it currently selects are a level-2
library-relative value that legitimately changes as the library changes.

Verdict certification: "holds by definition" outputs are now positively
checkable by the kernel (`mathrecord defcheck`: are the statement's sides
definitionally equal?). On the audited sample: 58/80 kernel-certified.


---


<!-- ==================== briefs/1_DEFENSE_OPENING.md ==================== -->
# Brief 1 — Defense Opening

*Delivered first, before the prosecution had written. Reproduced verbatim.
Note that pillar 3 of this statement was subsequently withdrawn by the defense
itself; see brief 3, concession 1.*

---

The question is whether this is the right STRUCTURE to carry forward, not
whether it is finished.

**1. THE ARCHITECTURE IS ONE IDEA APPLIED FOUR TIMES, NOT FOUR PATCHES.**
Every component has the same shape: measure a relation over the compiled
library, use it to ORDER candidates, never delete. Position (is this citation
load-bearing in the proof term?). Claim-hood (is this a proposition, and not a
constructor/recursor?). Universality (is this concept everywhere, so
mentioning it says nothing?). Apparatus (is this concept used far more than it
is stated?). Each answers one question: how much does this citation
distinguish THIS proof from any other proof? The system ranks by
informativeness relative to the theorem's own statement-world, and says so
when nothing informative is left ("holds by definition" / "discharged by
automation"). The test of patchwork is whether removing one piece forces a
special case elsewhere. It does not: each is an independent measured relation
over the same record, each certified separately on its own fresh
pre-registered sample.

**2. LONGEVITY IS ARGUED AT THE LEVEL OF MECHANISM, NOT OBSERVATION.**
The apparatus measure knows nothing about omega, grind, ring, or any tactic.
It detects one relation: used far more than stated. That relation is FORCED by
how decision procedures work — a procedure encodes goals into a private
vocabulary and proves denotation lemmas about that vocabulary, so the
vocabulary is cited by thousands of proofs and stated in almost no theorems.
Any replacement for omega must do the same thing to be a decision procedure,
so it is caught the day it lands, with no edit. The same holds for the rest:
"load-bearing position" is a fact about the proof term, "Prop-typed and not a
constructor/recursor" is a kernel classification, "used once" is a graph fact.
Nothing in the system reads a name. Receipt: eleven name-based or heuristic
detector designs were tried and falsified, and none shipped.

**3. RECALL IS PROTECTED STRUCTURALLY, THEN MEASURED.**
Nothing is ever removed. Demotion changes order; zoom opens containers; a
verdict is a statement about an ordering having no informative content, with
the underlying list still present. A wrongly demoted move sits at rank 5, not
in a bin. That is the deliberate answer to "filtering a key move is more
damaging than junk." Measured against an answer key that never passes through
this extraction (what Lean's elaborator resolved from the human's own source
text): the filters lose ZERO human-written citations. End-to-end median 100%,
mean 86%, and every single loss is a citation Lean itself erased during
compilation before anything existed to extract — recoverable only from the
provenance channel, which is built and measured but not yet merged into the
views.

**4. PRECISION, STATED AT THREE LEVELS, HONESTLY.**
Proxy agreement 94.8 / 94.5 (round 9, fresh seed, run once). True rate after
reading every failure case in the ledger: roughly 97. Semantic, from a blind
panel of three independent raters who named the key move before seeing any
system output: rank-1 is the key move 56.5% exactly, 92.8% exactly-or-nearly,
n=23.

**5. CONCESSIONS, VOLUNTEERED.**
Five constants live in the method: the 2% universality line, a 200-proof use
floor, a 20x used-over-stated ratio, 3 attribution hops, 8 zoom opens. Only
the first is read off a measured distribution. Grind's `Poly` (ratio 12.7)
falls below the 20x line and is NOT caught as apparatus. The cross-version
test is unexecuted. Keyness is n=23 and recall is n=29. V8's measured gain
over V6 is about 1.3 points. Ranking below rank 1 has never been measured at
all.


---


<!-- ==================== briefs/2_PROSECUTION_OPENING.md ==================== -->
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


---


<!-- ==================== briefs/3_DEFENSE_REBUTTAL.md ==================== -->
# Brief 3 — Defense Rebuttal

*The measurements cited as new in this brief were run during the trial, before
it was written. Code and data are in the package. Reproduced verbatim.*

---

I concede five charges outright, three of them serious, and I fixed or measured each before writing this.

**1. THE RECALL HARNESS WAS CIRCULAR.** You are right, and it is the worst defect you found. `phase4_provenance_recall.py:113-122` filters the answer key by the predicate under test, so `not-prop-flag = 0` was arithmetically forced. "The filters lose zero human-written citations" was not a measurement and I withdraw it.

I rebuilt the harness with an unfiltered answer key (`src/recall_loss_split.py`, committed) and ran it. Against every elaborator-resolved source identifier, mean recall is 0.317, median 0.25 — not 0.86. That is the honest number for that answer key.

But the loss taxonomy decides what it means. Of 146 losses: 51 are the theorem's OWN STATEMENT VOCABULARY (`Set`, `Iff`, `Nat`, `Finset.prod`, `Norm.norm` — the elaborator resolves every identifier the human typed, statement included, and these are not moves by anyone's definition); 60 are background slots, overwhelmingly the same statement vocabulary in implicit positions; 24 are elaboration-erased before any term exists; 8 are constructors (`And.intro`, `Exists.intro`) assembling a pair. The claims filter's irreducible cost — real moves it cannot express — is THREE of 146, and all three are the same class: "unfold this definition" (`ProbabilityTheory.iIndepSets`, `Ideal.radical`, `Int.fract` entering through the proof, not the statement).

So: your methodological charge lands completely, and the corrected measurement bounds the damage at ~2% of losses, in exactly the class ADR-0004 and HONEST_ASSESSMENT already document. Your "18.4% survival = four in five citations deleted" is arithmetically right and rhetorically wrong: the deleted majority is statement vocabulary and implicit-position noise, not moves. What you have not shown, and what I now cannot rule out, is the rate of that 3-per-146 class at scale. n=39.

**2. THE EMPTY BUCKET IS A FAILURE REPORTED AS AN OUTPUT.** Conceded without qualification. 239 theorems produce nothing, `live = a[a>0]` drops them from the denominator, and ACCOUNTING_STATUS folded them into "519 verdicts". A verdict requires items to demote; "we found nothing" is a different event and needs its own name and its own number. That is a reporting error I made, not a subtlety.

**3. SPEC/CODE DIVERGENCE ON ATTRIBUTION.** Conceded and verified: `make_attr` in the certified round-9 script has cycle detection but no hop cap; METHOD.md claims "up to 3 hops"; `parent_labels.py` enforces 3. Three artifacts, two behaviours, one document describing neither. Being cycle-safe means it terminates, not that it matches the spec.

**4. THE GRADER MOVED WITH THE TREATMENT.** Conceded as practice. The extension was declared in the file before the run, but shipping an instrument change alongside a treatment in the same round is exactly the error the certification discipline exists to prevent. The honest headline is the STANDING metric: V8 94.80 vs V6 94.38, +0.42 points, eight theorems. I will report that number.

**5. NAME-BASED SAMPLING POPULATION.** Conceded. `~has_class` derives from `Study.lean`'s name-based classifier and excludes 46% of theorems from every sample ever certified. "Nothing reads a name" is true of the ranking rules and false of the certification, and I stated it without that qualification.

## NOW WHAT I CONTEST.

**6. THE POLY CLAIM IS WRONG ON THE MERITS.** You wrote that grind's `Poly` falling below the threshold "causes 23% of the failures the measure exists to prevent", citing three residuals. I checked all three in `round9.log`: `Int.Internal.Linear.dvd_solve_combine`, `Lean.Grind.CommRing.Poly.denote_cancelVar`, `Lean.Grind.Linarith.eq_coeff` — every one carries `root_in_tactic_ns: True`. These are theorems inside a tactic's own development, where citing that tactic's denotation lemmas is the CORRECT answer, and the goal-relevance clause spares them deliberately. They are not failures. The concession you called load-bearing carries nothing.

**7. YOU MEASURED SET IDENTITY; I MEASURED OUTPUT.** Your Jaccard numbers are real, and irrelevant to the claim that matters. I swept both constants (`apparatus_sensitivity.py`, committed): ratio 10x-50x crossed with floor 50-500, fifteen configurations, apparatus set ranging 53 to 216 concepts — a 4x swing. Top-1 moves 0.9339 to 0.9333. Tactic blames: 20 in every single configuration. Verdicts: 245 in every configuration. The thresholds are not load-bearing because the concepts that do the work sit at ratios of 100-2400x. A tuned point that produces identical output across a 4x perturbation of its own output set is not tuned in any sense that threatens longevity.

*[Defense note added post-trial: this claim was subsequently RETRACTED by the
defense itself. See EVIDENCE.md item E7 — the invariance is sample-specific,
and on the certified seed one residual is decided by the 200 floor.]*

Your refactor simulation I accept, and read the opposite way: at K=500 statements about an internal type, zero survive as apparatus — correctly, because a type the community has written 500 theorems about has become mathematics and should stop being demoted. The measure retiring a concept once people talk about it is the design working.

**8. ON OCCAM, WE AGREE ON THE FACTS AND DIFFER ON THE INFERENCE.** My own ablation (dev seed, committed): stripped baselines 0.73-0.77, full system 0.9344. Logic-only demotion +10.8, position +4.8, claims +3.1, depth +2.9, attribution +2.3, statement-world +0.6, zoom +0.6, apparatus +0.4. Yours on the certified seed agrees directionally. So the complexity is not decorative — the gap over the simplest defensible rule is 16-20 points, and five of eight components each buy multiple points. But your trajectory argument is correct and I will not fight it: +2.56 then +0.42 is diminishing return, and the right conclusion is that V8 is the LAST component worth adding under this primitive. There should be no V9 of this kind. I also concede zoom's cost, which nobody had measured until today: it buys +0.56 top-1 while raising tactic junk from 12 to 20.

**9. ON QUESTION TWO I DO NOT CONTEST YOU.** You quoted my own HONEST_ASSESSMENT: declaration ranking hits a structural ceiling; local hypotheses, witnesses, case structure and representation changes cannot be expressed by any list of cited declarations. That is true, it is documented, and it means a ranked list per proof is a necessary substrate for the map and not sufficient for it. The map needs typed edges and cross-proof identity, and this architecture produces neither. Where we differ: a substrate that is wrong 5% of the time at rank 1 is still the thing the edge layer must be built on, and none of the nine rounds is wasted for that purpose. But I will not claim this architecture reaches the map.

**10. ON KEYNESS.** Conceded: the ranked view is 37.7% exact / 71.0% near; zoom is 56.5 / 92.8; both measured on V5v, two versions old. Zoom is a shipped step, so quoting it for the display is legitimate; quoting it as the ranking's semantic score is not, and my opening did that.

**DEFENSE POSITION:** question one, yes, conditional on the four fixes above and on stopping the accretion. Question two, no — not sufficient, by my own documentation.


---


<!-- ==================== briefs/4_PROSECUTION_REBUTTAL.md ==================== -->
# Brief 4 — Prosecution Rebuttal

*The prosecution had the last word, following from the owner's instruction
that the defense open. Reproduced verbatim.*

---

I withdraw one charge outright. The defense is right on point 6 and I was wrong. I asserted that grind's `Poly` "causes 23% of the failures the measure exists to prevent," citing three residuals. All three carry `root_in_tactic_ns: True` in `round9.log`. They are theorems inside a tactic's own development, the goal-relevance clause spares them by design, and they are not failures. That charge is dead and I will not recycle it.

But checking it surfaced something worse in the same list. ACCOUNTING_STATUS.md line 14 characterises the entire residual as "logic-shaped bridge lemmas (`Lean.Grind.forall_forall_or`, `Lean.Omega.Int.lt_of_not_le`) whose statements contain no apparatus vocabulary because they restate pure logic — the measure cannot see them and arguably should not." That taxonomy is false for at least two of the eight genuine residuals. `AlgebraicTopology.DoldKan.Q_succ` gets rank-1 `Mathlib.Tactic.Abel.subst_into_negg`. `WeierstrassCurve.exists_variableChange_isCharThreeNF` gets `Mathlib.Tactic.FieldSimp.NF.pow_eq_eval`. Neither is logic-shaped. Both are a tactic's normal-form vocabulary, on real mathematics, which is exactly the population the apparatus measure exists to catch and exactly the case where "the measure arguably should not see them" does not apply. The residual is not fully accounted for; it is partly misfiled.

On point 7, the defense has proved a stronger claim than it intended. Fifteen configurations, apparatus set 53 to 216 concepts, and: top-1 0.9339 to 0.9333; tactic blames 20 in every configuration; verdicts 245 in every configuration. Identical integers across a 4× swing in the set is not robustness — it is inertness. You cannot hold both "the thresholds are not load-bearing because output is invariant" and "the apparatus measure halved automation junk." If the most conservative setting (λ=50, floor=500, 53 concepts) produces byte-identical blame counts, then ship that one and delete the other 49 concepts, or concede the component is doing almost nothing. Your own ablation already prices it at +0.4. And `apparatus_sensitivity.py:73` reads `HOLDOUT_SEED = 20260819  # DEV`. The invariance was never checked on the certified seed.

The refactor reversal does not work, and the reason is in the code, not the principle. Your reading — "a type the community has written 500 theorems about has become mathematics" — requires `inherited[k]` to count attention paid to `k`. It does not. Lines 171–189 propagate a **max** downward: `inherited[k] = max(nstmt[p])` over every concept `p` whose definition transitively contains `k`. So the trigger is not 500 theorems about `Constraint`. It is *one* wrapper definition containing `Constraint` that someone states 500 theorems about — and it retires `Constraint` **and every concept beneath it simultaneously**, in one commit, with no intermediate state. A sum would degrade smoothly and would mean what you say it means. A max is a step function over a subtree. That is the longevity defect, and it is untouched by the sensitivity sweep, which perturbs the thresholds and never perturbs the graph.

On point 8, the largest number in your ablation is a denominator, not a ranking. "Logic-only demotion +10.8" cannot be reconciled with round 3's own pre-registered result: "**Falsified**: 83.24 → 83.33 (+0.09; bar was 88)." The difference is that removing the rule from the ablation also removes the verdict semantics, returning ~280 hard all-bookkeeping proofs to the denominator. That is the identical artifact round 4 diagnosed and round 5 monetised. My ablation controls for it — DEMONLY 0.8943 vs V8 0.9480 on the same 1,826 — which is why my ordering puts depth first and yours puts demotion first. Yours is also on the burned dev seed.

On the rebuilt recall harness: the methodological fix is real and the honest number, 0.317 mean, is the most valuable thing produced in this trial. But the taxonomy now carries the entire argument, and it is your own hand-classification of your own losses, n=39, on `HOLDOUT_SEED = 20260820` — a seed PHASE4_CERTIFICATION.md declares burned ("round 1 became development data too") — drawn from the same `~has_class` pool that excludes 46% of theorems. Four thousand five hundred twenty-two declarations are sitting there. Run it on all of them, with a classification protocol fixed in advance.

And one bucket is misfiled. Eight losses are dismissed as "constructors (`And.intro`, `Exists.intro`) assembling a pair." `Exists.intro` is not assembly; it is *exhibiting the witness* — one of the four move classes your own HONEST_ASSESSMENT names as invisible to declaration ranking. Sorting witnesses into "not a move" by kernel kind is the claims filter marking its own homework a second time. Your irreducible cost is 3 of 146 only if that reading holds; on the reading your own report already committed to, it is 11.

We now agree on the diagnosis and on question two. Then the roadmap must change: ACCOUNTING_STATUS.md's four remaining goal posts — cross-version, keyness at scale, provenance merge, bridge lemmas — contain no item for typed edges or cross-proof identity. The document still points at more of this.


---


<!-- ==================== EVIDENCE.md ==================== -->
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


---


<!-- ==================== system/ACCOUNTING_STATUS.md ==================== -->

# CURRENT FAILURE LEDGER — ACCOUNTING_STATUS.md (verbatim, post-trial)

# ACCOUNTING STATUS — every flagged case, marked (2026-08-20)

Latest certified run: **round 9, seed 20260831, V8, run once**
(data/phase4_holdout9_results.json). 2,400 theorems -> 280 verdicts
("holds by definition"), 239 EMPTY (the filters left nothing at all -- a
FAILURE MODE, not a designed output; it is excluded from the precision
denominator, which flatters the headline and is disclosed here for the first
time), 55 too small, 1,826 scored. Rank-1 pass 94.80% on the standing proxy, 94.52% under a
stricter grader (two measured blind spots closed for evaluation only:
core-internal arithmetic namespaces, and the True-twin normalization
family). Same-sample V6 baseline: 94.38 / 93.18. Markers:

| at #1 | n | marker | cause | fix status |
|---|---|---|---|---|
| machine-generated, several claims inside | 43 | OK-mislabel (mostly; ledger-read) | multi-parent derivations; attribution cannot pick one | **display label IMPLEMENTED** (src/parent_labels.py): 77.1% of 239,625 machine-generated claims now resolve to what they are part of (attribution 108k / definition-user 43k / statement-subject 34k); the rest keep their raw name |
| grader-stamped glue | 42 | 2/3 OK-mislabel (interface facts, byContradiction), 1/3 OK-by-owner-ruling (thin lists) | grader stamps structure fields / logic ops | none needed (grader work ruled out) |
| automation internals | 13 | NOT OK, halved (1.1% -> 0.71%; 5 of the 13 are correct answers on theorems inside a tactic's own development, leaving ~0.44% true junk) | tactic certificates are genuine claims | **apparatus measure IMPLEMENTED and CERTIFIED** (round 9). Residual taxonomy CORRECTED after adversarial review — the earlier claim that all of it is "logic-shaped bridge lemmas the measure should not see" was FALSE. Diagnosed by ingredient: (a) `Mathlib.Tactic.Abel.subst_into_negg` on `DoldKan.Q_succ` — its only non-universal ingredient is `NegZeroClass.toNeg` (ratio 1.2), i.e. a tactic's substitution lemma stated in ordinary algebraic vocabulary, carrying no apparatus fingerprint at all: a STRUCTURAL blind spot no threshold fixes; (b) `Mathlib.Tactic.FieldSimp.NF.pow_eq_eval` on a Weierstrass-curve theorem — it does carry `FieldSimp.NF` ingredients at ratios 18.2 and 32.2, and is missed only because `NF.instPowNat` has 129 uses against the 200 floor: a THRESHOLD miss, catchable by lowering the floor; (c) genuine logic restatements (`Lean.Grind.forall_forall_or`, `Lean.Omega.Int.lt_of_not_le`) which are real shallow facts and a ranking question |
| Prop-typed instances | 1 | OK-mislabel (read: real facts) | grader | none needed |
| own compiled helpers | 1 | OK (zoom opens) | kept by design | implemented |

## The apparatus measure (this round's fix, certified)

A concept is **apparatus** when it is used far more than it is stated:
proofs citing it > 200, and > 20x the number of human theorem statements
that mention it (inherited down the definition graph). 102 concepts qualify,
every one of them a decision procedure's encoding vocabulary. An item is
**machinery for T** when one of its ingredients is apparatus and none of its
ingredients appear in T's own statement; machinery ranks below real moves,
and a list that is entirely machinery yields "discharged by automation".

It names nothing. The longevity argument is mechanical: a decision procedure
works by encoding goals into private vocabulary and proving denotation
lemmas about it, so that vocabulary is cited by thousands of proofs and
stated in almost no theorems. Any replacement for omega exhibits the same
signature the day it lands.

Cost, measured: 2 real moves lost in 1,826 proofs (bar was 5).

Threshold sensitivity, and its limit: on the dev sample, sweeping the ratio
10x-50x and the floor 50-500 (apparatus set 53 to 216 concepts) leaves top-1
within 0.06 points and the tactic-blame and verdict counts identical
(data/apparatus_sensitivity.json). That invariance is SAMPLE-SPECIFIC and was
over-read: on the certified seed, case (b) above is decided by the 200 floor.
The correct statement is that the thresholds are not load-bearing for the
concepts that carry the effect (ratios 100-2400x), while boundary concepts
near the floor do change individual outcomes. The sweep has not been run on
the certified seed.

## Falsifications this round (recorded, not hidden)

- **Round 8 (seed 20260830) FALSIFIED by its own bar.** Same design, but
  "bare proposition" was tested as "mentions no constants" — which a
  predicate over abstract types also satisfies. `Function.Injective` and
  `Nonempty` were misfiled, and real moves ("an equivalence is injective")
  collapsed into definitional verdicts: 31 losses against a ceiling of 5.
  Fixed by reading arity from the kernel telescope (dump v7, field `ar`);
  exactly five bare propositions exist in Mathlib. Round 9 re-ran corrected.
- **Capsule atomization falsified twice on dev data.** Closing a
  machine-generated block when any inner claim is machinery, and when the
  top-ranked inner claim is machinery, both hide real moves (6 cases). No
  capsule rule ships; zoom is unchanged.
- **Audience test falsified on dev data.** "Cited only by machine-generated
  proofs" measures whether a block got outlined, not whether it is
  automation (`ring` emits inline into human theorems; `byContradiction`
  blocks get outlined). Dropped.

Earlier falsified detector designs, still recorded: raw statement-exposure,
root-grain strategy signatures, Lean registries, co-mention islands,
weighted islands, author-written priority at file and declaration grain.

## The empty bucket (disclosed, not yet fixed)

239 of 2,400 sampled theorems (12.8% library-wide) produce NO output: after
the position and claims filters nothing survives, so there is no list to rank
and no verdict to issue. The scoring code drops them from the denominator
(`live = a[a > 0]`), so they cost the reported precision nothing. They were
previously reported together with verdicts, which was wrong: a verdict is a
statement about every candidate being demoted, and requires candidates. This
is the single largest unmeasured failure mode in the system.

## Verdicts (280; 80 sampled from the earlier round, audited THREE ways)

- v1 (source text): 39/39 resolvable verified correct (30 literal rfl).
- v2 (exact-module + provenance channel via `mathrecord modules`): 28
  confirmed; 2 flags read as statement-side artifacts (proofs := rfl).
- v3 (KERNEL CERTIFICATION, `mathrecord defcheck`): 58/80 POSITIVELY
  KERNEL-CERTIFIED definitionally equal. Union with v1: 64/80 certified by
  at least one hard channel; of the 16 remaining, 10 are machine-generated
  congruence/injectivity lemmas (correct by construction), 6 named
  individually with no evidence of error. ZERO false verdicts, any channel.

The new "discharged by automation" verdict is a separate output from "holds
by definition" precisely so this audit stays meaningful.

Below rank 1: 97% of visible glue sits below the real moves (OK by owner
ruling). Plumbing-boundary display cut: floated, NOT implemented, cosmetic.

Recall (CORRECTED 2026-08-20; the previous claim was an artifact):
the old harness applied the claims filter to its own answer key, so its
"zero filter losses" was arithmetically forced. Rebuilt with an unfiltered
answer key (src/recall_loss_split.py): mean recall 0.317 / median 0.25
against EVERY elaborator-resolved source identifier. Loss taxonomy over 146
losses: 51 statement vocabulary (the theorem's own nouns -- not moves), 60
background slots (same vocabulary in implicit positions), 24 erased by
compilation before any term exists, 8 constructors assembling pairs, and
THREE genuine "unfold this definition" moves the claims filter cannot
express. That last class is the architecture's real recall cost and matches
the documented Type-valued gap (ADR-0004 s3). n=39; the rate at scale is
unknown.

Implemented and certified: position filter; claims filter; attribution;
verdict semantics; logic-only demotion; statement-world priority; depth
ranking; zoom; provenance sidecar; exact-module resolver + verdict audit v2;
kernel verdict certifier; **apparatus measure; machine-generated display
labels**.

Floated, NOT implemented (all non-blocking): plumbing display cut;
cross-version run; larger/human keyness panel; merging the provenance
channel into the views (the path to ~100% end-to-end recall).

Remaining goal posts, in order: (1) residual ~0.44% logic-shaped bridge
lemmas — reclassified: a ranking question, not a machinery question;
(2) cross-version run; (3) keyness at scale; (4) provenance merge for
end-to-end recall.


---
