#!/usr/bin/env python3
"""Build data for the browser review UI (review/ui/).

Per reviewed proof: candidates ranked by (new-to-statement, then global depth),
route-skeleton membership (shown only in the hidden section), and the Lean
source text of the declaration extracted from the Mathlib checkout.
"""
import json, os, re
import numpy as np

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/db11af5d-4211-45ea-97b3-8e87cef8aeb6/scratchpad"
DUMP = os.path.join(SCRATCH, "mathlib_deps.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
OUT = os.path.normpath(os.path.join(HERE, "..", "review", "ui"))
ML = "/Users/sam/my-repos/research/Map_Of_Mathematics/corpusenv/mathlib/Mathlib"

FILES = {
    "Logic_Function_Basic": "Logic/Function/Basic.lean",
    "Order_Lattice": "Order/Lattice.lean",
    "Topology_Basic": "Topology/Basic.lean",
    "Data_Nat_GCD_Basic": "Data/Nat/GCD/Basic.lean",
    "Analysis_SpecialFunctions_Log_Basic": "Analysis/SpecialFunctions/Log/Basic.lean",
    "Algebra_Group_Basic": "Algebra/Group/Basic.lean",
}

DECL_START = re.compile(
    r"^(@\[|/--|(protected |private |nonrec |noncomputable )*"
    r"(theorem|lemma|def|instance|abbrev|structure|class|inductive)\b"
    r"|end\b|section\b|namespace\b|variable|open |attribute |alias |#|deriving )")


def extract_source(path, decl):
    """Return the source block of `decl` (doc comment + attrs + body)."""
    parts = decl.split(".")
    suffixes = [".".join(parts[k:]) for k in range(len(parts))]  # longest first
    lines = open(path).read().splitlines()
    start = None
    for suf in suffixes:
        pat = re.compile(
            r"^(@\[[^\]]*\] )?(protected |private |nonrec |noncomputable )*(theorem|lemma|def|abbrev) "
            + re.escape(suf) + r"(?!['\w])")
        for i, l in enumerate(lines):
            if pat.match(l):
                start = i
                break
        if start is not None:
            break
    if start is None:
        return None
    # include preceding doc comment / attribute lines
    s = start
    while s > 0 and (lines[s - 1].startswith("@[") or lines[s - 1].rstrip().endswith("-/")):
        if lines[s - 1].rstrip().endswith("-/"):
            j = s - 1
            while j >= 0 and not lines[j].lstrip().startswith("/--"):
                j -= 1
            s = max(j, 0)
        else:
            s -= 1
    e = start + 1
    while e < len(lines):
        if lines[e].strip() and DECL_START.match(lines[e]):
            break
        e += 1
    while e > start and not lines[e - 1].strip():
        e -= 1
    return "\n".join(lines[s:e])


def load():
    idx, names, deps_v, deps_t = {}, [], [], []
    def nid(n):
        i = idx.get(n)
        if i is None:
            i = len(names); idx[n] = i; names.append(n)
            deps_v.append(()); deps_t.append(())
        return i
    with open(DUMP) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
    return idx, names, deps_v, deps_t


def main():
    idx, names, deps_v, deps_t = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    deps = [dv if dv else dt for dv, dt in zip(deps_v, deps_t)]
    # depth (Kahn + cyclic fixpoint), same as measures.py
    indeg = np.zeros(n, dtype=np.int32)
    users = [[] for _ in range(n)]
    clean = []
    for i, ds in enumerate(deps):
        ds2 = tuple(d for d in set(ds) if d != i)
        clean.append(ds2)
        indeg[i] = len(ds2)
        for d in ds2:
            users[d].append(i)
    deps = clean
    from collections import deque
    q = deque(np.where(indeg == 0)[0].tolist())
    order = []
    while q:
        i = q.popleft(); order.append(i)
        for u in users[i]:
            indeg[u] -= 1
            if indeg[u] == 0:
                q.append(u)
    depth = np.zeros(n, dtype=np.int32)
    for i in order:
        if deps[i]:
            depth[i] = 1 + max(depth[d] for d in deps[i])
    cyc = set(range(n)) - set(order)
    for _ in range(3):
        for i in cyc:
            ds = [depth[d] for d in deps[i] if d not in cyc]
            if ds:
                depth[i] = 1 + max(ds)
    print("depth done", flush=True)

    def stmt_cone(root):
        seen = set()
        stack = [d for d in set(deps_t[root]) if d != root]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(d for d in deps[x] if d not in seen)
        return seen

    rk = json.load(open(os.path.join(DATA, "rankings.json")))
    cones = json.load(open(os.path.join(DATA, "cones_results.json")))
    keep = {r["decl"] for r in cones["move_id_per_proof"]}
    out = {}
    for decl, p in rk["proofs"].items():
        if decl not in keep or decl not in idx:
            continue
        root = idx[decl]
        S = stmt_cone(root)
        cands = [c for c in p["features"] if c in idx]
        route = {c for c, f in p["features"].items()
                 if f["app_head_count"] > 0 and f["prop_result_frac"] > 0.5
                 and not f["p3_classified"]}
        ranked = sorted(cands, key=lambda c: (idx[c] in S, -int(depth[idx[c]])))
        src_file = os.path.join(ML, FILES[p["file"]])
        src = extract_source(src_file, decl)
        out[decl] = {
            "file": FILES[p["file"]],
            "stmt_depth": int(1 + max((depth[d] for d in set(deps_t[root]) if d != root), default=-1)),
            "depth": int(depth[root]),
            "n_cands": len(cands),
            "moves": [{"name": c, "depth": int(depth[idx[c]]),
                       "new": idx[c] not in S} for c in ranked[:8]],
            "all_cands": [{"name": c, "depth": int(depth[idx[c]]),
                           "new": idx[c] not in S} for c in ranked],
            "route": sorted(route),
            "source": src,
        }
        print(decl, "src:", "OK" if src else "MISSING", flush=True)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "review_data.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    # union of names needing English glosses
    shown = sorted({m["name"] for d in out.values() for m in d["moves"]})
    print(f"\n{len(shown)} distinct move names shown:")
    for s in shown:
        print("  ", s)


if __name__ == "__main__":
    main()
