#!/usr/bin/env python3
"""Graded keyness labels -- preparation.

The 25-proof vibes panel used BINARY picks, which cannot separate "there is
glue at rank 1" from "there is BAD glue at rank 1". This builds the larger,
GRADED label set that the rank-composition and precision/recall dashboard
needs.

PRE-REGISTERED DESIGN (fixed before any brief was generated):

  scale        180 proofs, 30 per target-depth band, so every band has enough
               n for a composition row. 9 batches of 20, one rater each.
               Batch 01 is additionally labelled by 2 extra raters, giving a
               20-proof overlap set for inter-rater agreement on the RUBRIC
               (the previous panel measured agreement on binary picks only).
  universe     U1D. Raters see EVERY candidate of the proof, shuffled.
  labels       graded 0-4 on EVERY candidate, not a pick-3. A graded label on
               every candidate is what makes rank-composition computable:
               whatever a ranking puts at rank 1 already has a label.
  blinding     no ranking is ever shown; per-proof shuffle seed.
  coverage     raters additionally report whether a key move is MISSING from
               the candidate list -- the semantic coverage gap.

Registered predictions (recorded so they can fail):
  Q1  BadGlue@1 falls monotonically with target depth for every candidate
      ranking: glue at rank 1 is mostly LEGITIMATE near the foundations.
  Q2  R_v8_faithful has lower BadGlue@1 than R_introduced_depth but also lower
      KeyMoveRecall@4, i.e. V8's demotions trade recall for precision.
  Q3  system `inc_glue` has high glue PRECISION and poor glue RECALL: what it
      calls glue really is plumbing, but much plumbing is not caught.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "review", "labels")
BANDS = [(0, 11), (11, 26), (26, 51), (51, 76), (76, 126), (126, 10**9)]
LABELS = ["0-10", "11-25", "26-50", "51-75", "76-125", "126+"]
PER_BAND = 30
BATCH = 20
OVERLAP_BATCH = "batch_01"      # additionally labelled by 2 extra raters
SEED = 20260821                 # fresh seed, not reused from any prior round
MIN_CAND, MAX_CAND = 3, 25
KIND_NAMES = ["theorem", "def", "inductive", "constructor", "recursor",
              "opaque", "quot", "axiom", "?"]
ROLE_NAMES = ["applied", "let-value", "explicit-arg", "implicit-arg",
              "instance-slot", "strict-implicit", "type-annotation",
              "unresolved"]

RUBRIC = """\
## The grade

Give **every** candidate a grade 0-4. Do not pick a top few -- grade all of
them. The grade is about THIS proof, not about the declaration in general.

| grade | name | meaning |
|---|---|---|
| **4** | `KEY` | A core move. If asked "how does this proof go?", you would name it. Removing it destroys the proof's central idea. |
| **3** | `SUPPORT` | Real mathematical content, genuinely used, but secondary -- a lemma the key move needs, a rewrite that does actual work. |
| **2** | `LEGIT_GLUE` | Logical or structural plumbing (`Eq.trans`, `congrArg`, `Iff.mpr`, coercions, instances) that **is genuinely the content of this proof**. Near the foundations, assembling equalities really can be the whole argument. |
| **1** | `BAD_GLUE` | Plumbing or background that is present but carries no idea here. A person explaining the proof would never mention it. Correct to demote. |
| **0** | `JUNK` | Irrelevant machinery: automation residue, instance/typeclass resolution, universe or decidability bookkeeping, notation unfolding. Noise. |

The 2-versus-1 line is the important one and it is the whole reason this
panel exists. **Do not grade something 1 just because it looks like plumbing.**
Ask whether a mathematician explaining *this specific theorem* would mention
it. If yes, it is 2 even if its name looks like machinery. If the theorem is a
deep result and the item is `Eq.mpr`, that is 1.

## Also required, per proof

`missing_key`: `true` if you believe this proof has a key move that is **not
in the list at all** -- it works by manipulating local hypotheses, exhibiting
a witness, splitting into cases, or pure rewriting, and no listed citation
captures that. This is a genuine measurement of our coverage gap, not a
failure to do the task. Otherwise `false`.

`confidence`: `high` / `medium` / `low` -- whether you understood the theorem
well enough to grade it.

## Output format

Return **only** a JSON object, no commentary. Every proof id in your batch
must appear exactly once, and every candidate number of that proof must
appear exactly once in its `grades` map.

```json
{
  "proof_007": {
    "grades": {"1": 1, "2": 4, "3": 0, "4": 3, "5": 2},
    "missing_key": false,
    "confidence": "high"
  }
}
```
"""


def main():
    sys.path.insert(0, ROOT)
    from mathmap_eval.corpus import get_corpus
    c = get_corpus()
    base = np.where(c.universe("U1D"))[0]
    rng = np.random.default_rng(SEED)

    by_art = {}
    for p in base:
        by_art.setdefault(int(c.inc_artifact[p]), []).append(int(p))

    prov = set(c.source_refs)
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
    for lab, (lo, hi) in zip(LABELS, BANDS):
        pool = [e for e in elig if lo <= e[3] < hi]
        pick = rng.choice(len(pool), size=min(PER_BAND, len(pool)), replace=False)
        for i in pick:
            chosen.append((lab,) + pool[int(i)])
    # interleave bands so every batch spans the depth range
    chosen.sort(key=lambda t: (LABELS.index(t[0]),))
    order = []
    per = {lab: [t for t in chosen if t[0] == lab] for lab in LABELS}
    for i in range(PER_BAND):
        for lab in LABELS:
            if i < len(per[lab]):
                order.append(per[lab][i])
    chosen = order
    print(f"selected: {len(chosen)} proofs", flush=True)

    key, briefs = {}, []
    for n, (lab, a, d, ncand, dep) in enumerate(chosen, 1):
        pid = f"proof_{n:03d}"
        pl = by_art[a]
        srng = np.random.default_rng(SEED + 7919 * n)
        perm = srng.permutation(len(pl))
        items = []
        for j, oi in enumerate(perm, 1):
            p = pl[int(oi)]
            di = int(c.inc_decl[p])
            r = c.inc_roles[p]
            items.append({
                "n": j, "name": c.names[di],
                "kind": KIND_NAMES[int(c.node_kind[di])],
                "depth": int(c.node_depth[di]),
                "in_statement": bool(c.inc_in_stmt_world[p]),
                "role": ROLE_NAMES[int(np.argmax(r))],
                "_incidence": p, "_decl": di,
            })
        key[pid] = {"artifact": a, "declaration": c.names[d], "band": lab,
                    "depth": dep, "has_provenance": c.names[d] in prov,
                    "batch": f"batch_{(n - 1) // BATCH + 1:02d}",
                    "items": {it["n"]: it["_incidence"] for it in items},
                    "decls": {it["n"]: it["_decl"] for it in items}}
        briefs.append({"id": pid, "theorem": c.names[d], "theorem_depth": dep,
                       "band": lab, "batch": key[pid]["batch"],
                       "candidates": [{k2: v for k2, v in it.items()
                                       if not k2.startswith("_")}
                                      for it in items]})

    os.makedirs(OUT, exist_ok=True)
    json.dump(key, open(os.path.join(OUT, "keymap.json"), "w"), indent=1)
    json.dump(briefs, open(os.path.join(OUT, "briefs.json"), "w"), indent=1)

    batches = sorted({b["batch"] for b in briefs})
    for bt in batches:
        bb = [b for b in briefs if b["batch"] == bt]
        L = [f"# Grading batch `{bt}` -- {len(bb)} proofs", "",
             "You are one of several independent raters. You will never see any",
             "ranking our system produces and must not try to guess one. Your",
             "grades are the ground truth those rankings are scored against.",
             "", "Candidates are listed in RANDOM order. Position means nothing.",
             "", "`depth` = how much mathematics sits beneath a declaration in the",
             "library. It is context so you can tell a deep theorem from a",
             "primitive. It is NOT a hint and you must not grade something high",
             "merely because it is deep, nor low because it is shallow.",
             "", "`in-statement` = already implied by what the theorem says.",
             "`introduced-by-proof` = the proof brought it in. Either can be key.",
             "", RUBRIC, "", "---", ""]
        for b in bb:
            L.append(f"### {b['id']}  (target depth {b['theorem_depth']}, "
                     f"band {b['band']})")
            L.append("")
            L.append(f"THEOREM PROVED: `{b['theorem']}`")
            L.append("")
            L.append(f"Grade all {len(b['candidates'])} candidates below.")
            L.append("")
            for it in b["candidates"]:
                st = "in-statement" if it["in_statement"] else "introduced-by-proof"
                L.append(f"  {it['n']:>2}. `{it['name']}`")
                L.append(f"      [{it['kind']}, depth {it['depth']}, {st}, "
                         f"role {it['role']}]")
            L.append("")
        open(os.path.join(OUT, f"{bt}.md"), "w").write("\n".join(L))

    sizes = [len(b["candidates"]) for b in briefs]
    print(f"batches: {len(batches)}  candidates/proof: mean {np.mean(sizes):.1f} "
          f"median {np.median(sizes):.0f}  total labels {sum(sizes):,}", flush=True)
    print(f"provenance overlap: {sum(v['has_provenance'] for v in key.values())}"
          f"/{len(key)} proofs", flush=True)
    print(f"written {OUT}/", flush=True)


if __name__ == "__main__":
    main()
