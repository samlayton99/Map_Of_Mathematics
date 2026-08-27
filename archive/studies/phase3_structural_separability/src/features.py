#!/usr/bin/env python3
"""Phase 3 feature builder.

Two tracks:
- STRICT: F0 basic topology + F1 global role + F2 community/bridge, computed on
  the collapsed directed graph. No names, no kinds, no P3, no file/domain, no
  coverage flags. Node identity is used only as an opaque join key.
- TYPED: strict features + F3 typed occurrence structure (type-vs-body layers,
  multiplicity, depth). Still no names/kinds/P3/files.

Deterministic: fixed seeds, sorted node order. The feature builder reads ONLY
edge_inventory.csv (+ node list); it cannot see labels by construction.
"""
import os, math, csv
from collections import defaultdict
import networkx as nx
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
SEED = 20260819
BETW_SAMPLES = 400

FORBIDDEN_COLUMNS = {"name", "kind", "stored", "files", "p3_evaluated", "p3_any"}


def load_edges(edge_file=None):
    df = pd.read_csv(edge_file or os.path.join(DATA, "edge_inventory.csv"))
    return df


def build_graphs(edges: pd.DataFrame):
    """Collapsed directed graph (strict) with unique/weighted multiplicities."""
    G = nx.DiGraph()
    agg = edges.groupby(["src", "dst"]).agg(mult=("mult", "sum")).reset_index()
    for r in agg.itertuples():
        G.add_edge(r.src, r.dst, weight=float(r.mult))
    return G


def f0_f1_f2(G: nx.DiGraph) -> pd.DataFrame:
    nodes = sorted(G.nodes())
    idx = {n: i for i, n in enumerate(nodes)}
    out = pd.DataFrame(index=nodes)
    out["in_deg"] = [G.in_degree(n) for n in nodes]
    out["out_deg"] = [G.out_degree(n) for n in nodes]
    out["in_wdeg"] = [G.in_degree(n, weight="weight") for n in nodes]
    out["out_wdeg"] = [G.out_degree(n, weight="weight") for n in nodes]
    out["deg"] = out.in_deg + out.out_deg
    out["deg_ratio"] = (out.in_deg + 1) / (out.out_deg + 1)
    out["is_sink"] = (out.out_deg == 0).astype(int)
    out["is_source"] = (out.in_deg == 0).astype(int)
    # neighbor degree summaries (undirected)
    U = G.to_undirected()
    nbr_mean, nbr_max = [], []
    for n in nodes:
        ds = [U.degree(m) for m in U.neighbors(n)]
        nbr_mean.append(float(np.mean(ds)) if ds else 0.0)
        nbr_max.append(float(np.max(ds)) if ds else 0.0)
    out["nbr_deg_mean"] = nbr_mean
    out["nbr_deg_max"] = nbr_max
    # DAG layer where well-defined (condensation topological layer)
    C = nx.condensation(G)
    layer = {}
    for c in nx.topological_sort(C):
        preds = list(C.predecessors(c))
        layer[c] = 0 if not preds else 1 + max(layer[p] for p in preds)
    maxlayer = max(layer.values()) or 1
    out["dag_layer_norm"] = [layer[C.graph["mapping"][n]] / maxlayer for n in nodes]
    # F1 global role
    pr = nx.pagerank(G, weight="weight", seed=None) if False else nx.pagerank(G, weight="weight")
    prr = nx.pagerank(G.reverse(copy=True), weight="weight")
    out["pagerank_dep"] = [pr[n] for n in nodes]
    out["pagerank_use"] = [prr[n] for n in nodes]
    try:
        hubs, auth = nx.hits(G, max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        hubs = {n: 0.0 for n in nodes}; auth = dict(hubs)
    out["hits_hub"] = [hubs[n] for n in nodes]
    out["hits_auth"] = [auth[n] for n in nodes]
    core = nx.core_number(nx.Graph(U))
    out["coreness"] = [core[n] for n in nodes]
    btw = nx.betweenness_centrality(G, k=min(BETW_SAMPLES, len(nodes)), seed=SEED)
    out["betweenness_approx"] = [btw[n] for n in nodes]
    harm = nx.harmonic_centrality(G, nbunch=None, distance=None)
    out["harmonic_in"] = [harm[n] for n in nodes]
    arts = set(nx.articulation_points(nx.Graph(U)))
    out["is_articulation"] = [int(n in arts) for n in nodes]
    # sampled reachability (deterministic full BFS on condensation is cheap here)
    reach_down = {}
    for c in reversed(list(nx.topological_sort(C))):
        s = set(C.nodes[c]["members"])
        for succ in C.successors(c):
            s |= reach_down[succ]
        reach_down[c] = s
    out["reach_dependencies"] = [len(reach_down[C.graph["mapping"][n]]) - 1 for n in nodes]
    reach_up = {}
    for c in nx.topological_sort(C):
        s = set(C.nodes[c]["members"])
        for pred in C.predecessors(c):
            s |= reach_up[pred]
        reach_up[c] = s
    out["reach_dependents"] = [len(reach_up[C.graph["mapping"][n]]) - 1 for n in nodes]
    # F2 community structure (deterministic greedy modularity on undirected)
    comms = list(nx.community.greedy_modularity_communities(U, weight=None))
    cmap = {}
    for ci, cset in enumerate(comms):
        for n in cset:
            cmap[n] = ci
    out["community_size"] = [len(comms[cmap[n]]) for n in nodes]
    within, part, ncomm, nent, crossfrac = [], [], [], [], []
    # within-community degree z-score per community
    wdeg = {n: sum(1 for m in U.neighbors(n) if cmap[m] == cmap[n]) for n in nodes}
    stats = defaultdict(list)
    for n in nodes:
        stats[cmap[n]].append(wdeg[n])
    mu = {c: float(np.mean(v)) for c, v in stats.items()}
    sd = {c: float(np.std(v)) or 1.0 for c, v in stats.items()}
    for n in nodes:
        within.append((wdeg[n] - mu[cmap[n]]) / sd[cmap[n]])
        nbrs = list(U.neighbors(n))
        k = len(nbrs) or 1
        counts = defaultdict(int)
        for m in nbrs:
            counts[cmap[m]] += 1
        part.append(1.0 - sum((c / k) ** 2 for c in counts.values()))
        ncomm.append(len(counts))
        probs = [c / k for c in counts.values()]
        nent.append(-sum(p * math.log(p) for p in probs if p > 0))
        crossfrac.append(sum(1 for m in nbrs if cmap[m] != cmap[n]) / k)
    out["within_comm_z"] = within
    out["participation"] = part
    out["n_neighbor_comms"] = ncomm
    out["neighbor_comm_entropy"] = nent
    out["cross_comm_frac"] = crossfrac
    return out


def f3_typed(edges: pd.DataFrame, nodes: list) -> pd.DataFrame:
    out = pd.DataFrame(index=nodes)
    for layer in ("type", "body"):
        el = edges[edges.layer == layer]
        ind = el.groupby("dst").agg(u=("src", "nunique"), w=("mult", "sum"),
                                    dmin=("minDepth", "min"), dmean=("minDepth", "mean"))
        outd = el.groupby("src").agg(u=("dst", "nunique"), w=("mult", "sum"))
        out[f"{layer}_in_deg"] = ind.u.reindex(nodes).fillna(0)
        out[f"{layer}_in_wdeg"] = ind.w.reindex(nodes).fillna(0)
        out[f"{layer}_out_deg"] = outd.u.reindex(nodes).fillna(0)
        out[f"{layer}_out_wdeg"] = outd.w.reindex(nodes).fillna(0)
        out[f"{layer}_in_depth_min"] = ind.dmin.reindex(nodes).fillna(-1)
        out[f"{layer}_in_depth_mean"] = ind.dmean.reindex(nodes).fillna(-1)
    out["stmt_body_in_ratio"] = (out.type_in_wdeg + 1) / (out.body_in_wdeg + 1)
    tot = out.type_in_wdeg + out.body_in_wdeg
    p = (out.type_in_wdeg / tot.replace(0, np.nan)).fillna(0.5).clip(1e-9, 1 - 1e-9)
    out["relation_entropy_in"] = -(p * np.log(p) + (1 - p) * np.log(1 - p))
    out["mult_per_unique_in"] = (out.type_in_wdeg + out.body_in_wdeg) / \
        (out.type_in_deg + out.body_in_deg).replace(0, 1)
    return out


def main(edge_file=None, out_prefix=""):
    edges = load_edges(edge_file)
    G = build_graphs(edges)
    strict = f0_f1_f2(G)
    assert FORBIDDEN_COLUMNS.isdisjoint(strict.columns)
    typed = strict.join(f3_typed(edges, sorted(G.nodes())))
    assert FORBIDDEN_COLUMNS.isdisjoint(typed.columns)
    strict.sort_index().to_csv(os.path.join(DATA, out_prefix + "feature_matrix_strict.csv"))
    typed.sort_index().to_csv(os.path.join(DATA, out_prefix + "feature_matrix_typed.csv"))
    print(f"features: strict {strict.shape}, typed {typed.shape}")


if __name__ == "__main__":
    main()
