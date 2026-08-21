#!/usr/bin/env python3
"""Phase 5: freeze the V8 boundary as a per-incidence mask (projection P4).

V8 is FROZEN per ADR-0005 -- these rules are copied from the certified round-9
script and must not be retuned in this phase. Two outputs:

  decl_logic_only[d]   every non-universal ingredient of d is a bare
                       proposition (or it has none)
  machinery[i]         incidence i cites a claim carrying apparatus
                       vocabulary, none of which appears in the certified
                       theorem's own statement

P4 = load_bearing AND is_claim AND NOT logic_only AND NOT machinery.
"""
import json, os
import numpy as np

DUMP = os.path.expanduser("~/mathmap_data/mathlib_deps7.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
LAMBDA, FLOOR, THETA = 20, 200, 0.02
LOAD_ROLES = (0, 1, 2, 7)


def main():
    idx, names = {}, []
    kinds, pr, ps, ar, gen, deps_t, deps_v, vo = [], [], [], [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            kinds.append(""); pr.append(False); ps.append(False); ar.append(0)
            gen.append(False); deps_t.append(()); deps_v.append(()); vo.append(())
        return i
    for line in open(DUMP):
        r = json.loads(line); i = nid(r["n"]); kinds[i] = r["k"]
        pr[i] = bool(r.get("pr", False)); ps[i] = bool(r.get("ps", False))
        ar[i] = int(r.get("ar", 0)); gen[i] = bool(r.get("gen", False))
        deps_t[i] = tuple(nid(d) for d in r["t"])
        deps_v[i] = tuple(nid(d) for d in r["v"])
        vo[i] = tuple(tuple(int(x) for x in row) for row in r.get("vo", ()))
    n = len(names)
    pr = np.array(pr); ps = np.array(ps); ar = np.array(ar); gen = np.array(gen)
    thm = np.array([k == "theorem" for k in kinds])
    CK = ("def", "inductive", "opaque", "quot", "axiom")
    is_concept = np.array([k in CK for k in kinds])
    print(f"declarations: {n}", flush=True)

    nstmt = np.zeros(n, dtype=np.int64)
    ht = np.where(thm & ~gen)[0]
    for i in ht:
        for c in set(deps_t[i]):
            nstmt[c] += 1
    univ = nstmt / max(1, len(ht))

    deps = [dv if dv else dt for dv, dt in zip(deps_v, deps_t)]
    deps = [tuple(d for d in set(ds) if d != i) for i, ds in enumerate(deps)]
    indeg = np.zeros(n, dtype=np.int32); users = [[] for _ in range(n)]
    for i, ds in enumerate(deps):
        indeg[i] = len(ds)
        for d in ds: users[d].append(i)
    from collections import deque
    q = deque(np.where(indeg == 0)[0].tolist()); order = []
    while q:
        i = q.popleft(); order.append(i)
        for u in users[i]:
            indeg[u] -= 1
            if indeg[u] == 0: q.append(u)
    del users
    inherited = nstmt.astype(np.float64).copy()
    for p in reversed(order):
        if not is_concept[p]: continue
        v = inherited[p]
        if v <= 0: continue
        for k in deps[p]:
            if is_concept[k] and inherited[k] < v: inherited[k] = v

    bare = is_concept & ps & (ar == 0)
    ing = {}
    def nonuniv(c):
        r = ing.get(c)
        if r is None:
            r = frozenset(k for k in set(deps_t[c])
                          if k != c and is_concept[k] and univ[k] < THETA)
            ing[c] = r
        return r
    claimf = pr & np.array([k not in ("constructor", "recursor") for k in kinds])

    nproof = np.zeros(n, dtype=np.int64)
    for i in range(n):
        if not deps_v[i]: continue
        ks = set()
        for d, row in zip(deps_v[i], vo[i]):
            if d != i and any(row[r0] > 0 for r0 in LOAD_ROLES) and claimf[d]:
                ks |= nonuniv(d)
        for k in ks: nproof[k] += 1
    apparatus = (is_concept & ~bare & (univ < THETA) & (nproof > FLOOR)
                 & (nproof > LAMBDA * (inherited + 1)))
    print(f"apparatus concepts: {int(apparatus.sum())}", flush=True)

    logic_only = np.array([all(bare[k] for k in nonuniv(c)) for c in range(n)])
    tainted = np.array([any(apparatus[k] for k in nonuniv(c)) for c in range(n)])
    print(f"logic-only decls: {int(logic_only.sum())}, tainted: {int(tainted.sum())}",
          flush=True)

    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    a_col = inc["artifact"].astype(np.int64); d_col = inc["decl"].astype(np.int64)
    certifies = arts["certifies"].astype(np.int64)
    tgt = certifies[a_col]

    # machinery: tainted candidate whose ingredients miss the target's statement
    mach = np.zeros(len(d_col), dtype=bool)
    stmt_cache = {}
    cand = np.where(tainted[d_col])[0]
    print(f"tainted incidences to test: {len(cand)}", flush=True)
    for pos in cand:
        T = tgt[pos]
        sc = stmt_cache.get(T)
        if sc is None:
            sc = frozenset(k for k in set(deps_t[T])
                           if is_concept[k] and univ[k] < THETA)
            stmt_cache[T] = sc
        mach[pos] = not (nonuniv(d_col[pos]) & sc)
    print(f"machinery incidences: {int(mach.sum())}", flush=True)

    np.savez_compressed(os.path.join(DATA, "v8_mask.npz"),
                        decl_logic_only=logic_only, decl_tainted=tainted,
                        decl_is_claim=claimf, apparatus=apparatus,
                        machinery=mach)
    print("written", flush=True)


if __name__ == "__main__":
    main()
