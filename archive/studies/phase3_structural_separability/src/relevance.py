#!/usr/bin/env python3
"""One-axis residue attack + abstraction-gradient study.

Subject-matter relevance (kernel facts only):
  universality u(k) = fraction of theorem statements whose direct type refs
    contain concept k (measured stop-words; threshold theta, sensitivity-swept)
  vocab(c) = non-universal concepts in c's own statement (direct type refs
    of kind def/inductive/opaque/quot)
  verdict(c, T):
    bookkeeping  vocab(c) empty            (pure logic vocabulary)
    relevant     some k in vocab(c) lies in A_S(T)  (statement cone)
    alien        vocab nonempty, none in A_S(T)

V5  = V4 moves reordered: relevant (new, depth) > alien > bookkeeping
V5b = V5 + forwarder collapse: a relevant candidate whose own move list has
      exactly one relevant item within depth-2 of itself is a pass-through;
      replace it by that item (container principle, generalized).

Gradient: recursive relevant-move trees for anchor theorems, plus depth-
cutoff slices; layer-coherence stat = fraction of grandchild moves relevant
to the root as well.
"""
import json, os
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP2 = os.path.join(SCRATCH2, "mathlib_deps2.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
SEED = 20260819
NSAMP = 2400
BATCH = 600
THETA = 0.02
CONCEPT_KINDS = ("def", "inductive", "opaque", "quot", "axiom")

TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.", "Batteries.Tactic.")
GEN_MARKS = (".match_", "._simp", "._proof_", "._unary", ".eq_def", ".brecOn",
             ".below", ".ibelow", ".ctorIdx", ".injEq", ".sizeOf_spec", "._eq_",
             ".noConfusion", "._aux", "._f", "._g", ".proof_")

ANCHORS = ["Real.exp_add", "Nat.exists_infinite_primes", "MeasureTheory.integral_add",
           "deriv_add", "Real.exp_log", "Nat.gcd_comm"]


def load():
    idx, names, deps_v, deps_t, kinds, classes, hbs = {}, [], [], [], [], [], []
    def nid(n):
        i = idx.get(n)
        if i is None:
            i = len(names); idx[n] = i; names.append(n)
            deps_v.append(()); deps_t.append(()); kinds.append(""); classes.append(())
            hbs.append(())
        return i
    with open(DUMP2) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]; classes[i] = tuple(r["c"])
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
            hbs[i] = tuple(nid(d) for d in r.get("hb", ()))
    return idx, names, deps_v, deps_t, kinds, classes, hbs


def main():
    idx, names, deps_v, deps_t, kinds, classes, hbs = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
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

    thm = np.array([k == "theorem" for k in kinds])
    has_class = np.array([len(c) > 0 for c in classes])
    is_concept = np.array([k in CONCEPT_KINDS for k in kinds])

    # ---- universality of concepts over theorem statements ----
    cnt = np.zeros(n, dtype=np.int64)
    n_thm = int(thm.sum())
    for i in np.where(thm)[0]:
        for k in set(deps_t[i]):
            cnt[k] += 1
    u = cnt / max(1, n_thm)
    theta_stats = {}
    for th in (0.01, 0.02, 0.05):
        m = is_concept & (u >= th)
        theta_stats[th] = {"n_universal_concepts": int(m.sum()),
                           "examples": [names[i] for i in np.argsort(-u * is_concept)[:8]]}
    print("universality done", flush=True)

    def vocab(c, th=THETA):
        return {k for k in set(deps_t[c])
                if k != c and is_concept[k] and u[k] < th}

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

    def hb_thm_expand(root):
        cur = set(c for c in hbs[root] if c != root)
        for _ in range(4):
            single = {c for c in cur if indeg_v[c] <= 1}
            if not single:
                break
            cur = (cur - single) | {d for c in single for d in hbs[c]
                                    if d != root and d not in single}
        return {c for c in cur if kinds[c] == "theorem"}

    rng = np.random.default_rng(SEED)
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    roots = rng.choice(pool, size=NSAMP, replace=False).tolist()
    anchor_ids = [idx[a] for a in ANCHORS if a in idx]
    # gradient needs cones for anchors' moves and their moves: collect levels
    lvl_roots = set(anchor_ids)
    cand = {}
    for r in list(lvl_roots):
        cand[r] = hb_thm_expand(r)
    l1 = set().union(*[cand[r] for r in anchor_ids]) if anchor_ids else set()
    for c in l1:
        cand.setdefault(c, hb_thm_expand(c))
    l2 = set().union(*[cand[c] for c in l1]) if l1 else set()
    for c in list(l2)[:4000]:
        cand.setdefault(c, hb_thm_expand(c))
    allroots = list(dict.fromkeys(roots + list(anchor_ids) + list(l1) + list(l2)[:4000]))
    for r in allroots:
        cand.setdefault(r, hb_thm_expand(r))
    need = {r: cand[r] | set().union(*[vocab(c) for c in cand[r]]) if cand[r] else set()
            for r in allroots}
    print(f"roots incl gradient levels: {len(allroots)}", flush=True)

    dep_arrays = [np.array(ds, dtype=np.int64) if ds else None for ds in deps]
    rev = list(reversed(order))
    inS = {}
    for b0 in range(0, len(allroots), BATCH):
        batch = allroots[b0:b0 + BATCH]
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
            inS[r] = {c: bool(reach[c, w] & bit) for c in need[r]}
        del reach
        print(f"batch {b0 // BATCH + 1}/{(len(allroots) + BATCH - 1) // BATCH}", flush=True)

    def verdict(c, r):
        vc = vocab(c)
        if not vc:
            return "bookkeeping"
        s = inS[r]
        return "relevant" if any(s.get(k, False) for k in vc) else "alien"

    def rank_v5(r, collapse=False):
        nf = inS[r]
        cands = cand[r]
        vs = {c: verdict(c, r) for c in cands}
        if collapse:
            newc = set()
            for c in cands:
                if vs[c] == "relevant" and c in cand:
                    sub = [m for m in cand.get(c, ()) if verdict(m, c) == "relevant"] \
                        if c in inS else []
                    # cheap forwarder test without sub-cones: single hb-thm ref near own depth
                    subs = [m for m in cand.get(c, set())
                            if depth[m] >= depth[c] - 2 and vocab(m)]
                    if len(subs) == 1 and len(cand.get(c, set())) <= 3:
                        newc.add(subs[0])
                        continue
                newc.add(c)
            cands = newc
            vs = {c: vs.get(c) or verdict(c, r) if c in need[r] else
                  ("relevant" if vocab(c) else "bookkeeping") for c in cands}
        grp = {"relevant": 0, "alien": 1, "bookkeeping": 2}
        return sorted(cands, key=lambda c: (grp[vs[c]],
                                            not (not nf.get(c, False)),
                                            -int(depth[c]))), vs

    # ---- A: metrics V4 vs V5 (V5b measured on category composition only) ----
    res = {}
    strata_depth = []
    comp = {"relevant": {}, "alien": {}, "bookkeeping": {}}
    for r in roots:
        if len(set(deps_v[r]) - {r}) < 3:
            continue
        strata_depth.append(int(depth[r]))
        nf = inS[r]
        for vname in ("V4", "V5"):
            if vname == "V4":
                ranked = sorted(cand[r], key=lambda c: (nf.get(c, False), -int(depth[c])))
                vs = None
            else:
                ranked, vs = rank_v5(r)
            cats = {c: category(c, names[r]) for c in ranked}
            e = res.setdefault(vname, {"fcr": [], "cause": {}, "defn": 0})
            if not ranked:
                e["defn"] += 1
                e["fcr"].append(0)
                continue
            fc = next((k + 1 for k, c in enumerate(ranked) if cats[c] == "content"), 99)
            e["fcr"].append(fc)
            c1 = cats[ranked[0]]
            if c1 != "content":
                e["cause"][c1] = e["cause"].get(c1, 0) + 1
            if vname == "V5":
                for c in ranked:
                    comp[vs[c]][cats[c]] = comp[vs[c]].get(cats[c], 0) + 1
    out = {"seed": SEED, "theta": THETA, "universality": {str(k): v for k, v in theta_stats.items()}}
    sd = np.array(strata_depth)
    terc = np.quantile(sd, [1 / 3, 2 / 3])
    for vname, e in res.items():
        a = np.array(e["fcr"])
        live = a[a > 0]
        s = {"definitional": int((a == 0).sum()),
             "top1_content": round(float((live == 1).mean()), 4),
             "top2_content": round(float((live <= 2).mean()), 4),
             "cause": e["cause"]}
        for lab, lo, hi in (("shallow", -1, terc[0]), ("mid", terc[0], terc[1]),
                            ("deep", terc[1], 1e9)):
            m = (sd > lo) & (sd <= hi) & (a > 0)
            s[f"top1_{lab}"] = round(float((a[m] == 1).mean()), 4)
        out[vname] = s
    out["verdict_x_category"] = comp

    # ---- B: loss check — are human-citable things ever tagged alien/bookkeeping? ----
    rk = json.load(open(os.path.join(DATA, "rankings.json")))
    gt_losses = []
    for d, p in rk["proofs"].items():
        if d not in idx or idx[d] not in cand:
            continue
        r = idx[d]
        route = {c for c, f in p["features"].items()
                 if f["app_head_count"] > 0 and f["prop_result_frac"] > 0.5
                 and not f["p3_classified"] and c in idx}
        for cn in route:
            c = idx[cn]
            if c in cand[r] and c in need[r]:
                v = verdict(c, r)
                if v != "relevant":
                    gt_losses.append({"root": d, "item": cn, "verdict": v})
    out["route_items_demoted"] = {"count": len(gt_losses), "examples": gt_losses[:20]}

    # ---- C: gradient — layered views + coherence ----
    def top_rel(r, k=6):
        ranked, vs = rank_v5(r)
        return [c for c in ranked if vs[c] == "relevant"][:k]

    grad = {}
    coher = []
    for a in ANCHORS:
        if a not in idx:
            continue
        r = idx[a]
        tree = {"decl": a, "depth": int(depth[r]), "levels": []}
        lvl1 = top_rel(r, 6)
        tree["levels"].append([{"name": names[c], "d": int(depth[c])} for c in lvl1])
        lvl2 = []
        for c in lvl1:
            if c in inS:
                subs = top_rel(c, 3)
            else:
                subs = sorted(cand.get(c, set()), key=lambda m: -int(depth[m]))[:3]
            lvl2.append({"parent": names[c],
                         "moves": [{"name": names[m], "d": int(depth[m])} for m in subs]})
            for m in subs:
                if m in need[r]:
                    coher.append(1 if verdict(m, r) == "relevant" else 0)
        tree["levels"].append(lvl2)
        # cutoff slices over the full recursive relevant tree, 2 levels deep
        allm = set(lvl1) | {idx[s["name"]] for e in lvl2 for s in e["moves"]}
        slices = {}
        for frac in (0.8, 0.5, 0.25):
            cut = int(depth[r] * frac)
            slices[f"depth>={cut}"] = sorted(
                [f"{names[m]} (d={int(depth[m])})" for m in allm if depth[m] >= cut])
        tree["cutoff_slices"] = slices
        grad[a] = tree
    out["gradient"] = grad
    out["layer_coherence_frac_grandchildren_relevant_to_root"] = (
        round(float(np.mean(coher)), 3) if coher else None)

    with open(os.path.join(DATA, "relevance_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for k in ("V4", "V5", "verdict_x_category", "route_items_demoted",
              "layer_coherence_frac_grandchildren_relevant_to_root", "universality"):
        v = out[k]
        if isinstance(v, dict):
            v = {kk: vv for kk, vv in v.items() if kk != "examples"}
        print(k, "=", json.dumps(v))


if __name__ == "__main__":
    main()
