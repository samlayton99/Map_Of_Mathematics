#!/usr/bin/env python3
"""CORRECTED merge analysis: batch-invariant mergers and bridge ENRICHMENT.

Two defects in the previous merge census, both identified by the external
audit, both fixed here.

DEFECT 1 -- merge attribution was not batch-invariant. Union-find credits
whichever edge of a tied batch happens to be processed first. That is an
artifact of iteration order, not a cause. Fixed: at each rank threshold,
freeze the previous partition, build the QUOTIENT GRAPH induced by every new
inter-component edge, and treat each connected component of that quotient as
ONE merger with ALL its contributing edges. No arbitrary causal edge.

DEFECT 2 -- raw merge shares are base rates, not evidence. "Definitions cause
58.8% of merges" means nothing if definitions are 58% of the edges eligible to
cause a merge. Fixed: report

    Enrichment(a) = P(a | crosses prior components) / P(a | eligible at step)

with bootstrap confidence intervals, plus KIND ABLATION (remove all edges of
kind a from the batch and recompute the component reduction) and exact SHAPLEY
contributions over the four kind groups.

Ranking: R4 (proof-introduced, then cited depth).
"""
import json, os
from itertools import combinations
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
KMAX = 8
KINDS = ["theorem", "definition/construction", "constructor/recursor", "glue"]
BOOT = 200


def main():
    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    nodes = np.load(os.path.join(DATA, "nodes.npz"))
    v8 = np.load(os.path.join(DATA, "v8_mask.npz"))
    names = json.load(open(os.path.join(DATA, "names.json")))

    a_col = inc["artifact"].astype(np.int64)
    d_col = inc["decl"].astype(np.int64)
    lb = inc["load_bearing"]
    in_sw = inc["in_stmt_world"]
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"].astype(np.float64)
    kind = nodes["kind"]
    n = len(depth)
    tgt = certifies[a_col]
    logic_only = v8["decl_logic_only"]
    machinery = v8["machinery"]

    bi = np.where(lb & (tgt != d_col))[0]
    not_new = in_sw[bi]
    dep = depth[d_col[bi]]

    order = np.lexsort((-dep, not_new.astype(np.int8), a_col[bi]))
    s = bi[order]
    aa = a_col[s]
    new = np.empty(len(s), bool); new[0] = True; new[1:] = aa[1:] != aa[:-1]
    st = np.where(new)[0]
    cnt = np.diff(np.append(st, len(s)))
    rk = np.concatenate([np.arange(c) for c in cnt])

    def kind_of(i):
        d = d_col[i]
        if logic_only[d] or machinery[i]:
            return "glue"
        if kind[d] == 0:
            return "theorem"
        if kind[d] in (1, 2, 5, 6, 7):
            return "definition/construction"
        return "constructor/recursor"

    touched = np.unique(np.concatenate([tgt[bi], d_col[bi]]))
    nid = -np.ones(n, dtype=np.int64)
    nid[touched] = np.arange(len(touched))
    N = len(touched)
    print(f"nodes: {N:,}", flush=True)

    # state: accumulate admitted edges; recompute the partition exactly at
    # each threshold. (An earlier version tried to fold the partition into a
    # sparse product and produced a partition that GREW with k, which is
    # impossible when only adding edges.)
    acc_u, acc_v = [], []
    lab = np.arange(N)          # start: every node isolated
    rows = []
    enrich_rows = []
    for k in range(KMAX):
        batch = s[rk == k]
        u = nid[tgt[batch]]; v = nid[d_col[batch]]
        ok = (u >= 0) & (v >= 0)
        batch, u, v = batch[ok], u[ok], v[ok]
        # eligible = every new incidence in this batch
        elig_kinds = Counter(kind_of(i) for i in batch)
        # crossing = those joining two DIFFERENT prior components
        cu, cv = lab[u], lab[v]
        crosses = cu != cv
        cross_kinds = Counter(kind_of(i) for i in batch[crosses])

        # --- batch-invariant mergers via the quotient graph ---
        if crosses.any():
            q = sp.coo_matrix((np.ones(int(crosses.sum()), np.int8),
                               (cu[crosses], cv[crosses])), shape=(N, N))
            nq, qlab = connected_components(q, directed=False)
            involved = np.unique(np.concatenate([cu[crosses], cv[crosses]]))
            groups = defaultdict(list)
            for c in involved:
                groups[qlab[c]].append(c)
            n_mergers = sum(1 for g in groups.values() if len(g) > 1)
            comps_eliminated = sum(len(g) - 1 for g in groups.values() if len(g) > 1)
        else:
            n_mergers = comps_eliminated = 0

        # --- enrichment with bootstrap CI ---
        tot_e = sum(elig_kinds.values()); tot_c = sum(cross_kinds.values())
        ek = {}
        if tot_c > 0:
            bkinds = np.array([kind_of(i) for i in batch])
            bcross = crosses
            rng = np.random.default_rng(7)
            for a in KINDS:
                pe = elig_kinds[a] / tot_e if tot_e else 0.0
                pc = cross_kinds[a] / tot_c if tot_c else 0.0
                val = (pc / pe) if pe > 0 else float("nan")
                bs = []
                m = len(batch)
                for _ in range(BOOT):
                    ii = rng.integers(0, m, m)
                    bk_, bc_ = bkinds[ii], bcross[ii]
                    e2 = (bk_ == a).mean()
                    c2 = ((bk_ == a) & bc_).sum() / max(bc_.sum(), 1)
                    bs.append(c2 / e2 if e2 > 0 else np.nan)
                bs = np.array([x for x in bs if np.isfinite(x)])
                lo, hi = (np.percentile(bs, 2.5), np.percentile(bs, 97.5)) if len(bs) else (np.nan, np.nan)
                ek[a] = {"p_eligible": pe, "p_crossing": pc, "enrichment": val,
                         "ci95": [float(lo), float(hi)]}

        # --- kind ablation: components eliminated without kind a ---
        abl = {}
        for a in KINDS:
            keep = crosses & np.array([kind_of(i) != a for i in batch])
            if keep.any():
                q2 = sp.coo_matrix((np.ones(int(keep.sum()), np.int8),
                                    (cu[keep], cv[keep])), shape=(N, N))
                _, ql2 = connected_components(q2, directed=False)
                inv2 = np.unique(np.concatenate([cu[keep], cv[keep]]))
                g2 = defaultdict(list)
                for c in inv2:
                    g2[ql2[c]].append(c)
                ce2 = sum(len(g) - 1 for g in g2.values() if len(g) > 1)
            else:
                ce2 = 0
            abl[a] = {"components_eliminated_without": ce2,
                      "marginal_loss": comps_eliminated - ce2}

        # --- exact Shapley over the four kind groups ---
        def value(subset):
            keep = crosses & np.array([kind_of(i) in subset for i in batch])
            if not keep.any():
                return 0
            q3 = sp.coo_matrix((np.ones(int(keep.sum()), np.int8),
                                (cu[keep], cv[keep])), shape=(N, N))
            _, ql3 = connected_components(q3, directed=False)
            inv3 = np.unique(np.concatenate([cu[keep], cv[keep]]))
            g3 = defaultdict(list)
            for c in inv3:
                g3[ql3[c]].append(c)
            return sum(len(g) - 1 for g in g3.values() if len(g) > 1)

        shap = {a: 0.0 for a in KINDS}
        others = {a: [x for x in KINDS if x != a] for a in KINDS}
        import math
        for a in KINDS:
            for r_ in range(len(others[a]) + 1):
                for S in combinations(others[a], r_):
                    w = (math.factorial(len(S)) *
                         math.factorial(len(KINDS) - len(S) - 1) /
                         math.factorial(len(KINDS)))
                    shap[a] += w * (value(set(S) | {a}) - value(set(S)))

        # apply the batch for real: accumulate, then recompute exactly
        acc_u.append(u); acc_v.append(v)
        au = np.concatenate(acc_u); av = np.concatenate(acc_v)
        gacc = sp.coo_matrix((np.ones(len(au), np.int8), (au, av)), shape=(N, N))
        _, lab = connected_components(gacc, directed=False)
        sizes = np.bincount(lab); sizes = sizes[sizes > 0]
        giant = sizes.max() / sizes.sum()
        rows.append({"k": k + 1, "eligible": int(len(batch)),
                     "crossing": int(crosses.sum()), "mergers": n_mergers,
                     "components_eliminated": comps_eliminated,
                     "components": int(len(sizes)), "giant": round(float(giant), 4),
                     "enrichment": ek, "ablation": abl,
                     "shapley": {a: round(shap[a], 1) for a in KINDS}})
        print(f"\n--- k={k+1}: eligible={len(batch):,} crossing={int(crosses.sum()):,} "
              f"mergers={n_mergers:,} components_eliminated={comps_eliminated:,} "
              f"-> components={len(sizes):,} giant={giant:.2%}", flush=True)
        if ek:
            print(f"    {'kind':<26} {'P(elig)':>9} {'P(cross)':>9} "
                  f"{'enrich':>8} {'95% CI':>18} {'shapley':>9} {'ablation':>9}",
                  flush=True)
            for a in KINDS:
                e = ek[a]
                ci = f"[{e['ci95'][0]:.2f},{e['ci95'][1]:.2f}]"
                print(f"    {a:<26} {e['p_eligible']:>8.1%} {e['p_crossing']:>8.1%} "
                      f"{e['enrichment']:>8.2f} {ci:>18} {shap[a]:>9.0f} "
                      f"{abl[a]['marginal_loss']:>9,}", flush=True)

    print(f"\n{'='*78}\nVERDICT on 'definitions are the bridges'\n{'='*78}", flush=True)
    for r in rows[1:4]:
        e = r["enrichment"].get("definition/construction")
        t = r["enrichment"].get("theorem")
        if e and t:
            print(f"  k={r['k']}: definitions enrichment {e['enrichment']:.2f} "
                  f"(CI {e['ci95'][0]:.2f}-{e['ci95'][1]:.2f}), "
                  f"theorems {t['enrichment']:.2f} "
                  f"(CI {t['ci95'][0]:.2f}-{t['ci95'][1]:.2f})", flush=True)
    print("\n  enrichment > 1 means the kind crosses components MORE than its "
          "share of eligible edges; ~1.0 means the earlier 58.8% was a base "
          "rate, not evidence.", flush=True)

    with open(os.path.join(DATA, "bridge_enrichment.json"), "w") as f:
        json.dump({"per_k": rows, "note": "batch-invariant mergers via quotient "
                   "graph; enrichment normalised by eligibility; Shapley over "
                   "kind groups"}, f, indent=1)
    print("\nwritten data/bridge_enrichment.json", flush=True)


if __name__ == "__main__":
    main()
