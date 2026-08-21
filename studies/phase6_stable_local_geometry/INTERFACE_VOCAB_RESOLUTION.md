# The interface-vocabulary mechanism: resolved (2026-08-21)

Three problems were attributed to OfNat/HAdd/coercion-class vocabulary.
Explored to closure; each has a different answer, and none is a new
demotion rule.

## 1. Per-proof ranking: NO new mechanism — tested and rejected

The kernel-principled cut (a citation is a reasoning move iff the cited
constant is proof-valued, `pr`; data-producing citations are term
construction), applied to theorem targets only:

| placement of data-vocab | KM@1 | R@4 | vs laneD_stmt |
|---|---|---|---|
| below transport (vocabB) | 0.847 | 0.855 | -34/+6, p=8e-6 |
| above transport (vocabA) | 0.906 | 0.895 | -5/+2, p=0.45 |

Graders' ontology disagrees with the cut: data-valued definitions
(`Real.posLog`, `Finset.Ico`) ARE key moves of theorem proofs. laneD_stmt
stands unmodified.

## 2. Metamorphic tail instability: a METRIC artifact

Raw candidate-set Jaccard across harmless pairs is 0.549; top-4 Jaccard
0.603 sits ABOVE it — the ordering already concentrates shared content
better than the citation sets agree. 47% of pairs have <= 5 candidates,
so top-4 measured proof-length variance. The honest metric is the MOVE
LANE at variable k (all lane-0 items; median k = 1):

    harmless 0.644 vs control 0.028  (separation 23:1; top-4 gave 6:1)

Registered as the metamorphic benchmark's primary skeleton metric.

## 3. Map hubs: a RENDERING question, geometrically validated

Relative span rho = (d_target - d_cite)/(1 + d_target) of admitted
laneD top-4 edges, 19,921 fresh artifacts:

| destination class | median rho | share rho > 1/2 |
|---|---|---|
| proof-valued citations | 0.100 | 0.259 |
| data/predicate vocabulary | 0.500 | 0.494 |
| transport | 0.806 | 0.718 |

The three classes form an ordered spectrum in the (cited depth, span)
geometry with no name lists: proof moves are same-scale (lateral),
transport is near-foundational (vertical), interface vocabulary sits
between. A long-span-renders-vertical rule removes ~72% of transport and
~49% of vocab edge mass from lateral hub rendering while touching 26% of
proof-move edges — edges preserved, nothing demoted. The concrete rule
(fixed rho threshold vs within-proof relative span rank) is decided with
the map pipeline's hub-by-span-band profiles.
