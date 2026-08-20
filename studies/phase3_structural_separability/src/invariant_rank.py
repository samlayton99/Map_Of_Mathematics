#!/usr/bin/env python3
"""Test kernel-invariant ranking rules on the forensics sample.

Rules under test (all expressible in the kernel calculus: type vs value,
Prop vs Type, and the reference graph — no names, no metadata):
  R1 moves-must-be-Props: rank only Prop-valued references (kind=theorem
     proxy here; final form checks `type : Prop` directly).
  R2 inline-single-use: a reference cited by exactly one constant in the
     whole library is private workings, not shared knowledge — replace it
     by its own references, recursively.
  R3 (measured only, not applied): statement-exposure. A concept's
     exposure = how many constants mention it in their TYPE. Machinery
     lemmas (tactic certificates) have statements built from unexposed
     vocabulary; mathematical lemmas from exposed vocabulary.

Variants evaluated on the same 2400-root sample as forensics.py:
  V1 baseline: all refs, (new, depth)          [= forensics new_depth]
  V2 R1: Prop refs only, (new, depth)
  V3 R1+R2: Prop refs after single-use inlining, (new, depth)
Diagnosis categories (name-based) are used ONLY to score the result.
"""
import json, os
import numpy as np

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/db11af5d-4211-45ea-97b3-8e87cef8aeb6/scratchpad"
DUMP = os.path.join(SCRATCH, "mathlib_deps.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
SEED = 20260819
NSAMP = 2400
BATCH = 600

TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.", "Batteries.Tactic.")
GEN_MARKS = (".match_", "._simp", "._proof_", "._unary", ".eq_def", ".brecOn",
             ".below", ".ibelow", ".ctorIdx", ".injEq", ".sizeOf_spec", "._eq_",
             ".noConfusion", "._aux", "._f", "._g", ".proof_")


def load():
    idx, names, deps_v, deps_t, kinds, classes = {}, [], [], [], [], []
    def nid(n):
        i = idx.get(n)
        if i is None:
            i = len(names); idx[n] = i; names.append(n)
            deps_v.append(()); deps_t.append(()); kinds.append(""); classes.append(())
        return i
    with open(DUMP) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]; classes[i] = tuple(r["c"])
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
    return idx, names, deps_v, deps_t, kinds, classes


def main():
    idx, names, deps_v, deps_t, kinds, classes = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    deps = [dv if dv else dt for dv, dt in zip(deps_v, deps_t)]
    indeg_v = np.zeros(n, dtype=np.int64)     # distinct users via value refs
    for i, ds in enumerate(deps_v):
        for d in set(ds):
            if d != i:
                indeg_v[d] += 1
    t_indeg = np.zeros(n, dtype=np.int64)     # distinct mentions in TYPES
    for i, ds in enumerate(deps_t):
        for d in set(ds):
            if d != i:
                t_indeg[d] += 1
    # topo + depth
    indeg = np.zeros(n, dtype=np.int32)
    users = [[] for _ in range(n)]
    clean = []
    for i, ds in enumerate(deps):
        ds2 = tuple(d for d in set(ds) if d != i)
        clean.append(ds2)
        indeg[i] = len(ds2)
        for d in ds2:
            users[d].append(i)
    deps = clean
    from collections import deque
    q = deque(np.where(indeg == 0)[0].tolist())
    order = []
    while q:
        i = q.popleft(); order.append(i)
        for u in users[i]:
            indeg[u] -= 1
            if indeg[u] == 0:
                q.append(u)
    depth = np.zeros(n, dtype=np.int32)
    for i in order:
        if deps[i]:
            depth[i] = 1 + max(depth[d] for d in deps[i])
    cyc = set(range(n)) - set(order)
    for _ in range(3):
        for i in cyc:
            ds = [depth[d] for d in deps[i] if d not in cyc]
            if ds:
                depth[i] = 1 + max(ds)
    del users
    print("depth done", flush=True)

    has_class = np.array([len(c) > 0 for c in classes])
    thm = np.array([k == "theorem" for k in kinds])

    def category(c, root_name):
        nm = names[c]
        if nm.startswith("_private."):
            base = root_name.split(".")[-1]
            return "self-helper" if ("." + base + "." in nm or nm.endswith(base)) else "generated"
        if nm.startswith(root_name + "."):
            return "self-helper"
        if any(m in nm for m in GEN_MARKS):
            base = root_name.split(".")[-1]
            return "self-helper" if base in nm else "generated"
        if nm.startswith(TACTIC_NS):
            return "tactic"
        cl = classes[c]
        if "typeclass-instance" in cl:
            return "instance"
        if any(x in cl for x in ("eq-machinery", "logic-core", "structure-projection",
                                 "coercion", "recursor")):
            return "glue"
        if any(x in cl for x in ("generated", "internal-detail")):
            return "generated"
        if kinds[c] in ("theorem", "def", "opaque"):
            return "content"
        return "other"

    rng = np.random.default_rng(SEED)
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    roots = rng.choice(pool, size=NSAMP, replace=False).tolist()

    # ---- candidate sets, with single-use inlining (R2) ----
    def expand(root):
        """Direct refs; single-use refs replaced by their own refs, ≤4 rounds."""
        cur = set(d for d in deps_v[root] if d != root)
        for _ in range(4):
            single = {c for c in cur if indeg_v[c] <= 1}
            if not single:
                break
            cur = (cur - single) | {d for c in single
                                    for d in (deps_v[c] if deps_v[c] else deps_t[c])
                                    if d != root and d not in single}
        return cur

    cand_v1 = {r: set(d for d in deps_v[r] if d != r) for r in roots}
    cand_v3 = {r: expand(r) for r in roots}
    need = {r: cand_v1[r] | cand_v3[r] for r in roots}

    # ---- statement-cone membership for all needed pairs ----
    dep_arrays = [np.array(ds, dtype=np.int64) if ds else None for ds in deps]
    rev = list(reversed(order))
    newflag = {}
    for b0 in range(0, len(roots), BATCH):
        batch = roots[b0:b0 + BATCH]
        pos = {r: j for j, r in enumerate(batch)}
        nwords = (len(batch) + 63) // 64
        reach = np.zeros((n, nwords), dtype=np.uint64)
        seeds = {r: np.array(sorted(set(deps_t[r]) - {r}), dtype=np.int64) for r in batch}
        for i in rev:
            row = reach[i]
            if row.any():
                ds = dep_arrays[i]
                if ds is not None:
                    reach[ds] |= row
            j = pos.get(i)
            if j is not None and len(seeds[i]):
                rr = np.zeros(nwords, dtype=np.uint64)
                rr[j >> 6] = np.uint64(1) << np.uint64(j & 63)
                reach[seeds[i]] |= rr
        for i in list(cyc) * 2:
            row = reach[i]
            if row.any() and dep_arrays[i] is not None:
                reach[dep_arrays[i]] |= row
        for r in batch:
            j = pos[r]
            w, bit = j >> 6, np.uint64(1) << np.uint64(j & 63)
            newflag[r] = {c: not bool(reach[c, w] & bit) for c in need[r]}
        del reach
        print(f"batch {b0 // BATCH + 1}/{(len(roots) + BATCH - 1) // BATCH}", flush=True)

    # ---- evaluate variants ----
    variants = {
        "V1_all_refs": lambda r: cand_v1[r],
        "V2_prop_only": lambda r: {c for c in cand_v1[r] if kinds[c] == "theorem"},
        "V3_prop_inlined": lambda r: {c for c in cand_v3[r] if kinds[c] == "theorem"},
    }
    res = {v: {"fcr": [], "top1cause": {}, "definitional": 0, "rows": []}
           for v in variants}
    strata_depth = []
    for r in roots:
        if len(cand_v1[r]) < 3:
            continue
        strata_depth.append(int(depth[r]))
        for vname, f in variants.items():
            cands = f(r)
            nf = newflag[r]
            ranked = sorted(cands, key=lambda c: (not nf[c], -int(depth[c])))
            cats = {c: category(c, names[r]) for c in ranked}
            if not ranked:
                res[vname]["definitional"] += 1
                res[vname]["fcr"].append(0)   # 0 = judged definitional
                continue
            fc = next((k + 1 for k, c in enumerate(ranked) if cats[c] == "content"), 99)
            res[vname]["fcr"].append(fc)
            c1 = cats[ranked[0]]
            if c1 != "content":
                res[vname]["top1cause"][c1] = res[vname]["top1cause"].get(c1, 0) + 1
            if vname == "V3_prop_inlined":
                res[vname]["rows"].append(
                    {"decl": names[r], "depth": int(depth[r]), "fcr": fc,
                     "top3": [{"name": names[c], "cat": cats[c], "d": int(depth[c])}
                              for c in ranked[:3]]})

    out = {"n_analyzed": len(strata_depth), "seed": SEED}
    sd = np.array(strata_depth)
    terc = np.quantile(sd, [1 / 3, 2 / 3])
    for vname in variants:
        a = np.array(res[vname]["fcr"])
        live = a[a > 0]
        e = {"definitional_verdicts": int((a == 0).sum()),
             "top1_content": round(float((live == 1).mean()), 4),
             "top2_content": round(float((live <= 2).mean()), 4),
             "no_content": round(float((live == 99).mean()), 4),
             "top1_cause_when_noncontent": res[vname]["top1cause"]}
        for lab, lo, hi in (("shallow", -1, terc[0]), ("mid", terc[0], terc[1]),
                            ("deep", terc[1], 1e9)):
            m = (sd > lo) & (sd <= hi) & (a > 0)
            e[f"top1_content_{lab}"] = round(float((a[m] == 1).mean()), 4)
        out[vname] = e

    # ---- R3 measurement: statement-exposure of candidate subject matter ----
    # subject exposure of lemma c = log10(1 + max t_indeg over defs in c's type)
    def subj_expo(c):
        ds = [d for d in set(deps_t[c]) if kinds[d] in ("def", "inductive", "opaque")]
        return float(np.log10(1 + max((t_indeg[d] for d in ds), default=0)))
    from collections import defaultdict
    expo = defaultdict(list)
    rng2 = np.random.default_rng(SEED + 2)
    sub = rng2.choice(roots, size=400, replace=False)
    for r in sub:
        for c in cand_v1[r]:
            if kinds[c] != "theorem":
                continue
            cat = category(c, names[r])
            if cat in ("content", "tactic", "generated"):
                expo[cat].append(subj_expo(c))
    out["R3_subject_exposure"] = {
        k: {"n": len(v), "median": round(float(np.median(v)), 2),
            "p25": round(float(np.percentile(v, 25)), 2)}
        for k, v in expo.items()}
    from sklearn.metrics import roc_auc_score
    if expo["content"] and expo["tactic"]:
        y = [1] * len(expo["content"]) + [0] * len(expo["tactic"])
        x = expo["content"] + expo["tactic"]
        out["R3_auc_content_vs_tactic"] = round(float(roc_auc_score(y, x)), 3)
    out["R3_anchor_t_indeg"] = {names[idx[a]]: int(t_indeg[idx[a]])
                                for a in ("Real.log", "Real.exp", "Nat.gcd",
                                          "Lean.Omega.LinearCombo",
                                          "Lean.Omega.Constraint",
                                          "Lean.Grind.CommRing.Expr") if a in idx}
    # keep a few V3 broken rows for reading
    bad = [r for r in res["V3_prop_inlined"]["rows"] if r["fcr"] > 2][:40]
    out["V3_broken_examples"] = bad

    with open(os.path.join(DATA, "invariant_rank_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for v in list(variants) + ["R3_subject_exposure", "R3_auc_content_vs_tactic",
                               "R3_anchor_t_indeg"]:
        if v in out:
            print(v, "=", json.dumps({k: x for k, x in out[v].items()}
                                     if isinstance(out[v], dict) else out[v]))


if __name__ == "__main__":
    main()
