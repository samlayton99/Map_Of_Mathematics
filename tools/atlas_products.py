#!/usr/bin/env python
"""Derived products from the full-Mathlib moves index (tools/atlas.py index).

Inputs (bigdata/): mathlib_moves_index.jsonl, mathlib_usage_counters.npz,
atlas cache.  Outputs (tools/output/):

  mathlib_interface_atlas.json   theorems with small statements and heavy
                                 proofs — the load-bearing abstraction
                                 boundaries of the library, ranked by
                                 leverage = proof_cone / statement_cone
                                 and by how many other proofs rest on them.
  mathlib_moves_vocabulary.json  the facts that actually appear as NEW moves
                                 inside other proofs, globally and per
                                 top-level namespace: the working vocabulary
                                 of mathematical practice, measured exactly.
  mathlib_atlas_summary.txt      headline numbers.

Run: ~/venv/general_ml/bin/python tools/atlas_products.py
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BIG = ROOT / "bigdata"
OUT = Path(__file__).resolve().parent / "output"
INDEX = BIG / "mathlib_moves_index.jsonl"
COUNTERS = BIG / "mathlib_usage_counters.npz"


def top_namespace(name):
    head = name.split(".", 1)[0]
    return head


def load_index(path=INDEX):
    rows = []
    with open(path) as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def interface_atlas(rows, limit=250, min_proof=200):
    """Small statement, heavy proof: high leverage boundaries."""
    scored = []
    for r in rows:
        if r["machinery"] or r["proof_cone"] < min_proof:
            continue
        lev = r["proof_cone"] / max(r["statement_cone"], 1)
        scored.append((lev, r))
    scored.sort(key=lambda x: -x[0])
    out = []
    for lev, r in scored[:limit]:
        out.append({
            "name": r["name"],
            "leverage": round(lev, 1),
            "statement_cone": r["statement_cone"],
            "proof_cone": r["proof_cone"],
            "new": r["new"],
            "new_share": r["new_share"],
            "top_math_moves": [m["name"] for m in r["top_math_moves"][:5]],
        })
    return out


def moves_vocabulary(atlas_names, atlas_kind, atlas_cls, counters,
                     per_ns=15, global_top=120):
    """Rank constants by how often they appear as a NEW move in a proof."""
    asNew = counters["asNew"]
    inP = counters["inP"]
    order = np.argsort(-asNew, kind="stable")
    vocab, ns_vocab = [], defaultdict(list)
    for i in order:
        i = int(i)
        if asNew[i] == 0:
            break
        if atlas_kind[i] != "theorem" or atlas_cls[i]:
            continue
        entry = {"name": atlas_names[i],
                 "times_as_new_move": int(asNew[i]),
                 "times_in_proof_cones": int(inP[i])}
        if len(vocab) < global_top:
            vocab.append(entry)
        ns = top_namespace(atlas_names[i])
        if len(ns_vocab[ns]) < per_ns:
            ns_vocab[ns].append(entry)
        if len(vocab) >= global_top and \
                all(len(v) >= per_ns for v in ns_vocab.values()) and \
                len(ns_vocab) > 60:
            break
    big_ns = {ns: v for ns, v in sorted(ns_vocab.items(),
                                        key=lambda kv: -kv[1][0]["times_as_new_move"])
              if v[0]["times_as_new_move"] >= 25}
    return {"global": vocab, "by_namespace": big_ns}


def summary(rows, counters):
    n = len(rows)
    new0 = sum(1 for r in rows if r["new"] == 0)
    shares = np.array([r["new_share"] for r in rows])
    pc = np.array([r["proof_cone"] for r in rows])
    sc = np.array([r["statement_cone"] for r in rows])
    lines = []
    lines.append("FULL-MATHLIB MOVES INDEX: SUMMARY")
    lines.append(f"theorem roots indexed: {n:,}")
    lines.append(f"interface theorems (proof stays inside statement cone): "
                 f"{new0:,} ({new0 / n:.1%})")
    lines.append(f"new-share: median {np.median(shares):.3f}, "
                 f"p90 {np.percentile(shares, 90):.3f}")
    lines.append(f"statement cone: median {int(np.median(sc)):,}, "
                 f"p90 {int(np.percentile(sc, 90)):,}")
    lines.append(f"proof cone: median {int(np.median(pc)):,}, "
                 f"p90 {int(np.percentile(pc, 90)):,}")
    asNew = counters["asNew"]
    lines.append(f"constants appearing as a new move at least once: "
                 f"{int((asNew > 0).sum()):,}")
    return "\n".join(lines) + "\n"


def main():
    from atlas import load_dump
    OUT.mkdir(exist_ok=True)
    print("loading atlas + index...")
    atlas = load_dump()
    rows = load_index()
    counters = np.load(COUNTERS)

    ia = interface_atlas(rows)
    (OUT / "mathlib_interface_atlas.json").write_text(
        json.dumps(ia, indent=1))
    print(f"interface atlas: {len(ia)} theorems")

    mv = moves_vocabulary(atlas.names, atlas.kind, atlas.cls, counters)
    (OUT / "mathlib_moves_vocabulary.json").write_text(
        json.dumps(mv, indent=1))
    print(f"moves vocabulary: {len(mv['global'])} global, "
          f"{len(mv['by_namespace'])} namespaces")

    s = summary(rows, counters)
    (OUT / "mathlib_atlas_summary.txt").write_text(s)
    print(s)


if __name__ == "__main__":
    main()
