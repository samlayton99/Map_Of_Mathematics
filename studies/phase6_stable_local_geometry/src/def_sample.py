#!/usr/bin/env python3
"""BLIND regrade round -- Task 1: draw the sample (seed 20260907).

120 targets = 84 theorems (kind 0) + 36 definitions/instances (kind 1),
non-generated, stratified over target-depth bands [11-25] [26-50] [51-100]
[101+], equal counts per band within each kind group.

The candidate universe per target is the FULL U1D pool for that artifact --
every load-bearing incidence (roles 0/1/2/7) plus every definition-kind
declaration cited in any role -- with generated candidates redirected to
their nearest non-generated dot-prefix owner. No policy filter is applied:
the labels have to judge the pool, not our policies.

Writes data/blind/sample.json.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lean_source as LS                                   # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, ".."))
P5DATA = os.path.normpath(
    os.path.join(ROOT, "..", "phase5_multiscale_navigation", "data"))
MODULES_TSV = "/Users/sam/mathmap_data/all_modules.tsv"
OUT = os.path.join(ROOT, "data", "blind2")

SEED = 20260911
BANDS = [(11, 25), (26, 50), (51, 100), (101, 10 ** 9)]
BAND_LABELS = ["11-25", "26-50", "51-100", "101+"]
N_THEOREM, N_DEF = 0, 48
MIN_CAND, MAX_CAND = 3, 25
DEFINITION_KINDS = (1, 2, 5, 6, 7)   # def / inductive / opaque / quot / axiom
LOAD_ROLES = (0, 1, 2, 7)            # applied / let-value / explicit / unresolved

# SAMPLING-ONLY name filter, carried over verbatim in spirit from
# src/pilot_sample.py: compiler-generated schemes and syntax metaprograms are
# not mathematics and must not be drawn as TARGETS. It is not applied to
# candidates -- the candidate pool stays unfiltered.
AUXSEG = {"casesOn", "recOn", "brecOn", "below", "ibelow", "noConfusion",
          "noConfusionType", "rec", "recAux", "binductionOn", "ndrec"}


def is_aux(name):
    return any(s in AUXSEG or s.startswith("_") or "macroRules" in s
               or "_aux" in s or "_unexpand" in s or s.startswith("proof_")
               for s in name.split("."))


def main():
    rng = np.random.default_rng(SEED)

    nodes = np.load(os.path.join(P5DATA, "nodes.npz"))
    arts = np.load(os.path.join(P5DATA, "artifacts.npz"))
    inc = np.load(os.path.join(P5DATA, "incid.npz"))
    names = json.load(open(os.path.join(P5DATA, "names.json")))
    name_to_id = {nm: i for i, nm in enumerate(names)}

    kind, gen, depth = nodes["kind"], nodes["gen"], nodes["depth"].astype(np.int64)
    certifies = arts["certifies"].astype(np.int64)
    inc_art = inc["artifact"].astype(np.int64)
    inc_decl = inc["decl"].astype(np.int64)
    roles = inc["roles"]
    load_bearing = inc["load_bearing"]

    # ---- module table -----------------------------------------------------
    module_of = {}
    with open(MODULES_TSV) as f:
        for line in f:
            nm, _, mod = line.rstrip("\n").partition("\t")
            module_of[nm] = mod
    print(f"modules loaded: {len(module_of):,}", flush=True)

    def mathlib_ok(nm):
        m = module_of.get(nm, "")
        return m.startswith("Mathlib.") and not m.startswith("Mathlib.Tactic")

    # ---- U1D incidence mask ----------------------------------------------
    inc_target = certifies[inc_art]
    is_def_kind = np.isin(kind[inc_decl], DEFINITION_KINDS)
    u1d = (load_bearing | is_def_kind) & (inc_target != inc_decl)
    print(f"U1D incidences: {int(u1d.sum()):,} of {len(u1d):,}", flush=True)

    # ---- eligible targets -------------------------------------------------
    art_of_decl = {int(d): a for a, d in enumerate(certifies)}
    n_inc = arts["n_incidences"]

    cand_depth = depth[certifies]
    cand_kind = kind[certifies]
    cand_gen = gen[certifies]
    base = np.where((~cand_gen) & np.isin(cand_kind, (0, 1))
                    & (cand_depth >= 11) & (n_inc >= 3))[0]
    print(f"pre-filter artifacts (kind 0/1, non-gen, depth>=11, n_inc>=3): "
          f"{len(base):,}", flush=True)

    keep = []
    for a in base:
        nm = names[int(certifies[a])]
        if is_aux(nm) or not mathlib_ok(nm):
            continue
        keep.append(int(a))
    keep = np.array(keep, dtype=np.int64)
    print(f"eligible after aux-name + Mathlib-module filter: {len(keep):,}",
          flush=True)

    # ---- exclude every previously graded target (fresh sample only) -------
    prior = set()
    b1 = os.path.join(ROOT, "data", "blind", "sample.json")
    if os.path.exists(b1):
        for t in json.load(open(b1))["targets"]:
            prior.add(t["target"])
    for fn in ("graded_names.txt", "pilot48_names.txt", "map20k_names.txt"):
        p = os.path.join(ROOT, "data", fn)
        if os.path.exists(p):
            prior.update(x.strip() for x in open(p) if x.strip())
    before = len(keep)
    keep = np.array([a for a in keep
                     if names[int(certifies[a])] not in prior], dtype=np.int64)
    print(f"excluded {before - len(keep)} previously graded targets; "
          f"{len(keep):,} remain", flush=True)

    # ---- generated -> owner redirection -----------------------------------
    owner_cache = {}

    def owner(decl_id):
        """Nearest non-generated dot-prefix owner of a generated declaration."""
        if decl_id in owner_cache:
            return owner_cache[decl_id]
        nm = names[decl_id]
        res = None
        parts = nm.split(".")
        for cut in range(len(parts) - 1, 0, -1):
            pid = name_to_id.get(".".join(parts[:cut]))
            if pid is not None and not gen[pid]:
                res = int(pid)
                break
        owner_cache[decl_id] = res
        return res

    # incidence slices per artifact, U1D only
    order = np.argsort(inc_art, kind="stable")
    art_sorted = inc_art[order]
    starts = np.searchsorted(art_sorted, np.arange(len(certifies)), "left")
    ends = np.searchsorted(art_sorted, np.arange(len(certifies)), "right")

    def pool_for(a):
        idx = order[starts[a]:ends[a]]
        idx = idx[u1d[idx]]
        tgt = int(certifies[a])
        out, seen = [], set()
        for p in idx:
            d = int(inc_decl[p])
            if gen[d]:
                d = owner(d)
                if d is None or d == tgt:
                    continue
            if d == tgt or d in seen:
                continue
            seen.add(d)
            out.append(d)
        return out

    # ---- stratified draw --------------------------------------------------
    band_of = np.full(len(keep), -1, np.int64)
    kd = depth[certifies[keep]]
    for b, (lo, hi) in enumerate(BANDS):
        band_of[(kd >= lo) & (kd <= hi)] = b
    kk = kind[certifies[keep]]

    picked, taken = [], set()
    stats = {}
    for kgroup, total in ((0, N_THEOREM), (1, N_DEF)):
        if total == 0:
            continue
        per_band = total // len(BANDS)
        for b in range(len(BANDS)):
            pool = keep[(band_of == b) & (kk == kgroup)]
            rng.shuffle(pool)
            got = []
            tried = n_nocand = n_nosrc = 0
            for a in pool:
                tried += 1
                a = int(a)
                if a in taken:
                    continue
                cands = pool_for(a)
                if not (MIN_CAND <= len(cands) <= MAX_CAND):
                    n_nocand += 1
                    continue
                nm = names[int(certifies[a])]
                src = LS.lookup(nm, module_of.get(nm), want_body=True)
                # A target whose source text cannot be located exactly cannot
                # be graded blind -- the brief would have no mathematics in
                # it. Approximate matches ("translated"/"generated-from")
                # would show the rater the WRONG statement, so they are
                # rejected here too. This drops Mathlib's machine-generated
                # lemmas (@[simps], @[reassoc], unnamed @[to_additive]) from
                # the TARGET frame; see MANIFEST.md.
                if src is None or src["how"] in ("translated", "generated-from") \
                        or not src["body"]:
                    n_nosrc += 1
                    continue
                taken.add(a)
                got.append((a, cands, src))
                if len(got) == per_band:
                    break
            stats[f"kind{kgroup}_{BAND_LABELS[b]}"] = {
                "pool": int(len(pool)), "examined": tried, "drawn": len(got),
                "rejected_candidate_count": n_nocand,
                "rejected_no_source": n_nosrc}
            for a, cands, src in got:
                picked.append({
                    "artifact": a,
                    "decl": int(certifies[a]),
                    "target": names[int(certifies[a])],
                    "kind": int(kgroup),
                    "band": BAND_LABELS[b],
                    "depth": int(depth[certifies[a]]),
                    "module": module_of.get(names[int(certifies[a])]),
                    "statement_src": src["statement"],
                    "proof_src": src["body"],
                    "statement_how": src["how"],
                    "candidates": [{"decl": d, "name": names[d]} for d in cands],
                })
            print(f"  kind {kgroup} band {BAND_LABELS[b]:>7}: pool "
                  f"{len(pool):>6,}  drawn {len(got)}/{per_band}", flush=True)

    os.makedirs(OUT, exist_ok=True)
    sizes = [len(p["candidates"]) for p in picked]
    doc = {
        "seed": SEED,
        "bands": BAND_LABELS,
        "n_targets": len(picked),
        "n_theorem": sum(1 for p in picked if p["kind"] == 0),
        "n_def": sum(1 for p in picked if p["kind"] == 1),
        "n_candidates": int(sum(sizes)),
        "mean_candidates": float(np.mean(sizes)),
        "draw_stats": stats,
        "targets": picked,
    }
    json.dump(doc, open(os.path.join(OUT, "sample.json"), "w"), indent=1)
    print(f"\ndrawn {len(picked)} targets, {sum(sizes):,} candidate slots, "
          f"mean {np.mean(sizes):.1f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
