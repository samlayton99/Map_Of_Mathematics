#!/usr/bin/env python3
"""Deterministically mine every failure of every viable ranking.

The point: we have a deterministic system and graded ground truth, and we have
never sat down and asked *why* an individual case went wrong. Aggregate scores
hide that. This extracts every failure with enough detail to diagnose it
without re-deriving anything.

Failure classes:

  PRECISION  an item graded <=1 sits at rank 1, or inside the top 4.
  RECALL     an item graded 4 (or >=3) sits below rank 4.
  GRADIENT   a case living in a score region where usefulness INCREASES as the
             score falls -- i.e. the score is locally anti-correlated with
             truth. These are the most diagnostic failures.

For every failure we emit the full deterministic state: the theorem, every
candidate, every signal that any ranking reads, all three rater grades, the
score and rank the method assigned, and -- for precision failures -- the
`blame` analysis: which single factor caused the bad item to outrank the best
graded item, computed by swapping one factor at a time.

Output: one JSON bank per method under review/failures/.
"""
import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

from mathmap_eval import navigation as N      # noqa: E402
from mathmap_eval import rankings as R        # noqa: E402
from mathmap_eval.corpus import get_corpus    # noqa: E402

SEALED = os.path.join(ROOT, "review", "sealed_r1")
OUT = os.path.join(ROOT, "review", "failures")
ROLE_NAMES = ["applied", "let-value", "explicit-arg", "implicit-arg",
              "instance-slot", "strict-implicit", "type-annotation",
              "unresolved"]
KIND_NAMES = ["theorem", "def", "inductive", "constructor", "recursor",
              "opaque", "quot", "axiom", "?"]
GRADE = {4: "CORE", 3: "MAJOR", 2: "LEGIT_GLUE", 1: "BAD_GLUE", 0: "JUNK"}


def load_labels(keymap, split):
    import glob
    votes, causes, moves = defaultdict(list), defaultdict(list), defaultdict(list)
    for f in sorted(glob.glob(os.path.join(SEALED, "grades_*.json"))):
        rater = os.path.basename(f)[7:-5]
        for pid, ent in json.load(open(f)).items():
            if pid not in keymap or keymap[pid]["split"] != split:
                continue
            if ent.get("moves"):
                moves[pid].append({"rater": rater, "moves": ent["moves"]})
            for num, g in (ent.get("grades") or {}).items():
                inc = keymap[pid]["items"].get(str(num))
                if inc is None:
                    continue
                try:
                    votes[int(inc)].append((rater, int(g)))
                except (TypeError, ValueError):
                    pass
            for num, cz in (ent.get("causes") or {}).items():
                inc = keymap[pid]["items"].get(str(num))
                if inc is not None:
                    causes[int(inc)].append(str(cz))
    return votes, causes, moves


def main():
    c = get_corpus()
    dmax = float(c.node_depth.max())
    keymap = json.load(open(os.path.join(SEALED, "keymap.json")))
    split = sys.argv[1] if len(sys.argv) > 1 else "TEST-R"
    votes, causes, moves = load_labels(keymap, split)
    grades = {i: int(np.median([g for _, g in v])) for i, v in votes.items()}
    kr = {p: v for p, v in keymap.items() if v["split"] == split}
    base = np.where(c.universe("U1D"))[0]
    pos = {int(p): i for i, p in enumerate(base)}

    # frozen-foundation rarity: append-safe by construction
    m50 = c.inc_d_target[base] <= 50
    pop50 = np.bincount(c.inc_decl[base[m50]], minlength=c.n_nodes).astype(float)
    n50 = float(len(np.unique(c.inc_artifact[base[m50]])))
    IDF50 = np.maximum(np.log(n50 / np.maximum(pop50, 1.0)), 0.0)

    def ROLE(b):
        r = c.inc_roles[b]
        return np.where(r[:, 0] > 0, 1.0,
                        np.where((r[:, 1] > 0) | (r[:, 2] > 0), 0.7, 0.5))

    def DEP(b):
        return 0.20 + 0.80 * c.inc_d_cite[b] / dmax

    # factor tables, so `blame` can swap exactly one factor at a time
    FACTORS = {
        "role":   lambda b: ROLE(b),
        "depth":  lambda b: DEP(b),
        "rarity_frozen": lambda b: IDF50[c.inc_decl[b]],
        "rarity_live":   lambda b: c.decl_idf[c.inc_decl[b]],
        "stmt":   lambda b: np.where(c.inc_in_stmt_world[b], 1.0, 1.5),
    }
    METHODS = {
        "M1_role_x_frozen_rarity": ["role", "rarity_frozen"],
        "M2_role_x_depth":         ["role", "depth"],
        "M3_promoted_composite":   ["role", "stmt", "depth", "rarity_live"],
    }

    def score_of(method, b):
        s = np.ones(len(b))
        for f in METHODS[method]:
            s = s * FACTORS[f](b)
        return s

    def signals(inc):
        di = int(c.inc_decl[inc])
        r = c.inc_roles[inc]
        return {
            "name": c.names[di],
            "kind": KIND_NAMES[int(c.node_kind[di])],
            "cited_depth": int(c.inc_d_cite[inc]),
            "role": ROLE_NAMES[int(np.argmax(r))],
            "roles_all": [ROLE_NAMES[j] for j in range(8) if r[j] > 0],
            "in_statement": bool(c.inc_in_stmt_world[inc]),
            "auto_generated": bool(c.node_gen[di]),
            "library_in_degree": int(c.node_in_degree[di]),
            "rarity_live": round(float(c.decl_idf[di]), 3),
            "rarity_frozen": round(float(IDF50[di]), 3),
            "system_says_glue": bool(c.inc_glue[inc]),
            "grades_by_rater": [{"rater": rr, "grade": g, "name": GRADE[g]}
                                for rr, g in votes.get(inc, [])],
            "median_grade": grades.get(inc),
            "median_grade_name": GRADE.get(grades.get(inc, -1), "?"),
            "rater_disagreement": (max(g for _, g in votes[inc])
                                   - min(g for _, g in votes[inc]))
            if inc in votes else None,
            "defect_causes": causes.get(inc, []),
        }

    os.makedirs(OUT, exist_ok=True)
    summary = {}
    for method in METHODS:
        b = base
        sc = score_of(method, b)
        # rank within proof, descending score
        order = np.lexsort((np.arange(len(b)), -sc, c.inc_artifact[b]))
        s = b[order]
        aa = c.inc_artifact[s]
        new = np.empty(len(s), bool); new[0] = True; new[1:] = aa[1:] != aa[:-1]
        starts = np.where(new)[0]
        counts = np.diff(np.append(starts, len(s)))
        rk = np.concatenate([np.arange(x) for x in counts])
        ranks = np.empty(len(b), np.int32); ranks[order] = rk

        bank = {"method": method,
                "factors": METHODS[method],
                "split": split,
                "append_safe": "rarity_live" not in METHODS[method],
                "precision_failures": [],
                "recall_failures": [],
                "gradient_reversals": []}

        for pid, meta in kr.items():
            incs = [int(x) for x in meta["items"].values() if int(x) in pos
                    and int(x) in grades]
            if not incs:
                continue
            incs.sort(key=lambda i: ranks[pos[i]])
            g = [grades[i] for i in incs]
            ctx = {"proof": pid, "theorem": meta["declaration"],
                   "target_depth": meta["depth"], "band": meta["band"],
                   "n_candidates": len(incs),
                   "rater_moves": moves.get(pid, []),
                   "ranked": [dict(rank=j + 1,
                                   score=round(float(sc[pos[i]]), 4),
                                   **signals(i)) for j, i in enumerate(incs)]}

            # --- PRECISION: a defect at rank 1, or inside top 4
            if g[0] <= 1:
                best = max(range(len(incs)), key=lambda j: g[j])
                bad, good = incs[0], incs[best]
                blame = {}
                for f in METHODS[method]:
                    swapped = 1.0
                    for f2 in METHODS[method]:
                        v = FACTORS[f2](np.array([bad if f2 != f else good]))[0]
                        swapped *= v
                    blame[f] = {
                        "bad_value": round(float(FACTORS[f](np.array([bad]))[0]), 4),
                        "good_value": round(float(FACTORS[f](np.array([good]))[0]), 4),
                        "score_if_bad_had_goods_value": round(float(swapped), 4),
                        "would_fix": bool(swapped < sc[pos[good]]),
                    }
                bank["precision_failures"].append({
                    **ctx, "failure": "defect_at_rank_1",
                    "bad_grade": GRADE[g[0]],
                    "best_available_grade": GRADE[g[best]],
                    "best_available_rank": best + 1,
                    "score_gap": round(float(sc[pos[bad]] - sc[pos[good]]), 4),
                    "blame": blame})
            elif sum(1 for x in g[:4] if x <= 1) >= 3 and len(incs) >= 6:
                bank["precision_failures"].append({
                    **ctx, "failure": "top4_mostly_defects",
                    "top4_grades": [GRADE[x] for x in g[:4]]})

            # --- RECALL: a CORE move below rank 4
            for j, i in enumerate(incs):
                if grades[i] == 4 and j >= 4:
                    bank["recall_failures"].append({
                        **ctx, "failure": "core_move_buried",
                        "buried_rank": j + 1,
                        "buried_name": c.names[int(c.inc_decl[i])],
                        "outranked_by": [dict(rank=k + 1,
                                              name=c.names[int(c.inc_decl[incs[k]])],
                                              grade=GRADE[grades[incs[k]]])
                                         for k in range(j)]})

            # --- GRADIENT: usefulness rises as rank falls, locally
            useful = [1 if x >= 2 else 0 for x in g]
            n = len(useful)
            if n >= 6:
                half = n // 2
                top_rate = sum(useful[:half]) / half
                bot_rate = sum(useful[half:]) / (n - half)
                if bot_rate > top_rate + 0.25:
                    bank["gradient_reversals"].append({
                        **ctx, "failure": "usefulness_increases_down_the_list",
                        "top_half_useful_rate": round(top_rate, 3),
                        "bottom_half_useful_rate": round(bot_rate, 3)})

        for k in ("precision_failures", "recall_failures", "gradient_reversals"):
            bank[k].sort(key=lambda r: (r.get("target_depth", 0)))
        summary[method] = {k: len(bank[k]) for k in
                           ("precision_failures", "recall_failures",
                            "gradient_reversals")}
        summary[method]["n_proofs"] = len(kr)
        summary[method]["append_safe"] = bank["append_safe"]
        with open(os.path.join(OUT, f"{method}.json"), "w") as f:
            json.dump(bank, f, indent=1, default=float)
        print(f"  {method:<28} precision {summary[method]['precision_failures']:>4} "
              f"recall {summary[method]['recall_failures']:>4} "
              f"gradient {summary[method]['gradient_reversals']:>4}", flush=True)

    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(f"\nwritten {OUT}/")


if __name__ == "__main__":
    main()
