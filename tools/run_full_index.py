#!/usr/bin/env python
"""Run the full-Mathlib moves index: calibrate one batch, then index all
theorem roots.  Logs to stderr; outputs to bigdata/."""
import sys
import time

import numpy as np

from atlas import BIG, load_dump, theorem_roots, batch_cones, run_index

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)

t0 = time.time()
log("loading atlas from cache...")
atlas = load_dump()
log(f"atlas ready in {time.time()-t0:.0f}s: {atlas.n:,} constants, "
    f"{atlas.ncomp:,} SCCs")

roots = theorem_roots(atlas)
log(f"roots: {len(roots):,} unclassified theorems with proof bodies")

t1 = time.time()
maskS, maskP = batch_cones(atlas, roots[:512])
dt = time.time() - t1
est = dt * (len(roots) / 512)
log(f"calibration: one 512-root batch in {dt:.1f}s -> "
    f"~{est/3600:.1f}h propagation for all roots (extraction extra)")

t2 = time.time()
inS, inP, asNew = run_index(atlas, roots, BIG / "mathlib_moves_index.jsonl",
                            batch=512, topk=12, log=log)
np.savez_compressed(BIG / "mathlib_usage_counters.npz",
                    inS=inS, inP=inP, asNew=asNew)
log(f"index complete in {(time.time()-t2)/3600:.2f}h; counters saved")
