"""CLI:  python -m mathmap_eval [command]

    list                    show registered rankings and inclusion policies
    compare [--universe U1] run every ranking, print the comparison tables
    coverage                candidate-universe coverage by declaration kind
    bridges [--ranking R]   bridge enrichment (batch-invariant mergers)
    nested                  verify every slider policy is actually nested
"""
import argparse, json, sys
import numpy as np
from . import (RunConfig, run, compare_table, depth_table, graph_table,
               ranking_names, inclusion_names, get_corpus, check_nested,
               RANKINGS, INCLUSIONS, metrics)
from . import rankings as R, inclusion as I


def cmd_list(a):
    print("RANKINGS")
    for fam in ("baseline", "candidate"):
        print(f"  [{fam}]")
        for n in ranking_names(fam):
            s = RANKINGS[n]
            print(f"    {n:<24} {s.doc.splitlines()[0] if s.doc else ''}")
    print("\nINCLUSION POLICIES")
    for fam in ("per-proof", "global"):
        print(f"  [{fam}]")
        for n in inclusion_names(fam):
            s = INCLUSIONS[n]
            print(f"    {n:<24} {s.doc.splitlines()[0] if s.doc else ''}")


def cmd_compare(a):
    out = run(RunConfig(universe=a.universe, out=a.out,
                        rankings=tuple(a.ranking) if a.ranking else ()))
    print("\n== Source agreement (NOT keyness) ==")
    print(compare_table(out))
    print("\n== SourceHit@1 by target depth ==")
    print(depth_table(out))
    print("\n== Graph structure by inclusion (top_k) ==")
    print(graph_table(out))
    print(f"\ncandidate coverage in {a.universe}: "
          f"{out['coverage']['ALL']['CoverageInUniverse']:.1%} of written citations")


def cmd_coverage(a):
    c = get_corpus()
    for u in a.universe:
        cov = metrics.coverage_metrics(c, u)
        print(f"\nuniverse {u}")
        print(f"  {'kind':<26}{'written':>10}{'in record':>11}{'in universe':>13}{'coverage':>10}")
        for k, v in sorted(cov.items()):
            print(f"  {k:<26}{v['written']:>10,}{v.get('in_record',0):>11,}"
                  f"{v['in_universe']:>13,}{v['CoverageInUniverse']:>9.1%}")


def cmd_bridges(a):
    c = get_corpus()
    base = np.where(c.universe(a.universe))[0]
    spec = R.get(a.ranking)
    ranks = spec.ranks_within_proof(c, base)
    rows = metrics.bridge_enrichment(c, base, ranks, kmax=a.kmax, boot=a.boot)
    for r in rows:
        print(f"\nk={r['k']}  eligible={r['eligible']:,} crossing={r['crossing']:,} "
              f"eliminated={r['components_eliminated']:,} -> "
              f"components={r['components']:,} giant={r['giant']:.2%}")
        print(f"  {'kind':<26}{'P(elig)':>9}{'P(cross)':>10}{'enrich':>9}{'95% CI':>18}")
        for k2, e in sorted(r["enrichment"].items()):
            ci = (f"[{e['ci95'][0]:.2f},{e['ci95'][1]:.2f}]" if "ci95" in e else "")
            print(f"  {k2:<26}{e['p_eligible']:>8.1%}{e['p_crossing']:>9.1%}"
                  f"{e['enrichment']:>9.2f}{ci:>18}")
    if a.out:
        json.dump(rows, open(a.out, "w"), indent=1, default=float)


def cmd_nested(a):
    c = get_corpus()
    base = np.where(c.universe(a.universe))[0]
    ranks = R.get("R_introduced_depth").ranks_within_proof(c, base)
    for name, params in (("top_k", [1, 2, 4, 8, 16]),
                         ("top_pct", [0.1, 0.25, 0.5, 1.0])):
        ok, sizes = check_nested(c, base, ranks, name, params)
        print(f"  {name:<12} nested={ok}  sizes={sizes}")


def main():
    p = argparse.ArgumentParser(prog="mathmap_eval", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.set_defaults(f=cmd_list)
    s = sub.add_parser("compare"); s.set_defaults(f=cmd_compare)
    s.add_argument("--universe", default="U1")
    s.add_argument("--ranking", action="append")
    s.add_argument("--out", default=None)
    s = sub.add_parser("coverage"); s.set_defaults(f=cmd_coverage)
    s.add_argument("--universe", action="append", default=None)
    s = sub.add_parser("bridges"); s.set_defaults(f=cmd_bridges)
    s.add_argument("--ranking", default="R_introduced_depth")
    s.add_argument("--universe", default="U1")
    s.add_argument("--kmax", type=int, default=4)
    s.add_argument("--boot", type=int, default=0)
    s.add_argument("--out", default=None)
    s = sub.add_parser("nested"); s.set_defaults(f=cmd_nested)
    s.add_argument("--universe", default="U1")
    a = p.parse_args()
    if getattr(a, "universe", None) is None and a.cmd == "coverage":
        a.universe = ["U1", "U1D", "U0"]
    a.f(a)


if __name__ == "__main__":
    main()
