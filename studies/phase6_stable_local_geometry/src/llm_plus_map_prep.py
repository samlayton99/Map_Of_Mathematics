#!/usr/bin/env python3
"""Does the map ADD anything to an LLM? (the product question)

Union recall (0.475 vs 0.444) was an ORACLE union -- it credits a hit
in either list without anyone having to choose. This builds the real
system: the LLM sees the statement AND the map's top-10 as candidate
hints, then commits to a final ranked 10. If LLM+map > LLM alone, the
map earns its place as context for a solver even though it loses the
head-to-head.

Also writes a REPEAT of the plain condition (same items, fresh agent)
to measure LLM run-to-run self-consistency -- the map's determinism is
only an advantage if the LLM is actually unstable, so measure it.

Writes data/llm_vs_map/{aug_XX.md, repeat_XX.md}.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, "..", "data", "llm_vs_map"))
PER_BATCH = 10
TOPK = 10

doc = json.load(open(os.path.join(D, "tasks.json")))
tasks = doc["tasks"]

AUG_INSTR = """\
# Premise retrieval with structural hints — batch {bt}

For each Lean 4 / Mathlib theorem you are shown its statement, plus a
list of CANDIDATE declarations proposed by a structural index. The
index knows nothing about mathematics or names: it ranks declarations
purely by which lemmas tend to be cited together with the things this
theorem's statement mentions. Its suggestions are often in the right
neighbourhood but the wrong lemma, and are sometimes useless. Roughly
one in ten of its top suggestions is actually used by the proof.

Use the hints as evidence, not as an answer key. You may keep, reorder,
or discard any of them, and you should add your own candidates freely.

For each item, give the {k} declarations you judge most likely to be
cited by the PROOF, most likely first. Rules:

- Fully-qualified Mathlib names, exactly as they appear in the library.
- Substantive mathematical lemmas/definitions, not tactic plumbing
  (`Eq.mpr`, `congrArg`, `rfl`, `id`), and not things already named in
  the statement.
- Exactly {k} names per item, no commentary, no duplicates.

Answer as JSON only:
{{"q01": ["Name.one", ...], "q02": [...], ...}}

---

"""

PLAIN_INSTR = """\
# Premise retrieval — batch {bt}

For each Lean 4 / Mathlib theorem below you are shown ONLY its statement.
The proof is not shown and you must not try to recall the file.

For each item, predict which Mathlib declarations the PROOF uses: name
the {k} declarations you judge most likely to be cited by the proof,
most likely first. Rules:

- Give fully-qualified Mathlib names exactly as they appear in the
  library (e.g. `Finset.sum_congr`, `Polynomial.degree_mul`).
- Predict the substantive mathematical lemmas/definitions the proof
  builds on, not tactic-level plumbing (`Eq.mpr`, `congrArg`, `rfl`,
  `id`) and not things already named in the statement itself.
- Exactly {k} names per item, no commentary, no duplicates.

Answer as JSON only:
{{"q01": ["Name.one", ...], "q02": [...], ...}}

---

"""


def write(cond, instr, with_hints):
    n = 0
    for bi in range(0, len(tasks), PER_BATCH):
        chunk = tasks[bi:bi + PER_BATCH]
        bt = "%02d" % (bi // PER_BATCH + 1)
        parts = [instr.format(bt=bt, k=TOPK)]
        for t in chunk:
            head = (f"## {t['id']}  `{t['target']}`\n"
                    f"module: `{t['module']}`\n")
            body = head + "\n```lean\n" + t["statement"] + "\n```\n"
            if with_hints:
                if t["map_top10"]:
                    body += "\nstructural index suggests:\n" + "\n".join(
                        f"  {i+1}. `{c}`" for i, c in enumerate(t["map_top10"]))
                    body += "\n"
                else:
                    body += "\nstructural index: no suggestion for this item.\n"
            parts.append(body)
        open(os.path.join(D, f"{cond}_{bt}.md"), "w").write("\n".join(parts))
        n += 1
    print(f"{cond}: {n} batches")


write("aug", AUG_INSTR, True)
write("repeat", PLAIN_INSTR, False)
