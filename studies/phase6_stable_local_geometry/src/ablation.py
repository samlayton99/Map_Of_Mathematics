#!/usr/bin/env python3
"""Component ablation of the laneD_stmt gain (GPT point 2). Each component
isolated, then the pairs that matter, then full. Fixed owner-equivalent
scoring everywhere. Graded corpus, fixed labels."""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec); sys.argv=["hv"]; spec.loader.exec_module(hv)
P5 = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
LOAD=(0,1,2,7)
briefs = json.load(open(P5+"/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5+"/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n,g in rec.get("grades", {}).items(): grades[pid][n].append(int(g))
forest = hv.load_forest(P6+"/data/graded_hier.jsonl")

def feats(occs, target, stmtmap, redirect, u1d):
    first, tier, nest, load, anyocc = {}, {}, {}, set(), {}
    for i,o in enumerate(occs):
        c,r,lv = o[0],o[2],o[4]
        first.setdefault(c,i)
        tier[c]=min(tier.get(c,9),hv.ROLE_TIER.get(r,9)); anyocc[c]=True
        if r in LOAD:
            load.add(c); nest[c]=min(nest.get(c,10**9),lv)
    out={}
    def add(c,dem):
        i=hv.name_id.get(c)
        if redirect and i is not None and hv.gen[i]:
            o=hv.owner_of(c)
            if o==target or o==c: return
            io=hv.name_id.get(o)
            isg=False; ds=int(hv.depth_stmt[io]) if io is not None else 9
            dv=int(hv.depth[io]) if io is not None else 0; key=o
        else:
            isg=bool(i is not None and hv.gen[i])
            ds=int(hv.depth_stmt[i]) if i is not None else 9
            dv=int(hv.depth[i]) if i is not None else 0; key=c
        if key not in out:
            out[key]=dict(inst=1 if tier[c]==5 else 0, gen=1 if isg else 0,
                          trans=1 if ds<=1 else 0, negd=-dv, tier=tier[c],
                          nest=nest.get(c,10**9), first=first[c],
                          stmt=1 if stmtmap.get(key) else 0, dem=1 if dem else 0)
    for c in load: add(c,False)
    if u1d:
        for c in anyocc:
            if c in load: continue
            i=hv.name_id.get(c)
            if i is not None and not hv.nodes["pr"][i]: add(c,True)
    return out

# each config: (redirect, u1d, key-tuple builder)
def K(*keys): return lambda F,c: tuple(F[c][k] if k[0]!='-' else -F[c][k[1:]] for k in keys)
CFG = {
 "flat":            (False, False, K("tier","first")),
 "+owner_redirect": (True,  False, K("tier","first")),
 "+infra_only":     (False, False, K("inst","gen","tier","first")),
 "+transport_only": (False, False, K("trans","tier","first")),
 "+nesting_only":   (False, False, K("nest","tier","first")),
 "+stmt_only":      (False, False, K("stmt","tier","first")),
 "+depth_only":     (False, False, K("negd","tier","first")),
 "+u1d_only":       (False, True,  K("dem","tier","first")),
 "lanes(inf+tr)":   (True,  False, K("inst","gen","trans","tier","first")),
 "lanes+depth":     (True,  False, K("inst","gen","trans","negd","first")),
 "full_laneD_stmt": (True,  True,  K("dem","inst","gen","trans","stmt","negd","first")),
}
def hit(c,S): return c in S or hv.owner_of(c) in S or any(hv.owner_of(s)==c for s in S)
res={k:{"km":[],"r4":[],"r8":[]} for k in CFG}
for b in briefs:
    cands=b["candidates"] if isinstance(b["candidates"],list) else eval(b["candidates"])
    cmap={str(c["n"]):c["name"] for c in cands}
    stmtmap={c["name"]:bool(c.get("in_statement")) for c in cands}
    pid,thm=b["id"],b["theorem"]
    occs=forest.get(thm)
    if not occs or pid not in grades: continue
    gmed={cmap[n]:float(np.median(gs)) for n,gs in grades[pid].items() if n in cmap}
    useful={c for c,g in gmed.items() if g>=3}; keys={c for c,g in gmed.items() if g>=4}
    if not useful: continue
    cache={}
    for name,(rd,u1,kf) in CFG.items():
        F = cache.get((rd,u1))
        if F is None:
            F = cache[(rd,u1)] = feats(occs,thm,stmtmap,rd,u1)
        if not F: continue
        lst=sorted(F,key=lambda c:kf(F,c))
        if keys: res[name]["km"].append(1.0 if hit(lst[0],keys) else 0.0)
        res[name]["r4"].append(sum(1 for u in useful if hit(u,set(lst[:4])))/len(useful))
        res[name]["r8"].append(sum(1 for u in useful if hit(u,set(lst[:8])))/len(useful))
print(f"{'config':17} {'KM@1':>7} {'R@4':>6} {'R@8':>6}")
for name in CFG:
    r=res[name]
    print(f"{name:17} {np.mean(r['km']):7.4f} {np.mean(r['r4']):6.4f} {np.mean(r['r8']):6.4f}")
json.dump({k:{m:float(np.mean(v)) for m,v in r.items()} for k,r in res.items()},
          open(P6+"/data/ablation.json","w"), indent=1)
