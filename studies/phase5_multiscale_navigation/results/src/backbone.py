#!/usr/bin/env python3
"""Phase 5: the connected filtration (approaches 1 and 2, converged).

Design follows the graph-theory consult. Three decisions that matter:

1. BACKBONE = maximum-weight spanning ANTI-ARBORESCENCE, not a spanning tree.
   Every edge points strictly downward in depth (the record is a DAG), so a
   per-node argmax over its citations can never create a cycle: greedy
   selection is provably optimal and Chu-Liu/Edmonds is vacuous here. Add a
   virtual root (the ambient framework) and attach every sink to it. Result:
   one component, always, by construction -- no union-find, no repair.
   This also beats a spanning tree on the owner's own requirement, because
   each node picks its OWN best parent (local) rather than having its fate
   decided by far-away edges (global).

2. FILTER = configuration-null z-score, not the disparity filter. Disparity
   is locally normalised but one-sided: it never sees that a lemma is cited
   200,000 times library-wide, and global commonness is precisely our
   plumbing signal. The configuration null conditions on BOTH endpoints, so a
   hub lemma's edges must be exceptional to survive. Plumbing detection falls
   out of the null rather than a blacklist.

3. NESTING INVARIANT: one static score per edge, computed once on the full
   graph, never recomputed on a filtered graph. The slider is a threshold on
   that score, stored as a rank array; every level is a PREFIX of one sorted
   array. Nesting then cannot be violated rather than merely being tested.
   Backbone edges get rank 0, so every level contains the backbone and is
   therefore connected.

Weights are log-linear with inverse document frequency as the workhorse:
idf is measured, not tuned, and encodes "globally common implies probably
plumbing" without naming anything. Raw depth GAP is deliberately not used:
our own measurement (median 22, p99 268) shows it barely discriminates.
"""
import json, os
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))


def main():
    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    nodes = np.load(os.path.join(DATA, "nodes.npz"))
    v8 = np.load(os.path.join(DATA, "v8_mask.npz"))
    names = json.load(open(os.path.join(DATA, "names.json")))

    a_col = inc["artifact"].astype(np.int64)
    d_col = inc["decl"].astype(np.int64)
    roles = inc["roles"]
    lb = inc["load_bearing"]
    in_sw = inc["in_stmt_world"]
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"].astype(np.float64)
    n = len(depth)
    n_art = len(certifies)
    tgt = certifies[a_col]

    base = lb & (tgt != d_col)
    bi = np.where(base)[0]
    print(f"base incidences (load-bearing): {len(bi):,}", flush=True)

    # ---- prerequisite for free stratification -------------------------
    # The consult's mechanism 1: purity rises with depth only if deeper
    # theorems have larger proofs. Verify BEFORE relying on it.
    csize = np.bincount(a_col[bi], minlength=n_art)
    live_art = np.where(csize > 0)[0]
    sample = live_art if len(live_art) < 200000 else np.random.default_rng(0).choice(
        live_art, 200000, replace=False)
    rho = spearmanr(depth[certifies[sample]], csize[sample]).correlation
    print(f"PREREQUISITE Spearman(depth(T), |citations|) = {rho:.4f}", flush=True)
    print("  (mechanism-1 stratification fires only if this is strongly positive)",
          flush=True)

    # ---- edge weight ---------------------------------------------------
    # m_role: applied as a proof step counts full; argument/let positions less
    r = roles[bi]
    m_role = np.where(r[:, 0] > 0, 1.0,
              np.where((r[:, 1] > 0) | (r[:, 2] > 0), 0.7, 0.5))
    # m_stmt: a citation the proof INTRODUCES is a step; one already implied
    # by the statement is closer to a definitional dependency
    m_stmt = np.where(in_sw[bi], 1.0, 1.5)
    # idf over proofs: measured commonness, no names
    dfc = np.bincount(d_col[bi], minlength=n).astype(np.float64)
    n_proofs = float(len(np.unique(a_col[bi])))
    idf = np.log(n_proofs / np.maximum(dfc, 1.0))
    idf = np.maximum(idf, 0.0)
    # DEPTH IS THE PRIMARY ORDERING. Our own ablation put the depth key
    # first among ranking signals (+3.45 points, the largest single
    # contributor), and the owner's standing finding is that the key move
    # correlates with the mathematical depth of the cited theorem. So the
    # absolute depth of the CITED declaration drives the weight; the ratio to
    # the target's depth is kept only as a mild secondary term (a citation
    # nearly as deep as its target is the last big step rather than a descent
    # into foundations). The raw depth GAP is deliberately unused: measured
    # median 22 / p99 268 means it barely discriminates.
    dmax = float(depth.max())
    dt = np.maximum(depth[tgt[bi]], 1.0)
    m_depth = ((0.20 + 0.80 * (depth[d_col[bi]] / dmax))
               * (0.70 + 0.30 * np.clip(depth[d_col[bi]] / dt, 0.0, 1.0)))

    w = (m_role * m_stmt * m_depth * idf[d_col[bi]]).astype(np.float64)
    w = np.maximum(w, 1e-9)
    print(f"weights: mean={w.mean():.3f} p50={np.percentile(w,50):.3f} "
          f"p99={np.percentile(w,99):.3f}", flush=True)

    # ---- BACKBONE: per-proof argmax (anti-arborescence, T0+) ------------
    ordA = np.argsort(a_col[bi], kind="stable")
    bi_a = bi[ordA]; w_a = w[ordA]
    aa = a_col[bi_a]
    starts = np.where(np.concatenate(([True], aa[1:] != aa[:-1])))[0]
    seg_max = np.maximum.reduceat(w_a, starts)
    counts = np.diff(np.append(starts, len(bi_a)))
    is_max = w_a >= np.repeat(seg_max, counts)
    first_max = np.zeros(len(bi_a), dtype=bool)
    idx_first = starts + np.array([np.argmax(is_max[s:s + c])
                                   for s, c in zip(starts, counts)])
    first_max[idx_first] = True
    backbone_inc = bi_a[first_max]
    print(f"backbone edges (one per proof, T0+): {len(backbone_inc):,}", flush=True)

    # ---- dedup to declaration-level directed edges ----------------------
    key = tgt[bi].astype(np.int64) * n + d_col[bi].astype(np.int64)
    ordk = np.argsort(key, kind="stable")
    key_s = key[ordk]; w_s = w[ordk]; bi_s = bi[ordk]
    us = np.where(np.concatenate(([True], key_s[1:] != key_s[:-1])))[0]
    eu = (key_s[us] // n).astype(np.int64)       # citing (target theorem)
    ev = (key_s[us] % n).astype(np.int64)        # cited
    ew = np.maximum.reduceat(w_s, us)
    print(f"distinct declaration edges: {len(eu):,}", flush=True)

    bkey = np.unique(tgt[backbone_inc].astype(np.int64) * n
                     + d_col[backbone_inc].astype(np.int64))
    in_backbone = np.isin(key_s[us], bkey)
    print(f"backbone as distinct edges: {int(in_backbone.sum()):,}", flush=True)

    # ---- FILTER SCORE: configuration-null z ----------------------------
    W = ew.sum()
    s_out = np.bincount(eu, weights=ew, minlength=n)
    s_in = np.bincount(ev, weights=ew, minlength=n)
    p_null = (s_out[eu] * s_in[ev]) / (W * W)
    p_null = np.clip(p_null, 1e-15, 1 - 1e-15)
    mean = W * p_null
    var = W * p_null * (1.0 - p_null)
    z = (ew - mean) / np.sqrt(np.maximum(var, 1e-12))
    print(f"z: p50={np.percentile(z,50):.2f} p90={np.percentile(z,90):.2f} "
          f"p99={np.percentile(z,99):.2f} max={z.max():.1f}", flush=True)

    # ---- the nested family, as one rank array --------------------------
    score = z.copy()
    score[in_backbone] = np.inf                  # backbone always first
    rank_order = np.argsort(-score, kind="stable")
    rank = np.empty(len(eu), dtype=np.int64)
    rank[rank_order] = np.arange(len(eu))

    touched = np.unique(np.concatenate([eu, ev]))
    ROOT = n                                     # virtual root: the ambient
    NN = n + 1                                   # logical framework

    def components(mask, with_root):
        """Weak components over the nodes this graph actually touches.
        with_root grounds every sink at the virtual root, which is what makes
        the family literally connected at every level."""
        u, v = eu[mask], ev[mask]
        if with_root:
            has_parent = np.zeros(NN, dtype=bool)
            has_parent[u] = True
            sinks = touched[~has_parent[touched]]
            u = np.concatenate([u, sinks])
            v = np.concatenate([v, np.full(len(sinks), ROOT)])
        g = sp.coo_matrix((np.ones(len(u), dtype=np.int8), (u, v)), shape=(NN, NN))
        _, lab = connected_components(g, directed=False)
        nodeset = np.concatenate([touched, [ROOT]]) if with_root else touched
        sz = np.bincount(lab[nodeset]); sz = sz[sz > 0]
        return len(sz), float(sz.max() / sz.sum())

    print(f"\n=== slider: every level is a PREFIX of one sorted array ===",
          flush=True)
    print(f"{'level':>22} {'edges':>12} {'comps(+root)':>11} {'giant':>9}   "
          f"{'comps(math)':>9} {'giant':>8}", flush=True)
    rows = []
    n_bb = int(in_backbone.sum())
    levels = [("backbone only", n_bb)]
    for frac in (0.05, 0.1, 0.25, 0.5, 0.75, 1.0):
        levels.append((f"top {int(frac*100)}% by z", max(n_bb, int(frac * len(eu)))))
    for label, cut in levels:
        keep = rank < cut
        c_root, g_root = components(keep, True)
        c_math, g_math = components(keep, False)
        rows.append({"level": label, "edges": int(keep.sum()),
                     "components_with_root": c_root, "giant_with_root": round(g_root, 4),
                     "components_math_only": c_math, "giant_math_only": round(g_math, 4)})
        print(f"{label:>22} {int(keep.sum()):>12,} {c_root:>11,} "
              f"{g_root:>8.2%}   {c_math:>9,} {g_math:>8.2%}", flush=True)

    # nesting is structural, but assert it once
    ok = all(rows[i]["edges"] <= rows[i + 1]["edges"] for i in range(len(rows) - 1))
    print(f"\nnested (edges monotone): {ok}", flush=True)

    # ---- does the backbone survive the filter on its own merits? -------
    zb = z[in_backbone]
    thresh = np.percentile(z, 75)
    print(f"backbone edges that would pass the top-25% filter anyway: "
          f"{float((zb >= thresh).mean()):.1%}", flush=True)

    # ---- stratified purity of the backbone -----------------------------
    is_claim = v8["decl_is_claim"]; logic_only = v8["decl_logic_only"]
    content_decl = is_claim & ~logic_only
    kind = nodes["kind"]
    is_def = np.isin(kind, [1, 2, 5, 6, 7])      # def/inductive/opaque/quot/axiom
    print("\n=== definitions and constructions in the structure ===", flush=True)
    print(f"  cited declarations that are definitions/constructions: "
          f"{int(is_def[ev].sum()):,} of {len(ev):,} edges "
          f"({100*is_def[ev].mean():.1f}%)", flush=True)
    print(f"  BACKBONE edges whose cited endpoint is a definition: "
          f"{int(is_def[ev[in_backbone]].sum()):,} "
          f"({100*is_def[ev[in_backbone]].mean():.1f}%)", flush=True)
    print(f"  distinct definitions present as nodes: "
          f"{len(np.unique(ev[is_def[ev]])):,}", flush=True)
    print("\n=== backbone composition by depth of the citing theorem ===",
          flush=True)
    bd = depth[eu]
    comp_rows = []
    for lo, hi in [(0, 10), (10, 25), (25, 50), (50, 75), (75, 125), (125, 350)]:
        sel = in_backbone & (bd >= lo) & (bd < hi)
        if not sel.any():
            continue
        frac = float(content_decl[ev[sel]].mean())
        comp_rows.append({"band": f"{lo}-{hi}", "edges": int(sel.sum()),
                          "content_fraction": round(frac, 4)})
        print(f"  depth {lo:>3}-{hi:<3}  edges={int(sel.sum()):>7,}  "
              f"cited is content: {frac:>6.1%}", flush=True)

    out = {"prerequisite_spearman_depth_vs_ncitations": float(rho),
           "base_incidences": int(len(bi)),
           "distinct_edges": int(len(eu)),
           "backbone_edges": int(n_bb),
           "slider": rows, "nested": bool(ok),
           "backbone_passes_filter_alone": float((zb >= thresh).mean()),
           "backbone_composition_by_depth": comp_rows}
    with open(os.path.join(DATA, "backbone_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    np.savez_compressed(os.path.join(DATA, "filtration.npz"),
                        eu=eu.astype(np.int32), ev=ev.astype(np.int32),
                        weight=ew.astype(np.float32), z=z.astype(np.float32),
                        rank=rank.astype(np.uint32),
                        in_backbone=in_backbone)
    print("\nwritten data/backbone_results.json and data/filtration.npz", flush=True)


if __name__ == "__main__":
    main()
