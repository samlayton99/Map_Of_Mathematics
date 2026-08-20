"""Which KINDS of human-written citation are missing from the record?
Directly addresses the recall worry: are we losing theorems, or definitions?"""
import json, os, glob
import numpy as np
from collections import defaultdict, Counter
SC="/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DATA="/Users/sam/my-repos/research/Map_Of_Mathematics/studies/phase5_multiscale_navigation/data"
inc=np.load(DATA+"/incid.npz"); arts=np.load(DATA+"/artifacts.npz")
nodes=np.load(DATA+"/nodes.npz"); v8=np.load(DATA+"/v8_mask.npz")
names=json.load(open(DATA+"/names.json")); idx={n:i for i,n in enumerate(names)}
a=inc["artifact"].astype(np.int64); d=inc["decl"].astype(np.int64)
lb=inc["load_bearing"]; insw=inc["in_stmt_world"]
allrefs_art=defaultdict(set)   # every occurrence, load-bearing or not
lbset=defaultdict(set)
cert=arts["certifies"].astype(np.int64); kind=nodes["kind"]; depth=nodes["depth"]
tgt=cert[a]
for i in range(len(a)):
    allrefs_art[a[i]].add(d[i])
    if lb[i]: lbset[a[i]].add(d[i])
art_of={dd:ai for ai,dd in enumerate(cert)}
prov={}
for f in glob.glob(SC+"/prov/*.json"):
    for e in json.load(open(f))["decls"]:
        if e.get("refs"): prov[e["name"]]=set(e["refs"])
KN={0:"theorem",1:"def",2:"inductive",3:"constructor",4:"recursor",5:"opaque",6:"quot",7:"axiom"}
def grp(k):
    if k==0: return "theorem"
    if k in (1,2,5,6,7): return "definition/construction"
    return "constructor/recursor"
stat=defaultdict(lambda: Counter())
for nm,refs in prov.items():
    di=idx.get(nm)
    if di is None or di not in art_of: continue
    ai=art_of[di]
    pl=lbset.get(ai)
    if not pl: continue
    stmt={names[x] for x in pl if False}
    # statement-world refs of this artifact
    stmtset=set()
    for i in range(0):
        pass
    gt=[c for c in refs if c!=nm and c in idx]
    for c in gt:
        ci=idx[c]; g=grp(kind[ci])
        stat[g]["written"]+=1
        if ci in allrefs_art[ai]: stat[g]["in_record_any"]+=1
        if ci in pl: stat[g]["in_record_loadbearing"]+=1
print(f"{'kind':<26}{'written':>10}{'in record':>12}{'load-bearing':>14}{'LB coverage':>13}")
for g,c in sorted(stat.items(), key=lambda x:-x[1]["written"]):
    w=c["written"]; r=c["in_record_any"]; l=c["in_record_loadbearing"]
    print(f"{g:<26}{w:>10,}{r:>12,}{l:>14,}{100*l/max(w,1):>12.1f}%")
tot_w=sum(c["written"] for c in stat.values()); tot_l=sum(c["in_record_loadbearing"] for c in stat.values())
print(f"\noverall load-bearing coverage of human-written citations: {100*tot_l/tot_w:.1f}%")
