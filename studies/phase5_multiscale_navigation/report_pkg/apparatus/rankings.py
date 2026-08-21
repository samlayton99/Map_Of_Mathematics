"""Rankings: pluggable per-incidence scores.

A ranking is a function

    f(corpus, base) -> tuple[np.ndarray, ...]

returning ASCENDING lexicographic sort keys over `base` (an array of incidence
positions). Returning a single array is fine -- it is treated as one key.

Rankings order the complete declared universe. They never delete: whatever a
ranking dislikes it ranks last. Register with @ranking("name").

Naming discipline (audit): a ranking is a *score*, and any metric computed
from it must say what it measures. Nothing here is called "precision".
"""
from __future__ import annotations

from typing import Callable, Dict

import numpy as np

REGISTRY: Dict[str, "RankingSpec"] = {}


class RankingSpec:
    def __init__(self, name, fn, doc="", family="candidate", complexity=None):
        self.name = name
        self.fn = fn
        self.doc = doc or (fn.__doc__ or "").strip()
        self.family = family              # "baseline" | "candidate"
        self.complexity = complexity or {}

    def keys(self, corpus, base):
        k = self.fn(corpus, base)
        return k if isinstance(k, tuple) else (k,)

    def ranks_within_proof(self, corpus, base) -> np.ndarray:
        """0-based rank of each element of `base` inside its own artifact."""
        keys = self.keys(corpus, base)
        order = np.lexsort(tuple(reversed(keys)) + (corpus.inc_artifact[base],))
        s = base[order]
        aa = corpus.inc_artifact[s]
        new = np.empty(len(s), bool)
        new[0] = True
        new[1:] = aa[1:] != aa[:-1]
        starts = np.where(new)[0]
        counts = np.diff(np.append(starts, len(s)))
        rk = np.concatenate([np.arange(c) for c in counts])
        out = np.empty(len(base), dtype=np.int32)
        out[order] = rk
        return out

    def global_score(self, corpus, base) -> np.ndarray:
        """A single global scalar, for cross-proof comparison (Target C).

        Lexicographic keys are folded into one float by ordering the tuples.
        Report tie statistics before trusting this.
        """
        keys = self.keys(corpus, base)
        order = np.lexsort(tuple(reversed(keys)))
        ranks = np.empty(len(base), dtype=np.float64)
        ranks[order] = np.arange(len(base))
        return -ranks


def ranking(name, family="candidate", **meta):
    def deco(fn):
        REGISTRY[name] = RankingSpec(name, fn, family=family, complexity=meta)
        return fn
    return deco


def get(name) -> RankingSpec:
    if name not in REGISTRY:
        raise KeyError(f"unknown ranking {name!r}; have {sorted(REGISTRY)}")
    return REGISTRY[name]


def names(family=None):
    return sorted(n for n, s in REGISTRY.items()
                  if family is None or s.family == family)


# ------------------------------------------------------------- baselines
@ranking("B0_random", family="baseline", features=0, seeded=True)
def _b0(c, base):
    """Uniform random order within each proof. The floor."""
    return np.random.default_rng(20260820).random(len(base))


@ranking("B1_reverse_depth", family="baseline", features=1)
def _b1(c, base):
    """Shallowest cited declaration first: the anti-ranking."""
    return c.inc_d_cite[base].astype(np.float64)


@ranking("B2_popularity", family="baseline", features=1)
def _b2(c, base):
    """Most globally cited first. Tests 'importance = citation count'."""
    return -c.decl_popularity[c.inc_decl[base]]


@ranking("B3_term_order", family="baseline", features=1)
def _b3(c, base):
    """Order of first occurrence in the record: a structural arbitrary order."""
    return base.astype(np.float64)


# ------------------------------------------------------------ candidates
@ranking("R_depth", features=1, thresholds=0)
def _r_depth(c, base):
    """Deepest cited declaration first. The simplest real candidate."""
    return -c.inc_d_cite[base].astype(np.float64)


@ranking("R_introduced_depth", features=2, thresholds=0)
def _r_intro(c, base):
    """Citations the proof introduces first, then deepest. Current leader."""
    return (c.inc_in_stmt_world[base].astype(np.int8),
            -c.inc_d_cite[base].astype(np.float64))


@ranking("R_v8_faithful", features=4, thresholds=3)
def _r_v8(c, base):
    """Frozen V8 order, with what V8 filtered merely ranked last."""
    return ((~c.decl_is_claim[c.inc_decl[base]]).astype(np.int8),
            c.inc_glue[base].astype(np.int8),
            c.inc_in_stmt_world[base].astype(np.int8),
            -c.inc_d_cite[base].astype(np.float64))


@ranking("R_v8_all_kinds", features=3, thresholds=3)
def _r_v8k(c, base):
    """V8's demotions, but declaration kind ignored so definitions compete."""
    return (c.inc_glue[base].astype(np.int8),
            c.inc_in_stmt_world[base].astype(np.int8),
            -c.inc_d_cite[base].astype(np.float64))


@ranking("R_phase5_composite", features=4, thresholds=2)
def _r_p5(c, base):
    """Frozen as a weak comparator: role x statement x depth x idf."""
    r = c.inc_roles[base]
    m_role = np.where(r[:, 0] > 0, 1.0,
                      np.where((r[:, 1] > 0) | (r[:, 2] > 0), 0.7, 0.5))
    m_stmt = np.where(c.inc_in_stmt_world[base], 1.0, 1.5)
    dmax = float(c.node_depth.max())
    m_depth = 0.20 + 0.80 * c.inc_d_cite[base] / dmax
    return -(m_role * m_stmt * m_depth * c.decl_idf[c.inc_decl[base]])


# ---------------------------------------------------------------- oracles
@ranking("O_source", family="baseline", features="oracle")
def _o_source(c, base):
    """SourceOracle: identifiers the human wrote first, then depth.

    NOT a keyness oracle (audit item 2). It is an upper bound for
    Source* metrics only, and its ceiling below 100% measures CANDIDATE
    COVERAGE, not ranking quality.
    """
    flag = getattr(c, "_source_flag_cache", None)
    if flag is None or len(flag) != c.n_incidences:
        flag = np.zeros(c.n_incidences, dtype=bool)
        for ai, pl, gt, _ in c.evaluation_set():
            for p in pl:
                if c.inc_decl[p] in gt:
                    flag[p] = True
        c._source_flag_cache = flag
    return (~flag[base], -c.inc_d_cite[base].astype(np.float64))
