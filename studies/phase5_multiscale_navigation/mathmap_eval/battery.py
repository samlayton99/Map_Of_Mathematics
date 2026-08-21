"""The full test battery — everything we actually care about, at every change.

Principle 8: a change can look better on one view and be genuinely worse. Never
accept a single headline number. Principle 7: the goal is a NAVIGABLE MAP, not
a per-proof metric, so every change must be re-tested at the graph level.

This module exists because the programme repeatedly optimised per-proof
ranking and never re-checked the graph. Every function here answers a question
from the invariant principles:

  P4 precision/recall at top-k, varying k, by depth       -> local()
  P4 gradient coherence, no inversions                    -> gradient()
  P5 does it find the key move                            -> local()
  P8 the failures themselves                              -> failures()

The graph-level question (does the map lie via false proximity through Lean
plumbing?) lives in mathmap_eval/shortcuts.py. A `navigability` connectivity
test used to live here; it measured the wrong thing and was removed.
"""
from __future__ import annotations

import numpy as np

BANDS = ["0-10", "11-25", "26-50", "51-75", "76-125", "126+"]
EDGES = [0, 11, 26, 51, 76, 126, 10 ** 9]


def _band_idx(d):
    return np.clip(np.searchsorted(np.array(EDGES), d, "right") - 1, 0,
                   len(BANDS) - 1)


def local(per_proof, ks=(1, 2, 4, 8)):
    """Precision and recall at top-k, overall and by target depth.

    `per_proof` is the output of navigation.per_proof_orders: each entry has
    `grades` in the ranking's order, plus `band`.
    """
    out = {"n_proofs": len(per_proof)}

    def prec(ps, k, thr=2):
        v = s = 0
        for p in ps:
            g = p["grades"][:k]
            v += len(g)
            s += int((g >= thr).sum())
        return s / v if v else None

    def rec(ps, k, thr):
        n = d = 0
        for p in ps:
            g = p["grades"]
            d += int((g >= thr).sum())
            n += int((g[:k] >= thr).sum())
        return n / d if d else None

    def rec_core(ps, k):
        n = d = 0
        for p in ps:
            g = p["grades"]
            d += int((g == 4).sum())
            n += int((g[:k] == 4).sum())
        return n / d if d else None

    for k in ks:
        out[f"precision@{k}"] = prec(per_proof, k)
        out[f"precision_major@{k}"] = prec(per_proof, k, 3)
        out[f"recall_useful@{k}"] = rec(per_proof, k, 2)
        out[f"recall_major@{k}"] = rec(per_proof, k, 3)
        out[f"recall_core@{k}"] = rec_core(per_proof, k)
    # P5: does rank 1 hold the single best move available in the proof?
    hit = tot = 0
    for p in per_proof:
        g = p["grades"]
        if not len(g):
            continue
        tot += 1
        if g[0] == g.max():
            hit += 1
    out["KeyMoveAt1"] = hit / tot if tot else None

    out["by_depth"] = {}
    for b in BANDS:
        sub = [p for p in per_proof if p["band"] == b]
        if not sub:
            continue
        out["by_depth"][b] = {
            "n": len(sub),
            "precision@1": prec(sub, 1), "precision@4": prec(sub, 4),
            "recall_core@4": rec_core(sub, 4),
            "recall_major@4": rec(sub, 4, 3),
        }
    return out


def gradient(per_proof, nbins=10):
    """Does usefulness fall monotonically as the view opens?

    Pools every candidate by its POSITION-FRACTION within its own proof, so
    proofs of different sizes are comparable, and reports the inversion count.
    A coherent gradient is a hard requirement for a slider to mean anything.
    """
    pos, use = [], []
    for p in per_proof:
        n = len(p["grades"])
        if n < 2:
            continue
        for j, g in enumerate(p["grades"]):
            pos.append(j / (n - 1))
            use.append(1 if g >= 2 else 0)
    if not pos:
        return {}
    pos = np.array(pos)
    use = np.array(use)
    order = np.argsort(pos)
    bins = np.array_split(use[order], nbins)
    rates = [float(b.mean()) for b in bins]
    inv = sum(1 for i in range(len(rates) - 1) if rates[i + 1] > rates[i])
    worst = max((rates[i + 1] - rates[i] for i in range(len(rates) - 1)),
                default=0.0)
    return {"bin_rates": rates, "inversions": inv,
            "worst_inversion": float(worst),
            "monotone": inv == 0,
            "spread": rates[0] - rates[-1]}


def failures(per_proof, k=4):
    """The counts we actually learn from. Principle 8."""
    prec_fail = rec_fail = grad_fail = unwinnable = 0
    for p in per_proof:
        g = p["grades"]
        if not len(g):
            continue
        n_useful = int((g >= 2).sum())
        if n_useful == 0:
            unwinnable += 1
            continue
        if g[0] <= 1:
            prec_fail += 1
        if (g == 4).any() and not (g[:k] == 4).any():
            rec_fail += 1
        if len(g) >= 6:
            h = len(g) // 2
            if (g[h:] >= 2).mean() > (g[:h] >= 2).mean() + 0.25:
                grad_fail += 1
    return {"precision_failures": prec_fail, "recall_failures": rec_fail,
            "gradient_inversions": grad_fail, "unwinnable": unwinnable,
            "n_proofs": len(per_proof)}


def report(name, per_proof):
    """One line per thing we care about. Never a single headline."""
    L = local(per_proof)
    G = gradient(per_proof)
    F = failures(per_proof)
    lines = [f"{name}",
             f"  P@1 {L['precision@1']:.3f}  P@4 {L['precision@4']:.3f}  "
             f"KeyMove@1 {L['KeyMoveAt1']:.3f}",
             f"  recall core@4 {L['recall_core@4']:.3f}  major@4 "
             f"{L['recall_major@4']:.3f}  useful@4 {L['recall_useful@4']:.3f}",
             f"  gradient monotone={G['monotone']} inversions={G['inversions']} "
             f"spread={G['spread']:.3f}",
             f"  failures: precision {F['precision_failures']} recall "
             f"{F['recall_failures']} gradient {F['gradient_inversions']} "
             f"(unwinnable {F['unwinnable']})"]
    return "\n".join(lines)
