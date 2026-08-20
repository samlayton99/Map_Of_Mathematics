#!/usr/bin/env python3
"""Proof-strategy detection v2 — root-grain.

v1 failure diagnosis (data/strategies_results.json): set-membership anywhere
in the term fires on compiler/automation internals (contradiction precision
0.095) and misses recursion hidden in single-use helpers (induction recall 0).

v2: a strategy is the OUTERMOST shape of the proof term. Uses the new dump
fields:
  rt  root head chain (peel binders, take head const, descend into the last
      explicit argument, <= 5 layers)
  ir  inductive-is-recursive flag (kernel fact from InductiveVal.isRec)
Chains are spliced through single-use containers (the theorem's own compiled
helpers), same container principle as ranking.

Signatures on the effective chain:
  contradiction   False.elim / absurd / byContradiction
  choice          Classical.choice / choose / epsilon
  contrapositive  mt / not_imp_not
  extensionality  funext / propext / Quot.sound
  computation     of_decide_eq_true
  induction       WellFounded.fix, or a recursor (or wrapper) of a RECURSIVE
                  inductive
  case_split      an eliminator (or wrapper) of a multi-constructor inductive
Validation vs source-text tactics as in v1.
"""
import json, os, re, sys
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP3 = os.path.join(SCRATCH2, "mathlib_deps3.jsonl")
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
    "wf": ["WellFounded.fix", "WellFounded.fixF", "WellFounded.recursion"],
}

SRC_PAT = {
    "contradiction": re.compile(r"\b(by_contra|contradiction|absurd|exfalso)\b"),
    "choice": re.compile(r"\b(choose|Classical\.choice|Exists\.choose)\b"),
    "contrapositive": re.compile(r"\b(contrapose|mt)\b"),
    "extensionality": re.compile(r"\b(ext|funext)\b"),
    "computation": re.compile(r"\b(decide|native_decide)\b"),
    "case_split": re.compile(r"\b(rcases|cases|obtain|rintro|match|split|by_cases)\b"),
    "induction": re.compile(r"\b(induction|fun_induction|strong_induction|Nat\.rec)\b"),
}


def main():
    idx, names = {}, []
    deps_v, deps_t, kinds, hbs, rts, irs = [], [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            deps_v.append(()); deps_t.append(()); kinds.append("")
            hbs.append(()); rts.append(()); irs.append(False)
        return i
    with open(DUMP3) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]
            deps_v[i] = tuple(nid(d) for d in r["v"])
            deps_t[i] = tuple(nid(d) for d in r["t"])
            hbs[i] = tuple(nid(d) for d in r.get("hb", ()))
            rts[i] = tuple(nid(d) for d in r.get("rt", ()))
            irs[i] = bool(r.get("ir", False))
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

    # recursor of which inductive: the inductive-kind constant in its type deps
    rec_ind = {}
    for i in np.where(is_rec)[0]:
        inds = [d for d in set(deps_t[i]) if kinds[d] == "inductive"]
        # the recursor's own inductive dominates its type; pick the one whose
        # constructors appear too, else the sole inductive
        best, bestn = None, -1
        for I in inds:
            nc = sum(1 for d in set(deps_t[i]) if is_ctor[d] and I in set(deps_t[d]))
            if nc > bestn:
                best, bestn = I, nc
        rec_ind[int(i)] = (best, sum(1 for d in set(deps_t[i]) if is_ctor[d]))
    multi_rec = {i for i, (I, nc) in rec_ind.items() if nc >= 2}
    rec_of_recursive = {i for i, (I, nc) in rec_ind.items()
                        if I is not None and irs[I]}
    # wrappers: defs whose hb is entirely recursors
    wrap_multi, wrap_recursive = set(), set()
    for i in range(n):
        if kinds[i] == "def" and hbs[i]:
            hs = set(hbs[i])
            if hs and all(is_rec[h] for h in hs):
                if hs & multi_rec:
                    wrap_multi.add(i)
                if hs & rec_of_recursive:
                    wrap_recursive.add(i)
    print(f"multi-ctor elims {len(multi_rec)}+{len(wrap_multi)}w, "
          f"recursive-elims {len(rec_of_recursive)}+{len(wrap_recursive)}w", flush=True)

    core_ids = {k: {idx[x] for x in v if x in idx} for k, v in CORE.items()}
    IND = rec_of_recursive | wrap_recursive | core_ids["wf"]
    CAS = multi_rec | wrap_multi

    def chain(r):
        out = list(rts[r])
        for _ in range(2):
            ext = []
            for c in out:
                if indeg_v[c] <= 1 and c != r and rts[c]:
                    ext.extend(x for x in rts[c] if x not in out)
            if not ext:
                break
            out.extend(ext)
        return set(out[:16])

    def tags(r):
        ch = chain(r)
        t = set()
        for k in ("contradiction", "choice", "contrapositive",
                  "extensionality", "computation"):
            if ch & core_ids[k]:
                t.add(k)
        if ch & IND:
            t.add("induction")
        if ch & CAS:
            t.add("case_split")
        return t

    rng = np.random.default_rng(SEED)
    pool = np.where(thm & np.array([len(v) > 0 for v in deps_v]))[0]
    samp = rng.choice(pool, size=40000, replace=False)
    all_tags = {int(r): tags(int(r)) for r in samp}
    from collections import Counter
    rate = Counter(t for ts in all_tags.values() for t in ts)
    out = {"n_sampled_theorems": len(samp),
           "strategy_rates": {k: round(v / len(samp), 4) for k, v in rate.most_common()}}

    sys.path.insert(0, HERE)
    from moves import build_source_index, decl_block
    print("building source index", flush=True)
    sidx = build_source_index()
    val_samp = rng.choice(samp, size=4000, replace=False)
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
            got = k in ts
            key = ("tp" if src else "fp") if got else ("fn" if src else "tn")
            stats[k][key] += 1
            if key == "fp" and len(fp_ex[k]) < 6:
                fp_ex[k].append(names[r])
            if key == "fn" and len(fn_ex[k]) < 6:
                fn_ex[k].append(names[r])
    val = {}
    for k, s in stats.items():
        val[k] = {"precision_vs_source": round(s["tp"] / max(1, s["tp"] + s["fp"]), 3),
                  "recall_vs_source": round(s["tp"] / max(1, s["tp"] + s["fn"]), 3),
                  **s, "fp_examples": fp_ex[k], "fn_examples": fn_ex[k]}
    out["validation_n"] = evaluated
    out["validation"] = val

    vibe = {}
    for a in ("Nat.exists_infinite_primes", "Real.exp_log", "Nat.gcd_comm",
              "zpow_mul", "Nat.pow_sub_one_gcd_pow_sub_one", "Real.range_log",
              "limUnder_of_not_tendsto", "Function.Injective.isPartialInv",
              "Nat.sqrt_lt", "List.length_append", "pow_iterate"):
        if a in idx:
            r = idx[a]
            vibe[a] = {"tags": sorted(tags(r)),
                       "chain": [names[c] for c in list(chain(r))[:8]]}
    out["anchor_strategies"] = vibe

    with open(os.path.join(DATA, "strategies2_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("strategy_rates =", json.dumps(out["strategy_rates"]))
    print("validation_n =", evaluated)
    print("validation =", json.dumps({k: {x: v[x] for x in
          ("precision_vs_source", "recall_vs_source", "tp", "fp", "fn")}
          for k, v in val.items()}))
    print("anchors =", json.dumps({k: v["tags"] for k, v in vibe.items()}))


if __name__ == "__main__":
    main()
