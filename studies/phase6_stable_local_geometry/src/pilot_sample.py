#!/usr/bin/env python3
"""P1 pilot sample: 48 proofs, 8 per target-depth band, satisfying the
categorical minima of gpt_handoff/05_EXPERIMENT_PROGRAM.md Phase 1:
>=12 definition/construction targets, >=12 instance-heavy, >=12 with
let-value structure, >=12 long. Categories overlap. Structural sample
(principle 9): fresh seed, no graded reuse.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P5DATA = os.path.normpath(os.path.join(HERE, "..", "..", "phase5_multiscale_navigation", "data"))
OUT = os.path.normpath(os.path.join(HERE, "..", "data"))
SEED = 20260901
BANDS = [(1, 10), (11, 25), (26, 50), (51, 100), (101, 200), (201, 10**9)]

nodes = np.load(os.path.join(P5DATA, "nodes.npz"))
arts = np.load(os.path.join(P5DATA, "artifacts.npz"))
incid = np.load(os.path.join(P5DATA, "incid.npz"))
names = json.load(open(os.path.join(P5DATA, "names.json")))

certifies = arts["certifies"]
depth = nodes["depth"][certifies]
kind = nodes["kind"][certifies]          # 0 theorem, 1 def
gen = nodes["gen"][certifies]
n_inc = arts["n_incidences"]

# per-artifact structure flags from incidences
na = len(certifies)
art_i = incid["artifact"]
roles = incid["roles"]
has_inst = np.zeros(na, bool)
has_let = np.zeros(na, bool)
inst_cnt = np.zeros(na, np.int32)
np.logical_or.at(has_inst, art_i, roles[:, 4] > 0)
np.logical_or.at(has_let, art_i, roles[:, 1] > 0)
np.add.at(inst_cnt, art_i, (roles[:, 4] > 0).astype(np.int32))
inst_share = inst_cnt / np.maximum(n_inc, 1)

rng = np.random.default_rng(SEED)

# SAMPLING-ONLY name filter (not scoring): exclude compiler/metaprogram
# artifacts that slip past the gen flag. casesOn etc. are compiler-generated
# schemes; _aux/macroRules/_unexpand are syntax metaprograms, not mathematics.
AUXSEG = {"casesOn", "recOn", "brecOn", "below", "ibelow", "noConfusion",
          "noConfusionType", "rec", "recAux", "binductionOn", "ndrec"}
def is_aux(name):
    return any(s in AUXSEG or s.startswith("_") or "macroRules" in s
               or "_aux" in s or "_unexpand" in s or s.startswith("proof_")
               for s in name.split("."))
aux = np.array([is_aux(names[int(d)]) for d in certifies])
eligible = (~gen) & (~aux) & ((kind == 0) | (kind == 1)) & (n_inc >= 3)

picked = []
for lo, hi in BANDS:
    band = np.where(eligible & (depth >= lo) & (depth <= hi))[0]
    if len(band) == 0:
        continue
    long_thr = np.quantile(n_inc[band], 0.9)
    inst_thr = np.median(inst_share[band])
    cats = [
        band[kind[band] == 1],                        # definition targets
        band[inst_share[band] > inst_thr],            # instance-heavy
        band[has_let[band]],                          # let-value structure
        band[n_inc[band] >= long_thr],                # long
    ]
    sel = []
    for cat in cats:
        pool = np.setdiff1d(cat, np.array(sel + picked, dtype=cat.dtype))
        if len(pool):
            sel += rng.choice(pool, min(2, len(pool)), replace=False).tolist()
    pool = np.setdiff1d(band, np.array(sel + picked, dtype=band.dtype))
    while len(sel) < 8 and len(pool):
        c = rng.choice(pool, 1)[0]
        sel.append(int(c))
        pool = pool[pool != c]
    picked += [int(x) for x in sel[:8]]

os.makedirs(OUT, exist_ok=True)
rows = []
for a in picked:
    d = int(certifies[a])
    rows.append({"artifact": int(a), "decl": d, "name": names[d],
                 "depth": int(depth[a]), "kind": int(kind[a]),
                 "n_inc": int(n_inc[a]), "has_let": bool(has_let[a]),
                 "inst_share": float(inst_share[a])})
json.dump({"seed": SEED, "bands": BANDS, "proofs": rows},
          open(os.path.join(OUT, "pilot48.json"), "w"), indent=1)
with open(os.path.join(OUT, "pilot48_names.txt"), "w") as f:
    for r in rows:
        f.write(r["name"] + "\n")

nk = sum(1 for r in rows if r["kind"] == 1)
nl = sum(1 for r in rows if r["has_let"])
print(f"picked {len(rows)}: {nk} defs, {nl} with let, "
      f"bands {[sum(1 for r in rows if lo <= r['depth'] <= hi) for lo, hi in BANDS]}")
