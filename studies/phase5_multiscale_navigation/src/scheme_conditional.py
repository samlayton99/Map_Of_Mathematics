#!/usr/bin/env python3
"""Conditional-structure ranking schemes: regimes, trees, cascades, semiorders.

Reproduces every number in reports/SCHEME_CONDITIONAL.md. Run:

    ~/venv/general_ml/bin/python src/scheme_conditional.py [section]

sections: battery | tiers | escape | tree | sweep | gradient | bands | nav | all

The premise of this family is that the signals are not symmetric: role is a
near-deterministic filter, depth and rarity are graded evidence. So role should
CONDITION the ordering rather than vote in it.

Constraints honoured throughout:
  * no arbitrary decimal constants -- every constant is a small integer, and
    every one is listed in the report;
  * append-safe -- rarity is the pinned depth<=50 foundation table, every other
    quantity is either a kernel fact or proof-local;
  * no name-string matching;
  * the deployed object is a set of readable rules.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

from mathmap_eval import battery as B                  # noqa: E402
from mathmap_eval.corpus import get_corpus             # noqa: E402
from mathmap_eval.navigation import per_proof_orders   # noqa: E402

SEALED = os.path.join(ROOT, "review", "sealed_r1")
SPLIT_NAMES = ("TEST-R", "CAL", "TEST-C")

# ----------------------------------------------------------------- constants
# Every constant used by any scheme below, with its meaning. All integers.
FROZEN_FOUNDATION_DEPTH = 50   # pinned rarity table: proofs of target depth <=50
ESCAPE_RARITY = 8              # nats of frozen rarity that buy a one-tier jump
ESCAPE_EV_RANK = 2             # alternative escape: within-proof evidence rank
TREE_MAX_DEPTH = 3             # interpretability cap
TREE_MIN_LEAF = 100            # candidates; interpretability + stability cap

# ------------------------------------------------------------------- loading
c = get_corpus()
keymap = json.load(open(os.path.join(SEALED, "keymap.json")))
FULL = np.where(c.universe("U1D"))[0]


def load_grades():
    """Median of the three sealed-R1 rater grades, per incidence."""
    votes = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(SEALED, "grades_*.json"))):
        for pid, ent in json.load(open(f)).items():
            if pid not in keymap:
                continue
            for num, g in (ent.get("grades") or {}).items():
                inc = keymap[pid]["items"].get(str(num))
                if inc is None:
                    continue
                try:
                    votes[int(inc)].append(int(g))
                except (TypeError, ValueError):
                    pass
    return {i: int(np.median(v)) for i, v in votes.items()}


GRADES = load_grades()
SPLITS = {s: {p: v for p, v in keymap.items() if v["split"] == s}
          for s in SPLIT_NAMES}

# frozen-foundation rarity, identical to src/mine_failures.py
_m = c.inc_d_target[FULL] <= FROZEN_FOUNDATION_DEPTH
_pop = np.bincount(c.inc_decl[FULL[_m]], minlength=c.n_nodes).astype(float)
_nart = float(len(np.unique(c.inc_artifact[FULL[_m]])))
IDF = np.maximum(np.log(_nart / np.maximum(_pop, 1.0)), 0.0)

# evaluation works on the labelled proofs only
LAB_ARTS = np.array(sorted({int(m["artifact"]) for m in keymap.values()}))
base = FULL[np.isin(c.inc_artifact[FULL], LAB_ARTS)]


def signals(b):
    """Every append-safe signal any scheme here reads."""
    r = c.inc_roles[b]
    # ROLE TIER: ordinal, 5 levels, from syntactic position in the proof term.
    # 4 applied | 3 let-value/explicit-arg | 2 implicit/strict-implicit
    # 1 type-annotation/unresolved | 0 instance-slot.  Strongest role present.
    tier = np.where(r[:, 0] > 0, 4,
            np.where((r[:, 1] > 0) | (r[:, 2] > 0), 3,
            np.where((r[:, 3] > 0) | (r[:, 5] > 0), 2,
            np.where((r[:, 6] > 0) | (r[:, 7] > 0), 1, 0)))).astype(np.int64)
    return dict(TIER=tier,
                DEPTH=c.inc_d_cite[b].astype(np.int64),
                RARITY=IDF[c.inc_decl[b]],
                INSTMT=c.inc_in_stmt_world[b].astype(np.int64),
                ARITY=c.node_arity[c.inc_decl[b]].astype(np.int64),
                ISPROOF=c.node_is_proof[c.inc_decl[b]].astype(np.int64),
                ISPROP=c.node_is_prop[c.inc_decl[b]].astype(np.int64),
                ART=c.inc_artifact[b])


S = signals(base)
TIER, DEPTH, RARITY = S["TIER"], S["DEPTH"], S["RARITY"]
INSTMT, ARITY, ISPROOF, ISPROP = S["INSTMT"], S["ARITY"], S["ISPROOF"], S["ISPROP"]
ART = S["ART"]
N = len(base)
GRD = np.array([GRADES.get(int(p), -1) for p in base])
SPLIT_OF = np.array([{int(m["artifact"]): m["split"]
                      for m in keymap.values()}[int(a)] for a in ART])


# ---------------------------------------------------------------- rank utils
def _ranks(art, score):
    order = np.lexsort((np.arange(len(score)), -np.asarray(score, float), art))
    aa = art[order]
    new = np.empty(len(order), bool); new[0] = True; new[1:] = aa[1:] != aa[:-1]
    counts = np.diff(np.append(np.where(new)[0], len(order)))
    out = np.empty(len(score), np.int32)
    out[order] = np.concatenate([np.arange(x) for x in counts])
    return out


def ranks_from_score(score):
    return _ranks(ART, score)


def ranks_lex(keys, art=None, n=None):
    """0-based within-proof rank; `keys` ascending priority, smaller = better."""
    art = ART if art is None else art
    n = N if n is None else n
    ks = tuple(np.asarray(k, float) for k in keys)
    order = np.lexsort(tuple(reversed(ks + (np.arange(n).astype(float),))) + (art,))
    aa = art[order]
    new = np.empty(n, bool); new[0] = True; new[1:] = aa[1:] != aa[:-1]
    counts = np.diff(np.append(np.where(new)[0], n))
    out = np.empty(n, np.int32)
    out[order] = np.concatenate([np.arange(x) for x in counts])
    return out


def avg_rank(sig, art=None, desc=True):
    """Within-proof rank, 1-based, ties share the mean rank."""
    art = ART if art is None else art
    v = -np.asarray(sig, float) if desc else np.asarray(sig, float)
    order = np.lexsort((v, art))
    aa, vv = art[order], v[order]
    n = len(order)
    gnew = np.empty(n, bool); gnew[0] = True; gnew[1:] = aa[1:] != aa[:-1]
    gstart = np.maximum.accumulate(np.where(gnew, np.arange(n), 0))
    tnew = gnew | (vv != np.roll(vv, 1)); tnew[0] = True
    tstart = np.maximum.accumulate(np.where(tnew, np.arange(n), 0))
    idx = np.where(tnew)[0]
    tend = np.zeros(n, np.int64)
    tend[idx] = np.append(idx[1:] - 1, n - 1)
    tend = np.maximum.accumulate(np.where(tnew, tend, 0))
    out = np.empty(n)
    out[order] = ((tstart - gstart + 1) + (tend - gstart + 1)) / 2.0
    return out


def evaluate(ranks, split):
    pp = per_proof_orders(c, base, ranks, GRADES, SPLITS[split])
    L, G, F = B.local(pp), B.gradient(pp), B.failures(pp)
    return {"P@1": L["precision@1"], "P@4": L["precision@4"],
            "KM@1": L["KeyMoveAt1"], "core@4": L["recall_core@4"],
            "maj@4": L["recall_major@4"], "use@4": L["recall_useful@4"],
            "mono": G["monotone"], "inv": G["inversions"],
            "bins": G["bin_rates"], "pf": F["precision_failures"],
            "rf": F["recall_failures"], "gf": F["gradient_inversions"]}


def md_row(name, ranks, split):
    r = evaluate(ranks, split)
    return (f"| {name} | {split} | {r['P@1']:.3f} | {r['P@4']:.3f} | "
            f"{r['KM@1']:.3f} | {r['core@4']:.3f} | {r['maj@4']:.3f} | "
            f"{r['use@4']:.3f} | {r['mono']} | {r['inv']} | {r['pf']} | "
            f"{r['rf']} | {r['gf']} |")


# ------------------------------------------------------------------ the tree
TREE_FEATS = {"tier": TIER, "depth": DEPTH, "rarity": RARITY, "arity": ARITY,
              "is_proof": ISPROOF, "is_prop": ISPROP, "in_stmt": INSTMT}
TREE_THR = {
    "is_proof": [0], "is_prop": [0], "in_stmt": [0],
    "tier": [0, 1, 2, 3],
    "rarity": list(range(13)),       # integer thresholds on a real-valued signal
    "arity": list(range(13)),
    "depth": [0, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150],
}


def _sse(y):
    return float(((y - y.mean()) ** 2).sum()) if len(y) else 0.0


def fit_tree(idx, y, depth=0, min_leaf=TREE_MIN_LEAF):
    node = {"n": len(idx), "mean": float(y[idx].mean())}
    if depth >= TREE_MAX_DEPTH:
        return node
    b = None
    s0 = _sse(y[idx])
    for nm, v in TREE_FEATS.items():
        vv = v[idx]
        for t in TREE_THR[nm]:
            L = vv <= t
            if int(L.sum()) < min_leaf or len(idx) - int(L.sum()) < min_leaf:
                continue
            gain = s0 - _sse(y[idx][L]) - _sse(y[idx][~L])
            if b is None or gain > b[0]:
                b = (gain, nm, t)
    if b is None or b[0] <= 0:
        return node
    _, nm, t = b
    L = TREE_FEATS[nm][idx] <= t
    node.update(feat=nm, thr=t, left=fit_tree(idx[L], y, depth + 1, min_leaf),
                right=fit_tree(idx[~L], y, depth + 1, min_leaf))
    return node


def tree_leaves(node, path=()):
    if "feat" not in node:
        return [(path, node)]
    return (tree_leaves(node["left"], path + ((node["feat"], node["thr"], True),))
            + tree_leaves(node["right"], path + ((node["feat"], node["thr"], False),)))


def tree_classes(node):
    """Per-candidate ordered class: 0 = highest mean grade."""
    lv = tree_leaves(node)
    leaf = np.full(N, -1, np.int64)
    for k, (path, _) in enumerate(lv):
        m = np.ones(N, bool)
        for nm, t, le in path:
            m &= (TREE_FEATS[nm] <= t) if le else (TREE_FEATS[nm] > t)
        leaf[m] = k
    order = np.argsort(-np.array([lv[k][1]["mean"] for k in range(len(lv))]))
    rank_of = np.empty(len(lv), np.int64)
    for r, k in enumerate(order):
        rank_of[k] = r
    return rank_of[leaf].astype(float), lv, list(order)


def tree_rules(lv, order):
    rank = {k: r for r, k in enumerate(order)}
    out = []
    for k, (path, leaf) in enumerate(lv):
        cond = " and ".join(f"{nm} <= {t}" if le else f"{nm} > {t}"
                            for nm, t, le in path)
        out.append((rank[k] + 1, cond, leaf["n"], leaf["mean"]))
    return sorted(out)


# ------------------------------------------------------------- scheme bodies
RD, RR, RA = avg_rank(DEPTH), avg_rank(RARITY), avg_rank(ARITY)
RT, RS = avg_rank(TIER), avg_rank(-INSTMT.astype(float))
EV_RANK = avg_rank(-(RD + RR))          # 1 = strongest evidence in the proof
COARSE = np.select([TIER >= 3, TIER >= 1], [2, 1], default=0)
W_REF = np.select([TIER == 4, TIER == 3], [1.0, 0.7], default=0.5)

_TREE = fit_tree(np.where(SPLIT_OF == "TEST-R")[0], GRD.astype(float))
TCLS, TLEAVES, TORDER = tree_classes(_TREE)


def escape(fire):
    """Lexicographic on role tier, one-tier jump for candidates that fire."""
    return ranks_lex((-(TIER + fire.astype(int)).astype(float), EV_RANK))


def cascade(preds, sec=EV_RANK):
    """First matching predicate wins the class; unmatched fall to the last."""
    cls = np.full(N, len(preds), float)
    for k in range(len(preds) - 1, -1, -1):
        cls[preds[k]] = k
    return ranks_lex((cls, sec))


SCHEMES = [
    ("REF-W  role x frozen rarity", ranks_from_score(W_REF * RARITY)),
    ("REF-B  Borda tier+depth+rarity+stmt", ranks_from_score(-(RT + RD + RR + RS))),
    ("REF-LEX tier -> rarity", ranks_lex((-TIER.astype(float), RR))),
    ("C1a tier -> rarity", ranks_lex((-TIER.astype(float), RR))),
    ("C1b tier -> depth", ranks_lex((-TIER.astype(float), RD))),
    ("C1c tier -> borda(depth,rarity)", ranks_lex((-TIER.astype(float), EV_RANK))),
    ("C1d tier -> per-tier signal",
     ranks_lex((-TIER.astype(float),
                np.select([TIER == 4, TIER == 3, TIER == 2, TIER == 1, TIER == 0],
                          [RR, RR, RA, EV_RANK, EV_RANK])))),
    ("C2a merge {4,3}{2,1}{0}", ranks_lex((-COARSE.astype(float), EV_RANK))),
    ("C2b merge {4,3}{2,1,0}", ranks_lex((-(TIER >= 3).astype(float), EV_RANK))),
    ("C2c merge {4,3,2,1}{0}", ranks_lex((-(TIER >= 1).astype(float), EV_RANK))),
    ("C3a escape ev-rank<=1", escape(EV_RANK <= 1)),
    ("C3b escape ev-rank<=2", escape(EV_RANK <= ESCAPE_EV_RANK)),
    ("C3c escape ev-rank<=3", escape(EV_RANK <= 3)),
    ("C3d escape rarity>=8", escape(RARITY >= ESCAPE_RARITY)),
    ("C3e escape rarity>=8 & tier>=1",
     escape((RARITY >= ESCAPE_RARITY) & (TIER >= 1))),
    ("C3f escape rarity>=8 & is_proof",
     escape((RARITY >= ESCAPE_RARITY) & (ISPROOF == 1))),
    ("C3g escape two tiers, ev-rank<=1",
     ranks_lex((-(TIER + 2 * (EV_RANK <= 1)).astype(float), EV_RANK))),
    ("C4a cascade 6-class",
     cascade([(TIER >= 3) & (RARITY >= 8), (TIER >= 3),
              (TIER >= 1) & (RARITY >= 10), (TIER == 2), (TIER == 1)])),
    ("C4b cascade 4-class",
     cascade([(TIER >= 3) & (RARITY >= 8) & (INSTMT == 0), (TIER >= 3),
              (TIER >= 1) & (RARITY >= 10)])),
    ("C5  tree d3 -> rarity+depth", ranks_lex((TCLS, RR + RD))),
    ("C5b tree d3 -> rarity", ranks_lex((TCLS, RR))),
    ("C6  merge{4,3}{2,1}{0} + escape rarity>=8",
     ranks_lex((-(COARSE + ((RARITY >= 8) & (TIER >= 1))).astype(float), EV_RANK))),
    ("C7  tree class + escape rarity>=8",
     ranks_lex((TCLS - ((RARITY >= 8) & (TIER >= 1)), RR + RD))),
]

HEAD = ("| scheme | split | P@1 | P@4 | KeyMove@1 | core@4 | major@4 | "
        "useful@4 | monotone | inv | prec fail | rec fail | grad fail |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|")


# --------------------------------------------------------------- diagnostics
def sec_battery():
    print(HEAD)
    for nm, rk in SCHEMES:
        for s in SPLIT_NAMES:
            print(md_row(nm, rk, s))


def sec_tiers():
    """Which secondary signal orders best WITHIN each tier?"""
    from itertools import combinations
    cands = {"depth": DEPTH.astype(float), "rarity": RARITY,
             "borda(d,r)": -(RD + RR), "arity": ARITY.astype(float),
             "not_in_stmt": -INSTMT.astype(float), "is_proof": ISPROOF.astype(float),
             "is_prop": ISPROP.astype(float)}
    for split in SPLIT_NAMES:
        print(f"\n=== {split} ===")
        sm = SPLIT_OF == split
        for t in range(4, -1, -1):
            m = sm & (TIER == t)
            if m.sum() < 20:
                continue
            res, tot = {}, 0
            for nm, sig in cands.items():
                conc = disc = tie = 0
                idx = np.where(m)[0]
                for a in np.unique(ART[idx]):
                    j = idx[ART[idx] == a]
                    for u, v in combinations(range(len(j)), 2):
                        gu, gv = GRD[j[u]], GRD[j[v]]
                        if gu == gv:
                            continue
                        hi, lo = (j[u], j[v]) if gu > gv else (j[v], j[u])
                        if sig[hi] > sig[lo]:
                            conc += 1
                        elif sig[hi] < sig[lo]:
                            disc += 1
                        else:
                            tie += 1
                tot = conc + disc + tie
                if tot:
                    res[nm] = (conc + 0.5 * tie) / tot
            g = GRD[m]
            print(f"tier {t}: n={m.sum()} P(useful)={(g >= 2).mean():.3f} "
                  f"P(>=3)={(g >= 3).mean():.3f} decidable pairs={tot}")
            for nm, v in sorted(res.items(), key=lambda kv: -kv[1]):
                print(f"    {nm:<14} C={v:.3f}")


def sec_escape():
    fire = (RARITY >= ESCAPE_RARITY) & (TIER >= 1)
    lex = ranks_lex((-TIER.astype(float), EV_RANK))
    esc = escape(fire)
    print("selectivity of the escape predicate, P(useful | fires) vs | does not |")
    for split in SPLIT_NAMES:
        sm = SPLIT_OF == split
        parts = []
        for t in range(5):
            a, b = sm & fire & (TIER == t), sm & (~fire) & (TIER == t)
            if a.sum() >= 10 and b.sum() >= 10:
                parts.append(f"t{t} {(GRD[a] >= 2).mean():.2f} vs "
                             f"{(GRD[b] >= 2).mean():.2f} (n={a.sum()})")
        print(f"  {split:<7} " + "   ".join(parts))
    print("\nwhat the escape does to rank 1")
    for split in SPLIT_NAMES:
        arts = np.unique(ART[SPLIT_OF == split])
        crossed = fixed = broke = 0
        for a in arts:
            j = np.where(ART == a)[0]
            il, ie = j[np.argmin(lex[j])], j[np.argmin(esc[j])]
            if il == ie:
                continue
            crossed += int(TIER[ie] < TIER[il])
            fixed += int(GRD[ie] >= 2 and GRD[il] <= 1)
            broke += int(GRD[il] >= 2 and GRD[ie] <= 1)
        print(f"  {split:<7} {len(arts)} proofs: rank-1 crossed a tier {crossed}, "
              f"defect->useful {fixed}, useful->defect {broke}")


def sec_tree():
    print(f"tree fitted on TEST-R, max depth {TREE_MAX_DEPTH}, "
          f"min leaf {TREE_MIN_LEAF}, {len(TLEAVES)} leaves")
    for r, cond, n, mean in tree_rules(TLEAVES, TORDER):
        print(f"  class {r}: {cond}   [n={n}, mean grade {mean:.2f}]")
    print("\nclass mean grade per split (does the fitted order transfer?)")
    for s in SPLIT_NAMES:
        m = SPLIT_OF == s
        print(f"  {s:<7} " + "  ".join(
            f"c{k+1}:{GRD[m & (TCLS == k)].mean():.2f}"
            f"(n={int((m & (TCLS == k)).sum())})"
            for k in range(int(TCLS.max()) + 1)))
    print("\nrefits (stability of the learned rule)")
    for split, ml in (("CAL", 30), ("TEST-C", 50), ("TEST-R", 300)):
        t = fit_tree(np.where(SPLIT_OF == split)[0], GRD.astype(float), min_leaf=ml)
        lv = tree_leaves(t)
        order = list(np.argsort(-np.array([lv[k][1]["mean"] for k in range(len(lv))])))
        print(f"  --- fit on {split}, min leaf {ml}")
        for r, cond, n, mean in tree_rules(lv, order):
            print(f"    class {r}: {cond}   [n={n}, mean {mean:.2f}]")


def sec_sweep():
    print(HEAD)
    for t in range(5, 13):
        rk = escape((RARITY >= t) & (TIER >= 1))
        for s in SPLIT_NAMES:
            print(md_row(f"escape rarity>={t} & tier>=1", rk, s))


def sec_gradient():
    keep = ("REF-W", "REF-B", "REF-LEX", "C2a", "C3e", "C5", "C6")
    for nm, rk in SCHEMES:
        if not nm.startswith(keep):
            continue
        for s in SPLIT_NAMES:
            r = evaluate(rk, s)
            print(f"{nm:<42} {s:<7} "
                  + " ".join(f"{x:.2f}" for x in r["bins"])
                  + f"   inversions={r['inv']}")


def sec_bands():
    keep = ("REF-W", "REF-B", "REF-LEX", "C3e", "C5", "C6")
    for nm, rk in SCHEMES:
        if not nm.startswith(keep):
            continue
        pp = per_proof_orders(c, base, rk, GRADES, SPLITS["TEST-R"])
        print(nm)
        for b, r in B.local(pp)["by_depth"].items():
            print(f"    {b:<8} n={r['n']:<4} P@1 {r['precision@1']:.3f} "
                  f"P@4 {r['precision@4']:.3f} core@4 {r['recall_core@4']:.3f}")


def sec_regimes():
    """Proof-level regimes: choose the ORDERING RULE from a proof-local fact."""
    npro = np.zeros(N)
    has_t4 = np.zeros(N, bool)
    for a in np.unique(ART):
        m = ART == a
        npro[m] = m.sum()
        has_t4[m] = (TIER[m] == 4).any()
    print(f"proofs with a tier-4 candidate: "
          f"{len(np.unique(ART[has_t4]))} of {len(np.unique(ART))} "
          f"-- the regime is near-degenerate")
    rk_esc = escape((RARITY >= ESCAPE_RARITY) & (TIER >= 1))
    rk_ev = ranks_from_score(-EV_RANK)

    def blend(mask, a, b):
        out = b.copy(); out[mask] = a[mask]; return out

    print(HEAD)
    for nm, m in (("R1 proofs <=8 candidates -> evidence only", npro <= 8),
                  ("R2 proofs without tier-4 -> evidence only", ~has_t4),
                  ("R3 proofs with tier-4 -> evidence only", has_t4)):
        rk = blend(m, rk_ev, rk_esc)
        for s in SPLIT_NAMES:
            print(md_row(nm, rk, s))


SECTIONS = {"battery": sec_battery, "tiers": sec_tiers, "escape": sec_escape,
            "tree": sec_tree, "sweep": sec_sweep, "gradient": sec_gradient,
            "bands": sec_bands, "regimes": sec_regimes}

if __name__ == "__main__":
    want = sys.argv[1:] or ["battery"]
    if want == ["all"]:
        want = list(SECTIONS)
    for w in want:
        print(f"\n########## {w}\n")
        SECTIONS[w]()
