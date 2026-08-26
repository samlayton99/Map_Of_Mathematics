#!/usr/bin/env python
"""The rolodex, measured: premise retrieval over all of Mathlib, no ML.

Task: given only a theorem's STATEMENT (its direct type-dependencies), rank
all 771k constants so that the premises its proof actually cites land in a
small shortlist.  Ground truth is exact (the kernel's value-deps).  All
retrievers are graph-structural and evaluated leave-one-out; this is the
floor any learned policy must beat, and a measurement of how much of the
"mathematical rolodex" problem the static dependency graph already solves.

Retrievers:
  prior    global premise frequency (how often c is cited by any proof)
  cousage  statement->premise co-occurrence: score(c) = sum over statement
           constants s of idf(s) * #{proofs with s in statement, c in
           premises}, own-proof contribution subtracted
  peers    nearest neighbors by rare shared statement constants; premises
           pooled from the top peers, similarity-weighted
  fused    reciprocal-rank fusion of the three

Targets: "math premises" = cited premises that are unclassified theorems
(median 2 per proof - the actual rolodex entries), split into expected
(inside the statement cone) and surprise (outside it: the moves).

Run: ~/venv/general_ml/bin/python rolodex.py [--test-n 2000] [--seed 0]
Writes tools/output/rolodex_eval.json
"""
import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import scipy.sparse as sp

from atlas import load_dump, theorem_roots, BIG

OUT = Path(__file__).resolve().parent / "output"
KS = (8, 16, 64, 256, 1024)
DF_CAP = 10_000          # statement constants with df above this carry no signal
RARE_DF = 1_000          # "rare" features used for peer matching
N_PEERS = 64


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


# ----------------------------------------------------------------- statistics

def stmt_deps(a, r):
    return a.t_indices[a.t_indptr[r]:a.t_indptr[r + 1]]


def proof_deps(a, r):
    return a.v_indices[a.v_indptr[r]:a.v_indptr[r + 1]]


def build_stats(a, roots, chunk=20_000):
    """df over statement constants, global premise prior, and the
    statement->premise co-usage matrix (rows limited to df<=DF_CAP)."""
    n = a.n
    df = np.zeros(n, dtype=np.int64)
    prior = np.zeros(n, dtype=np.int64)
    for r in roots:
        df[np.unique(stmt_deps(a, r))] += 1
        prior[np.unique(proof_deps(a, r))] += 1
    keep = df <= DF_CAP        # informative statement rows

    partials = []
    for lo in range(0, len(roots), chunk):
        keys = []
        for r in roots[lo:lo + chunk]:
            s = np.unique(stmt_deps(a, r))
            s = s[keep[s]]
            c = np.unique(proof_deps(a, r))
            if len(s) == 0 or len(c) == 0:
                continue
            k = (s.astype(np.int64)[:, None] * n + c[None, :]).ravel()
            keys.append(k)
        if not keys:
            continue
        k = np.concatenate(keys)
        u, cnt = np.unique(k, return_counts=True)
        partials.append((u, cnt.astype(np.int32)))
        log(f"  co-usage chunk {lo + chunk}/{len(roots)}: "
            f"{len(u):,} unique pairs")
    allk = np.concatenate([p[0] for p in partials])
    allc = np.concatenate([p[1] for p in partials])
    del partials
    order = np.argsort(allk, kind="stable")
    allk, allc = allk[order], allc[order]
    uk, start = np.unique(allk, return_index=True)
    sums = np.add.reduceat(allc.astype(np.int64), start)
    rows = (uk // n).astype(np.int32)
    cols = (uk % n).astype(np.int32)
    M = sp.csr_matrix((sums.astype(np.int32), (rows, cols)), shape=(n, n))
    log(f"co-usage matrix: {M.nnz:,} nonzeros")
    return df, prior, M


def build_inverted(a, roots, df):
    """Inverted index: rare statement constant -> list of root positions."""
    inv = defaultdict(list)
    for pos, r in enumerate(roots):
        for s in np.unique(stmt_deps(a, r)):
            if df[s] <= RARE_DF:
                inv[int(s)].append(pos)
    return inv


# ----------------------------------------------------------------- retrievers

def score_prior(a, r, prior):
    s = prior.astype(np.float64).copy()
    s[np.unique(proof_deps(a, r))] -= 1.0        # leave-one-out
    return s


def score_cousage(a, r, df, M):
    s_ids = np.unique(stmt_deps(a, r))
    s_ids = s_ids[df[s_ids] <= DF_CAP]
    if len(s_ids) == 0:
        return None
    w = 1.0 / np.log1p(df[s_ids].astype(np.float64))
    vec = (sp.diags(w) @ M[s_ids]).sum(axis=0)
    vec = np.asarray(vec).ravel()
    own = np.unique(proof_deps(a, r))            # leave-one-out correction
    vec[own] -= w.sum()
    return vec


def score_peers(a, r, roots, df, inv, self_pos):
    sims = defaultdict(float)
    for s in np.unique(stmt_deps(a, r)):
        if df[s] <= RARE_DF and int(s) in inv:
            idf = 1.0 / np.log1p(df[s])
            for pos in inv[int(s)]:
                if pos != self_pos:
                    sims[pos] += idf
    if not sims:
        return None
    top = sorted(sims.items(), key=lambda kv: -kv[1])[:N_PEERS]
    vec = np.zeros(a.n)
    for pos, sim in top:
        vec[np.unique(proof_deps(a, roots[pos]))] += sim
    return vec


def rrf(rank_lists, n, k0=60):
    s = np.zeros(n)
    for ranks in rank_lists:
        if ranks is None:
            continue
        s[ranks] += 1.0 / (k0 + np.arange(1, len(ranks) + 1))
    return s


def topk_ids(vec, K, exclude):
    v = vec.copy()
    v[exclude] = -np.inf
    if K >= len(v):
        return np.argsort(-v)
    ids = np.argpartition(-v, K)[:K]
    return ids[np.argsort(-v[ids])]


# ----------------------------------------------------------------- evaluation

def evaluate(a, roots, test_pos, df, prior, M, inv):
    maxK = max(KS)
    isthm = np.zeros(a.n, dtype=bool)
    for i in range(a.n):
        if a.kind[i] == "theorem" and not a.cls[i]:
            isthm[i] = True

    methods = ("prior", "cousage", "peers", "fused")
    hits = {m: {K: [] for K in KS} for m in methods}          # macro recall
    hits_surprise = {m: {K: [] for K in KS} for m in methods}
    full_hit = {m: {K: 0 for K in KS} for m in methods}
    n_eval = n_surprise_eval = 0

    for j, pos in enumerate(test_pos):
        r = roots[pos]
        prem = np.unique(proof_deps(a, r))
        target = prem[isthm[prem]]
        if len(target) == 0:
            continue
        a_s = a.cone_from(stmt_deps(a, r))
        surprise = np.array([c for c in target if c not in a_s], dtype=np.int64)

        vec_p = score_prior(a, r, prior)
        vec_c = score_cousage(a, r, df, M)
        vec_k = score_peers(a, r, roots, df, inv, pos)
        excl = np.array([r])
        ids = {}
        ids["prior"] = topk_ids(vec_p, maxK, excl)
        ids["cousage"] = topk_ids(vec_c, maxK, excl) if vec_c is not None else None
        ids["peers"] = topk_ids(vec_k, maxK, excl) if vec_k is not None else None
        fused_vec = rrf([ids["prior"], ids["cousage"], ids["peers"]], a.n)
        ids["fused"] = topk_ids(fused_vec, maxK, excl)

        n_eval += 1
        if len(surprise):
            n_surprise_eval += 1
        for m in methods:
            got = ids[m]
            got_set = set(got.tolist()) if got is not None else set()
            for K in KS:
                topset = set(got[:K].tolist()) if got is not None else set()
                rec = sum(1 for c in target if c in topset) / len(target)
                hits[m][K].append(rec)
                if rec == 1.0:
                    full_hit[m][K] += 1
                if len(surprise):
                    rec_s = sum(1 for c in surprise if c in topset) / len(surprise)
                    hits_surprise[m][K].append(rec_s)
        if (j + 1) % 200 == 0:
            log(f"  evaluated {j + 1}/{len(test_pos)}")

    res = {"n_eval": n_eval, "n_with_surprise": n_surprise_eval,
           "recall": {}, "recall_surprise": {}, "full_rolodex_rate": {}}
    for m in methods:
        res["recall"][m] = {K: round(float(np.mean(hits[m][K])), 4) for K in KS}
        res["recall_surprise"][m] = {
            K: round(float(np.mean(hits_surprise[m][K])), 4) for K in KS}
        res["full_rolodex_rate"][m] = {
            K: round(full_hit[m][K] / n_eval, 4) for K in KS}
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)

    log("loading atlas...")
    a = load_dump()
    roots = theorem_roots(a)
    log(f"{len(roots):,} roots")

    log("building statistics (df, prior, co-usage)...")
    df, prior, M = build_stats(a, roots)
    log("building inverted index for peers...")
    inv = build_inverted(a, roots, df)

    rng = np.random.default_rng(args.seed)
    test_pos = rng.choice(len(roots), size=args.test_n * 2, replace=False)
    # keep those with at least one math premise
    isthm = {i for i in range(a.n) if a.kind[i] == "theorem" and not a.cls[i]}
    keep = [int(p) for p in test_pos
            if any(int(c) in isthm for c in proof_deps(a, roots[p]))]
    test_pos = keep[:args.test_n]
    log(f"evaluating {len(test_pos)} test theorems...")

    res = evaluate(a, roots, test_pos, df, prior, M, inv)
    res["config"] = {"df_cap": DF_CAP, "rare_df": RARE_DF, "n_peers": N_PEERS,
                     "seed": args.seed, "ks": list(KS)}
    OUT.mkdir(exist_ok=True)
    (OUT / "rolodex_eval.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
