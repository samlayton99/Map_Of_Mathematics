# The inclusion policy: largest-depth-gap cut (2026-08-21)

Ranking and inclusion are different axes. The ranking (laneD_stmt) was
settled; inclusion had been a crude global top-4. The adopted policy:

> Per proof, sort candidates by cited depth and cut at the LARGEST GAP.
> Everything at or above the gap is the proof's mathematics; everything
> below is its relative plumbing.

Properties: purely local (only this proof's own depths — append-safe by
construction), zero constants (the break is the proof's own argmax, so it
adapts from depth-300 proofs to depth-12 proofs), relative (principle 10
implemented at the inclusion axis).

## Per-proof, against grades (strict matching, 522 proofs)

| policy | precision | junk share | recall | empty |
|---|---|---|---|---|
| top-4 | 0.434 | 0.298 | 0.854 | 0.000 |
| lane cut (EL0) | 0.918 | 0.013 | 0.551 | 0.280 |
| gap cut | 0.818 | 0.045 | 0.635 | 0.021-0.051 |

Gap trades a little of EL0's precision for +8pts recall and solves the
28%-empty failure (foundational proofs keep their content).

## Refactoring stability (metamorphic pairs)

Included-set Jaccard: harmless 0.772 vs control 0.062 — the most stable
set measured (move lane: 0.644/0.028). The within-proof depth profile is
route-determined.

## Map level (corrected substrate, full corpus)

| metric | flat4 | E4 | EL0 | GAP |
|---|---|---|---|---|
| community-vs-area AMI | 0.212 | 0.342 | 0.335 | **0.386** |
| modularity | 0.600 | 0.684 | 0.675 | **0.886** |
| distance AUC | 0.541 | 0.574 | 0.567 | **0.627** |
| within-area edge share | 0.533 | 0.669 | 0.538 | **0.787** |
| top-100 hub link share | 0.407 | 0.211 | 0.176 | **0.109** |
| cross-area plumbing share | 0.743 | 0.489 | **0.033** | 0.350 |
| edges | 1.48M | 1.70M | 1.46M | 1.06M |

GAP dominates every emergent-structure metric. EL0 stays cleanest on
cross-area plumbing (definitionally — it filters transport). The two
compose: GAP decides WHAT is an edge; the lane/span geometry decides HOW
a cross-area plumbing edge above the gap renders (vertical portal).

Caveats: modularity partly reflects the sparser graph (1.06M edges) —
AMI and AUC are the guard metrics and both improved; graded evaluation
inherits the depth-visible brief contamination; k distribution: median 1,
p90 5, mean 2.49.
