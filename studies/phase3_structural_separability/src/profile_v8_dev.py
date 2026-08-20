#!/usr/bin/env python3
"""DEVELOPMENT profiling for the V8 candidate fix (NOT a certification round).

Question 1 (automation junk): does the name-free "foreign apparatus" predicate
separate tactic internals from real moves?
  foreign(r, c) := c's statement has >=1 non-universal concept ingredient AND
                   none of c's non-universal ingredients lie in r's
                   statement-world cone.
Inputs are constitution-level quantities only: statement references (kernel),
statement-world cone (kernel closure), measured universality theta=2%
(library-relative, certified in round 5).

Question 2 (multi-parent labels): for generated constants whose own move-set
has >=2 substantive claims (V6 attribution declines), does "the unique
non-generated NON-PROP user that cites it load-bearing" identify the parent
definition it was manufactured for?

Evaluated on: the 17 ledger tactic cases (round-5 sample) + the full dev
sample (seed 20260819). Dev data only; the registered round runs later on a
fresh seed.
"""
import json, os
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP = os.path.join(SCRATCH2, "mathlib_deps5.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
DEV_SEED = 20260819
NSAMP = 2400
BATCH = 600
LOAD_ROLES = (0, 1, 2, 7)

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
    return idx, names, deps_v, deps_t, kinds, classes, hbs, vo, pr, bf, gen


def main():
    idx, names, deps_v, deps_t, kinds, classes, hbs, vo, pr, bf, gen = load()
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
    print("depth done", flush=True)

    # value-side load-bearing user index (for multi-parent resolution)
    users_lb = [[] for _ in range(n)]
    for i in range(n):
        for d, row in zip(deps_v[i], vo[i]):
            if d != i and any(row[k] > 0 for k in LOAD_ROLES):
                users_lb[d].append(i)

    CONCEPT_KINDS = ("def", "inductive", "opaque", "quot", "axiom")
    is_concept = np.array([k in CONCEPT_KINDS for k in kinds])
    cnt = np.zeros(n, dtype=np.int64)
    thm_ids = np.where(thm)[0]
    for i in thm_ids:
        for c in set(deps_t[i]):
            cnt[c] += 1
    univ = cnt / max(1, len(thm_ids))

    def nonuniv_ingredients(c):
        return {k for k in set(deps_t[c]) if k != c and is_concept[k] and univ[k] < 0.02}

    def bookkeeping(c):
        return not nonuniv_ingredients(c)

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

    def loadbearing(r):
        out = set()
        for d, row in zip(deps_v[r], vo[r]):
            if d != r and any(row[k] > 0 for k in LOAD_ROLES):
                out.add(d)
        return out

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

    # -------- roots: dev sample + the 17 ledger tactic-case theorems --------
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    dev_roots = np.random.default_rng(DEV_SEED).choice(pool, size=NSAMP, replace=False).tolist()
    ledger = json.load(open(os.path.join(DATA, "phase4_ledger.json")))
    tac_cases = [(f["thm"], f["top1"]) for f in ledger["failures"] if f["cat"] == "tactic"]
    tac_roots = [idx[t] for t, _ in tac_cases if t in idx]
    roots = list(dict.fromkeys(dev_roots + tac_roots))
    print(f"roots: {len(roots)} ({len(tac_roots)} ledger tactic cases)", flush=True)

    # candidates (post-attribution) and the ingredient sets we need cone
    # membership for
    cand, need = {}, {}
    for r in roots:
        lb = {c for c in loadbearing(r) if claimf(c)}
        lb = {attribute(c) for c in lb}
        cand[r] = lb
        u = set(lb)
        for c in lb:
            u |= nonuniv_ingredients(c)
        need[r] = u
    print("candidates built", flush=True)

    dep_arrays = [np.array(ds, dtype=np.int64) if ds else None for ds in deps]
    rev = list(reversed(order))
    incone = {}
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
            incone[r] = {c: bool(reach[c, w] & bit) for c in need[r]}
        del reach
        print(f"batch {b0 // BATCH + 1}/{(len(roots) + BATCH - 1) // BATCH}", flush=True)

    def foreign(r, c):
        ing = nonuniv_ingredients(c)
        if not ing:
            return False
        ic = incone[r]
        return not any(ic.get(k, False) for k in ing)

    def foreign_frac(r, c):
        ing = nonuniv_ingredients(c)
        if not ing:
            return None
        ic = incone[r]
        return sum(0 if ic.get(k, False) else 1 for k in ing) / len(ing)

    out = {}

    # -------- Q1a: the 17 ledger junk cases, full-list profile --------
    cases = []
    for tname, top1name in tac_cases:
        r = idx.get(tname)
        if r is None:
            continue
        rows = []
        for c in sorted(cand[r], key=lambda c: (bookkeeping(c), not foreign(r, c))):
            rows.append({"cand": names[c], "cat": category(c, tname),
                         "bookkeeping": bool(bookkeeping(c)),
                         "foreign": bool(foreign(r, c)),
                         "foreign_frac": foreign_frac(r, c),
                         "n_ingredients": len(nonuniv_ingredients(c)),
                         "depth": int(depth[c])})
        # V8 ranking: demote bookkeeping-or-foreign, then (new omitted here —
        # nf not computed for this profile; use -depth as the residual key)
        v8 = sorted(cand[r], key=lambda c: (bookkeeping(c) or foreign(r, c), -int(depth[c])))
        v8top = names[v8[0]] if v8 else None
        v8cat = category(v8[0], tname) if v8 else None
        all_dem = bool(cand[r]) and all(bookkeeping(c) or foreign(r, c) for c in cand[r])
        cases.append({"thm": tname, "old_top1": top1name,
                      "old_top1_foreign": next((x["foreign"] for x in rows if x["cand"] == top1name), None),
                      "v8_top1": v8top, "v8_top1_cat": v8cat,
                      "all_demoted_verdict": all_dem, "list": rows})
    out["ledger_tactic_cases"] = cases
    flagged = sum(1 for c in cases if c["old_top1_foreign"])
    fixed = sum(1 for c in cases if c["v8_top1_cat"] == "content" or c["all_demoted_verdict"])
    print(f"Q1a: old junk top1 flagged foreign: {flagged}/{len(cases)}; "
          f"v8 content-or-verdict: {fixed}/{len(cases)}", flush=True)

    # -------- Q1b: false-demotion audit on the dev sample --------
    changed, newly_verdicted, content_demoted = [], [], 0
    n_live = 0
    for r in dev_roots:
        if len(set(deps_v[r]) - {r}) < 3 or not cand[r]:
            continue
        cs = cand[r]
        if all(bookkeeping(c) for c in cs):
            continue  # already a by-definition verdict in V6
        n_live += 1
        v6 = sorted(cs, key=lambda c: (bookkeeping(c), -int(depth[c])))
        v8 = sorted(cs, key=lambda c: (bookkeeping(c) or foreign(r, c), -int(depth[c])))
        all_dem = all(bookkeeping(c) or foreign(r, c) for c in cs)
        rn = names[r]
        c6, c8 = category(v6[0], rn), category(v8[0], rn)
        if c6 == "content" and foreign(r, v6[0]):
            content_demoted += 1
        if all_dem:
            newly_verdicted.append({"thm": rn, "old_top1": names[v6[0]], "old_cat": c6,
                                    "list": [names[c] for c in v6[:6]]})
        elif v6[0] != v8[0]:
            changed.append({"thm": rn, "old": names[v6[0]], "old_cat": c6,
                            "new": names[v8[0]], "new_cat": c8})
    out["dev_audit"] = {
        "n_live": n_live,
        "content_top1_flagged_foreign": content_demoted,
        "rank1_changed": changed,
        "newly_verdicted": newly_verdicted}
    from collections import Counter
    trans = Counter((c["old_cat"], c["new_cat"]) for c in changed)
    print(f"Q1b: live {n_live}; content-top1 flagged foreign: {content_demoted}; "
          f"rank1 changed: {len(changed)}; newly verdicted: {len(newly_verdicted)}", flush=True)
    print("transitions:", dict(trans), flush=True)
    print("newly verdicted sample:", flush=True)
    for x in newly_verdicted[:25]:
        print("  ", x["thm"], "| old top1:", x["old_top1"], f"({x['old_cat']})", flush=True)

    # -------- Q2: multi-parent resolution on ledger generated cases --------
    gcases = []
    for f in ledger["failures"]:
        if f["cat"] != "generated":
            continue
        c = idx.get(f["top1"])
        if c is None or not gen[c]:
            continue
        if attribute(c) != c:
            continue  # V6 already resolves it
        subst = [d for d in loadbearing_g(c) if claimf(d) and not bookkeeping(d)]
        nong = [u for u in set(users_lb[c]) if not gen[u]]
        defs = [u for u in nong if not pr[u]]
        props = [u for u in nong if pr[u]]
        gcases.append({"gen": names[c], "thm": f["thm"], "n_subst_claims": len(subst),
                       "n_nongen_users": len(nong), "n_def_users": len(defs),
                       "def_users": [names[u] for u in defs[:5]],
                       "unique_def_parent": names[defs[0]] if len(defs) == 1 else None,
                       "prop_users": [names[u] for u in props[:3]]})
    out["multiparent_cases"] = gcases
    uniq = sum(1 for g in gcases if g["unique_def_parent"])
    zero = sum(1 for g in gcases if g["n_def_users"] == 0)
    multi = sum(1 for g in gcases if g["n_def_users"] > 1)
    print(f"Q2: {len(gcases)} unresolved generated rank-1s; unique def parent: {uniq}; "
          f"zero def users: {zero}; multiple: {multi}", flush=True)
    for g in gcases[:15]:
        print("  ", g["gen"], "-> parent:", g["unique_def_parent"],
              f"(defs={g['n_def_users']}, nongen={g['n_nongen_users']})", flush=True)

    with open(os.path.join(DATA, "profile_v8_dev.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("written", flush=True)


if __name__ == "__main__":
    main()
