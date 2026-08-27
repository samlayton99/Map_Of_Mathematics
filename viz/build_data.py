#!/usr/bin/env python
"""Compile the Phase 3 corpus graph into viz/data.js for the WebGL map.

Run: ~/venv/general_ml/bin/python viz/build_data.py
Deterministic (fixed seed). Reads archive/studies/phase3_structural_separability/data/,
writes viz/data.js (~2 MB). No repo data is modified.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np
import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "archive" / "studies" / "phase3_structural_separability" / "data"
OUT = Path(__file__).resolve().parent / "data.js"
SEED = 20260825

DOMAINS = [
    "Algebra_Group_Basic",
    "Analysis_SpecialFunctions_Log_Basic",
    "Data_Nat_GCD_Basic",
    "Logic_Function_Basic",
    "Order_Lattice",
    "Topology_Basic",
]
KINDS = ["theorem", "def", "axiom", "inductive", "constructor", "recursor"]
P3 = [
    "typeclass-instance", "structure-projection", "recursor", "generated",
    "internal-detail", "eq-machinery", "logic-core", "coercion",
]


def read_nodes():
    nodes = []
    with open(DATA / "node_inventory.csv") as f:
        for row in csv.DictReader(f):
            files = row["files"].split("|")
            nodes.append({
                "name": row["name"],
                "stored": int(row["stored"]),
                "kind": KINDS.index(row["kind"]),
                "evaluated": int(row["p3_evaluated"]),
                "p3any": int(row["p3_any"]),
                "files": sum(1 << DOMAINS.index(x) for x in files),
                "p3": sum(int(row[f"p3_{c}"]) << i for i, c in enumerate(P3)),
            })
    return nodes


def read_edges(idx):
    edges = []
    with open(DATA / "edge_inventory.csv") as f:
        for row in csv.DictReader(f):
            edges.append((idx[row["src"]], idx[row["dst"]],
                          0 if row["layer"] == "type" else 1,
                          int(row["mult"]), int(row["minDepth"])))
    return edges


def read_features(names):
    feats = {}
    with open(DATA / "feature_matrix_typed.csv") as f:
        rdr = csv.DictReader(f)
        first = rdr.fieldnames[0]  # unnamed index column
        for row in rdr:
            feats[row[first]] = row
    cols = ["pagerank_dep", "pagerank_use", "betweenness_approx", "coreness",
            "reach_dependencies", "reach_dependents"]
    out = {c: [] for c in cols}
    for n in names:
        r = feats.get(n, {})
        for c in cols:
            out[c].append(float(r.get(c, 0) or 0))
    return out


def dag_depth(n, edges):
    """depth(u) = 1 + max depth of its dependencies (u -> v means u refers to v)."""
    deps = [[] for _ in range(n)]
    outdeg = [0] * n
    rev = [[] for _ in range(n)]
    for s, d, *_ in edges:
        deps[s].append(d)
    # unique
    deps = [sorted(set(ds)) for ds in deps]
    for s in range(n):
        outdeg[s] = len(deps[s])
        for d in deps[s]:
            rev[d].append(s)
    depth = [0] * n
    from collections import deque
    q = deque(i for i in range(n) if outdeg[i] == 0)
    remaining = outdeg[:]
    while q:
        v = q.popleft()
        for u in rev[v]:
            depth[u] = max(depth[u], depth[v] + 1)
            remaining[u] -= 1
            if remaining[u] == 0:
                q.append(u)
    return depth


def communities(n, names, edges):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    w = {}
    for s, d, _l, mult, _md in edges:
        if s != d:
            k = (min(s, d), max(s, d))
            w[k] = w.get(k, 0) + mult
    for (a, b), mult in w.items():
        G.add_edge(a, b, weight=math.log1p(mult))
    comms = nx.community.greedy_modularity_communities(G, weight="weight")
    comm = [0] * n
    for i, c in enumerate(sorted(comms, key=len, reverse=True)):
        for v in c:
            comm[v] = i
    return comm


def layout(n, nodes, edges, deg):
    rng = np.random.default_rng(SEED)
    pos = np.zeros((n, 2), dtype=np.float64)
    for i, nd in enumerate(nodes):
        doms = [k for k in range(6) if nd["files"] >> k & 1]
        ang = sum(2 * math.pi * d / 6 for d in doms) / len(doms)
        r = 420 if len(doms) == 1 else 160
        pos[i] = [r * math.cos(ang), r * math.sin(ang)]
    pos += rng.normal(0, 60, (n, 2))

    # unique weighted pairs for attraction
    w = {}
    for s, d, _l, mult, _md in edges:
        if s != d:
            w[(s, d)] = w.get((s, d), 0) + mult
    src = np.array([k[0] for k in w], dtype=np.int64)
    dst = np.array([k[1] for k in w], dtype=np.int64)
    ew = np.log1p(np.array(list(w.values()), dtype=np.float64))

    mass = (deg + 1.0)
    kr, kg = 60.0, 0.03
    chunk = 512
    for it in range(400):
        disp = np.zeros((n, 2))
        # repulsion (chunked O(n^2))
        for a in range(0, n, chunk):
            b = min(a + chunk, n)
            diff = pos[a:b, None, :] - pos[None, :, :]          # (c, n, 2)
            d2 = (diff * diff).sum(-1) + 1e-3
            f = kr * mass[a:b, None] * mass[None, :] / d2       # (c, n)
            disp[a:b] += (diff * (f / np.sqrt(d2))[..., None]).sum(1)
        # attraction: linear in distance (FA2), weighted
        dvec = pos[dst] - pos[src]
        dist = np.sqrt((dvec * dvec).sum(-1)) + 1e-6
        fa = (ew * dist)[:, None] * (dvec / dist[:, None])
        np.add.at(disp, src, fa)
        np.add.at(disp, dst, -fa)
        # gravity
        disp -= kg * mass[:, None] * pos
        # annealed step with displacement cap
        step = 8.0 * (1.0 - it / 400) ** 1.5 + 0.2
        norm = np.sqrt((disp * disp).sum(-1)) + 1e-9
        cap = np.minimum(norm, step * 30.0)
        pos += disp / norm[:, None] * cap[:, None] * 0.01 * step
        if it % 50 == 0:
            print(f"  layout iter {it}, mean |disp| {norm.mean():.1f}")
    pos -= pos.mean(0)
    scale = 900.0 / np.abs(pos).max()
    return pos * scale


def main():
    nodes = read_nodes()
    n = len(nodes)
    idx = {nd["name"]: i for i, nd in enumerate(nodes)}
    edges = read_edges(idx)
    print(f"{n} nodes, {len(edges)} edge rows")

    indeg = np.zeros(n); outdeg = np.zeros(n)
    for s, d, *_ in edges:
        outdeg[s] += 1; indeg[d] += 1
    deg = indeg + outdeg

    depth = dag_depth(n, edges)
    print("depth max", max(depth))
    comm = communities(n, [nd["name"] for nd in nodes], edges)
    print("communities", max(comm) + 1)
    feats = read_features([nd["name"] for nd in nodes])
    pos = layout(n, nodes, edges, deg)

    r3 = lambda xs: [round(float(x), 3) for x in xs]
    data = {
        "meta": {
            "domains": DOMAINS, "kinds": KINDS, "p3": P3, "seed": SEED,
            "nNodes": n, "nEdges": len(edges),
        },
        "nodes": {
            "name": [nd["name"] for nd in nodes],
            "kind": [nd["kind"] for nd in nodes],
            "files": [nd["files"] for nd in nodes],
            "stored": [nd["stored"] for nd in nodes],
            "evaluated": [nd["evaluated"] for nd in nodes],
            "p3any": [nd["p3any"] for nd in nodes],
            "p3": [nd["p3"] for nd in nodes],
            "depth": depth,
            "comm": comm,
            "x": r3(pos[:, 0]), "y": r3(pos[:, 1]),
            "inDeg": [int(x) for x in indeg],
            "outDeg": [int(x) for x in outdeg],
            "pagerank": [round(float(x), 8) for x in feats["pagerank_dep"]],
            "pagerankUse": [round(float(x), 8) for x in feats["pagerank_use"]],
            "betweenness": [round(float(x), 6) for x in feats["betweenness_approx"]],
            "coreness": [int(x) for x in feats["coreness"]],
            "reachDeps": [int(x) for x in feats["reach_dependencies"]],
            "reachUsers": [int(x) for x in feats["reach_dependents"]],
        },
        "edges": {
            "src": [e[0] for e in edges],
            "dst": [e[1] for e in edges],
            "layer": [e[2] for e in edges],
            "mult": [e[3] for e in edges],
            "minDepth": [e[4] for e in edges],
        },
    }
    OUT.write_text("window.MATHMAP=" + json.dumps(data, separators=(",", ":")) + ";\n")
    print(f"wrote {OUT} ({OUT.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
