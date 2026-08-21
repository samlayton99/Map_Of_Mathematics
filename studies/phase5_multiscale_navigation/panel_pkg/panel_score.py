#!/usr/bin/env python3
"""Semantic keyness panel -- scoring.

This is the ONLY place a Semantic* metric may be computed, because it is the
only place graded rater labels exist. Everything else in the apparatus reports
Source*, Role*, Coverage* or Graph*.

Scores every registered ranking against what three blind raters independently
called the key moves. Raters never saw a ranking, so one annotation scores all
rankings without anchoring.

Metrics:
  SemanticCoreHit@1   rank-1 is a key move  (agreement rule below)
  SemanticCoreHit@k   a key move appears in the top k
  SemanticRecall@4    share of the rater's key moves in the top 4
  NoneListedRate      share of proofs where the rater says the key move is
                      absent from the candidate list -- semantic evidence of
                      the coverage gap, not a rating failure

Agreement rules, fixed in advance:
  union     an item counts as key if ANY rater picked it (lenient)
  majority  at least 2 of 3 raters picked it (headline)
  unanimous all 3 picked it (strict)
"""
import glob
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PANEL = os.path.join(ROOT, "review", "panel")
sys.path.insert(0, ROOT)


def load_ratings():
    out = {}
    for f in sorted(glob.glob(os.path.join(PANEL, "ratings_*.json"))):
        out[os.path.basename(f)[8:-5]] = json.load(open(f))
    return out


def main():
    from mathmap_eval import rankings as R
    from mathmap_eval.corpus import get_corpus

    c = get_corpus()
    key = json.load(open(os.path.join(PANEL, "keymap.json")))
    ratings = load_ratings()
    if len(ratings) < 2:
        print(f"only {len(ratings)} rating file(s) present; need >=2", flush=True)
        return 1
    print(f"raters: {', '.join(ratings)}", flush=True)

    # ---- assemble labels -------------------------------------------------
    per_proof = {}
    none_by_rater = Counter()
    for pid, meta in key.items():
        picks_by_rater = {}
        for rname, rr in ratings.items():
            ent = rr.get(pid)
            if ent is None:
                continue
            p = ent.get("picks")
            if p == "NONE_LISTED" or p is None:
                picks_by_rater[rname] = "NONE"
                none_by_rater[rname] += 1
            else:
                picks_by_rater[rname] = set(int(x) for x in
                                            (p if isinstance(p, list) else [p]))
        per_proof[pid] = picks_by_rater

    n_raters = len(ratings)
    print(f"\nNONE_LISTED per rater (of {len(key)} proofs): "
          + ", ".join(f"{k}={v}" for k, v in none_by_rater.items()), flush=True)

    # ---- inter-rater agreement ------------------------------------------
    def jacc(a, b):
        if a == "NONE" and b == "NONE":
            return 1.0
        if a == "NONE" or b == "NONE":
            return 0.0
        return len(a & b) / max(len(a | b), 1)

    pair_scores, by_band_agree = [], defaultdict(list)
    names_r = list(ratings)
    for pid, pb in per_proof.items():
        vals = []
        for i in range(len(names_r)):
            for j in range(i + 1, len(names_r)):
                a, b = pb.get(names_r[i]), pb.get(names_r[j])
                if a is None or b is None:
                    continue
                vals.append(jacc(a, b))
        if vals:
            pair_scores.extend(vals)
            by_band_agree[key[pid]["band"]].append(float(np.mean(vals)))
    print(f"inter-rater agreement (mean pairwise Jaccard): "
          f"{np.mean(pair_scores):.3f}", flush=True)
    print("  by depth band: " + "  ".join(
        f"{b}={np.mean(v):.2f}" for b, v in sorted(by_band_agree.items())),
        flush=True)

    # ---- consensus label sets -------------------------------------------
    consensus = {}
    for pid, pb in per_proof.items():
        counts = Counter()
        none_votes = 0
        for rname, p in pb.items():
            if p == "NONE":
                none_votes += 1
            else:
                for x in p:
                    counts[x] += 1
        consensus[pid] = {
            "union": {x for x, n in counts.items() if n >= 1},
            "majority": {x for x, n in counts.items() if n >= 2},
            "unanimous": {x for x, n in counts.items() if n >= n_raters},
            "none_votes": none_votes,
        }
    maj_none = sum(1 for v in consensus.values()
                   if v["none_votes"] >= (n_raters + 1) // 2)
    print(f"proofs where a MAJORITY says the key move is not listed: "
          f"{maj_none}/{len(key)}", flush=True)

    # ---- score every ranking --------------------------------------------
    base = np.where(c.universe("U1D"))[0]
    pos_index = {int(p): i for i, p in enumerate(base)}
    results = {}
    for rname in R.names():
        spec = R.get(rname)
        ranks = spec.ranks_within_proof(c, base)
        rows = {"union": [], "majority": [], "unanimous": []}
        rec4, hit4 = [], []
        by_band = defaultdict(list)
        for pid, meta in key.items():
            items = {int(k2): int(v) for k2, v in meta["items"].items()}
            cons = consensus[pid]
            if cons["none_votes"] >= (n_raters + 1) // 2:
                continue                      # excluded: nothing to hit
            ordered = sorted(items.items(),
                             key=lambda kv: ranks[pos_index[kv[1]]])
            order_nums = [n for n, _ in ordered]
            for mode in ("union", "majority", "unanimous"):
                gt = cons[mode]
                if not gt:
                    continue
                rows[mode].append(order_nums[0] in gt)
                if mode == "majority":
                    top4 = set(order_nums[:4])
                    hit4.append(bool(top4 & gt))
                    rec4.append(len(top4 & gt) / len(gt))
                    by_band[meta["band"]].append(order_nums[0] in gt)
        results[rname] = {
            "SemanticCoreHit@1_union": float(np.mean(rows["union"])) if rows["union"] else None,
            "SemanticCoreHit@1_majority": float(np.mean(rows["majority"])) if rows["majority"] else None,
            "SemanticCoreHit@1_unanimous": float(np.mean(rows["unanimous"])) if rows["unanimous"] else None,
            "SemanticCoreHit@4_majority": float(np.mean(hit4)) if hit4 else None,
            "SemanticRecall@4_majority": float(np.mean(rec4)) if rec4 else None,
            "n_scored": len(rows["majority"]),
            "by_band_majority": {b: [float(np.mean(v)), len(v)]
                                 for b, v in sorted(by_band.items())},
        }

    order = sorted(results, key=lambda k: -(results[k]["SemanticCoreHit@1_majority"] or 0))
    print(f"\n{'ranking':<22}{'Core@1 maj':>12}{'Core@1 uni':>12}"
          f"{'Core@4 maj':>12}{'Rec@4 maj':>11}{'n':>5}", flush=True)
    for k2 in order:
        r = results[k2]
        f = lambda x: "-" if x is None else f"{x:.3f}"
        print(f"{k2:<22}{f(r['SemanticCoreHit@1_majority']):>12}"
              f"{f(r['SemanticCoreHit@1_unanimous']):>12}"
              f"{f(r['SemanticCoreHit@4_majority']):>12}"
              f"{f(r['SemanticRecall@4_majority']):>11}{r['n_scored']:>5}",
              flush=True)

    print(f"\nSemanticCoreHit@1 (majority) by depth band", flush=True)
    bands = sorted({b for r in results.values() for b in r["by_band_majority"]})
    print(f"{'ranking':<22}" + "".join(b.rjust(12) for b in bands), flush=True)
    for k2 in order:
        cells = []
        for b in bands:
            v = results[k2]["by_band_majority"].get(b)
            cells.append((f"{v[0]:.2f}({v[1]})" if v else "-").rjust(12))
        print(f"{k2:<22}" + "".join(cells), flush=True)

    out = {"n_proofs": len(key), "n_raters": n_raters,
           "inter_rater_jaccard": float(np.mean(pair_scores)),
           "inter_rater_by_band": {b: float(np.mean(v))
                                   for b, v in by_band_agree.items()},
           "none_listed_by_rater": dict(none_by_rater),
           "majority_none_listed": maj_none,
           "results": results}
    json.dump(out, open(os.path.join(ROOT, "data", "panel_results.json"), "w"),
              indent=1)
    print("\nwritten data/panel_results.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
