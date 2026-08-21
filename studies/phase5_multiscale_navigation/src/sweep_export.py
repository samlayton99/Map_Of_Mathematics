#!/usr/bin/env python3
"""Build dashboard/data/sweep.json -- the inclusiveness curve.

ONE FIGURE, ONE QUESTION: as the view slides from "show everything" to "show
one thing per proof", what happens to the things worth having?

The x-axis is a single ordered ladder of INCLUSION LEVELS, from most to least
inclusive:

    top_pct at 100 .. 1 percent   (per-proof percentile, always at least one)
    top_k   at 8, 4, 2, 1         (per-proof fixed count)
    cluster_split                 (per-proof ADAPTIVE cut -- one marked point,
                                   not a rung on the ladder, because its size
                                   is chosen per proof rather than dialled)

Every level is scored on the same y-axes for every (universe, ranking) pair:
size, proof coverage, structural glue share, retention of rater-graded KEY
moves, graded precision, mean grade, and the connectivity of the resulting
projection.

Nothing here re-ranks. A level only ever takes a prefix of an already-fixed
ranking, so the whole file is a statement about DISPLAY, never about belief.

Graph metrics are the expensive part (a connected-components pass over up to
18M edges), so they are computed on a declared subset of levels. Every point
carries `has_graph_metrics` and the manifest lists the subset; a level without
graph numbers reports null rather than an interpolated guess.

Writes only `dashboard/data/sweep.json`. It touches nothing else in that
directory.
"""
import json
import os
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

from mathmap_eval import cluster_split as CS       # noqa: E402  (registers policy)
from mathmap_eval import composition as C          # noqa: E402
from mathmap_eval import inclusions as I           # noqa: E402
from mathmap_eval import metrics as M              # noqa: E402
from mathmap_eval import rankings as R             # noqa: E402
from mathmap_eval.corpus import get_corpus         # noqa: E402

OUT = os.path.join(ROOT, "dashboard", "data")
LAB = os.path.join(ROOT, "review", "labels")

UNIVERSES = ["U1", "U1D", "U0"]
PCTS = [100, 75, 50, 40, 30, 25, 20, 15, 10, 7, 5, 3, 2, 1]
TOPKS = [8, 4, 2, 1]

# Levels that also get a connected-components pass. The full grid measured at
# 8.7 min with a 12-of-19 subset, so every level gets one; narrow these sets if
# the grid ever grows past the ~25 min budget. Levels outside them report null
# graph numbers and carry has_graph_metrics = false, never an interpolation.
GRAPH_PCTS = set(PCTS)
GRAPH_TOPKS = set(TOPKS)


def clean(o):
    """NaN/Infinity -> None, recursively.

    Python's json writes bare `NaN`, which is invalid JSON and makes
    JSON.parse throw. Missing numbers become null. (Same sanitizer as
    src/dashboard_export.py; duplicated rather than imported so that this
    script never touches that module while it is running.)
    """
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return None if (f != f or f in (float("inf"), float("-inf"))) else f
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def build_levels():
    """The x-axis ladder, declared most-inclusive first."""
    lv = []
    for p in PCTS:
        lv.append({"id": f"pct_{p}", "label": f"top {p}%", "kind": "percentile",
                   "param": p / 100.0, "param_label": f"{p}%",
                   "has_graph_metrics": p in GRAPH_PCTS,
                   "doc": f"Per proof, the top {p}% of its ranked candidates "
                          f"(always at least one)."})
    for k in TOPKS:
        lv.append({"id": f"topk_{k}", "label": f"top {k}", "kind": "topk",
                   "param": k, "param_label": f"k={k}",
                   "has_graph_metrics": k in GRAPH_TOPKS,
                   "doc": f"Per proof, the {k} highest-ranked candidates."})
    lv.append({"id": "cluster_split",
               "label": f"cluster split ({CS.DEFAULT_METHOD})",
               "kind": "cluster", "param": CS.DEFAULT_METHOD,
               "param_label": CS.DEFAULT_METHOD,
               "has_graph_metrics": True,
               "doc": "Per proof, an ADAPTIVE cut at the ranking's own "
                      "natural boundary: the first two TIE-BLOCKS of the "
                      "lexicographic key, i.e. everything the ranking cannot "
                      "separate from its top choice, plus the next "
                      "indistinguishable stratum. Its size is chosen per "
                      "proof (2 for most, up to 65 where the ranking "
                      "genuinely cannot discriminate), so it is a marked "
                      "point rather than a rung on the ladder. It beats "
                      "fixed top-k at the same mean size by about one graded "
                      "candidate in 154, which is INSIDE the Wilson "
                      "interval -- see reports/CLUSTER_SPLIT.md before "
                      "quoting it as an improvement."})
    return lv


def level_mask(c, base, ranks, keys, level):
    k = level["kind"]
    if k == "percentile":
        return I.get("top_pct").mask(c, base, ranks, pct=level["param"])
    if k == "topk":
        return I.get("top_k").mask(c, base, ranks, k=level["param"])
    if k == "cluster":
        return I.get("cluster_split").mask(c, base, ranks, keys=keys,
                                           method=level["param"])
    raise KeyError(k)


def score_point(c, base, mask, art, n_art, gb, n_key_corpus, want_graph):
    lab = gb >= 0
    adm_lab = mask & lab
    n_adm_lab = int(adm_lab.sum())
    n_key_adm = int((adm_lab & (gb == 4)).sum())
    n_good = int((adm_lab & (gb >= 3)).sum())
    sub = base[mask]
    cat = C.structural_category(c, sub)
    cc = np.bincount(cat, minlength=len(C.STRUCT_CATS))
    tot = max(int(cc.sum()), 1)
    covered = int((np.bincount(art[mask], minlength=n_art) > 0).sum())
    pt = {
        "ViewSize": int(mask.sum()),
        "ViewSizeFraction": float(mask.sum() / max(len(base), 1)),
        "ViewProofsCovered": covered,
        "ViewGlueShare": float(int(cc[0] + cc[1]) / tot),
        "ViewComposition": {a: float(int(cc[i]) / tot)
                            for i, a in enumerate(C.STRUCT_CATS)},
        "ViewKeyRetained": {
            "value": (n_key_adm / n_key_corpus if n_key_corpus
                      else float("nan")),
            "k": n_key_adm, "n": n_key_corpus},
        "ViewPrecisionGraded": {
            "value": (n_good / n_adm_lab if n_adm_lab else float("nan")),
            "k": n_good, "n": n_adm_lab},
        "ViewMeanGrade": (float(gb[adm_lab].mean()) if n_adm_lab
                          else float("nan")),
        "ViewAdmittedLabelled": n_adm_lab,
        "GraphComponents": None,
        "GraphGiantFraction": None,
        "has_graph_metrics": bool(want_graph),
    }
    if want_graph:
        g = M.graph_metrics(c, base, mask)
        pt["GraphComponents"] = int(g["GraphComponents"])
        pt["GraphGiantFraction"] = float(g["GraphGiantFraction"])
        pt["GraphEdges"] = int(g["GraphEdges"])
        pt["GraphSecondLargest"] = int(g["GraphSecondLargest"])
        pt["GraphActiveNodeFraction"] = float(g["GraphActiveNodeFraction"])
    return pt


def main():
    t_all = time.time()
    os.makedirs(OUT, exist_ok=True)
    c = get_corpus()
    keymap = json.load(open(os.path.join(LAB, "keymap.json")))
    grades, label_meta, _mv = C.load_labels(LAB, keymap)
    n_key_corpus = int(sum(1 for g in grades.values() if g == 4))

    levels = build_levels()
    names = R.names()
    print(f"levels: {len(levels)}  rankings: {len(names)}  "
          f"universes: {UNIVERSES}", flush=True)
    print(f"graph metrics on {sum(l['has_graph_metrics'] for l in levels)} "
          f"of {len(levels)} levels", flush=True)

    out = {
        "built": time.strftime("%Y-%m-%d %H:%M"),
        "what_this_is":
            "The inclusiveness curve. One ordered ladder of inclusion levels "
            "from most to least inclusive, scored on the same axes for every "
            "(universe, ranking) pair. Nothing here re-ranks: each level takes "
            "a prefix of a fixed ranking. `cluster_split` is an adaptive "
            "per-proof cut and is a MARKED POINT, not a rung on the ladder.",
        "universes": UNIVERSES,
        "rankings": [{"name": n, "family": R.get(n).family, "doc": R.get(n).doc}
                     for n in names],
        "levels": levels,
        "graph_metric_levels": [l["id"] for l in levels
                                if l["has_graph_metrics"]],
        "graph_metric_note":
            "Connected components over up to 18M edges is the expensive part "
            "of this grid, so the levels that get one are declared above "
            "rather than assumed. In this build that is EVERY level. If the "
            "grid ever outgrows its runtime budget the subset shrinks, and "
            "points outside it report GraphComponents = GraphGiantFraction = "
            "null and carry has_graph_metrics = false. No graph number in "
            "this file is ever interpolated.",
        "cluster_split": {
            "method": CS.DEFAULT_METHOD,
            "doc": CS.split_sizes.__doc__.strip().splitlines()[0],
            "evidence": "reports/CLUSTER_SPLIT.md",
        },
        "labels": {"n_proofs": label_meta["n_proofs_labelled"],
                   "n_candidates": label_meta["n_incidences_labelled"],
                   "n_key": n_key_corpus},
        "metric_doc": {
            "ViewSizeFraction": "Admitted candidates / candidates in the "
                                "universe. The x-axis the points are sorted "
                                "on.",
            "ViewProofsCovered": "Proofs with at least one admitted candidate.",
            "ViewGlueShare": "Share of admitted candidates our OWN structural "
                             "classifier calls glue (logic-only declaration or "
                             "apparatus machinery). A statistic, not a "
                             "judgement.",
            "ViewKeyRetained": "Share of the 0-4 rater-graded KEY (grade 4) "
                               "candidates that survive into the view. "
                               "Denominator is every graded KEY in the "
                               "labelled set, so a universe that never offered "
                               "the candidate is penalised here -- that is "
                               "deliberate.",
            "ViewPrecisionGraded": "Of the admitted candidates that carry a "
                                   "rater grade, the share graded >= 3 (KEY or "
                                   "SUPPORT). Small n; it is measured on the "
                                   "180 labelled proofs only.",
            "ViewMeanGrade": "Mean rater grade of the admitted graded "
                             "candidates, 0-4.",
            "GraphComponents": "Connected components of the projection the "
                               "view draws (targets joined to admitted "
                               "citations).",
            "GraphGiantFraction": "Share of touched declarations in the "
                                  "largest component.",
        },
        "series": {},
    }

    for U in UNIVERSES:
        base = np.where(c.universe(U))[0]
        art = c.inc_artifact[base]
        n_art = int(art.max()) + 1
        gb = CS.grade_array(c, base, grades)
        n_proofs = int((np.bincount(art, minlength=n_art) > 0).sum())
        print(f"\n{U}: {len(base):,} candidates, {n_proofs:,} proofs, "
              f"{int((gb >= 0).sum()):,} graded candidates present", flush=True)
        for nm in names:
            t0 = time.time()
            spec = R.get(nm)
            ranks = spec.ranks_within_proof(c, base)
            keys = spec.keys(c, base)
            pts = []
            for lvl in levels:
                mask = level_mask(c, base, ranks, keys, lvl)
                pt = score_point(c, base, mask, art, n_art, gb, n_key_corpus,
                                 lvl["has_graph_metrics"])
                pt.update(id=lvl["id"], label=lvl["label"], kind=lvl["kind"],
                          param=lvl["param"], param_label=lvl["param_label"])
                pts.append(pt)
                del mask
            # monotone in x: the curve is drawn left (inclusive) to right
            pts.sort(key=lambda p: -p["ViewSizeFraction"])
            cl = next(p for p in pts if p["kind"] == "cluster")
            out["series"][f"{U}|{nm}"] = {
                "universe": U, "ranking": nm, "family": spec.family,
                "n_candidates": int(len(base)), "n_proofs": n_proofs,
                "n_graded_candidates": int((gb >= 0).sum()),
                "points": pts,
                "cluster": {**cl,
                            "MeanAdmittedPerProof": float(
                                cl["ViewSize"] / max(n_proofs, 1))},
            }
            print(f"  {nm:<22} cluster frac={cl['ViewSizeFraction']:.4f} "
                  f"mean/proof={cl['ViewSize'] / max(n_proofs, 1):.2f} "
                  f"key={cl['ViewKeyRetained']['value']:.3f} "
                  f"prec={cl['ViewPrecisionGraded']['value']:.3f} "
                  f"({time.time() - t0:.0f}s)", flush=True)
            del ranks, keys

    try:
        out["git"] = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        out["git"] = "unknown"

    path = os.path.join(OUT, "sweep.json")
    with open(path, "w") as f:
        json.dump(clean(out), f, allow_nan=False)
    print(f"\nwritten {path} ({os.path.getsize(path) / 1e6:.1f} MB) in "
          f"{time.time() - t_all:.0f}s", flush=True)

    # -------- self-check: strict JSON, monotone percentile ladder ---------
    txt = open(path).read()
    assert "NaN" not in txt and "Infinity" not in txt, "non-strict JSON"
    got = json.loads(txt)
    bad = []
    for key, s in got["series"].items():
        pct = [p for p in s["points"] if p["kind"] == "percentile"]
        pct.sort(key=lambda p: -p["param"])
        fr = [p["ViewSizeFraction"] for p in pct]
        if any(b - a > 1e-12 for a, b in zip(fr, fr[1:])):
            bad.append(key)
    assert not bad, f"percentile ladder not monotone for {bad}"
    print(f"self-check ok: strict JSON, {len(got['series'])} series, "
          f"percentile ladder monotone in size fraction", flush=True)


if __name__ == "__main__":
    main()
