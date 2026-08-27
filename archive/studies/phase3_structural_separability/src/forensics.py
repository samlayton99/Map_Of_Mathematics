#!/usr/bin/env python3
"""Forensics: where does the move ranking break, and why?

Ranking under test: candidates = a theorem's direct proof-term references,
ordered by (new-to-statement first, then global depth desc).

For ~2400 sampled theorems, classify what occupies ranks 1..3:
  content      unclassified human-named theorem/def, not tactic-internal,
               not a compiler byproduct of this very theorem
  self-helper  compiler byproduct of the theorem itself (match_/unary/proof_/
               simp helpers carrying the real proof one level down)
  tactic       automation-internal lemma (omega/grind/linarith/ring/simp cores)
  instance     typeclass instance
  glue         eq-machinery / logic-core / projections / coercions / recursors
  generated    other compiler-generated or internal-detail
Categories are used for DIAGNOSIS only, never inside the ranking.

Key metrics:
  first_content_rank distribution for three ranking variants
    (depth-only; new+depth; new+depth with self-helpers expanded one level)
  broken rate: ranks 1 AND 2 non-content while content exists among candidates
  cause of top-1 when top-1 is non-content; rates by depth tercile and domain.
Selected exemplars are dumped for manual (stage B) reading.
"""
import json, os, re
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
        """Diagnosis category of candidate index c relative to theorem root_name."""
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
        if kinds[c] in ("theorem", "def") or kinds[c] == "opaque":
            return "content"
        return "other"   # inductives, constructors, quot, ...

    # ---- sample ----
    rng = np.random.default_rng(SEED)
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    roots = rng.choice(pool, size=NSAMP, replace=False).tolist()
    print(f"sample: {len(roots)} theorems", flush=True)

    # ---- statement-cone membership per batch (bitmask propagation) ----
    dep_arrays = [np.array(ds, dtype=np.int64) if ds else None for ds in deps]
    rev = list(reversed(order))
    newflag = {}   # root -> {cand_idx: bool}
    for b0 in range(0, len(roots), BATCH):
        batch = roots[b0:b0 + BATCH]
        pos = {r: j for j, r in enumerate(batch)}
        nwords = (len(batch) + 63) // 64
        reach = np.zeros((n, nwords), dtype=np.uint64)
        seeds = {}
        for r in batch:
            tds = np.array(sorted(set(deps_t[r]) - {r}), dtype=np.int64)
            seeds[r] = tds
        for i in rev:
            row = reach[i]
            if row.any():
                ds = dep_arrays[i]
                if ds is not None:
                    reach[ds] |= row
            j = pos.get(i)
            if j is not None and len(seeds[i]):
                w, bit = j >> 6, np.uint64(1) << np.uint64(j & 63)
                rr = np.zeros(nwords, dtype=np.uint64); rr[w] = bit
                reach[seeds[i]] |= rr
        for i in list(cyc) * 2:
            row = reach[i]
            if row.any() and dep_arrays[i] is not None:
                reach[dep_arrays[i]] |= row
        for r in batch:
            j = pos[r]
            w, bit = j >> 6, np.uint64(1) << np.uint64(j & 63)
            cands = [c for c in set(deps_v[r]) if c != r]
            newflag[r] = {c: not bool(reach[c, w] & bit) for c in cands}
        del reach
        print(f"batch {b0 // BATCH + 1}/{(len(roots) + BATCH - 1) // BATCH} done", flush=True)

    # ---- rank + classify ----
    def first_content(ranked, cats):
        for k, c in enumerate(ranked):
            if cats[c] == "content":
                return k + 1
        return None

    variants = ("depth_only", "new_depth", "new_depth_expand")
    fcr = {v: [] for v in variants}          # first content rank (None -> 99)
    broken = {v: 0 for v in variants}
    denom_broken = 0
    top1_cause = {v: {} for v in variants}
    strata = []
    records = []
    for r in roots:
        cands = [c for c in set(deps_v[r]) if c != r]
        if len(cands) < 3:
            continue
        cats = {c: category(c, names[r]) for c in cands}
        has_content = any(v == "content" for v in cats.values())
        nf = newflag[r]
        rank_d = sorted(cands, key=lambda c: -int(depth[c]))
        rank_nd = sorted(cands, key=lambda c: (not nf[c], -int(depth[c])))
        # expand variant: replace each top self-helper by its own deps (one level)
        expanded = []
        seen = set()
        for c in rank_nd:
            if cats[c] == "self-helper":
                for d in sorted(set(deps[c]), key=lambda x: -int(depth[x])):
                    if d not in seen and d != r:
                        expanded.append(d); seen.add(d)
            elif c not in seen:
                expanded.append(c); seen.add(c)
        cats_x = dict(cats)
        for c in expanded:
            if c not in cats_x:
                cats_x[c] = category(c, names[r])
        rank_x = sorted(expanded, key=lambda c: (not nf.get(c, True), -int(depth[c])))
        has_content_x = has_content or any(cats_x[c] == "content" for c in rank_x)

        row = {"decl": names[r], "depth": int(depth[r]), "n_cands": len(cands),
               "domain": names[r].split(".")[0]}
        for v, ranked, cc, hc in (("depth_only", rank_d, cats, has_content),
                                  ("new_depth", rank_nd, cats, has_content),
                                  ("new_depth_expand", rank_x, cats_x, has_content_x)):
            f = first_content(ranked, cc)
            fcr[v].append(f if f else 99)
            row[v + "_fcr"] = f
            if hc:
                if v == "new_depth":
                    denom_broken += 1
                if f is None or f > 2:
                    broken[v] += 1
                c1 = cc[ranked[0]]
                if c1 != "content":
                    top1_cause[v][c1] = top1_cause[v].get(c1, 0) + 1
        row["top8"] = [{"name": names[c], "cat": cats[c], "d": int(depth[c]),
                        "new": bool(nf[c])} for c in rank_nd[:8]]
        strata.append(row)

    m = len(strata)
    print(f"analyzed {m} theorems", flush=True)
    out = {"n_analyzed": m, "seed": SEED}

    def dist(v):
        a = np.array(fcr[v])
        return {"rank1": round(float((a == 1).mean()), 4),
                "rank2": round(float((a == 2).mean()), 4),
                "rank3": round(float((a == 3).mean()), 4),
                "rank4plus": round(float(((a > 3) & (a < 99)).mean()), 4),
                "no_content_in_cands": round(float((a == 99).mean()), 4)}
    out["first_content_rank"] = {v: dist(v) for v in variants}
    out["broken_rate_top2_noncontent"] = {
        v: round(broken[v] / max(1, denom_broken), 4) for v in variants}
    out["top1_cause_when_noncontent"] = top1_cause

    # by depth tercile and domain (new_depth variant)
    dths = np.array([r["depth"] for r in strata])
    terc = np.quantile(dths, [1 / 3, 2 / 3])
    by_terc = {}
    for lab, lo, hi in (("shallow", -1, terc[0]), ("mid", terc[0], terc[1]),
                        ("deep", terc[1], 1e9)):
        sel = [r for r in strata if lo < r["depth"] <= hi]
        f = np.array([r["new_depth_fcr"] or 99 for r in sel])
        by_terc[lab] = {"n": len(sel), "top1_content": round(float((f == 1).mean()), 3),
                        "top2_content": round(float((f <= 2).mean()), 3),
                        "depth_range": [int(min(r['depth'] for r in sel)),
                                        int(max(r['depth'] for r in sel))]}
    out["by_depth_tercile"] = by_terc
    from collections import Counter
    domc = Counter(r["domain"] for r in strata)
    by_dom = {}
    for dom, cnt in domc.most_common(14):
        sel = [r for r in strata if r["domain"] == dom]
        f = np.array([r["new_depth_fcr"] or 99 for r in sel])
        by_dom[dom] = {"n": cnt, "top1_content": round(float((f == 1).mean()), 3),
                       "top2_content": round(float((f <= 2).mean()), 3)}
    out["by_domain"] = by_dom

    # ---- exemplars for stage-B manual reading ----
    rng2 = np.random.default_rng(SEED + 1)
    broken_rows = [r for r in strata if (r["new_depth_fcr"] or 99) > 2]
    clean_rows = [r for r in strata if r["new_depth_fcr"] == 1]
    causes = {}
    for r in broken_rows:
        causes.setdefault(r["top8"][0]["cat"], []).append(r)
    ex = []
    for cat, rows in causes.items():
        take = rng2.choice(len(rows), size=min(8, len(rows)), replace=False)
        ex += [rows[int(t)] for t in take]
    take = rng2.choice(len(clean_rows), size=min(15, len(clean_rows)), replace=False)
    ex += [clean_rows[int(t)] for t in take]
    out["exemplars"] = ex
    out["exemplar_counts"] = {c: len(v) for c, v in causes.items()}

    with open(os.path.join(DATA, "forensics_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for k in ("first_content_rank", "broken_rate_top2_noncontent",
              "top1_cause_when_noncontent", "by_depth_tercile", "by_domain",
              "exemplar_counts"):
        print(k, "=", json.dumps(out[k]))


if __name__ == "__main__":
    main()
