#!/usr/bin/env python3
"""Package the dashboard into one self-contained viewer.html plus its data.

The shipped folder is:

    map_results/
      viewer.html          one file: markup + CSS + charts + report generator
      data/all.js          the whole payload as one JS assignment
      data/*.json          the same payload as strict JSON, for agents
      README.txt

viewer.html is opened by double-clicking. It loads `data/all.js` through a
<script> tag, which is the one mechanism that works from `file://` in every
browser -- `fetch()` of an adjacent file does not. The JSON files are shipped
alongside because they are what gets handed to another agent, and because the
viewer will fetch them if the folder is ever served over http. A File API
folder picker is the third fallback.
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DASH = os.path.join(ROOT, "dashboard")
DATA = os.path.join(DASH, "data")
DIST = os.path.join(DASH, "dist", "map_results")

README = """MathMap ranking results suite
=============================

Open `viewer.html` by double-clicking it. No server, no install, no terminal.

If the page ever comes up asking for the data folder, point the picker at the
`data` folder sitting next to viewer.html. That fallback exists because a few
browser configurations block even script-tag loads from file://.

What is in here
---------------
  viewer.html      the dashboard. Self-contained: markup, styling, charts and
                   the report generator are all inlined.
  data/all.js      the entire payload as one JavaScript assignment. This is
                   what the page actually reads.
  data/*.json      the same payload as strict JSON (no NaN literals), for
                   handing to another agent or loading in Python.
  data/manifest.json  lists every file, every ranking, and the build stamp.

Reading the dashboard
---------------------
The controls at the top are split into two groups and the split is the whole
point:

  EXPERIMENT (universe)  changes the candidate set, so it genuinely re-ranks.
  VIEW (policy, k, lane) only changes what is displayed. It can never move a
                         ranking-quality number.

Panels are badged INVARIANT or CURRENT SLICE so you always know which kind of
number you are reading.

Tabs: How to read this / Summary / Vibe check, then one detailed tab per
ranking. Each ranking tab has an "Export this report" button that downloads a
detailed Markdown report of that ranking plus its comparison against all the
others -- that is the file to hand to another agent.
"""


def main():
    if not os.path.isdir(DATA):
        sys.exit(f"no data at {DATA}; run src/dashboard_export.py first")
    head = open(os.path.join(DASH, "viewer_head.html")).read()
    body = open(os.path.join(DASH, "viewer_body.html")).read()

    parts = []
    for js in ("charts.js", "report.js"):
        p = os.path.join(DASH, js)
        if not os.path.exists(p):
            sys.exit(f"missing {p}")
        parts.append(f"<!-- inlined {js} -->\n<script>\n"
                     + open(p).read() + "\n</script>")

    html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n" + head
            + "\n</head>\n<body>\n"
            + "\n".join(parts) + "\n"
            + "<script src=\"data/all.js\"></script>\n"
            + body + "\n</body>\n</html>\n")

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "data"))
    with open(os.path.join(DIST, "viewer.html"), "w") as f:
        f.write(html)
    for fn in sorted(os.listdir(DATA)):
        shutil.copy2(os.path.join(DATA, fn), os.path.join(DIST, "data", fn))
    with open(os.path.join(DIST, "README.txt"), "w") as f:
        f.write(README)

    # Rebuild all.js from the JSON files rather than trusting whatever the
    # export left behind. Later stages (vibe_scores.py, sweep_export.py) edit
    # the JSON after the export wrote its bundle, so a copied all.js would be
    # silently stale: the page would show old numbers while the JSON beside it
    # showed new ones. Regenerating here makes that class of bug impossible.
    alljs = os.path.join(DIST, "data", "all.js")
    dd = os.path.join(DIST, "data")
    load = lambda n: json.load(open(os.path.join(dd, n)))
    payload = {"manifest": load("manifest.json"),
               "summary": load("summary.json"),
               "definitions": load("definitions.json"),
               "vibe": load("vibe.json"), "rankings": {}}
    for r in payload["manifest"]["rankings"]:
        payload["rankings"][r["name"]] = load(f"ranking_{r['name']}.json")
    if os.path.exists(os.path.join(dd, "sweep.json")):
        payload["sweep"] = load("sweep.json")
        if "sweep.json" not in payload["manifest"].setdefault("files", []):
            payload["manifest"]["files"].append("sweep.json")
    print("  rebuilt all.js from the JSON payload"
          + (" (with sweep)" if payload.get("sweep") else " (no sweep yet)"),
          flush=True)
    with open(alljs, "w") as f:
        f.write("window.MAPDATA = ")
        json.dump(payload, f, allow_nan=False)
        f.write(";\n")
    n_json = len([f for f in os.listdir(os.path.join(DIST, "data"))
                  if f.endswith(".json")])
    size = sum(os.path.getsize(os.path.join(dp, f))
               for dp, _, fs in os.walk(DIST) for f in fs) / 1e6
    print(f"packaged {DIST}", flush=True)
    print(f"  viewer.html   {os.path.getsize(os.path.join(DIST, 'viewer.html'))/1e3:.0f} KB "
          f"(charts + report inlined)", flush=True)
    print(f"  data/all.js   {os.path.getsize(alljs)/1e6:.1f} MB", flush=True)
    print(f"  data/*.json   {n_json} files", flush=True)
    print(f"  rankings      {len(payload['rankings'])}", flush=True)
    print(f"  sweep         {'yes' if payload.get('sweep') else 'NO'}", flush=True)
    print(f"  total         {size:.1f} MB", flush=True)


if __name__ == "__main__":
    main()
