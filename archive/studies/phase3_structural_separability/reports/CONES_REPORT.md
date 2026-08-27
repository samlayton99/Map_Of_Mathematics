# Statement Cone vs Proof Cone — Full-Library Study (2026-08-19)

Data: `data/cones_results.json`. Code: `src/cones.py`. Graph: full `import Mathlib` closure (771,129 constants). Sample: the 24 reviewed proofs + 500 random unclassified theorems (seed 20260819), cones computed exactly by bitmask propagation. Constraints honored: no name/namespace cuts, no probabilistic-classifier filtering; deterministic P3 classes used as evaluation labels only.

Definitions. For theorem T: **A_S(T)** = all ancestors reachable from the constants in T's statement; **A_P(T)** = all ancestors reachable from its proof term; **N(T) = A_P \ A_S** = mathematics the proof introduced beyond what stating the problem already required.

## 1. What does global dependency depth actually measure?

One thing, three disguises. Over the sample: Spearman(depth, log ancestor-count) = 0.98; Spearman(depth, log unfolded-tree-size) = 0.992; Spearman(ancestor-count, tree-size) = 0.98. Depth, total-distinct-prerequisites, and fully-unfolded proof-tree size are monotone transforms of a single latent coordinate: **log-volume of the library beneath you**. There is no separate "height vs width" information at global scale (confirming the earlier depth≈size finding, now with the set-based third witness).

Byproduct — sharing factor: median log10(tree size) − log10(ancestor set) = **8.2**. The unfolded proof tree is ~10^8 times larger than the set of distinct facts it uses; formal proofs reuse the same facts astronomically often.

## 2. Which formal roles have distinctive structural signatures? (labels only, no filtering)

| role | n | med depth | med stmtDepth | med relDepth | med log10 users | strongest coordinate (oriented AUC) |
|---|---|---|---|---|---|---|
| structure-projection | 15,056 | 1 | 3 | 0 | 1.61 | shallow depth 0.96; **many users 0.79** |
| coercion | 110 | 3 | 2 | 0 | 0.69 | shallow depth 0.99 |
| recursor | 6,913 | 5 | 5 | 0 | 1.39 | **many users 0.77**; shallow 0.84 |
| generated | 95,465 | 11 | 7 | 0 | 0.69 | shallow depth 0.79 |
| internal-detail | 297,988 | 28 | 15 | 1 | 0.69 | weak everywhere (0.67 max) |
| typeclass-instance | 42,904 | 35 | 11 | **9** | 1.10 | **relDepth 0.64** — digs 9 levels past its statement |
| unclassified defs | 72,280 | 32 | 8 | **7** | 1.39 | — |
| unclassified theorems | 287,483 | 64 | 45 | 2 | 0.69 | — |

Two distinct machinery signatures emerge: **glue is shallow** (projections/coercions/recursors, near-perfect by depth) and additionally **heavily reused** (projections and recursors are the only roles whose user-count is discriminative). **Instances are the opposite**: shallow *statements* (median 11 vs theorems' 45) with bodies that dig 9 levels deeper — relDepth is the first single coordinate that sees them at all (depth alone was a coin flip, 0.56).

relDepth is not a machinery axis at all — it is a **construction-vs-assertion axis**: definitions (7) and instances (9) build objects deeper than their statements; theorems (2) mostly restate what their statements already imply. Instances score as machinery on it only because they are constructions living among assertions.

## 3. Does a multiscale geometry appear?

The interface layer is enormous: **35% of unclassified theorems have relDepth ≤ 0** (proof no deeper than statement; 51% at ≤ 2), and **19% of sampled theorems have N(T) = ∅** — the proof stays entirely inside the statement's own prerequisite cone. The `dist_triangle` phenomenon (shallow interface over deep implementation) is not an anomaly; it is a third of the library. Median share of proof-cone that is new: 12%; p90: 87% — theorems split cleanly into "restatements/interface" (N empty or tiny) and "constructions" (N dominates, e.g. `IsClosed.and`: statement cone 5, proof cone 1,479, 99.7% new).

## 4. Does N(T) = A_P \ A_S expose the mathematical moves? — YES (headline)

Two ends of the spectrum, both informative:

- `Real.abs_log_mul_self_lt` (depth 169): statement cone 15,725; proof adds **29** new facts. The deepest new ones are exactly the proof's moves: `Real.log_nonneg`, `Real.log_nonneg_iff`, `Real.log_one`. Everything else the proof touches was already implied by stating the problem.
- `IsClosed.and`: statement cone 5; proof cone 1,479. Deepest new element: `IsClosed.inter` — the one lemma the proof actually invokes.

Move-identification rematch on the reviewed proofs (overlap of top-5 with the P4-route applied-lemma skeleton, median): **ranking by "new, then depth" scores 0.775 vs 0.708 for depth alone** — it never hurt any proof and rescued the failures (`limUnder_of_not_tendsto` 0.0 → 0.75; `Nat.eq_one_of_dvd_coprimes` 0.67 → 1.0). Against the (rigged-against-us) proxy keys: 0.225 vs 0.20, matching the best Phase 3 local method's neighborhood.

Reuse as a signal: ranking by **most-used scores 0.0** (the most-reused facts are pure glue); rarely-used ties new-depth on proxy keys (specialized = contentful).

## 5. Do global features beat Phase 3 local features for landmarks?

For finding a proof's applied lemmas: yes — two precomputed global numbers per constant (depth + statement-cone membership) recover 77.5% of the route skeleton without opening the proof, where Phase 3's global features scored ~0.2 on proxy keys. For *ordering* the moves by importance, the exact local route view remains better; the global coordinates are the cheap filter, not the final ranking.

## 6. Surprises / falsified intuitions

1. Depth, cone size, and tree size were three hypotheses; they are one measure (0.98+). "Find a better combination of depth and size" is a dead end — falsified.
2. Automation pollution reappears inside N(T): omega certificate lemmas (`Lean.Omega.LinearCombo.coordinate_eval_*`, d=45) enter the new set of arithmetic proofs. N(T) does not by itself remove tactic-generated noise.
3. Reuse inverts intuition: being used everywhere marks glue, not importance. Raw "descendant count" will be a machinery detector, not a landmark detector.
4. Instances are not "deep machinery" so much as **relDepth outliers**: shallow claims, deep constructions — a signature theorems don't share.

## 7. Single next experiment

Generate the "**proof-introduced mathematics**" view for the 12-proof user packet: per proof, show N(T) ranked by depth (statement-relative, name-free, zero training) next to the existing P4-route view, and let the user judge which reads as "the moves." This directly tests the only claim that matters — whether the view helps a mathematician — on infrastructure that already exists.
