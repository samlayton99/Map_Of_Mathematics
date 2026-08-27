#!/usr/bin/env python3
"""Phase 3: build the raw declaration graph G_decl_raw from P1 evidence.

Nodes: every declaration seen in the Phase 2 studies (stored + shallow).
Edges: u -> v when stored declaration u's type or body refers to v (P1
occurrences), with layer, multiplicity, and min path depth preserved.

P3 classifications ride along as LABELS ONLY (never features).
Deterministic: sorted outputs, no randomness.
"""
import json, glob, os, csv
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "..", "studies"))
DATA_DIR = os.path.normpath(os.path.join(HERE, "..", "data"))

P3_CLASSES = ["typeclass-instance", "recursor", "structure-projection", "generated",
              "internal-detail", "eq-machinery", "logic-core", "coercion"]


def path_depth(path: str) -> int:
    return path.count(".")


def build():
    nodes = {}   # name -> dict
    edges = {}   # (u, v, layer) -> {mult, minDepth}

    for p in sorted(glob.glob(os.path.join(STUDY_DIR, "*.study.json"))):
        fname = os.path.basename(p).replace(".study.json", "")
        with open(p) as f:
            s = json.load(f)

        # stored declarations (full bodies)
        kind_by_name = {}
        for d in s["record"]["declarations"]:
            n = d["name"]
            kind_by_name[n] = d["kind"]
            nd = nodes.setdefault(n, {
                "name": n, "stored": 0, "files": set(), "kind": "",
                "p3_evaluated": 0, **{f"p3_{c}": 0 for c in P3_CLASSES}})
            nd["stored"] = 1
            nd["kind"] = d["kind"]
            nd["files"].add(fname)

        # referenced declarations: shallow records carrying P3 labels
        for r in s["referencedDecls"]:
            if "error" in r:
                continue
            n = r["name"]
            nd = nodes.setdefault(n, {
                "name": n, "stored": 0, "files": set(), "kind": "",
                "p3_evaluated": 0, **{f"p3_{c}": 0 for c in P3_CLASSES}})
            nd["files"].add(fname)
            if not nd["kind"]:
                nd["kind"] = r.get("kind", "")
            nd["p3_evaluated"] = 1
            for c in r.get("classification", []):
                if c in P3_CLASSES:
                    nd[f"p3_{c}"] = 1

        # P1 edges from stored declarations
        for d in s["declStudies"]:
            u = d["name"]
            for layer_key, layer in (("p1_typeRefs", "type"), ("p1_bodyRefs", "body")):
                for occ in d[layer_key]:
                    v = occ["name"]
                    nodes.setdefault(v, {
                        "name": v, "stored": 0, "files": set(), "kind": "",
                        "p3_evaluated": 0, **{f"p3_{c}": 0 for c in P3_CLASSES}})
                    key = (u, v, layer)
                    e = edges.setdefault(key, {"mult": 0, "minDepth": 10**9})
                    e["mult"] += 1
                    e["minDepth"] = min(e["minDepth"], path_depth(occ["path"]))

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "node_inventory.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "stored", "kind", "p3_evaluated", "p3_any", "files"]
                   + [f"p3_{c}" for c in P3_CLASSES])
        for n in sorted(nodes):
            nd = nodes[n]
            p3_any = int(any(nd[f"p3_{c}"] for c in P3_CLASSES))
            w.writerow([n, nd["stored"], nd["kind"], nd["p3_evaluated"], p3_any,
                        "|".join(sorted(nd["files"]))]
                       + [nd[f"p3_{c}"] for c in P3_CLASSES])

    with open(os.path.join(DATA_DIR, "edge_inventory.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["src", "dst", "layer", "mult", "minDepth"])
        for (u, v, layer) in sorted(edges):
            e = edges[(u, v, layer)]
            w.writerow([u, v, layer, e["mult"], e["minDepth"]])

    print(f"nodes={len(nodes)} edges={len(edges)} -> {DATA_DIR}")
    return nodes, edges


if __name__ == "__main__":
    build()
