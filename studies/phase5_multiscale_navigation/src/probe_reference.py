#!/usr/bin/env python3
"""Find which weighted product model reproduces the quoted reference line
(P@1 0.975, P@4 0.712, KeyMove@1 0.825, core@4 0.974, 8 precision failures)."""
import itertools
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from mathmap_eval import battery as B                    # noqa: E402
from mathmap_eval import navigation as NAV               # noqa: E402
from mathmap_eval.corpus import get_corpus               # noqa: E402
import social_choice as SC                               # noqa: E402
from run_social_choice import ranks_within_proof, DPIN   # noqa: E402

TIER_MAPS = {
    "A_maxtier":   np.array([5, 5, 4, 3, 1, 3, 2, 4], np.int8),
    "B_unres3":    np.array([5, 5, 4, 3, 1, 3, 2, 3], np.int8),
    "C_let4":      np.array([5, 4, 4, 3, 1, 3, 2, 4], np.int8),
    "D_strict2":   np.array([5, 5, 4, 3, 1, 2, 2, 4], np.int8),
    "E_argmax":    None,          # strongest raw role column, same tiers as A
}
WEIGHTS = {
    "w1": np.array([0.0, 0.25, 0.35, 0.5, 0.85, 1.0]),
    "w2": np.array([0.0, 0.25, 0.35, 0.5, 0.7, 1.0]),
    "w3": np.array([0.0, 0.25, 0.5, 0.5, 0.85, 1.0]),
    "w4": np.array([0.0, 0.1, 0.25, 0.5, 0.85, 1.0]),
}


def main():
    c = get_corpus()
    keymap = json.load(open(os.path.join(SC.SEALED, "keymap.json")))
    grades = SC.load_grades(keymap, "TEST-R")
    kr = {p: v for p, v in keymap.items() if v["split"] == "TEST-R"}
    full = np.where(c.universe("U1D"))[0]
    arts = np.array(sorted({v["artifact"] for v in kr.values()}))
    base = full[np.isin(c.inc_artifact[full], arts)]
    sig = SC.Signals(c)
    d = c.inc_decl[base]
    idf = sig.IDF[d]
    logd = 0.20 + 0.80 * np.log1p(c.inc_d_cite[base]) / np.log1p(DPIN)
    lind = 0.20 + 0.80 * c.inc_d_cite[base] / DPIN
    stmt = np.where(c.inc_in_stmt_world[base], 1.0, 1.5)
    roles = c.inc_roles[base] > 0
    FACTORS = {"idf": idf, "logd": logd, "lind": lind, "stmt": stmt,
               "one": np.ones(len(base))}
    combos = [("idf",), ("logd",), ("lind",), ("idf", "stmt"),
              ("logd", "stmt"), ("idf", "logd"), ("idf", "lind"),
              ("idf", "logd", "stmt"), ("idf", "lind", "stmt")]
    best = []
    for tname, tmap in TIER_MAPS.items():
        if tmap is None:
            tier = SC.TIER_OF_ROLE[np.argmax(c.inc_roles[base], axis=1)]
        else:
            tier = (roles * tmap[None, :]).max(axis=1)
        for wname, w in WEIGHTS.items():
            rw = w[tier]
            for combo in combos:
                s = rw.copy()
                for f in combo:
                    s = s * FACTORS[f]
                rk = ranks_within_proof(c, base, -s)
                pp = NAV.per_proof_orders(c, base, rk, grades, kr)
                L = B.local(pp)
                F = B.failures(pp)
                row = (round(L["precision@1"], 3), round(L["precision@4"], 3),
                       round(L["KeyMoveAt1"], 3), round(L["recall_core@4"], 3),
                       F["precision_failures"])
                err = (abs(row[0] - 0.975) + abs(row[1] - 0.712)
                       + abs(row[2] - 0.825) + abs(row[3] - 0.974)
                       + abs(row[4] - 8) / 100.0)
                best.append((err, tname, wname, combo, row))
    best.sort()
    for e, t, w, combo, row in best[:15]:
        print(f"err {e:.4f}  {t:<10} {w} {'*'.join(combo):<20} "
              f"P@1 {row[0]} P@4 {row[1]} Key {row[2]} core {row[3]} "
              f"fails {row[4]}")


if __name__ == "__main__":
    main()
