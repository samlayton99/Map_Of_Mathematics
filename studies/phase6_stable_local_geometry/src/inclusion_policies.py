#!/usr/bin/env python3
"""Inclusion-policy study: per-proof boundary between mathematics and
relative plumbing. All policies LOCAL (only this proof's candidates) and
constant-free unless stated. Evaluated as set classifiers against grades:
useful = g>=3, junk = g<=1. Owner-equivalent matching.
"""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec); sys.argv=["hv"]; spec.loader.exec_module(hv)
P5 = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
LOAD=(0,1,2,7)

def feats(occs, target, stmtmap):
    first, tier, load, anyocc = {}, {}, set(), {}
    for i,o in enumerate(occs):
        c,r=o[0],o[2]
        first.setdefault(c,i)
        tier[c]=min(tier.get(c,9),hv.ROLE_TIER.get(r,9)); anyocc[c]=True
        if r in LOAD: load.add(c)
    out={}
    def add(c,dem):
        i=hv.name_id.get(c)
        if i is not None and hv.gen[i]:
            o=hv.owner_of(c)
            if o==target or o==c: return
            io=hv.name_id.get(o)
            ds=int(hv.depth_stmt[io]) if io is not None else 9
            dv=int(hv.depth[io]) if io is not None else 0
            key=o; inst=0
        else:
            ds=int(hv.depth_stmt[i]) if i is not None else 9
            dv=int(hv.depth[i]) if i is not None else 0
            key=c; inst=1 if tier[c]==5 else 0
        if key not in out:
            lane = 2 if inst else (1 if ds<=1 else 0)
            out[key]=dict(dem=1 if dem else 0, lane=lane,
                          stmt=1 if stmtmap.get(key) else 0, d=dv, first=first[c])
    for c in load: add(c,False)
    for c in anyocc:
        if c in load: continue
        i=hv.name_id.get(c)
        if i is not None and not hv.nodes["pr"][i]: add(c,True)
    return out

def gap_cut(pool, F):
    """include everything above the largest cited-depth gap in this pool"""
    if not pool: return set()
    ds = sorted({F[c]["d"] for c in pool}, reverse=True)
    if len(ds) == 1: return set(pool)
    gaps = [(ds[i]-ds[i+1], i) for i in range(len(ds)-1)]
    g, i = max(gaps)
    if g == 0: return set(pool)
    thresh = ds[i]
    return {c for c in pool if F[c]["d"] >= thresh}

def order(F):
    return sorted(F, key=lambda c:(F[c]["dem"],F[c]["lane"],F[c]["stmt"],-F[c]["d"],F[c]["first"]))

POLICIES = {}
POLICIES["top2"]   = lambda F: set(order(F)[:2])
POLICIES["top4"]   = lambda F: set(order(F)[:4])
POLICIES["top8"]   = lambda F: set(order(F)[:8])
POLICIES["EL0"]    = lambda F: {c for c in F if F[c]["dem"]==0 and F[c]["lane"]==0 and F[c]["stmt"]==0}
POLICIES["lane0"]  = lambda F: {c for c in F if F[c]["dem"]==0 and F[c]["lane"]==0}
POLICIES["gap_all"]   = lambda F: gap_cut([c for c in F if F[c]["dem"]==0], F)
POLICIES["gap_lane0"] = lambda F: gap_cut([c for c in F if F[c]["dem"]==0 and F[c]["lane"]==0], F)
POLICIES["gap_EL0"]   = lambda F: gap_cut([c for c in F if F[c]["dem"]==0 and F[c]["lane"]==0 and F[c]["stmt"]==0], F)
POLICIES["ratio_half"]= lambda F,: set()  # placeholder replaced below
def ratio_half(F, dt):
    return {c for c in F if F[c]["dem"]==0 and F[c]["d"]*2 > dt}
def med_rel(F, dt):
    pool=[c for c in F if F[c]["dem"]==0]
    if not pool: return set()
    m=np.median([F[c]["d"] for c in pool])
    return {c for c in pool if F[c]["d"] >= m}
def hit(c,S): return c in S or hv.owner_of(c) in S or any(hv.owner_of(s)==c for s in S)

briefs = json.load(open(P5+"/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5+"/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n,g in rec.get("grades", {}).items(): grades[pid][n].append(int(g))
forest = hv.load_forest(P6+"/data/graded_hier.jsonl")
names = list(POLICIES) + ["ratio_half","med_rel"]
agg = {p: defaultdict(list) for p in names}
for b in briefs:
    cands=b["candidates"] if isinstance(b["candidates"],list) else eval(b["candidates"])
    cmap={str(c["n"]):c["name"] for c in cands}
    stmtmap={c["name"]:bool(c.get("in_statement")) for c in cands}
    pid,thm,dt=b["id"],b["theorem"],int(b["theorem_depth"])
    occs=forest.get(thm)
    if not occs or pid not in grades: continue
    gmed={cmap[n]:float(np.median(gs)) for n,gs in grades[pid].items() if n in cmap}
    useful={c for c,g in gmed.items() if g>=3}; junk={c for c,g in gmed.items() if g<=1}
    core={c for c,g in gmed.items() if g>=4}
    if not useful: continue
    F=feats(occs,thm,stmtmap)
    if not F: continue
    for p in names:
        if p=="ratio_half": inc=ratio_half(F,dt)
        elif p=="med_rel": inc=med_rel(F,dt)
        else: inc=POLICIES[p](F)
        tp=sum(1 for u in useful if hit(u,inc))
        ji=sum(1 for c in inc if hit(c,junk))
        agg[p]["prec"].append(tp/max(len(inc),1) if inc else 0.0)
        agg[p]["rec"].append(tp/len(useful))
        agg[p]["junk_in"].append(ji/max(len(inc),1) if inc else 0.0)
        clean = (not core or all(hit(u,inc) for u in core)) and ji==0 and len(inc)>0
        agg[p]["clean"].append(1.0 if clean else 0.0)
        agg[p]["k"].append(len(inc))
        agg[p]["empty"].append(1.0 if not inc else 0.0)
print(f"{'policy':11} {'prec':>6} {'rec':>6} {'F1':>6} {'junkIn':>7} {'clean':>6} {'medK':>5} {'empty':>6}")
for p in names:
    a=agg[p]
    pr,re=np.mean(a["prec"]),np.mean(a["rec"])
    f1=2*pr*re/max(pr+re,1e-9)
    print(f"{p:11} {pr:6.3f} {re:6.3f} {f1:6.3f} {np.mean(a['junk_in']):7.3f} "
          f"{np.mean(a['clean']):6.3f} {np.median(a['k']):5.0f} {np.mean(a['empty']):6.3f}")
json.dump({p:{m:float(np.mean(v)) for m,v in a.items()} for p,a in agg.items()},
          open(P6+"/data/inclusion_policies.json","w"), indent=1)
