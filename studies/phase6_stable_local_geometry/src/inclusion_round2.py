#!/usr/bin/env python3
"""Inclusion round 2: oracle ceilings, gap_all failure mining, and the
variant grid the failures dictate. Strict-name metrics throughout.
CAVEAT: grades saw candidate depth (brief contamination); metamorphic
stability is computed for top variants as the uncontaminated check."""
import json, glob, os, sys
from collections import defaultdict, Counter
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
    if not pool: return set()
    ds = sorted({F[c]["d"] for c in pool}, reverse=True)
    if len(ds)==1: return set(pool)
    gaps=[(ds[i]-ds[i+1], i) for i in range(len(ds)-1)]
    g,i=max(gaps)
    if g==0: return set(pool)
    return {c for c in pool if F[c]["d"]>=ds[i]}

def top2gap(pool, F):
    """include down to the deeper of the two largest gaps (2 clusters)"""
    if not pool: return set()
    ds = sorted({F[c]["d"] for c in pool}, reverse=True)
    if len(ds)<=2: return set(pool)
    gaps=sorted([(ds[i]-ds[i+1], i) for i in range(len(ds)-1)], reverse=True)
    if gaps[0][0]==0: return set(pool)
    i = max(gaps[0][1], gaps[1][1]) if len(gaps)>1 and gaps[1][0]>0 else gaps[0][1]
    return {c for c in pool if F[c]["d"]>=ds[i]}

def order(F):
    return sorted(F, key=lambda c:(F[c]["dem"],F[c]["lane"],F[c]["stmt"],-F[c]["d"],F[c]["first"]))

def prefix_gap(F):
    """largest depth drop between consecutive items of the laneD_stmt
    order (dem-0 only); include the prefix"""
    lst=[c for c in order(F) if F[c]["dem"]==0]
    if len(lst)<=1: return set(lst)
    ds=[F[c]["d"] for c in lst]
    drops=[(ds[i]-ds[i+1], i) for i in range(len(ds)-1)]
    g,i=max(drops)
    if g<=0: return set(lst)
    return set(lst[:i+1])

briefs = json.load(open(P5+"/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5+"/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n,g in rec.get("grades", {}).items(): grades[pid][n].append(int(g))
forest = hv.load_forest(P6+"/data/graded_hier.jsonl")

POLS = {
 "gap_all":       lambda F: gap_cut([c for c in F if F[c]["dem"]==0], F),
 "gap_no_infra":  lambda F: {c for c in gap_cut([c for c in F if F[c]["dem"]==0],F) if F[c]["lane"]!=2},
 "gap_no_l12":    lambda F: {c for c in gap_cut([c for c in F if F[c]["dem"]==0],F) if F[c]["lane"]==0},
 "top2gap":       lambda F: top2gap([c for c in F if F[c]["dem"]==0], F),
 "prefix_gap":    lambda F: prefix_gap(F),
 "gap_or_EL0":    lambda F: gap_cut([c for c in F if F[c]["dem"]==0],F) |
                            {c for c in F if F[c]["dem"]==0 and F[c]["lane"]==0 and F[c]["stmt"]==0},
}
S = {p: defaultdict(list) for p in POLS}
S["oracle_depth"]=defaultdict(list); S["oracle_prefix"]=defaultdict(list)
miss_loc = Counter(); junk_loc = Counter(); nprf=0
for b in briefs:
    cands=b["candidates"] if isinstance(b["candidates"],list) else eval(b["candidates"])
    cmap={str(c["n"]):c["name"] for c in cands}
    stmtmap={c["name"]:bool(c.get("in_statement")) for c in cands}
    pid,thm,dt=b["id"],b["theorem"],int(b["theorem_depth"])
    occs=forest.get(thm)
    if not occs or pid not in grades: continue
    gmed={cmap[n]:float(np.median(gs)) for n,gs in grades[pid].items() if n in cmap}
    useful={c for c,g in gmed.items() if g>=3}; junk={c for c,g in gmed.items() if g<=1}
    if not useful: continue
    F=feats(occs,thm,stmtmap)
    if not F: continue
    nprf+=1
    def score(inc):
        gi=[c for c in inc if c in gmed]
        pr=np.mean([gmed[c]>=3 for c in gi]) if gi else 0.0
        jr=np.mean([gmed[c]<=1 for c in gi]) if gi else 0.0
        rc=sum(1 for u in useful if u in inc)/len(useful)
        f1=2*pr*rc/max(pr+rc,1e-9)
        return pr,jr,rc,f1
    for p,fn in POLS.items():
        inc=fn(F)
        pr,jr,rc,f1=score(inc)
        S[p]["prec"].append(pr); S[p]["junk"].append(jr); S[p]["rec"].append(rc)
        S[p]["f1"].append(f1); S[p]["k"].append(len(inc)); S[p]["empty"].append(0.0 if inc else 1.0)
    # oracles
    dem0=[c for c in F if F[c]["dem"]==0]
    best=0.0
    for t in sorted({F[c]["d"] for c in dem0}):
        _,_,_,f1=score({c for c in dem0 if F[c]["d"]>=t})
        best=max(best,f1)
    S["oracle_depth"]["f1"].append(best)
    lst=[c for c in order(F) if F[c]["dem"]==0]
    best=0.0
    for k in range(1,len(lst)+1):
        _,_,_,f1=score(set(lst[:k]))
        best=max(best,f1)
    S["oracle_prefix"]["f1"].append(best)
    # failure mining for gap_all
    inc = POLS["gap_all"](F)
    for u in useful:
        if u in inc: continue
        if u not in F: miss_loc["not_in_universe"]+=1
        elif F[u]["dem"]==1: miss_loc["u1d_demoted"]+=1
        else: miss_loc[f"below_gap_lane{F[u]['lane']}"]+=1
    for c in inc:
        if c in gmed and gmed[c]<=1:
            junk_loc[f"lane{F[c]['lane']}_stmt{F[c]['stmt']}"]+=1
print(f"proofs {nprf}\n{'policy':13} {'prec':>6} {'junk':>6} {'rec':>6} {'F1':>6} {'medK':>5} {'empty':>6}")
for p in POLS:
    a=S[p]
    print(f"{p:13} {np.mean(a['prec']):6.3f} {np.mean(a['junk']):6.3f} {np.mean(a['rec']):6.3f} "
          f"{np.mean(a['f1']):6.3f} {np.median(a['k']):5.0f} {np.mean(a['empty']):6.3f}")
print(f"\nORACLE ceilings (best per-proof cut): depth-threshold F1 {np.mean(S['oracle_depth']['f1']):.3f}   "
      f"order-prefix F1 {np.mean(S['oracle_prefix']['f1']):.3f}")
print("\ngap_all missed-useful locations:", dict(miss_loc.most_common()))
print("gap_all included-junk classes:", dict(junk_loc.most_common()))
json.dump({p:{m:float(np.mean(v)) for m,v in a.items()} for p,a in S.items()},
          open(P6+"/data/inclusion_round2.json","w"), indent=1)
