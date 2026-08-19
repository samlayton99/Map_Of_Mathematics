#!/usr/bin/env python3
"""Phase 2A quantitative characterization of candidate projections P0-P6.

Input: studies/*.study.json (produced by `mathrecord study`).
Output: studies/characterization.json + markdown tables on stdout.

All numbers here are deterministic-derived from the exact records; no semantic
judgment is applied. Infrastructure classification comes from the documented
reversible classifiers in the extractor.
"""
import json, sys, glob, os, statistics as st
from collections import Counter, defaultdict

STUDY_DIR = os.path.join(os.path.dirname(__file__), "..", "studies")

AUTOMATION_ROLES = {"simp", "simp_all"}
AUTOMATION_KIND_HINTS = ("omega", "decide", "aesop", "positivity", "fieldSimp",
                         "norm_num", "normNum", "grind", "linarith", "gcongr",
                         "abel", "ring", "fun_prop", "continuity", "tauto")


def load_studies():
    out = {}
    for p in sorted(glob.glob(os.path.join(STUDY_DIR, "*.study.json"))):
        name = os.path.basename(p).replace(".study.json", "")
        with open(p) as f:
            out[name] = json.load(f)
    return out


def classify_style(decl_name, events_by_decl, nonfam_by_decl):
    evs = events_by_decl.get(decl_name, [])
    roles = {e["role"] for e in evs}
    if not evs:
        return "term"
    if roles & AUTOMATION_ROLES:
        return "automation"
    if "induction" in roles or "cases" in roles:
        return "induction"
    if "rw" in roles or "rewrite" in roles:
        return "rewrite"
    return "tactic-other"


def dedup_events(events):
    """Nested rw->rewrite / refine->refine duplicates share a source span.
    Keep, per span, the event with attributions (inner) else the first."""
    by_span = {}
    for e in events:
        key = json.dumps(e.get("src"), sort_keys=True) + e.get("decl", "")
        cur = by_span.get(key)
        if cur is None or (not cur["attributions"] and e["attributions"]):
            by_span[key] = e
    return list(by_span.values())


def main():
    studies = load_studies()
    if not studies:
        print("no studies found", file=sys.stderr)
        sys.exit(1)

    report = {}
    grand = defaultdict(list)

    for fname, s in studies.items():
        rec = s["record"]
        ref = {d["name"]: d for d in s["referencedDecls"] if "error" not in d}
        ref_errors = [d for d in s["referencedDecls"] if "error" in d]
        infra = {n for n, d in ref.items() if d.get("classification")}
        ds = s["declStudies"]
        showcase = [d for d in ds if d["showcase"]]

        events = dedup_events(s["useEvents"])
        events_by_decl = defaultdict(list)
        for e in events:
            events_by_decl[e["decl"]].append(e)

        # per-declaration measures over showcase decls
        rows = []
        for d in showcase:
            body = d["p2_supportBody"]
            body_infra = [n for n in body if n in infra]
            apps = d["p4_apps"] if isinstance(d["p4_apps"], list) else []
            named_app_heads = sorted({a["head"] for a in apps})
            evs = events_by_decl.get(d["name"], [])
            attributed = [a["decl"] for e in evs for a in e["attributions"]]
            style = classify_style(d["name"], events_by_decl, None)
            vsz = d["sizes"]["valueSize"]
            rows.append({
                "name": d["name"], "style": style,
                "valueSize": vsz, "typeSize": d["sizes"]["typeSize"],
                "p1_bodyOccs": len(d["p1_bodyRefs"]),
                "p2_body": len(body),
                "p2_bodyInfraFrac": (len(body_infra) / len(body)) if body else 0.0,
                "p2_domain": len(body) - len(body_infra),
                "p4_apps": len(apps),
                "p4_heads": len(named_app_heads),
                "p4_resultOkFrac": (sum(1 for a in apps if a["resultOk"]) / len(apps)) if apps else None,
                "p4_complete": d["p4_completeness"] == "complete",
                "p5_events": len(evs),
                "p5_attributed": sum(1 for e in evs if e["attributions"]),
                "compression_p2": (len(body) / vsz) if vsz else None,
                "compression_p4": (len(apps) / vsz) if vsz else None,
                # overlap: P5 attributed decls vs P2 body support / P4 heads
                "p5_in_p2": (len([a for a in set(attributed) if a in body]) / len(set(attributed))) if attributed else None,
                "p5_in_p4": (len([a for a in set(attributed) if a in named_app_heads]) / len(set(attributed))) if attributed else None,
                "p4_heads_in_p2": (len([h for h in named_app_heads if h in body]) / len(named_app_heads)) if named_app_heads else None,
            })

        styles = Counter(r["style"] for r in rows)
        nonfam = s.get("nonFamilyTacticKinds", {})
        automation_nonfam = {k: v for k, v in nonfam.items()
                             if any(h in k for h in AUTOMATION_KIND_HINTS)}

        def med(key, rows=rows, cond=lambda r: True):
            vals = [r[key] for r in rows if cond(r) and r[key] is not None]
            return round(st.median(vals), 3) if vals else None

        file_report = {
            "declsStored": len(rec["declarations"]),
            "declsUnsupported": len(rec["unsupported"]),
            "referencedDecls": len(ref),
            "referencedDeclErrors": len(ref_errors),
            "referencedInfraFrac": round(len(infra) / len(ref), 3) if ref else None,
            "states": len(rec["states"]),
            "transitions": len(rec["transitions"]),
            "showcaseCandidates": len(showcase),
            "styles": dict(styles),
            "useEvents": len(events),
            "useEventsAttributed": sum(1 for e in events if e["attributions"]),
            "declsWithAtLeastOneAttributedEvent":
                sum(1 for d in showcase
                    if any(e["attributions"] for e in events_by_decl.get(d["name"], []))),
            "p4_failures": [d["name"] for d in showcase if not (d["p4_completeness"] in ("complete", "no-body"))],
            "medians": {
                "valueSize": med("valueSize"),
                "p2_body": med("p2_body"),
                "p2_bodyInfraFrac": med("p2_bodyInfraFrac"),
                "p2_domain": med("p2_domain"),
                "p4_apps": med("p4_apps"),
                "p4_resultOkFrac": med("p4_resultOkFrac"),
                "compression_p2": med("compression_p2"),
                "compression_p4": med("compression_p4"),
                "p5_in_p2": med("p5_in_p2"),
                "p5_in_p4": med("p5_in_p4"),
                "p4_heads_in_p2": med("p4_heads_in_p2"),
            },
            "mediansByStyle": {
                sty: {"p2_bodyInfraFrac": med("p2_bodyInfraFrac", cond=lambda r, s=sty: r["style"] == s),
                      "p2_domain": med("p2_domain", cond=lambda r, s=sty: r["style"] == s),
                      "p5_events": med("p5_events", cond=lambda r, s=sty: r["style"] == s)}
                for sty in styles
            },
            "automationNonFamilyKinds": automation_nonfam,
            "rows": rows,
        }
        report[fname] = file_report
        grand["decls"].append(len(rec["declarations"]))
        grand["refs"].append(len(ref))

    total_backing = sum(grand["decls"]) + sum(grand["refs"])
    summary = {
        "files": len(studies),
        "storedDecls": sum(grand["decls"]),
        "referencedShallowDecls": sum(grand["refs"]),
        "totalBackingDecls": total_backing,
    }

    out = {"summary": summary, "files": report}
    with open(os.path.join(STUDY_DIR, "characterization.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    # markdown summary
    print(f"## Corpus totals\n")
    print(f"- files: {summary['files']}, stored decls: {summary['storedDecls']}, "
          f"referenced shallow decls: {summary['referencedShallowDecls']}, "
          f"total backing declarations: {summary['totalBackingDecls']}\n")
    hdr = ("| file | stored | showcase | styles | ref-infra% | P2 med (infra%) | P4 med apps | "
           "P5 ev (attr) | P5⊆P2 | P4⊆P2 | c(P2) | c(P4) |")
    print(hdr)
    print("|" + "---|" * 12)
    for fname, r in report.items():
        m = r["medians"]
        sty = ",".join(f"{k}:{v}" for k, v in sorted(r["styles"].items()))
        print(f"| {fname} | {r['declsStored']} | {r['showcaseCandidates']} | {sty} | "
              f"{r['referencedInfraFrac']} | {m['p2_body']} ({m['p2_bodyInfraFrac']}) | {m['p4_apps']} | "
              f"{r['useEvents']} ({r['useEventsAttributed']}) | {m['p5_in_p2']} | {m['p4_heads_in_p2']} | "
              f"{m['compression_p2']} | {m['compression_p4']} |")


if __name__ == "__main__":
    main()
