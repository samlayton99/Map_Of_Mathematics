#!/usr/bin/env python3
"""DEVELOPMENT profiling #4: machinery by audience.

Adds to profile3's concept-level apparatus (stated-vs-used with inherited
statedness) a claim-level audience test for automation BRIDGE lemmas
(goal-world statements emitted only by tactics, e.g. omega's Int
restatements):

  served_to_machines(c) := humanUsers(c) == 0 AND genUsers(c) >= 3

where users are load-bearing value-side citers, counted DIRECTLY (a capsule
citing c is a gen user; the theorem owning the capsule is not a user of c).

  machineryB(root, c) := (taint(c) OR served_to_machines(c))
                         AND ingredients(c) ∩ stmtConcepts(root) == ∅

Measured: (a) audience distributions for known bridges vs real-move
controls (dev content rank-1s); false-flag rate on real moves;
(b) V6 vs V8b full proxy on dev (real sort key, zoom, atomic capsules);
(c) ledger tactic cases; (d) parent labels v2 (non-gen stmt-subject).
Dev data only.
"""
import json, os
import numpy as np
from collections import Counter

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP = os.path.join(SCRATCH2, "mathlib_deps5.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
DEV_SEED = 20260819
NSAMP = 2400
BATCH = 600
LOAD_ROLES = (0, 1, 2, 7)
LAMBDA = 20
NPROOF_FLOOR = 200

TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.", "Batteries.Tactic.")
GEN_MARKS = (".match_", "._simp", "._proof_", "._unary", ".eq_def", ".brecOn",
             ".below", ".ibelow", ".ctorIdx", ".injEq", ".sizeOf_spec", "._eq_",
             ".noConfusion", "._aux", "._f", "._g", ".proof_")

BRIDGE_PROBES = [
    "Lean.Omega.Int.le_of_not_lt", "Lean.Omega.Int.lt_of_not_le",
    "Lean.Omega.Int.ofNat_lt_of_lt", "Lean.Omega.Int.ofNat_le_of_le",
    "Lean.Omega.Constraint.addEquality_sat", "Nat.ToInt.add_congr",
    "Int.sub_nonneg_of_le", "Int.sub_eq_zero_of_eq",
    "Lean.Grind.eq_false_of_imp_eq_false", "Lean.Grind.of_forall_eq_false",
    "Lean.Grind.Order.nat_eq", "Mathlib.Tactic.Ring.Common.add_pf_add_gt",
]
REAL_PROBES = [
    "Decidable.byContradiction", "Classical.byContradiction", "eq_of_heq",
    "DFunLike.ext", "of_eq_true", "mul_one", "le_antisymm", "Int.toNat_eq_max",
    "Nat.div_lt_iff_lt_mul", "Set.prod_mono", "spectrum.resolvent_eq",
]


def load():
    idx, names = {}, []
    deps_v, deps_t, kinds, classes, vo, pr, gen = [], [], [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            deps_v.append(()); deps_t.append(()); kinds.append(""); classes.append(())
            vo.append(()); pr.append(False); gen.append(False)
        return i
    with open(DUMP) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]; classes[i] = tuple(r["c"])
            pr[i] = bool(r.get("pr", False)); gen[i] = bool(r.get("gen", False))
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
            vo[i] = tuple(tuple(int(x) for x in row) for row in r.get("vo", ()))
    return idx, names, deps_v, deps_t, kinds, classes, vo, pr, gen


def main():
    idx, names, deps_v, deps_t, kinds, classes, vo, pr, gen = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    pr = np.array(pr); gen = np.array(gen)
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

    ing_cache = {}
    def nonuniv_ingredients(c):
        r = ing_cache.get(c)
        if r is None:
            r = frozenset(k for k in set(deps_t[c])
                          if k != c and is_concept[k] and univ[k] < 0.02)
            ing_cache[c] = r
        return r
    def bookkeeping(c):
        return not nonuniv_ingredients(c)
    claimf = lambda c: pr[c] and kinds[c] not in ("constructor", "recursor")

    # nproof + per-claim audience in one pass
    nproof = np.zeros(n, dtype=np.int64)
    huse = np.zeros(n, dtype=np.int64)   # human (non-gen) load-bearing users
    guse = np.zeros(n, dtype=np.int64)   # gen load-bearing users
    for i in range(n):
        if not deps_v[i]:
            continue
        ig = bool(gen[i])
        ks = set()
        for d, row in zip(deps_v[i], vo[i]):
            if d != i and any(row[r0] > 0 for r0 in LOAD_ROLES):
                if claimf(d):
                    ks |= nonuniv_ingredients(d)
                if ig:
                    guse[d] += 1
                else:
                    huse[d] += 1
        for k in ks:
            nproof[k] += 1
    print("usage/audience done", flush=True)

    apparatus = is_concept & (univ < 0.02) & (nproof > NPROOF_FLOOR) & (nproof > LAMBDA * (inherited + 1))
    print(f"apparatus concepts: {int(apparatus.sum())}", flush=True)

    taint_cache = {}
    def tainted(c):
        r = taint_cache.get(c)
        if r is None:
            r = any(apparatus[k] for k in nonuniv_ingredients(c))
            taint_cache[c] = r
        return r
    def served_to_machines(c):
        return huse[c] == 0 and guse[c] >= 3

    print("\n=== audience probes ===", flush=True)
    for group, lst in (("BRIDGE", BRIDGE_PROBES), ("REAL", REAL_PROBES)):
        for nm in lst:
            i = idx.get(nm)
            if i is None:
                print(f"  {group:<7} {nm:<50} (absent)"); continue
            print(f"  {group:<7} {nm:<50} human={int(huse[i]):>7} gen={int(guse[i]):>7} "
                  f"taint={int(tainted(i))} stm={int(served_to_machines(i))}", flush=True)

    def loadbearing(r):
        outp = set()
        for d, row in zip(deps_v[r], vo[r]):
            if d != r and any(row[k] > 0 for k in LOAD_ROLES):
                outp.add(d)
        return outp
    def loadbearing_g(c):
        return {d for d, row in zip(deps_v[c], vo[c])
                if d != c and any(row[k] > 0 for k in (0, 1, 2, 7))}

    def machinery0(c):
        return tainted(c) or served_to_machines(c)

    def make_attr(exclude_mach):
        cache = {}
        def attribute(c, seen=None):
            if c in cache:
                return cache[c]
            if seen is None:
                seen = set()
            if not gen[c] or c in seen:
                return c
            seen.add(c)
            subst = [d for d in loadbearing_g(c) if claimf(d) and not bookkeeping(d)
                     and not (exclude_mach and machinery0(d))]
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

    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    dev_roots = np.random.default_rng(DEV_SEED).choice(pool, size=NSAMP, replace=False).tolist()
    ledger = json.load(open(os.path.join(DATA, "phase4_ledger.json")))
    tac_thms = [f["thm"] for f in ledger["failures"] if f["cat"] == "tactic"]
    roots = list(dict.fromkeys(dev_roots + [idx[t] for t in tac_thms if t in idx]))

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
        return machinery0(c) and not (nonuniv_ingredients(c) & rs)

    def score(vname, r):
        rn = names[r]
        rs = stmt_concepts(r)
        if vname == "V6":
            cs = set(cand6[r]); dem = lambda c: bookkeeping(c)
        else:
            cs = set(cand8[r]); dem = lambda c: bookkeeping(c) or machinery(rs, c)
        nf = newflag[r]
        key = lambda c: (dem(c), not nf.get(c, True), -int(depth[c]))
        if cs and all(dem(c) for c in cs):
            kind = "definitional" if all(bookkeeping(c) for c in cs) else "automation"
            return kind, [], {}
        ranked = sorted(cs, key=key)
        opened = set()
        for _ in range(8):
            if not ranked or indeg_v[ranked[0]] > 1 or ranked[0] in opened:
                break
            top = ranked[0]
            inner = {c for c in loadbearing_g(top) if claimf(c) and c != r}
            if vname == "V8" and gen[top]:
                sub = [d for d in inner if not bookkeeping(d)]
                if sub and all(machinery(rs, d) for d in sub):
                    break
            opened.add(top)
            ranked = sorted((set(ranked) - {top}) | inner, key=key)
        cats = {c: category(c, rn) for c in ranked}
        return None, ranked, cats

    out = {"apparatus_count": int(apparatus.sum())}
    for vname in ("V6", "V8"):
        fcr, cause, verd = [], Counter(), Counter()
        atomic_top1 = 0
        for r in dev_roots:
            if len(set(deps_v[r]) - {r}) < 3:
                continue
            kind, ranked, cats = score(vname, r)
            if kind:
                verd[kind] += 1; fcr.append(0); continue
            if not ranked:
                verd["empty"] += 1; fcr.append(0); continue
            fc = next((k + 1 for k, c in enumerate(ranked) if cats[c] == "content"), 99)
            fcr.append(fc)
            c1 = cats[ranked[0]]
            if c1 != "content":
                cause[c1] += 1
                if vname == "V8" and gen[ranked[0]]:
                    rs = stmt_concepts(r)
                    sub = [d for d in loadbearing_g(ranked[0]) if claimf(d) and not bookkeeping(d)]
                    if sub and all(machinery(rs, d) for d in sub):
                        atomic_top1 += 1
        a = np.array(fcr)
        live = a[a > 0]
        e = {"verdicts": dict(verd),
             "top1_nonmachinery_proxy": round(float((live == 1).mean()), 4),
             "no_content": round(float((live == 99).mean()), 4),
             "top1_cause_when_machinery": dict(cause),
             "n_live": int((a > 0).sum())}
        if vname == "V8":
            e["atomic_capsule_top1"] = atomic_top1
            lv = (live == 1).sum()
            e["top1_proxy_capsule_as_ok"] = round(float((lv + atomic_top1) / max(1, len(live))), 4)
        out[vname] = e
        print(vname, "=", json.dumps(e), flush=True)

    lt = []
    for tname in tac_thms:
        r = idx.get(tname)
        if r is None:
            continue
        kind, ranked, cats = score("V8", r)
        row = {"thm": tname, "verdict": kind,
               "top5": [(names[c], cats[c]) for c in ranked[:5]]}
        lt.append(row)
        print(" LEDGER", tname, "->", kind or [f"{nm}({ct})" for nm, ct in row["top5"][:3]], flush=True)
    out["ledger_cases_v8"] = lt

    diffs = []
    for r in dev_roots:
        if len(set(deps_v[r]) - {r}) < 3:
            continue
        k6, r6, c6c = score("V6", r)
        k8, r8, c8c = score("V8", r)
        t6 = ("VERDICT:" + k6) if k6 else (names[r6[0]] if r6 else "empty")
        t8 = ("VERDICT:" + k8) if k8 else (names[r8[0]] if r8 else "empty")
        if t6 != t8:
            diffs.append({"thm": names[r], "v6": t6,
                          "v6_cat": (c6c.get(r6[0]) if r6 and not k6 else None),
                          "v8": t8,
                          "v8_cat": (c8c.get(r8[0]) if r8 and not k8 else None)})
    out["rank1_diffs"] = diffs
    print(f"rank1 diffs: {len(diffs)}", flush=True)
    for d in diffs:
        if d["v6_cat"] == "content" and (d["v8_cat"] != "content"):
            print("  REGRESS:", d["thm"], "|", d["v6"], "->", d["v8"], f"({d['v8_cat']})", flush=True)

    # false-flag audit: dev V6 content rank-1s that machineryB would demote
    ff = []
    for r in dev_roots:
        if len(set(deps_v[r]) - {r}) < 3:
            continue
        k6, r6, c6c = score("V6", r)
        if k6 or not r6:
            continue
        c = r6[0]
        if c6c.get(c) == "content" and machinery(stmt_concepts(r), c):
            ff.append((names[r], names[c], "stm" if served_to_machines(c) else "taint"))
    out["false_flags_on_content_top1"] = ff
    print(f"content rank-1 flagged by machineryB: {len(ff)}", flush=True)
    for x in ff:
        print("   ", x, flush=True)

    # parent labels v2: stmt-subject restricted to non-gen concepts
    needg = set()
    for f in ledger["failures"]:
        if f["cat"] == "generated":
            c = idx.get(f["top1"])
            if c is not None and gen[c]:
                needg.add(c)
    ulb = {c: [] for c in needg}
    for i in range(n):
        for d, row in zip(deps_v[i], vo[i]):
            if d in ulb and d != i and any(row[k] > 0 for k in LOAD_ROLES):
                ulb[d].append(i)
    plab = []
    for c in sorted(needg, key=lambda c: names[c]):
        a = attr8(c)
        if a != c and not machinery0(a):
            plab.append({"gen": names[c], "rule": "attribution", "parent": names[a]}); continue
        defs = [u for u in set(ulb[c]) if not gen[u] and not pr[u]]
        if len(defs) == 1:
            plab.append({"gen": names[c], "rule": "def-user", "parent": names[defs[0]]}); continue
        sc = [k for k in set(deps_t[c]) if is_concept[k] and univ[k] < 0.02 and not gen[k]]
        best, bestcov = None, -1.0
        for k in sc:
            kd = set(deps[k]) | {k}
            rest = [x for x in sc if x != k]
            cov = sum(1 for x in rest if x in kd) / max(1, len(rest))
            if cov > bestcov or (cov == bestcov and best is not None and depth[k] > depth[best]):
                best, bestcov = k, cov
        if best is not None and bestcov >= 0.49:
            plab.append({"gen": names[c], "rule": f"stmt-subject({bestcov:.2f})", "parent": names[best]})
        else:
            plab.append({"gen": names[c], "rule": "UNRESOLVED", "parent": None})
    out["parent_labels"] = plab
    cov = Counter(p["rule"].split("(")[0] for p in plab)
    print("parent label coverage:", dict(cov), flush=True)
    for p in plab:
        if p["rule"].startswith(("stmt-subject", "UNRESOLVED", "def-user")):
            print(f"   {p['gen']:<75} {p['rule']:<18} -> {p['parent']}", flush=True)

    with open(os.path.join(DATA, "profile4_audience.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("written", flush=True)


if __name__ == "__main__":
    main()
