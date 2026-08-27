#!/usr/bin/env python
"""Analyze prover ladder runs (bigdata/prover_out_<banks>.jsonl).

Per configuration: solve rate, verified rate, calls per solved theorem,
solve rate as a function of budget (from callsUsed), per-bank legality
census aggregated over all expansions, duplicate-child rate, zero-action
states, and which banks appear in successful proof paths.

Run: ~/venv/general_ml/bin/python prover_analysis.py [banks ...]
Writes tools/output/prover_ladder.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from atlas import BIG

OUT = Path(__file__).resolve().parent / "output"


def bank_of(label):
    if label.startswith("apply "):
        return "backward"
    if label.startswith("rw"):
        return "rewrite"
    if label == "simp":
        return "automation"
    return "structural"


def analyze(banks):
    path = BIG / f"prover_out_{banks}.jsonl"
    if not path.exists():
        return None
    rows = [json.loads(l) for l in open(path)]
    n = len(rows)
    solved = [r for r in rows if r["solved"]]
    att = Counter()
    leg = Counter()
    dups = exps = 0
    for r in rows:
        s = r["stats"]
        for k, v in s["attempts"].items():
            att[k] += v
        for k, v in s["legal"].items():
            leg[k] += v
        dups += s["dups"]
        exps += s["expansions"]
    budgets = (25, 50, 100, 200, 300, 400)
    solve_by_budget = {b: sum(1 for r in solved if r["calls"] <= b) / n
                       for b in budgets}
    path_banks = Counter()
    for r in solved:
        for lab in r["path"]:
            path_banks[bank_of(lab)] += 1
    return {
        "n": n,
        "solved": len(solved),
        "solve_rate": round(len(solved) / n, 4),
        "verified": sum(1 for r in solved if r["verified"]),
        "median_calls_when_solved": int(np.median([r["calls"] for r in solved]))
        if solved else None,
        "solve_rate_by_budget": {str(b): round(v, 4)
                                 for b, v in solve_by_budget.items()},
        "legality_census": {
            k: {"attempts": att[k], "legal": leg[k],
                "rate": round(leg[k] / max(att[k], 1), 4)}
            for k in sorted(att)},
        "expansions": exps,
        "duplicate_children": dups,
        "proof_path_bank_usage": dict(path_banks),
        "median_proof_length": int(np.median([len(r["path"]) for r in solved]))
        if solved else None,
        "example_proofs": [
            {"n": r["n"], "path": r["path"], "calls": r["calls"]}
            for r in solved[:8]],
    }


def main():
    configs = sys.argv[1:] or ["s", "sb", "sbr", "sbrp"]
    out = {}
    for c in configs:
        res = analyze(c)
        if res:
            out[c] = res
            print(f"== {c}: solved {res['solved']}/{res['n']} "
                  f"({res['solve_rate']:.1%}), verified {res['verified']}, "
                  f"median calls {res['median_calls_when_solved']}")
            print(f"   census: " + "  ".join(
                f"{k}:{v['rate']:.3f}({v['legal']}/{v['attempts']})"
                for k, v in res["legality_census"].items()))
            print(f"   path banks: {res['proof_path_bank_usage']}")
    OUT.mkdir(exist_ok=True)
    (OUT / "prover_ladder.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
