"""Metrics, with the naming discipline the audit demands.

Prefixes are load-bearing and must not be mixed:

  Source*   agreement with identifiers the human wrote. NOT keyness.
            A ranking cannot be promoted on Source* alone.
  Role*     descriptive composition of what sits at a rank (e.g. how much is
            glue). A statistic, not a judgement.
  Coverage* what fraction of the ground truth is present in a universe at all.
            A property of candidate generation, not of ranking.
  Graph*    structure of the projection: components, giant, entropy,
            susceptibility, bridge enrichment.
  Semantic* reserved. Requires graded human/rater labels; nothing here
            computes it, and no other metric may be reported under this name.
"""
from __future__ import annotations

from collections import Counter, defaultdict

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

DEPTH_BANDS = [(0, 11), (11, 26), (26, 51), (51, 76), (76, 126), (126, 10**9)]
BAND_LABELS = ["0-10", "11-25", "26-50", "51-75", "76-125", "126+"]


def _band(d):
    for lab, (lo, hi) in zip(BAND_LABELS, DEPTH_BANDS):
        if lo <= d < hi:
            return lab
    return BAND_LABELS[-1]


# ------------------------------------------------------------ Source*
def source_metrics(c, evalset, ranks_by_pos, ks=(1, 2, 4, 8)):
    """Agreement of the ranking with human-written citations.

    ranks_by_pos: dict incidence-position -> rank within its proof.
    """
    hit1, mrr = [], []
    rec = {k: [] for k in ks}
    per_band = defaultdict(lambda: {"hit1": [], "rec4": []})
    for ai, pl, gt, dth in evalset:
        ordered = sorted(pl, key=lambda p: ranks_by_pos[p])
        dd = [c.inc_decl[p] for p in ordered]
        pos = {d: j for j, d in enumerate(dd)}
        hits = sorted(pos[g] for g in gt if g in pos)
        h1 = bool(dd and dd[0] in gt)
        hit1.append(h1)
        mrr.append(1.0 / (hits[0] + 1) if hits else 0.0)
        for k in ks:
            rec[k].append(len([h for h in hits if h < k]) / len(gt))
        b = _band(dth)
        per_band[b]["hit1"].append(h1)
        per_band[b]["rec4"].append(len([h for h in hits if h < 4]) / len(gt))
    return {
        "SourceHit@1": float(np.mean(hit1)),
        "SourceMRR": float(np.mean(mrr)),
        **{f"SourceRecall@{k}": float(np.mean(rec[k])) for k in ks},
        "by_target_depth": {b: {"SourceHit@1": float(np.mean(v["hit1"])),
                                "SourceRecall@4": float(np.mean(v["rec4"])),
                                "n": len(v["hit1"])}
                            for b, v in sorted(per_band.items())},
        "n_proofs": len(evalset),
    }


# -------------------------------------------------------------- Role*
def role_metrics(c, evalset, ranks_by_pos):
    """What KIND of thing sits at rank 1, descriptively, by depth."""
    at1 = Counter()
    per_band = defaultdict(Counter)
    for ai, pl, gt, dth in evalset:
        top = min(pl, key=lambda p: ranks_by_pos[p])
        grp = str(c.kind_group(np.array([c.inc_decl[top]]))[0])
        lab = "glue" if c.inc_glue[top] else grp
        at1[lab] += 1
        per_band[_band(dth)][lab] += 1
    tot = sum(at1.values())
    return {
        "RoleAt1": {k: v / tot for k, v in at1.items()},
        "RoleGlueAt1": at1.get("glue", 0) / tot,
        "by_target_depth": {b: {k: v / sum(cc.values()) for k, v in cc.items()}
                            for b, cc in sorted(per_band.items())},
    }


# ---------------------------------------------------------- Coverage*
def coverage_metrics(c, universe="U1"):
    """How much of what humans wrote is present in a universe AT ALL.

    A property of candidate generation. Reported by declaration kind, because
    the load-bearing filter behaves very differently for theorems and
    definitions.
    """
    base_all = np.where(c.universe("U0"))[0]
    base_u = np.where(c.universe(universe))[0]
    by_art_all, by_art_u = defaultdict(set), defaultdict(set)
    for p in base_all:
        by_art_all[c.inc_artifact[p]].add(c.inc_decl[p])
    for p in base_u:
        by_art_u[c.inc_artifact[p]].add(c.inc_decl[p])
    stat = defaultdict(Counter)
    for nm, refs in c.source_refs.items():
        di = c.name_to_id.get(nm)
        ai = c.art_of_decl.get(di) if di is not None else None
        if ai is None or ai not in by_art_u:
            continue
        for r in refs:
            ri = c.name_to_id.get(r)
            if ri is None or ri == di:
                continue
            g = str(c.kind_group(np.array([ri]))[0])
            stat[g]["written"] += 1
            if ri in by_art_all[ai]:
                stat[g]["in_record"] += 1
            if ri in by_art_u[ai]:
                stat[g]["in_universe"] += 1
    out = {}
    for g, cc in stat.items():
        out[g] = {"written": cc["written"], "in_record": cc["in_record"],
                  "in_universe": cc["in_universe"],
                  "CoverageInUniverse": cc["in_universe"] / max(cc["written"], 1)}
    tw = sum(v["written"] for v in out.values())
    tu = sum(v["in_universe"] for v in out.values())
    out["ALL"] = {"written": tw, "in_universe": tu,
                  "CoverageInUniverse": tu / max(tw, 1)}
    return out


# ------------------------------------------------------------- Graph*
def graph_metrics(c, base, mask, exclude_virtual_root=True):
    """Structure of one projection. The virtual root is excluded (audit)."""
    sel = base[mask]
    u = c.inc_target[sel]
    v = c.inc_decl[sel]
    touched = np.unique(np.concatenate([c.inc_target[base], c.inc_decl[base]]))
    nid = -np.ones(c.n_nodes, dtype=np.int64)
    nid[touched] = np.arange(len(touched))
    N = len(touched)
    g = sp.coo_matrix((np.ones(len(u), np.int8), (nid[u], nid[v])), shape=(N, N))
    _, lab = connected_components(g, directed=False)
    sizes = np.bincount(lab)
    sizes = sizes[sizes > 0]
    p = sizes / sizes.sum()
    giant = sizes.max()
    non_giant = sizes[sizes != giant]
    chi = float((non_giant ** 2).sum() / non_giant.sum()) if len(non_giant) else 0.0
    active = len(np.unique(np.concatenate([nid[u], nid[v]]))) if len(u) else 0
    return {
        "GraphEdges": int(len(sel)),
        "GraphComponents": int(len(sizes)),
        "GraphGiantFraction": float(giant / sizes.sum()),
        "GraphSecondLargest": int(np.sort(sizes)[-2]) if len(sizes) > 1 else 0,
        "GraphEntropy": float(-(p * np.log(p)).sum()),
        "GraphSusceptibility": chi,
        "GraphActiveNodeFraction": float(active / N),
    }


def bridge_enrichment(c, base, ranks, kmax=4, boot=0, seed=7):
    """Enrichment of each declaration kind among component-CROSSING edges.

    Enrichment(a) = P(a | crosses prior components) / P(a | eligible now).
    ~1.0 means a kind's merge share is its base rate, i.e. no evidence that it
    bridges. Mergers are batch-invariant: the prior partition is frozen and the
    quotient graph over the whole tied batch defines the mergers, so no single
    edge is credited by iteration order.
    """
    touched = np.unique(np.concatenate([c.inc_target[base], c.inc_decl[base]]))
    nid = -np.ones(c.n_nodes, dtype=np.int64)
    nid[touched] = np.arange(len(touched))
    N = len(touched)
    grp = c.kind_group(c.inc_decl[base])
    grp = np.where(c.inc_glue[base], "glue", grp.astype(str))
    acc_u, acc_v = [], []
    lab = np.arange(N)
    rows = []
    rng = np.random.default_rng(seed)
    for k in range(kmax):
        sel = ranks == k
        u, v = nid[c.inc_target[base[sel]]], nid[c.inc_decl[base[sel]]]
        kinds = grp[sel]
        crosses = lab[u] != lab[v]
        elig = Counter(kinds)
        cross = Counter(kinds[crosses])
        te, tc = sum(elig.values()), sum(cross.values())
        ent = {}
        for a in set(elig) | set(cross):
            pe = elig[a] / te if te else 0.0
            pc = cross[a] / tc if tc else 0.0
            e = {"p_eligible": pe, "p_crossing": pc,
                 "enrichment": (pc / pe) if pe else float("nan")}
            if boot:
                vals = []
                m = len(kinds)
                for _ in range(boot):
                    ii = rng.integers(0, m, m)
                    e2 = (kinds[ii] == a).mean()
                    cc = crosses[ii]
                    c2 = ((kinds[ii] == a) & cc).sum() / max(cc.sum(), 1)
                    if e2 > 0:
                        vals.append(c2 / e2)
                if vals:
                    e["ci95"] = [float(np.percentile(vals, 2.5)),
                                 float(np.percentile(vals, 97.5))]
            ent[a] = e
        # batch-invariant merge count
        if crosses.any():
            q = sp.coo_matrix((np.ones(int(crosses.sum()), np.int8),
                               (lab[u][crosses], lab[v][crosses])), shape=(N, N))
            _, ql = connected_components(q, directed=False)
            inv = np.unique(np.concatenate([lab[u][crosses], lab[v][crosses]]))
            gg = defaultdict(list)
            for x in inv:
                gg[ql[x]].append(x)
            elim = sum(len(g) - 1 for g in gg.values() if len(g) > 1)
        else:
            elim = 0
        acc_u.append(u); acc_v.append(v)
        au, av = np.concatenate(acc_u), np.concatenate(acc_v)
        _, lab = connected_components(
            sp.coo_matrix((np.ones(len(au), np.int8), (au, av)), shape=(N, N)),
            directed=False)
        sizes = np.bincount(lab); sizes = sizes[sizes > 0]
        rows.append({"k": k + 1, "eligible": int(te), "crossing": int(tc),
                     "components_eliminated": int(elim),
                     "components": int(len(sizes)),
                     "giant": float(sizes.max() / sizes.sum()),
                     "enrichment": ent})
    return rows
