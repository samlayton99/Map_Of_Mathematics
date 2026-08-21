#!/usr/bin/env python3
"""Draw the sealed-round samples exactly as pre-registered.

Implements PREREGISTRATION_SEALED_R1.md sections 2 and 3. Nothing here makes a
choice the pre-registration did not already fix: seed, sizes, bands, strata,
eligibility and the two-stage brief format are all declared in advance.

Writes review/sealed_r1/{keymap,briefs}.json and one markdown brief per
rating batch.
"""
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "review", "sealed_r1")
DEV = os.path.join(ROOT, "review", "labels", "keymap.json")
PREREG = os.path.join(ROOT, "PREREGISTRATION_SEALED_R1.md")

SEED = 20260824
BANDS = [(0, 11), (11, 26), (26, 51), (51, 76), (76, 126), (126, 10**9)]
LABELS = ["0-10", "11-25", "26-50", "51-75", "76-125", "126+"]
CAL_PER_BAND = 12          # 72
TESTR_PER_BAND = 60        # 360
TESTC_PER_STRATUM = 20     # 120
MIN_CAND, MAX_CAND = 3, 25
BATCH = 24
KIND_NAMES = ["theorem", "def", "inductive", "constructor", "recursor",
              "opaque", "quot", "axiom", "?"]
ROLE_NAMES = ["applied", "let-value", "explicit-arg", "implicit-arg",
              "instance-slot", "strict-implicit", "type-annotation",
              "unresolved"]

RUBRIC = """\
## Stage 1 — say what the proof does, BEFORE judging the list

For each proof, first write `moves`: in your own words, one or two sentences,
what the key mathematical steps of this proof are. Write this from the theorem
statement and your own understanding.

Do this before you weigh the candidate list. If the real content of the proof
is something no citation could name -- a case split, exhibiting a witness,
manipulating a local hypothesis, pure rewriting -- say so plainly. That is a
genuine measurement, not a failure.

## Stage 2 — grade every candidate 0-4

Grade **every** candidate. Do not pick a top few. The grade is about THIS
proof, not about the declaration in general.

| grade | name | meaning |
|---|---|---|
| **4** | `CORE` | A core move. If asked "how does this proof go?", you would name it. |
| **3** | `MAJOR` | Real mathematical content, genuinely used, but secondary. |
| **2** | `LEGIT_GLUE` | Logical or structural plumbing that **is genuinely the content of this proof**. Near the foundations, assembling equalities really can be the whole argument. |
| **1** | `BAD_GLUE` | Plumbing or background that carries no idea here. A person explaining the proof would never mention it. |
| **0** | `JUNK` | Irrelevant machinery: automation residue, instance/typeclass resolution, universe or decidability bookkeeping, notation unfolding. |

The 2-versus-1 line is the important one. **Do not grade something 1 just
because it looks like plumbing.** Ask whether a mathematician explaining *this
specific theorem* would mention it. If yes, it is 2 even if its name looks
like machinery. If the theorem is a deep result and the item is `Eq.mpr`,
that is 1.

Candidates are in RANDOM order. Position means nothing. `depth` is context so
you can tell a deep theorem from a primitive -- it is NOT a hint, and you must
not grade something high merely because it is deep.
"""

DEFECT_TAXONOMY = """\
## Stage 3 — for this batch only: why is it a defect?

For every candidate you graded **0 or 1**, add a cause code:

| code | meaning |
|---|---|
| `A` | Generated proof obligation or private/internal helper |
| `B` | Wrapper/forwarder that just routes to a more useful boundary |
| `C` | Irrelevant instance / typeclass / interface plumbing |
| `D` | Tactic or certificate machinery (explains Lean's automation, not the maths) |
| `E` | Incidental logic/equality assembly (context-dependent) |
| `F` | Depth-inflated: looks deep structurally, but its mathematical role here is background |
| `G` | Other — name it in one short phrase |

Put these in a `causes` map from candidate number to code.
"""

OUTPUT_FMT = """\
## Output format

Return **only** a JSON object, no commentary:

```json
{
  "proof_0007": {
    "moves": "Rewrites along commutativity of addition, then closes by reflexivity.",
    "grades": {"1": 1, "2": 4, "3": 0, "4": 3, "5": 2},
    "missing_key": false,
    "confidence": "high"%s
  }
}
```

Every proof id in your batch must appear exactly once, and every candidate
number of that proof must appear exactly once in its `grades` map.
"""


def main():
    sys.path.insert(0, ROOT)
    from mathmap_eval.corpus import get_corpus
    c = get_corpus()
    rng = np.random.default_rng(SEED)

    prereg_hash = hashlib.sha256(open(PREREG, "rb").read()).hexdigest()
    print(f"pre-registration sha256 {prereg_hash}", flush=True)

    dev = json.load(open(DEV))
    dev_decls = {c.name_to_id.get(v["declaration"]) for v in dev.values()}
    dev_decls.discard(None)
    print(f"excluding {len(dev_decls)} development proofs", flush=True)

    base = np.where(c.universe("U1D"))[0]
    by_art = {}
    for p in base:
        by_art.setdefault(int(c.inc_artifact[p]), []).append(int(p))

    elig = []
    for a, pl in by_art.items():
        d = int(c.art_certifies[a])
        if c.node_gen[d] or c.node_kind[d] != 0 or d in dev_decls:
            continue
        if not (MIN_CAND <= len(pl) <= MAX_CAND):
            continue
        elig.append((a, d, len(pl), int(c.node_depth[d])))
    print(f"eligible proofs: {len(elig):,}", flush=True)

    band_of = {}
    for a, d, n, dep in elig:
        for lab, (lo, hi) in zip(LABELS, BANDS):
            if lo <= dep < hi:
                band_of[a] = lab
                break

    taken = set()

    def draw(pool, k):
        pool = [e for e in pool if e[0] not in taken]
        if not pool:
            return []
        idx = rng.choice(len(pool), size=min(k, len(pool)), replace=False)
        got = [pool[int(i)] for i in idx]
        for e in got:
            taken.add(e[0])
        return got

    # ---- CAL and TEST-R: stratified by depth band ------------------------
    cal, testr = [], []
    for lab in LABELS:
        pool = [e for e in elig if band_of.get(e[0]) == lab]
        cal += [(lab, "CAL", None) + e for e in draw(pool, CAL_PER_BAND)]
    for lab in LABELS:
        pool = [e for e in elig if band_of.get(e[0]) == lab]
        testr += [(lab, "TEST-R", None) + e for e in draw(pool, TESTR_PER_BAND)]

    # ---- TEST-C: defect-enriched strata, structural signals only ---------
    def has(a, fn):
        return any(fn(p) for p in by_art[a])

    strata = {
        "S1_generated": lambda a: has(a, lambda p: bool(c.node_gen[c.inc_decl[p]])),
        "S2_instance_heavy": lambda a: (
            np.mean([c.inc_roles[p][4] > 0 for p in by_art[a]]) >= 0.5),
        "S3_type_position": lambda a: has(
            a, lambda p: c.inc_roles[p][6] > 0 and c.inc_roles[p].sum() == c.inc_roles[p][6]),
        "S4_single_user": lambda a: has(
            a, lambda p: c.node_in_degree[c.inc_decl[p]] <= 1),
        "S5_deep_glue": lambda a: (
            int(c.node_depth[c.art_certifies[a]]) >= 76
            and has(a, lambda p: bool(c.decl_logic_only[c.inc_decl[p]]))),
        "S6_shallow_glue": lambda a: (
            int(c.node_depth[c.art_certifies[a]]) <= 25
            and has(a, lambda p: bool(c.decl_logic_only[c.inc_decl[p]]))),
    }
    testc = []
    for sname, fn in strata.items():
        pool = [e for e in elig if e[0] not in taken and fn(e[0])]
        got = draw(pool, TESTC_PER_STRATUM)
        testc += [(band_of.get(e[0]), "TEST-C", sname) + e for e in got]
        print(f"  TEST-C {sname:<20} pool {len(pool):>7,}  drawn {len(got)}",
              flush=True)

    chosen = cal + testr + testc
    print(f"\nCAL {len(cal)}  TEST-R {len(testr)}  TEST-C {len(testc)}  "
          f"total {len(chosen)}", flush=True)

    # ---- build briefs -----------------------------------------------------
    key, briefs = {}, []
    for n, (lab, split, stratum, a, d, ncand, dep) in enumerate(chosen, 1):
        pid = f"proof_{n:04d}"
        pl = by_art[a]
        srng = np.random.default_rng(SEED + 7919 * n)
        perm = srng.permutation(len(pl))
        items = []
        for j, oi in enumerate(perm, 1):
            p = pl[int(oi)]
            di = int(c.inc_decl[p])
            items.append({"n": j, "name": c.names[di],
                          "kind": KIND_NAMES[int(c.node_kind[di])],
                          "depth": int(c.node_depth[di]),
                          "in_statement": bool(c.inc_in_stmt_world[p]),
                          "role": ROLE_NAMES[int(np.argmax(c.inc_roles[p]))],
                          "_incidence": p})
        batch = f"{split.lower().replace('-', '')}_{(n - 1) // BATCH + 1:02d}"
        key[pid] = {"artifact": a, "declaration": c.names[d], "band": lab,
                    "depth": dep, "split": split, "stratum": stratum,
                    "batch": batch,
                    "items": {it["n"]: it["_incidence"] for it in items}}
        briefs.append({"id": pid, "theorem": c.names[d], "theorem_depth": dep,
                       "band": lab, "split": split, "stratum": stratum,
                       "batch": batch,
                       "candidates": [{k2: v for k2, v in it.items()
                                       if not k2.startswith("_")}
                                      for it in items]})

    os.makedirs(OUT, exist_ok=True)
    json.dump(key, open(os.path.join(OUT, "keymap.json"), "w"), indent=1)
    json.dump(briefs, open(os.path.join(OUT, "briefs.json"), "w"), indent=1)

    batches = sorted({b["batch"] for b in briefs})
    for bt in batches:
        bb = [b for b in briefs if b["batch"] == bt]
        is_c = bb[0]["split"] == "TEST-C"
        L = [f"# Grading batch `{bt}` — {len(bb)} proofs", "",
             "You are one of three independent raters. You will never see any",
             "ranking our system produces and must not try to guess one. Your",
             "grades are the ground truth those rankings are scored against.",
             "Do not look at any other file in this repository.", "",
             RUBRIC]
        if is_c:
            L.append(DEFECT_TAXONOMY)
        L.append(OUTPUT_FMT % (',\n    "causes": {"1": "C", "3": "A"}'
                               if is_c else ""))
        L += ["", "---", ""]
        for b in bb:
            L.append(f"### {b['id']}  (target depth {b['theorem_depth']}, "
                     f"band {b['band']})")
            L.append("")
            L.append(f"THEOREM PROVED: `{b['theorem']}`")
            L.append("")
            L.append(f"Grade all {len(b['candidates'])} candidates.")
            L.append("")
            for it in b["candidates"]:
                st = ("in-statement" if it["in_statement"]
                      else "introduced-by-proof")
                L.append(f"  {it['n']:>2}. `{it['name']}`")
                L.append(f"      [{it['kind']}, depth {it['depth']}, {st}, "
                         f"role {it['role']}]")
            L.append("")
        open(os.path.join(OUT, f"{bt}.md"), "w").write("\n".join(L))

    sizes = [len(b["candidates"]) for b in briefs]
    manifest = {
        "round": "SEALED-R1",
        "preregistration_sha256": prereg_hash,
        "seed": SEED,
        "n_proofs": len(chosen),
        "splits": {s: sum(1 for v in key.values() if v["split"] == s)
                   for s in ("CAL", "TEST-R", "TEST-C")},
        "by_band": {lab: sum(1 for v in key.values() if v["band"] == lab)
                    for lab in LABELS},
        "by_stratum": {s: sum(1 for v in key.values() if v["stratum"] == s)
                       for s in strata},
        "n_candidates": int(sum(sizes)),
        "mean_candidates_per_proof": float(np.mean(sizes)),
        "batches": batches,
        "n_rating_tasks": len(batches) * 3,
        "excluded_development_proofs": len(dev_decls),
        "briefs_sha256": hashlib.sha256(
            open(os.path.join(OUT, "briefs.json"), "rb").read()).hexdigest(),
    }
    json.dump(manifest, open(os.path.join(ROOT, "SEALED_R1_MANIFEST.json"), "w"),
              indent=1)
    print(f"\ncandidates: {sum(sizes):,} total, {np.mean(sizes):.1f} mean/proof")
    print(f"batches: {len(batches)} x 3 raters = {len(batches) * 3} rating tasks")
    print(f"written {OUT}/ and SEALED_R1_MANIFEST.json", flush=True)


if __name__ == "__main__":
    main()
