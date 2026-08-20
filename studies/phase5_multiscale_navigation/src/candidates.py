#!/usr/bin/env python3
"""V8-alt: five frozen candidate rankings, evaluated on Q1 (coverage) and
Q2 (precision/keyness) against human-written ground truth.

Per PRE_REGISTRATION_V8ALT.md. Binding: every candidate is an ORDERING over
the complete load-bearing incidence record. Nothing is deleted; what V8
filtered out is merely ranked last.

Ground truth: Lean's elaborator records which identifiers the human wrote in
each declaration's source. Proof-written citations = those references minus
the ones already resolved from the declaration's own statement. The answer key
is NEVER filtered by any candidate's own predicate (the circular-harness
defect found in the last trial is not repeated).
"""
import json, os, glob
import numpy as np
from collections import defaultdict

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
PROV = os.path.join(SCRATCH, "prov")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
KS = (1, 2, 4, 8, 16)


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
    print(f"base incidences: {len(bi):,}", flush=True)

    demote = (logic_only[d_col[bi]] | machinery[bi])
    not_claim = ~is_claim[d_col[bi]]
    not_new = in_sw[bi]
    dep = depth[d_col[bi]]
    r = roles[bi]
    m_role = np.where(r[:, 0] > 0, 1.0, np.where((r[:, 1] > 0) | (r[:, 2] > 0), 0.7, 0.5))
    m_stmt = np.where(in_sw[bi], 1.0, 1.5)
    dfc = np.bincount(d_col[bi], minlength=n).astype(np.float64)
    n_proofs = float(len(np.unique(a_col[bi])))
    idf = np.maximum(np.log(n_proofs / np.maximum(dfc, 1.0)), 0.0)[d_col[bi]]
    dmax = float(depth.max())
    w5 = m_role * m_stmt * (0.20 + 0.80 * dep / dmax) * idf

    # frozen candidate sort keys (ascending). Nothing removed; only ordered.
    CAND = {
        "C1 V8-faithful":        (not_claim.astype(np.int8), demote.astype(np.int8),
                                  not_new.astype(np.int8), -dep),
        "C2 V8 + all kinds":     (demote.astype(np.int8), not_new.astype(np.int8), -dep),
        "C3 pure depth":         (-dep,),
        "C4 introduced+depth":   (not_new.astype(np.int8), -dep),
        "C5 phase5 composite":   (-w5,),
    }

    # rank within each proof, for every candidate
    ranks = {}
    for lab, keys in CAND.items():
        order = np.lexsort(tuple(reversed(keys)) + (a_col[bi],))
        s = bi[order]
        aa = a_col[s]
        new = np.empty(len(s), bool); new[0] = True; new[1:] = aa[1:] != aa[:-1]
        st = np.where(new)[0]
        cnt = np.diff(np.append(st, len(s)))
        rk = np.concatenate([np.arange(c) for c in cnt])
        rr = np.empty(len(bi), dtype=np.int32)
        pos = np.empty(len(bi), dtype=np.int64)
        pos[order] = np.arange(len(bi))
        rr[order] = rk
        ranks[lab] = rr
        print(f"  ranked {lab}", flush=True)

    # ---- ground truth ------------------------------------------------
    prov = {}
    for f in glob.glob(os.path.join(PROV, "*.json")):
        for e in json.load(open(f))["decls"]:
            if e.get("refs"):
                prov[e["name"]] = set(e["refs"])
    print(f"declarations with provenance: {len(prov):,}", flush=True)

    art_of = {}
    for ai, dcl in enumerate(certifies):
        art_of[dcl] = ai
    # incidence lookup per artifact
    by_art = defaultdict(list)
    for p, i in enumerate(bi):
        by_art[a_col[i]].append(p)

    evals = []
    for nm, refs in prov.items():
        di = idx.get(nm)
        if di is None or di not in art_of:
            continue
        ai = art_of[di]
        pos_list = by_art.get(ai)
        if not pos_list:
            continue
        # proof-written = human-written refs minus the statement's own refs
        stmt = set()
        for p in pos_list:
            i = bi[p]
            if in_sw[i]:
                stmt.add(names[d_col[i]])
        gt = {c for c in refs if c != nm and c not in stmt}
        gt_ids = {idx[c] for c in gt if c in idx}
        if not gt_ids:
            continue
        evals.append((ai, pos_list, gt_ids, depth[di]))
    print(f"evaluable proofs: {len(evals):,}", flush=True)

    out = {"n_evaluable": len(evals), "candidates": {}}
    BANDS = [(0, 10), (10, 25), (25, 50), (50, 75), (75, 125), (125, 350)]

    print(f"\n{'candidate':<22} {'Q1 present':>11} {'MRR':>7} " +
          " ".join(f"R@{k:<3}".rjust(7) for k in KS) + f" {'P@1':>7}", flush=True)
    for lab in CAND:
        rr = ranks[lab]
        present, mrr, rec = [], [], {k: [] for k in KS}
        p1, p1_by_band = [], defaultdict(list)
        p1_def, p1_thm = [], []
        for ai, pos_list, gt_ids, dth in evals:
            byrank = sorted(pos_list, key=lambda p: rr[p])
            ordered = [d_col[bi[p]] for p in byrank]
            oset = set(ordered)
            hit = gt_ids & oset
            present.append(len(hit) / len(gt_ids))
            pos_of = {c: j for j, c in enumerate(ordered)}
            rs = sorted(pos_of[c] for c in hit) if hit else []
            mrr.append(1.0 / (rs[0] + 1) if rs else 0.0)
            for k in KS:
                rec[k].append(len([x for x in rs if x < k]) / len(gt_ids))
            top = ordered[0]
            good = top in gt_ids
            p1.append(good)
            for lo, hi in BANDS:
                if lo <= dth < hi:
                    p1_by_band[(lo, hi)].append(good)
            (p1_def if kind[top] in (1, 2, 5, 6, 7) else p1_thm).append(good)
        row = {"q1_present": float(np.mean(present)), "mrr": float(np.mean(mrr)),
               **{f"recall@{k}": float(np.mean(rec[k])) for k in KS},
               "p_at_1": float(np.mean(p1)),
               "p_at_1_when_top_is_definition": float(np.mean(p1_def)) if p1_def else None,
               "n_top_is_definition": len(p1_def),
               "p_at_1_when_top_is_theorem": float(np.mean(p1_thm)) if p1_thm else None,
               "p_at_1_by_theorem_depth": {f"{lo}-{hi}": [float(np.mean(v)), len(v)]
                                           for (lo, hi), v in sorted(p1_by_band.items())}}
        out["candidates"][lab] = row
        print(f"{lab:<22} {row['q1_present']:>10.1%} {row['mrr']:>7.3f} " +
              " ".join(f"{row[f'recall@{k}']:>6.1%} " for k in KS) +
              f"{row['p_at_1']:>6.1%}", flush=True)

    print(f"\n=== Q2.2 does restoring definitions cost precision? ===", flush=True)
    for lab in CAND:
        r = out["candidates"][lab]
        d_ = r["p_at_1_when_top_is_definition"]
        t_ = r["p_at_1_when_top_is_theorem"]
        print(f"  {lab:<22} top-is-definition n={r['n_top_is_definition']:>5} "
              f"P@1={d_ if d_ is None else f'{d_:.1%}':>7}   "
              f"top-is-theorem P@1={t_ if t_ is None else f'{t_:.1%}':>7}", flush=True)

    print(f"\n=== Q2.3 P@1 stratified by theorem depth (the owner's hypothesis) ===",
          flush=True)
    hdr = "  " + f"{'candidate':<22}" + "".join(f"{lo}-{hi}".rjust(11) for lo, hi in BANDS)
    print(hdr, flush=True)
    for lab in CAND:
        cells = []
        for lo, hi in BANDS:
            v = out["candidates"][lab]["p_at_1_by_theorem_depth"].get(f"{lo}-{hi}")
            cells.append(f"{v[0]:.0%}({v[1]})".rjust(11) if v and v[1] else "-".rjust(11))
        print(f"  {lab:<22}" + "".join(cells), flush=True)

    with open(os.path.join(DATA, "candidates_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten data/candidates_results.json", flush=True)


if __name__ == "__main__":
    main()
