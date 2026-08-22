#!/usr/bin/env python3
"""Deep comparison: where does the map win, how does it fail, and how do
its answers DIFFER IN KIND from an LLM's?

Conditions scored:
  map      Lambda co-use from the statement world, top 10
  plain    LLM, statement only (run 1)
  repeat   LLM, statement only (run 2, independent agent) -> self-consistency
  blind    LLM, statement anonymised -> memorisation probe
  aug      LLM shown the map's top 10 as structural hints -> product value

Analyses:
  1. headline recall + the augmentation delta
  2. LLM run-to-run instability (the only thing that makes determinism
     an advantage rather than a slogan)
  3. NEAR MISS: when a system misses, how close did it get? namespace
     prefix match, and token overlap with the true answer
  4. SOLUTION CHARACTER: depth, popularity (in-degree), area, and
     abstraction level of what each system proposes
  5. every case where the map beat the LLM, itemised
"""
import json
import os
import sys
from collections import defaultdict
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_tree import load_common

D = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "llm_vs_map"))
doc = json.load(open(os.path.join(D, "tasks.json")))
tasks = {t["id"]: t for t in doc["tasks"]}

def load(cond):
    out = {}
    for s in "AB":
        p = os.path.join(D, f"llm_{cond}_{s}.json")
        if os.path.exists(p):
            out.update(json.load(open(p)))
    return out

preds = {"map": {i: t["map_top10"] for i, t in tasks.items()}}
for c in ("named", "blind", "aug", "repeat"):
    preds[c] = load(c)
preds["plain"] = preds.pop("named")

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int64)
indeg = nodes["in_degree"].astype(np.int64)
nid = {n: i for i, n in enumerate(names)}

def rec(p, truth):
    return len(set(p) & set(truth)) / len(truth)

print("=== 1. HEADLINE ===")
head = {}
for c in ("map", "plain", "repeat", "blind", "aug"):
    v = [rec(preds[c][i], t["answers"]) for i, t in tasks.items()
         if preds[c].get(i) is not None]
    head[c] = float(np.mean(v))
    print(f"  {c:8s} recall@10 {head[c]:.3f}  (n={len(v)})")
print(f"  augmentation delta (aug - plain): {head['aug'] - head['plain']:+.3f}")

# paired on aug vs plain
pa = [(rec(preds["plain"][i], t["answers"]), rec(preds["aug"][i], t["answers"]))
      for i, t in tasks.items()]
print(f"  aug better {np.mean([b > a for a, b in pa]):.3f}  "
      f"worse {np.mean([b < a for a, b in pa]):.3f}  "
      f"same {np.mean([b == a for a, b in pa]):.3f}")
# did aug adopt the hints?
adopt, adopt_correct = [], []
for i, t in tasks.items():
    if not t["map_top10"]:
        continue
    a = set(preds["aug"][i]); m = set(t["map_top10"]); p = set(preds["plain"][i])
    adopt.append(len(a & m) / 10.0)
    newly = (a & m) - p
    adopt_correct.append(len(newly & set(t["answers"])))
print(f"  hints adopted into final answer: {np.mean(adopt):.3f} of 10 slots")
print(f"  hint-adopted names that were CORRECT and not in plain: "
      f"{sum(adopt_correct)} total")

print("\n=== 2. LLM RUN-TO-RUN INSTABILITY (map is deterministic) ===")
jac, rdelta, both_hit = [], [], []
for i, t in tasks.items():
    a, b = preds["plain"].get(i), preds["repeat"].get(i)
    if not a or not b:
        continue
    A, B = set(a), set(b)
    jac.append(len(A & B) / len(A | B))
    ra, rb = rec(a, t["answers"]), rec(b, t["answers"])
    rdelta.append(abs(ra - rb))
    both_hit.append((ra > 0, rb > 0))
print(f"  top-10 Jaccard between two independent runs: {np.mean(jac):.3f}")
print(f"  mean |recall difference| between runs:       {np.mean(rdelta):.3f}")
flip = np.mean([x != y for x, y in both_hit])
print(f"  items where one run scored and the other didn't: {flip:.3f}")

print("\n=== 3. NEAR MISS: how close is a miss? ===")
def ns(n):
    return ".".join(n.split(".")[:-1])
def toks(n):
    return {x.lower() for x in n.replace("'", "").split(".") if x}
for c in ("map", "plain"):
    pref, tok, dd = [], [], []
    for i, t in tasks.items():
        p = preds[c].get(i)
        if not p:
            continue
        for a in t["answers"]:
            if a in p:
                continue                       # a hit, not a miss
            pref.append(any(ns(x) == ns(a) for x in p))
            ta = toks(a)
            tok.append(max((len(ta & toks(x)) / len(ta | toks(x))
                            for x in p), default=0.0))
            ia = nid.get(a)
            if ia is not None:
                ds = [abs(int(depth[nid[x]]) - int(depth[ia]))
                      for x in p if x in nid]
                if ds:
                    dd.append(min(ds))
    print(f"  {c:6s} missed answers: same namespace proposed "
          f"{np.mean(pref):.3f} | best token overlap {np.mean(tok):.3f} "
          f"| closest proposal depth gap {np.median(dd):.0f}")

print("\n=== 4. SOLUTION CHARACTER (what KIND of thing is proposed) ===")
def profile(c):
    dp, ig, ar, ex = [], [], [], []
    for i, t in tasks.items():
        p = preds[c].get(i)
        if not p:
            continue
        ta = int(area[t["decl"]])
        for x in p:
            j = nid.get(x)
            ex.append(j is not None)
            if j is None:
                continue
            dp.append(int(depth[j])); ig.append(int(indeg[j]))
            ar.append(int(area[j]) == ta)
    return dict(exists=float(np.mean(ex)), depth=float(np.median(dp)),
                indeg_med=float(np.median(ig)),
                indeg_mean=float(np.mean(ig)), same_area=float(np.mean(ar)))
truth_prof = []
for t in tasks.values():
    for a in t["answers"]:
        j = nid.get(a)
        if j is not None:
            truth_prof.append((int(depth[j]), int(indeg[j]),
                               int(area[j]) == int(area[t["decl"]])))
print(f"  {'':8s} {'exists':>7} {'med depth':>10} {'med indeg':>10} "
      f"{'mean indeg':>11} {'same area':>10}")
tp = np.array([[a, b, c] for a, b, c in truth_prof])
print(f"  {'TRUTH':8s} {1.0:7.3f} {np.median(tp[:,0]):10.0f} "
      f"{np.median(tp[:,1]):10.0f} {tp[:,1].mean():11.1f} {tp[:,2].mean():10.3f}")
for c in ("map", "plain", "aug"):
    p = profile(c)
    print(f"  {c:8s} {p['exists']:7.3f} {p['depth']:10.0f} "
          f"{p['indeg_med']:10.0f} {p['indeg_mean']:11.1f} "
          f"{p['same_area']:10.3f}")

print("\n=== 5. CASES WHERE THE MAP BEAT THE LLM ===")
for i, t in tasks.items():
    m = rec(preds["map"][i], t["answers"])
    l = rec(preds["plain"][i], t["answers"])
    if m > l:
        got = [a for a in t["answers"] if a in preds["map"][i]]
        print(f"  {t['target']}")
        print(f"    depth {int(depth[t['decl']])}  area "
              f"{aname.get(int(area[t['decl']]), '?')}  map {m:.2f} vs llm {l:.2f}")
        for a in got:
            print(f"    FOUND {a} (rank {preds['map'][i].index(a)+1})")
        print(f"    llm proposed instead: {', '.join(preds['plain'][i][:4])}")

out = {"headline": head}
json.dump(out, open(os.path.join(D, "deep.json"), "w"), indent=1)
