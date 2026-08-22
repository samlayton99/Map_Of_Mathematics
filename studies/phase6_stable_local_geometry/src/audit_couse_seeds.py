#!/usr/bin/env python3
"""Seed-variance study: GAP vs GAP2 held-out co-use across 4 seeds."""
import json, os, sys
from collections import defaultdict
import numpy as np
from merge_tree import load_common
nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32); gen = nodes["gen"]; kind = nodes["kind"]
P = '../data/map_final/'
def run(edgefile, seed):
    z = np.load(P+edgefile)
    es, ed = z["src_decl"].astype(np.int64), z["dst_decl"].astype(np.int64)
    rng = np.random.default_rng(seed)
    srcs = np.unique(es)
    hold = set(rng.choice(srcs, len(srcs)//10, replace=False).tolist())
    adj = defaultdict(list); cocite = defaultdict(list)
    for s, d in zip(es, ed): (cocite if s in hold else adj)[s].append(d)
    def sig(x):
        s1 = adj.get(x, []); out = set(s1)
        for y in s1: out.update(adj.get(y, []))
        out.discard(x); return out
    ok = lambda x: (not gen[x]) and kind[x]==0 and depth[x]>=11
    pos=[]
    for t,cs in cocite.items():
        good=[c for c in set(cs) if ok(c)]
        if len(good)>=2:
            a,b=rng.choice(good,2,replace=False)
            if a!=b: pos.append((int(a),int(b)))
        if len(pos)>=3000: break
    pos=np.array(pos)
    mdp=np.minimum(depth[pos[:,0]],depth[pos[:,1]])
    pool=np.where((~gen)&(kind==0)&(depth>=11))[0]
    neg=[]
    for m in mdp:
        while True:
            a,b=rng.choice(pool,2)
            if a!=b and abs(int(min(depth[a],depth[b]))-int(m))<=5:
                neg.append((int(a),int(b))); break
    def kin(Pp):
        cache={}; c=0
        for a,b in Pp:
            sa=cache.get(a)
            if sa is None: sa=cache[a]=sig(a)
            sb=cache.get(b)
            if sb is None: sb=cache[b]=sig(b)
            if sa&sb: c+=1
        return c/len(Pp)
    kp, kn = kin(pos), kin(np.array(neg))
    return kp, kn, kp/max(kn,1e-9)
for ef, tag in (("edges_GAP.npz","GAP "),("edges_GAP2.npz","GAP2")):
    lifts=[]
    for seed in (20260904, 20260905, 20260906, 20260908):
        kp,kn,l = run(ef, seed)
        lifts.append(l)
        print(f"  {tag} seed {seed}: pos {kp:.3f} neg {kn:.3f} lift {l:.1f}x")
    print(f"  {tag} lifts: {[round(x,1) for x in lifts]}  mean {np.mean(lifts):.1f}")
