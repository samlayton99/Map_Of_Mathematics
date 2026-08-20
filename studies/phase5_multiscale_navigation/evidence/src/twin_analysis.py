import json, os, re
import numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
DATA="/Users/sam/my-repos/research/Map_Of_Mathematics/studies/phase5_multiscale_navigation/data"
inc=np.load(DATA+"/incid.npz"); arts=np.load(DATA+"/artifacts.npz")
nodes=np.load(DATA+"/nodes.npz"); v8=np.load(DATA+"/v8_mask.npz")
names=json.load(open(DATA+"/names.json"))
a=inc["artifact"].astype(np.int64); d=inc["decl"].astype(np.int64)
lb=inc["load_bearing"]; dc=inc["d_cite"].astype(np.int32)
cert=arts["certifies"].astype(np.int64); gen=nodes["gen"]; n=len(gen)
tgt=cert[a]
P4=lb & v8["decl_is_claim"][d] & ~v8["decl_logic_only"][d] & ~v8["machinery"]
i4=np.where(P4)[0]; o=np.lexsort((-dc[i4],a[i4])); i4=i4[o]
ne=np.empty(len(i4),bool); ne[0]=True; ne[1:]=a[i4][1:]!=a[i4][:-1]
t1=i4[ne]
g=sp.coo_matrix((np.ones(len(t1),np.int8),(tgt[t1],d[t1])),shape=(n,n))
_,lab=connected_components(g,directed=False)
touched=np.unique(np.concatenate([tgt[t1],d[t1]]))
sizes=np.bincount(lab[touched]); live=np.where(sizes>0)[0]
small=live[(sizes[live]>=2)&(sizes[live]<=3)]
print(f"components of size 2-3: {len(small):,} of {len(live):,} total")
# does the component consist of one declaration plus its OWN generated offspring?
GEN=re.compile(r"\.(_simp_\d+|_proof_\d+|_unary|eq_\d+|_aux.*|match_\d+.*|_f|_g|_sparseCasesOn.*|eq_def|_eq_\d+)$")
def stem(s):
    prev=None
    while prev!=s:
        prev=s; s=GEN.sub("",s)
    if s.startswith("_private."):
        p=s.split(".");  s=".".join(p[3:]) if len(p)>3 else s
    return s
rng=np.random.default_rng(5)
samp=rng.choice(small,size=min(4000,len(small)),replace=False)
twin=0; anygen=0
for c in samp:
    nd=touched[lab[touched]==c]
    stems={stem(names[i]) for i in nd}
    if len(stems)==1: twin+=1
    if gen[nd].any(): anygen+=1
print(f"  of {len(samp)} sampled small components:")
print(f"    ALL members share one stem (a lemma + its own compiler twin): {100*twin/len(samp):.1f}%")
print(f"    contain at least one machine-generated node:                  {100*anygen/len(samp):.1f}%")
# what would attribution-merging do to the component count?
covered=sizes[live]
n_small=int(((covered>=2)&(covered<=3)).sum())
print(f"\n  size 2-3 components: {n_small:,} ({100*n_small/len(live):.1f}% of all components)")
print(f"  if twin-pairs merged into their parent, components drop by roughly")
print(f"    {int(n_small*twin/len(samp)):,} -> leaving ~{len(live)-int(n_small*twin/len(samp)):,}")
