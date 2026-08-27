#!/usr/bin/env python3
"""Semantic action trace analysis: compression vs raw certificate grain.

Usage: semtrace_analysis.py semtrace.jsonl replay.jsonl
"""
import json, sys, collections, statistics

sem_fn, rep_fn = sys.argv[1], sys.argv[2]

raw_nodes = {}
for line in open(rep_fn):
    r = json.loads(line)
    if 'n_nodes' in r:
        raw_nodes[r['n']] = r['n_nodes']
use_internal_raw = True

fam = collections.Counter()
leaf_heads = collections.Counter()
leaf_kinds = collections.Counter()
per = []
rw_leaves, rw_struct, rw_conts = [], [], []
errors = 0
for line in open(sem_fn):
    r = json.loads(line)
    if 'error' in r:
        errors += 1
        continue
    acts = r.get('actions', [])
    for a in acts:
        fam[a['f']] += 1
        if a['f'] == 'rewrite':
            rw_leaves.append(a.get('nleaves', 0))
            rw_struct.append(a.get('nstruct', 0))
            rw_conts.append(a.get('nconts', 0))
            for l in a.get('leaves', []):
                leaf_heads[l['h']] += 1
                leaf_kinds[(l['k'], l['g'])] += 1
    rn = r.get('n_raw') or raw_nodes.get(r['n'])
    per.append((r['n'], len(acts), rn))

print(f"theorems: {len(per)}  (extraction errors: {errors})")
n_act = [p[1] for p in per]
print(f"semantic actions/theorem: median {statistics.median(n_act)}  mean {statistics.mean(n_act):.1f}  max {max(n_act)}")
both = [(a, rn) for _, a, rn in per if rn]
if both:
    ratios = [a / rn for a, rn in both if rn > 0]
    print(f"raw proof nodes/theorem (replay): median {statistics.median([rn for _,rn in both])}  mean {statistics.mean([rn for _,rn in both]):.1f}")
    print(f"compression (actions/raw): median {statistics.median(ratios):.3f}  mean {statistics.mean(ratios):.3f}")
    print(f"total: {sum(a for a,_ in both)} actions vs {sum(rn for _,rn in both)} raw nodes = {sum(a for a,_ in both)/sum(rn for _,rn in both):.3f}")
print("\naction families:")
for f, c in fam.most_common():
    print(f"  {c:6d}  {f}")
if rw_leaves:
    print(f"\nrewrite regions: {len(rw_leaves)}")
    print(f"  facts/region: median {statistics.median(rw_leaves)}  mean {statistics.mean(rw_leaves):.1f}  max {max(rw_leaves)}")
    print(f"  internal certificate nodes absorbed/region: median {statistics.median(rw_struct)}  mean {statistics.mean(rw_struct):.1f}  max {max(rw_struct)}")
    print(f"  continuations/region: {collections.Counter(rw_conts).most_common(6)}")
    print(f"  total certificate nodes absorbed: {sum(rw_struct)}")
print("\nleaf kinds (kind, generalized):")
for k, c in leaf_kinds.most_common():
    print(f"  {c:6d}  {k}")
print("\ntop 30 fact-leaf heads:")
for h, c in leaf_heads.most_common(30):
    print(f"  {c:6d}  {h}")

per.sort(key=lambda p: -(p[1]))
print("\nlargest traces (name, actions, raw):")
for p in per[:8]:
    print(f"  {p[1]:5d} {str(p[2]):>6s}  {p[0]}")
