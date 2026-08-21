#!/usr/bin/env python3
"""The landing port: one command turns a new ranking into a delivered dashboard.

    ~/venv/general_ml/bin/python src/ship.py

Steps, in order, each skippable by flag:

    1. load  rankings_local/*.py, so a ranking dropped in as a file joins the
             suite with no edit anywhere else
    2. verify every registered ranking against the contract (orders every
             candidate, never drops one, finite numeric keys)
    3. export the full metric grid            -> dashboard/data/
    4. sweep  the inclusiveness curve          -> dashboard/data/sweep.json
    5. package a single self-contained viewer  -> dashboard/dist/map_results/
    6. deliver to the laptop

Flags: --no-export --no-sweep --no-send --only-package
       --rankings A,B   restrict the export to these rankings (fast iteration)
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PY = sys.executable
SEND = os.path.expanduser("~/sam-setup/utilities/send")
DEST = "laptop:~/Desktop/map_results"


def run(script, *args):
    t = time.time()
    print(f"\n=== {script} {' '.join(args)}", flush=True)
    r = subprocess.run([PY, os.path.join(HERE, script), *args], cwd=ROOT)
    if r.returncode:
        sys.exit(f"{script} failed with code {r.returncode}")
    print(f"=== {script} ok ({time.time() - t:.0f}s)", flush=True)


def main():
    a = sys.argv[1:]
    only_pkg = "--only-package" in a
    sys.path.insert(0, ROOT)

    from mathmap_eval import plugins
    from mathmap_eval import rankings as R
    print("=== landing port", flush=True)
    plugins.load_local()
    print(f"  {len(R.REGISTRY)} rankings registered: "
          f"{', '.join(R.names())}", flush=True)

    if not only_pkg:
        from mathmap_eval.corpus import get_corpus
        c = get_corpus()
        bad = False
        for nm in R.names():
            probs = plugins.verify(nm, c)
            if probs:
                bad = True
                print(f"  FAIL {nm}", flush=True)
                for p in probs:
                    print(f"       - {p}", flush=True)
            else:
                print(f"  ok   {nm}", flush=True)
        if bad:
            sys.exit("a ranking violates the contract; not shipping")

    if not only_pkg and "--no-export" not in a:
        extra = []
        if "--rankings" in a:
            extra = ["--rankings", a[a.index("--rankings") + 1]]
        run("dashboard_export.py", *extra)
    if not only_pkg and "--no-sweep" not in a:
        if os.path.exists(os.path.join(HERE, "sweep_export.py")):
            run("sweep_export.py")
        else:
            print("\n(no sweep_export.py yet; slider curve will be absent)",
                  flush=True)
    run("package_dashboard.py")

    if "--no-send" not in a:
        dist = os.path.join(ROOT, "dashboard", "dist", "map_results")
        if not os.path.exists(SEND):
            print(f"\n(no send utility at {SEND}; dashboard is at {dist})",
                  flush=True)
            return
        print(f"\n=== delivering to {DEST}", flush=True)
        r = subprocess.run([SEND, dist, "laptop"], cwd=ROOT)
        if r.returncode:
            print("delivery failed; the built folder is at " + dist, flush=True)
        else:
            print("delivered.", flush=True)


if __name__ == "__main__":
    main()
