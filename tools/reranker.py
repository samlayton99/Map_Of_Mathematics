#!/usr/bin/env python
"""A modest learned reranker over the structural cascade, honest splits.

Pipeline per theorem: accessibility-masked candidate pool = union of the
top-256 candidates from each structural retriever (prior / co-usage /
peers) -> logistic-regression reranker over cheap features -> recall@K.

Trained ONLY on module-holdout train theorems (statistics likewise); hard
negatives are the retrievers' own high-scoring non-cited candidates.
Evaluated on the module-holdout test set and its novel-premise subset -
the splits where nothing about the test modules leaks into training.

This is the smallest possible test of the vision's claim that a learned
concentrator over a structural cascade closes the shortlist gap.

Run: ~/venv/general_ml/bin/python reranker.py
Writes tools/output/reranker_eval.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

from atlas import load_dump, theorem_roots
from accessibility import Accessibility
from heads_util import load_heads, refined_key
import rolodex as R
from rolodex2 import score_cousage_noloo, score_peers_masked, HOLDOUT_FRAC

OUT = Path(__file__).resolve().parent / "output"
KS = (8, 16, 64, 256)
POOL_K = 256
N_TRAIN = 8000
N_TEST = 1200


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def candidate_pool(vecs, amask, r, k=POOL_K):
    excl = ~amask.copy()
    excl[r] = True
    pool = set()
    for v in vecs:
        if v is None:
            continue
        vv = v.copy()
        vv[excl] = -np.inf
        ids = np.argpartition(-vv, k)[:k]
        pool.update(int(i) for i in ids[vv[ids] > 0])
    return np.array(sorted(pool), dtype=np.int64)


def features(a, r, cands, vec_p, vec_c, vec_k, ch, ca, keys, ns_of, depth):
    f = np.zeros((len(cands), 8))
    gkey = keys.get(a.names[r])
    gns = ns_of[r]
    for i, c in enumerate(cands):
        f[i, 0] = np.log1p(vec_p[c]) if vec_p is not None else 0
        f[i, 1] = np.log1p(max(vec_c[c], 0)) if vec_c is not None else 0
        f[i, 2] = np.log1p(vec_k[c]) if vec_k is not None else 0
        ckey = keys.get(a.names[c])
        f[i, 3] = 1.0 if (gkey and ckey == gkey) else 0.0
        f[i, 4] = 1.0 if (gkey and ckey and ckey[0] == gkey[0]) else 0.0
        f[i, 5] = depth[c] / 100.0
        f[i, 6] = abs(int(depth[c]) - int(depth[r])) / 100.0
        f[i, 7] = 1.0 if ns_of[c] == gns else 0.0
    return f


def main():
    log("loading atlas, accessibility, heads...")
    a = load_dump()
    acc = Accessibility(a)
    ch, ca, _ = load_heads()
    keys = {}
    for nm in ch:
        k = refined_key(ch, ca, nm)
        if k:
            keys[nm] = k
    ns_of = [n.split(".", 1)[0] for n in a.names]
    depth = a.depth
    roots = theorem_roots(a)
    isthm = np.zeros(a.n, dtype=bool)
    for i in range(a.n):
        if a.kind[i] == "theorem" and not a.cls[i]:
            isthm[i] = True

    # ---- module holdout split (same seed as rolodex2)
    rng = np.random.default_rng(1)
    root_mods = acc.mod_of[np.array(roots)]
    mathlib_mods = [i for i, nm in enumerate(acc.mod_names)
                    if nm.startswith("Mathlib.")]
    held = set(int(x) for x in
               rng.choice(mathlib_mods,
                          size=int(len(mathlib_mods) * HOLDOUT_FRAC),
                          replace=False))
    test_all = [p for p in range(len(roots)) if int(root_mods[p]) in held]
    train_pos = [p for p in range(len(roots)) if int(root_mods[p]) not in held]
    rng.shuffle(test_all)
    test_pos = [p for p in test_all
                if isthm[R.proof_deps(a, roots[p])].any()][:N_TEST]
    train_roots = [roots[p] for p in train_pos]
    pos_in_train = {p: i for i, p in enumerate(train_pos)}
    log(f"stats on {len(train_roots):,} train roots...")
    df, prior, M = R.build_stats(a, train_roots)
    inv = R.build_inverted(a, train_roots, df)
    train_cited = np.zeros(a.n, dtype=bool)
    for r in train_roots:
        train_cited[np.unique(R.proof_deps(a, r))] = True

    def vectors(r, amask, self_pos):
        vp = prior.astype(np.float64)
        vc = score_cousage_noloo(a, r, df, M)
        vk = score_peers_masked(a, r, train_roots, df, inv, self_pos, amask)
        return vp, vc, vk

    # ---- training data from train roots (leave-one-out inside train)
    log("building training pairs...")
    rng2 = np.random.default_rng(7)
    sample = rng2.choice(len(train_pos), size=N_TRAIN * 2, replace=False)
    X, y = [], []
    used = 0
    for si in sample:
        p = train_pos[int(si)]
        r = roots[p]
        prem = np.unique(R.proof_deps(a, r))
        amask = acc.mask(r)
        if amask is None:
            continue
        target = prem[isthm[prem] & amask[prem]]
        if len(target) == 0:
            continue
        # train theorems ARE in the stats: leave-one-out both channels
        vp = prior.astype(np.float64)
        vp[prem] -= 1.0
        vc = R.score_cousage(a, r, df, M)      # LOO variant
        vk = score_peers_masked(a, r, train_roots, df, inv,
                                pos_in_train[p], amask)
        pool = candidate_pool([vp, vc, vk], amask, r)
        if len(pool) == 0:
            continue
        tset = set(int(t) for t in target)
        fx = features(a, r, pool, vp, vc, vk, ch, ca, keys, ns_of, depth)
        lab = np.array([1 if int(c) in tset else 0 for c in pool])
        # keep all positives + up to 24 hard negatives
        posi = np.where(lab == 1)[0]
        negi = np.where(lab == 0)[0][:24]
        keep = np.concatenate([posi, negi])
        X.append(fx[keep])
        y.append(lab[keep])
        used += 1
        if used >= N_TRAIN:
            break
        if used % 500 == 0:
            log(f"  train theorems {used}/{N_TRAIN}")
    X = np.vstack(X)
    y = np.concatenate(y)
    log(f"training on {len(y):,} pairs ({y.sum():,} positives)...")
    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced")
    clf.fit(X, y)
    log(f"coefs: {np.round(clf.coef_[0], 3).tolist()}")

    # ---- evaluation on holdout test (+ novel subset)
    log(f"evaluating on {len(test_pos)} held-out theorems...")
    rec = {K: [] for K in KS}
    rec_base = {K: [] for K in KS}       # best structural (peers) baseline
    rec_novel = {K: [] for K in KS}
    pool_hit = []                        # was the answer even in the pool?
    n_eval = 0
    for j, p in enumerate(test_pos):
        r = roots[p]
        amask = acc.mask(r)
        if amask is None:
            continue
        prem = np.unique(R.proof_deps(a, r))
        target = prem[isthm[prem] & amask[prem]]
        if len(target) == 0:
            continue
        vp, vc, vk = vectors(r, amask, None)
        pool = candidate_pool([vp, vc, vk], amask, r)
        if len(pool) == 0:
            continue
        tset = set(int(t) for t in target)
        fx = features(a, r, pool, vp, vc, vk, ch, ca, keys, ns_of, depth)
        score = clf.predict_proba(fx)[:, 1]
        order = pool[np.argsort(-score)]
        # structural baseline: peers ranking on the same pool
        if vk is not None:
            border = pool[np.argsort(-vk[pool])]
        else:
            border = pool[np.argsort(-vp[pool])]
        novel = bool((~train_cited[target]).any())
        n_eval += 1
        pool_hit.append(sum(1 for t in tset if t in set(pool.tolist()))
                        / len(tset))
        for K in KS:
            top = set(order[:K].tolist())
            btop = set(border[:K].tolist())
            rc = sum(1 for t in tset if t in top) / len(tset)
            rb = sum(1 for t in tset if t in btop) / len(tset)
            rec[K].append(rc)
            rec_base[K].append(rb)
            if novel:
                rec_novel[K].append(rc)
        if (j + 1) % 200 == 0:
            log(f"  {j + 1}/{len(test_pos)}")

    out = {
        "n_eval": n_eval,
        "pool_recall_ceiling": round(float(np.mean(pool_hit)), 4),
        "reranker_recall": {K: round(float(np.mean(rec[K])), 4) for K in KS},
        "structural_baseline_recall": {K: round(float(np.mean(rec_base[K])), 4)
                                       for K in KS},
        "reranker_recall_novel_premise": {
            K: round(float(np.mean(rec_novel[K])), 4) for K in KS}
        if rec_novel[KS[0]] else None,
        "n_novel": len(rec_novel[KS[0]]),
        "features": ["log_prior", "log_cousage", "log_peers", "refined_key_match",
                     "head_match", "depth", "depth_gap", "same_namespace"],
        "coefs": np.round(clf.coef_[0], 4).tolist(),
        "train_pairs": int(len(y)),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "reranker_eval.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
