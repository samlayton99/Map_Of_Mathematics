#!/usr/bin/env python3
"""Graph measures over the full Mathlib closure (extends depth.py).

Measures per constant n (deps = value deps if body exists, else type deps):
  depth        = 1 + max(depth(deps))                     [longest chain to primitives]
  logTreeSize  = log10 of fully-unfolded proof-tree size:
                 T(n) = 1 + sum(T(d) for d in deps)       [Sam's "size", log-space]
  directDeps   = |deps|
  stmtDepth    = 1 + max(depth over TYPE deps)            [depth the statement already needs]
  relDepth     = depth - stmtDepth                        [how much deeper the proof digs]
  copillars    = #{d in deps : depth(d) >= depth(n) - 2}  [how many near-top towers it joins]
  critParent   = argmax-depth dep                         [the load-bearing citation]

Analyses:
  1. machinery separability (AUC) for each measure + combinations, full population
     and per P3 class;
  2. depth x size quadrant map with examples (where each succeeds/fails);
  3. per-proof move identification on the 24 reviewed proofs (rank candidates by
     each measure; proxy-key overlap; overlap with P4-route heads);
  4. critical-path demo (the "main road" from a theorem down to primitives);
  5. does depth/size add to the Phase 3 typed track on the corpus population?
"""
import json, os, sys
import numpy as np

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/db11af5d-4211-45ea-97b3-8e87cef8aeb6/scratchpad"
DUMP = os.path.join(SCRATCH, "mathlib_deps.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
P3C = ["typeclass-instance", "recursor", "structure-projection", "generated",
       "internal-detail", "eq-machinery", "logic-core", "coercion"]


def load():
    idx, names, deps_v, deps_t, kinds, classes = {}, [], [], [], [], []
    def nid(n):
        i = idx.get(n)
        if i is None:
            i = len(names); idx[n] = i; names.append(n)
            deps_v.append(()); deps_t.append(()); kinds.append(""); classes.append(())
        return i
    with open(DUMP) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]; classes[i] = tuple(r["c"])
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
    return idx, names, deps_v, deps_t, kinds, classes


def topo_order(deps):
    n = len(deps)
    indeg = np.zeros(n, dtype=np.int32)
    users = [[] for _ in range(n)]
    clean = []
    for i, ds in enumerate(deps):
        ds2 = tuple(d for d in set(ds) if d != i)
        clean.append(ds2)
        indeg[i] = len(ds2)
        for d in ds2:
            users[d].append(i)
    from collections import deque
    q = deque(np.where(indeg == 0)[0].tolist())
    order = []
    while q:
        i = q.popleft(); order.append(i)
        for u in users[i]:
            indeg[u] -= 1
            if indeg[u] == 0:
                q.append(u)
    cyclic = [i for i in range(n) if indeg[i] > 0]
    return clean, order, cyclic


def main():
    idx, names, deps_v, deps_t, kinds, classes = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    deps = [dv if dv else dt for dv, dt in zip(deps_v, deps_t)]
    deps, order, cyclic = topo_order(deps)
    depth = np.zeros(n, dtype=np.int32)
    logsz = np.zeros(n, dtype=np.float64)   # log10(T(n)), T = 1 + sum T(d)
    crit = np.full(n, -1, dtype=np.int64)
    for i in order:
        ds = deps[i]
        if ds:
            dd = [depth[d] for d in ds]
            m = max(dd)
            depth[i] = 1 + m
            crit[i] = ds[int(np.argmax(dd))]
            # log10(1 + sum 10^logsz[d]) via stable logsumexp
            ls = np.array([logsz[d] for d in ds])
            mx = ls.max()
            logsz[i] = mx + np.log10(np.power(10.0, ls - mx).sum() + np.power(10.0, -mx))
    for i in cyclic:  # tiny residue: approximate from resolved deps
        ds = [d for d in deps[i] if d not in cyclic]
        if ds:
            depth[i] = 1 + max(depth[d] for d in ds)
            logsz[i] = max(logsz[d] for d in ds) + 0.3
    ndeps = np.array([len(d) for d in deps], dtype=np.int32)
    # statement depth and relative depth
    stmt = np.zeros(n, dtype=np.int32)
    for i in order:
        ts = deps_t[i]
        stmt[i] = 1 + max((depth[d] for d in set(ts) if d != i), default=-1)
    rel = depth - stmt
    copil = np.array([sum(1 for d in ds if depth[d] >= depth[i] - 2) if ds else 0
                      for i, ds in enumerate(deps)], dtype=np.int32)

    has_class = np.array([len(c) > 0 for c in classes])
    from sklearn.metrics import roc_auc_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    from sklearn.model_selection import cross_val_score

    y = has_class.astype(int)
    feats = {"depth": -depth.astype(float), "logTreeSize": -logsz,
             "directDeps": -ndeps.astype(float), "relDepth": -rel.astype(float),
             "copillars": -copil.astype(float)}
    out = {"constants": n, "auc_single_full_population": {}}
    for k, v in feats.items():
        out["auc_single_full_population"][k] = round(float(roc_auc_score(y, v)), 4)
    # combinations (5-fold CV logistic on a stratified 80k subsample for speed)
    rng = np.random.default_rng(20260819)
    sub = rng.choice(n, size=min(80000, n), replace=False)
    X = np.column_stack([depth, logsz, ndeps, rel, copil]).astype(float)[sub]
    ys = y[sub]
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    out["auc_combo_depth_size"] = round(float(np.mean(cross_val_score(
        lr, X[:, :2], ys, cv=5, scoring="roc_auc"))), 4)
    out["auc_combo_all5"] = round(float(np.mean(cross_val_score(
        lr, X, ys, cv=5, scoring="roc_auc"))), 4)
    # per-class single-measure AUCs
    percls = {}
    neg = ~has_class
    for cname in P3C:
        m = np.array([cname in c for c in classes])
        if m.sum() < 30:
            continue
        percls[cname] = {k: round(float(roc_auc_score(
            np.r_[np.ones(m.sum()), np.zeros(neg.sum())],
            np.r_[v[m], v[neg]])), 3) for k, v in feats.items()}
    out["auc_per_class"] = percls

    # quadrant map: depth tercile x size tercile among theorems
    thm = np.array([k == "theorem" for k in kinds])
    dq = np.quantile(depth[thm], [1 / 3, 2 / 3])
    sq = np.quantile(logsz[thm], [1 / 3, 2 / 3])
    quad = {}
    for di, dl in enumerate(("shallow", "mid-depth", "deep")):
        for si, sl in enumerate(("small", "mid-size", "large")):
            m = thm.copy()
            m &= (depth >= (dq[di - 1] if di else -1)) & (depth < (dq[di] if di < 2 else 1e9))
            m &= (logsz >= (sq[si - 1] if si else -1)) & (logsz < (sq[si] if si < 2 else 1e9))
            if m.sum() == 0:
                continue
            infrac = float(has_class[m].mean())
            ex = [names[i] for i in np.where(m)[0][:400]
                  if not names[i].startswith("_") and "._" not in names[i]][:3]
            quad[f"{dl}|{sl}"] = {"n": int(m.sum()), "p3_frac": round(infrac, 3), "examples": ex}
    out["quadrants_theorems"] = quad

    # per-proof move identification on the 24 reviewed proofs
    rk = json.load(open(os.path.join(DATA, "rankings.json")))
    per_proof, agg = [], {m: [] for m in ("depth", "logTreeSize", "relDepth", "route_overlap_depth")}
    for decl, p in rk["proofs"].items():
        cands = list(p["features"].keys())
        known = [c for c in cands if c in idx]
        if len(known) < 3:
            continue
        keys = set(p["proxy_keys"])
        route = {c for c, f in p["features"].items()
                 if f["app_head_count"] > 0 and f["prop_result_frac"] > 0.5 and not f["p3_classified"]}
        row = {"decl": decl, "n_cands": len(known)}
        for mname, arr in (("depth", depth), ("logTreeSize", logsz), ("relDepth", rel)):
            ranked = sorted(known, key=lambda c: -arr[idx[c]])
            top5 = ranked[:5]
            p5 = len([c for c in top5 if c in keys]) / min(5, len(ranked))
            row[f"{mname}_p_at_5"] = round(p5, 3)
            if mname == "depth":
                row["depth_top5_route_overlap"] = round(
                    len([c for c in top5 if c in route]) / max(1, min(5, len(route)) or 1), 3)
                agg["route_overlap_depth"].append(row["depth_top5_route_overlap"])
            agg[mname].append(p5) if mname in agg else None
        per_proof.append(row)
    out["move_id_median_p_at_5"] = {
        "depth": round(float(np.median(agg["depth"])), 3),
        "logTreeSize": round(float(np.median(agg["logTreeSize"])), 3),
        "relDepth": round(float(np.median(agg["relDepth"])), 3),
        "depth_top5_vs_route_overlap": round(float(np.median(agg["route_overlap_depth"])), 3),
        "phase3_reference": {"M_p4_route": 0.4, "M_global_pagerank": 0.2, "others": 0.0}}
    out["move_id_per_proof"] = per_proof

    # critical path demo
    def crit_path(name, k=18):
        i = idx[name]; path = []
        while i >= 0 and len(path) < k:
            path.append(f"{names[i]} (d={int(depth[i])})")
            i = int(crit[i])
        return path
    out["critical_paths"] = {a: crit_path(a) for a in
                             ("Real.exp_log", "Nat.gcd_comm", "norm_add_le") if a in idx}

    # does depth/size add to the Phase 3 typed track? (corpus primary population)
    import pandas as pd
    nodes = pd.read_csv(os.path.join(DATA, "node_inventory.csv")).set_index("name")
    typed = pd.read_csv(os.path.join(DATA, "feature_matrix_typed.csv"), index_col=0)
    sel = nodes[(nodes.stored == 1) & (nodes.p3_evaluated == 1)]
    common = [nm for nm in sel.index if nm in typed.index and nm in idx]
    sys.path.insert(0, HERE)
    from models_qa import prep
    Xt = prep(typed.loc[common]).values
    add = np.column_stack([[depth[idx[nm]] for nm in common],
                           [logsz[idx[nm]] for nm in common],
                           [rel[idx[nm]] for nm in common]])
    yc = sel.loc[common].p3_any.values
    groups = sel.loc[common].files.str.split("|").str[0].values
    from sklearn.model_selection import GroupKFold
    def gauc(Xm):
        cv = GroupKFold(n_splits=6)
        scs = []
        for tr, te in cv.split(Xm, yc, groups):
            m = lr.fit(Xm[tr], yc[tr])
            scs.append(roc_auc_score(yc[te], m.predict_proba(Xm[te])[:, 1]))
        return round(float(np.mean(scs)), 4)
    out["corpus_primary_grouped_auc"] = {
        "typed_track_alone": gauc(Xt),
        "depth_size_rel_alone": gauc(add),
        "typed_plus_depth_size_rel": gauc(np.column_stack([Xt, add]))}

    with open(os.path.join(DATA, "measures_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for k in ("auc_single_full_population", "auc_combo_depth_size", "auc_combo_all5",
              "move_id_median_p_at_5", "corpus_primary_grouped_auc"):
        print(k, "=", json.dumps(out[k]))


if __name__ == "__main__":
    main()
