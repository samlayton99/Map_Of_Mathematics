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
