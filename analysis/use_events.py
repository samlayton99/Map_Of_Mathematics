#!/usr/bin/env python3
"""Phase 2B use-event feasibility measurement.

Reads studies/*.study.json, dedups nested events, and reports per file and
overall: coverage (events per proof, proofs with >=1 attributed event),
attribution rate by role, ambiguity (multi-attribution events), tier counts,
and the automation gap (family vs non-family tactic volume). Also emits a
stratified sample for manual precision inspection.

All numbers are deterministic-derived from observed elaborator data.
"""
import json, glob, os, sys, random
from collections import Counter, defaultdict

STUDY_DIR = os.path.join(os.path.dirname(__file__), "..", "studies")
sys.path.insert(0, os.path.dirname(__file__))
from characterize import dedup_events  # noqa: E402


def main():
    overall = Counter()
    role_attr = defaultdict(lambda: [0, 0])  # role -> [events, attributed]
    ambiguity = Counter()
    per_file = {}
    sample_pool = []

    for path in sorted(glob.glob(os.path.join(STUDY_DIR, "*.study.json"))):
        fname = os.path.basename(path).replace(".study.json", "")
        with open(path) as f:
            s = json.load(f)
        events = dedup_events(s["useEvents"])
        by_decl = defaultdict(list)
        for e in events:
            by_decl[e["decl"]].append(e)
        theorems = [d["name"] for d in s["declStudies"]
                    if d["showcase"] and d["kind"] == "theorem"]
        tactic_thms = [t for t in theorems if by_decl.get(t)]
        attributed_thms = [t for t in theorems
                           if any(e["attributions"] for e in by_decl.get(t, []))]
        nonfam_total = sum(v for k, v in s.get("nonFamilyTacticKinds", {}).items()
                           if k not in ("null", "by", "Lean.Parser.Term.byTactic",
                                        "Lean.Parser.Tactic.tacticSeq",
                                        "Lean.Parser.Tactic.tacticSeq1Indented",
                                        "Lean.Parser.Tactic.paren"))
        n_attr = sum(1 for e in events if e["attributions"])
        for e in events:
            role_attr[e["role"]][0] += 1
            if e["attributions"]:
                role_attr[e["role"]][1] += 1
            n = len({a["decl"] for a in e["attributions"]})
            ambiguity["multi" if n > 1 else ("one" if n == 1 else "zero")] += 1
            if e["attributions"]:
                sample_pool.append((fname, e))
        per_file[fname] = {
            "theorems": len(theorems),
            "tacticTheorems": len(tactic_thms),
            "theoremsWithAttributedEvent": len(attributed_thms),
            "events": len(events),
            "attributedEvents": n_attr,
            "attrRate": round(n_attr / len(events), 3) if events else None,
            "nonFamilyTacticNodes": nonfam_total,
            "familyShareOfTacticNodes":
                round(len(events) / (len(events) + nonfam_total), 3)
                if (events or nonfam_total) else None,
            "unsupportedStates": len(s.get("unsupportedStates", [])),
        }
        overall["events"] += len(events)
        overall["attributed"] += n_attr
        overall["theorems"] += len(theorems)
        overall["attributedThms"] += len(attributed_thms)
        overall["tacticThms"] += len(tactic_thms)

    out = {
        "perFile": per_file,
        "overall": {
            "events": overall["events"],
            "attributedEvents": overall["attributed"],
            "attributionRate": round(overall["attributed"] / overall["events"], 3),
            "theorems": overall["theorems"],
            "tacticTheorems": overall["tacticThms"],
            "theoremsWithAttributedEvent": overall["attributedThms"],
            "coverageAllTheorems": round(overall["attributedThms"] / overall["theorems"], 3),
            "coverageTacticTheorems":
                round(overall["attributedThms"] / overall["tacticThms"], 3)
                if overall["tacticThms"] else None,
        },
        "byRole": {r: {"events": v[0], "attributed": v[1],
                       "rate": round(v[1] / v[0], 3)} for r, v in sorted(role_attr.items())},
        "ambiguity": dict(ambiguity),
    }

    # deterministic stratified sample for manual precision check
    random.seed(20260818)
    by_role = defaultdict(list)
    for fname, e in sample_pool:
        by_role[e["role"]].append((fname, e))
    sample = []
    for role, items in sorted(by_role.items()):
        for fname, e in random.sample(items, min(4, len(items))):
            sample.append({"file": fname, "role": role,
                           "actionText": e["actionText"],
                           "attributions": [a["decl"] for a in e["attributions"]],
                           "decl": e["decl"], "src": e.get("src")})
    out["manualPrecisionSample"] = sample

    with open(os.path.join(STUDY_DIR, "use_events.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(out["overall"], indent=1))
    print("\nby role:")
    for r, v in out["byRole"].items():
        print(f"  {r:12s} events={v['events']:4d} attributed={v['attributed']:4d} rate={v['rate']}")
    print("\nambiguity:", out["ambiguity"])
    print(f"\nmanual sample: {len(sample)} events -> studies/use_events.json")


if __name__ == "__main__":
    main()
