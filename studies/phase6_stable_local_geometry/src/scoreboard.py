#!/usr/bin/env python3
"""The scoreboard: random / frozen / ceiling, split by target kind,
on the blind instrument. Boundary = reading view; zoom1 = map edges."""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util
spec2 = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec2); sys.argv=["hv"]; spec2.loader.exec_module(hv)
import frozen
P6 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
B = os.path.join(P6, "data", "blind")
node={"gen":hv.gen,"depth":hv.depth,"kind":hv.nodes["kind"],"pr":hv.nodes["pr"]}
CP=set()
for line in open('/Users/sam/mathmap_data/projflags.tsv'):
    n,isp,iscls=line.rstrip('\n').split('\t')
    if int(iscls)==1: CP.add(n)
briefs=json.load(open(os.path.join(B,"briefs.json")))
forest=hv.load_forest(os.path.join(B,"targets_hier.jsonl"))
stmtf=hv.load_forest(os.path.join(B,"targets_stmt_hier.jsonl"))
per=defaultdict(lambda: defaultdict(dict))
for rf in sorted(glob.glob(os.path.join(B,"grades_R*.json"))):
    rid=rf[-6]
    for batch,tgts in json.load(open(rf)).items():
        for tid,cs in tgts.items():
            for n,g in cs.items():
                if g is not None: per[tid][n][rid]=int(g)
def f1(inc,useful,gmed):
    gi=[c for c in inc if c in gmed]
    pr=np.mean([gmed[c]>=3 for c in gi]) if gi else 0.0
    rc=sum(1 for u in useful if u in inc)/len(useful)
    return 2*pr*rc/max(pr+rc,1e-9), pr, rc
# ---- ceiling: rater vs rest, per kind
ceil=defaultdict(list)
kindof={b["id"]:("def" if b.get("kind",0)==1 else "thm") for b in briefs}
for tid,cs in per.items():
    rids=sorted({r for n in cs for r in cs[n]})
    if len(rids)<3: continue
    g=kindof.get(tid,"thm")
    for r in rids:
        mine={n for n,gs in cs.items() if gs.get(r,0)>=3}
        rest={n for n,gs in cs.items() if [v for k,v in gs.items() if k!=r]
              and np.median([v for k,v in gs.items() if k!=r])>=3}
        if not mine and not rest: continue
        tp=len(mine&rest)
        pr=tp/len(mine) if mine else (1.0 if not rest else 0.0)
        rc=tp/len(rest) if rest else (1.0 if not mine else 0.0)
        v=2*pr*rc/max(pr+rc,1e-9)
        ceil[g].append(v); ceil["all"].append(v)
# ---- frozen + random
rng=np.random.default_rng(11)
S=defaultdict(lambda: defaultdict(list))
for b in briefs:
    tid,tgt=b["id"],b["target"]; tk=b.get("kind",0); g="def" if tk==1 else "thm"
    cmap={str(c["n"]):c["name"] for c in b["candidates"]}
    gmed={cmap[n]:float(np.median(list(gs.values()))) for n,gs in per.get(tid,{}).items() if n in cmap and len(gs)>=2}
    useful={c for c,gg in gmed.items() if gg>=3}
    occs=forest.get(tgt)
    if not occs or not useful: continue
    F=frozen.candidate_features(occs,tgt,node,hv.name_id,hv.owner_of,hv.depth_stmt,CP,
                                {o[0] for o in stmtf.get(tgt,[])})
    if not F: continue
    bd=frozen.boundary(F,tk==1); z1=frozen.zoom1(F,tk==1)
    for tag,inc in (("boundary",bd),("zoom1",z1)):
        v,pr,rc=f1(inc,useful,gmed)
        for k in (g,"all"):
            S[(tag,k)]["f1"].append(v); S[(tag,k)]["pr"].append(pr); S[(tag,k)]["rc"].append(rc)
    # random matched to boundary size
    P=list(F); kk=max(len(bd),1)
    for _ in range(20):
        inc=set(rng.permutation(P)[:kk])
        v,_,_=f1(inc,useful,gmed)
        for k in (g,"all"): S[("random",k)]["f1"].append(v)
print(f"{'':10} {'THEOREMS':>18} {'DEFINITIONS':>18} {'ALL':>18}")
def row(label, vals):
    print(f"{label:10} " + "".join(f"{v:>18.3f}" for v in vals))
row("random", [np.mean(S[("random",k)]["f1"]) for k in ("thm","def","all")])
row("zoom1", [np.mean(S[("zoom1",k)]["f1"]) for k in ("thm","def","all")])
row("boundary", [np.mean(S[("boundary",k)]["f1"]) for k in ("thm","def","all")])
row("CEILING", [np.mean(ceil[k]) for k in ("thm","def","all")])
print()
for k,lab in (("thm","theorems"),("def","definitions"),("all","overall")):
    r=np.mean(S[("random",k)]["f1"]); m=np.mean(S[("boundary",k)]["f1"]); c=np.mean(ceil[k])
    print(f"  {lab:12}: boundary is {100*(m-r)/max(c-r,1e-9):.0f}% of the chance-to-ceiling range "
          f"(prec {np.mean(S[('boundary',k)]['pr']):.3f}, rec {np.mean(S[('boundary',k)]['rc']):.3f})")
print(f"\n  n targets: thm {len(S[('boundary','thm')]['f1'])}, def {len(S[('boundary','def')]['f1'])}")
