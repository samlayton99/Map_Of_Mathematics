#!/usr/bin/env python
"""Full-Mathlib atlas: statement/proof cones and proof moves at library scale.

Scales the exact study-path decomposition (tools/study_path.py) from the
six-file corpus (3,662 nodes) to the complete `import Mathlib` environment
(~771k constants) using:

  1. SCC condensation of the unfold graph (scipy; cycles are rare unsafe/
     partial-def artifacts, theorems live in singleton SCCs),
  2. one reverse-topological bitmask pass per batch of roots: for a batch of
     B roots, mask[v] holds one bit per root, set iff v lies in that root's
     cone.  Two planes per batch: statement (seeded from type-deps) and
     proof (seeded from body-deps).  Interior closure follows unfold =
     body-deps if nonempty else type-deps, exactly as study_path.cone_from.

Per theorem T this yields A_S(T), A_P(T), N(T)=A_P\\A_S (the proof moves)
with no extraction-boundary artifact — the closure is the real one.

Data source: bigdata/mathlib_deps.jsonl (tools/extract_full_mathlib.sh).
Definitions and semantics identical to study_path.py; test_atlas.py checks
bit-for-bit agreement on the six-file corpus.

CLI:
  atlas.py path <Const.name> [--drop-machinery] [--per-layer N]
  atlas.py index [--roots-kind theorem] [--batch 512] [--topk 12]
  atlas.py stats
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BIG = ROOT / "bigdata"
DUMP = BIG / "mathlib_deps.jsonl"
CACHE = BIG / "atlas_cache.npz"
NAMES_CACHE = BIG / "atlas_names.txt"


# --------------------------------------------------------------------- load

def _csr_from_lists(lists, dtype=np.int32):
    indptr = np.zeros(len(lists) + 1, dtype=np.int64)
    for i, l in enumerate(lists):
        indptr[i + 1] = indptr[i] + len(l)
    indices = np.empty(indptr[-1], dtype=dtype)
    for i, l in enumerate(lists):
        indices[indptr[i]:indptr[i + 1]] = l
    return indptr, indices


class Atlas:
    """Condensed exact dependency graph over the full constant population.

    u -> v means u refers to v.  All cone computations run on the SCC
    condensation of the unfold graph; on a DAG (the corpus) this is the
    identity and results match study_path.Corpus exactly.
    """

    def __init__(self, names, kind, cls, t_indptr, t_indices, v_indptr, v_indices):
        self.names = names
        self.idx = {n: i for i, n in enumerate(names)}
        self.kind = kind                     # list[str] per node
        self.cls = cls                       # tuple[str] machinery classes per node
        self.n = len(names)
        self.t_indptr, self.t_indices = t_indptr, t_indices
        self.v_indptr, self.v_indices = v_indptr, v_indices
        self._build_unfold()
        self._condense()
        self._depths()

    # unfold(v) = body-deps if the body is nonempty else type-deps
    def _build_unfold(self):
        has_body = (self.v_indptr[1:] - self.v_indptr[:-1]) > 0
        u_lists_ptr = np.where(has_body, 0, 1)  # 0 -> value CSR, 1 -> type CSR
        n = self.n
        counts = np.where(has_body,
                          self.v_indptr[1:] - self.v_indptr[:-1],
                          self.t_indptr[1:] - self.t_indptr[:-1])
        indptr = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(counts, out=indptr[1:])
        indices = np.empty(indptr[-1], dtype=np.int32)
        for i in range(n):
            if u_lists_ptr[i] == 0:
                s, e = self.v_indptr[i], self.v_indptr[i + 1]
                indices[indptr[i]:indptr[i + 1]] = self.v_indices[s:e]
            else:
                s, e = self.t_indptr[i], self.t_indptr[i + 1]
                indices[indptr[i]:indptr[i + 1]] = self.t_indices[s:e]
        self.u_indptr, self.u_indices = indptr, indices

    def _condense(self):
        import scipy.sparse as sp
        from scipy.sparse.csgraph import connected_components
        n = self.n
        # drop self-loops for the SCC/condensation step
        src = np.repeat(np.arange(n, dtype=np.int32),
                        np.diff(self.u_indptr).astype(np.int64))
        dst = self.u_indices
        keep = src != dst
        src, dst = src[keep], dst[keep]
        g = sp.csr_matrix((np.ones(len(src), dtype=np.int8), (src, dst)),
                          shape=(n, n))
        ncomp, label = connected_components(g, directed=True, connection="strong")
        self.ncomp, self.label = ncomp, label.astype(np.int32)
        # members of each SCC, CSR-style
        order = np.argsort(self.label, kind="stable")
        counts = np.bincount(self.label, minlength=ncomp)
        self.scc_indptr = np.zeros(ncomp + 1, dtype=np.int64)
        np.cumsum(counts, out=self.scc_indptr[1:])
        self.scc_members = order.astype(np.int32)
        self.scc_size = counts.astype(np.int64)
        # condensed edge list, deduplicated
        cs, cd = self.label[src], self.label[dst]
        keep = cs != cd
        key = cs[keep].astype(np.int64) * ncomp + cd[keep]
        key = np.unique(key)
        cs, cd = (key // ncomp).astype(np.int32), (key % ncomp).astype(np.int32)
        o = np.argsort(cs, kind="stable")
        cs, cd = cs[o], cd[o]
        self.c_indptr = np.zeros(ncomp + 1, dtype=np.int64)
        np.cumsum(np.bincount(cs, minlength=ncomp), out=self.c_indptr[1:])
        self.c_indices = cd

    def _depths(self):
        """Longest chain beneath each SCC on the condensed DAG; Kahn order."""
        ncomp = self.ncomp
        pend = np.diff(self.c_indptr).astype(np.int64).copy()
        rev_ptr, rev_idx = _reverse_csr(self.c_indptr, self.c_indices, ncomp)
        depth = np.zeros(ncomp, dtype=np.int32)
        from collections import deque
        q = deque(np.where(pend == 0)[0].tolist())
        order = []
        while q:
            v = q.popleft()
            order.append(v)
            for u in rev_idx[rev_ptr[v]:rev_ptr[v + 1]]:
                if depth[v] + 1 > depth[u]:
                    depth[u] = depth[v] + 1
                pend[u] -= 1
                if pend[u] == 0:
                    q.append(int(u))
        if len(order) != ncomp:
            raise RuntimeError("condensation is not a DAG")
        self.scc_depth = depth
        self.order = order                    # deps before users
        self.push_order = order[::-1]         # users before deps
        self.depth = depth[self.label]        # per node

    # ------------------------------------------------------------ per-node views
    def type_deps(self, i):
        return self.t_indices[self.t_indptr[i]:self.t_indptr[i + 1]]

    def body_deps(self, i):
        return self.v_indices[self.v_indptr[i]:self.v_indptr[i + 1]]

    def unfold(self, i):
        return self.u_indices[self.u_indptr[i]:self.u_indptr[i + 1]]

    # ------------------------------------------------------------ single target
    def cone_from(self, seeds):
        """Exact closure (set of node ids) downward from node-id seeds.
        Matches study_path.Corpus.cone_from: seeds are included."""
        seen = np.zeros(self.ncomp, dtype=bool)
        stack = [int(self.label[s]) for s in seeds]
        for s in stack:
            seen[s] = True
        while stack:
            u = stack.pop()
            for d in self.c_indices[self.c_indptr[u]:self.c_indptr[u + 1]]:
                if not seen[d]:
                    seen[d] = True
                    stack.append(int(d))
        out = set()
        for s in np.where(seen)[0]:
            for m in self.scc_members[self.scc_indptr[s]:self.scc_indptr[s + 1]]:
                out.add(int(m))
        return out


def _reverse_csr(indptr, indices, n):
    counts = np.bincount(indices, minlength=n)
    rptr = np.zeros(n + 1, dtype=np.int64)
    np.cumsum(counts, out=rptr[1:])
    ridx = np.empty(len(indices), dtype=np.int32)
    fill = rptr[:-1].copy()
    src = np.repeat(np.arange(n, dtype=np.int32),
                    np.diff(indptr).astype(np.int64))
    for s, d in zip(src, indices):
        ridx[fill[d]] = s
        fill[d] += 1
    return rptr, ridx


# ------------------------------------------------------------------ dump load

def load_dump(dump=DUMP, cache=CACHE, names_cache=NAMES_CACHE):
    """Parse mathlib_deps.jsonl into an Atlas, with an npz cache."""
    if Path(cache).exists() and Path(names_cache).exists():
        z = np.load(cache)
        names = Path(names_cache).read_text().splitlines()
        kind_vocab = list(z["kind_vocab"])
        cls_vocab = list(z["cls_vocab"])
        kind = [kind_vocab[k] for k in z["kind"]]
        cls = [tuple(c for j, c in enumerate(cls_vocab) if m >> j & 1)
               for m in z["cls"]]
        return Atlas(names, kind, cls, z["t_indptr"], z["t_indices"],
                     z["v_indptr"], z["v_indices"])

    from array import array
    idx, names = {}, []
    kind, clsmask = [], []
    kind_vocab, kv_idx = [], {}
    cls_vocab, cv_idx = [], {}
    # CSR built incrementally; rows arrive in dump order, which we make node
    # order by registering each row's name before its deps.
    t_flat, v_flat = array("i"), array("i")
    t_ptr, v_ptr = array("q", [0]), array("q", [0])
    row_of = {}                       # node id -> row number in CSR

    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names)
            idx[nm] = i
            names.append(nm)
            kind.append(0)
            clsmask.append(0)
        return i

    def kid(k):
        i = kv_idx.get(k)
        if i is None:
            i = len(kind_vocab); kv_idx[k] = i; kind_vocab.append(k)
        return i

    def cid(c):
        i = cv_idx.get(c)
        if i is None:
            i = len(cls_vocab); cv_idx[c] = i; cls_vocab.append(c)
        return i

    with open(dump) as f:
        for ln, line in enumerate(f):
            r = json.loads(line)
            i = nid(r["n"])
            row_of[i] = len(t_ptr) - 1
            kind[i] = kid(r["k"])
            m = 0
            for c in r["c"]:
                m |= 1 << cid(c)
            clsmask[i] = m
            for d in r["t"]:
                t_flat.append(nid(d))
            t_ptr.append(len(t_flat))
            for d in r["v"]:
                v_flat.append(nid(d))
            v_ptr.append(len(v_flat))
            if ln % 100000 == 0:
                print(f"  parsed {ln} rows", file=sys.stderr)

    n = len(names)
    # nodes referenced but never dumped (should not happen; be safe): empty rows
    for i in range(n):
        if i not in row_of:
            row_of[i] = len(t_ptr) - 1
            t_ptr.append(len(t_flat))
            v_ptr.append(len(v_flat))
    # permute CSR rows from dump order to node-id order
    rows = np.empty(n, dtype=np.int64)
    for i, rw in row_of.items():
        rows[i] = rw
    tp = np.frombuffer(t_ptr, dtype=np.int64)
    vp = np.frombuffer(v_ptr, dtype=np.int64)
    tf = np.frombuffer(t_flat, dtype=np.int32)
    vf = np.frombuffer(v_flat, dtype=np.int32)

    def permute(ptr, flat):
        counts = (ptr[1:] - ptr[:-1])[rows]
        indptr = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(counts, out=indptr[1:])
        indices = np.empty(len(flat), dtype=np.int32)
        for i in range(n):
            rw = rows[i]
            indices[indptr[i]:indptr[i + 1]] = flat[ptr[rw]:ptr[rw + 1]]
        return indptr, indices

    t_indptr, t_indices = permute(tp, tf)
    del t_flat
    v_indptr, v_indices = permute(vp, vf)
    del v_flat
    np.savez_compressed(
        cache,
        kind=np.array(kind, dtype=np.int8),
        cls=np.array(clsmask, dtype=np.int32),
        kind_vocab=np.array(kind_vocab), cls_vocab=np.array(cls_vocab),
        t_indptr=t_indptr, t_indices=t_indices,
        v_indptr=v_indptr, v_indices=v_indices)
    Path(names_cache).write_text("\n".join(names))
    kindS = [kind_vocab[k] for k in kind]
    clsS = [tuple(c for j, c in enumerate(cls_vocab) if m >> j & 1)
            for m in clsmask]
    return Atlas(names, kindS, clsS, t_indptr, t_indices, v_indptr, v_indices)


# ------------------------------------------------------------- batched cones

def _propagate(atlas, mask, active):
    """Push each SCC's root-membership bits into its condensed deps.
    push_order guarantees every pusher is final before it pushes."""
    c_indptr, c_indices = atlas.c_indptr, atlas.c_indices
    for u in atlas.push_order:
        if not active[u]:
            continue
        s, e = c_indptr[u], c_indptr[u + 1]
        if s == e:
            continue
        tgt = c_indices[s:e]
        mask[tgt] |= mask[u]
        active[tgt] = True


def batch_cones(atlas, roots, nwords=None):
    """Compute statement/proof cone membership for a batch of root node ids.

    Returns (maskS, maskP): (ncomp, W) uint64 matrices; bit j of column word
    w marks membership of that SCC in root j's cone (j = w*64 + bit).
    """
    B = len(roots)
    W = nwords or (B + 63) // 64
    maskS = np.zeros((atlas.ncomp, W), dtype=np.uint64)
    maskP = np.zeros((atlas.ncomp, W), dtype=np.uint64)
    activeS = np.zeros(atlas.ncomp, dtype=bool)
    activeP = np.zeros(atlas.ncomp, dtype=bool)
    for j, r in enumerate(roots):
        w, b = divmod(j, 64)
        bit = np.uint64(1 << b)
        ts = atlas.label[atlas.type_deps(r)]
        vs = atlas.label[atlas.body_deps(r)]
        if len(ts):
            maskS[ts, w] |= bit
            activeS[ts] = True
        if len(vs):
            maskP[vs, w] |= bit
            activeP[vs] = True
    _propagate(atlas, maskS, activeS)
    _propagate(atlas, maskP, activeP)
    return maskS, maskP


def _col(mask, j):
    """Boolean membership column for root j from the packed mask matrix."""
    w, b = divmod(j, 64)
    return (mask[:, w] & np.uint64(1 << b)) != 0


# ------------------------------------------------------------------ indexing

def run_index(atlas, roots, out_path, batch=512, topk=12, log=print):
    """Cone decomposition for every root; writes one JSONL row per root and
    returns per-constant global counters (times in statement cones, in proof
    cones, as a new move)."""
    ncomp = atlas.ncomp
    inS = np.zeros(ncomp, dtype=np.int64)
    inP = np.zeros(ncomp, dtype=np.int64)
    asNew = np.zeros(ncomp, dtype=np.int64)
    scc_size = atlas.scc_size
    scc_depth = atlas.scc_depth
    machinery_scc = np.zeros(ncomp, dtype=bool)
    for i in range(atlas.n):
        if atlas.cls[i]:
            machinery_scc[atlas.label[i]] = True

    with open(out_path, "w") as out:
        for a in range(0, len(roots), batch):
            chunk = roots[a:a + batch]
            maskS, maskP = batch_cones(atlas, chunk)
            newM = maskP & ~maskS
            inS += np.bitwise_count(maskS).sum(axis=1, dtype=np.int64)
            inP += np.bitwise_count(maskP).sum(axis=1, dtype=np.int64)
            asNew += np.bitwise_count(newM).sum(axis=1, dtype=np.int64)
            for j, r in enumerate(chunk):
                sC = _col(maskS, j)
                pC = _col(maskP, j)
                nC = _col(newM, j)
                s_size = int(scc_size[sC].sum())
                p_size = int(scc_size[pC].sum())
                n_sccs = np.where(nC)[0]
                n_size = int(scc_size[n_sccs].sum())
                mach_new = int(scc_size[n_sccs[machinery_scc[n_sccs]]].sum())
                # rank new facts: depth descending (deepest new fact first)
                dd = scc_depth[n_sccs]
                order = n_sccs[np.argsort(-dd, kind="stable")]
                moves, math_moves = [], []
                for s in order:
                    for m in atlas.scc_members[atlas.scc_indptr[s]:
                                               atlas.scc_indptr[s + 1]]:
                        m = int(m)
                        entry = (atlas.names[m], int(atlas.depth[m]))
                        if len(moves) < topk:
                            moves.append(entry)
                        if not atlas.cls[m] and atlas.kind[m] == "theorem" \
                                and len(math_moves) < topk:
                            math_moves.append(entry)
                    if len(moves) >= topk and len(math_moves) >= topk:
                        break
                row = {
                    "name": atlas.names[r],
                    "machinery": list(atlas.cls[r]),
                    "depth": int(atlas.depth[r]),
                    "statement_cone": s_size,
                    "proof_cone": p_size,
                    "new": n_size,
                    "new_share": round(n_size / p_size, 4) if p_size else 0.0,
                    "machinery_new": mach_new,
                    "top_moves": [{"name": nm, "depth": d} for nm, d in moves],
                    "top_math_moves": [{"name": nm, "depth": d}
                                       for nm, d in math_moves],
                }
                out.write(json.dumps(row) + "\n")
            log(f"  indexed {min(a + batch, len(roots))}/{len(roots)} roots")

    # map SCC counters back to nodes
    node_inS = inS[atlas.label]
    node_inP = inP[atlas.label]
    node_asNew = asNew[atlas.label]
    return node_inS, node_inP, node_asNew


def theorem_roots(atlas, include_machinery=False):
    out = []
    for i in range(atlas.n):
        if atlas.kind[i] != "theorem":
            continue
        if atlas.v_indptr[i + 1] == atlas.v_indptr[i]:
            continue
        if not include_machinery and atlas.cls[i]:
            continue
        out.append(i)
    return out


# ------------------------------------------------------------- study path CLI

def build_path(atlas, target, per_layer=6, drop_machinery=False):
    """Same output shape as study_path.build_path, at full-Mathlib scale."""
    t = atlas.idx.get(target)
    if t is None:
        raise KeyError(target)
    a_s = atlas.cone_from(atlas.type_deps(t))
    a_p = atlas.cone_from(atlas.body_deps(t))
    new = a_p - a_s

    def item(i):
        return {"name": atlas.names[i], "kind": atlas.kind[i],
                "depth": int(atlas.depth[i]), "machinery": list(atlas.cls[i])}

    by_depth = {}
    for i in sorted(a_s, key=lambda x: (atlas.depth[x], atlas.names[x])):
        if drop_machinery and atlas.cls[i]:
            continue
        by_depth.setdefault(int(atlas.depth[i]), []).append(i)
    layers = []
    for d in sorted(by_depth):
        ids = by_depth[d]
        layers.append({
            "depth": d,
            "items": [item(i) for i in ids[:per_layer]],
            "more": max(0, len(ids) - per_layer),
            "machinery_here": sum(1 for i in ids if atlas.cls[i]),
        })
    moves = sorted(new, key=lambda x: (-atlas.depth[x], atlas.names[x]))
    return {
        "target": target,
        "statement_cone_size": len(a_s),
        "proof_cone_size": len(a_p),
        "new_count": len(new),
        "new_share": round(len(new) / len(a_p), 4) if a_p else 0.0,
        "proof_stays_in_statement_cone": len(new) == 0,
        "statement_path": layers,
        "proof_moves": [item(i) for i in moves[:40]],
    }


def render_text(r):
    lines = []
    lines.append(f"== {r['target']}")
    lines.append(f"   statement cone {r['statement_cone_size']:,} | proof cone "
                 f"{r['proof_cone_size']:,} | new {r['new_count']:,} "
                 f"({r['new_share']:.0%} of proof)")
    lines.append("")
    lines.append("-- statement path (understand these, shallow to deep)")
    for layer in r["statement_path"]:
        row = ", ".join(i["name"] for i in layer["items"])
        extra = f"  (+{layer['more']} more)" if layer["more"] else ""
        lines.append(f"   d{layer['depth']:>3}  {row}{extra}")
    lines.append("")
    lines.append("-- proof moves (new facts the proof pulls in, deepest first)")
    math = [m for m in r["proof_moves"] if not m["machinery"]
            and m["kind"] == "theorem"]
    glue = [m for m in r["proof_moves"] if m["machinery"]]
    for m in math[:12]:
        lines.append(f"   d{m['depth']:>3}  {m['name']}")
    if glue:
        lines.append(f"   [+{len(glue)} machinery/glue moves in top "
                     f"{len(r['proof_moves'])}]")
    return "\n".join(lines)


# ----------------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("path")
    p.add_argument("targets", nargs="+")
    p.add_argument("--per-layer", type=int, default=6)
    p.add_argument("--drop-machinery", action="store_true")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("index")
    p.add_argument("--batch", type=int, default=512)
    p.add_argument("--topk", type=int, default=12)
    p.add_argument("--include-machinery", action="store_true")
    p.add_argument("--out", default=str(BIG / "mathlib_moves_index.jsonl"))
    p.add_argument("--counters-out", default=str(BIG / "mathlib_usage_counters.npz"))
    sub.add_parser("stats")
    args = ap.parse_args(argv)

    print("loading atlas...", file=sys.stderr)
    atlas = load_dump()
    print(f"atlas: {atlas.n:,} constants, {atlas.ncomp:,} SCCs, "
          f"max depth {int(atlas.scc_depth.max())}", file=sys.stderr)

    if args.cmd == "path":
        for t in args.targets:
            r = build_path(atlas, t, per_layer=args.per_layer,
                           drop_machinery=args.drop_machinery)
            print(json.dumps(r, indent=1) if args.json else render_text(r))
            print()
    elif args.cmd == "index":
        roots = theorem_roots(atlas, include_machinery=args.include_machinery)
        print(f"indexing {len(roots):,} theorem roots", file=sys.stderr)
        inS, inP, asNew = run_index(atlas, roots, args.out,
                                    batch=args.batch, topk=args.topk,
                                    log=lambda m: print(m, file=sys.stderr))
        np.savez_compressed(args.counters_out, inS=inS, inP=inP, asNew=asNew)
        print(f"wrote {args.out} and {args.counters_out}", file=sys.stderr)
    elif args.cmd == "stats":
        from collections import Counter
        print(json.dumps({
            "constants": atlas.n,
            "sccs": atlas.ncomp,
            "nontrivial_sccs": int((atlas.scc_size > 1).sum()),
            "max_depth": int(atlas.scc_depth.max()),
            "kinds": dict(Counter(atlas.kind)),
            "machinery_classes": dict(Counter(c for cs in atlas.cls for c in cs)),
        }, indent=1))


if __name__ == "__main__":
    main()
