# Defense Brief — The Kernel-Invariant Move Formulation

Prepared by the implementing agent. All numbers are reproducible from the included data files and scripts; every claim cites its source.

## 1. The formulation on trial

For any theorem T in Mathlib (771,129 constants, full `import Mathlib` closure):

1. **Candidates** = constants occurring in T's proof term at *load-bearing positions* (applied as a step, bound in a let, or filling an explicit argument), excluding occurrences that only fill instance-implicit/implicit slots or type annotations. (Dump field `hb`; extraction is a purely syntactic walk of the kernel term.)
2. **Claims filter**: keep only Prop-valued constants (a step of an argument must be a claim; instances and definitions are constructions).
3. **Container semantics**: a candidate cited exactly once in the entire library is a container (compiled private helper or once-used lemma) — opened for ranking, label retained for membership.
4. **Ranking**: candidates not already in the statement's prerequisite cone first ("new to the statement"), then by depth (length of the longest unfolding chain to the axioms).
5. **Display grouping** (no filtering): relevant / imported / logic-bookkeeping, by measured subject-matter overlap with the statement cone; plus three strategy facets (induction, case-split, extensionality) from the proof term's root shape.

Every primitive is a fact of the kernel calculus — statement vs body, Prop vs Type, citation positions, citation counts — or a measured library-relative quantity (concept universality). No names, no namespaces, no tactic knowledge, no trained models.

## 2. Performance evidence

**Precision** (`data/moves_results.json`, `src/moves.py`; 2,355 uniformly random unclassified theorems, seed 20260819):
- Rank-1 is a genuine named lemma: **90.3%** overall; **94.6%** in the deep tercile (depth 81–323); 91.5% mid; 83.4% shallow.
- Top-2 contains one: **94.2%**.
- Error *decreases with depth* — the measure purifies as the library grows, which was an explicit design requirement.
- The largest historical failure mode (typeclass instances topping lists) fell from 99 rank-1 blames to **1** from the position rule alone, with no instance-specific logic anywhere.

**Recall** (`data/moves_results.json` §B; independent ground truth = lemma names humans explicitly wrote in proof source, 130 random proofs): mean **92.5%**, median **100%**. Loss forensics: 28 of 30 examined misses were dissolved by the single-use inlining rule (verified in-degree ≤ 1), i.e. self-inflicted and *restored by construction* under container semantics → realistic recall **~97–99%**. Only 2 losses trace to the position rule, both background side-conditions.

**Consistency with prior best** (`C2` in the same file): the move set contains the previously highest-rated per-proof view (the hand-verified applied-lemma skeleton of 20 reviewed proofs) at **median 100% coverage**.

**Qualitative exhibits** (`data/moves_results.json` §D, `data/relevance_results.json` gradient): the extracted lists read as proof sketches — `Nat.exists_infinite_primes` yields Euclid's argument verbatim (minFac_prime, minFac_dvd, Prime.not_dvd_one, dvd_factorial); `Real.exp_add` exposes the non-obvious via-ℂ strategy; `deriv_add` yields the exact three-step argument; `dist_triangle` correctly reports "interface, no proof content". Depth-cutoff slices over recursive move trees produce nested, coherent abstraction layers on all six anchors (e.g. `integral_add`: setToFun layer → L1/Integrable layer → functional analysis).

## 3. The longevity argument (why this stands as Lean evolves)

The formulation uses only the kernel calculus — the dependent type theory with Prop that *defines* what Lean is. Names, tactics, `to_additive`, simp-normal forms, and every automation framework live in the elaboration layer above it and change yearly; the kernel term of every accepted proof must forever express its argument in applications, binders, and sorts. Consequences:

- Any future "structural bureaucracy" consists of constructions → excluded by the claims filter *by what bureaucracy is*.
- Any future compiled-helper scheme produces single-use constants → handled by container semantics *by what private means*.
- Any future automation's certificate vocabulary structurally cannot enter mathematical statements (no one states theorems about a solver's internal data structures) → the statement/proof asymmetry that our measures exploit **widens** as the library grows, rather than decaying like a patch.
- The three shipped strategy facets rest on recursors, fix operators, and `isRec` — kernel-generated machinery.

The formulation contains zero facts that a Lean release, a tactic rewrite, or a naming-convention migration could invalidate.

## 4. The graveyard — alternatives already tried, with their causes of death

The court should not be offered these as fresh suggestions; each was implemented and measured in this program:

1. **Learned classifier over typed topology features** (Phase 3, `MACHINERY_SEPARABILITY.md`): machinery detection AUC 0.80 — but in blinded landmark review its ranking scored 2.7/5 vs 3.9 for the exact route view; it is probabilistic (vetoed constraint), and retrains forever as Lean drifts. Kept only as a soft diagnostic.
2. **PageRank / centrality** (Phase 3 `LANDMARK_STRUCTURE_AND_RANKING.md`, `data/rankings.json`): global PageRank p@5 = 0.2 on proxy keys; the most-central constants are glue.
3. **Betweenness and community features**: order-sensitive under renaming (rank correlation 0.50 across runs); ablation showed *removing* community features raised AUC 0.677→0.691. Dead.
4. **Reuse/degree as importance** (`data/cones_results.json`, `data/moves_results.json` v1): ranking by citation count scores **0.0** at move identification — the most-used constants are `Eq.mpr`-glue. Inverted use (rarity) merely ties depth.
5. **Depth + size combinations** (`data/measures_results.json`, `data/cones_results.json`): depth, unfolded tree size, and ancestor-set size are one coordinate (Spearman ≥ 0.98); all combinations of them are dead ends, measured (combo AUC 0.640 vs 0.638 single).
6. **relDepth alone** (proof-digs-deeper-than-statement): AUC 0.56 as a machinery detector; useful only as a construction-vs-assertion axis.
7. **Name/namespace cuts** (`data/depth_mathonly.json`): improved one metric (route coverage 0.71→0.80) while silently severing `_private.*` real mathematics; also the paradigm of what the longevity constraint forbids. Rejected.
8. **Raw statement-mention exposure for tactic vocabulary** (`data/invariant_rank_results.json` R3): AUC **0.40** — worse than chance, because large tactic libraries state hundreds of internal lemmas. Reported as a negative result; the directional-seclusion refinement is designed but unproven, and the residue it targets is ~1% of rank-1 errors.
9. **Anywhere-in-term strategy detection** (`data/strategies_results.json`): contradiction precision 0.095, induction recall 0.0. Killed by measurement; replaced by root-grain (v2), which works for term-visible strategies and exposed the term/intent distinction for the rest.
10. **Spectral analysis of the raw dependency DAG**: provably degenerate (nilpotent adjacency, all eigenvalues zero). Not a missed idea — a mathematical fact. A symmetrized/statement-graph construction is queued with an explicit design question.
11. **Embeddings / GNNs / LLM scoring**: excluded by the program's constitution — results must be exact, certifiable, and stable across Lean versions; a learned scorer is none of these, and Phase 3's learned baseline (item 1) already demonstrated the review-quality gap.

## 5. Concessions, and why they do not sink the formulation

The defense does not claim:
1. **That ranking order matches human importance at scale.** Rank-1 genuineness is measured (90.3%); *keyness* is verified only on ~50 hand-read proofs and 20 ground-truth skeletons. This is an evaluation gap, not a design defect; the formulation is the instrument that makes the evaluation cheap to run.
2. **The shallow floor.** Near the axioms (depth ≲ 15) glue and content are structurally indistinguishable by any depth-family measure; rank-1 quality drops to 83%. This region is bounded, is arguably where "moves" barely exist (35% of theorems are interface-only; 407/2,355 correctly return "holds by definition"), and shrinks in relative weight as the library deepens.
3. **Perfect yardsticks.** Precision uses automated role labels (±3–4 points by hand audit); recall uses source citations (understates the true move set). Both biases are documented in-file; neither is directional in the formulation's favor in any way we could detect.
4. **Version-transfer, empirically.** The longevity argument is structural (§3), tested against automation pollution within one snapshot, but not yet against a second Mathlib version. This is the cheapest decisive experiment available and the defense welcomes it.

## 6. What the defense asks the court to recognize

1. The formulation meets its constitution: exact, name-free, model-free, purifying with depth.
2. Its measured performance (90/94.6 precision, ~97–99 recall) was reached not by tuning but by *removing* every non-kernel assumption; each improvement step is traceable to a principle, and each rejected alternative to a measurement.
3. Every known residue is named, bounded, and has either a designed next experiment (universality grain, seclusion, prominence-grain strategies, cross-version test) or an explicit reason to live with it (shallow floor).
4. The realistic alternative families — learned scoring, centrality, name heuristics — were all tried and lost on the same evidence used to certify the current model.
