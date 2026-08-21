"""Inter-rater reliability: Krippendorff's alpha with ordinal weights.

The pre-registration makes this a GATE: alpha >= 0.67 on CAL or no ranking may
be promoted this round. It is computed before TEST is analysed.

Ordinal (not nominal) is the right metric here because the grades 0-4 are
ranked: two raters saying 3 and 4 disagree far less than two saying 0 and 4,
and a nominal alpha would treat those as equally wrong.

Definition (Krippendorff):

    alpha = 1 - Do / De

with a coincidence matrix built from units rated by >= 2 raters, and the
ordinal difference function

    delta^2(c,k) = ( sum_{g=c..k} n_g  -  (n_c + n_k)/2 )^2

Do is observed disagreement, De is what disagreement would be if the same
marginal grade distribution were assigned at random.
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np


def _coincidence(units, categories):
    """Coincidence matrix o[c][k] over units rated by at least two raters."""
    idx = {c: i for i, c in enumerate(categories)}
    n = len(categories)
    o = np.zeros((n, n), dtype=float)
    for vals in units:
        m = len(vals)
        if m < 2:
            continue
        for a in range(m):
            for b in range(m):
                if a == b:
                    continue
                o[idx[vals[a]], idx[vals[b]]] += 1.0 / (m - 1)
    return o


def krippendorff_alpha(units, categories=(0, 1, 2, 3, 4), metric="ordinal"):
    """`units` is an iterable of lists of grades, one list per rated item."""
    units = [list(v) for v in units if len(v) >= 2]
    if not units:
        return {"alpha": None, "n_units": 0}
    cats = list(categories)
    o = _coincidence(units, cats)
    n_c = o.sum(axis=1)
    n = n_c.sum()
    if n <= 1:
        return {"alpha": None, "n_units": len(units)}

    k = len(cats)
    d2 = np.zeros((k, k), dtype=float)
    for a in range(k):
        for b in range(k):
            if metric == "ordinal":
                lo, hi = (a, b) if a <= b else (b, a)
                s = n_c[lo:hi + 1].sum() - (n_c[a] + n_c[b]) / 2.0
                d2[a, b] = s * s
            elif metric == "interval":
                d2[a, b] = (cats[a] - cats[b]) ** 2
            else:                                   # nominal
                d2[a, b] = 0.0 if a == b else 1.0

    do = (o * d2).sum() / n
    de = (np.outer(n_c, n_c) * d2).sum() - (n_c * np.diag(d2) * 1.0).sum()
    de = de / (n * (n - 1))
    alpha = 1.0 - do / de if de > 0 else None
    return {"alpha": float(alpha) if alpha is not None else None,
            "n_units": len(units),
            "n_pairable_values": float(n),
            "Do": float(do), "De": float(de),
            "marginals": {int(cats[i]): float(n_c[i]) for i in range(k)}}


def agreement_report(per_rater, keymap, gate=0.67, bands=None):
    """Full reliability picture for a set of rater files.

    `per_rater` maps rater name -> {proof_id: {"grades": {num: grade}, ...}}.
    Returns alpha overall and per depth band, plus the simple agreement
    statistics that make an alpha interpretable.
    """
    cell = defaultdict(dict)                 # (pid, num) -> rater -> grade
    for rn, rr in per_rater.items():
        for pid, ent in (rr or {}).items():
            for num, g in (ent.get("grades") or {}).items():
                try:
                    cell[(pid, str(num))][rn] = int(g)
                except (TypeError, ValueError):
                    continue

    units, band_units = [], defaultdict(list)
    exact, adj, diffs = [], [], []
    for (pid, num), byr in cell.items():
        vals = list(byr.values())
        if len(vals) < 2:
            continue
        units.append(vals)
        b = (keymap.get(pid) or {}).get("band")
        if b:
            band_units[b].append(vals)
        for a in range(len(vals)):
            for bb in range(a + 1, len(vals)):
                d = abs(vals[a] - vals[bb])
                exact.append(d == 0)
                adj.append(d <= 1)
                diffs.append(d)

    overall = krippendorff_alpha(units)
    out = {
        "alpha_ordinal": overall["alpha"],
        "alpha_nominal": krippendorff_alpha(units, metric="nominal")["alpha"],
        "gate": gate,
        "passes_gate": (overall["alpha"] is not None
                        and overall["alpha"] >= gate),
        "n_units_multi_rated": overall["n_units"],
        "n_pairs": len(exact),
        "ExactAgreement": float(np.mean(exact)) if exact else None,
        "AdjacentAgreement": float(np.mean(adj)) if adj else None,
        "MeanAbsDiff": float(np.mean(diffs)) if diffs else None,
        "diff_histogram": {str(d): int(np.sum(np.array(diffs) == d))
                           for d in range(5)} if diffs else {},
        "marginals": overall.get("marginals"),
        "by_band": {},
    }
    for b, u in sorted(band_units.items()):
        a = krippendorff_alpha(u)
        out["by_band"][b] = {"alpha_ordinal": a["alpha"], "n_units": a["n_units"]}

    # do raters agree about whether a key move is missing entirely?
    mk = defaultdict(list)
    for rn, rr in per_rater.items():
        for pid, ent in (rr or {}).items():
            if "missing_key" in ent:
                mk[pid].append(bool(ent["missing_key"]))
    if mk:
        split = sum(1 for v in mk.values() if 0 < sum(v) < len(v))
        out["missing_key_disagreement_rate"] = split / len(mk)
        out["missing_key_majority_rate"] = (
            sum(1 for v in mk.values() if sum(v) > len(v) / 2) / len(mk))
    return out
