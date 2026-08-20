#!/usr/bin/env python3
"""Statement-cone vs proof-cone study over the full Mathlib closure.

For a theorem T:
  A_S(T) = all ancestors reachable from the constants in T's STATEMENT (type)
  A_P(T) = all ancestors reachable from the constants in T's PROOF (value)
  N(T)   = A_P(T) \\ A_S(T)   -- mathematics the proof introduced beyond what
                                 was needed merely to state the problem.

Computed exactly for a sample (24 reviewed proofs + 500 random unclassified
theorems) via bitmask propagation in one reverse-topological pass.

Also: direct-user counts (in-degree) for all constants; role-signature table
(deterministic P3 classes used as evaluation LABELS ONLY, never as filters);
what-depth-measures correlations (depth vs cone size vs tree size); and a
move-identification rematch on the 24 reviewed proofs.

No name/namespace-based cuts, no probabilistic-classifier filtering.
"""
import json, os, sys
import numpy as np

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/db11af5d-4211-45ea-97b3-8e87cef8aeb6/scratchpad"
DUMP = os.path.join(SCRATCH, "mathlib_deps.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
SEED = 20260819
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


def topo(deps):
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
    deps, order, cyclic = topo(deps)
    print(f"topo done, cyclic residue {len(cyclic)}", flush=True)

    # ---- global scalar coordinates ----
    depth = np.zeros(n, dtype=np.int32)
    logsz = np.zeros(n, dtype=np.float64)
    for i in order:
        ds = deps[i]
        if ds:
            dd = [depth[d] for d in ds]
            depth[i] = 1 + max(dd)
            ls = np.array([logsz[d] for d in ds])
            mx = ls.max()
            logsz[i] = mx + np.log10(np.power(10.0, ls - mx).sum() + np.power(10.0, -mx))
    for i in cyclic:
        ds = [d for d in deps[i] if d not in cyclic]
        if ds:
            depth[i] = 1 + max(depth[d] for d in ds)
            logsz[i] = max(logsz[d] for d in ds) + 0.3
    stmt = np.zeros(n, dtype=np.int32)
    for i in range(n):
        ts = deps_t[i]
        stmt[i] = 1 + max((depth[d] for d in set(ts) if d != i), default=-1)
    rel = depth - stmt
    outdeg = np.array([len(d) for d in deps], dtype=np.int32)
    indeg = np.zeros(n, dtype=np.int64)          # direct users
    for i, ds in enumerate(deps):
        for d in ds:
            indeg[d] += 1
    print("scalars done", flush=True)

    has_class = np.array([len(c) > 0 for c in classes])
    thm = np.array([k == "theorem" for k in kinds])

    # ---- sample roots ----
    rk = json.load(open(os.path.join(DATA, "rankings.json")))
    review_roots = [d for d in rk["proofs"] if d in idx]
    rng = np.random.default_rng(SEED)
    pool = np.where(thm & ~has_class & (np.array([len(v) > 0 for v in deps_v])))[0]
    samp = rng.choice(pool, size=500, replace=False).tolist()
    roots = [idx[d] for d in review_roots] + [i for i in samp if names[i] not in set(review_roots)]
    nroots = len(roots)
    root_pos = {r: j for j, r in enumerate(roots)}
    nbits = 2 * nroots                     # bit 2j = statement cone, 2j+1 = proof cone
    nwords = (nbits + 63) // 64
    print(f"roots: {nroots}, words/node: {nwords}", flush=True)

    # ---- bitmask propagation (reverse topo: users before deps) ----
    reach = np.zeros((n, nwords), dtype=np.uint64)
    dep_arrays = [np.array(ds, dtype=np.int64) if ds else None for ds in deps]
    tdep_arrays, vdep_arrays = {}, {}
    for r in roots:
        j = root_pos[r]
        tdep_arrays[r] = np.array(sorted(set(deps_t[r]) - {r}), dtype=np.int64)
        vdep_arrays[r] = np.array(sorted(set(deps_v[r]) - {r}), dtype=np.int64)
    def bitrow(b):
        row = np.zeros(nwords, dtype=np.uint64)
        row[b >> 6] = np.uint64(1) << np.uint64(b & 63)
        return row
    seq = list(reversed(order)) + cyclic + cyclic   # cyclic residue: two extra passes
    for i in seq:
        row = reach[i]
        if row.any():
            ds = dep_arrays[i]
            if ds is not None:
                reach[ds] |= row
        j = root_pos.get(i)
        if j is not None:
            if len(tdep_arrays[i]):
                reach[tdep_arrays[i]] |= bitrow(2 * j)
            if len(vdep_arrays[i]):
                reach[vdep_arrays[i]] |= bitrow(2 * j + 1)
    print("propagation done", flush=True)

    def cone_mask(j, proof):
        b = 2 * j + (1 if proof else 0)
        return (reach[:, b >> 6] >> np.uint64(b & 63)) & np.uint64(1)

    # ---- per-root cone stats ----
    per_root = []
    for r in roots:
        j = root_pos[r]
        S = cone_mask(j, False).astype(bool)
        P = cone_mask(j, True).astype(bool)
        N = P & ~S
        nn = int(N.sum())
        row = {"decl": names[r], "depth": int(depth[r]), "stmtDepth": int(stmt[r]),
               "A_S": int(S.sum()), "A_P": int(P.sum()), "N": nn,
               "share_new": round(nn / max(1, int(P.sum())), 4)}
        if nn:
            nd = depth[N]
            row["N_max_depth"] = int(nd.max())
            row["N_deeper_than_stmt"] = int((nd >= stmt[r]).sum())
            if names[r] in rk["proofs"]:   # examples only for the reviewed 24
                cand = np.where(N)[0]
                top = cand[np.argsort(-depth[cand])[:8]]
                row["N_deepest"] = [f"{names[t]} (d={int(depth[t])})" for t in top]
        per_root.append(row)
    review_set = set(review_roots)
    samp_rows = [r for r in per_root if r["decl"] not in review_set]
    out = {"n_roots": nroots, "seed": SEED}
    sn = np.array([r["share_new"] for r in samp_rows])
    ap = np.array([r["A_P"] for r in samp_rows], dtype=float)
    dp = np.array([r["depth"] for r in samp_rows], dtype=float)
    lz = np.array([logsz[idx[r["decl"]]] for r in samp_rows])
    out["sample_cone_stats"] = {
        "A_P_percentiles": {p: float(np.percentile(ap, p)) for p in (10, 50, 90)},
        "share_new_percentiles": {p: round(float(np.percentile(sn, p)), 4) for p in (10, 50, 90)},
        "frac_with_empty_N": round(float((sn == 0).mean()), 4)}
    from scipy.stats import spearmanr
    out["what_depth_measures"] = {
        "spearman_depth_vs_log_coneSize": round(float(spearmanr(dp, np.log10(ap + 1)).statistic), 3),
        "spearman_depth_vs_logTreeSize": round(float(spearmanr(dp, lz).statistic), 3),
        "spearman_coneSize_vs_logTreeSize": round(float(spearmanr(np.log10(ap + 1), lz).statistic), 3),
        "sharing_factor_median": round(float(np.median(lz - np.log10(ap + 1))), 2)}
    out["reviewed_cones"] = [r for r in per_root if r["decl"] in review_set]

    # ---- move identification rematch on the reviewed proofs ----
    agg = {k: [] for k in ("depth", "new_depth", "users_desc", "users_asc",
                           "route_depth", "route_new_depth")}
    per_proof = []
    for decl, p in rk["proofs"].items():
        if decl not in idx or decl not in review_set:
            continue
        j = root_pos[idx[decl]]
        S = cone_mask(j, False).astype(bool)
        known = [c for c in p["features"] if c in idx]
        if len(known) < 3:
            continue
        keys = set(p["proxy_keys"])
        route = {c for c, f in p["features"].items()
                 if f["app_head_count"] > 0 and f["prop_result_frac"] > 0.5 and not f["p3_classified"]}
        is_new = {c: (not S[idx[c]]) for c in known}
        rankers = {
            "depth": sorted(known, key=lambda c: -depth[idx[c]]),
            "new_depth": sorted(known, key=lambda c: (not is_new[c], -depth[idx[c]])),
            "users_desc": sorted(known, key=lambda c: -indeg[idx[c]]),
            "users_asc": sorted(known, key=lambda c: indeg[idx[c]]),
        }
        row = {"decl": decl, "n_cands": len(known),
               "n_new": sum(is_new.values())}
        for mname, ranked in rankers.items():
            top5 = ranked[:5]
            row[f"{mname}_p_at_5"] = round(len([c for c in top5 if c in keys]) / min(5, len(ranked)), 3)
            agg[mname].append(row[f"{mname}_p_at_5"])
        for mname in ("depth", "new_depth"):
            top5 = rankers[mname][:5]
            ov = len([c for c in top5 if c in route]) / max(1, min(5, len(route)) or 1)
            row[f"{mname}_route_overlap"] = round(ov, 3)
            agg[f"route_{mname}"].append(ov)
        per_proof.append(row)
    out["move_id_median"] = {k: round(float(np.median(v)), 3) for k, v in agg.items() if v}
    out["move_id_reference"] = {"phase3_M_p4_route_p_at_5": 0.4, "prev_depth_p_at_5": 0.2}
    out["move_id_per_proof"] = per_proof

    # ---- role signatures (labels only) ----
    from sklearn.metrics import roc_auc_score
    coords = {"depth": depth.astype(float), "stmtDepth": stmt.astype(float),
              "relDepth": rel.astype(float), "logTreeSize": logsz,
              "log_directUsers": np.log1p(indeg.astype(float)),
              "directDeps": outdeg.astype(float)}
    neg = np.where(thm & ~has_class)[0]
    negs = rng.choice(neg, size=min(60000, len(neg)), replace=False)
    sig = {}
    for cname in P3C:
        m = np.where(np.array([cname in c for c in classes]))[0]
        if len(m) < 30:
            continue
        ms = rng.choice(m, size=min(30000, len(m)), replace=False)
        y = np.r_[np.ones(len(ms)), np.zeros(len(negs))]
        e = {"n": int(len(m))}
        for k, v in coords.items():
            e[f"median_{k}"] = round(float(np.median(v[m])), 2)
            e[f"auc_{k}"] = round(float(roc_auc_score(y, np.r_[v[ms], v[negs]])), 3)
        sig[cname] = e
    for label, mask in (("unclassified_theorems", thm & ~has_class),
                        ("unclassified_defs", (np.array([k == "def" for k in kinds]) & ~has_class))):
        m = np.where(mask)[0]
        sig[label] = {"n": int(len(m))}
        for k, v in coords.items():
            sig[label][f"median_{k}"] = round(float(np.median(v[m])), 2)
    out["role_signatures"] = sig

    # interface phenomenon: proofs that add no depth beyond their statement
    ut = thm & ~has_class
    out["interface_stats"] = {
        "frac_unclassified_thms_relDepth_leq_0": round(float((rel[ut] <= 0).mean()), 4),
        "frac_unclassified_thms_relDepth_leq_2": round(float((rel[ut] <= 2).mean()), 4)}

    with open(os.path.join(DATA, "cones_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for k in ("sample_cone_stats", "what_depth_measures", "move_id_median", "interface_stats"):
        print(k, "=", json.dumps(out[k]))


if __name__ == "__main__":
    main()
