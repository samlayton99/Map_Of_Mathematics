#!/usr/bin/env python3
"""Q3.4: is component structure real, or would any ranking produce it?

The claim under test (mine, previously stated with more confidence than the
evidence carried): sparse top-1 components group proofs by TECHNIQUE rather
than by SUBJECT.

That claim has two halves and they need different tests.

  (i)  components are NOT subject-coherent. Testable against controls: compare
       the module purity of real components against size-matched random node
       sets and against a shuffled-ranking control.
  (ii) components ARE technique-coherent. The honest operationalisation: every
       component of a one-edge-per-proof graph is a tree flowing to one sink,
       so "shared technique" means the sink is a genuine technique rather than
       an arbitrary endpoint. Measured by what the sinks ARE: their depth,
       their library-wide usage, and whether they are glue.

CONTROLS
  C-random-nodes  size-matched random node sets (the null for "how coherent
                  would any group of this size be?")
  C-depth-matched size- and depth-matched random node sets
  C-shuffled      re-rank each proof's citations uniformly at random, rebuild
                  the graph, recompute component purity. This is the strongest
                  control: it holds the hypergraph fixed and destroys only the
                  ranking.
"""
import json, os
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
SEED = 20260820


def mod2(nm):
    p = nm.split(".")
    if p[0] == "_private":
        p = p[3:] if len(p) > 3 else p
    return ".".join(p[:2]) if len(p) >= 2 else p[0]


def build_top1(bi, a_col, keys, tgt, d_col, n):
    order = np.lexsort(tuple(reversed(keys)) + (a_col[bi],))
    s = bi[order]
    aa = a_col[s]
    new = np.empty(len(s), bool); new[0] = True; new[1:] = aa[1:] != aa[:-1]
    top = s[new]
    g = sp.coo_matrix((np.ones(len(top), np.int8), (tgt[top], d_col[top])),
                      shape=(n, n))
    _, lab = connected_components(g, directed=False)
    touched = np.unique(np.concatenate([tgt[top], d_col[top]]))
    return lab, touched, top


def purity_stats(lab, touched, names, min_size=5, nsamp=400, rng=None):
    sizes = np.bincount(lab[touched])
    live = [c for c in np.unique(lab[touched]) if sizes[c] >= min_size]
    if not live:
        return None, []
    pick = rng.choice(live, size=min(nsamp, len(live)), replace=False)
    pur, comps = [], []
    for c in pick:
        nd = touched[lab[touched] == c]
        cnt = Counter(mod2(names[i]) for i in nd)
        pur.append(cnt.most_common(1)[0][1] / len(nd))
        comps.append(nd)
    return np.array(pur), comps


def main():
    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    nodes = np.load(os.path.join(DATA, "nodes.npz"))
    v8 = np.load(os.path.join(DATA, "v8_mask.npz"))
    names = json.load(open(os.path.join(DATA, "names.json")))

    a_col = inc["artifact"].astype(np.int64)
    d_col = inc["decl"].astype(np.int64)
    lb = inc["load_bearing"]
    in_sw = inc["in_stmt_world"]
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"].astype(np.float64)
    kind = nodes["kind"]
    n = len(depth)
    tgt = certifies[a_col]
    logic_only = v8["decl_logic_only"]
    machinery = v8["machinery"]
    is_claim = v8["decl_is_claim"]

    bi = np.where(lb & (tgt != d_col))[0]
    demote = logic_only[d_col[bi]] | machinery[bi]
    not_new = in_sw[bi]
    dep = depth[d_col[bi]]
    rng = np.random.default_rng(SEED)

    # REAL: R4 introduced+depth (the suite's leading ranking)
    lab, touched, top = build_top1(bi, a_col, (not_new.astype(np.int8), -dep),
                                   tgt, d_col, n)
    sizes = np.bincount(lab[touched])
    nlive = len([c for c in np.unique(lab[touched]) if sizes[c] > 0])
    print(f"REAL top-1 graph: {len(touched):,} nodes, {nlive:,} components",
          flush=True)
    pur_real, comps_real = purity_stats(lab, touched, names, rng=rng)
    print(f"  module purity (components of size>=5, n={len(pur_real)}): "
          f"mean={pur_real.mean():.3f} median={np.median(pur_real):.3f}", flush=True)

    # CONTROL: shuffled ranking, same hypergraph
    noise = rng.random(len(bi))
    lab_s, touched_s, top_s = build_top1(bi, a_col, (noise,), tgt, d_col, n)
    sizes_s = np.bincount(lab_s[touched_s])
    nlive_s = len([c for c in np.unique(lab_s[touched_s]) if sizes_s[c] > 0])
    pur_shuf, _ = purity_stats(lab_s, touched_s, names, rng=rng)
    print(f"\nCONTROL shuffled ranking: {len(touched_s):,} nodes, "
          f"{nlive_s:,} components", flush=True)
    print(f"  module purity: mean={pur_shuf.mean():.3f} "
          f"median={np.median(pur_shuf):.3f}", flush=True)

    # CONTROL: size-matched random node sets
    all_nodes = touched
    pur_rand = []
    for nd in comps_real:
        s = rng.choice(all_nodes, size=len(nd), replace=False)
        cnt = Counter(mod2(names[i]) for i in s)
        pur_rand.append(cnt.most_common(1)[0][1] / len(s))
    pur_rand = np.array(pur_rand)
    print(f"\nCONTROL size-matched random node sets:", flush=True)
    print(f"  module purity: mean={pur_rand.mean():.3f} "
          f"median={np.median(pur_rand):.3f}", flush=True)

    # CONTROL: size- AND depth-matched
    order_by_depth = np.argsort(depth[all_nodes])
    sorted_nodes = all_nodes[order_by_depth]
    sorted_d = depth[sorted_nodes]
    pur_dm = []
    for nd in comps_real:
        picks = []
        for x in nd:
            j = int(np.searchsorted(sorted_d, depth[x]))
            lo, hi = max(0, j - 500), min(len(sorted_nodes), j + 500)
            picks.append(sorted_nodes[rng.integers(lo, hi)])
        cnt = Counter(mod2(names[i]) for i in picks)
        pur_dm.append(cnt.most_common(1)[0][1] / len(picks))
    pur_dm = np.array(pur_dm)
    print(f"\nCONTROL size+depth-matched random node sets:", flush=True)
    print(f"  module purity: mean={pur_dm.mean():.3f} "
          f"median={np.median(pur_dm):.3f}", flush=True)

    # verdict on half (i)
    print(f"\n{'='*72}\nHALF (i): are real components subject-coherent?\n{'='*72}",
          flush=True)
    print(f"  real            {pur_real.mean():.3f}", flush=True)
    print(f"  shuffled rank   {pur_shuf.mean():.3f}", flush=True)
    print(f"  size-matched    {pur_rand.mean():.3f}", flush=True)
    print(f"  size+depth      {pur_dm.mean():.3f}", flush=True)
    lift_rand = pur_real.mean() / max(pur_rand.mean(), 1e-9)
    lift_shuf = pur_real.mean() / max(pur_shuf.mean(), 1e-9)
    print(f"\n  lift over size-matched random: {lift_rand:.1f}x", flush=True)
    print(f"  lift over shuffled ranking:    {lift_shuf:.2f}x", flush=True)
    if lift_rand > 3 and lift_shuf > 1.2:
        v_i = ("REJECTED: real components ARE strongly subject-coherent, far "
               "above both controls. My 'not a subject atlas' claim was wrong.")
    elif lift_rand > 3:
        v_i = ("MIXED: components are subject-coherent, but a shuffled ranking "
               "achieves nearly the same -- the coherence comes from the "
               "hypergraph, not from the ranking.")
    else:
        v_i = ("SUPPORTED: real components are no more subject-coherent than "
               "random node sets.")
    print(f"\n  VERDICT (i): {v_i}", flush=True)

    # half (ii): what ARE the sinks?
    print(f"\n{'='*72}\nHALF (ii): what are the sinks the components flow to?\n{'='*72}",
          flush=True)
    has_out = np.zeros(n, dtype=bool)
    has_out[tgt[top]] = True
    sinks = touched[~has_out[touched]]
    pop = np.bincount(d_col[bi], minlength=n)
    print(f"  sinks: {len(sinks):,}", flush=True)
    print(f"    median depth {np.median(depth[sinks]):.0f} "
          f"(all touched: {np.median(depth[touched]):.0f})", flush=True)
    print(f"    glue (logic-only): {100*logic_only[sinks].mean():.1f}% "
          f"(all touched: {100*logic_only[touched].mean():.1f}%)", flush=True)
    print(f"    definitions: {100*np.isin(kind[sinks],[1,2,5,6,7]).mean():.1f}% "
          f"(all touched: {100*np.isin(kind[touched],[1,2,5,6,7]).mean():.1f}%)",
          flush=True)
    print(f"    median library-wide citations: {np.median(pop[sinks]):.0f} "
          f"(all touched: {np.median(pop[touched]):.0f})", flush=True)
    big = sinks[np.argsort(-pop[sinks])][:25]
    print("\n  the 25 most-used sinks (candidate 'techniques'):", flush=True)
    for s_ in big:
        print(f"    {names[s_][:56]:<58} used={int(pop[s_]):>7,} "
              f"depth={int(depth[s_]):>3} glue={bool(logic_only[s_])}", flush=True)

    out = {"real_purity": float(pur_real.mean()),
           "shuffled_purity": float(pur_shuf.mean()),
           "size_matched_purity": float(pur_rand.mean()),
           "depth_matched_purity": float(pur_dm.mean()),
           "lift_over_random": float(lift_rand),
           "lift_over_shuffled": float(lift_shuf),
           "verdict_subject_coherence": v_i,
           "n_components_real": int(nlive), "n_components_shuffled": int(nlive_s),
           "sinks": {"n": int(len(sinks)),
                     "median_depth": float(np.median(depth[sinks])),
                     "glue_frac": float(logic_only[sinks].mean()),
                     "definition_frac": float(np.isin(kind[sinks], [1,2,5,6,7]).mean()),
                     "top_used": [{"name": names[s_], "used": int(pop[s_]),
                                   "depth": int(depth[s_]),
                                   "glue": bool(logic_only[s_])} for s_ in big]}}
    with open(os.path.join(DATA, "island_controls.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten data/island_controls.json", flush=True)


if __name__ == "__main__":
    main()
