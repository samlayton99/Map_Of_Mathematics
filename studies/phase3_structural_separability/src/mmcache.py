#!/usr/bin/env python3
"""Binary analysis cache for the full-library dump (disposable, derived).

The JSONL dump is the source of truth (regenerable from Lean); this cache is
a derived, throwaway acceleration: one parse of the 900MB JSONL (~4 min)
produces an .npz that loads in seconds and already contains the standard
derived projections (topo order, depth, in-degree), so analysis scripts skip
both the parse and the recompute.

Layout (all numpy arrays; graphs in CSR form, int32):
  name_bytes/name_off   utf-8 names, offsets (n+1)
  kind                  int8, index into KINDS
  cls                   uint16 bitmask over P3C classification flags
  ir                    bool (inductive isRec)
  {t,v,hb,rt}_indptr/{t,v,hb,rt}_idx   CSR edges (deduped, self-loops kept
                                        as in the dump; rt preserves order)
  order                 topological order over value-or-type deps (deps first)
  cyclic                residue node ids (unsafe-rec artifacts)
  depth                 recursive unfolding depth (cyclic fixpoint applied)
  indeg_v               distinct-user counts over value deps

Usage:
  python mmcache.py <dump.jsonl> [cache.npz]     # build
  from mmcache import load; L = load(cache)      # analyze
  L.idx (name->id dict, lazy), L.names(i), L.deps_v(i) -> np array, ...
"""
import json, os, sys, time
import numpy as np

KINDS = ["", "theorem", "def", "constructor", "recursor", "inductive",
         "opaque", "axiom", "quot"]
P3C = ["typeclass-instance", "recursor", "structure-projection", "generated",
       "internal-detail", "eq-machinery", "logic-core", "coercion"]


def build(dump_path, cache_path):
    t0 = time.time()
    idx, names = {}, []
    kinds, cls, ir = [], [], []
    edges = {k: [] for k in ("t", "v", "hb", "rt")}

    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            kinds.append(0); cls.append(0); ir.append(False)
            for k in edges:
                edges[k].append(())
        return i

    kcode = {k: i for i, k in enumerate(KINDS)}
    ccode = {c: 1 << i for i, c in enumerate(P3C)}
    with open(dump_path) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = kcode.get(r["k"], 0)
            m = 0
            for c in r["c"]:
                m |= ccode.get(c, 0)
            cls[i] = m
            ir[i] = bool(r.get("ir", False))
            edges["t"][i] = tuple(nid(d) for d in r["t"])
            edges["v"][i] = tuple(nid(d) for d in r["v"])
            edges["hb"][i] = tuple(nid(d) for d in r.get("hb", ()))
            edges["rt"][i] = tuple(nid(d) for d in r.get("rt", ()))
    n = len(names)
    print(f"parsed {n} constants in {time.time()-t0:.0f}s", flush=True)

    out = {}
    name_bytes = "\x00".join(names).encode("utf-8")
    off = np.zeros(n + 1, dtype=np.int64)
    p = 0
    for i, nm in enumerate(names):
        off[i] = p
        p += len(nm.encode("utf-8")) + 1
    off[n] = p
    out["name_bytes"] = np.frombuffer(name_bytes + b"\x00", dtype=np.uint8)
    out["name_off"] = off
    out["kind"] = np.array(kinds, dtype=np.int8)
    out["cls"] = np.array(cls, dtype=np.uint16)
    out["ir"] = np.array(ir, dtype=bool)
    for k, es in edges.items():
        indptr = np.zeros(n + 1, dtype=np.int64)
        for i, e in enumerate(es):
            indptr[i + 1] = indptr[i] + len(e)
        flat = np.zeros(indptr[-1], dtype=np.int32)
        for i, e in enumerate(es):
            flat[indptr[i]:indptr[i + 1]] = e
        out[f"{k}_indptr"] = indptr
        out[f"{k}_idx"] = flat

    # derived: value-or-type deps, dedup + no self, topo, depth, indeg_v
    deps = [tuple(set(edges["v"][i] or edges["t"][i]) - {i}) for i in range(n)]
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
    cyc = sorted(set(range(n)) - set(order))
    depth = np.zeros(n, dtype=np.int32)
    for i in order:
        if deps[i]:
            depth[i] = 1 + max(depth[d] for d in deps[i])
    cycset = set(cyc)
    for _ in range(3):
        for i in cyc:
            ds = [depth[d] for d in deps[i] if d not in cycset]
            if ds:
                depth[i] = 1 + max(ds)
    indeg_v = np.zeros(n, dtype=np.int64)
    for i in range(n):
        s, e = out["v_indptr"][i], out["v_indptr"][i + 1]
        for d in set(out["v_idx"][s:e].tolist()):
            if d != i:
                indeg_v[d] += 1
    out["order"] = np.array(order, dtype=np.int32)
    out["cyclic"] = np.array(cyc, dtype=np.int32)
    out["depth"] = depth
    out["indeg_v"] = indeg_v
    # dep CSR (value-or-type, dedup, no self) since every script rebuilds it
    dp = np.zeros(n + 1, dtype=np.int64)
    for i, ds in enumerate(deps):
        dp[i + 1] = dp[i] + len(ds)
    df = np.zeros(dp[-1], dtype=np.int32)
    for i, ds in enumerate(deps):
        df[dp[i]:dp[i + 1]] = ds
    out["dep_indptr"] = dp
    out["dep_idx"] = df

    np.savez(cache_path, **out)
    print(f"cache written: {cache_path} "
          f"({os.path.getsize(cache_path)//2**20} MB, {time.time()-t0:.0f}s total)", flush=True)


class Lib:
    def __init__(self, z):
        self.z = z
        self.n = len(z["kind"])
        self.kind = z["kind"]; self.cls = z["cls"]; self.ir = z["ir"]
        self.depth = z["depth"]; self.order = z["order"]
        self.cyclic = z["cyclic"]; self.indeg_v = z["indeg_v"]
        self._names = None; self._idx = None
        self._nb = z["name_bytes"].tobytes(); self._off = z["name_off"]

    def name(self, i):
        return self._nb[self._off[i]:self._off[i + 1] - 1].decode("utf-8")

    @property
    def names(self):
        if self._names is None:
            self._names = self._nb.decode("utf-8").split("\x00")[:self.n]
        return self._names

    @property
    def idx(self):
        if self._idx is None:
            self._idx = {nm: i for i, nm in enumerate(self.names)}
        return self._idx

    def _csr(self, k, i):
        p = self.z[f"{k}_indptr"]
        return self.z[f"{k}_idx"][p[i]:p[i + 1]]

    def deps_t(self, i): return self._csr("t", i)
    def deps_v(self, i): return self._csr("v", i)
    def hb(self, i): return self._csr("hb", i)
    def rt(self, i): return self._csr("rt", i)
    def deps(self, i): return self._csr("dep", i)   # value-or-type, dedup, no self

    def kind_is(self, name):
        return self.kind == KINDS.index(name)

    def cls_has(self, cname):
        return (self.cls & np.uint16(1 << P3C.index(cname))) != 0


def load(cache_path):
    return Lib(np.load(cache_path, allow_pickle=False))


if __name__ == "__main__":
    dump = sys.argv[1]
    cache = sys.argv[2] if len(sys.argv) > 2 else dump.replace(".jsonl", ".npz")
    build(dump, cache)
