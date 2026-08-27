#!/usr/bin/env python3
"""Proof-strategy detection from kernel signatures (no tactic names).

Signatures (all from load-bearing heads `hb` + structure):
  contradiction   eliminator of False / absurd / byContradiction applied
  choice          Classical.choice / choose / epsilon applied
  contrapositive  modus tollens (mt / not_imp_not) applied
  extensionality  funext / propext / Quot.sound applied
  computation     of_decide_eq_true applied (proof by kernel evaluation)
  case_split      eliminator of an inductive with >=2 constructors applied;
                  the constructor count is derived structurally: the
                  recursor's TYPE mentions exactly the inductive's
                  constructors (kind=constructor)
  induction       the proof cites itself, or a single-use private dep that
                  cites itself/the proof (structural recursion), or applies
                  WellFounded.fix

Validation: source-text tactics (by_contra, induction, rcases, contrapose,
choose, decide) as imperfect ground truth on proofs whose source is found.
Large-scale: strategy rates overall / by depth tercile / by domain.
"""
import json, os, re
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP2 = os.path.join(SCRATCH2, "mathlib_deps2.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
SEED = 20260819

CORE = {
    "contradiction": ["False.elim", "False.rec", "absurd", "Not.elim",
                      "Classical.byContradiction", "Decidable.byContradiction"],
    "choice": ["Classical.choice", "Classical.choose", "Classical.choose_spec",
               "Classical.epsilon", "Classical.indefiniteDescription",
               "Exists.choose", "Exists.choose_spec"],
    "contrapositive": ["mt", "not_imp_not", "Not.imp"],
    "extensionality": ["funext", "propext", "Quot.sound", "Quotient.sound"],
    "computation": ["of_decide_eq_true", "of_decide_eq_false", "eq_true_of_decide"],
    "wf_induction": ["WellFounded.fix", "WellFounded.fixF", "WellFounded.recursion"],
}

SRC_PAT = {
    "contradiction": re.compile(r"\b(by_contra|contradiction|absurd|exfalso)\b"),
    "choice": re.compile(r"\b(choose|Classical\.choice|Exists\.choose)\b"),
    "contrapositive": re.compile(r"\b(contrapose|mt)\b"),
    "extensionality": re.compile(r"\b(ext|funext)\b"),
    "computation": re.compile(r"\b(decide|native_decide)\b"),
    "case_split": re.compile(r"\b(rcases|cases|obtain|rintro|match|split|by_cases|induction)\b"),
    "induction": re.compile(r"\b(induction|fun_induction|Nat\.rec|strong_induction)\b"),
}


def load():
    idx, names, deps_v, deps_t, kinds, hbs = {}, [], [], [], [], []
    def nid(n):
        i = idx.get(n)
        if i is None:
            i = len(names); idx[n] = i; names.append(n)
            deps_v.append(()); deps_t.append(()); kinds.append(""); hbs.append(())
        return i
    with open(DUMP2) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
            hbs[i] = tuple(nid(d) for d in r.get("hb", ()))
    return idx, names, deps_v, deps_t, kinds, hbs


def main():
    idx, names, deps_v, deps_t, kinds, hbs = load()
    n = len(names)
    print(f"constants: {n}", flush=True)
    thm = np.array([k == "theorem" for k in kinds])
    is_ctor = np.array([k == "constructor" for k in kinds])
    is_rec = np.array([k == "recursor" for k in kinds])

    indeg_v = np.zeros(n, dtype=np.int64)
    for i, ds in enumerate(deps_v):
        for d in set(ds):
            if d != i:
                indeg_v[d] += 1

    # multi-constructor eliminators: recursor whose TYPE mentions >=2 ctors,
    # plus small def wrappers whose hb is exactly such recursors (casesOn/elim)
    multi_rec = set()
    for i in np.where(is_rec)[0]:
        nc = sum(1 for d in set(deps_t[i]) if is_ctor[d])
        if nc >= 2:
            multi_rec.add(i)
    elim = set(multi_rec)
    for i in range(n):
        if kinds[i] == "def" and hbs[i]:
            hs = set(hbs[i])
            if hs and hs <= multi_rec:
                elim.add(i)
    print(f"multi-ctor recursors: {len(multi_rec)}, eliminator set: {len(elim)}", flush=True)

    core_ids = {k: {idx[x] for x in v if x in idx} for k, v in CORE.items()}
    self_rec = np.zeros(n, dtype=bool)
    for i in range(n):
        if i in set(deps_v[i]):
            self_rec[i] = True

    def tags(r):
        hs = set(hbs[r])
        t = set()
        for k, ids in core_ids.items():
            if hs & ids:
                t.add("induction" if k == "wf_induction" else k)
        if hs & elim:
            t.add("case_split")
        if self_rec[r]:
            t.add("induction")
        else:
            for d in set(deps_v[r]):
                if indeg_v[d] <= 1 and d != r and (self_rec[d] or r in set(deps_v[d])):
                    t.add("induction")
                    break
        return t

    # ---- large-scale distribution ----
    depth_proxy = None
    # cheap depth: reuse ordering not needed; use logsize proxy? compute depth properly
    indeg = np.zeros(n, dtype=np.int32)
    users = [[] for _ in range(n)]
    deps = [dv if dv else dt for dv, dt in zip(deps_v, deps_t)]
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
    del users
    print("depth done", flush=True)

    pool = np.where(thm & np.array([len(v) > 0 for v in deps_v]))[0]
    rng = np.random.default_rng(SEED)
    samp = rng.choice(pool, size=40000, replace=False)
    all_tags = {int(r): tags(int(r)) for r in samp}
    from collections import Counter
    rate = Counter(t for ts in all_tags.values() for t in ts)
    out = {"n_sampled_theorems": len(samp),
           "strategy_rates": {k: round(v / len(samp), 4) for k, v in rate.most_common()}}
    d_arr = np.array([depth[r] for r in samp])
    terc = np.quantile(d_arr, [1 / 3, 2 / 3])
    bydepth = {}
    for lab, lo, hi in (("shallow", -1, terc[0]), ("mid", terc[0], terc[1]),
                        ("deep", terc[1], 1e9)):
        sel = [r for r in samp if lo < depth[r] <= hi]
        c = Counter(t for r in sel for t in all_tags[int(r)])
        bydepth[lab] = {k: round(v / len(sel), 4) for k, v in c.most_common(8)}
    out["by_depth_tercile"] = bydepth
    dom = {}
    for r in samp:
        d0 = names[int(r)].split(".")[0]
        dom.setdefault(d0, []).append(int(r))
    bydom = {}
    for d0, rs in sorted(dom.items(), key=lambda kv: -len(kv[1]))[:12]:
        c = Counter(t for r in rs for t in all_tags[r])
        bydom[d0] = {"n": len(rs), **{k: round(v / len(rs), 3) for k, v in c.most_common(5)}}
    out["by_domain"] = bydom

    # ---- validation vs source text ----
    import sys
    sys.path.insert(0, HERE)
    from moves import build_source_index, decl_block
    print("building source index", flush=True)
    sidx = build_source_index()
    val_samp = rng.choice(samp, size=3000, replace=False)
    stats = {k: {"tp": 0, "fp": 0, "fn": 0, "tn": 0} for k in SRC_PAT}
    fp_ex, fn_ex = {k: [] for k in SRC_PAT}, {k: [] for k in SRC_PAT}
    evaluated = 0
    for r in val_samp:
        r = int(r)
        short = names[r].split(".")[-1]
        block = None
        for p, ln in sidx.get(short, []):
            b = decl_block(p, ln)
            if b and re.search(r"(theorem|lemma) " + re.escape(short) + r"(?!['\w])",
                               b.splitlines()[0]):
                block = b
                break
        if block is None:
            continue
        m = re.search(r":=", block)
        body = block[m.end():] if m else block
        evaluated += 1
        ts = all_tags[r]
        for k, pat in SRC_PAT.items():
            src = bool(pat.search(body))
            kt = "case_split" if k == "case_split" else k
            got = kt in ts
            if got and src:
                stats[k]["tp"] += 1
            elif got and not src:
                stats[k]["fp"] += 1
                if len(fp_ex[k]) < 5:
                    fp_ex[k].append(names[r])
            elif not got and src:
                stats[k]["fn"] += 1
                if len(fn_ex[k]) < 5:
                    fn_ex[k].append(names[r])
            else:
                stats[k]["tn"] += 1
    val = {}
    for k, s in stats.items():
        prec = s["tp"] / max(1, s["tp"] + s["fp"])
        rec = s["tp"] / max(1, s["tp"] + s["fn"])
        val[k] = {"precision_vs_source": round(prec, 3), "recall_vs_source": round(rec, 3),
                  **s, "fp_examples": fp_ex[k], "fn_examples": fn_ex[k]}
    out["validation_n"] = evaluated
    out["validation"] = val

    # anchors for the vibe
    vibe = {}
    for a in ("Nat.exists_infinite_primes", "Real.exp_log", "Nat.gcd_comm",
              "zpow_mul", "Nat.pow_sub_one_gcd_pow_sub_one", "Real.range_log",
              "limUnder_of_not_tendsto", "Function.Injective.isPartialInv"):
        if a in idx:
            vibe[a] = sorted(tags(idx[a]))
    out["anchor_strategies"] = vibe

    with open(os.path.join(DATA, "strategies_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for k in ("strategy_rates", "by_depth_tercile", "validation_n", "anchor_strategies"):
        print(k, "=", json.dumps(out[k]))
    print("validation =", json.dumps({k: {x: v[x] for x in
          ("precision_vs_source", "recall_vs_source", "tp", "fp", "fn")}
          for k, v in val.items()}))


if __name__ == "__main__":
    main()
