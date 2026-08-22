#!/usr/bin/env python3
"""Score the FROZEN construction on the fresh definition-heavy blind
sample (data/blind2: 48 def targets, 3 raters, drawn AFTER the freeze;
zero of these labels touched any rule). This closes the one stated
freeze debt: the def rule set was a third iteration against blind
(n=36); these labels are its first true test.

Reports: rater ceiling (rater-vs-rest F1), frozen def KM@1, boundary
F1, zoom1 F1, and drop-one for the def rules (no-ctor, no-classproj,
no-U1D-admission) -- confirmation or trim, as promised.
"""
import glob
import json
import os
import sys
from collections import defaultdict
import importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec2 = importlib.util.spec_from_file_location("hv", os.path.join(HERE, "hier_views.py"))
hv = importlib.util.module_from_spec(spec2); sys.argv = ["hv"]; spec2.loader.exec_module(hv)
import frozen

P6 = os.path.normpath(os.path.join(HERE, ".."))
B = os.path.join(P6, "data", "blind2")
node = {"gen": hv.gen, "depth": hv.depth, "kind": hv.nodes["kind"], "pr": hv.nodes["pr"]}
CLASSPROJ = set()
for line in open("/Users/sam/mathmap_data/projflags.tsv"):
    n, isp, iscls = line.rstrip("\n").split("\t")
    if int(iscls) == 1:
        CLASSPROJ.add(n)

briefs = json.load(open(os.path.join(B, "briefs.json")))
forest = hv.load_forest(os.path.join(B, "targets_hier.jsonl"))
stmtf = hv.load_forest(os.path.join(B, "targets_stmt_hier.jsonl"))
per = defaultdict(lambda: defaultdict(dict))
for rf in sorted(glob.glob(os.path.join(B, "grades_R*.json"))):
    rid = rf[-6]
    for batch, tgts in json.load(open(rf)).items():
        for tid, cs in tgts.items():
            for n, g in cs.items():
                if g is not None:
                    per[tid][n][rid] = int(g)

def f1(pred, truth, universe):
    tp = len(pred & truth)
    p = tp / len(pred) if pred else (1.0 if not truth else 0.0)
    r = tp / len(truth) if truth else 1.0
    return 2 * p * r / (p + r) if p + r else 0.0

# ---- 1. rater ceiling on useful (>=3), defs
ceil = []
for tid, cs in per.items():
    raters = sorted({r for gs in cs.values() for r in gs})
    for r in raters:
        mine, rest = set(), set()
        universe = set(cs)
        for n, gs in cs.items():
            if gs.get(r, 0) >= 3:
                mine.add(n)
            others = [g for rr, g in gs.items() if rr != r]
            if others and float(np.median(others)) >= 3:
                rest.add(n)
        ceil.append(f1(mine, rest, universe))
print(f"rater-vs-rest ceiling (fresh defs, n={len(per)} targets): "
      f"{np.mean(ceil):.3f}")

# ---- 2/3/4. frozen policy vs consensus
def evaluate(no_ctor=False, no_cp=False, no_u1d=False, label=""):
    km, bf1, zf1 = [], [], []
    for b in briefs:
        tid, tgt = b["id"], b["target"]
        cmap = {str(c["n"]): c["name"] for c in b["candidates"]}
        cs = per.get(tid, {})
        gmed = {cmap[n]: float(np.median(list(gs.values())))
                for n, gs in cs.items() if n in cmap and len(gs) >= 2}
        useful = {c for c, g in gmed.items() if g >= 3}
        keys = {c for c, g in gmed.items() if g >= 4}
        occs = forest.get(tgt)
        if not occs:
            continue
        F = frozen.candidate_features(
            occs, tgt, node, hv.name_id, hv.owner_of, hv.depth_stmt,
            set() if no_cp else CLASSPROJ,
            {o[0] for o in stmtf.get(tgt, [])})
        if not F:
            continue
        if no_ctor:
            for c in F:
                F[c]["ctor"] = 0
        lst = frozen.order(F, True)
        if keys:
            km.append(1.0 if lst[0] in keys else 0.0)
        graded_universe = set(gmed)
        if no_u1d:
            t = frozen.gap_threshold(F)
            inc = {c for c in F if F[c]["dem"] == 0 and t is not None
                   and F[c]["d"] >= t}
            lane_side = {c for c in F if F[c]["dem"] == 0
                         and F[c]["lane"] == 0 and F[c]["stmt"] == 0
                         and not (F[c]["ctor"] or F[c]["cp"])}
            bd = inc | lane_side
        else:
            bd = frozen.boundary(F, True)
        z = frozen.zoom1(F, True)
        bf1.append(f1(bd & graded_universe, useful, graded_universe))
        zf1.append(f1(z & graded_universe, useful, graded_universe))
    print(f"{label:16s} KM@1 {np.mean(km):.3f} (n={len(km)})  "
          f"boundary F1 {np.mean(bf1):.3f}  zoom1 F1 {np.mean(zf1):.3f}")
    return {"km": float(np.mean(km)), "n_km": len(km),
            "boundary_f1": float(np.mean(bf1)), "zoom1_f1": float(np.mean(zf1))}

res = {"ceiling": float(np.mean(ceil))}
res["frozen"] = evaluate(label="FROZEN")
res["no_ctor"] = evaluate(no_ctor=True, label="drop ctor")
res["no_classproj"] = evaluate(no_cp=True, label="drop classproj")
res["no_u1d_admit"] = evaluate(no_u1d=True, label="drop U1D admit")

# random baseline on boundary F1: expected F1 of random subset same size
rng = np.random.default_rng(0)
rf = []
for b in briefs:
    tid = b["id"]
    cs = per.get(tid, {})
    cmap = {str(c["n"]): c["name"] for c in b["candidates"]}
    gmed = {cmap[n]: float(np.median(list(gs.values())))
            for n, gs in cs.items() if n in cmap and len(gs) >= 2}
    useful = {c for c, g in gmed.items() if g >= 3}
    universe = sorted(gmed)
    if not universe:
        continue
    for _ in range(20):
        k = rng.integers(1, len(universe) + 1)
        pred = set(rng.choice(universe, k, replace=False))
        rf.append(f1(pred, useful, set(universe)))
res["random_boundary_f1"] = float(np.mean(rf))
print(f"random boundary F1: {np.mean(rf):.3f}")
json.dump(res, open(os.path.join(B, "eval.json"), "w"), indent=1)
