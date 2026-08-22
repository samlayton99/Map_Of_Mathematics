#!/usr/bin/env python3
"""GPT program Part 3c: chronological held-out validation.

Can geometry built from OLDER mathematics predict which old theorems
FUTURE proofs will use together? Split by file first-appearance date in
the mathlib4 git history (blobless clone): training graph = zoom-1
edges whose src AND dst live in pre-cutoff files; positives = move
pairs of proofs in post-cutoff files where both moves are pre-cutoff
pool members; matched negatives from the pre-cutoff pool.

Honest caveats (stated, not hidden): (1) statements/proofs are in
their CURRENT snapshot form, not their historical form -- this is a
date-restricted subgraph, not a rebuild of an older Mathlib; (2) file
date proxies declaration date; a moved file counts as new, which
misclassifies some old content as future.
"""
import json
from collections import defaultdict
import numpy as np
from merge_tree import load_common, load_edges

SEED = 20260912
NEG_PER_POS = 10
NPOS = 3000
CUT_QUANTILE = 0.85

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
es, ed = load_edges("GAPC")
pool_mask = (~gen) & (kind == 0) & (depth >= 11)
pool = np.where(pool_mask)[0]

# file dates: stream is git log (new -> old); last-seen date per path is
# the OLDEST add, which is what we want
fdate = {}
date = None
for line in open("/private/tmp/claude-501/-Users-sam-my-repos-research-"
                 "Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/"
                 "scratchpad/file_add_log.txt"):
    line = line.rstrip("\n")
    if line.startswith("#"):
        date = line[1:]
    elif line.endswith(".lean"):
        fdate[line] = date
print(f"dated files: {len(fdate)}")

# decl -> file via module name
mod_of = {}
for line in open("/Users/sam/mathmap_data/all_modules.tsv"):
    n, _, m = line.rstrip("\n").partition("\t")
    mod_of[n] = m
decl_date = np.full(len(names), "", dtype=object)
n_dated = 0
for i, n in enumerate(names):
    m = mod_of.get(n, "")
    if m.startswith("Mathlib"):
        d = fdate.get(m.replace(".", "/") + ".lean")
        if d:
            decl_date[i] = d
            n_dated += 1
print(f"dated declarations: {n_dated}")

dates = sorted(d for d in decl_date if d)
cut = dates[int(len(dates) * CUT_QUANTILE)]
print(f"cutoff date (q={CUT_QUANTILE}): {cut}")
is_old = np.array([bool(d) and d < cut for d in decl_date])
is_new = np.array([bool(d) and d >= cut for d in decl_date])

adj = defaultdict(list)
future = defaultdict(list)
for s, d in zip(es, ed):
    if is_old[s] and is_old[d]:
        adj[s].append(d)
    elif is_new[s]:
        future[s].append(d)
print(f"training srcs: {len(adj)}  future proofs: {len(future)}")

odeg = np.zeros(len(names), np.int32)
for s, ds in adj.items():
    odeg[s] = len(ds)
DEGBINS = np.array([0, 1, 2, 3, 6, 11, 10**9])
degbin_all = np.searchsorted(DEGBINS, odeg, side="right")

rng = np.random.default_rng(SEED)
old_pool = pool[is_old[pool]]
old_pool_mask = pool_mask & is_old
pos = []
for t, cs in future.items():
    good = [c for c in set(cs) if old_pool_mask[c]]
    if len(good) >= 2:
        a, b = rng.choice(good, 2, replace=False)
        if a != b:
            pos.append((int(a), int(b)))
    if len(pos) >= NPOS:
        break
print(f"chronological positive pairs: {len(pos)}")

by_key = defaultdict(list)
for i in old_pool:
    by_key[degbin_all[i]].append(i)
by_key = {k: np.array(v) for k, v in by_key.items()}
neg = []
for a, b in pos:
    md = int(min(depth[a], depth[b]))
    same = area[a] == area[b] and area[a] >= 0
    pa = by_key.get(degbin_all[a], old_pool)
    pb = by_key.get(degbin_all[b], old_pool)
    got = tries = 0
    while got < NEG_PER_POS and tries < 4000:
        tries += 1
        x = int(pa[rng.integers(len(pa))])
        y = int(pb[rng.integers(len(pb))])
        if x == y or abs(int(min(depth[x], depth[y])) - md) > 5:
            continue
        if (area[x] == area[y] and area[x] >= 0) != same:
            continue
        neg.append((x, y)); got += 1
    while got < NEG_PER_POS:
        x, y = rng.choice(old_pool, 2)
        if x != y and abs(int(min(depth[x], depth[y])) - md) <= 5:
            neg.append((int(x), int(y))); got += 1

R = 4
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

def scores(P):
    r2, ms = [], []
    for a, b in P:
        ra, rb = rings(a), rings(b)
        da = {}
        for i, ring in enumerate(ra):
            for c in ring:
                da[c] = i + 1
        touch = {}
        for j, ring in enumerate(rb):
            for c in ring:
                if c in da:
                    touch[c] = (da[c], j + 1)
        ca = ra[0] | ra[1]; cb = rb[0] | rb[1]
        r2.append(len(ca & cb))
        ms.append(sum(2.0 ** -(i + j) for i, j in touch.values()))
    return np.array(r2, float), np.array(ms, float)

def average_precision(scores_, labels, nshuf=32, seed=0):
    rng2 = np.random.default_rng(seed)
    n = len(scores_)
    aps = []
    for _ in range(nshuf):
        perm = rng2.permutation(n)
        order = perm[np.argsort(-scores_[perm], kind="stable")]
        l = labels[order]
        tp = np.cumsum(l)
        prec = tp / (np.arange(n) + 1)
        aps.append((prec * l).sum() / max(l.sum(), 1))
    return float(np.mean(aps))

pr2, pms = scores(pos)
nr2, nms = scores(neg)
labels = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
res = {
    "cutoff": cut, "n_pos": len(pos), "n_neg": len(neg),
    "prior": len(pos) / (len(pos) + len(neg)),
    "auprc_r2": average_precision(np.concatenate([pr2, nr2]), labels),
    "auprc_ms": average_precision(np.concatenate([pms, nms]), labels),
    "pos_kinship_r2": float((pr2 > 0).mean()),
    "neg_kinship_r2": float((nr2 > 0).mean()),
}
res["lift_r2"] = res["pos_kinship_r2"] / max(res["neg_kinship_r2"], 1e-9)
print(json.dumps(res, indent=1))
json.dump(res, open("../data/chrono_validation.json", "w"), indent=1)
