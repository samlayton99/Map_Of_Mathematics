#!/usr/bin/env python
"""Oracle-support experiment: task files with exact reference-proof support.

Support definitions (per handoff):
  D_all(T)      constants occurring directly in the proof body, with
                target-attached auxiliaries (T.*, generated match/proof/simp
                helpers of T) INLINED into their own dependencies and never
                exposed as heads
  D_semantic(T) the theorem/axiom/def members of D_all excluding machinery-
                classified constants
  B(T)          base vocabulary: the statement's dependency closure (the
                problem gives it) - reported, not restricted
  D_new(T)      D_semantic minus B(T)

Same-module members of D_all are CERTIFIED PRIOR (the reference proof
compiled at its source location), so they are legal support even under the
conservative regime; the per-task forbid list excludes them explicitly.

Regimes written (same 80 theorems as the prover ladder):
  S1  bw/rw = D_all support           (the wiring oracle)
  S2  bw/rw = D_semantic support      (math tools only)
  S3  S1 + 128 accessible distractors (retrieval-noise robustness)

Run: ~/venv/general_ml/bin/python support_tasks.py
Writes bigdata/support_tasks_{S1,S2,S3}.json + support_stats.json
"""
import json
import sys
import time
from collections import Counter

import numpy as np

from atlas import load_dump, theorem_roots, BIG
from accessibility import Accessibility
from heads_util import load_heads
import rolodex as R


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def is_target_aux(name, target):
    if name.startswith(target + "."):
        return True
    if name.startswith("_private.") and ("." + target.split(".")[-1] + ".") in name:
        return True
    return False


def expand_support(a, t, target_name):
    """Direct proof-body constants with target-attached auxiliaries inlined
    (transitively).  Returns a set of node ids, target excluded."""
    out = set()
    stack = list(a.v_indices[a.v_indptr[t]:a.v_indptr[t + 1]])
    seen = set(stack)
    while stack:
        c = int(stack.pop())
        nm = a.names[c]
        if c == t:
            continue
        if is_target_aux(nm, target_name):
            for d in a.v_indices[a.v_indptr[c]:a.v_indptr[c + 1]]:
                if int(d) not in seen:
                    seen.add(int(d))
                    stack.append(int(d))
        else:
            out.add(c)
    return out


def main():
    log("loading atlas, accessibility, heads...")
    a = load_dump()
    acc = Accessibility(a)
    ch, ca, _ = load_heads()
    rng = np.random.default_rng(1)

    base = json.load(open(BIG / "prover_tasks80.json"))["tasks"]
    meta = {m["n"]: m for m in json.loads((BIG / "prover_tasks_meta.json").read_text())}
    names80 = [t["n"] for t in base]
    old = {t["n"]: t for t in base}

    def kindof(c):
        k = a.kind[c]
        if a.cls[c]:
            return "machinery:" + a.cls[c][0]
        return k

    is_eqiff = lambda c: ch.get(a.names[c]) in ("Eq", "Iff")

    stats_rows = []
    s1, s2, s3 = [], [], []
    for nm in names80:
        t = a.idx[nm]
        d_all = expand_support(a, t, nm)
        d_sem = {c for c in d_all
                 if a.kind[c] in ("theorem", "axiom", "def") and not a.cls[c]}
        stmt_cone = a.cone_from(a.type_deps(t))
        d_new = d_sem - stmt_cone
        cats = Counter(kindof(c) for c in d_all)
        stats_rows.append({
            "n": nm, "d_all": len(d_all), "d_semantic": len(d_sem),
            "d_new": len(d_new), "stmt_cone": len(stmt_cone),
            "categories": dict(cats),
            "same_module_support": int(sum(
                1 for c in d_all if acc.mod_of[c] == acc.mod_of[t])),
        })

        # forbid: own-module minus statement cone minus certified support
        own = acc.mod_of[t]
        own_members = np.where(acc.mod_of == own)[0]
        forbid = [a.names[int(c)] for c in own_members
                  if int(c) not in stmt_cone and int(c) not in d_all
                  and int(c) != t]

        def mk(support, extra_bw=()):
            sup = sorted(support, key=lambda c: -a.depth[c])
            bw = [a.names[c] for c in sup] + list(extra_bw)
            rw = [a.names[c] for c in sup if is_eqiff(c)]
            return {"n": nm, "bw": bw, "rw": rw, "fb": forbid}

        s1.append(mk(d_all))
        s2.append(mk(d_sem))
        # S3: S1 + 128 accessible distractors from the old toolkit
        distract = [x for x in old[nm]["bw"]
                    if a.idx.get(x) not in d_all][:128]
        s3.append(mk(d_all, extra_bw=distract))

    for tag, ts in (("S1", s1), ("S2", s2), ("S3", s3)):
        (BIG / f"support_tasks_{tag}.json").write_text(json.dumps({"tasks": ts}))

    d_all_sizes = [r["d_all"] for r in stats_rows]
    d_sem_sizes = [r["d_semantic"] for r in stats_rows]
    d_new_sizes = [r["d_new"] for r in stats_rows]
    summary = {
        "n_tasks": len(stats_rows),
        "d_all": {"median": float(np.median(d_all_sizes)),
                  "mean": round(float(np.mean(d_all_sizes)), 1),
                  "p90": float(np.percentile(d_all_sizes, 90))},
        "d_semantic": {"median": float(np.median(d_sem_sizes)),
                       "mean": round(float(np.mean(d_sem_sizes)), 1)},
        "d_new": {"median": float(np.median(d_new_sizes)),
                  "mean": round(float(np.mean(d_new_sizes)), 1)},
        "rows": stats_rows,
    }
    (BIG / "support_stats.json").write_text(json.dumps(summary, indent=1))
    log(f"S1/S2/S3 written; |D_all| median {np.median(d_all_sizes):.0f} "
        f"mean {np.mean(d_all_sizes):.1f}, |D_semantic| median "
        f"{np.median(d_sem_sizes):.0f}, |D_new| median {np.median(d_new_sizes):.0f}")


if __name__ == "__main__":
    main()
