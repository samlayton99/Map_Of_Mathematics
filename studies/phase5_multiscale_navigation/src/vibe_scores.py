#!/usr/bin/env python3
"""Add true GLOBAL score percentiles to vibe.json.

Without this, a "global score threshold" control in the viewer has nothing
cross-proof to threshold on, and would silently degrade into a per-proof
percentile -- a different policy wearing the same label. Rather than ship
that, compute the real thing: each candidate's position in the ranking's
global score order over the whole universe.

`score_pct` = 0.0 for the single best-scoring candidate in the library and
1.0 for the worst, so "global top q%" is exactly `score_pct <= q/100`.

CAVEAT carried into the UI: cross-proof score comparability has never been
validated in this program. A lexicographic key that orders candidates
correctly WITHIN a proof need not be comparable BETWEEN proofs, and most of
these rankings are heavily tied globally. The tie fraction is recorded here
so the viewer can show it next to the control.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

from mathmap_eval import rankings as R                    # noqa: E402
from mathmap_eval.corpus import get_corpus                # noqa: E402

OUT = os.path.join(ROOT, "dashboard", "data", "vibe.json")


def main():
    try:
        from mathmap_eval import plugins
        plugins.load_local()
    except Exception:
        pass
    vibe = json.load(open(OUT))
    c = get_corpus()
    want = sorted({int(cd["incidence"]) for p in vibe["proofs"]
                   for cd in p["candidates"]})
    universes = vibe["universes"]
    names = vibe["rankings"]
    pctl = {}
    ties = {}
    for U in universes:
        base = np.where(c.universe(U))[0]
        pos = {int(p): i for i, p in enumerate(base)}
        for nm in names:
            t0 = time.time()
            spec = R.get(nm)
            keys = spec.keys(c, base)
            order = np.lexsort(tuple(reversed(keys)))
            rank = np.empty(len(base), dtype=np.float64)
            rank[order] = np.arange(len(base))
            # ties share a percentile: use the first index of each tie block
            sorted_keys = np.stack([np.asarray(k)[order] for k in keys], axis=1)
            newblk = np.ones(len(order), bool)
            newblk[1:] = (sorted_keys[1:] != sorted_keys[:-1]).any(axis=1)
            blockstart = np.maximum.accumulate(
                np.where(newblk, np.arange(len(order)), 0))
            shared = np.empty(len(base), dtype=np.float64)
            shared[order] = blockstart
            pctl[f"{U}|{nm}"] = {
                str(i): float(shared[pos[i]] / max(len(base) - 1, 1))
                for i in want if i in pos}
            ties[f"{U}|{nm}"] = float(1.0 - newblk.mean())
            print(f"  {U}|{nm:<22} tied={ties[f'{U}|{nm}']:.4f} "
                  f"({time.time() - t0:.0f}s)", flush=True)

    for p in vibe["proofs"]:
        for cd in p["candidates"]:
            for U in universes:
                for nm in names:
                    k = f"{U}|{nm}"
                    v = pctl[k].get(str(int(cd["incidence"])))
                    if v is not None and k in p["orders"]:
                        p["orders"][k][str(cd["n"])]["score_pct"] = v
    vibe["global_score_tie_fraction"] = ties
    vibe["global_score_caveat"] = (
        "score_pct is the candidate's position in this ranking's GLOBAL score "
        "order over the whole universe, ties sharing a percentile. "
        "Cross-proof score comparability has never been validated in this "
        "program: a key that orders candidates correctly within a proof need "
        "not be comparable between proofs. Treat the global-threshold policy "
        "as exploratory.")
    with open(OUT, "w") as f:
        json.dump(vibe, f, allow_nan=False)
    print(f"written {OUT}", flush=True)


if __name__ == "__main__":
    main()
