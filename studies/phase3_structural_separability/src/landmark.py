#!/usr/bin/env python3
"""Question B: theorem-local landmark ranking.

Builds the 24-proof stratified sample (from the existing Phase 2 review bundle,
selected BEFORE model outputs are inspected, fixed seed), computes theorem-local
features for every P2-support candidate, produces rankings from eight methods,
and scores them against explicitly-marked PROXY labels (P4/P5-derived — note
the circularity caveat: proxies favor P4/P5-based methods; decisive evidence is
the user/agent review, not these numbers).
"""
import os, json, glob, math
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
STUDY_DIR = os.path.join(ROOT, "studies")
REVIEW_DIR = os.path.join(ROOT, "review")
SEED = 20260819
LAM = 1.0

import sys
sys.path.insert(0, os.path.join(ROOT, "analysis"))
from characterize import dedup_events, classify_style  # noqa: E402


def machinery_probability():
    """Calibrated logistic on the typed track (best QA model), fit on all
    evaluated nodes; probabilities for every node."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    from sklearn.calibration import CalibratedClassifierCV
    from models_qa import prep
    nodes = pd.read_csv(os.path.join(DATA, "node_inventory.csv")).set_index("name")
    typed = pd.read_csv(os.path.join(DATA, "feature_matrix_typed.csv"), index_col=0)
    ev = nodes[nodes.p3_evaluated == 1]
    names = [n for n in ev.index if n in typed.index]
    X = prep(typed.loc[names]); y = ev.loc[names].p3_any.values
    base = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000, random_state=SEED))
    cal = CalibratedClassifierCV(base, cv=5, method="sigmoid").fit(X, y)
    allX = prep(typed)
    prob = pd.Series(cal.predict_proba(allX)[:, 1], index=typed.index)
    return prob


def select_sample():
    """24 proofs, 4/file, stratified by (style group, size), seeded, from the
    committed review bundle manifest."""
    rng = np.random.default_rng(SEED)
    manifest = []
    for fdir in sorted(glob.glob(os.path.join(REVIEW_DIR, "*"))):
        if not os.path.isdir(fdir):
            continue
        fname = os.path.basename(fdir)
        cands = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(fdir, "*.md")))
        s = json.load(open(os.path.join(STUDY_DIR, fname + ".study.json")))
        rows = {d["name"]: d for d in s["declStudies"]}
        events = dedup_events(s["useEvents"])
        by_decl = {}
        for e in events:
            by_decl.setdefault(e["decl"], []).append(e)
        info = []
        for c in cands:
            d = rows.get(c)
            if not d:
                continue
            style = classify_style(c, by_decl, None)
            info.append((c, "term" if style == "term" else "tactic", d["sizes"]["valueSize"]))
        # strata: term-small, term-large, tactic-small, tactic-large (fallback: fill)
        picked = []
        for grp in ("term", "tactic"):
            g = sorted([i for i in info if i[1] == grp], key=lambda t: (t[2], t[0]))
            if g:
                picked.append(g[0][0])
                if len(g) > 1:
                    picked.append(g[-1][0])
        pool = [i[0] for i in info if i[0] not in picked]
        while len(picked) < 4 and pool:
            picked.append(pool[int(rng.integers(len(pool)))])
            pool.remove(picked[-1])
        for c in picked[:4]:
            manifest.append({"file": fname, "decl": c})
    with open(os.path.join(DATA, "landmark_sample_manifest.json"), "w") as f:
        json.dump({"seed": SEED, "criteria": "4/file: smallest+largest term proof, smallest+largest tactic proof (by proof-term size, name tiebreak), random fill",
                   "proofs": manifest}, f, indent=1)
    return manifest


def local_features(s, decl_row, events_by_decl):
    """Per-candidate theorem-local features for one proof."""
    name = decl_row["name"]
    ref = {d["name"]: d for d in s["referencedDecls"] if "error" not in d}
    support = decl_row["p2_supportBody"]
    stmt = set(decl_row["p2_supportType"])
    apps = decl_row["p4_apps"] if isinstance(decl_row["p4_apps"], list) else []
    total_apps = len(apps) or 1
    mult = {}
    for occ in decl_row["p1_bodyRefs"]:
        mult[occ["name"]] = mult.get(occ["name"], 0) + 1
    by_head = {}
    for a in apps:
        by_head.setdefault(a["head"], []).append(a)
    attributed = {a["decl"] for e in events_by_decl.get(name, []) for a in e["attributions"]}
    feats = {}
    for v in support:
        occ = by_head.get(v, [])
        depths = [a["depth"] for a in occ]
        feats[v] = {
            "multiplicity": mult.get(v, 0),
            "in_statement": int(v in stmt),
            "app_head_count": len(occ),
            "app_head_frac": len(occ) / total_apps,
            "min_depth": min(depths) if depths else -1,
            "prop_result_frac": (np.mean([a["resultIsProp"] for a in occ]) if occ else 0.0),
            "result_ok_frac": (np.mean([a["resultOk"] for a in occ]) if occ else None),  # None = missingness explicit
            "p5_attributed": int(v in attributed),
            "p3_classified": int(bool(ref.get(v, {}).get("classification"))),
            "p3_classes": ",".join(ref.get(v, {}).get("classification", [])),
        }
    return feats


def zscore(vals):
    a = np.array(vals, dtype=float)
    sd = a.std() or 1.0
    return (a - a.mean()) / sd


def rank_methods(feats, prob, pagerank_use):
    cands = list(feats)
    f = pd.DataFrame(feats).T
    for c in ("multiplicity", "in_statement", "app_head_count", "app_head_frac",
              "min_depth", "prop_result_frac", "p5_attributed", "p3_classified"):
        f[c] = pd.to_numeric(f[c], errors="coerce").fillna(0.0)
    inv_depth = [1.0 / (1 + d) if d >= 0 else 0.0 for d in f.min_depth]
    salience = (zscore(np.log1p(f.multiplicity)) + zscore(f.app_head_count > 0)
                + zscore(f.in_statement) + zscore(inv_depth) + zscore(f.p5_attributed)) / 5
    mach = np.array([prob.get(v, 0.5) for v in cands])
    pr = np.array([pagerank_use.get(v, 0.0) for v in cands])
    route_mask = (f.app_head_count > 0) & (f.prop_result_frac > 0.5) & (f.p3_classified == 0)
    methods = {
        "M_p2_order": list(cands),
        "M_multiplicity": [c for _, c in sorted(zip(-f.multiplicity, cands))],
        "M_global_pagerank": [c for _, c in sorted(zip(-pr, cands))],
        "M_p3_filter": [c for _, c in sorted(zip(list(zip(f.p3_classified, range(len(cands)))), cands))],
        "M_p4_route": [c for _, c in sorted(zip(list(zip(~route_mask, f.min_depth.replace(-1, 999))), cands))],
        "M_local_salience": [c for _, c in sorted(zip(-salience, cands))],
        "M_combined": [c for _, c in sorted(zip(-(salience - LAM * mach), cands))],
        "M_hybrid": [c for _, c in sorted(zip(list(zip(~(route_mask | (f.p5_attributed == 1)),
                                                       -(salience - LAM * mach))), cands))],
    }
    scores = {"salience": dict(zip(cands, salience.round(3))),
              "machineryProb": dict(zip(cands, mach.round(3)))}
    return methods, scores, f


def proxy_labels(f):
    """PROXY ONLY: key = P4-route head at shallow depth or P5-attributed.
    Circular for P4/P5-based methods — documented."""
    route = f[(f.app_head_count > 0) & (f.prop_result_frac > 0.5) & (f.p3_classified == 0)]
    med = route.min_depth.median() if len(route) else 0
    key = set(route[route.min_depth <= med].index) | set(f[f.p5_attributed == 1].index)
    key -= set(f[f.p3_classified == 1].index)
    return key


def ndcg_at_k(ranking, grades, k=5):
    dcg = sum(grades.get(v, 0) / math.log2(i + 2) for i, v in enumerate(ranking[:k]))
    ideal = sorted(grades.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal)) or 1.0
    return dcg / idcg


def main():
    prob = machinery_probability()
    strict = pd.read_csv(os.path.join(DATA, "feature_matrix_strict.csv"), index_col=0)
    pagerank_use = strict.pagerank_use.to_dict()
    manifest = select_sample()
    out = {"lambda": LAM, "proxy_note":
           "proxy_key labels derive from P4-route depth and P5 attribution; they "
           "structurally favor M_p4_route/M_hybrid and are DESCRIPTIVE ONLY — "
           "decisive usefulness evidence is the user/agent review.",
           "proofs": {}}
    metrics = []
    for item in manifest:
        s = json.load(open(os.path.join(STUDY_DIR, item["file"] + ".study.json")))
        rows = {d["name"]: d for d in s["declStudies"]}
        events = dedup_events(s["useEvents"])
        by_decl = {}
        for e in events:
            by_decl.setdefault(e["decl"], []).append(e)
        d = rows[item["decl"]]
        feats = local_features(s, d, by_decl)
        if not feats:
            continue
        methods, scores, f = rank_methods(feats, prob, pagerank_use)
        key = proxy_labels(f)
        grades = {v: (2 if v in key else (0 if feats[v]["p3_classified"] else 1)) for v in feats}
        m = {"file": item["file"], "n_candidates": len(feats), "proxy_keys": sorted(key)}
        for name, ranking in methods.items():
            top5 = ranking[:5]
            m[name] = {
                "p_at_5": round(len([v for v in top5 if v in key]) / min(5, len(ranking)), 3),
                "recall_key_at_5": round(len([v for v in top5 if v in key]) / (len(key) or 1), 3),
                "ndcg_at_5": round(ndcg_at_k(ranking, grades), 3),
                "scaffolding_at_5": round(np.mean([feats[v]["p3_classified"] for v in top5]), 3),
            }
        metrics.append(m)
        out["proofs"][item["decl"]] = {
            "file": item["file"], "rankings": {k: v[:10] for k, v in methods.items()},
            "features": feats, "scores": scores, "proxy_keys": sorted(key)}
    out["metrics_per_proof"] = metrics
    med = {}
    for meth in ["M_p2_order", "M_multiplicity", "M_global_pagerank", "M_p3_filter",
                 "M_p4_route", "M_local_salience", "M_combined", "M_hybrid"]:
        med[meth] = {k: round(float(np.median([m[meth][k] for m in metrics])), 3)
                     for k in ("p_at_5", "recall_key_at_5", "ndcg_at_5", "scaffolding_at_5")}
    out["median_metrics_proxy"] = med
    with open(os.path.join(DATA, "rankings.json"), "w") as f_:
        json.dump(out, f_, indent=1, sort_keys=True)
    print(json.dumps(med, indent=1))
    print("proofs analyzed:", len(metrics))


if __name__ == "__main__":
    main()
