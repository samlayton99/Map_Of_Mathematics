#!/usr/bin/env python
"""Study-path engine over the exact MathRecord corpus graph.

Turns the Phase 3 corpus record (six Mathlib files, 3,662 declarations) into
navigation: for a target declaration T it computes, exactly,

  A_S(T)  statement cone -- everything reachable from the constants in T's
          statement (type-layer out-edges), i.e. what you must already have
          to UNDERSTAND THE CLAIM;
  A_P(T)  proof cone -- everything reachable from T's proof term
          (body-layer out-edges);
  N(T)  = A_P \\ A_S -- the mathematics the proof introduces beyond what
          stating the problem already required ("the moves", per
          studies/phase3_structural_separability/reports/CONES_REPORT.md).

and renders them as an ordered study path:

  1. statement prerequisites, machinery-marked (P3 classes as labels, never
     silent deletion -- reversible filtering only), grouped by dependency
     depth, ranked within a depth layer by how often the rest of the cone
     uses them;
  2. the proof's new mathematics ranked "new, then depth" -- the method that
     scored 0.775 median move-identification vs 0.708 for depth alone.

Definitions mirror src/cones.py: closure follows body-layer deps where a
declaration has them, else type-layer deps ("unfold" deps). The corpus
truncates at the extraction boundary (shallow imported nodes have no
out-edges); every result reports how many cone members are boundary nodes.

Usage:
  study_path.py Real.log_mul                     # print a study path
  study_path.py A B C --json out.json            # machine-readable
  study_path.py --index proof_moves_index.jsonl  # whole-corpus moves index
"""
import argparse
import csv
import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "studies" / "phase3_structural_separability" / "data"
P3 = ["typeclass-instance", "structure-projection", "recursor", "generated",
      "internal-detail", "eq-machinery", "logic-core", "coercion"]


class Corpus:
    """The exact corpus graph. u -> v means u refers to v."""

    def __init__(self, names, kind, stored, p3flags, files, type_out, body_out):
        self.names = names
        self.idx = {n: i for i, n in enumerate(names)}
        self.kind = kind
        self.stored = stored
        self.p3 = p3flags              # per node: tuple of P3 class names
        self.files = files
        self.type_out = type_out       # per node: {dst: mult}
        self.body_out = body_out
        self.n = len(names)
        self.unfold = [list((body_out[i] or type_out[i]).keys())
                       for i in range(self.n)]
        self.depth, self.order = self._depths()
        self.masks = self._ancestor_masks()
        self.users = [0] * self.n      # direct users on unfold graph
        for i in range(self.n):
            for d in self.unfold[i]:
                self.users[d] += 1

    def _depths(self):
        """Longest chain beneath each node on the unfold graph (a DAG)."""
        indeg = [0] * self.n
        rev = [[] for _ in range(self.n)]
        for i in range(self.n):
            for d in self.unfold[i]:
                indeg[i] += 0  # placeholder for symmetry
        # depth over deps: process nodes after all their deps
        pend = [len(self.unfold[i]) for i in range(self.n)]
        for i in range(self.n):
            for d in self.unfold[i]:
                rev[d].append(i)
        depth = [0] * self.n
        q = deque(i for i in range(self.n) if pend[i] == 0)
        order = []
        while q:
            v = q.popleft()
            order.append(v)
            for u in rev[v]:
                if depth[v] + 1 > depth[u]:
                    depth[u] = depth[v] + 1
                pend[u] -= 1
                if pend[u] == 0:
                    q.append(u)
        if len(order) != self.n:
            raise RuntimeError("unfold graph is not a DAG")
        return depth, order

    def _ancestor_masks(self):
        """Exact ancestor set per node as int bitmask, one topo pass."""
        masks = [0] * self.n
        for v in self.order:           # deps before users
            m = 0
            for d in self.unfold[v]:
                m |= masks[d] | (1 << d)
            masks[v] = m
        return masks

    def cone_from(self, seeds):
        """Exact closure (as a set of ids) downward from an iterable of ids."""
        m = 0
        for s in seeds:
            m |= self.masks[s] | (1 << s)
        out, i = set(), 0
        while m:
            low = m & -m
            out.add(low.bit_length() - 1)
            m ^= low
        return out


def load_corpus(data_dir=DATA):
    names, kind, stored, p3flags, files = [], [], [], [], []
    with open(Path(data_dir) / "node_inventory.csv") as f:
        for row in csv.DictReader(f):
            names.append(row["name"])
            kind.append(row["kind"])
            stored.append(int(row["stored"]))
            p3flags.append(tuple(c for c in P3 if int(row[f"p3_{c}"])))
            files.append(row["files"].split("|"))
    idx = {n: i for i, n in enumerate(names)}
    type_out = [dict() for _ in names]
    body_out = [dict() for _ in names]
    with open(Path(data_dir) / "edge_inventory.csv") as f:
        for row in csv.DictReader(f):
            s, d, m = idx[row["src"]], idx[row["dst"]], int(row["mult"])
            layer = type_out if row["layer"] == "type" else body_out
            layer[s][d] = layer[s].get(d, 0) + m
    return Corpus(names, kind, stored, p3flags, files, type_out, body_out)


# ------------------------------------------------------------------ analysis

def cones(c, t):
    """(A_S, A_P, N) for target id t. Sets exclude t itself."""
    a_s = c.cone_from(c.type_out[t].keys())
    a_p = c.cone_from(c.body_out[t].keys())
    return a_s, a_p, a_p - a_s


def in_cone_usage(c, cone, t):
    """For each cone member, how many members of cone+{t} directly use it."""
    use = {i: 0 for i in cone}
    for v in list(cone) + [t]:
        for d in c.unfold[v]:
            if d in use:
                use[d] += 1
    return use


def build_path(c, target, per_layer=6, drop_machinery=False):
    t = c.idx.get(target)
    if t is None:
        raise KeyError(f"'{target}' is not in the corpus")
    a_s, a_p, new = cones(c, t)
    use = in_cone_usage(c, a_s, t)

    def item(i, extra=None):
        d = {"name": c.names[i], "kind": c.kind[i], "depth": c.depth[i],
             "machinery": list(c.p3[i]), "stored": bool(c.stored[i])}
        if extra:
            d.update(extra)
        return d

    # --- statement path: depth layers, ranked by in-cone usage ---
    is_mach = {i: bool(c.p3[i]) for i in a_s | new}
    layers = {}
    for i in a_s:
        if drop_machinery and is_mach[i]:
            continue
        layers.setdefault(c.depth[i], []).append(i)
    stmt_path = []
    for d in sorted(layers):
        ranked = sorted(layers[d], key=lambda i: (-use[i], c.names[i]))
        shown = [i for i in ranked if not is_mach[i]][:per_layer]
        mach = [i for i in ranked if is_mach[i]]
        stmt_path.append({
            "depth": d,
            "items": [item(i, {"used_by_in_cone": use[i]}) for i in shown],
            "more": len([i for i in ranked if not is_mach[i]]) - len(shown),
            "machinery_here": 0 if drop_machinery else len(mach),
        })

    # --- proof moves: N(T), ranked new-then-depth ---
    puse = in_cone_usage(c, a_p, t)
    moves = sorted(new, key=lambda i: (-c.depth[i], c.names[i]))
    moves_out = [item(i, {"used_by_in_proof_cone": puse[i]}) for i in moves]

    boundary = sum(1 for i in a_s | a_p
                   if not c.stored[i] and not c.unfold[i])
    return {
        "target": item(t),
        "statement_cone_size": len(a_s),
        "proof_cone_size": len(a_p),
        "new_count": len(new),
        "new_share": round(len(new) / len(a_p), 3) if a_p else None,
        "proof_stays_in_statement_cone": bool(a_p) and not new,
        "boundary_nodes_in_cones": boundary,
        "statement_path": stmt_path,
        "proof_moves": moves_out,
    }


def corpus_index(c, top_moves=5):
    """One record per stored theorem: cone sizes + top proof moves."""
    out = []
    for t in range(c.n):
        if c.kind[t] != "theorem" or not c.stored[t] or not c.body_out[t]:
            continue
        a_s, a_p, new = cones(c, t)
        moves = sorted(new, key=lambda i: (-c.depth[i], c.names[i]))
        out.append({
            "name": c.names[t],
            "files": c.files[t],
            "machinery": list(c.p3[t]),
            "statement_cone": len(a_s),
            "proof_cone": len(a_p),
            "new": len(new),
            "new_share": round(len(new) / len(a_p), 3) if a_p else None,
            "top_moves": [c.names[i] for i in moves[:top_moves]],
            "top_math_moves": [c.names[i] for i in moves if not c.p3[i]][:top_moves],
        })
    return out


# ------------------------------------------------------------------ rendering

def render_text(r):
    L = []
    t = r["target"]
    mach = f"  [{' '.join(t['machinery'])}]" if t["machinery"] else ""
    L.append(f"== {t['name']}  ({t['kind']}, depth {t['depth']}){mach}")
    L.append(f"   statement cone {r['statement_cone_size']} | proof cone "
             f"{r['proof_cone_size']} | new {r['new_count']}"
             + (f" ({r['new_share']:.0%} of proof cone)" if r["new_share"] is not None else "")
             + f" | boundary nodes {r['boundary_nodes_in_cones']}")
    L.append("")
    L.append("-- To understand the statement (dependency order, most-used first per layer):")
    for layer in r["statement_path"]:
        for it in layer["items"]:
            L.append(f"   d{layer['depth']:>2}  {it['name']}"
                     f"  ({it['kind']}, used by {it['used_by_in_cone']} in cone)")
        notes = []
        if layer["more"] > 0:
            notes.append(f"+{layer['more']} more")
        if layer["machinery_here"]:
            notes.append(f"{layer['machinery_here']} machinery")
        if notes:
            L.append(f"   d{layer['depth']:>2}  ... {', '.join(notes)}")
    L.append("")
    if r["proof_stays_in_statement_cone"]:
        L.append("-- Proof introduces NOTHING beyond the statement's own cone"
                 " (interface theorem).")
    elif not r["proof_moves"]:
        L.append("-- No proof body in the corpus record (shallow/imported or axiom).")
    else:
        math = [m for m in r["proof_moves"] if not m["machinery"]]
        glue = [m for m in r["proof_moves"] if m["machinery"]]
        L.append("-- What the proof actually adds, deepest first (the moves):")
        for it in math[:12]:
            L.append(f"   d{it['depth']:>2}  {it['name']}  ({it['kind']})")
        if len(math) > 12:
            L.append(f"        ... +{len(math) - 12} more new mathematical facts")
        if glue:
            cls = {}
            for m in glue:
                for c in m["machinery"]:
                    cls[c] = cls.get(c, 0) + 1
            top = ", ".join(f"{k} {v}" for k, v in
                            sorted(cls.items(), key=lambda x: -x[1])[:3])
            L.append(f"   (+{len(glue)} machinery/glue also entered the proof: {top})")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("targets", nargs="*", help="declaration names")
    ap.add_argument("--json", metavar="PATH", help="write results as JSON")
    ap.add_argument("--index", metavar="PATH",
                    help="write whole-corpus proof-moves index (JSONL)")
    ap.add_argument("--per-layer", type=int, default=6)
    ap.add_argument("--drop-machinery", action="store_true",
                    help="hide P3-machinery from the statement path (reversible view)")
    a = ap.parse_args(argv)
    if not a.targets and not a.index:
        ap.error("give declaration names or --index")
    c = load_corpus()
    if a.index:
        rows = corpus_index(c)
        with open(a.index, "w") as f:
            for r in rows:
                f.write(json.dumps(r, separators=(",", ":")) + "\n")
        print(f"wrote {len(rows)} theorem records to {a.index}")
        interface = sum(1 for r in rows if r["new"] == 0)
        shares = sorted(r["new_share"] for r in rows if r["new_share"] is not None)
        print(f"  interface theorems (proof adds nothing): {interface} "
              f"({interface / len(rows):.0%})")
        if shares:
            print(f"  new-share of proof cone: median "
                  f"{shares[len(shares) // 2]:.0%}, p90 "
                  f"{shares[int(len(shares) * .9)]:.0%}")
    results = []
    for tgt in a.targets:
        r = build_path(c, tgt, per_layer=a.per_layer,
                       drop_machinery=a.drop_machinery)
        results.append(r)
        print(render_text(r))
        print()
    if a.json:
        with open(a.json, "w") as f:
            json.dump(results, f, indent=1)
        print(f"wrote {a.json}")


if __name__ == "__main__":
    main()
