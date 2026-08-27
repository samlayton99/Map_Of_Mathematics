#!/usr/bin/env python3
"""Display labels for machine-generated constants (the multi-parent fix).

A machine-generated constant (`gen`: no source declaration range) has a name
the compiler invented -- `AlgebraicGeometry.Scheme.Pullback.pullbackP1Iso._proof_2`.
Showing that name as a "move" is correct in content and useless as a label.
This module resolves, for each such constant, WHAT IT IS PART OF, using three
rules in order, all name-free:

  1. attribution   the constant's own proof has exactly one substantive claim
                   (not bookkeeping, not machinery) -- it IS that claim
                   (kernel necessity: derived forms prove themselves from
                   their originals). Recurses, cycle-safe, <=3 hops.
  2. def-user      exactly one non-generated, non-Prop constant cites it
                   load-bearing -- it is an obligation of that definition
                   ("part of the construction of X").
  3. stmt-subject  the concept in its own statement that definitionally
                   contains the other statement concepts -- what the
                   statement is ABOUT (covers `X.eq_N` equation lemmas).

Unresolved constants keep their raw name: an honest "no label" beats a wrong
one. Nothing is renamed in the record; this is a display map only.

Writes the full map (24MB, ~185k labels) to the scratchpad; a coverage
summary with a sample lives in data/parent_labels_summary.json.
"""
import json, os
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP = os.path.join(SCRATCH2, "mathlib_deps7.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
LOAD_ROLES = (0, 1, 2, 7)
LAMBDA = 20
NPROOF_FLOOR = 200
THETA = 0.02


def load():
    idx, names = {}, []
    deps_v, deps_t, kinds, vo, pr, gen, ps, ar = [], [], [], [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            deps_v.append(()); deps_t.append(()); kinds.append("")
            vo.append(()); pr.append(False); gen.append(False); ps.append(False)
            ar.append(0)
        return i
    with open(DUMP) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]
            pr[i] = bool(r.get("pr", False)); gen[i] = bool(r.get("gen", False))
            ps[i] = bool(r.get("ps", False)); ar[i] = int(r.get("ar", 0))
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
            vo[i] = tuple(tuple(int(x) for x in row) for row in r.get("vo", ()))
    return idx, names, deps_v, deps_t, kinds, vo, pr, gen, ps, ar


def main():
    idx, names, deps_v, deps_t, kinds, vo, pr, gen, ps, ar = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    pr = np.array(pr); gen = np.array(gen); ps = np.array(ps); ar = np.array(ar)
    thm = np.array([k == "theorem" for k in kinds])
    CONCEPT_KINDS = ("def", "inductive", "opaque", "quot", "axiom")
    is_concept = np.array([k in CONCEPT_KINDS for k in kinds])

    nstmt = np.zeros(n, dtype=np.int64)
    ht = np.where(thm & ~gen)[0]
    for i in ht:
        for c in set(deps_t[i]):
            nstmt[c] += 1
    univ = nstmt / max(1, len(ht))

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
    inherited = nstmt.astype(np.float64).copy()
    for p in reversed(order):
        if not is_concept[p]:
            continue
        v = inherited[p]
        if v <= 0:
            continue
        for k in deps[p]:
            if is_concept[k] and inherited[k] < v:
                inherited[k] = v
    print("graph done", flush=True)

    bare_prop = is_concept & ps & (ar == 0)

    ing = {}
    def nonuniv(c):
        r = ing.get(c)
        if r is None:
            r = frozenset(k for k in set(deps_t[c])
                          if k != c and is_concept[k] and univ[k] < THETA)
            ing[c] = r
        return r
    def bookkeeping(c):
        return all(bare_prop[k] for k in nonuniv(c))
    claimf = lambda c: pr[c] and kinds[c] not in ("constructor", "recursor")

    nproof = np.zeros(n, dtype=np.int64)
    for i in range(n):
        if not deps_v[i]:
            continue
        ks = set()
        for d, row in zip(deps_v[i], vo[i]):
            if d != i and any(row[r0] > 0 for r0 in LOAD_ROLES) and claimf(d):
                ks |= nonuniv(d)
        for k in ks:
            nproof[k] += 1
    apparatus = (is_concept & ~bare_prop & (univ < THETA) & (nproof > NPROOF_FLOOR)
                 & (nproof > LAMBDA * (inherited + 1)))
    tc = {}
    def tainted(c):
        r = tc.get(c)
        if r is None:
            r = any(apparatus[k] for k in nonuniv(c))
            tc[c] = r
        return r
    print(f"apparatus concepts: {int(apparatus.sum())}", flush=True)

    def lb_g(c):
        return {d for d, row in zip(deps_v[c], vo[c])
                if d != c and any(row[k] > 0 for k in LOAD_ROLES)}

    targets = [i for i in range(n) if gen[i] and claimf(i)]
    print(f"machine-generated claims: {len(targets)}", flush=True)
    tset = set(targets)
    ulb = {c: [] for c in targets}
    for i in range(n):
        for d, row in zip(deps_v[i], vo[i]):
            if d in tset and d != i and any(row[k] > 0 for k in LOAD_ROLES):
                ulb[d].append(i)
    print("user index done", flush=True)

    cache = {}
    def attribute(c, seen=None):
        if c in cache:
            return cache[c]
        if seen is None:
            seen = set()
        if not gen[c] or c in seen or len(seen) >= 3:
            return c
        seen.add(c)
        sub = [d for d in lb_g(c) if claimf(d) and not bookkeeping(d) and not tainted(d)]
        res = attribute(sub[0], seen) if len(sub) == 1 else c
        cache[c] = res
        return res

    def stmt_subject(c):
        sc = [k for k in set(deps_t[c]) if is_concept[k] and univ[k] < THETA and not gen[k]]
        if not sc:
            sc = [k for k in set(deps_t[c]) if is_concept[k] and not gen[k]]
        best, bestcov = None, -1.0
        for k in sc:
            kd = set(deps[k]) | {k}
            rest = [x for x in sc if x != k]
            cov = sum(1 for x in rest if x in kd) / max(1, len(rest))
            if cov > bestcov or (cov == bestcov and best is not None
                                 and depth[k] > depth[best]):
                best, bestcov = k, cov
        return best, bestcov

    out = {}
    from collections import Counter
    stats = Counter()
    for c in targets:
        a = attribute(c)
        if a != c and not gen[a]:
            out[names[c]] = {"rule": "attribution", "parent": names[a]}
            stats["attribution"] += 1
            continue
        defs = [u for u in set(ulb[c]) if not gen[u] and not pr[u]]
        if len(defs) == 1:
            out[names[c]] = {"rule": "def-user", "parent": names[defs[0]]}
            stats["def-user"] += 1
            continue
        best, cov = stmt_subject(c)
        if best is not None and cov >= 0.49:
            out[names[c]] = {"rule": "stmt-subject", "parent": names[best],
                             "coverage": round(float(cov), 2)}
            stats["stmt-subject"] += 1
            continue
        stats["unresolved"] += 1
    print("label coverage:", dict(stats),
          f"= {100 * (len(targets) - stats['unresolved']) / max(1, len(targets)):.1f}% resolved",
          flush=True)

    outp = os.environ.get("PARENT_LABELS_OUT",
                          os.path.join(SCRATCH2, "parent_labels.json"))
    with open(outp, "w") as fh:
        json.dump({"note": "display labels for machine-generated constants; "
                           "the record itself is unchanged",
                   "n_targets": len(targets), "coverage": dict(stats),
                   "labels": out}, fh)
    print("written", flush=True)


if __name__ == "__main__":
    main()
