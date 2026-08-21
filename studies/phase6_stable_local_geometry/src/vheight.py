#!/usr/bin/env python3
"""V-merge: Sam's down-and-up geometry. vheight(A,B) = depth of the
deepest node shared by the radius-2 DOWNWARD move signatures of A and B
(GAP edges only). Deep shared substance = lateral kinship; shallow-only
= foundation-routed. Tested on the same 12k depth-matched pairs."""
import json, os
from collections import defaultdict
import numpy as np
from merge_tree import load_common, load_edges

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
rng = np.random.default_rng(20260903)
excl = {k for k, v in aname.items() if v in ("Core", "Tactic", "Lean", "Init", "Std")}
ok = (~gen) & (kind == 0) & (depth >= 11) & (area >= 0)
ok &= ~np.isin(area, np.array(sorted(excl), dtype=np.int16))
pool = np.where(ok)[0]
BANDS = [(11, 25), (26, 50), (51, 100), (101, 10**9)]
PER = 1500
pairs, labels, bands = [], [], []
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

es, ed = load_edges("GAP")
adj = defaultdict(list)
for s, d in zip(es, ed):
    adj[s].append(d)
def sig(x):
    s1 = adj.get(x, [])
    out = set(s1)
    for y in s1:
        out.update(adj.get(y, []))
    out.discard(x)
    return out
from sklearn.metrics import roc_auc_score
vh = np.full(len(pairs), -1, np.int32)
cache = {}
for q, (a, b) in enumerate(pairs):
    sa = cache.get(a)
    if sa is None: sa = cache[a] = sig(a)
    sb = cache.get(b)
    if sb is None: sb = cache[b] = sig(b)
    common = sa & sb
    if common:
        vh[q] = max(depth[c] for c in common)
res = {}
res["share_no_common"] = float((vh < 0).mean())
aucs, aucs_all = [], []
for bi in range(len(BANDS)):
    m = bands == bi
    # AUC treating no-common as vheight 0 (foundation-only)
    v = np.where(vh[m] < 0, 0, vh[m])
    if len(set(labels[m])) == 2:
        aucs_all.append(round(roc_auc_score(labels[m], v), 4))
res["auc_by_band(vheight,nocommon=0)"] = aucs_all
c = vh >= 0
res["median_vheight_same"] = float(np.median(vh[c & (labels == 1)]))
res["median_vheight_cross"] = float(np.median(vh[c & (labels == 0)]))
res["share_common_same"] = float(c[labels == 1].mean())
res["share_common_cross"] = float(c[labels == 0].mean())
# V-dip: how far below the pair's own level the shared substance sits
md = np.minimum(depth[pairs[:, 0]], depth[pairs[:, 1]])
res["median_vdip_same"] = float(np.median((md - vh)[c & (labels == 1)]))
res["median_vdip_cross"] = float(np.median((md - vh)[c & (labels == 0)]))
for k, v in res.items(): print(f"{k}: {v}")
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "vheight_areas.json"), "w"), indent=1)
