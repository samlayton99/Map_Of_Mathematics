#!/usr/bin/env python3
"""P1 pilot: hierarchy-vs-flat comparison (H1).

Four views per proof, built from the same occurrence forest:
  flat          all load-bearing cited consts as siblings (phase5 status quo)
  owner         flat + generated consts collapsed into their owning decl
  hier          named-application hierarchy: visible = root-level items only
  hier_lanes    hierarchy + lanes; budget draws from the move lane only

Fixed sibling ordering everywhere (stated, ordinal, constant-free):
  role tier (applied/let=0, explicit=1, unresolved=2, strict-implicit=3,
  implicit=4, instance=5, type-annot=6) then walk order. No fitted weights.

Structural metrics (primary): generated exposure@k, foundational
exposure@k (d_cite<=10 while d_target>=26 shown as top-level siblings —
the artificial-lateral candidates), vertical/lateral split, expansion
completeness. Band edges are the stated depth bands, not fitted constants.

Grade-based recall (secondary, contamination-flagged — see
p0/P0_GRADING_BRIEF_AUDIT.md) runs only when graded_hier.jsonl exists.
"""
import json, os, sys
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, ".."))
P5DATA = os.path.normpath(os.path.join(P6, "..", "phase5_multiscale_navigation", "data"))
LOAD_ROLES = (0, 1, 2, 7)
ROLE_TIER = {0: 0, 1: 0, 2: 1, 7: 2, 5: 3, 3: 4, 4: 5, 6: 6}
BUDGETS = (1, 2, 4, 8)

nodes = np.load(os.path.join(P5DATA, "nodes.npz"))
names = json.load(open(os.path.join(P5DATA, "names.json")))
name_id = {n: i for i, n in enumerate(names)}
depth = nodes["depth"]; gen = nodes["gen"]
# statement-vocabulary depth (type-only graph, exact SCC) — separates
# universal automation (type mentions only logical core, depth_stmt <= 1)
# from universal mathematics (type needs real vocabulary)
depth_stmt = np.load(os.path.join(P5DATA, "depth_scc.npz"))["depth_stmt"]

nonint = set()  # names present but non-gen, for owner lookup
NONGEN = {n for i, n in enumerate(names) if not gen[i]}

def owner_of(cname):
    """Longest proper name-prefix that is an existing non-generated decl.
    Elaborator provenance (stated exception to the no-names principle)."""
    parts = cname.split(".")
    for cut in range(len(parts) - 1, 0, -1):
        p = ".".join(parts[:cut])
        if p in NONGEN:
            return p
    return cname

def load_forest(path):
    out = {}
    for line in open(path):
        r = json.loads(line)
        if r.get("ok"):
            out[r["n"]] = r["occ"]
    return out

def build_views(occs, d_target, target=""):
    """occs: [[const, parent, role, argIdx, nesting, nargs], ...]"""
    # per-occurrence tuples
    C, P, R = [o[0] for o in occs], [o[1] for o in occs], [o[2] for o in occs]
    # ---- flat: distinct consts with a load-bearing occurrence
    first, tier, load = {}, {}, set()
    for i, (c, r) in enumerate(zip(C, R)):
        if c not in first:
            first[c] = i
        tier[c] = min(tier.get(c, 9), ROLE_TIER.get(r, 9))
        if r in LOAD_ROLES:
            load.add(c)
    flat = sorted(load, key=lambda c: (tier[c], first[c]))
    # ---- owner collapse
    omap = {c: (owner_of(c) if (c in name_id and gen[name_id[c]]) else c)
            for c in load}
    ofirst, otier = {}, {}
    for c in flat:
        o = omap[c]
        ofirst.setdefault(o, first[c])
        otier[o] = min(otier.get(o, 9), tier[c])
    owner = sorted(set(omap.values()), key=lambda c: (otier[c], ofirst[c]))
    # ---- hierarchy AS ORDERING: shallower (fewer named-application
    # ancestors) before deeper. A roots-only cut hides most useful moves
    # (measured: recall flatlines at ~0.31); the hierarchy's information is
    # the nesting key, applied ahead of the role tier.
    #   flat  = (tier, first-occurrence)
    #   hier  = (min load-bearing nesting, tier, first-occurrence)
    nest, kids = {}, defaultdict(set)
    n_roots = 0
    for i, (c, p, r, o) in enumerate(zip(C, P, R, occs)):
        if r in LOAD_ROLES:
            lv = o[4]
            nest[c] = min(nest.get(c, 10**9), lv)
            if p == -1:
                n_roots += 1
        if p != -1:
            kids[C[p]].add(c)
    hier = sorted(load, key=lambda c: (nest.get(c, 10**9), tier[c], first[c]))
    # expansion completeness: every load-bearing const reachable from the
    # full root set (any role — concept roots stay expandable)
    allroots = {c for c, p in zip(C, P) if p == -1}
    reach = set(allroots)
    frontier = list(allroots)
    while frontier:
        nxt = []
        for c in frontier:
            for k in kids[c]:
                if k not in reach:
                    reach.add(k); nxt.append(k)
        frontier = nxt
    complete = load <= reach
    # ---- lanes: infra = generated const or instance-only occurrences;
    # they leave the budget entirely (remain expandable)
    def is_infra(c):
        return (c in name_id and gen[name_id[c]]) or tier[c] == 5
    hier_lanes = [c for c in hier if not is_infra(c)]
    # ---- full stack: hierarchy order + lanes + owner REDIRECT.
    # A generated helper owned by the target itself is an internal step:
    # dropped. Owned by another declaration: redirected to that owner (a
    # real navigational target). Instance-only occurrences leave the budget.
    ffirst, ftier, fnest = {}, {}, {}
    for c in hier:
        if c in name_id and gen[name_id[c]]:
            o = owner_of(c)
            if o == target or o == c:
                continue
        else:
            if tier[c] == 5:
                continue
            o = c
        ffirst.setdefault(o, first[c])
        ftier[o] = min(ftier.get(o, 9), tier[c])
        fnest[o] = min(fnest.get(o, 10**9), nest.get(c, 10**9))
    full = sorted(ffirst, key=lambda c: (fnest[c], ftier[c], ffirst[c]))
    # ---- laned: lane as the OUTERMOST ordinal key — demotion, not
    # removal (relativity: a purely logical proof still shows its logic).
    # lane 0 = move, 1 = transport (depth_stmt <= 1), 2 = infrastructure.
    def lane_rank(c):
        i = name_id.get(c)
        if (i is not None and gen[i]) or ftier.get(c, tier.get(c, 9)) == 5:
            return 2
        if i is not None and depth_stmt[i] <= 1:
            return 1
        return 0
    laned = sorted(ffirst, key=lambda c: (lane_rank(c), fnest[c], ftier[c], ffirst[c]))
    n_r = len({c for c in load if nest.get(c, 10**9) == 0})
    return {"flat": flat, "owner": owner, "hier": hier,
            "hier_lanes": hier_lanes, "full": full, "laned": laned,
            "complete": complete, "n_roots": n_r, "n_load": len(load)}

def metrics(view_list, d_target, k):
    vis = view_list[:k]
    if not vis:
        return None
    dg = [bool(gen[name_id[c]]) if c in name_id else False for c in vis]
    dc = [int(depth[name_id[c]]) if c in name_id else -1 for c in vis]
    found = [c for c, d in zip(vis, dc) if d_target >= 26 and 0 <= d <= 10]
    return {"gen_exp": sum(dg) / len(vis),
            "foundational_exp": len(found) / len(vis),
            "n_vis": len(vis)}

def main():
    pilot = json.load(open(os.path.join(P6, "data", "pilot48.json")))
    forest = load_forest(os.path.join(P6, "data", "pilot48_hier.jsonl"))
    rows, agg = [], defaultdict(list)
    for pr in pilot["proofs"]:
        occs = forest.get(pr["name"])
        if not occs:
            continue
        v = build_views(occs, pr["depth"], pr["name"])
        rec = {"name": pr["name"], "depth": pr["depth"], "kind": pr["kind"],
               "n_load": v["n_load"], "n_roots": v["n_roots"],
               "complete": v["complete"], "views": {}}
        for vn in ("flat", "owner", "hier", "hier_lanes", "full", "laned"):
            rec["views"][vn] = v[vn][:12]
            for k in BUDGETS:
                m = metrics(v[vn], pr["depth"], k)
                if m:
                    agg[(vn, k, "gen")].append(m["gen_exp"])
                    agg[(vn, k, "fnd")].append(m["foundational_exp"])
        agg[("_", 0, "compress")].append(
            v["n_roots"] / max(v["n_load"], 1))
        agg[("_", 0, "complete")].append(float(v["complete"]))
        rows.append(rec)
    out = {"per_proof": rows, "summary": {}}
    s = out["summary"]
    s["expansion_completeness"] = float(np.mean(agg[("_", 0, "complete")]))
    s["root_compression"] = float(np.mean(agg[("_", 0, "compress")]))
    for vn in ("flat", "owner", "hier", "hier_lanes", "full", "laned"):
        for k in BUDGETS:
            for mname, key in (("gen_exposure", "gen"), ("foundational_exposure", "fnd")):
                vals = agg[(vn, k, key)]
                if vals:
                    s[f"{vn}@{k}_{mname}"] = round(float(np.mean(vals)), 4)
    path = os.path.join(P6, "data", "pilot_views.json")
    json.dump(out, open(path, "w"), indent=1)
    print(f"proofs {len(rows)}  completeness {s['expansion_completeness']:.3f}  "
          f"root compression {s['root_compression']:.3f}")
    for k in BUDGETS:
        print(f"k={k}  " + "  ".join(
            f"{vn}: gen {s.get(f'{vn}@{k}_gen_exposure', 0):.3f} fnd {s.get(f'{vn}@{k}_foundational_exposure', 0):.3f}"
            for vn in ("flat", "owner", "hier", "hier_lanes")))

if __name__ == "__main__":
    main()
