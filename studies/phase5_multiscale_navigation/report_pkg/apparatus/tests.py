"""Self-tests for the apparatus. Run: python -m mathmap_eval.tests

These are invariants, not examples. Each one has caught (or would have caught)
a real bug in this program:

  T1  every ranking is a permutation within each proof -- nothing deleted.
      (principle 1: rankings order, they never filter)
  T2  candidate coverage is identical across rankings on a fixed universe.
      (the check that proved "nothing was removed" -- and, per the audit, all
       it proves is that the universe was shared)
  T3  every slider policy is nested as its parameter opens.
  T4  components are MONOTONE NON-INCREASING as edges are admitted.
      (this exact invariant was violated by a partition-accumulation bug in
       the first bridge-enrichment run; components grew from 255k to 450k)
  T5  the SourceOracle is optimal for SourceHit@1 among all rankings.
      (if a candidate beats the oracle, the oracle is misdefined)
  T6  the SourceOracle's ceiling equals candidate coverage, not 1.0.
      (audit item 2: a sub-100% source oracle measures COVERAGE failure)
  T7  universes nest: U1 subset of U1D subset of U0.
  T8  metric names never cross families (no Semantic* is computed here).
"""
from __future__ import annotations

import sys

import numpy as np

from . import inclusions as I
from . import metrics as M
from . import rankings as R
from .corpus import get_corpus

FAILED = []


def check(name, cond, detail=""):
    ok = bool(cond)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILED.append(name)
    return ok


def main(universe="U1", sample_proofs=400):
    c = get_corpus()
    base = np.where(c.universe(universe))[0]
    print(f"corpus: {c.n_incidences:,} incidences, universe {universe} "
          f"= {len(base):,}\n")

    # ---- T7 universes nest
    u1 = c.universe("U1"); u1d = c.universe("U1D"); u0 = c.universe("U0")
    check("T7 universes nest U1 <= U1D <= U0",
          np.all(u1 <= u1d) and np.all(u1d <= u0),
          f"{u1.sum():,} <= {u1d.sum():,} <= {u0.sum():,}")

    # small deterministic slice for the per-proof invariants
    rng = np.random.default_rng(0)
    arts = np.unique(c.inc_artifact[base])
    keep_arts = set(rng.choice(arts, min(sample_proofs, len(arts)),
                               replace=False).tolist())
    sl = base[np.isin(c.inc_artifact[base], list(keep_arts))]

    sizes = np.bincount(c.inc_artifact[sl])
    for nm in R.names():
        spec = R.get(nm)
        ranks = spec.ranks_within_proof(c, sl)
        # T1: within each proof ranks are exactly 0..n-1
        ok = True
        for a in keep_arts:
            m = c.inc_artifact[sl] == a
            if m.sum() == 0:
                continue
            r = np.sort(ranks[m])
            if not np.array_equal(r, np.arange(len(r))):
                ok = False
                break
        check(f"T1 {nm} is a permutation within every proof", ok)

    # ---- T2 coverage identical across rankings (fixed universe)
    evalset = c.evaluation_set(universe)
    covs = []
    for nm in R.names():
        ranks = R.get(nm).ranks_within_proof(c, base)
        by = dict(zip(base.tolist(), ranks.tolist()))
        s = M.source_metrics(c, evalset, by, ks=(1,))
        # "present anywhere" = recall at the full list length
        present = []
        for ai, pl, gt, _ in evalset:
            dd = {c.inc_decl[p] for p in pl}
            present.append(len(gt & dd) / len(gt))
        covs.append(round(float(np.mean(present)), 10))
    check("T2 candidate coverage identical across rankings",
          len(set(covs)) == 1, f"coverage={covs[0]:.4f}")

    # ---- T3 nested sliders
    ranks = R.get("R_introduced_depth").ranks_within_proof(c, base)
    ok_k, sizes_k = I.check_nested(c, base, ranks, "top_k", [1, 2, 4, 8, 16])
    check("T3a top_k is nested", ok_k, str(sizes_k))
    ok_p, sizes_p = I.check_nested(c, base, ranks, "top_pct", [0.1, 0.25, 0.5, 1.0])
    check("T3b top_pct is nested", ok_p, str(sizes_p))

    # ---- T4 components monotone non-increasing
    comps = []
    for k in (1, 2, 4, 8):
        m = I.get("top_k").mask(c, base, ranks, k=k)
        comps.append(M.graph_metrics(c, base, m)["GraphComponents"])
    check("T4 components non-increasing as edges are admitted",
          all(comps[i] >= comps[i + 1] for i in range(len(comps) - 1)),
          str(comps))

    giants = []
    for k in (1, 2, 4, 8):
        m = I.get("top_k").mask(c, base, ranks, k=k)
        giants.append(M.graph_metrics(c, base, m)["GraphGiantFraction"])
    check("T4b giant fraction non-decreasing",
          all(giants[i] <= giants[i + 1] + 1e-12 for i in range(len(giants) - 1)),
          str([round(g, 4) for g in giants]))

    # ---- T5/T6 oracle behaviour
    scores = {}
    for nm in R.names():
        rk = R.get(nm).ranks_within_proof(c, base)
        by = dict(zip(base.tolist(), rk.tolist()))
        scores[nm] = M.source_metrics(c, evalset, by, ks=(1,))["SourceHit@1"]
    best_non_oracle = max(v for k, v in scores.items() if k != "O_source")
    check("T5 SourceOracle is optimal for SourceHit@1",
          scores["O_source"] >= best_non_oracle - 1e-12,
          f"oracle={scores['O_source']:.4f} best_other={best_non_oracle:.4f}")

    frac_with_gt_present = float(np.mean([
        1.0 if (gt & {c.inc_decl[p] for p in pl}) else 0.0
        for ai, pl, gt, _ in evalset]))
    check("T6 oracle ceiling == fraction of proofs with a source ref present "
          "(it measures COVERAGE, not ranking)",
          abs(scores["O_source"] - frac_with_gt_present) < 1e-9,
          f"oracle={scores['O_source']:.4f} coverage={frac_with_gt_present:.4f}")

    # ---- T8 no Semantic* metric is computed anywhere
    keys = set()
    by = dict(zip(base.tolist(),
                  R.get("R_depth").ranks_within_proof(c, base).tolist()))
    keys |= set(M.source_metrics(c, evalset, by, ks=(1,)))
    keys |= set(M.role_metrics(c, evalset, by))
    check("T8 no metric claims to be Semantic*",
          not any(str(k).startswith("Semantic") for k in keys))

    print(f"\n{len(FAILED)} failed" if FAILED else "\nall invariants hold")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
