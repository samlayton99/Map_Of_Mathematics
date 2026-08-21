#!/usr/bin/env python3
"""Paired comparison of the headline schemes against their anchor.

Proof-level paired bootstrap (2000 replicates, seed 20260821) for KeyMove@1
and P@4, plus an exact McNemar sign test on the KeyMove@1 discordant proofs.
"""
import json
import os
import sys
from math import comb

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from mathmap_eval import navigation as NAV               # noqa: E402
from mathmap_eval.corpus import get_corpus               # noqa: E402
import social_choice as SC                               # noqa: E402
from run_social_choice import (ranks_within_proof, reference_scores,
                               scheme_scores, build)     # noqa: E402

PAIRS = [
    ("HYB_copeland_first__role5w_x_logdepth_x_rarity",
     "REF*_role5w_x_logdepth_x_rarity"),
    ("HYB_condorcet_first__role5w_x_logdepth_x_rarity",
     "REF*_role5w_x_logdepth_x_rarity"),
    ("HYB_borda_first__role5w_x_logdepth_x_rarity",
     "REF*_role5w_x_logdepth_x_rarity"),
    ("copeland6", "borda6"),
    ("copeland6", "REF*_role5w_x_logdepth_x_rarity"),
    ("kemeny6", "borda6"),
    ("borda6_rarityx2", "REF*_role5w_x_logdepth_x_rarity"),
    ("borda6_rarityx2", "borda6"),
    ("borda6_rolex2", "borda6"),
]


def per_proof_vectors(c, base, grades, kr, score):
    rk = ranks_within_proof(c, base, score)
    pp = NAV.per_proof_orders(c, base, rk, grades, kr)
    key, p4n, p4d = [], [], []
    for p in pp:
        g = p["grades"]
        key.append(int(g[0] == g.max()))
        p4n.append(int((g[:4] >= 2).sum()))
        p4d.append(len(g[:4]))
    return (np.array(key, float), np.array(p4n, float), np.array(p4d, float),
            [p["pid"] for p in pp])


def main():
    split = os.environ.get("SPLIT", "TEST-R")
    c = get_corpus()
    keymap = json.load(open(os.path.join(SC.SEALED, "keymap.json")))
    grades = SC.load_grades(keymap, split)
    kr = {p: v for p, v in keymap.items() if v["split"] == split}
    full = np.where(c.universe("U1D"))[0]
    arts = np.array(sorted({v["artifact"] for v in kr.values()}))
    base = full[np.isin(c.inc_artifact[full], arts)]
    sig, keys, tier = build(c, base)
    refs = reference_scores(c, base, sig, tier)
    scores, _ = scheme_scores(c, base, sig, keys, tier,
                              anchor=refs["REF*_role5w_x_logdepth_x_rarity"])
    scores.update(refs)
    for aname, asc in refs.items():
        ctx = {"tier": tier.astype(np.float64), "anchor": asc}
        rr, _ = SC.Aggregator(c, base, keys, SC.VOTERS, ctx=ctx).run(
            {k: SC.make_first_anchor(k)
             for k in ("condorcet", "copeland", "borda")})
        short = aname.split("_", 1)[1]
        for k, v in rr.items():
            scores[f"HYB_{k}_first__{short}"] = v

    rng = np.random.default_rng(20260821)
    print(f"split {split}, {len(kr)} proofs, paired bootstrap 2000 reps")
    for a, b in PAIRS:
        ka, na, da, _ = per_proof_vectors(c, base, grades, kr, scores[a])
        kb, nb, db, _ = per_proof_vectors(c, base, grades, kr, scores[b])
        n = len(ka)
        dk, d4 = [], []
        for _ in range(2000):
            i = rng.integers(0, n, n)
            dk.append(ka[i].mean() - kb[i].mean())
            d4.append(na[i].sum() / da[i].sum() - nb[i].sum() / db[i].sum())
        dk = np.array(dk); d4 = np.array(d4)
        win = int(((ka == 1) & (kb == 0)).sum())
        loss = int(((ka == 0) & (kb == 1)).sum())
        m = win + loss
        p = (sum(comb(m, i) for i in range(min(win, loss) + 1)) * 2
             / 2 ** m) if m else 1.0
        print(f"\n{a}\n  vs {b}")
        print(f"  KeyMove@1 {ka.mean():.3f} vs {kb.mean():.3f}  "
              f"delta {ka.mean()-kb.mean():+.3f} "
              f"95% CI [{np.percentile(dk,2.5):+.3f}, "
              f"{np.percentile(dk,97.5):+.3f}]")
        print(f"  McNemar: {win} proofs fixed, {loss} broken, "
              f"exact two-sided p = {min(p,1.0):.4f}")
        print(f"  P@4 {na.sum()/da.sum():.3f} vs {nb.sum()/db.sum():.3f}  "
              f"delta {na.sum()/da.sum()-nb.sum()/db.sum():+.4f} "
              f"95% CI [{np.percentile(d4,2.5):+.4f}, "
              f"{np.percentile(d4,97.5):+.4f}]")


if __name__ == "__main__":
    main()
