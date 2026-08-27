#!/usr/bin/env python
"""Scaled train-module task file for reference-trace extraction.

Samples N train-module (module-holdout, seed 1, same as the benchmark
suite) unclassified theorems with proof bodies, and writes S1-style tasks:
bw/rw = exact D_all support (aux-inlined), fb = own-module forbid list.

Run: ~/venv/general_ml/bin/python train_tasks.py <N> <out.json> [seed]
"""
import json
import sys
import time

import numpy as np

from atlas import load_dump, theorem_roots, BIG
from accessibility import Accessibility
from heads_util import load_heads
from rolodex2 import HOLDOUT_FRAC
from support_tasks import expand_support
import rolodex as R


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def main():
    n_want = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    out = sys.argv[2] if len(sys.argv) > 2 else str(BIG / "support_tasks_train3k.json")
    sample_seed = int(sys.argv[3]) if len(sys.argv) > 3 else 7

    log("loading atlas, accessibility, heads...")
    a = load_dump()
    acc = Accessibility(a)
    ch, _, _ = load_heads()
    roots = theorem_roots(a)

    # module-holdout split, SAME seed as the benchmark suite
    rng = np.random.default_rng(1)
    root_mods = acc.mod_of[np.array(roots)]
    mathlib_mods = [i for i, nm in enumerate(acc.mod_names)
                    if nm.startswith("Mathlib.")]
    held = set(int(x) for x in
               rng.choice(mathlib_mods,
                          size=int(len(mathlib_mods) * HOLDOUT_FRAC),
                          replace=False))
    train_pos = [p for p in range(len(roots)) if int(root_mods[p]) not in held]
    log(f"{len(train_pos)} train-module theorem roots")

    # exclude anything already in the 300-train file (dataset separation
    # is by module split; this just avoids duplicate rows)
    prev = {t["n"] for t in
            json.load(open(BIG / "support_tasks_train300.json"))["tasks"]}

    srng = np.random.default_rng(sample_seed)
    order = srng.permutation(len(train_pos))
    is_eqiff = lambda c: ch.get(a.names[c]) in ("Eq", "Iff")

    tasks = []
    for oi in order:
        if len(tasks) >= n_want:
            break
        t = roots[train_pos[int(oi)]]
        nm = a.names[t]
        if nm in prev:
            continue
        d_all = expand_support(a, t, nm)
        if not d_all or len(d_all) > 120:
            continue
        stmt_cone = a.cone_from(a.type_deps(t))
        own = acc.mod_of[t]
        own_members = np.where(acc.mod_of == own)[0]
        forbid = [a.names[int(c)] for c in own_members
                  if int(c) not in stmt_cone and int(c) not in d_all
                  and int(c) != t]
        sup = sorted(d_all, key=lambda c: -a.depth[c])
        tasks.append({
            "n": nm,
            "bw": [a.names[c] for c in sup],
            "rw": [a.names[c] for c in sup if is_eqiff(c)],
            "fb": forbid,
        })
        if len(tasks) % 500 == 0:
            log(f"{len(tasks)} tasks built")

    with open(out, "w") as f:
        json.dump({"tasks": tasks}, f)
    log(f"wrote {len(tasks)} tasks -> {out}")


if __name__ == "__main__":
    main()
