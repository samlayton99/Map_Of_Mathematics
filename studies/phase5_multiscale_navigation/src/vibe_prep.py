#!/usr/bin/env python3
"""Vibe-check set -- one fixed, seeded, depth-stratified set of 12 proofs.

The SAME 12 proofs are used for every ranking experiment, so the viewer can
toggle rankings over identical material and the comparison is like-for-like.
Drawn from the graded label set, so every candidate already carries a rater
grade next to whatever rank a ranking gives it.

Selection rule (fixed here, before inspection):
  * 2 proofs per target-depth band, 12 total -- shallow, middle and deep.
  * within each band, one SEEDED-RANDOM pick and one THEOREM-RICHEST pick
    (lowest fraction of definition candidates).

The second rule exists because U1D is 83% definitions on average and 98% of
proofs are majority-definition, so a purely random draw is 12/12
definition-heavy and shows no contrast. Taking the theorem-richest proof of
each band guarantees the set spans the kind mix while staying deterministic.
Definition-heavy examples are therefore automatic, not quota'd.

Writes the proof set; English explanations are produced separately by raters
and merged in by dashboard_export.py.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
LAB = os.path.join(ROOT, "review", "labels")
OUT = os.path.join(ROOT, "review", "vibe")
BAND_LABELS = ["0-10", "11-25", "26-50", "51-75", "76-125", "126+"]
PER_BAND = 2
MIN_DEF_HEAVY = 3
SEED = 20260822
DEFINITION_KINDS = {"def", "inductive", "opaque", "quot", "axiom"}


def main():
    sys.path.insert(0, ROOT)
    briefs = {b["id"]: b for b in json.load(open(os.path.join(LAB, "briefs.json")))}
    key = json.load(open(os.path.join(LAB, "keymap.json")))
    rng = np.random.default_rng(SEED)

    def def_frac(pid):
        cs = briefs[pid]["candidates"]
        return sum(c["kind"] in DEFINITION_KINDS for c in cs) / len(cs)

    by_band = {b: [] for b in BAND_LABELS}
    for pid, k in key.items():
        by_band[k["band"]].append(pid)

    chosen = []
    for b in BAND_LABELS:
        pool = sorted(by_band[b])
        # one theorem-richest (deterministic), one seeded-random from the rest
        richest = min(pool, key=lambda p: (def_frac(p), p))
        rest = [p for p in pool if p != richest]
        pick = rng.choice(len(rest), size=1, replace=False)
        chosen += [richest, rest[int(pick[0])]]

    chosen.sort(key=lambda p: (BAND_LABELS.index(key[p]["band"]),
                               key[p]["depth"]))

    out = []
    for pid in chosen:
        b = briefs[pid]
        out.append({"id": pid, "theorem": b["theorem"], "band": key[pid]["band"],
                    "theorem_depth": b["theorem_depth"],
                    "artifact": key[pid]["artifact"],
                    "def_fraction": round(def_frac(pid), 3),
                    "candidates": b["candidates"]})

    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "vibe_set.json"), "w"), indent=1)

    # explanation briefs: 2 files of 6 proofs each
    for gi in range(2):
        part = out[gi * 6:(gi + 1) * 6]
        L = [f"# Explain these {len(part)} Lean proofs in English -- part {gi + 1}",
             "",
             "The reader cannot read Lean. For EVERY proof below, and EVERY",
             "candidate citation of that proof, write a short plain-English",
             "explanation of what that declaration actually is and what it does.",
             "",
             "Also write, for each proof, a 1-3 sentence explanation of what the",
             "THEOREM says in English, and a 1-2 sentence sketch of how the proof",
             "plausibly goes.",
             "",
             "Be concrete. `Eq.mpr` is 'rewrites the goal along an equality', not",
             "'a fundamental equality operation'. Name the mathematical object",
             "when there is one. If a declaration is pure machinery, say so and",
             "say what machinery.",
             "",
             "Keep each candidate explanation to 1-2 sentences. This is a quick",
             "orientation aid, not a treatise.",
             "",
             "## Output",
             "",
             "Write ONLY a JSON object to the path given at the end, shaped:",
             "",
             "```json",
             '{"proof_012": {',
             '   "statement_en": "...", "proof_sketch_en": "...",',
             '   "candidates": {"1": "...", "2": "..."}',
             "}}", "```", "",
             "Every proof id and every candidate number must appear.",
             "", "---", ""]
        for p in part:
            L.append(f"### {p['id']}  (target depth {p['theorem_depth']}, "
                     f"band {p['band']})")
            L.append("")
            L.append(f"THEOREM: `{p['theorem']}`")
            L.append("")
            L.append("Candidates:")
            L.append("")
            for it in p["candidates"]:
                st = ("in-statement" if it["in_statement"]
                      else "introduced-by-proof")
                L.append(f"  {it['n']:>2}. `{it['name']}`")
                L.append(f"      [{it['kind']}, depth {it['depth']}, {st}]")
            L.append("")
        open(os.path.join(OUT, f"explain_part{gi + 1}.md"), "w").write("\n".join(L))

    print(f"vibe set: {len(out)} proofs", flush=True)
    for p in out:
        print(f"  {p['id']}  band {p['band']:<7} depth {p['theorem_depth']:>4} "
              f"cands {len(p['candidates']):>3}  def_frac {p['def_fraction']:.2f}"
              f"  {p['theorem'][:58]}", flush=True)
    print(f"definition-heavy: {sum(p['def_fraction'] >= 0.5 for p in out)}/12",
          flush=True)
    print(f"written {OUT}/", flush=True)


if __name__ == "__main__":
    main()
