#!/usr/bin/env python3
"""Direct test of the owner's depth hypothesis (PRE_REGISTRATION_V8ALT Q2.3).

Hypothesis as stated: "what counts as acceptable glue or a meaningful move
changes with mathematical depth. Glue in first place would badly hurt
precision for Fermat's Last Theorem, but similar logical machinery may
legitimately be the mathematical content of a theorem near the foundations."

The P@1-by-band table tests this only indirectly. This is the direct test:
look at what HUMANS actually wrote, and ask whether the things they wrote are
themselves glue more often at shallow depth.

  For each proof with elaborator provenance, take the citations the human
  wrote in the proof body. Classify each by our own categories (logic-only /
  machinery / definition / theorem). Report the composition by the depth of
  the theorem being proved.

If the hypothesis holds, the human-written citations of shallow theorems
should be substantially more glue-heavy than those of deep theorems. If the
composition is flat, the hypothesis is falsified and precision should not be
excused at shallow depth.
"""
import json, os, glob
import numpy as np
from collections import defaultdict, Counter

SCRATCH = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
PROV = os.path.join(SCRATCH, "prov")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
BANDS = [(0, 10), (10, 25), (25, 50), (50, 75), (75, 125), (125, 350)]


def main():
    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    nodes = np.load(os.path.join(DATA, "nodes.npz"))
    v8 = np.load(os.path.join(DATA, "v8_mask.npz"))
    names = json.load(open(os.path.join(DATA, "names.json")))
    idx = {nm: i for i, nm in enumerate(names)}

    a_col = inc["artifact"].astype(np.int64)
    d_col = inc["decl"].astype(np.int64)
    lb = inc["load_bearing"]
    in_sw = inc["in_stmt_world"]
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"].astype(np.float64)
    kind = nodes["kind"]
    is_claim = v8["decl_is_claim"]
    logic_only = v8["decl_logic_only"]

    art_of = {d: a for a, d in enumerate(certifies)}
    bi = np.where(lb & (certifies[a_col] != d_col))[0]
    by_art = defaultdict(list)
    for p in bi:
        by_art[a_col[p]].append(p)

    prov = {}
    for f in glob.glob(os.path.join(PROV, "*.json")):
        for e in json.load(open(f))["decls"]:
            if e.get("refs"):
                prov[e["name"]] = set(e["refs"])

    def klass(d):
        if kind[d] in (1, 2, 5, 6, 7):
            return "definition/construction"
        if logic_only[d]:
            return "glue (logic-only)"
        if is_claim[d]:
            return "theorem"
        return "other (ctor/recursor)"

    comp = {b: Counter() for b in BANDS}
    ntheorems = {b: 0 for b in BANDS}
    for nm, refs in prov.items():
        di = idx.get(nm)
        if di is None or di not in art_of:
            continue
        pl = by_art.get(art_of[di])
        if not pl:
            continue
        stmt = {names[d_col[p]] for p in pl if in_sw[p]}
        gt = [c for c in refs if c != nm and c not in stmt and c in idx]
        if not gt:
            continue
        band = next((b for b in BANDS if b[0] <= depth[di] < b[1]), None)
        if band is None:
            continue
        ntheorems[band] += 1
        for c in gt:
            comp[band][klass(idx[c])] += 1

    print("=== What humans actually WRITE, by depth of the theorem proved ===",
          flush=True)
    print("(composition of human-written proof-body citations)\n", flush=True)
    cats = ["theorem", "definition/construction", "glue (logic-only)",
            "other (ctor/recursor)"]
    hdr = f"{'depth band':<12} {'proofs':>7} {'citations':>10} " + \
          "".join(c[:22].rjust(24) for c in cats)
    print(hdr, flush=True)
    rows = []
    for b in BANDS:
        tot = sum(comp[b].values())
        if tot == 0:
            continue
        cells = "".join(f"{100*comp[b][c]/tot:>22.1f}% " for c in cats)
        print(f"{b[0]}-{b[1]:<8} {ntheorems[b]:>7,} {tot:>10,} {cells}", flush=True)
        rows.append({"band": f"{b[0]}-{b[1]}", "proofs": ntheorems[b],
                     "citations": tot,
                     **{c: round(100 * comp[b][c] / tot, 2) for c in cats}})

    glue = [r["glue (logic-only)"] for r in rows]
    print(f"\nglue share of human-written citations: shallow={glue[0]:.1f}% "
          f"deep={glue[-1]:.1f}%   spread={max(glue)-min(glue):.1f} points",
          flush=True)
    if glue[0] > glue[-1] + 5:
        verdict = ("SUPPORTED: humans genuinely write more glue at shallow depth, "
                   "so glue at rank 1 is more often correct there")
    elif abs(glue[0] - glue[-1]) <= 5:
        verdict = ("NOT SUPPORTED: the glue share of what humans write is "
                   "essentially flat across depth, so shallow precision cannot "
                   "be excused on these grounds")
    else:
        verdict = ("REVERSED: humans write MORE glue at deep than shallow depth")
    print(f"VERDICT ON THE REGISTERED HYPOTHESIS: {verdict}", flush=True)

    with open(os.path.join(DATA, "glue_by_depth.json"), "w") as f:
        json.dump({"rows": rows, "verdict": verdict}, f, indent=1)
    print("\nwritten data/glue_by_depth.json", flush=True)


if __name__ == "__main__":
    main()
