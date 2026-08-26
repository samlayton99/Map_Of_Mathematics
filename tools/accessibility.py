#!/usr/bin/env python
"""Accessible-premise universes from the module graph.

A theorem may only use declarations from (transitively) imported modules,
or declared EARLIER in its own module.  Built from bigdata/mathlib_modules
.jsonl (mathrecord moddump): per module - name, direct imports, constants
in declaration order.

API:
    acc = Accessibility(atlas)
    mask = acc.mask(node_id)     # boolean over atlas nodes: legal universe
    acc.mod_of[i], acc.pos_of[i] # module idx and intra-module position
"""
import json
from pathlib import Path

import numpy as np

from atlas import BIG

MODULES = BIG / "mathlib_modules.jsonl"


class Accessibility:
    def __init__(self, atlas, path=MODULES):
        self.atlas = atlas
        mods = []
        with open(path) as f:
            for line in f:
                mods.append(json.loads(line))
        self.n_mods = len(mods)
        self.mod_names = [m["name"] for m in mods]
        midx = {m["name"]: m["i"] for m in mods}
        n = atlas.n
        self.mod_of = np.full(n, -1, dtype=np.int32)
        self.pos_of = np.full(n, -1, dtype=np.int64)
        for m in mods:
            i = m["i"]
            for pos, cn in enumerate(m["consts"]):
                j = atlas.idx.get(cn)
                if j is not None and self.mod_of[j] < 0:
                    self.mod_of[j] = i
                    self.pos_of[j] = pos
        self.unmapped = int((self.mod_of < 0).sum())

        # transitive import closure as bitsets (n_mods x words)
        W = (self.n_mods + 63) // 64
        clo = np.zeros((self.n_mods, W), dtype=np.uint64)
        order = self._topo(mods, midx)
        self.direct = [[midx[im] for im in m["imports"] if im in midx]
                       for m in mods]
        for i in order:                      # imports before importers
            w, b = divmod(i, 64)
            clo[i, w] |= np.uint64(1 << b)   # module sees itself
            for d in self.direct[i]:
                clo[i] |= clo[d]
        self.closure = clo
        self.W = W

    def _topo(self, mods, midx):
        indeg = np.zeros(self.n_mods, dtype=np.int64)
        users = [[] for _ in range(self.n_mods)]
        deps = []
        for m in mods:
            ds = [midx[im] for im in m["imports"] if im in midx]
            deps.append(ds)
            indeg[m["i"]] = len(ds)
            for d in ds:
                users[d].append(m["i"])
        from collections import deque
        q = deque(np.where(indeg == 0)[0].tolist())
        order = []
        while q:
            v = q.popleft()
            order.append(v)
            for u in users[v]:
                indeg[u] -= 1
                if indeg[u] == 0:
                    q.append(u)
        if len(order) != self.n_mods:
            raise RuntimeError("module import graph is not a DAG")
        return order

    def module_visible(self, node):
        """Bool over modules: which modules node's location can see."""
        m = self.mod_of[node]
        if m < 0:
            return None
        bits = np.unpackbits(self.closure[m].view(np.uint8), bitorder="little")
        return bits[:self.n_mods].astype(bool)

    def mask(self, node):
        """Boolean over atlas nodes: the legal premise universe at node's
        source location - transitively imported modules plus the node's own
        module IN FULL.  (ModuleData.constNames is serialization order, not
        source order - validated: all mask violations were same-module, none
        cross-module - so intra-module position cannot be used for a strict
        earlier-only cut.  Own-module-in-full is mildly optimistic at file
        granularity, the standard fallback absent source line numbers.)"""
        m = self.mod_of[node]
        if m < 0:
            return None
        vis = self.module_visible(node)
        ok = np.zeros(self.atlas.n, dtype=bool)
        mapped = self.mod_of >= 0
        ok[mapped] = vis[self.mod_of[mapped]]
        return ok
