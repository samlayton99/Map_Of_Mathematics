#!/usr/bin/env python3
"""DEVELOPMENT profiling #2: the stated-vs-used asymmetry.

Hypothesis: a decision procedure's encoding concepts are USED (via support
claims, in proofs) out of all proportion to how often they are STATED
(mentioned in theorem statements). Real mathematical concepts are used
roughly in proportion to their statement audience. Formally, per concept k:

  nstmt(k)  = number of human-stated theorems whose statement mentions k
  nproof(k) = number of constants (any, incl. generated capsules) whose
              proof cites, load-bearing, a claim having k among its
              non-universal ingredients

  apparatus(k) := nproof(k) > lambda * (nstmt(k) + 1)     [lambda swept]

Then, relative to a root theorem T, a candidate claim C demotes iff some
ingredient of C is apparatus AND no ingredient of C appears directly in T's
statement (goal-relevant claims are spared).

This script measures: (a) the (nstmt, nproof) landscape — do known
apparatus clusters separate from known math concepts, and by what margin;
(b) junk-fix rate on the 17 ledger tactic cases including INSIDE their
capsules; (c) false-demotion on the dev sample.
Also (d): root-chain parent resolution for multi-parent generated rank-1s.
Dev data only; no certification claims.
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
LOAD_ROLES = (0, 1, 2, 7)

TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.", "Batteries.Tactic.")
GEN_MARKS = (".match_", "._simp", "._proof_", "._unary", ".eq_def", ".brecOn",
             ".below", ".ibelow", ".ctorIdx", ".injEq", ".sizeOf_spec", "._eq_",
             ".noConfusion", "._aux", "._f", "._g", ".proof_")

PROBE_APPARATUS = [
    "Lean.Omega.LinearCombo", "Lean.Omega.LinearCombo.eval", "Lean.Omega.Coeffs",
    "Lean.Omega.Coeffs.ofList", "Lean.Grind.CommRing.Poly", "Lean.Grind.CommRing.Expr",
    "Lean.Grind.CommRing.Poly.denote", "Mathlib.Tactic.Abel.termg",
    "Mathlib.Tactic.Abel.term", "Mathlib.Tactic.Module.NF", "Lean.Data.AC.Context",
    "Mathlib.Tactic.Ring.ExSum", "Mathlib.Tactic.NormNum.IsInt",
    "Lean.Grind.IsCharP",
]
PROBE_REAL = [
    "ConvexOn", "Finset.sum", "Real.exp", "Nat.mul", "Int.emod", "Filter",
    "MeasureTheory.Measure", "Polynomial", "CategoryTheory.Functor", "Set.image",
    "Nat.gcd", "Matrix", "HPow.hPow", "Finset", "List.length", "Multiset",
    "WellFounded", "Acc", "Nonempty", "Decidable",
]


def load():
    idx, names = {}, []
    deps_v, deps_t, kinds, classes, hbs, vo, pr, bf, gen, rts = [], [], [], [], [], [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            deps_v.append(()); deps_t.append(()); kinds.append(""); classes.append(())
            hbs.append(()); vo.append(()); pr.append(False); bf.append(0); gen.append(False)
            rts.append(())
        return i
    with open(DUMP) as f:
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
            rts[i] = tuple(nid(d) for d in r.get("rt", ()))
    return idx, names, deps_v, deps_t, kinds, classes, hbs, vo, pr, bf, gen, rts


def main():
    idx, names, deps_v, deps_t, kinds, classes, hbs, vo, pr, bf, gen, rts = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    pr = np.array(pr); gen = np.array(gen)
    thm = np.array([k == "theorem" for k in kinds])
    has_class = np.array([len(c) > 0 for c in classes])

    CONCEPT_KINDS = ("def", "inductive", "opaque", "quot", "axiom")
    is_concept = np.array([k in CONCEPT_KINDS for k in kinds])
    human_thm = thm & ~gen
    cnt = np.zeros(n, dtype=np.int64)
    ht_ids = np.where(human_thm)[0]
    for i in ht_ids:
        for c in set(deps_t[i]):
            cnt[c] += 1
    nstmt = cnt
    univ = cnt / max(1, len(ht_ids))

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

    # ---- nproof(k): constants whose proof cites (load-bearing) a claim with
    # ingredient k. One pass over all constants with values.
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
    print("usage counts done", flush=True)

    # ---- (a) landscape
    print("\n=== probe concepts: nstmt / nproof / ratio ===", flush=True)
    for group, lst in (("APPARATUS", PROBE_APPARATUS), ("REAL", PROBE_REAL)):
        for nm in lst:
            i = idx.get(nm)
            if i is None:
                print(f"  {group:<9} {nm:<45} (absent)")
                continue
            r = nproof[i] / (nstmt[i] + 1)
            print(f"  {group:<9} {nm:<45} nstmt={int(nstmt[i]):>7} nproof={int(nproof[i]):>8} ratio={r:>9.1f} univ={univ[i]*100:.3f}%")

    # global distribution: concepts with meaningful usage
    mask = is_concept & (univ < 0.02) & (nproof > 200)
    ratios = nproof[mask] / (nstmt[mask] + 1)
    print(f"\nconcepts (nonuniversal, nproof>200): {int(mask.sum())}")
    for q in (50, 75, 90, 95, 98, 99, 99.5):
        print(f"  ratio p{q}: {np.percentile(ratios, q):.1f}")
    # who lives above various lambdas
    out_top = []
    for lam in (5, 10, 20, 50):
        ids = np.where(mask & (nproof > lam * (nstmt + 1)))[0]
        out_top.append((lam, len(ids)))
        print(f"  lambda={lam}: {len(ids)} apparatus concepts")
    lam = 20
    app_ids = np.where(is_concept & (univ < 0.02) & (nproof > lam * (nstmt + 1)) & (nproof > 200))[0]
    order_ids = app_ids[np.argsort(-nproof[app_ids])]
    print(f"\ntop apparatus concepts at lambda={lam} (by nproof):")
    for i in order_ids[:60]:
        print(f"  {names[i]:<70} nstmt={int(nstmt[i]):>5} nproof={int(nproof[i]):>8}")
    apparatus = np.zeros(n, dtype=bool)
    apparatus[app_ids] = True

    def loadbearing(r):
        out = set()
        for d, row in zip(deps_v[r], vo[r]):
            if d != r and any(row[k] > 0 for k in LOAD_ROLES):
                out.add(d)
        return out

    def tainted(c):
        return any(apparatus[k] for k in nonuniv_ingredients(c))

    def demoted(rt_stmt, c):
        return tainted(c) and not (nonuniv_ingredients(c) & rt_stmt)

    attr_cache = {}
    def loadbearing_g(c):
        return {d for d, row in zip(deps_v[c], vo[c])
                if d != c and any(row[k] > 0 for k in (0, 1, 2, 7))}
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

    # ---- (b) the 17 ledger cases: look INSIDE capsules
    ledger = json.load(open(os.path.join(DATA, "phase4_ledger.json")))
    tac_cases = [(f["thm"], f["top1"]) for f in ledger["failures"] if f["cat"] == "tactic"]
    print("\n=== ledger tactic cases: capsule-aware assessment ===", flush=True)
    results = []
    for tname, top1name in tac_cases:
        r = idx.get(tname)
        if r is None:
            continue
        rt_stmt = frozenset(k for k in set(deps_t[r]) if is_concept[k] and univ[k] < 0.02)
        lb = {attribute(c) for c in loadbearing(r) if claimf(c)}
        rows = []
        for c in sorted(lb, key=lambda c: -int(nproof[c] if False else 0)):
            inner = None
            if gen[c]:
                sub = [d for d in loadbearing_g(c) if claimf(d) and not bookkeeping(d)]
                inner = {"n_sub": len(sub),
                         "n_sub_demoted": sum(1 for d in sub if demoted(rt_stmt, d)),
                         "sub_sample": [(names[d], demoted(rt_stmt, d)) for d in sub[:8]]}
            rows.append({"cand": names[c], "cat": category(c, tname),
                         "bk": bool(bookkeeping(c)), "demoted": bool(demoted(rt_stmt, c)),
                         "capsule": inner})
        results.append({"thm": tname, "old_top1": top1name, "rows": rows})
        # summary line
        direct_junk_fixed = all(x["demoted"] or x["bk"] or x["cat"] != "tactic" for x in rows)
        caps = [x for x in rows if x["capsule"]]
        cap_atomic = [x for x in caps if x["capsule"]["n_sub"] > 0 and
                      x["capsule"]["n_sub_demoted"] == x["capsule"]["n_sub"]]
        print(f"  {tname}")
        for x in rows:
            mark = "DEMOTED" if x["demoted"] else ("bk" if x["bk"] else "keep")
            capnote = ""
            if x["capsule"]:
                capnote = f" [capsule: {x['capsule']['n_sub_demoted']}/{x['capsule']['n_sub']} inner demoted]"
            print(f"     {mark:<8} {x['cat']:<11} {x['cand']}{capnote}")

    # ---- (c) dev-sample false-demotion audit
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    dev_roots = np.random.default_rng(DEV_SEED).choice(pool, size=NSAMP, replace=False).tolist()
    n_live = 0; content_demoted = []; verdicts = []; changed = Counter()
    cap_atomic_count = 0; cap_total = 0
    for r in dev_roots:
        if len(set(deps_v[r]) - {r}) < 3:
            continue
        rn = names[r]
        rt_stmt = frozenset(k for k in set(deps_t[r]) if is_concept[k] and univ[k] < 0.02)
        cs = {attribute(c) for c in loadbearing(r) if claimf(c)}
        if not cs or all(bookkeeping(c) for c in cs):
            continue
        n_live += 1
        for c in cs:
            if gen[c]:
                sub = [d for d in loadbearing_g(c) if claimf(d) and not bookkeeping(d)]
                if sub:
                    cap_total += 1
                    if all(demoted(rt_stmt, d) for d in sub):
                        cap_atomic_count += 1
        v6 = sorted(cs, key=lambda c: (bookkeeping(c),))
        # order within tiers is arbitrary here; we only audit flag effects
        dem = {c for c in cs if demoted(rt_stmt, c)}
        for c in dem:
            if category(c, rn) == "content":
                content_demoted.append((rn, names[c]))
        if all(bookkeeping(c) or c in dem for c in cs):
            verdicts.append((rn, [names[c] for c in cs if c in dem][:6]))
    print(f"\ndev audit: live={n_live}, content-claims demoted={len(content_demoted)}, "
          f"all-demoted verdicts={len(verdicts)}, capsules={cap_total} of which atomic={cap_atomic_count}", flush=True)
    print("content demotions (all):")
    for rn, cn in content_demoted[:40]:
        print(f"   {rn}  ->  {cn}")
    print("new automation verdicts (sample):")
    for rn, l in verdicts[:20]:
        print(f"   {rn}: {l}")

    # ---- (d) root-chain parent resolution for multi-parent gen rank-1s
    print("\n=== multi-parent label: root-chain resolution ===", flush=True)
    def rt_parent(c):
        for d in rts[c]:
            if d != c and not gen[d] and any(is_concept[k] or True for k in (d,)) :
                # first non-generated constant in the root chain
                if univ[d] < 0.02 or not is_concept[d]:
                    return d
        return None
    ok = 0; tot = 0
    for f in ledger["failures"]:
        if f["cat"] != "generated":
            continue
        c = idx.get(f["top1"])
        if c is None or not gen[c] or attribute(c) != c:
            continue
        tot += 1
        p = rt_parent(c)
        # fallback: unique non-gen non-Prop user
        print(f"   {names[c]:<75} rt-parent: {names[p] if p is not None else None}")
        if p is not None:
            ok += 1
    print(f"root-chain parent resolved: {ok}/{tot}")

    with open(os.path.join(DATA, "profile2_apparatus.json"), "w") as fh:
        json.dump({"lambda_counts": out_top,
                   "ledger_cases": results,
                   "content_demoted": content_demoted,
                   "verdicts": verdicts}, fh, indent=1)
    print("written", flush=True)


if __name__ == "__main__":
    main()
