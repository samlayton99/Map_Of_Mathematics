#!/usr/bin/env python3
"""Self-test for the shipped dashboard.

Checks the payload the viewer will actually read, not the code that made it.
Every failure here is something the user would have seen as a blank panel, a
dash where a number should be, or a page that would not load at all.

    ~/venv/general_ml/bin/python src/dashboard_check.py [dist_dir]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

FAILS, WARNS = [], []


def bad(msg):
    FAILS.append(msg)


def warn(msg):
    WARNS.append(msg)


def strict_load(path):
    """Parse exactly as JSON.parse would: NaN and Infinity are errors."""
    txt = open(path).read()
    return json.loads(txt, parse_constant=lambda c: (_ for _ in ()).throw(
        ValueError(f"non-finite literal {c!r} in {os.path.basename(path)}")))


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        ROOT, "dashboard", "dist", "map_results")
    data = os.path.join(d, "data")
    if not os.path.isdir(data):
        sys.exit(f"no data dir at {data}")
    print(f"checking {d}", flush=True)

    # ---- viewer -----------------------------------------------------------
    vh = os.path.join(d, "viewer.html")
    if not os.path.exists(vh):
        bad("viewer.html missing")
    else:
        html = open(vh).read()
        for need, why in [
                ("window.Charts", "charts library not inlined"),
                ("window.Report", "report generator not inlined"),
                ('src="data/all.js"', "offline data loader not linked"),
                ("webkitdirectory", "folder-picker fallback missing"),
                ("MAPDATA", "bundle global not referenced")]:
            if need not in html:
                bad(f"viewer.html: {why} ({need!r} absent)")
        if "<script src=\"http" in html or "cdn." in html:
            bad("viewer.html references an external resource; it must be "
                "fully self-contained")

    # ---- strict JSON ------------------------------------------------------
    payloads = {}
    for fn in sorted(os.listdir(data)):
        if not fn.endswith(".json"):
            continue
        try:
            payloads[fn] = strict_load(os.path.join(data, fn))
        except Exception as e:
            bad(f"{fn}: {e}")
    print(f"  {len(payloads)} json files parse strictly", flush=True)

    man = payloads.get("manifest.json")
    if not man:
        sys.exit("manifest.json missing or unparseable")
    for fn in man.get("files", []):
        if fn not in payloads:
            bad(f"manifest lists {fn} but it is not present")

    # ---- all.js -----------------------------------------------------------
    ajs = os.path.join(data, "all.js")
    bundle = None
    if not os.path.exists(ajs):
        bad("data/all.js missing -- the viewer cannot load offline")
    else:
        txt = open(ajs).read()
        if not txt.startswith("window.MAPDATA"):
            bad("all.js does not assign window.MAPDATA")
        try:
            bundle = json.loads(txt[txt.index("=") + 1:].rstrip().rstrip(";"))
        except Exception as e:
            bad(f"all.js payload is not valid JSON: {e}")
    if bundle:
        for k in ("manifest", "summary", "definitions", "vibe", "rankings"):
            if not bundle.get(k):
                bad(f"all.js payload missing {k!r}")
        if set(bundle.get("rankings", {})) != {r["name"] for r in man["rankings"]}:
            bad("all.js rankings do not match the manifest")
        if not bundle.get("sweep"):
            warn("all.js has no sweep data: the slider curve will show a "
                 "'not available' notice instead of the figure")

    universes = man["universes"]
    lanes = man["lanes"]
    ks = man["ks"]
    names = [r["name"] for r in man["rankings"]]

    # ---- definitions ------------------------------------------------------
    defs = payloads.get("definitions.json", {})
    for k in ("how_a_run_is_built", "universes", "lanes", "metric_families",
              "grades", "headline_metrics", "signals", "cautions"):
        if k not in defs:
            bad(f"definitions.json missing section {k!r}")
    for u in universes:
        if u not in defs.get("universes", {}):
            bad(f"definitions.json does not document universe {u}")
    for l in lanes:
        if l not in defs.get("lanes", {}):
            bad(f"definitions.json does not document lane {l}")

    # ---- ranking payloads -------------------------------------------------
    for nm in names:
        fn = f"ranking_{nm}.json"
        p = payloads.get(fn)
        if not p:
            bad(f"{fn} missing")
            continue
        if not (p.get("spec") or {}).get("source"):
            bad(f"{fn}: no reproducible source in spec")
        for u in universes:
            e = (p.get("experiments") or {}).get(u)
            if not e:
                bad(f"{fn}: no experiment for universe {u}")
                continue
            rq = e.get("ranking_quality") or {}
            for k in ("source", "semantic", "composition", "ties"):
                if k not in rq:
                    bad(f"{fn}[{u}]: ranking_quality missing {k}")
            sem = rq.get("semantic") or {}
            for k in ("SemanticKeyMoveAt1", "SemanticBadAt1",
                      "SemanticLegitGlueAt1", "grade_at_1", "by_target_depth",
                      "worst_misses", "false_promotions"):
                if k not in sem:
                    bad(f"{fn}[{u}]: semantic missing {k}")
            g1 = sem.get("grade_at_1") or {}
            if g1:
                tot = sum(v for v in g1.values() if v is not None)
                if abs(tot - 1.0) > 0.02:
                    bad(f"{fn}[{u}]: grade_at_1 sums to {tot:.3f}, not 1")
            if sem.get("n_proofs_scored", 0) < 50:
                warn(f"{fn}[{u}]: only {sem.get('n_proofs_scored')} graded "
                     "proofs scored")
            for l in lanes:
                for k in ks:
                    if f"{l}|{k}" not in (e.get("views") or {}):
                        bad(f"{fn}[{u}]: no view cell {l}|{k}")
            comp = rq.get("composition") or {}
            if str(1) not in {str(x) for x in (comp.get("at_k") or {})}:
                bad(f"{fn}[{u}]: composition has no at_k=1")

    # ---- summary ----------------------------------------------------------
    summ = payloads.get("summary.json", {})
    for nm in names:
        r = (summ.get("rankings") or {}).get(nm)
        if not r:
            bad(f"summary.json: no entry for {nm}")
            continue
        for u in universes:
            if u not in r.get("by_universe", {}):
                bad(f"summary.json[{nm}]: missing universe {u}")

    # ---- vibe -------------------------------------------------------------
    vibe = payloads.get("vibe.json", {})
    proofs = vibe.get("proofs") or []
    if len(proofs) < 8:
        bad(f"vibe.json has only {len(proofs)} proofs")
    depths = sorted(p["theorem_depth"] for p in proofs)
    if depths and depths[-1] - depths[0] < 50:
        warn("vibe proofs do not span much depth")
    n_expl = n_grade = n_cand = 0
    for p in proofs:
        for u in universes:
            for nm in names:
                if f"{u}|{nm}" not in (p.get("orders") or {}):
                    bad(f"vibe.json[{p['id']}]: no order for {u}|{nm}")
        for cd in p["candidates"]:
            n_cand += 1
            for f in ("name", "kind", "cited_depth", "target_depth",
                      "in_statement", "role", "system_category", "lanes"):
                if f not in cd:
                    bad(f"vibe.json[{p['id']}] candidate {cd.get('n')}: "
                        f"missing display field {f}")
            if cd.get("grade") is not None:
                n_grade += 1
            if cd.get("explanation_llm"):
                n_expl += 1
        # every candidate must be ranked by every ranking
        for u in universes:
            for nm in names:
                o = p["orders"][f"{u}|{nm}"]
                ranked = [k for k, v in o.items() if v.get("rank") is not None]
                if u == man["reference_universe"] and not ranked:
                    bad(f"vibe.json[{p['id']}]: nothing ranked under {u}|{nm}")
    if n_cand:
        print(f"  vibe: {len(proofs)} proofs, {n_cand} candidates, "
              f"{n_grade} graded ({100*n_grade//n_cand}%), "
              f"{n_expl} glossed ({100*n_expl//n_cand}%)", flush=True)
    if n_expl < 0.9 * n_cand:
        warn(f"only {n_expl}/{n_cand} vibe candidates have an English gloss")
    if n_grade < 0.9 * n_cand:
        warn(f"only {n_grade}/{n_cand} vibe candidates carry a rater grade")

    # ---- sweep ------------------------------------------------------------
    sw = payloads.get("sweep.json")
    if not sw:
        warn("sweep.json absent: no slider curve")
    else:
        lv = sw.get("levels") or []
        if not any(l.get("kind") == "cluster" for l in lv):
            warn("sweep has no cluster_split level")
        for u in universes:
            for nm in names:
                key = f"{u}|{nm}"
                cur = (sw.get("curves") or {}).get(key)
                if not cur:
                    bad(f"sweep.json: no curve for {key}")
                    continue
                pts = [(v.get("ViewSizeFraction"), v.get("ViewKeyRetained"))
                       for lid, v in cur.items() if v]
                pts = [(a, b) for a, b in pts if a is not None]
                if len(pts) < 5:
                    warn(f"sweep {key}: only {len(pts)} usable points")
                # key retention must not increase as the view shrinks
                pts.sort()
                ys = [b for _, b in pts if b is not None]
                if ys and any(ys[i] - ys[i + 1] > 0.02
                              for i in range(len(ys) - 1)):
                    warn(f"sweep {key}: key retention is not monotone in size")

    # ---- report -----------------------------------------------------------
    print()
    for w in WARNS:
        print(f"  WARN  {w}", flush=True)
    for f in FAILS:
        print(f"  FAIL  {f}", flush=True)
    print(f"\n{len(FAILS)} failures, {len(WARNS)} warnings", flush=True)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
