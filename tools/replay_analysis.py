#!/usr/bin/env python3
"""Replay v2 analysis: node/theorem replay rates, residual failure heads,
inference-shadow tiers for data arguments, and the 100%-replayable subsets
that gate all G-rung interpretation."""
import json, sys, collections

def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def analyze(tag, rows):
    print(f"=== {tag} ===")
    thm_total = thm_ok = 0
    node_total = node_ok = 0
    fail_heads = collections.Counter()
    tiers = collections.Counter()          # overall tier
    tiers_by_cls = collections.defaultdict(collections.Counter)
    t3_shape = collections.Counter()       # shape of genuine-fabrication args
    t3_value_shape = collections.Counter() # ... restricted to cls == value
    t3_fvar = collections.Counter()
    sub = collections.Counter()            # raw t1/t2 status pairs
    subset = []
    errs = 0
    for r in rows:
        if "error" in r:
            errs += 1
            continue
        thm_total += 1
        if r.get("all_ok"):
            thm_ok += 1
            subset.append(r["n"])
        for nd in r.get("nodes", []):
            node_total += 1
            if nd["ok"]:
                node_ok += 1
            else:
                fail_heads[nd["head"]] += 1
            for da in nd.get("data_args", []):
                t1, t2 = da["t1"], da["t2"]
                sub[(t1, t2)] += 1
                if t1 == "untested":
                    tier = "untested"
                elif t1 == "det":
                    tier = "T1"
                elif t2 == "det":
                    tier = "T2"
                else:
                    tier = "T3"
                tiers[tier] += 1
                tiers_by_cls[da["cls"]][tier] += 1
                if tier == "T3":
                    t3_shape[da["shape"]] += 1
                    t3_fvar["has_fvar" if da["has_fvar"] else "closed"] += 1
                    if da["cls"] == "value":
                        t3_value_shape[da["shape"]] += 1
    print(f"theorems: {thm_ok}/{thm_total} fully replayable "
          f"({100*thm_ok/max(1,thm_total):.1f}%)  errors={errs}")
    print(f"nodes:    {node_ok}/{node_total} ({100*node_ok/max(1,node_total):.2f}%)")
    print("residual failure heads:", dict(fail_heads.most_common(12)))
    total_args = sum(v for k, v in tiers.items())
    print(f"\ndata-argument occurrences: {total_args}")
    for k in ("T1", "T2", "T3", "untested"):
        print(f"  {k}: {tiers[k]} ({100*tiers[k]/max(1,total_args):.1f}%)")
    print("by class (type/instance/value):")
    for cls, c in sorted(tiers_by_cls.items()):
        tot = sum(c.values())
        print(f"  {cls:9s} n={tot:6d}  " +
              "  ".join(f"{k}={c[k]} ({100*c[k]/max(1,tot):.1f}%)"
                        for k in ("T1", "T2", "T3")))
    print("T3 shapes (all):", dict(t3_shape.most_common()))
    print("T3 shapes (cls=value):", dict(t3_value_shape.most_common()))
    print("T3 locality:", dict(t3_fvar))
    print("raw (t1,t2) statuses:", {f"{a}/{b}": n for (a, b), n in sub.most_common(14)})
    print()
    return subset

if __name__ == "__main__":
    root = "/Users/samlayton/my-repos/research/Map_Of_Mathematics/bigdata"
    s80 = analyze("replay80v2", load(f"{root}/replay80v2.jsonl"))
    s300 = analyze("replay300v2", load(f"{root}/replay300v2.jsonl"))
    with open(f"{root}/replayable_subsets.json", "w") as f:
        json.dump({"R80": s80, "R300": s300}, f, indent=1)
    print(f"subsets written: |R80|={len(s80)} |R300|={len(s300)}")
