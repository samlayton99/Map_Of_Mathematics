#!/usr/bin/env python3
"""Build the Phase 2A human-review bundle: one markdown file per showcase proof
with side-by-side candidate views (P1-P6), trust labels, and a reviewer
worksheet. Selection is deterministic and stratified by proof style.

Usage: python3 review_bundle.py [--per-style N]
Reads studies/*.study.json; writes review/<file>/<decl>.md + review/WORKSHEET.md
"""
import json, glob, os, sys
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(__file__), "..")
STUDY_DIR = os.path.join(ROOT, "studies")
REVIEW_DIR = os.path.join(ROOT, "review")
PER_STYLE = int(sys.argv[sys.argv.index("--per-style") + 1]) if "--per-style" in sys.argv else 3

sys.path.insert(0, os.path.dirname(__file__))
from characterize import classify_style, dedup_events, AUTOMATION_ROLES  # noqa: E402

MATHLIB = os.path.join(ROOT, "corpusenv", "mathlib")


def src_excerpt(module_file, span, max_lines=40):
    if not span or not isinstance(span, dict):
        return "(no span recorded)"
    try:
        with open(os.path.join(MATHLIB, module_file)) as f:
            lines = f.readlines()
        a, b = span["start"]["line"] - 1, span["end"]["line"]
        chunk = lines[a:b]
        if len(chunk) > max_lines:
            chunk = chunk[:max_lines] + ["  ... (truncated)\n"]
        return "".join(chunk)
    except Exception as e:
        return f"(source unavailable: {e})"


def render_apps_tree(apps, max_items=30):
    if not isinstance(apps, list) or not apps:
        return "(none recovered)"
    kids = defaultdict(list)
    roots = []
    for i, a in enumerate(apps):
        if a["parent"] is None:
            roots.append(i)
        else:
            kids[a["parent"]].append(i)
    lines, count = [], 0

    def walk(i, ind):
        nonlocal count
        if count >= max_items:
            return
        a = apps[i]
        res = f" : {a['resultHead']}" if a["resultOk"] else ""
        prop = " [Prop]" if a["resultIsProp"] else ""
        lines.append(f"{'  ' * ind}- `{a['head']}` ({a['nArgs']} args){res}{prop}")
        count += 1
        for k in kids.get(i, []):
            walk(k, ind + 1)

    for r in roots:
        walk(r, 0)
    if count >= max_items:
        lines.append(f"  ... ({len(apps)} occurrences total)")
    return "\n".join(lines)


def main():
    os.makedirs(REVIEW_DIR, exist_ok=True)
    manifest = []
    for path in sorted(glob.glob(os.path.join(STUDY_DIR, "*.study.json"))):
        fname = os.path.basename(path).replace(".study.json", "")
        with open(path) as f:
            s = json.load(f)
        module_file = s["record"]["source"]["file"]
        ref = {d["name"]: d for d in s["referencedDecls"] if "error" not in d}
        decls = {d["name"]: d for d in s["record"]["declarations"]}
        events = dedup_events(s["useEvents"])
        events_by_decl = defaultdict(list)
        for e in events:
            events_by_decl[e["decl"]].append(e)

        showcase = [d for d in s["declStudies"] if d["showcase"] and d["kind"] == "theorem"]
        by_style = defaultdict(list)
        for d in showcase:
            sty = classify_style(d["name"], events_by_decl, None)
            by_style[sty].append(d)
        picked = []
        for sty in sorted(by_style):
            # deterministic spread: sort by body-support size, take small/medium/large
            cands = sorted(by_style[sty], key=lambda d: (len(d["p2_supportBody"]), d["name"]))
            n = len(cands)
            idxs = sorted({0, n // 2, n - 1})[:PER_STYLE] if n else []
            picked += [(sty, cands[i]) for i in idxs]

        outdir = os.path.join(REVIEW_DIR, fname)
        os.makedirs(outdir, exist_ok=True)
        for sty, d in picked:
            name = d["name"]
            rec = decls.get(name, {})
            evs = events_by_decl.get(name, [])
            body = d["p2_supportBody"]
            infra = [(n_, ",".join(ref[n_]["classification"])) for n_ in body
                     if n_ in ref and ref[n_]["classification"]]
            domain = [n_ for n_ in body if not (n_ in ref and ref[n_]["classification"])]
            md = []
            md.append(f"# {name}\n")
            md.append(f"*file:* `{module_file}` · *style (derived):* {sty} · "
                      f"*proof-term size:* {d['sizes']['valueSize']} nodes\n")
            md.append("## Statement and source  [lean-exact]\n")
            md.append("```lean\n" + src_excerpt(module_file, rec.get("span")) + "```\n")
            md.append(f"Exact proof reference: record decl `{rec.get('id','?')}` in "
                      f"`studies/{fname}.study.json` (type `{rec.get('type','?')}`, "
                      f"value `{rec.get('value','?')}`).\n")
            md.append("## P2 — support set (body)  [deterministic-derived]\n")
            md.append(f"**Domain ({len(domain)}):** " + ", ".join(f"`{x}`" for x in domain) + "\n")
            md.append(f"**Classified infrastructure ({len(infra)}):** " +
                      (", ".join(f"`{x}` ({c})" for x, c in infra) or "(none)") + "\n")
            md.append("## P4 — named application spine (top of tree)  [deterministic-derived]\n")
            md.append(render_apps_tree(d["p4_apps"] if isinstance(d["p4_apps"], list) else []) + "\n")
            md.append("## P5 — source-level use events  [observed]\n")
            if evs:
                for e in sorted(evs, key=lambda e: json.dumps(e.get("src"), sort_keys=True)):
                    at = ", ".join(f"`{a['decl']}`" for a in e["attributions"]) or "(no named attribution)"
                    md.append(f"- `{e['role']}` → {at} — `{e['actionText'][:80]}`")
                md.append("")
            else:
                md.append("(term-mode proof: no tactic events)\n")
            md.append("## P6 — one-level expansion of top domain dependencies  [deterministic-derived]\n")
            for dep in domain[:5]:
                r = ref.get(dep)
                if r:
                    md.append(f"- `{dep}` — {r['kind']}, module `{r['module']}`")
            md.append("\n## Reviewer questions (see WORKSHEET.md)\n")
            md.append("P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   "
                      "P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   "
                      "best coarse view? [P2/P3/P4/P5/none]\n")
            safe = name.replace("/", "_").replace("'", "_")
            with open(os.path.join(outdir, f"{safe}.md"), "w") as f:
                f.write("\n".join(md))
            manifest.append((fname, sty, name))

    with open(os.path.join(REVIEW_DIR, "WORKSHEET.md"), "w") as f:
        f.write("""# Reviewer Worksheet — Phase 2A candidate representations

For each proof file in this bundle, answer (1=useless … 5=excellent). No human
review has been performed by the extraction pipeline itself; nothing in the
bundle is a usefulness claim.

1. Which single named declaration would be the most helpful hint for
   reconstructing this proof, and does the P2 domain list contain it?
2. Rate P2 (support set) as a short proof hint. How much is noise/infrastructure?
3. Rate P4 (application spine): does structure/nesting add information over P2?
4. Rate P5 (tactic events): does source-level order/role add information?
5. Which important conceptual tools are missing from every view?
6. Does order/grouping matter for this proof?
7. Does one-level expansion (P6) help or merely add verbosity?
8. Where would a natural-language tag be indispensable?
9. Best coarse summary for this proof: P2 / P3 / P4 / P5 / hybrid / none.

## Bundle contents
""")
        for fname, sty, name in manifest:
            f.write(f"- {fname} / {sty} / `{name}`\n")
    print(f"review bundle: {len(manifest)} proofs -> {REVIEW_DIR}")


if __name__ == "__main__":
    main()
