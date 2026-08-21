# Why the leading ranking fails — a first-principles trace

Development data (180 proofs, 2,419 graded candidates). Read the mechanism,
not the scoreboard. Everything here is a hypothesis-generator for the next
registered round; the rankings are frozen for the sealed round in flight.

---

## 1. What the leading score actually is

`R_phase5_composite` is written as a product of four factors:

```
score = m_role  x  m_stmt  x  m_depth  x  idf
```

- `m_role` — 1.0 applied, 0.7 let-value/explicit-arg, 0.5 everything else
- `m_stmt` — 1.0 if already in the theorem's statement, 1.5 if the proof introduced it
- `m_depth` — 0.20 + 0.80 x (cited depth / 346)
- `idf` — log(number of proofs / how often this declaration is cited), i.e. **rarity**

Measured over the 2,419 graded candidates:

| factor | min | max | range | share of log-score variance |
|---|---|---|---|---|
| m_role | 0.500 | 1.000 | 2.0x | 0.057 |
| m_stmt | 1.000 | 1.500 | 1.5x | 0.025 |
| m_depth | 0.200 | 0.917 | 4.6x | 0.077 |
| **idf** | 0.908 | 13.525 | **14.9x** | **0.479** |

**corr(log score, log idf) = 0.897.**

**The four-factor composite is a rarity score with decoration.** The other
three factors together move 16% of the variance.

Two of them are close to inert in practice:

- `m_stmt` fires on only 14.6% of candidates overall, and on **0%** of the
  candidates in the eight worst-scoring proofs — those are `_apply`-style
  lemmas where everything is already in the statement.
- `m_depth` is normalised by the library's maximum depth, 346, which is set by
  a single outlier. Real cited depths are mostly under 70, so the factor is
  compressed into roughly [0.20, 0.36] — a 1.8x spread, not the 4.6x the
  formula suggests.

---

## 2. Why it works: rarity really does track importance

| rater grade | mean idf | median idf |
|---|---|---|
| 4 CORE | 11.37 | 11.73 |
| 3 MAJOR | 9.24 | 9.29 |
| 2 LEGIT_GLUE | 5.93 | 5.68 |
| 1 BAD_GLUE | 4.28 | 3.80 |
| 0 JUNK | 3.94 | 3.42 |

Monotone across all five grades, with a wide spread. **This is the real
finding underneath the composite's win**, and it is a statement about
mathematics, not about our code: the moves that carry a proof's idea are
mostly cited rarely; the things cited constantly are plumbing.

That is why the composite beats lexicographic rankings. It is also the whole
of what it knows.

---

## 3. Why it fails: exactly where rarity and importance come apart

### Failure A — rare *because* it is machine-generated

Auto-generated declarations (the kernel's own `node_gen` flag, not a name
rule):

| | value |
|---|---|
| mean idf | **12.70** |
| mean idf of everything else | 5.23 |
| mean idf of CORE-graded items | 11.37 |
| share sitting in the top idf decile | **95%** (base rate 0.8%) |

**Compiler-generated helpers are rarer than the core mathematics.** They are
the single most rarity-extreme class in the corpus, and they carry no
mathematical content by construction — they exist because a proof was split
during compilation.

A rarity-driven score cannot help but promote them. Two traces:

`HomologicalComplex₂.flip_d_f` (target depth 27) —

| rank | grade | role | d_cite | in stmt | idf | score | name |
|---|---|---|---|---|---|---|---|
| 1 | BAD_GLUE | explicit-arg | 23 | yes | **11.92** | 2.112 | `HomologicalComplex₂.flip._proof_2` |
| 3 | **CORE** | explicit-arg | 26 | yes | 10.03 | 1.826 | `HomologicalComplex₂.flip` |

Same role, same statement status, *deeper* for the correct answer. The only
differing factor is rarity, and it inverts the ordering.

`CategoryTheory.Comma.isoMk_inv_left` (target depth 22) —

| rank | grade | idf | score | name |
|---|---|---|---|---|
| 1 | JUNK | **12.14** | 1.857 | `CategoryTheory.Comma.isoMk._auto_1` |
| 2 | **CORE** | 10.19 | 1.773 | `CategoryTheory.Comma.isoMk` |

Identical mechanism.

### Failure B — common *because* it is universal

The mirror image. Moves that appear everywhere get a near-zero idf, so they
sink — even when the rater says they are the content.

| | mean position in the list (1.0 = last) |
|---|---|
| **useful** items (grade ≥ 2) with idf < 4 | **0.63** |
| **defect** items (grade ≤ 1) with idf > 9 | **0.23** |

`Eq.refl` is graded LEGIT_GLUE in proof after proof and lands at position
14 of 19, 16 of 22, 12 of 15. For an `_apply` lemma whose proof is literally
`rfl`, reflexivity *is* the argument, and rarity guarantees we bury it.

### Failure C — generated instances inherit deep hosts

`CoalgEquiv.refl_apply`: `CoalgEquiv.instFunLike` reaches rank 2 with cited
depth 67 and idf 9.81. It is a generated instance for a deep structure, so it
inherits both a high depth *and* high rarity. Both surviving factors point the
wrong way at once.

### How often does this actually break a proof?

Only **8 of 180 proofs (4.4%)** have a defect ranked above *every* useful
item. The mechanism is real and pervasive in the ordering, but catastrophic
inversion is rare. That matters for how much to spend fixing it.

---

## 4. Recall

Precision has had all the attention; here is the other half. Composite, 180
proofs, pooled across all graded candidates.

**Of the CORE moves (grade 4):**

| top k | 1 | 2 | 3 | 4 | 6 |
|---|---|---|---|---|---|
| recall | 0.669 | 0.916 | 0.961 | 0.981 | **1.000** |

**Of major mathematics (grade ≥ 3):**

| top k | 1 | 2 | 4 | 8 | 12 |
|---|---|---|---|---|---|
| recall | 0.463 | 0.719 | 0.901 | 0.987 | 1.000 |

**Of everything useful (grade ≥ 2):**

| top k | 1 | 2 | 4 | 8 | 12 |
|---|---|---|---|---|---|
| recall | 0.214 | 0.393 | 0.610 | 0.852 | 0.934 |

**Recall is not the problem. Every core move is visible by k=6.** The useful
figure is lower only because legitimate glue is numerous — a proof may contain
six grade-2 items, and showing four of them is not a failure.

The price of recall, which is the actual design decision:

| show top k | % of all candidates | recall (useful) | recall (major) | precision |
|---|---|---|---|---|
| 1 | 7% | 0.214 | 0.463 | **0.956** |
| 2 | 15% | 0.393 | 0.719 | 0.878 |
| 4 | 29% | 0.610 | 0.901 | 0.693 |
| 8 | 54% | 0.852 | 0.987 | 0.521 |
| 12 | 75% | 0.934 | 1.000 | 0.417 |

**k=2 is the knee**: 72% of major mathematics at 88% precision, showing 15% of
the record.

Composite leads on recall as well as precision — major@4 is 0.901 against
0.847 (V8), 0.840 (introduced+depth), 0.815 (depth). It is not a
precision/recall trade; it dominates.

**The recall ceiling, set before any ranking runs:** the candidate universe
contains 81.2% of what authors actually wrote, and raters judge that in 3.3%
of proofs the real key move cannot be expressed as any citation at all.

**By depth, band 26–50 is worst again** (useful@4 = 0.474 against 0.748 at
0–10) — the fourth independent replication of that band being hardest.

---

## 5. Interpretability, simplicity, longevity

These are project values, and the current leader scores badly on two of three.

### Interpretability — the stated model is not the operative model

The score is presented as "role x statement x depth x rarity". It is
empirically ~90% rarity. Anyone told "we rank by mathematical depth" would be
misled about why a given item appeared. **A score whose name does not predict
its behaviour is not interpretable**, regardless of how well it performs.

The honest description of the current leader is: *rank by how rarely a
declaration is cited, with a mild depth tilt.*

### Simplicity — three factors are not earning their place

`m_stmt` moves 2.5% of variance and is inert on the hardest proofs. `m_role`
moves 5.7%. Together with `m_depth` they account for 16%.

**Two baselines that have never been run and should be:** rarity alone, and
rarity x depth. If rarity alone matches the four-factor score, the composite
should be replaced by it — not because it scores better, but because it says
what it does.

### Longevity — the most serious problem, and it cuts against the winner

`idf` is computed from **library-wide citation counts**. Those change every
time Mathlib changes: add a file, and every declaration's rarity shifts. Worse,
its most extreme values come from compiler-generated declarations, whose
existence and count depend on the *elaborator version*.

So the ranking that wins the new objective is also **the one whose score is
least stable across Lean and Mathlib versions** — in direct tension with the
standing requirement that this work survive an "omega replacement".

Depth, by contrast, is a kernel dependency-graph property: it changes only
when the mathematics beneath a declaration changes.

**This is a real conflict and it should not be resolved by whichever number is
larger.** The options are to measure rarity's version-stability directly
(re-run against an older Mathlib snapshot and measure rank churn), to replace
raw counts with a stabler proxy, or to accept a lower score for a stabler
signal.

---

## 6. Registered hypotheses for the NEXT round

Not applied now. The current round's rankings are frozen and nothing here may
tune them.

| id | hypothesis |
|---|---|
| H1 | Rarity alone (`idf`) matches the four-factor composite within the equivalence margin. If so, adopt it for interpretability. |
| H2 | Excluding kernel auto-generated declarations (`node_gen`, a structural flag, no name rule) from the candidate universe raises navigation AP and removes failure mode A entirely. |
| H3 | Re-normalising depth by a percentile rather than the library maximum (346, an outlier) restores the depth factor's intended influence. |
| H4 | A rarity score is materially less stable across Mathlib snapshots than a depth score; measured as rank churn between two versions. |
| H5 | Down-weighting by occurrence role — specifically instance-slot — fixes failure mode C without touching mode A. |

H2 and H4 are the two that matter. H2 is cheap and principled; H4 decides
whether the current leader is admissible at all under the longevity
requirement.
