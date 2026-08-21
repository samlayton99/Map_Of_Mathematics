"""Recompute analysis 1 (relative hubs) and merge it into map_analysis.json.

Cheap (seconds) — used to refresh the hub tables without re-running the
expensive community/distance analyses.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_graph as MG  # noqa: E402
import map_analysis as MA  # noqa: E402

A = MG.load_arrays()
area, area_names = MA.build_areas(A["names"])
cls = MA.class_vector(A)
path = os.path.join(MG.OUT_DIR, "map_analysis.json")
out = json.load(open(path))
for name in MA.EDGE_SETS:
    p = os.path.join(MG.OUT_DIR, "edges_%s.npz" % name)
    if not os.path.exists(p) or name not in out["edge_sets"]:
        continue
    z = np.load(p)
    src = z["src_decl"].astype(np.int64)
    dst = z["dst_decl"].astype(np.int64)
    MA.log("=== %s" % name)
    out["edge_sets"][name]["hubs"] = MA.analysis_hubs(
        src, dst, A, area, area_names, cls)
json.dump(out, open(path, "w"), indent=2)
MA.log("patched %s" % path)
