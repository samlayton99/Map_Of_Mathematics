#!/usr/bin/env python3
"""Transparent semantic frontier (GPT point 3, corrected form).

Per occurrence forest: traverse from roots, skipping type-annotation
(role 6) branches. An occurrence is STRUCTURAL if its position is
instance (role 4), its constant is generated, or its constant's
statement-vocabulary depth <= 1 (transport). Otherwise SUBSTANTIVE.
The FRONTIER = substantive occurrences with no substantive proper
ancestor: the first real mathematics on each branch, wrappers and
transport traversed through.

Frontier is a SORT KEY, not a visibility cut (roots-only taught us
that): frank 0 = frontier, 1 = substantive non-frontier, 2 = structural.
Ordering: (dem, frank, stmt, -depth, first). Structural-only proofs
degrade automatically to the old keys (foundational fallback).

Evaluated against BOTH yardsticks:
  A. graded corpus (KM@1, R@4, R@8, owner-equivalent) vs laneD_stmt;
  B. metamorphic benchmark: top-4 Jaccard harmless vs control pairs.
"""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec); sys.argv=["hv"]; spec.loader.exec_module(hv)
P5 = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
LOAD = (0, 1, 2, 7)

def const_info(c):
    i = hv.name_id.get(c)
    if i is None:
        return dict(gen=False, ds=9, dv=0, pr=True)
    return dict(gen=bool(hv.gen[i]), ds=int(hv.depth_stmt[i]),
                dv=int(hv.depth[i]), pr=bool(hv.nodes["pr"][i]))

def frontier_feats(occs, target, stmtmap):
    kids = defaultdict(list)
    roots = []
    for i, o in enumerate(occs):
        (kids[o[1]] if o[1] != -1 else roots).append(i) if o[1] != -1 else roots.append(i)
    # note: append happens twice for parented nodes in the expr above; rebuild cleanly
    kids = defaultdict(list); roots = []
    for i, o in enumerate(occs):
        if o[1] == -1: roots.append(i)
        else: kids[o[1]].append(i)
    info = {}
    frank_occ = {}
    stack = [(i, False) for i in roots if occs[i][2] != 6]
    while stack:
        i, seen_sub = stack.pop()
        o = occs[i]
        c = o[0]
        if c not in info: info[c] = const_info(c)
        ci = info[c]
        structural = (o[2] == 4) or ci["gen"] or ci["ds"] <= 1
        if not structural:
            frank_occ[i] = 1 if seen_sub else 0
            seen_sub = True
        else:
            frank_occ[i] = 2
        for j in kids[i]:
            if occs[j][2] != 6:
                stack.append((j, seen_sub))
    # aggregate per constant with the usual universe / redirect / features
    first, tier, load, anyocc = {}, {}, set(), {}
    for i, o in enumerate(occs):
        c, r = o[0], o[2]
        first.setdefault(c, i)
        tier[c] = min(tier.get(c, 9), hv.ROLE_TIER.get(r, 9))
        anyocc[c] = True
        if r in LOAD: load.add(c)
    frank_const = {}
    for i, fr in frank_occ.items():
        c = occs[i][0]
        frank_const[c] = min(frank_const.get(c, 9), fr)
    out = {}
    def add(c, dem):
        ci = info.get(c) or const_info(c)
        if ci["gen"]:
            o = hv.owner_of(c)
            if o == target or o == c: return
            oi = const_info(o)
            key, dv = o, oi["dv"]
            fr = frank_const.get(c, 2)   # helper's frontier status transfers to owner
            if oi["ds"] > 1 and fr == 2: fr = 1  # substantive owner never worse than 1
        else:
            key, dv = c, ci["dv"]
            fr = frank_const.get(c, 2 if ci["ds"] <= 1 else 1)
        if key not in out or True:
            prev = out.get(key)
            cur = dict(dem=1 if dem else 0, frank=fr,
                       stmt=1 if stmtmap.get(key) else 0, negd=-dv,
                       first=first[c], tier=tier[c])
            if prev is None or (cur["frank"], cur["negd"]) < (prev["frank"], prev["negd"]):
                cur["first"] = min(first[c], prev["first"]) if prev else first[c]
                out[key] = cur
    for c in load: add(c, False)
    for c in anyocc:
        if c in load: continue
        i = hv.name_id.get(c)
        if i is not None and not hv.nodes["pr"][i]: add(c, True)
    return out

def order(F):
    return sorted(F, key=lambda c: (F[c]["dem"], F[c]["frank"], F[c]["stmt"],
                                    F[c]["negd"], F[c]["first"]))
def hit(c, S):
    return c in S or hv.owner_of(c) in S or any(hv.owner_of(s) == c for s in S)

# ---- A. graded corpus
briefs = json.load(open(P5 + "/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5 + "/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n, g in rec.get("grades", {}).items(): grades[pid][n].append(int(g))
forest = hv.load_forest(P6 + "/data/graded_hier.jsonl")
km, r4, r8 = [], [], []
for b in briefs:
    cands = b["candidates"] if isinstance(b["candidates"], list) else eval(b["candidates"])
    cmap = {str(c["n"]): c["name"] for c in cands}
    stmtmap = {c["name"]: bool(c.get("in_statement")) for c in cands}
    pid, thm = b["id"], b["theorem"]
    occs = forest.get(thm)
    if not occs or pid not in grades: continue
    gmed = {cmap[n]: float(np.median(gs)) for n, gs in grades[pid].items() if n in cmap}
    useful = {c for c, g in gmed.items() if g >= 3}; keys = {c for c, g in gmed.items() if g >= 4}
    if not useful: continue
    F = frontier_feats(occs, thm, stmtmap)
    if not F: continue
    lst = order(F)
    if keys: km.append(1.0 if hit(lst[0], keys) else 0.0)
    r4.append(sum(1 for u in useful if hit(u, set(lst[:4]))) / len(useful))
    r8.append(sum(1 for u in useful if hit(u, set(lst[:8]))) / len(useful))
print(f"A. graded:  frontier KM@1 {np.mean(km):.4f}  R@4 {np.mean(r4):.4f}  R@8 {np.mean(r8):.4f}")
print(f"            (laneD_stmt   0.9127        0.8945       0.9591)")

# ---- B. metamorphic
man = json.load(open(P6 + "/metamorphic/manifest.json"))
vf = hv.load_forest(P6 + "/metamorphic/variants_hier.jsonl")
def top4(name):
    occs = vf.get(name)
    if not occs: return None
    F = frontier_feats(occs, name, {})
    return [c for c in order(F)][:4]
res = defaultdict(list)
for g in man["groups"]:
    for a, b2, fam, kind in g["pairs"]:
        ta, tb = top4(a), top4(b2)
        if ta is None or tb is None: continue
        ja = len(set(ta) & set(tb)) / max(len(set(ta) | set(tb)), 1)
        t1 = 1.0 if (ta and tb and ta[0] == tb[0]) else 0.0
        res[kind].append((ja, t1))
        res["fam:" + fam + ":" + kind].append((ja, t1))
for kind in ("harmless", "control"):
    v = res[kind]
    print(f"B. metamorphic {kind:9}: top4 Jaccard {np.mean([x[0] for x in v]):.3f}  "
          f"top-1 agree {np.mean([x[1] for x in v]):.3f}  (n={len(v)})")
print("   (laneD was:  harmless 0.619 / 0.868   control 0.101 / 0.000)")
for k in sorted(res):
    if k.startswith("fam:") and k.endswith("harmless"):
        v = res[k]
        print(f"   {k[4:-9]:28} J {np.mean([x[0] for x in v]):.3f} t1 {np.mean([x[1] for x in v]):.3f} (n={len(v)})")
json.dump({"graded": {"km": float(np.mean(km)), "r4": float(np.mean(r4)), "r8": float(np.mean(r8))},
           "metamorphic": {k: [float(np.mean([x[0] for x in v])), float(np.mean([x[1] for x in v]))]
                           for k, v in res.items() if not k.startswith("fam:")}},
          open(P6 + "/data/frontier_results.json", "w"), indent=1)
