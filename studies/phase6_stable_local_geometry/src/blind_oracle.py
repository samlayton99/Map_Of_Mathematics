#!/usr/bin/env python3
"""Oracle decomposition + boundary failure mining on BLIND labels.
This round develops on blind (stated); blind becomes dev after it."""
import json, glob, os, sys
from collections import defaultdict, Counter
import numpy as np, importlib.util
spec2 = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec2); sys.argv=["hv"]; spec2.loader.exec_module(hv)
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
B = os.path.join(P6, "data", "blind")
LOAD=(0,1,2,7); KIND = hv.nodes["kind"]
briefs = json.load(open(os.path.join(B,"briefs.json")))
forest = hv.load_forest(os.path.join(B,"targets_hier.jsonl"))
stmtf = hv.load_forest(os.path.join(B,"targets_stmt_hier.jsonl"))
per = defaultdict(lambda: defaultdict(dict))
for rf in sorted(glob.glob(os.path.join(B,"grades_R*.json"))):
    rid=rf[-6]
    for batch,tgts in json.load(open(rf)).items():
        for tid,cs in tgts.items():
            for n,g in cs.items():
                if g is not None: per[tid][n][rid]=int(g)
def feats(occs, target, stmtnames, tkind):
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
            dv=int(hv.depth[io]) if io is not None else 0; key=o; inst=0
            kk=int(KIND[io]) if io is not None else -1
        else:
            ds=int(hv.depth_stmt[i]) if i is not None else 9
            dv=int(hv.depth[i]) if i is not None else 0
            key=c; inst=1 if tier[c]==5 else 0
            kk=int(KIND[i]) if i is not None else -1
        if key not in out:
            lane=2 if inst else (1 if ds<=1 else 0)
            ctor=1 if (tkind==1 and kk==3) else 0
            out[key]=dict(dem=1 if dem else 0, lane=lane, ctor=ctor, kk=kk,
                          stmt=1 if key in stmtnames else 0, d=dv, first=first[c])
    for c in load: add(c,False)
    for c in anyocc:
        if c in load: continue
        i=hv.name_id.get(c)
        if i is not None and not hv.nodes["pr"][i]: add(c,True)
    return out
def order(F):
    return sorted(F,key=lambda c:(F[c]["dem"],F[c]["lane"],F[c]["ctor"],F[c]["stmt"],-F[c]["d"],F[c]["first"]))
def gap_t(pool,F):
    if not pool: return None
    ds=sorted({F[c]["d"] for c in pool},reverse=True)
    if len(ds)==1: return ds[0]
    gaps=[(ds[i]-ds[i+1],i) for i in range(len(ds)-1)]
    g,i=max(gaps)
    return ds[i] if g>0 else ds[-1]
def f1(inc,useful,gmed):
    gi=[c for c in inc if c in gmed]
    pr=np.mean([gmed[c]>=3 for c in gi]) if gi else 0.0
    rc=sum(1 for u in useful if u in inc)/len(useful)
    return 2*pr*rc/max(pr+rc,1e-9)
S=defaultdict(lambda: defaultdict(list))
fn_loc=Counter(); fp_loc=Counter()
for b in briefs:
    tid,tgt=b["id"],b["target"]
    tkind=b.get("kind",0)
    grp="thm" if tkind==0 else "def"
    cmap={str(c["n"]):c["name"] for c in b["candidates"]}
    cs=per.get(tid,{})
    gmed={cmap[n]:float(np.median(list(gs.values()))) for n,gs in cs.items() if n in cmap and len(gs)>=2}
    useful={c for c,g in gmed.items() if g>=3}
    if not useful: continue
    occs=forest.get(tgt)
    if not occs: continue
    F=feats(occs,tgt,{o[0] for o in stmtf.get(tgt,[])},tkind)
    if not F: continue
    pool=[c for c in F if F[c]["dem"]==0]
    lst=order(F); lst0=[c for c in lst if F[c]["dem"]==0]
    # policies
    t=gap_t(pool,F)
    gap={c for c in pool if t is not None and F[c]["d"]>=t}
    el0={c for c in pool if F[c]["lane"]==0 and F[c]["stmt"]==0}
    un=gap|el0
    for g2 in ("all",grp):
        S[g2]["pol_gap"].append(f1(gap,useful,gmed))
        S[g2]["pol_un"].append(f1(un,useful,gmed))
        # oracles
        S[g2]["o_pool"].append(f1({c for c in pool if c in useful},useful,gmed))
        best=0.0
        for th in sorted({F[c]["d"] for c in pool}):
            best=max(best,f1({c for c in pool if F[c]["d"]>=th},useful,gmed))
        S[g2]["o_depth"].append(best)
        best=0.0
        for k in range(1,len(lst0)+1):
            best=max(best,f1(set(lst0[:k]),useful,gmed))
        S[g2]["o_prefix"].append(best)
    # failure mining vs the union policy
    for u in useful:
        if u in un: continue
        if u not in F: fn_loc[grp+":not_in_universe"]+=1
        elif F[u]["dem"]==1: fn_loc[grp+":u1d_excluded"]+=1
        else: fn_loc[f"{grp}:below_gap_lane{F[u]['lane']}_stmt{F[u]['stmt']}"]+=1
    for c in un:
        if c in gmed and gmed[c]<=1:
            kinds={0:"thm",1:"def",2:"ind",3:"ctor",4:"rec"}
            fp_loc[f"{grp}:lane{F[c]['lane']}_stmt{F[c]['stmt']}_{kinds.get(F[c]['kk'],'?')}"]+=1
print(f"{'group':5} {'gap':>6} {'union':>6} | {'poolOr':>7} {'depthOr':>8} {'prefixOr':>9}  (blind ceiling 0.836)")
for g2 in ("all","thm","def"):
    a=S[g2]
    print(f"{g2:5} {np.mean(a['pol_gap']):6.3f} {np.mean(a['pol_un']):6.3f} | "
          f"{np.mean(a['o_pool']):7.3f} {np.mean(a['o_depth']):8.3f} {np.mean(a['o_prefix']):9.3f}")
print("\nFN (useful missed by union):", dict(fn_loc.most_common(10)))
print("FP (junk included by union):", dict(fp_loc.most_common(10)))
