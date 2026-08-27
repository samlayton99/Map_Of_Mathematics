#!/usr/bin/env python3
"""Decision 2 supplement: rule disagreement, false-vertical proxies, and the
interface-vocabulary link mass that vertical rendering is meant to remove."""
import json
import os

import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "data", "map_final")
P5 = os.path.normpath(os.path.join(ROOT, "..", "phase5_multiscale_navigation", "data"))

names = json.load(open(os.path.join(P5, "names.json")))
nod = np.load(os.path.join(P5, "nodes.npz"))
dsc = np.load(os.path.join(P5, "depth_scc.npz"))
depth = nod["depth"].astype(np.int64)
gen = nod["gen"]
depth_stmt = dsc["depth_stmt"]
az = np.load(os.path.join(OUT, "areas.npz"), allow_pickle=True)
area = az["area"]

INTERFACE = ["OfNat.ofNat", "HAdd.hAdd", "HMul.hMul", "DFunLike.coe",
             "Membership.mem", "HSMul.hSMul", "HSub.hSub", "rfl", "Eq.ndrec",
             "of_eq_true", "Iff.rfl", "eq_self", "Inhabited.default"]
iface_ids = {names.index(nm) for nm in INTERFACE if nm in names}

z = np.load(os.path.join(OUT, "edges_GAP.npz"))
src = z["src_decl"].astype(np.int64)
dst = z["dst_decl"].astype(np.int64)
tg = np.load(os.path.join(ROOT, "data", "traversal_geometry.npz"))
span = tg["span"].astype(np.int64)
rho = span / (1.0 + depth[src])
lat_fix = rho <= 0.5

usrc, inv = np.unique(src, return_inverse=True)
order = np.lexsort((span, inv))
inv_s = inv[order]
starts = np.flatnonzero(np.append(True, inv_s[1:] != inv_s[:-1]))
ends = np.append(starts[1:], len(inv_s))
med = np.empty(len(usrc))
sp_s = span[order]
for s, e in zip(starts.tolist(), ends.tolist()):
    med[inv_s[s]] = np.median(sp_s[s:e])
lat_med = span <= med[inv]

zm = np.load(os.path.join(OUT, "edges_GAPM.npz"))
math_edge = np.isin(src, np.unique(zm["src_decl"].astype(np.int64)))

cls = np.full(len(names), 3, dtype=np.int8)
cls[depth_stmt <= 1] = 2
cls[gen] = 1
is_iface = np.zeros(len(names), bool)
for i in iface_ids:
    is_iface[i] = True

res = {}
for base_name, base in [("GAP", np.ones(len(src), bool)), ("GAPM", math_edge)]:
    b = base
    both = b & lat_fix & lat_med
    only_fix = b & lat_fix & (~lat_med)
    only_med = b & (~lat_fix) & lat_med
    neither = b & (~lat_fix) & (~lat_med)

    def blk(m):
        return {"n": int(m.sum()),
                "median_span": float(np.median(span[m])) if m.any() else None,
                "median_rho": float(np.median(rho[m])) if m.any() else None,
                "dst_math_frac": float((cls[dst[m]] == 3).mean()) if m.any() else None}

    ifm = {}
    for nm in INTERFACE:
        if nm not in names:
            continue
        i = names.index(nm)
        tgt = (dst == i)
        ifm[nm] = {
            "GAP_or_base": int((b & tgt).sum()),
            "LATFIX": int((b & lat_fix & tgt).sum()),
            "LATMED": int((b & lat_med & tgt).sum()),
        }
    tot_iface = b & is_iface[dst]
    res[base_name] = {
        "agreement": {"both_lateral": blk(both), "only_LATFIX": blk(only_fix),
                      "only_LATMED": blk(only_med), "neither": blk(neither)},
        "interface_link_mass": {
            "base_n": int(tot_iface.sum()),
            "base_share": float(tot_iface.sum() / b.sum()),
            "LATFIX_n": int((b & lat_fix & is_iface[dst]).sum()),
            "LATFIX_share": float((b & lat_fix & is_iface[dst]).sum()
                                  / max(1, (b & lat_fix).sum())),
            "LATMED_n": int((b & lat_med & is_iface[dst]).sum()),
            "LATMED_share": float((b & lat_med & is_iface[dst]).sum()
                                  / max(1, (b & lat_med).sum())),
            "per_name": ifm,
        },
        # false-vertical proxy: removed edges that are unambiguously short-range
        "false_vertical_proxy": {
            "LATFIX": {
                "removed": int((b & ~lat_fix).sum()),
                "removed_with_rho_le_0.25": int((b & ~lat_fix & (rho <= 0.25)).sum()),
                "removed_with_span_le_5": int((b & ~lat_fix & (span <= 5)).sum()),
                "removed_math_dst": int((b & ~lat_fix & (cls[dst] == 3)).sum()),
            },
            "LATMED": {
                "removed": int((b & ~lat_med).sum()),
                "removed_with_rho_le_0.25": int((b & ~lat_med & (rho <= 0.25)).sum()),
                "removed_with_span_le_5": int((b & ~lat_med & (span <= 5)).sum()),
                "removed_math_dst": int((b & ~lat_med & (cls[dst] == 3)).sum()),
            },
        },
    }

with open(os.path.join(OUT, "decision2_disagreement.json"), "w") as fh:
    json.dump(res, fh, indent=2)
print(json.dumps(res, indent=2)[:4000])
