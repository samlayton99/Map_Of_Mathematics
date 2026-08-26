#!/usr/bin/env python
"""Typed legality, measured: what head-schema structure buys proof search.

From bigdata/mathlib_heads.jsonl (every declaration's conclusion head,
explicit-premise heads, and proof-term head), computes:

  1. Backward-candidate pools: for each goal head h, how many constants
     could attack a goal shaped h.  The "typed legality" compression of
     771k constants, measured against the actual goal-head distribution.
  2. The top-level move of every proof in Mathlib: the head of the proof
     term after intros.  What fraction of proofs open with a rewrite
     (Eq.mpr), a landmark (let), a hypothesis (VAR), a math theorem?
  3. Head-match rate: when the top move is a constant, how often does its
     conclusion head equal the goal's head (the unification proxy)?
  4. Next-move prediction, no ML: rank the goal-head pool by global
     citation frequency; recall@K of the actual top-level move.

Run: ~/venv/general_ml/bin/python heads_analysis.py
Writes tools/output/mathlib_heads_analysis.json
"""
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from atlas import load_dump, theorem_roots, BIG

OUT = Path(__file__).resolve().parent / "output"
HEADS = BIG / "mathlib_heads.jsonl"
KS = (1, 8, 16, 64, 256)


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def main():
    log("loading atlas...")
    a = load_dump()
    log("loading heads dump...")
    ch = {}     # name -> conclusion head tag
    ca = {}     # name -> head tags of first conclusion args
    vh = {}     # name -> value head tag (top-level move)
    ne = {}
    with open(HEADS) as f:
        for line in f:
            r = json.loads(line)
            ch[r["n"]] = r["ch"]
            ca[r["n"]] = r.get("ca", [])
            if r["vh"] is not None:
                vh[r["n"]] = r["vh"]
            ne[r["n"]] = r["ne"]
    log(f"{len(ch):,} head rows")

    def refined_key(nm):
        """Goal index key: head, refined by the LHS head for the huge
        relational classes (Eq/Iff/orders) where the bare head is vacuous."""
        h = ch.get(nm)
        if h is None:
            return None
        args = ca.get(nm, [])
        if h in ("Eq", "HEq", "Ne") and len(args) >= 2:
            return (h, args[1])
        if h == "Iff" and len(args) >= 1:
            return (h, args[0])
        if h in ("LE.le", "LT.lt", "GE.ge", "GT.gt") and len(args) >= 3:
            return (h, args[2])
        return (h,)

    roots = theorem_roots(a)
    root_names = [a.names[r] for r in roots]

    # ---- 1. backward pools: candidates = theorems/ctors whose ch == h
    pool = Counter()
    for i in range(a.n):
        if a.kind[i] in ("theorem", "constructor"):
            h = ch.get(a.names[i])
            if h:
                pool[h] += 1
    goal_heads = Counter(ch.get(nm, "?") for nm in root_names)
    # pool size experienced by an average goal (weighted by goal frequency)
    sizes = []
    for h, cnt in goal_heads.items():
        sizes.extend([pool.get(h, 0)] * cnt)
    sizes = np.array(sizes)
    pools = {
        "n_goal_heads": len(goal_heads),
        "goal_weighted_pool": {
            "median": int(np.median(sizes)), "mean": round(float(sizes.mean()), 1),
            "p90": int(np.percentile(sizes, 90)), "max": int(sizes.max()),
        },
        "top_goal_heads": [
            {"head": h, "goals": c, "pool": pool.get(h, 0)}
            for h, c in goal_heads.most_common(20)],
    }

    # ---- 2. top-level move census
    move_kind = Counter()
    move_const = Counter()
    isthm_math = {a.names[i] for i in range(a.n)
                  if a.kind[i] == "theorem" and not a.cls[i]}
    for nm in root_names:
        v = vh.get(nm)
        if v is None:
            move_kind["NO_BODY"] += 1
        elif v in ("LET", "VAR", "MVAR", "SORT", "LIT", "LAM", "FORALL", "OTHER") \
                or v.startswith("PROJ:"):
            move_kind[v if not v.startswith("PROJ:") else "PROJ"] += 1
        else:
            move_const[v] += 1
            if v in isthm_math:
                move_kind["MATH_THEOREM"] += 1
            else:
                move_kind["OTHER_CONST"] += 1
    census = {
        "note": ("head of the FINISHED proof term after stripping lambdas - "
                 "the outer certificate constructor. Not necessarily the "
                 "author's first tactic, the discovery-time first decision, or "
                 "the best opening action for another valid proof."),
        "kinds": dict(move_kind),
        "top_move_constants": [
            {"name": n, "count": c} for n, c in move_const.most_common(25)],
    }

    # ---- 3. head-match rate for constant top moves
    match = tot = 0
    match_math = tot_math = 0
    for nm in root_names:
        v = vh.get(nm)
        if v is None or v not in ch:
            continue
        g = ch.get(nm)
        if g is None:
            continue
        tot += 1
        m = ch[v] == g
        match += m
        if v in isthm_math:
            tot_math += 1
            match_math += m
    headmatch = {
        "const_top_moves_checked": tot,
        "head_match_rate": round(match / tot, 4) if tot else None,
        "math_theorem_top_moves": tot_math,
        "head_match_rate_math": round(match_math / tot_math, 4) if tot_math else None,
    }

    # ---- 1b. refined pools: relational goals indexed by LHS head too
    rpool = Counter()
    for i in range(a.n):
        if a.kind[i] in ("theorem", "constructor"):
            k = refined_key(a.names[i])
            if k:
                rpool[k] += 1
    rsizes = []
    for nm in root_names:
        k = refined_key(nm)
        if k:
            rsizes.append(rpool.get(k, 0))
    rsizes = np.array(rsizes)
    pools["refined_goal_weighted_pool"] = {
        "median": int(np.median(rsizes)), "mean": round(float(rsizes.mean()), 1),
        "p90": int(np.percentile(rsizes, 90)), "max": int(rsizes.max()),
        "note": "Eq/Iff/order goals additionally keyed by LHS head",
    }

    # ---- 4. next-move prediction: frequency-ranked pool, recall@K
    log("next-move prediction eval...")
    cite = np.zeros(a.n, dtype=np.int64)          # direct citation prior
    for r in roots:
        cite[np.unique(a.v_indices[a.v_indptr[r]:a.v_indptr[r + 1]])] += 1
    by_head = defaultdict(list)
    by_ref = defaultdict(list)
    for i in range(a.n):
        if a.kind[i] in ("theorem", "constructor"):
            h = ch.get(a.names[i])
            if h:
                by_head[h].append(i)
            k = refined_key(a.names[i])
            if k:
                by_ref[k].append(i)
    for d in (by_head, by_ref):
        for h in d:
            ids = np.array(d[h])
            d[h] = ids[np.argsort(-cite[ids], kind="stable")]

    rng = np.random.default_rng(0)
    sample = rng.choice(len(roots), size=8000, replace=False)
    rec = {K: [0, 0] for K in KS}      # coarse pool: hits, total
    rrec = {K: [0, 0] for K in KS}     # refined pool
    for pos in sample:
        nm = root_names[pos]
        v = vh.get(nm)
        if v is None or v not in isthm_math:
            continue                   # eval where the top move is a math theorem
        vi = a.idx[v]
        for pools_d, key, acc in ((by_head, ch.get(nm), rec),
                                  (by_ref, refined_key(nm), rrec)):
            cands = pools_d.get(key)
            if cands is None:
                continue
            for K in KS:
                top = cands[:K + 1]
                top = top[top != roots[pos]][:K]   # leave-one-out
                acc[K][1] += 1
                if vi in top:
                    acc[K][0] += 1
    nextmove = {
        "eval_theorems": rec[KS[0]][1],
        "recall_at": {K: round(h / t, 4) if t else None
                      for K, (h, t) in rec.items()},
        "recall_at_refined": {K: round(h / t, 4) if t else None
                              for K, (h, t) in rrec.items()},
        "note": "candidates restricted to conclusion-head match (coarse) or "
                "head+LHS-head match (refined); ranked by global citation count",
    }

    out = {"pools": pools, "top_certificate_head_census": census,
           "head_match": headmatch, "certificate_head_prediction_baseline": nextmove}
    OUT.mkdir(exist_ok=True)
    (OUT / "mathlib_heads_analysis.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
