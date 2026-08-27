#!/usr/bin/env python3
"""Decision 2: build the two candidate LATERAL subgraphs of GAP (and GAPM) and
report the descriptive statistics that do not need community detection.

  rule (i)  fixed      rho = (d_src - d_dst) / (1 + d_src) <= 1/2
  rule (ii) within     span <= median span of the source artifact's admitted
                       edges (constant-free, relative)

Writes edges_{LATFIX,LATMED}_{GAP,GAPM}.npz into data/map_final and
decision2_lateral.json with the descriptive tables.
"""
import json
import os

import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "data", "map_final")
P5 = os.path.normpath(os.path.join(ROOT, "..", "phase5_multiscale_navigation", "data"))
SEED = 20260821

names = json.load(open(os.path.join(P5, "names.json")))
nod = np.load(os.path.join(P5, "nodes.npz"))
dsc = np.load(os.path.join(P5, "depth_scc.npz"))
depth = nod["depth"].astype(np.int64)
gen = nod["gen"]
depth_stmt = dsc["depth_stmt"]

az = np.load(os.path.join(OUT, "areas.npz"), allow_pickle=True)
area = az["area"]
area_names = [str(x) for x in az["area_names"]]

NOTATION_NAMES = {"OfNat.ofNat", "HAdd.hAdd", "HMul.hMul", "DFunLike.coe",
                  "Membership.mem", "HSMul.hSMul", "HSub.hSub"}
CLASS_LABELS = ["notation", "generated", "transport", "mathematics"]
cls = np.full(len(names), 3, dtype=np.int8)
cls[depth_stmt <= 1] = 2
cls[gen] = 1
for nm in NOTATION_NAMES:
    try:
        cls[names.index(nm)] = 0
    except ValueError:
        pass

z = np.load(os.path.join(OUT, "edges_GAP.npz"))
src = z["src_decl"].astype(np.int64)
dst = z["dst_decl"].astype(np.int64)
tg = np.load(os.path.join(ROOT, "data", "traversal_geometry.npz"))
assert np.array_equal(tg["src"].astype(np.int64), src)
span = tg["span"].astype(np.int64)

zm = np.load(os.path.join(OUT, "edges_GAPM.npz"))
math_edge = np.zeros(len(src), dtype=bool)
# GAPM drops whole sources, so recompute the source mask directly
math_src_ids = np.unique(zm["src_decl"].astype(np.int64))
math_edge = np.isin(src, math_src_ids)
assert int(math_edge.sum()) == len(zm["src_decl"])

# ---- rule (i) fixed relative span -----------------------------------------
rho = span / (1.0 + depth[src])
lat_fix = rho <= 0.5

# ---- rule (ii) within-proof median -----------------------------------------
usrc, inv = np.unique(src, return_inverse=True)
order = np.lexsort((span, inv))
inv_s = inv[order]
starts = np.flatnonzero(np.append(True, inv_s[1:] != inv_s[:-1]))
ends = np.append(starts[1:], len(inv_s))
med = np.empty(len(usrc), dtype=np.float64)
sp_s = span[order]
for gi, (s, e) in enumerate(zip(starts.tolist(), ends.tolist())):
    med[inv_s[s]] = np.median(sp_s[s:e])
lat_med = span <= med[inv]

RULES = {"LATFIX": lat_fix, "LATMED": lat_med}
BASES = {"GAP": np.ones(len(src), bool), "GAPM": math_edge}


def top100(mask):
    d = dst[mask]
    n = len(names)
    ind = np.bincount(d, minlength=n)
    top = np.argsort(-ind)[:100]
    top = top[ind[top] > 0]
    c = np.bincount(cls[top], minlength=4)
    return {
        "share_of_all_links": float(ind[top].sum() / max(1, mask.sum())),
        "class_counts": {CLASS_LABELS[i]: int(c[i]) for i in range(4)},
        "class_link_mass": {
            CLASS_LABELS[i]: float(ind[top][cls[top] == i].sum() / max(1, mask.sum()))
            for i in range(4)},
        "top25": [{"name": names[int(t)], "in_deg": int(ind[t]),
                   "class": CLASS_LABELS[int(cls[t])],
                   "area": area_names[int(area[t])],
                   "depth_stmt": int(depth_stmt[t])} for t in top[:25]],
    }


def dst_class_share(mask):
    c = np.bincount(cls[dst[mask]], minlength=4)
    tot = max(1, int(c.sum()))
    return {CLASS_LABELS[i]: float(c[i]) / tot for i in range(4)} | {
        "n": int(c.sum()),
        "counts": {CLASS_LABELS[i]: int(c[i]) for i in range(4)}}


def within_area(mask):
    s, d = src[mask], dst[mask]
    known = (area[s] != 0) & (area[d] != 0)
    return float((known & (area[s] == area[d])).mean())


def cross_plumbing(mask):
    s, d = src[mask], dst[mask]
    known = (area[s] != 0) & (area[d] != 0)
    cross = known & (area[s] != area[d])
    c = np.bincount(cls[d[cross]], minlength=4)
    tot = max(1, int(c.sum()))
    return float((c[0] + c[1] + c[2]) / tot)


rng = np.random.default_rng(SEED)
res = {"seed": SEED, "rules": {}}

for base_name, base in BASES.items():
    res["rules"][base_name] = {}
    res["rules"][base_name]["ALL"] = {
        "n_edges": int(base.sum()),
        "dst_class": dst_class_share(base),
        "within_area_edge_share": within_area(base),
        "cross_area_plumbing_share": cross_plumbing(base),
        "top100_hubs": top100(base),
        "span": {"median": float(np.median(span[base])),
                 "p90": float(np.percentile(span[base], 90))},
    }
    for rname, rmask in RULES.items():
        m = base & rmask
        r = {
            "n_edges": int(m.sum()),
            "retained_frac": float(m.sum() / base.sum()),
            "dst_class": dst_class_share(m),
            "within_area_edge_share": within_area(m),
            "cross_area_plumbing_share": cross_plumbing(m),
            "top100_hubs": top100(m),
            "span": {"median": float(np.median(span[m])),
                     "p90": float(np.percentile(span[m], 90))},
            "n_sources_with_at_least_one": int(len(np.unique(src[m]))),
            "n_sources_in_base": int(len(np.unique(src[base]))),
        }
        # what mathematics is pushed vertical
        rem = base & (~rmask)
        r["removed"] = {
            "n_edges": int(rem.sum()),
            "dst_class": dst_class_share(rem),
            "span": {"median": float(np.median(span[rem])) if rem.any() else None,
                     "p10": float(np.percentile(span[rem], 10)) if rem.any() else None},
        }
        rm_math = np.flatnonzero(rem & (cls[dst] == 3))
        pick = rng.choice(rm_math, size=min(20, len(rm_math)), replace=False)
        r["removed_math_sample"] = [
            {"src": names[int(src[i])], "dst": names[int(dst[i])],
             "d_src": int(depth[src[i]]), "d_dst": int(depth[dst[i]]),
             "span": int(span[i]), "rho": round(float(rho[i]), 3),
             "src_area": area_names[int(area[src[i]])],
             "dst_area": area_names[int(area[dst[i]])]}
            for i in sorted(pick.tolist())]
        res["rules"][base_name][rname] = r
        if base_name == "GAP":
            np.savez_compressed(os.path.join(OUT, "edges_%s_GAP.npz" % rname),
                                src_decl=src[m].astype(np.int32),
                                dst_decl=dst[m].astype(np.int32))
        else:
            np.savez_compressed(os.path.join(OUT, "edges_%s_GAPM.npz" % rname),
                                src_decl=src[m].astype(np.int32),
                                dst_decl=dst[m].astype(np.int32))

with open(os.path.join(OUT, "decision2_lateral.json"), "w") as fh:
    json.dump(res, fh, indent=2)

for b in BASES:
    print("=== base", b)
    for k in ["ALL", "LATFIX", "LATMED"]:
        v = res["rules"][b][k]
        t = v["top100_hubs"]
        print("  %-7s n=%8d  frac=%s  within=%.3f  crossplumb=%.3f  "
              "top100 mass=%.3f [math %d/100, mass %.3f]  dstmath=%.3f transport=%.3f gen=%.3f not=%.4f"
              % (k, v["n_edges"], ("%.3f" % v["retained_frac"]) if "retained_frac" in v else "1.000",
                 v["within_area_edge_share"], v["cross_area_plumbing_share"],
                 t["share_of_all_links"], t["class_counts"]["mathematics"],
                 t["class_link_mass"]["mathematics"],
                 v["dst_class"]["mathematics"], v["dst_class"]["transport"],
                 v["dst_class"]["generated"], v["dst_class"]["notation"]))
print("wrote decision2_lateral.json")
