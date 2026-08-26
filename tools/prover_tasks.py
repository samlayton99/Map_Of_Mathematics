#!/usr/bin/env python
"""Build prover task files: held-out theorems + conservative global toolkits.

Accessibility regime: CONSERVATIVE - transitively imported modules only,
the theorem's own module excluded entirely.  Leak-free by construction
(sacrifices legitimate same-file premises; that price is reported).

Toolkit per theorem (the "global rolodex" the search will instantiate
locally):
  bw: backward candidates - accessible theorems ranked by peer score and
      citation prior (union of top lists, capped)
  rw: rewrite candidates - accessible Eq/Iff-conclusion theorems by the
      same ranking (the Lean side re-checks conclusion shape and filters
      by head occurrence per goal)

Run: ~/venv/general_ml/bin/python prover_tasks.py [--n 120] [--cap 220]
Writes bigdata/prover_tasks.json (+ sidecar bigdata/prover_tasks_meta.json)
"""
import argparse
import json
import sys
import time

import numpy as np

from atlas import load_dump, theorem_roots, BIG
from accessibility import Accessibility
from heads_util import load_heads
import rolodex as R
from rolodex2 import score_peers_masked, HOLDOUT_FRAC


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=120)
    ap.add_argument("--cap", type=int, default=220)
    ap.add_argument("--out", default=str(BIG / "prover_tasks.json"))
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
    is_eqiff = np.zeros(a.n, dtype=bool)
    for i in range(a.n):
        if isthm[i] and ch.get(a.names[i]) in ("Eq", "Iff"):
            is_eqiff[i] = True

    # module-holdout split, same seed as the benchmark suite
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

    log("train statistics...")
    df = np.zeros(a.n, dtype=np.int64)
    cite = np.zeros(a.n, dtype=np.int64)
    for r in train_roots:
        df[np.unique(R.stmt_deps(a, r))] += 1
        cite[np.unique(R.proof_deps(a, r))] += 1
    inv = R.build_inverted(a, train_roots, df)

    tasks, meta = [], []
    excluded_own_module_premises = 0
    total_premises = 0
    for p in test_pos:
        r = roots[p]
        vis = acc.module_visible(r)
        if vis is None:
            continue
        vis = vis.copy()
        vis[acc.mod_of[r]] = False          # conservative: own module OUT
        amask = np.zeros(a.n, dtype=bool)
        mapped = acc.mod_of >= 0
        amask[mapped] = vis[acc.mod_of[mapped]]

        prem = np.unique(R.proof_deps(a, r))
        target = prem[isthm[prem]]
        total_premises += len(target)
        excluded_own_module_premises += int((~amask[target]).sum())

        # rank accessible candidates: peers + citation prior
        vk = score_peers_masked(a, r, train_roots, df, inv, None, amask)
        scores = cite.astype(np.float64).copy()
        if vk is not None:
            scores = scores / max(scores.max(), 1) + 3.0 * vk / max(vk.max(), 1)
        ok = amask & isthm
        ok[r] = False
        ids = np.where(ok)[0]
        order = ids[np.argsort(-scores[ids], kind="stable")]
        bw = order[:args.cap]
        rw_ids = order[is_eqiff[order]][:args.cap // 2]
        tasks.append({"n": a.names[r],
                      "bw": [a.names[c] for c in bw],
                      "rw": [a.names[c] for c in rw_ids]})
        meta.append({"n": a.names[r],
                     "module": acc.mod_names[acc.mod_of[r]],
                     "target": [a.names[c] for c in target],
                     "target_accessible": [a.names[c] for c in target[amask[target]]]})

    with open(args.out, "w") as f:
        json.dump({"tasks": tasks}, f)
    (BIG / "prover_tasks_meta.json").write_text(json.dumps(meta))
    log(f"wrote {len(tasks)} tasks; conservative regime excludes "
        f"{excluded_own_module_premises}/{total_premises} cited premises "
        f"({excluded_own_module_premises / max(total_premises,1):.1%}) as same-module")


if __name__ == "__main__":
    main()
