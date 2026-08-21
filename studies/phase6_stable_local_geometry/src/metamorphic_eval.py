#!/usr/bin/env python3
"""P2 metamorphic benchmark: is the laneD skeleton invariant under harmless
refactoring and divergent under a genuinely different proof?

The ordering under test is **laneD**, not laneD_stmt.  Every variant in a group
proves the SAME statement, so the `stmt` key (proof-introduced vocabulary
before statement vocabulary) is computed against an identical statement world
in every variant of a group: it is a group-constant relabelling of candidates
and cannot separate variants.  Including it would only add noise from the
statement-world audit (p0/P0_DEPTH_AND_STMT_WORLD.md).  laneD is therefore the
honest object under test here.

Sort keys, reimplemented from SYNTHESIS_LANED.md / src/synth_orders2.py:

    (dem, lane, -depth_value, first_occurrence)

  dem    U1D demotion: a non-Prop constant (data/def) cited ONLY through
         non-load-bearing roles enters the list demoted, never deleted.
  lane   infra(2) if the constant's occurrences are instance-slot only
         (role tier 5) or it is a generated helper; transport(1) if
         depth_stmt <= 1; move(0) otherwise.
  depth  value depth (deepest first).
  first  first occurrence index in the term walk.

Load-bearing roles {0,1,2,7}.  Generated-owner redirect: owner = longest
proper dot-prefix that is an existing non-generated declaration; owned by the
TARGET ITSELF (or by nothing) -> dropped as an internal step; owned elsewhere
-> redirected to the owner.

New declarations (the mm_* helpers authored for this benchmark) are absent
from the frozen names.json.  Treatment, stated once:
  * a name whose owner is another known declaration (Lean-generated aux such
    as `mm_g1_v1.proof_1`, or the hand-written `mm_g5_v3.aux`) is treated as
    GENERATED and goes through the owner redirect -- so a helper Lean names
    under the variant is target-owned and is dropped as internal;
  * an otherwise-unknown declaration (`mm_g5_helper`, `mm_dbl`) gets lane 0
    (or lane 2 if instance-only) and depth = 1 + max depth of the constants
    its own body cites, computed recursively from this corpus.
"""
import json, os, sys, itertools
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(P6, "data", "v7_backup")
MM = os.path.join(P6, "metamorphic")

LOAD_ROLES = (0, 1, 2, 7)
ROLE_TIER = {0: 0, 1: 0, 2: 1, 7: 2, 5: 3, 3: 4, 4: 5, 6: 6}
TOPK = 4

# ---------------------------------------------------------------- substrate
nodes = np.load(os.path.join(DATA, "nodes.npz"))
names = json.load(open(os.path.join(DATA, "names.json")))
name_id = {n: i for i, n in enumerate(names)}
gen = nodes["gen"]; depth = nodes["depth"]; pr = nodes["pr"]
depth_stmt = np.load(os.path.join(DATA, "depth_scc.npz"))["depth_stmt"]
NONGEN = {n for i, n in enumerate(names) if not gen[i]}

# ---------------------------------------------------------------- corpus
def load_forest(path):
    out, bad = {}, []
    for line in open(path):
        r = json.loads(line)
        if r.get("ok"):
            out[r["n"]] = r["occ"]
            if r.get("trunc"):
                bad.append((r["n"], "truncated"))
        else:
            bad.append((r["n"], r.get("err", "not ok")))
    return out, bad

forest, bad_rows = load_forest(os.path.join(MM, "variants_hier.jsonl"))
manifest = json.load(open(os.path.join(MM, "manifest.json")))

# local declarations authored in Variants.lean, with their Prop-ness
LOCAL_PR = {}
for line in open(os.path.join(MM, "Variants.lean")):
    s = line.strip()
    for kw, isprop in (("theorem ", True), ("def ", False), ("lemma ", True)):
        if s.startswith(kw):
            nm = s[len(kw):].split()[0].split("(")[0].split("{")[0].split(":")[0]
            if nm.startswith("mm_"):
                LOCAL_PR[nm] = isprop
LOCAL = set(LOCAL_PR)
KNOWN_NONGEN = NONGEN | LOCAL


def owner_of(c):
    """Longest proper name-prefix that is an existing non-generated decl."""
    parts = c.split(".")
    for cut in range(len(parts) - 1, 0, -1):
        p = ".".join(parts[:cut])
        if p in KNOWN_NONGEN:
            return p
    return c


# depth of a locally authored declaration: 1 + max depth of what it cites
_local_depth_memo = {}
def local_depth(c, stack=()):
    if c in _local_depth_memo:
        return _local_depth_memo[c]
    if c in stack:
        return 0
    occs = forest.get(c)
    if not occs:
        return 0
    best = 0
    for o in occs:
        d = o[0]
        i = name_id.get(d)
        if i is not None:
            best = max(best, int(depth[i]))
        elif d in LOCAL:
            best = max(best, local_depth(d, stack + (c,)))
    _local_depth_memo[c] = best + 1
    return best + 1


def is_prop(c):
    i = name_id.get(c)
    if i is not None:
        return bool(pr[i])
    if c in LOCAL_PR:
        return LOCAL_PR[c]
    return True   # unknown aux: assume Prop (no U1D demotion)


def is_generated(c):
    """gen flag from the frozen substrate; for names absent from it, a name
    that sits under another known declaration is a Lean aux / owned helper."""
    i = name_id.get(c)
    if i is not None:
        return bool(gen[i])
    if c in LOCAL:
        return owner_of(c) != c      # e.g. mm_g5_v3.aux -> owned by mm_g5_v3
    return owner_of(c) != c


def dv_ds(c):
    """(value depth, statement depth) for a constant, known or local."""
    i = name_id.get(c)
    if i is not None:
        return int(depth[i]), int(depth_stmt[i])
    if c in forest:
        return local_depth(c), 99    # unknown stmt world -> never transport
    return 0, 99


# ---------------------------------------------------------------- laneD
def laneD_features(occs, target):
    first, tier, load, anyocc = {}, {}, set(), set()
    for i, o in enumerate(occs):
        c, r = o[0], o[2]
        first.setdefault(c, i)
        tier[c] = min(tier.get(c, 9), ROLE_TIER.get(r, 9))
        anyocc.add(c)
        if r in LOAD_ROLES:
            load.add(c)
    out = {}

    def add(c, demoted):
        if is_generated(c):
            o = owner_of(c)
            if o == target or o == c:
                return                       # internal step: dropped
            dvo, dso = dv_ds(o)
            lane = 0 if dso > 1 else 1
            key, dv = o, dvo
        else:
            dvc, dsc = dv_ds(c)
            lane = 2 if tier[c] == 5 else (1 if dsc <= 1 else 0)
            key, dv = c, dvc
        if key not in out:
            out[key] = dict(dem=1 if demoted else 0, lane=lane, negd=-dv,
                            tier=tier[c], first=first[c])

    for c in load:
        add(c, False)
    for c in anyocc - load:                  # U1D demoted entry
        if not is_prop(c):
            add(c, True)
    return out


def laneD_order(F, with_tier=False):
    ks = ("dem", "lane", "negd", "tier", "first") if with_tier \
        else ("dem", "lane", "negd", "first")
    return sorted(F, key=lambda c: tuple(F[c][k] for k in ks))


# ---------------------------------------------------------------- metrics
def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a | b) else 1.0


def spearman(la, lb):
    shared = [c for c in la if c in set(lb)]
    if len(shared) < 3:
        return None
    ra = {c: i for i, c in enumerate(la)}
    rb = {c: i for i, c in enumerate(lb)}
    x = np.array([ra[c] for c in shared], float)
    y = np.array([rb[c] for c in shared], float)

    def rank(v):
        o = np.argsort(v, kind="stable")
        r = np.empty_like(o, dtype=float)
        r[o] = np.arange(len(v), dtype=float)
        return r
    x, y = rank(x), rank(y)
    if x.std() == 0 or y.std() == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def pair_metrics(la, lb, ca, cb):
    A, B = set(la[:TOPK]), set(lb[:TOPK])
    denom = max(1, min(TOPK, len(la), len(lb)))
    return {
        "top1_agree": bool(la[:1] == lb[:1]),
        # length-robust companion: several term-mode proofs cite fewer than 4
        # constants at all, which caps Jaccard mechanically.
        "top4_containment": round(len(A & B) / denom, 4),
        "top1_in_other_top4": bool(
            (la[:1] and la[0] in B) and (lb[:1] and lb[0] in A)),
        "top4_jaccard": round(jaccard(la[:TOPK], lb[:TOPK]), 4),
        "top1_a": la[0] if la else None,
        "top1_b": lb[0] if lb else None,
        "top4_a": la[:TOPK], "top4_b": lb[:TOPK],
        "spearman": (lambda s: round(s, 4) if s is not None else None)(
            spearman(la, lb)),
        "n_cand_a": len(la), "n_cand_b": len(lb),
        "raw_cite_jaccard": round(jaccard(ca, cb), 4),
    }


# ---------------------------------------------------------------- run
def main():
    if bad_rows:
        print("WARNING: bad extractor rows:", bad_rows)
    orders, orders_tier, cites = {}, {}, {}
    missing = []
    for g in manifest["groups"]:
        for v in g["variants"]:
            occs = forest.get(v)
            if occs is None:
                missing.append(v)
                continue
            F = laneD_features(occs, v)
            orders[v] = laneD_order(F)
            orders_tier[v] = laneD_order(F, with_tier=True)
            cites[v] = {o[0] for o in occs if o[2] in LOAD_ROLES}
    if missing:
        print("MISSING FROM FOREST:", missing)

    pairs = []
    for g in manifest["groups"]:
        for a, b, fam, kind in g["pairs"]:
            if a not in orders or b not in orders:
                continue
            rec = {"group": g["id"], "a": a, "b": b, "family": fam,
                   "kind": kind, "statement": g["statement"]}
            rec.update(pair_metrics(orders[a], orders[b], cites[a], cites[b]))
            rec["top4_jaccard_tierkey"] = round(
                jaccard(orders_tier[a][:TOPK], orders_tier[b][:TOPK]), 4)
            pairs.append(rec)

    def agg(rows):
        if not rows:
            return None
        sp = [r["spearman"] for r in rows if r["spearman"] is not None]
        return {
            "n_pairs": len(rows),
            "mean_top4_jaccard": round(float(np.mean([r["top4_jaccard"] for r in rows])), 4),
            "mean_top4_containment": round(float(np.mean([r["top4_containment"] for r in rows])), 4),
            "top1_agreement": round(float(np.mean([r["top1_agree"] for r in rows])), 4),
            "top1_mutual_in_top4": round(float(np.mean([r["top1_in_other_top4"] for r in rows])), 4),
            "mean_spearman": round(float(np.mean(sp)), 4) if sp else None,
            "n_spearman": len(sp),
            "mean_raw_cite_jaccard": round(float(np.mean([r["raw_cite_jaccard"] for r in rows])), 4),
            "mean_top4_jaccard_tierkey": round(float(np.mean([r["top4_jaccard_tierkey"] for r in rows])), 4),
        }

    harmless = [r for r in pairs if r["kind"] == "harmless"]
    control = [r for r in pairs if r["kind"] == "control"]
    by_family = {}
    for fam in sorted({r["family"] for r in harmless}):
        rows = [r for r in harmless if r["family"] == fam]
        by_family[fam] = agg(rows)
        by_family[fam]["pass_vs_control"] = bool(
            by_family[fam]["mean_top4_jaccard"] > agg(control)["mean_top4_jaccard"])

    worst = sorted(harmless, key=lambda r: (r["top4_jaccard"], r["top1_agree"]))[:8]
    best_control = sorted(control, key=lambda r: -r["top4_jaccard"])[:5]

    out = {
        "ordering_under_test": "laneD = (dem, lane, -depth_value, first_occurrence)",
        "note_on_stmt_key": ("laneD_stmt is NOT used: variants of a group share "
                             "their statement, so the stmt key is constant within "
                             "a group and cannot separate variants."),
        "n_declarations": len(orders),
        "extractor_bad_rows": bad_rows,
        "aggregate": {"harmless": agg(harmless), "control": agg(control)},
        "by_family": by_family,
        "worst_harmless_pairs": worst,
        "most_invariant_control_pairs": best_control,
        "pairs": pairs,
        "orders": {k: v[:8] for k, v in sorted(orders.items())},
    }
    path = os.path.join(P6, "data", "metamorphic_results.json")
    json.dump(out, open(path, "w"), indent=1)

    ah, ac = agg(harmless), agg(control)
    print(f"declarations {len(orders)}  harmless pairs {ah['n_pairs']}  "
          f"control pairs {ac['n_pairs']}")
    hdr = f"{'family':26} {'n':>3} {'top4J':>6} {'top4C':>6} {'top1':>6} {'rho':>7} {'rawJ':>6}"
    print(hdr)

    def row(lbl, a):
        rho = "    n/a" if a["mean_spearman"] is None else f"{a['mean_spearman']:7.3f}"
        print(f"{lbl:26} {a['n_pairs']:3d} {a['mean_top4_jaccard']:6.3f} "
              f"{a['mean_top4_containment']:6.3f} {a['top1_agreement']:6.3f} "
              f"{rho} {a['mean_raw_cite_jaccard']:6.3f}")
    for fam, a in by_family.items():
        row(fam, a)
    row("HARMLESS (all)", ah)
    row("CONTROL (all)", ac)
    print("\nworst harmless pairs:")
    for r in worst:
        print(f"  {r['a']} vs {r['b']} [{r['family']}] J={r['top4_jaccard']:.2f}")
        print(f"     A: {r['top4_a']}")
        print(f"     B: {r['top4_b']}")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
