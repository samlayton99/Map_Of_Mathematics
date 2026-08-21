#!/usr/bin/env python3
"""Synthesis: the pre-GPT verified components (depth keys, tier merge,
Copeland/Condorcet aggregation) composed with the new substrate (lanes,
nesting). All voters append-safe, all orderings ordinal, no fitted
constants. Paired evaluation on the 522 graded proofs, fixed labels.
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

def feats(occs, target):
    first, tier, nest, load = {}, {}, {}, set()
    for i, o in enumerate(occs):
        c, p, r, lv = o[0], o[1], o[2], o[4]
        first.setdefault(c, i)
        t = hv.ROLE_TIER.get(r, 9)
        tier[c] = min(tier.get(c, 9), t)
        if r in LOAD:
            load.add(c)
            nest[c] = min(nest.get(c, 10**9), lv)
    out = {}
    for c in load:
        i = hv.name_id.get(c)
        if i is not None and hv.gen[i]:
            o = hv.owner_of(c)
            if o == target or o == c:
                continue
            lane = 0 if (o in hv.name_id and hv.depth_stmt[hv.name_id[o]] > 1) else 1
            dc = hv.depth[hv.name_id[o]] if o in hv.name_id else 0
            key = o
        else:
            lane = 2 if tier[c] == 5 else (1 if (i is not None and hv.depth_stmt[i] <= 1) else 0)
            dc = hv.depth[i] if i is not None else 0
            key = c
        if key in out:
            continue
        t3 = 0 if tier[c] <= 2 else (1 if tier[c] <= 4 else 2)
        out[key] = dict(lane=lane, nest=nest.get(c, 10**9), tier=tier[c],
                        t3=t3, negd=-int(dc), first=first[c])
    return out

def copeland(F, voters):
    cs = list(F)
    score = {c: 0 for c in cs}
    for a in cs:
        for b in cs:
            if a >= b:
                continue
            wa = sum(1 for v in voters if F[a][v] < F[b][v])
            wb = sum(1 for v in voters if F[b][v] < F[a][v])
            if wa > wb: score[a] += 1; score[b] -= 1
            elif wb > wa: score[b] += 1; score[a] -= 1
    return score

ORDERS = {
    "laned":      lambda F: sorted(F, key=lambda c: (F[c]["lane"], F[c]["nest"], F[c]["tier"], F[c]["first"])),
    "laneD":      lambda F: sorted(F, key=lambda c: (F[c]["lane"], F[c]["negd"], F[c]["tier"], F[c]["first"])),
    "laneNestD":  lambda F: sorted(F, key=lambda c: (F[c]["lane"], F[c]["nest"], F[c]["negd"], F[c]["first"])),
    "laneDnest":  lambda F: sorted(F, key=lambda c: (F[c]["lane"], F[c]["negd"], F[c]["nest"], F[c]["first"])),
    "laneD3":     lambda F: sorted(F, key=lambda c: (F[c]["lane"], F[c]["negd"], F[c]["t3"], F[c]["first"])),
    "laneT3D":    lambda F: sorted(F, key=lambda c: (F[c]["lane"], F[c]["t3"], F[c]["negd"], F[c]["first"])),
    "flatD":      lambda F: sorted(F, key=lambda c: (F[c]["negd"], F[c]["tier"], F[c]["first"])),
}
def cope_order(F):
    sc = copeland(F, ("lane", "nest", "tier", "negd"))
    return sorted(F, key=lambda c: (-sc[c], F[c]["lane"], F[c]["nest"], F[c]["tier"], F[c]["first"]))
def condorcet_first(F):
    base = ORDERS["laneD"](F)
    cs = list(F)
    for a in cs:
        if all(a == b or sum(1 for v in ("lane","nest","tier","negd") if F[a][v] < F[b][v]) >
               sum(1 for v in ("lane","nest","tier","negd") if F[b][v] < F[a][v]) for b in cs):
            return [a] + [c for c in base if c != a]
    return base
ORDERS["copeland"] = cope_order
ORDERS["condorcet1"] = condorcet_first

res = {k: {"km": [], "r4": [], "r8": []} for k in ORDERS}
km_pair = {k: [] for k in ORDERS}
for b in briefs:
    cands = b["candidates"] if isinstance(b["candidates"], list) else eval(b["candidates"])
    cmap = {str(c["n"]): c["name"] for c in cands}
    pid, thm = b["id"], b["theorem"]
    occs = forest.get(thm)
    if not occs or pid not in grades:
        continue
    gmed = {cmap[n]: float(np.median(gs)) for n, gs in grades[pid].items() if n in cmap}
    useful = {c for c, g in gmed.items() if g >= 3}
    key = {c for c, g in gmed.items() if g >= 4}
    if not useful:
        continue
    F = feats(occs, thm)
    if not F:
        continue
    for name, fn in ORDERS.items():
        lst = fn(F)
        if key:
            res[name]["km"].append(1.0 if lst[0] in key else 0.0)
        res[name]["r4"].append(len(set(lst[:4]) & useful) / len(useful))
        res[name]["r8"].append(len(set(lst[:8]) & useful) / len(useful))

print(f"{'order':12} {'KeyMove@1':>9} {'R@4':>6} {'R@8':>6}   (n={len(res['laned']['km'])})")
for name in ORDERS:
    r = res[name]
    print(f"{name:12} {np.mean(r['km']):9.4f} {np.mean(r['r4']):6.4f} {np.mean(r['r8']):6.4f}")
json.dump({k: {m: float(np.mean(v)) for m, v in r.items()} for k, r in res.items()},
          open(P6 + "/data/synth_orders.json", "w"), indent=1)
