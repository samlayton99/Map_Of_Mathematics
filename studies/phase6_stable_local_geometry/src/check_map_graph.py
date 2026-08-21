"""Brute-force reference check of map_graph.py on a random sample of artifacts."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_graph as MG  # noqa: E402

A = MG.load_arrays()
owner = np.load(os.path.join(MG.OUT_DIR, "owner.npy"))
TIER = {0: 0, 1: 0, 2: 1, 7: 2, 5: 3, 3: 4, 4: 5, 6: 6}

rng = np.random.default_rng(7)
nongen = np.flatnonzero(~A["is_generated"])
sample = rng.choice(nongen, 400, replace=False)

starts = np.zeros(len(A["n_incidences"]), dtype=np.int64)
np.cumsum(A["n_incidences"][:-1], out=starts[1:])

E4 = np.load(os.path.join(MG.OUT_DIR, "edges_E4.npz"))
got4 = {}
for s, d in zip(E4["src_decl"], E4["dst_decl"]):
    got4.setdefault(int(s), set()).add(int(d))

EL0 = np.load(os.path.join(MG.OUT_DIR, "edges_EL0.npz"))
gotL = {}
for s, d in zip(EL0["src_decl"], EL0["dst_decl"]):
    gotL.setdefault(int(s), set()).add(int(d))

EF = np.load(os.path.join(MG.OUT_DIR, "edges_E4_flat.npz"))
gotF = {}
for s, d in zip(EF["src_decl"], EF["dst_decl"]):
    gotF.setdefault(int(s), set()).add(int(d))

bad4 = badL = badF = 0
checked = 0
for a in sample:
    a = int(a)
    tgt = int(A["certifies"][a])
    lo, hi = int(starts[a]), int(starts[a]) + int(A["n_incidences"][a])
    cands = {}
    for p, r in enumerate(range(lo, hi)):
        d = int(A["decl"][r])
        roles = A["roles"][r]
        occ = [i for i in range(8) if roles[i] > 0]
        if not occ:
            continue
        tier = min(TIER[i] for i in occ)
        lb = bool(A["load_bearing"][r])
        if lb:
            dem = 0
        elif not bool(A["pr"][d]):
            dem = 1
        else:
            continue
        g = bool(A["gen"][d])
        if g:
            o = int(owner[d])
            if o < 0 or o == tgt:
                continue
            cand = o
            depth = int(A["depth"][o])
            ds = int(A["depth_stmt"][o])
            lane = 1 if ds <= 1 else 0
        else:
            cand = d
            depth = int(A["d_cite"][r])
            ds = int(A["depth_stmt"][d])
            lane = 2 if tier == 5 else (1 if ds <= 1 else 0)
        if cand == tgt:
            continue
        stmt = int(A["in_stmt_world"][r])
        key = (dem, lane, stmt, -depth, p)
        if cand not in cands or key < cands[cand]:
            cands[cand] = key
    # flat control: (role tier, position) over load-bearing candidates only
    flat = []
    for p, r in enumerate(range(lo, hi)):
        if not bool(A["load_bearing"][r]):
            continue
        d = int(A["decl"][r])
        if d == tgt:
            continue
        roles = A["roles"][r]
        occ = [i for i in range(8) if roles[i] > 0]
        if not occ:
            continue
        flat.append((min(TIER[i] for i in occ), p, d))
    expF = {d for _, _, d in sorted(flat)[:4]}

    ordered = sorted(cands.items(), key=lambda kv: kv[1])
    exp4 = {c for c, _ in ordered[:4]}
    expL = {c for c, k in ordered if k[0] == 0 and k[1] == 0 and k[2] == 0}
    # multiple artifacts can certify the same declaration; only compare when
    # the target has exactly one non-generated artifact
    checked += 1
    if not exp4 <= got4.get(tgt, set()):
        bad4 += 1
        if bad4 <= 3:
            print("E4 mismatch tgt", tgt, "expected", sorted(exp4),
                  "got", sorted(got4.get(tgt, set())))
    if not expL <= gotL.get(tgt, set()):
        badL += 1
        if badL <= 3:
            print("EL0 mismatch tgt", tgt, "expected", sorted(expL),
                  "got", sorted(gotL.get(tgt, set())))

    if not expF <= gotF.get(tgt, set()):
        badF += 1
        if badF <= 3:
            print("E4_flat mismatch tgt", tgt, "expected", sorted(expF),
                  "got", sorted(gotF.get(tgt, set())))

print("checked %d artifacts: E4 mismatches %d, EL0 mismatches %d, "
      "E4_flat mismatches %d" % (checked, bad4, badL, badF))
