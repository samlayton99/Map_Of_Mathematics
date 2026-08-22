#!/usr/bin/env python3
"""Sam's proposal: integer edge weight = |depth(a) - depth(b)|, route by
minimising TOTAL vertical travel. Tests it against what we actually ran
before (unweighted hops; bottleneck-dip Dijkstra).

Why this is a different object from both: for any path,
    sum |delta d|  =  |d(s) - d(t)|  +  2 * (backtracking)
so the additive metric charges TWICE for every step down that must be
climbed back. Bottleneck-dip charged a deep dive ONCE; hop count did
not charge for it at all. Sam's metric is the one that actually makes
"connect through the foundations" expensive.

Weight variants:
  W0  w = |delta d|          (literal proposal; same-depth hops free)
  W1  w = 1 + |delta d|      (hop-penalised; blocks free lateral drift)
Baseline:
  HOP w = 1                  (what route_finding.py used)

Graphs: GAPC undirected (holdout-blind), optionally + Lambda co-use
edges. Same 800-task seed as route_finding.py / route_reach.py.

Reported per router: vertical cost, hops, EXCESS over the unavoidable
|d(s)-d(t)| floor, how far below both endpoints the route dives, lane
mix of intermediates, hub share.
"""
import json
import os
from collections import defaultdict
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from merge_tree import load_common, load_edges

SEED = 20260914
NROUTES = 300          # scipy SSSP per source; 300 keeps this ~minutes
CHUNK = 25
P5DATA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "phase5_multiscale_navigation", "data"))
P6DATA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data"))

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int64)
gen = nodes["gen"]; kind = nodes["kind"]
pool_mask = (~gen) & (kind == 0) & (depth >= 11)
N = len(depth)
lane = np.load(os.path.join(P6DATA, "traversal_geometry.npz"))["node_lane"]

inc = np.load(os.path.join(P5DATA, "incid.npz"))
arts = np.load(os.path.join(P5DATA, "artifacts.npz"))
certifies = arts["certifies"].astype(np.int64)
tgt = certifies[inc["artifact"].astype(np.int64)]
dec = inc["decl"].astype(np.int64)
sel = inc["in_stmt_world"].astype(bool) & (dec != tgt)
stmt_of = defaultdict(set)
for t, d in zip(tgt[sel], dec[sel]):
    if not gen[d]:
        stmt_of[int(t)].add(int(d))

es, ed = load_edges("GAPC")
rng = np.random.default_rng(SEED)
srcs = np.unique(es)
hold = set(rng.choice(srcs, len(srcs) // 10, replace=False).tolist())
moves_of = defaultdict(list)
for s, d in zip(es, ed):
    if s in hold:
        moves_of[s].append(d)

indeg_all = nodes["in_degree"].astype(np.int64)
tasks = []
for s, ds in moves_of.items():
    S = stmt_of.get(int(s), set())
    ms = sorted({d for d in ds if pool_mask[d]} - S)
    if S and ms:
        tasks.append((int(min(S, key=lambda x: indeg_all[x])),
                      int(ms[rng.integers(len(ms))])))
rng.shuffle(tasks)
tasks = tasks[:NROUTES]
print(f"tasks: {len(tasks)}")

keep = ~np.isin(es, np.fromiter(hold, np.int64, len(hold)))
gs, gd = es[keep], ed[keep]

# Lambda lateral pairs, holdout-blind
by_src = defaultdict(list)
for s, d in zip(gs, gd):
    by_src[int(s)].append(int(d))
la, lb = [], []
for s, ms in by_src.items():
    ms = sorted(set(ms))[:20]
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            la.append(ms[i]); lb.append(ms[j])
la = np.array(la, np.int64); lb = np.array(lb, np.int64)
ldel = np.abs(depth[la] - depth[lb])
print(f"lambda edges {len(la)}  |delta| median {np.median(ldel):.0f} "
f" zero-frac {(ldel == 0).mean():.3f}")

hub = set(np.argsort(-nodes["in_degree"].astype(np.int64))[:100].tolist())


def build(with_lambda, mode):
    a = np.concatenate([gs, la]) if with_lambda else gs
    b = np.concatenate([gd, lb]) if with_lambda else gd
    dl = np.abs(depth[a] - depth[b]).astype(np.float64)
    if mode == "W0":
        w = np.maximum(dl, 0.0) + 1e-9      # literal |delta d|
    elif mode == "W1":
        w = dl + 1.0                        # hop-penalised
    else:
        w = np.ones(len(a))                 # plain hops
    ai = np.concatenate([a, b]); bi = np.concatenate([b, a])
    ww = np.concatenate([w, w])
    return csr_matrix((ww, (ai, bi)), shape=(N, N))


def analyse(M, tasks_):
    rows = []
    for c0 in range(0, len(tasks_), CHUNK):
        chunk = tasks_[c0:c0 + CHUNK]
        sources = np.array([s for s, _ in chunk])
        dist, pred = dijkstra(M, directed=False, indices=sources,
                              return_predecessors=True, limit=np.inf)
        for k, (s, t) in enumerate(chunk):
            if not np.isfinite(dist[k, t]):
                rows.append(None)
                continue
            path = [t]
            while path[-1] != s:
                p = pred[k, path[-1]]
                if p < 0:
                    break
                path.append(int(p))
            path = path[::-1]
            dp = depth[path]
            base = min(int(depth[s]), int(depth[t]))
            top = max(int(depth[s]), int(depth[t]))
            vcost = int(np.abs(np.diff(dp)).sum())
            inter = path[1:-1]
            rows.append({
                "hops": len(path) - 1,
                "vcost": vcost,
                "excess": vcost - abs(int(depth[s]) - int(depth[t])),
                "dive": max(0, base - int(dp.min())),
                "climb": max(0, int(dp.max()) - top),
                "lane_math": float(np.mean([lane[x] == 0 for x in inter]))
                if inter else None,
                "hub": float(np.mean([x in hub for x in inter]))
                if inter else None,
            })
        print(f"    {min(c0+CHUNK, len(tasks_))}/{len(tasks_)}", flush=True)
    return rows


res = {}
for with_lambda in (False, True):
    for mode in ("HOP", "W0", "W1"):
        name = ("gapc+lambda" if with_lambda else "gapc") + "/" + mode
        M = build(with_lambda, mode)
        rows = analyse(M, tasks)
        ok = [r for r in rows if r]
        agg = {"found": len(ok) / len(rows)}
        for k in ("hops", "vcost", "excess", "dive", "climb"):
            agg["median_" + k] = float(np.median([r[k] for r in ok]))
            agg["mean_" + k] = float(np.mean([r[k] for r in ok]))
        agg["frac_zero_excess"] = float(
            np.mean([r["excess"] == 0 for r in ok]))
        agg["frac_zero_dive"] = float(np.mean([r["dive"] == 0 for r in ok]))
        lm = [r["lane_math"] for r in ok if r["lane_math"] is not None]
        hb = [r["hub"] for r in ok if r["hub"] is not None]
        agg["mean_lane_math"] = float(np.mean(lm)) if lm else None
        agg["mean_hub_share"] = float(np.mean(hb)) if hb else None
        res[name] = agg
        print(name, json.dumps(agg), flush=True)

json.dump(res, open("../data/weighted_routes.json", "w"), indent=1)
