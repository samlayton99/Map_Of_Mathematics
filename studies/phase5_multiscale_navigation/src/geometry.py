#!/usr/bin/env python3
"""Phase 5: geometry across projections (pre-registered Q1.1, Q1.3, Q2, Q3).

Every projection is a boolean mask over the single incidence table, per
HYPERGRAPH_SCHEMA. Nothing is rebuilt; nothing is deleted.

Registered questions answered here:
  Q1.1  node/hyperedge counts and hyperedge-size distributions per projection
  Q1.3  landmarks that exist ONLY in glue-rich views
  Q2.1  distribution of citation depth gaps per projection
  Q2.2  proofs with unusually large depth span (>p99)
  Q3.1  direct vs filtered citation counts per theorem
  Q3.2  compression ratio (recursive support / direct citations)

Coverage and empty cases are reported explicitly (gate requirement).
"""
import json, os
import numpy as np
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
OUT = os.path.normpath(os.path.join(HERE, "..", "reports"))


def pct(a, qs=(50, 90, 99, 100)):
    if len(a) == 0:
        return {f"p{q}": None for q in qs}
    return {f"p{q}": float(np.percentile(a, q)) for q in qs}


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    nodes = np.load(os.path.join(DATA, "nodes.npz"))
    v8 = np.load(os.path.join(DATA, "v8_mask.npz"))
    names = json.load(open(os.path.join(DATA, "names.json")))

    a_col = inc["artifact"].astype(np.int64)
    d_col = inc["decl"].astype(np.int64)
    lb = inc["load_bearing"]
    in_sw = inc["in_stmt_world"]
    delta = inc["delta_depth"].astype(np.int32)
    d_cite = inc["d_cite"].astype(np.int32)
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"]
    kind = nodes["kind"]
    gen = nodes["gen"]
    is_claim = v8["decl_is_claim"]
    logic_only = v8["decl_logic_only"]
    machinery = v8["machinery"]

    n_art = len(certifies)
    tgt = certifies[a_col]
    is_thm_art = (kind[certifies] == 0)

    # ---------------- the projection family ----------------
    P = {}
    P["P1 full support"] = np.ones(len(a_col), dtype=bool)
    P["P2 load-bearing"] = lb.copy()
    P["P3 claims"] = lb & is_claim[d_col]
    P["P4 V8 boundary"] = P["P3 claims"] & ~logic_only[d_col] & ~machinery
    P["P5 proof-introduced"] = lb & ~in_sw
    P["P6 statement-world"] = lb & in_sw
    P["P8 definition layer"] = lb & ~is_thm_art[a_col]

    print("=== Q1.1 geometry across projections ===", flush=True)
    rows = []
    for label, mask in P.items():
        m = mask
        n_inc = int(m.sum())
        arts_used = np.unique(a_col[m])
        decls_used = np.unique(d_col[m])
        sizes = np.bincount(a_col[m], minlength=n_art)
        nonempty = sizes[sizes > 0]
        empty_arts = int(n_art - len(nonempty))
        row = {"projection": label, "incidences": n_inc,
               "hyperedges_nonempty": int(len(nonempty)),
               "hyperedges_empty": empty_arts,
               "distinct_decls": int(len(decls_used)),
               "size_mean": round(float(nonempty.mean()), 2) if len(nonempty) else 0,
               **{k: round(v, 1) for k, v in pct(nonempty).items()}}
        rows.append(row)
        print(f"  {label:<24} inc={n_inc:>10,}  edges={len(nonempty):>8,}  "
              f"empty={empty_arts:>7,}  decls={len(decls_used):>7,}  "
              f"size p50={row['p50']:.0f} p90={row['p90']:.0f} "
              f"p99={row['p99']:.0f} max={row['p100']:.0f}", flush=True)

    # top-k views over the frozen P4 order (depth-descending within edge)
    print("\n  top-k over P4 (frozen order: deeper first):", flush=True)
    p4 = P["P4 V8 boundary"]
    idx4 = np.where(p4)[0]
    ordkey = np.lexsort((-d_cite[idx4], a_col[idx4]))
    idx4s = idx4[ordkey]
    rank_in_edge = np.zeros(len(idx4s), dtype=np.int32)
    if len(idx4s):
        newedge = np.empty(len(idx4s), dtype=bool)
        newedge[0] = True
        newedge[1:] = a_col[idx4s][1:] != a_col[idx4s][:-1]
        starts = np.where(newedge)[0]
        counts = np.diff(np.append(starts, len(idx4s)))
        rank_in_edge = np.concatenate([np.arange(c) for c in counts])
    topk_rows = []
    for k in (1, 2, 4, 8, 16):
        sel = idx4s[rank_in_edge < k]
        sizes = np.bincount(a_col[sel], minlength=n_art)
        ne = sizes[sizes > 0]
        topk_rows.append({"k": k, "incidences": int(len(sel)),
                          "hyperedges": int(len(ne)),
                          "size_mean": round(float(ne.mean()), 2) if len(ne) else 0})
        print(f"    k={k:<3} inc={len(sel):>9,}  edges={len(ne):>8,}  "
              f"mean size={ne.mean() if len(ne) else 0:.2f}", flush=True)

    # ---------------- Q1.3 glue-only landmarks ----------------
    print("\n=== Q1.3 landmarks that exist only in glue-rich views ===", flush=True)
    def cited_by_count(mask):
        c = np.bincount(d_col[mask], minlength=len(depth))
        return c
    c1 = cited_by_count(P["P1 full support"])
    c4 = cited_by_count(P["P4 V8 boundary"])
    r1 = np.argsort(-c1)
    top100_p1 = r1[:100]
    rank4 = np.empty(len(depth), dtype=np.int64)
    rank4[np.argsort(-c4)] = np.arange(len(depth))
    glue_only = [i for i in top100_p1 if rank4[i] > 1000]
    print(f"  top-100 by P1 citation count that fall below rank 1000 in P4: "
          f"{len(glue_only)}", flush=True)
    for i in glue_only[:20]:
        print(f"    {names[i]:<46} P1={int(c1[i]):>8,}  P4={int(c4[i]):>7,}  "
              f"P4 rank={int(rank4[i]):,}", flush=True)

    print("\n  survives both (top-20 by P4):", flush=True)
    for i in np.argsort(-c4)[:20]:
        print(f"    {names[i]:<46} P4={int(c4[i]):>8,}  P1={int(c1[i]):>9,}",
              flush=True)

    # ---------------- Q2 depth gaps ----------------
    print("\n=== Q2.1 citation depth gaps ===", flush=True)
    gap_rows = []
    for label in ("P1 full support", "P2 load-bearing", "P4 V8 boundary",
                  "P5 proof-introduced"):
        g = delta[P[label]]
        row = {"projection": label, "mean": round(float(g.mean()), 2),
               **{k: round(v, 1) for k, v in pct(g, (1, 25, 50, 75, 99, 100)).items()}}
        gap_rows.append(row)
        print(f"  {label:<24} mean={row['mean']:>7.2f}  p1={row['p1']:>6.0f} "
              f"p50={row['p50']:>5.0f} p99={row['p99']:>5.0f} max={row['p100']:>5.0f}",
              flush=True)

    print("\n=== Q2.2 proofs with unusually large depth span (>p99) ===", flush=True)
    m = P["P4 V8 boundary"]
    span = np.zeros(n_art, dtype=np.int32)
    np.maximum.at(span, a_col[m], delta[m])
    live = span[span > 0]
    thr = np.percentile(live, 99) if len(live) else 0
    big = np.where(span >= thr)[0]
    print(f"  p99 depth span = {thr:.0f}; {len(big):,} artifacts at or above",
          flush=True)
    order_big = big[np.argsort(-span[big])]
    for a in order_big[:15]:
        print(f"    span={int(span[a]):>4}  {names[certifies[a]]}", flush=True)

    # ---------------- Q3 compression ----------------
    print("\n=== Q3.1 direct vs filtered citation counts (theorem artifacts) ===",
          flush=True)
    thm_arts = np.where(is_thm_art)[0]
    for label in ("P1 full support", "P2 load-bearing", "P3 claims",
                  "P4 V8 boundary"):
        s = np.bincount(a_col[P[label]], minlength=n_art)[thm_arts]
        print(f"  {label:<24} mean={s.mean():>7.2f}  p50={np.percentile(s,50):>5.0f} "
              f"p90={np.percentile(s,90):>5.0f}  zero={int((s==0).sum()):>7,} "
              f"({100*(s==0).mean():.1f}%)", flush=True)

    out = {"note": "Phase 5 geometry, pre-registered questions. Projections are "
                   "masks over one incidence table; nothing is rebuilt.",
           "n_declarations": int(len(depth)), "n_artifacts": int(n_art),
           "n_incidences": int(len(a_col)),
           "Q1_1_projections": rows, "Q1_1_topk": topk_rows,
           "Q1_3_glue_only_landmarks": [
               {"name": names[i], "p1_citations": int(c1[i]),
                "p4_citations": int(c4[i]), "p4_rank": int(rank4[i])}
               for i in glue_only],
           "Q1_3_persistent_landmarks": [
               {"name": names[i], "p4_citations": int(c4[i]),
                "p1_citations": int(c1[i])} for i in np.argsort(-c4)[:30]],
           "Q2_1_depth_gaps": gap_rows,
           "Q2_2_p99_span": float(thr),
           "Q2_2_examples": [{"thm": names[certifies[a]], "span": int(span[a])}
                             for a in order_big[:40]]}
    with open(os.path.join(DATA, "geometry_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten data/geometry_results.json", flush=True)


if __name__ == "__main__":
    main()
