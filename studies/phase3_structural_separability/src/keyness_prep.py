#!/usr/bin/env python3
"""Keyness evaluation prep (judge's step 5).

Selects ~26 difficult proofs by STRUCTURAL criteria (no cherry-picking):
from the never-used remainder of the population, stratified by depth
tercile, requiring >=8 proof-term candidates (excludes trivial one-move
proofs), and force-including structural diversity: automation-heavy
(tactic-namespace refs), self-recursive (induction), witness-style
(existential statement), and high-import (many new-to-statement moves).

For each proof emits a brief with FIVE ANONYMIZED VIEWS (labels A-E
shuffled per proof with a recorded keymap):
  moveset   unordered exact move set (V5pzb candidates, alphabetical)
  ranked    V5pzb ranking (bookkeeping-demoted, new-then-depth, zoom)
  applied   candidates ordered by applied-occurrence count (role 0)
  prov      elaborator-resolved human source citations (sidecar)
  zoom      hierarchical: ranked view with single-use nodes expanded inline

Output: review/keyness/brief_<i>.md + keymap.json (never shown to raters).
"""
import json, os, subprocess, sys, re
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP4 = os.path.join(SCRATCH2, "mathlib_deps4.jsonl")
ML_PKG = "/Users/sam/my-repos/research/Map_Of_Mathematics/corpusenv/mathlib"
BIN = "/Users/sam/my-repos/research/Map_Of_Mathematics/mathrecord/.lake/build/bin/mathrecord"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "review", "keyness"))
PROVDIR = os.path.join(SCRATCH2, "prov_key")
SEED = 20260823
NPROOFS = 26
LOAD_ROLES = (0, 1, 2, 7)
TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", "Plausible.", "Qq.")


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
    thm = np.array([k == "theorem" for k in kinds])
    has_class = np.array([len(c) > 0 for c in classes])
    # depth + indeg + topo (standard)
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
    # universality
    CONCEPT_KINDS = ("def", "inductive", "opaque", "quot", "axiom")
    is_concept = np.array([k in CONCEPT_KINDS for k in kinds])
    cnt = np.zeros(n, dtype=np.int64)
    for i in np.where(thm)[0]:
        for c in set(deps_t[i]):
            cnt[c] += 1
    u = cnt / max(1, int(thm.sum()))
    def bookkeeping(c):
        return not any(is_concept[k] and u[k] < 0.02
                       for k in set(deps_t[c]) if k != c)
    print("derived done", flush=True)

    claim = lambda c: pr[c] and kinds[c] not in ("constructor", "recursor")
    def loadbearing(r):
        return {d for d, row in zip(deps_v[r], vo[r])
                if d != r and any(row[k] > 0 for k in LOAD_ROLES)}
    def cands(r):
        return {c for c in loadbearing(r) if claim(c)}
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

    # ---- selection (structural criteria, seed-fixed) ----
    used = set()
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    dev = set(np.random.default_rng(20260819).choice(pool, size=2400, replace=False).tolist())
    p = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260820).choice(p, size=2400, replace=False).tolist())
    p = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260821).choice(p, size=2400, replace=False).tolist())
    p = np.array([i for i in pool if i not in dev])
    dev |= set(np.random.default_rng(20260822).choice(p, size=2400, replace=False).tolist())
    rest = np.array([i for i in pool if i not in dev])
    rng = np.random.default_rng(SEED)
    shuffled = rng.permutation(rest)

    sys.path.insert(0, HERE)
    from moves import build_source_index, decl_block
    print("source index", flush=True)
    sidx = build_source_index()

    def source_of(r):
        short = names[r].split(".")[-1]
        for pth, ln in sidx.get(short, []):
            b = decl_block(pth, ln)
            if b and re.search(r"(theorem|lemma) " + re.escape(short) + r"(?!['\w])",
                               b.splitlines()[0]):
                return pth, b
        return None, None

    def traits(r):
        cs = cands(r)
        vs = set(deps_v[r])
        t = set()
        if any(names[c].startswith(TACTIC_NS) for c in vs):
            t.add("automation")
        if any(indeg_v[c] <= 1 and names[c].startswith(names[r]) for c in vs):
            t.add("self-recursive-or-helper")
        if "Exists" in [names[k].split(".")[0] for k in set(deps_t[r])]:
            t.add("witness")
        return cs, t

    picks, quotas = [], {"shallow": 0, "mid": 0, "deep": 0}
    trait_need = {"automation": 5, "self-recursive-or-helper": 5, "witness": 4}
    dq = np.quantile(depth[pool], [1 / 3, 2 / 3])
    for r in shuffled:
        if len(picks) >= NPROOFS:
            break
        r = int(r)
        cs, t = traits(r)
        if len(cs) < 8:
            continue
        pth, src = source_of(r)
        if src is None or len(src) > 4000:
            continue
        band = "shallow" if depth[r] <= dq[0] else ("mid" if depth[r] <= dq[1] else "deep")
        needed_trait = any(trait_need.get(x, 0) > 0 for x in t)
        if quotas[band] >= NPROOFS // 3 + 2 and not needed_trait:
            continue
        picks.append((r, pth, src, sorted(t)))
        quotas[band] += 1
        for x in t:
            if x in trait_need:
                trait_need[x] -= 1
    print(f"selected {len(picks)}; bands {quotas}; residual trait need {trait_need}", flush=True)

    # provenance for the selected files
    os.makedirs(PROVDIR, exist_ok=True)
    prov = {}
    files = sorted({pth for _, pth, _, _ in picks})
    for k, pth in enumerate(files):
        rel = os.path.relpath(pth, ML_PKG)
        o = os.path.join(PROVDIR, f"p{k}.json")
        if not os.path.exists(o):
            res = subprocess.run(["lake", "env", BIN, "provenance", rel, o],
                                 cwd=ML_PKG, capture_output=True, text=True, timeout=600)
            if res.returncode != 0:
                continue
        try:
            j = json.load(open(o))
            for d in j["decls"]:
                prov[d["name"]] = d["refs"]
        except Exception:
            pass
    print(f"provenance decls: {len(prov)}", flush=True)

    # ---- views ----
    os.makedirs(OUT, exist_ok=True)
    keymap = {}
    VIEWS = ("moveset", "ranked", "applied", "prov", "zoom")
    for pi, (r, pth, src, tr) in enumerate(picks):
        cs = cands(r)
        S = stmt_cone(r)
        nf = {c: c not in S for c in cs}
        key = lambda c: (bookkeeping(c), not nf.get(c, True), -int(depth[c]))
        ranked = sorted(cs, key=key)
        # zoom semantics on rank list
        rk, opened = list(ranked), set()
        for _ in range(8):
            if not rk or indeg_v[rk[0]] > 1 or rk[0] in opened:
                break
            top = rk[0]; opened.add(top)
            inner = {c for c in loadbearing(top) if claim(c) and c != r}
            rk = sorted((set(rk) - {top}) | inner, key=key)
        def render(items, k=10):
            return "\n".join(f"  {j+1}. {names[c]}" for j, c in enumerate(items[:k]))
        views = {}
        views["moveset"] = "\n".join(f"  - {names[c]}" for c in sorted(cs, key=lambda c: names[c])[:14])
        views["ranked"] = render(rk)
        role0 = sorted(cs, key=lambda c: -vo[r][deps_v[r].index(c)][0]
                       if c in deps_v[r] else 0)
        views["applied"] = render(role0)
        pv = prov.get(names[r], {})
        pvs = [cn for cn in sorted(pv, key=lambda x: -pv[x])
               if cn in idx and claim(idx[cn])]
        views["prov"] = "\n".join(f"  {j+1}. {cn}" for j, cn in enumerate(pvs[:10])) or "  (none)"
        zoom_lines = []
        for c in ranked[:6]:
            zoom_lines.append(f"  - {names[c]}")
            if indeg_v[c] <= 1:
                for m in sorted({x for x in loadbearing(c) if claim(x)},
                                key=lambda x: -int(depth[x]))[:4]:
                    zoom_lines.append(f"      . {names[m]}")
        views["zoom"] = "\n".join(zoom_lines)
        perm = rng.permutation(len(VIEWS))
        letters = "ABCDE"
        keymap[f"proof_{pi}"] = {"decl": names[r],
                                 "map": {letters[j]: VIEWS[perm[j]] for j in range(5)},
                                 "traits": tr, "depth": int(depth[r])}
        body = [f"# Proof {pi}", "",
                f"Theorem `{names[r]}` (Mathlib source below).", "",
                "```lean", src, "```", "",
                "## Candidate views (anonymized)"]
        for j in range(5):
            body.append(f"\n### View {letters[j]}\n{views[VIEWS[perm[j]]]}")
        open(os.path.join(OUT, f"brief_{pi}.md"), "w").write("\n".join(body))
    json.dump(keymap, open(os.path.join(OUT, "keymap.json"), "w"), indent=1)
    print(f"wrote {len(picks)} briefs to {OUT}", flush=True)


if __name__ == "__main__":
    main()
