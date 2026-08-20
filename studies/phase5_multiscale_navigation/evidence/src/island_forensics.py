#!/usr/bin/env python3
"""Are the islands a finding about mathematics, or an artifact of filtering?

Two graphs are examined:

  A. the FULL load-bearing graph (every proof step, no content filter). It has
     569 components. If mathematics genuinely has islands, this is where they
     live -- nothing has been filtered away, so a component here is a region
     that truly shares no proof step with the rest of the library.

  B. the top-1 graph under the frozen V8 ranking, which has 25,230 components.
     These may be an artifact of keeping one edge per proof.

For each component we ask what it IS: how big, how deep, whether it is
machine-generated, and whether it is a coherent mathematical area or a random
mix. Namespaces are used ONLY as descriptive labels here -- this is analysis,
not the measure.
"""
import json, os
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))


def ns(nm, k=2):
    p = nm.split(".")
    if p[0] == "_private":
        p = p[3:] if len(p) > 3 else p
    return ".".join(p[:k]) if len(p) >= k else p[0]


def describe(label, comp_ids, lab, touched, names, depth, gen, kind, top=18):
    print(f"\n{'='*74}\n{label}\n{'='*74}", flush=True)
    sizes = np.bincount(lab[touched])
    live = np.where(sizes > 0)[0]
    ls = sizes[live]
    order = live[np.argsort(-ls)]
    print(f"  components: {len(live):,}   sizes: max={ls.max():,} "
          f"p50={np.percentile(ls,50):.0f} min={ls.min()}", flush=True)
    print(f"  size<=2: {int((ls<=2).sum()):,} ({100*(ls<=2).mean():.1f}%)   "
          f"size>=100: {int((ls>=100).sum()):,}", flush=True)

    node_of = {}
    for c in order[:top]:
        node_of[c] = touched[lab[touched] == c]

    print(f"\n  --- the {top} largest components ---", flush=True)
    rows = []
    for rank, c in enumerate(order[:top]):
        nd = node_of[c]
        d = depth[nd]
        nsc = Counter(ns(names[i]) for i in nd)
        dom, domn = nsc.most_common(1)[0]
        purity = domn / len(nd)
        genf = float(gen[nd].mean())
        thmf = float((kind[nd] == 0).mean())
        rows.append({"rank": rank, "size": int(len(nd)),
                     "dominant_namespace": dom, "namespace_purity": round(purity, 3),
                     "median_depth": int(np.median(d)),
                     "machine_generated_frac": round(genf, 3),
                     "theorem_frac": round(thmf, 3),
                     "sample": [names[i] for i in nd[:4]]})
        print(f"  #{rank:<3} n={len(nd):>7,}  depth~{int(np.median(d)):>3}  "
              f"gen={genf:>5.1%}  {dom[:34]:<36} purity={purity:>5.1%}", flush=True)
        if len(nd) <= 6 or rank >= top - 6:
            for i in nd[:4]:
                print(f"          {names[i][:88]}", flush=True)
    return rows, ls, order, lab


def main():
    inc = np.load(os.path.join(DATA, "incid.npz"))
    arts = np.load(os.path.join(DATA, "artifacts.npz"))
    nodes = np.load(os.path.join(DATA, "nodes.npz"))
    v8 = np.load(os.path.join(DATA, "v8_mask.npz"))
    names = json.load(open(os.path.join(DATA, "names.json")))

    a_col = inc["artifact"].astype(np.int64)
    d_col = inc["decl"].astype(np.int64)
    lb = inc["load_bearing"]
    d_cite = inc["d_cite"].astype(np.int32)
    certifies = arts["certifies"].astype(np.int64)
    depth = nodes["depth"].astype(np.int32)
    gen = nodes["gen"]; kind = nodes["kind"]
    n = len(depth)
    tgt = certifies[a_col]
    is_claim = v8["decl_is_claim"]
    logic_only = v8["decl_logic_only"]
    machinery = v8["machinery"]

    out = {}

    # ---------- A. the FULL load-bearing graph ----------
    mA = lb & (tgt != d_col)
    gA = sp.coo_matrix((np.ones(int(mA.sum()), dtype=np.int8),
                        (tgt[mA], d_col[mA])), shape=(n, n))
    ncA, labA = connected_components(gA, directed=False)
    touchedA = np.unique(np.concatenate([tgt[mA], d_col[mA]]))
    rowsA, lsA, orderA, _ = describe(
        "A. FULL load-bearing graph -- nothing filtered. Are there genuine islands?",
        None, labA, touchedA, names, depth, gen, kind)
    out["full_graph"] = {"components": int(len(lsA)),
                         "largest": rowsA}

    # what fraction of the non-giant mass is machine-generated?
    giantA = orderA[0]
    nonG = touchedA[labA[touchedA] != giantA]
    print(f"\n  outside the giant component: {len(nonG):,} declarations, "
          f"{100*gen[nonG].mean():.1f}% machine-generated, "
          f"median depth {int(np.median(depth[nonG]))}", flush=True)
    nsn = Counter(ns(names[i]) for i in nonG)
    print("  their areas:", flush=True)
    for a, c in nsn.most_common(12):
        print(f"    {a[:40]:<42} {c:>6,}", flush=True)
    out["full_graph"]["outside_giant"] = {
        "n": int(len(nonG)), "machine_generated_frac": round(float(gen[nonG].mean()), 3),
        "median_depth": int(np.median(depth[nonG])),
        "areas": [{"area": a, "n": int(c)} for a, c in nsn.most_common(25)]}

    # ---------- B. top-1 under the frozen V8 ranking ----------
    P4 = lb & is_claim[d_col] & ~logic_only[d_col] & ~machinery
    idx4 = np.where(P4)[0]
    ordk = np.lexsort((-d_cite[idx4], a_col[idx4]))
    idx4s = idx4[ordk]
    ne = np.empty(len(idx4s), dtype=bool)
    ne[0] = True
    ne[1:] = a_col[idx4s][1:] != a_col[idx4s][:-1]
    top1 = idx4s[ne]
    gB = sp.coo_matrix((np.ones(len(top1), dtype=np.int8),
                        (tgt[top1], d_col[top1])), shape=(n, n))
    ncB, labB = connected_components(gB, directed=False)
    touchedB = np.unique(np.concatenate([tgt[top1], d_col[top1]]))
    rowsB, lsB, orderB, _ = describe(
        "B. TOP-1 under the frozen V8 ranking -- 25,230 components. Artifact or finding?",
        None, labB, touchedB, names, depth, gen, kind)
    out["top1_graph"] = {"components": int(len(lsB)), "largest": rowsB}

    # coherence: is a typical component a single mathematical area?
    print("\n  --- coherence of components (are they real areas?) ---", flush=True)
    rng = np.random.default_rng(3)
    mid = orderB[(lsB[np.argsort(-lsB)] >= 5)]
    mid = [c for c in orderB if (labB[touchedB] == c).sum() >= 5]
    samp = rng.choice(mid, size=min(400, len(mid)), replace=False)
    purities, genfracs = [], []
    for c in samp:
        nd = touchedB[labB[touchedB] == c]
        nsc = Counter(ns(names[i]) for i in nd)
        purities.append(nsc.most_common(1)[0][1] / len(nd))
        genfracs.append(float(gen[nd].mean()))
    purities = np.array(purities); genfracs = np.array(genfracs)
    print(f"  {len(samp)} components of size>=5: namespace purity "
          f"mean={purities.mean():.1%} median={np.median(purities):.1%}", flush=True)
    print(f"    single-area components (purity>=80%): "
          f"{100*(purities>=0.8).mean():.1f}%", flush=True)
    print(f"    machine-generated fraction: mean={genfracs.mean():.1%} "
          f"median={np.median(genfracs):.1%}", flush=True)
    print(f"    components that are >=80% machine-generated: "
          f"{100*(genfracs>=0.8).mean():.1f}%", flush=True)
    out["top1_graph"]["coherence"] = {
        "n_sampled": int(len(samp)),
        "namespace_purity_mean": round(float(purities.mean()), 3),
        "single_area_frac": round(float((purities >= 0.8).mean()), 3),
        "machine_generated_mean": round(float(genfracs.mean()), 3),
        "mostly_generated_frac": round(float((genfracs >= 0.8).mean()), 3)}

    # small components: what are they?
    print("\n  --- a sample of SMALL components (size 2-4) ---", flush=True)
    small = [c for c in orderB if 2 <= (labB[touchedB] == c).sum() <= 4]
    for c in rng.choice(small, size=min(12, len(small)), replace=False):
        nd = touchedB[labB[touchedB] == c]
        print(f"    [{len(nd)}] " + " | ".join(names[i][:44] for i in nd[:3]),
              flush=True)

    with open(os.path.join(DATA, "island_forensics.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten data/island_forensics.json", flush=True)


if __name__ == "__main__":
    main()
