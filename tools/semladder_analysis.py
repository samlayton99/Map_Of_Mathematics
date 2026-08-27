#!/usr/bin/env python3
"""Aggregate the semantic ladder: solved counts, dominance, per-rung deltas.

Usage: semladder_analysis.py rung1=file1.jsonl rung2=file2.jsonl ...
The first rung is treated as the reference superset for dominance checks.
"""
import json, sys

rungs = []
for arg in sys.argv[1:]:
    name, fn = arg.split('=', 1)
    s = set()
    n = 0
    for line in open(fn):
        r = json.loads(line)
        n += 1
        if r['solved']:
            s.add(r['n'])
    rungs.append((name, s, n))

ref_name, ref, _ = rungs[0]
print(f"{'rung':>14s}  solved  subset_of_{ref_name}  minus_{ref_name}")
for name, s, n in rungs:
    extra = sorted(s - ref)
    print(f"{name:>14s}  {len(s):3d}/{n}   {str(s <= ref):>5s}          {extra if extra else ''}")

union = set()
for _, s, _ in rungs:
    union |= s
print(f"\nunion of all rungs: {len(union)}")
inter = rungs[0][1]
for _, s, _ in rungs[1:]:
    inter &= s
print(f"intersection: {len(inter)}")

for i, (na, sa, _) in enumerate(rungs):
    for nb, sb, _ in rungs[i+1:]:
        if not (sb <= sa or sa <= sb):
            onlyb = sorted(sb - sa)[:4]
            onlya = sorted(sa - sb)[:4]
            print(f"non-nested pair {na}/{nb}: only-{na} {len(sa-sb)} {onlya} | only-{nb} {len(sb-sa)} {onlyb}")
