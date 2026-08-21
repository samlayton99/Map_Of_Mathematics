# MathMap Status Report — the evaluation apparatus and what it found

2026-08-20. Written after building `mathmap_eval`, the API for testing ranking
techniques and inclusion policies. Everything below is measured on the whole
of Mathlib (771,129 declarations, 18,721,317 citation incidences) unless
marked otherwise.

---

## 1. What was built

An apparatus that keeps three layers strictly apart, because conflating them
is how this program went wrong before.

| layer | decides | whose job |
|---|---|---|
| corpus | what relationships exist | the extractor's |
| **ranking** | in what ORDER they appear | **ours to get right** |
| **inclusion** | how much of that order a view admits | **the user's** |

Adding either knob is a decorator; it then appears in every table, with
baselines and self-tests attached automatically.

```python
@ranking("R_mine", features=2)
def _mine(c, base):
    return (c.inc_in_stmt_world[base].astype("int8"),
            -c.inc_d_cite[base].astype(float))
```

```bash
python -m mathmap_eval list | compare | coverage | bridges | nested
python -m mathmap_eval.tests
```

A ten-ranking comparison runs in about 40 seconds.

### Naming discipline, enforced by test

| prefix | meaning |
|---|---|
| `Source*` | agreement with what the human wrote. **Not keyness.** Cannot promote a ranking alone. |
| `Role*` | descriptive composition at a rank. A statistic, not a judgement. |
| `Coverage*` | fraction of ground truth present in a universe. A property of candidate generation. |
| `Graph*` | components, giant fraction, entropy, susceptibility, enrichment. |
| `Semantic*` | **reserved.** Requires graded rater labels. Test T8 fails if anything computes one. |

This exists so a proxy metric cannot quietly promote a ranking, which is
precisely what happened with V8.

### Eighteen invariants, all passing

Each has caught, or would have caught, a real bug in this program:

- every ranking is a permutation within each proof — nothing is deleted;
- candidate coverage is identical across rankings on a fixed universe;
- every slider policy is nested as its parameter opens;
- **components are monotone non-increasing** and the giant fraction monotone
  non-decreasing as edges are admitted — the exact invariant a
  partition-accumulation bug violated earlier the same day, growing components
  from 255k to 450k;
- the SourceOracle is optimal for `SourceHit@1`;
- **the oracle's ceiling equals candidate coverage**, not 1.0;
- universes nest U1 ⊆ U1D ⊆ U0;
- no metric claims to be `Semantic*`.

---

## 2. The definition question is settled

Definitions were being lost, and the cause was exact: the load-bearing role
filter was designed around how *theorems* appear in proof terms. Definitions
appear in type positions, implicit arguments and instance slots — because that
is where a definition gets used.

New universe **U1D**: load-bearing roles for theorems, **all roles for
definitions**. Coverage of what humans actually wrote:

| universe | theorems | definitions | overall |
|---|---|---|---|
| U1 (historical) | 80.7% | 47.5% | 60.0% |
| **U1D** | 80.6% | **82.1%** | **81.2%** |
| U0 (everything) | 80.7% | 82.1% | 81.2% |

**U1D recovers 5,479 definition citations at no cost to theorems, and reaches
the same coverage as admitting everything.** Humans write nearly twice as many
definition citations as theorem citations (15,769 vs 8,719), so this was the
larger half of the record going missing.

Per the audit's warning, these are restored **with roles preserved** — they are
not thereby declared key moves. Where they belong in the ordering is a
question for semantic evaluation, not for a filter.

---

## 3. Ranking standings (universe U1)

| ranking | SourceHit@1 | MRR | glue@1 | tied pairs |
|---|---|---|---|---|
| **R_introduced_depth** | **0.603** | **0.663** | 0.073 | 0.055 |
| R_v8_all_kinds | 0.591 | 0.655 | 0.027 | 0.035 |
| R_v8_faithful | 0.587 | 0.652 | 0.112 | 0.029 |
| R_depth | 0.570 | 0.636 | 0.070 | 0.089 |
| R_phase5_composite | 0.561 | 0.641 | 0.056 | 0.002 |
| *O_source (coverage bound)* | *0.759* | *0.759* | *0.086* | *0.089* |
| B0_random | 0.243 | 0.387 | 0.353 | 0.000 |
| B3_term_order | 0.225 | 0.375 | 0.378 | 0.000 |
| B1_reverse_depth | 0.128 | 0.256 | 0.631 | 0.089 |
| B2_popularity | 0.120 | 0.243 | 0.564 | 0.006 |

The leader is the **simplest** real candidate: two signals, no demotion
machinery, no claims filter. V8's full apparatus scores lower.

**Popularity lands at 0.120 — below random.** Library-wide citation count is
anti-correlated with being the key move of a particular proof. This retires
"importance = how often cited" **as a local keyness score**; it says nothing
about reuse, API importance, or curation, and that scope matters.

### By target depth

| ranking | 0-10 | 11-25 | 26-50 | 51-75 | 76-125 | 126+ |
|---|---|---|---|---|---|---|
| O_source (bound) | 0.729 | 0.601 | 0.799 | 0.891 | 0.805 | 0.828 |
| R_introduced_depth | 0.567 | 0.427 | 0.570 | 0.753 | 0.638 | 0.714 |
| R_v8_faithful | 0.544 | 0.411 | 0.553 | 0.729 | 0.627 | 0.704 |

Every ranking dips in the 11–25 band — but so does the oracle (0.601). That
dip is a **coverage** failure, not a ranking failure, and it would have been
misread as the latter without the oracle line.

---

## 4. Corrections to previously reported claims

Three numbers I reported earlier were wrong. All are corrected in the
apparatus and enforced by tests.

**"75.9% is the ranking ceiling" — WRONG.** It is a *SourceOracle*, and test
T6 now asserts what it actually equals: the fraction of proofs with any human
citation present in the candidate set (0.7595 = 0.7595 exactly). It was
measuring coverage failure the whole time.

**"P@1 is precision" — WRONG NAME.** It is `SourceHit@1`: agreement with what
the author wrote. A proof may mention six lemmas and only one is the
conceptual core. No ranking can be promoted on this alone.

**"Definitions are the bridges (58.8% of merges)" — WITHDRAWN.** With
enrichment normalised by eligibility and batch-invariant mergers, definitions
sit at 1.00–1.04, exactly their base rate:

| kind | enrichment k=2 | k=3 |
|---|---|---|
| constructor/recursor | 1.23 | **5.64** |
| glue | 1.06 | 0.92 |
| definition/construction | 1.04 | 0.69 |
| theorem | 0.86 | 0.43 |

What *is* enriched: **constructors and recursors** — 6% of eligible edges but
33.8% of component crossings at k=3 (CI 5.45–5.77). The structural eliminators
are doing the connecting, which nobody predicted.

Also corrected: the island/technique hypothesis was refuted by controls
(components are 5.3x more subject-coherent than size-matched random, so they
are a subject atlas), and the honest lift over a *shuffled-ranking* control is
only 1.30x — most coherence comes from the hypergraph, not from any ranking.

---

## 5. What is still not established

- **Semantic keyness of any ranking.** Every number here is source alignment
  or structure. Promoting `R_introduced_depth` requires graded rater labels on
  a pre-registered sample, and the apparatus deliberately refuses to compute a
  `Semantic*` metric until those exist.
- **Cross-proof comparability.** Every candidate is a *within-proof* ordering.
  A map must compare an incidence in one proof against one in another, and a
  global slider ("top 25% overall") is meaningless without it. Tie statistics
  are reported per ranking as a first diagnostic; the calibration work is not
  done.
- **The remaining 19%** of human-written citations absent even from U0 —
  erased during elaboration before any kernel term exists. Only the provenance
  channel can recover those, and it is built but not merged into the views.

## 6. Recommended next step

Run the semantic annotation panel on a pre-registered stratified sample, with
the candidate universe fixed to U1D. That is the only instrument that can
promote a ranking, and everything built today is diagnostics until it exists.

It needs a decision from the owner on scale and rater budget.
