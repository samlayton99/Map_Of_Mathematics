#!/usr/bin/env python
"""Study paths for landmark theorems at full-Mathlib scale.

Resolves each candidate (exact name, else unique dot-suffix match), builds
its statement-path / proof-moves decomposition with the real library-wide
closure, writes tools/output/mathlib_showcase_paths.{txt,json}.

Run: ~/venv/general_ml/bin/python tools/atlas_showcase.py
"""
import json
from pathlib import Path

from atlas import load_dump, build_path, render_text

OUT = Path(__file__).resolve().parent / "output"

CANDIDATES = [
    "Nat.exists_infinite_primes",           # Euclid: infinitude of primes
    "irrational_sqrt_two",                  # sqrt 2 is irrational
    "Complex.exp_pi_mul_I",                 # Euler's identity
    "legendreSym.quadratic_reciprocity",    # Gauss: quadratic reciprocity
    "intervalIntegral.integral_deriv_eq_sub",  # fundamental thm of calculus
    "norm_inner_le_norm",                   # Cauchy-Schwarz
    "Real.log_mul",                         # continuity with the corpus study
    "CompactIccSpace.isCompact_Icc",        # Heine-Borel on an interval
    "Nat.Prime.dvd_mul",                    # Euclid's lemma
    "Real.tendsto_sum_pi_div_four",         # Leibniz series for pi
]


def resolve(atlas, name):
    if name in atlas.idx:
        return name
    tail = "." + name
    hits = [n for n in atlas.names if n.endswith(tail)]
    if len(hits) == 1:
        return hits[0]
    return None


def main():
    OUT.mkdir(exist_ok=True)
    print("loading atlas...")
    atlas = load_dump()
    texts, blobs = [], []
    for cand in CANDIDATES:
        name = resolve(atlas, cand)
        if name is None:
            print(f"  UNRESOLVED: {cand}")
            continue
        r = build_path(atlas, name)
        rm = build_path(atlas, name, drop_machinery=True)
        texts.append(render_text(rm) +
                     f"\n   [machinery hidden from statement path; "
                     f"full cones: A_S {r['statement_cone_size']:,}, "
                     f"A_P {r['proof_cone_size']:,}]")
        blobs.append(r)
        print(f"  {name}: A_S {r['statement_cone_size']:,}  "
              f"A_P {r['proof_cone_size']:,}  N {r['new_count']:,}")
    (OUT / "mathlib_showcase_paths.txt").write_text("\n\n".join(texts) + "\n")
    (OUT / "mathlib_showcase_paths.json").write_text(json.dumps(blobs, indent=1))
    print(f"wrote {len(blobs)} showcase paths")


if __name__ == "__main__":
    main()
