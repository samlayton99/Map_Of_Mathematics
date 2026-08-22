#!/usr/bin/env python3
"""GPT program Part 3b: provenance-resolved held-out validation.

Positives come from the elaboration-provenance sidecar (40 Mathlib
files): the names the human author's SOURCE TEXT referenced, per
declaration. This is external to the kernel citation construction --
our inclusion rule contributed nothing to these pairs.

Protocol: hold out every declaration in the prov files (remove their
zoom-1 edges); positives = theorem pairs co-referenced by one held-out
declaration; matched negatives (min-depth +-5, same-area flag, degree
bins); score = radius-2 cone overlap and multiscale ms; AUPRC-first.
"""
import glob
import json
from collections import defaultdict
import numpy as np
from merge_tree import load_common, load_edges

R = 4
NEG_PER_POS = 10
SEED = 20260908

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
es, ed = load_edges("GAPC")
name_id = {n: i for i, n in enumerate(names)}
pool_mask = (~gen) & (kind == 0) & (depth >= 11)
pool = np.where(pool_mask)[0]

odeg = np.zeros(len(depth), np.int32)
np.add.at(odeg, es, 1)
DEGBINS = np.array([0, 1, 2, 3, 6, 11, 10**9])
degbin_all = np.searchsorted(DEGBINS, odeg, side="right")

# load provenance
prov_files = sorted(glob.glob("/Users/sam/mathmap_data/prov/prov_*.json"))
decl_refs = {}
for pf in prov_files:
    d = json.load(open(pf))
    for rec in d["decls"]:
        nm = rec.get("name")
        if nm is None or nm not in name_id:
            continue
        refs = [name_id[r] for r in rec.get("refs", {}) if r in name_id]
        decl_refs[name_id[nm]] = refs
print(f"prov files: {len(prov_files)}  decls mapped: {len(decl_refs)}")

hold = set(decl_refs)
rng = np.random.default_rng(SEED)
adj = defaultdict(list)
for s, d in zip(es, ed):
    if s not in hold:
        adj[s].append(d)

pos = []
seen_pairs = set()
for t, refs in decl_refs.items():
    good = sorted({r for r in refs if pool_mask[r] and r != t})
    if len(good) < 2:
        continue
    # all pairs, capped at 6 per decl to avoid single-decl domination
    idx = np.arange(len(good))
    pairs = [(good[i], good[j]) for i in idx for j in idx[idx > i]]
    if len(pairs) > 6:
        pairs = [pairs[k] for k in rng.choice(len(pairs), 6, replace=False)]
    for p in pairs:
        if p not in seen_pairs:
            seen_pairs.add(p)
            pos.append(p)
print(f"provenance positive pairs: {len(pos)}")

by_key = defaultdict(list)
for i in pool:
    by_key[degbin_all[i]].append(i)
by_key = {k: np.array(v) for k, v in by_key.items()}
neg = []
for a, b in pos:
    md = int(min(depth[a], depth[b]))
    same = area[a] == area[b] and area[a] >= 0
    pa = by_key.get(degbin_all[a], pool)
    pb = by_key.get(degbin_all[b], pool)
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
        x, y = rng.choice(pool, 2)
        if x != y and abs(int(min(depth[x], depth[y])) - md) <= 5:
            neg.append((int(x), int(y))); got += 1

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
    """Tie-fair AP: expected value over random ordering within ties."""
    rng = np.random.default_rng(seed)
    n = len(scores_)
    aps = []
    for _ in range(nshuf):
        perm = rng.permutation(n)
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
    "n_pos": len(pos), "n_neg": len(neg),
    "prior": len(pos) / (len(pos) + len(neg)),
    "auprc_r2": average_precision(np.concatenate([pr2, nr2]), labels),
    "auprc_ms": average_precision(np.concatenate([pms, nms]), labels),
    "pos_kinship_r2": float((pr2 > 0).mean()),
    "neg_kinship_r2": float((nr2 > 0).mean()),
}
res["lift_r2"] = res["pos_kinship_r2"] / max(res["neg_kinship_r2"], 1e-9)
print(json.dumps(res, indent=1))
json.dump(res, open("../data/prov_validation.json", "w"), indent=1)
