"""EL0 budget sensitivity: how much of the EL0 admission is decided by the
stmt key (the flag that is being rebuilt) vs by dem/lane.

Writes data/map/el0_sensitivity.json.  Does not touch the edge files.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_graph as MG  # noqa: E402

A = MG.load_arrays()
owner = np.load(os.path.join(MG.OUT_DIR, "owner.npy"))
C = MG.build_candidates(A, owner)
order, rank = MG.order_and_dedup(C, len(A["certifies"]))

n_art = len(A["certifies"])
nongen = np.flatnonzero(~A["is_generated"])
o = order


def k_stats(mask, label):
    sel = o[mask]
    k = np.bincount(C["artifact"][sel], minlength=n_art)[nongen]
    d = dict(label=label, n_edges=int(len(sel)), mean=float(k.mean()),
             median=float(np.median(k)), p90=float(np.percentile(k, 90)),
             p99=float(np.percentile(k, 99)), max=int(k.max()),
             frac_zero=float((k == 0).mean()))
    MG.log("%-28s edges %8d  mean %.2f median %.0f p90 %.0f max %4d zero %.3f"
           % (label, d["n_edges"], d["mean"], d["median"], d["p90"], d["max"],
              d["frac_zero"]))
    return d


dem = C["dem"][o]
lane = C["lane"][o]
stmt = C["stmt"][o]
res = [
    k_stats((dem == 0) & (lane == 0) & (stmt == 0), "EL0 (dem0 lane0 stmt0)"),
    k_stats((dem == 0) & (lane == 0), "dem0 lane0 (no stmt key)"),
    k_stats((dem == 0), "dem0 (load-bearing only)"),
    k_stats(np.ones(len(o), dtype=bool), "all candidates"),
]
with open(os.path.join(MG.OUT_DIR, "el0_sensitivity.json"), "w") as fh:
    json.dump(res, fh, indent=2)
MG.log("wrote el0_sensitivity.json")
