#!/usr/bin/env python3
"""THE FROZEN CONSTRUCTION — single canonical implementation (v2, post-audit).

Ranking (per proof, ordinal keys, ascending):
  theorem targets:    (u1d-demoted, lane, stmt, -depth, position)
  definition targets: (ctor, classproj, stmt, -depth, position)
    -- definitions draw content from ALL roles: no universe demotion, no
       transport/infra lane (audit showed those demote the parent
       instances raters call the content; removing them reached
       theorem-parity KM 0.903)
Boundary (reading view):
  theorems:    gap-set  UNION  {lane0, stmt0}
  definitions: gap-set  UNION  {lane0, stmt0, non-ctor, non-classproj}
               UNION  {u1d, d >= gap threshold, non-ctor, non-classproj}
Zoom-1 (map/kinship substrate): plain gap-set over the dem-0 pool for
  ALL targets (audit: def admissions cost paired co-use lift on 4/4
  seeds for noise-level AMI gain; Occam keeps the simpler object).
Atlas view: zoom-1, sources scoped to Mathlib mathematics, edges with
  relative span > 1/2 rendered vertical.
All facts kernel/elaborator-derived; constants are stated small
integers; the 1/2 is a view constant (swept: plateau).
"""
import numpy as np

ROLE_TIER = {0: 0, 1: 0, 2: 1, 7: 2, 5: 3, 3: 4, 4: 5, 6: 6}
LOAD = (0, 1, 2, 7)

def candidate_features(occs, target, node, name_id, owner_of, depth_stmt,
                       classproj, stmt_names):
    """occs: hierdump rows [[const,parent,role,argIdx,nesting,nargs],..].
    Returns {const: feature dict} after generated-owner redirect."""
    first, tier, load, anyocc = {}, {}, set(), {}
    for i, o in enumerate(occs):
        c, r = o[0], o[2]
        first.setdefault(c, i)
        tier[c] = min(tier.get(c, 9), ROLE_TIER.get(r, 9))
        anyocc[c] = True
        if r in LOAD:
            load.add(c)
    out = {}
    def add(c, dem):
        i = name_id.get(c)
        if i is not None and node["gen"][i]:
            o = owner_of(c)
            if o == target or o == c:
                return
            io = name_id.get(o)
            ds = int(depth_stmt[io]) if io is not None else 9
            dv = int(node["depth"][io]) if io is not None else 0
            key = o
            kk = int(node["kind"][io]) if io is not None else -1
            inst = 0
        else:
            ds = int(depth_stmt[i]) if i is not None else 9
            dv = int(node["depth"][i]) if i is not None else 0
            key = c
            kk = int(node["kind"][i]) if i is not None else -1
            inst = 1 if tier[c] == 5 else 0
        if key not in out:
            out[key] = dict(
                dem=1 if dem else 0,
                lane=2 if inst else (1 if ds <= 1 else 0),
                ctor=1 if kk == 3 else 0,
                cp=1 if key in classproj else 0,
                stmt=1 if key in stmt_names else 0,
                d=dv, first=first[c])
    for c in load:
        add(c, False)
    for c in anyocc:
        if c in load:
            continue
        i = name_id.get(c)
        if i is not None and not node["pr"][i]:
            add(c, True)
    return out

def order(F, target_is_def):
    if target_is_def:
        key = lambda c: (F[c]["ctor"], F[c]["cp"], F[c]["stmt"], -F[c]["d"], F[c]["first"])
    else:
        key = lambda c: (F[c]["dem"], F[c]["lane"], F[c]["stmt"], -F[c]["d"], F[c]["first"])
    return sorted(F, key=key)

def gap_threshold(F):
    pool = [c for c in F if F[c]["dem"] == 0]
    if not pool:
        return None
    ds = sorted({F[c]["d"] for c in pool}, reverse=True)
    if len(ds) == 1:
        return ds[0]
    gaps = [(ds[i] - ds[i + 1], i) for i in range(len(ds) - 1)]
    g, i = max(gaps)
    return ds[i] if g > 0 else ds[-1]

def zoom1(F):
    t = gap_threshold(F)
    return {c for c in F if F[c]["dem"] == 0 and t is not None and F[c]["d"] >= t}

def boundary(F, target_is_def):
    t = gap_threshold(F)
    inc = {c for c in F if F[c]["dem"] == 0 and t is not None and F[c]["d"] >= t}
    lane_side = {c for c in F if F[c]["dem"] == 0 and F[c]["lane"] == 0 and F[c]["stmt"] == 0}
    if target_is_def:
        lane_side = {c for c in lane_side if not (F[c]["ctor"] or F[c]["cp"])}
        if t is not None:
            inc |= {c for c in F if F[c]["dem"] == 1 and F[c]["d"] >= t
                    and not (F[c]["ctor"] or F[c]["cp"])}
    return inc | lane_side
