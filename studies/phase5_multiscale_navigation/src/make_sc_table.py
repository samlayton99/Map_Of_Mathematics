#!/usr/bin/env python3
"""Emit the markdown battery table for reports/SCHEME_SOCIAL_CHOICE.md."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
D = os.path.join(ROOT, "results", "social_choice")

bat = json.load(open(os.path.join(D, "battery_TEST-R.json")))
nav = {}
p = os.path.join(D, "navigability_full.json")
if os.path.exists(p):
    nav = json.load(open(p))

hdr = ("| scheme | P@1 | P@4 | Key@1 | core@4 | major@4 | useful@4 | mono | "
       "inv | fail P | fail R | fail G | junk@4 | giant | retained |")
sep = "|---|" + "---|" * 14
print(hdr)
print(sep)
order = sys.argv[1:] or sorted(bat)
for name in order:
    if name not in bat:
        print(f"MISSING {name}", file=sys.stderr)
        continue
    r = bat[name]
    L, G, F = r["local"], r["gradient"], r["failures"]
    ALIAS = {
        "HYB_copeland_first__role5w_x_logdepth_x_rarity": "HYB_copeland_first6",
        "HYB_condorcet_first__role5w_x_logdepth_x_rarity":
            "HYB_condorcet_first6",
        "HYB_borda_first__role5w_x_logdepth_x_rarity": "HYB_borda_first6",
        "condorcet_first_anchor6": "HYB_condorcet_first6",
        "borda6_veto_below_t2": "veto_below_t26",
        "borda6_veto_below_t3": "veto_below_t36",
        "role_lex_then_borda6": "role_lex6",
        "borda6_condorcet_first": "black_condorcet6",
    }
    n = nav.get(name) or nav.get(ALIAS.get(name, "")) or {}
    if n:
        nv = (f" {n['junk_edge_share']:.3f} | "
              f"{n['all_edges']['giant_fraction']:.3f} | "
              f"{n['giant_retained_without_junk']:.3f} |")
    else:
        nv = " - | - | - |"
    print(f"| `{name}` | {L['precision@1']:.3f} | {L['precision@4']:.3f} | "
          f"{L['KeyMoveAt1']:.3f} | {L['recall_core@4']:.3f} | "
          f"{L['recall_major@4']:.3f} | {L['recall_useful@4']:.3f} | "
          f"{'y' if G['monotone'] else 'N'} | {G['inversions']} | "
          f"{F['precision_failures']} | {F['recall_failures']} | "
          f"{F['gradient_inversions']} |" + nv)
