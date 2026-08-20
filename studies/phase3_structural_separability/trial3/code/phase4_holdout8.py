#!/usr/bin/env python3
"""Phase 4 certification, round 8 (seed 20260830; seeds 20260819-29 all
excluded as development data).

REGISTERED BEFORE RUNNING.

  V6  round-6/7 certified system (anchor; 9th replication)
  V8  V6 + the apparatus measure:

      ps        kernel sort fact (dump v6): the constant's type telescopes
                to `Prop` -- it IS a proposition or predicate, as opposed to
                DATA (`Nat`, `Finset`, `Lean.Omega.Constraint`).
      bare      a Prop-sorted concept with no ingredients of its own
                (`True`, `False`) -- predicates always mention their data.
      bookkeeping'(c)  every non-universal ingredient of c is bare
                (extends the certified bookkeeping rule from "none" to
                "none that are about anything but bare propositions")
      stated(k)  number of human-written theorem STATEMENTS mentioning k,
                inherited down the concept graph (a statement about Ring
                states AddCommMagma, because Ring contains it)
      used(k)    number of proofs citing, load-bearing, a claim whose
                non-universal ingredients include k
      APPARATUS(k) := NOT a bare proposition AND non-universal
                AND used(k) > 200 AND used(k) > 20 * (stated(k) + 1)
                -- a vocabulary that exists to be COMPUTED WITH inside
                proofs rather than TALKED ABOUT in theorems. Bare
                propositions are excluded because they are already
                bookkeeping; every other concept with this profile is some
                procedure's private vocabulary (data OR predicate: omega's
                Constraint, NormNum's IsNat).
      machinery(T, c) := some ingredient of c is APPARATUS
                AND no ingredient of c appears in T's own statement
                (goal-relevant apparatus is spared: a theorem about
                Constraint keeps its constraint lemmas)
      demote tier      := bookkeeping'(c) OR machinery(T, c)
      verdict          := whole list demoted -> "holds by definition"
                (all bookkeeping') or "discharged by automation"
      NO capsule rule: dev profiling (profile7/8) falsified two variants
                (close-if-any-inner-machinery, close-if-top-inner-machinery);
                both hide real moves. Zoom is unchanged from V6.

Bars declared in advance (all must pass). Dev reference (seed 20260819,
never quoted as validation): V6 ext 0.9312 / V8 ext 0.9344, tactic-cause
blames 27 -> 20, real content demotions 0, junk fixes 6.
  1. V8 top-1 (extended grader) >= V6 top-1 (extended grader)
  2. V8 tactic-cause rank-1 blames <= 0.8 * V6 tactic-cause rank-1 blames
  3. real content demotions (a content rank-1 under V6 replaced by a
     non-content rank-1 under V8) <= 5 per 2400 sampled

Metric names: `top1_nonmachinery_proxy` = agreement with an automated
labeling proxy, NOT semantic precision (ADR-0004). The extended grader adds
two measured blind spots (core-internal arithmetic namespaces, True-twin
normalization family) for EVALUATION ONLY -- no name is used anywhere in the
system itself.
"""
import json, os
import numpy as np
from collections import Counter

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP = os.path.join(SCRATCH2, "mathlib_deps6.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
DEV_SEED = 20260819
HOLDOUT_SEED = 20260830
NSAMP = 2400
BATCH = 600
LOAD_ROLES = (0, 1, 2, 7)
LAMBDA = 20
NPROOF_FLOOR = 200

TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.", "Batteries.Tactic.")
GEN_MARKS = (".match_", "._simp", "._proof_", "._unary", ".eq_def", ".brecOn",
             ".below", ".ibelow", ".ctorIdx", ".injEq", ".sizeOf_spec", "._eq_",
             ".noConfusion", "._aux", "._f", "._g", ".proof_")
EXTRA_TACTIC_NS = ("Int.Internal.", "Nat.Internal.")
TRUE_TWINS = {"of_eq_true", "eq_true", "eq_self", "eq_self_iff_true",
              "iff_self", "iff_self_iff", "ite_cond_eq_true", "ite_cond_eq_false",
              "forall_true_left", "forall_const", "not_true_eq_false",
              "implies_true", "and_true", "true_and", "and_self", "eq_true_eq_id"}


def load():
    idx, names = {}, []
    deps_v, deps_t, kinds, classes, vo, pr, gen, ps = [], [], [], [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            deps_v.append(()); deps_t.append(()); kinds.append(""); classes.append(())
            vo.append(()); pr.append(False); gen.append(False); ps.append(False)
        return i
    with open(DUMP) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]; classes[i] = tuple(r["c"])
            pr[i] = bool(r.get("pr", False)); gen[i] = bool(r.get("gen", False))
            ps[i] = bool(r.get("ps", False))
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
            vo[i] = tuple(tuple(int(x) for x in row) for row in r.get("vo", ()))
    return idx, names, deps_v, deps_t, kinds, classes, vo, pr, gen, ps


def main():
    idx, names, deps_v, deps_t, kinds, classes, vo, pr, gen, ps = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    pr = np.array(pr); gen = np.array(gen); ps = np.array(ps)
    thm = np.array([k == "theorem" for k in kinds])
    has_class = np.array([len(c) > 0 for c in classes])

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

    CONCEPT_KINDS = ("def", "inductive", "opaque", "quot", "axiom")
    is_concept = np.array([k in CONCEPT_KINDS for k in kinds])
    human_thm = thm & ~gen
    nstmt = np.zeros(n, dtype=np.int64)
    ht_ids = np.where(human_thm)[0]
    for i in ht_ids:
        for c in set(deps_t[i]):
            nstmt[c] += 1
    univ = nstmt / max(1, len(ht_ids))

    inherited = nstmt.astype(np.float64).copy()
    rev = list(reversed(order))
    for p in rev:
        if not is_concept[p]:
            continue
        v = inherited[p]
        if v <= 0:
            continue
        for k in deps[p]:
            if is_concept[k] and inherited[k] < v:
                inherited[k] = v
    for _ in range(3):
        for p in cyc:
            if not is_concept[p]:
                continue
            v = inherited[p]
            for k in deps[p]:
                if is_concept[k] and inherited[k] < v:
                    inherited[k] = v
    print("inherited done", flush=True)

    n_tdeps = np.array([len(set(t)) for t in deps_t])
    bare_prop = is_concept & ps & (n_tdeps == 0)

    ing_cache = {}
    def nonuniv_ingredients(c):
        r = ing_cache.get(c)
        if r is None:
            r = frozenset(k for k in set(deps_t[c])
                          if k != c and is_concept[k] and univ[k] < 0.02)
            ing_cache[c] = r
        return r
    def bookkeeping6(c):
        return not nonuniv_ingredients(c)
    def bookkeeping8(c):
        return all(bare_prop[k] for k in nonuniv_ingredients(c))
    claimf = lambda c: pr[c] and kinds[c] not in ("constructor", "recursor")

    nproof = np.zeros(n, dtype=np.int64)
    for i in range(n):
        if not deps_v[i]:
            continue
        ks = set()
        for d, row in zip(deps_v[i], vo[i]):
            if d != i and any(row[r0] > 0 for r0 in LOAD_ROLES) and claimf(d):
                ks |= nonuniv_ingredients(d)
        for k in ks:
            nproof[k] += 1
    apparatus = (is_concept & ~bare_prop & (univ < 0.02) & (nproof > NPROOF_FLOOR)
                 & (nproof > LAMBDA * (inherited + 1)))
    print(f"apparatus concepts: {int(apparatus.sum())}", flush=True)

    taint_cache = {}
    def tainted(c):
        r = taint_cache.get(c)
        if r is None:
            r = any(apparatus[k] for k in nonuniv_ingredients(c))
            taint_cache[c] = r
        return r

    def loadbearing(r):
        outp = set()
        for d, row in zip(deps_v[r], vo[r]):
            if d != r and any(row[k] > 0 for k in LOAD_ROLES):
                outp.add(d)
        return outp
    def loadbearing_g(c):
        return {d for d, row in zip(deps_v[c], vo[c])
                if d != c and any(row[k] > 0 for k in (0, 1, 2, 7))}

    def make_attr(v8):
        cache = {}
        bk = bookkeeping8 if v8 else bookkeeping6
        def attribute(c, seen=None):
            if c in cache:
                return cache[c]
            if seen is None:
                seen = set()
            if not gen[c] or c in seen:
                return c
            seen.add(c)
            subst = [d for d in loadbearing_g(c) if claimf(d) and not bk(d)
                     and not (v8 and tainted(d))]
            res = attribute(subst[0], seen) if len(subst) == 1 else c
            cache[c] = res
            return res
        return attribute
    attr6 = make_attr(False)
    attr8 = make_attr(True)

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
    def category2(c, root_name):
        nm = names[c]
        if nm.startswith(EXTRA_TACTIC_NS):
            return "tactic"
        if nm.split(".")[-1] in TRUE_TWINS or nm in TRUE_TWINS:
            return "glue"
        return category(c, root_name)

    # population and samples (all prior seeds excluded)
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    dev = set(np.random.default_rng(DEV_SEED).choice(pool, size=NSAMP, replace=False).tolist())
    for sd in (20260820, 20260821, 20260822, 20260824, 20260825):
        p = np.array([i for i in pool if i not in dev])
        dev |= set(np.random.default_rng(sd).choice(p, size=NSAMP, replace=False).tolist())
    dev |= set(np.random.default_rng(20260826).choice(pool, size=1500, replace=False).tolist())
    dev |= set(np.random.default_rng(20260827).choice(pool, size=1500, replace=False).tolist())
    for sd in (20260828, 20260829):
        p = np.array([i for i in pool if i not in dev])
        dev |= set(np.random.default_rng(sd).choice(p, size=NSAMP, replace=False).tolist())
    pool2 = np.array([i for i in pool if i not in dev])
    roots = np.random.default_rng(HOLDOUT_SEED).choice(pool2, size=NSAMP, replace=False).tolist()
    print(f"holdout sample: {len(roots)} (disjoint: {len(set(roots) & dev) == 0})", flush=True)

    cand6, cand8, need = {}, {}, {}
    for r in roots:
        lb = {c for c in loadbearing(r) if claimf(c)}
        c6 = {attr6(c) for c in lb}
        c8 = {attr8(c) for c in lb}
        cand6[r] = c6; cand8[r] = c8
        u = c6 | c8
        for c in list(u):
            if indeg_v[c] <= 1 or gen[c]:
                u = u | {d for d in loadbearing_g(c) if claimf(d)}
        need[r] = u
    print("candidates built", flush=True)

    dep_arrays = [np.array(ds, dtype=np.int64) if ds else None for ds in deps]
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

    def stmt_concepts(r):
        return frozenset(k for k in set(deps_t[r]) if is_concept[k] and univ[k] < 0.02)
    def machinery(rs, c):
        return tainted(c) and not (nonuniv_ingredients(c) & rs)

    def score(vname, r):
        rn = names[r]
        rs = stmt_concepts(r)
        if vname == "V6":
            cs = set(cand6[r]); dem = bookkeeping6; bk = bookkeeping6
        else:
            cs = set(cand8[r])
            bk = bookkeeping8
            dem = lambda c: bookkeeping8(c) or machinery(rs, c)
        nf = newflag[r]
        key = lambda c: (dem(c), not nf.get(c, True), -int(depth[c]))
        if cs and all(dem(c) for c in cs):
            kind = "definitional" if all(bk(c) for c in cs) else "automation"
            return kind, [], {}, False
        ranked = sorted(cs, key=key)
        opened = set()
        for _ in range(8):
            if not ranked or indeg_v[ranked[0]] > 1 or ranked[0] in opened:
                break
            top = ranked[0]
            inner = {c for c in loadbearing_g(top) if claimf(c) and c != r}
            opened.add(top)
            ranked = sorted((set(ranked) - {top}) | inner, key=key)
        cats = {c: category(c, rn) for c in ranked}
        return None, ranked, cats, False

    out = {"holdout_seed": HOLDOUT_SEED, "apparatus_concepts": int(apparatus.sum()),
           "note": "top1_nonmachinery_proxy = agreement with an automated "
                   "machinery-labeling proxy, NOT semantic precision"}
    live_top1 = {}
    for vname in ("V6", "V8"):
        fcr, fcr2, cause, cause2, verd = [], [], Counter(), Counter(), Counter()
        atomic_top1 = 0
        lt = {}
        for r in roots:
            if len(set(deps_v[r]) - {r}) < 3:
                continue
            kind, ranked, cats, atomic = score(vname, r)
            if kind:
                verd[kind] += 1; fcr.append(0); fcr2.append(0); continue
            if not ranked:
                verd["empty"] += 1; fcr.append(0); fcr2.append(0); continue
            rn = names[r]
            cats2 = {c: category2(c, rn) for c in ranked}
            fc = next((k + 1 for k, c in enumerate(ranked) if cats[c] == "content"), 99)
            fc2 = next((k + 1 for k, c in enumerate(ranked) if cats2[c] == "content"), 99)
            fcr.append(fc); fcr2.append(fc2)
            lt[r] = (fc2 == 1)
            if atomic:
                atomic_top1 += 1
            if cats[ranked[0]] != "content":
                cause[cats[ranked[0]]] += 1
            if cats2[ranked[0]] != "content":
                cause2[cats2[ranked[0]]] += 1
        live_top1[vname] = lt
        a = np.array(fcr); a2 = np.array(fcr2)
        live = a[a > 0]; live2 = a2[a2 > 0]
        e = {"verdicts": dict(verd),
             "top1_nonmachinery_proxy": round(float((live == 1).mean()), 4),
             "top1_extended_grader": round(float((live2 == 1).mean()), 4),
             "no_content": round(float((live == 99).mean()), 4),
             "top1_cause_when_machinery": dict(cause),
             "top1_cause_extended": dict(cause2),
             "n_live": int((a > 0).sum())}
        out[vname] = e
        print(vname, "=", json.dumps(e), flush=True)

    # content-move demotions: V6 rank-1 was content (extended grader) and V8
    # moved it off rank 1 for a non-content item
    dem_cases = []
    for r in roots:
        if len(set(deps_v[r]) - {r}) < 3:
            continue
        k6, r6, _, _ = score("V6", r)
        k8, r8, _, a8 = score("V8", r)
        rn = names[r]
        if k6 or not r6:
            continue
        if category2(r6[0], rn) != "content":
            continue
        if k8:
            dem_cases.append({"thm": rn, "was": names[r6[0]], "now": "VERDICT:" + k8})
        elif not r8:
            dem_cases.append({"thm": rn, "was": names[r6[0]], "now": "empty"})
        elif r8[0] != r6[0] and category2(r8[0], rn) != "content":
            dem_cases.append({"thm": rn, "was": names[r6[0]], "now": names[r8[0]],
                              "atomic": bool(a8)})
    out["content_demotions"] = dem_cases
    print(f"content-move demotions: {len(dem_cases)}", flush=True)
    for d in dem_cases[:30]:
        print("   ", d, flush=True)

    both = set(live_top1["V6"]) & set(live_top1["V8"])
    out["matched_denominator"] = {
        "n_both_live": len(both),
        "V6_top1_ext_matched": round(float(np.mean([live_top1["V6"][r] for r in both])), 4),
        "V8_top1_ext_matched": round(float(np.mean([live_top1["V8"][r] for r in both])), 4)}
    print("matched:", json.dumps(out["matched_denominator"]), flush=True)

    # residual accounting: every remaining tactic-cause rank-1 under V8,
    # split by whether the ROOT theorem is itself part of a tactic's own
    # development (in which case the tactic candidate is the right answer
    # and the namespace-based grader is what is wrong)
    residual = []
    for r in roots:
        if len(set(deps_v[r]) - {r}) < 3:
            continue
        k8, r8, _, _ = score("V8", r)
        if k8 or not r8:
            continue
        rn = names[r]
        if category2(r8[0], rn) != "tactic":
            continue
        root_is_apparatus_dev = bool(stmt_concepts(r) & set(np.where(apparatus)[0]))
        residual.append({"thm": rn, "top1": names[r8[0]],
                         "root_in_tactic_ns": rn.startswith(TACTIC_NS + EXTRA_TACTIC_NS),
                         "root_states_apparatus": root_is_apparatus_dev})
    out["residual_tactic_rank1"] = residual
    n_root_tac = sum(1 for x in residual if x["root_in_tactic_ns"] or x["root_states_apparatus"])
    print(f"residual tactic rank-1: {len(residual)}; of which the root is itself "
          f"tactic-development: {n_root_tac}", flush=True)
    for x in residual:
        print("   ", x, flush=True)

    # bars
    v6e = out["V6"]["top1_extended_grader"]; v8e = out["V8"]["top1_extended_grader"]
    t6 = out["V6"]["top1_cause_extended"].get("tactic", 0)
    t8 = out["V8"]["top1_cause_extended"].get("tactic", 0)
    bars = {
        "bar1_v8_ge_v6_extended": bool(v8e >= v6e),
        "bar2_tactic_blames_cut_20pct": bool(t8 <= 0.8 * t6),
        "bar3_content_demotions_le_5": bool(len(dem_cases) <= 5)}
    out["bars"] = bars
    print("BARS:", json.dumps(bars), flush=True)
    print("CERTIFIED" if all(bars.values()) else "FALSIFIED", flush=True)

    with open(os.path.join(DATA, "phase4_holdout8_results.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
