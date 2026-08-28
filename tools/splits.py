#!/usr/bin/env python
"""Module-granular TRAIN / DEV-LARGE / SEALED-MODULE partition.

WHY THIS EXISTS.  `prover_tasks.py` holds out MODULES (seed 1,
HOLDOUT_FRAC) but then draws theorems from the held pool by shuffling and
slicing.  DEV80 is therefore scattered across held modules, and "the rest
of the holdout" is NOT module-disjoint from DEV80: a theorem sitting in the
same file as a DEV80 theorem shares its imports, its local API, and often
its proof idiom.  Calling that set sealed would be wrong.

This tool partitions at MODULE granularity:

  TRAIN       every non-held module.  Retrieval statistics (peer scores,
              citation priors) are computed from these roots only - the
              same population `prover_tasks.py` already uses.
  DEV-LARGE   the held modules that DEV80 touched, plus a designated
              development share of the remaining held modules.  Mechanism
              development (IR fields, executor fixes) may look at these.
  SEALED      the held modules DEV80 never touched and DEV-LARGE did not
              claim.  Never used to modify the IR or the executor.

DEV80 is a strict subset of DEV-LARGE by construction.

SEALING DISCIPLINE.  Reference proofs of SEALED theorems may be opened
AFTER inference, only to build labels and score results.  They must never
supply oracle support, semantic actions, action parameters, or
proof-body-derived features to an autonomous prover.  Once semantic IR v1
is frozen, a SEALED failure must not motivate an IR change while the set
keeps that name; re-drawing the sealed set is the only honest response, and
`--seal-seed` records which draw was used.

Usage:
  splits.py [--dev-share 0.35] [--seal-seed 20260827] [--n-dev80 80]
Writes bigdata/splits.json.
"""
import argparse
import json
import sys
import time

import numpy as np

from atlas import BIG, load_dump, theorem_roots
from accessibility import Accessibility
import rolodex as R
from rolodex2 import HOLDOUT_FRAC


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-share", type=float, default=0.35,
                    help="share of non-DEV80 held modules assigned to DEV-LARGE")
    ap.add_argument("--seal-seed", type=int, default=20260827,
                    help="seed for the DEV-LARGE/SEALED draw; recorded in the manifest")
    ap.add_argument("--n-dev80", type=int, default=80,
                    help="prefix length that defines DEV80 (must match prover_tasks.py)")
    ap.add_argument("--out", default=str(BIG / "splits.json"))
    args = ap.parse_args(argv)

    log("loading atlas + accessibility...")
    a = load_dump()
    acc = Accessibility(a)
    roots = theorem_roots(a)
    isthm = np.array([a.kind[i] == "theorem" and not a.cls[i] for i in range(a.n)])

    # --- reproduce prover_tasks.py's holdout EXACTLY (seed 1) -----------
    rng = np.random.default_rng(1)
    root_mods = acc.mod_of[np.array(roots)]
    mathlib_mods = [i for i, nm in enumerate(acc.mod_names)
                    if nm.startswith("Mathlib.")]
    held = set(int(x) for x in
               rng.choice(mathlib_mods,
                          size=int(len(mathlib_mods) * HOLDOUT_FRAC),
                          replace=False))
    test_all = [p for p in range(len(roots)) if int(root_mods[p]) in held]
    rng.shuffle(test_all)
    test_pos = [p for p in test_all if isthm[R.proof_deps(a, roots[p])].any()]
    dev80_pos = test_pos[:args.n_dev80]
    dev80_names = [a.names[roots[p]] for p in dev80_pos]
    dev80_mods = sorted({int(root_mods[p]) for p in dev80_pos})
    log(f"held modules {len(held)}; eligible held theorems {len(test_pos)}; "
        f"DEV80 touches {len(dev80_mods)} modules")

    # --- DEV-LARGE / SEALED at module granularity ----------------------
    rest = sorted(set(held) - set(dev80_mods))
    srng = np.random.default_rng(args.seal_seed)
    perm = srng.permutation(len(rest))
    k = int(len(rest) * args.dev_share)
    dev_extra = sorted(int(rest[i]) for i in perm[:k])
    sealed_mods = sorted(int(rest[i]) for i in perm[k:])
    dev_mods = sorted(set(dev80_mods) | set(dev_extra))
    train_mods = sorted(set(mathlib_mods) - set(held))

    assert not (set(dev_mods) & set(sealed_mods)), "DEV/SEALED overlap"
    assert not (set(train_mods) & set(held)), "TRAIN/held overlap"
    assert set(dev80_mods) <= set(dev_mods), "DEV80 not inside DEV-LARGE"

    def theorems_in(mods):
        ms = set(mods)
        return [a.names[roots[p]] for p in range(len(roots))
                if int(root_mods[p]) in ms]

    dev_thms = theorems_in(dev_mods)
    sealed_thms = theorems_in(sealed_mods)
    train_thms = theorems_in(train_mods)

    # eligible = has at least one theorem premise in its proof (the
    # condition prover_tasks.py applies when drawing tasks)
    def eligible_in(mods):
        ms = set(mods)
        return [a.names[roots[p]] for p in range(len(roots))
                if int(root_mods[p]) in ms and isthm[R.proof_deps(a, roots[p])].any()]

    sealed_elig = eligible_in(sealed_mods)
    dev_elig = eligible_in(dev_mods)

    manifest = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "provenance": {
            "holdout_seed": 1,
            "holdout_frac": HOLDOUT_FRAC,
            "seal_seed": args.seal_seed,
            "dev_share": args.dev_share,
            "n_dev80": args.n_dev80,
            "note": "holdout reproduces prover_tasks.py; DEV/SEALED split is "
                    "module-granular so SEALED shares no module with DEV80",
        },
        "counts": {
            "modules": {"train": len(train_mods), "dev_large": len(dev_mods),
                        "sealed": len(sealed_mods), "dev80": len(dev80_mods)},
            "theorems": {"train": len(train_thms), "dev_large": len(dev_thms),
                         "sealed": len(sealed_thms), "dev80": len(dev80_names)},
            "eligible": {"dev_large": len(dev_elig), "sealed": len(sealed_elig)},
        },
        "modules": {
            "dev80": [acc.mod_names[m] for m in dev80_mods],
            "dev_large": [acc.mod_names[m] for m in dev_mods],
            "sealed": [acc.mod_names[m] for m in sealed_mods],
        },
        "dev80": dev80_names,
        "sealed_eligible": sealed_elig,
        "dev_large_eligible": dev_elig,
    }
    with open(args.out, "w") as f:
        json.dump(manifest, f)

    c = manifest["counts"]
    log(f"TRAIN      {c['modules']['train']:5d} modules  {c['theorems']['train']:7d} theorems")
    log(f"DEV-LARGE  {c['modules']['dev_large']:5d} modules  {c['theorems']['dev_large']:7d} theorems"
        f"  ({c['eligible']['dev_large']} eligible)")
    log(f"  of which DEV80 {c['modules']['dev80']} modules / {c['theorems']['dev80']} theorems")
    log(f"SEALED     {c['modules']['sealed']:5d} modules  {c['theorems']['sealed']:7d} theorems"
        f"  ({c['eligible']['sealed']} eligible)")
    log(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
