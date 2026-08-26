#!/usr/bin/env python
"""Proof motifs: recurring premise bundles across all 287k Mathlib proofs.

A "method" (Taylor-expand-and-bound, epsilon-delta unfold, ...) should leave
a footprint: the same small set of theorems cited together by many different
proofs.  This mines those bundles from the exact citation record - the
empirical basis for the vision's method/macro layer.

Transactions: per proof, the set of cited math premises (unclassified
theorems, depth >= MIN_DEPTH to exclude logic glue).  Mines pairs and
triples, scored by count and lift; reports breadth (distinct top-level
namespaces of the citing proofs) so a bundle used across domains ranks as a
technique, not a local idiom.

Run: ~/venv/general_ml/bin/python motifs.py
Writes tools/output/mathlib_proof_motifs.json
"""
import json
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

from atlas import load_dump, theorem_roots

OUT = Path(__file__).resolve().parent / "output"
MIN_DEPTH = 20          # premises below this are logic/arith glue
MAX_SET = 12            # ignore mega-proofs' full blowup: cap itemset source
MIN_COUNT = 30


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def main():
    log("loading atlas...")
    a = load_dump()
    roots = theorem_roots(a)
    isthm = np.zeros(a.n, dtype=bool)
    for i in range(a.n):
        if a.kind[i] == "theorem" and not a.cls[i] and a.depth[i] >= MIN_DEPTH:
            isthm[i] = True

    log("building transactions...")
    tx = []
    ns_of = [n.split(".", 1)[0] for n in a.names]
    single = Counter()
    for r in roots:
        prem = np.unique(a.v_indices[a.v_indptr[r]:a.v_indptr[r + 1]])
        t = prem[isthm[prem]]
        if len(t) < 2:
            continue
        if len(t) > MAX_SET:
            # keep the deepest members: they carry the method identity
            t = t[np.argsort(-a.depth[t])][:MAX_SET]
        t = tuple(sorted(int(x) for x in t))
        tx.append((r, t))
        for c in t:
            single[c] += 1
    log(f"{len(tx):,} transactions")

    pairs = Counter()
    triples = Counter()
    for _, t in tx:
        for p in combinations(t, 2):
            pairs[p] += 1
    log(f"{len(pairs):,} distinct pairs")
    frequent_pairs = {p for p, c in pairs.items() if c >= MIN_COUNT}
    for _, t in tx:
        if len(t) < 3:
            continue
        for tr in combinations(t, 3):
            if (tr[0], tr[1]) in frequent_pairs and \
               (tr[0], tr[2]) in frequent_pairs and \
               (tr[1], tr[2]) in frequent_pairs:
                triples[tr] += 1
    log(f"{len(triples):,} candidate triples")

    n_tx = len(tx)
    breadth = defaultdict(set)

    def lift2(p, c):
        return c * n_tx / (single[p[0]] * single[p[1]])

    top_pairs = sorted(((c, p) for p, c in pairs.items() if c >= MIN_COUNT),
                       key=lambda x: -x[0])[:3000]
    # breadth pass for winners only
    winners = {p for _, p in top_pairs}
    wtr = set(k for k, c in triples.items() if c >= MIN_COUNT)
    for r, t in tx:
        st = t
        for p in combinations(st, 2):
            if p in winners:
                breadth[p].add(ns_of[r])
        if len(st) >= 3:
            for tr in combinations(st, 3):
                if tr in wtr:
                    breadth[tr].add(ns_of[r])

    pair_rows = []
    for c, p in top_pairs[:400]:
        r = {"premises": [a.names[i] for i in p],
             "depths": [int(a.depth[i]) for i in p],
             "count": c,
             "lift": round(lift2(p, c), 1),
             "n_namespaces": len(breadth[p]),
             "namespaces": sorted(breadth[p])[:10]}
        pair_rows.append(r)
    triple_rows = []
    for tr, c in sorted(triples.items(), key=lambda kv: -kv[1])[:150]:
        triple_rows.append({
            "premises": [a.names[i] for i in tr],
            "depths": [int(a.depth[i]) for i in tr],
            "count": c,
            "n_namespaces": len(breadth[tr]),
            "namespaces": sorted(breadth[tr])[:10]})

    out = {"config": {"min_depth": MIN_DEPTH, "min_count": MIN_COUNT,
                      "max_set": MAX_SET, "n_transactions": n_tx},
           "pairs_by_count": pair_rows,
           "pairs_by_lift": sorted(
               [r for r in pair_rows if r["count"] >= 100],
               key=lambda r: -r["lift"])[:150],
           "triples_by_count": triple_rows}
    OUT.mkdir(exist_ok=True)
    (OUT / "mathlib_proof_motifs.json").write_text(json.dumps(out, indent=1))
    log("wrote mathlib_proof_motifs.json")
    for r in pair_rows[:12]:
        print(f"{r['count']:>6}  lift {r['lift']:>8}  ns {r['n_namespaces']:>3}  "
              f"{r['premises'][0]}  +  {r['premises'][1]}")


if __name__ == "__main__":
    main()
