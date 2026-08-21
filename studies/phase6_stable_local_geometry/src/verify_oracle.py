#!/usr/bin/env python3
"""Independent verification + decomposition of the inclusion oracle
ceiling. Reimplements the oracles from scratch (no shared code with
inclusion_round2 beyond feats), adds the POOL oracle (perfect subset of
the pool) to separate pool-loss from ordering-loss, prints the
per-proof distribution and concrete interleaving examples."""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec2 = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec2); sys.argv=["hv"]; spec2.loader.exec_module(hv)
P5 = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
LOAD=(0,1,2,7)
def feats(occs, target, stmtmap):
    first, tier, load, anyocc, mult = {}, {}, set(), {}, defaultdict(int)
    for i,o in enumerate(occs):
        c,r=o[0],o[2]
        first.setdefault(c,i)
        tier[c]=min(tier.get(c,9),hv.ROLE_TIER.get(r,9)); anyocc[c]=True
        mult[c]+=1
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
            key=o; inst=0; pr=bool(hv.nodes["pr"][io]) if io is not None else True
            ar=int(hv.nodes["ar"][io]) if io is not None else 0
        else:
            ds=int(hv.depth_stmt[i]) if i is not None else 9
            dv=int(hv.depth[i]) if i is not None else 0
            key=c; inst=1 if tier[c]==5 else 0
            pr=bool(hv.nodes["pr"][i]) if i is not None else True
            ar=int(hv.nodes["ar"][i]) if i is not None else 0
        if key not in out:
            lane = 2 if inst else (1 if ds<=1 else 0)
            out[key]=dict(dem=1 if dem else 0, lane=lane, ds=ds, pr=pr, ar=ar,
                          stmt=1 if stmtmap.get(key) else 0, d=dv,
                          first=first[c], mult=mult[c])
    for c in load: add(c,False)
    for c in anyocc:
        if c in load: continue
        i=hv.name_id.get(c)
        if i is not None and not hv.nodes["pr"][i]: add(c,True)
    return out
def f1(inc, useful, gmed):
    gi=[c for c in inc if c in gmed]
    pr=np.mean([gmed[c]>=3 for c in gi]) if gi else 0.0
    rc=sum(1 for u in useful if u in inc)/len(useful)
    return 2*pr*rc/max(pr+rc,1e-9)
briefs = json.load(open(P5+"/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5+"/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n,g in rec.get("grades", {}).items(): grades[pid][n].append(int(g))
forest = hv.load_forest(P6+"/data/graded_hier.jsonl")
od, op, opool = [], [], []
perfect_prefix = 0; nprf = 0
examples = []
for b in briefs:
    cands=b["candidates"] if isinstance(b["candidates"],list) else eval(b["candidates"])
    cmap={str(c["n"]):c["name"] for c in cands}
    stmtmap={c["name"]:bool(c.get("in_statement")) for c in cands}
    pid,thm=b["id"],b["theorem"]
    occs=forest.get(thm)
    if not occs or pid not in grades: continue
    gmed={cmap[n]:float(np.median(gs)) for n,gs in grades[pid].items() if n in cmap}
    useful={c for c,g in gmed.items() if g>=3}
    if not useful: continue
    F=feats(occs,thm,stmtmap)
    if not F: continue
    nprf+=1
    pool=[c for c in F if F[c]["dem"]==0]
    # pool oracle: include exactly useful-in-pool
    opool.append(f1({c for c in pool if c in useful}, useful, gmed))
    # depth oracle
    best=0.0
    for t in sorted({F[c]["d"] for c in pool}):
        best=max(best, f1({c for c in pool if F[c]["d"]>=t}, useful, gmed))
    od.append(best)
    # prefix oracle over laneD_stmt order
    lst=sorted(pool, key=lambda c:(F[c]["lane"],F[c]["stmt"],-F[c]["d"],F[c]["first"]))
    best=0.0
    for k in range(1,len(lst)+1):
        best=max(best, f1(set(lst[:k]), useful, gmed))
    op.append(best)
    if best>=0.999: perfect_prefix+=1
    elif best<0.75 and len(examples)<3 and len(lst)<=9:
        examples.append((thm,[(c, gmed.get(c,'-'), F[c]["lane"], F[c]["stmt"], F[c]["d"]) for c in lst]))
print(f"proofs {nprf}")
print(f"POOL oracle (perfect subset of pool): F1 {np.mean(opool):.4f}")
print(f"depth-threshold oracle:               F1 {np.mean(od):.4f}")
print(f"order-prefix oracle:                  F1 {np.mean(op):.4f}")
print(f"prefix oracle achieves 1.0 on {perfect_prefix}/{nprf} = {perfect_prefix/nprf:.1%} of proofs")
print(f"\ndecomposition of (1 - 0.83): pool loss {1-np.mean(opool):.3f}, "
      f"ordering interleaving loss {np.mean(opool)-np.mean(op):.3f}")
print("\nconcrete interleaved proofs (order shown top-to-bottom: name [grade|lane|stmt|depth]):")
for thm, lst in examples:
    print(f"  {thm}")
    for c,g,l,s,d in lst:
        print(f"     [{g}|L{l}|s{s}|d{d}] {c}")
