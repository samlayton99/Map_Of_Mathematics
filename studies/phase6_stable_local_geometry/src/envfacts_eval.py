#!/usr/bin/env python3
"""Do the newly-extracted environment facts predict machinery?

Measured against BOTH blind instruments (120 targets + 48 fresh
definition targets, 3 raters each, tag-free briefs). For every graded
candidate slot we have a consensus grade 0-4; "useful" = median >= 3.

For each new fact we report P(useful | fact) vs P(useful | not fact)
and the slot counts, separately for theorem and definition targets --
the def rules and thm rules were always scoped separately and a fact
that helps one may hurt the other (that has happened twice already).

This is MEASUREMENT, not tuning. Nothing here changes frozen.py.
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
node = {"gen": hv.gen, "depth": hv.depth, "kind": hv.nodes["kind"], "pr": hv.nodes["pr"]}

FACTS = {}
for line in open("/Users/sam/mathmap_data/envfacts.tsv"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 10:
        continue
    FACTS[p[0]] = dict(inst=int(p[1]), red=int(p[2]), simp=int(p[3]),
                       proj=int(p[4]), cls=int(p[5]), rec=int(p[6]),
                       unsafe=int(p[7]), line=int(p[8]), levels=int(p[9]))
print(f"envfacts loaded: {len(FACTS)}")
CLASSPROJ = {n for n, f in FACTS.items() if f["cls"] == 1 and f["proj"] == 1}

rows = []
for tag, sub in (("blind1", "blind"), ("blind2", "blind2")):
    B = os.path.join(P6, "data", sub)
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
    for b in briefs:
        tid, tgt = b["id"], b["target"]
        tkind = b.get("kind", 0) if sub == "blind" else 1
        cmap = {str(c["n"]): c["name"] for c in b["candidates"]}
        cs = per.get(tid, {})
        gmed = {cmap[n]: float(np.median(list(gs.values())))
                for n, gs in cs.items() if n in cmap and len(gs) >= 2}
        occs = forest.get(tgt)
        if not occs or not gmed:
            continue
        F = frozen.candidate_features(
            occs, tgt, node, hv.name_id, hv.owner_of, hv.depth_stmt,
            CLASSPROJ, {o[0] for o in stmtf.get(tgt, [])})
        for name, g in gmed.items():
            f = FACTS.get(name)
            if f is None:
                continue
            ff = F.get(name, {})
            rows.append(dict(corpus=tag, isdef=tkind == 1, name=name,
                             grade=g, useful=g >= 3, key=g >= 4,
                             lane=ff.get("lane"), dem=ff.get("dem"),
                             **{k: f[k] for k in
                                ("inst", "red", "simp", "proj", "cls", "rec")}))
print(f"graded slots joined to envfacts: {len(rows)}")


def report(fact, test, label):
    print(f"\n--- {label}")
    for scope, sel in (("theorem targets", lambda r: not r["isdef"]),
                       ("definition targets", lambda r: r["isdef"]),
                       ("ALL", lambda r: True)):
        rs = [r for r in rows if sel(r)]
        pos = [r for r in rs if test(r)]
        neg = [r for r in rs if not test(r)]
        if len(pos) < 15:
            print(f"  {scope:20s} n={len(pos):4d}  (too few to read)")
            continue
        pu = np.mean([r["useful"] for r in pos])
        nu = np.mean([r["useful"] for r in neg])
        pk = np.mean([r["key"] for r in pos])
        print(f"  {scope:20s} n={len(pos):4d}  P(useful|fact) {pu:.3f}  "
              f"P(useful|not) {nu:.3f}  ratio {pu/max(nu,1e-9):5.2f}x  "
              f"P(key|fact) {pk:.3f}")


report("simp", lambda r: r["simp"] == 1, "@[simp] member of default simp set")
report("red", lambda r: r["red"] == 0, "reducible (abbreviation-like)")
report("irred", lambda r: r["red"] == 2, "irreducible")
report("inst", lambda r: r["inst"] == 1, "registered typeclass instance")
report("rec", lambda r: r["rec"] == 1, "recursive inductive")

# does simp add ON TOP of the existing lane split?
print("\n=== does @[simp] add information the lane rule does not already have? ===")
for scope, sel in (("theorem", lambda r: not r["isdef"]),
                   ("definition", lambda r: r["isdef"])):
    rs = [r for r in rows if sel(r) and r["lane"] is not None]
    for lane in (0, 1, 2):
        sub = [r for r in rs if r["lane"] == lane]
        if len(sub) < 20:
            continue
        s1 = [r for r in sub if r["simp"] == 1]
        s0 = [r for r in sub if r["simp"] == 0]
        if len(s1) < 10 or len(s0) < 10:
            continue
        print(f"  {scope:10s} lane {lane}: simp n={len(s1):4d} useful "
              f"{np.mean([r['useful'] for r in s1]):.3f} | "
              f"non-simp n={len(s0):4d} useful "
              f"{np.mean([r['useful'] for r in s0]):.3f}")

json.dump({"n_rows": len(rows)},
          open(os.path.join(P6, "data", "envfacts_eval.json"), "w"), indent=1)
