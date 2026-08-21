#!/usr/bin/env python3
"""Emit the markdown battery table for reports/SCHEME_SOCIAL_CHOICE.md."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
D = os.path.join(ROOT, "results", "social_choice")

bat = json.load(open(os.path.join(D, "battery_TEST-R.json")))

hdr = ("| scheme | P@1 | P@4 | Key@1 | core@4 | major@4 | useful@4 | mono | "
       "inv | fail P | fail R | fail G |")
sep = "|---|" + "---|" * 11
print(hdr)
print(sep)
order = sys.argv[1:] or sorted(bat)
for name in order:
    if name not in bat:
        print(f"MISSING {name}", file=sys.stderr)
        continue
    r = bat[name]
    L, G, F = r["local"], r["gradient"], r["failures"]
    print(f"| `{name}` | {L['precision@1']:.3f} | {L['precision@4']:.3f} | "
          f"{L['KeyMoveAt1']:.3f} | {L['recall_core@4']:.3f} | "
          f"{L['recall_major@4']:.3f} | {L['recall_useful@4']:.3f} | "
          f"{'y' if G['monotone'] else 'N'} | {G['inversions']} | "
          f"{F['precision_failures']} | {F['recall_failures']} | "
          f"{F['gradient_inversions']} |")
