#!/usr/bin/env python3
"""Social-choice / rank-aggregation schemes for citation keyness.

Each available signal is treated as a VOTER that produces a within-proof
ordering of the proof's candidates. Aggregation rules combine those orderings.

Everything here is append-safe by construction:
  * role, depth, in-statement, arity, is_proof are per-declaration or
    per-incidence facts fixed at elaboration time;
  * rarity is read from the PINNED frozen-foundation table (proofs whose
    target has depth <= 50), the same table `src/mine_failures.py` builds.
No library-wide max / mean / quantile is taken. No name strings are read.

Constants used anywhere in this module (all small integers or a pinned
threshold that already existed in the programme):
  ROLE TIERS      1..5      ordinal labels, not weights
  FOUNDATION      50        the pinned rarity foundation (pre-existing)
  MULTIPLICITY    2, 3      integer ballot multiplicities for the role voter
  k               1,2,4,8   battery report points (pre-existing)
"""
from __future__ import annotations

import glob
import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from mathmap_eval.corpus import get_corpus            # noqa: E402
from mathmap_eval import battery as B                 # noqa: E402
from mathmap_eval import navigation as NAV            # noqa: E402

SEALED = os.path.join(ROOT, "review", "sealed_r1")
FOUNDATION = 50                     # pinned rarity foundation depth

# raw role columns, as written by build_incidence.py
R_APPLIED, R_LET, R_EXPL, R_IMPL, R_INST, R_STRICT, R_TYPE, R_UNRES = range(8)

# ---------------------------------------------------------------- role tiers
# Five ordinal levels read off the SYNTACTIC POSITION in the proof term.
# The order comes from what the position MEANS (does the term do work here?),
# and matches the published usefulness rates: applied 44%, explicit-arg 29%,
# implicit 10%, type-annotation 3.5%, instance-slot 1.6%.
#   5 the term is applied, or bound as a let-value: it is the operative step
#   4 the term is passed as an explicit argument (incl. unresolved, which is
#     a load-bearing position whose head the extractor could not name)
#   3 implicit / strict-implicit argument: inferred, but still a term argument
#   2 type annotation: appears only in a type ascription
#   1 instance slot: supplied by typeclass resolution, not by the author
TIER_OF_ROLE = np.array([5, 5, 4, 3, 1, 3, 2, 4], dtype=np.int8)


def load_grades(keymap, split):
    """Median rater grade per incidence, exactly as src/mine_failures.py."""
    votes = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(SEALED, "grades_*.json"))):
        rater = os.path.basename(f)[7:-5]
        for pid, ent in json.load(open(f)).items():
            if pid not in keymap or keymap[pid]["split"] != split:
                continue
            for num, g in (ent.get("grades") or {}).items():
                inc = keymap[pid]["items"].get(str(num))
                if inc is None:
                    continue
                try:
                    votes[int(inc)].append((rater, int(g)))
                except (TypeError, ValueError):
                    pass
    return {i: int(np.median([g for _, g in v])) for i, v in votes.items()}


class Signals:
    """Per-incidence voter keys. ASCENDING key = better candidate."""

    def __init__(self, c):
        self.c = c
        full = np.where(c.universe("U1D"))[0]
        m = c.inc_d_target[full] <= FOUNDATION
        pop = np.bincount(c.inc_decl[full[m]], minlength=c.n_nodes).astype(float)
        n_art = float(len(np.unique(c.inc_artifact[full[m]])))
        self.IDF = np.maximum(np.log(n_art / np.maximum(pop, 1.0)), 0.0)

    def tier(self, b):
        r = self.c.inc_roles[b] > 0                       # (n, 8) multi-hot
        return (r * TIER_OF_ROLE[None, :]).max(axis=1).astype(np.int16)

    def keys(self, b):
        c = self.c
        d = c.inc_decl[b]
        return {
            "role":    -self.tier(b).astype(np.float64),
            "depth":   -c.inc_d_cite[b].astype(np.float64),
            "rarity":  -self.IDF[d],
            "stmt":    c.inc_in_stmt_world[b].astype(np.float64),
            "arity":   -c.node_arity[d].astype(np.float64),
            "isproof": -c.node_is_proof[d].astype(np.float64),
        }


VOTERS = ["role", "depth", "rarity", "stmt", "arity", "isproof"]
VOTERS4 = ["role", "depth", "rarity", "stmt"]


# ---------------------------------------------------------------- batching
def group_by_artifact(c, base):
    """Sort base by artifact and return (order, starts, counts)."""
    art = c.inc_artifact[base]
    order = np.lexsort((base, art))
    a = art[order]
    new = np.empty(len(a), bool)
    new[0] = True
    new[1:] = a[1:] != a[:-1]
    starts = np.where(new)[0]
    counts = np.diff(np.append(starts, len(a)))
    return order, starts, counts


def _pad_groups(order, starts, counts):
    """Yield (n, idx_block) where idx_block is (m, n) of positions in `base`."""
    for n in np.unique(counts):
        sel = np.where(counts == n)[0]
        idx = starts[sel][:, None] + np.arange(n)[None, :]
        yield int(n), order[idx]


class Aggregator:
    """Computes, per proof, the per-voter midranks and the majority matrix,
    then evaluates every registered rule. Vectorised in groups of equal-size
    proofs so it runs over the whole corpus, not just the graded proofs."""

    def __init__(self, c, base, keys, voter_names, mult=None, budget=1.5e8,
                 ctx=None):
        self.c, self.base = c, base
        self.names = list(voter_names)
        self.mult = mult or {}
        self.budget = budget
        self.K = np.stack([keys[v] for v in self.names])       # (L, N)
        self.W = np.array([self.mult.get(v, 1) for v in self.names], float)
        self.ctx = ctx or {}                                   # per-incidence

    def run(self, rules, as_ranks=False):
        """Evaluate every rule. `as_ranks=True` returns int32 within-proof
        ranks instead of scores (compact enough for the whole corpus)."""
        c, base = self.c, self.base
        order, starts, counts = group_by_artifact(c, base)
        dt = np.int32 if as_ranks else np.float64
        out = {r: np.empty(len(base), dt) for r in rules}
        extra = {"condorcet": np.zeros(len(base), np.int8)}
        L = len(self.names)
        for n, block in _pad_groups(order, starts, counts):
            per = max(1, int(self.budget // max(L * n * n, 1)))
            for s in range(0, len(block), per):
                blk = block[s:s + per]                          # (m, n)
                X = self.K[:, blk]                              # (L, m, n)
                # pref[l,m,a,b] = voter l strictly prefers a over b
                pref = (X[:, :, :, None] < X[:, :, None, :])
                nbet = pref.sum(axis=2).astype(np.float32)      # #better than b
                nwor = pref.sum(axis=3).astype(np.float32)      # #a beats
                nties = n - nbet - nwor                         # includes self
                rk = nbet + (nties - 1.0) / 2.0                 # midrank
                Wm = np.einsum("l,lmab->mab", self.W,
                               pref.astype(np.float32))
                del pref, nbet, nwor, nties
                cx = {k: v[blk] for k, v in self.ctx.items()}
                for name, fn in rules.items():
                    val = np.asarray(fn(rk, Wm, self.W, self.names, cx))
                    if as_ranks:
                        # stable argsort: ties keep term order (append-safe)
                        o = np.argsort(val, axis=1, kind="stable")
                        r = np.empty_like(o)
                        np.put_along_axis(
                            r, o, np.arange(val.shape[1])[None, :]
                            .repeat(val.shape[0], 0), axis=1)
                        out[name][blk.ravel()] = r.ravel()
                    else:
                        out[name][blk.ravel()] = val.ravel()
                cw = self._condorcet(Wm)
                extra["condorcet"][blk.ravel()] = cw.ravel()
        return out, extra

    @staticmethod
    def _condorcet(Wm):
        beats = Wm > Wm.transpose(0, 2, 1)
        n = Wm.shape[1]
        return (beats.sum(axis=2) == n - 1)


# ------------------------------------------------------------------- rules
def borda(rk, Wm, w, names, cx=None):
    return (rk * w[:, None, None]).sum(axis=0)


def _tiebreak(rk, Wm, w, names, cx=None):
    """Borda, scaled below 1 so it can only break exact ties."""
    return borda(rk, Wm, w, names, cx=None) / (w.sum() * rk.shape[2] + 1.0)


def median_ranks(rk, Wm, w, names, cx=None):
    return np.median(rk, axis=0) + _tiebreak(rk, Wm, w, names, cx=None)


def minimax_rank(rk, Wm, w, names, cx=None):
    """'Only as good as its weakest qualification': the WORST rank any voter
    gives it. Borda as the stated tie-break (it is dense with ties)."""
    return rk.max(axis=0) + _tiebreak(rk, Wm, w, names, cx=None)


def best_rank(rk, Wm, w, names, cx=None):
    """The mirror image: a candidate is as good as its BEST qualification."""
    return rk.min(axis=0) + _tiebreak(rk, Wm, w, names, cx=None)


def harmonic(rk, Wm, w, names, cx=None):
    """Dowdall/harmonic positional rule: points 1/(1+rank). Rational weights
    fixed by the rule, no free parameter."""
    return -(w[:, None, None] / (1.0 + rk)).sum(axis=0)


def copeland(rk, Wm, w, names, cx=None):
    beats = (Wm > Wm.transpose(0, 2, 1)).sum(axis=2)
    loses = (Wm < Wm.transpose(0, 2, 1)).sum(axis=2)
    return -(beats - loses).astype(np.float64)


def maximin(rk, Wm, w, names, cx=None):
    """Simpson-Kramer: score = min over opponents of pairwise support."""
    n = Wm.shape[1]
    M = Wm + np.eye(n, dtype=Wm.dtype)[None] * 10 ** 6
    return -M.min(axis=2).astype(np.float64)


def copeland_bt(rk, Wm, w, names, cx=None):
    """Copeland with Borda as the stated tie-break instead of term order."""
    return copeland(rk, Wm, w, names) + _tiebreak(rk, Wm, w, names)


def maximin_bt(rk, Wm, w, names, cx=None):
    """Maximin with Borda as the stated tie-break instead of term order."""
    return maximin(rk, Wm, w, names) + _tiebreak(rk, Wm, w, names)


def black(rk, Wm, w, names, cx=None):
    """Condorcet winner first if one exists, Borda otherwise (Black's rule,
    applied at the top only)."""
    cw = Aggregator._condorcet(Wm)
    bd = borda(rk, Wm, w, names, cx=None)
    return np.where(cw, -1.0, 0.0) * (bd.max() + 1.0) + bd


def kemeny(rk, Wm, w, names, cx=None, max_passes=64):
    """Kemeny-ish: minimise total pairwise disagreement.

    HEURISTIC, stated: seed with the Borda order, then run odd-even adjacent
    transposition passes, swapping a neighbouring pair whenever the swap
    strictly reduces the Kemeny cost. Every accepted swap strictly decreases
    the objective, so it terminates at a local optimum with respect to
    adjacent transpositions. Exact Kemeny is NP-hard; §'exactness' in the
    report measures the gap on small proofs by brute force.
    """
    m, n = Wm.shape[0], Wm.shape[1]
    if n == 1:
        return np.zeros((m, 1))
    bd = borda(rk, Wm, w, names, cx=None)
    P = np.argsort(bd, axis=1, kind="stable")            # (m, n) positions
    rows = np.arange(m)[:, None]
    for p in range(max_passes):
        moved = False
        for parity in (0, 1):
            i = np.arange(parity, n - 1, 2)
            if not len(i):
                continue
            a = P[:, i]
            b = P[:, i + 1]
            gain = Wm[rows, b, a] - Wm[rows, a, b]        # >0 -> swap helps
            sw = gain > 0
            if sw.any():
                moved = True
                A = P[:, i].copy()
                Bb = P[:, i + 1].copy()
                P[:, i] = np.where(sw, Bb, A)
                P[:, i + 1] = np.where(sw, A, Bb)
        if not moved:
            break
    pos = np.empty_like(P)
    np.put_along_axis(pos, P, np.arange(n)[None, :].repeat(m, 0), axis=1)
    return pos.astype(np.float64)


def _rank_within(vals):
    """Within-row 0-based rank, ties broken by term position (stable)."""
    o = np.argsort(vals, axis=1, kind="stable")
    r = np.empty_like(o)
    np.put_along_axis(r, o, np.arange(vals.shape[1])[None, :]
                      .repeat(vals.shape[0], 0), axis=1)
    return r.astype(np.float64)


def make_veto(min_tier):
    """Role as a VETO. Every candidate whose role tier is below `min_tier`
    is ranked after every candidate that is not vetoed; Borda inside each
    block. Lexicographic, implemented with an offset that provably exceeds
    the largest Borda score in the block."""
    def rule(rk, Wm, w, names, cx=None):
        big = w.sum() * rk.shape[2] + 1.0
        return (cx["tier"] < min_tier) * big + borda(rk, Wm, w, names)
    return rule


def role_lex(rk, Wm, w, names, cx=None):
    """Role as a DICTATOR with Borda as the tie-break: the extreme of
    multiplicity. Included to show where the asymmetry argument breaks."""
    big = w.sum() * rk.shape[2] + 1.0
    return (5 - cx["tier"]) * big + borda(rk, Wm, w, names)


def _unique_winner(score):
    """Boolean mask of the unique minimiser per row; all-False when tied."""
    mn = score.min(axis=1, keepdims=True)
    at = score == mn
    return at & (at.sum(axis=1, keepdims=True) == 1)


def make_first_anchor(kind):
    """Social choice used ONLY at the top: promote one candidate to rank 1
    and leave the anchor ordering (a cardinal score in cx['anchor'])
    otherwise untouched.

      kind='condorcet'  the Condorcet winner, when one exists (Black at the
                        top, with a cardinal fallback instead of Borda)
      kind='copeland'   the unique Copeland winner (always defined up to ties)
      kind='borda'      the unique Borda winner -- the CONTROL: if this does
                        as well, nothing about Condorcet is doing the work
    """
    def rule(rk, Wm, w, names, cx=None):
        n = rk.shape[2]
        if kind == "condorcet":
            promote = Aggregator._condorcet(Wm)
        elif kind == "copeland":
            promote = _unique_winner(copeland(rk, Wm, w, names))
        elif kind == "borda":
            promote = _unique_winner(borda(rk, Wm, w, names))
        else:
            raise KeyError(kind)
        return np.where(promote, 0.0, float(n)) + _rank_within(cx["anchor"])
    return rule


condorcet_first_anchor = make_first_anchor("condorcet")


RULES = {
    "borda": borda,
    "copeland": copeland,
    "kemeny": kemeny,
    "maximin_pairwise": maximin,
    "maximin_bordatb": maximin_bt,
    "copeland_bordatb": copeland_bt,
    "minimax_rank": minimax_rank,
    "best_rank": best_rank,
    "median_rank": median_ranks,
    "black_condorcet": black,
    "harmonic": harmonic,
}
