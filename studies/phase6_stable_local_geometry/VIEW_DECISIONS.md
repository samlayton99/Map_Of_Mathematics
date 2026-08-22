# Map-view decisions (2026-08-21)

Two open rendering choices, decided on measurement. Substrate: the GAP edge
set (`data/map_final/edges_GAP.npz`, 1,060,755 edges), corrected phase5
arrays, areas from `all_modules.tsv` (second component of `Mathlib.*`, else
`Core`). All side files under `data/map_final/`.

1. **Corpus scoping: YES, scope.** It removes zero mathematics-to-mathematics
   edges (785,870 in both graphs, identical) while cutting meta-area
   destination mass 0.258 -> 0.069 and flipping the top-100 hub list from
   transport-majority to mathematics-majority (42 -> 49 mathematics).
2. **Vertical rendering: the FIXED rule**, `rho <= 1/2`. It cuts interface
   link share in the lateral view by 61% (2.79% -> 1.08%; the within-proof
   rule *raises* it to 3.80%) and lifts AMI 0.386 -> 0.416 and distance AUC
   0.627 -> 0.679, where the within-proof rule moves both the wrong way.

---

## Decision 1 — exclude non-mathematical SOURCES from the map?

`GAPM` = GAP restricted to edges whose SOURCE artifact's own module is
`Mathlib.*` and not `Mathlib.Tactic.*`. Cited targets are untouched.

### What scoping removes

| | GAP | GAPM | delta |
|---|---|---|---|
| edges | 1,060,755 | 844,638 | -216,117 (-20.4%) |
| source proofs | 425,895 | 320,024 | -105,871 (-24.9%) |
| distinct cited targets | 227,333 | 175,188 | -52,145 (-22.9%) |
| **math-area -> math-area edges** | **785,870** | **785,870** | **0** |

Dropped sources by home package: Init 35,706, Std 29,686, Lean 24,427,
`Mathlib.Tactic.*` 6,644, Batteries 3,801, Aesop 2,812, no-module 1,772,
rest <400 each. By area, source-edge loss is 100% of `Core` (201,593) and
100% of `Tactic` (14,524) and **exactly zero for every mathematics area**
(Algebra, Analysis, CategoryTheory, MeasureTheory, RingTheory, ... all 0.000).

### Emergent structure, GAP vs GAPM

| metric | GAP | GAPM |
|---|---|---|
| community-vs-area AMI (Louvain, full scale) | 0.3858 | 0.3661 |
| modularity | 0.8858 | 0.8686 |
| distance AUC (same vs cross area) | 0.6265 | **0.6308** |
| within-area edge share (all areas) | 0.7868 | 0.7442 |
| within-area share, math-area edges only | 0.7986 | **0.7986** |
| top-100 hub link mass | 0.1092 | 0.1117 |
| top-100 hubs that are mathematics | 42 / 100 | **49 / 100** |
| top-100 hubs that are transport | 53 / 100 | **45 / 100** |
| cross-area plumbing share | 0.3499 | 0.3327 |
| same-area plumbing share | 0.1556 | **0.0775** |
| edges landing in a meta area (Core/Tactic/...) | 0.2577 | **0.0694** |
| LCC share of active nodes | 0.960 | 0.958 |

Sources: `map_analysis_gap.json`, `map_analysis_gapm.json`,
`decision1_scoping.json`, `decision1_mathonly_within.json`.

**Verdict data.** Scoping does not change the emergent structure; it shrinks
the graph. The mathematics-to-mathematics subgraph is *bit-identical* —
785,870 edges in both, within-area share 0.7986 in both. Every metric move
in the table is accounted for by deleting the Core/Tactic block from the
node set, not by any change inside mathematics: AMI -0.020 and modularity
-0.017 are the cost of removing a large, tightly-clustered, machine-generated
Core community that Louvain scored well; AUC actually improves. What does
change is what a reader sees: destination mass landing in meta areas drops
0.258 -> 0.069, same-area plumbing halves 0.156 -> 0.078, and the top-100
hub list flips from transport-majority (53/100) to mathematics-majority
(49/100).

**Recommendation: SCOPE.** Exclude non-mathematical sources. It costs zero
mathematics edges and 0.02 AMI (a node-set artifact, not a structural loss),
and buys a 3.7x reduction in meta-area destination mass and a
transport-majority -> mathematics-majority top-100 hub list.

### Caveats

- The 52,145 cited targets that disappear are declarations *only ever cited
  by* Init/Std/Lean/Aesop/tactic proofs. They are unreachable in the scoped
  map, not merely demoted. If drill-down should be able to reach them, keep
  them as targets of a hidden layer rather than deleting the arrays.
- Module home is not the same as being mathematics. `Lean.Syntax.isOfKind`
  is still the 4th-largest hub of GAPM (3,007 in-links) because Mathlib's own
  `notation`/`macro` declarations live in `Mathlib.*` modules. A syntax-artifact
  filter is a separate axis from module scoping.
- 0.3% of GAPM source edges still sit in a `Core`-labelled area (module
  `Mathlib` with no second component). Harmless, but the area label is coarse.
- AMI/modularity are computed over different node sets in the two columns, so
  their difference is not a like-for-like comparison. The like-for-like
  measure is the math-only within-area share, which is unchanged.

---

## Decision 2 — which edges render LATERAL?

Long-span edges become vertical drill-down portals; the rest are the lateral
neighbour view. Two candidate rules, `span = d_src - d_dst`:

- **LATFIX** (fixed): `rho = span / (1 + d_src) <= 1/2`.
- **LATMED** (within-proof): `span <= median span of the source artifact's
  own admitted edges`. Constant-free.

### Head to head

| metric | GAP (all) | LATFIX | LATMED | GAPM (all) | LATFIX | LATMED |
|---|---|---|---|---|---|---|
| edges retained | 1,060,755 | 955,591 (90.1%) | 736,532 (69.4%) | 844,638 | 765,415 (90.6%) | 572,727 (67.8%) |
| dst = mathematics | 0.803 | **0.832** | 0.814 | 0.857 | **0.881** | 0.870 |
| dst = transport | 0.187 | **0.164** | 0.173 | 0.134 | **0.116** | 0.117 |
| dst = notation | 0.0097 | **0.0041** | 0.0133 | 0.0091 | **0.0033** | 0.0126 |
| **interface link mass** | 0.0279 | **0.0108** | 0.0380 | 0.0221 | **0.0073** | 0.0312 |
| top-100 hubs: mathematics | 42 | **48** | 43 | 49 | **55** | 53 |
| top-100 hubs: notation | 5 | **1** | 7 | 6 | **1** | 7 |
| top-100 hub link mass | 0.109 | 0.091 | 0.100 | 0.112 | 0.096 | 0.090 |
| within-area edge share | 0.787 | 0.815 | 0.820 | 0.744 | 0.780 | 0.781 |
| cross-area plumbing share | 0.350 | **0.295** | 0.408 | 0.333 | **0.275** | 0.389 |
| community AMI (Louvain, full) | 0.3858 | **0.4161** | 0.3824 | 0.3661 | **0.3991** | 0.3664 |
| modularity | 0.8858 | 0.9067 | 0.9285 | 0.8686 | 0.8873 | 0.9186 |
| distance AUC | 0.6265 | **0.6787** | 0.6112 | 0.6308 | **0.6696** | 0.6281 |
| LCC share of active nodes | 0.960 | 0.910 | 0.937 | 0.958 | 0.911 | 0.925 |

Interface link mass = share of lateral edges landing on the 13 observed
interface/transport names (`OfNat.ofNat`, `HAdd.hAdd`, `HMul.hMul`,
`DFunLike.coe`, `Membership.mem`, `HSMul.hSMul`, `HSub.hSub`, `rfl`,
`Eq.ndrec`, `of_eq_true`, `Iff.rfl`, `eq_self`, `Inhabited.default`).

### The metric that decides it: does the interface mass leave the lateral view?

Per-hub in-degree in the lateral view, GAP base:

| hub | GAP | LATFIX | LATMED |
|---|---|---|---|
| `rfl` | 9,900 | **1,495** | 9,876 |
| `OfNat.ofNat` | 6,285 | **3,411** | 6,166 |
| `DFunLike.coe` | 490 | **9** | 392 |
| `HAdd.hAdd` | 1,095 | **119** | 989 |
| `Inhabited.default` | 2,130 | **440** | 2,130 |
| `Membership.mem` | 863 | **130** | 792 |

LATFIX drops 65% of the interface links (29,575 -> 10,304) and cuts their
share of the lateral view by 61% (2.79% -> 1.08%). LATMED drops under 2% of
`rfl` and `OfNat.ofNat` and, because it deletes 30% of the graph elsewhere,
*raises* interface share to 3.80%. In the GAP top-25 lateral hub list,
`rfl` falls from rank 1 to rank 15 under LATFIX and stays rank 1 under
LATMED; `OfNat.ofNat` remains rank 2 under both but at 3,411 links vs 6,166.

### Why LATMED fails structurally

50.5% of GAP source artifacts cite exactly one thing (k=1). For those the
within-proof median *is* that edge's own span, so the rule is vacuous: it can
never mark anything vertical in a single-citation proof. That is 20.3% of all
edges, and 5,019 of the 9,900 `rfl` links — a lone drill-down to `rfl` is
exactly the case the rule cannot see (`decision2_k1_diagnostic.json`).

### What mathematics is LOST from the lateral view

| | LATFIX (GAPM) | LATMED (GAPM) |
|---|---|---|
| edges removed | 79,223 | 271,911 |
| of which dst = mathematics | 54,985 (69.4%) | 226,000 (83.1%) |
| median span of removed | 41 | 18 |
| removed with `rho <= 0.25` | **0** | **131,914** (48.5%) |
| removed with `span <= 5` | 2,754 | 48,966 |

LATFIX's removals are genuine drill-downs — 20 sampled math-destination
removals (`decision2_lateral.json -> rules.GAPM.LATFIX.removed_math_sample`)
are things like `IsSelfAdjoint.norm_eq_max_norm_posPart_negPart ->
Continuous.continuousOn` (191 -> 69), `Real.hasDerivAt_fourier -> HasDerivAt`
(256 -> 105), `ContMDiffMap.semigroup -> Function.Injective.semigroup`
(196 -> 7). The borderline cases sit at rho 0.53-0.67 from shallow sources,
e.g. `Preord.hom_inv_apply -> CategoryTheory.Iso.inv_hom_id_apply` (14 -> 6),
`Flag.ext -> SetLike.ext'` (11 -> 3) — arguably lateral, and they are the
whole false-vertical exposure.

LATMED's removals include the most lateral edges in the entire graph:
`Ordinal.left_le_veblenWith -> Ordinal.veblenWith_right_strictMono`
(92 -> 87, span 5), `CategoryTheory.ReflQuiv.forget.Faithful ->
CategoryTheory.ReflQuiv.forget` (35 -> 33, span 2),
`FiniteDimensional.of_rank_eq_zero -> Module.rank` (90 -> 82, span 8),
`Polynomial.monomial_natDegree_leadingCoeff_eq_self ->
Polynomial.monomial_zero_right` (99 -> 90, span 9). 48.5% of what it calls
vertical has rho <= 0.25. Its false-vertical rate is catastrophic by
construction: it always renders half of every proof as a portal, however
short the hop.

### Rule agreement (GAP base)

| | n | median span | median rho | dst math |
|---|---|---|---|---|
| both lateral | 667,078 | 1 | 0.047 | 0.857 |
| LATFIX only | 288,513 | 14 | 0.227 | 0.787 |
| LATMED only | 69,454 | 27 | 0.792 | 0.534 |
| neither | 35,710 | 56 | 0.584 | 0.726 |

The 69,454 edges LATMED calls lateral and LATFIX does not sit at median
rho 0.79 and are only 53% mathematics — they are the deep plumbing hops
LATMED admits because their source proof's other citations are deeper still.

**Recommendation: LATFIX** — `rho = (d_src - d_dst)/(1 + d_src) <= 1/2`.
It keeps 90% of the edges, cuts interface link mass 2.79% -> 1.08% (LATMED
raises it to 3.80%), lifts community AMI 0.386 -> 0.416 and distance AUC
0.627 -> 0.679 (LATMED moves both the wrong way: 0.382 and 0.611), and
removes zero edges with rho <= 0.25 (LATMED removes 131,914). LATFIX is the
only view measured in this study that improves AMI *and* AUC over the GAP
baseline simultaneously — the lateral view is a better map than the full
graph, which is what "long spans are portals, not neighbours" predicts.
This confirms the span-relative reading of the interface-vocabulary hubs
recorded in `INTERFACE_VOCAB_RESOLUTION.md` and settles the rule choice
left open there.

### Caveats

- LATFIX carries a constant (1/2). LATMED is constant-free, which is its only
  principled advantage and the reason it was worth testing. The constant is
  not fitted here — 1/2 is the relative-depth threshold already in the
  project's vocabulary (`INCLUSION_ROUND3.md`) — but it is a constant, and
  principle 2 exposure should be recorded. Sensitivity to the threshold was
  not swept.
- LATFIX leaves 45,879 GAP sources (10.8%; 32,137 = 10.0% under GAPM) with no
  lateral edge at all — those proofs are pure drill-down and vanish from the
  lateral view. LATMED, by construction, keeps every source represented. If
  "every proof must appear laterally" is a requirement, LATFIX needs a
  per-proof floor (e.g. always keep the proof's minimum-span edge), which
  would be a third rule, untested here.
- Modularity rises for both lateral graphs mostly because they are sparser;
  AMI and AUC are the guard metrics and only LATFIX improves them.
- LATFIX fragments the graph slightly more than LATMED (LCC 0.910 vs 0.937 of
  active nodes on GAP). The vertical channel is what reconnects those pieces,
  so this is a cost only if portals are not rendered.
- `span` is value-depth difference from `nodes.npz` / `traversal_geometry.npz`;
  it is negative for 0.09% of edges (deeper target than source), which both
  rules treat as maximally lateral.
- The lateral/vertical split is a rendering choice, not an edge-admission
  choice. Both rules partition GAP; nothing is deleted from the map, only
  moved to the portal channel.

---

## Files

| file | contents |
|---|---|
| `data/map_final/edges_GAPM.npz` | Decision 1 scoped edge set |
| `data/map_final/edges_{LATFIX,LATMED}_{GAP,GAPM}.npz` | Decision 2 lateral subgraphs |
| `data/map_final/decision1_scoping.json` | removal accounting, per-area loss |
| `data/map_final/decision1_mathonly_within.json` | math-only within-area check |
| `data/map_final/map_analysis_gapm.json` | full map_analysis on GAPM |
| `data/map_final/map_analysis_lateral.json` | full map_analysis on the 4 lateral sets |
| `data/map_final/decision2_lateral.json` | per-rule tables + removed-math samples |
| `data/map_final/decision2_disagreement.json` | rule agreement, interface mass |
| `data/map_final/decision2_k1_diagnostic.json` | k=1 vacuity of the within-proof rule |
| `src/{scope_gapm,lateral_rules,lateral_disagree,run_gapm_analysis}.py` | producers |

`src/map_graph.py` and `src/map_analysis.py` were not modified; the analyses
ran through `run_gapm_analysis.py`, which sets `MAPGRAPH_OUT_DIR` to a scratch
directory and assigns `map_analysis.EDGE_SETS` before `main()`. Existing
`map_analysis*.json` files were not clobbered.
