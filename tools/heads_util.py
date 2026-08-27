#!/usr/bin/env python
"""Shared loader for the head-schema dump (bigdata/mathlib_heads.jsonl)."""
import json

from atlas import BIG

HEADS = BIG / "mathlib_heads.jsonl"

RELATIONAL_LHS1 = ("Eq", "HEq", "Ne")     # LHS is arg index 1
RELATIONAL_LHS0 = ("Iff",)                # LHS is arg index 0
RELATIONAL_LHS2 = ("LE.le", "LT.lt", "GE.ge", "GT.gt")


def load_heads(path=HEADS):
    """name -> (conclusion head, tuple of first conclusion-arg heads,
    value head or None)."""
    ch, ca, vh = {}, {}, {}
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            ch[r["n"]] = r["ch"]
            ca[r["n"]] = tuple(r.get("ca", []))
            if r["vh"] is not None:
                vh[r["n"]] = r["vh"]
    return ch, ca, vh


def refined_key(ch, ca, nm):
    """Two-level structural key: conclusion head, plus LHS head for the
    large relational classes."""
    h = ch.get(nm)
    if h is None:
        return None
    args = ca.get(nm, ())
    if h in RELATIONAL_LHS1 and len(args) >= 2:
        return (h, args[1])
    if h in RELATIONAL_LHS0 and len(args) >= 1:
        return (h, args[0])
    if h in RELATIONAL_LHS2 and len(args) >= 3:
        return (h, args[2])
    return (h,)
