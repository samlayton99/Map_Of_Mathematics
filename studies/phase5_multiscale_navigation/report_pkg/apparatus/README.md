# mathmap_eval — the evaluation apparatus

An API for testing **ranking techniques** and **inclusion policies** against
the exact citation record, with baselines that make the numbers mean
something.

Three things are kept strictly apart, because conflating them is how this
program went wrong before:

| layer | what it decides | whose job |
|---|---|---|
| **corpus** | what relationships exist | the extractor's |
| **ranking** | in what ORDER they appear | ours to get right |
| **inclusion** | how much of that order a view ADMITS | the user's |

## Quick start

```bash
python -m mathmap_eval list                 # registered rankings + policies
python -m mathmap_eval compare              # full head-to-head, all tables
python -m mathmap_eval coverage             # candidate coverage per universe
python -m mathmap_eval bridges --boot 100   # bridge enrichment, batch-invariant
python -m mathmap_eval nested               # verify sliders are really nested
python -m mathmap_eval.tests                # 18 invariants
```

```python
from mathmap_eval import run, RunConfig, compare_table, depth_table
out = run(RunConfig(universe="U1D"))
print(compare_table(out))
print(depth_table(out))
```

## Adding a ranking

Rankings return ascending lexicographic sort keys. They **order** the complete
universe and never delete: whatever a ranking dislikes, it ranks last.

```python
from mathmap_eval import ranking

@ranking("R_mine", features=2, thresholds=0)
def _mine(c, base):
    "Proof-introduced first, then deepest cited. (Docstring is published.)"
    return (c.inc_in_stmt_world[base].astype("int8"),
            -c.inc_d_cite[base].astype(float))
```

It is now in `list`, `compare`, and every table, with baselines attached.

## Adding an inclusion policy

Policies return a boolean mask and must be **monotone** in their opening
parameter, so a slider is a nested family. `nested` verifies this.

```python
from mathmap_eval import inclusion

@inclusion("my_policy", "per-proof", monotone_param="k")
def _mine(c, base, ranks, k=1):
    return ranks < k
```

## Candidate universes

Declared, never silently applied:

| universe | definition |
|---|---|
| `U0` | every exact occurrence, any role |
| `U1` | load-bearing roles only (the historical filter) |
| `U1D` | U1 for theorems, **all roles for definitions** |

Measured coverage of what humans actually wrote:

| universe | theorems | definitions | overall |
|---|---|---|---|
| U1 | 80.7% | 47.5% | 60.0% |
| **U1D** | 80.6% | **82.1%** | **81.2%** |
| U0 | 80.7% | 82.1% | 81.2% |

U1D recovers 5,479 definition citations and reaches U0's coverage at no cost
to theorems. Definitions are used in type, implicit and instance positions —
that is *where a definition gets used* — and the load-bearing filter was
designed around how theorems appear.

## Metric naming is enforced

| prefix | meaning |
|---|---|
| `Source*` | agreement with identifiers the human wrote. **Not keyness.** A ranking cannot be promoted on `Source*` alone. |
| `Role*` | descriptive composition at a rank (e.g. how much glue). A statistic, not a judgement. |
| `Coverage*` | what fraction of ground truth exists in a universe. A property of candidate generation. |
| `Graph*` | components, giant fraction, entropy, susceptibility, enrichment. |
| `Semantic*` | **reserved.** Requires graded rater labels. Nothing here computes it, and test T8 fails if anything tries. |

## The oracles

`O_source` is a **SourceOracle**: it ranks the human's own citations first. It
is an upper bound for `Source*` metrics only. Test T6 asserts that its ceiling
equals candidate coverage exactly (0.7595 = 0.7595), which proves that a
sub-100% source oracle measures **coverage failure, not ranking quality** —
the error that produced the earlier "75.9% ceiling" claim.

A `CandidateSemanticOracle` and `FullEvidenceSemanticOracle` require rater
labels and are deliberately absent.

## Self-tests

`python -m mathmap_eval.tests` checks 18 invariants. Each one has caught, or
would have caught, a real bug in this program:

- **T1** every ranking is a permutation within each proof (nothing deleted).
- **T2** candidate coverage is identical across rankings on a fixed universe.
- **T3** every slider policy is nested as its parameter opens.
- **T4** components are monotone non-increasing and the giant fraction is
  monotone non-decreasing as edges are admitted. *A partition-accumulation bug
  once made components grow from 255k to 450k; this test catches that class.*
- **T5** the SourceOracle is optimal for `SourceHit@1`.
- **T6** the oracle's ceiling equals coverage, not 1.0.
- **T7** universes nest: U1 ⊆ U1D ⊆ U0.
- **T8** no metric claims to be `Semantic*`.

## Current standings (universe U1)

| ranking | SourceHit@1 | MRR | glue@1 | tied pairs |
|---|---|---|---|---|
| R_introduced_depth | **0.603** | **0.663** | 0.073 | 0.055 |
| R_v8_all_kinds | 0.591 | 0.655 | 0.027 | 0.035 |
| R_v8_faithful | 0.587 | 0.652 | 0.112 | 0.029 |
| R_depth | 0.570 | 0.636 | 0.070 | 0.089 |
| R_phase5_composite | 0.561 | 0.641 | 0.056 | 0.002 |
| *O_source (coverage bound)* | *0.759* | *0.759* | *0.086* | *0.089* |
| B0_random | 0.243 | 0.387 | 0.353 | 0.000 |
| B3_term_order | 0.225 | 0.375 | 0.378 | 0.000 |
| B1_reverse_depth | 0.128 | 0.256 | 0.631 | 0.089 |
| B2_popularity | 0.120 | 0.243 | 0.564 | 0.006 |

`B2_popularity` scoring below random retires "importance = citation count"
**as a local keyness score**. It says nothing about reuse, API importance or
curation.

## Bridge enrichment (batch-invariant)

`Enrichment(a) = P(a | crosses prior components) / P(a | eligible now)`.
Mergers are found by freezing the prior partition and taking connected
components of the quotient graph over the whole tied batch, so no single edge
is credited by iteration order.

| kind | k=2 | k=3 |
|---|---|---|
| constructor/recursor | 1.23 | **5.64** |
| glue | 1.06 | 0.92 |
| definition/construction | 1.04 | 0.69 |
| theorem | 0.86 | 0.43 |

**Definitions are at ~1.0 — not enriched.** The earlier "definitions cause
58.8% of merges, so they are the bridges" was a base rate, and the claim is
withdrawn. What *is* enriched is constructors and recursors: 6% of eligible
edges but 33.8% of component crossings at k=3.
