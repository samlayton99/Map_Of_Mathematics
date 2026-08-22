#!/usr/bin/env python3
"""GPT program Part 5a: self-similarity across depth bands.

Question: is the local geometry the construction produces the SAME KIND
of object at every depth, or an artifact of one stratum? For each
min-depth band we measure, on the holdout-blind graph:

  - gap-cut anatomy: moves per proof (k), relative gap size
  - lane mix of selected moves
  - co-use kinship lift (pos vs matched neg, r2) INSIDE the band
  - branch-drop first-touch profile inside the band

If the construction is self-similar, these curves are flat-ish; a
regime change (e.g. foundations band behaving differently) shows up as
a break. Bands are on the raw dependency depth used map-wide.
"""
import json
from collections import defaultdict
import numpy as np
from merge_tree import load_common, load_edges

SEED = 20260910
BANDS = [(11, 25), (26, 50), (51, 100), (101, 200), (201, 10**9)]
NPOS = 1200
NEG_PER_POS = 5
R = 4

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
lane = nodes["lane"] if "lane" in nodes.files else None
es, ed = load_edges("GAPC")
pool_mask = (~gen) & (kind == 0) & (depth >= 11)
pool = np.where(pool_mask)[0]

rng = np.random.default_rng(SEED)
srcs = np.unique(es)
hold = set(rng.choice(srcs, len(srcs) // 10, replace=False).tolist())
adj = defaultdict(list)
cocite = defaultdict(list)
for s, d in zip(es, ed):
    (cocite if s in hold else adj)[s].append(d)

# per-proof k (moves per proof) by src depth band
k_by_band = defaultdict(list)
for s, ds in adj.items():
    b = None
    sd = int(depth[s])
    for bi, (lo, hi) in enumerate(BANDS):
        if lo <= sd <= hi:
            b = bi
    if b is not None:
        k_by_band[b].append(len(ds))

cache = {}
def rings(x):
    r = cache.get(x)
    if r is not None:
        return r
    seen = {x}; frontier = [x]; out = []
    for _ in range(R):
        nxt = []
        for y in frontier:
            for z in adj.get(y, ()):
                if z not in seen:
                    seen.add(z); nxt.append(z)
        out.append(frozenset(nxt)); frontier = nxt
    cache[x] = out
    return out

def touch_profile(a, b):
    ra, rb = rings(a), rings(b)
    da = {}
    for i, ring in enumerate(ra):
        for c in ring:
            da[c] = i + 1
    best = None
    r2 = 0
    for j, ring in enumerate(rb):
        for c in ring:
            if c in da:
                i = da[c]
                if i <= 2 and j + 1 <= 2:
                    r2 += 1
                t = (i + j + 1, max(i, j + 1), i, j + 1)
                if best is None or t < best:
                    best = t
    return r2, (None if best is None else (best[2], best[3]))

# band-restricted positives and matched negatives
pool_by_band = {}
for bi, (lo, hi) in enumerate(BANDS):
    pool_by_band[bi] = pool[(depth[pool] >= lo) & (depth[pool] <= hi)]

results = {}
for bi, (lo, hi) in enumerate(BANDS):
    pos = []
    for t, cs in cocite.items():
        good = [c for c in set(cs)
                if pool_mask[c] and lo <= depth[c] <= hi]
        if len(good) >= 2:
            a, b = rng.choice(good, 2, replace=False)
            if a != b:
                pos.append((int(a), int(b)))
        if len(pos) >= NPOS:
            break
    bp = pool_by_band[bi]
    neg = []
    for _ in range(len(pos) * NEG_PER_POS):
        x, y = rng.choice(bp, 2)
        if x != y:
            neg.append((int(x), int(y)))
    def stats(P):
        kin = 0; touches = []
        for a, b in P:
            r2, ft = touch_profile(a, b)
            kin += r2 > 0
            if ft:
                touches.append(ft)
        return kin / max(len(P), 1), touches
    pk, pt = stats(pos)
    nk, _ = stats(neg)
    ks = np.array(k_by_band.get(bi, [0]))
    res = {
        "band": [lo, min(hi, 10**6)],
        "n_proofs": len(k_by_band.get(bi, [])),
        "k_median": float(np.median(ks)),
        "k_mean": float(ks.mean()),
        "n_pos": len(pos), "n_neg": len(neg),
        "pos_kinship_r2": pk, "neg_kinship_r2": nk,
        "lift_r2": pk / max(nk, 1e-9),
    }
    if pt:
        asym = np.array([abs(i - j) for i, j in pt])
        res["touch_sym"] = float((asym == 0).mean())
        res["touch_asym2p"] = float((asym >= 2).mean())
        res["median_total_drop"] = float(np.median([i + j for i, j in pt]))
    results["band_%d" % bi] = res
    print(json.dumps(res), flush=True)

json.dump(results, open("../data/depth_self_similarity.json", "w"), indent=1)
