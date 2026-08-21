"""Navigation cleanliness metrics (constitution v2, doc 06A).

The v2 constitution demotes Key@1 from primary objective and replaces it with a
Pareto tradeoff:

    NavigationCleanliness   share of what you can SEE that is a useful landmark
                            (grade >= 2: core, major/support, or legitimate
                            assembly)
    LegitimateCoverage      share of all useful landmarks in the proof that are
                            visible
    MajorMathCoverage       the same, for grade >= 3 only, so a ranking cannot
                            win by being clean and bland

The binary at grade 2 is deliberately less subjective than "which single move
was best": it asks only whether a thing is acceptable to show at some
resolution, not whether it is THE move.

Why this can separate rankings when Key@1 could not: Key@1 reads one item per
proof, so 180 proofs give 180 observations. These metrics read every graded
candidate, giving 2,419 -- roughly 13x the resolution per proof.

Everything here is computed on the DEVELOPMENT label set. It is evidence for
choosing what to seal, not a sealed result.
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np

from .composition import _wilson
from .metrics import BAND_LABELS, _band

USEFUL = 2          # grade >= USEFUL is a useful visible landmark
MAJOR = 3           # grade >= MAJOR is substantive mathematics


def _ap(labels):
    """Average precision of a binary sequence already in ranked order."""
    labels = np.asarray(labels, dtype=bool)
    n_pos = int(labels.sum())
    if n_pos == 0:
        return None
    hits = np.cumsum(labels)
    prec = hits / np.arange(1, len(labels) + 1)
    return float(prec[labels].sum() / n_pos)


def per_proof_orders(c, base, ranks, grades_by_inc, keymap):
    """For each labelled proof: graded labels in this ranking's order."""
    pos = {int(p): i for i, p in enumerate(base)}
    out = []
    for pid, meta in keymap.items():
        items = {int(n): int(i) for n, i in meta["items"].items()}
        live = [(n, i) for n, i in items.items()
                if i in pos and i in grades_by_inc]
        if not live:
            continue
        live.sort(key=lambda ni: ranks[pos[ni[1]]])
        g = np.array([grades_by_inc[i] for _, i in live])
        out.append({"pid": pid, "band": meta["band"], "depth": meta["depth"],
                    "grades": g, "incidences": [i for _, i in live]})
    return out


def navigation_metrics(c, base, ranks, grades_by_inc, keymap,
                       defect_budgets=(0.01, 0.025, 0.05, 0.10),
                       coverage_targets=(0.50, 0.75, 0.90, 0.95)):
    """The v2 primary objective, on the development labels."""
    proofs = per_proof_orders(c, base, ranks, grades_by_inc, keymap)
    if not proofs:
        return {}
    maxlen = max(len(p["grades"]) for p in proofs)

    # ---- pooled prefix sweep: theta = per-proof top-k -------------------
    curve = []
    tot_useful = sum(int((p["grades"] >= USEFUL).sum()) for p in proofs)
    tot_major = sum(int((p["grades"] >= MAJOR).sum()) for p in proofs)
    for k in range(1, maxlen + 1):
        vis = useful = major = 0
        for p in proofs:
            g = p["grades"][:k]
            vis += len(g)
            useful += int((g >= USEFUL).sum())
            major += int((g >= MAJOR).sum())
        curve.append({
            "k": k,
            "visible": vis,
            "NavigationCleanliness": useful / vis if vis else None,
            "NavigationDefectRate": 1 - useful / vis if vis else None,
            "LegitimateCoverage": useful / tot_useful if tot_useful else None,
            "MajorMathCoverage": major / tot_major if tot_major else None,
        })

    def at_defect(budget):
        """Most coverage reachable while defect rate stays within budget."""
        ok = [r for r in curve if r["NavigationDefectRate"] is not None
              and r["NavigationDefectRate"] <= budget]
        if not ok:
            return None
        best = max(ok, key=lambda r: r["LegitimateCoverage"])
        return {"k": best["k"], "LegitimateCoverage": best["LegitimateCoverage"],
                "MajorMathCoverage": best["MajorMathCoverage"],
                "NavigationDefectRate": best["NavigationDefectRate"]}

    def at_coverage(target):
        """Cleanliness at the first k reaching a legitimate-coverage target."""
        ok = [r for r in curve if r["LegitimateCoverage"] is not None
              and r["LegitimateCoverage"] >= target]
        if not ok:
            return None
        first = min(ok, key=lambda r: r["k"])
        return {"k": first["k"],
                "NavigationCleanliness": first["NavigationCleanliness"],
                "MajorMathCoverage": first["MajorMathCoverage"]}

    # ---- average precision ---------------------------------------------
    aps = [_ap(p["grades"] >= USEFUL) for p in proofs]
    aps = [a for a in aps if a is not None]
    aps_major = [_ap(p["grades"] >= MAJOR) for p in proofs]
    aps_major = [a for a in aps_major if a is not None]
    # bad-edge demotion: reverse the order, positives are defects
    aps_bad = [_ap((p["grades"][::-1] <= 1)) for p in proofs]
    aps_bad = [a for a in aps_bad if a is not None]

    # ---- by depth band ---------------------------------------------------
    by_band = {}
    for b in BAND_LABELS:
        sel = [p for p in proofs if p["band"] == b]
        if not sel:
            continue
        tu = sum(int((p["grades"] >= USEFUL).sum()) for p in sel)
        row = {"n_proofs": len(sel), "n_candidates": sum(len(p["grades"])
                                                         for p in sel)}
        for k in (1, 2, 4):
            vis = useful = 0
            for p in sel:
                g = p["grades"][:k]
                vis += len(g)
                useful += int((g >= USEFUL).sum())
            row[f"NavigationCleanliness@{k}"] = useful / vis if vis else None
            row[f"LegitimateCoverage@{k}"] = useful / tu if tu else None
        a = [_ap(p["grades"] >= USEFUL) for p in sel]
        a = [x for x in a if x is not None]
        row["NavigationAP"] = float(np.mean(a)) if a else None
        # base rate: what a random order would achieve
        allg = np.concatenate([p["grades"] for p in sel])
        row["BaseRateUseful"] = float((allg >= USEFUL).mean())
        by_band[b] = row

    allg = np.concatenate([p["grades"] for p in proofs])
    base_rate = float((allg >= USEFUL).mean())
    return {
        "n_proofs": len(proofs),
        "n_candidates": int(len(allg)),
        "BaseRateUseful": base_rate,
        "BaseRateMajor": float((allg >= MAJOR).mean()),
        "NavigationAP": float(np.mean(aps)) if aps else None,
        "NavigationAPLift": (float(np.mean(aps)) / base_rate) if aps else None,
        "MajorAP": float(np.mean(aps_major)) if aps_major else None,
        "BadEdgeDemotionAP": float(np.mean(aps_bad)) if aps_bad else None,
        "curve": curve,
        "coverage_at_defect_budget": {str(b): at_defect(b)
                                      for b in defect_budgets},
        "cleanliness_at_coverage": {str(t): at_coverage(t)
                                    for t in coverage_targets},
        "by_target_depth": by_band,
    }


def gradient_quality(c, base, ranks, grades_by_inc, keymap, spec, nbins=10):
    """Does usefulness decline sensibly as the global score opens?

    Bins the ranking's GLOBAL order into equal-mass bins over the labelled
    candidates and reports P(useful | bin). A ranking whose global scale means
    anything should show this decreasing monotonically.
    """
    pos = {int(p): i for i, p in enumerate(base)}
    inc = [i for m in keymap.values() for i in
           (int(x) for x in m["items"].values())
           if i in pos and i in grades_by_inc]
    if len(inc) < nbins * 5:
        return {}
    keys = spec.keys(c, base)
    order = np.lexsort(tuple(reversed(keys)))
    globrank = np.empty(len(base), dtype=np.int64)
    globrank[order] = np.arange(len(base))
    gr = np.array([globrank[pos[i]] for i in inc])
    g = np.array([grades_by_inc[i] for i in inc])
    o = np.argsort(gr)
    g = g[o]
    bins = np.array_split(g, nbins)
    rows = [{"bin": j + 1, "n": len(b),
             "P_useful": float((b >= USEFUL).mean()),
             "P_major": float((b >= MAJOR).mean()),
             "ci95_useful": _wilson(int((b >= USEFUL).sum()), len(b))}
            for j, b in enumerate(bins)]
    pu = [r["P_useful"] for r in rows]
    violations = sum(1 for j in range(len(pu) - 1) if pu[j + 1] > pu[j] + 0.02)
    # cross-depth calibration: same bins, per band
    band_of = {}
    for m in keymap.values():
        for x in m["items"].values():
            band_of[int(x)] = m["band"]
    bands = np.array([band_of.get(i, "?") for i in inc])[o]
    # CrossDepthCalibrationGap: does a given SCORE BIN mean the same thing at
    # every target depth? It must be measured WITHIN a bin -- comparing the
    # marginal P(useful | band) instead is ranking-independent and produces the
    # same number for every ranking, including random.
    edges = np.array_split(np.arange(len(g)), nbins)
    gaps = []
    per_bin_band = []
    for j, idx in enumerate(edges):
        row = {}
        for b in BAND_LABELS:
            sel = idx[bands[idx] == b]
            if len(sel) < 15:
                continue
            row[b] = float((g[sel] >= USEFUL).mean())
        per_bin_band.append({"bin": j + 1, "by_band": row,
                             "gap": (max(row.values()) - min(row.values()))
                             if len(row) > 1 else None})
        if len(row) > 1:
            gaps.append(max(row.values()) - min(row.values()))
    gap = float(np.mean(gaps)) if gaps else None
    per_band = {}
    for b in BAND_LABELS:
        sel = bands == b
        if sel.sum() >= 20:
            per_band[b] = float((g[sel] >= USEFUL).mean())
    return {"bins": rows, "GradientViolationRate": violations / max(len(pu) - 1, 1),
            "GradientMonotone": violations == 0,
            "P_useful_top_bin": pu[0], "P_useful_bottom_bin": pu[-1],
            "GradientSpread": pu[0] - pu[-1],
            "CrossDepthCalibrationGap": gap,
            "per_bin_by_band": per_bin_band,
            "P_useful_by_band": per_band}
