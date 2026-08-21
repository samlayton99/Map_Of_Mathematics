#!/usr/bin/env python3
"""Interface-vocabulary mechanism: in THEOREM proofs, a citation that
produces data (cited const not proof-valued: pr=False) is term
construction, not a reasoning move. Target-relative: definition targets
unaffected (construction IS their move). Kernel facts only (pr flag).

Lane orders tested (theorem targets):
  base:    0 move | 1 transport(ds<=1) | 2 infra          (laneD_stmt)
  vocabB:  0 proof-move(pr, ds>1) | 1 transport | 2 data/pred vocab | 3 infra
  vocabA:  0 proof-move | 1 data/pred vocab | 2 transport | 3 infra
Keys: (dem, lane, stmt, -depth, first). Yardsticks: grades + metamorphic.
"""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec); sys.argv=["hv"]; spec.loader.exec_module(hv)
P5 = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
LOAD=(0,1,2,7)
PR = hv.nodes["pr"]

def feats(occs, target, stmtmap):
    first, tier, load, anyocc = {}, {}, set(), {}
    for i,o in enumerate(occs):
        c,r = o[0],o[2]
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
            pr=bool(PR[io]) if io is not None else True
            key=o; inst=0
        else:
            ds=int(hv.depth_stmt[i]) if i is not None else 9
            dv=int(hv.depth[i]) if i is not None else 0
            pr=bool(PR[i]) if i is not None else True
            key=c; inst=1 if tier[c]==5 else 0
        if key not in out:
            trans=1 if ds<=1 else 0
            vocab=1 if (not pr and not trans and not inst) else 0
            laneB = 3 if inst else (2 if vocab else (1 if trans else 0))
            laneA = 3 if inst else (2 if trans else (1 if vocab else 0))
            base  = 2 if inst else (1 if trans else 0)
            out[key]=dict(dem=1 if dem else 0, base=base, laneB=laneB, laneA=laneA,
                          stmt=1 if stmtmap.get(key) else 0, negd=-dv, first=first[c])
    for c in load: add(c,False)
    for c in anyocc:
        if c in load: continue
        i=hv.name_id.get(c)
        if i is not None and not hv.nodes["pr"][i]: add(c,True)
    return out

KEYS = {"laneD_stmt": "base", "vocabB": "laneB", "vocabA": "laneA"}
def hit(c,S): return c in S or hv.owner_of(c) in S or any(hv.owner_of(s)==c for s in S)
briefs = json.load(open(P5+"/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5+"/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n,g in rec.get("grades", {}).items(): grades[pid][n].append(int(g))
forest = hv.load_forest(P6+"/data/graded_hier.jsonl")
res={k:{"km":[],"r4":[],"r8":[]} for k in KEYS}
flags={k:{} for k in KEYS}
for b in briefs:
    cands=b["candidates"] if isinstance(b["candidates"],list) else eval(b["candidates"])
    cmap={str(c["n"]):c["name"] for c in cands}
    stmtmap={c["name"]:bool(c.get("in_statement")) for c in cands}
    pid,thm=b["id"],b["theorem"]
    occs=forest.get(thm)
    if not occs or pid not in grades: continue
    gmed={cmap[n]:float(np.median(gs)) for n,gs in grades[pid].items() if n in cmap}
    useful={c for c,g in gmed.items() if g>=3}; keyset={c for c,g in gmed.items() if g>=4}
    if not useful: continue
    F=feats(occs,thm,stmtmap)
    if not F: continue
    for name,lk in KEYS.items():
        lst=sorted(F,key=lambda c:(F[c]["dem"],F[c][lk],F[c]["stmt"],F[c]["negd"],F[c]["first"]))
        if keyset:
            v=1.0 if hit(lst[0],keyset) else 0.0
            res[name]["km"].append(v); flags[name][pid]=v
        res[name]["r4"].append(sum(1 for u in useful if hit(u,set(lst[:4])))/len(useful))
        res[name]["r8"].append(sum(1 for u in useful if hit(u,set(lst[:8])))/len(useful))
print(f"{'variant':11} {'KM@1':>7} {'R@4':>6} {'R@8':>6}")
for name in KEYS:
    r=res[name]
    print(f"{name:11} {np.mean(r['km']):7.4f} {np.mean(r['r4']):6.4f} {np.mean(r['r8']):6.4f}")
from scipy.stats import binomtest
for name in ("vocabB","vocabA"):
    b01=sum(1 for p in flags["laneD_stmt"] if flags["laneD_stmt"][p]==1 and flags[name].get(p)==0)
    b10=sum(1 for p in flags["laneD_stmt"] if flags["laneD_stmt"][p]==0 and flags[name].get(p)==1)
    p=binomtest(min(b01,b10),b01+b10).pvalue if b01+b10 else 1.0
    print(f"  {name} vs laneD_stmt: +{b10}/-{b01} p={p:.3g}")
# metamorphic
man = json.load(open(P6+"/metamorphic/manifest.json"))
vf = hv.load_forest(P6+"/metamorphic/variants_hier.jsonl")
for name,lk in KEYS.items():
    agg=defaultdict(lambda: [[],[]])
    for g in man["groups"]:
        for a,b2,fam,kind in g["pairs"]:
            oa,ob = vf.get(a), vf.get(b2)
            if not oa or not ob: continue
            Fa,Fb = feats(oa,a,{}), feats(ob,b2,{})
            la=sorted(Fa,key=lambda c:(Fa[c]["dem"],Fa[c][lk],Fa[c]["stmt"],Fa[c]["negd"],Fa[c]["first"]))[:4]
            lb=sorted(Fb,key=lambda c:(Fb[c]["dem"],Fb[c][lk],Fb[c]["stmt"],Fb[c]["negd"],Fb[c]["first"]))[:4]
            agg[kind][0].append(len(set(la)&set(lb))/max(len(set(la)|set(lb)),1))
            agg[kind][1].append(1.0 if (la and lb and la[0]==lb[0]) else 0.0)
    print(f"meta {name:11}: harmless J {np.mean(agg['harmless'][0]):.3f} t1 {np.mean(agg['harmless'][1]):.3f}"
          f" | control J {np.mean(agg['control'][0]):.3f} t1 {np.mean(agg['control'][1]):.3f}")
