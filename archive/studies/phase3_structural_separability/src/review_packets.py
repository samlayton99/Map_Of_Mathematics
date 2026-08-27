#!/usr/bin/env python3
"""Build blinded review packets (user: 12 proofs; agent: 24 proofs).

Per proof, PART 1 shows the theorem statement and eight anonymized top-8
rankings (method names shuffled per proof, seeded); PART 2 reveals the source
proof for the fidelity judgment. The method-key mapping is stored separately
so reviewers cannot see it.
"""
import os, json, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
REVIEW = os.path.normpath(os.path.join(HERE, "..", "review"))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
MATHLIB = os.path.join(ROOT, "corpusenv", "mathlib")
SEED = 20260819
METHODS = ["M_p2_order", "M_multiplicity", "M_global_pagerank", "M_p3_filter",
           "M_p4_route", "M_local_salience", "M_combined", "M_hybrid"]


def source_lines(study_file, decl):
    import json as j
    s = j.load(open(os.path.join(ROOT, "studies", study_file + ".study.json")))
    rec = {d["name"]: d for d in s["record"]["declarations"]}
    d = rec.get(decl, {})
    span = d.get("span")
    mf = s["record"]["source"]["file"]
    if not span or not isinstance(span, dict):
        return "(no span)", "(no span)"
    lines = open(os.path.join(MATHLIB, mf)).readlines()
    chunk = lines[span["start"]["line"] - 1: span["end"]["line"]]
    text = "".join(chunk)
    # statement heuristic: up to first ':=' or 'by' terminator (display only)
    stmt = text
    for sep in (":= by", ":=", " by\n"):
        i = text.find(sep)
        if i > 0:
            stmt = text[:i].rstrip()
            break
    return stmt, text


def main():
    rankings = json.load(open(os.path.join(DATA, "rankings.json")))
    manifest = json.load(open(os.path.join(DATA, "landmark_sample_manifest.json")))["proofs"]
    rng = np.random.default_rng(SEED)
    os.makedirs(os.path.join(REVIEW, "agent_packet"), exist_ok=True)
    os.makedirs(os.path.join(REVIEW, "user_packet"), exist_ok=True)
    os.makedirs(os.path.join(REVIEW, "prompts"), exist_ok=True)
    keymap = {}
    # user packet: first 2 proofs per file in manifest order
    per_file_count = {}
    user_set = set()
    for item in manifest:
        c = per_file_count.get(item["file"], 0)
        if c < 2:
            user_set.add(item["decl"])
        per_file_count[item["file"]] = c + 1

    for item in manifest:
        decl = item["decl"]
        if decl not in rankings["proofs"]:
            continue
        r = rankings["proofs"][decl]
        stmt, full = source_lines(item["file"], decl)
        perm = list(rng.permutation(len(METHODS)))
        labels = {METHODS[perm[i]]: f"V{i+1}" for i in range(len(METHODS))}
        keymap[decl] = {v: k for k, v in labels.items()}
        md = [f"# Review packet — `{decl}`\n",
              f"*domain file:* {item['file']}\n",
              "## PART 1 — statement and candidate views (do NOT read Part 2 yet)\n",
              "Theorem statement:\n", "```lean", stmt, "```\n",
              "Each view lists up to 8 declarations that the view considers the "
              "most important mathematical content of this proof. Rate each view "
              "1–5 for: *would this list help a mathematically informed reader "
              "see how the theorem is proved?*\n"]
        for meth in METHODS:
            lab = labels[meth]
            top = r["rankings"][meth][:8]
            md.append(f"**{lab}:** " + ", ".join(f"`{x}`" for x in top))
        md += ["\n## PART 2 — source proof (read only after Part 1 ratings)\n",
               "```lean", full, "```\n",
               "Now rate each view 1–5 for *certificate fidelity*: does it "
               "preserve the important moves of THIS proof? Note any key move "
               "(local hypothesis, witness, case split, representation change) "
               "that no view captures.\n"]
        text = "\n".join(md)
        with open(os.path.join(REVIEW, "agent_packet", f"{decl}.md"), "w") as f:
            f.write(text)
        if decl in user_set:
            with open(os.path.join(REVIEW, "user_packet", f"{decl}.md"), "w") as f:
                f.write(text)

    with open(os.path.join(REVIEW, "method_keymap.json"), "w") as f:
        json.dump({"note": "do not show to reviewers before responses are collected",
                   "map": keymap}, f, indent=1, sort_keys=True)
    schema = {
        "reviewer_type": "user | coding agent | reasoning agent | proxy",
        "reviewer_id": "model/agent identifier",
        "prompt_version": "p3-review-v1",
        "per_proof": {"<decl>": {
            "part1_usefulness": {"V1": "1-5", "V2": "1-5", "V3": "1-5", "V4": "1-5",
                                  "V5": "1-5", "V6": "1-5", "V7": "1-5", "V8": "1-5"},
            "part1_best_view": "V?",
            "part2_fidelity": {"V1": "1-5", "V2": "1-5", "V3": "1-5", "V4": "1-5",
                                "V5": "1-5", "V6": "1-5", "V7": "1-5", "V8": "1-5"},
            "missing_moves": "free text",
            "confidence": "1-5", "rationale": "free text"}}}
    with open(os.path.join(REVIEW, "response_schema.json"), "w") as f:
        json.dump(schema, f, indent=1)
    prompt = """You are an independent mathematical reviewer. You will review proof-view
packets. For each packet file:
1. Read PART 1 only. Rate each view V1..V8 from 1 (useless) to 5 (excellent)
   for mathematical usefulness: would the listed declarations help a
   mathematically informed reader see how the theorem is proved? Pick the best view.
2. Then read PART 2 (the source proof). Rate each view 1-5 for certificate
   fidelity: does it preserve the important moves of THIS proof?
3. Note key moves (local hypotheses, witnesses, case splits, rewrites,
   representation changes) that NO view captures.
Do not attempt to identify which method produced which view. Do not consult
anything outside the packet. Output strict JSON per response_schema.json.
Prompt version: p3-review-v1.
"""
    with open(os.path.join(REVIEW, "prompts", "reviewer_prompt.md"), "w") as f:
        f.write(prompt)
    print(f"packets: agent={len(keymap)} user={len(user_set)} -> {REVIEW}")


if __name__ == "__main__":
    main()
