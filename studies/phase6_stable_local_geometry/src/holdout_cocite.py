#!/usr/bin/env python3
"""Practice-prediction validation. Hold out 10% of artifacts; remove
their edges from the GAP graph; from held-out proofs take co-cited
theorem pairs; controls = depth-band-matched random pairs. Does the
held-out-blind map's kinship (radius-2 shared substance, V-dip) predict
actual co-use? Non-circular: the predicted proofs contributed nothing."""
import json, os
from collections import defaultdict
import numpy as np
from merge_tree import load_common, load_edges

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
rng = np.random.default_rng(20260904)
es, ed = load_edges("GAP")
srcs = np.unique(es)
hold = set(rng.choice(srcs, len(srcs) // 10, replace=False).tolist())
adj = defaultdict(list)
cocite = defaultdict(list)
for s, d in zip(es, ed):
    if s in hold:
        cocite[s].append(d)
    else:
        adj[s].append(d)
def sig(x):
    s1 = adj.get(x, [])
    out = set(s1)
    for y in s1:
        out.update(adj.get(y, []))
    out.discard(x)
    return out
ok = lambda x: (not gen[x]) and kind[x] == 0 and depth[x] >= 11
pos = []
for t, cs in cocite.items():
    good = [c for c in set(cs) if ok(c)]
    if len(good) >= 2:
        a, b = rng.choice(good, 2, replace=False)
        if a != b:
            pos.append((int(a), int(b)))
    if len(pos) >= 3000:
        break
pos = np.array(pos)
mdp = np.minimum(depth[pos[:, 0]], depth[pos[:, 1]])
pool = np.where((~gen) & (kind == 0) & (depth >= 11))[0]
neg = []
for m in mdp:
    while True:
        a, b = rng.choice(pool, 2)
        if a != b and abs(int(min(depth[a], depth[b])) - int(m)) <= 5:
            neg.append((int(a), int(b))); break
neg = np.array(neg)
def stats(P):
    common, vdip, direct = [], [], 0
    cache = {}
    for a, b in P:
        sa = cache.get(a)
        if sa is None: sa = cache[a] = sig(a)
        sb = cache.get(b)
        if sb is None: sb = cache[b] = sig(b)
        if b in sa or a in sb: direct += 1
        cm = sa & sb
        common.append(bool(cm))
        if cm:
            vh = max(depth[c] for c in cm)
            vdip.append(int(min(depth[a], depth[b])) - vh)
    return np.mean(common), np.median(vdip) if vdip else None, direct / len(P)
pc, pv, pd = stats(pos)
nc, nv, nd = stats(neg)
print(f"co-cited pairs (n={len(pos)}): kinship {pc:.3f}  median V-dip {pv}  direct-link {pd:.3f}")
print(f"matched random  (n={len(neg)}): kinship {nc:.3f}  median V-dip {nv}  direct-link {nd:.3f}")
print(f"kinship lift: {pc/max(nc,1e-9):.1f}x")
json.dump({"pos_kinship": pc, "neg_kinship": nc, "pos_vdip": pv, "neg_vdip": nv,
           "pos_direct": pd, "neg_direct": nd},
          open("../data/holdout_cocite.json", "w"), indent=1)
