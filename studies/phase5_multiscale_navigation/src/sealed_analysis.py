#!/usr/bin/env python3
"""Sealed round 1 analysis — run ONCE.

Order is fixed by the pre-registration and enforced here:

  1. CAL reliability gate (Krippendorff ordinal alpha >= 0.67). If it fails,
     the round ends with INSUFFICIENT RELIABILITY and TEST is not analysed.
  2. TEST-R primary endpoint (NavigationAP) and all secondary endpoints.
  3. TEST-C defect challenge.
  4. Hierarchical bootstrap, Holm correction, equivalence margin,
     catastrophic-stratum rule.
  5. Promotion matrix.

Nothing here may be re-run with different settings to obtain a nicer answer.
"""
import glob
import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

from mathmap_eval import composition as C          # noqa: E402
from mathmap_eval import navigation as N           # noqa: E402
from mathmap_eval import rankings as R             # noqa: E402
from mathmap_eval import reliability as REL        # noqa: E402
from mathmap_eval.corpus import get_corpus         # noqa: E402

SEALED = os.path.join(ROOT, "review", "sealed_r1")
OUT = os.path.join(ROOT, "data", "sealed_r1_results.json")
GATE = 0.67
MARGIN = 0.02          # practical equivalence, AP units
CATASTROPHIC = 0.10    # per-band shortfall that disqualifies
BOOT = 2000
SEED = 20260825
BANDS = ["0-10", "11-25", "26-50", "51-75", "76-125", "126+"]


def load_raters(prefix):
    out = {}
    for f in sorted(glob.glob(os.path.join(SEALED, f"grades_{prefix}*.json"))):
        out[os.path.basename(f)[7:-5]] = json.load(open(f))
    return out


def median_grades(per_rater, keymap, splits):
    """incidence -> median grade, restricted to the named splits."""
    want = {p for p, v in keymap.items() if v["split"] in splits}
    votes = defaultdict(list)
    moves, missing = {}, defaultdict(list)
    causes = defaultdict(list)
    for rn, rr in per_rater.items():
        for pid, ent in (rr or {}).items():
            if pid not in want:
                continue
            k = keymap[pid]
            missing[pid].append(bool(ent.get("missing_key")))
            moves.setdefault(pid, []).append(ent.get("moves", ""))
            for num, g in (ent.get("grades") or {}).items():
                inc = k["items"].get(str(num), k["items"].get(int(num)))
                if inc is None:
                    continue
                try:
                    votes[int(inc)].append(int(g))
                except (TypeError, ValueError):
                    continue
            for num, cz in (ent.get("causes") or {}).items():
                inc = k["items"].get(str(num), k["items"].get(int(num)))
                if inc is not None:
                    causes[int(inc)].append(str(cz))
    return ({i: int(np.median(v)) for i, v in votes.items()},
            {i: v for i, v in votes.items()}, moves, missing, causes)


def subset_keymap(keymap, splits=None, stratum=None):
    return {p: v for p, v in keymap.items()
            if (splits is None or v["split"] in splits)
            and (stratum is None or v["stratum"] == stratum)}


def main():
    c = get_corpus()
    keymap = json.load(open(os.path.join(SEALED, "keymap.json")))
    manifest = json.load(open(os.path.join(ROOT, "SEALED_R1_MANIFEST.json")))
    base = np.where(c.universe("U1D"))[0]
    names = R.names()
    results = {"round": "SEALED-R1", "manifest": manifest, "gate": {},
               "test_r": {}, "test_c": {}, "decision": {}}

    # ---------------- 1. CAL reliability gate ---------------------------
    cal_raters = load_raters("cal_")
    cal_keys = subset_keymap(keymap, {"CAL"})
    rel = REL.agreement_report(cal_raters, cal_keys, gate=GATE)
    results["gate"] = rel
    print("=" * 78)
    print("STEP 1 — CAL RELIABILITY GATE")
    print(f"  rater files      : {len(cal_raters)}")
    print(f"  multi-rated units: {rel['n_units_multi_rated']}")
    print(f"  alpha (ordinal)  : {rel['alpha_ordinal']:.4f}   gate {GATE}")
    print(f"  alpha (nominal)  : {rel['alpha_nominal']:.4f}")
    print(f"  exact / adjacent : {rel['ExactAgreement']:.3f} / "
          f"{rel['AdjacentAgreement']:.3f}")
    print(f"  PASSES GATE      : {rel['passes_gate']}")
    for b, v in rel["by_band"].items():
        a = v["alpha_ordinal"]
        print(f"    {b:<9} alpha {a:.3f}" if a is not None else f"    {b:<9} -")
    if not rel["passes_gate"]:
        results["decision"] = {"outcome": "INSUFFICIENT RELIABILITY",
                               "reason": f"CAL alpha {rel['alpha_ordinal']:.4f} "
                                         f"< {GATE}; TEST not analysed"}
        json.dump(results, open(OUT, "w"), indent=1, default=float)
        print("\nGATE FAILED — TEST is NOT analysed. Round ends.")
        return 1

    # ---------------- 2. TEST-R primary ---------------------------------
    test_raters = load_raters("test")
    grades, votes, moves, missing, causes = median_grades(
        test_raters, keymap, {"TEST-R"})
    kr = subset_keymap(keymap, {"TEST-R"})
    print("\n" + "=" * 78)
    print("STEP 2 — TEST-R PRIMARY ENDPOINT")
    print(f"  proofs {len(kr)}  graded candidates {len(grades)}")

    per_proof, nav = {}, {}
    for nm in names:
        ranks = R.get(nm).ranks_within_proof(c, base)
        nav[nm] = N.navigation_metrics(c, base, ranks, grades, kr)
        pr = N.per_proof_orders(c, base, ranks, grades, kr)
        per_proof[nm] = {p["pid"]: (N._ap(p["grades"] >= 2), p["band"])
                         for p in pr}
    results["test_r"]["navigation"] = nav

    order = sorted(names, key=lambda n: -(nav[n]["NavigationAP"] or 0))
    print(f"\n  {'ranking':<22}{'NavAP':>8}{'MajorAP':>9}{'BadDemAP':>10}"
          f"{'clean@1':>9}{'recall(maj)@4':>15}")
    for nm in order:
        v = nav[nm]
        cv = {x["k"]: x for x in v["curve"]}
        print(f"  {nm:<22}{v['NavigationAP']:>8.3f}{v['MajorAP']:>9.3f}"
              f"{v['BadEdgeDemotionAP']:>10.3f}"
              f"{cv[1]['NavigationCleanliness']:>9.3f}"
              f"{cv[4]['MajorMathCoverage']:>15.3f}")

    # ---------------- 3. hierarchical bootstrap + Holm -------------------
    leader = order[0]
    pids = sorted(p for p in per_proof[leader]
                  if per_proof[leader][p][0] is not None)
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(pids), (BOOT, len(pids)))
    comps = []
    for other in order[1:]:
        a = np.array([per_proof[leader][p][0] for p in pids])
        b = np.array([per_proof[other][p][0]
                      if per_proof[other].get(p, (None,))[0] is not None
                      else np.nan for p in pids])
        ok = ~np.isnan(b)
        d = (a - b)[ok]
        bs = d[idx[:, :len(d)] % len(d)].mean(axis=1)
        comps.append({"vs": other, "delta": float(d.mean()),
                      "ci95": [float(np.percentile(bs, 2.5)),
                               float(np.percentile(bs, 97.5))],
                      "p_raw": float((bs <= 0).mean()), "n": int(len(d))})
    m = len(comps)
    for i, cc in enumerate(sorted(comps, key=lambda x: x["p_raw"])):
        cc["p_holm"] = min(1.0, cc["p_raw"] * (m - i))
    results["test_r"]["comparisons"] = comps
    print(f"\n  paired hierarchical bootstrap ({BOOT}x), leader = {leader}")
    print(f"  {'vs':<22}{'dAP':>8}{'95% CI':>20}{'p_holm':>9}{'verdict':>16}")
    for cc in comps:
        v = ("SUPERIOR" if cc["ci95"][0] > MARGIN else
             "equivalent" if abs(cc["delta"]) <= MARGIN
             and cc["ci95"][1] <= MARGIN else
             "better" if cc["ci95"][0] > 0 else "not separated")
        ci = f"[{cc['ci95'][0]:+.3f},{cc['ci95'][1]:+.3f}]"
        print(f"  {cc['vs']:<22}{cc['delta']:>8.3f}{ci:>20}"
              f"{cc['p_holm']:>9.4f}{v:>16}")

    # ---------------- catastrophic stratum rule --------------------------
    band_best = {}
    for b in BANDS:
        vals = [(nav[n]["by_target_depth"].get(b, {}).get("NavigationAP"), n)
                for n in names]
        vals = [(v, n) for v, n in vals if v is not None]
        if vals:
            band_best[b] = max(vals)[0]
    disq = {}
    for nm in names:
        worst = None
        for b in BANDS:
            v = nav[nm]["by_target_depth"].get(b, {}).get("NavigationAP")
            if v is None or b not in band_best:
                continue
            gap = band_best[b] - v
            if worst is None or gap > worst[1]:
                worst = (b, gap)
        if worst:
            disq[nm] = {"worst_band": worst[0], "gap": worst[1],
                        "disqualified": worst[1] > CATASTROPHIC}
    results["test_r"]["catastrophic_rule"] = disq

    # ---------------- 4. TEST-C -----------------------------------------
    gc, votes_c, moves_c, missing_c, causes_c = median_grades(
        test_raters, keymap, {"TEST-C"})
    print("\n" + "=" * 78)
    print("STEP 3 — TEST-C DEFECT CHALLENGE")
    tc = {}
    strata = sorted({v["stratum"] for v in keymap.values() if v["stratum"]})
    for st in strata:
        ks = subset_keymap(keymap, {"TEST-C"}, st)
        row = {}
        for nm in names:
            ranks = R.get(nm).ranks_within_proof(c, base)
            row[nm] = N.navigation_metrics(c, base, ranks, gc, ks)
        tc[st] = row
        lead = row[leader]
        cv = {x["k"]: x for x in lead["curve"]}
        print(f"  {st:<22} n={lead['n_proofs']:<4} leader defect@1="
              f"{1 - cv[1]['NavigationCleanliness']:.3f}  NavAP={lead['NavigationAP']:.3f}")
    results["test_c"]["by_stratum"] = tc
    cause_counts = defaultdict(int)
    for v in causes_c.values():
        for x in v:
            cause_counts[x] += 1
    results["test_c"]["defect_causes"] = dict(cause_counts)
    print(f"  defect causes: {dict(cause_counts)}")

    # ---------------- 5. decision ---------------------------------------
    lead_disq = disq.get(leader, {}).get("disqualified", False)
    simpler = [n for n in order[1:]
               if any(cc["vs"] == n and abs(cc["delta"]) <= MARGIN
                      and cc["ci95"][1] <= MARGIN for cc in comps)]
    if lead_disq:
        outcome = "PARETO / TASK-SPECIFIC"
        reason = (f"{leader} leads overall but fails the catastrophic-stratum "
                  f"rule in band {disq[leader]['worst_band']}")
    elif simpler:
        outcome = "NON-INFERIOR / SIMPLER"
        reason = f"{simpler} are within the {MARGIN} equivalence margin"
    elif all(cc["ci95"][0] > MARGIN for cc in comps):
        outcome = "PROMOTE"
        reason = (f"{leader} exceeds every rival by more than the "
                  f"{MARGIN} margin with Holm-corrected CIs excluding zero")
    elif all(cc["ci95"][0] > 0 for cc in comps):
        outcome = "PROMOTE"
        reason = (f"{leader} beats every rival with CIs excluding zero, "
                  f"though some margins are within {MARGIN}")
    else:
        outcome = "PARETO / TASK-SPECIFIC"
        reason = "no ranking separates from all rivals"
    results["decision"] = {"outcome": outcome, "leader": leader,
                           "reason": reason, "margin": MARGIN}
    print("\n" + "=" * 78)
    print(f"DECISION: {outcome}\n  leader: {leader}\n  {reason}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(results, open(OUT, "w"), indent=1, default=float)
    print(f"\nwritten {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
