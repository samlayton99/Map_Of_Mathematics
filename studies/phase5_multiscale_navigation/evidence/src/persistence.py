#!/usr/bin/env python3
"""Phase 5: persistence of structure across projections (Q1.2, Q4).

Registered prediction under test (PRE_REGISTRATION Q1.2):
  "centrality ranking will be substantially more stable between P3 and P4
   (both claim-level) than between P2 and P3 (crossing the Prop boundary).
   If instead P2->P3 is the stable transition and P3->P4 is not, the V8
   content boundary is doing more violence to the geometry than the claims
   filter, and that is evidence against keeping P4 as the default view."

Centrality is computed on the BIPARTITE incidence (ADR-0005 forbids clique
expansion). PageRank runs on the declaration-to-declaration projection
obtained by walking decl -> artifact -> certified declaration, which is a
random walk on the bipartite graph and never materializes a clique.

Also computed: weak-component structure per projection, and how many
components merge as evidence is added (the filtration's component births).
"""
import json, os
import numpy as np
import scipy.sparse as sp
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))


def pagerank_bipartite(rows, cols, n, iters=30, alpha=0.85):
    """Random walk decl -> (artifact) -> certified decl, on the sparse
    adjacency implied by the incidence. rows = citing declaration (the
    certified target), cols = cited declaration."""
    A = sp.coo_matrix((np.ones(len(rows), dtype=np.float32), (rows, cols)),
                      shape=(n, n)).tocsr()
    outdeg = np.asarray(A.sum(axis=1)).ravel()
    outdeg[outdeg == 0] = 1.0
    D = sp.diags(1.0 / outdeg)
    M = (D @ A).T.tocsr()          # column-stochastic transition
    r = np.full(n, 1.0 / n, dtype=np.float32)
    for _ in range(iters):
        r = alpha * (M @ r) + (1.0 - alpha) / n
    return r


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
    d_cite = inc["d_cite"].astype(np.int32)
    certifies = arts["certifies"].astype(np.int64)
    n = len(nodes["depth"])
    is_claim = v8["decl_is_claim"]
    logic_only = v8["decl_logic_only"]
    machinery = v8["machinery"]
    tgt = certifies[a_col]

    P = {}
    P["P1"] = np.ones(len(a_col), dtype=bool)
    P["P2"] = lb.copy()
    P["P3"] = lb & is_claim[d_col]
    P["P4"] = P["P3"] & ~logic_only[d_col] & ~machinery
    # top-k over the frozen P4 order
    idx4 = np.where(P["P4"])[0]
    ordk = np.lexsort((-d_cite[idx4], a_col[idx4]))
    idx4s = idx4[ordk]
    newedge = np.empty(len(idx4s), dtype=bool)
    newedge[0] = True
    newedge[1:] = a_col[idx4s][1:] != a_col[idx4s][:-1]
    starts = np.where(newedge)[0]
    counts = np.diff(np.append(starts, len(idx4s)))
    rank_in_edge = np.concatenate([np.arange(c) for c in counts])
    for k in (1, 4, 16):
        m = np.zeros(len(a_col), dtype=bool)
        m[idx4s[rank_in_edge < k]] = True
        P[f"top{k}"] = m

    order = ["P1", "P2", "P3", "P4", "top16", "top4", "top1"]

    print("=== centrality per projection (bipartite PageRank) ===", flush=True)
    pr = {}
    deg = {}
    for lab in order:
        m = P[lab]
        pr[lab] = pagerank_bipartite(tgt[m], d_col[m], n)
        deg[lab] = np.bincount(d_col[m], minlength=n)
        top = np.argsort(-pr[lab])[:10]
        print(f"  {lab:<6} top: " + ", ".join(names[i] for i in top[:5]), flush=True)

    print("\n=== Q1.2 centrality persistence between adjacent projections ===",
          flush=True)
    print("  (Spearman over the union of each pair's top-1000 by PageRank)",
          flush=True)
    rows = []
    for a, b in zip(order[:-1], order[1:]):
        ta = set(np.argsort(-pr[a])[:1000].tolist())
        tb = set(np.argsort(-pr[b])[:1000].tolist())
        u = np.array(sorted(ta | tb))
        rho = spearmanr(pr[a][u], pr[b][u]).correlation
        overlap = len(ta & tb) / 1000.0
        rows.append({"from": a, "to": b, "spearman_top1000_union": round(float(rho), 4),
                     "top1000_overlap": round(overlap, 4)})
        print(f"  {a:>5} -> {b:<6} spearman={rho:>7.4f}   top-1000 overlap={overlap:>6.1%}",
              flush=True)

    print("\n  REGISTERED PREDICTION: P3->P4 more stable than P2->P3", flush=True)
    p23 = [r for r in rows if r["from"] == "P2"][0]
    p34 = [r for r in rows if r["from"] == "P3"][0]
    verdict = ("CONFIRMED" if p34["spearman_top1000_union"] > p23["spearman_top1000_union"]
               else "FALSIFIED")
    print(f"  P2->P3 = {p23['spearman_top1000_union']:.4f}, "
          f"P3->P4 = {p34['spearman_top1000_union']:.4f}  ==> {verdict}", flush=True)

    print("\n=== weak components per projection ===", flush=True)
    comp_rows = []
    for lab in order:
        m = P[lab]
        g = sp.coo_matrix((np.ones(int(m.sum()), dtype=np.int8),
                           (tgt[m], d_col[m])), shape=(n, n))
        ncomp, lbl = sp.csgraph.connected_components(g, directed=False)
        sizes = np.bincount(lbl)
        touched = np.unique(np.concatenate([tgt[m], d_col[m]]))
        tl = lbl[touched]
        ts = np.bincount(tl)
        ts = ts[ts > 0]
        giant = ts.max() / ts.sum()
        comp_rows.append({"projection": lab, "components_over_touched_nodes": int(len(ts)),
                          "touched_nodes": int(len(touched)),
                          "giant_fraction": round(float(giant), 4)})
        print(f"  {lab:<6} touched={len(touched):>7,}  components={len(ts):>7,}  "
              f"giant={giant:>7.2%}", flush=True)

    out = {"note": "Phase 5 persistence. Centrality on the bipartite incidence; "
                   "no clique expansion (ADR-0005).",
           "registered_prediction": "P3->P4 more stable than P2->P3",
           "prediction_verdict": verdict,
           "centrality_persistence": rows,
           "components": comp_rows,
           "top20_by_projection": {lab: [names[i] for i in np.argsort(-pr[lab])[:20]]
                                   for lab in order}}
    with open(os.path.join(DATA, "persistence_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten data/persistence_results.json", flush=True)


if __name__ == "__main__":
    main()
