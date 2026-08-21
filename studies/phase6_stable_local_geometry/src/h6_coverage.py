#!/usr/bin/env python3
"""H6 preregistered: exclusive nonstructural subtree coverage as the LAST
tiebreak (before position) in laneD_stmt. Primary vs two mechanism
controls: raw subtree size, direct child count. Metrics: graded KM/R@k
overall and the foundations band 0-10; metamorphic tail Jaccard.
"""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec); sys.argv=["hv"]; spec.loader.exec_module(hv)
P5 = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
LOAD=(0,1,2,7)

def cinfo(c):
    i = hv.name_id.get(c)
    if i is None: return (False, 9, 0, True)
    return (bool(hv.gen[i]), int(hv.depth_stmt[i]), int(hv.depth[i]), bool(hv.nodes["pr"][i]))

def feats(occs, target, stmtmap):
    n = len(occs)
    kids = defaultdict(list); roots = []
    for i,o in enumerate(occs):
        (roots if o[1]==-1 else kids[o[1]]).append(i)
    # postorder subtree sizes: all nodes and substantive-only
    size_all = [1]*n; size_sub = [0]*n
    info = {}
    substantive = [False]*n
    for i,o in enumerate(occs):
        c = o[0]
        if c not in info: info[c] = cinfo(c)
        g, ds, dv, pr = info[c]
        substantive[i] = not (o[2]==4 or g or ds<=1) and o[2]!=6
    orderlist = []
    stack = list(roots)
    while stack:
        i = stack.pop(); orderlist.append(i)
        for j in kids[i]: stack.append(j)
    for i in reversed(orderlist):
        s = 1; ss = 1 if substantive[i] else 0
        for j in kids[i]:
            s += size_all[j]; ss += size_sub[j]
        size_all[i] = s; size_sub[i] = ss
    total_sub = max(sum(1 for i in range(n) if substantive[i]), 1)
    # per-const: union coverage approx = max subtree (occurrence subtrees of
    # the same const rarely overlap; max is a safe lower bound), sizes, kids
    cov, raw, ch = {}, {}, {}
    for i,o in enumerate(occs):
        c = o[0]
        cov[c] = max(cov.get(c,0), size_sub[i])
        raw[c] = max(raw.get(c,0), size_all[i])
        ch[c] = max(ch.get(c,0), len(kids[i]))
    first, tier, load, anyocc = {}, {}, set(), {}
    for i,o in enumerate(occs):
        c,r = o[0],o[2]
        first.setdefault(c,i)
        tier[c]=min(tier.get(c,9),hv.ROLE_TIER.get(r,9)); anyocc[c]=True
        if r in LOAD: load.add(c)
    out={}
    def add(c,dem):
        g, ds, dv, pr = info.get(c) or cinfo(c)
        if g:
            o=hv.owner_of(c)
            if o==target or o==c: return
            _,ods,odv,_ = cinfo(o)
            key,dv2 = o,odv
        else:
            key,dv2 = c,dv
        if key not in out:
            _,kds,_,_ = cinfo(key)
            out[key]=dict(dem=1 if dem else 0, inst=1 if tier[c]==5 else 0,
                          gen=1 if (g and False) else 0, trans=1 if kds<=1 else 0,
                          stmt=1 if stmtmap.get(key) else 0, negd=-dv2,
                          ncov=-cov.get(c,0)/total_sub, nraw=-raw.get(c,0),
                          nch=-ch.get(c,0), first=first[c])
    for c in load: add(c,False)
    for c in anyocc:
        if c in load: continue
        i=hv.name_id.get(c)
        if i is not None and not hv.nodes["pr"][i]: add(c,True)
    return out

KEYS = {
  "laneD_stmt":  ("dem","inst","trans","stmt","negd","first"),
  "+coverage":   ("dem","inst","trans","stmt","negd","ncov","first"),
  "+rawsize":    ("dem","inst","trans","stmt","negd","nraw","first"),
  "+childcnt":   ("dem","inst","trans","stmt","negd","nch","first"),
}
def hit(c,S): return c in S or hv.owner_of(c) in S or any(hv.owner_of(s)==c for s in S)
briefs = json.load(open(P5+"/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5+"/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n,g in rec.get("grades", {}).items(): grades[pid][n].append(int(g))
forest = hv.load_forest(P6+"/data/graded_hier.jsonl")
res={k:{"km":[],"km0":[],"r4":[],"r8":[]} for k in KEYS}
for b in briefs:
    cands=b["candidates"] if isinstance(b["candidates"],list) else eval(b["candidates"])
    cmap={str(c["n"]):c["name"] for c in cands}
    stmtmap={c["name"]:bool(c.get("in_statement")) for c in cands}
    pid,thm,dt=b["id"],b["theorem"],int(b["theorem_depth"])
    occs=forest.get(thm)
    if not occs or pid not in grades: continue
    gmed={cmap[n]:float(np.median(gs)) for n,gs in grades[pid].items() if n in cmap}
    useful={c for c,g in gmed.items() if g>=3}; keys={c for c,g in gmed.items() if g>=4}
    if not useful: continue
    F=feats(occs,thm,stmtmap)
    if not F: continue
    for name,ks in KEYS.items():
        lst=sorted(F,key=lambda c:tuple(F[c][k] for k in ks))
        if keys:
            v=1.0 if hit(lst[0],keys) else 0.0
            res[name]["km"].append(v)
            if dt<=10: res[name]["km0"].append(v)
        res[name]["r4"].append(sum(1 for u in useful if hit(u,set(lst[:4])))/len(useful))
        res[name]["r8"].append(sum(1 for u in useful if hit(u,set(lst[:8])))/len(useful))
print(f"{'variant':12} {'KM@1':>7} {'KM@1 d<=10':>10} {'R@4':>6} {'R@8':>6}")
for name in KEYS:
    r=res[name]
    print(f"{name:12} {np.mean(r['km']):7.4f} {np.mean(r['km0']):10.4f} {np.mean(r['r4']):6.4f} {np.mean(r['r8']):6.4f}")
# metamorphic tail with coverage
man = json.load(open(P6+"/metamorphic/manifest.json"))
vf = hv.load_forest(P6+"/metamorphic/variants_hier.jsonl")
def top4(name, ks):
    occs = vf.get(name)
    if not occs: return None
    F = feats(occs, name, {})
    return sorted(F, key=lambda c: tuple(F[c][k] for k in ks))[:4]
for name in ("laneD_stmt","+coverage"):
    ks = KEYS[name]
    agg=defaultdict(list)
    for g in man["groups"]:
        for a,b2,fam,kind in g["pairs"]:
            ta,tb = top4(a,ks), top4(b2,ks)
            if ta is None or tb is None: continue
            agg[kind].append(len(set(ta)&set(tb))/max(len(set(ta)|set(tb)),1))
    print(f"metamorphic {name:11}: harmless J {np.mean(agg['harmless']):.3f}  control J {np.mean(agg['control']):.3f}")
