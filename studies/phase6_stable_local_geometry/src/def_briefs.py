#!/usr/bin/env python3
"""BLIND regrade round -- Tasks 2 and 3: build the briefs, batches, manifest.

A brief shows a rater exactly two things: the mathematics of the target
(statement + proof/construction source) and, for each candidate, its name and
its statement source, in an order shuffled by a per-target seed. No depth, no
role, no in-statement flag, no kind, no lane, no rank, no score, no system
coordinate of any sort appears in anything a rater reads. See
p0/P0_GRADING_BRIEF_AUDIT.md for what went wrong last time.

Writes data/blind/{briefs.json, answer_template.json, MANIFEST.md,
batches/batch_XX.md}.
"""
import hashlib
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lean_source as LS                                   # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "data", "blind2")
BATCHES = os.path.join(OUT, "batches")
MODULES_TSV = "/Users/sam/mathmap_data/all_modules.tsv"

SEED = 20260911
SHUFFLE_STRIDE = 7919
PER_BATCH = 10

RUBRIC = """\
Grade each candidate 0-4 by its mathematical function in THIS proof/construction:
4 = a core move: the proof's central idea or decisive step depends on it
3 = a major step: substantive mathematics the proof genuinely builds on
2 = a legitimate connective step: honest but routine glue between the real steps
1 = boilerplate: bookkeeping that any formalization would need; contributes no mathematical content
0 = noise: irrelevant or purely administrative
Judge from the mathematics alone. If unsure between two grades, give the lower.
There are no quotas; a proof may have several 4s or none."""

HEADER = """\
# Blind grading batch {bt} — {n} items

Each item below gives you one Lean declaration: its statement, then the proof
or construction that establishes it. After that comes the list of declarations
that proof or construction cites, in random order. Grade every candidate in
every item.

## Rubric

{rubric}

## Output

Return only a JSON object, no commentary: one key per item id, mapping each
candidate number to its grade.

```json
{{"{ex}": {{"1": 2, "2": 4, "3": 0}}}}
```

Every item id in this batch must appear exactly once, and every candidate
number of that item must appear exactly once.

---
"""


def fence(text):
    return "```lean\n" + (text or "").rstrip() + "\n```"


def main():
    module_of = {}
    with open(MODULES_TSV) as f:
        for line in f:
            nm, _, mod = line.rstrip("\n").partition("\t")
            module_of[nm] = mod

    sample = json.load(open(os.path.join(OUT, "sample.json")))
    targets = sample["targets"]

    # Shuffle the target ORDER with the global seed, so that batch membership
    # itself carries no information about kind or depth band.
    order = np.random.default_rng(SEED).permutation(len(targets))
    targets = [targets[int(i)] for i in order]

    stats = {"cand_total": 0, "cand_exact": 0, "cand_approx": 0,
             "cand_miss": 0, "how": {}}
    briefs = []
    for n, t in enumerate(targets, 1):
        tid = f"t{n:03d}"
        shuffle_seed = SEED + SHUFFLE_STRIDE * n
        cands = list(t["candidates"])
        perm = np.random.default_rng(shuffle_seed).permutation(len(cands))
        items = []
        for j, oi in enumerate(perm, 1):
            c = cands[int(oi)]
            src = LS.lookup(c["name"], module_of.get(c["name"]))
            stats["cand_total"] += 1
            if src is None:
                stats["cand_miss"] += 1
                stats["how"]["MISS"] = stats["how"].get("MISS", 0) + 1
                stmt, how = c["name"], "not-found"
            else:
                how = src["how"]
                stats["how"][how] = stats["how"].get(how, 0) + 1
                if how in ("translated", "generated-from"):
                    stats["cand_approx"] += 1
                    stmt = (f"-- Mathlib generates `{c['name']}` from the "
                            f"declaration below.\n" + src["statement"])
                else:
                    stats["cand_exact"] += 1
                    stmt = src["statement"]
            items.append({"n": j, "name": c["name"], "statement_src": stmt,
                          "_decl": c["decl"], "_how": how})
        briefs.append({
            "id": tid,
            "target": t["target"],
            "kind": t["kind"],
            "band": t["band"],
            "statement_src": t["statement_src"],
            "proof_src": t["proof_src"],
            "candidates": [{k: v for k, v in it.items()
                            if not k.startswith("_")} for it in items],
            "shuffle_seed": shuffle_seed,
            "_batch": f"batch_{(n - 1) // PER_BATCH + 1:02d}",
            "_decl": t["decl"],
            "_module": t["module"],
            "_candidate_decls": {it["n"]: it["_decl"] for it in items},
            "_candidate_how": {it["n"]: it["_how"] for it in items},
        })

    os.makedirs(BATCHES, exist_ok=True)
    json.dump([{k: v for k, v in b.items() if not k.startswith("_")}
               for b in briefs],
              open(os.path.join(OUT, "briefs.json"), "w"), indent=1)
    # separate keymap so briefs.json stays the rater-facing record
    json.dump({b["id"]: {"declaration": b["target"], "module": b["_module"],
                         "decl_id": b["_decl"], "batch": b["_batch"],
                         "kind": b["kind"], "band": b["band"],
                         "candidates": b["_candidate_decls"],
                         "candidate_source_match": b["_candidate_how"]}
               for b in briefs},
              open(os.path.join(OUT, "keymap.json"), "w"), indent=1)

    # ---- rendered batches -------------------------------------------------
    batch_names = sorted({b["_batch"] for b in briefs})
    for bt in batch_names:
        bb = [b for b in briefs if b["_batch"] == bt]
        L = [HEADER.format(bt=bt.replace("batch_", ""), n=len(bb),
                           rubric=RUBRIC, ex=bb[0]["id"])]
        for b in bb:
            L.append(f"\n## {b['id']}\n")
            L.append(f"Target: `{b['target']}`\n")
            L.append(fence(b["statement_src"]))
            L.append("\nProof / construction:\n")
            L.append(fence(b["proof_src"]))
            L.append(f"\nCandidates ({len(b['candidates'])}), random order:\n")
            for it in b["candidates"]:
                L.append(f"{it['n']}. `{it['name']}`\n")
                L.append(fence(it["statement_src"]))
                L.append("")
            L.append("\n---")
        open(os.path.join(BATCHES, bt + ".md"), "w").write("\n".join(L) + "\n")

    # ---- answer template --------------------------------------------------
    tpl = {}
    for b in briefs:
        tpl.setdefault(b["_batch"], {})[b["id"]] = {
            str(it["n"]): None for it in b["candidates"]}
    json.dump(tpl, open(os.path.join(OUT, "answer_template.json"), "w"),
              indent=1)

    # ---- blind-contract checklist ----------------------------------------
    banned = ["depth", "role", "in-statement", "instance-slot", "lane",
              "rank", "score", "kind"]
    findings = {w: {"total": 0, "outside_lean_source": 0, "examples": []}
                for w in banned}
    fence_re = re.compile(r"```lean\n.*?\n```", re.S)
    for bt in batch_names:
        txt = open(os.path.join(BATCHES, bt + ".md")).read()
        prose = fence_re.sub("", txt)
        for w in banned:
            pat = re.compile(re.escape(w), re.I)
            findings[w]["total"] += len(pat.findall(txt))
            for m in pat.finditer(prose):
                findings[w]["outside_lean_source"] += 1
                if len(findings[w]["examples"]) < 3:
                    s = max(0, m.start() - 45)
                    findings[w]["examples"].append(
                        f"{bt}: ...{prose[s:m.end() + 45]}...")

    sizes = [len(b["candidates"]) for b in briefs]
    kinds = [b["kind"] for b in briefs]
    bands = [b["band"] for b in briefs]
    digest = hashlib.sha256(
        open(os.path.join(OUT, "briefs.json"), "rb").read()).hexdigest()

    write_manifest(sample, briefs, stats, findings, sizes, kinds, bands,
                   batch_names, digest)

    print(f"briefs {len(briefs)}, candidates {sum(sizes):,}, "
          f"batches {len(batch_names)}")
    print("candidate statement location:", stats["how"])
    hit = 100.0 * (stats["cand_total"] - stats["cand_miss"]) / stats["cand_total"]
    print(f"candidate hit rate {hit:.1f}%  (exact-ish "
          f"{100.0 * stats['cand_exact'] / stats['cand_total']:.1f}%)")
    print("contract greps outside Lean source:",
          {w: v["outside_lean_source"] for w, v in findings.items()})
    return 0


def prior_graded():
    """Declarations already graded as TARGETS in the dev / SEALED-R1 rounds."""
    out = set()
    p5 = os.path.normpath(os.path.join(ROOT, "..",
                                       "phase5_multiscale_navigation"))
    for rel in ("review/sealed_r1/keymap.json", "review/labels/keymap.json"):
        p = os.path.join(p5, rel)
        if os.path.exists(p):
            for v in json.load(open(p)).values():
                out.add(v["declaration"])
    return out


def write_manifest(sample, briefs, stats, findings, sizes, kinds, bands,
                   batch_names, digest):
    tot = stats["cand_total"]
    hit = tot - stats["cand_miss"]
    ok = all(v["outside_lean_source"] == 0 for v in findings.values())
    L = []
    A = L.append
    A("# BLIND regrade round — manifest\n")
    A("Fresh label instrument built after `p0/P0_GRADING_BRIEF_AUDIT.md`. The")
    A("previous round showed raters the system's own tags (depth, role,")
    A("in-statement, kind) and encoded two of its predictions in the rubric.")
    A("Nothing a rater reads in this round contains any system coordinate.\n")

    A("## Sample\n")
    A(f"- seed: `{sample['seed']}` (global). Per-target shuffle seed:")
    A(f"  `{SEED} + {SHUFFLE_STRIDE} * n`, n = 1..{len(briefs)} in batch order.")
    A(f"- batch order: the {len(briefs)} targets are permuted with the global")
    A("  seed before batching, so batch membership carries no information")
    A("  about kind or depth band.")
    A(f"- targets: {len(briefs)} = {sum(1 for k in kinds if k == 0)} theorems "
      f"(kind 0) + {sum(1 for k in kinds if k == 1)} definitions/instances "
      "(kind 1).")
    A("- depth bands (target declaration depth), equal counts per band within")
    A("  each kind group, depth <= 10 skipped:\n")
    A("| band | theorems | defs/instances |")
    A("|---|---|---|")
    for lab in sample["bands"]:
        A(f"| {lab} | {sum(1 for b, k in zip(bands, kinds) if b == lab and k == 0)}"
          f" | {sum(1 for b, k in zip(bands, kinds) if b == lab and k == 1)} |")
    A("")
    A("- **Definitions and instances have never been graded as targets before**")
    A("  (audit, 'Sampling frame': all 552 previously graded proofs were")
    A("  theorem targets). This round is the first evidence about them.")
    prev = prior_graded()
    overlap = sorted({b["target"] for b in briefs} & prev)
    A(f"- overlap with the {len(prev)} declarations graded as targets in the")
    A(f"  dev and SEALED-R1 rounds: **{len(overlap)}**"
      + (f" ({', '.join(overlap[:5])})" if overlap else "") + ".\n")

    A("### Target eligibility\n")
    A("1. non-generated (`gen` flag false), kind 0 or 1, depth >= 11;")
    A("2. >= 3 incidences;")
    A("3. sampling-only aux-name filter from `src/pilot_sample.py`")
    A("   (`casesOn`/`rec`/`_aux`/`macroRules`/`_unexpand`/leading `_` ...);")
    A("4. module under `Mathlib.`, not under `Mathlib.Tactic`;")
    A("5. statement AND body located **exactly** in the Mathlib source.\n")
    A("Criterion 5 is new and it is a real restriction, recorded here rather")
    A("than hidden: it drops Mathlib's machine-generated lemmas (`@[simps]`,")
    A("`@[reassoc]`, unnamed `@[to_additive]`/`@[to_dual]`) from the target")
    A("frame, because those declarations have no source text to show and no")
    A("human proof to judge. It skews the target sample away from category")
    A("theory `_hom_app`/`_obj` projection lemmas and away from the additive")
    A("halves of algebraic hierarchies. It is applied to targets only.\n")

    A("### Candidate universe (unfiltered)\n")
    A("Per target, ALL of its incidence declarations that are load-bearing")
    A("(roles 0/1/2/7 = applied / let-value / explicit-arg / unresolved) PLUS")
    A("all definition-kind declarations cited in any role — i.e. the U1D pool")
    A("of `mathmap_eval/corpus.py`, verbatim. Generated candidates are")
    A("redirected to their nearest non-generated dot-prefix owner and dropped")
    A("if that owner is the target itself; then deduplicated. Targets with")
    A("fewer than 3 or more than 25 candidates were resampled.\n")
    A("**No inclusion policy, ranking, lane or score touches this pool.** The")
    A("labels are meant to judge the pool, so the pool must not have been")
    A("pre-judged.\n")
    A(f"- candidate slots: {sum(sizes):,}, mean {np.mean(sizes):.1f} per target,")
    A(f"  min {min(sizes)}, max {max(sizes)}.\n")

    A("## Statement extraction\n")
    A("Statements come from the Lean source: `all_modules.tsv` gives the")
    A("module, `src/lean_source.py` indexes that file by fully qualified name")
    A("(namespace stack + declared name), including structure/class fields,")
    A("inductive constructors, `extends` parent projections, `mk`")
    A("constructors, explicitly named `@[to_dual X]` / `@[to_additive X]`")
    A("targets, and anonymous `instance : C ...` blocks matched by Lean's")
    A("`inst<C>...` naming. Mathlib source is `corpusenv/mathlib`; `Init.*`,")
    A("`Lean.*`, `Std.*` come from the v4.33.0 toolchain source; the rest")
    A("from `.lake/packages`.\n")
    A(f"- targets: {len(briefs)}/{len(briefs)} statements and bodies located")
    A("  exactly (enforced by eligibility criterion 5, above).")
    A(f"- candidates: {hit:,}/{tot:,} located = **{100.0 * hit / tot:.1f}%**; "
      f"**{100.0 * stats['cand_miss'] / tot:.1f}% could not be located** "
      f"({stats['cand_miss']} of {tot}).")
    A(f"- of those located, {stats['cand_exact']:,} are the declaration's own")
    A(f"  source text and {stats['cand_approx']:,} are approximate: the")
    A("  declaration is generated by Mathlib and the brief shows the")
    A("  declaration it was generated from, prefixed with a one-line comment")
    A("  saying so. Those are flagged as `translated` / `generated-from` in")
    A("  `keymap.json`.")
    A("- a candidate whose source could not be located is rendered as its")
    A("  declaration name alone (flagged `not-found` in `keymap.json`).\n")
    A("Match kinds: `" + json.dumps(stats["how"]) + "`\n")
    A("Known residual signal, stated so it can be controlled for: a")
    A("`not-found` candidate is visibly different from the others (a bare")
    A(f"name, no statement), and it correlates weakly with being")
    A("machine-generated — the previous round treated the generated flag as")
    A(f"hidden. This affects {stats['cand_miss']} of {tot} candidate slots "
      f"({100.0 * stats['cand_miss'] / tot:.1f}%). Exclude those slots in any")
    A("analysis where it matters; `keymap.json` marks every one of them.\n")

    A("## Blind-contract checklist\n")
    A("Every rendered batch in `batches/` was grepped, case-insensitively,")
    A("for the vocabulary that contaminated the last round. Occurrences")
    A("inside a ```lean fence are Lean source text (Mathlib really does have")
    A("declarations named `Nat.rec`, fields named `map`, and the `instance`")
    A("keyword); occurrences OUTSIDE the fences would be instrument leakage.")
    A("The contract is that the outside-source count is zero.\n")
    A("| term | occurrences in batch files | outside Lean source |")
    A("|---|---|---|")
    for w, v in findings.items():
        A(f"| `{w}` | {v['total']} | **{v['outside_lean_source']}** |")
    A("")
    for w, v in findings.items():
        for ex in v["examples"]:
            A(f"- LEAK `{w}`: {ex}")
    A(f"\n**Contract holds: {'YES' if ok else 'NO'}.**\n")
    A("What a rater sees, exhaustively: the batch header, the rubric text")
    A("above verbatim, the output-format example, and per item — the target's")
    A("statement source, its proof/construction source, and a numbered list")
    A("of candidate names each with its statement source. Nothing else.\n")
    A("What a rater never sees: depth or depth band, role or role name,")
    A("in-statement vs introduced-by-proof, declaration kind, lane, rank,")
    A("score, rarity, in-degree, generated flag, inclusion policy, or any")
    A("hint about how many grades of each value to expect. The rubric names")
    A("no constant, no typeclass, no tactic, and no expected distribution.\n")
    A("The rubric, identical in all 12 batches:\n")
    A("```")
    A(RUBRIC)
    A("```\n")

    A("## Draw statistics\n")
    A("| cell | eligible pool | examined | drawn | rejected: candidate count "
      "| rejected: no source |")
    A("|---|---|---|---|---|---|")
    for cell, v in sample["draw_stats"].items():
        A(f"| {cell} | {v['pool']:,} | {v['examined']} | {v['drawn']} | "
          f"{v['rejected_candidate_count']} | {v['rejected_no_source']} |")
    A("")

    A("## Files\n")
    A(f"- `sample.json` — the draw ({len(briefs)} targets, candidate ids)")
    A(f"- `briefs.json` — rater-facing record, sha256 `{digest[:16]}...`")
    A("- `keymap.json` — analysis-side key: declaration ids per candidate")
    A("  number, batch, kind, band, source-match kind. **Not** given to raters.")
    A(f"- `batches/batch_01..{batch_names[-1][-2:]}.md` — {PER_BATCH} targets each")
    A("- `answer_template.json` — `{batch: {target_id: {candidate_n: null}}}`\n")
    A("`briefs.json` carries `kind` and `band` because it is also the")
    A("analysis-side record; neither field is rendered into any batch file.")
    A("Only `batches/*.md` is given to a rater.\n")

    open(os.path.join(OUT, "MANIFEST.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    sys.exit(main())
