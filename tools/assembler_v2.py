#!/usr/bin/env python
"""Cardinality-agnostic head-selection assembler v2.

Dataset: reference-derived decisions from the neg-mode replay traces.  A
decision = a proof node whose head is a support constant, with candidate
set = the Lean-legal support heads at that goal (hard negatives measured
by the engine's own unification).  Train on train-module traces
(traces_neg300 + traces_neg3k), evaluate on the module-holdout benchmark
traces (traces_neg80).

Model: LightGBM LGBMRanker (lambdarank) over per-candidate features; the
scorer sees ONE candidate at a time (shared weights), so it applies to any
candidate-set size.

Run: ~/venv/general_ml/bin/python assembler_v2.py
"""
import json
import sys
import time
from collections import Counter, defaultdict

import numpy as np

from atlas import load_dump, BIG
from heads_util import load_heads


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def load_tasks(fn):
    return {t["n"]: t for t in json.load(open(BIG / fn))["tasks"]}


def decisions(trace_fn, tasks):
    """Yield (theorem, node) decisions with candidate sets."""
    out, cover = [], Counter()
    with open(BIG / trace_fn) as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                cover["torn_line"] += 1   # file may still be being written
                continue
            if "error" in r or not r.get("nodes"):
                continue
            t = tasks.get(r["n"])
            if t is None:
                continue
            support = t["bw"]
            rank = {c: i for i, c in enumerate(support)}
            for nd in r["nodes"]:
                head = nd["head"]
                if head in ("FVAR", "OTHER", "LEAF"):
                    cover["local_or_other"] += 1
                    continue
                if head not in rank:
                    cover["head_not_in_support"] += 1
                    continue
                cands = nd.get("legal_heads", [])
                if head not in cands:
                    cover["positive_not_legal"] += 1
                    continue
                if len(cands) < 2:
                    cover["singleton"] += 1
                    continue
                cover["decision"] += 1
                out.append({
                    "n": r["n"], "head": head, "cands": cands,
                    "goal": nd.get("goal", ""), "depth": nd.get("depth", 0),
                    "rank": rank, "support_size": len(support),
                })
    return out, cover


def featurize(decs, a, ch, use):
    X, y, grp, meta = [], [], [], []
    logp = lambda v: float(np.log1p(v))
    for d in decs:
        goal = d["goal"]
        gl = len(goal)
        nc = len(d["cands"])
        for c in d["cands"]:
            i = a.idx.get(c)
            depth = float(a.depth[i]) if i is not None else 0.0
            inP = logp(use["inP"][i]) if i is not None else 0.0
            inS = logp(use["inS"][i]) if i is not None else 0.0
            chc = ch.get(c, "")
            last = c.split(".")[-1]
            X.append([
                depth, inP, inS,
                float(d["rank"].get(c, 99)),          # support-list rank
                1.0 if chc and (chc in goal) else 0.0, # concl head occurs in goal
                1.0 if last and (last in goal) else 0.0,
                1.0 if chc in ("Eq", "Iff") else 0.0,
                float(len(c)),
                float(d["depth"]), float(gl), float(nc),
                float(d["support_size"]),
            ])
            y.append(1 if c == d["head"] else 0)
        grp.append(nc)
        meta.append(d)
    return np.array(X), np.array(y), np.array(grp), meta


def rank_eval(scores, y, grp, meta, label, strat=True):
    pos, mrr = 0, 0.0
    topk = Counter()
    strata = defaultdict(lambda: [0, 0])
    off = 0
    n = len(grp)
    for gi, g in enumerate(grp):
        s = scores[off:off + g]
        yy = y[off:off + g]
        order = np.argsort(-s, kind="stable")
        r = int(np.where(yy[order] == 1)[0][0]) + 1
        mrr += 1.0 / r
        for k in (1, 3, 5, 10):
            if r <= k:
                topk[k] += 1
        d = meta[gi]
        for key in (f"cands<={5 if g<=5 else (15 if g<=15 else 999)}",
                    f"depth<={3 if d['depth']<=3 else 999}",
                    f"support<={25 if d['support_size']<=25 else 999}"):
            strata[key][1] += 1
            if r == 1:
                strata[key][0] += 1
        off += g
    line = (f"{label:24s} top1 {topk[1]/n:.3f}  top3 {topk[3]/n:.3f}  "
            f"top5 {topk[5]/n:.3f}  top10 {topk[10]/n:.3f}  MRR {mrr/n:.3f}  (n={n})")
    print(line)
    if strat:
        for k in sorted(strata):
            hit, tot = strata[k]
            print(f"    {k:14s} top1 {hit/max(1,tot):.3f} (n={tot})")
    return topk[1] / n


def main():
    log("loading atlas + heads + usage...")
    a = load_dump()
    ch, _, _ = load_heads()
    use = dict(np.load(BIG / "mathlib_usage_counters.npz"))

    train_decs, cov_tr = [], Counter()
    for tf, taskf in (("traces_neg300.jsonl", "support_tasks_train300.json"),
                      ("traces_neg3k.jsonl", "support_tasks_train3k.json")):
        try:
            d, c = decisions(tf, load_tasks(taskf))
            train_decs += d
            cov_tr += c
        except FileNotFoundError:
            log(f"missing {tf}, skipping")
    test_decs, cov_te = decisions("traces_neg80.jsonl", load_tasks("support_tasks_S1.json"))
    log(f"train decisions {len(train_decs)} coverage {dict(cov_tr)}")
    log(f"test  decisions {len(test_decs)} coverage {dict(cov_te)}")

    Xtr, ytr, gtr, mtr = featurize(train_decs, a, ch, use)
    Xte, yte, gte, mte = featurize(test_decs, a, ch, use)

    # baselines on test
    print("\n== module-holdout evaluation (benchmark 80) ==")
    rng = np.random.default_rng(0)
    rank_eval(rng.random(len(yte)), yte, gte, mte, "random", strat=False)
    rank_eval(-Xte[:, 3], yte, gte, mte, "support-rank order", strat=False)
    rank_eval(Xte[:, 1], yte, gte, mte, "citation order", strat=False)
    rank_eval(Xte[:, 4] * 10 + Xte[:, 1], yte, gte, mte, "headmatch+cite", strat=False)

    import lightgbm as lgb
    model = lgb.LGBMRanker(
        objective="lambdarank", n_estimators=400, learning_rate=0.06,
        num_leaves=63, min_child_samples=20, label_gain=[0, 1],
        verbose=-1)
    model.fit(Xtr, ytr, group=gtr)
    rank_eval(model.predict(Xte), yte, gte, mte, "LGBMRanker v2")
    names = ["depth", "logInP", "logInS", "srank", "headmatch", "namematch",
             "eqiff", "namelen", "pdepth", "goallen", "ncands", "supsize"]
    imp = sorted(zip(names, model.feature_importances_), key=lambda kv: -kv[1])
    print("feature importances:", imp)
    import joblib
    joblib.dump(model, BIG / "assembler_v2.joblib")
    log("model saved")


if __name__ == "__main__":
    main()
