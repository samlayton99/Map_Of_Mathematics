#!/usr/bin/env python3
"""Run the social-choice family through the shared battery on TEST-R.

Stage 1 (this script): per-proof metrics over the graded proofs.
Stage 2 (--nav):       navigability over the WHOLE U1D corpus.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from mathmap_eval import battery as B                    # noqa: E402
from mathmap_eval import navigation as NAV               # noqa: E402
from mathmap_eval.corpus import get_corpus               # noqa: E402
import social_choice as SC                               # noqa: E402

SPLIT = os.environ.get("SPLIT", "TEST-R")
OUT = os.path.join(ROOT, "results", "social_choice")

# ---- reference comparators (decimal weights, NOT part of our family) ------
ROLE_W = np.array([0.0, 0.25, 0.35, 0.5, 0.85, 1.0])   # indexed by tier 1..5
DPIN = 346.0            # pinned depth normaliser (constant, never a max())


def ranks_within_proof(c, base, score):
    """0-based rank inside the proof, best (lowest key) first.

    `score` is one ascending key or a tuple of keys, most significant first.
    Final tie-break is position in the elaborated term (append-safe).
    """
    keys = score if isinstance(score, tuple) else (score,)
    order = np.lexsort((np.arange(len(base)),) + tuple(reversed(keys))
                       + (c.inc_artifact[base],))
    s = base[order]
    aa = c.inc_artifact[s]
    new = np.empty(len(s), bool)
    new[0] = True
    new[1:] = aa[1:] != aa[:-1]
    starts = np.where(new)[0]
    counts = np.diff(np.append(starts, len(s)))
    rk = np.concatenate([np.arange(x) for x in counts])
    out = np.empty(len(base), np.int32)
    out[order] = rk
    return out


def build(c, base):
    sig = SC.Signals(c)
    keys = sig.keys(base)
    tier = sig.tier(base)
    return sig, keys, tier


def reference_scores(c, base, sig, tier):
    d = c.inc_decl[base]
    rw = ROLE_W[tier]
    logd = 0.20 + 0.80 * np.log1p(c.inc_d_cite[base]) / np.log1p(DPIN)
    lind = 0.20 + 0.80 * c.inc_d_cite[base] / DPIN
    stmt = np.where(c.inc_in_stmt_world[base], 1.0, 1.5)
    idf = sig.IDF[d]
    return {
        "REF_role5w_x_logdepth": -(rw * logd),
        "REF_role5w_x_lindepth": -(rw * lind),
        "REF_role5w_x_rarity": -(rw * idf),
        "REF_role5w_x_stmt_x_logdepth": -(rw * stmt * logd),
        "REF_role5w_x_stmt_x_logdepth_x_rarity": -(rw * stmt * logd * idf),
        "REF_role5w_x_stmt_x_rarity": -(rw * stmt * idf),
    }


def scheme_scores(c, base, sig, keys, tier, want_all=True):
    """Every social-choice scheme, as a score array over `base`."""
    out = {}
    t0 = time.time()

    def agg(names, mult=None, tag=""):
        a = SC.Aggregator(c, base, keys, names, mult=mult)
        return a.run(SC.RULES)

    # --- 6-voter symmetric panel
    res6, ex6 = agg(SC.VOTERS)
    for r, v in res6.items():
        out[f"{r}6"] = v
    condorcet6 = ex6["condorcet"]

    # --- 4-voter panel (the factors the incumbent product model uses)
    res4, ex4 = agg(SC.VOTERS4)
    for r, v in res4.items():
        out[f"{r}4"] = v
    condorcet4 = ex4["condorcet"]

    if want_all:
        # --- role with integer ballot multiplicity
        for m in (2, 3):
            r, _ = agg(SC.VOTERS, mult={"role": m})
            out[f"borda6_rolex{m}"] = r["borda"]
            out[f"copeland6_rolex{m}"] = r["copeland"]
            out[f"kemeny6_rolex{m}"] = r["kemeny"]

    # --- role as veto / role lexicographic, applied on top of Borda
    # (lexicographic composition: a key TUPLE, not a numeric offset)
    bd = out["borda6"]
    for t in (2, 3):                 # veto everything strictly below tier t
        out[f"borda6_veto_below_t{t}"] = ((tier < t).astype(np.int8), bd)
    out["role_lex_then_borda6"] = (-tier.astype(np.int8), bd)
    out["borda6_condorcet_first"] = ((~condorcet6).astype(np.int8), bd)

    # --- single-voter references (a "dictatorship" per Arrow)
    for v in SC.VOTERS:
        out[f"dictator_{v}"] = (keys[v], bd)
    sys.stderr.write(f"  scheme_scores {time.time()-t0:.1f}s\n")
    return out, {"condorcet6": condorcet6, "condorcet4": condorcet4}


def main():
    c = get_corpus()
    keymap = json.load(open(os.path.join(SC.SEALED, "keymap.json")))
    grades = SC.load_grades(keymap, SPLIT)
    kr = {p: v for p, v in keymap.items() if v["split"] == SPLIT}
    print(f"{SPLIT}: {len(kr)} proofs, {len(grades)} graded incidences")

    full = np.where(c.universe("U1D"))[0]
    arts = np.array(sorted({v["artifact"] for v in kr.values()}))
    base = full[np.isin(c.inc_artifact[full], arts)]
    print(f"eval base: {len(base)} incidences in {len(arts)} artifacts")

    sig, keys, tier = build(c, base)
    scores, extras = scheme_scores(c, base, sig, keys, tier)
    scores.update(reference_scores(c, base, sig, tier))

    rows = {}
    for name, sc in scores.items():
        rk = ranks_within_proof(c, base, sc)
        pp = NAV.per_proof_orders(c, base, rk, grades, kr)
        L = B.local(pp)
        G = B.gradient(pp)
        F = B.failures(pp)
        rows[name] = {"local": L, "gradient": G, "failures": F}
        print(B.report(name, pp), flush=True)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"battery_{SPLIT}.json"), "w") as f:
        json.dump(rows, f, indent=1, default=float)

    # Condorcet existence
    cw = extras["condorcet6"]
    n_cw = sum(1 for a in arts if cw[c.inc_artifact[base] == a].any())
    print(f"\nCondorcet winner exists (6 voters): {n_cw}/{len(arts)} proofs")
    cw4 = extras["condorcet4"]
    n4 = sum(1 for a in arts if cw4[c.inc_artifact[base] == a].any())
    print(f"Condorcet winner exists (4 voters): {n4}/{len(arts)} proofs")


if __name__ == "__main__":
    main()
