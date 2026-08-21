#!/usr/bin/env python3
"""P1 map-level test (H1's core claim): when each proof admits its top-k
view items as navigational edges, who are the hubs?

For each view, every artifact in the fresh 20k sample contributes edges to
its top-4 visible items. Hubs = most-linked constants. Each hub classified
by lane: infra (generated), transport (depth_stmt <= 1), instance-flavored
(min role tier == instance), mathematics (rest). The phase5 finding to beat:
junk held 49-70% of top hubs in the flat map.
"""
import json, os, sys
from collections import Counter, defaultdict
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, ".."))
spec = importlib.util.spec_from_file_location("hv", os.path.join(HERE, "hier_views.py"))
hv = importlib.util.module_from_spec(spec)
sys.argv = ["hv"]; spec.loader.exec_module(hv)

K = 4
VIEWS = ("flat", "laned")
links = {vn: Counter() for vn in VIEWS}
n = 0
for line in open(os.path.join(P6, "data", "map20k_hier.jsonl")):
    r = json.loads(line)
    if not r.get("ok"):
        continue
    v = hv.build_views(r["occ"], 0, r["n"])
    for vn in VIEWS:
        for c in v[vn][:K]:
            links[vn][c] += 1
    n += 1
    if n % 5000 == 0:
        print(f"  {n}", flush=True)

def lane_of(c):
    i = hv.name_id.get(c)
    if i is None:
        return "unknown"
    if hv.gen[i]:
        return "infra"
    if hv.depth_stmt[i] <= 1:
        return "transport"
    return "math"

out = {"n_artifacts": n, "k": K, "views": {}}
for vn in VIEWS:
    top = links[vn].most_common(100)
    lanes = Counter(lane_of(c) for c, _ in top)
    mass = Counter()
    for c, m in top:
        mass[lane_of(c)] += m
    tot = sum(m for _, m in top)
    out["views"][vn] = {
        "top100_lane_counts": dict(lanes),
        "top100_link_mass_share": {k: round(v / tot, 4) for k, v in mass.items()},
        "top20": [[c, m, lane_of(c)] for c, m in top[:20]],
    }
    print(f"\n{vn}: top-100 hubs by lane {dict(lanes)}  "
          f"link-mass share {out['views'][vn]['top100_link_mass_share']}")
    for c, m, l in out["views"][vn]["top20"][:12]:
        print(f"   {m:6d} {l:9} {c}")
json.dump(out, open(os.path.join(P6, "data", "map_hubs.json"), "w"), indent=1)
