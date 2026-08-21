#!/usr/bin/env python3
"""Shortcut precision/recall for the social-choice schemes.

A since-removed `battery.navigability` test asked whether the map stays
CONNECTED without junk edges; `mathmap_eval/shortcuts` asks whether junk edges
create FALSE PROXIMITY, which is the question that actually discriminates.

junk_node = `corpus.decl_logic_only` (frozen V8 per-declaration flag).
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from mathmap_eval import shortcuts as SH                  # noqa: E402
from mathmap_eval.corpus import get_corpus                # noqa: E402
import social_choice as SC                                # noqa: E402
from run_social_choice import reference_scores, ranks_within_proof  # noqa: E402

OUT = os.path.join(ROOT, "results", "social_choice")
K = 4


def main():
    t0 = time.time()
    c = get_corpus()
    base = np.where(c.universe("U1D"))[0]
    sig = SC.Signals(c)
    keys = sig.keys(base)
    tier = sig.tier(base)
    refs = reference_scores(c, base, sig, tier)
    ctx = {"tier": tier.astype(np.float64),
           "anchor": refs["REF*_role5w_x_logdepth_x_rarity"]}
    rules = {"borda": SC.borda, "copeland": SC.copeland,
             "HYB_copeland_first": SC.make_first_anchor("copeland")}
    ranks = {}
    r, _ = SC.Aggregator(c, base, keys, SC.VOTERS, ctx=ctx,
                         budget=1.2e8).run(rules, as_ranks=True)
    ranks.update({f"{k}6": v for k, v in r.items()})
    r2, _ = SC.Aggregator(c, base, keys, SC.VOTERS, mult={"rarity": 2},
                          ctx=ctx, budget=1.2e8).run(
        {"borda": SC.borda, "copeland": SC.copeland}, as_ranks=True)
    ranks.update({f"{k}6_rarityx2": v for k, v in r2.items()})
    ranks["REF*"] = ranks_within_proof(
        c, base, refs["REF*_role5w_x_logdepth_x_rarity"])
    print(f"ranks ready ({time.time()-t0:.0f}s)", flush=True)

    junk_node = c.decl_logic_only
    keymap = json.load(open(os.path.join(SC.SEALED, "keymap.json")))
    grades = {}
    for sp in ("TEST-R", "TEST-C", "CAL"):
        grades.update(SC.load_grades(keymap, sp))

    rows = {}
    for name in sorted(ranks):
        res = SH.evaluate(c, base, ranks[name].astype(np.int64), K, junk_node,
                          grades=grades, keymap=keymap)
        rows[name] = res
        h, d = res["hubs"], res["distance"]
        rc = res.get("recall", {})
        print(f"{name:<24} hubs junk {h['junk_share_of_top_hubs']:.3f} "
              f"({h['enrichment']:.2f}x) mass {h['degree_mass_on_junk']:.3f} | "
              f"dist {d['mean_distance_all_edges']:.2f} -> "
              f"{d['mean_distance_mathematics_only']:.2f} "
              f"(+2 {d['pairs_lengthened_2plus']:.3f}, disc "
              f"{d['pairs_disconnected_by_removing_junk']:.3f}) | "
              f"recall maths {rc.get('graded_real_maths_reaching_hub_tail',0):.3f} "
              f"junk {rc.get('graded_junk_reaching_hub_tail',0):.3f} "
              f"({time.time()-t0:.0f}s)", flush=True)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "shortcuts_full.json"), "w") as f:
        json.dump(rows, f, indent=1, default=float)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
