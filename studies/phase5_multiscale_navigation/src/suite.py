#!/usr/bin/env python3
"""The evaluation suite: RANKING techniques x INCLUSION techniques x metrics,
against baselines that make the numbers interpretable.

Two knobs, deliberately kept separate:

  RANKING   the per-proof ordering over the COMPLETE record. Ours to get
            right; must be principled, simple, and robust to library growth.
  INCLUSION how much of that order a viewer admits (top-k, top-percentile,
            depth band, kind filter). Suggested by us, chosen by the user.

Baselines are the point. A ranking number means nothing without:
  RANDOM     shuffle each proof's citations (seeded) -- the floor
  REVERSE    anti-ranking (shallowest first) -- shows the signal is directional
  POPULAR    global citation count, descending -- the naive "importance"
  ORACLE     human-written citations first -- the CEILING achievable given
             that only 39.4% of what humans write is in the record at all

Metrics answer the owner's two standing worries:
  precision worry -- glue at rank 1, measured AGAINST the rate at which humans
                     themselves cite glue at that depth (a calibration ratio,
                     not an absolute)
  recall worry    -- human-written citations that fall BELOW the inclusion cut,
                     stratified by depth
"""
import json, os, glob
import numpy as np
from collections import defaultdict, Counter

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
PROV = os.path.join(SCRATCH, "prov")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
BANDS = [(0, 10), (10, 25), (25, 50), (50, 75), (75, 125), (125, 350)]
KS = (1, 2, 4, 8)


def main():
    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    nodes = np.load(os.path.join(DATA, "nodes.npz"))
    v8 = np.load(os.path.join(DATA, "v8_mask.npz"))
    names = json.load(open(os.path.join(DATA, "names.json")))
    idx = {nm: i for i, nm in enumerate(names)}

    a_col = inc["artifact"].astype(np.int64)
    d_col = inc["decl"].astype(np.int64)
    roles = inc["roles"]
    lb = inc["load_bearing"]
    in_sw = inc["in_stmt_world"]
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"].astype(np.float64)
    kind = nodes["kind"]
    n = len(depth)
    tgt = certifies[a_col]
    is_claim = v8["decl_is_claim"]
    logic_only = v8["decl_logic_only"]
    machinery = v8["machinery"]

    bi = np.where(lb & (tgt != d_col))[0]
    demote = logic_only[d_col[bi]] | machinery[bi]
    not_claim = ~is_claim[d_col[bi]]
    not_new = in_sw[bi]
    dep = depth[d_col[bi]]
    popularity = np.bincount(d_col[bi], minlength=n).astype(np.float64)[d_col[bi]]
    rng = np.random.default_rng(20260820)
    noise = rng.random(len(bi))

    def is_glue(d):
        return logic_only[d]

    # ---- ground truth ------------------------------------------------
    art_of = {d: a for a, d in enumerate(certifies)}
    by_art = defaultdict(list)
    for p in bi:
        by_art[a_col[p]].append(p)
    prov = {}
    for f in glob.glob(os.path.join(PROV, "*.json")):
        for e in json.load(open(f))["decls"]:
            if e.get("refs"):
                prov[e["name"]] = set(e["refs"])

    evals = []
    for nm, refs in prov.items():
        di = idx.get(nm)
        if di is None or di not in art_of:
            continue
        pl = by_art.get(art_of[di])
        if not pl:
            continue
        stmt = {names[d_col[p]] for p in pl if in_sw[p]}
        gt = {idx[c] for c in refs if c != nm and c not in stmt and c in idx}
        if not gt:
            continue
        evals.append((pl, gt, depth[di]))
    print(f"evaluable proofs: {len(evals):,}", flush=True)

    # human glue rate by depth band -- the calibration target
    human_glue = {}
    for b in BANDS:
        tot = g = 0
        for pl, gt, dth in evals:
            if not (b[0] <= dth < b[1]):
                continue
            for c in gt:
                tot += 1
                g += int(is_glue(c))
        human_glue[b] = (g / tot) if tot else None
    print("\nhuman glue rate by depth (the calibration target):", flush=True)
    for b in BANDS:
        v = human_glue[b]
        print(f"  {b[0]}-{b[1]:<5} {'-' if v is None else f'{v:.1%}'}", flush=True)

    # ---- RANKINGS -----------------------------------------------------
    gt_flag = np.zeros(len(bi), dtype=bool)
    pos_of_bi = {p: j for j, p in enumerate(bi)}
    for pl, gt, _ in evals:
        for p in pl:
            if d_col[p] in gt:
                gt_flag[pos_of_bi[p]] = True

    RANK = {
        "B0 random":            (noise,),
        "B1 reverse (shallow)": (dep,),
        "B2 popularity":        (-popularity,),
        "R3 pure depth":        (-dep,),
        "R4 introduced+depth":  (not_new.astype(np.int8), -dep),
        "R5 V8-faithful":       (not_claim.astype(np.int8), demote.astype(np.int8),
                                 not_new.astype(np.int8), -dep),
        "R6 V8+all kinds":      (demote.astype(np.int8), not_new.astype(np.int8), -dep),
        "B9 ORACLE (ceiling)":  (~gt_flag, -dep),
    }

    ranks = {}
    for lab, keys in RANK.items():
        order = np.lexsort(tuple(reversed(keys)) + (a_col[bi],))
        s = bi[order]
        aa = a_col[s]
        new = np.empty(len(s), bool); new[0] = True; new[1:] = aa[1:] != aa[:-1]
        st = np.where(new)[0]
        cnt = np.diff(np.append(st, len(s)))
        rk = np.concatenate([np.arange(c) for c in cnt])
        rr = np.empty(len(bi), dtype=np.int32)
        rr[order] = rk
        ranks[lab] = {p: rr[j] for j, p in enumerate(bi)}
        print(f"  ranked {lab}", flush=True)

    # ---- METRICS ------------------------------------------------------
    out = {"human_glue_by_depth": {f"{b[0]}-{b[1]}": human_glue[b] for b in BANDS},
           "rankings": {}}

    print(f"\n{'='*104}\nLOCAL METRICS  (inclusion = top-k per proof)\n{'='*104}",
          flush=True)
    print(f"{'ranking':<22} {'P@1':>7} {'MRR':>7} " +
          "".join(f"R@{k}".rjust(8) for k in KS) +
          f"{'glue@1':>9} {'calib':>8}", flush=True)
    for lab in RANK:
        rr = ranks[lab]
        p1, mrr, rec = [], [], {k: [] for k in KS}
        glue1 = []
        by_band = defaultdict(lambda: {"p1": [], "glue1": [], "missed": defaultdict(list)})
        for pl, gt, dth in evals:
            ordered = sorted(pl, key=lambda p: rr[p])
            dd = [d_col[p] for p in ordered]
            pos = {c: j for j, c in enumerate(dd)}
            hits = sorted(pos[c] for c in gt if c in pos)
            mrr.append(1.0 / (hits[0] + 1) if hits else 0.0)
            for k in KS:
                rec[k].append(len([h for h in hits if h < k]) / len(gt))
            good = dd[0] in gt
            p1.append(good)
            g1 = bool(is_glue(dd[0]))
            glue1.append(g1)
            b = next((b for b in BANDS if b[0] <= dth < b[1]), None)
            if b:
                by_band[b]["p1"].append(good)
                by_band[b]["glue1"].append(g1)
                for k in KS:
                    by_band[b]["missed"][k].append(
                        1.0 - len([h for h in hits if h < k]) / len(gt))
        gm = float(np.mean(glue1))
        overall_human = float(np.mean([is_glue(c) for _, gt, _ in evals for c in gt]))
        calib = gm / overall_human if overall_human else float("nan")
        row = {"p_at_1": float(np.mean(p1)), "mrr": float(np.mean(mrr)),
               **{f"recall@{k}": float(np.mean(rec[k])) for k in KS},
               "glue_at_1": gm, "glue_calibration_vs_human": calib,
               "by_band": {f"{b[0]}-{b[1]}": {
                   "p_at_1": float(np.mean(v["p1"])),
                   "glue_at_1": float(np.mean(v["glue1"])),
                   "human_glue": human_glue[b],
                   "missed_at_1": float(np.mean(v["missed"][1])),
                   "missed_at_4": float(np.mean(v["missed"][4])),
                   "n": len(v["p1"])} for b, v in sorted(by_band.items())}}
        out["rankings"][lab] = row
        print(f"{lab:<22} {row['p_at_1']:>6.1%} {row['mrr']:>7.3f} " +
              "".join(f"{row[f'recall@{k}']:>7.1%} " for k in KS) +
              f"{gm:>8.1%} {calib:>7.2f}x", flush=True)

    print("\n  glue@1 calibration: 1.00x means we surface glue at exactly the "
          "rate humans cite it.", flush=True)

    # ---- the owner's precision worry, stratified ----------------------
    print(f"\n{'='*104}\nPRECISION WORRY: glue at rank 1 vs the rate humans cite "
          f"glue, BY DEPTH\n{'='*104}", flush=True)
    hdr = f"{'ranking':<22}" + "".join(f"{b[0]}-{b[1]}".rjust(13) for b in BANDS)
    print(hdr, flush=True)
    print(f"{'(human rate)':<22}" +
          "".join((f"{human_glue[b]:.1%}" if human_glue[b] is not None else "-").rjust(13)
                  for b in BANDS), flush=True)
    for lab in RANK:
        cells = []
        for b in BANDS:
            v = out["rankings"][lab]["by_band"].get(f"{b[0]}-{b[1]}")
            cells.append((f"{v['glue_at_1']:.1%}" if v else "-").rjust(13))
        print(f"{lab:<22}" + "".join(cells), flush=True)

    # ---- the owner's recall worry, stratified -------------------------
    print(f"\n{'='*104}\nRECALL WORRY: share of human-written citations MISSED at "
          f"top-4, BY DEPTH\n{'='*104}", flush=True)
    print(hdr, flush=True)
    for lab in RANK:
        cells = []
        for b in BANDS:
            v = out["rankings"][lab]["by_band"].get(f"{b[0]}-{b[1]}")
            cells.append((f"{v['missed_at_4']:.1%}" if v else "-").rjust(13))
        print(f"{lab:<22}" + "".join(cells), flush=True)

    # ---- INCLUSION techniques ----------------------------------------
    print(f"\n{'='*104}\nINCLUSION TECHNIQUES (ranking fixed = R4 "
          f"introduced+depth)\n{'='*104}", flush=True)
    rr = ranks["R4 introduced+depth"]
    incl = {}
    # top-k
    for k in (1, 2, 4, 8):
        kept = miss = 0
        for pl, gt, dth in evals:
            ordered = sorted(pl, key=lambda p: rr[p])[:k]
            dd = {d_col[p] for p in ordered}
            kept += len(gt & dd); miss += len(gt - dd)
        incl[f"top-{k}"] = {"gt_kept": kept, "gt_missed": miss,
                            "gt_recall": kept / (kept + miss)}
    # top percentile of each proof
    for pctl in (0.10, 0.25, 0.50):
        kept = miss = 0
        for pl, gt, dth in evals:
            ordered = sorted(pl, key=lambda p: rr[p])
            m = max(1, int(np.ceil(pctl * len(ordered))))
            dd = {d_col[p] for p in ordered[:m]}
            kept += len(gt & dd); miss += len(gt - dd)
        incl[f"top-{int(pctl*100)}%"] = {"gt_kept": kept, "gt_missed": miss,
                                         "gt_recall": kept / (kept + miss)}
    # kind filters
    for lab2, f in (("theorems only", lambda d: is_claim[d] and kind[d] == 0),
                    ("definitions only", lambda d: kind[d] in (1, 2, 5, 6, 7)),
                    ("non-glue only", lambda d: not logic_only[d])):
        kept = miss = 0
        for pl, gt, dth in evals:
            dd = {d_col[p] for p in pl if f(d_col[p])}
            kept += len(gt & dd); miss += len(gt - dd)
        incl[lab2] = {"gt_kept": kept, "gt_missed": miss,
                      "gt_recall": kept / (kept + miss)}
    print(f"{'inclusion':<22} {'human citations kept':>22} {'missed':>10} "
          f"{'recall':>9}", flush=True)
    for lab2, v in incl.items():
        print(f"{lab2:<22} {v['gt_kept']:>22,} {v['gt_missed']:>10,} "
              f"{v['gt_recall']:>8.1%}", flush=True)
    out["inclusion"] = incl

    with open(os.path.join(DATA, "suite_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten data/suite_results.json", flush=True)


if __name__ == "__main__":
    main()
