#!/usr/bin/env python3
"""PRINCIPLE 7: navigability of the whole map, per aggregation rule.

Builds the top-k graph over the WHOLE U1D corpus (18.1M incidences, 747,605
proofs) for each rule and asks how much of the giant component survives
deleting every edge whose cited declaration is machinery.

junk_mask = `corpus.inc_glue` (decl_logic_only | machinery), the frozen V8
descriptive statistic. It is the best corpus-wide junk estimate available;
graded labels exist for 552 proofs only. Stated, not assumed.

Usage:  run_social_choice_nav.py [frac]     frac<1 subsamples artifacts (timing)
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

from mathmap_eval import battery as B                    # noqa: E402
from mathmap_eval.corpus import get_corpus               # noqa: E402
import social_choice as SC                               # noqa: E402
from run_social_choice import reference_scores, ranks_within_proof  # noqa: E402

OUT = os.path.join(ROOT, "results", "social_choice")
K = 4


def main():
    frac = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    t0 = time.time()
    c = get_corpus()
    base = np.where(c.universe("U1D"))[0]
    if frac < 1.0:
        arts = np.unique(c.inc_artifact[base])
        rng = np.random.default_rng(20260821)
        keep = rng.random(len(arts)) < frac
        base = base[np.isin(c.inc_artifact[base], arts[keep])]
    print(f"base {len(base)} incidences  ({time.time()-t0:.0f}s)", flush=True)

    sig = SC.Signals(c)
    keys = sig.keys(base)
    tier = sig.tier(base)
    refs = reference_scores(c, base, sig, tier)
    anchor = refs["REF*_role5w_x_logdepth_x_rarity"]
    ctx = {"tier": tier.astype(np.float64), "anchor": anchor}
    print(f"signals ready ({time.time()-t0:.0f}s)", flush=True)

    rules = dict(SC.RULES)
    rules["veto_below_t2"] = SC.make_veto(2)
    rules["veto_below_t3"] = SC.make_veto(3)
    rules["role_lex"] = SC.role_lex
    for k in ("condorcet", "copeland", "borda"):
        rules[f"HYB_{k}_first"] = SC.make_first_anchor(k)

    ranks = {}
    agg = SC.Aggregator(c, base, keys, SC.VOTERS, ctx=ctx, budget=1.2e8)
    r6, extra = agg.run(rules, as_ranks=True)
    ranks.update({f"{k}6": v for k, v in r6.items()})
    print(f"6-voter pass done ({time.time()-t0:.0f}s)", flush=True)
    del r6

    for v in ("role", "rarity"):
        agg2 = SC.Aggregator(c, base, keys, SC.VOTERS, mult={v: 2}, ctx=ctx,
                             budget=1.2e8)
        r6b, _ = agg2.run({"borda": SC.borda, "copeland": SC.copeland},
                          as_ranks=True)
        ranks.update({f"{k}6_{v}x2": vv for k, vv in r6b.items()})
        print(f"multiplicity pass {v} done ({time.time()-t0:.0f}s)", flush=True)
        del r6b

    for name, sc in refs.items():
        ranks[name] = ranks_within_proof(c, base, sc)
    print(f"reference ranks done ({time.time()-t0:.0f}s)", flush=True)

    junk = c.inc_glue[base]
    print(f"junk share of all candidate edges: {junk.mean():.4f}", flush=True)
    rows = {}
    for name in sorted(ranks):
        nav = B.navigability(c, base, ranks[name].astype(np.int64), K, junk)
        rows[name] = nav
        print(f"{name:<30} junk@{K} {nav['junk_edge_share']:.4f}  "
              f"giant {nav['all_edges']['giant_fraction']:.4f} -> "
              f"{nav['mathematics_only']['giant_fraction']:.4f}  "
              f"retained {nav['giant_retained_without_junk']:.4f}  "
              f"comps {nav['all_edges']['components']} -> "
              f"{nav['mathematics_only']['components']}  "
              f"({time.time()-t0:.0f}s)", flush=True)

    os.makedirs(OUT, exist_ok=True)
    tag = "full" if frac >= 1.0 else f"sample{frac}"
    with open(os.path.join(OUT, f"navigability_{tag}.json"), "w") as f:
        json.dump(rows, f, indent=1, default=float)
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
