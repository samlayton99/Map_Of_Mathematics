"""The suite runner: rankings x inclusions x metrics, reproducibly.

Every result carries the universe it was computed on and the metric family it
belongs to, so a Source* number can never be quoted as keyness by accident.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict

import numpy as np

from . import inclusions as I
from . import metrics as M
from . import rankings as R
from .corpus import get_corpus


@dataclass
class RunConfig:
    universe: str = "U1"
    rankings: tuple = ()
    ks: tuple = (1, 2, 4, 8)
    graph_ks: tuple = (1, 2, 4, 8)
    proof_written_only: bool = True
    bootstrap: int = 0
    out: str | None = None


def evaluate_ranking(c, name, base, evalset, cfg: RunConfig):
    spec = R.get(name)
    t0 = time.time()
    ranks = spec.ranks_within_proof(c, base)
    by_pos = dict(zip(base.tolist(), ranks.tolist()))
    res = {
        "ranking": name,
        "family": spec.family,
        "universe": cfg.universe,
        "complexity": spec.complexity,
        "doc": spec.doc,
        "source": M.source_metrics(c, evalset, by_pos, ks=cfg.ks),
        "role": M.role_metrics(c, evalset, by_pos),
        "ties": tie_stats(c, spec, base),
        "graph": {},
        "seconds": None,
    }
    for k in cfg.graph_ks:
        m = I.get("top_k").mask(c, base, ranks, k=k)
        res["graph"][f"top_k={k}"] = M.graph_metrics(c, base, m)
    res["seconds"] = round(time.time() - t0, 1)
    return res, ranks


def tie_stats(c, spec, base, sample=200_000, seed=3):
    """Tie structure of the global score (audit item 10: a stable-ID
    tie-break is reproducible, not meaningful)."""
    keys = spec.keys(c, base)
    rng = np.random.default_rng(seed)
    idx = (rng.choice(len(base), sample, replace=False)
           if len(base) > sample else np.arange(len(base)))
    cols = [np.asarray(k)[idx] for k in keys]
    view = np.stack(cols, axis=1)
    _, inv, counts = np.unique(view, axis=0, return_inverse=True,
                               return_counts=True)
    blocks = counts[inv]
    n = len(idx)
    tied_pairs = float(((blocks - 1).sum()) / max(n * (n - 1), 1))
    return {"distinct_levels": int(len(counts)),
            "median_tie_block": float(np.median(counts)),
            "p90_tie_block": float(np.percentile(counts, 90)),
            "max_tie_block": int(counts.max()),
            "approx_frac_pairs_tied": tied_pairs,
            "sampled": int(n)}


def run(cfg: RunConfig):
    c = get_corpus()
    base = np.where(c.universe(cfg.universe))[0]
    evalset = c.evaluation_set(cfg.universe, cfg.proof_written_only)
    names = cfg.rankings or tuple(R.names())
    out = {"config": asdict(cfg),
           "n_incidences_in_universe": int(len(base)),
           "n_eval_proofs": len(evalset),
           "coverage": M.coverage_metrics(c, cfg.universe),
           "results": {}}
    for nm in names:
        res, ranks = evaluate_ranking(c, nm, base, evalset, cfg)
        out["results"][nm] = res
        print(f"  {nm:<22} SourceHit@1={res['source']['SourceHit@1']:.3f} "
              f"MRR={res['source']['SourceMRR']:.3f} "
              f"glue@1={res['role']['RoleGlueAt1']:.3f} "
              f"({res['seconds']}s)", flush=True)
    if cfg.out:
        os.makedirs(os.path.dirname(cfg.out), exist_ok=True)
        with open(cfg.out, "w") as f:
            json.dump(out, f, indent=1, default=float)
    return out


def compare_table(out, metric="SourceHit@1"):
    rows = []
    for nm, r in out["results"].items():
        src = r["source"]
        rows.append((r["family"], nm, src.get(metric, float("nan")),
                     src["SourceMRR"], src.get("SourceRecall@4", float("nan")),
                     r["role"]["RoleGlueAt1"],
                     r["ties"]["approx_frac_pairs_tied"]))
    rows.sort(key=lambda x: (x[0] != "candidate", -x[2]))
    w = max(len(r[1]) for r in rows) + 2
    lines = [f"{'ranking':<{w}}{'family':<11}{metric:>12}{'MRR':>8}"
             f"{'SrcRec@4':>10}{'glue@1':>9}{'tied':>9}"]
    for fam, nm, a, b, cc, d, e in rows:
        lines.append(f"{nm:<{w}}{fam:<11}{a:>12.3f}{b:>8.3f}{cc:>10.3f}"
                     f"{d:>9.3f}{e:>9.3f}")
    return "\n".join(lines)


def depth_table(out, metric="SourceHit@1"):
    bands = M.BAND_LABELS
    w = 24
    lines = [f"{'ranking':<{w}}" + "".join(b.rjust(11) for b in bands)]
    for nm, r in out["results"].items():
        cells = []
        for b in bands:
            v = r["source"]["by_target_depth"].get(b)
            cells.append((f"{v[metric]:.3f}" if v else "-").rjust(11))
        lines.append(f"{nm:<{w}}" + "".join(cells))
    return "\n".join(lines)


def graph_table(out):
    ks = sorted(next(iter(out["results"].values()))["graph"].keys())
    w = 24
    lines = [f"{'ranking':<{w}}" + "".join(k.rjust(22) for k in ks),
             f"{'':<{w}}" + "".join("comps / giant".rjust(22) for _ in ks)]
    for nm, r in out["results"].items():
        cells = []
        for k in ks:
            g = r["graph"][k]
            cells.append(f"{g['GraphComponents']:,} / {g['GraphGiantFraction']:.1%}".rjust(22))
        lines.append(f"{nm:<{w}}" + "".join(cells))
    return "\n".join(lines)
