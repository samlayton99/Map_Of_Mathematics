#!/usr/bin/env python3
"""DEVELOPMENT profiling #7: capsule-rule variants (dev only).

V8a = demotion tier + verdicts, NO capsule rule (zoom opens as in V6).
V8b = V8a + capsule atomic iff the TOP-RANKED inner claim is machinery
      (rank inside the capsule with the same key; if the best thing in
      there is a machine step, the capsule is a machine block).
Profile6 showed "atomic iff ANY inner claim is machinery" hides real
moves (4 cases / 1874). Regressions counted under the EXTENDED grader so
core-internal arithmetic junk is not miscounted as content.

Original profile6 header follows.

DEVELOPMENT profiling #6: V8 with the sort split.

Profile5's capsule rule over-atomized through the True-taint (every simp
block carries an eq_true twin). Fix is the kernel's own sort distinction:

  APPARATUS concepts (drive demotion + capsule atomicity) must be
  DATA-sorted (pr = false): a decision procedure's certificate vocabulary
  is data by nature (Constraint, ExSum, Poly, decide). True/False are
  Prop-sorted and drop out.

  BOOKKEEPING is extended kernel-honestly: a claim whose non-universal
  ingredients are all Prop-sorted concepts (True, False) is bookkeeping —
  its only non-universal subject matter is propositional constants
  (eq_true, iff_self, of_eq_true). This is what resolves simp twins in
  attribution, and what turns simp-trivial lists into verdicts.

  machinery(root, c) := taint(c) AND ingredients(c) ∩ stmtConcepts(root)=∅
  demote tier = bookkeeping' OR machinery; all-demoted => verdict
  capsule atomic := gen AND >=1 inner substantive claim is machinery
  attribution/labels: substantive = not bookkeeping' and not machinery;
  labels never fall back to bookkeeping targets.

Measured: V6 vs V8 (raw + extended grader), capsule cost with named hidden
content, ledger cases, parent-label coverage.  Dev data only.
"""
import json, os
import numpy as np
from collections import Counter

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP = os.path.join(SCRATCH2, "mathlib_deps6.jsonl")
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

    # bare proposition: Prop-sorted concept with no ingredients of its own
    # (True, False) -- as opposed to predicates (Even, Membership.mem), which
    # always mention the data they speak about. Kernel sort + kernel refs.
    n_tdeps = np.array([len(set(t)) for t in deps_t])
    bare_prop = is_concept & ps & (n_tdeps == 0)
    print(f"bare propositions: {int(bare_prop.sum())} -> "
          f"{[names[i] for i in np.where(bare_prop)[0][:12]]}", flush=True)

    ing_cache = {}
    def nonuniv_ingredients(c):
        r = ing_cache.get(c)
        if r is None:
            r = frozenset(k for k in set(deps_t[c])
                          if k != c and is_concept[k] and univ[k] < 0.02)
            ing_cache[c] = r
        return r
    def bookkeeping(c):
        # extended: no non-universal ingredient, or every one of them is a
        # bare PROPOSITION (ps and no data arguments) -- True/False style
        return all(bare_prop[k] for k in nonuniv_ingredients(c))
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

    apparatus = (is_concept & ~ps & (univ < 0.02) & (nproof > NPROOF_FLOOR)
                 & (nproof > LAMBDA * (inherited + 1)))
    print(f"apparatus concepts (data-sorted): {int(apparatus.sum())}", flush=True)
    app_ids = np.where(apparatus)[0]
    for i in app_ids[np.argsort(-nproof[app_ids])][:30]:
        print(f"   {names[i]:<70} inh={int(inherited[i]):>6} nproof={int(nproof[i]):>8}", flush=True)

    taint_cache = {}
    def tainted(c):
        r = taint_cache.get(c)
        if r is None:
            r = any(apparatus[k] for k in nonuniv_ingredients(c))
            taint_cache[c] = r
        return r
    def served_to_machines(c):
        return huse[c] == 0 and guse[c] >= 3

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
        return tainted(c)

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

    # extended grader (EVAL ONLY): two measured blind spots fixed —
    # core-Lean internal-arith namespaces counted as tactic machinery, and
    # the True-twin normalization family counted as glue
    EXTRA_TACTIC_NS = ("Int.Internal.", "Nat.Internal.")
    TRUE_TWINS = {"of_eq_true", "eq_true", "eq_self", "eq_self_iff_true",
                  "iff_self", "iff_self_iff", "ite_cond_eq_true", "ite_cond_eq_false",
                  "forall_true_left", "forall_const", "not_true_eq_false",
                  "implies_true", "and_true", "true_and", "and_self", "eq_true_eq_id"}
    def category2(c, root_name):
        nm = names[c]
        if nm.startswith(EXTRA_TACTIC_NS):
            return "tactic"
        if nm.split(".")[-1] in TRUE_TWINS or nm in TRUE_TWINS:
            return "glue"
        return category(c, root_name)

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

    def atomic_capsule(rs, g):
        """gen constant whose inner substantive claims include >=1 machinery
        item: provably machine-emitted, zoom keeps it closed."""
        if not gen[g]:
            return False
        sub = [d for d in loadbearing_g(g) if claimf(d) and not bookkeeping(d)]
        return bool(sub) and any(machinery(rs, d) for d in sub)

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
            return kind, [], {}, None
        ranked = sorted(cs, key=key)
        opened = set()
        top1_atomic = False
        for _ in range(8):
            if not ranked or indeg_v[ranked[0]] > 1 or ranked[0] in opened:
                break
            top = ranked[0]
            if vname == "V8b" and gen[top]:
                inner0 = [c for c in loadbearing_g(top) if claimf(c) and c != r]
                if inner0:
                    best = sorted(inner0, key=key)[0]
                    if dem(best):
                        top1_atomic = True
                        break
            inner = {c for c in loadbearing_g(top) if claimf(c) and c != r}
            opened.add(top)
            ranked = sorted((set(ranked) - {top}) | inner, key=key)
        cats = {c: category(c, rn) for c in ranked}
        return None, ranked, cats, top1_atomic

    out = {"apparatus_count": int(apparatus.sum())}
    for vname in ("V6", "V8a", "V8b"):
        fcr, fcr2, cause, cause2, verd = [], [], Counter(), Counter(), Counter()
        atomic_top1 = 0
        for r in dev_roots:
            if len(set(deps_v[r]) - {r}) < 3:
                continue
            kind, ranked, cats, t1a = score(vname, r)
            if kind:
                verd[kind] += 1; fcr.append(0); fcr2.append(0); continue
            if not ranked:
                verd["empty"] += 1; fcr.append(0); fcr2.append(0); continue
            rn = names[r]
            cats2 = {c: category2(c, rn) for c in ranked}
            fc = next((k + 1 for k, c in enumerate(ranked) if cats[c] == "content"), 99)
            fc2 = next((k + 1 for k, c in enumerate(ranked) if cats2[c] == "content"), 99)
            fcr.append(fc); fcr2.append(fc2)
            if t1a:
                atomic_top1 += 1
            if cats[ranked[0]] != "content":
                cause[cats[ranked[0]]] += 1
            if cats2[ranked[0]] != "content":
                cause2[cats2[ranked[0]]] += 1
        a = np.array(fcr); a2 = np.array(fcr2)
        live = a[a > 0]; live2 = a2[a2 > 0]
        e = {"verdicts": dict(verd),
             "top1_nonmachinery_proxy": round(float((live == 1).mean()), 4),
             "top1_extended_grader": round(float((live2 == 1).mean()), 4),
             "no_content": round(float((live == 99).mean()), 4),
             "top1_cause_when_machinery": dict(cause),
             "top1_cause_extended": dict(cause2),
             "n_live": int((a > 0).sum())}
        if vname != "V6":
            e["atomic_capsule_top1"] = atomic_top1
            e["top1_extended_capsule_as_verdict"] = round(
                float((live2 == 1).sum() + atomic_top1) / max(1, len(live2)), 4)
        out[vname] = e
        print(vname, "=", json.dumps(e), flush=True)

    lt = []
    for tname in tac_thms:
        r = idx.get(tname)
        if r is None:
            continue
        for vn in ("V8a", "V8b"):
            kind, ranked, cats, t1a = score(vn, r)
            row = {"thm": tname, "variant": vn, "verdict": kind,
                   "top1_atomic_capsule": t1a,
                   "top5": [(names[c], cats[c]) for c in ranked[:5]]}
            lt.append(row)
            lab = kind or ("ATOMIC-CAPSULE" if t1a else
                           [f"{nm}({ct})" for nm, ct in row["top5"][:3]])
            print(f" LEDGER[{vn}]", tname, "->", lab, flush=True)
    out["ledger_cases_v8"] = lt

    for vn in ("V8a", "V8b"):
        real_reg, real_fix = [], []
        for r in dev_roots:
            if len(set(deps_v[r]) - {r}) < 3:
                continue
            rn = names[r]
            k6, r6, _, _ = score("V6", r)
            k8, r8, _, a8 = score(vn, r)
            if k6 or not r6:
                continue
            was_content = category2(r6[0], rn) == "content"
            now = ("VERDICT:" + k8) if k8 else (names[r8[0]] if r8 else "empty")
            now_content = (not k8) and bool(r8) and category2(r8[0], rn) == "content"
            if r8 and not k8 and r8[0] == r6[0]:
                continue
            if k8 or not r8 or r8[0] != r6[0]:
                rec = {"thm": rn, "was": names[r6[0]], "now": now, "atomic": bool(a8)}
                if was_content and not now_content and not a8:
                    real_reg.append(rec)
                elif was_content and a8:
                    real_reg.append({**rec, "note": "hidden behind capsule"})
                elif not was_content and (now_content or a8 or k8):
                    real_fix.append(rec)
        out[vn + "_regressions"] = real_reg
        out[vn + "_fixes"] = real_fix
        print(f"{vn}: real regressions {len(real_reg)}, junk fixes {len(real_fix)}", flush=True)
        for d in real_reg:
            print("   REGRESS:", d, flush=True)
        for d in real_fix[:15]:
            print("   FIX:", d, flush=True)

    # capsule-atomization cost: capsules that contain CLEAN content items
    # which default-collapse behind the verdict
    cost = []
    n_atomic = 0
    for r in dev_roots:
        if len(set(deps_v[r]) - {r}) < 3:
            continue
        rs = stmt_concepts(r)
        for c in cand8[r]:
            if False:
                n_atomic += 1
                rn = names[r]
                clean = [names[d] for d in loadbearing_g(c)
                         if claimf(d) and not bookkeeping(d) and not machinery(rs, d)
                         and category2(d, rn) == "content"]
                if clean:
                    cost.append({"thm": rn, "capsule": names[c], "hidden_clean": clean[:6]})
    out["capsule_cost"] = {"n_atomic_capsules": n_atomic, "n_with_clean_content": len(cost),
                          "cases": cost[:40]}
    print(f"atomic capsules in dev candidate lists: {n_atomic}; "
          f"with clean content default-hidden: {len(cost)}", flush=True)
    for x in cost[:20]:
        print("   ", x["thm"], "|", x["capsule"], "hides", x["hidden_clean"], flush=True)

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
    # label attribution: unique NON-MACHINERY claim in own proof, bookkeeping
    # targets allowed (labels need a parent, not a rank)
    lab_cache = {}
    def label_attr(c, seen=None):
        if c in lab_cache:
            return lab_cache[c]
        if seen is None:
            seen = set()
        if not gen[c] or c in seen:
            return c
        seen.add(c)
        nb = [d for d in loadbearing_g(c)
              if claimf(d) and not machinery0(d) and not bookkeeping(d)]
        res = label_attr(nb[0], seen) if len(nb) == 1 else c
        lab_cache[c] = res
        return res

    def stmt_subject(c):
        sc = [k for k in set(deps_t[c]) if is_concept[k] and univ[k] < 0.02 and not gen[k]]
        universal_fallback = False
        if not sc:
            sc = [k for k in set(deps_t[c]) if is_concept[k] and not gen[k]]
            universal_fallback = True
        best, bestcov = None, -1.0
        for k in sc:
            kd = set(deps[k]) | {k}
            rest = [x for x in sc if x != k]
            cov = sum(1 for x in rest if x in kd) / max(1, len(rest))
            if cov > bestcov or (cov == bestcov and best is not None and depth[k] > depth[best]):
                best, bestcov = k, cov
        return best, bestcov, universal_fallback

    plab = []
    for c in sorted(needg, key=lambda c: names[c]):
        a = label_attr(c)
        if a != c and not gen[a]:
            plab.append({"gen": names[c], "rule": "attribution", "parent": names[a]}); continue
        defs = [u for u in set(ulb[c]) if not gen[u] and not pr[u]]
        if len(defs) == 1:
            plab.append({"gen": names[c], "rule": "def-user", "parent": names[defs[0]]}); continue
        best, bestcov, uf = stmt_subject(c)
        if best is not None and bestcov >= 0.49:
            tag = "stmt-subject" + ("-univ" if uf else "")
            plab.append({"gen": names[c], "rule": f"{tag}({bestcov:.2f})", "parent": names[best]})
        else:
            plab.append({"gen": names[c], "rule": "UNRESOLVED", "parent": None})
    out["parent_labels"] = plab
    cov = Counter(p["rule"].split("(")[0] for p in plab)
    print("parent label coverage:", dict(cov), flush=True)
    for p in plab:
        print(f"   {p['gen']:<75} {p['rule']:<22} -> {p['parent']}", flush=True)

    with open(os.path.join(DATA, "profile7_variants.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("written", flush=True)


if __name__ == "__main__":
    main()
