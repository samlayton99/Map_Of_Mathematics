#!/usr/bin/env python3
"""Question A: no-name structural separability of P3 infrastructure classes.

Populations:
  primary    = stored & p3-evaluated nodes (full in+out structure observed)
  sensitivity= all p3-evaluated nodes (includes shallow; boundary caveats)

Tracks: strict topology-only features; typed formal-occurrence features.
Models: prevalence, degree threshold, logistic regression, shallow tree,
        random-forest ceiling (labeled as ceiling only).
Splits: transductive stratified CV, grouped-by-file CV, leave-one-domain-out.
Controls: degree-matched subsample, within-domain label permutation test.
"""
import os, json, warnings
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, GroupKFold
from sklearn.metrics import (roc_auc_score, average_precision_score,
                             balanced_accuracy_score, f1_score, brier_score_loss)
from build_graph import P3_CLASSES

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
SEED = 20260819
rng = np.random.default_rng(SEED)

DEGREE_COLS = ["in_deg", "out_deg", "deg", "in_wdeg", "out_wdeg"]

# Target-defining leakage guards (core/04 §4): the typed track's stmt/body split
# does not encode the env instance/projection tables or name suffixes, so no
# column is target-defining; asserted structurally in tests instead.


def load():
    nodes = pd.read_csv(os.path.join(DATA, "node_inventory.csv")).set_index("name")
    strict = pd.read_csv(os.path.join(DATA, "feature_matrix_strict.csv"), index_col=0)
    typed = pd.read_csv(os.path.join(DATA, "feature_matrix_typed.csv"), index_col=0)
    assert not set(nodes.columns) & set(strict.columns), "label/feature leakage"
    nodes["primary_file"] = nodes.files.str.split("|").str[0]
    return nodes, strict, typed


def prep(X: pd.DataFrame) -> pd.DataFrame:
    Xl = X.copy()
    for c in Xl.columns:
        if Xl[c].max() > 50:  # heavy-tailed counts
            Xl[c] = np.log1p(Xl[c].clip(lower=0))
    return Xl.fillna(0)


def models():
    return {
        "logistic": make_pipeline(StandardScaler(),
                                  LogisticRegression(C=1.0, max_iter=2000, random_state=SEED)),
        "tree_d4": DecisionTreeClassifier(max_depth=4, random_state=SEED,
                                          class_weight="balanced"),
        "rf_ceiling": RandomForestClassifier(n_estimators=300, random_state=SEED,
                                             class_weight="balanced", n_jobs=-1),
    }


def eval_split(X, y, tr, te, model):
    m = model.fit(X.iloc[tr], y[tr])
    p = m.predict_proba(X.iloc[te])[:, 1]
    ptr = m.predict_proba(X.iloc[tr])[:, 1]
    # threshold chosen on training data (max F1)
    ths = np.unique(np.quantile(ptr, np.linspace(0.05, 0.95, 19)))
    best_t = max(ths, key=lambda t: f1_score(y[tr], ptr >= t, zero_division=0))
    yhat = p >= best_t
    if len(np.unique(y[te])) < 2:
        return None
    return {
        "roc_auc": roc_auc_score(y[te], p),
        "pr_auc": average_precision_score(y[te], p),
        "bal_acc": balanced_accuracy_score(y[te], yhat),
        "f1": f1_score(y[te], yhat, zero_division=0),
        "brier": brier_score_loss(y[te], p),
        "n_test": int(len(te)), "pos_test": int(y[te].sum()),
    }


def agg(results):
    if not results:
        return None
    keys = [k for k in results[0] if k not in ("n_test", "pos_test")]
    return {k: round(float(np.mean([r[k] for r in results])), 4) for k in keys} | \
           {"n_folds": len(results)}


def run_target(X, y, groups, label, track, population, out):
    """All splits and models for one (features, target)."""
    Xp = prep(X)
    prevalence = float(np.mean(y))
    entry = {"prevalence": round(prevalence, 4), "n": int(len(y)), "pos": int(y.sum())}
    if y.sum() < 10 or y.sum() > len(y) - 10:
        entry["skipped"] = "underpowered (<10 in a class)"
        out[f"{population}|{track}|{label}"] = entry
        return
    # degree-only baseline: logistic on degree columns only
    degcols = [c for c in DEGREE_COLS if c in Xp.columns]
    for mname, model in models().items():
        for split, splitname in [("transductive", "transductive"),
                                 ("grouped", "grouped_file"), ("lodo", "lodo")]:
            res = []
            if split == "transductive":
                cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
                folds = cv.split(Xp, y)
            elif split == "grouped":
                cv = GroupKFold(n_splits=min(6, len(set(groups))))
                folds = cv.split(Xp, y, groups)
            else:
                doms = sorted(set(groups))
                folds = (( np.where(groups != d)[0], np.where(groups == d)[0]) for d in doms)
            for tr, te in folds:
                r = eval_split(Xp, y, tr, te, model)
                if r:
                    res.append(r)
            entry[f"{mname}|{splitname}"] = agg(res)
    # degree-only logistic (all splits summarized on grouped)
    cv = GroupKFold(n_splits=min(6, len(set(groups))))
    res = [r for tr, te in cv.split(Xp[degcols], y, groups)
           if (r := eval_split(Xp[degcols], y, tr, te, models()["logistic"]))]
    entry["degree_only_logistic|grouped_file"] = agg(res)
    # permutation test (within-domain shuffles, logistic, grouped split)
    perm_aucs = []
    for _ in range(30):
        yp = y.copy()
        for d in set(groups):
            m = groups == d
            yp[m] = rng.permutation(yp[m])
        res = [r["roc_auc"] for tr, te in cv.split(Xp, yp, groups)
               if (r := eval_split(Xp, yp, tr, te, models()["logistic"]))]
        if res:
            perm_aucs.append(float(np.mean(res)))
    entry["permutation_auc_mean"] = round(float(np.mean(perm_aucs)), 4) if perm_aucs else None
    entry["permutation_auc_p95"] = round(float(np.quantile(perm_aucs, 0.95)), 4) if perm_aucs else None
    out[f"{population}|{track}|{label}"] = entry


def degree_matched_control(X, y, out, track, population):
    """Match pos/neg on log-degree deciles; compare full vs degree-only logistic."""
    Xp = prep(X)
    bins = pd.qcut(Xp["deg"], 10, duplicates="drop", labels=False)
    idx_keep = []
    for b in sorted(bins.unique()):
        pos = np.where((bins == b) & (y == 1))[0]
        neg = np.where((bins == b) & (y == 0))[0]
        k = min(len(pos), len(neg))
        if k == 0:
            continue
        idx_keep += list(rng.choice(pos, k, replace=False)) + list(rng.choice(neg, k, replace=False))
    idx_keep = np.array(sorted(idx_keep))
    Xm, ym = Xp.iloc[idx_keep], y[idx_keep]
    cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
    full = [r["roc_auc"] for tr, te in cv.split(Xm, ym)
            if (r := eval_split(Xm, ym, tr, te, models()["logistic"]))]
    degcols = [c for c in DEGREE_COLS if c in Xm.columns]
    dg = [r["roc_auc"] for tr, te in cv.split(Xm[degcols], ym)
          if (r := eval_split(Xm[degcols], ym, tr, te, models()["logistic"]))]
    out[f"{population}|{track}|p3_any|degree_matched"] = {
        "n_matched": int(len(ym)), "full_features_auc": round(float(np.mean(full)), 4),
        "degree_only_auc": round(float(np.mean(dg)), 4)}


def main():
    nodes, strict, typed = load()
    out = {}
    for population, mask in [
            ("primary", (nodes.stored == 1) & (nodes.p3_evaluated == 1)),
            ("sensitivity", nodes.p3_evaluated == 1)]:
        sel = nodes[mask]
        names = [n for n in sel.index if n in strict.index]
        sel = sel.loc[names]
        groups = sel.primary_file.values
        for track, F in [("strict", strict), ("typed", typed)]:
            X = F.loc[names]
            run_target(X, sel.p3_any.values.astype(int).copy(), groups,
                       "p3_any", track, population, out)
            for c in P3_CLASSES:
                run_target(X, sel[f"p3_{c}"].values.astype(int).copy(), groups,
                           c, track, population, out)
            degree_matched_control(X, sel.p3_any.values.astype(int), out, track, population)
    # logistic coefficients on primary/strict/p3_any for interpretation
    sel = nodes[(nodes.stored == 1) & (nodes.p3_evaluated == 1)]
    names = [n for n in sel.index if n in strict.index]
    Xp = prep(strict.loc[names])
    m = models()["logistic"].fit(Xp, sel.loc[names].p3_any.values)
    coefs = dict(zip(Xp.columns, m.named_steps["logisticregression"].coef_[0]))
    out["interpretation|primary|strict|p3_any|logistic_coefs"] = {
        k: round(float(v), 3) for k, v in sorted(coefs.items(), key=lambda kv: -abs(kv[1]))}
    with open(os.path.join(DATA, "qa_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    # compact print
    for k in sorted(out):
        if k.endswith("p3_any") and "|" in k:
            e = out[k]
            lg = e.get("logistic|grouped_file") or {}
            ld = e.get("logistic|lodo") or {}
            do = e.get("degree_only_logistic|grouped_file") or {}
            print(f"{k:32s} prev={e['prevalence']:.3f} n={e['n']:5d} | "
                  f"logit grouped AUC={lg.get('roc_auc')} lodo AUC={ld.get('roc_auc')} "
                  f"deg-only={do.get('roc_auc')} perm95={e.get('permutation_auc_p95')}")
    for k in sorted(out):
        if "degree_matched" in k:
            print(k, out[k])


if __name__ == "__main__":
    main()
