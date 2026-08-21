#!/usr/bin/env python3
"""Diagnostics for the social-choice family, on TEST-R.

 1. Condorcet: how often does a winner exist, and is it the right item?
 2. Kemeny heuristic: exact optimum by brute force on the small proofs.
 3. IIA (Arrow): restrict the candidate universe U1D -> U1 and count how many
    surviving pairs change their relative order. A cardinal score gives 0 by
    construction; every rank-aggregation rule can be nonzero.
 4. Role-tier base rates: is the tier ordinal actually monotone in usefulness?
"""
import json
import os
import sys
from collections import defaultdict
from itertools import permutations

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from mathmap_eval.corpus import get_corpus               # noqa: E402
import social_choice as SC                               # noqa: E402
from run_social_choice import ranks_within_proof, reference_scores  # noqa: E402


def proof_blocks(c, base):
    order, starts, counts = SC.group_by_artifact(c, base)
    for s, n in zip(starts, counts):
        yield order[s:s + n]


def main():
    c = get_corpus()
    keymap = json.load(open(os.path.join(SC.SEALED, "keymap.json")))
    grades = SC.load_grades(keymap, "TEST-R")
    kr = {p: v for p, v in keymap.items() if v["split"] == "TEST-R"}
    full = np.where(c.universe("U1D"))[0]
    arts = np.array(sorted({v["artifact"] for v in kr.values()}))
    base = full[np.isin(c.inc_artifact[full], arts)]
    sig = SC.Signals(c)
    keys = sig.keys(base)
    tier = sig.tier(base)
    g = np.array([grades.get(int(i), -1) for i in base])

    print("=" * 70)
    print("4. ROLE TIER base rates on TEST-R (is the ordinal monotone?)")
    print(f"{'tier':<6}{'n':>7}{'useful>=2':>12}{'major>=3':>11}{'core=4':>10}")
    for t in (5, 4, 3, 2, 1):
        m = (tier == t) & (g >= 0)
        if not m.sum():
            continue
        print(f"{t:<6}{int(m.sum()):>7}{(g[m] >= 2).mean():>12.3f}"
              f"{(g[m] >= 3).mean():>11.3f}{(g[m] == 4).mean():>10.3f}")

    # ---------------- 1. Condorcet ------------------------------------
    print()
    print("=" * 70)
    print("1. CONDORCET")
    for tag, voters in (("6 voters", SC.VOTERS), ("4 voters", SC.VOTERS4)):
        agg = SC.Aggregator(c, base, keys, voters,
                            ctx={"tier": tier.astype(float)})
        res, extra = agg.run({"borda": SC.borda, "copeland": SC.copeland})
        cw = extra["condorcet"].astype(bool)
        n_ex = n_right = n_borda_same = 0
        key_no = key_yes = tot_no = tot_yes = 0
        for blk in proof_blocks(c, base):
            gg = g[blk]
            if (gg < 0).all():
                continue
            best = gg.max()
            has = cw[blk].any()
            bd_top = blk[np.argmin(res["borda"][blk])]
            if has:
                n_ex += 1
                i = blk[np.argmax(cw[blk])]
                n_right += int(g[i] == best)
                n_borda_same += int(i == bd_top)
                tot_yes += 1
                key_yes += int(g[bd_top] == best)
            else:
                tot_no += 1
                key_no += int(g[bd_top] == best)
        print(f"  {tag}: winner exists in {n_ex}/{len(arts)} proofs "
              f"({n_ex/len(arts):.3f})")
        print(f"    when it exists it is a top-graded item in "
              f"{n_right}/{n_ex} ({n_right/max(n_ex,1):.3f})")
        print(f"    it coincides with the Borda winner in "
              f"{n_borda_same}/{n_ex} ({n_borda_same/max(n_ex,1):.3f})")
        print(f"    Borda KeyMove@1 | winner exists  {key_yes}/{tot_yes} "
              f"= {key_yes/max(tot_yes,1):.3f}")
        print(f"    Borda KeyMove@1 | no winner      {key_no}/{tot_no} "
              f"= {key_no/max(tot_no,1):.3f}")

    # ---------------- 2. Kemeny exactness -----------------------------
    print()
    print("=" * 70)
    print("2. KEMENY heuristic vs exact optimum (brute force, n <= 8)")
    agg = SC.Aggregator(c, base, keys, SC.VOTERS,
                        ctx={"tier": tier.astype(float)})
    res, _ = agg.run({"kemeny": SC.kemeny, "borda": SC.borda})
    K = np.stack([keys[v] for v in SC.VOTERS])
    n_small = n_opt = 0
    gap = 0.0
    n_diff_borda = n_tot = 0
    for blk in proof_blocks(c, base):
        n = len(blk)
        X = K[:, blk]
        W = np.zeros((n, n))
        for a in range(n):
            for b in range(n):
                W[a, b] = float((X[:, a] < X[:, b]).sum())
        ordk = np.argsort(res["kemeny"][blk], kind="stable")
        ordb = np.argsort(res["borda"][blk], kind="stable")
        n_tot += 1
        n_diff_borda += int(not np.array_equal(ordk, ordb))
        if n <= 8:
            n_small += 1

            def cost(P):
                return sum(W[P[j], P[i]] for i in range(len(P))
                           for j in range(i + 1, len(P)))
            best = min(permutations(range(n)), key=cost)
            ch, co = cost(list(ordk)), cost(list(best))
            n_opt += int(abs(ch - co) < 1e-9)
            gap += ch - co
    print(f"  proofs with n <= 8: {n_small}/{n_tot}")
    print(f"  heuristic hits the exact optimum in {n_opt}/{n_small} "
          f"({n_opt/max(n_small,1):.3f}); mean excess cost "
          f"{gap/max(n_small,1):.4f} disagreements")
    print(f"  Kemeny order differs from Borda order in {n_diff_borda}/{n_tot} "
          f"proofs")

    # ---------------- 5. tie density ----------------------------------
    print()
    print("=" * 70)
    print("5. TIE DENSITY: how much of each rule's order is decided by the")
    print("   tie-break (term position) rather than by the rule?")
    rules_all = dict(SC.RULES)
    ctx0 = {"tier": tier.astype(float),
            "anchor": reference_scores(
                c, base, sig, tier)["REF*_role5w_x_logdepth_x_rarity"]}
    rules_all["condorcet_first_anchor"] = SC.make_first_anchor("condorcet")
    rules_all["copeland_first_anchor"] = SC.make_first_anchor("copeland")
    rall, _ = SC.Aggregator(c, base, keys, SC.VOTERS, ctx=ctx0).run(rules_all)
    print(f"{'rule':<26}{'tied share':>12}{'distinct/n':>12}")
    for name in sorted(rall):
        tied = tot = 0
        dist = nn = 0.0
        for blk in proof_blocks(c, base):
            v = rall[name][blk]
            _, cnt = np.unique(v, return_counts=True)
            tied += int(cnt[cnt > 1].sum())
            tot += len(v)
            dist += len(cnt)
            nn += len(v)
        print(f"{name:<26}{tied/tot:>12.4f}{dist/nn:>12.4f}")

    # ---------------- 3. IIA ------------------------------------------
    print()
    print("=" * 70)
    print("3. IIA: restrict U1D -> U1, count relative-order flips among the")
    print("   pairs that survive the restriction")
    keep = c.universe("U1")[base]
    print(f"   surviving candidates: {int(keep.sum())}/{len(base)}")
    base2 = base[keep]
    sig2 = SC.Signals(c)
    keys2 = sig2.keys(base2)
    tier2 = sig2.tier(base2)
    ctx1 = {"tier": tier.astype(float)}
    ctx2 = {"tier": tier2.astype(float)}
    refs1 = reference_scores(c, base, sig, tier)
    refs2 = reference_scores(c, base2, sig2, tier2)
    ctx1["anchor"] = refs1["REF*_role5w_x_logdepth_x_rarity"]
    ctx2["anchor"] = refs2["REF*_role5w_x_logdepth_x_rarity"]
    rules = dict(SC.RULES)
    rules["condorcet_first_anchor"] = SC.make_first_anchor("condorcet")
    rules["copeland_first_anchor"] = SC.make_first_anchor("copeland")
    r1, _ = SC.Aggregator(c, base, keys, SC.VOTERS, ctx=ctx1).run(rules)
    r2, _ = SC.Aggregator(c, base2, keys2, SC.VOTERS, ctx=ctx2).run(rules)
    r1["REF*_cardinal"] = refs1["REF*_role5w_x_logdepth_x_rarity"]
    r2["REF*_cardinal"] = refs2["REF*_role5w_x_logdepth_x_rarity"]
    pos1 = {int(p): i for i, p in enumerate(base)}
    pos2 = {int(p): i for i, p in enumerate(base2)}
    blocks2 = [blk for blk in proof_blocks(c, base2) if len(blk) >= 2]
    print(f"{'rule':<26}{'pairs':>9}{'flipped':>9}{'rate':>8}"
          f"{'top1 moved':>12}")
    for name in sorted(r1):
        flips = pairs = 0
        top_changed = nprf = 0
        for blk in blocks2:
            ids = base2[blk]
            i1 = np.array([pos1[int(x)] for x in ids])
            s1 = r1[name][i1]
            s2 = r2[name][blk]
            o1 = np.argsort(s1, kind="stable")
            o2 = np.argsort(s2, kind="stable")
            rk1 = np.empty(len(ids), int); rk1[o1] = np.arange(len(ids))
            rk2 = np.empty(len(ids), int); rk2[o2] = np.arange(len(ids))
            a, b = np.triu_indices(len(ids), 1)
            pairs += len(a)
            flips += int((np.sign(rk1[a] - rk1[b])
                          != np.sign(rk2[a] - rk2[b])).sum())
            nprf += 1
            top_changed += int(o1[0] != o2[0])
        print(f"{name:<26}{pairs:>9}{flips:>9}{flips/max(pairs,1):>8.4f}"
              f"{top_changed/max(nprf,1):>12.4f}")


if __name__ == "__main__":
    main()
