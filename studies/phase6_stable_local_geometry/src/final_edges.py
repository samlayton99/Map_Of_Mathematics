#!/usr/bin/env python3
"""Build edges_FINAL: the frozen construction at corpus scale.
Per artifact: gap-cut over dem-0 pool UNION move-lane (lane0,stmt0) —
with DEF-TARGET scoping: constructors and class projections excluded
from the lane side, and U1D items (non-ctor, non-classproj) admitted
above the gap threshold. Theorem targets: base union (held-out tests
rejected classproj exclusion there)."""
import os, json
import numpy as np
os.environ["MAPGRAPH_DATA_DIR"] = "/Users/sam/my-repos/research/Map_Of_Mathematics/studies/phase5_multiscale_navigation/data"
os.environ["MAPGRAPH_OUT_DIR"] = "/Users/sam/my-repos/research/Map_Of_Mathematics/studies/phase6_stable_local_geometry/data/map_final"
import importlib, map_graph as MG
importlib.reload(MG)
A = MG.load_arrays()
owner = MG.build_owner_map(A)
C = MG.build_candidates(A, owner)
order, rank = MG.order_and_dedup(C, len(A["certifies"]))
art = C["artifact"][order]; dem = C["dem"][order]; lane = C["lane"][order]
stmt = C["stmt"][order]; dep = C["depth"][order].astype(np.int64)
cand = C["cand"][order]; tgt = C["target"][order]
names = json.load(open(os.environ["MAPGRAPH_DATA_DIR"]+"/names.json"))
name_id = {n:i for i,n in enumerate(names)}
PROJ = np.zeros(len(names), bool)
for line in open('/Users/sam/mathmap_data/projflags.tsv'):
    n, isp, iscls = line.rstrip('\n').split('\t')
    if int(iscls)==1 and n in name_id: PROJ[name_id[n]]=True
import numpy as _np
nodes = _np.load(os.environ["MAPGRAPH_DATA_DIR"]+"/nodes.npz")
KIND = nodes["kind"]
tkind = KIND[A["certifies"]]     # per artifact: 0 thm, 1 def
is_ctor = KIND[cand]==3
is_cp = PROJ[cand]
o2 = np.argsort((art.astype(np.int64)<<22) | ((1<<21) if 0 else 0) | (dem.astype(np.int64)<<20) | (2**19-dep), kind="stable")
art,dem,lane,stmt,dep,cand,tgt,is_ctor,is_cp = (x[o2] for x in (art,dem,lane,stmt,dep,cand,tgt,is_ctor,is_cp))
newblk=np.empty(len(art),bool); newblk[0]=True
np.not_equal(art[1:],art[:-1],out=newblk[1:])
starts=np.flatnonzero(newblk); ends=np.append(starts[1:],len(art))
keep=np.zeros(len(art),bool)
for s,e in zip(starts,ends):
    a=art[s]
    kdef = tkind[a]==1
    m0 = dem[s:e]==0
    d0 = dep[s:e][m0]
    if len(d0)==0: continue
    du = np.unique(d0)[::-1]
    if len(du)==1: t=du[0]
    else:
        gaps=du[:-1]-du[1:]
        g=gaps.max()
        t = du[int(np.argmax(gaps))] if g>0 else du[-1]
    blk=slice(s,e)
    gap_m = m0 & (dep[s:e]>=t)
    el0_m = m0 & (lane[s:e]==0) & (stmt[s:e]==0)
    if kdef:
        el0_m = el0_m & (~is_ctor[s:e]) & (~is_cp[s:e])
        u1d_m = (dem[s:e]==1) & (dep[s:e]>=t) & (~is_ctor[s:e]) & (~is_cp[s:e])
    else:
        u1d_m = np.zeros(e-s,bool)
    keep[s:e] = gap_m | el0_m | u1d_m
src,dst = tgt[keep].astype(np.int32), cand[keep].astype(np.int32)
np.savez_compressed(os.environ["MAPGRAPH_OUT_DIR"]+"/edges_FINAL.npz", src_decl=src, dst_decl=dst)
depth = nodes["depth"].astype(np.int64)
rho = (depth[src]-depth[dst])/(1.0+depth[src])
lat = rho<=0.5
np.savez_compressed(os.environ["MAPGRAPH_OUT_DIR"]+"/edges_LATFIX_FINAL.npz",
                    src_decl=src[lat], dst_decl=dst[lat])
print(f"FINAL: {keep.sum()} edges from {len(starts)} artifacts; LATFIX_FINAL: {lat.sum()} edges")
