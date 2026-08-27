#!/usr/bin/env python3
"""Aggregate blind keyness ratings: un-blind via keymap, per-view stats."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.normpath(os.path.join(HERE, "..", "review", "keyness"))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
VIEWS = ("moveset", "ranked", "applied", "prov", "zoom")


def main():
    km = json.load(open(os.path.join(K, "keymap.json")))
    raters = {}
    for rn in ("R1", "R2", "R3"):
        p = os.path.join(K, f"ratings_{rn}.json")
        if os.path.exists(p):
            raters[rn] = json.load(open(p))
    print(f"raters present: {sorted(raters)}")
    ratings = {v: [] for v in VIEWS}
    top1 = {v: {"yes": 0, "partial": 0, "no": 0} for v in VIEWS}
    best = {v: 0 for v in VIEWS}
    bydepth = {v: {"shallow": [], "mid": [], "deep": []} for v in VIEWS}
    per_proof_best = {}
    key_moves = {}
    for pid, meta in km.items():
        letter2view = meta["map"]
        d = meta["depth"]
        band = "shallow" if d < 40 else ("mid" if d < 90 else "deep")
        for rn, rr in raters.items():
            e = rr.get(pid)
            if not e:
                continue
            key_moves.setdefault(pid, []).append(e.get("key_move", ""))
            for letter, view in letter2view.items():
                sc = e.get("ratings", {}).get(letter)
                if isinstance(sc, (int, float)):
                    ratings[view].append(sc)
                    bydepth[view][band].append(sc)
                t = e.get("top1_is_key", {}).get(letter)
                if t in top1[view]:
                    top1[view][t] += 1
            bv = e.get("best_view")
            if bv in letter2view:
                best[letter2view[bv]] += 1
                per_proof_best.setdefault(pid, []).append(letter2view[bv])
    out = {"n_raters": len(raters), "n_proofs": len(km)}
    out["mean_rating"] = {v: round(float(np.mean(r)), 2) if r else None
                          for v, r in ratings.items()}
    out["top1_is_key"] = {v: {k: c for k, c in t.items()} for v, t in top1.items()}
    out["top1_yes_rate"] = {v: round(t["yes"] / max(1, sum(t.values())), 3)
                            for v, t in top1.items()}
    out["best_view_votes"] = best
    out["mean_rating_by_depth"] = {v: {b: round(float(np.mean(x)), 2) if x else None
                                       for b, x in bb.items()}
                                   for v, bb in bydepth.items()}
    cons = [len(set(v)) == 1 for v in per_proof_best.values() if len(v) == len(raters)]
    out["best_view_unanimity_rate"] = round(float(np.mean(cons)), 3) if cons else None
    kk = [len(set(k)) for k in key_moves.values() if len(k) == len(raters)]
    out["distinct_key_moves_per_proof_mean"] = round(float(np.mean(kk)), 2) if kk else None
    with open(os.path.join(DATA, "keyness_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
