#!/usr/bin/env python3
"""Head-to-head: map search vs an LLM at premise retrieval.

Task (identical for both): given ONLY a theorem's statement, name the
Mathlib declarations its proof will use. Answers = the proof's map
moves (GAPC zoom-1 edges), the same ground truth premise_retrieval.py
scores against. Held-out: the theorem's own edges are removed from the
graph before the map predicts.

Two LLM conditions, to bound the contamination Sam named:
  NAMED  statement WITH its real declaration name (an LLM that has
         memorised Mathlib can recall the proof from the name alone)
  BLIND  identical statement, name replaced by `target_thm`, and the
         module path withheld

The gap between them is a memorisation probe: a solver reasoning from
mathematics should barely notice; a solver recalling a specific proof
should collapse.

Writes data/llm_vs_map/{tasks.json, named_XX.md, blind_XX.md}.
"""
import json
import os
import re
import sys
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lean_source as LS
from merge_tree import load_common, load_edges

SEED = 20260913          # same holdout as premise_retrieval.py
NTASKS = 60
PER_BATCH = 10
TOPK = 10
MAX_SEEDS = 5
P5DATA = os.path.normpath(os.path.join(HERE, "..", "..",
                                       "phase5_multiscale_navigation", "data"))
OUT = os.path.normpath(os.path.join(HERE, "..", "data", "llm_vs_map"))
MODULES_TSV = "/Users/sam/mathmap_data/all_modules.tsv"

nodes, names, area, aname = load_common()
depth = nodes["depth"].astype(np.int32)
gen = nodes["gen"]; kind = nodes["kind"]
es, ed = load_edges("GAPC")
pool_mask = (~gen) & (kind == 0) & (depth >= 11)

module_of = {}
for line in open(MODULES_TSV):
    nm, _, mod = line.rstrip("\n").partition("\t")
    module_of[nm] = mod

inc = np.load(os.path.join(P5DATA, "incid.npz"))
arts = np.load(os.path.join(P5DATA, "artifacts.npz"))
certifies = arts["certifies"].astype(np.int64)
tgt = certifies[inc["artifact"].astype(np.int64)]
dec = inc["decl"].astype(np.int64)
sel = inc["in_stmt_world"].astype(bool) & (dec != tgt)
stmt_of = defaultdict(set)
for t, d in zip(tgt[sel], dec[sel]):
    if not gen[d]:
        stmt_of[int(t)].add(int(d))

rng = np.random.default_rng(SEED)
srcs = np.unique(es)
hold = set(rng.choice(srcs, len(srcs) // 10, replace=False).tolist())
adj = defaultdict(list)
radj = defaultdict(list)
moves_of = defaultdict(list)
for s, d in zip(es, ed):
    if s in hold:
        moves_of[s].append(d)
    else:
        adj[s].append(d)
        radj[d].append(s)

lam_nbrs = defaultdict(dict)
by_src = defaultdict(list)
for s, d in zip(es, ed):
    if s not in hold:
        by_src[s].append(d)
for s, ms in by_src.items():
    ms = sorted(set(ms))[:20]
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            a, b = ms[i], ms[j]
            if pool_mask[b]:
                lam_nbrs[a][b] = lam_nbrs[a].get(b, 0) + 1
            if pool_mask[a]:
                lam_nbrs[b][a] = lam_nbrs[b].get(a, 0) + 1

indeg = np.zeros(len(depth), np.int64)
for d, ss in radj.items():
    indeg[d] = len(ss)

# same query construction as premise_retrieval.py
queries = []
for s, ds in moves_of.items():
    S = stmt_of.get(int(s), set())
    S = {x for x in S if x in adj or x in lam_nbrs or pool_mask[x]}
    answers = sorted({d for d in ds if pool_mask[d]} - S)
    if S and answers:
        queries.append((int(s), sorted(S), answers))
rng.shuffle(queries)

AUXSEG = {"casesOn", "recOn", "brecOn", "below", "noConfusion", "rec"}
def is_aux(n):
    return any(s in AUXSEG or s.startswith("_") for s in n.split("."))

tasks = []
for t, S, answers in queries:
    if len(tasks) >= NTASKS:
        break
    nm = names[t]
    if is_aux(nm):
        continue
    mod = module_of.get(nm, "")
    if not mod.startswith("Mathlib.") or mod.startswith("Mathlib.Tactic"):
        continue
    src = LS.lookup(nm, mod, want_body=False)
    if src is None or src["how"] != "exact" or not src.get("statement"):
        continue
    stmt = src["statement"].rstrip()
    if len(stmt) > 1400 or len(stmt) < 20:
        continue
    # map prediction: Lambda from the statement world, top-K
    sl = defaultdict(float)
    for x in S:
        for c, v in lam_nbrs.get(x, {}).items():
            sl[c] += v
    for x in S:
        sl.pop(x, None)
    sl.pop(t, None)
    top = sorted(sl, key=lambda c: (-sl[c], indeg[c]))[:TOPK]
    tasks.append({
        "id": "q%02d" % (len(tasks) + 1),
        "decl": int(t),
        "target": nm,
        "module": mod,
        "statement": stmt,
        "n_stmt_world": len(S),
        "answers": [names[a] for a in answers],
        "map_top10": [names[c] for c in top],
    })

os.makedirs(OUT, exist_ok=True)
json.dump({"seed": SEED, "n": len(tasks), "topk": TOPK, "tasks": tasks},
          open(os.path.join(OUT, "tasks.json"), "w"), indent=1)
print(f"tasks: {len(tasks)}  mean answers "
      f"{np.mean([len(t['answers']) for t in tasks]):.1f}")

INSTR = """\
# Premise retrieval — batch {bt}

For each Lean 4 / Mathlib theorem below you are shown ONLY its statement.
The proof is not shown and you must not try to recall the file.

For each item, predict which Mathlib declarations the PROOF uses: name
the {k} declarations you judge most likely to be cited by the proof,
most likely first. Rules:

- Give fully-qualified Mathlib names exactly as they appear in the
  library (e.g. `Finset.sum_congr`, `Polynomial.degree_mul`).
- Predict the substantive mathematical lemmas/definitions the proof
  builds on, not tactic-level plumbing (`Eq.mpr`, `congrArg`, `rfl`,
  `id`) and not things already named in the statement itself.
- Exactly {k} names per item, no commentary, no duplicates.

Answer as JSON only:
{{"q01": ["Name.one", "Name.two", ...], "q02": [...], ...}}

---

"""

def write_batches(cond):
    files = []
    for bi in range(0, len(tasks), PER_BATCH):
        chunk = tasks[bi:bi + PER_BATCH]
        bt = "%02d" % (bi // PER_BATCH + 1)
        parts = [INSTR.format(bt=bt, k=TOPK)]
        for t in chunk:
            stmt = t["statement"]
            if cond == "blind":
                short = t["target"].split(".")[-1]
                stmt = re.sub(r"\b" + re.escape(t["target"]) + r"\b",
                              "target_thm", stmt)
                stmt = re.sub(r"\b" + re.escape(short) + r"\b",
                              "target_thm", stmt)
                head = f"## {t['id']}\n"
            else:
                head = (f"## {t['id']}  `{t['target']}`\n"
                        f"module: `{t['module']}`\n")
            parts.append(head + "\n```lean\n" + stmt + "\n```\n")
        p = os.path.join(OUT, f"{cond}_{bt}.md")
        open(p, "w").write("\n".join(parts))
        files.append(p)
    return files

for cond in ("named", "blind"):
    fs = write_batches(cond)
    print(f"{cond}: {len(fs)} batches")

tpl = {t["id"]: None for t in tasks}
json.dump(tpl, open(os.path.join(OUT, "answer_template.json"), "w"), indent=1)
