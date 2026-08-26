#!/usr/bin/env python
"""Analyze the live legality probe output.

Joins bigdata/probe_out.jsonl (per goal: which candidates the elaborator
accepted backward, and how many subgoals each would open) with
bigdata/probe_meta.json (candidate provenance: structural pool / peer
retrieval / true cited premises).

Reports:
  - legality rate by candidate source (structural key vs peers vs truth)
  - legal-pool size: structural median 167 -> how many survive unification
  - representability: share of goals where >= 1 actually-cited premise is
    backward-applicable at the root goal (the rest were used forward, in
    rewrites, or on subgoals - a measure of how much of proving is NOT
    root-level backward application)
  - hyperedge arity: subgoals opened by legal moves (the instantiated
    G -> {A_1..A_k})

Run: ~/venv/general_ml/bin/python probe_analysis.py
Writes tools/output/legality_probe_results.json
"""
import json
from collections import Counter
from pathlib import Path

import numpy as np

from atlas import BIG

OUT = Path(__file__).resolve().parent / "output"


def main():
    meta = {m["n"]: m for m in json.loads((BIG / "probe_meta.json").read_text())}
    rows = []
    with open(BIG / "probe_out.jsonl") as f:
        for line in f:
            rows.append(json.loads(line))

    n_goals = 0
    legal_counts, struct_pool, struct_legal = [], [], []
    src_tried = Counter()
    src_legal = Counter()
    goals_with_legal_target = 0
    goals_with_any_target = 0
    arity = Counter()
    inst_open = Counter()

    for row in rows:
        if "error" in row:
            continue
        m = meta.get(row["n"])
        if m is None:
            continue
        n_goals += 1
        legal = {e["c"]: e for e in row["legal"]}
        legal_counts.append(len(legal))
        struct = set(m["struct"])
        peers = set(m["peers"])
        target = set(m["target"])
        struct_pool.append(len(struct))
        struct_legal.append(sum(1 for c in struct if c in legal))
        for src, group in (("struct", struct), ("peers", peers),
                           ("target", target)):
            src_tried[src] += len(group)
            src_legal[src] += sum(1 for c in group if c in legal)
        if target:
            goals_with_any_target += 1
            if any(c in legal for c in target):
                goals_with_legal_target += 1
        for e in row["legal"]:
            arity[e["ng"]] += 1
            inst_open[e["ni"]] += 1

    la = np.array(legal_counts)
    sp = np.array(struct_pool)
    sl = np.array(struct_legal)
    res = {
        "n_goals": n_goals,
        "legal_actions_per_goal": {
            "median": int(np.median(la)), "mean": round(float(la.mean()), 1),
            "p90": int(np.percentile(la, 90)), "zero": int((la == 0).sum()),
        },
        "structural_pool_vs_legal": {
            "pool_median": int(np.median(sp)),
            "legal_median": int(np.median(sl)),
            "legality_rate_struct": round(src_legal["struct"] /
                                          max(src_tried["struct"], 1), 4),
        },
        "legality_rate_by_source": {
            s: {"tried": src_tried[s], "legal": src_legal[s],
                "rate": round(src_legal[s] / max(src_tried[s], 1), 4)}
            for s in ("struct", "peers", "target")},
        "root_backward_representability": {
            "goals_with_cited_premise_legal_at_root": goals_with_legal_target,
            "share": round(goals_with_legal_target /
                           max(goals_with_any_target, 1), 4),
            "note": ("cited premises NOT legal at the root were used forward, "
                     "in rewrites, or on later subgoals - this bounds how much "
                     "of proving is root-level backward application"),
        },
        "hyperedge_arity_distribution": dict(sorted(arity.items())[:12]),
        "open_instance_goals_distribution": dict(sorted(inst_open.items())[:8]),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "legality_probe_results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
