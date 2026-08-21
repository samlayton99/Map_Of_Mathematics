"""The landing port: drop a ranking in a file, it appears in the suite.

Any `.py` file in `rankings_local/` is imported at load time. Whatever it
registers with `@ranking` or `@inclusion` joins the registry, and from then on
every part of the apparatus -- metrics, dashboard tabs, sweep curves, export
reports, the vibe check -- picks it up automatically with no other edit.

    # rankings_local/my_idea.py
    from mathmap_eval import ranking

    @ranking("R_my_idea", features=2)
    def _mine(c, base):
        "One line describing it; this string is published in the dashboard."
        return (c.inc_in_stmt_world[base].astype("int8"),
                -c.inc_d_cite[base].astype(float))

Then `python src/ship.py` rebuilds and delivers the dashboard.

A ranking must be a PURE function of the corpus returning ascending
lexicographic sort keys, and must never delete: whatever it dislikes it ranks
last. `verify()` below enforces the parts of that which are checkable.
"""
from __future__ import annotations

import importlib.util
import os
import traceback

import numpy as np

from . import rankings as R

LOCAL_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                 "rankings_local"))


def load_local(verbose=True):
    """Import every rankings_local/*.py. Returns (loaded, failed)."""
    loaded, failed = [], []
    if not os.path.isdir(LOCAL_DIR):
        return loaded, failed
    before = set(R.REGISTRY)
    for fn in sorted(os.listdir(LOCAL_DIR)):
        if not fn.endswith(".py") or fn.startswith("_"):
            continue
        path = os.path.join(LOCAL_DIR, fn)
        try:
            spec = importlib.util.spec_from_file_location(
                "rankings_local." + fn[:-3], path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            loaded.append(fn)
        except Exception:
            failed.append((fn, traceback.format_exc()))
            if verbose:
                print(f"  ! {fn} failed to load:\n{traceback.format_exc()}",
                      flush=True)
    new = sorted(set(R.REGISTRY) - before)
    if verbose and new:
        print(f"  landing port: registered {', '.join(new)}", flush=True)
    return loaded, failed


def verify(name, corpus, sample=200_000, seed=11):
    """Check a ranking obeys the contract, on a sample.

    Catches the mistakes that would otherwise produce a silently wrong tab:
    wrong length, non-finite keys, keys that are not sortable, and -- the
    important one -- a ranking that drops candidates instead of ordering them.
    Returns a list of problems; empty means it is safe to publish.
    """
    problems = []
    spec = R.get(name)
    base_all = np.where(corpus.universe("U1D"))[0]
    rng = np.random.default_rng(seed)
    idx = (rng.choice(len(base_all), sample, replace=False)
           if len(base_all) > sample else np.arange(len(base_all)))
    base = np.sort(base_all[idx])
    try:
        keys = spec.keys(corpus, base)
    except Exception as e:
        return [f"raised {type(e).__name__}: {e}"]
    if not isinstance(keys, tuple):
        problems.append("keys() did not return a tuple of arrays")
        keys = (keys,)
    for i, k in enumerate(keys):
        k = np.asarray(k)
        if len(k) != len(base):
            problems.append(f"key {i} has length {len(k)}, expected {len(base)}")
        if k.dtype.kind == "f" and not np.isfinite(k).all():
            problems.append(f"key {i} contains NaN or infinity")
        if k.dtype.kind not in "biuf":
            problems.append(f"key {i} has non-numeric dtype {k.dtype}")
    try:
        ranks = spec.ranks_within_proof(corpus, base)
    except Exception as e:
        return problems + [f"ranks_within_proof raised {type(e).__name__}: {e}"]
    if len(ranks) != len(base):
        problems.append("ranks_within_proof returned the wrong length")
    else:
        # every proof must be ranked 0..n-1 exactly once: nothing dropped
        order = np.argsort(corpus.inc_artifact[base], kind="stable")
        arts = corpus.inc_artifact[base][order]
        rk = ranks[order]
        bounds = np.flatnonzero(np.r_[True, arts[1:] != arts[:-1], True])
        bad = 0
        for a, b in zip(bounds[:-1], bounds[1:]):
            seg = np.sort(rk[a:b])
            if not np.array_equal(seg, np.arange(b - a)):
                bad += 1
        if bad:
            problems.append(
                f"{bad} proofs are not ranked as a permutation 0..n-1 "
                "(a ranking must order every candidate, never drop one)")
    return problems
