#!/usr/bin/env python3
"""Run the unmodified map_analysis over one or more edge sets in an isolated
OUT_DIR, then copy the result to data/map_final under a distinct name."""
import os
import shutil
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
P5 = os.path.normpath(os.path.join(ROOT, "..", "phase5_multiscale_navigation", "data"))

sets = sys.argv[1].split(",")
tag = sys.argv[2]
outdir = os.path.join(ROOT, "data", "work_%s" % tag)
os.makedirs(outdir, exist_ok=True)
for s in sets:
    shutil.copy(os.path.join(ROOT, "data", "map_final", "edges_%s.npz" % s), outdir)

os.environ["MAPGRAPH_DATA_DIR"] = P5
os.environ["MAPGRAPH_OUT_DIR"] = outdir
os.environ.setdefault("MAPGRAPH_MODULES_TSV", "/Users/sam/mathmap_data/all_modules.tsv")

sys.path.insert(0, os.path.join(ROOT, "src"))
import map_graph as MG            # noqa: E402
import map_analysis as MA         # noqa: E402

MG.DATA_DIR = P5
MG.OUT_DIR = outdir
MA.EDGE_SETS = sets
MA.main()

shutil.copy(os.path.join(outdir, "map_analysis.json"),
            os.path.join(ROOT, "data", "map_final", "map_analysis_%s.json" % tag))
print("copied -> data/map_final/map_analysis_%s.json" % tag)
