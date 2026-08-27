#!/usr/bin/env python3
"""Evaluate the position-aware move definition (V4) at library scale.

V4 move list for theorem T:
  candidates = load-bearing head refs of T (dump field `hb`) of kind theorem,
  with single-use refs inlined (replaced by their own hb-theorem refs, <=4
  rounds), ranked by (new-to-statement, then depth).

Evaluations:
  A. precision proxy on the standard 2400-root sample: top-1/top-2 content
     rates and failure causes; compare with V3 (prop_inlined, position-blind).
  B. recall vs human source text: identifiers written in the Lean proof
     source (rw [foo], exact bar) that resolve to library theorems = ground
     truth; measure fraction recovered by the move list, and diagnose losses.
  C. loss accounting: content that V3 surfaced but V4 drops; route-view
     coverage on the 20 ground-truth proofs.
  D. vibe dump: ranked moves for anchor theorems across the depth range.
"""
import json, os, re
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP2 = os.path.join(SCRATCH2, "mathlib_deps2.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
ML = "/Users/sam/my-repos/research/Map_Of_Mathematics/corpusenv/mathlib/Mathlib"
SEED = 20260819
NSAMP = 2400
BATCH = 600

TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.", "Batteries.Tactic.")
GEN_MARKS = (".match_", "._simp", "._proof_", "._unary", ".eq_def", ".brecOn",
             ".below", ".ibelow", ".ctorIdx", ".injEq", ".sizeOf_spec", "._eq_",
             ".noConfusion", "._aux", "._f", "._g", ".proof_")

ANCHORS = ["Real.exp_log", "Real.exp_add", "Nat.gcd_comm", "Nat.exists_infinite_primes",
           "abs_add", "dist_triangle", "deriv_add", "MeasureTheory.integral_add",
           "Filter.Tendsto.add", "inner_mul_le_norm_mul_norm", "Real.add_comm",
           "Nat.sqrt_lt", "List.length_append", "Finset.sum_comm",
           "Continuous.comp", "IsCompact.exists_forall_ge"]


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


def build_source_index():
    """shortname -> (path, line) for theorem/lemma declarations in Mathlib."""
    pat = re.compile(r"^(?:@\[[^\]]*\] )?(?:protected |private |nonrec |noncomputable )*"
                     r"(?:theorem|lemma) ([A-Za-z0-9_'.₀-₉ʹᵃ-ᵣ]+)")
    index = {}
    for root, _dirs, files in os.walk(ML):
        for fn in files:
            if not fn.endswith(".lean"):
                continue
            p = os.path.join(root, fn)
            try:
                for ln, line in enumerate(open(p, encoding="utf-8"), 1):
                    m = pat.match(line)
                    if m:
                        index.setdefault(m.group(1), []).append((p, ln))
            except OSError:
                pass
    return index


def decl_block(path, line0):
    lines = open(path, encoding="utf-8").read().splitlines()
    stop = re.compile(r"^(@\[|/--|(protected |private |nonrec |noncomputable )*"
                      r"(theorem|lemma|def|instance|abbrev|structure|class|inductive)\b"
                      r"|end\b|section\b|namespace\b|variable|open |attribute |alias |#)")
    e = line0
    while e < len(lines):
        if e > line0 and lines[e - 1].strip() == "" and stop.match(lines[e]):
            break
        e += 1
    return "\n".join(lines[line0 - 1:e])


IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_'.₀-₉]*")


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

    def hb_thm_expand(root):
        """V4 candidates: hb refs of kind theorem, single-use inlined."""
        cur = set(c for c in hbs[root] if c != root)
        for _ in range(4):
            single = {c for c in cur if indeg_v[c] <= 1}
            if not single:
                break
            cur = (cur - single) | {d for c in single for d in hbs[c]
                                    if d != root and d not in single}
        return {c for c in cur if kinds[c] == "theorem"}

    def v3_expand(root):
        cur = set(d for d in deps_v[root] if d != root)
        for _ in range(4):
            single = {c for c in cur if indeg_v[c] <= 1}
            if not single:
                break
            cur = (cur - single) | {d for c in single
                                    for d in (deps_v[c] if deps_v[c] else deps_t[c])
                                    if d != root and d not in single}
        return {c for c in cur if kinds[c] == "theorem"}

    rng = np.random.default_rng(SEED)
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    roots = rng.choice(pool, size=NSAMP, replace=False).tolist()
    anchor_ids = [idx[a] for a in ANCHORS if a in idx]
    rk = json.load(open(os.path.join(DATA, "rankings.json")))
    gt20 = [idx[d] for d in rk["proofs"] if d in idx]
    allroots = list(dict.fromkeys(roots + anchor_ids + gt20))

    cand4 = {r: hb_thm_expand(r) for r in allroots}
    cand3 = {r: v3_expand(r) for r in allroots}
    need = {r: cand3[r] | cand4[r] for r in allroots}
    print("candidates built", flush=True)

    dep_arrays = [np.array(ds, dtype=np.int64) if ds else None for ds in deps]
    rev = list(reversed(order))
    newflag = {}
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
            newflag[r] = {c: not bool(reach[c, w] & bit) for c in need[r]}
        del reach
        print(f"batch {b0 // BATCH + 1}", flush=True)

    def ranked(r, cands):
        nf = newflag[r]
        return sorted(cands, key=lambda c: (not nf[c], -int(depth[c])))

    # ---- A: precision proxy on the sample ----
    out = {"seed": SEED}
    res = {}
    strata_depth = []
    lost_content = []          # C: content in V3 top-3 dropped by V4
    for r in roots:
        if len(set(deps_v[r]) - {r}) < 3:
            continue
        strata_depth.append(int(depth[r]))
        for vname, cands in (("V3", cand3[r]), ("V4", cand4[r])):
            rk_ = ranked(r, cands)
            cats = {c: category(c, names[r]) for c in rk_}
            e = res.setdefault(vname, {"fcr": [], "cause": {}, "defn": 0})
            if not rk_:
                e["defn"] += 1
                e["fcr"].append(0)
                continue
            fc = next((k + 1 for k, c in enumerate(rk_) if cats[c] == "content"), 99)
            e["fcr"].append(fc)
            c1 = cats[rk_[0]]
            if c1 != "content":
                e["cause"][c1] = e["cause"].get(c1, 0) + 1
        # C: content dropped
        r3 = ranked(r, cand3[r])
        for c in r3[:3]:
            if category(c, names[r]) == "content" and c not in cand4[r]:
                lost_content.append({"root": names[r], "dropped": names[c],
                                     "d": int(depth[c]),
                                     "in_hb": c in set(hbs[r])})
    sd = np.array(strata_depth)
    terc = np.quantile(sd, [1 / 3, 2 / 3])
    for vname, e in res.items():
        a = np.array(e["fcr"])
        live = a[a > 0]
        s = {"definitional": int((a == 0).sum()),
             "top1_content": round(float((live == 1).mean()), 4),
             "top2_content": round(float((live <= 2).mean()), 4),
             "no_content": round(float((live == 99).mean()), 4),
             "cause": e["cause"]}
        for lab, lo, hi in (("shallow", -1, terc[0]), ("mid", terc[0], terc[1]),
                            ("deep", terc[1], 1e9)):
            m = (sd > lo) & (sd <= hi) & (a > 0)
            s[f"top1_{lab}"] = round(float((a[m] == 1).mean()), 4)
        out[vname] = s
    out["C_content_dropped_by_V4"] = {
        "count": len(lost_content), "per_theorem": round(len(lost_content) / max(1, len(sd)), 4),
        "examples": lost_content[:25]}

    # ---- B: recall vs human source text ----
    print("building source index", flush=True)
    sidx = build_source_index()
    rng3 = np.random.default_rng(SEED + 3)
    rec_sample = [int(x) for x in rng3.choice(roots, size=600, replace=False)]
    recalls, losses, evaluated = [], [], 0
    for r in rec_sample:
        short = names[r].split(".")[-1]
        hits = [h for h in sidx.get(short, [])]
        block = None
        for p, ln in hits:
            b = decl_block(p, ln)
            first = b.splitlines()[0] if b else ""
            if re.search(r"(theorem|lemma) " + re.escape(names[r].split(".")[-1]) + r"(?!['\w])", b.splitlines()[0]):
                block = b
                break
        if block is None or ":=" not in block and " by" not in block:
            continue
        m = re.search(r":=", block)
        body = block[m.end():] if m else block
        toks = set(IDENT.findall(body))
        refs = set(deps_v[r])
        # resolve source tokens to referenced theorems
        gt = set()
        for c in refs:
            if kinds[c] != "theorem" or c == r:
                continue
            nm = names[c]
            if nm in toks or nm.split(".")[-1] in toks:
                if category(c, names[r]) in ("content", "glue"):
                    gt.add(c)
        if len(gt) < 2:
            continue
        evaluated += 1
        moves = cand4[r]
        got = gt & moves
        recalls.append(len(got) / len(gt))
        for c in gt - moves:
            losses.append({"root": names[r], "lost": names[c],
                           "cat": category(c, names[r]),
                           "why": "not-load-bearing" if c not in set(hbs[r])
                                  else "excluded-other"})
    out["B_source_recall"] = {
        "n_evaluated": evaluated,
        "median_recall": round(float(np.median(recalls)), 3) if recalls else None,
        "mean_recall": round(float(np.mean(recalls)), 3) if recalls else None,
        "frac_perfect": round(float(np.mean([x == 1 for x in recalls])), 3) if recalls else None,
        "n_losses": len(losses),
        "loss_examples": losses[:30]}

    # ---- C2: route coverage on the 20 ground-truth proofs ----
    cov = []
    for d, p in rk["proofs"].items():
        if d not in idx or idx[d] not in cand4:
            continue
        r = idx[d]
        route = {c for c, f in p["features"].items()
                 if f["app_head_count"] > 0 and f["prop_result_frac"] > 0.5
                 and not f["p3_classified"] and c in idx}
        rt = {idx[c] for c in route}
        if not rt:
            continue
        cov.append({"decl": d, "route_n": len(rt),
                    "covered": len(rt & cand4[r]) / len(rt)})
    out["C2_route_coverage_20"] = {
        "median": round(float(np.median([c["covered"] for c in cov])), 3),
        "per_proof": cov}

    # ---- D: vibe dump ----
    vibe = {}
    for a in ANCHORS:
        if a not in idx:
            continue
        r = idx[a]
        rk_ = ranked(r, cand4[r])
        cats = {c: category(c, names[r]) for c in rk_}
        vibe[a] = {"depth": int(depth[r]), "n_moves": len(rk_),
                   "top10": [{"name": names[c], "cat": cats[c], "d": int(depth[c]),
                              "new": bool(newflag[r][c])} for c in rk_[:10]]}
    out["D_vibe"] = vibe

    with open(os.path.join(DATA, "moves_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for k in ("V3", "V4", "C_content_dropped_by_V4", "B_source_recall",
              "C2_route_coverage_20"):
        v = dict(out[k])
        v.pop("examples", None); v.pop("loss_examples", None); v.pop("per_proof", None)
        print(k, "=", json.dumps(v))


if __name__ == "__main__":
    main()
