#!/usr/bin/env python3
"""Route reachability diagnostic: was 39% a real limit or the hop cap?

Sam's point: with a virtual root, EVERY pair connects by descending to
shared foundations and climbing back. So reachability is not the
question -- COST is. This script measures, for the same 800 tasks
(statement seed -> proof move, held-out proof's edges excised):

  1. reachability at hop caps 8 / 16 / unbounded
  2. the route's SHAPE, in depth terms:
       dip   = min(depth of endpoints) - min(depth along route)
               (how far down toward foundations the route had to go)
       climb = max(depth along route) - max(depth of endpoints)
               (how far up above both endpoints it had to go)
     A lateral route has dip ~ 0 and climb ~ 0.
  3. what Lambda edges (co-use pairs from NON-held-out proofs, added as
     undirected lateral links) do to both.

Cheapest-dip routing, not fewest-hops: we search for the route that
minimizes the deepest descent, breaking ties by length (Dijkstra on
the cost vector (dip, hops)).
"""
import heapq
import json
import os
from collections import defaultdict, deque
import numpy as np
from merge_tree import load_common, load_edges

SEED = 20260914          # same seed as route_finding.py -> same tasks
NROUTES = 800
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

# atlas graph, held-out proofs' own edges excised
a_src, a_dst = load_edges("ATLAS")
G = defaultdict(list)
for x, y in zip(a_src, a_dst):
    if int(x) in hold:
        continue
    G[int(x)].append(int(y))
    G[int(y)].append(int(x))
print(f"atlas undirected adjacency: {len(G)} nodes")

# Lambda lateral edges from NON-held-out proofs only
lam_pairs = defaultdict(set)
by_src = defaultdict(list)
for s, d in zip(es, ed):
    if int(s) not in hold:
        by_src[int(s)].append(int(d))
np_lam = 0
for s, ms in by_src.items():
    ms = sorted(set(ms))[:20]
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            lam_pairs[ms[i]].add(ms[j])
            lam_pairs[ms[j]].add(ms[i])
            np_lam += 1
print(f"lambda lateral pairs (holdout-blind): {np_lam}")

GL = defaultdict(list)
for x, ys in G.items():
    GL[x].extend(ys)
for x, ys in lam_pairs.items():
    GL[x].extend(ys)

indeg_all = nodes["in_degree"].astype(np.int64)
tasks = []
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


def bfs_cap(g, s, t, cap):
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


def cheapest_dip(g, s, t, maxpop=400000):
    """Dijkstra minimizing (deepest descent below the shallower
    endpoint, then hops). Returns (dip, hops, climb) or None."""
    base = min(int(depth[s]), int(depth[t]))
    top = max(int(depth[s]), int(depth[t]))
    # state cost = max dip seen so far; standard Dijkstra on bottleneck
    best = {s: (0, 0)}
    pq = [(0, 0, 0, s)]   # dip, hops, climb, node
    pops = 0
    while pq:
        dip, hops, climb, x = heapq.heappop(pq)
        pops += 1
        if pops > maxpop:
            return None
        if x == t:
            return dip, hops, climb
        if best.get(x, (10**9, 10**9)) < (dip, hops):
            continue
        for y in g.get(x, ()):
            dy = int(depth[y])
            nd = max(dip, base - dy) if dy < base else dip
            nc = max(climb, dy - top) if dy > top else climb
            st = (nd, hops + 1)
            if st < best.get(y, (10**9, 10**9)):
                best[y] = st
                heapq.heappush(pq, (nd, hops + 1, nc, y))
    return None


res = {}
for gname, g in (("atlas", G), ("atlas+lambda", GL)):
    row = {}
    for cap in (8, 16, 10**6):
        found = sum(1 for s, m in tasks if bfs_cap(g, s, m, cap) is not None)
        row["reach@%s" % ("inf" if cap > 100 else cap)] = found / len(tasks)
        print(f"  {gname} cap {cap}: {found/len(tasks):.3f}", flush=True)
    dips, hops_, climbs = [], [], []
    for s, m in tasks:
        r = cheapest_dip(g, s, m)
        if r:
            dips.append(r[0]); hops_.append(r[1]); climbs.append(r[2])
    row["cheapest_dip_found"] = len(dips) / len(tasks)
    row["median_dip"] = float(np.median(dips)) if dips else None
    row["mean_dip"] = float(np.mean(dips)) if dips else None
    row["frac_dip_zero"] = float(np.mean(np.array(dips) == 0)) if dips else None
    row["median_hops_at_min_dip"] = float(np.median(hops_)) if hops_ else None
    row["median_climb"] = float(np.median(climbs)) if climbs else None
    res[gname] = row
    print(gname, json.dumps(row), flush=True)

json.dump(res, open("../data/route_reach.json", "w"), indent=1)
