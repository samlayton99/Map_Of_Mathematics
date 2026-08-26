#!/usr/bin/env python
"""Deliverable D: failure taxonomy for the prover, from run outputs.

For every theorem the baseline (T1, sbrp) failed, assign the strongest
supported categories using the oracle matrix and task metadata:

  J  source-accessibility: the recorded proof needs same-module premises
     that the conservative regime removes
  A  premise absent: an accessible recorded premise missing from toolkit
  RETRIEVAL  solved under T2 (oracle premises) but not T1
  TRUNCATION solved under T3 (large pool) but not T1
  SCHEDULING solved with goal selection (gsel) but not T1
  E  frontier exhausted below budget: action-language coverage gap
  BUDGET     budget exhausted with a live frontier: search/ranking limited

Categories are not exclusive; percentages reported per category over all
T1 failures.  Run after the oracle matrix runs complete.

Run: ~/venv/general_ml/bin/python failure_taxonomy.py
Writes tools/output/prover_failure_taxonomy.json
"""
import json
from pathlib import Path

from atlas import BIG

OUT = Path(__file__).resolve().parent / "output"


def load(fn):
    p = BIG / fn
    if not p.exists():
        return {}
    return {r["n"]: r for r in map(json.loads, open(p))}


def main():
    t1 = load("prover_out_v2_sbrp.jsonl")
    t2 = load("prover_out_v2_T2.jsonl")
    t3 = load("prover_out_v2_T3.jsonl")
    gs = load("prover_out_v2_gsel.jsonl")
    tasks = {t["n"]: t for t in
             json.load(open(BIG / "prover_tasks80.json"))["tasks"]}
    meta = {m["n"]: m for m in json.loads((BIG / "prover_tasks_meta.json").read_text())}

    failures = [n for n, r in t1.items() if not r["solved"]]
    cats = {c: [] for c in ("J_same_module_premises", "A_premise_absent",
                            "RETRIEVAL_oracle_fixes", "TRUNCATION_bigpool_fixes",
                            "SCHEDULING_goalsel_fixes", "E_frontier_exhausted",
                            "BUDGET_exhausted")}
    rows = []
    for n in failures:
        m = meta.get(n, {})
        task = tasks.get(n, {})
        tags = []
        target = set(m.get("target", []))
        target_acc = set(m.get("target_accessible", []))
        if target - target_acc:
            tags.append("J_same_module_premises")
        if target_acc - set(task.get("bw", [])):
            tags.append("A_premise_absent")
        if t2.get(n, {}).get("solved"):
            tags.append("RETRIEVAL_oracle_fixes")
        if t3.get(n, {}).get("solved"):
            tags.append("TRUNCATION_bigpool_fixes")
        if gs.get(n, {}).get("solved"):
            tags.append("SCHEDULING_goalsel_fixes")
        r = t1[n]
        if r["frontier_left"] == 0 and r["calls"] < 300:
            tags.append("E_frontier_exhausted")
        if r["calls"] >= 300:
            tags.append("BUDGET_exhausted")
        for t in tags:
            cats[t].append(n)
        rows.append({"n": n, "tags": tags})

    nf = len(failures)
    out = {
        "n_failures": nf,
        "category_share": {c: round(len(v) / nf, 4) for c, v in cats.items()},
        "category_counts": {c: len(v) for c, v in cats.items()},
        "per_theorem": rows,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "prover_failure_taxonomy.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "per_theorem"},
                     indent=1))


if __name__ == "__main__":
    main()
