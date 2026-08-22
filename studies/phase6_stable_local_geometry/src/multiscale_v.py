#!/usr/bin/env python3
"""GPT program Parts 2 + 3a.

Part 2: multiscale V-profile. For node pairs, compute the overlap of
their downward zoom-1 cones at every radius pair (ra, rb) in 1..4, and
record the FIRST TOUCH (minimal total drop ra+rb with nonzero overlap)
including its asymmetry |ra-rb| -- GPT's "asymmetric branch drop"
record. A mathematician relating a deep theorem to a shallow object
descends unequal distances; symmetric radius-2 kinship cannot see that.

Part 3a: holdout co-use validation upgraded to AUPRC-first reporting
with STRICTLY matched negatives (min-depth band, same/cross-area flag,
out-degree bin of both endpoints), 1:10 prior, 4 seeds. Scores compared:
  r1/r2/r3/r4  cumulative cone-overlap size at symmetric radius r
  ms           discounted multiscale score sum 2^-(da(c)+db(c))
  flat2        same r=2 overlap on the flat citation graph (E4_flat)

Non-circular as before: hold out 10% of proof artifacts, delete their
edges, predict the co-use inside the held-out proofs.
"""
import json
import sys
from collections import defaultdict
import numpy as np
from merge_tree import load_common, load_edges

R = 4
SEEDS = [20260904, 20260905, 20260906, 20260907]
NEG_PER_POS = 10
NPOS = 3000

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
es, ed = load_edges("GAPC")
fs, fd = load_edges("E4_flat")

pool_mask = (~gen) & (kind == 0) & (depth >= 11)
pool = np.where(pool_mask)[0]

# out-degree on the full (un-heldout) zoom1 graph, for matching bins
odeg = np.zeros(len(depth), np.int32)
np.add.at(odeg, es, 1)
DEGBINS = np.array([0, 1, 2, 3, 6, 11, 10**9])
degbin_all = np.searchsorted(DEGBINS, odeg, side="right")


def average_precision(scores, labels, nshuf=32, seed=0):
    """Tie-fair AP: expected value over random ordering within tied
    scores, estimated by averaging over random shuffles. A stable sort
    with positives listed first inflates AP badly when most scores tie
    at zero."""
    rng = np.random.default_rng(seed)
    n = len(scores)
    aps = []
    for _ in range(nshuf):
        perm = rng.permutation(n)
        order = perm[np.argsort(-scores[perm], kind="stable")]
        l = labels[order]
        tp = np.cumsum(l)
        prec = tp / (np.arange(n) + 1)
        aps.append((prec * l).sum() / max(l.sum(), 1))
    return float(np.mean(aps))


def rings_factory(adj, radius):
    cache = {}
    def rings(x):
        r = cache.get(x)
        if r is not None:
            return r
        seen = {x}
        frontier = [x]
        out = []
        for _ in range(radius):
            nxt = []
            for y in frontier:
                for z in adj.get(y, ()):
                    if z not in seen:
                        seen.add(z)
                        nxt.append(z)
            out.append(frozenset(nxt))
            frontier = nxt
        cache[x] = out
        return out
    return rings


def pair_profile(ra_rings, rb_rings):
    """4x4 cumulative overlap counts + node->(da,db) for common nodes."""
    da = {}
    for i, ring in enumerate(ra_rings):
        for c in ring:
            da[c] = i + 1
    touch = {}
    for j, ring in enumerate(rb_rings):
        for c in ring:
            if c in da:
                touch[c] = (da[c], j + 1)
    prof = np.zeros((R, R), np.int32)
    for (i, j) in touch.values():
        prof[i - 1 :, j - 1 :] += 1
    return prof, touch


def run(seed):
    rng = np.random.default_rng(seed)
    srcs = np.unique(es)
    hold = set(rng.choice(srcs, len(srcs) // 10, replace=False).tolist())
    adj = defaultdict(list)
    cocite = defaultdict(list)
    for s, d in zip(es, ed):
        if s in hold:
            cocite[s].append(d)
        else:
            adj[s].append(d)
    fadj = defaultdict(list)
    for s, d in zip(fs, fd):
        if s not in hold:
            fadj[s].append(d)

    ok = lambda x: pool_mask[x]
    pos = []
    for t, cs in cocite.items():
        good = [c for c in set(cs) if ok(c)]
        if len(good) >= 2:
            a, b = rng.choice(good, 2, replace=False)
            if a != b:
                pos.append((int(a), int(b)))
        if len(pos) >= NPOS:
            break

    # matched negatives: same min-depth band (+-5), same same-area flag,
    # same degree bin for both endpoints
    by_key = defaultdict(list)
    for i in pool:
        by_key[degbin_all[i]].append(i)
    by_key = {k: np.array(v) for k, v in by_key.items()}
    neg = []
    for a, b in pos:
        md = int(min(depth[a], depth[b]))
        same = area[a] == area[b] and area[a] >= 0
        ka, kb = degbin_all[a], degbin_all[b]
        pa, pb = by_key.get(ka, pool), by_key.get(kb, pool)
        got = 0
        tries = 0
        while got < NEG_PER_POS and tries < 4000:
            tries += 1
            x = int(pa[rng.integers(len(pa))])
            y = int(pb[rng.integers(len(pb))])
            if x == y:
                continue
            if abs(int(min(depth[x], depth[y])) - md) > 5:
                continue
            if (area[x] == area[y] and area[x] >= 0) != same:
                continue
            neg.append((x, y))
            got += 1
        while got < NEG_PER_POS:  # fallback: depth-matched only
            x, y = rng.choice(pool, 2)
            if x != y and abs(int(min(depth[x], depth[y])) - md) <= 5:
                neg.append((int(x), int(y)))
                got += 1

    rings = rings_factory(adj, R)
    frings = rings_factory(fadj, 2)

    def score_pairs(P):
        out = {k: [] for k in ("r1", "r2", "r3", "r4", "ms", "flat2")}
        touches = []
        for a, b in P:
            prof, touch = pair_profile(rings(a), rings(b))
            for r in range(1, R + 1):
                out["r%d" % r].append(int(prof[r - 1, r - 1]))
            ms = sum(2.0 ** -(i + j) for (i, j) in touch.values())
            out["ms"].append(ms)
            fa, fb = frings(a), frings(b)
            ca = fa[0] | fa[1]
            cb = fb[0] | fb[1]
            out["flat2"].append(len(ca & cb))
            if touch:
                ft = min(touch.values(), key=lambda ij: (ij[0] + ij[1], max(ij)))
                # V-dip at first touch: depth drop to deepest touching node
                # among minimal-total-drop touches
                tmin = ft[0] + ft[1]
                cand = [c for c, ij in touch.items() if ij[0] + ij[1] == tmin]
                vh = max(depth[c] for c in cand)
                touches.append((ft[0], ft[1], int(min(depth[a], depth[b])) - int(vh)))
            else:
                touches.append(None)
        return {k: np.array(v, float) for k, v in out.items()}, touches

    sp, tp_ = score_pairs(pos)
    sn, tn_ = score_pairs(neg)

    res = {"seed": seed, "n_pos": len(pos), "n_neg": len(neg)}
    labels = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    res["prior"] = len(pos) / (len(pos) + len(neg))
    for k in sp:
        res["auprc_" + k] = average_precision(
            np.concatenate([sp[k], sn[k]]), labels)
        res["posrate_" + k] = float((sp[k] > 0).mean())
        res["negrate_" + k] = float((sn[k] > 0).mean())
    # branch-drop record on positives
    ft = [t for t in tp_ if t]
    res["pos_touch_frac"] = len(ft) / len(pos)
    res["neg_touch_frac"] = sum(1 for t in tn_ if t) / len(neg)
    if ft:
        asym = np.array([abs(a - b) for a, b, _ in ft])
        tot = np.array([a + b for a, b, _ in ft])
        dip = np.array([d for _, _, d in ft])
        res["touch_sym"] = float((asym == 0).mean())
        res["touch_asym1"] = float((asym == 1).mean())
        res["touch_asym2p"] = float((asym >= 2).mean())
        res["touch_total_hist"] = {int(k): int(v) for k, v in
                                   zip(*np.unique(tot, return_counts=True))}
        res["median_total_drop"] = float(np.median(tot))
        res["median_vdip"] = float(np.median(dip))
    nf = [t for t in tn_ if t]
    if nf:
        nasym = np.array([abs(a - b) for a, b, _ in nf])
        res["neg_touch_sym"] = float((nasym == 0).mean())
        res["neg_touch_asym2p"] = float((nasym >= 2).mean())
        res["neg_median_total_drop"] = float(np.median([a + b for a, b, _ in nf]))
    return res


all_res = []
for seed in SEEDS:
    r = run(seed)
    all_res.append(r)
    print(json.dumps(r, indent=1), flush=True)

# aggregate
agg = {"seeds": SEEDS, "runs": all_res}
for k in ("auprc_r1", "auprc_r2", "auprc_r3", "auprc_r4", "auprc_ms",
          "auprc_flat2", "prior", "pos_touch_frac", "neg_touch_frac",
          "touch_sym", "touch_asym1", "touch_asym2p", "median_total_drop",
          "median_vdip"):
    vals = [r[k] for r in all_res if k in r]
    if vals:
        agg["mean_" + k] = float(np.mean(vals))
        agg["range_" + k] = [float(np.min(vals)), float(np.max(vals))]
json.dump(agg, open("../data/multiscale_v.json", "w"), indent=1)
print("\n=== AGGREGATE (4 seeds) ===")
for k in sorted(agg):
    if k.startswith("mean_"):
        print(f"{k[5:]:24s} {agg[k]:.4f}  range {agg['range_'+k[5:]]}")
