"""Global-map structure analyses (Phase 6, Tasks 2 and 3).

Runs four analyses over each admitted edge set (E4_flat, E4, EL0):

  1. relative hubs      per-area within-area hubs vs cross-area mediators
  2. community emergence Louvain communities vs human area labels (AMI)
  3. distance honesty   same-area vs cross-area BFS distance, AUC
  4. verticality        delta_depth over admitted edges

Areas are VALIDATION-ONLY evidence.  They never feed the ordering.

Paths come from map_graph.DATA_DIR / OUT_DIR so the final run can point at the
rebuilt arrays.
"""

import json
import os
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components, dijkstra

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_graph as MG  # noqa: E402

MODULES_TSV = os.environ.get(
    "MAPGRAPH_MODULES_TSV", "/Users/sam/mathmap_data/all_modules.tsv")

EDGE_SETS = ["E4_flat", "E4", "EL0"]

# observed interface vocabulary; name-based REPORTING only, never ordering
NOTATION_NAMES = {
    "OfNat.ofNat", "HAdd.hAdd", "HMul.hMul", "DFunLike.coe",
    "Membership.mem", "HSMul.hSMul", "HSub.hSub",
}

# areas that are library infrastructure rather than mathematics; used for a
# REPORTING-ONLY diagnostic that is independent of the lane construction
META_AREAS = {"Core", "Tactic", "Util", "Lean", "Testing", "Init", "Control"}

N_PAIRS = int(os.environ.get("MAP_N_PAIRS", "1500"))
BFS_CAP = 12
SEED = 20260821
# 0 = run community detection at full scale
COMMUNITY_SUBSAMPLE = int(os.environ.get("MAP_COMMUNITY_SUBSAMPLE", "0"))
# "louvain" (networkx, better quality, slow) or "lpa" (vectorised scipy, fast)
COMMUNITY_METHOD = os.environ.get("MAP_COMMUNITY_METHOD", "louvain")

_T0 = time.time()


def log(msg):
    print("[%7.1fs] %s" % (time.time() - _T0, msg), flush=True)


# ---------------------------------------------------------------------------
# Task 2 — area mapping (validation-only)
# ---------------------------------------------------------------------------
def build_areas(names):
    """area code per declaration id, plus the code -> name table."""
    log("building area map from %s" % MODULES_TSV)
    mod = {}
    if os.path.exists(MODULES_TSV):
        with open(MODULES_TSV) as fh:
            for line in fh:
                nm, _, m = line.rstrip("\n").partition("\t")
                if m:
                    mod[nm] = m
        log("  %d name->module rows" % len(mod))
    else:
        log("  MISSING: all declarations will be Unknown")

    area_of = {}
    codes = {"Unknown": 0, "Core": 1}
    area = np.zeros(len(names), dtype=np.int16)
    n_hit = 0
    for i, nm in enumerate(names):
        m = mod.get(nm)
        if m is None:
            continue
        n_hit += 1
        a = area_of.get(m)
        if a is None:
            parts = m.split(".")
            if parts[0] == "Mathlib" and len(parts) >= 2:
                lab = parts[1]
            else:
                lab = "Core"
            a = codes.setdefault(lab, len(codes))
            area_of[m] = a
        area[i] = a
    log("  %d / %d declarations have a module (%.1f%%); %d areas"
        % (n_hit, len(names), 100.0 * n_hit / len(names), len(codes)))
    names_by_code = [None] * len(codes)
    for k, v in codes.items():
        names_by_code[v] = k
    return area, names_by_code


def area_distribution(area, area_names):
    cnt = np.bincount(area, minlength=len(area_names))
    order = np.argsort(-cnt)
    return [{"area": area_names[i], "n_decls": int(cnt[i])} for i in order]


# ---------------------------------------------------------------------------
def classify(decl_ids, A, area_names=None):
    """Hub class, precedence notation > generated > transport > mathematics.

    notation-suspect is a name-lookup against the observed interface set and is
    reporting-only; transport is depth_stmt <= 1.
    """
    names = A["names"]
    out = []
    for d in decl_ids:
        d = int(d)
        if names[d] in NOTATION_NAMES:
            out.append("notation")
        elif bool(A["gen"][d]):
            out.append("generated")
        elif int(A["depth_stmt"][d]) <= 1:
            out.append("transport")
        else:
            out.append("mathematics")
    return out


def class_vector(A):
    """vectorised class code per declaration: 0 notation 1 generated
    2 transport 3 mathematics."""
    names = A["names"]
    n = len(names)
    cls = np.full(n, 3, dtype=np.int8)
    cls[A["depth_stmt"] <= 1] = 2
    cls[A["gen"]] = 1
    for nm in NOTATION_NAMES:
        try:
            cls[names.index(nm)] = 0
        except ValueError:
            pass
    return cls


CLASS_LABELS = ["notation", "generated", "transport", "mathematics"]


# ---------------------------------------------------------------------------
# Analysis 1 — relative hubs
# ---------------------------------------------------------------------------
def analysis_hubs(src, dst, A, area, area_names, cls, top=15):
    log("  [1] relative hubs")
    n = len(A["names"])
    known = (area[src] != 0) & (area[dst] != 0)
    same = known & (area[src] == area[dst])
    cross = known & (area[src] != area[dst])

    in_same = np.bincount(dst[same], minlength=n)
    in_cross = np.bincount(dst[cross], minlength=n)
    in_all = np.bincount(dst, minlength=n)

    res = {}
    # global link-mass split by hub class
    def mass(mask):
        c = np.bincount(cls[dst[mask]], minlength=4)
        tot = max(1, int(c.sum()))
        return {CLASS_LABELS[i]: float(c[i]) / tot for i in range(4)} | {
            "n_links": int(c.sum())}
    res["link_mass"] = {
        "same_area": mass(same),
        "cross_area": mass(cross),
        "all_edges": mass(np.ones(len(dst), dtype=bool)),
    }
    res["link_mass"]["cross_area_plumbing_share"] = (
        res["link_mass"]["cross_area"]["transport"]
        + res["link_mass"]["cross_area"]["notation"]
        + res["link_mass"]["cross_area"]["generated"])
    res["link_mass"]["same_area_plumbing_share"] = (
        res["link_mass"]["same_area"]["transport"]
        + res["link_mass"]["same_area"]["notation"]
        + res["link_mass"]["same_area"]["generated"])

    # per-area tables
    per_area = {}
    hub_areas = np.unique(area[dst[known]])
    for a in hub_areas:
        if a == 0:
            continue
        members = np.flatnonzero(area == a)
        if len(members) == 0:
            continue
        s = in_same[members]
        c = in_cross[members]
        if s.sum() + c.sum() == 0:
            continue
        top_s = members[np.argsort(-s)[:top]]
        top_c = members[np.argsort(-c)[:top]]
        per_area[area_names[a]] = {
            "n_decls": int(len(members)),
            "in_same_total": int(s.sum()),
            "in_cross_total": int(c.sum()),
            "within_area_hubs": [
                {"name": A["names"][int(d)], "in_same": int(in_same[d]),
                 "in_cross": int(in_cross[d]), "in_all": int(in_all[d]),
                 "class": CLASS_LABELS[int(cls[d])],
                 "depth_stmt": int(A["depth_stmt"][d])}
                for d in top_s if in_same[d] > 0],
            "cross_area_mediators": [
                {"name": A["names"][int(d)], "in_same": int(in_same[d]),
                 "in_cross": int(in_cross[d]), "in_all": int(in_all[d]),
                 "class": CLASS_LABELS[int(cls[d])],
                 "depth_stmt": int(A["depth_stmt"][d])}
                for d in top_c if in_cross[d] > 0],
        }
    res["per_area"] = per_area

    # class composition of the top-15 lists, pooled over areas
    def pooled(key):
        c = {k: 0 for k in CLASS_LABELS}
        for v in per_area.values():
            for h in v[key]:
                c[h["class"]] += 1
        tot = max(1, sum(c.values()))
        return {k: v / tot for k, v in c.items()} | {"n": tot}
    res["pooled_top15_classes"] = {
        "within_area_hubs": pooled("within_area_hubs"),
        "cross_area_mediators": pooled("cross_area_mediators"),
    }

    # area assortativity: pure human-label evidence, independent of the lanes
    meta = np.array([nm in META_AREAS for nm in area_names])
    res["area_assortativity"] = {
        "within_area_edge_share": float(same.mean()),
        "dst_in_meta_area_share": float(meta[area[dst]].mean()),
        "src_in_meta_area_share": float(meta[area[src]].mean()),
    }

    # where does cross-area mass LAND, by hub area?  Purely area-based, so it
    # is independent of the lane/depth construction that defines the edge sets.
    ca = np.bincount(area[dst[cross]], minlength=len(area_names))
    tot_c = max(1, int(cross.sum()))
    res["cross_mass_by_hub_area"] = [
        {"area": area_names[i], "links": int(ca[i]),
         "share": float(ca[i]) / tot_c}
        for i in np.argsort(-ca)[:12] if ca[i] > 0]
    res["link_mass"]["cross_area_core_or_tactic_share"] = float(
        sum(ca[i] for i, nm in enumerate(area_names)
            if nm in META_AREAS) / tot_c)

    # global top hubs by total in-degree, and the mass they absorb
    top_g = np.argsort(-in_all)[:100]
    res["global_top_hubs"] = [
        {"name": A["names"][int(d)], "in_all": int(in_all[d]),
         "in_cross": int(in_cross[d]), "class": CLASS_LABELS[int(cls[d])],
         "area": area_names[int(area[d])], "depth_stmt": int(A["depth_stmt"][d]),
         "n_areas_citing": int(len(np.unique(area[src[dst == d]])))}
        for d in top_g[:25]]
    res["top100_hub_mass"] = {
        "share_of_all_links": float(in_all[top_g].sum() / max(1, len(dst))),
        "share_of_cross_links": float(
            in_cross[top_g].sum() / max(1, int(cross.sum()))),
        "class_counts": {CLASS_LABELS[i]: int(c) for i, c in
                         enumerate(np.bincount(cls[top_g], minlength=4))},
    }
    log("      cross-area link mass: math %.3f transport %.3f notation %.3f gen %.3f"
        % (res["link_mass"]["cross_area"]["mathematics"],
           res["link_mass"]["cross_area"]["transport"],
           res["link_mass"]["cross_area"]["notation"],
           res["link_mass"]["cross_area"]["generated"]))
    return res


# ---------------------------------------------------------------------------
# undirected graph helpers
# ---------------------------------------------------------------------------
def build_graph(src, dst, n):
    """symmetric weighted CSR; weight = collapsed edge multiplicity."""
    M = sp.coo_matrix((np.ones(len(src), dtype=np.float32),
                       (src.astype(np.int64), dst.astype(np.int64))),
                      shape=(n, n)).tocsr()
    M = M + M.T
    M.sum_duplicates()
    return M


def largest_component(M):
    ncomp, lab = connected_components(M, directed=False)
    sizes = np.bincount(lab)
    big = int(np.argmax(sizes))
    nodes = np.flatnonzero(lab == big)
    return nodes, ncomp, int(sizes[big])


# ---------------------------------------------------------------------------
# Analysis 2 — community emergence
# ---------------------------------------------------------------------------
def lpa_sparse(S, rng, n_iter=80, frac=0.5):
    """Semi-synchronous weighted label propagation, vectorised with scipy.

    Fallback when networkx Louvain is too slow at full scale.  Each round a
    random half of the nodes adopt the highest-weight label among their
    neighbours; ties broken by a fixed random priority.
    """
    n = S.shape[0]
    lab = np.arange(n, dtype=np.int64)
    S = S.tocsr()
    for it in range(n_iter):
        k = lab.max() + 1
        H = sp.csr_matrix((np.ones(n, dtype=np.float32),
                           (np.arange(n), lab)), shape=(n, k))
        W = (S @ H).tocsr()
        new = lab.copy()
        # vectorised argmax per CSR row
        rowrep = np.repeat(np.arange(n), np.diff(W.indptr))
        ordr = np.lexsort((-W.data, rowrep))
        rr = rowrep[ordr]
        first = np.empty(len(rr), dtype=bool)
        if len(rr):
            first[0] = True
            np.not_equal(rr[1:], rr[:-1], out=first[1:])
            new[rr[first]] = W.indices[ordr[first]]
        upd = rng.random(n) < frac
        moved = int((new[upd] != lab[upd]).sum())
        lab[upd] = new[upd]
        if it % 10 == 0 or moved == 0:
            log("        lpa iter %d: %d moves, %d labels"
                % (it, moved, len(np.unique(lab))))
        if moved == 0:
            break
    _, lab = np.unique(lab, return_inverse=True)
    return lab


def modularity_from_labels(S, lab):
    """Newman modularity of a labelling on a symmetric weighted CSR matrix."""
    S = S.tocoo()
    deg = np.asarray(S.sum(axis=1)).ravel()
    two_m = deg.sum()
    if two_m == 0:
        return 0.0
    k = lab.max() + 1
    same = lab[S.row] == lab[S.col]
    in_w = np.bincount(lab[S.row[same]], weights=S.data[same], minlength=k)
    deg_c = np.bincount(lab, weights=deg, minlength=k)
    return float((in_w / two_m - (deg_c / two_m) ** 2).sum())


def analysis_communities(M, nodes, A, area, rng):
    from sklearn.metrics import adjusted_mutual_info_score

    log("  [2] community emergence (method=%s)" % COMMUNITY_METHOD)
    sub_nodes = nodes
    subsampled = False
    if COMMUNITY_SUBSAMPLE and len(nodes) > COMMUNITY_SUBSAMPLE:
        sub_nodes = np.sort(rng.choice(nodes, COMMUNITY_SUBSAMPLE,
                                       replace=False))
        subsampled = True
    S = M[sub_nodes][:, sub_nodes].tocsr()
    log("      graph: %d nodes, %d undirected edges%s"
        % (len(sub_nodes), S.nnz // 2, " (SUBSAMPLED)" if subsampled else ""))
    t = time.time()
    if COMMUNITY_METHOD == "lpa":
        lab = lpa_sparse(S, rng)
        n_comm = int(lab.max() + 1)
        mod = modularity_from_labels(S, lab)
    else:
        import networkx as nx
        from networkx.algorithms.community import louvain_communities
        Sc = S.tocoo()
        G = nx.Graph()
        G.add_nodes_from(range(len(sub_nodes)))
        keep = Sc.row < Sc.col
        G.add_weighted_edges_from(zip(Sc.row[keep].tolist(),
                                      Sc.col[keep].tolist(),
                                      Sc.data[keep].tolist()))
        del Sc
        log("      running louvain")
        comms = louvain_communities(G, weight="weight", seed=SEED)
        lab = np.full(len(sub_nodes), -1, dtype=np.int64)
        for ci, c in enumerate(comms):
            lab[list(c)] = ci
        n_comm = len(comms)
        mod = float(nx.algorithms.community.modularity(G, comms,
                                                       weight="weight"))
        del G
    log("      %s done in %.1fs: %d communities"
        % (COMMUNITY_METHOD, time.time() - t, n_comm))
    a = area[sub_nodes]
    known = a != 0
    ami = float(adjusted_mutual_info_score(a[known], lab[known]))
    sizes = np.bincount(lab[lab >= 0])
    log("      AMI vs areas (%d known-area nodes): %.4f  modularity %.4f"
        % (known.sum(), ami, mod))
    return {
        "method": COMMUNITY_METHOD,
        "n_nodes": int(len(sub_nodes)),
        "n_edges_undirected": int(S.nnz // 2),
        "subsampled": subsampled,
        "n_communities": int(n_comm),
        "largest_community_frac": float(sizes.max() / sizes.sum()),
        "n_communities_ge_100": int((sizes >= 100).sum()),
        "n_known_area_nodes": int(known.sum()),
        "AMI": ami,
        "modularity": mod,
    }


# ---------------------------------------------------------------------------
# Analysis 3 — distance honesty
# ---------------------------------------------------------------------------
def analysis_distance(M, nodes, A, area, rng, n_pairs=N_PAIRS):
    from sklearn.metrics import roc_auc_score
    log("  [3] distance honesty")
    in_lcc = np.zeros(M.shape[0], dtype=bool)
    in_lcc[nodes] = True
    pool = np.flatnonzero(in_lcc & (A["kind"] == 0) & (~A["gen"])
                          & (area != 0))
    log("      theorem pool in largest component with known area: %d"
        % len(pool))
    if len(pool) < 100:
        return {"error": "pool too small", "pool": int(len(pool))}

    pa = area[pool]
    by_area = {}
    for a in np.unique(pa):
        by_area[int(a)] = pool[pa == a]
    usable = np.array([a for a, v in by_area.items() if len(v) >= 2])
    usable_pool = pool[np.isin(pa, usable)]

    def sample_pairs(same):
        us, vs = [], []
        while len(us) < n_pairs:
            u = int(rng.choice(usable_pool))
            a = int(area[u])
            if same:
                cand = by_area[a]
                v = int(rng.choice(cand))
                if v == u:
                    continue
            else:
                v = int(rng.choice(usable_pool))
                if int(area[v]) == a:
                    continue
            us.append(u)
            vs.append(v)
        return np.array(us), np.array(vs)

    su, sv = sample_pairs(True)
    cu, cv = sample_pairs(False)
    U = np.concatenate([su, cu])
    V = np.concatenate([sv, cv])
    lab = np.concatenate([np.ones(len(su)), np.zeros(len(cu))])

    uniq, inv = np.unique(U, return_inverse=True)
    log("      BFS from %d distinct sources (cap %d)" % (len(uniq), BFS_CAP))
    Mb = M.tocsr()
    dists = np.full(len(U), float(BFS_CAP))
    CH = 32
    for s in range(0, len(uniq), CH):
        chunk = uniq[s:s + CH]
        D = dijkstra(Mb, directed=False, indices=chunk, unweighted=True,
                     limit=BFS_CAP)
        sel = np.flatnonzero((inv >= s) & (inv < s + len(chunk)))
        dists[sel] = D[inv[sel] - s, V[sel]]
        if (s // CH) % 5 == 0:
            log("        %d / %d sources" % (s, len(uniq)))
    dists[~np.isfinite(dists)] = BFS_CAP
    dists = np.minimum(dists, BFS_CAP)

    sd, cd = dists[lab == 1], dists[lab == 0]
    auc = float(roc_auc_score(lab, -dists))

    def summ(x):
        return {
            "n": int(len(x)), "mean": float(x.mean()),
            "median": float(np.median(x)),
            "q": {str(q): float(np.percentile(x, q))
                  for q in (10, 25, 50, 75, 90)},
            "frac_capped": float((x >= BFS_CAP).mean()),
            "hist": {str(i): int((x == i).sum()) for i in range(BFS_CAP + 1)},
        }
    log("      same mean %.3f  cross mean %.3f  AUC %.4f"
        % (sd.mean(), cd.mean(), auc))
    return {"same_area": summ(sd), "cross_area": summ(cd), "AUC": auc,
            "cap": BFS_CAP, "n_pairs_each": n_pairs}


# ---------------------------------------------------------------------------
# Analysis 4 — verticality
# ---------------------------------------------------------------------------
def analysis_verticality(src, dst, A, area):
    log("  [4] verticality")
    depth = A["depth"].astype(np.int64)
    dd = depth[src] - depth[dst]
    known = (area[src] != 0) & (area[dst] != 0)
    cross = known & (area[src] != area[dst])
    same = known & (area[src] == area[dst])

    def summ(x):
        if len(x) == 0:
            return {"n": 0}
        return {
            "n": int(len(x)), "mean": float(x.mean()),
            "q": {str(q): float(np.percentile(x, q))
                  for q in (1, 5, 10, 25, 50, 75, 90, 95, 99)},
            "frac_le_0": float((x <= 0).mean()),
            "frac_gt_20": float((x > 20).mean()),
        }
    out = {"all_edges": summ(dd), "cross_area": summ(dd[cross]),
           "same_area": summ(dd[same])}
    log("      all median %.0f p90 %.0f | cross median %.0f p90 %.0f"
        % (out["all_edges"]["q"]["50"], out["all_edges"]["q"]["90"],
           out["cross_area"]["q"]["50"], out["cross_area"]["q"]["90"]))
    return out


# ---------------------------------------------------------------------------
def main():
    A = MG.load_arrays()
    n = len(A["names"])
    area, area_names = build_areas(A["names"])
    cls = class_vector(A)

    out = {
        "data_dir": MG.DATA_DIR,
        "modules_tsv": MODULES_TSV,
        "modules_tsv_present": os.path.exists(MODULES_TSV),
        "area_distribution": area_distribution(area, area_names),
        "n_areas": len(area_names),
        "edge_sets": {},
    }
    np.savez_compressed(os.path.join(MG.OUT_DIR, "areas.npz"),
                        area=area, area_names=np.array(area_names))
    log("area distribution (top 15): %s"
        % ", ".join("%s=%d" % (d["area"], d["n_decls"])
                    for d in out["area_distribution"][:15]))

    for name in EDGE_SETS:
        p = os.path.join(MG.OUT_DIR, "edges_%s.npz" % name)
        if not os.path.exists(p):
            log("SKIP %s (missing)" % p)
            continue
        log("=== edge set %s" % name)
        z = np.load(p)
        src = z["src_decl"].astype(np.int64)
        dst = z["dst_decl"].astype(np.int64)
        rng = np.random.default_rng(SEED)
        r = {"n_edges": int(len(src))}
        r["hubs"] = analysis_hubs(src, dst, A, area, area_names, cls)
        M = build_graph(src, dst, n)
        nodes, ncomp, big = largest_component(M)
        # connected_components counts isolated vertices of the full id space;
        # restrict to vertices with at least one incident edge
        deg = np.diff(M.indptr)
        r["graph"] = {
            "n_nodes_with_edges": int((deg > 0).sum()),
            "n_components_over_active_nodes": int(ncomp - (deg == 0).sum()),
            "largest_component_nodes": big,
            "largest_component_frac_of_active":
                float(big / max(1, (deg > 0).sum())),
        }
        log("      LCC %d nodes / %d active (%.3f)"
            % (big, (deg > 0).sum(), r["graph"]["largest_component_frac_of_active"]))
        r["communities"] = analysis_communities(M, nodes, A, area, rng)
        r["distance"] = analysis_distance(M, nodes, A, area, rng)
        r["verticality"] = analysis_verticality(src, dst, A, area)
        out["edge_sets"][name] = r
        with open(os.path.join(MG.OUT_DIR, "map_analysis.json"), "w") as fh:
            json.dump(out, fh, indent=2)
        log("wrote partial results for %s" % name)

    with open(os.path.join(MG.OUT_DIR, "map_analysis.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    log("DONE -> %s" % os.path.join(MG.OUT_DIR, "map_analysis.json"))


if __name__ == "__main__":
    main()
