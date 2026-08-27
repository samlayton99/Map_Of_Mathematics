#!/usr/bin/env python3
"""Phase 4: extraction-independent recall via the elaboration-provenance
sidecar.

Ground truth per declaration = the global constants the HUMAN SOURCE
referenced, as resolved by Lean's elaborator (InfoTree TermInfo idents),
restricted to Prop-valued constants. This ground truth does NOT pass through
our extraction, so it can see references the kernel-term extraction missed
entirely — the measurement the old recall benchmark was structurally unable
to make (judge charge 3).

Loss taxonomy per missed reference:
  not-in-term      the constant does not occur in the kernel proof term at
                   all (erased by elaboration: simp-closure, defeq, etc.)
  background-slot  occurs in the term but only in non-load-bearing roles
  not-prop-flag    occurs load-bearing but pr=false in the dump
"""
import json, os, subprocess, sys
import numpy as np

SCRATCH2 = "/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad"
DUMP4 = os.path.join(SCRATCH2, "mathlib_deps4.jsonl")
PROVDIR = os.path.join(SCRATCH2, "prov")
ML_PKG = "/Users/sam/my-repos/research/Map_Of_Mathematics/corpusenv/mathlib"
BIN = "/Users/sam/my-repos/research/Map_Of_Mathematics/mathrecord/.lake/build/bin/mathrecord"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
DEV_SEED = 20260819
HOLDOUT_SEED = 20260820
NSAMP = 2400
NFILES = 40
LOAD_ROLES = (0, 1, 2, 7)


def main():
    # light dump load: names, kinds, classes, pr, v, vo
    idx, names = {}, []
    kinds, classes, pr, deps_v, vo = [], [], [], [], []
    def nid(nm):
        i = idx.get(nm)
        if i is None:
            i = len(names); idx[nm] = i; names.append(nm)
            kinds.append(""); classes.append(()); pr.append(False)
            deps_v.append(()); vo.append(())
        return i
    with open(DUMP4) as f:
        for line in f:
            r = json.loads(line)
            i = nid(r["n"])
            kinds[i] = r["k"]; classes[i] = tuple(r["c"]); pr[i] = bool(r.get("pr", False))
            deps_v[i] = tuple(nid(d) for d in r["v"])
            vo[i] = tuple(tuple(int(x) for x in row) for row in r.get("vo", ()))
    n = len(names)
    print(f"constants: {n}", flush=True)
    thm = np.array([k == "theorem" for k in kinds])
    has_class = np.array([len(c) > 0 for c in classes])
    pool = np.where(thm & ~has_class & np.array([len(v) > 0 for v in deps_v]))[0]
    dev = set(np.random.default_rng(DEV_SEED).choice(pool, size=NSAMP, replace=False).tolist())
    pool2 = np.array([i for i in pool if i not in dev])
    holdout = set(np.random.default_rng(HOLDOUT_SEED).choice(pool2, size=NSAMP, replace=False).tolist())

    sys.path.insert(0, HERE)
    from moves import build_source_index
    print("building source index", flush=True)
    sidx = build_source_index()
    # pick files that contain holdout decls
    filecount = {}
    for r in holdout:
        short = names[r].split(".")[-1]
        for p, _ in sidx.get(short, [])[:1]:
            filecount[p] = filecount.get(p, 0) + 1
    files = [p for p, _ in sorted(filecount.items(), key=lambda kv: -kv[1])[:NFILES]]
    os.makedirs(PROVDIR, exist_ok=True)
    prov_decls = {}
    for k, p in enumerate(files):
        rel = os.path.relpath(p, ML_PKG)
        out = os.path.join(PROVDIR, f"prov_{k}.json")
        if not os.path.exists(out):
            res = subprocess.run(["lake", "env", BIN, "provenance", rel, out],
                                 cwd=ML_PKG, capture_output=True, text=True, timeout=600)
            if res.returncode != 0:
                print(f"  provenance failed for {rel}: {res.stderr[-200:]}", flush=True)
                continue
        try:
            o = json.load(open(out))
        except Exception:
            continue
        for d in o["decls"]:
            prov_decls[d["name"]] = d["refs"]
        if (k + 1) % 10 == 0:
            print(f"  {k+1}/{len(files)} files", flush=True)
    print(f"provenance decls: {len(prov_decls)}", flush=True)

    def loadbearing(r):
        out = set()
        for d, row in zip(deps_v[r], vo[r]):
            if d != r and any(row[k] > 0 for k in LOAD_ROLES):
                out.add(d)
        return out

    recalls, losses = [], {"not-in-term": 0, "background-slot": 0, "not-prop-flag": 0}
    loss_examples = []
    evaluated = 0
    extraction_misses_seen = 0
    for r in holdout:
        nm = names[r]
        refs = prov_decls.get(nm)
        if not refs:
            continue
        gt = set()
        for cn in refs:
            c = idx.get(cn)
            if c is None or c == r or not pr[c]:
                continue
            if kinds[c] in ("constructor", "recursor"):
                continue
            gt.add(c)
        if len(gt) < 2:
            continue
        evaluated += 1
        moves = {c for c in loadbearing(r)
                 if pr[c] and kinds[c] not in ("constructor", "recursor")}
        got = gt & moves
        recalls.append(len(got) / len(gt))
        vset = set(deps_v[r])
        for c in gt - moves:
            if c not in vset:
                why = "not-in-term"
                extraction_misses_seen += 1
            elif c not in loadbearing(r):
                why = "background-slot"
            else:
                why = "not-prop-flag"
            losses[why] += 1
            if len(loss_examples) < 25:
                loss_examples.append({"decl": nm, "lost": names[c], "why": why})
    out = {
        "n_files": len(files), "n_prov_decls": len(prov_decls),
        "n_evaluated": evaluated,
        "median_recall": round(float(np.median(recalls)), 3) if recalls else None,
        "mean_recall": round(float(np.mean(recalls)), 3) if recalls else None,
        "frac_perfect": round(float(np.mean([x == 1 for x in recalls])), 3) if recalls else None,
        "loss_taxonomy": losses,
        "extraction_misses_(refs_absent_from_kernel_term)": extraction_misses_seen,
        "loss_examples": loss_examples,
        "note": "ground truth = elaborator-resolved source identifiers "
                "(Prop-valued), independent of our extraction"}
    with open(os.path.join(DATA, "phase4_provenance_recall.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if k != "loss_examples"}, indent=1))


if __name__ == "__main__":
    main()
