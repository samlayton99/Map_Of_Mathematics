#!/usr/bin/env python3
"""Reference numbers, recomputed from the record. Committed so they cannot rot.

The quoted reference line (P@1 0.975, P@4 0.712, KeyMove@1 0.825, core@4
0.974) previously lived only in throwaway scripts; two reports document
failed reproduction attempts (SCHEME_SOCIAL_CHOICE.md section 4,
SCHEME_CONDITIONAL.md "Reproduction caveat"). The recipe below DOES reproduce
all four to 4 decimals on sealed TEST-R. It is the reference model from the
DOMINANCE/PROBABILISTIC study apparatus (scratchpad famAB_ref.py,
"REF_weighted_role_x_rarity_5dec"):

    score = -( W[tier] * IDF50[cited decl] ),  W = [1.0, 0.7, 0.5, 0.35, 0.15]

with the 5-level syntactic role tier (0 best) and the frozen depth<=50 rarity
table, ties broken by term order. NOTE: the registered `R_phase5_composite`
(mathmap_eval/rankings.py) is a DIFFERENT reconstruction and does NOT
reproduce the quoted line (it gives P@1 0.9833, P@4 0.6892, KeyMove@1 0.8861,
core@4 0.9869 on TEST-R); its values are recorded alongside for the audit
trail.

Run:  ~/venv/general_ml/bin/python src/reference_numbers.py
Writes results/reference_numbers.json and exits non-zero on any mismatch.
"""
import datetime
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
from mathmap_eval import rankings as R                   # noqa: E402
from mathmap_eval.corpus import get_corpus               # noqa: E402
import social_choice as SC                               # noqa: E402

SPLIT = "TEST-R"
EXPECTED = {
    "precision@1": 0.9750,
    "precision@4": 0.7123,
    "KeyMoveAt1": 0.8250,
    "recall_core@4": 0.9738,
}
TOL = 5e-5          # values are quoted to 4 decimals
ROLE_W = np.array([1.0, 0.7, 0.5, 0.35, 0.15])   # indexed by tier 0..4, 0 best
OUT = os.path.join(ROOT, "results", "reference_numbers.json")


def tier5(c, b):
    """5-level ordinal role tier from syntactic position. 0 = best.

    Exactly the DOMINANCE-study tier: applied 0; let-value/explicit 1;
    default (implicit etc.) 2; pure type-annotation 3; pure instance-slot 4,
    except an instance-slot citation one depth step below its target is 2.
    """
    r = c.inc_roles[b]
    t = np.full(len(b), 2, dtype=np.int8)
    inst = (r[:, 4] > 0) & (r.sum(axis=1) == r[:, 4])
    ta = (r[:, 6] > 0) & (r.sum(axis=1) == r[:, 6])
    t[ta] = 3
    t[inst] = 4
    t[(r[:, 1] > 0) | (r[:, 2] > 0)] = 1
    t[r[:, 0] > 0] = 0
    t[inst & ((c.inc_d_target[b] - c.inc_d_cite[b]) == 1)] = 2
    return t


def idf50(c, base):
    """Frozen rarity: IDF over the pinned depth<=50 foundation, U1D."""
    m50 = c.inc_d_target[base] <= 50
    pop = np.bincount(c.inc_decl[base[m50]], minlength=c.n_nodes).astype(float)
    n50 = float(len(np.unique(c.inc_artifact[base[m50]])))
    return np.maximum(np.log(n50 / np.maximum(pop, 1.0)), 0.0)


def ranks_within_proof(arts, key):
    """0-based rank inside each proof; ascending key, term-order tie-break."""
    n = len(arts)
    order = np.lexsort((np.arange(n), key, arts))
    aa = arts[order]
    new = np.empty(n, bool)
    new[0] = True
    new[1:] = aa[1:] != aa[:-1]
    counts = np.diff(np.append(np.where(new)[0], n))
    rk = np.concatenate([np.arange(x) for x in counts])
    out = np.empty(n, np.int32)
    out[order] = rk
    return out


def local_metrics(c, base, ranks, grades, kr):
    L = B.local(NAV.per_proof_orders(c, base, ranks, grades, kr))
    return {m: float(L[m]) for m in EXPECTED}, L


def main():
    c = get_corpus()
    keymap = json.load(open(os.path.join(SC.SEALED, "keymap.json")))
    grades = SC.load_grades(keymap, SPLIT)
    kr = {p: v for p, v in keymap.items() if v["split"] == SPLIT}
    print(f"{SPLIT}: {len(kr)} proofs, {len(grades)} graded incidences")

    base = np.where(c.universe("U1D"))[0]
    arts = c.inc_artifact[base]

    # --- the reference line: role-tier weights x frozen rarity -----------
    score = -(ROLE_W[tier5(c, base)] * idf50(c, base)[c.inc_decl[base]])
    ranks = ranks_within_proof(arts, score)
    computed, L = local_metrics(c, base, ranks, grades, kr)

    ok = True
    for m, want in EXPECTED.items():
        got = computed[m]
        match = abs(got - want) <= TOL
        ok &= match
        print(f"{m:<14} computed {got:.4f}  expected {want:.4f}  "
              f"{'OK' if match else 'MISMATCH'}")

    # --- the registered reconstruction, for the audit trail --------------
    rk_p5 = R.get("R_phase5_composite").ranks_within_proof(c, base)
    p5_vals, _ = local_metrics(c, base, rk_p5, grades, kr)
    print("R_phase5_composite (registered reconstruction, does not match):")
    for m, v in p5_vals.items():
        print(f"  {m:<14} {v:.4f}")

    payload = dict(computed)
    payload["provenance"] = {
        "ranking": "REF_weighted_role_x_rarity_5dec: "
                   "-(W[tier5] * IDF50[decl]), W=[1.0,0.7,0.5,0.35,0.15], "
                   "term-order tie-break (this file)",
        "split": SPLIT,
        "labels": "review/sealed_r1/grades_*.json (median rater grade), "
                  "keymap review/sealed_r1/keymap.json",
        "universe": "U1D",
        "apparatus": "mathmap_eval battery.local via navigation.per_proof_orders",
        "n_proofs": L["n_proofs"],
        "date": datetime.date.today().isoformat(),
        "expected": EXPECTED,
        "all_match": ok,
        "note": "registered R_phase5_composite is a different reconstruction "
                "and does not reproduce the quoted line; its values are in "
                "R_phase5_composite_actual",
    }
    payload["R_phase5_composite_actual"] = p5_vals
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=1)
    print(f"wrote {OUT}")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
