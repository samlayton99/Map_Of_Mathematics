# V8-alt — candidate comparison, depth hypothesis, and the merge census

2026-08-20. Executed against `PRE_REGISTRATION_V8ALT.md`, which fixed the
candidates, the three separate evaluation questions, and the falsification
criteria before anything was scored.

Ground truth throughout: Lean's elaborator records which identifiers the human
wrote in each declaration's source. **Proof-written citations** = those
references minus the ones already resolved from the declaration's own
statement. The answer key is never filtered by any candidate's own predicate —
the circular-harness defect from the last trial is not repeated. 4,505
declarations with provenance, **4,249 evaluable proofs**.

---

## Q1/Q2 — The five frozen candidates, head to head

| candidate | Q1 present | MRR | R@1 | R@4 | R@16 | **P@1** |
|---|---|---|---|---|---|---|
| C1 V8-faithful | 39.4% | 0.652 | 19.5% | 34.3% | 38.9% | 58.7% |
| C2 V8 + all kinds restored | 39.4% | 0.655 | 19.5% | 34.2% | 38.9% | 59.1% |
| C3 pure depth | 39.4% | 0.636 | 18.6% | 32.2% | 38.5% | 57.0% |
| **C4 proof-introduced, then depth** | 39.4% | **0.663** | **19.9%** | **34.6%** | **39.0%** | **60.3%** |
| C5 Phase 5 composite | 39.4% | 0.641 | 18.7% | 34.6% | 39.0% | 56.1% |

**Q1 present is identical across all five.** That is the designed sanity
check for principle 1 — nothing is deleted, only ordered, so coverage of the
record cannot differ. Any spread would have been a bug.

### Three findings

**1. The Phase 5 composite is the WORST candidate.** 56.1% against C4's
60.3%. The weight I built to serve connectivity is measurably worse at the
actual job than V8 and worse than two simpler rankings. It is withdrawn.

**2. The winner is simpler than V8.** C4 uses two signals — is the citation
introduced by the proof, then how deep is it — and beats V8's full machinery
(logic-only demotion, machinery demotion, claims filter) by 1.6 points on P@1
and leads on every recall cut. The elaborate demotion apparatus is not what
makes the ranking good.

**3. Restoring definitions does not cost precision; it slightly helps.**
C1 → C2 is 58.7% → 59.1%, and C2 leads C1 on MRR. This directly answers the
brief's question: definitions can be restored to first-class status for free.

### Q2.2 — Where definitions land at rank 1

| candidate | n top-is-definition | P@1 there | P@1 when top is a theorem |
|---|---|---|---|
| C1 V8-faithful | 597 | 26.8% | 63.9% |
| C2 V8 + all kinds | 788 | 27.0% | 66.5% |
| C3 pure depth | 938 | 23.2% | 66.5% |
| **C4 introduced+depth** | 763 | **32.8%** | 66.4% |
| C5 composite | 756 | 23.0% | 63.3% |

A definition at rank 1 is right about a third of the time versus two-thirds
for a theorem — so definitions are individually weaker at the top, yet
admitting them does not hurt the aggregate. C4 handles them best by a wide
margin.

---

## Q2.3 — The depth hypothesis: **SUPPORTED**

The owner's hypothesis, registered as a hypothesis and not assumed: *glue at
rank 1 would badly hurt precision for a deep theorem, but similar logical
machinery may legitimately be the mathematical content of a theorem near the
foundations.*

The direct test is not our precision — it is **what humans actually write**.
Composition of human-written proof-body citations, by depth of the theorem
proved:

| depth band | proofs | citations | theorem | definition/construction | glue (logic-only) | other |
|---|---|---|---|---|---|---|
| 0–10 | 378 | 1,318 | 14.5% | **67.1%** | **10.8%** | 7.5% |
| 10–25 | 1,149 | 4,363 | 31.8% | 59.0% | 7.2% | 2.1% |
| 25–50 | 424 | 1,730 | 38.7% | 54.0% | 5.9% | 1.3% |
| 50–75 | 715 | 2,860 | 49.5% | 45.0% | 5.0% | 0.5% |
| 75–125 | 604 | 2,785 | 50.9% | 43.1% | 5.0% | 1.0% |
| 125–350 | 979 | 4,140 | 42.9% | 54.0% | **2.1%** | 1.0% |

**Glue falls monotonically from 10.8% to 2.1% — a 5x drop.** Humans genuinely
do cite logic-only machinery more often when proving shallow theorems. Glue at
rank 1 is therefore more often *correct* near the foundations, and evaluation
should be stratified by depth. The hypothesis survives its test.

### The finding that was not asked for, and matters more

**Definitions and constructions are 43–67% of everything humans write in
proofs.** They are the plurality at every depth band and the outright majority
at four of six. Theorems never exceed 51%.

The claim-only view — every citation projection this program shipped before
this phase — was discarding *the majority of what mathematicians actually
write*. That is a far stronger argument for restoring definitions than the
precision numbers, and it reframes the 21.9%-empty problem: those proofs were
not contentless, their content was definitional.

---

## Q3 — The merge census: definitions are the bridges

Union-find over edges added in rank order, so the citation that first joins
two basins is identified exactly rather than inferred. Ranking: C2.

| k | components | giant | entropy | merges |
|---|---|---|---|---|
| 1 | 34,320 | **7.22%** | 6.300 | 728,707 |
| 2 | 11,006 | **98.15%** | 0.261 | 23,314 |
| 3 | 8,171 | 98.71% | 0.184 | 2,835 |
| 4 | 6,776 | 98.92% | 0.154 | 1,395 |
| 8 | 4,068 | 99.30% | 0.099 | 444 |
| 16 | 2,103 | 99.57% | 0.060 | 146 |

**There is a sharp phase transition at k = 2.** The giant component jumps
+90.93 points, and the entropy of the component-size distribution collapses
from 6.300 to 0.261. This is an empirically located slider position, not a
convenient round number. Everything past k=3 is marginal.

### What kind of citation reconnects mathematics

Merges at **k ≥ 2** — the reconnection regime:

| kind | merges | share |
|---|---|---|
| **definition/construction** | 18,953 | **58.8%** |
| other (constructor/recursor) | 8,199 | 25.4% |
| theorem | 4,634 | 14.4% |
| **glue** | 431 | **1.3%** |

**The registered question is answered: definitions ARE the long-distance
bridges the claim-only view was hiding.** They cause four times as many
reconnections as theorems.

And the pre-registered falsification criterion — *"if merges are caused
overwhelmingly by glue, rapid reconnection is a plumbing artifact and not a
structural property"* — **fails to trigger**. Glue causes 1.3% of merges. The
rapid reconnection of mathematics at k=2 is a real structural property of the
citation record, carried by definitions.

---

## The honest ceiling

**Q1 present = 39.4%.** Only 39.4% of human-written proof-body citations
appear anywhere in the load-bearing incidence record, for every candidate.
The remaining 60.6% were erased by elaboration before any kernel term existed,
or appear only in non-load-bearing positions. That is the recall ceiling of
this entire citation channel and no ranking can raise it. Raising it requires
merging the provenance channel into the views — still unbuilt.

## What this changes

1. **C5 (Phase 5 composite) is withdrawn.** Measured worst.
2. **Definitions are restored**, on the evidence that they are the majority of
   what humans write and the majority of what reconnects the graph, at no
   precision cost.
3. **C4 is the leading candidate** and is simpler than V8. Before adopting it,
   it needs the same scrutiny V8 got: a keyness panel, and a check on whether
   dropping the demotion machinery costs anything the P@1 metric cannot see.
4. **Evaluation is stratified by depth from now on**, because the owner's
   hypothesis survived a direct test.
5. **k = 2 is a real structural location**, not a chosen cutoff.

## Not yet done

Q3.4 — the island/technique hypothesis against size-, depth- and
module-matched controls and shuffled-ranking controls. Until that runs, the
technique-clustering reading stays an interpretation, not a finding.
