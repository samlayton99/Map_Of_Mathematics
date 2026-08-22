#!/usr/bin/env python3
"""Score the construction against the BLIND labels (first uncontaminated
instrument; first-ever definition targets). Run after grades_RA/RB/RC.json
exist under data/blind/.

Reports:
1. Rater agreement: rater-vs-rest F1 on useful (>=3) — the new
   instrument's own resolution, to compare with the old 0.856.
2. laneD_stmt ranking: KeyMove@1, R@4, R@8 — overall, theorems-only,
   DEFINITIONS-only (never measured before).
3. Inclusion policies (gap_all, gap|movelane, top-4) on blind labels.
4. Depth-visibility check: is grade-vs-depth correlation LOWER than in
   the contaminated round? (Raters could not see depth here.)
5. Statement-concept separator on clean labels: among U1D stmt-defs,
   does (stmt-nesting<=1 & rel-depth>=1/2) separate useful from junk
   better than under noisy labels (was prec 0.53)?
"""
import json, glob, os, sys
from collections import defaultdict
import numpy as np, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec2 = importlib.util.spec_from_file_location("hv", os.path.join(HERE, "hier_views.py"))
hv = importlib.util.module_from_spec(spec2); sys.argv = ["hv"]; spec2.loader.exec_module(hv)
P6 = os.path.normpath(os.path.join(HERE, ".."))
B = os.path.join(P6, "data", "blind")
LOAD = (0, 1, 2, 7)

briefs = json.load(open(os.path.join(B, "briefs.json")))
keymap = json.load(open(os.path.join(B, "keymap.json")))
forest = hv.load_forest(os.path.join(B, "targets_hier.jsonl"))
stmt_forest = hv.load_forest(os.path.join(B, "targets_stmt_hier.jsonl"))

def load_grades():
    per = defaultdict(lambda: defaultdict(dict))   # tid -> n -> rater -> g
    for rf in sorted(glob.glob(os.path.join(B, "grades_R*.json"))):
        rid = rf[-6]
        d = json.load(open(rf))
        for batch, tgts in d.items():
            for tid, cs in tgts.items():
                for n, g in cs.items():
                    if g is not None:
                        per[tid][n][rid] = int(g)
    return per

def feats(occs, target, stmtnames):
    first, tier, load, anyocc = {}, {}, set(), {}
    for i, o in enumerate(occs):
        c, r = o[0], o[2]
        first.setdefault(c, i)
        tier[c] = min(tier.get(c, 9), hv.ROLE_TIER.get(r, 9)); anyocc[c] = True
        if r in LOAD: load.add(c)
    out = {}
    def add(c, dem):
        i = hv.name_id.get(c)
        if i is not None and hv.gen[i]:
            o = hv.owner_of(c)
            if o == target or o == c: return
            io = hv.name_id.get(o)
            ds = int(hv.depth_stmt[io]) if io is not None else 9
            dv = int(hv.depth[io]) if io is not None else 0
            key = o; inst = 0
        else:
            ds = int(hv.depth_stmt[i]) if i is not None else 9
            dv = int(hv.depth[i]) if i is not None else 0
            key = c; inst = 1 if tier[c] == 5 else 0
        if key not in out:
            lane = 2 if inst else (1 if ds <= 1 else 0)
            out[key] = dict(dem=1 if dem else 0, lane=lane,
                            stmt=1 if key in stmtnames else 0, d=dv, first=first[c])
    for c in load: add(c, False)
    for c in anyocc:
        if c in load: continue
        i = hv.name_id.get(c)
        if i is not None and not hv.nodes["pr"][i]: add(c, True)
    return out

def gap_cut_thresh(pool, F):
    if not pool: return None
    ds = sorted({F[c]["d"] for c in pool}, reverse=True)
    if len(ds) == 1: return ds[0]
    gaps = [(ds[i] - ds[i + 1], i) for i in range(len(ds) - 1)]
    g, i = max(gaps)
    return ds[i] if g > 0 else ds[-1]

def main():
    per = load_grades()
    # rater agreement
    f1s = []
    for tid, cs in per.items():
        rids = sorted({r for n in cs for r in cs[n]})
        if len(rids) < 3: continue
        for r in rids:
            mine = {n for n, gs in cs.items() if gs.get(r, 0) >= 3}
            rest = {n for n, gs in cs.items()
                    if [v for k, v in gs.items() if k != r]
                    and np.median([v for k, v in gs.items() if k != r]) >= 3}
            if not mine and not rest: continue
            tp = len(mine & rest)
            pr = tp / len(mine) if mine else (1.0 if not rest else 0.0)
            rc = tp / len(rest) if rest else (1.0 if not mine else 0.0)
            f1s.append(2 * pr * rc / max(pr + rc, 1e-9))
    print(f"1. BLIND rater-vs-rest F1: {np.mean(f1s):.4f} (n={len(f1s)}; old contaminated round: 0.856)")

    # per-target structures
    S = defaultdict(lambda: defaultdict(list))
    sep_u, sep_j = [], []
    depth_grade = []
    for b in briefs:
        tid = b["id"]; tgt = b["target"]
        kindrow = next((k for k in keymap if isinstance(k, dict) and k.get("id") == tid), None)
        kind = b.get("kind", kindrow.get("kind") if kindrow else 0)
        cmap = {str(c["n"]): c["name"] for c in b["candidates"]}
        cs = per.get(tid, {})
        gmed = {cmap[n]: float(np.median(list(gs.values())))
                for n, gs in cs.items() if n in cmap and len(gs) >= 2}
        if not gmed: continue
        useful = {c for c, g in gmed.items() if g >= 3}
        keys = {c for c, g in gmed.items() if g >= 4}
        occs = forest.get(tgt)
        if not occs: continue
        stmtnames = {o[0] for o in stmt_forest.get(tgt, [])}
        F = feats(occs, tgt, stmtnames)
        if not F: continue
        # depth-grade correlation material
        for c, g in gmed.items():
            if c in F: depth_grade.append((F[c]["d"], g))
        grp = "thm" if kind == 0 else "def"
        lst = sorted(F, key=lambda c: (F[c]["dem"], F[c]["lane"], F[c]["stmt"], -F[c]["d"], F[c]["first"]))
        if useful:
            for gname in ("all", grp):
                if keys:
                    S[gname]["km"].append(1.0 if lst[0] in keys else 0.0)
                S[gname]["r4"].append(sum(1 for u in useful if u in lst[:4]) / len(useful))
                S[gname]["r8"].append(sum(1 for u in useful if u in lst[:8]) / len(useful))
            pool = [c for c in F if F[c]["dem"] == 0]
            t = gap_cut_thresh(pool, F)
            gap = {c for c in pool if t is not None and F[c]["d"] >= t}
            el0 = {c for c in pool if F[c]["lane"] == 0 and F[c]["stmt"] == 0}
            for pname, inc in (("gap", gap), ("gap|el0", gap | el0), ("top4", set(lst[:4]))):
                gi = [c for c in inc if c in gmed]
                pr = np.mean([gmed[c] >= 3 for c in gi]) if gi else 0.0
                jr = np.mean([gmed[c] <= 1 for c in gi]) if gi else 0.0
                rc = sum(1 for u in useful if u in inc) / len(useful)
                S["pol_" + pname]["prec"].append(pr)
                S["pol_" + pname]["junk"].append(jr)
                S["pol_" + pname]["rec"].append(rc)
        # statement-concept separator on clean labels
        dt = max(int(hv.depth[hv.name_id[tgt]]) if tgt in hv.name_id else 1, 1)
        sn = {}
        for o in stmt_forest.get(tgt, []):
            sn[o[0]] = min(sn.get(o[0], 99), o[4] + (50 if o[2] == 4 else 0))
        for c in F:
            if F[c]["dem"] == 1 and F[c]["stmt"] == 1 and c in gmed:
                hit = sn.get(c, 99) <= 1 and F[c]["d"] / dt >= 0.5
                if gmed[c] >= 3: sep_u.append(hit)
                elif gmed[c] <= 1: sep_j.append(hit)
    print("\n2-3. ranking and policies on BLIND labels:")
    for g in ("all", "thm", "def"):
        a = S[g]
        if a["r4"]:
            km = np.mean(a["km"]) if a["km"] else float("nan")
            print(f"   laneD_stmt [{g:3}]: KM@1 {km:.3f}  R@4 {np.mean(a['r4']):.3f}  "
                  f"R@8 {np.mean(a['r8']):.3f}  (n={len(a['r4'])})")
    for p in ("pol_gap", "pol_gap|el0", "pol_top4"):
        a = S[p]
        if a["prec"]:
            print(f"   {p[4:]:8}: prec {np.mean(a['prec']):.3f}  junk {np.mean(a['junk']):.3f}  "
                  f"rec {np.mean(a['rec']):.3f}")
    if depth_grade:
        from scipy.stats import spearmanr
        d, g = zip(*depth_grade)
        print(f"\n4. depth-grade Spearman on blind labels: {spearmanr(d, g).statistic:.3f} "
              f"(contaminated round had depth visible)")
    if sep_u or sep_j:
        tp = sum(sep_u); fp = sum(sep_j)
        print(f"\n5. stmt-concept separator (nesting<=1 & rel>=1/2) on clean labels: "
              f"catches {tp}/{len(sep_u)} useful, {fp}/{len(sep_j)} junk "
              f"(prec-ish {tp/max(tp+fp,1):.2f}; was 0.53 on noisy labels)")

if __name__ == "__main__":
    main()
