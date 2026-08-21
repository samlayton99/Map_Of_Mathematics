#!/usr/bin/env python3
"""Deterministic failure mining for laneD = (lane, -d_cite, tier, first).
For every graded proof with a grade-4 key: if top-1 is not a key, classify
WHY by the sort key that made the decision. Also: universe exclusions
(key items we can never rank), lane false-demotions among useful items,
per-depth-band KeyMove@1.
"""
import json, glob, os, sys
from collections import defaultdict, Counter
import numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("hv", "hier_views.py")
hv = importlib.util.module_from_spec(spec); sys.argv = ["hv"]; spec.loader.exec_module(hv)
P5 = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "phase5_multiscale_navigation"))
P6 = os.path.normpath(os.path.join(os.getcwd(), ".."))
LOAD = (0, 1, 2, 7)

briefs = json.load(open(P5 + "/review/sealed_r1/briefs.json"))
grades = defaultdict(lambda: defaultdict(list))
for f in glob.glob(P5 + "/review/sealed_r1/grades_*.json"):
    for pid, rec in json.load(open(f)).items():
        for n, g in rec.get("grades", {}).items():
            grades[pid][n].append(int(g))
forest = hv.load_forest(P6 + "/data/graded_hier.jsonl")

def feats(occs, target):
    first, tier, nest, load, roles_seen = {}, {}, {}, set(), defaultdict(set)
    for i, o in enumerate(occs):
        c, p, r, lv = o[0], o[1], o[2], o[4]
        first.setdefault(c, i)
        tier[c] = min(tier.get(c, 9), hv.ROLE_TIER.get(r, 9))
        roles_seen[c].add(r)
        if r in LOAD:
            load.add(c); nest[c] = min(nest.get(c, 10**9), lv)
    out, dropped = {}, {}
    for c in set(first):
        i = hv.name_id.get(c)
        if c not in load:
            dropped[c] = "not_load_bearing"
            continue
        if i is not None and hv.gen[i]:
            o = hv.owner_of(c)
            if o == target or o == c:
                dropped[c] = "gen_owned_by_target"
                continue
            lane = 0 if (o in hv.name_id and hv.depth_stmt[hv.name_id[o]] > 1) else 1
            dc = int(hv.depth[hv.name_id[o]]) if o in hv.name_id else 0
            key = o
        else:
            lane = 2 if tier[c] == 5 else (1 if (i is not None and hv.depth_stmt[i] <= 1) else 0)
            dc = int(hv.depth[i]) if i is not None else 0
            key = c
        if key not in out:
            out[key] = dict(lane=lane, negd=-dc, tier=tier[c], first=first[c],
                            roles=sorted(roles_seen[c]))
    return out, dropped

cls = Counter(); ex = defaultdict(list)
band_tot = Counter(); band_hit = Counter()
useful_lane = Counter(); n_use = 0
key_excluded_detail = Counter()
BANDS = [(0,10),(11,25),(26,50),(51,100),(101,200),(201,10**9)]
def band(d):
    for lo,hi in BANDS:
        if lo <= d <= hi: return f"{lo}-{hi if hi<10**9 else 'inf'}"
for b in briefs:
    cands = b["candidates"] if isinstance(b["candidates"], list) else eval(b["candidates"])
    cmap = {str(c["n"]): c["name"] for c in cands}
    stmt = {c["name"]: bool(c.get("in_statement")) for c in cands}
    pid, thm, dt = b["id"], b["theorem"], int(b["theorem_depth"])
    occs = forest.get(thm)
    if not occs or pid not in grades: continue
    gmed = {cmap[n]: float(np.median(gs)) for n, gs in grades[pid].items() if n in cmap}
    useful = {c for c, g in gmed.items() if g >= 3}
    keys = {c for c, g in gmed.items() if g >= 4}
    F, dropped = feats(occs, thm)
    if not F: continue
    order = sorted(F, key=lambda c: (F[c]["lane"], F[c]["negd"], F[c]["tier"], F[c]["first"]))
    # lane composition of useful items (tail analysis)
    for c in useful:
        if c in F: useful_lane[F[c]["lane"]] += 1; n_use += 1
    if not keys: continue
    bd = band(dt); band_tot[bd] += 1
    top = order[0]
    if top in keys:
        band_hit[bd] += 1
        continue
    # ---- classify the failure
    ranked_keys = [c for c in order if c in keys]
    if not ranked_keys:
        cls["key_excluded_from_universe"] += 1
        for c in keys:
            key_excluded_detail[dropped.get(c, "absent_from_term")] += 1
        ex["key_excluded"].append((thm, dt, sorted(keys), order[:3]))
        continue
    kbest = ranked_keys[0]
    ft, fk = F[top], F[kbest]
    if ft["lane"] < fk["lane"]:
        cls["lane_demoted_key"] += 1
        ex["lane_demoted"].append((thm, dt, top, int(gmed.get(top,-1)), kbest, ft["lane"], fk["lane"]))
    elif ft["negd"] < fk["negd"]:
        c = "depth_inversion_stmtvocab" if stmt.get(top) else "depth_inversion_proofintro"
        cls[c] += 1
        ex[c].append((thm, dt, top, int(gmed.get(top,-1)), -ft["negd"], kbest, -fk["negd"], stmt.get(top)))
    elif ft["negd"] == fk["negd"] and ft["tier"] < fk["tier"]:
        cls["tier_decided_wrong"] += 1
    elif ft["negd"] == fk["negd"] and ft["tier"] == fk["tier"]:
        cls["first_occurrence_decided"] += 1
        ex["first_occ"].append((thm, dt, top, kbest))
    else:
        cls["other"] += 1
print("FAILURE CLASSES (laneD rank-1 misses):")
tot = sum(cls.values())
for k, v in cls.most_common():
    print(f"  {k:32} {v:4d}  ({v/tot:.0%})")
print(f"  total failures {tot} / proofs-with-key {sum(band_tot.values())}")
print("\nkey_excluded reasons:", dict(key_excluded_detail))
print("\nKeyMove@1 by target-depth band:")
for bd in [band((lo+min(hi,300))//2) for lo,hi in BANDS]:
    if band_tot[bd]:
        print(f"  {bd:9} {band_hit[bd]}/{band_tot[bd]} = {band_hit[bd]/band_tot[bd]:.3f}")
print(f"\nuseful items by lane: " +
      str({k: f"{v} ({v/n_use:.0%})" for k, v in sorted(useful_lane.items())}))
json.dump({k: v[:12] for k, v in ex.items()}, open(P6 + "/data/laneD_failures.json", "w"),
          indent=1, default=str)
print("\nexamples -> data/laneD_failures.json")
