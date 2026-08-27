#!/usr/bin/env python3
"""Remaining required ablations (core/05 §8) for p3_any on the primary
population, logistic regression, grouped-file split:
  - P2 simple graph (dedup, unweighted) vs P1 weighted occurrence graph;
  - with vs without community features;
  - strict full vs degree-only (already in qa_results; repeated for the table).
"""
import os, json
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from models_qa import prep, models, eval_split, agg, DEGREE_COLS
import features

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
COMM_COLS = ["community_size", "within_comm_z", "participation",
             "n_neighbor_comms", "neighbor_comm_entropy", "cross_comm_frac"]


def grouped_auc(X, y, groups):
    cv = GroupKFold(n_splits=min(6, len(set(groups))))
    res = [r for tr, te in cv.split(X, y, groups)
           if (r := eval_split(X, y, tr, te, models()["logistic"]))]
    return agg(res)


def main():
    nodes = pd.read_csv(os.path.join(DATA, "node_inventory.csv")).set_index("name")
    nodes["primary_file"] = nodes.files.str.split("|").str[0]
    strict = pd.read_csv(os.path.join(DATA, "feature_matrix_strict.csv"), index_col=0)
    sel = nodes[(nodes.stored == 1) & (nodes.p3_evaluated == 1)]
    names = [n for n in sel.index if n in strict.index]
    y = sel.loc[names].p3_any.values.astype(int)
    groups = sel.loc[names].primary_file.values
    out = {}
    # P1 weighted (existing strict matrix)
    out["p1_weighted_strict"] = grouped_auc(prep(strict.loc[names]), y, groups)
    # P2 simple graph: dedup edges, weight 1
    edges = features.load_edges()
    e2 = edges.groupby(["src", "dst"], as_index=False).agg(mult=("mult", "size"))
    e2["mult"] = 1
    e2["layer"] = "any"
    e2["minDepth"] = 0
    G2 = features.build_graphs(e2)
    f2 = features.f0_f1_f2(G2)
    out["p2_simple_strict"] = grouped_auc(prep(f2.loc[names]), y, groups)
    # without community features
    nocomm = strict.loc[names].drop(columns=COMM_COLS)
    out["strict_without_community"] = grouped_auc(prep(nocomm), y, groups)
    # degree-only
    out["degree_only"] = grouped_auc(prep(strict.loc[names][DEGREE_COLS]), y, groups)
    with open(os.path.join(DATA, "ablations.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for k, v in out.items():
        print(f"{k:28s} AUC={v['roc_auc']} PR={v['pr_auc']}")


if __name__ == "__main__":
    main()
