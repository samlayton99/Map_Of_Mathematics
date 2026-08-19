#!/usr/bin/env python3
"""Phase 3 data & graph audit (core/03 §4): coverage, boundary effects,
components, acyclicity, centrality sensitivity to shallow nodes."""
import os, json
import networkx as nx
import numpy as np
import pandas as pd
from build_graph import P3_CLASSES
from features import load_edges, build_graphs

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))


def main():
    nodes = pd.read_csv(os.path.join(DATA, "node_inventory.csv"))
    edges = load_edges()
    G = build_graphs(edges)
    stored = set(nodes[nodes.stored == 1].name)
    out = {}
    out["nodes_total"] = len(nodes)
    out["nodes_stored"] = int(nodes.stored.sum())
    out["nodes_shallow"] = int((1 - nodes.stored).sum())
    out["nodes_p3_evaluated"] = int(nodes.p3_evaluated.sum())
    out["nodes_stored_unevaluated"] = int(((nodes.stored == 1) & (nodes.p3_evaluated == 0)).sum())
    out["edges_unique_pairs"] = int(edges.groupby(["src", "dst"]).ngroups)
    out["edges_typed_rows"] = len(edges)
    out["occurrences_total"] = int(edges.mult.sum())
    out["multi_file_nodes"] = int(nodes.files.str.contains(r"\|").sum())

    # P3 prevalence by coverage stratum
    ev = nodes[nodes.p3_evaluated == 1]
    out["p3_any_prevalence"] = {
        "evaluated_all": round(ev.p3_any.mean(), 4),
        "evaluated_stored": round(ev[ev.name.isin(stored)].p3_any.mean(), 4),
        "evaluated_shallow": round(ev[~ev.name.isin(stored)].p3_any.mean(), 4)}
    out["p3_class_prevalence_evaluated"] = {
        c: int(ev[f"p3_{c}"].sum()) for c in P3_CLASSES}

    # degree by stratum
    deg = pd.Series({n: G.in_degree(n) + G.out_degree(n) for n in G.nodes()})
    sflag = pd.Series({n: (n in stored) for n in G.nodes()})
    out["degree_by_stratum"] = {
        "stored_median": float(deg[sflag].median()), "stored_mean": round(float(deg[sflag].mean()), 2),
        "shallow_median": float(deg[~sflag].median()), "shallow_mean": round(float(deg[~sflag].mean()), 2),
        "shallow_out_deg_zero_frac": round(float(np.mean([G.out_degree(n) == 0 for n in G.nodes() if n not in stored])), 4),
        "stored_out_deg_zero_frac": round(float(np.mean([G.out_degree(n) == 0 for n in G.nodes() if n in stored])), 4)}

    # components / acyclicity
    U = G.to_undirected()
    comps = sorted((len(c) for c in nx.connected_components(U)), reverse=True)
    out["weakly_connected_components"] = len(comps)
    out["largest_component_frac"] = round(comps[0] / len(nodes), 4)
    sccs = [c for c in nx.strongly_connected_components(G) if len(c) > 1]
    out["nontrivial_sccs"] = len(sccs)
    out["scc_examples"] = [sorted(c)[:4] for c in sorted(sccs, key=len, reverse=True)[:3]]
    out["is_dag"] = nx.is_directed_acyclic_graph(G)

    # centrality sensitivity: pagerank with vs without shallow nodes
    pr_full = nx.pagerank(G, weight="weight")
    Gs = G.subgraph(stored).copy()
    pr_stored = nx.pagerank(Gs, weight="weight") if len(Gs) else {}
    common = [n for n in Gs.nodes()]
    if common:
        a = pd.Series({n: pr_full[n] for n in common}).rank()
        b = pd.Series({n: pr_stored[n] for n in common}).rank()
        out["pagerank_rank_correlation_stored_subgraph"] = round(float(a.corr(b, method="spearman")), 4)

    with open(os.path.join(DATA, "audit.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True, default=str)
    print(json.dumps(out, indent=1, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
