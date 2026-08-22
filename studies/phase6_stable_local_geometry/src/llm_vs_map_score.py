#!/usr/bin/env python3
"""Score the map-vs-LLM head-to-head.

Both systems emit exactly 10 fully-qualified names per theorem from the
statement alone; recall@10 = fraction of the proof's true map moves that
appear in the list. Also reports:
  - name validity (does the predicted name exist in Mathlib at all) --
    an LLM that hallucinates plausible names cannot be used as a
    retriever regardless of its mathematical taste
  - the NAMED vs BLIND gap: memorisation sensitivity
  - complementarity: of all true moves, who found what
  - union recall: map top-10 + LLM top-10 as one 20-slot candidate set
"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, "..", "data", "llm_vs_map"))
P5DATA = os.path.normpath(os.path.join(HERE, "..", "..",
                                       "phase5_multiscale_navigation", "data"))

doc = json.load(open(os.path.join(D, "tasks.json")))
tasks = {t["id"]: t for t in doc["tasks"]}
allnames = set(json.load(open(os.path.join(P5DATA, "names.json"))))

def load(cond):
    out = {}
    for suf in ("A", "B"):
        p = os.path.join(D, f"llm_{cond}_{suf}.json")
        if os.path.exists(p):
            out.update(json.load(open(p)))
    return out

named = load("named")
blind = load("blind")
print(f"tasks {len(tasks)}  named answers {len(named)}  blind {len(blind)}")

def recall(pred, truth):
    if not truth:
        return None
    return len(set(pred) & set(truth)) / len(truth)

rows = []
for tid, t in tasks.items():
    truth = t["answers"]
    r = {"id": tid, "target": t["target"], "n_answers": len(truth)}
    r["map"] = recall(t["map_top10"], truth)
    for cond, src in (("named", named), ("blind", blind)):
        p = src.get(tid)
        if p is None:
            r[cond] = None
            r[cond + "_valid"] = None
            continue
        p = list(dict.fromkeys(p))[:10]
        r[cond] = recall(p, truth)
        r[cond + "_valid"] = np.mean([x in allnames for x in p])
    if named.get(tid) is not None:
        r["union"] = recall(list(t["map_top10"]) + list(named[tid]), truth)
    rows.append(r)

def agg(key):
    v = [r[key] for r in rows if r.get(key) is not None]
    return float(np.mean(v)) if v else None

res = {
    "n": len(rows),
    "mean_answers": float(np.mean([r["n_answers"] for r in rows])),
    "recall10_map": agg("map"),
    "recall10_llm_named": agg("named"),
    "recall10_llm_blind": agg("blind"),
    "recall20_union_map_plus_named": agg("union"),
    "name_validity_named": agg("named_valid"),
    "name_validity_blind": agg("blind_valid"),
}

# complementarity over individual true moves (named condition)
both = maponly = llmonly = neither = 0
for tid, t in tasks.items():
    p = named.get(tid)
    if p is None:
        continue
    m, l = set(t["map_top10"]), set(p)
    for a in t["answers"]:
        inm, inl = a in m, a in l
        if inm and inl: both += 1
        elif inm: maponly += 1
        elif inl: llmonly += 1
        else: neither += 1
tot = both + maponly + llmonly + neither
if tot:
    res["moves_both"] = both / tot
    res["moves_map_only"] = maponly / tot
    res["moves_llm_only"] = llmonly / tot
    res["moves_neither"] = neither / tot
    res["n_moves_scored"] = tot

# per-item paired comparison
paired = [(r["map"], r["named"]) for r in rows if r.get("named") is not None]
res["map_better"] = float(np.mean([m > l for m, l in paired]))
res["llm_better"] = float(np.mean([l > m for m, l in paired]))
res["tie"] = float(np.mean([l == m for m, l in paired]))

print(json.dumps(res, indent=1))
json.dump({"summary": res, "rows": rows},
          open(os.path.join(D, "scores.json"), "w"), indent=1)
