#!/usr/bin/env python3
"""Supplement to route_reach.py: isolate WHY atlas routing fails.

Three graphs, same 800 tasks, same holdout:
  atlas   rendered view: math-scoped sources, portal edges (rho>1/2)
          DELETED -- this is what route_finding.py walked
  gapc    the unrendered zoom-1 map: portals retained, all sources
  gapc+L  plus holdout-blind Lambda co-use pairs as lateral edges

Also reports endpoint presence, which caps reachability from above.
"""
import json
import os
from collections import defaultdict, deque
import numpy as np
from merge_tree import load_common, load_edges

SEED = 20260914
NROUTES = 800
CAP = 16
P5DATA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "phase5_multiscale_navigation", "data"))

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
pool_mask = (~gen) & (kind == 0) & (depth >= 11)

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

def undirected(src, dst):
    g = defaultdict(list)
    for x, y in zip(src, dst):
        if int(x) in hold:
            continue
        g[int(x)].append(int(y))
        g[int(y)].append(int(x))
    return g

a_s, a_d = load_edges("ATLAS")
G_atlas = undirected(a_s, a_d)
G_gapc = undirected(es, ed)
lam = defaultdict(set)
by_src = defaultdict(list)
for s, d in zip(es, ed):
    if int(s) not in hold:
        by_src[int(s)].append(int(d))
for s, ms in by_src.items():
    ms = sorted(set(ms))[:20]
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            lam[ms[i]].add(ms[j]); lam[ms[j]].add(ms[i])
G_gl = defaultdict(list)
for x, ys in G_gapc.items():
    G_gl[x].extend(ys)
for x, ys in lam.items():
    G_gl[x].extend(ys)

def bfs(g, s, t, cap):
    if s == t:
        return 0
    seen = {s}
    q = deque([(s, 0)])
    while q:
        x, h = q.popleft()
        if h >= cap:
            continue
        for y in g.get(x, ()):
            if y not in seen:
                if y == t:
                    return h + 1
                seen.add(y)
                q.append((y, h + 1))
    return None

res = {}
for gname, g in (("atlas", G_atlas), ("gapc", G_gapc), ("gapc+lambda", G_gl)):
    present = np.mean([(s in g and t in g) for s, t in tasks])
    lens = [bfs(g, s, t, CAP) for s, t in tasks]
    found = [l for l in lens if l is not None]
    res[gname] = {
        "both_endpoints_present": float(present),
        "reach@16": len(found) / len(tasks),
        "reach_given_present": len(found) / max(present * len(tasks), 1),
        "median_len": float(np.median(found)) if found else None,
    }
    print(gname, json.dumps(res[gname]), flush=True)

json.dump(res, open("../data/route_reach2.json", "w"), indent=1)
