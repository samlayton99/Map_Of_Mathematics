#!/usr/bin/env python3
"""Decision 1: build edges_GAPM = GAP restricted to SOURCES whose own module
is Mathlib.* and not Mathlib.Tactic.*.  Reports removal accounting."""
import json
import os
import sys

import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "data", "map_final")
P5 = os.path.normpath(os.path.join(ROOT, "..", "phase5_multiscale_navigation", "data"))
MODULES_TSV = os.environ.get("MAPGRAPH_MODULES_TSV", "/Users/sam/mathmap_data/all_modules.tsv")

names = json.load(open(os.path.join(P5, "names.json")))
n = len(names)
mod = {}
with open(MODULES_TSV) as fh:
    for line in fh:
        nm, _, m = line.rstrip("\n").partition("\t")
        if m:
            mod[nm] = m
modarr = [mod.get(nm) for nm in names]


def is_math_module(m):
    if m is None:
        return False
    if not m.startswith("Mathlib"):
        return False
    if m == "Mathlib" or m.startswith("Mathlib."):
        pass
    else:
        return False          # e.g. "MathlibFoo"
    return not (m == "Mathlib.Tactic" or m.startswith("Mathlib.Tactic."))


math_src = np.array([is_math_module(m) for m in modarr], dtype=bool)

# area labels (same convention as map_analysis.build_areas)
az = np.load(os.path.join(OUT, "areas.npz"), allow_pickle=True)
area = az["area"]
area_names = [str(x) for x in az["area_names"]]

z = np.load(os.path.join(OUT, "edges_GAP.npz"))
src = z["src_decl"].astype(np.int64)
dst = z["dst_decl"].astype(np.int64)

keep = math_src[src]
np.savez_compressed(os.path.join(OUT, "edges_GAPM.npz"),
                    src_decl=src[keep].astype(np.int32),
                    dst_decl=dst[keep].astype(np.int32))

usrc = np.unique(src)
kept_src = np.unique(src[keep])
lost_src = np.setdiff1d(usrc, kept_src)

# why sources are dropped
reason = {}
for d in lost_src.tolist():
    m = modarr[d]
    if m is None:
        r = "no module"
    elif m.startswith("Mathlib.Tactic"):
        r = "Mathlib.Tactic.*"
    else:
        r = m.split(".")[0]
    reason[r] = reason.get(r, 0) + 1

# area mass lost, by SOURCE area and by DESTINATION area
def area_counts(mask, arr):
    c = np.bincount(area[arr[mask]], minlength=len(area_names))
    return c


src_all = area_counts(np.ones(len(src), bool), src)
src_kept = area_counts(keep, src)
dst_all = area_counts(np.ones(len(src), bool), dst)
dst_kept = area_counts(keep, dst)

rows = []
for i, nm in enumerate(area_names):
    if src_all[i] == 0 and dst_all[i] == 0:
        continue
    rows.append({
        "area": nm,
        "src_edges_all": int(src_all[i]), "src_edges_kept": int(src_kept[i]),
        "src_edges_lost": int(src_all[i] - src_kept[i]),
        "src_frac_lost": float(1 - src_kept[i] / max(1, src_all[i])),
        "dst_edges_all": int(dst_all[i]), "dst_edges_kept": int(dst_kept[i]),
        "dst_frac_lost": float(1 - dst_kept[i] / max(1, dst_all[i])),
    })
rows.sort(key=lambda r: -r["src_edges_lost"])

# destination-node coverage: do targets disappear entirely?
dst_all_nodes = np.unique(dst)
dst_kept_nodes = np.unique(dst[keep])

res = {
    "n_edges_GAP": int(len(src)),
    "n_edges_GAPM": int(keep.sum()),
    "edges_removed": int((~keep).sum()),
    "edge_removal_frac": float((~keep).mean()),
    "n_sources_GAP": int(len(usrc)),
    "n_sources_GAPM": int(len(kept_src)),
    "sources_removed": int(len(lost_src)),
    "source_removal_frac": float(len(lost_src) / len(usrc)),
    "removed_source_reasons": dict(sorted(reason.items(), key=lambda kv: -kv[1])),
    "n_dst_nodes_GAP": int(len(dst_all_nodes)),
    "n_dst_nodes_GAPM": int(len(dst_kept_nodes)),
    "dst_nodes_lost": int(len(dst_all_nodes) - len(dst_kept_nodes)),
    "per_area": rows,
}
with open(os.path.join(OUT, "decision1_scoping.json"), "w") as fh:
    json.dump(res, fh, indent=2)
print(json.dumps({k: v for k, v in res.items() if k != "per_area"}, indent=2))
print("\ntop areas by source-edge loss:")
for r in rows[:15]:
    print("  %-18s src lost %8d / %8d (%.3f)   dst lost frac %.3f"
          % (r["area"], r["src_edges_lost"], r["src_edges_all"],
             r["src_frac_lost"], r["dst_frac_lost"]))
