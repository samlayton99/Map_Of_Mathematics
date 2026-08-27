#!/usr/bin/env python
"""First learned head-selection assembler (v1: logistic ranker).

Dataset: typed-hole decisions from the WINNING search paths of the 300
train-module oracle runs (prover_out_v2_traces300.jsonl).  Each backward
decision "apply c" at a goal with head h yields one positive (c) and
negatives = the other inventory members whose conclusion head also matches
h (the prover only ever attempts head-matching candidates, so these are
the real alternatives at that decision).

Features per candidate: log1p(global citation count), depth/100, |depth
gap to target|/100, is-Eq/Iff-conclusion, same top-level namespace as the
target, inventory-rank/|inventory|.

Application: reorder the RETRIEVED toolkit (where inventory 220 > per-
expansion cap 50, so order determines which candidates are tried) by
learned score against the target's root goal head.  Evaluated end-to-end
by rerunning the prover on the reordered tasks.

Run: ~/venv/general_ml/bin/python assembler_ranker.py
Writes bigdata/prover_tasks80_learned.json, tools/output/assembler_ranker.json
"""
import json
import sys
import time

import numpy as np

from atlas import load_dump, theorem_roots, BIG
from heads_util import load_heads

OUT_JSON = "output/assembler_ranker.json"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def main():
    log("loading atlas + heads...")
    a = load_dump()
    ch, ca, _ = load_heads()
    roots = theorem_roots(a)
    cite = np.zeros(a.n, dtype=np.int64)
    for r in roots:
        cite[np.unique(a.v_indices[a.v_indptr[r]:a.v_indptr[r + 1]])] += 1
    ns_of = [n.split(".", 1)[0] for n in a.names]

    def feats(cname, target, h, rank, ninv):
        c = a.idx.get(cname)
        t = a.idx.get(target)
        if c is None or t is None:
            return None
        return [
            np.log1p(cite[c]),
            a.depth[c] / 100.0,
            abs(int(a.depth[c]) - int(a.depth[t])) / 100.0,
            1.0 if ch.get(cname) in ("Eq", "Iff") else 0.0,
            1.0 if ns_of[c] == ns_of[t] else 0.0,
            rank / max(ninv, 1),
        ]

    # ---- dataset from winning traces
    tasks = {t["n"]: t for t in
             json.load(open(BIG / "support_tasks_train300.json"))["tasks"]}
    X, y, groups = [], [], 0
    rows = [json.loads(l) for l in open(BIG / "prover_out_v2_traces300.jsonl")]
    for r in rows:
        if not r["solved"]:
            continue
        task = tasks[r["n"]]
        inv = task["bw"]
        heads = r.get("goal_heads", [])
        for i, lab in enumerate(r["path"]):
            if not lab.startswith("apply ") or lab.startswith("apply hyp"):
                continue
            chosen = lab[len("apply "):]
            h = heads[i] if i < len(heads) else None
            if h is None:
                continue
            alts = [c for c in inv if ch.get(c) == h and c != chosen]
            fpos = feats(chosen, r["n"], h, inv.index(chosen) if chosen in inv else len(inv), len(inv))
            if fpos is None:
                continue
            X.append(fpos); y.append(1); groups += 1
            for c in alts[:20]:
                f = feats(c, r["n"], h, inv.index(c), len(inv))
                if f is not None:
                    X.append(f); y.append(0)
    X = np.array(X); y = np.array(y)
    log(f"dataset: {groups} decisions, {len(y)} rows ({int(y.sum())} positives)")
    if groups < 10:
        log("TOO FEW DECISIONS - aborting honestly")
        json.dump({"error": "insufficient decisions", "n_decisions": groups},
                  open(OUT_JSON, "w"))
        return

    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression(max_iter=2000, class_weight="balanced")
    clf.fit(X, y)
    coefs = dict(zip(["log_cite", "depth", "depth_gap", "eqiff", "same_ns",
                      "inv_rank"], np.round(clf.coef_[0], 3).tolist()))
    log(f"coefs: {coefs}")

    # ---- reorder the retrieved toolkit for the 80 test tasks
    test = json.load(open(BIG / "prover_tasks80.json"))["tasks"]
    out = []
    for t in test:
        inv = t["bw"]
        scores = []
        for rank, c in enumerate(inv):
            f = feats(c, t["n"], ch.get(t["n"]), rank, len(inv))
            scores.append(-1e9 if f is None else
                          float(clf.decision_function([f])[0]))
        order = np.argsort(-np.array(scores))
        out.append({"n": t["n"], "bw": [inv[i] for i in order],
                    "rw": t["rw"], "fb": t["fb"]})
    json.dump({"tasks": out}, open(BIG / "prover_tasks80_learned.json", "w"))
    json.dump({"n_decisions": groups, "n_rows": int(len(y)),
               "coefs": coefs}, open(OUT_JSON, "w"), indent=1)
    log("wrote reordered tasks + ranker summary")


if __name__ == "__main__":
    main()
