"""Inclusion policies: which part of a ranked record a view admits.

An inclusion policy is a function

    f(corpus, base, ranks, **params) -> np.ndarray[bool]

returning a mask over `base`. Policies are the USER's knob; rankings are ours.
Keeping them separate is the whole point of the apparatus -- a change in what
you display must never be confused with a change in what you believe is
important.

Two families:
  per-proof  top-k, top-percentile, role/kind lanes
  global     score quantile, depth band, evidence tier

Policies must be MONOTONE in their parameter (opening admits a superset) so a
slider is a nested family. `check_nested` verifies this rather than assuming.
"""
from __future__ import annotations

from typing import Callable, Dict

import numpy as np

REGISTRY: Dict[str, "InclusionSpec"] = {}


class InclusionSpec:
    def __init__(self, name, fn, family, monotone_param=None, doc=""):
        self.name = name
        self.fn = fn
        self.family = family                 # "per-proof" | "global"
        self.monotone_param = monotone_param  # name of the opening parameter
        self.doc = doc or (fn.__doc__ or "").strip()

    def mask(self, corpus, base, ranks, **params) -> np.ndarray:
        return self.fn(corpus, base, ranks, **params)


def inclusion(name, family, monotone_param=None):
    def deco(fn):
        REGISTRY[name] = InclusionSpec(name, fn, family, monotone_param)
        return fn
    return deco


def get(name) -> InclusionSpec:
    if name not in REGISTRY:
        raise KeyError(f"unknown inclusion {name!r}; have {sorted(REGISTRY)}")
    return REGISTRY[name]


def names(family=None):
    return sorted(n for n, s in REGISTRY.items()
                  if family is None or s.family == family)


# ------------------------------------------------------------- per proof
@inclusion("top_k", "per-proof", monotone_param="k")
def _top_k(c, base, ranks, k=1):
    """The k highest-ranked citations of every proof."""
    return ranks < k


@inclusion("top_pct", "per-proof", monotone_param="pct")
def _top_pct(c, base, ranks, pct=0.25):
    """The top `pct` fraction of each proof's citations, at least one."""
    arts = c.inc_artifact[base]
    sizes = np.bincount(arts, minlength=int(arts.max()) + 1)
    lim = np.maximum(1, np.ceil(pct * sizes[arts]).astype(np.int64))
    return ranks < lim


@inclusion("kind_lane", "per-proof")
def _kind_lane(c, base, ranks, kinds=("theorem", "definition/construction")):
    """Only citations of the named declaration kinds. A lane, not a filter."""
    grp = c.kind_group(c.inc_decl[base])
    return np.isin(grp.astype(str), list(kinds))


@inclusion("role_lane", "per-proof")
def _role_lane(c, base, ranks, roles=(0, 1, 2, 7)):
    """Only citations occurring in the named occurrence roles."""
    r = c.inc_roles[base]
    return r[:, list(roles)].sum(axis=1) > 0


@inclusion("introduced_only", "per-proof")
def _introduced(c, base, ranks):
    """Only citations the proof introduces (not implied by the statement)."""
    return ~c.inc_in_stmt_world[base]


# ---------------------------------------------------------------- global
@inclusion("global_quantile", "global", monotone_param="q")
def _global_q(c, base, ranks, q=0.25, score=None):
    """The globally top-scoring `q` fraction of all incidences."""
    if score is None:
        raise ValueError("global_quantile needs the ranking's global score")
    if q >= 1.0:
        return np.ones(len(base), dtype=bool)
    thr = np.quantile(score, 1.0 - q)
    return score >= thr


@inclusion("cited_depth_band", "global")
def _cited_band(c, base, ranks, lo=0, hi=10**9):
    """Only citations whose CITED declaration lies in a depth band."""
    d = c.inc_d_cite[base]
    return (d >= lo) & (d < hi)


@inclusion("target_depth_band", "global")
def _target_band(c, base, ranks, lo=0, hi=10**9):
    """Only citations whose PROVED theorem lies in a depth band."""
    d = c.inc_d_target[base]
    return (d >= lo) & (d < hi)


@inclusion("all", "global")
def _all(c, base, ranks):
    """Everything in the declared universe. The fully open slider."""
    return np.ones(len(base), dtype=bool)


# ---------------------------------------------------------------- checks
def check_nested(c, base, ranks, name, params_ascending, **fixed):
    """Verify a policy really is nested as its parameter opens.

    Returns (ok, sizes). A slider that is not nested is not a slider.
    """
    spec = get(name)
    prev = None
    sizes = []
    ok = True
    for p in params_ascending:
        kw = dict(fixed)
        kw[spec.monotone_param] = p
        m = spec.mask(c, base, ranks, **kw)
        sizes.append(int(m.sum()))
        if prev is not None and not np.all(prev <= m):
            ok = False
        prev = m
    return ok, sizes
