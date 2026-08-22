#!/usr/bin/env python3
"""Navigation benchmark v3: route finding.

For a held-out proof: start at its most specific statement-world item s
(what the theorem talks about) and route to each map move m (what the
proof uses). The proof's own edges are excised first. Compare the ATLAS
graph against the flat citation graph (E4_flat):

  - reachability within 8 undirected hops
  - route length
  - what the route passes THROUGH: lane mix of intermediates (math /
    transport / infra) and hub share (top-100 in-degree nodes)

The navigation claim is not just "shorter" but "through mathematics":
a route through `Eq.mpr` teaches nothing.
"""
import json
import os
from collections import defaultdict, deque
import numpy as np
from merge_tree import load_common, load_edges

SEED = 20260914
NROUTES = 800
MAXHOP = 8
P6DATA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data"))
P5DATA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "phase5_multiscale_navigation", "data"))

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
tz = np.load(os.path.join(P6DATA, "traversal_geometry.npz"))
lane = tz["node_lane"]
pool_mask = (~gen) & (kind == 0) & (depth >= 11)

inc = np.load(os.path.join(P5DATA, "incid.npz"))
arts = np.load(os.path.join(P5DATA, "artifacts.npz"))
certifies = arts["certifies"].astype(np.int64)
inc_art = inc["artifact"].astype(np.int64)
inc_decl = inc["decl"].astype(np.int64)
in_stmt = inc["in_stmt_world"].astype(bool)
stmt_of = defaultdict(set)
tgt = certifies[inc_art]
sel = in_stmt & (inc_decl != tgt)
for t, d in zip(tgt[sel], inc_decl[sel]):
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

def build_undirected(name):
    a, b = load_edges(name)
    g = defaultdict(list)
    for x, y in zip(a, b):
        if x in hold:
            continue  # excise held-out proofs' edges
        g[int(x)].append(int(y))
        g[int(y)].append(int(x))
    return g

G = {"atlas": build_undirected("ATLAS"), "flat": build_undirected("E4_flat")}
indeg = {}
for gname, g in G.items():
    dd = np.zeros(len(depth), np.int64)
    a, b = load_edges("ATLAS" if gname == "atlas" else "E4_flat")
    np.add.at(dd, b, 1)
    hubs = set(np.argsort(-dd)[:100].tolist())
    indeg[gname] = hubs

def bfs_route(g, s, t):
    if s == t:
        return []
    prev = {s: None}
    q = deque([(s, 0)])
    while q:
        x, h = q.popleft()
        if h >= MAXHOP:
            continue
        for y in g.get(x, ()):
            if y not in prev:
                prev[y] = x
                if y == t:
                    path = [y]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])
                    return path[::-1]
                q.append((y, h + 1))
    return None

# sample (seed, move) tasks
tasks = []
indeg_all = nodes["in_degree"].astype(np.int64)
for s, ds in moves_of.items():
    S = stmt_of.get(int(s), set())
    ms = sorted({d for d in ds if pool_mask[d]} - S)
    if S and ms:
        seed_node = min(S, key=lambda x: indeg_all[x])
        m = int(ms[rng.integers(len(ms))])
        tasks.append((int(seed_node), m))
rng.shuffle(tasks)
tasks = tasks[:NROUTES]
print(f"route tasks: {len(tasks)}")

res = {}
for gname, g in G.items():
    found, lens, lane_mix, hubshare = 0, [], np.zeros(4), []
    for s, m in tasks:
        p = bfs_route(g, s, m)
        if p is None:
            continue
        found += 1
        lens.append(len(p) - 1)
        inter = p[1:-1]
        if inter:
            for x in inter:
                l = int(lane[x]) if 0 <= int(lane[x]) <= 2 else 3
                lane_mix[l] += 1
            hubshare.append(np.mean([x in indeg[gname] for x in inter]))
    tot = lane_mix.sum()
    res[gname] = {
        "found_frac": found / len(tasks),
        "median_len": float(np.median(lens)) if lens else None,
        "mean_len": float(np.mean(lens)) if lens else None,
        "intermediate_lane_mix": {
            "math": float(lane_mix[0] / tot) if tot else None,
            "transport": float(lane_mix[1] / tot) if tot else None,
            "infra": float(lane_mix[2] / tot) if tot else None,
            "other": float(lane_mix[3] / tot) if tot else None,
        },
        "mean_hub_share_of_intermediates":
            float(np.mean(hubshare)) if hubshare else None,
    }
    print(gname, json.dumps(res[gname]), flush=True)

json.dump(res, open("../data/route_finding.json", "w"), indent=1)
