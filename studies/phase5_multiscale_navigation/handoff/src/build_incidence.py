#!/usr/bin/env python3
"""Phase 5, step 1: build the whole-Mathlib bipartite incidence structure.

Derived from the MathRecord dump (v7). Nothing here is a new source of truth;
every field is regenerable. Schema: reports/HYPERGRAPH_SCHEMA.md.

Outputs (column arrays, one row per incidence):
    nodes.npz      per declaration
    artifacts.npz  per proof artifact (one per declaration with a body)
    incid.npz      artifact, decl, roles[8], load_bearing, in_stmt_world,
                   d_target, d_cite, delta_depth

The statement-world flag is the expensive part: for each artifact we need to
know whether each cited declaration is reachable from the certified theorem's
STATEMENT closure. Computed exactly by reverse-reachability in batches of
64-bit lanes, the same technique the certification rounds used.
"""
import json, os, sys
import numpy as np

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP = os.path.join(SCRATCH, "mathlib_deps7.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "data"))
LOAD_ROLES = (0, 1, 2, 7)
BATCH = 4096          # artifacts per statement-world batch


def main():
    os.makedirs(OUT, exist_ok=True)
    idx, names = {}, []
    kinds, pr, ps, ar, gen = [], [], [], [], []
    deps_t, deps_v, vo = [], [], []

    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            kinds.append(""); pr.append(False); ps.append(False)
            ar.append(0); gen.append(False)
            deps_t.append(()); deps_v.append(()); vo.append(())
        return i

    with open(DUMP) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]
            pr[i] = bool(r.get("pr", False)); ps[i] = bool(r.get("ps", False))
            ar[i] = int(r.get("ar", 0)); gen[i] = bool(r.get("gen", False))
            deps_t[i] = tuple(nid(d) for d in r["t"])
            deps_v[i] = tuple(nid(d) for d in r["v"])
            vo[i] = tuple(tuple(int(x) for x in row) for row in r.get("vo", ()))
    n = len(names)
    print(f"declarations: {n}", flush=True)

    pr = np.array(pr); ps = np.array(ps); ar = np.array(ar, dtype=np.int32)
    gen = np.array(gen)
    KINDS = ["theorem", "def", "inductive", "constructor", "recursor",
             "opaque", "quot", "axiom", ""]
    kcode = np.array([KINDS.index(k) if k in KINDS else 8 for k in kinds],
                     dtype=np.int8)
    is_thm = kcode == 0

    # ---- depth over the citation graph (value side, falling back to type)
    deps = [dv if dv else dt for dv, dt in zip(deps_v, deps_t)]
    deps = [tuple(d for d in set(ds) if d != i) for i, ds in enumerate(deps)]
    indeg = np.zeros(n, dtype=np.int32)
    users = [[] for _ in range(n)]
    for i, ds in enumerate(deps):
        indeg[i] = len(ds)
        for d in ds:
            users[d].append(i)
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
    del users
    print(f"depth done (max {int(depth.max())}, {len(cyc)} in cycles)", flush=True)

    # ---- in-degree and stated-count (library-relative node coordinates)
    in_degree = np.zeros(n, dtype=np.int32)
    for i, ds in enumerate(deps_v):
        for d in set(ds):
            if d != i:
                in_degree[d] += 1
    stated = np.zeros(n, dtype=np.int32)
    for i in np.where(is_thm & ~gen)[0]:
        for c in set(deps_t[i]):
            stated[c] += 1

    # ---- artifacts: one per declaration with a body
    art_decl = np.array([i for i in range(n) if deps_v[i]], dtype=np.int64)
    art_of = -np.ones(n, dtype=np.int64)
    art_of[art_decl] = np.arange(len(art_decl))
    print(f"artifacts: {len(art_decl)}", flush=True)

    # ---- incidences
    a_col, d_col, roles_col = [], [], []
    for a, i in enumerate(art_decl):
        seen = {}
        for d, row in zip(deps_v[i], vo[i]):
            if d == i:
                continue
            prev = seen.get(d)
            if prev is None:
                seen[d] = list(row) if row else [0] * 8
            else:
                for k in range(8):
                    prev[k] += row[k] if row else 0
        for d, row in seen.items():
            a_col.append(a); d_col.append(d); roles_col.append(row)
    a_col = np.array(a_col, dtype=np.int64)
    d_col = np.array(d_col, dtype=np.int64)
    roles = np.array(roles_col, dtype=np.int32)
    del roles_col
    load_bearing = (roles[:, list(LOAD_ROLES)].sum(axis=1) > 0)
    print(f"incidences: {len(a_col)} ({int(load_bearing.sum())} load-bearing)",
          flush=True)

    tgt = art_decl[a_col]
    d_target = depth[tgt]
    d_cite = depth[d_col]
    delta = d_target.astype(np.int32) - d_cite.astype(np.int32)

    # ---- statement-world membership, exactly, in lanes
    # For artifact a certifying T: is cited d reachable from T's statement refs?
    in_stmt = np.zeros(len(a_col), dtype=bool)
    dep_arrays = [np.array(ds, dtype=np.int64) if ds else None for ds in deps]
    rev = list(reversed(order))
    # incidence ranges per artifact (a_col is non-decreasing by construction)
    starts = np.searchsorted(a_col, np.arange(len(art_decl)), side="left")
    ends = np.searchsorted(a_col, np.arange(len(art_decl)), side="right")

    nb = (len(art_decl) + BATCH - 1) // BATCH
    for b in range(nb):
        lo, hi = b * BATCH, min((b + 1) * BATCH, len(art_decl))
        batch = np.arange(lo, hi)
        nw = (len(batch) + 63) // 64
        reach = np.zeros((n, nw), dtype=np.uint64)
        for j, a in enumerate(batch):
            T = art_decl[a]
            seeds = np.array(sorted(set(deps_t[T]) - {T}), dtype=np.int64)
            if len(seeds):
                bit = np.zeros(nw, dtype=np.uint64)
                bit[j >> 6] = np.uint64(1) << np.uint64(j & 63)
                reach[seeds] |= bit
        for i in rev:
            row = reach[i]
            if row.any():
                ds = dep_arrays[i]
                if ds is not None:
                    reach[ds] |= row
        for i in list(cyc) * 2:
            row = reach[i]
            if row.any() and dep_arrays[i] is not None:
                reach[dep_arrays[i]] |= row
        for j, a in enumerate(batch):
            s, e = starts[a], ends[a]
            if s == e:
                continue
            w, bit = j >> 6, np.uint64(1) << np.uint64(j & 63)
            in_stmt[s:e] = (reach[d_col[s:e], w] & bit) != 0
        del reach
        if (b + 1) % 10 == 0 or b + 1 == nb:
            print(f"  statement-world batch {b+1}/{nb}", flush=True)

    print(f"in statement world: {int(in_stmt.sum())} / {len(in_stmt)}", flush=True)

    np.savez_compressed(os.path.join(OUT, "nodes.npz"),
                        kind=kcode, pr=pr, ps=ps, ar=ar, gen=gen,
                        depth=depth, in_degree=in_degree, stated=stated)
    np.savez_compressed(os.path.join(OUT, "artifacts.npz"),
                        certifies=art_decl,
                        is_generated=gen[art_decl],
                        n_incidences=(ends - starts).astype(np.int32))
    np.savez_compressed(os.path.join(OUT, "incid.npz"),
                        artifact=a_col.astype(np.int32),
                        decl=d_col.astype(np.int32),
                        roles=roles.astype(np.int16),
                        load_bearing=load_bearing,
                        in_stmt_world=in_stmt,
                        d_target=d_target.astype(np.int16),
                        d_cite=d_cite.astype(np.int16),
                        delta_depth=delta.astype(np.int16))
    with open(os.path.join(OUT, "names.json"), "w") as f:
        json.dump(names, f)
    print("written to", OUT, flush=True)


if __name__ == "__main__":
    main()
