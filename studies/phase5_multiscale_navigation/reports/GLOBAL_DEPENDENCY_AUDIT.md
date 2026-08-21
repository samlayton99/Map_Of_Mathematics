# Global-dependency audit: which signals shift the ground

**Requirement.** Adding a declaration at the edge must never change the score,
rank, or displayed position of anything that already existed. A signal is
APPEND-SAFE only if its value for an existing declaration is a function of that
declaration and things beneath it in the dependency graph — never of the
library's size, of how many things cite it, or of any max/mean/sum/quantile
taken over the corpus.

Verdicts are **reasoned first, then measured**. Where the two disagree it is
flagged explicitly.

---

## 0. Method

The dump `mathlib_deps7.jsonl` (771,129 declarations) was reparsed and every
array of `data/*.npz` was rebuilt from scratch. The reimplementation reproduces
**every shipped array bit-for-bit** — `node_depth`, `node_in_degree`,
`node_stated`, `node_kind`, `art_certifies`, `inc_artifact`, `inc_decl`,
`inc_roles`, `inc_load_bearing`, `inc_d_target`, `inc_d_cite`,
`inc_delta_depth`, `decl_is_claim`, `decl_logic_only`, `decl_tainted`,
`apparatus`, `machinery` — so the measurements below are of the apparatus, not
of a lookalike.

Two growth scenarios. In each, a **past library** `L0` is a downward-closed
sub-library (closed under both value and type dependencies, so every present
declaration keeps its complete dependency record); the **present library** `L1`
is all of Mathlib. Every signal is compared on declarations / incidences present
in both. Append-safe means **bit-identical**.

| scenario | past library `L0` | decls | artifacts | incidences | interpretation |
|---|---|---|---|---|---|
| **A** `random70` | closure of a random 70% of artifacts | 698,147 (90.5%) | 674,919 | 17,204,624 | growth lands anywhere |
| **B** `depth<=60` | closure of every declaration at depth ≤ 60 | 523,702 (67.9%) | 501,728 | 9,274,595 | growth lands strictly above a frozen foundation |

For every artifact present in `L0`, its candidate set is identical in `L0` and
`L1` (closure guarantees it), so within-proof rank comparison is exact.

Two properties of the scenarios that matter for reading the numbers:

- Scenario A's random subset **retained the deepest declaration**: `dmax` = 346
  in both libraries, so every `dmax`-dependent signal measures as safe there.
  Scenario B has `dmax` = 338 vs 346 and exposes it.
- Scenario B's closure is not purely shallow — closing under *type* dependencies
  pulls in some deep declarations (`L0` reaches depth 338) — but every artifact
  with target depth ≤ 50 is present, which is precisely the precondition
  `IDF50` needs.

Harness: `scratchpad/audit/{parse_dump,recompute,validate_full,append_test,derived_test}.py`.

---

## 1. Per-incidence signals (`inc_*`)

| signal | verdict | reasoning | scenario A | scenario B |
|---|---|---|---|---|
| `inc_artifact` | APPEND-SAFE (value) / CONDITIONAL (id) | identity of the proof; but the integer is a position in a file-order array — see §8 | — | — |
| `inc_decl` | APPEND-SAFE (value) / CONDITIONAL (id) | same | — | — |
| `inc_roles` | **APPEND-SAFE** | occurrence counts inside an already-elaborated proof term; immutable | 0 / 17,204,624 | 0 / 9,274,595 |
| `inc_load_bearing` | **APPEND-SAFE** | `roles[:, (0,1,2,7)].sum() > 0`, fixed threshold on an immutable array | 0 | 0 |
| `inc_in_stmt_world` | **APPEND-SAFE** | reverse reachability from the target's own statement refs, downward only; the reach set of a present declaration cannot acquire members | 0 / 400 artifacts (exact reach-set equality) | 0 / 400 |
| `inc_d_target` | **APPEND-SAFE** | `depth[target]`; see §2 | 0 | 0 |
| `inc_d_cite` | **APPEND-SAFE** | `depth[cited]` | 0 | 0 |
| `inc_delta_depth` | **APPEND-SAFE** | difference of two safe depths | 0 | 0 |
| `inc_is_definition` / `inc_is_theorem` | **APPEND-SAFE** | kernel declaration kind, immutable | 0 | 0 |
| `inc_strongest_role` | **APPEND-SAFE** | `argmax` over an immutable row | — | — |
| `inc_machinery` | **VIOLATES** | `decl_tainted` ∘ `apparatus`, whose test is `nproof > 200` and `nproof > 20·(inherited+1)` — both library-wide counts — combined with `univ[k] < 0.02`, a library-wide frequency | 1,485 (0.009%) | 17,934 (0.193%) |
| `inc_glue` | **VIOLATES** | `decl_logic_only[decl] \| inc_machinery`; both terms violate | 8,296 (0.048%) | 157,185 (1.695%) |

---

## 2. Per-declaration signals (`node_*`, `decl_*`)

| signal | verdict | reasoning | scenario A | scenario B |
|---|---|---|---|---|
| `node_kind`, `node_gen`, `pr`, `ps`, `ar` | **APPEND-SAFE** | kernel attributes of the declaration itself | 0 | 0 |
| `node_depth` | **APPEND-SAFE** (see caveat) | `build_incidence.py` computes `depth[i] = 1 + max(depth[d] for d in deps[i])` over a Kahn topological order. No normaliser, no clamp, no global term. Verified by reading the implementation, not assumed. | **0 / 698,147** | **0 / 523,702** |
| `node_in_degree` | **VIOLATES** | count of citers; every new citer increments it | 115,634 (16.56%) | 149,985 (28.64%) |
| `node_stated` | **VIOLATES** | count of human theorem statements that mention the declaration | 34,049 (4.88%) | 25,279 (4.83%) |
| `decl_is_claim` | **APPEND-SAFE** | `pr & kind ∉ {constructor, recursor}`; both immutable | 0 | 0 |
| `decl_logic_only` | **VIOLATES** | `all(bare[k] for k in nonuniv(c))`; `nonuniv` filters ingredients by `univ[k] < 0.02` where `univ = nstmt / n_human_theorems`. Both terms move with the library, so the *ingredient set of an existing declaration silently changes*. | 233 (0.033%) | 2,864 (0.547%) |
| `decl_tainted` | **VIOLATES** | `any(apparatus[k] for k in nonuniv(c))` | 39 (0.006%) | 5,873 (1.121%) |
| `apparatus` (V8) | **VIOLATES** | `nproof > FLOOR(200)` and `nproof > LAMBDA(20)·(inherited+1)` and `univ < THETA(0.02)` — three library-wide counts and one library-wide frequency | 6 decls | 48 decls |
| `decl_popularity` | **VIOLATES** | citation count over the whole record | 115,634 (16.56%) | 149,985 (28.64%) |
| `decl_idf` | **VIOLATES** | `log(n_artifacts / popularity)`; **both** terms move, so it changes for *every* declaration on *every* append | **698,147 (100%)** | **523,702 (100%)** |
| `IDF50` "frozen rarity" (`src/mine_failures.py`) | **CONDITIONAL** | code comment says *"append-safe by construction"*. It is not, in general: the stratum `d_target ≤ 50` is re-derived from the live library each run, so `n50` and `pop50` move whenever a new artifact lands in the band. It **is** exactly safe when every addition has depth > 50. | **698,147 (100%)** | **0 (0%)** |
| V8 internals `univ`, `nproof`, `inherited`, `nstmt` | **VIOLATES** | all counts / count ratios over the whole library | 9.63% / 3.54% / 6.40% | 10.04% / 4.71% / 6.66% |
| `bare` (V8 internal) | **APPEND-SAFE** | `is_concept & ps & (ar == 0)` | 0 | 0 |

### `node_depth`: the implementation was checked, not assumed

`src/build_incidence.py:83-92`:

```python
depth = np.zeros(n, dtype=np.int32)
for i in order:                       # Kahn topological order
    if deps[i]:
        depth[i] = 1 + max(depth[d] for d in deps[i])
cyc = set(range(n)) - set(order)      # 543 declarations in dependency cycles
for _ in range(3):
    for i in cyc:
        ds = [depth[d] for d in deps[i] if d not in cyc]
        if ds:
            depth[i] = 1 + max(ds)
```

No `max()` over the corpus, no normaliser, no clamp. `deps[i]` is the
declaration's own value dependencies (falling back to its type dependencies),
so `depth[i]` reads only downward. It is saved as `int32` at full precision;
`inc_d_cite` / `inc_d_target` are cast to `int16`, which is lossless while
`max depth = 346` and will stay so for any plausible library.

One residual, stated: the cycle-relaxation loop iterates a Python `set` for a
fixed 3 rounds, so its result is in principle iteration-order dependent, and set
iteration order depends on set *content*. Measured: 543 cyclic declarations in
`L1`, 517 in `L0`(A), 289 in `L0`(B), and **every shared declaration's depth was
identical in both scenarios**. Stable in practice; not guaranteed by
construction. Replacing the 3 fixed rounds with iterate-to-fixpoint over a
sorted list would make it a guarantee.

**Reasoning-vs-measurement disagreements found: three.** These are the most
valuable results here.

1. **Code asserts a false safety.** `src/mine_failures.py:86` annotates `IDF50`
   `# frozen-foundation rarity: append-safe by construction`, and line 163
   emits `"append_safe": "rarity_live" not in METHODS[method]`, which marks
   **M1 and M2 as append-safe** in the failure-bank JSON. Measured: `IDF50`
   changes for **100% of shared declarations** under general growth, moving M1's
   top item in 0.704% of proofs; M2 moves in 0.350% of proofs under edge growth.
   Both flags are wrong.
2. **A report asserts a false safety.** `reports/APPEND_SAFETY.md` §1 lists only
   `rarity/idf`, `in-degree` and `popularity` as violating and promotes
   `role x depth` as append-safe (§5, "viable contenders"). It reads
   `dmax = node_depth.max()`. §4 measures it moving.
3. **Measurement asserts a false safety — the dangerous direction.** In
   scenario A, `M2_role_x_depth` measured **exactly 0 changes**, because the
   random 70% subset happened to retain the deepest declaration (`dmax` = 346 in
   both libraries). A growth simulation that does not perturb the argmax cannot
   see a `max()`-normaliser violation at all. Any empirical append-safety test
   must include a scenario that removes the extremum; a "we simulated growth and
   nothing moved" result is not evidence of safety for this class of bug. This
   is presumably why `dmax` survived undetected for months.

---

## 3. Universes

| universe | verdict | reasoning | measurement |
|---|---|---|---|
| `U0` = `inc_target != inc_decl` | **APPEND-SAFE** | pure identity test | shared artifacts had identical candidate sets in both scenarios |
| `U1` = `load_bearing & no_self` | **APPEND-SAFE** | both terms safe | identical |
| `U1D` = `(load_bearing \| is_definition) & no_self` | **APPEND-SAFE** | both terms safe | identical |

Membership never changes. Note that the *number* of candidates in a universe
grows, which is what breaks every quantity normalised by it (§5, §6).

---

## 4. Rankings

Top-1 change = proofs whose displayed rank-1 item is different. This is the
number that matters: it is what the map shows.

| ranking | verdict | offending term | A: ranks moved | A: top-1 changed | B: ranks moved | B: top-1 changed |
|---|---|---|---|---|---|---|
| `R_introduced_depth` | **APPEND-SAFE** | — | 0 | **0.000%** | 0 | **0.000%** |
| `R_depth` | **APPEND-SAFE** | — | 0 | **0.000%** | 0 | **0.000%** |
| `B1_reverse_depth` | **APPEND-SAFE** | — | 0 | 0.000% | 0 | 0.000% |
| `B3_term_order` | **CONDITIONAL** | `base.astype(float)` — an incidence array index. *Within* a proof this is first-occurrence order in the proof term, which is stable; as a global score it is an array position that shifts on any insertion (§8). | not measured | — | — | — |
| `O_source` | **APPEND-SAFE** | ground truth is elaborator provenance + `inc_d_cite`; the cache is keyed by `n_incidences` and merely rebuilds | — | — | — | — |
| `M2_role_x_depth` | **VIOLATES** | `dmax = node_depth.max()` | 0 | 0.000% | 61,366 | **0.350%** |
| `R_v8_faithful` | **VIOLATES** | `inc_glue` | 96,870 | 0.092% | 1,058,482 | 0.809% |
| `R_v8_all_kinds` | **VIOLATES** | `inc_glue` | 175,424 | 0.103% | 1,428,894 | 1.088% |
| `B2_popularity` | **VIOLATES** | `decl_popularity` | 1,573,955 | 0.201% | 3,949,654 | **11.976%** |
| `M1_role_x_frozen_rarity` | **CONDITIONAL** | `IDF50` | 1,994,975 | **0.704%** | 0 | **0.000%** |
| `R_phase5_composite` / `M3_promoted_composite` | **VIOLATES** | `decl_idf` **and** `dmax` | 1,488,807 | **0.640%** | 3,731,743 | **2.185%** |
| `B0_random` | **VIOLATES** | `rng.random(len(base))` — the value assigned to a candidate is its *position* in `base`, so inserting one incidence anywhere re-draws every subsequent candidate's key | analytic | — | — | — |

**`dmax` is a step-function violation.** In scenario A the deepest declaration
survived (`dmax` = 346 in both libraries), so `M2_role_x_depth` measured as
identical — the bug is invisible until something deeper than everything else is
added. In scenario B `dmax` moved 338 → 346 (a 2.4% rescale) and immediately
reordered 61,366 candidates and changed the headline item in 1,757 proofs.
A single new record-depth declaration rescales the entire library at once.

---

## 5. Inclusion policies

| policy | verdict | reasoning |
|---|---|---|
| `top_k` | **APPEND-SAFE** | `ranks < k` on an append-safe rank |
| `top_pct` | **APPEND-SAFE** | `sizes` is `bincount` **per artifact**; an artifact's candidate count is fixed |
| `kind_lane` | **APPEND-SAFE** | declaration kind |
| `role_lane` | **APPEND-SAFE** | occurrence roles |
| `introduced_only` | **APPEND-SAFE** | `inc_in_stmt_world` |
| `cited_depth_band` / `target_depth_band` | **APPEND-SAFE** | fixed integer thresholds on depth |
| `all` | **APPEND-SAFE** | constant |
| `cluster_split[tie_first, tie_two, tie_first_capped]` | **APPEND-SAFE**, conditional on the ranking | these read only *equality* of the level scalar within a proof; level re-indexing preserves equality. `tie_two` is `DEFAULT_METHOD`. |
| `cluster_split[max_gap, max_gap_half, max_gap_rel, otsu, kneedle, curvature]` | **VIOLATES** | they read *differences* of `s = level / (n_levels - 1)`, and `n_levels` is the count of distinct key tuples over the whole universe |
| `global_quantile` | **VIOLATES** | `np.quantile(score, 1 - q)` over the corpus, on top of a `global_score` that is itself a corpus-wide rank |

---

## 6. Derived and displayed quantities

These are not rankings, but three of them are literally *the displayed position*.

| quantity | where | verdict | reasoning | measurement |
|---|---|---|---|---|
| `RankingSpec.global_score` | `rankings.py:53` | **VIOLATES** | `-rank` of the item in a lexsort over the whole `base`. Every insertion anywhere in the order shifts every item below it. Feeds `global_quantile`. | analytic; guaranteed to move |
| `score_pct` | `src/vibe_scores.py`, shown as a column in the viewer | **VIOLATES** | `tie_block_start / (len(base) - 1)`. Corpus-size denominator. | **100% of candidates, even for append-safe rankings** |
| `cluster_split` scalar `s` | `cluster_split.py:110` | **VIOLATES** for continuous-key rankings, safe for coarse ones | `level / (n_levels - 1)`; `n_levels` counts distinct key tuples corpus-wide | 99.4% for `R_phase5_composite`, 0% for `R_depth` |
| backbone weight `w` | `src/backbone.py:101-106` | **VIOLATES** | contains `idf` (live) **and** `dmax` | — |
| filtration `z` | `src/backbone.py:142-149` | **VIOLATES** | configuration-null: `p = s_out[u]·s_in[v] / W²` with `W = total edge weight of the library` and `s_in/s_out` per-node library totals. Every term is a corpus-wide sum. | see below |
| filtration `rank`, `in_backbone` | `data/filtration.npz` | **VIOLATES** | global `argsort(-z)`; `in_backbone` is per-proof argmax of `w` | — |
| backbone filter threshold | `src/backbone.py:206` | **VIOLATES** | `np.percentile(z, 75)` | — |
| bipartite PageRank | `src/persistence.py:28` | **VIOLATES** | a global eigenvector; every node's score depends on the whole graph | — |
| `cited_by_count` / P4 rank | `src/geometry.py:117-125` | **VIOLATES** | corpus-wide citation counts and a global `argsort` | — |
| `ViewLaneHidesOfUniverse` | `dashboard_export.py:415` | **VIOLATES** | `1 - lane_mask.mean()` over the corpus | — |

### Measured (scenario A, over each library's **full** U1D — 16,609,418 vs 18,081,920 candidates)

| ranking | distinct key levels L0 / L1 | `cluster_split` scalar `s` changed | `score_pct` changed | max shift in `score_pct` |
|---|---|---|---|---|
| `R_depth` | 346 / 346 | 0 (0.000%) | **16,609,417 (100%)** | 0.26 pp |
| `R_introduced_depth` | 684 / 684 | 0 (0.000%) | **16,609,417 (100%)** | 0.15 pp |
| `R_phase5_composite` | 70,271 / 72,963 | **16,508,703 (99.394%)** | **16,609,417 (100%)** | 3.33 pp |

**This is the sharpest result in the audit.** `R_depth` and
`R_introduced_depth` are append-safe rankings — 0 rank changes, 0 top-1 changes
— and their **displayed** `score_pct` still moves for 100% of candidates, purely
because the denominator is the size of the library. An append-safe ranking
behind a corpus-normalised display is not append-safe to the user.

`cluster_split`'s scalar is safe only because `R_depth` and
`R_introduced_depth` have key spaces bounded by the depth range, which happened
not to change; a continuous key (`R_phase5_composite`) moves 99.4% of it.

### Filtration (`data/filtration.npz`, 8,485,349 edges; 7,817,343 shared)

| quantity | changed | magnitude |
|---|---|---|
| configuration-null `z` | **7,817,343 / 7,817,343 (100%)** | max &#124;Δz&#124; = 1876.7 |
| position in the global filtration order | 7,817,341 / 7,817,343 | max shift 6.81 pp |

Every edge of the shipped multiscale map moves when the library grows. Nothing
in the filtration survives.

---

## 7. Metrics

None of these is a per-declaration position, so none "shifts the ground" in the
strict sense — but every one of them changes when the library grows, so **no
metric in this apparatus is comparable across two library versions**, and two
of them additionally propagate a violating signal down to the item level.

| metric | verdict | note |
|---|---|---|
| `structural_category` (`composition.py:47`) | **VIOLATES at item level** | reads `decl_logic_only` and `inc_machinery`; the category of an existing candidate flips as the library grows. Feeds `rank_composition`, `RoleGlueAt1`, `ViewComposition`, `bridge_enrichment`. |
| `gradient_quality` (`navigation.py:171`) | **VIOLATES at item level** | assigns each labelled candidate to an equal-mass bin of the **global** order; the bin an item lands in is corpus-dependent |
| `Source*`, `Role*`, `Coverage*`, `Semantic*`, `Navigation*` | corpus/label-set aggregate | means over a growing population |
| `Graph*` (`metrics.py:133`) | corpus aggregate | components, giant fraction, entropy, susceptibility over the whole projection |
| `bridge_enrichment` | corpus aggregate | plus the `structural_category` item-level defect above |
| `tie_stats` (`runner.py:56`) | corpus aggregate | samples 200k of `base` by position |
| `View*` | display aggregate | by design |
| `krippendorff_alpha`, `rater_agreement`, `_wilson` | **APPEND-SAFE** | functions of the label set only |

---

## 8. The identifier hazard (separate from scoring)

`build_incidence.py:nid` assigns declaration ids in **dump line order**, first
appearance wins. A declaration inserted anywhere but the end of the dump shifts
every subsequent id, and artifact ids (`art_certifies` = ordered list of
declarations with a body) shift with them.

This changes no *value* of any append-safe signal — those are functions of the
declaration, not of its index — but it invalidates every persisted integer
reference:

- `review/labels/keymap.json` and `review/sealed_r1/keymap.json` store raw
  `_incidence` positions. After a rebuild these point at different citations,
  silently.
- `B0_random` and `tie_stats`/`plugins.verify` sampling are position-indexed.
- `data/filtration.npz` edge arrays are index-based.

Fix: key persisted references by declaration *name* (or a content hash), never
by array position, and re-resolve at load.

---

## 9. Violations ranked by how much they actually move rankings

Ordered by how much of the shipped product actually moves.

| # | violation | measured movement | already known? |
|---|---|---|---|
| 1 | **filtration `z` / backbone weight `w` / `rank` / `in_backbone`** (`src/backbone.py`, `data/filtration.npz`, `reports/NAVIGABLE_FILTRATION_REPORT.md`) — the phase's multiscale-navigation deliverable | **100% of 7.8M edges**; position in the filtration order shifts up to 6.81 pp | **NO** |
| 2 | **`score_pct` / `global_score` / `global_quantile`** | **100% of candidates**, *even for rankings that are themselves append-safe* | **NO** |
| 3 | `decl_idf` → `R_phase5_composite` / `M3_promoted_composite` | top-1 changes in **2.185%** of proofs (B), 0.640% (A) | yes |
| 4 | `decl_popularity` → `B2_popularity` | top-1 changes in **11.976%** of proofs (B) — largest single number, but a baseline only | yes |
| 5 | `inc_glue` (`decl_logic_only` + `inc_machinery` + `apparatus` + `univ`) → `R_v8_faithful`, `R_v8_all_kinds`, `structural_category`, `RoleGlueAt1` | top-1 changes in 1.088% of proofs (B), 0.103% (A) | **NO** |
| 6 | `IDF50` → `M1_role_x_frozen_rarity` | top-1 changes in 0.704% of proofs (A), 0% (B) | **NO** — actively mislabelled append-safe in code |
| 7 | `dmax` → `M2_role_x_depth`, `R_phase5_composite` | top-1 changes in 0.350% of proofs (B), 0% (A) — dormant until a record-depth append, then global | yes |
| 8 | `cluster_split` `max_gap` / `max_gap_half` / `max_gap_rel` / `otsu` / `kneedle` / `curvature` | 99.4% of the scalar they read, for a continuous-key ranking | **NO** |
| 9 | `node_in_degree` | 16.6% / 28.6% of declarations; no registered ranking uses it, but it defines the sealed stratum `S4_single_user` | yes |
| 10 | `node_stated` → V8 `univ` | 4.9% / 4.8% of declarations | **NO** |
| 11 | bipartite PageRank (`src/persistence.py`), `cited_by_count` + global `argsort` (`src/geometry.py`) | analysis reports only | **NO** |
| 12 | `gradient_quality` equal-mass global bins, `structural_category` inside metrics | reported numbers, not displayed ranks | **NO** |
| 13 | `B0_random` | baseline only | **NO** |
| 14 | array-index identity (§8) | breaks persisted `keymap` references, not scores | **NO** |

---

## 10. Substitutes

| violating signal | append-safe substitute |
|---|---|
| `decl_idf`, `decl_popularity` | **None exists that preserves the meaning.** Rarity is a statement about the rest of the library. `IDF50` is the closest and is safe only under a *pinned-foundation policy*: freeze the counts to the library at version V and never recompute them. That is a policy, not a property — state it as such, store the frozen vector as data, and version it. |
| `node_in_degree` | none; it is by definition a count of things above |
| `dmax` in `m_depth` | drop the normaliser. `m_depth = 0.20 + 0.80 · min(d_cite / D, 1)` with **D a declared constant** (e.g. 350), or use raw `d_cite` as a lexicographic key — `R_depth` and `R_introduced_depth` already do exactly that and measured at 0.000%. |
| `node_stated`, V8 `univ` (`< 0.02`) | replace the frequency test with a structural one: an ingredient is "universal" if it lies below a declared foundation set (a pinned list of declarations), not if it appears in more than 2% of statements. |
| V8 `apparatus` (`nproof > 200`, `> 20·(inherited+1)`) | none preserving the definition — it is *defined* as a usage count. Freeze the flag as data at version V and treat it as a fixed label, exactly as ADR-0005 already claims ("V8 is FROZEN") — the code currently recomputes it from the live library, which contradicts that. |
| `decl_logic_only`, `decl_tainted`, `inc_machinery`, `inc_glue` | follow whatever fix is chosen for `univ`/`apparatus`; the structural half (`bare = is_concept & ps & ar==0`) is already append-safe, so a `logic_only` defined as *all* type-ingredients bare (no `univ` filter) would be safe. Measure the cost before adopting. |
| `global_score`, `score_pct`, `global_quantile` | no cross-proof scalar can be corpus-independent while being a *rank*. Publish the raw key tuple instead (e.g. the depth integer and the role class), or normalise by a declared constant. The dashboard already warns that cross-proof comparability was never validated; the append-safety failure is a second, independent reason to drop the control. |
| `cluster_split` gap/otsu/kneedle/curvature | `tie_two` (the default) and the other `tie_*` methods are already safe. `reports/CLUSTER_SPLIT.md` already finds the varying methods worse than fixed top-k, so nothing is lost by removing them. |
| filtration `z` (configuration null) | none — a null model is by construction a statement about the whole graph. If the filtration must be append-safe, order edges by an append-safe per-edge quantity (`d_cite`, role class) rather than by a global-null surprise score. |
| PageRank | none |
| `B0_random` | seed the RNG per candidate identity (hash of `(target_name, cited_name)`) rather than per array position |

---

## 11. Bottom line

Exactly **two registered candidate rankings are append-safe as written**:
`R_depth` and `R_introduced_depth`, both measured at 0 rank changes and 0
top-1 changes across 16.6M and 9.0M shared candidates. Everything else in the
registry moves.

The two code sites that currently *assert* append-safety —
`src/mine_failures.py:86,163` and `reports/APPEND_SAFETY.md` §1/§5 — are both
wrong: they clear `M1` (via `IDF50`) and `M2` (via `dmax`), and both were
measured moving here.
