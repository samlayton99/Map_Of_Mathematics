#!/usr/bin/env python3
"""Round 2 grid from failure mining. Changes vs synth_orders.py:
- METRIC owner-equivalence: top-1 counts as a key hit if it is the
  owner of a graded key (or vice versa) — removes the redirect artifact.
- stmt key: proof-introduced before statement vocabulary (old rule).
- ds key: statement-vocabulary depth as the specialization key (fixes
  the projection defect of value depth), value depth as tiebreak.
CAVEAT: this grid iterates on the same labels as round 1 — the winner
needs fresh validation before promotion.
"""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec); sys.argv = ["hv"]; spec.loader.exec_module(hv)
P5 = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
LOAD = (0, 1, 2, 7)

briefs = json.load(open(P5 + "/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5 + "/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n, g in rec.get("grades", {}).items():
            grades[pid][n].append(int(g))
forest = hv.load_forest(P6 + "/data/graded_hier.jsonl")

def feats(occs, target, stmtmap):
    first, tier, nest, load = {}, {}, {}, set()
    anyocc = {}
    for i, o in enumerate(occs):
        c, r = o[0], o[2]
        first.setdefault(c, i)
        tier[c] = min(tier.get(c, 9), hv.ROLE_TIER.get(r, 9))
        anyocc[c] = True
        if r in LOAD:
            load.add(c)
    out = {}
    def add(c, demoted):
        i = hv.name_id.get(c)
        if i is not None and hv.gen[i]:
            o = hv.owner_of(c)
            if o == target or o == c:
                return
            io = hv.name_id.get(o)
            lane = 0 if (io is not None and hv.depth_stmt[io] > 1) else 1
            dv = int(hv.depth[io]) if io is not None else 0
            ds = int(hv.depth_stmt[io]) if io is not None else 0
            key = o
        else:
            lane = 2 if tier[c] == 5 else (1 if (i is not None and hv.depth_stmt[i] <= 1) else 0)
            dv = int(hv.depth[i]) if i is not None else 0
            ds = int(hv.depth_stmt[i]) if i is not None else 0
            key = c
        if key not in out:
            out[key] = dict(lane=lane, negd=-dv, negs=-ds, tier=tier[c],
                            first=first[c], stmt=1 if stmtmap.get(key) else 0,
                            dem=1 if demoted else 0)
    for c in load:
        add(c, False)
    # U1D expansion: non-Prop declarations (data/defs) cited only via
    # implicit/annotation roles enter DEMOTED (dem key sorts them after)
    for c in anyocc:
        if c in load:
            continue
        i = hv.name_id.get(c)
        if i is not None and not hv.nodes["pr"][i]:
            add(c, True)
    return out

ORDERS = {
    "laneD":       ("lane", "negd", "tier", "first"),
    "laneD_stmt":  ("lane", "stmt", "negd", "tier", "first"),
    "laneS":       ("lane", "negs", "tier", "first"),
    "laneSD":      ("lane", "negs", "negd", "tier", "first"),
    "laneSD_stmt": ("lane", "stmt", "negs", "negd", "tier", "first"),
    "laneDS_stmt": ("lane", "stmt", "negd", "negs", "tier", "first"),
}
USE_DEM = True   # U1D items always sort after via dem as second key
res = {k: {"km": [], "r4": [], "r8": []} for k in ORDERS}
km_flags = {k: [] for k in ORDERS}
for b in briefs:
    cands = b["candidates"] if isinstance(b["candidates"], list) else eval(b["candidates"])
    cmap = {str(c["n"]): c["name"] for c in cands}
    stmtmap = {c["name"]: bool(c.get("in_statement")) for c in cands}
    pid, thm = b["id"], b["theorem"]
    occs = forest.get(thm)
    if not occs or pid not in grades:
        continue
    gmed = {cmap[n]: float(np.median(gs)) for n, gs in grades[pid].items() if n in cmap}
    useful = {c for c, g in gmed.items() if g >= 3}
    keys = {c for c, g in gmed.items() if g >= 4}
    if not useful:
        continue
    F = feats(occs, thm, stmtmap)
    if not F:
        continue
    # owner-equivalence closure for scoring
    def hit(c, S):
        return c in S or hv.owner_of(c) in S or any(hv.owner_of(s) == c for s in S)
    for name, ks in ORDERS.items():
        keyf = (lambda c, ks=ks: tuple([F[c]["dem"]] + [F[c][k] for k in ks])) if USE_DEM \
               else (lambda c, ks=ks: tuple(F[c][k] for k in ks))
        lst = sorted(F, key=keyf)
        if keys:
            res[name]["km"].append(1.0 if hit(lst[0], keys) else 0.0)
            km_flags[name].append((pid, res[name]["km"][-1]))
        res[name]["r4"].append(sum(1 for u in useful if hit(u, set(lst[:4]))) / len(useful))
        res[name]["r8"].append(sum(1 for u in useful if hit(u, set(lst[:8]))) / len(useful))
print(f"{'order':12} {'KeyMove@1':>9} {'R@4':>6} {'R@8':>6}   (n_km={len(res['laneD']['km'])})")
for name in ORDERS:
    r = res[name]
    print(f"{name:12} {np.mean(r['km']):9.4f} {np.mean(r['r4']):6.4f} {np.mean(r['r8']):6.4f}")
# paired McNemar best vs laneD
import itertools
base = dict(km_flags["laneD"])
for name in ORDERS:
    if name == "laneD": continue
    cur = dict(km_flags[name])
    b01 = sum(1 for p in base if base[p] == 1 and cur.get(p) == 0)
    b10 = sum(1 for p in base if base[p] == 0 and cur.get(p) == 1)
    print(f"  {name:12} vs laneD flips +{b10}/-{b01}")
