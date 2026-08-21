# P0: Exact depth + statement-world audit

Date 2026-08-21. Node ids throughout = `data/names.json` order (771,129 constants).

## Exact depth (SCC condensation)

New `src/depth_scc.py` -> `data/depth_scc.npz`: `depth_exact`, `scc_id`, `scc_size` (citation graph = value deps, fallback to type deps, self-loops removed; 18,900,271 edges) and `depth_stmt`, `scc_id_stmt`, `scc_size_stmt` (type deps only; 10,915,861 edges). Method: scipy strong connected_components, then longest path on the condensation DAG (vectorized Kahn).

- Nontrivial SCCs: 542 nodes in 167 components (96 of size 2; largest 20). Every one is a Lean-internal `_unsafe_rec` mutual-recursion cluster (Lean.Meta.Sym.Canon, Grind mkCongrProof, delaborator TopDownAnalyze, do-elab, Doc.Parser, ...). No mathematics sits in a cycle.
- Correction vs old 3-pass relaxation (`nodes.npz depth`): **356 nodes change (0.046%)**, all increases, range +1..+143 (median +12, mean +29); 316 are SCC members, 40 sit downstream of cycles. **Max depth unchanged: 346.**
- `depth_stmt`: the type-dep graph is a DAG (0 nontrivial SCCs), max depth 13, mean 3.17.

Verdict: the old depth was near-correct globally (junk-recursion cycles only), but SCC members were badly wrong locally (up to 143 levels).

## in_stmt_world audit

Current `build_incidence.py` seeds from the theorem's t-deps but propagates along the value-fallback-type graph for every node -> the statement closure DOES traverse other theorems' proof bodies. Requirement violated.

Sample: 1000 random artifacts (seed 20260821), 26,699 incidences.

- Sanity: exact BFS of the current rule reproduces stored flags perfectly (0/26,699 mismatches).
- Corrected rule (theorems contribute statement deps only; non-theorems contribute type + body deps): **2,544 flips (9.53% of incidences)** — 2,539 in-world -> out, 5 out -> in; 395/1000 artifacts affected. Sample in-world rate drops 75.2% -> 65.7% (global stored rate 75.9%).
- Flips concentrate on proof plumbing: congrArg (159), Eq.mpr (87), id (61), propext (43), Eq.refl, of_eq_true, Eq.symm, ... The old flag inflated statement-world membership exactly on rewriting machinery.

## Changes to src/build_incidence.py (patched, NOT re-run)

1. Depth: Kahn + 3-pass relaxation replaced by shared `depth_scc.scc_depth` (exact). Output schema unchanged.
2. Statement-world closure graph: `t-deps for all nodes + v-deps for non-theorems`; propagation order = SCC condensation, users-first, per-SCC fixpoint (also closes an old ordering gap where marks entering a cycle could stop propagating; never observed in sample).

Verification: patched lane-propagation logic run in isolation on 128 random artifacts equals a reference BFS on all 771k node flags per artifact — 0 mismatches (scratchpad `test_lane_prop.py`).

Note for rebuild: with the corrected rule, expect global in_stmt_world to drop by roughly 10 points; `depth` field becomes `depth_exact`.
