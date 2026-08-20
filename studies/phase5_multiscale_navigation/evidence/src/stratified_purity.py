#!/usr/bin/env python3
"""Approach 1, first question: does the stratified-purity property already
hold, and where exactly does connectivity break?

The owner's requirement: "total rank purity at the top of the tree, and fine
to have less purity the lower you go." Before massaging anything, measure
whether the frozen ranking already has that shape, and diagnose the component
structure of top-1 -- specifically WHAT the 25,230 components are, because if
they are overwhelmingly shallow plumbing regions then the base of the tree is
exactly where the breakage is, which is the owner's own prediction.

Measured here:
  A. rank-1 composition by depth band (purity vs altitude)
  B. component-size distribution of the top-1 graph
  C. depth profile of components: are the shards shallow or deep?
  D. why each component terminates: what its sink is
  E. how many edges would have to be added back to reconnect, and of what kind
"""
import json, os
import numpy as np
import scipy.sparse as sp
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))


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
    d_cite = inc["d_cite"].astype(np.int32)
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"].astype(np.int32)
    kind = nodes["kind"]
    n = len(depth)
    is_claim = v8["decl_is_claim"]
    logic_only = v8["decl_logic_only"]
    machinery = v8["machinery"]
    tgt = certifies[a_col]

    P4 = lb & is_claim[d_col] & ~logic_only[d_col] & ~machinery
    P2 = lb

    # ---- A. purity by depth band -------------------------------------
    # "content" here = not logic-only and not machinery and is a claim, i.e.
    # exactly what P4 keeps. Purity of a proof's rank-1 = did the top-ranked
    # LOAD-BEARING citation survive the content boundary?
    print("=== A. rank-1 composition by depth band (theorem artifacts) ===",
          flush=True)
    is_thm_art = (kind[certifies] == 0)
    idx2 = np.where(P2 & is_thm_art[a_col])[0]
    ordk = np.lexsort((-d_cite[idx2], a_col[idx2]))
    idx2s = idx2[ordk]
    newedge = np.empty(len(idx2s), dtype=bool)
    newedge[0] = True
    newedge[1:] = a_col[idx2s][1:] != a_col[idx2s][:-1]
    top_inc = idx2s[newedge]                       # rank-1 incidence per proof
    top_art = a_col[top_inc]
    top_is_content = P4[top_inc]
    tdepth = depth[certifies[top_art]]

    bands = [(0, 10), (10, 25), (25, 50), (50, 75), (75, 125), (125, 350)]
    rows = []
    for lo, hi in bands:
        m = (tdepth >= lo) & (tdepth < hi)
        if not m.any():
            continue
        pur = float(top_is_content[m].mean())
        rows.append({"band": f"{lo}-{hi}", "n_proofs": int(m.sum()),
                     "rank1_is_content": round(pur, 4)})
        print(f"  depth {lo:>3}-{hi:<3}  proofs={int(m.sum()):>7,}  "
              f"rank-1 is content: {pur:>6.1%}", flush=True)

    # ---- B/C/D. component structure of the top-1 graph ---------------
    print("\n=== B. components of the top-1 graph ===", flush=True)
    idx4 = np.where(P4)[0]
    ordk4 = np.lexsort((-d_cite[idx4], a_col[idx4]))
    idx4s = idx4[ordk4]
    ne4 = np.empty(len(idx4s), dtype=bool)
    ne4[0] = True
    ne4[1:] = a_col[idx4s][1:] != a_col[idx4s][:-1]
    top1 = idx4s[ne4]
    src = tgt[top1]; dst = d_col[top1]
    g = sp.coo_matrix((np.ones(len(src), dtype=np.int8), (src, dst)), shape=(n, n))
    ncomp, lbl = sp.csgraph.connected_components(g, directed=False)
    touched = np.unique(np.concatenate([src, dst]))
    tl = lbl[touched]
    sizes = np.bincount(tl)
    live = np.where(sizes > 0)[0]
    ls = sizes[live]
    print(f"  touched nodes {len(touched):,}, components {len(ls):,}", flush=True)
    print(f"  size distribution: max={ls.max():,} p99={np.percentile(ls,99):.0f} "
          f"p50={np.percentile(ls,50):.0f} min={ls.min()}", flush=True)
    print(f"  singletons+pairs: {int((ls<=2).sum()):,} components "
          f"({100*(ls<=2).sum()/len(ls):.1f}%)", flush=True)

    print("\n=== C. are the shards shallow or deep? ===", flush=True)
    comp_of = lbl[touched]
    dep_t = depth[touched]
    giant = live[np.argmax(ls)]
    ing = comp_of == giant
    print(f"  giant component: {int(ing.sum()):,} nodes, "
          f"median depth {np.median(dep_t[ing]):.0f}", flush=True)
    print(f"  everything else: {int((~ing).sum()):,} nodes, "
          f"median depth {np.median(dep_t[~ing]):.0f}", flush=True)
    for lo, hi in bands:
        m = (dep_t >= lo) & (dep_t < hi)
        if not m.any():
            continue
        frac = float(ing[m].mean())
        print(f"    depth {lo:>3}-{hi:<3}: {int(m.sum()):>7,} nodes, "
              f"{frac:>6.1%} in the giant component", flush=True)

    # ---- D. what terminates each component ---------------------------
    print("\n=== D. sinks: where top-1 chains stop ===", flush=True)
    has_out = np.zeros(n, dtype=bool)
    has_out[src] = True
    sinks = touched[~has_out[touched]]
    print(f"  sinks (no outgoing top-1 edge): {len(sinks):,}", flush=True)
    sd = depth[sinks]
    print(f"  sink depth: p50={np.median(sd):.0f} p90={np.percentile(sd,90):.0f}",
          flush=True)
    cnt = Counter()
    for s in sinks:
        cnt[names[s].split(".")[0]] += 1
    print("  most common sink roots:", flush=True)
    for r, c in cnt.most_common(12):
        print(f"    {r:<28} {c:>6,}", flush=True)

    # ---- E. reconnection cost ----------------------------------------
    print("\n=== E. how much evidence reconnects it? ===", flush=True)
    for k in (2, 3, 4):
        rank_in_edge = np.zeros(len(idx4s), dtype=np.int32)
        starts = np.where(ne4)[0]
        counts = np.diff(np.append(starts, len(idx4s)))
        rank_in_edge = np.concatenate([np.arange(c) for c in counts])
        sel = idx4s[rank_in_edge < k]
        s2, d2 = tgt[sel], d_col[sel]
        g2 = sp.coo_matrix((np.ones(len(s2), dtype=np.int8), (s2, d2)), shape=(n, n))
        nc2, l2 = sp.csgraph.connected_components(g2, directed=False)
        t2 = np.unique(np.concatenate([s2, d2]))
        sz = np.bincount(l2[t2])
        sz = sz[sz > 0]
        print(f"  top-{k}: edges={len(sel):,} components={len(sz):,} "
              f"giant={sz.max()/sz.sum():.2%}", flush=True)

    out = {"purity_by_depth_band": rows,
           "top1_components": int(len(ls)),
           "top1_giant_fraction": float(ls.max() / ls.sum()),
           "top1_small_components_le2": int((ls <= 2).sum()),
           "sinks": int(len(sinks)),
           "sink_depth_median": float(np.median(sd))}
    with open(os.path.join(DATA, "stratified_purity.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten data/stratified_purity.json", flush=True)


if __name__ == "__main__":
    main()
