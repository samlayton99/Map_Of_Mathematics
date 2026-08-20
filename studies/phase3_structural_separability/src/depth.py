#!/usr/bin/env python3
"""Recursive unfolding depth over the FULL Mathlib environment (Sam's proposal).

depth(n) = 0 if n has no dependencies, else 1 + max(depth of deps).
deps(n) = value/proof-term dependencies when a body exists, else type deps
(axioms, inductives, constructors, recursors bottom out through their types).

Tests: does depth alone separate P3 machinery? class-wise depth profiles;
anchor declarations (triangle inequality etc.); the resolution-dial view;
correlation with the Phase 3 typed-track machinery probability.
"""
import json, os, sys
import numpy as np

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/db11af5d-4211-45ea-97b3-8e87cef8aeb6/scratchpad"
DUMP = os.path.join(SCRATCH, "mathlib_deps.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))

ANCHORS = [
    # plumbing
    "Eq.mpr", "congrArg", "id", "Eq.trans", "And.intro", "Iff.intro",
    "instHAdd", "instAddNat", "OfNat.ofNat", "Nat.rec",
    # instances on deep towers (prediction: deep despite being machinery)
    "Real.instAdd", "Real.instLinearOrder", "Complex.instField",
    # named mathematics, roughly increasing sophistication
    "Nat.add_comm", "Nat.gcd_comm", "abs_add", "norm_add_le", "dist_triangle",
    "Real.add_comm", "Real.exp", "Real.log", "Real.log_le_sub_one_of_pos",
    "Real.exp_log", "Cauchy.value?", "CauSeq.Completion.Cauchy",
    "MeasureTheory.integral_add", "deriv_add", "HasDerivAt.exp",
]


def load():
    idx, names = {}, []
    deps_v, deps_t, kinds, classes = [], [], [], []
    def nid(n):
        i = idx.get(n)
        if i is None:
            i = len(names); idx[n] = i; names.append(n)
            deps_v.append(None); deps_t.append(None); kinds.append(""); classes.append(())
        return i
    with open(DUMP) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]
            classes[i] = tuple(r["c"])
            deps_v[i] = [nid(d) for d in r["v"]]
            deps_t[i] = [nid(d) for d in r["t"]]
    return idx, names, deps_v, deps_t, kinds, classes


def compute_depth(deps):
    """Kahn-style: process nodes whose deps are all resolved. Nodes stuck in
    cycles (unsafe recursion artifacts) get the max depth of their SCC env +1,
    resolved by iterating until fixpoint on the residue."""
    n = len(deps)
    depth = np.full(n, -1, dtype=np.int32)
    indeg = np.zeros(n, dtype=np.int32)   # number of unresolved deps
    users = [[] for _ in range(n)]
    for i, ds in enumerate(deps):
        ds2 = [d for d in set(ds or []) if d != i]
        deps[i] = ds2
        indeg[i] = len(ds2)
        for d in ds2:
            users[d].append(i)
    from collections import deque
    q = deque(np.where(indeg == 0)[0].tolist())
    for i in q:
        depth[i] = 0
    while q:
        i = q.popleft()
        for u in users[i]:
            indeg[u] -= 1
            if indeg[u] == 0:
                depth[u] = 1 + max(depth[d] for d in deps[u])
                q.append(u)
    # cyclic residue: assign 1 + max(resolved deps), iterate to fixpoint
    stuck = np.where(depth < 0)[0]
    for _ in range(50):
        changed = False
        for i in stuck:
            cand = [depth[d] for d in deps[i] if depth[d] >= 0]
            v = (1 + max(cand)) if cand else 0
            if depth[i] != v:
                depth[i] = v; changed = True
        if not changed:
            break
    return depth, len(stuck)


def auc(pos, neg):
    from sklearn.metrics import roc_auc_score
    y = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    x = np.concatenate([pos, neg])
    return roc_auc_score(y, x)


def main():
    idx, names, deps_v, deps_t, kinds, classes = load()
    n = len(names)
    print(f"constants: {n}")
    # Sam's depth: value deps when body exists, else type deps
    deps = [dv if dv else dt for dv, dt in zip(deps_v, deps_t)]
    depth, n_cyclic = compute_depth(deps)
    print(f"cyclic residue nodes: {n_cyclic}")
    d = np.asarray(depth, dtype=float)
    out = {"constants": n, "cyclic_nodes": int(n_cyclic),
           "depth_percentiles": {p: float(np.percentile(d, p)) for p in (50, 75, 90, 99, 100)}}

    has_class = np.array([len(c) > 0 for c in classes])
    out["auc_depth_p3_any_full_population"] = round(float(auc(-d[has_class], -d[~has_class])), 4)
    # class-wise depth medians
    from collections import defaultdict
    med = {}
    for cname in ("typeclass-instance", "recursor", "structure-projection", "generated",
                  "internal-detail", "eq-machinery", "logic-core", "coercion"):
        m = np.array([cname in c for c in classes])
        if m.sum() > 20:
            med[cname] = {"n": int(m.sum()), "median": float(np.median(d[m])),
                          "p90": float(np.percentile(d[m], 90)),
                          "auc_shallow": round(float(auc(-d[m], -d[~has_class])), 4)}
    m = ~has_class
    med["UNCLASSIFIED"] = {"n": int(m.sum()), "median": float(np.median(d[m])),
                           "p90": float(np.percentile(d[m], 90))}
    thm = np.array([k == "theorem" for k in kinds]) & ~has_class
    med["unclassified_theorems"] = {"n": int(thm.sum()), "median": float(np.median(d[thm])),
                                    "p90": float(np.percentile(d[thm], 90))}
    out["depth_by_class"] = med
    out["anchors"] = {a: int(depth[idx[a]]) for a in ANCHORS if a in idx}
    # resolution dial: how many unclassified theorems above each cutoff
    dial = {}
    for cut in (5, 10, 20, 30, 50, 75, 100, 150):
        dial[cut] = int(((d >= cut) & thm).sum())
    out["theorems_at_depth_geq"] = dial
    # correlation with Phase 3 machinery probability on the primary population
    try:
        import pandas as pd
        sys.path.insert(0, HERE)
        from landmark import machinery_probability
        prob = machinery_probability()
        common = [nm for nm in prob.index if nm in idx]
        dp = np.array([depth[idx[nm]] for nm in common], dtype=float)
        pr = prob.loc[common].values
        from scipy.stats import spearmanr
        r = spearmanr(dp, pr)
        out["spearman_depth_vs_machineryProb"] = {"rho": round(float(r.statistic), 3),
                                                  "n": len(common)}
    except Exception as e:
        out["spearman_depth_vs_machineryProb"] = f"skipped: {e}"
    with open(os.path.join(DATA, "depth_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
