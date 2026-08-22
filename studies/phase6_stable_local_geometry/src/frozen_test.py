#!/usr/bin/env python3
"""Regression + equivalence harness for the canonical frozen.py.
1. Reproduce headline numbers from frozen.py's own code paths:
   blind thm KM ~0.894, blind def KM ~0.903, old-corpus thm KM ~0.9127.
2. Production equivalence: frozen.zoom1 vs edges_GAP.npz on 300 random
   artifacts from the 20k occurrence sample.
Exits nonzero on any failure."""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec2 = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec2); sys.argv = ["hv"]; spec2.loader.exec_module(hv)
import frozen
P5 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
node = {"gen": hv.gen, "depth": hv.depth, "kind": hv.nodes["kind"], "pr": hv.nodes["pr"]}
CLASSPROJ = set()
for line in open('/Users/sam/mathmap_data/projflags.tsv'):
    n, isp, iscls = line.rstrip('\n').split('\t')
    if int(iscls) == 1: CLASSPROJ.add(n)
fails = []

def check(name, got, expect, tol):
    ok = abs(got - expect) <= tol
    print(f"  {'PASS' if ok else 'FAIL'} {name}: {got:.4f} (expect {expect} +/- {tol})")
    if not ok: fails.append(name)

# --- 1a. blind
B = os.path.join(P6, "data", "blind")
briefs = json.load(open(os.path.join(B, "briefs.json")))
forest = hv.load_forest(os.path.join(B, "targets_hier.jsonl"))
stmtf = hv.load_forest(os.path.join(B, "targets_stmt_hier.jsonl"))
per = defaultdict(lambda: defaultdict(dict))
for rf in sorted(glob.glob(os.path.join(B, "grades_R*.json"))):
    rid = rf[-6]
    for batch, tgts in json.load(open(rf)).items():
        for tid, cs in tgts.items():
            for n, g in cs.items():
                if g is not None: per[tid][n][rid] = int(g)
km = {"thm": [], "def": []}
for b in briefs:
    tid, tgt = b["id"], b["target"]; tkind = b.get("kind", 0)
    cmap = {str(c["n"]): c["name"] for c in b["candidates"]}
    cs = per.get(tid, {})
    gmed = {cmap[n]: float(np.median(list(gs.values()))) for n, gs in cs.items() if n in cmap and len(gs) >= 2}
    keys = {c for c, g in gmed.items() if g >= 4}
    occs = forest.get(tgt)
    if not occs or not keys: continue
    F = frozen.candidate_features(occs, tgt, node, hv.name_id, hv.owner_of,
                                  hv.depth_stmt, CLASSPROJ,
                                  {o[0] for o in stmtf.get(tgt, [])})
    if not F: continue
    lst = frozen.order(F, tkind == 1)
    km["thm" if tkind == 0 else "def"].append(1.0 if lst[0] in keys else 0.0)
check("blind thm KM (frozen.py)", np.mean(km["thm"]), 0.894, 0.005)
check("blind def KM (frozen.py)", np.mean(km["def"]), 0.903, 0.005)

# --- 1b. old corpus (owner-equivalent scoring, stmt from briefs)
ob = json.load(open(P5 + "/review/sealed_r1/briefs.json"))
og = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5 + "/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n, g in rec.get("grades", {}).items(): og[pid][n].append(int(g))
of = hv.load_forest(P6 + "/data/graded_hier.jsonl")
def hit(c, S): return c in S or hv.owner_of(c) in S or any(hv.owner_of(s) == c for s in S)
okm = []
for b in ob:
    cands = b["candidates"] if isinstance(b["candidates"], list) else eval(b["candidates"])
    cmap = {str(c["n"]): c["name"] for c in cands}
    stmtnames = {c["name"] for c in cands if c.get("in_statement")}
    pid, thm = b["id"], b["theorem"]
    occs = of.get(thm)
    if not occs or pid not in og: continue
    gmed = {cmap[n]: float(np.median(gs)) for n, gs in og[pid].items() if n in cmap}
    keys = {c for c, g in gmed.items() if g >= 4}
    if not keys: continue
    F = frozen.candidate_features(occs, thm, node, hv.name_id, hv.owner_of,
                                  hv.depth_stmt, CLASSPROJ, stmtnames)
    if not F: continue
    lst = frozen.order(F, False)
    okm.append(1.0 if hit(lst[0], keys) else 0.0)
check("old thm KM (frozen.py)", np.mean(okm), 0.9127, 0.005)

# --- 2. production equivalence: zoom1 vs edges_GAP on 300 artifacts
z = np.load(P6 + "/data/map_final/edges_GAPC.npz")
gap_by_src = defaultdict(set)
for s, d in zip(z["src_decl"], z["dst_decl"]):
    gap_by_src[int(s)].add(int(d))
rng = np.random.default_rng(1)
rows = []
for line in open(P6 + "/data/map20k_hier.jsonl"):
    r = json.loads(line)
    if r.get("ok"): rows.append(r)
sample = rng.choice(len(rows), 300, replace=False)
mismatch = 0
for i in sample:
    r = rows[i]
    tgt = r["n"]
    ti = hv.name_id.get(tgt)
    if ti is None: continue
    F = frozen.candidate_features(r["occ"], tgt, node, hv.name_id, hv.owner_of,
                                  hv.depth_stmt, CLASSPROJ, set())
    isdef = int(node["kind"][ti]) == 1   # kind 1 = def; rules validated there only
    mine = {hv.name_id[c] for c in frozen.zoom1(F, isdef) if c in hv.name_id}
    prod = gap_by_src.get(int(ti), set())
    if mine != prod:
        mismatch += 1
print(f"  {'PASS' if mismatch == 0 else 'FAIL'} zoom1 vs production edges_GAPC: {mismatch}/300 artifacts mismatch")
if mismatch: fails.append("zoom1-equivalence")
print("\nALL PASS" if not fails else f"FAILURES: {fails}")
sys.exit(0 if not fails else 1)
