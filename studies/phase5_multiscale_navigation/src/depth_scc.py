#!/usr/bin/env python3
"""Exact depth over the Mathlib dependency graph via SCC condensation.

Replaces the 3-pass cycle relaxation in build_incidence.py. Method:
contract strongly connected components (scipy csgraph, iterative Tarjan
in C), then longest-path depth on the condensation DAG by vectorized
Kahn; every node gets its SCC's depth. Nodes with no deps have depth 0.

Outputs data/depth_scc.npz:
    depth_exact  int32  per node, over value deps (fallback to type deps)
    scc_id       int32  SCC label on that graph
    scc_size     int32  size of the node's SCC
    depth_stmt   int32  same algorithm over TYPE deps only
    scc_id_stmt, scc_size_stmt  ditto for the type graph

Also caches the parsed dep graphs (CSR, deduped, self-loops removed) to
SCRATCH/deps_csr.npz for reuse by audit scripts.

Node ids are taken from data/names.json so everything lines up with
nodes.npz / incid.npz.
"""
import json
import os
import sys

import numpy as np

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
DUMP_CANDIDATES = [
    os.path.expanduser("~/mathmap_data/mathlib_deps7.jsonl"),
    os.path.join(SCRATCH, "mathlib_deps7.jsonl"),
]


def deps_to_csr(deps, n):
    """List of per-node dep tuples -> CSR (indptr int64, indices int32)."""
    counts = np.fromiter((len(d) for d in deps), dtype=np.int64, count=n)
    indptr = np.zeros(n + 1, dtype=np.int64)
    np.cumsum(counts, out=indptr[1:])
    indices = np.empty(indptr[-1], dtype=np.int32)
    for i, ds in enumerate(deps):
        if ds:
            indices[indptr[i]:indptr[i + 1]] = ds
    return indptr, indices


def scc_depth(indptr, indices, n):
    """Exact longest-path depth via SCC condensation.

    (indptr, indices): CSR where row i lists the deps of node i
    (self-loops need not be removed; intra-SCC edges are dropped).
    Returns (depth int32, scc_id int32, scc_size-per-node int32).
    depth[i] = 0 if i has no deps outside its SCC, else
    1 + max(depth[d]) over deps d in other SCCs -- computed on the
    condensation DAG, so it is exact for nodes in cycles too.
    """
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components

    g = csr_matrix((np.ones(len(indices), dtype=np.int8), indices, indptr),
                   shape=(n, n))
    ncomp, labels = connected_components(g, directed=True, connection="strong")
    labels = labels.astype(np.int32)
    sizes = np.bincount(labels, minlength=ncomp).astype(np.int32)

    # condensation edges: cu depends on cd
    src = np.repeat(np.arange(n, dtype=np.int32),
                    np.diff(indptr).astype(np.int64))
    cu, cd = labels[src], labels[indices]
    keep = cu != cd
    cu, cd = cu[keep], cd[keep]
    if len(cu):
        e = np.unique(cu.astype(np.int64) * ncomp + cd.astype(np.int64))
        cu = (e // ncomp).astype(np.int32)
        cd = (e % ncomp).astype(np.int32)

    # CSR from dep-SCC -> user-SCCs
    order = np.argsort(cd, kind="stable")
    users = cu[order]
    uptr = np.zeros(ncomp + 1, dtype=np.int64)
    np.cumsum(np.bincount(cd, minlength=ncomp), out=uptr[1:])
    indeg = np.bincount(cu, minlength=ncomp).astype(np.int64)

    depth_c = np.zeros(ncomp, dtype=np.int32)
    frontier = np.where(indeg == 0)[0]
    done = len(frontier)
    while len(frontier):
        starts, ends = uptr[frontier], uptr[frontier + 1]
        lens = ends - starts
        nz = lens > 0
        if not nz.any():
            break
        f, starts, lens = frontier[nz], starts[nz], lens[nz]
        # gather all users of the frontier
        offs = np.repeat(starts - np.concatenate(([0], np.cumsum(lens)[:-1])),
                         lens)
        dst = users[np.arange(lens.sum(), dtype=np.int64) + offs]
        dsrc = np.repeat(f, lens).astype(np.int32)
        np.maximum.at(depth_c, dst, depth_c[dsrc] + 1)
        np.subtract.at(indeg, dst, 1)
        frontier = np.unique(dst[indeg[dst] == 0])
        done += len(frontier)
    assert (indeg == 0).all(), "condensation was not a DAG?"
    return depth_c[labels], labels, sizes[labels]


def _parse_dump(names_path, dump_path, log=print):
    with open(names_path) as f:
        names = json.load(f)
    idx = {nm: i for i, nm in enumerate(names)}
    n = len(names)
    log(f"names: {n}")
    t_deps = [()] * n
    v_deps = [()] * n
    with open(dump_path) as f:
        for k, line in enumerate(f):
            r = json.loads(line)
            i = idx[r["n"]]
            t_deps[i] = tuple(idx[d] for d in set(r["t"]) if idx[d] != i)
            v_deps[i] = tuple(idx[d] for d in set(r["v"]) if idx[d] != i)
            if (k + 1) % 100000 == 0:
                log(f"  parsed {k + 1} rows")
    log(f"parsed all rows; t edges {sum(map(len, t_deps))}, "
        f"v edges {sum(map(len, v_deps))}")
    return n, t_deps, v_deps


def main():
    def log(*a):
        print(*a, flush=True)

    dump = next((p for p in DUMP_CANDIDATES if os.path.exists(p)), None)
    if dump is None:
        sys.exit("no dump found")
    log("dump:", dump)
    n, t_deps, v_deps = _parse_dump(os.path.join(DATA, "names.json"), dump, log)

    t_indptr, t_indices = deps_to_csr(t_deps, n)
    v_indptr, v_indices = deps_to_csr(v_deps, n)
    np.savez(os.path.join(SCRATCH, "deps_csr.npz"),
             t_indptr=t_indptr, t_indices=t_indices,
             v_indptr=v_indptr, v_indices=v_indices)
    log("cached CSR graphs to scratchpad")

    # citation graph: value deps, falling back to type deps (as build_incidence)
    deps = [dv if dv else dt for dv, dt in zip(v_deps, t_deps)]
    del v_deps
    c_indptr, c_indices = deps_to_csr(deps, n)
    del deps
    log(f"citation graph: {len(c_indices)} edges")
    depth_exact, scc_id, scc_size = scc_depth(c_indptr, c_indices, n)
    log(f"depth_exact: max {depth_exact.max()}, "
        f"{int((scc_size > 1).sum())} nodes in nontrivial SCCs")

    s_indptr, s_indices = deps_to_csr(t_deps, n)
    del t_deps
    log(f"type graph: {len(s_indices)} edges")
    depth_stmt, scc_id_s, scc_size_s = scc_depth(s_indptr, s_indices, n)
    log(f"depth_stmt: max {depth_stmt.max()}, "
        f"{int((scc_size_s > 1).sum())} nodes in nontrivial SCCs")

    np.savez_compressed(os.path.join(DATA, "depth_scc.npz"),
                        depth_exact=depth_exact.astype(np.int32),
                        scc_id=scc_id.astype(np.int32),
                        scc_size=scc_size.astype(np.int32),
                        depth_stmt=depth_stmt.astype(np.int32),
                        scc_id_stmt=scc_id_s.astype(np.int32),
                        scc_size_stmt=scc_size_s.astype(np.int32))
    log("written", os.path.join(DATA, "depth_scc.npz"))


if __name__ == "__main__":
    main()
