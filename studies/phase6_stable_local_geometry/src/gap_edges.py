#!/usr/bin/env python3
"""Build the GAP edge set: per artifact, include all dem-0 candidates at
or above the largest cited-depth gap (local, constant-free inclusion).
Writes data/map_final/edges_GAP.npz in map_graph format."""
import os, sys
import numpy as np
import map_graph as MG

os.environ.setdefault("MAPGRAPH_DATA_DIR",
    os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "phase5_multiscale_navigation", "data")))
A = MG.load_arrays()
owner = MG.build_owner_map(A)
C = MG.build_candidates(A, owner)
order, rank = MG.order_and_dedup(C, int(A["artifact"].max()) + 1 if "artifact" in A else len(A["certifies"]))
art = C["artifact"][order]; dem = C["dem"][order]
dep = C["depth"][order]; cand = C["cand"][order]; tgt = C["target"][order]
m = dem == 0
art, dep, cand, tgt = art[m], dep[m].astype(np.int64), cand[m], tgt[m]
o2 = np.argsort((art.astype(np.int64) << 20) | (2**19 - dep), kind="stable")
art, dep, cand, tgt = art[o2], dep[o2], cand[o2], tgt[o2]
newblk = np.empty(len(art), bool); newblk[0] = True
np.not_equal(art[1:], art[:-1], out=newblk[1:])
starts = np.flatnonzero(newblk)
ends = np.append(starts[1:], len(art))
keep = np.zeros(len(art), bool)
for s, e in zip(starts, ends):
    d = dep[s:e]
    if e - s == 1:
        keep[s:e] = True; continue
    gaps = d[:-1] - d[1:]
    g = gaps.max()
    if g == 0:
        keep[s:e] = True; continue
    i = int(np.argmax(gaps))
    keep[s:e] = d >= d[i]
src, dst = tgt[keep], cand[keep]
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "map_final")
np.savez_compressed(os.path.join(outdir, "edges_GAP.npz"),
                    src=src.astype(np.int32), dst=dst.astype(np.int32))
ks = np.diff(np.append(np.flatnonzero(np.append(True, art[keep][1:] != art[keep][:-1])), keep.sum()))
print(f"GAP edges: {keep.sum()} from {len(starts)} artifacts; "
      f"k mean {keep.sum()/len(starts):.2f} median {np.median(ks):.0f} p90 {np.percentile(ks,90):.0f}")
