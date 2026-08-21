#!/usr/bin/env python3
"""Correctness tests for the batched aggregator: brute force vs vectorised."""
import os
import sys
from itertools import permutations

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import social_choice as SC        # noqa: E402


class FakeCorpus:
    def __init__(self, art):
        self.inc_artifact = art


def brute(K, w):
    """Reference implementation, per proof, straight from the definitions."""
    L, n = K.shape
    midrank = np.zeros((L, n))
    for l in range(L):
        for a in range(n):
            better = sum(1 for b in range(n) if K[l, b] < K[l, a])
            ties = sum(1 for b in range(n) if K[l, b] == K[l, a])
            midrank[l, a] = better + (ties - 1) / 2
    W = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            W[a, b] = sum(w[l] for l in range(L) if K[l, a] < K[l, b])
    return midrank, W


def kemeny_cost(P, W):
    return sum(W[P[j], P[i]] for i in range(len(P)) for j in range(i + 1, len(P)))


def main():
    rng = np.random.default_rng(7)
    fails = 0
    n_exact = n_opt = 0
    gap_sum = 0.0
    for trial in range(300):
        n = int(rng.integers(2, 7))
        L = 4
        K = rng.integers(0, 4, size=(L, n)).astype(float)   # many ties on purpose
        w = np.ones(L)
        mr, W = brute(K, w)

        art = np.zeros(n, np.int64)
        c = FakeCorpus(art)
        base = np.arange(n)
        keys = {f"v{l}": K[l] for l in range(L)}
        agg = SC.Aggregator(c, base, keys, [f"v{l}" for l in range(L)])
        rules = dict(SC.RULES)
        got, extra = agg.run(rules)

        # midrank / majority matrix reproduced through borda and copeland
        if not np.allclose(got["borda"], mr.sum(axis=0)):
            fails += 1
            print("borda mismatch", K)
        beats = (W > W.T).sum(axis=1) - (W < W.T).sum(axis=1)
        if not np.allclose(got["copeland"], -beats):
            fails += 1
            print("copeland mismatch", K)
        cw = [a for a in range(n) if (W[a] > W[:, a]).sum() == n - 1]
        if len(cw) > 1:
            fails += 1
        if bool(extra["condorcet"].any()) != bool(cw):
            fails += 1
            print("condorcet mismatch", K)
        mm = np.array([min(W[a, b] for b in range(n) if b != a)
                       for a in range(n)])
        if not np.allclose(got["maximin_pairwise"], -mm):
            fails += 1
            print("maximin mismatch", K)
        if not np.allclose(got["minimax_rank"] - got["borda"] /
                           (L * n + 1.0), mr.max(axis=0)):
            fails += 1
            print("minimax_rank mismatch", K)

        # kemeny heuristic against the exact optimum
        if n <= 6:
            order = np.argsort(got["kemeny"], kind="stable")
            best = min(permutations(range(n)), key=lambda P: kemeny_cost(P, W))
            c_h = kemeny_cost(list(order), W)
            c_o = kemeny_cost(list(best), W)
            n_opt += 1
            n_exact += int(abs(c_h - c_o) < 1e-9)
            gap_sum += (c_h - c_o)
    print(f"failures: {fails}")
    print(f"kemeny heuristic optimal on {n_exact}/{n_opt} random proofs, "
          f"mean cost gap {gap_sum / max(n_opt,1):.4f}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
