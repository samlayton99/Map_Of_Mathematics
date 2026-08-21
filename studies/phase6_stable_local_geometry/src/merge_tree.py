#!/usr/bin/env python3
"""Lateral geometry via the depth superlevel filtration.

Filter the undirected citation graph by depth from the top: at level t,
nodes with depth >= t are active, an edge is active when both endpoints
are. merge_height(A,B) = highest t at which A,B are connected.
dip(A,B) = min(dA,dB) - merge_height: how far below their own level the
connection forces a traversal. Lateral = small dip; foundation shortcut
= dip to the bottom. All derived from depth (append-safe, ordinal); no
fitted weights.

Machinery: union-find over nodes sorted by depth descending; pair
queries answered by checking connectivity after each level's unions.
"""
import json, os, sys
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, ".."))
P5DATA = os.path.normpath(os.path.join(P6, "..", "phase5_multiscale_navigation", "data"))

def load_common():
    nodes = np.load(os.path.join(P5DATA, "nodes.npz"))
    names = json.load(open(os.path.join(P5DATA, "names.json")))
    area = {}
    for line in open("/Users/sam/mathmap_data/all_modules.tsv"):
        n, m = line.rstrip("\n").split("\t")
        if m.startswith("Mathlib."):
            area[n] = m.split(".")[1]
        else:
            area[n] = "Core"
    aid = {}
    arr = np.full(len(names), -1, np.int16)
    for i, n in enumerate(names):
        a = area.get(n)
        if a is not None:
            arr[i] = aid.setdefault(a, len(aid))
    return nodes, names, arr, {v: k for k, v in aid.items()}

class DSU:
    def __init__(self, n):
        self.p = np.arange(n, dtype=np.int64)
    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra
            return True
        return False

def merge_heights(edge_src, edge_dst, depth, pairs):
    """pairs: (n,2) int array. Returns per-pair merge height (or -1)."""
    lvl = np.minimum(depth[edge_src], depth[edge_dst])
    order = np.argsort(-lvl, kind="stable")
    es, ed, lv = edge_src[order], edge_dst[order], lvl[order]
    dsu = DSU(len(depth))
    out = np.full(len(pairs), -1, np.int32)
    pending = list(range(len(pairs)))
    i = 0
    levels = np.unique(lv)[::-1]
    for t in levels:
        j = i
        while j < len(lv) and lv[j] == t:
            dsu.union(es[j], ed[j]); j += 1
        i = j
        still = []
        for q in pending:
            a, b = pairs[q]
            if dsu.find(a) == dsu.find(b):
                out[q] = t
            else:
                still.append(q)
        pending = still
        if not pending:
            break
    return out

def load_edges(name):
    z = np.load(os.path.join(P6, "data", "map_final", "edges_%s.npz" % name))
    return z["src_decl"].astype(np.int64), z["dst_decl"].astype(np.int64)

def main():
    nodes, names, area, aname = load_common()
    depth = nodes["depth"].astype(np.int32)
    gen = nodes["gen"]; kind = nodes["kind"]
    rng = np.random.default_rng(20260903)
    # theorem pool: non-generated theorems with depth >= 11 and known area,
    # excluding Core/Tactic (map-of-mathematics scope)
    excl = {k for k, v in aname.items() if v in ("Core", "Tactic", "Lean", "Init", "Std")}
    ok = (~gen) & (kind == 0) & (depth >= 11) & (area >= 0)
    ok &= ~np.isin(area, np.array(sorted(excl), dtype=np.int16))
    pool = np.where(ok)[0]
    print(f"theorem pool: {len(pool)}")
    # sample same-area and cross-area pairs, depth-band matched:
    # bin by min-depth band; sample equal counts per band per class
    BANDS = [(11, 25), (26, 50), (51, 100), (101, 10**9)]
    PER = 1500
    pairs, labels, bands = [], [], []
    by_area = defaultdict(list)
    for i in pool:
        by_area[area[i]].append(i)
    for bi, (lo, hi) in enumerate(BANDS):
        got_s = got_c = 0
        while got_s < PER or got_c < PER:
            a, b = rng.choice(pool, 2)
            if a == b: continue
            md = min(depth[a], depth[b])
            if not (lo <= md <= hi): continue
            same = area[a] == area[b]
            if same and got_s < PER:
                pairs.append((a, b)); labels.append(1); bands.append(bi); got_s += 1
            elif not same and got_c < PER:
                pairs.append((a, b)); labels.append(0); bands.append(bi); got_c += 1
    pairs = np.array(pairs); labels = np.array(labels); bands = np.array(bands)
    print(f"pairs sampled: {len(pairs)}")
    results = {}
    for pol in ("E4_flat", "GAP"):
        es, ed = load_edges(pol)
        mh = merge_heights(es, ed, depth, pairs)
        md = np.minimum(depth[pairs[:, 0]], depth[pairs[:, 1]])
        dip = md - np.maximum(mh, 0)
        conn = mh >= 0
        # AUC within bands then averaged (depth-matched by construction)
        from sklearn.metrics import roc_auc_score
        aucs = []
        for bi in range(len(BANDS)):
            m = (bands == bi) & conn
            if m.sum() > 100 and len(set(labels[m])) == 2:
                aucs.append(roc_auc_score(labels[m], mh[m]))
        r = {
            "connected_share": float(conn.mean()),
            "auc_same_vs_cross_by_mergeheight": [round(a, 4) for a in aucs],
            "median_merge_same": float(np.median(mh[conn & (labels == 1)])),
            "median_merge_cross": float(np.median(mh[conn & (labels == 0)])),
            "median_dip_same": float(np.median(dip[conn & (labels == 1)])),
            "median_dip_cross": float(np.median(dip[conn & (labels == 0)])),
            "cross_pairs_merging_at_foundations(<=10)":
                float((mh[conn & (labels == 0)] <= 10).mean()),
            "same_pairs_merging_at_foundations(<=10)":
                float((mh[conn & (labels == 1)] <= 10).mean()),
        }
        results[pol] = r
        print(f"\n== {pol}")
        for k, v in r.items():
            print(f"   {k}: {v}")
    json.dump(results, open(os.path.join(P6, "data", "merge_tree_areas.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
