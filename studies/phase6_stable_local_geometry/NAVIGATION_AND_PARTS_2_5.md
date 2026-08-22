# GPT program Parts 2-5: results (2026-08-22)

One session, marched in order. Frozen construction untouched throughout.
All studies on the holdout-blind GAPC graph unless noted. Tie-fair AUPRC
everywhere (a stable-sort tie bug was caught and fixed before any number
was recorded; it had inflated one AUPRC from 0.13 to 0.67).

## Part 2 — multiscale V-profile (src/multiscale_v.py, 4 seeds)

AUPRC vs matched negatives (prior 0.091), co-use pairs from held-out proofs:

| score | AUPRC |
|---|---|
| multiscale discounted (r<=4) | **0.350** |
| radius 2 only | 0.332 |
| radius 3 / 1 / 4 | 0.316 / 0.270 / 0.283 |
| flat graph radius 2 | 0.213 |

- Multiscale beats every single radius; r=2 was the best single choice.
- Branch-drop record (first touch of the two cones): 54% symmetric,
  33% one-level asymmetric, 13% asymmetric by >=2. Median total drop 3.
- Negatives that touch at all are DEEPER (median 5) and MORE asymmetric
  (29% >=2). Co-use lives at shallow, near-symmetric touches; GPT's
  asymmetric-drop pairs exist but are not the co-use signature.

## Part 3a — matched negatives + AUPRC upgrade

Negatives now matched on min-depth band AND same/cross-area AND
out-degree bin of both endpoints (old protocol: depth only).

- Old protocol reproduced exactly: pos kinship 0.368, lift 23x.
- New protocol: pos kinship 0.364 (unchanged), neg 0.016 -> 0.030.
  **Lift 23-33x -> 12x; the entire compression is harder negatives.**
  Flat graph under the same matching: 1.5x, AUPRC 0.213.

## Part 3b — provenance-resolved positives (src/prov_validation.py)

External pair source: elaboration sidecar, 40 files, 4,447 decls -- the
names the human AUTHOR's source referenced. Our inclusion contributed
nothing to these pairs.

- 2,915 pairs: kinship 0.081 vs matched 0.020, lift 4.0x;
  AUPRC 0.128 vs prior 0.091.
- Honest read: raw source refs mix moves with machinery; the signal is
  real but diluted ~3x vs move-pair positives. This is the external
  floor, the 12x is the move-level number.

## Part 3c — chronological: script ready, NOT RUN

src/chrono_validation.py + full mathlib4 file-date history extracted
(blobless clone). Deliberately not run: Sam called validation sufficient
mid-session. Run cost when wanted: ~2 minutes.

## Part 4 — navigation benchmark (the new center)

### v1: next-lemma retrieval (src/navigation_benchmark.py)
Given ONE move of a held-out proof, rank all 281,205 pool theorems for
its OTHER moves. Tie-fair expected recall.

| method | recall@10 | recall@100 | MRR |
|---|---|---|---|
| Lambda co-use (map) | **0.246** | 0.338 | 0.127 |
| kinship + Lambda | 0.208 | **0.357** | 0.112 |
| V-kinship alone | 0.049 | 0.150 | 0.021 |
| name-token text | 0.036 | 0.152 | 0.011 |
| flat-graph co-use | 0.024 | 0.026 | 0.016 |
| popularity | 0.024 | 0.066 | 0.012 |
| random | 0.00004 | 0.0004 | -- |

Flat co-use is crippled at the source: only 12.4% of flat top-4 edge
targets are pool theorems (GAPC: 40.2%) -- the flat graph cites
machinery, so it cannot even form theorem-level co-use.

### v2: premise retrieval from the STATEMENT (src/premise_retrieval.py)
Query = only what exists before the proof (statement-world citations +
target name). Answers = the proof's map moves. Same pool.

| method | recall@10 | recall@100 | MRR |
|---|---|---|---|
| Lambda from statement | **0.155** | **0.321** | 0.077 |
| combined | 0.093 | 0.187 | 0.047 |
| text (name tokens) | 0.064 | 0.168 | 0.033 |
| V-kinship from statement | 0.020 | 0.062 | 0.009 |
| popularity | 0.018 | 0.046 | 0.008 |

First direct evidence on "does the map help PROVE": from the statement
alone, map co-use retrieves the proof's actual moves at 2.4x the text
baseline at recall@10 (4,350x random). Negative result recorded: V is
not a retriever; retrieval power lives in Lambda. V's role stays what
Part 2 measured -- kinship/structure, not search.

### v3: route finding (src/route_finding.py, 800 tasks)
Statement seed -> proof move, held-out proof's own edges excised.

| | atlas | flat |
|---|---|---|
| route found (<=8 hops) | 0.39 | 0.79 |
| median length | 2 | 3 |
| intermediates: math lane | **87%** | 63% |
| intermediates: transport | 13% | 37% |
| intermediates through top-100 hubs | **9%** | 32% |

The trade is explicit: the atlas reaches less (sparser by design) but
travels through mathematics; flat routes go through hubs 3.4x more.
The 39% reachability is the open navigation problem to fix (portal
edges, Lambda edges as traversal links).

## Part 5 — self-similarity across depth (src/depth_self_similarity.py)

Bands 11-25 / 26-50 / 51-100 / 101-200: near-identical geometry --
kinship 0.30-0.43, ~55% symmetric touches, median total drop 3,
k median 1-2. ONE regime change, at the deep end (201+): graph
densifies, base co-use rate x10, lift compresses to 6.8x, k median 3.
The special band is the modern frontier, not the foundations.

## Freeze debt — CLOSED (data/blind2, src/blind2_eval.py)

Fresh sample: 48 def targets (12/band, seed 20260911, all previously
ungraded), 3 independent blind raters, 658 slots, tag-free briefs
(contract greps clean).

- Rater ceiling on fresh defs: 0.944.
- **Frozen def KM@1: 0.756** (n=45). The 0.903 was partly fit to
  blind1's 36 defs; ~0.76 is the honest generalization number (from
  0.516 pre-cleanup). Boundary F1 0.642 vs random 0.272.
- ctor rule CONFIRMED (drop: KM -0.023, F1 -0.016).
- classproj rule CONFIRMED (drop: KM -0.023, F1 -0.033).
- U1D-admission rule NEUTRAL: helps blind1 (+0.038), hurts blind2
  (-0.019), net ~0 over 84 targets. Kept (no churn on a wash);
  flagged as first cut at the next revision. frozen.py untouched;
  frozen_test still passes by construction (rule is boundary-only).

## What this session changes about the program

1. The co-use headline is now 12x (strictly matched), 4x (external
   provenance floor), AUPRC 0.35 vs 0.21 flat vs 0.09 prior.
2. Navigation went from untested to measured: Lambda is a real
   retriever (0.25 next-lemma, 0.16 from-statement at top-10 of 281k);
   V is structure, not search; atlas routes are mathematical but reach
   only 39%.
3. Def ranking honest number: 0.756, ceiling 0.944 -- real headroom,
   now measured on labels no rule ever saw.
4. Open next: route reachability (add Lambda/portal traversal edges),
   learned combination of Lambda+V+text for premise selection,
   chronological run if ever wanted (script ready).
