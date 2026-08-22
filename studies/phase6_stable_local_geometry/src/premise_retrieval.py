#!/usr/bin/env python3
"""Navigation benchmark v2: premise retrieval from the STATEMENT.

Setup: hold out 10% of proofs. For each held-out theorem, the query is
what exists BEFORE the proof: the theorem's name and its statement-world
citations S (in_stmt_world). The answers are its map moves (GAPC) that
are not already in the statement. Rank the whole theorem pool.

Methods (graph methods use only the holdout-blind graph):
  lamS   sum over s in S of co-citation counts lam(s, c)
  kinS   sum over the 5 most specific seeds of radius-2 discounted
         V-kinship to the candidate
  l+k    scaled 0.5/0.5 combination
  text   name-token Jaccard vs target name + S names (no graph)
  pop    global in-degree ranking
  rand   analytic

Tie-fair expected ranks throughout. This is the premise-selection task:
first direct evidence bearing on "does the map help PROVE things".
"""
import json
import os
from collections import defaultdict
import numpy as np
from merge_tree import load_common, load_edges

SEED = 20260913
NQUERIES = 1500
KS = (10, 100)
HUB_CAP = 2000
TOKEN_CAP = 5000
MAX_SEEDS = 5
P5DATA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "phase5_multiscale_navigation", "data"))

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
es, ed = load_edges("GAPC")
pool_mask = (~gen) & (kind == 0) & (depth >= 11)
NPOOL = int(pool_mask.sum())

# statement world per artifact target
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
print(f"targets with statement world: {len(stmt_of)}")

rng = np.random.default_rng(SEED)
srcs = np.unique(es)
hold = set(rng.choice(srcs, len(srcs) // 10, replace=False).tolist())
adj = defaultdict(list)
radj = defaultdict(list)
moves_of = defaultdict(list)
for s, d in zip(es, ed):
    if s in hold:
        moves_of[s].append(d)
    else:
        adj[s].append(d)
        radj[d].append(s)

# co-citation counts over ALL cited items per non-held-out proof
lam_nbrs = defaultdict(dict)
by_src = defaultdict(list)
for s, d in zip(es, ed):
    if s not in hold:
        by_src[s].append(d)
npairs = 0
for s, ms in by_src.items():
    ms = sorted(set(ms))[:20]
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            a, b = ms[i], ms[j]
            if pool_mask[b]:
                lam_nbrs[a][b] = lam_nbrs[a].get(b, 0) + 1
            if pool_mask[a]:
                lam_nbrs[b][a] = lam_nbrs[b].get(a, 0) + 1
            npairs += 1
print(f"co-citation pairs: {npairs}")

indeg = np.zeros(len(depth), np.int64)
for d, ss in radj.items():
    indeg[d] = len(ss)
pop_order = {int(x): r for r, x in enumerate(
    sorted(np.where(pool_mask)[0], key=lambda x: -indeg[x]))}

def tokens(n):
    return {t.lower() for t in n.replace("'", "").split(".") if t and not t.isdigit()}
tok_index = defaultdict(list)
toks_of = {}
for i in np.where(pool_mask)[0]:
    ts = tokens(names[i])
    toks_of[int(i)] = ts
    for t in ts:
        tok_index[t].append(int(i))
skipped_tokens = {t for t, v in tok_index.items() if len(v) > TOKEN_CAP}

def cone2(x):
    c1 = set(adj.get(x, ()))
    c2 = set()
    for y in c1:
        c2.update(adj.get(y, ()))
    c2 -= c1
    c2.discard(x)
    return c1, c2

def kin2_scores(a):
    c1, c2 = cone2(a)
    da = {}
    for n in c1: da[n] = 1
    for n in c2: da[n] = 2
    scores = defaultdict(float)
    for n, dan in da.items():
        up1 = radj.get(n, ())
        if len(up1) > HUB_CAP:
            continue
        for c in up1:
            scores[c] += 2.0 ** -(dan + 1)
        for m in up1:
            up2 = radj.get(m, ())
            if len(up2) > HUB_CAP:
                continue
            for c in up2:
                scores[c] += 2.0 ** -(dan + 2) * 0.5
    scores.pop(a, None)
    return scores

def expected_metrics(score_map, answers, fixed_rank=None):
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
            ties = int((vals == sb).sum())
        else:
            sg = nz
            ties = NPOOL - nz
        for k in KS:
            if sg >= k:
                c = 0.0
            elif sg + ties <= k:
                c = 1.0
            else:
                c = (k - sg) / ties
            out.setdefault(k, []).append(c)
        out.setdefault("rr", []).append(1.0 / (sg + (ties + 1) / 2.0))
    return out

# queries: held-out proofs with a usable statement world and >=1 answer
queries = []
for s, ds in moves_of.items():
    S = stmt_of.get(int(s), set())
    S = {x for x in S if x in adj or x in lam_nbrs or pool_mask[x]}
    answers = sorted({d for d in ds if pool_mask[d]} - S)
    if S and answers:
        queries.append((int(s), sorted(S), answers))
rng.shuffle(queries)
queries = queries[:NQUERIES]
print(f"queries: {len(queries)}")

methods = ["lamS", "kinS", "l+k", "text", "pop"]
acc = {m: defaultdict(list) for m in methods}
for qi, (t, S, answers) in enumerate(queries):
    # lamS
    sl = defaultdict(float)
    for s in S:
        for c, v in lam_nbrs.get(s, {}).items():
            sl[c] += v
    # kinS from most specific seeds (lowest in-degree)
    seeds = sorted(S, key=lambda x: indeg[x])[:MAX_SEEDS]
    sk = defaultdict(float)
    for s in seeds:
        for c, v in kin2_scores(s).items():
            if pool_mask[c]:
                sk[c] += v
    for d in (sl, sk):
        for x in S:
            d.pop(x, None)
        d.pop(t, None)
    ml = max(sl.values()) if sl else 1.0
    mk = max(sk.values()) if sk else 1.0
    slk = defaultdict(float)
    for c, v in sl.items(): slk[c] += 0.5 * v / ml
    for c, v in sk.items(): slk[c] += 0.5 * v / mk
    # text
    ta = tokens(names[t])
    for s in S:
        ta |= tokens(names[s])
    st = defaultdict(int)
    for tok in ta:
        if tok in skipped_tokens or tok not in tok_index:
            continue
        for c in tok_index[tok]:
            st[c] += 1
    st.pop(int(t), None)
    st2 = {c: v / (len(ta) + len(toks_of[c]) - v) for c, v in st.items()}
    for m, sm in (("lamS", sl), ("kinS", sk), ("l+k", slk), ("text", st2)):
        em = expected_metrics(sm, answers)
        for k, v in em.items():
            acc[m][k].extend(v)
    em = expected_metrics(None, answers, fixed_rank=pop_order)
    for k, v in em.items():
        acc["pop"][k].extend(v)
    if (qi + 1) % 200 == 0:
        print(f"  {qi+1}/{len(queries)}", flush=True)

res = {"n_queries": len(queries), "pool": NPOOL,
       "rand_recall": {str(k): k / NPOOL for k in KS}}
for m in methods:
    res[m] = {("recall@%d" % k if isinstance(k, int) else "mrr"):
              float(np.mean(acc[m][k])) for k in list(KS) + ["rr"]}
print(json.dumps(res, indent=1))
json.dump(res, open("../data/premise_retrieval.json", "w"), indent=1)
