# Map search vs an LLM at premise retrieval (2026-08-22)

Sam's question, and the answer is not flattering to the map.

## Setup

Identical task for both: from a theorem's STATEMENT ALONE, name the 10
Mathlib declarations its proof will cite. Ground truth = the proof's
map moves (GAPC zoom-1 edges). 60 held-out theorems; the theorem's own
edges are removed from the graph before the map predicts. Mean 1.95
true moves per theorem.

- **map** = Lambda co-use scored from the statement world, top 10.
- **LLM** = Opus, statement only, explicitly forbidden from reading any
  Mathlib source or searching the corpus; answers from its own
  knowledge. Two conditions:
  - NAMED: real declaration name and module shown
  - BLIND: name replaced by `target_thm`, module withheld

## Result

| system | recall@10 | top-1 hit |
|---|---|---|
| map (Lambda from statement) | 0.098 | 0.118 |
| **LLM, named** | **0.444** | 0.183 |
| LLM, blind (anonymised) | 0.360 | -- |
| map + LLM union (20 slots) | 0.475 | -- |

Paired over 60 theorems: LLM better on 47%, tie 47%, **map better on
7%**. The LLM wins, by roughly 4.5x.

## Contamination: real, but not the whole story

Sam's caveat is correct and unquantifiable in the strict sense -- the
model has read Mathlib. The BLIND condition bounds it: stripping the
declaration name and module costs the LLM only 19% relative (0.444 ->
0.360), not a collapse. If it were purely recalling "the proof of
`Foo.bar_baz`", anonymising the name should have hurt far more. So a
substantial part of its advantage is genuine mathematical inference
from the statement, not lookup. Name validity (predicted names that
actually exist in Mathlib) was 0.878 named / 0.832 blind -- it is not
hallucinating a fake namespace either.

## Where the map actually fails

1. **It abstains 15% of the time.** On 9 of 60 theorems the statement
   world had no co-use neighbours at all, so the map returned NOTHING.
   The LLM scored 0.778 on exactly those 9 -- the map is blank
   precisely where the answer is easy.
2. **On the 51 where it does predict, it still loses**: 0.115 vs 0.385.
3. Its errors are same-neighbourhood-wrong: for
   `QuadraticForm.discr'_smul` it proposed `Matrix.det_transpose`,
   `Matrix.det_mul`, `Matrix.det_one` when the answer was
   `Matrix.det_smul_of_tower` -- right area, right subject, wrong lemma.
   Co-use statistics locate the neighbourhood; they do not discriminate
   within it.

## What the map contributes anyway

Union recall 0.475 vs LLM alone 0.444: the map adds 3.1 points, and
4 of 117 true moves (3.4%) were found by the map and missed by the LLM:

    CoxeterSystem.IsReflection.inv  -> CoxeterSystem.inv_simple      (rank 1)
    UniformOnFun.postcomp_uniformContinuous
                                    -> uniformContinuous_iff_le_comap (rank 2)
    Finsupp.mem_range_embDomain_iff -> Finsupp.embDomain_eq_mapDomain (rank 3)
    eventually_singleton_add_smul_subset -> norm_nonneg               (rank 3)

Small, and honestly reported as small.

## How to read this

The map is not, and on this evidence should not be sold as, a better
next-move predictor than a language model. What it is: a
semantics-free object built from kernel facts alone, no names, no
training, that ranks a 281k-declaration pool and lands a true move in
its top 10 about a tenth of the time (random: 0.00004). It is a
structural prior, not a solver.

The honest framing for the program: the map's value has to come from
what a language model CANNOT do -- append-safety, determinism, an
auditable reason for every edge, coverage of mathematics written after
any training cutoff (the chronological test: 13.5x), and stability
under refactoring (metamorphic: 0.868 vs 0.000). Retrieval accuracy
against a frontier model is not the ground it wins on, and this
experiment says so.

## Caveats

- n=60, mean 1.95 answers per theorem, so per-item recall is coarse
  (0, 0.5, 1). Differences this large are not at risk from that; the
  3.1-point union gain is.
- The map's top-10 here uses a deterministic tie-break (lowest
  in-degree), where premise_retrieval.py used tie-fair expectation over
  the full pool -- which is why its number here (0.098) sits below the
  1500-query figure (0.155).
- Ground truth is OUR inclusion policy's move set. A move the LLM names
  that is genuinely used but not selected as a map edge scores as a
  miss for both systems equally, so the comparison is fair, but the
  absolute ceiling is not 1.0.
- One LLM, one prompt, no retrieval augmentation, no chain of thought
  budget beyond default. A weaker or stronger model moves this number.
