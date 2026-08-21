#!/usr/bin/env python3
"""Semantic keyness panel -- preparation.

PRE-REGISTERED DESIGN (fixed before any brief was generated):

  scale        25 proofs spread across the six registered target-depth bands
               (4 per band, 5 in the deepest). 3 raters, ALL rating the SAME
               25, so inter-rater agreement is measurable. A vibes check, not
               a certification.
  universe     U1D (load-bearing roles for theorems, all roles for
               definitions) -- the universe the coverage work settled on.
  eligibility  proofs with 3..25 candidates, so the task fits ~30s each.
               DECLARED SCOPE LIMIT: trivial proofs (<3) and monsters (>25)
               are out of this panel and their behaviour is not measured here.
  blinding     raters never see any ranking. Candidates are SHUFFLED with a
               per-proof seed. One annotation therefore scores every ranking,
               present and future, with no anchoring.
  task         pick the 1-3 citations that are the KEY MOVES, or answer
               NONE_LISTED if the real key move is absent from the list.
               NONE_LISTED is itself a measurement: it is semantic evidence
               of the candidate-coverage gap.

Registered predictions (may be wrong; recorded so they can fail):
  P1  R_introduced_depth will lead on SemanticCoreHit@1, consistent with its
      SourceHit@1 lead.
  P2  NONE_LISTED will be more common in the two shallowest bands, where
      coverage is worst and glue is most often the content.
  P3  inter-rater agreement will be lower at shallow depth than deep.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "review", "panel")
BANDS = [(0, 11), (11, 26), (26, 51), (51, 76), (76, 126), (126, 10**9)]
LABELS = ["0-10", "11-25", "26-50", "51-75", "76-125", "126+"]
TOTAL = 25
PER_BAND = [4, 4, 4, 4, 4, 5]   # sums to TOTAL
SEED = 20260820
MIN_CAND, MAX_CAND = 3, 25
KIND_NAMES = ["theorem", "def", "inductive", "constructor", "recursor",
              "opaque", "quot", "axiom", "?"]


def main():
    import sys
    sys.path.insert(0, ROOT)
    from mathmap_eval.corpus import get_corpus
    c = get_corpus()
    base = np.where(c.universe("U1D"))[0]
    rng = np.random.default_rng(SEED)

    by_art = {}
    for p in base:
        by_art.setdefault(int(c.inc_artifact[p]), []).append(int(p))

    # eligible artifacts: human-written theorems with a workable candidate count
    elig = []
    for a, pl in by_art.items():
        d = int(c.art_certifies[a])
        if c.node_gen[d] or c.node_kind[d] != 0:
            continue
        if not (MIN_CAND <= len(pl) <= MAX_CAND):
            continue
        elig.append((a, d, len(pl), int(c.node_depth[d])))
    print(f"eligible proofs: {len(elig):,}", flush=True)

    chosen = []
    for lab, (lo, hi), want in zip(LABELS, BANDS, PER_BAND):
        pool = [e for e in elig if lo <= e[3] < hi]
        if not pool:
            continue
        pick = rng.choice(len(pool), size=min(want, len(pool)), replace=False)
        for i in pick:
            chosen.append((lab,) + pool[int(i)])
    print(f"selected: {len(chosen)} proofs", flush=True)

    briefs, key = [], {}
    for n, (lab, a, d, ncand, dep) in enumerate(chosen, 1):
        pid = f"proof_{n:02d}"
        pl = by_art[a]
        srng = np.random.default_rng(SEED + n)
        order = srng.permutation(len(pl))
        items = []
        for j, oi in enumerate(order, 1):
            p = pl[int(oi)]
            di = int(c.inc_decl[p])
            items.append({"n": j, "name": c.names[di],
                          "kind": KIND_NAMES[int(c.node_kind[di])],
                          "depth": int(c.node_depth[di]),
                          "in_statement": bool(c.inc_in_stmt_world[p]),
                          "_incidence": p})
        key[pid] = {"artifact": a, "declaration": c.names[d], "band": lab,
                    "depth": dep,
                    "items": {it["n"]: it["_incidence"] for it in items}}
        briefs.append({
            "id": pid, "theorem": c.names[d], "theorem_depth": dep,
            "band": lab,
            "candidates": [{k: v for k, v in it.items() if k != "_incidence"}
                           for it in items]})

    os.makedirs(OUT, exist_ok=True)
    json.dump(briefs, open(os.path.join(OUT, "briefs.json"), "w"), indent=1)
    json.dump(key, open(os.path.join(OUT, "keymap.json"), "w"), indent=1)

    lines = []
    for b in briefs:
        lines.append(f"### {b['id']}  (depth {b['theorem_depth']}, band {b['band']})")
        lines.append(f"THEOREM BEING PROVED: `{b['theorem']}`")
        lines.append("")
        lines.append("Citations used by this proof, in random order:")
        lines.append("")
        for it in b["candidates"]:
            stmt = "in-statement" if it["in_statement"] else "introduced-by-proof"
            lines.append(f"  {it['n']:>2}. {it['name']}")
            lines.append(f"      [{it['kind']}, depth {it['depth']}, {stmt}]")
        lines.append("")
    open(os.path.join(OUT, "briefs.md"), "w").write("\n".join(lines))
    print(f"written {OUT}/briefs.json, keymap.json, briefs.md", flush=True)
    print(f"candidates per proof: "
          f"{np.mean([len(b['candidates']) for b in briefs]):.1f} mean", flush=True)


if __name__ == "__main__":
    main()
