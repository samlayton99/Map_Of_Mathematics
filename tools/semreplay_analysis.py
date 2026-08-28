#!/usr/bin/env python
"""Aggregate deterministic semantic replay: per-action failure classes.

Reads the `mathrecord semreplay` output and reports the decomposition the
semantic-conformance gate is scored on.  Every failing theorem resolves to
a NAMED mechanism - "dead end" and "budget" are not possible outcomes of
semantic replay, because replay has neither a frontier nor a budget.

Two independent failure surfaces are reported separately:

  EXTRACTION  a reference step has no IR v1 parameterization
              (reason string = the missing mechanism)
  REPLAY      the recorded IR did not execute
              (first discrepancy = the executor defect)

Usage: semreplay_analysis.py <semreplay_out.jsonl> [--ir]
"""
import argparse
import collections
import json
import statistics
import sys


def _count_lam(node):
    """Lambda-shaped data-oracle arguments in an IR subtree (motives)."""
    n = node.get("ndatalam", 0) or 0
    for k in node.get("kids", []):
        n += _count_lam(k)
    return n


def pct(a, b):
    return f"{100.0 * a / b:.1f}%" if b else "n/a"


def norm_reason(r):
    """Collapse a reason to its mechanism class (drop the instance payload
    after the first colon) so classes aggregate across theorems."""
    return r.split(":", 1)[0]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--ir", action="store_true",
                    help="also dump the IR of the first failing theorem")
    args = ap.parse_args(argv)

    rows = []
    with open(args.path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    errored = [r for r in rows if "error" in r]
    rows = [r for r in rows if "error" not in r]
    n = len(rows)
    if not n:
        print("no usable rows", file=sys.stderr)
        return 1

    clean = [r for r in rows if r["extract_clean"]]
    replayed = [r for r in rows if r["replay_ok"]]
    verified = [r for r in rows if r["verified"]]

    print(f"theorems                 {n}"
          + (f"  (+{len(errored)} harness errors)" if errored else ""))
    print(f"extraction clean         {len(clean):3d}/{n}  {pct(len(clean), n)}"
          "   (an IR v1 parameterization exists for every step)")
    print(f"semantic replay ok       {len(replayed):3d}/{n}  {pct(len(replayed), n)}"
          "   (recorded IR executed, no reference term)")
    print(f"kernel verified          {len(verified):3d}/{n}  {pct(len(verified), n)}")
    print()

    # ---- extraction failures: the action language is not expressive enough
    reasons = collections.Counter()
    thms_per_reason = collections.defaultdict(set)
    for r in rows:
        for u in r.get("unsupported", []):
            k = norm_reason(u)
            reasons[k] += 1
            thms_per_reason[k].add(r["n"])
    if reasons:
        print("EXTRACTION failures by mechanism "
              "(missing IR expressivity; count = actions, thms = theorems)")
        print("  NOTE: read the THEOREM column for 'how often does this "
              "mechanism block a proof'.  The action column is dominated by "
              "a few proofs with enormous machine-generated certificate "
              "trees (decision-procedure output), so action-weighting "
              "overstates whatever those particular proofs happen to hit.")
        for k, c in reasons.most_common():
            print(f"  {k:<34s} {c:5d} actions   {len(thms_per_reason[k]):3d} thms")
        print()
        # concentration: how much of the action count is a handful of proofs
        per_thm = collections.Counter()
        for r in rows:
            per_thm[r["n"]] = len(r.get("unsupported", []))
        tot_act = sum(per_thm.values())
        if tot_act:
            top = per_thm.most_common(5)
            share = sum(c for _, c in top) / tot_act
            print(f"  ACTION CONCENTRATION: the 5 most action-heavy failing "
                  f"proofs hold {share*100:.0f}% of all unsupported actions")
            for nm, c in top:
                print(f"      {c:5d}  {nm[:60]}")
            print()

    # ---- replay failures: executor defects, localized to one action
    disc = collections.Counter()
    disc_detail = collections.defaultdict(list)
    for r in rows:
        if r["replay_ok"]:
            continue
        d = r.get("first_discrepancy")
        if not d:
            disc["no_trace_entry"] += 1
            disc_detail["no_trace_entry"].append((r["n"], r.get("replay_err") or ""))
            continue
        key = f"{d.get('f', '?')}/{d.get('status', '?')}"
        disc[key] += 1
        disc_detail[key].append((r["n"], (d.get("detail") or "")[:110]))
    if disc:
        print("REPLAY first-discrepancy classes (family/status)")
        for k, c in disc.most_common():
            print(f"  {k:<34s} {c:5d} thms")
            for nm, det in disc_detail[k][:3]:
                print(f"      {nm}")
                if det:
                    print(f"        {det}")
        print()

    # ---- action family distribution over the whole corpus
    fams = collections.Counter()
    for r in rows:
        for k, v in (r.get("families") or {}).items():
            fams[k] += v
    total_actions = sum(fams.values())
    print(f"ACTION FAMILY distribution ({total_actions} actions)")
    for k, c in fams.most_common():
        print(f"  {k:<14s} {c:6d}  {pct(c, total_actions)}")
    print()

    # ---- compression and horizon
    cov = [r["n_covered"] for r in rows if r.get("n_raw")]
    rawv = [r["n_raw"] for r in rows if r.get("n_raw")]
    acts = [r["n_actions"] for r in rows if r.get("n_raw")]
    if rawv:
        tot_raw, tot_act = sum(rawv), sum(acts)
        print(f"CERTIFICATE COMPRESSION  {tot_act} semantic actions / "
              f"{tot_raw} certificate nodes = {tot_act / tot_raw:.3f}")
        per = [a / r for a, r in zip(acts, rawv) if r]
        print(f"  per-theorem ratio        median {statistics.median(per):.3f}  "
              f"min {min(per):.3f}  max {max(per):.3f}")
        print(f"  nodes absorbed by covers {sum(cov)}")
    hz = [r["horizon"] for r in rows]
    if hz:
        print(f"SEMANTIC HORIZON         median {statistics.median(hz):.0f}  "
              f"p90 {sorted(hz)[int(0.9 * (len(hz) - 1))]}  max {max(hz)}")
    print()
    print("FALLBACK                 0.0%  (semantic replay has no "
          "certificate-grain fallback path)")

    # ---- difficulty stratification -------------------------------
    def band(r):
        n = r.get("n_raw") or 0
        if n <= 3:   return "1 trivial  (<=3)"
        if n <= 12:  return "2 small    (4-12)"
        if n <= 28:  return "3 medium   (13-28)"
        if n <= 71:  return "4 large    (29-71)"
        if n <= 200: return "5 hard     (72-200)"
        return           "6 very hard (>200)"

    g = collections.defaultdict(list)
    for r in rows:
        if r.get("n_raw"):
            g[band(r)].append(r)
    if g:
        print()
        print("DIFFICULTY STRATIFICATION (band by certificate-node count of "
              "the reference proof)")
        print(f"  {'band':<20s} {'n':>5s} {'extract':>8s} {'replay':>8s} "
              f"{'verified':>9s} {'act-fail':>9s} {'timeout':>8s} {'oracle-lam':>11s}")
        for k in sorted(g):
            v = g[k]
            n = len(v)
            e = sum(1 for r in v if r["extract_clean"])
            rp = sum(1 for r in v if r["replay_ok"])
            ve = sum(1 for r in v if r["verified"])
            acts = sum(r["n_actions"] for r in v) or 1
            uns = sum(len(r.get("unsupported", [])) for r in v)
            tmo = sum(1 for r in v for u in r.get("unsupported", [])
                      if u.startswith("instrument_timeout"))
            lam = sum(_count_lam(r["ir"]) for r in v)
            print(f"  {k:<20s} {n:5d} {e/n*100:7.1f}% {rp/n*100:7.1f}% "
                  f"{ve/n*100:8.1f}% {uns/acts*100:8.2f}% {tmo:8d} {lam:11d}")
        print("  act-fail = share of ACTIONS with no IR parameterization; "
              "timeout = instrument-limit actions (must be ~0 to read the "
              "band as mathematics); oracle-lam = lambda-shaped data "
              "arguments replay consumes from the reference (motives - "
              "the genuine-fabrication class, not yet synthesized).")

    if args.ir:
        bad = next((r for r in rows if not r["replay_ok"] or not r["extract_clean"]),
                   None)
        if bad:
            print(f"\n--- IR of first failing theorem: {bad['n']} ---")
            print(json.dumps(bad["ir"], indent=1)[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
