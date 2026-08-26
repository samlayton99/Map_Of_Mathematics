#!/usr/bin/env python
"""Rolodex benchmark v2: accessibility-masked, multi-split premise retrieval.

Fixes to v1 (tools/rolodex.py), per review:
  1. Candidates are masked to the theorem's LEGAL premise universe -
     transitively imported modules plus earlier declarations in its own
     module (from mathrecord moddump).  v1 ranked all 771k constants,
     including declarations that do not exist at the theorem's location.
  2. Peer proofs must themselves be accessible to count as knowledge.
  3. Three splits:
       random          seeded random test set, leave-one-out stats
                       (residual caveat: co-usage counts still include
                       proofs from unimported "future" modules)
       module_holdout  held-out modules; all statistics rebuilt from the
                       remaining modules only - no future information
       novel_premise   module_holdout test theorems citing at least one
                       premise no train proof ever cited (hard subset)
  4. Targets = accessible cited math premises; the (tiny) violation rate
     where a cited premise falls outside the computed universe is reported
     as a validation of the accessibility computation itself.

Run: ~/venv/general_ml/bin/python rolodex2.py
Writes tools/output/rolodex_eval_v2.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

from atlas import load_dump, theorem_roots
from accessibility import Accessibility
import rolodex as R

OUT = Path(__file__).resolve().parent / "output"
KS = (8, 16, 64, 256, 1024)
HOLDOUT_FRAC = 0.08


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def eval_split(a, acc, roots, test_pos, df, prior, M, inv, isthm,
               train_cited=None, loo=True):
    maxK = max(KS)
    methods = ("prior", "cousage", "peers", "fused")
    hits = {m: {K: [] for K in KS} for m in methods}
    full = {m: {K: 0 for K in KS} for m in methods}
    n_eval = 0
    viol = tot_target = 0
    novel_rows = []

    for j, pos in enumerate(test_pos):
        r = roots[pos]
        amask = acc.mask(r)
        if amask is None:
            continue
        prem = np.unique(R.proof_deps(a, r))
        target_all = prem[isthm[prem]]
        tot_target += len(target_all)
        target = target_all[amask[target_all]]
        viol += len(target_all) - len(target)
        if len(target) == 0:
            continue
        if train_cited is not None:
            novel_rows.append(bool((~train_cited[target]).any()))

        if loo:
            vec_p = R.score_prior(a, r, prior)
            vec_c = R.score_cousage(a, r, df, M)
        else:
            vec_p = prior.astype(np.float64)
            vec_c = score_cousage_noloo(a, r, df, M)
        vec_k = score_peers_masked(a, r, roots, df, inv, pos, amask)
        excl = ~amask.copy()
        excl[r] = True

        def top(vec):
            if vec is None:
                return None
            v = vec.copy()
            v[excl] = -np.inf
            ids = np.argpartition(-v, maxK)[:maxK]
            return ids[np.argsort(-v[ids])]

        ids = {"prior": top(vec_p), "cousage": top(vec_c), "peers": top(vec_k)}
        fused = R.rrf([ids["prior"], ids["cousage"], ids["peers"]], a.n)
        ids["fused"] = top(fused)

        n_eval += 1
        for m in methods:
            got = ids[m]
            for K in KS:
                topset = set(got[:K].tolist()) if got is not None else set()
                rec = sum(1 for c in target if c in topset) / len(target)
                hits[m][K].append(rec)
                if rec == 1.0:
                    full[m][K] += 1
        if (j + 1) % 200 == 0:
            log(f"    {j + 1}/{len(test_pos)}")

    res = {"n_eval": n_eval,
           "cited_premise_accessibility_violations": viol,
           "total_cited_premises": tot_target,
           "recall": {}, "full_rolodex_rate": {}}
    for m in methods:
        res["recall"][m] = {K: round(float(np.mean(hits[m][K])), 4)
                            for K in KS}
        res["full_rolodex_rate"][m] = {K: round(full[m][K] / n_eval, 4)
                                       for K in KS}
    return res, novel_rows, hits


def score_cousage_noloo(a, r, df, M):
    import scipy.sparse as sp
    s_ids = np.unique(R.stmt_deps(a, r))
    s_ids = s_ids[df[s_ids] <= R.DF_CAP]
    if len(s_ids) == 0:
        return None
    w = 1.0 / np.log1p(df[s_ids].astype(np.float64))
    vec = (sp.diags(w) @ M[s_ids]).sum(axis=0)
    return np.asarray(vec).ravel()


def score_peers_masked(a, r, roots, df, inv, self_pos, amask):
    """Peers scorer where only accessible peer THEOREMS count as knowledge."""
    from collections import defaultdict
    sims = defaultdict(float)
    for s in np.unique(R.stmt_deps(a, r)):
        if df[s] <= R.RARE_DF and int(s) in inv:
            idf = 1.0 / np.log1p(df[s])
            for pos in inv[int(s)]:
                if pos != self_pos and amask[roots[pos]]:
                    sims[pos] += idf
    if not sims:
        return None
    top = sorted(sims.items(), key=lambda kv: -kv[1])[:R.N_PEERS]
    vec = np.zeros(a.n)
    for pos, sim in top:
        vec[np.unique(R.proof_deps(a, roots[pos]))] += sim
    return vec


def main():
    log("loading atlas + accessibility...")
    a = load_dump()
    acc = Accessibility(a)
    log(f"modules: {acc.n_mods:,}; unmapped constants: {acc.unmapped:,}")
    roots = theorem_roots(a)
    isthm = np.zeros(a.n, dtype=bool)
    for i in range(a.n):
        if a.kind[i] == "theorem" and not a.cls[i]:
            isthm[i] = True
    out = {"config": {"holdout_frac": HOLDOUT_FRAC, "ks": list(KS),
                      "n_modules": acc.n_mods, "unmapped": acc.unmapped}}

    # ---------------- split 1: random (global stats, LOO, masked candidates)
    log("split 1: random (global stats + accessibility mask)")
    df, prior, M = R.build_stats(a, roots)
    inv = R.build_inverted(a, roots, df)
    rng = np.random.default_rng(0)
    cand = rng.choice(len(roots), size=3000, replace=False)
    test_pos = [int(p) for p in cand
                if isthm[R.proof_deps(a, roots[p])].any()][:1500]
    res, _, _ = eval_split(a, acc, roots, test_pos, df, prior, M, inv, isthm)
    out["random"] = res

    # ---------------- split 2: module holdout (train stats exclude test mods)
    log("split 2: module holdout")
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
                if isthm[R.proof_deps(a, roots[p])].any()][:1200]
    log(f"  held-out modules: {len(held)}; test roots available: "
        f"{len(test_all):,}; train roots: {len(train_pos):,}")
    train_roots = [roots[p] for p in train_pos]
    df2, prior2, M2 = R.build_stats(a, train_roots)
    inv2 = R.build_inverted(a, train_roots, df2)
    train_cited = np.zeros(a.n, dtype=bool)
    for r in train_roots:
        train_cited[np.unique(R.proof_deps(a, r))] = True
    # inv2/scorers index into train_roots; adapt positions
    res2, novel_rows, hits2 = eval_split(
        a, acc, train_roots + [roots[p] for p in test_pos],
        list(range(len(train_roots), len(train_roots) + len(test_pos))),
        df2, prior2, M2, inv2, isthm, train_cited=train_cited, loo=False)
    out["module_holdout"] = res2

    # ---------------- split 3: novel-premise subset of module holdout
    log("split 3: novel-premise subset")
    novel_share = float(np.mean(novel_rows)) if novel_rows else 0.0
    sub = {"share_of_holdout_tests_with_novel_premise": round(novel_share, 4)}
    methods = ("prior", "cousage", "peers", "fused")
    novel_mask = np.array(novel_rows, dtype=bool)
    for m in methods:
        sub[m] = {K: round(float(np.mean(
            np.array(hits2[m][K])[novel_mask])), 4) for K in KS} \
            if novel_mask.any() else None
    out["novel_premise"] = sub

    OUT.mkdir(exist_ok=True)
    (OUT / "rolodex_eval_v2.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
