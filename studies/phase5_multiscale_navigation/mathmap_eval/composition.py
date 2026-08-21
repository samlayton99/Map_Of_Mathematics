"""Rank composition and precision/recall -- the V8-style scorecard.

Two channels, never mixed, because they answer different questions and have
very different n.

  Channel A -- STRUCTURAL (prefix Role*/Rank*).  What our own classifier says
  is sitting at rank 1, over EVERY proof in the corpus.  No labels needed, so
  n is ~700k and the depth breakdown is exact.  It can tell you "there is glue
  at rank 1"; it CANNOT tell you whether that glue is wrong.

  Channel B -- SEMANTIC (prefix Semantic*).  What graded raters say is sitting
  at rank 1, over the 180-proof labelled set.  This is the only channel that
  can separate BAD glue from LEGITIMATE glue, and the only one that can say
  what a ranking MISSED.  n is small; every number carries its n.

The distinction Sam asked for is exactly Channel A's `RoleGlueAt1` versus
Channel B's `SemanticBadGlueAt1`.  Reporting either alone is misleading.

Grade scale (see review/labels/): 4 KEY, 3 SUPPORT, 2 LEGIT_GLUE,
1 BAD_GLUE, 0 JUNK.
"""
from __future__ import annotations

from collections import Counter, defaultdict

import numpy as np

from .metrics import BAND_LABELS, DEPTH_BANDS, _band

GRADE_NAMES = {4: "KEY", 3: "SUPPORT", 2: "LEGIT_GLUE", 1: "BAD_GLUE",
               0: "JUNK"}
STRUCT_CATS = ["machinery", "logic-glue", "theorem", "definition/construction",
               "constructor/recursor"]


def _wilson(k, n, z=1.96):
    """Wilson score interval -- honest at the small n the semantic channel has."""
    if n == 0:
        return [float("nan"), float("nan")]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [float(max(0.0, c - h)), float(min(1.0, c + h))]


def structural_category(c, base) -> np.ndarray:
    """Our own 5-way classification of each candidate, as codes into
    STRUCT_CATS. A statistic, not truth.

    Integer codes rather than strings: `base` can be 18M long and a string
    Counter over it costs 12s per call, which the policy grid cannot afford.
    """
    d = c.inc_decl[base]
    k = c.node_kind[d]
    out = np.full(len(base), 4, dtype=np.int8)          # constructor/recursor
    out[k == 0] = 2                                     # theorem
    out[np.isin(k, (1, 2, 5, 6, 7))] = 3                # definition/construction
    out[c.decl_logic_only[d]] = 1                       # logic-glue
    out[c.inc_machinery[base]] = 0                      # machinery wins
    return out


# ------------------------------------------------------- Channel A
def rank_composition(c, base, ranks, ks=(1, 2, 4, 8)):
    """What sits at each rank prefix, by our classifier, over ALL proofs.

    Returns overall and per target-depth-band composition, plus the headline
    `RoleGlueAt1` = share of proofs whose top-ranked citation our classifier
    calls glue (logic-glue or machinery).
    """
    cat = structural_category(c, base)
    edges = np.array([lo for lo, _ in DEPTH_BANDS] + [DEPTH_BANDS[-1][1]])
    bidx = np.clip(np.searchsorted(edges, c.inc_d_target[base], "right") - 1,
                   0, len(BAND_LABELS) - 1)
    out = {"n_proofs": int(len(np.unique(c.inc_artifact[base]))), "at_k": {}}
    for k in ks:
        sel = ranks < k
        # joint histogram of (band, category) in one pass
        joint = np.bincount(bidx[sel] * len(STRUCT_CATS) + cat[sel],
                            minlength=len(BAND_LABELS) * len(STRUCT_CATS))
        joint = joint.reshape(len(BAND_LABELS), len(STRUCT_CATS))
        cc = joint.sum(axis=0)
        tot = max(int(cc.sum()), 1)
        band_rows = {}
        for bi, b in enumerate(BAND_LABELS):
            t2 = int(joint[bi].sum())
            if not t2:
                continue
            band_rows[b] = {"n": t2,
                            **{a: int(joint[bi, ai]) / t2
                               for ai, a in enumerate(STRUCT_CATS)},
                            "glue": int(joint[bi, 0] + joint[bi, 1]) / t2}
        out["at_k"][k] = {
            "n_items": int(cc.sum()),
            "composition": {a: int(cc[ai]) / tot
                            for ai, a in enumerate(STRUCT_CATS)},
            "glue": int(cc[0] + cc[1]) / tot,
            "by_target_depth": band_rows,
        }
    a1 = out["at_k"][1]
    out["RoleGlueAt1"] = a1["glue"]
    out["RoleMachineryAt1"] = a1["composition"]["machinery"]
    out["RoleTheoremAt1"] = a1["composition"]["theorem"]
    out["RoleDefinitionAt1"] = a1["composition"]["definition/construction"]
    return out


# ------------------------------------------------------- Channel B
def load_labels(label_dir, keymap):
    """Merge rater grade files into per-incidence grades.

    Returns (by_incidence, meta). Where several raters graded the same proof
    the MEDIAN grade is used, and the spread is reported so a disputed label
    is never silently averaged into a clean-looking number.
    """
    import glob
    import json
    import os

    per_rater = {}
    for f in sorted(glob.glob(os.path.join(label_dir, "grades_*.json"))):
        per_rater[os.path.basename(f)[7:-5]] = json.load(open(f))

    votes = defaultdict(list)          # incidence -> [grades]
    missing_votes = defaultdict(list)  # pid -> [bool]
    conf = Counter()
    for rname, rr in per_rater.items():
        for pid, ent in rr.items():
            k = keymap.get(pid)
            if k is None:
                continue
            missing_votes[pid].append(bool(ent.get("missing_key")))
            conf[ent.get("confidence", "?")] += 1
            for num, g in (ent.get("grades") or {}).items():
                inc = k["items"].get(str(num), k["items"].get(int(num)))
                if inc is None:
                    continue
                try:
                    votes[int(inc)].append(int(g))
                except (TypeError, ValueError):
                    continue

    by_inc, spread = {}, []
    for inc, vs in votes.items():
        by_inc[inc] = int(np.median(vs))
        if len(vs) > 1:
            spread.append(max(vs) - min(vs))
    meta = {
        "raters": sorted(per_rater),
        "n_rater_files": len(per_rater),
        "n_incidences_labelled": len(by_inc),
        "n_multi_rated": int(sum(1 for v in votes.values() if len(v) > 1)),
        "mean_spread_multi_rated": float(np.mean(spread)) if spread else None,
        "confidence": dict(conf),
        "missing_key_rate": (float(np.mean([np.mean(v) >= 0.5
                                            for v in missing_votes.values()]))
                             if missing_votes else None),
        "n_proofs_labelled": len(missing_votes),
    }
    return by_inc, meta, missing_votes


def semantic_metrics(c, base, ranks, grades_by_inc, keymap, ks=(1, 2, 4, 8)):
    """Graded-label scorecard for one (ranking, inclusion policy) cell.

    Everything here is conditional on the policy: a candidate the policy
    removed is not ranked, and if it was graded KEY that loss is counted as
    `SemanticKeyLostToPolicy` rather than quietly ignored.
    """
    pos = {int(p): i for i, p in enumerate(base)}
    rows, band_rows = [], defaultdict(list)
    recall = {k: [] for k in ks}
    recall_band = {k: defaultdict(list) for k in ks}
    support_recall = {k: [] for k in ks}
    key_total = key_lost = 0
    worst_misses, false_promotions = [], []

    for pid, meta in keymap.items():
        items = {int(n): int(inc) for n, inc in meta["items"].items()}
        graded = {n: grades_by_inc[i] for n, i in items.items()
                  if i in grades_by_inc}
        if not graded:
            continue
        live = {n: i for n, i in items.items() if i in pos and n in graded}
        keys_all = [n for n, g in graded.items() if g == 4]
        key_total += len(keys_all)
        key_lost += sum(1 for n in keys_all if n not in live)
        if not live:
            continue
        band = meta["band"]
        order = sorted(live, key=lambda n: ranks[pos[live[n]]])
        top_grade = graded[order[0]]
        rows.append(top_grade)
        band_rows[band].append(top_grade)

        live_keys = [n for n in keys_all if n in live]
        live_sup = [n for n, g in graded.items() if g >= 3 and n in live]
        rank_of = {n: j for j, n in enumerate(order)}
        for k in ks:
            if live_keys:
                r = sum(1 for n in live_keys if rank_of[n] < k) / len(live_keys)
                recall[k].append(r)
                recall_band[k][band].append(r)
            if live_sup:
                support_recall[k].append(
                    sum(1 for n in live_sup if rank_of[n] < k) / len(live_sup))

        # named diagnostics: what got buried, and what got wrongly promoted
        for n in live_keys:
            if rank_of[n] >= 4:
                worst_misses.append({
                    "proof": pid, "theorem": meta["declaration"], "band": band,
                    "target_depth": meta["depth"],
                    "name": c.names[int(c.inc_decl[live[n]])],
                    "rank": rank_of[n] + 1, "of": len(order), "grade": 4})
        if top_grade <= 1:
            false_promotions.append({
                "proof": pid, "theorem": meta["declaration"], "band": band,
                "target_depth": meta["depth"],
                "name": c.names[int(c.inc_decl[live[order[0]]])],
                "grade": int(top_grade), "grade_name": GRADE_NAMES[int(top_grade)],
                "system_says_glue": bool(c.inc_glue[live[order[0]]]),
                "best_available_grade": int(max(graded[n] for n in live))})

    n = len(rows)
    cnt = Counter(rows)

    def share(pred):
        k_ = sum(v for g, v in cnt.items() if pred(g))
        return {"value": k_ / n if n else float("nan"), "k": int(k_), "n": n,
                "ci95": _wilson(k_, n)}

    out = {
        "n_proofs_scored": n,
        "grade_at_1": {GRADE_NAMES[g]: cnt.get(g, 0) / n if n else 0.0
                       for g in (4, 3, 2, 1, 0)},
        "SemanticKeyMoveAt1": share(lambda g: g == 4),
        "SemanticKeyOrSupportAt1": share(lambda g: g >= 3),
        "SemanticLegitGlueAt1": share(lambda g: g == 2),
        "SemanticBadGlueAt1": share(lambda g: g == 1),
        "SemanticJunkAt1": share(lambda g: g == 0),
        "SemanticBadAt1": share(lambda g: g <= 1),
        "SemanticMeanGradeAt1": float(np.mean(rows)) if rows else float("nan"),
        "SemanticKeyLostToPolicy": {
            "value": key_lost / key_total if key_total else 0.0,
            "k": int(key_lost), "n": int(key_total)},
        "by_target_depth": {},
        "worst_misses": sorted(worst_misses,
                               key=lambda r: -r["rank"] / max(r["of"], 1))[:40],
        "false_promotions": sorted(false_promotions,
                                   key=lambda r: (r["grade"],
                                                  -r["best_available_grade"]))[:40],
    }
    for k in ks:
        out[f"SemanticKeyMoveRecall@{k}"] = (float(np.mean(recall[k]))
                                             if recall[k] else float("nan"))
        out[f"SemanticKeyOrSupportRecall@{k}"] = (
            float(np.mean(support_recall[k])) if support_recall[k]
            else float("nan"))
    for b, gs in band_rows.items():
        cb = Counter(gs)
        nb = len(gs)
        row = {"n": nb,
               "grade_at_1": {GRADE_NAMES[g]: cb.get(g, 0) / nb
                              for g in (4, 3, 2, 1, 0)},
               "SemanticKeyMoveAt1": cb.get(4, 0) / nb,
               "SemanticLegitGlueAt1": cb.get(2, 0) / nb,
               "SemanticBadGlueAt1": cb.get(1, 0) / nb,
               "SemanticJunkAt1": cb.get(0, 0) / nb,
               "SemanticBadAt1": (cb.get(1, 0) + cb.get(0, 0)) / nb,
               "SemanticMeanGradeAt1": float(np.mean(gs)),
               "ci95_bad": _wilson(cb.get(1, 0) + cb.get(0, 0), nb)}
        for k in ks:
            v = recall_band[k].get(b)
            row[f"SemanticKeyMoveRecall@{k}"] = (float(np.mean(v)) if v
                                                 else float("nan"))
        out["by_target_depth"][b] = row
    return out


def glue_classifier_report(c, grades_by_inc, keymap):
    """How good is our OWN glue flag, judged against graded labels?

    `inc_glue` (logic-only declaration OR machinery) is a claim about which
    candidates are plumbing. Raters grade plumbing as 2 (legitimate here) or
    1 (carries no idea); junk is 0. So:

      rater_glue  := grade in {1, 2}          plumbing-shaped
      rater_noise := grade == 0               machinery/automation noise

      GluePrecision = P(rater_glue | system glue)
      GlueRecall    = P(system glue | rater_glue)

    The full confusion matrix is returned as well, because precision/recall
    depend on where you draw the rater_glue line and the matrix does not.
    """
    inc_all = [int(i) for m in keymap.values() for i in m["items"].values()]
    inc_all = [i for i in inc_all if i in grades_by_inc]
    if not inc_all:
        return {}
    idx = np.array(inc_all)
    g = np.array([grades_by_inc[i] for i in inc_all])
    sysglue = c.inc_glue[idx]
    sysmach = c.inc_machinery[idx]

    conf = {}
    for gg in (4, 3, 2, 1, 0):
        m = g == gg
        conf[GRADE_NAMES[gg]] = {
            "n": int(m.sum()),
            "system_glue": int((m & sysglue).sum()),
            "system_machinery": int((m & sysmach).sum()),
        }
    rater_glue = (g == 1) | (g == 2)
    tp = int((sysglue & rater_glue).sum())
    fp = int((sysglue & ~rater_glue).sum())
    fn = int((~sysglue & rater_glue).sum())
    prec = tp / max(tp + fp, 1)
    rec = tp / max(tp + fn, 1)

    # what our glue flag actually costs: graded-KEY items we call glue
    key_flagged = int((sysglue & (g == 4)).sum())
    n_key = int((g == 4).sum())
    return {
        "n_labelled_candidates": len(inc_all),
        "confusion_by_grade": conf,
        "GluePrecision": {"value": prec, "k": tp, "n": tp + fp,
                          "ci95": _wilson(tp, tp + fp)},
        "GlueRecall": {"value": rec, "k": tp, "n": tp + fn,
                       "ci95": _wilson(tp, tp + fn)},
        "GlueF1": 2 * prec * rec / max(prec + rec, 1e-9),
        "KeyMovesFlaggedAsGlue": {"value": key_flagged / max(n_key, 1),
                                  "k": key_flagged, "n": n_key,
                                  "ci95": _wilson(key_flagged, n_key)},
        "grade_distribution": {GRADE_NAMES[gg]: int((g == gg).sum())
                               for gg in (4, 3, 2, 1, 0)},
    }


def rater_agreement(label_dir, keymap):
    """Agreement on the GRADED rubric, from the overlap batch.

    The previous panel measured agreement on binary picks only; a 0-4 scale
    needs exact-agreement, adjacent-agreement (|diff| <= 1) and a chance-
    corrected figure, because raters can agree on the ordering while
    disagreeing on where to cut.
    """
    import glob
    import json
    import os

    per_rater = {}
    for f in sorted(glob.glob(os.path.join(label_dir, "grades_*.json"))):
        per_rater[os.path.basename(f)[7:-5]] = json.load(open(f))

    cell = defaultdict(dict)      # (pid, num) -> rater -> grade
    for rn, rr in per_rater.items():
        for pid, ent in rr.items():
            for num, gg in (ent.get("grades") or {}).items():
                try:
                    cell[(pid, str(num))][rn] = int(gg)
                except (TypeError, ValueError):
                    pass
    pairs = [v for v in cell.values() if len(v) > 1]
    if not pairs:
        return {"n_overlap_candidates": 0}

    exact, adj, diffs, obs = [], [], [], []
    for v in pairs:
        gs = list(v.values())
        for i in range(len(gs)):
            for j in range(i + 1, len(gs)):
                d = abs(gs[i] - gs[j])
                exact.append(d == 0)
                adj.append(d <= 1)
                diffs.append(d)
                obs.append((gs[i], gs[j]))
    # chance-corrected on the observed marginal (quadratic-weighted kappa)
    a = np.array([x for x, _ in obs])
    b = np.array([y for _, y in obs])
    cats = np.arange(5)
    pa = np.array([(a == k).mean() for k in cats])
    pb = np.array([(b == k).mean() for k in cats])
    W = (cats[:, None] - cats[None, :]) ** 2 / 16.0
    O = np.zeros((5, 5))
    for x, y in obs:
        O[x, y] += 1
    O /= len(obs)
    E = np.outer(pa, pb)
    do = float((W * O).sum())
    de = float((W * E).sum())
    kappa = 1 - do / de if de > 0 else float("nan")
    return {
        "n_overlap_candidates": len(pairs),
        "n_pairs": len(exact),
        "raters": sorted(per_rater),
        "ExactAgreement": float(np.mean(exact)),
        "AdjacentAgreement": float(np.mean(adj)),
        "MeanAbsDiff": float(np.mean(diffs)),
        "QuadraticWeightedKappa": kappa,
        "diff_histogram": {str(d): int((np.array(diffs) == d).sum())
                           for d in range(5)},
    }
