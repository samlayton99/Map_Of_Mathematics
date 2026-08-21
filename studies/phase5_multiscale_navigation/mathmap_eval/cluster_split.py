"""Adaptive per-proof cut: where does the content stop and the plumbing start?

A fixed top-k is a blunt instrument. Some proofs have one real move, some have
five, and "plumbing" is a continuum rather than a class. This module asks a
different question of every proof separately: given the ranking's own score
sequence over that proof's candidates, is there a NATURAL BOUNDARY, and where?

The score is a lexicographic key tuple, so before any break-finding can happen
the tuple has to become a number. The only honest scalar is one that is a
strictly monotone function of the ranking's own order, so we use the DENSE
LEXICOGRAPHIC LEVEL of the key tuple over the whole universe, normalised to
[0, 1]:

    s(item) = (index of the item's distinct key tuple in the globally sorted
               list of distinct key tuples) / (number of distinct tuples - 1)

Two items with the same key have the same s -- ties are preserved exactly,
which matters because ties are the ranking honestly saying "I cannot separate
these". `scale="mass"` instead measures the share of the universe the ranking
places strictly ahead of the item; it is offered because it is a defensible
alternative, not because it wins (it does not; see reports/CLUSTER_SPLIT.md).

Everything is computed by sorted-by-artifact segment arithmetic: one lexsort
and a handful of `reduceat` calls over the whole 18M-candidate record. There
is no Python loop over proofs.

Methods (all guarantee 1 <= admitted <= proof size):

  tie_first          the first tie-block of the lexicographic key
  tie_first_capped   ... capped at min(8, ceil(L/2)) so a degenerate first
                     block cannot admit the whole proof
  tie_two            the first two tie-blocks
  max_gap            cut after the largest jump in the score sequence
  max_gap_half       ... restricted to the first half of the proof
  max_gap_rel        largest MULTIPLICATIVE jump, g_i / max(s_i, one level)
  otsu               1-D two-class Otsu / Jenks natural break (for two classes
                     maximising between-class variance and minimising
                     within-class sum of squares are the same problem)
  kneedle            largest normalised distance below the chord of the
                     score curve (Satopaa et al.'s Kneedle, convex branch)
  curvature          largest discrete second difference of the score curve

`DEFAULT_METHOD` is the one registered as the `cluster_split` inclusion
policy. It was chosen by `evaluate_methods` against the graded rater labels.
READ reports/CLUSTER_SPLIT.md BEFORE QUOTING IT: the honest result is that the
methods which genuinely vary per proof (max_gap, otsu, kneedle, curvature) are
WORSE than fixed top-k at the same mean size, and the tie-block methods that
do win, win by about one graded candidate out of 154 -- well inside the Wilson
interval. The default is defensible, not demonstrated.

The module must be IMPORTED for the `cluster_split` policy to appear in
`mathmap_eval.inclusions.REGISTRY`.
"""
from __future__ import annotations

from typing import Dict, Sequence, Tuple

import numpy as np

from .inclusions import inclusion

METHODS = ("tie_first", "tie_first_capped", "tie_two", "max_gap",
           "max_gap_half", "max_gap_rel", "otsu", "kneedle", "curvature")

#: Chosen by evidence in reports/CLUSTER_SPLIT.md. It wins by a margin the
#: 180-proof labelled set cannot resolve -- read that report before quoting it.
DEFAULT_METHOD = "tie_two"

_NEG = -np.inf


# --------------------------------------------------------------- the scalar
def lex_levels(keys: Sequence[np.ndarray]) -> Tuple[np.ndarray, int]:
    """Dense level index of each item's key tuple in global lexicographic order.

    Returns (level, n_levels) with level in 0..n_levels-1 and
    level[i] < level[j] iff the ranking strictly prefers i to j.
    """
    cols, bits = [], []
    for k in keys:
        kk = np.asarray(k)
        if kk.dtype == np.bool_:
            kk = kk.astype(np.int8)
        _u, inv = np.unique(kk, return_inverse=True)
        cols.append(np.asarray(inv).reshape(-1).astype(np.int64))
        bits.append(max(1, int(max(len(_u) - 1, 1)).bit_length()))
    n = len(cols[0])
    if sum(bits) <= 62:
        packed = np.zeros(n, np.int64)
        sh = int(sum(bits))
        for col, b in zip(cols, bits):
            sh -= b
            packed |= col << sh
            del col
        lev, inv = np.unique(packed, return_inverse=True)
        return np.asarray(inv).reshape(-1).astype(np.int64), int(len(lev))
    # too many distinct values to pack: fall back to an explicit lexsort
    order = np.lexsort(tuple(reversed(cols)))
    new = np.zeros(n, bool)
    new[0] = True
    for col in cols:
        cs = col[order]
        new[1:] |= cs[1:] != cs[:-1]
    lv = np.cumsum(new) - 1
    out = np.empty(n, np.int64)
    out[order] = lv
    return out, int(lv[-1] + 1)


def score_from_keys(keys: Sequence[np.ndarray], scale: str = "level"
                    ) -> Tuple[np.ndarray, float]:
    """Monotone [0,1] scalar per candidate, plus the size of one level step."""
    lev, nlev = lex_levels(keys)
    if scale == "level":
        step = 1.0 / max(nlev - 1, 1)
        return lev.astype(np.float64) * step, step
    if scale == "mass":
        cnt = np.bincount(lev, minlength=nlev).astype(np.float64)
        cum = np.concatenate(([0.0], np.cumsum(cnt)[:-1]))
        n = float(max(len(lev), 1))
        return cum[lev] / n, 1.0 / n
    raise ValueError(f"unknown scale {scale!r} (have 'level', 'mass')")


# ------------------------------------------------------------- segmentation
class _Segments:
    """Candidates sorted by (artifact, rank), with segment arithmetic."""

    def __init__(self, art: np.ndarray, ranks: np.ndarray, s: np.ndarray,
                 step: float):
        self.n = int(len(art))
        self.step = float(step)
        if self.n == 0:
            self.order = np.zeros(0, np.int64)
            self.starts = np.zeros(0, np.int64)
            self.lens = np.zeros(0, np.int64)
            self.seg_of = np.zeros(0, np.int32)
            self.pos = np.zeros(0, np.int64)
            self.s = np.zeros(0, np.float64)
            self.nseg = 0
            return
        self.order = np.lexsort((ranks, art))
        a = art[self.order]
        new = np.empty(self.n, bool)
        new[0] = True
        np.not_equal(a[1:], a[:-1], out=new[1:])
        del a
        self.starts = np.flatnonzero(new)
        self.nseg = int(len(self.starts))
        self.lens = np.diff(np.append(self.starts, self.n))
        self.seg_of = np.repeat(np.arange(self.nseg, dtype=np.int32), self.lens)
        self.pos = np.arange(self.n, dtype=np.int64) - self.starts[self.seg_of]
        self.s = np.ascontiguousarray(s[self.order], dtype=np.float64)

    # -- broadcasts of per-segment quantities back to per-item ------------
    def bcast(self, per_seg: np.ndarray) -> np.ndarray:
        return per_seg[self.seg_of]

    @property
    def L(self) -> np.ndarray:
        return self.lens[self.seg_of]

    def seg_max(self, v):
        return np.maximum.reduceat(v, self.starts)

    def seg_min(self, v):
        return np.minimum.reduceat(v, self.starts)

    def first_argmax(self, v: np.ndarray) -> np.ndarray:
        """Index WITHIN each segment of its first maximal element."""
        mx = np.maximum.reduceat(v, self.starts)
        idx = np.where(v >= mx[self.seg_of],
                       np.arange(self.n, dtype=np.int64), self.n)
        return np.minimum.reduceat(idx, self.starts) - self.starts

    def cumsum(self, v: np.ndarray) -> np.ndarray:
        cs = np.cumsum(v)
        off = cs[self.starts] - v[self.starts]
        return cs - off[self.seg_of]

    def blocks(self) -> np.ndarray:
        """0-based tie-block index of each item inside its own segment."""
        new = np.empty(self.n, bool)
        new[0] = True
        np.not_equal(self.s[1:], self.s[:-1], out=new[1:])
        new[self.starts] = True
        gb = np.cumsum(new, dtype=np.int32) - 1
        return gb - gb[self.starts][self.seg_of]

    def last_of_segment(self) -> np.ndarray:
        return self.pos == (self.L - 1)


# ------------------------------------------------------------- the methods
def _first_n_blocks(seg: _Segments, nb: int) -> np.ndarray:
    blk = seg.blocks()
    v = (blk >= nb).astype(np.float64)
    has = seg.seg_max(v) > 0
    j = seg.first_argmax(v)
    return np.where(has, j, seg.lens)


def _gaps(seg: _Segments) -> np.ndarray:
    g = np.empty(seg.n, np.float64)
    g[:-1] = seg.s[1:] - seg.s[:-1]
    g[-1] = _NEG
    g[seg.last_of_segment()] = _NEG
    return g


def _m_max_gap(seg, half=False, relative=False):
    g = _gaps(seg)
    if relative:
        g = np.where(g > _NEG / 2, g / np.maximum(seg.s, seg.step), _NEG)
    if half:
        g = np.where(seg.pos < np.ceil(seg.L / 2.0), g, _NEG)
    return seg.first_argmax(g) + 1


def _m_otsu(seg):
    P = seg.cumsum(seg.s)
    tot = seg.bcast(P[seg.starts + seg.lens - 1])
    n1 = (seg.pos + 1).astype(np.float64)
    n2 = seg.L.astype(np.float64) - n1
    with np.errstate(divide="ignore", invalid="ignore"):
        mu1 = P / n1
        mu2 = np.where(n2 > 0, (tot - P) / np.maximum(n2, 1.0), 0.0)
        v = n1 * n2 * (mu1 - mu2) ** 2 / (seg.L.astype(np.float64) ** 2)
    v = np.where(n2 > 0, v, _NEG)
    return seg.first_argmax(v) + 1


def _m_kneedle(seg):
    smin = seg.bcast(seg.seg_min(seg.s))
    smax = seg.bcast(seg.seg_max(seg.s))
    rng = smax - smin
    Lf = seg.L.astype(np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        x = seg.pos.astype(np.float64) / np.maximum(Lf - 1.0, 1.0)
        y = np.where(rng > 0, (seg.s - smin) / np.maximum(rng, 1e-300), 0.0)
    d = np.where(seg.L >= 3, x - y, _NEG)
    j = seg.first_argmax(d)
    return np.where(seg.lens >= 3, j + 1, 1)


def _m_curvature(seg):
    cur = np.empty(seg.n, np.float64)
    cur[0] = _NEG
    cur[-1] = _NEG
    if seg.n > 2:
        cur[1:-1] = seg.s[2:] - 2.0 * seg.s[1:-1] + seg.s[:-2]
    interior = (seg.pos > 0) & (seg.pos < seg.L - 1)
    cur = np.where(interior, cur, _NEG)
    j = seg.first_argmax(cur)
    return np.where(seg.lens >= 3, j + 1, 1)


def _sizes_for_method(seg: _Segments, method: str, tied_all: bool,
                      cap_abs: int, cap_frac: float) -> np.ndarray:
    if method == "tie_first":
        m = _first_n_blocks(seg, 1)
    elif method == "tie_two":
        m = _first_n_blocks(seg, 2)
    elif method == "tie_first_capped":
        m = _first_n_blocks(seg, 1)
        cap = np.maximum(1, np.minimum(cap_abs,
                                       np.ceil(cap_frac * seg.lens).astype(np.int64)))
        m = np.minimum(m, cap)
    elif method == "max_gap":
        m = _m_max_gap(seg)
    elif method == "max_gap_half":
        m = _m_max_gap(seg, half=True)
    elif method == "max_gap_rel":
        m = _m_max_gap(seg, relative=True)
    elif method == "otsu":
        m = _m_otsu(seg)
    elif method == "kneedle":
        m = _m_kneedle(seg)
    elif method == "curvature":
        m = _m_curvature(seg)
    else:
        raise ValueError(f"unknown method {method!r}; have {METHODS}")

    if not method.startswith("tie_"):
        # A proof whose candidates are ALL tied has no boundary to find: any
        # prefix would be an arbitrary tie-break. `tied_all` says whether to
        # read that as "show them all" or "show the minimum".
        flat = seg.seg_max(seg.s) == seg.seg_min(seg.s)
        m = np.where(flat, seg.lens if tied_all else 1, m)
    return np.clip(m, 1, seg.lens).astype(np.int64)


# ------------------------------------------------------------------- public
def make_segments(corpus, base: np.ndarray, ranks: np.ndarray,
                  keys: Sequence[np.ndarray], scale: str = "level"
                  ) -> "_Segments":
    """The sorted-by-(artifact, rank) working set, shared by all methods.

    Building it costs one dense-ranking pass and one lexsort over the whole
    universe, so comparing several methods on the same ranking should build it
    ONCE and hand it to `split_sizes(..., seg=...)`.
    """
    if isinstance(keys, np.ndarray):
        keys = (keys,)
    art = corpus.inc_artifact[np.asarray(base)]
    s, step = score_from_keys(tuple(keys), scale=scale)
    seg = _Segments(art, np.asarray(ranks), s, step)
    seg.art_sorted_starts = art[seg.order][seg.starts] if seg.n else \
        np.zeros(0, np.int64)
    return seg


def split_sizes(corpus, base: np.ndarray, ranks: np.ndarray,
                keys: Sequence[np.ndarray] | None = None,
                method: str = DEFAULT_METHOD,
                scale: str = "level", tied_all: bool = True,
                cap_abs: int = 8, cap_frac: float = 0.5,
                return_sizes: bool = False, seg: "_Segments | None" = None
                ) -> np.ndarray:
    """Per-proof adaptive admission mask over `base`.

    `keys` are the ranking's ascending lexicographic sort keys aligned to
    `base` (i.e. `RankingSpec.keys(corpus, base)`); `ranks` are the 0-based
    within-proof ranks (`RankingSpec.ranks_within_proof`). Pass `seg` from
    `make_segments` to reuse the shared work across methods.

    Returns a bool mask over `base`. With `return_sizes=True` returns
    `(mask, sizes, seg_artifacts)` where `sizes` is the admitted count per
    proof and `seg_artifacts` names the proofs in the same order.
    """
    base = np.asarray(base)
    if len(base) == 0:
        empty = np.zeros(0, bool)
        return (empty, np.zeros(0, np.int64), np.zeros(0, np.int64)) \
            if return_sizes else empty
    if seg is None:
        if keys is None:
            raise ValueError("split_sizes needs keys=... or seg=...")
        seg = make_segments(corpus, base, ranks, keys, scale=scale)
    m = _sizes_for_method(seg, method, tied_all, cap_abs, cap_frac)
    admitted = seg.pos < m[seg.seg_of]
    mask = np.zeros(len(base), bool)
    mask[seg.order] = admitted
    if return_sizes:
        return mask, m, seg.art_sorted_starts
    return mask


@inclusion("cluster_split", "per-proof")
def _cluster_split(c, base, ranks, keys=None, ranking=None,
                   method=DEFAULT_METHOD, scale="level", tied_all=True,
                   cap_abs=8, cap_frac=0.5):
    """Adaptive per-proof cut at the ranking's own natural boundary.

    Not a slider: it has no monotone opening parameter, because the whole
    point is that the cut is chosen per proof rather than dialled globally.
    Pass either `keys` (the ranking's sort keys over `base`) or `ranking`
    (its registry name).
    """
    if keys is None:
        if ranking is None:
            raise ValueError("cluster_split needs keys=... or ranking=...")
        from . import rankings as _R
        keys = _R.get(ranking).keys(c, base)
    return split_sizes(c, base, ranks, keys, method=method, scale=scale,
                       tied_all=tied_all, cap_abs=cap_abs, cap_frac=cap_frac)


# ---------------------------------------------------------------- evaluation
def grade_array(corpus, base, grades_by_inc):
    """Per-candidate rater grade over `base`; -1 where the candidate is
    ungraded. Small, dense, and the only thing the label channel needs."""
    g = np.full(corpus.n_incidences, -1, np.int8)
    if grades_by_inc:
        idx = np.fromiter(grades_by_inc.keys(), np.int64, len(grades_by_inc))
        val = np.fromiter(grades_by_inc.values(), np.int8, len(grades_by_inc))
        g[idx] = val
    gb = g[base]
    return gb


def _score_mask(mask, gb, art, lab_arts, n_art):
    """Label-side scorecard of one admission mask."""
    lab = gb >= 0
    adm_lab = mask & lab
    n_adm_lab = int(adm_lab.sum())
    key_tot = int((gb == 4).sum())
    key_adm = int((adm_lab & (gb == 4)).sum())
    good = int((adm_lab & (gb >= 3)).sum())
    bad = int((adm_lab & (gb <= 1)).sum())
    sizes = np.bincount(art[mask], minlength=n_art)[lab_arts]
    return {
        "MeanAdmitted": float(sizes.mean()) if len(sizes) else float("nan"),
        "MedianAdmitted": float(np.median(sizes)) if len(sizes) else float("nan"),
        "KeyRecall": key_adm / key_tot if key_tot else float("nan"),
        "PrecisionGraded": good / n_adm_lab if n_adm_lab else float("nan"),
        "BadShare": bad / n_adm_lab if n_adm_lab else float("nan"),
        "MeanGrade": (float(gb[adm_lab].mean()) if n_adm_lab
                      else float("nan")),
        "n_admitted_labelled": n_adm_lab,
        "n_key_total": key_tot,
    }


def evaluate_methods(corpus=None, universe: str = "U1D", rankings=None,
                     label_dir: str | None = None, methods=None,
                     scales=("level",), ks=(1, 2, 4, 8), kmax: int = 24,
                     verbose: bool = True) -> Dict:
    """Compare adaptive methods with fixed top-k against the graded labels.

    For every ranking: every method's mean admitted size, KEY recall,
    precision (admitted graded >= 3), share admitted graded <= 1 and mean
    grade -- next to fixed top-k at k in `ks`, and next to the fixed-k
    baseline INTERPOLATED to the method's own mean admitted size, which is
    the only fair comparison (a bigger view buys recall for free).

    Returns {"rows": [...], "by_ranking": {...}, "aggregate": {...},
             "table": "<text>"}.
    """
    import json
    import os

    from . import composition as C
    from . import rankings as R
    from .corpus import get_corpus

    c = corpus if corpus is not None else get_corpus()
    if label_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        label_dir = os.path.normpath(os.path.join(here, "..", "review", "labels"))
    keymap = json.load(open(os.path.join(label_dir, "keymap.json")))
    grades, _meta, _mv = C.load_labels(label_dir, keymap)

    methods = tuple(methods or METHODS)
    names = tuple(rankings or R.names())

    base = np.where(c.universe(universe))[0]
    art = c.inc_artifact[base]
    n_art = int(art.max()) + 1
    gb = grade_array(c, base, grades)
    lab_arts = np.unique(art[gb >= 0])

    rows = []
    for nm in names:
        spec = R.get(nm)
        ranks = spec.ranks_within_proof(c, base)
        keys = spec.keys(c, base)

        fixed = []
        for k in range(1, kmax + 1):
            r = _score_mask(ranks < k, gb, art, lab_arts, n_art)
            r.update(ranking=nm, universe=universe, kind="top_k",
                     method=f"top_k={k}", param=k)
            fixed.append(r)
        fx_size = np.array([r["MeanAdmitted"] for r in fixed])

        def matched(size, field):
            y = np.array([r[field] for r in fixed], float)
            ok = np.isfinite(y) & np.isfinite(fx_size)
            if ok.sum() < 2:
                return float("nan")
            return float(np.interp(size, fx_size[ok], y[ok]))

        for k in ks:
            rows.append(fixed[k - 1])
        for sc in scales:
            seg = make_segments(c, base, ranks, keys, scale=sc)
            for meth in methods:
                mask = split_sizes(c, base, ranks, method=meth, seg=seg)
                r = _score_mask(mask, gb, art, lab_arts, n_art)
                r.update(ranking=nm, universe=universe,
                         kind="cluster" if sc == "level" else f"cluster[{sc}]",
                         method=meth if sc == "level" else f"{meth}[{sc}]",
                         param=None,
                         CorpusSizeFraction=float(mask.mean()))
                for f in ("KeyRecall", "PrecisionGraded", "BadShare",
                          "MeanGrade"):
                    r[f"matched_{f}"] = matched(r["MeanAdmitted"], f)
                r["beats_matched"] = bool(
                    r["KeyRecall"] > r["matched_KeyRecall"]
                    and r["PrecisionGraded"] > r["matched_PrecisionGraded"])
                rows.append(r)
                del mask
            del seg
        if verbose:
            print(f"  evaluated {nm}", flush=True)

    # aggregate over CANDIDATE rankings only: baselines are not the target
    cand = [n for n in names if R.get(n).family == "candidate"]
    agg = {}
    for r in rows:
        if r["ranking"] not in cand:
            continue
        a = agg.setdefault(r["method"], {"kind": r["kind"], "n": 0})
        a["n"] += 1
        for f in ("MeanAdmitted", "KeyRecall", "PrecisionGraded", "BadShare",
                  "MeanGrade", "matched_KeyRecall", "matched_PrecisionGraded",
                  "matched_BadShare", "matched_MeanGrade"):
            if f in r and r[f] == r[f]:
                a[f] = a.get(f, 0.0) + float(r[f])
    for a in agg.values():
        for f in list(a):
            if f not in ("kind", "n"):
                a[f] = a[f] / a["n"]

    by_ranking = {}
    for r in rows:
        by_ranking.setdefault(r["ranking"], {})[r["method"]] = r

    return {"universe": universe, "rankings": list(names),
            "methods": list(methods), "rows": rows, "by_ranking": by_ranking,
            "aggregate": agg,
            "table": format_table(agg),
            "n_labelled_proofs": int(len(lab_arts)),
            "n_labelled_candidates": int((gb >= 0).sum())}


def format_table(agg: Dict) -> str:
    """Aggregate comparison table, averaged over candidate rankings."""
    def f(v, d=3):
        return "  --  " if v is None or v != v else f"{v:.{d}f}"

    order = sorted(agg, key=lambda m: (agg[m]["kind"] != "top_k",
                                       agg[m].get("MeanAdmitted", 0.0)))
    w = max(len(m) for m in agg) + 2
    head = (f"{'policy':<{w}}{'size':>7}{'KeyRec':>8}{'Prec>=3':>9}"
            f"{'Bad<=1':>8}{'MeanG':>7}   | matched fixed-k at same size: "
            f"{'KeyRec':>7}{'Prec>=3':>9}{'Bad<=1':>8}")
    lines = [head, "-" * len(head)]
    for m in order:
        a = agg[m]
        base_ = ""
        if a["kind"] != "top_k":
            base_ = (f"   | {f(a.get('matched_KeyRecall')):>7}"
                     f"{f(a.get('matched_PrecisionGraded')):>9}"
                     f"{f(a.get('matched_BadShare')):>8}")
        lines.append(f"{m:<{w}}{f(a.get('MeanAdmitted'), 2):>7}"
                     f"{f(a.get('KeyRecall')):>8}"
                     f"{f(a.get('PrecisionGraded')):>9}"
                     f"{f(a.get('BadShare')):>8}"
                     f"{f(a.get('MeanGrade'), 2):>7}{base_}")
    return "\n".join(lines)
