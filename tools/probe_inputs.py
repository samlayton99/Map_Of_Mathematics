#!/usr/bin/env python
"""Build the live legality-probe input: goals + candidate lists.

For N module-holdout test theorems, assemble the candidate set a real
proof-search step would consider at the root goal:
  - the refined structural pool (goal head + LHS head), accessible only,
    top STRUCT_K by citation count,
  - the top PEER_K peer-retrieved premises (accessible),
  - every actually-cited accessible math premise (ground truth - included
    so the probe measures their backward-applicability too).

Writes bigdata/probe_input.json (for `mathrecord probe`) and
bigdata/probe_meta.json (per-goal candidate provenance for analysis).

Run: ~/venv/general_ml/bin/python probe_inputs.py [--n 1000]
"""
import argparse
import json
import sys
import time
from collections import defaultdict

import numpy as np

from atlas import load_dump, theorem_roots, BIG
from accessibility import Accessibility
from heads_util import load_heads, refined_key
import rolodex as R
from rolodex2 import score_peers_masked, HOLDOUT_FRAC

STRUCT_K = 200
PEER_K = 64


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    args = ap.parse_args(argv)

    log("loading atlas, accessibility, heads...")
    a = load_dump()
    acc = Accessibility(a)
    ch, ca, _ = load_heads()
    roots = theorem_roots(a)
    isthm = np.zeros(a.n, dtype=bool)
    for i in range(a.n):
        if a.kind[i] == "theorem" and not a.cls[i]:
            isthm[i] = True

    # same holdout split as rolodex2/reranker
    rng = np.random.default_rng(1)
    root_mods = acc.mod_of[np.array(roots)]
    mathlib_mods = [i for i, nm in enumerate(acc.mod_names)
                    if nm.startswith("Mathlib.")]
    held = set(int(x) for x in
               rng.choice(mathlib_mods,
                          size=int(len(mathlib_mods) * HOLDOUT_FRAC),
                          replace=False))
    test_all = [p for p in range(len(roots)) if int(root_mods[p]) in held]
    train_pos = [p for p in range(len(roots)) if int(root_mods[p]) not in held]
    rng.shuffle(test_all)
    test_pos = [p for p in test_all
                if isthm[R.proof_deps(a, roots[p])].any()][:args.n]
    train_roots = [roots[p] for p in train_pos]

    log("stats (df + inverted index on train)...")
    df = np.zeros(a.n, dtype=np.int64)
    cite = np.zeros(a.n, dtype=np.int64)
    for r in train_roots:
        df[np.unique(R.stmt_deps(a, r))] += 1
        cite[np.unique(R.proof_deps(a, r))] += 1
    inv = R.build_inverted(a, train_roots, df)

    log("building refined-key index...")
    by_key = defaultdict(list)
    for i in range(a.n):
        if a.kind[i] in ("theorem", "constructor"):
            k = refined_key(ch, ca, a.names[i])
            if k:
                by_key[k].append(i)
    for k in by_key:
        ids = np.array(by_key[k])
        by_key[k] = ids[np.argsort(-cite[ids], kind="stable")]

    goals, meta = [], []
    for p in test_pos:
        r = roots[p]
        amask = acc.mask(r)
        if amask is None:
            continue
        prem = np.unique(R.proof_deps(a, r))
        target = [int(c) for c in prem[isthm[prem] & amask[prem]]]
        if not target:
            continue
        gkey = refined_key(ch, ca, a.names[r])
        struct = []
        if gkey is not None and gkey in by_key:
            ids = by_key[gkey]
            ids = ids[ids != r]
            ids = ids[amask[ids]][:STRUCT_K]
            struct = [int(i) for i in ids]
        vk = score_peers_masked(a, r, train_roots, df, inv, None, amask)
        peers = []
        if vk is not None:
            vv = vk.copy()
            vv[~amask] = -np.inf
            vv[r] = -np.inf
            ids = np.argpartition(-vv, PEER_K)[:PEER_K]
            peers = [int(i) for i in ids[vv[ids] > 0]]
        cands = list(dict.fromkeys(struct + peers + target))
        goals.append({"n": a.names[r], "cands": [a.names[c] for c in cands]})
        meta.append({"n": a.names[r],
                     "target": [a.names[c] for c in target],
                     "struct": [a.names[c] for c in struct],
                     "peers": [a.names[c] for c in peers],
                     "goal_key": list(gkey) if gkey else None})

    (BIG / "probe_input.json").write_text(json.dumps({"goals": goals}))
    (BIG / "probe_meta.json").write_text(json.dumps(meta))
    log(f"wrote {len(goals)} goals; mean candidates "
        f"{np.mean([len(g['cands']) for g in goals]):.0f}")


if __name__ == "__main__":
    main()
