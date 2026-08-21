#!/usr/bin/env python3
"""P1 secondary metric: grade-based recall of the four views on the 552
graded proofs. SECONDARY because the grades are contaminated (raters saw
depth/role/in-statement tags and the rubric encoded predictions — see
p0/P0_GRADING_BRIEF_AUDIT.md). Valid use: paired view-vs-view comparison
on identical fixed labels; invalid use: absolute usefulness claims.

Grades: median across raters, per candidate. useful = grade >= 3
(CORE/MAJOR). keymove = grade 4 exists and top-1 visible item has grade 4.
Visible items with no grade count against the budget (conservative for
hierarchy views, which can surface consts outside the graded universe).
"""
import json, glob, os, re
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, ".."))
P5 = os.path.normpath(os.path.join(P6, "..", "phase5_multiscale_navigation"))
BUDGETS = (1, 2, 4, 8)

import importlib.util
spec = importlib.util.spec_from_file_location("hv", os.path.join(HERE, "hier_views.py"))
hv = importlib.util.module_from_spec(spec)
import sys; sys.argv = ["hv"]; spec.loader.exec_module(hv)  # reuse build_views

briefs = json.load(open(os.path.join(P5, "review", "sealed_r1", "briefs.json")))
by_thm = {}
for b in briefs:
    cands = b["candidates"] if isinstance(b["candidates"], list) else eval(b["candidates"])
    by_thm[b["theorem"]] = (b["id"], {str(c["n"]): c["name"] for c in cands},
                            int(b["theorem_depth"]))

grades = defaultdict(lambda: defaultdict(list))   # proof_id -> cand_n -> [g]
for f in glob.glob(os.path.join(P5, "review", "sealed_r1", "grades_*.json")):
    for pid, rec in json.load(open(f)).items():
        for n, g in rec.get("grades", {}).items():
            grades[pid][n].append(int(g))

forest = hv.load_forest(os.path.join(P6, "data", "graded_hier.jsonl"))

agg = defaultdict(list)
n_used = 0
for thm, (pid, cmap, dtar) in by_thm.items():
    occs = forest.get(thm)
    if not occs or pid not in grades:
        continue
    gmed = {cmap[n]: float(np.median(gs)) for n, gs in grades[pid].items()
            if n in cmap}
    useful = {c for c, g in gmed.items() if g >= 3}
    key = {c for c, g in gmed.items() if g >= 4}
    if not useful:
        continue
    v = hv.build_views(occs, dtar, thm)
    n_used += 1
    for vn in ("flat", "owner", "hier", "hier_lanes", "full", "laned"):
        lst = v[vn]
        for k in BUDGETS:
            vis = set(lst[:k])
            agg[(vn, k, "recall")].append(len(vis & useful) / len(useful))
        if key:
            agg[(vn, 1, "keymove")].append(1.0 if lst and lst[0] in key else 0.0)
        vis8 = lst[:8]
        if vis8:
            agg[(vn, 8, "ungraded")].append(
                sum(1 for c in vis8 if c not in gmed) / len(vis8))

out = {"n_proofs": n_used, "summary": {}}
for (vn, k, m), vals in sorted(agg.items()):
    out["summary"][f"{vn}@{k}_{m}"] = round(float(np.mean(vals)), 4)
json.dump(out, open(os.path.join(P6, "data", "graded_views.json"), "w"), indent=1)
print(f"proofs used: {n_used}")
for m, ks in (("recall", BUDGETS), ("keymove", (1,)), ("ungraded", (8,))):
    for k in ks:
        print(f"{m}@{k}: " + "  ".join(
            f"{vn} {out['summary'].get(f'{vn}@{k}_{m}', float('nan')):.3f}"
            for vn in ("flat", "owner", "hier", "hier_lanes", "full", "laned")))
