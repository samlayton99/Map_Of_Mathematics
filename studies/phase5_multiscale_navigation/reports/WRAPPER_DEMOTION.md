# Wrapper demotion: can auto-generated junk be separated from auto-generated content?

Scope: one question — a sharp, append-safe, name-free condition that demotes artificial
wrapper/scaffolding citations without demoting real mathematics.
Data: 7531 graded incidences (TEST-R 4800, TEST-C 1769, CAL 962), three raters, median grade.
Of these, **88 are auto-generated** (`node_gen`): 48 junk (grade <=1), 14 LEGIT_GLUE, 26 MAJOR/CORE.

## Headline

The generated class is **not** a defect class. It is a *ranking* problem, not a *content* problem.

| population | n | useful rate (>=2) | MAJOR+ rate (>=3) |
|---|---|---|---|
| TEST-R all | 4800 | 0.316 | 0.142 |
| TEST-R auto-generated | 32 | **0.688** | **0.469** |
| TEST-C all | 1769 | 0.366 | 0.181 |
| TEST-C auto-generated | 50 | 0.320 | 0.180 |
| TEST-C stratum S1_generated, all candidates | 363 | 0.336 | 0.174 |
| TEST-C stratum S1_generated, the generated ones | 30 | **0.433** | **0.300** |

Representatively, an auto-generated candidate is **twice as likely to be useful** as an average
candidate. Even inside the defect-enriched generated stratum it beats its own stratum average.
The reason the class dominates rank-1 defects (18 of 20 rank-1 defects on `R_phase5_composite`
over TEST-C carry rater cause `A generated-obligation`) is that the *score over-ranks the whole
class*, not that the class is bad. Any blanket move against it pays for the top-of-list wins
with the CORE items it buries.

Also worth recording: rater cause `B wrapper/forwarder` was assigned **2 times** in the entire
challenge set, against `C irrelevant-instance` 2187 and `A generated-obligation` 99. The
"artificial wrapper" framing names a defect the raters essentially never saw. What they saw is
generated *proof obligations* ranked too high, and irrelevant *instances* filling the tail.

## Conditions tested

All predicates below are conjoined with `node_gen`. Every input is a declaration's own
kernel/body property — append-safe, no library-wide counts, no name strings.
Fields: `claim = decl_is_claim` (Prop-valued, not ctor/rec); `lbkids` = number of load-bearing
citations in the declaration's own body; `ifdepth` = max depth over the body citations that lie
in the declaration's *own statement* closure (its interface depth); `sub` = number of body
citations that are substantive claims; `cone` = distinct declarations in its own body.

Counts are over the 88 graded generated items.

| # | condition | flagged | junk caught | LEGIT_GLUE hit | MAJOR/CORE hit |
|---|---|---|---|---|---|
| W0 | `gen` (blanket) | 88 | 48/48 | 14 | **26** |
| W1 | `gen & ~claim` — generated non-proposition (elaboration value, ctor index, `_auto`) | 4 | 4 | 0 | 0 |
| W2 | `gen & ifdepth <= 0` — body cites nothing its own statement reaches | 8 | 8 | 0 | 0 |
| W3 | `gen & lbkids <= 1` — pure forwarder: at most one load-bearing child | 4 | 4 | 0 | 0 |
| **W4** | **W1 or W2 or W3** | **11** | **11/48** | **0** | **0** |
| W5 | `gen & sub == 0` — no substantive claim in its body | 24 | 15 | 9 | 0 |
| W6 | `gen & cone <= 4` — tiny own cone | 15 | 10 | 5 | 0 |
| DI-a | `gen & (depth - ifdepth) >= 57` — absolute depth inflation | 5 | 5 | 0 | 0 |
| DI-r | `gen & ifdepth < 0.5 * depth` — relative depth inflation | 38 | 26 | 5 | **7** |
| DI-r | `gen & ifdepth < 0.25 * depth` | 24 | 16 | 4 | **4** |
| DI-r | `gen & ifdepth < 0.10 * depth` | 14 | 12 | 1 | **1** |
| S1 | `gen & subsumed by another candidate in the same proof` | 1 | 1 | 0 | 0 |
| S2 | `gen & its unique substantive child is itself a candidate` | 0 | - | - | - |

Split-wise, W4 holds: TEST-C 5 flagged / 5 junk; TEST-R+CAL 6 flagged / 6 junk. 100% precision
on both sides of the fit/held-out line.

DI-a (`depth - ifdepth >= 57`) is **rejected as overfit** despite 100% precision: a CORE item sits
at gap 56 and the highest junk gap is 64. There is no plateau — the threshold is one item wide.
The relative form of the same idea, which does have a plateau, buries CORE items at every setting.

Proof-relative subsumption (S1/S2) fires almost never: generated declarations very rarely have
their parent or their whole child set sitting in the same candidate list.

## The residual class does not separate

Strip W4 off and 77 generated items remain: 37 junk, 14 LEGIT_GLUE, 26 MAJOR/CORE. Exhaustive
single-threshold search over 18 structural features (arity, depth, cited depth, delta depth, own
cone, load-bearing children, substantive children, theorem children, max child depth, interface
depth, children present in the proof, candidate-list size, target depth, in-statement, logic-only,
subsumption) finds **no rule catching more than 6 of 37 junk without hitting a MAJOR/CORE item**,
and every such rule is an extreme tail fit to 1-4 points.

The reason is visible by inspection. These are the `_simp` / `_proof` / `.eq_n` family, and the
CORE and the JUNK members are structurally identical:

```
CORE  (4,4,4)  ENNReal.coe_le_coe._simp_1     ar=2 depth=105 cone=10 lbkids=3 sub=1 ifdepth=104
JUNK  (1,1,1)  ...nndist_eq_zero._simp_1      ar=2 depth= 98 cone= 6 lbkids=3 sub=1 ifdepth= 95
```

Same generator, same shape, same arity, same cone, adjacent depth. Whether the item is the proof's
key move or noise depends on what the *parent lemma says* relative to the target — mathematical
content the kernel record does not carry. No structural condition can decide it, and pretending
otherwise means fitting the 88 points we have.

## Effect on the ranking

Demotion implemented as a leading lexicographic key (flagged items rank last within their proof;
nothing is deleted). Paired per-proof bootstrap, 2000x, seed 20260901.

| ranking | rule | split | dNavAP | 95% CI | proofs better / worse |
|---|---|---|---|---|---|
| R_phase5_composite | W4 | TEST-R | +0.0008 | [+0.0000, +0.0021] | 4 / 0 |
| R_phase5_composite | W4 | TEST-C | +0.0050 | [+0.0008, +0.0110] | 4 / 0 |
| R_phase5_composite | W0 blanket | TEST-R | **-0.0107** | [-0.0180, -0.0036] | 9 / 20 |
| R_phase5_composite | W0 blanket | TEST-C | +0.0322 | [+0.0119, +0.0534] | 24 / 8 |
| R_introduced_depth | W4 | TEST-R | +0.0009 | [+0.0000, +0.0021] | 4 / 0 |
| R_introduced_depth | W4 | TEST-C | +0.0018 | [+0.0001, +0.0048] | 4 / 0 |
| R_introduced_depth | W0 blanket | TEST-R | **-0.0129** | [-0.0217, -0.0059] | 9 / 20 |
| R_v8_faithful | W4 | TEST-R | +0.0003 | [+0.0000, +0.0007] | 4 / 0 |
| R_v8_faithful | W4 | TEST-C | +0.0018 | [+0.0002, +0.0048] | 4 / 0 |
| R_v8_faithful | W0 blanket | TEST-R | **-0.0139** | [-0.0226, -0.0065] | 9 / 20 |

W4 changes 4 proofs per split and every one of them improves. It is monotone: no proof on any
split under any ranking gets worse. TEST-C rank-1 defect rate 0.1667 -> 0.1500 on the composite
(2 of 20 rank-1 defects fixed). TEST-R rank-1 defect rate unchanged or better.

The blanket rule reproduces the known regression exactly: it wins on the defect-enriched set and
loses on the representative one, 20 proofs damaged against 9 helped.

Also tested and rejected: replacing a generated declaration's cited depth by its *interface* depth
(a re-scoring rather than a demotion). Same trade as the blanket rule in miniature — TEST-C
defect@1 0.200 -> 0.142 on `R_introduced_depth`, but TEST-R NavAP 0.8061 -> 0.8050 and defect@1
0.0444 -> 0.0472. Applying interface depth to *all* declarations is clearly worse (TEST-R NavAP
0.8061 -> 0.7646).

## Recommendation

**Adopt W4. Do not expect it to solve the stated problem.**

```python
# append-safe, name-free, own-body properties only; demote, never delete
W4 = c.node_gen & (~decl_is_claim              # generated non-proposition
                   | (ifdepth <= 0)            # body touches nothing its own statement reaches
                   | (lbkids <= 1))            # pure forwarder
# ifdepth[d] = max node_depth over d's own body citations with inc_in_stmt_world
# lbkids[d]  = count of d's own body citations with inc_load_bearing
# used as a leading lexicographic key, value 1 sorts last within the proof
```

It is three clauses, each with a mechanism, each independently clean, and it is free: 11 of 48
graded generated defects caught, zero LEGIT_GLUE and zero MAJOR/CORE items demoted, 4 proofs
improved and 0 damaged per split across three rankings. It is worth taking because it never costs
anything, not because it moves the number.

**The honest answer to "filter out artificial wrapper citations" is that the premise is wrong.**
The wrapper class the lead has in mind (`B`, 2 rater assignments) barely exists. The class that
actually sits at rank 1 is generated proof obligations (`A`), and that class is *above average in
usefulness* — 0.688 useful on the representative set. 37 of its 48 graded defects are structurally
indistinguishable from its 26 CORE/MAJOR members. There is no sharp condition left to find in the
kernel record; anything further requires content the record does not carry, or a rule fit to the
88 labelled points we have.

If defect@1 on generated-heavy proofs is still the goal, the remaining levers are (a) accept the
class-level trade and demote generated candidates only when the proof has a non-generated
alternative — this is the blanket rule with a guard and still costs MAJOR/CORE on TEST-R, or
(b) fix the score that over-ranks them rather than adding a demotion on top. Neither is a wrapper
filter.

## How to test in a fresh round

1. Register W4 as a leading key on the incumbent ranking. Nothing else changes, so append-safety
   and the no-name-strings constraint need no new argument — every input is a property of the
   cited declaration's own body and statement.
2. Pre-register the direction: W4 is claimed **non-inferior on TEST-R** and **>= 0 on TEST-C**.
   The claim to falsify is monotonicity: *no proof gets worse*. One damaged proof on fresh labels
   kills it. Do not pre-register an AP improvement — the effect is +0.001 and will not clear noise.
3. Draw fresh proofs, seeds past 20260831 (earlier seeds are burned). Sample the generated stratum
   at its representative rate, **not** enriched — the enrichment is what made the blanket rule look
   good and is the trap this whole question walked into.
4. Grade with the standing 0-4 scheme and require causes on 0/1 items. The specific quantity to
   watch is the useful rate of `node_gen` candidates: this study says 0.688 representatively. If a
   fresh round reproduces anything above the overall base rate, the "generated = wrapper" hypothesis
   is dead and should not be revisited.
5. Report W4 flag counts on the new sample. Expect ~11 flags per 88 generated items and precision
   1.00; a single MAJOR/CORE flag on fresh data means retire the rule rather than retune it.
