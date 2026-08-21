# The Evaluation Suite — rankings, inclusions, baselines, controls

2026-08-20. Two knobs held separate throughout: **ranking** (the per-proof
order over the complete record — ours to get right) and **inclusion** (how
much of that order a viewer admits — suggested by us, chosen by the user).

Ground truth: elaborator-resolved human-written citations, never filtered by
any candidate's own predicate. 4,249 evaluable proofs.

---

## 1. Rankings, with the baselines that make them interpretable

| ranking | P@1 | MRR | R@4 | glue@1 |
|---|---|---|---|---|
| B0 random (floor) | 24.3% | 0.387 | 19.2% | 34.6% |
| B1 reverse (anti-ranking) | 12.8% | 0.256 | 13.0% | 62.8% |
| B2 popularity | 12.1% | 0.244 | 12.4% | 37.3% |
| R3 pure depth | 57.0% | 0.636 | 32.2% | 6.7% |
| **R4 proof-introduced + depth** | **60.3%** | **0.663** | **34.6%** | 7.1% |
| R5 V8-faithful | 58.7% | 0.652 | 34.3% | 11.1% |
| R6 V8 + all kinds | 59.1% | 0.655 | 34.2% | 2.6% |
| **B9 ORACLE (ceiling)** | **75.9%** | 0.759 | 37.5% | 8.4% |

**R4 reaches 79% of the achievable ceiling** and captures 70% of the distance
between random and oracle. It is also the simplest of the real candidates:
two signals, no demotion machinery, no claims filter.

**Popularity is catastrophic — 12.1%, below random and barely above the
anti-ranking.** How often a declaration is cited library-wide is essentially
anti-correlated with whether it is the key move of any particular proof. This
retires "importance = citation count" permanently, and it independently
explains the earlier finding that centrality inverts between projections.

---

## 2. The precision worry, with a correction to our own framing

Comparing rank-1 glue against the *average* rate at which humans cite glue is
the wrong test: humans cite plenty of glue, but glue is not their key move.
The right baseline is the **oracle's** rank-1 glue — what you get when you
rank the human's own citations first.

Glue at rank 1, by depth of the theorem proved:

| ranking | 0–10 | 10–25 | 25–50 | 50–75 | 75–125 | 125+ |
|---|---|---|---|---|---|---|
| **ORACLE** | **32.0%** | 12.7% | 12.5% | 2.0% | 2.5% | 0.9% |
| R4 introduced+depth | 29.1% | 10.6% | 10.6% | 1.3% | 1.2% | 0.8% |
| R5 V8-faithful | 28.0% | 19.8% | 15.1% | 4.1% | 4.3% | 2.0% |
| R6 V8 + all kinds | **12.7%** | 3.0% | 4.0% | 0.7% | 0.8% | 0.2% |
| B0 random | 33.9% | 36.4% | 33.5% | 31.5% | 33.6% | 36.1% |

**R4 tracks the oracle at every depth.** V8's demotion machinery (R6)
over-suppresses: 12.7% glue at shallow depth where the oracle says 32%.

That is exactly the failure the owner's hypothesis predicted. Near the
foundations, logic-only machinery genuinely *is* the mathematical content, and
V8's global demotion removes it. A ranking that carries no glue-demotion rule
at all is better calibrated than one that does.

---

## 3. The recall worry — and where the hole actually is

Share of human-written citations missed at top-4:

| ranking | 0–10 | 25–50 | 50–75 | 125+ |
|---|---|---|---|---|
| ORACLE | 64.6% | 66.1% | 50.7% | 61.1% |
| R4 | 67.6% | 69.8% | 53.0% | 62.8% |

R4 sits within ~3 points of the ceiling everywhere. **The loss is not the
ranking. It is the record.**

### The record's coverage is kind-specific, and the role filter is the cause

| kind of human-written citation | written | in record (any position) | load-bearing | coverage |
|---|---|---|---|---|
| theorem | 8,717 | 7,033 | 7,031 | **80.7%** |
| definition/construction | 15,736 | 12,930 | 7,470 | **47.5%** |
| constructor/recursor | 1,282 | 955 | 941 | 73.4% |
| **overall** | 25,735 | 20,918 | 15,442 | 60.0% |

Two things fall out.

1. **Humans write nearly twice as many definition citations as theorem
   citations** (15,736 vs 8,717), and we capture barely half of them.
2. **For theorems the role filter costs nothing** — 7,033 in the record,
   7,031 load-bearing. **For definitions it costs 5,460 citations**, 42% of
   those present. Definitions appear in type positions, implicit arguments and
   instance slots, because that is *where a definition gets used*. The
   load-bearing filter was designed around how theorems appear and it
   systematically discards how definitions appear.

**This is the single most actionable result in the suite.** The recall hole is
not diffuse; it is one filter interacting badly with one declaration kind, and
5,460 recoverable citations are sitting in the record already.

---

## 4. Inclusion techniques (ranking fixed at R4)

| inclusion | human citations kept | recall |
|---|---|---|
| top-1 | 2,563 | 14.9% |
| top-2 | 3,925 | 22.8% |
| top-4 | 5,256 | 30.6% |
| top-8 | 6,188 | 36.0% |
| top-10% per proof | 3,886 | 22.6% |
| top-25% per proof | 5,352 | 31.1% |
| top-50% per proof | 6,186 | 36.0% |
| theorems only | 5,619 | 32.7% |
| definitions only | 851 | 4.9% |
| non-glue only | 6,206 | 36.1% |

Fixed top-k and per-proof percentile track each other closely (top-4 ≈
top-25%, top-8 ≈ top-50%), so the choice between them is ergonomic rather than
substantive. The "definitions only" row is the coverage gap above, seen from
the inclusion side.

---

## 5. The island/technique hypothesis — REFUTED by controls

The claim under test was mine: that sparse top-1 components group proofs by
technique rather than subject. It was based on reading eight declaration
names, and the owner was right to demand controls.

| | module purity |
|---|---|
| **real components** | **0.621** |
| shuffled-ranking control | 0.477 |
| size-matched random nodes | 0.117 |
| size+depth-matched random nodes | 0.126 |

**Real components are 5.3x more subject-coherent than size-matched random.**
They are a subject atlas. The claim is withdrawn.

Two refinements worth keeping:

- Lift over the **shuffled-ranking** control is only **1.30x**. Most subject
  coherence comes from the hypergraph itself — proofs cite things near them in
  subject — and only about 30% is contributed by the ranking. Any ranking
  would look fairly coherent here.
- The sinks are **not techniques**. 18,249 of them, median depth 4, and the
  most-used are `OfNat.ofNat`, `Eq`, `Eq.refl`, `id`, `DFunLike.coe`,
  `propext`, `HAdd.hAdd` — primitive vocabulary, not `Classical.choice` or
  quotient formation. Both halves of my claim fail.

---

## 6. What the suite establishes

1. **R4 (proof-introduced, then depth) is the leading ranking**: best P@1 and
   MRR, best glue calibration against the oracle at every depth, and the
   simplest real candidate. It satisfies the Occam requirement better than V8.
2. **V8's demotion machinery is a net negative at shallow depth** and buys
   nothing measurable at any depth.
3. **Popularity-based importance is dead.**
4. **The recall problem is a role-filter/definition interaction**, not a
   ranking problem, and 5,460 human-written citations are recoverable now.
5. **Components are subject-coherent**, mostly because of the hypergraph
   rather than the ranking.

## What has NOT been done

R4 has not faced a keyness panel — the semantic instrument V8's lineage was
tested with. P@1 against elaborator-resolved citations is a good proxy but it
is not a mathematician saying "this is the key step". Before R4 replaces V8 as
the standing ranking it needs that test, and the head-to-head must be
pre-registered.
