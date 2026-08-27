#!/usr/bin/env python3
"""G-rung comparison, restricted to the 100%-replayable subset R80.

Rungs: aprime (A' free-search baseline, banks sbrh), g1 (exact head +
exact data), g2 (exact head, data left to unification/coupling), g3
(free search, reference head top-priority when tracked), condc (free
search + occurrence-specific data oracle)."""
import json, collections, sys

ROOT = "/Users/samlayton/my-repos/research/Map_Of_Mathematics/bigdata"

def load(tag):
    rows = {}
    try:
        with open(f"{ROOT}/prover_out_v2_{tag}.jsonl") as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    rows[r["n"]] = r
    except FileNotFoundError:
        pass
    return rows

def main(tags):
    subs = json.load(open(f"{ROOT}/replayable_subsets.json"))
    R80 = set(subs["R80"])
    runs = {t: load(t) for t in tags}
    allnames = None
    for t, rs in runs.items():
        if rs:
            allnames = list(rs.keys())
            break
    print(f"|R80| = {len(R80)} of {len(allnames)} benchmark theorems\n")
    print(f"{'rung':10s} {'solved/80':>10s} {'on R80':>10s} {'off-R80':>8s}")
    solved_sets = {}
    for t in tags:
        rs = runs[t]
        if not rs:
            print(f"{t:10s} (missing)")
            continue
        sv = {n for n, r in rs.items() if r.get("solved")}
        solved_sets[t] = sv
        on = len(sv & R80)
        print(f"{t:10s} {len(sv):>7d}/{len(rs)} {on:>6d}/{len(R80 & set(rs))} "
              f"{len(sv - R80):>8d}")
    print()
    # pairwise diffs on R80
    ts = [t for t in tags if t in solved_sets]
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            a, b = ts[i], ts[j]
            onlyA = (solved_sets[a] - solved_sets[b]) & R80
            onlyB = (solved_sets[b] - solved_sets[a]) & R80
            if onlyA or onlyB:
                print(f"{a} only (R80): {sorted(onlyA)}")
                print(f"{b} only (R80): {sorted(onlyB)}")
                print()
    # guided-bank legality census + failures of guided rungs on R80
    for t in ts:
        rs = runs[t]
        att = collections.Counter(); leg = collections.Counter()
        for r in rs.values():
            st = r.get("stats", {})
            for k, v in st.get("attempts", {}).items():
                att[k] += v
            for k, v in st.get("legal", {}).items():
                leg[k] += v
        gl = {k: f"{leg[k]}/{att[k]}" for k in att if k in
              ("guided", "dirty_rejected", "backward", "part")}
        print(f"{t}: bank legal/attempts {gl}")
        fails = sorted(n for n, r in rs.items()
                       if n in R80 and not r.get("solved"))
        if t in ("g1", "g2") and fails:
            print(f"  {t} failures on R80 ({len(fails)}): {fails[:20]}")
    print()

if __name__ == "__main__":
    main(sys.argv[1:] or ["aprime", "g1", "g2", "g3", "condc"])
