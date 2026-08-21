"""Shortcut precision and recall — the thing that actually matters for a map.

WHY THIS EXISTS. An earlier navigability test asked "does the graph stay
connected when junk edges are removed?", got 94.8%, and concluded junk was not
a problem. That question was irrelevant and the conclusion was wrong.

The danger is not disconnection. It is FALSE PROXIMITY. Universal machinery
(`Eq.trans`, `congrArg`, an instance) is cited by an enormous number of proofs,
so admitting one such edge wires thousands of unrelated theorems together
within two hops. The graph stays connected either way; what changes is
DISTANCE. A map that says two unrelated theorems are adjacent is lying, and it
lies precisely by routing through Lean's plumbing.

The mirror failure matters just as much: a genuinely important lemma that many
results depend on IS a legitimate shortcut. Losing it means the map fails to
show real mathematical structure.

So there are two quantities, and both are about PATHS, not components:

  SHORTCUT PRECISION  of the shortcuts the map offers, how many are real
                      mathematics rather than machinery?
  SHORTCUT RECALL     of the shortcuts that SHOULD exist (important lemmas
                      many proofs genuinely rest on), how many survive?

Everything here samples: exact betweenness over ~700k nodes is infeasible, and
a sampled estimate with a stated sample size is honest where an exact number
we cannot compute is not.
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import breadth_first_order, shortest_path


def build(c, base, ranks, k):
    """The undirected graph a reader traverses at top-k."""
    sel = ranks < k
    u = c.inc_target[base[sel]]
    v = c.inc_decl[base[sel]]
    touched = np.unique(np.concatenate([u, v]))
    nid = -np.ones(c.n_nodes, dtype=np.int64)
    nid[touched] = np.arange(len(touched))
    N = len(touched)
    g = sp.coo_matrix((np.ones(len(u), np.int8), (nid[u], nid[v])),
                      shape=(N, N)).tocsr()
    g = ((g + g.T) > 0).astype(np.int8)
    return g, nid, touched, sel


def hub_composition(c, g, touched, junk_node, top=200):
    """The most-connected nodes ARE the shortcuts. What are they made of?

    Degree is the crudest possible proxy for "everything routes through this",
    but it is exact and cheap, and for this question it is close to sufficient:
    a node with degree 50,000 is a shortcut whether or not any particular
    shortest path uses it.
    """
    deg = np.asarray(g.sum(axis=1)).ravel()
    order = np.argsort(-deg)[:top]
    ids = touched[order]
    isjunk = junk_node[ids]
    return {
        "top_n": int(top),
        "junk_share_of_top_hubs": float(isjunk.mean()),
        "junk_share_of_all_nodes": float(junk_node[touched].mean()),
        "enrichment": float(isjunk.mean() / max(junk_node[touched].mean(), 1e-9)),
        "degree_mass_on_junk": float(deg[order][isjunk].sum()
                                     / max(deg[order].sum(), 1e-9)),
        "top_hubs": [{"name": c.names[int(i)], "degree": int(deg[o]),
                      "junk": bool(junk_node[int(i)])}
                     for i, o in list(zip(ids, order))[:25]],
    }


def distance_distortion(g, junk_col, n_sources=60, seed=11):
    """Do junk edges shorten paths between things that are actually far apart?

    Runs BFS from the same sampled sources on the full graph and on the
    mathematics-only graph, and compares distances over pairs reachable in
    BOTH. If junk edges are creating false proximity, removing them lengthens
    paths sharply. If they are riding along real structure, distances barely
    move.

    This is the measurement the component test could not make.
    """
    N = g.shape[0]
    rng = np.random.default_rng(seed)
    deg = np.asarray(g.sum(axis=1)).ravel()
    live = np.where(deg > 0)[0]
    src = rng.choice(live, size=min(n_sources, len(live)), replace=False)

    keep = ~junk_col
    gm = g[:, keep][keep, :]
    remap = -np.ones(N, dtype=np.int64)
    remap[np.where(keep)[0]] = np.arange(int(keep.sum()))

    d_all = shortest_path(g, method="D", unweighted=True, indices=src)
    src_m = remap[src]
    ok = src_m >= 0
    d_math = shortest_path(gm, method="D", unweighted=True,
                           indices=src_m[ok]) if ok.any() else None
    if d_math is None:
        return {"error": "no mathematics-only sources"}

    a = d_all[ok][:, keep]
    b = d_math
    both = np.isfinite(a) & np.isfinite(b) & (a > 0)
    if not both.any():
        return {"error": "no comparable pairs"}
    aa, bb = a[both], b[both]
    broke = np.isfinite(a) & ~np.isfinite(b) & (a > 0)
    return {
        "n_sources": int(ok.sum()),
        "n_pairs_compared": int(both.sum()),
        "mean_distance_all_edges": float(aa.mean()),
        "mean_distance_mathematics_only": float(bb.mean()),
        "mean_lengthening": float((bb - aa).mean()),
        "median_lengthening": float(np.median(bb - aa)),
        "pairs_unchanged": float((bb == aa).mean()),
        "pairs_lengthened_2plus": float((bb - aa >= 2).mean()),
        "pairs_disconnected_by_removing_junk": float(
            broke.sum() / max(np.isfinite(a).sum(), 1)),
    }


def shortcut_recall(c, g, touched, nid, grades, keymap, top_frac=0.01):
    """Do the lemmas that SHOULD be shortcuts actually appear as hubs?

    "Should be a shortcut" is taken from the graded labels: a declaration
    raters called CORE or MAJOR is real mathematics, and if many proofs rest on
    it, the map ought to route through it. We check whether such declarations
    land in the graph's high-degree tail at all.
    """
    deg = np.asarray(g.sum(axis=1)).ravel()
    thr = np.quantile(deg[deg > 0], 1 - top_frac)
    good, bad = [], []
    for inc, gr in grades.items():
        d = int(c.inc_decl[inc])
        n = nid[d]
        if n < 0:
            continue
        (good if gr >= 3 else bad).append(deg[n])
    good, bad = np.array(good), np.array(bad)
    if not len(good):
        return {}
    return {
        "hub_threshold_degree": float(thr),
        "graded_real_maths_reaching_hub_tail": float((good >= thr).mean()),
        "graded_junk_reaching_hub_tail": float((bad >= thr).mean()),
        "median_degree_real_maths": float(np.median(good)),
        "median_degree_junk": float(np.median(bad)),
        "n_real": int(len(good)), "n_junk": int(len(bad)),
    }


def evaluate(c, base, ranks, k, junk_node, grades=None, keymap=None,
             n_sources=60):
    g, nid, touched, sel = build(c, base, ranks, k)
    junk_col = junk_node[touched]
    out = {
        "k": k, "nodes": int(g.shape[0]),
        "edges": int(g.nnz // 2),
        "hubs": hub_composition(c, g, touched, junk_node),
        "distance": distance_distortion(g, junk_col, n_sources=n_sources),
    }
    if grades is not None:
        out["recall"] = shortcut_recall(c, g, touched, nid, grades, keymap)
    return out
