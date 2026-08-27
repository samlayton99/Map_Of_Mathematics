#!/usr/bin/env python3
"""Literal 100% accounting of glue in top-10 move lists, plus the
precision/recall funnel.

For every glue-category item appearing in a V5v top-10, assign it to exactly
one cell of an EXHAUSTIVE partition (the cells cover all combinations by
construction, so the residual is zero by design — the point is to see the
sizes and read named examples from every cell):

  T   tail: appears BELOW the first content item (benign by position)
  V   would-be-verdict leakage: list has no content and all items are
      bookkeeping (should be a holds-by-definition verdict; V5v issues the
      verdict at evaluation time, listed here if any slip through)
  A1  above content, NON-bookkeeping glue, new-to-statement
      (rare-vocabulary glue elevated by the new-first rule)
  A2  above content, NON-bookkeeping glue, in-statement-cone
      (elevated purely by depth)
  A3  above content, bookkeeping glue (can only happen when the content
      itself is also bookkeeping-tagged, since demotion sorts groups)
  N1  no content anywhere in list, NON-bookkeeping glue present
      (interface-only proofs: the 'moves' are projection/cast lemmas)
  N2  no content anywhere, item is bookkeeping but list is NOT all-
      bookkeeping (mixed with non-claim/other items)

Per cell: count, share, top named constants, P3 class distribution.
Two independent samples (seeds 20260826, 20260827) to show stability.

Funnel (per theorem, averaged): raw value refs -> load-bearing occurrence
roles -> claims filter -> verdicts -> top-10 composition by category; plus
counts of what each stage removes, by category.
"""
import json, os
import numpy as np
from collections import Counter

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP4 = os.path.join(SCRATCH2, "mathlib_deps4.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
LOAD_ROLES = (0, 1, 2, 7)
NSAMP = 1500
GLUE = {"eq-machinery", "logic-core", "structure-projection", "coercion", "recursor"}
TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.", "Batteries.Tactic.")
GEN_MARKS = (".match_", "._simp", "._proof_", "._unary", ".eq_def", ".brecOn",
             ".below", ".ibelow", ".ctorIdx", ".injEq", ".sizeOf_spec", "._eq_",
             ".noConfusion", "._aux", "._f", "._g", ".proof_")


def main():
    idx, names = {}, []
    kinds, classes, pr, deps_v, deps_t, vo = [], [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            kinds.append(""); classes.append(()); pr.append(False)
            deps_v.append(()); deps_t.append(()); vo.append(())
        return i
    with open(DUMP4) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]; classes[i] = tuple(r["c"]); pr[i] = bool(r.get("pr", False))
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
            vo[i] = tuple(tuple(int(x) for x in row) for row in r.get("vo", ()))
    n = len(names)
    print(f"constants: {n}", flush=True)
    pr = np.array(pr)
    thm = np.array([k == "theorem" for k in kinds])
    has_class = np.array([len(c) > 0 for c in classes])
    deps = [tuple(set(dv if dv else dt) - {i})
            for i, (dv, dt) in enumerate(zip(deps_v, deps_t))]
    indeg = np.zeros(n, dtype=np.int32)
    users = [[] for _ in range(n)]
    for i, ds in enumerate(deps):
        indeg[i] = len(ds)
        for d in ds:
            users[d].append(i)
    from collections import deque
    q = deque(np.where(indeg == 0)[0].tolist())
    order = []
    while q:
        i = q.popleft(); order.append(i)
        for u2 in users[i]:
            indeg[u2] -= 1
            if indeg[u2] == 0:
                q.append(u2)
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
    CONCEPT_KINDS = ("def", "inductive", "opaque", "quot", "axiom")
    is_concept = np.array([k in CONCEPT_KINDS for k in kinds])
    cnt = np.zeros(n, dtype=np.int64)
    for i in np.where(thm)[0]:
        for c in set(deps_t[i]):
            cnt[c] += 1
    univ = cnt / max(1, int(thm.sum()))
    def bookkeeping(c):
        return not any(is_concept[k] and univ[k] < 0.02
                       for k in set(deps_t[c]) if k != c)
    print("derived done", flush=True)

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
        if any(x in cl for x in GLUE):
            return "glue"
        if any(x in cl for x in ("generated", "internal-detail")):
            return "generated"
        if kinds[c] in ("theorem", "def", "opaque"):
            return "content"
        return "other"

    claim = lambda c: pr[c] and kinds[c] not in ("constructor", "recursor")
    def role_sets(r):
        lb, dropped_bg = set(), set()
        for d, row in zip(deps_v[r], vo[r]):
            if d == r:
                continue
            if any(row[k] > 0 for k in LOAD_ROLES):
                lb.add(d)
            else:
                dropped_bg.add(d)
        return lb, dropped_bg
    def stmt_cone(root):
        seen = set()
        stack = [d for d in set(deps_t[root]) if d != root]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(d for d in deps[x] if d not in seen)
        return seen

    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    out = {}
    for seed in (20260826, 20260827):
        roots = np.random.default_rng(seed).choice(pool, size=NSAMP, replace=False).tolist()
        cells = Counter()
        cellnames = {k: Counter() for k in ("T", "V", "A1", "A2", "A3", "N1", "N2")}
        cellcls = {k: Counter() for k in cellnames}
        funnel = Counter()
        top10comp = Counter()
        slots = 0
        n_scored = n_verdict = 0
        for r in roots:
            if len(set(deps_v[r]) - {r}) < 3:
                continue
            lb, dropped_bg = role_sets(r)
            cs = {c for c in lb if claim(c)}
            dropped_claims = lb - cs
            funnel["raw_refs"] += len(set(deps_v[r]) - {r})
            funnel["load_bearing"] += len(lb)
            funnel["claims"] += len(cs)
            for d in dropped_bg:
                funnel[f"bgdrop_{category(d, names[r])}"] += 1
            for d in dropped_claims:
                funnel[f"claimdrop_{category(d, names[r])}"] += 1
            if cs and all(bookkeeping(c) for c in cs):
                n_verdict += 1
                funnel["verdict_by_definition"] += 1
                continue
            if not cs:
                n_verdict += 1
                funnel["verdict_empty"] += 1
                continue
            n_scored += 1
            S = stmt_cone(r)
            key = lambda c: (bookkeeping(c), c in S, -int(depth[c]))
            ranked = sorted(cs, key=key)[:10]
            cats = [category(c, names[r]) for c in ranked]
            for cc in cats:
                top10comp[cc] += 1
            slots += len(ranked)
            fc = next((k for k, cc in enumerate(cats) if cc == "content"), None)
            for p, (c, cc) in enumerate(zip(ranked, cats)):
                if cc != "glue":
                    continue
                bk = bookkeeping(c)
                if fc is not None and p > fc:
                    cell = "T"
                elif fc is not None:
                    if not bk:
                        cell = "A1" if c not in S else "A2"
                    else:
                        cell = "A3"
                else:
                    if not bk:
                        cell = "N1"
                    else:
                        cell = "V" if all(bookkeeping(x) for x in ranked) else "N2"
                cells[cell] += 1
                cellnames[cell][names[c]] += 1
                cellcls[cell][next(x for x in classes[c] if x in GLUE)] += 1
        total_glue = sum(cells.values())
        out[str(seed)] = {
            "n_scored": n_scored, "n_verdict": n_verdict,
            "top10_slots": slots,
            "top10_composition": dict(top10comp),
            "glue_in_top10_total": total_glue,
            "glue_share_of_slots": round(total_glue / max(1, slots), 4),
            "cells": dict(cells),
            "residual_unaccounted": total_glue - sum(cells.values()),
            "cell_top_constants": {k: v.most_common(8) for k, v in cellnames.items()},
            "cell_class_mix": {k: dict(v) for k, v in cellcls.items()},
            "funnel_totals": dict(funnel)}
        print(seed, "cells:", dict(cells), "residual:",
              total_glue - sum(cells.values()), flush=True)
    with open(os.path.join(DATA, "glue_accounting.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("written", flush=True)


if __name__ == "__main__":
    main()
