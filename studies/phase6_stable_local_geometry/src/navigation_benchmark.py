#!/usr/bin/env python3
"""GPT program Part 4 (v1): navigation benchmark -- next-lemma retrieval.

Task: a proof is held out. Given ONE of its map moves (a), rank the full
theorem pool for its OTHER moves (B). This is the retrieval form of the
co-use validation: not "do co-used pairs score high" but "can you FIND
the partner from 300k candidates".

Methods (all built on the holdout-blind graph):
  kin2   V-kinship: discounted shared-cone overlap at radius <= 2
  lam    Lambda co-use counts from non-held-out proofs' move sets
  k+l    0.5/0.5 rank-free score sum of kin2 (scaled) and lam (scaled)
  flat   co-use counts on the FLAT citation graph (E4_flat)
  text   name-token Jaccard (text baseline, no graph)
  pop    global in-degree popularity (fixed ranking)
  rand   analytic: expected recall@k = k / |pool|

Scoring is tie-fair: expected rank under random tie ordering; recall@k
uses fractional credit when the answer ties across the k boundary.
Hub caps (in-degree > 2000 not expanded in reverse BFS; tokens in > 5000
names skipped) are logged, not hidden.
"""
import json
from collections import defaultdict
import numpy as np
from merge_tree import load_common, load_edges

SEED = 20260909
NQUERIES = 1500
KS = (10, 100)
HUB_CAP = 2000
TOKEN_CAP = 5000
MAX_MOVES_PER_SRC = 20

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
es, ed = load_edges("GAPC")
fs, fd = load_edges("E4_flat")
pool_mask = (~gen) & (kind == 0) & (depth >= 11)
NPOOL = int(pool_mask.sum())
print(f"pool: {NPOOL}")

rng = np.random.default_rng(SEED)
srcs = np.unique(es)
hold = set(rng.choice(srcs, len(srcs) // 10, replace=False).tolist())

adj = defaultdict(list)      # forward: proof -> cited moves
radj = defaultdict(list)     # reverse: theorem -> citing proofs
moves_of = defaultdict(list)  # held-out proof -> moves
for s, d in zip(es, ed):
    if s in hold:
        moves_of[s].append(d)
    else:
        adj[s].append(d)
        radj[d].append(s)

# Lambda co-use pair counts from non-held-out move sets
lam = defaultdict(int)
by_src = defaultdict(list)
for s, d in zip(es, ed):
    if s not in hold and pool_mask[d]:
        by_src[s].append(d)
for s, ms in by_src.items():
    ms = sorted(set(ms))[:MAX_MOVES_PER_SRC]
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            lam[(ms[i], ms[j])] += 1
print(f"lambda pairs: {len(lam)}")

# flat co-use pair counts
flam = defaultdict(int)
fby = defaultdict(list)
for s, d in zip(fs, fd):
    if s not in hold and pool_mask[d]:
        fby[s].append(d)
for s, ms in fby.items():
    ms = sorted(set(ms))
    if len(ms) > MAX_MOVES_PER_SRC:
        ms = [ms[k] for k in np.random.default_rng(s).choice(
            len(ms), MAX_MOVES_PER_SRC, replace=False)]
        ms = sorted(ms)
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            flam[(ms[i], ms[j])] += 1
print(f"flat pairs: {len(flam)}")

lam_nbrs = defaultdict(dict)
for (a, b), c in lam.items():
    lam_nbrs[a][b] = c
    lam_nbrs[b][a] = c
flam_nbrs = defaultdict(dict)
for (a, b), c in flam.items():
    flam_nbrs[a][b] = c
    flam_nbrs[b][a] = c

# popularity (fixed): in-degree on holdout-blind GAPC
indeg = np.zeros(len(depth), np.int64)
for d, ss in radj.items():
    indeg[d] = len(ss)
pop_order = {int(x): r for r, x in enumerate(
    sorted(np.where(pool_mask)[0], key=lambda x: -indeg[x]))}

# name-token inverted index over the pool
def tokens(n):
    return {t.lower() for t in n.replace("'", "").split(".") if t and not t.isdigit()}
tok_index = defaultdict(list)
pool_ids = np.where(pool_mask)[0]
toks_of = {}
for i in pool_ids:
    ts = tokens(names[i])
    toks_of[int(i)] = ts
    for t in ts:
        tok_index[t].append(int(i))
skipped_tokens = {t for t, v in tok_index.items() if len(v) > TOKEN_CAP}
print(f"tokens skipped as stopwords (> {TOKEN_CAP} names): {len(skipped_tokens)}")

def cone2(x):
    c1 = set(adj.get(x, ()))
    c2 = set()
    for y in c1:
        c2.update(adj.get(y, ()))
    c2 -= c1
    c2.discard(x)
    return c1, c2

hub_skips = 0
def kin2_scores(a):
    """candidate -> ms score restricted to radius 2 both sides."""
    global hub_skips
    c1, c2 = cone2(a)
    da = {}
    for n in c1: da[n] = 1
    for n in c2: da[n] = 2
    scores = defaultdict(float)
    for n, dan in da.items():
        up1 = radj.get(n, ())
        if len(up1) > HUB_CAP:
            hub_skips += 1
            continue
        for c in up1:
            scores[c] += 2.0 ** -(dan + 1)
        for m in up1:
            up2 = radj.get(m, ())
            if len(up2) > HUB_CAP:
                continue
            # c has n at depth 2 via m? only if n not already at depth 1
            # from c; we accept the approximation (upper path length 2)
            for c in up2:
                scores[c] += 2.0 ** -(dan + 2) * 0.5  # discounted approx
    scores.pop(a, None)
    return scores

def text_scores(a):
    ta = toks_of.get(int(a)) or tokens(names[a])
    scores = defaultdict(int)
    for t in ta:
        if t in skipped_tokens or t not in tok_index:
            continue
        for c in tok_index[t]:
            scores[c] += 1
    scores.pop(int(a), None)
    return {c: v / (len(ta) + len(toks_of[c]) - v) for c, v in scores.items()}

def expected_metrics(score_map, answers, fixed_rank=None):
    """tie-fair expected recall@k and reciprocal rank (midpoint)."""
    out = {}
    if fixed_rank is not None:
        for b in answers:
            r = fixed_rank.get(int(b))
            for k in KS:
                out.setdefault(k, []).append(1.0 if r is not None and r < k else 0.0)
            out.setdefault("rr", []).append(1.0 / (r + 1) if r is not None else 0.0)
        return out
    vals = np.array(list(score_map.values())) if score_map else np.array([])
    nz = len(vals)
    for b in answers:
        sb = score_map.get(int(b), 0.0)
        if sb > 0:
            sg = int((vals > sb).sum())
            ties = int((vals == sb).sum())  # includes b
        else:
            sg = nz
            ties = NPOOL - nz  # all zero-scored pool members tie
        for k in KS:
            if sg >= k:
                c = 0.0
            elif sg + ties <= k:
                c = 1.0
            else:
                c = (k - sg) / ties
            out.setdefault(k, []).append(c)
        mid = sg + (ties + 1) / 2.0
        out.setdefault("rr", []).append(1.0 / mid)
    return out

# queries
held = [(s, sorted({d for d in ds if pool_mask[d]}))
        for s, ds in moves_of.items()]
held = [(s, ms) for s, ms in held if len(ms) >= 2]
rng.shuffle(held)
held = held[:NQUERIES]
print(f"queries: {len(held)}")

methods = ["kin2", "lam", "k+l", "flat", "text", "pop"]
acc = {m: defaultdict(list) for m in methods}
for qi, (s, ms) in enumerate(held):
    a = ms[rng.integers(len(ms))]
    answers = [b for b in ms if b != a]
    sk = kin2_scores(a)
    sl = {c: float(v) for c, v in lam_nbrs.get(a, {}).items()}
    mk = max(sk.values()) if sk else 1.0
    ml = max(sl.values()) if sl else 1.0
    skl = defaultdict(float)
    for c, v in sk.items(): skl[c] += 0.5 * v / mk
    for c, v in sl.items(): skl[c] += 0.5 * v / ml
    sf = {c: float(v) for c, v in flam_nbrs.get(a, {}).items()}
    st = text_scores(a)
    for m, sm in (("kin2", sk), ("lam", sl), ("k+l", skl),
                  ("flat", sf), ("text", st)):
        em = expected_metrics(sm, answers)
        for k, v in em.items():
            acc[m][k].extend(v)
    em = expected_metrics(None, answers, fixed_rank=pop_order)
    for k, v in em.items():
        acc["pop"][k].extend(v)
    if (qi + 1) % 200 == 0:
        print(f"  {qi+1}/{len(held)}", flush=True)

res = {"n_queries": len(held), "pool": NPOOL, "hub_skips": hub_skips,
       "rand_recall": {str(k): k / NPOOL for k in KS}}
for m in methods:
    res[m] = {("recall@%d" % k if isinstance(k, int) else "mrr"):
              float(np.mean(acc[m][k])) for k in list(KS) + ["rr"]}
print(json.dumps(res, indent=1))
json.dump(res, open("../data/navigation_benchmark.json", "w"), indent=1)
