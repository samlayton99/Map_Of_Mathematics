#!/usr/bin/env python3
"""Q3: the slider as a scientific object.

Per PRE_REGISTRATION_V8ALT.md Q3.1-Q3.3. As k (citations admitted per proof)
rises, record:

  - components and giant-component fraction;
  - EVERY component merge, and which ranked citation caused it, and what KIND
    of declaration that citation was (theorem / definition-construction /
    instance / glue). Registered question: are definitions the long-distance
    bridges the claim-only view was hiding?
  - structural signals for choosing slider positions rather than picking
    k = 1,2,4,8 for convenience: merge rate, the derivative of the
    giant-component curve, and the entropy of the component-size distribution.

Merges are detected with a union-find over edges added in rank order, so the
citation that first joins two basins is identified exactly, not inferred.
"""
import json, os
import numpy as np
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
KMAX = 16


class DSU:
    def __init__(self, n):
        self.p = np.arange(n, dtype=np.int64)
        self.sz = np.ones(n, dtype=np.int64)
        self.ncomp = 0

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return 0
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        return 1


def main():
    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    nodes = np.load(os.path.join(DATA, "nodes.npz"))
    v8 = np.load(os.path.join(DATA, "v8_mask.npz"))
    names = json.load(open(os.path.join(DATA, "names.json")))

    a_col = inc["artifact"].astype(np.int64)
    d_col = inc["decl"].astype(np.int64)
    lb = inc["load_bearing"]
    in_sw = inc["in_stmt_world"]
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"].astype(np.float64)
    kind = nodes["kind"]
    n = len(depth)
    tgt = certifies[a_col]
    is_claim = v8["decl_is_claim"]
    logic_only = v8["decl_logic_only"]
    machinery = v8["machinery"]

    bi = np.where(lb & (tgt != d_col))[0]
    demote = logic_only[d_col[bi]] | machinery[bi]
    not_new = in_sw[bi]
    dep = depth[d_col[bi]]

    # C2 (V8 rules, all declaration kinds competing) -- the candidate the
    # brief is most interested in, since it is V8 with definitions restored.
    keys = (demote.astype(np.int8), not_new.astype(np.int8), -dep)
    order = np.lexsort(tuple(reversed(keys)) + (a_col[bi],))
    s = bi[order]
    aa = a_col[s]
    new = np.empty(len(s), bool); new[0] = True; new[1:] = aa[1:] != aa[:-1]
    st = np.where(new)[0]
    cnt = np.diff(np.append(st, len(s)))
    rk = np.concatenate([np.arange(c) for c in cnt])

    def klass(i):
        d = d_col[i]
        if kind[d] in (1, 2, 5, 6, 7):
            return "definition/construction"
        if logic_only[d] or machinery[i]:
            return "glue"
        if is_claim[d]:
            return "theorem"
        return "other"

    touched = np.unique(np.concatenate([tgt[bi], d_col[bi]]))
    node_index = -np.ones(n, dtype=np.int64)
    node_index[touched] = np.arange(len(touched))
    N = len(touched)
    print(f"nodes touched: {N:,}", flush=True)

    dsu = DSU(N)
    rows, merge_kinds_by_k, first_bridge = [], {}, []
    prev_comp = N
    for k in range(KMAX):
        sel = s[rk == k]
        kinds_here = Counter()
        merges = 0
        for i in sel:
            u, v = node_index[tgt[i]], node_index[d_col[i]]
            if u < 0 or v < 0:
                continue
            if dsu.union(u, v):
                merges += 1
                c = klass(i)
                kinds_here[c] += 1
                if len(first_bridge) < 25 and k > 0:
                    first_bridge.append({
                        "k": k + 1, "kind": c,
                        "theorem": names[tgt[i]], "cites": names[d_col[i]],
                        "depth_thm": int(depth[tgt[i]]),
                        "depth_cited": int(depth[d_col[i]])})
        roots = np.array([dsu.find(x) for x in range(N)])
        sizes = np.bincount(roots, minlength=N)
        sizes = sizes[sizes > 0]
        ncomp = len(sizes)
        giant = sizes.max() / sizes.sum()
        p = sizes / sizes.sum()
        ent = float(-(p * np.log(p)).sum())
        rows.append({"k": k + 1, "edges_added": int(len(sel)), "merges": merges,
                     "components": int(ncomp), "giant": round(float(giant), 4),
                     "entropy": round(ent, 4),
                     "delta_components": int(prev_comp - ncomp),
                     "merge_kinds": dict(kinds_here)})
        merge_kinds_by_k[k + 1] = dict(kinds_here)
        prev_comp = ncomp
        print(f"  k={k+1:<3} added={len(sel):>8,} merges={merges:>7,} "
              f"components={ncomp:>8,} giant={giant:>7.2%} H={ent:>6.3f}  "
              + " ".join(f"{a}:{b:,}" for a, b in kinds_here.most_common(4)),
              flush=True)

    print("\n=== Q3.2 merge census: what KIND of citation reconnects the graph ===",
          flush=True)
    tot = Counter()
    for k, kk in merge_kinds_by_k.items():
        for a, b in kk.items():
            tot[a] += b
    T = sum(tot.values())
    for a, b in tot.most_common():
        print(f"  {a:<26} {b:>9,}  ({100*b/T:.1f}% of all merges)", flush=True)
    print("\n  merges at k>=2 only (the reconnection regime):", flush=True)
    tot2 = Counter()
    for k, kk in merge_kinds_by_k.items():
        if k >= 2:
            for a, b in kk.items():
                tot2[a] += b
    T2 = max(1, sum(tot2.values()))
    for a, b in tot2.most_common():
        print(f"  {a:<26} {b:>9,}  ({100*b/T2:.1f}%)", flush=True)

    print("\n=== Q3.3 where are the natural slider positions? ===", flush=True)
    g = np.array([r["giant"] for r in rows])
    dg = np.diff(g, prepend=g[0])
    for r, d_ in zip(rows, dg):
        bar = "#" * int(60 * r["giant"])
        print(f"  k={r['k']:<3} giant={r['giant']:>7.2%} d(giant)={d_:>+7.2%} "
              f"H={r['entropy']:>6.3f} |{bar}", flush=True)
    kbest = int(np.argmax(dg)) + 1
    print(f"\n  largest single jump in giant-component fraction: k={kbest}", flush=True)

    print("\n=== sample of citations that first bridged two basins (k>=2) ===",
          flush=True)
    for b in first_bridge[:18]:
        print(f"  k={b['k']} [{b['kind'][:12]:<12}] {b['theorem'][:44]:<46} -> "
              f"{b['cites'][:36]:<38} d{b['depth_thm']}->{b['depth_cited']}", flush=True)

    out = {"per_k": rows, "merge_kinds_total": dict(tot),
           "merge_kinds_k_ge_2": dict(tot2), "bridge_examples": first_bridge,
           "largest_giant_jump_at_k": kbest}
    with open(os.path.join(DATA, "merge_census.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten data/merge_census.json", flush=True)


if __name__ == "__main__":
    main()
