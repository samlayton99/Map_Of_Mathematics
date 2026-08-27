#!/usr/bin/env python3
"""Phase 4 certification, round 7 (seed 20260829; seeds 20260819-28 all
excluded as development data).

Registered before running:
  V6   round-6 certified system (anchor)
  V7   V6 + author-written priority: within a list, candidates whose short
       name the author actually wrote in the theorem's source FILE rank
       before candidates injected by compilation (level-3 behavioral
       provenance, ADR-0004: any future tactic's internals are also never
       typed by authors). File resolved via the environment's recorded
       module (exact); theorems without a resolvable file get no demotion
       (conservative). Sort key: (logic-only, NOT-written-in-file,
       in-statement-world, -depth).
Bars declared in advance: V7 top-1 >= 0.945 AND tactic-cause blames <= 8.

Context: four structural automation-detector formulations were falsified
(raw exposure, root-grain, registries, co-mention islands incl. weighted) —
the behavioral-provenance route is the surviving principled design.
"""
_ = """Phase 4 certification: pre-registered holdout evaluation of the exact
move substrate. RUN ONCE. (Judge's conditions, 2026-08-19.)

Development data: the seed-20260819 sample of 2,400 (never quoted as
validation again). Holdout: fresh disjoint 2,400 sample, seed 20260820,
drawn from the same population definition minus the development ids.

Pre-registered variants (fixed before results are seen):
  V4hist  historical formulation: hb set, kind==theorem proxy, single-use
          refs INLINED (4 rounds), rank (new-to-statement, depth)
  V4b     V4hist with the exact Prop check (field `pr`) replacing the proxy
  V5      substrate formulation: refs with load-bearing occurrence roles
          ({applied, let-value, explicit-arg, unresolved} > 0) and pr=true;
          single-use kept as an ATTRIBUTE (no inlining); rank (new, depth)
  V5z     V5 with zoom-expansion applied for display: single-use nodes
          auto-expanded to fixpoint (cycle-safe), labels retained

Metric names say what they measure: `top1_nonmachinery_proxy` is agreement
with an automated machinery-labeling proxy (name/namespace/P3-based), NOT
semantic precision. Reported per depth tercile, with single-use rates and
binder-fallback incidence.
"""
import json, os
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP4 = os.path.join(SCRATCH2, "mathlib_deps5.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
DEV_SEED = 20260819
HOLDOUT_SEED = 20260829
NSAMP = 2400
BATCH = 600
LOAD_ROLES = (0, 1, 2, 7)   # applied, let-value, explicit-arg, unresolved

TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.", "Batteries.Tactic.")
GEN_MARKS = (".match_", "._simp", "._proof_", "._unary", ".eq_def", ".brecOn",
             ".below", ".ibelow", ".ctorIdx", ".injEq", ".sizeOf_spec", "._eq_",
             ".noConfusion", "._aux", "._f", "._g", ".proof_")


def load():
    idx, names = {}, []
    deps_v, deps_t, kinds, classes, hbs, vo, pr, bf, gen = [], [], [], [], [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            deps_v.append(()); deps_t.append(()); kinds.append(""); classes.append(())
            hbs.append(()); vo.append(()); pr.append(False); bf.append(0); gen.append(False)
        return i
    with open(DUMP4) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]; classes[i] = tuple(r["c"])
            pr[i] = bool(r.get("pr", False)); gen[i] = bool(r.get("gen", False))
            bf[i] = int(r.get("bf", 0))
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
            hbs[i] = tuple(nid(d) for d in r.get("hb", ()))
            vo[i] = tuple(tuple(int(x) for x in row) for row in r.get("vo", ()))
    return idx, names, deps_v, deps_t, kinds, classes, hbs, vo, pr, bf, gen


def main():
    idx, names, deps_v, deps_t, kinds, classes, hbs, vo, pr, bf, gen = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    pr = np.array(pr)
    thm = np.array([k == "theorem" for k in kinds])
    has_class = np.array([len(c) > 0 for c in classes])
    print(f"kind==theorem: {int(thm.sum())}, pr==True: {int(pr.sum())}, "
          f"disagree: {int((thm != pr).sum())}", flush=True)
    print(f"rows with binder fallbacks: {int((np.array(bf) > 0).sum())}, "
          f"total fallback events: {int(np.array(bf).sum())}", flush=True)

    deps = [dv if dv else dt for dv, dt in zip(deps_v, deps_t)]
    indeg_v = np.zeros(n, dtype=np.int64)
    for i, ds in enumerate(deps_v):
        for d in set(ds):
            if d != i:
                indeg_v[d] += 1
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

    # measured concept universality over theorem statements (theta = 2%)
    CONCEPT_KINDS = ("def", "inductive", "opaque", "quot", "axiom")
    is_concept = np.array([k in CONCEPT_KINDS for k in kinds])
    cnt = np.zeros(n, dtype=np.int64)
    thm_ids = np.where(thm)[0]
    for i in thm_ids:
        for c in set(deps_t[i]):
            cnt[c] += 1
    univ = cnt / max(1, len(thm_ids))
    def bookkeeping(c):
        return not any(is_concept[k] and univ[k] < 0.02
                       for k in set(deps_t[c]) if k != c)

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

    # population and samples (dev excluded from holdout)
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    dev = set(np.random.default_rng(DEV_SEED).choice(pool, size=NSAMP, replace=False).tolist())
    p1 = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260820).choice(p1, size=NSAMP, replace=False).tolist())
    p2 = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260821).choice(p2, size=NSAMP, replace=False).tolist())
    p3 = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260822).choice(p3, size=NSAMP, replace=False).tolist())
    p4 = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260824).choice(p4, size=NSAMP, replace=False).tolist())
    p5 = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260825).choice(p5, size=NSAMP, replace=False).tolist())
    dev |= set(np.random.default_rng(20260826).choice(pool, size=1500, replace=False).tolist())
    dev |= set(np.random.default_rng(20260827).choice(pool, size=1500, replace=False).tolist())
    p6 = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260828).choice(p6, size=NSAMP, replace=False).tolist())
    pool2 = np.array([i for i in pool if i not in dev])
    roots = np.random.default_rng(HOLDOUT_SEED).choice(pool2, size=NSAMP, replace=False).tolist()
    print(f"holdout sample: {len(roots)} (disjoint from dev: "
          f"{len(set(roots) & dev) == 0})", flush=True)

    def loadbearing(r):
        """refs of r with any occurrence in LOAD_ROLES (from vo)."""
        out = set()
        for d, row in zip(deps_v[r], vo[r]):
            if d != r and any(row[k] > 0 for k in LOAD_ROLES):
                out.add(d)
        return out

    def inline4(cur, root):
        for _ in range(4):
            single = {c for c in cur if indeg_v[c] <= 1}
            if not single:
                break
            cur = (cur - single) | {d for c in single for d in hbs[c]
                                    if d != root and d not in single}
        return cur

    def expand_fix(cur, root):
        """zoom expansion to fixpoint with cycle detection; labels retained."""
        out = set(cur)
        frontier = {c for c in cur if indeg_v[c] <= 1}
        seen = set(frontier)
        for _ in range(64):
            new = set()
            for c in frontier:
                for d in loadbearing(c):
                    if d != root and d not in out and d not in seen:
                        new.add(d)
            if not new:
                break
            out |= {d for d in new if pr[d]}
            frontier = {d for d in new if indeg_v[d] <= 1}
            seen |= new
        return out

    def variant_cands(vname, r):
        claim = lambda c: pr[c] and kinds[c] not in ("constructor", "recursor")
        lb = {c for c in loadbearing(r) if claim(c)}
        if vname in ("V6", "V7"):
            return lb, {c for c in lb if indeg_v[c] <= 1}
        raise ValueError(vname)

    variants = ("V6", "V7")
    # statement cones for the union of candidates across variants
    cand = {v: {} for v in variants}
    need = {}
    for r in roots:
        u = set()
        for v in variants:
            cs, _ = variant_cands(v, r)
            cand[v][r] = cs
            u |= cs
        need[r] = u
    print("candidates built", flush=True)

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

    out = {"dev_seed": DEV_SEED, "holdout_seed": HOLDOUT_SEED,
           "note": "top1_nonmachinery_proxy = agreement with an automated "
                   "machinery-labeling proxy, NOT semantic precision",
           "kind_vs_pr_disagreements": int((thm != pr).sum()),
           "binder_fallback_rows": int((np.array(bf) > 0).sum())}
    strata_depth = [int(depth[r]) for r in roots
                    if len(set(deps_v[r]) - {r}) >= 3]
    sd = np.array(strata_depth)
    terc = np.quantile(sd, [1 / 3, 2 / 3])
    # forwarder attribution (V6): gen constant with exactly one substantive claim
    claimf = lambda c: pr[c] and kinds[c] not in ("constructor", "recursor")
    def loadbearing_g(c):
        return {d for d, row in zip(deps_v[c], vo[c])
                if d != c and any(row[k] > 0 for k in (0, 1, 2, 7))}
    attr_cache = {}
    def attribute(c, seen=None):
        if c in attr_cache:
            return attr_cache[c]
        if seen is None:
            seen = set()
        if not gen[c] or c in seen:
            return c
        seen.add(c)
        subst = [d for d in loadbearing_g(c) if claimf(d) and not bookkeeping(d)]
        res = attribute(subst[0], seen) if len(subst) == 1 else c
        attr_cache[c] = res
        return res
    tk = json.load(open(SCRATCH2 + "/r7_tokens.json"))
    file_tokens = {fp: set(t) for fp, t in tk["file_tokens"].items()}
    thm_file = tk["thm_file"]
    def written_in_file(r, c):
        fp = thm_file.get(names[r])
        if fp is None:
            return True   # unknown source: no demotion (conservative)
        return names[c].split(".")[-1] in file_tokens[fp]
    live_top1 = {v: {} for v in variants}
    for vname in variants:
        fcr, cause, defn, single_top1 = [], {}, 0, 0
        for r in roots:
            if len(set(deps_v[r]) - {r}) < 3:
                continue
            cs = cand[vname][r]
            nf = newflag[r]
            if vname == "V7":
                key = lambda c: (bookkeeping(c), not written_in_file(r, c),
                                 not nf.get(c, True), -int(depth[c]))
            else:
                key = lambda c: (bookkeeping(c), not nf.get(c, True), -int(depth[c]))
            cs = {attribute(c) for c in cs}
            if cs and all(bookkeeping(c) for c in cs):
                cs = set()   # holds-by-definition/logic verdict
            ranked = sorted(cs, key=key)
            if True:
                claim = lambda c: pr[c] and kinds[c] not in ("constructor", "recursor")
                opened = set()
                for _ in range(8):
                    if not ranked or indeg_v[ranked[0]] > 1 or ranked[0] in opened:
                        break
                    top = ranked[0]
                    opened.add(top)
                    inner = {c for c in loadbearing(top) if claim(c) and c != r}
                    ranked = sorted((set(ranked) - {top}) | inner, key=key)
            if not ranked:
                defn += 1
                fcr.append(0)
                continue
            cats = {c: category(c, names[r]) for c in ranked}
            fc = next((k + 1 for k, c in enumerate(ranked) if cats[c] == "content"), 99)
            fcr.append(fc)
            live_top1[vname][r] = (fc == 1)
            c1 = cats[ranked[0]]
            if c1 != "content":
                cause[c1] = cause.get(c1, 0) + 1
            if indeg_v[ranked[0]] <= 1:
                single_top1 += 1
        a = np.array(fcr)
        live = a[a > 0]
        e = {"definitional_verdicts": int((a == 0).sum()),
             "top1_nonmachinery_proxy": round(float((live == 1).mean()), 4),
             "top2_nonmachinery_proxy": round(float((live <= 2).mean()), 4),
             "no_content": round(float((live == 99).mean()), 4),
             "top1_cause_when_machinery": cause,
             "top1_single_use_rate": round(single_top1 / max(1, len(live)), 4)}
        for lab, lo, hi in (("shallow", -1, terc[0]), ("mid", terc[0], terc[1]),
                            ("deep", terc[1], 1e9)):
            m = (sd > lo) & (sd <= hi) & (a > 0)
            e[f"top1_{lab}"] = round(float((a[m] == 1).mean()), 4)
        out[vname] = e
        print(vname, "=", json.dumps(e), flush=True)

    both = set(live_top1["V6"]) & set(live_top1["V7"])
    out["matched_denominator"] = {
        "n_both_live": len(both),
        "V6_top1_matched": round(float(np.mean([live_top1["V6"][r] for r in both])), 4),
        "V7_top1_matched": round(float(np.mean([live_top1["V7"][r] for r in both])), 4)}
    print("matched_denominator =", json.dumps(out["matched_denominator"]))
    with open(os.path.join(DATA, "phase4_holdout7_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
