#!/usr/bin/env python3
"""Build every JSON the dashboard reads.

THE CENTRAL DISCIPLINE OF THIS FILE, and the reason it is structured the way
it is:

  A number is either a property of the RANKING or a property of the
  CURRENTLY DISPLAYED SLICE, and the two live in different objects that are
  never merged.

  * `experiments[universe].ranking_quality` -- semantic scorecard, source
    agreement, rank composition, ties. Computed on the FULL ranked universe.
    These do NOT move when the viewer changes lane or k. The universe is part
    of the experiment's identity because changing it changes the candidate
    set and therefore genuinely re-ranks.

  * `experiments[universe].views["<lane>|<k>"]` -- size, composition, key-move
    retention, graph connectivity, islands, entropy, bridge composition of
    the slice the viewer is looking at right now. These are the ONLY numbers
    the display controls may move.

  A `view` never re-orders anything: the lane filters the already-ranked list
  and k takes the first k survivors. So the ranking is fixed and the slider is
  a window onto it.

Also strictly separated:
  * rater GRADES (review/labels/) feed metrics. They are the experiment.
  * LLM ENGLISH EXPLANATIONS (review/vibe/explanations_*.json) are written to
    a separate file, are consumed by no metric in this program, and are marked
    as inspection-only in the payload. `assert_explanations_unused()` below is
    a live check of that, not a promise.
"""
import glob
import inspect
import json
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

from mathmap_eval import composition as C          # noqa: E402
from mathmap_eval import inclusions as I           # noqa: E402
from mathmap_eval import metrics as M              # noqa: E402
from mathmap_eval import rankings as R             # noqa: E402
from mathmap_eval.corpus import get_corpus         # noqa: E402

OUT = os.path.join(ROOT, "dashboard", "data")
LAB = os.path.join(ROOT, "review", "labels")
VIBE = os.path.join(ROOT, "review", "vibe")

UNIVERSES = ["U1", "U1D", "U0"]
REFERENCE_UNIVERSE = "U1D"
KS = [1, 2, 4, 8]
LANES = ["all", "no_glue", "theorems_defs", "introduced_only", "theorems_only"]
GRAPH_KS = [1, 2, 4, 8]

LANE_DOC = {
    "all": "Every candidate in the universe. The fully open slider.",
    "no_glue": "Hide anything our own classifier calls glue (logic-only "
               "declaration or apparatus machinery). The classic V8 view. "
               "Nothing is deleted from the ranking -- it is hidden from the "
               "display.",
    "theorems_defs": "Only theorems and definitions/constructions; hides "
                     "constructors and recursors.",
    "introduced_only": "Only citations the proof introduces, hiding anything "
                       "already implied by the theorem's own statement.",
    "theorems_only": "Only cited theorems. The narrowest lane.",
}


def clean(o):
    """NaN/Infinity -> None, recursively.

    Python's json writes bare `NaN`, which is invalid JSON and makes
    JSON.parse throw -- so the dashboard would silently fail to load and any
    agent handed these files would reject them. Missing numbers become null.
    """
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return None if (f != f or f in (float("inf"), float("-inf"))) else f
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def dump(obj, path, indent=None):
    with open(path, "w") as f:
        json.dump(clean(obj), f, indent=indent, allow_nan=False)


def lane_mask(c, base, lane):
    if lane == "all":
        return np.ones(len(base), bool)
    if lane == "no_glue":
        return ~c.inc_glue[base]
    if lane == "theorems_defs":
        k = c.node_kind[c.inc_decl[base]]
        return (k == 0) | np.isin(k, (1, 2, 5, 6, 7))
    if lane == "introduced_only":
        return ~c.inc_in_stmt_world[base]
    if lane == "theorems_only":
        return c.node_kind[c.inc_decl[base]] == 0
    raise KeyError(lane)


def ranks_within_lane(c, spec, base, lmask):
    """Positions inside each proof AFTER the lane hides some items.

    This does not re-order: it is the same ranking with hidden rows removed,
    so position j means 'the (j+1)-th visible item'.
    """
    sub = base[lmask]
    if not len(sub):
        return np.zeros(0, np.int32), sub
    return spec.ranks_within_proof(c, sub), sub


def ranking_spec_payload(name):
    """Everything another agent needs to REBUILD this ranking from scratch."""
    spec = R.get(name)
    try:
        src = inspect.getsource(spec.fn)
    except OSError:
        src = "(source unavailable)"
    return {
        "name": name,
        "family": spec.family,
        "doc": spec.doc,
        "complexity": spec.complexity,
        "source": src,
        "sort_semantics":
            "The function returns a tuple of ASCENDING lexicographic sort "
            "keys, one array per key, aligned to the candidate array `base`. "
            "Candidates are ordered within each proof by np.lexsort over "
            "those keys. Lower key value = better rank. A ranking never "
            "deletes: anything it dislikes it places last.",
    }


SIGNAL_DOC = {
    "inc_d_cite": "Depth of the CITED declaration: how many unfolding levels "
                  "of Mathlib sit beneath it. Computed from the kernel "
                  "dependency graph, no names used.",
    "inc_d_target": "Depth of the theorem being proved.",
    "inc_in_stmt_world": "True if the cited declaration is already implied by "
                         "the theorem's own statement; False if the proof "
                         "introduced it.",
    "inc_roles": "One-hot occurrence roles: applied, let-value, explicit-arg, "
                 "implicit-arg, instance-slot, strict-implicit, "
                 "type-annotation, unresolved.",
    "decl_is_claim": "Frozen V8 flag: the declaration's type is a Prop, i.e. "
                     "it is a proof of something rather than data.",
    "decl_logic_only": "Frozen V8 flag: the declaration's ingredients are "
                       "purely logical, i.e. structural plumbing.",
    "inc_machinery": "Frozen V8 flag: the cited concept is apparatus -- used "
                     "far more often than it is stated (used>200 and "
                     "used>20x inherited-stated) AND shares no ingredient "
                     "with the target theorem's statement.",
    "decl_popularity": "How many times a declaration is cited across the "
                       "whole library.",
    "decl_idf": "log(n_proofs / popularity), floored at 0.",
}


def build_definitions():
    return {
        "how_a_run_is_built": {
            "pipeline": [
                "1. DEPENDENCY DUMP. Every constant in Mathlib is walked in "
                "the Lean kernel (`mathrecord depdump`, run inside `lake "
                "env`). For each constant we record its kernel dependencies, "
                "whether its type is a Prop (`pr`), whether its type "
                "telescopes to Sort 0 (`ps`), and its arity (`ar`). 771,129 "
                "constants. No name string is ever pattern-matched.",
                "2. INCIDENCE RECORD. For each proof term we record every "
                "exact occurrence of every other declaration, together with "
                "the syntactic ROLE of that occurrence (applied, "
                "explicit-arg, instance-slot, ...) and whether the cited "
                "declaration already appears in the theorem's statement. "
                "747,644 artifacts, 18,721,317 incidences.",
                "3. UNIVERSE. A named mask over that record decides which "
                "occurrences are candidates at all. This is declared, never "
                "assumed, and is part of the experiment's identity.",
                "4. RANKING. A pure function of the corpus returning "
                "ascending lexicographic sort keys over the candidates. "
                "Candidates are ordered within each proof. Rankings never "
                "delete.",
                "5. VIEW. A lane hides rows from the ranked list and k takes "
                "the first k survivors. The view cannot re-order and cannot "
                "change any ranking-quality number.",
            ],
            "reproducing_a_ranking":
                "Each ranking tab carries the literal Python source of its "
                "scoring function plus the definition of every signal it "
                "reads. Given the incidence record, that source and "
                "np.lexsort reproduce the ranking exactly. There are no "
                "hidden constants, no name lists and no learned parameters "
                "in any ranking here.",
        },
        "universes": {
            "U0": "Every exact occurrence, any role. The complete record; "
                  "18.7M candidates.",
            "U1": "Load-bearing roles only (applied, let-value, explicit-arg, "
                  "unresolved). The historical filter; 8.5M candidates.",
            "U1D": "U1 for theorems, but ALL roles for definitions. Restores "
                   "definitions that occur in type, implicit and instance "
                   "positions while keeping the role recorded; 18.1M "
                   "candidates. The reference universe.",
            "_note": "Changing universe changes the candidate set and "
                     "therefore genuinely RE-RANKS. It is an experiment "
                     "control, not a display control.",
        },
        "lanes": LANE_DOC,
        "metric_families": {
            "Source*": "Agreement with the identifiers the human author "
                       "actually wrote, recovered from the elaborator and "
                       "never through our extraction. THIS IS NOT KEYNESS. "
                       "The 25-proof semantic panel measured the SourceOracle "
                       "-- which by construction ranks the author's own "
                       "citations first -- at only 0.619 semantic keyness, "
                       "beaten by four candidate rankings. Source* is an "
                       "authorship-alignment diagnostic. A ranking may not be "
                       "promoted on it.",
            "Role*": "Descriptive composition of what our OWN classifier says "
                     "is sitting at a rank. A statistic, not a judgement. "
                     "`RoleGlueAt1` answers 'is there glue at rank 1', and "
                     "cannot answer 'is that glue wrong'.",
            "Semantic*": "Graded rater labels, 0-4, on every candidate of 180 "
                         "proofs. The only channel that can separate BAD glue "
                         "from LEGITIMATE glue and the only one that can say "
                         "what a ranking MISSED. Small n; every figure carries "
                         "its n and a 95% Wilson interval.",
            "Coverage*": "What fraction of what humans wrote is present in a "
                         "universe AT ALL. A property of candidate "
                         "generation, not of ranking. A ranking cannot be "
                         "blamed for a candidate that was never offered.",
            "Graph*/View*": "Structure and content of the currently displayed "
                            "slice. These MOVE when you change lane or k, and "
                            "that is their whole purpose. They say nothing "
                            "about ranking quality.",
        },
        "grades": {
            "4 KEY": "A core move. You would name it when asked how the proof "
                     "goes.",
            "3 SUPPORT": "Real mathematical content, genuinely used, "
                         "secondary.",
            "2 LEGIT_GLUE": "Plumbing that genuinely IS the content of this "
                            "proof. Near the foundations, assembling "
                            "equalities really can be the whole argument.",
            "1 BAD_GLUE": "Plumbing that carries no idea here. Correct to "
                          "demote.",
            "0 JUNK": "Irrelevant machinery: automation residue, instance "
                      "resolution, universe or decidability bookkeeping.",
        },
        "headline_metrics": {
            "RoleGlueAt1": "Share of proofs whose rank-1 item OUR CLASSIFIER "
                           "calls glue. Structural, full corpus.",
            "SemanticKeyMoveAt1": "Share of proofs whose rank-1 item raters "
                                  "graded 4 (KEY).",
            "SemanticBadGlueAt1": "Share graded 1 (BAD_GLUE). The real "
                                  "failure rate at rank 1.",
            "SemanticLegitGlueAt1": "Share graded 2. Glue at rank 1 that is "
                                    "CORRECT. Distinguishing this from "
                                    "BadGlue@1 is the point of the panel.",
            "SemanticJunkAt1": "Share graded 0.",
            "SemanticBadAt1": "BadGlue@1 + Junk@1. The headline failure rate.",
            "SemanticKeyMoveRecall@k": "Of all candidates graded KEY in a "
                                       "proof, the share appearing in the top "
                                       "k. Averaged over proofs that have at "
                                       "least one KEY.",
            "GluePrecision": "Of candidates OUR classifier calls glue, the "
                             "share raters graded 1 or 2 (plumbing-shaped).",
            "GlueRecall": "Of candidates raters graded 1 or 2, the share our "
                          "classifier catches.",
            "KeyMovesFlaggedAsGlue": "Of candidates graded KEY, the share our "
                                     "glue flag would demote. The cost of the "
                                     "glue channel; must stay near zero.",
            "SemanticKeyLostToPolicy": "Of candidates graded KEY, the share "
                                       "the CURRENT LANE hides entirely. A "
                                       "view property, not a ranking "
                                       "property.",
            "ViewKeyRetained@k": "Of candidates graded KEY, the share visible "
                                 "in the current slice.",
        },
        "signals": SIGNAL_DOC,
        "cautions": [
            "SourceHit@1 is retired as a promotion criterion. It measures "
            "agreement with authorship, and the semantic panel showed the "
            "SourceOracle itself scores only 0.619 on keyness.",
            "The apparatus/machinery flag fires on ZERO candidates in the "
            "labelled sample. It is extremely sparse (102 concepts) and "
            "carries no weight in these numbers; do not read Junk@1 as "
            "evidence that it works.",
            "The labelled set is 180 proofs. Single-rater for 160 of them, "
            "triple-rated for 20. Differences smaller than the Wilson "
            "intervals shown are not real.",
            "Only 5 of the 180 labelled proofs also carry source provenance, "
            "so Source* and Semantic* are measured on almost disjoint "
            "samples and should not be differenced.",
            "English explanations in the vibe check are LLM-generated for "
            "your inspection only. They are not used by any metric and were "
            "produced after all grading was complete.",
        ],
    }


def assert_explanations_unused():
    """Live check that the gloss never reaches a metric."""
    import mathmap_eval.composition as _c
    import mathmap_eval.metrics as _m
    import mathmap_eval.rankings as _r
    for mod in (_c, _m, _r):
        src = inspect.getsource(mod)
        for bad in ("explanation", "statement_en", "proof_sketch_en"):
            assert bad not in src, f"{mod.__name__} references {bad!r}"
    return True


def main():
    t_all = time.time()
    os.makedirs(OUT, exist_ok=True)
    assert_explanations_unused()
    c = get_corpus()
    keymap = json.load(open(os.path.join(LAB, "keymap.json")))
    grades, label_meta, missing_votes = C.load_labels(LAB, keymap)
    agreement = C.rater_agreement(LAB, keymap)
    glue_report = C.glue_classifier_report(c, grades, keymap)

    names = R.names()
    print(f"rankings: {len(names)}  universes: {UNIVERSES}", flush=True)

    # ---- shared per-universe context ------------------------------------
    ctx = {}
    for U in UNIVERSES:
        base = np.where(c.universe(U))[0]
        ctx[U] = {"base": base,
                  "evalset": c.evaluation_set(U, True),
                  "lane": {L: lane_mask(c, base, L) for L in LANES},
                  "coverage": M.coverage_metrics(c, U)}
        print(f"  {U}: {len(base):,} candidates, "
              f"{len(ctx[U]['evalset']):,} proofs with provenance", flush=True)

    summary = {"reference_universe": REFERENCE_UNIVERSE, "ks": KS,
               "lanes": LANES, "universes": UNIVERSES, "rankings": {},
               "coverage": {U: ctx[U]["coverage"] for U in UNIVERSES},
               "labels": {"meta": label_meta, "agreement": agreement,
                          "glue_classifier": glue_report}}

    vibe_orders = defaultdict(dict)      # (universe, ranking) -> {inc: rank}
    vibe_keys = defaultdict(dict)
    vibe_set = json.load(open(os.path.join(VIBE, "vibe_set.json")))
    vibe_inc = sorted({int(i) for p in vibe_set
                       for i in json.load(open(os.path.join(
                           LAB, "keymap.json")))[p["id"]]["items"].values()})

    for nm in names:
        t0 = time.time()
        spec = R.get(nm)
        payload = {"ranking": nm, "family": spec.family,
                   "spec": ranking_spec_payload(nm), "experiments": {}}
        for U in UNIVERSES:
            base = ctx[U]["base"]
            ranks = spec.ranks_within_proof(c, base)
            by_pos = dict(zip(base.tolist(), ranks.tolist()))

            # ---------- RANKING QUALITY (invariant under display controls)
            rq = {
                "source": M.source_metrics(c, ctx[U]["evalset"], by_pos, ks=KS),
                "semantic": C.semantic_metrics(c, base, ranks, grades, keymap,
                                               ks=KS),
                "composition": C.rank_composition(c, base, ranks, ks=KS),
                "ties": None,
            }
            from mathmap_eval.runner import tie_stats
            rq["ties"] = tie_stats(c, spec, base)

            # ---------- VIEWS (the only things the slider may move)
            views = {}
            for L in LANES:
                lm = ctx[U]["lane"][L]
                lranks, lbase = ranks_within_lane(c, spec, base, lm)
                lgrade = np.array([grades.get(int(p), -1) for p in lbase])
                n_key_total = int(sum(1 for g in grades.values() if g == 4))
                for k in KS:
                    sel = lranks < k
                    subset = lbase[sel]
                    cat = C.structural_category(c, subset)
                    cc = np.bincount(cat, minlength=len(C.STRUCT_CATS))
                    tot = max(int(cc.sum()), 1)
                    kept = int(((lgrade == 4) & sel).sum())
                    v = {
                        "lane": L, "k": k,
                        "ViewSize": int(len(subset)),
                        "ViewProofsCovered": int(len(np.unique(
                            c.inc_artifact[subset]))) if len(subset) else 0,
                        "ViewComposition": {a: int(cc[ai]) / tot for ai, a
                                            in enumerate(C.STRUCT_CATS)},
                        "ViewGlueShare": int(cc[0] + cc[1]) / tot,
                        "ViewKeyRetained": {
                            "value": kept / n_key_total if n_key_total else 0.0,
                            "k": kept, "n": n_key_total},
                        "ViewLaneHidesOfUniverse": float(1 - lm.mean()),
                    }
                    if k in GRAPH_KS:
                        v["graph"] = M.graph_metrics(c, lbase, sel)
                    views[f"{L}|{k}"] = v

            payload["experiments"][U] = {
                "universe": U,
                "n_candidates": int(len(base)),
                "n_proofs": int(len(np.unique(c.inc_artifact[base]))),
                "n_proofs_with_provenance": len(ctx[U]["evalset"]),
                "coverage": ctx[U]["coverage"],
                "ranking_quality": rq,
                "views": views,
            }

            # vibe orderings for this (ranking, universe)
            pos = {int(p): i for i, p in enumerate(base)}
            kv = spec.keys(c, base)
            for inc in vibe_inc:
                i = pos.get(inc)
                if i is None:
                    continue
                vibe_orders[(U, nm)][inc] = int(ranks[i])
                vibe_keys[(U, nm)][inc] = [
                    (float(a[i]) if not isinstance(a[i], (bool, np.bool_))
                     else int(a[i])) for a in kv]

        dump(payload, os.path.join(OUT, f"ranking_{nm}.json"))
        ref = payload["experiments"][REFERENCE_UNIVERSE]["ranking_quality"]
        summary["rankings"][nm] = {
            "family": spec.family,
            "doc": spec.doc,
            "complexity": spec.complexity,
            "by_universe": {
                U: {
                    "SourceHit@1": payload["experiments"][U]["ranking_quality"]
                        ["source"]["SourceHit@1"],
                    "SourceMRR": payload["experiments"][U]["ranking_quality"]
                        ["source"]["SourceMRR"],
                    "RoleGlueAt1": payload["experiments"][U]["ranking_quality"]
                        ["composition"]["RoleGlueAt1"],
                    "SemanticKeyMoveAt1": payload["experiments"][U]
                        ["ranking_quality"]["semantic"]["SemanticKeyMoveAt1"],
                    "SemanticBadAt1": payload["experiments"][U]
                        ["ranking_quality"]["semantic"]["SemanticBadAt1"],
                    "SemanticLegitGlueAt1": payload["experiments"][U]
                        ["ranking_quality"]["semantic"]["SemanticLegitGlueAt1"],
                    "SemanticMeanGradeAt1": payload["experiments"][U]
                        ["ranking_quality"]["semantic"]["SemanticMeanGradeAt1"],
                    "grade_at_1": payload["experiments"][U]["ranking_quality"]
                        ["semantic"]["grade_at_1"],
                    "by_target_depth": payload["experiments"][U]
                        ["ranking_quality"]["semantic"]["by_target_depth"],
                    "composition_by_depth": payload["experiments"][U]
                        ["ranking_quality"]["composition"]["at_k"][1]
                        ["by_target_depth"],
                    **{f"SemanticKeyMoveRecall@{k}": payload["experiments"][U]
                       ["ranking_quality"]["semantic"]
                       [f"SemanticKeyMoveRecall@{k}"] for k in KS},
                    **{f"SourceRecall@{k}": payload["experiments"][U]
                       ["ranking_quality"]["source"][f"SourceRecall@{k}"]
                       for k in KS},
                } for U in UNIVERSES},
        }
        s = ref["semantic"]
        print(f"  {nm:<22} key@1={s['SemanticKeyMoveAt1']['value']:.3f} "
              f"bad@1={s['SemanticBadAt1']['value']:.3f} "
              f"glue@1={ref['composition']['RoleGlueAt1']:.3f} "
              f"src@1={ref['source']['SourceHit@1']:.3f} "
              f"({time.time() - t0:.0f}s)", flush=True)

    dump(summary, os.path.join(OUT, "summary.json"))
    dump(build_definitions(), os.path.join(OUT, "definitions.json"), indent=1)

    # ---- vibe check ------------------------------------------------------
    expl = {}
    for f in sorted(glob.glob(os.path.join(VIBE, "explanations_*.json"))):
        expl.update(json.load(open(f)))
    prov_flag = {}
    for p in vibe_set:
        d = c.name_to_id.get(p["theorem"])
        refs = c.source_refs.get(p["theorem"])
        prov_flag[p["id"]] = refs

    vibe_out = {"universes": UNIVERSES, "lanes": LANES, "ks": KS,
                "rankings": names, "proofs": []}
    for p in vibe_set:
        km = keymap[p["id"]]
        e = expl.get(p["id"], {})
        refs = prov_flag[p["id"]]
        cands = []
        for it in p["candidates"]:
            inc = int(km["items"][str(it["n"])])
            g = grades.get(inc)
            cands.append({
                "n": it["n"], "name": it["name"], "kind": it["kind"],
                "cited_depth": it["depth"], "target_depth": p["theorem_depth"],
                "in_statement": it["in_statement"], "role": it["role"],
                "incidence": inc,
                "grade": g, "grade_name": C.GRADE_NAMES.get(g),
                "system_glue": bool(c.inc_glue[inc]),
                "system_category": C.STRUCT_CATS[int(
                    C.structural_category(c, np.array([inc]))[0])],
                "source_cited": (None if refs is None
                                 else bool(it["name"] in refs)),
                "lanes": [L for L in LANES
                          if bool(lane_mask(c, np.array([inc]), L)[0])],
                "explanation_llm": (e.get("candidates") or {}).get(str(it["n"])),
            })
        vibe_out["proofs"].append({
            "id": p["id"], "theorem": p["theorem"], "band": p["band"],
            "theorem_depth": p["theorem_depth"],
            "def_fraction": p["def_fraction"],
            "has_provenance": refs is not None,
            "missing_key_votes": missing_votes.get(p["id"], []),
            "statement_en_llm": e.get("statement_en"),
            "proof_sketch_en_llm": e.get("proof_sketch_en"),
            "candidates": cands,
            "orders": {f"{U}|{nm}": {
                str(cd["n"]): {
                    "rank": vibe_orders[(U, nm)].get(cd["incidence"]),
                    "keys": vibe_keys[(U, nm)].get(cd["incidence"])}
                for cd in cands}
                for U in UNIVERSES for nm in names},
        })
    dump(vibe_out, os.path.join(OUT, "vibe.json"))

    # ---- manifest --------------------------------------------------------
    try:
        rev = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                      cwd=ROOT, text=True).strip()
    except Exception:
        rev = "unknown"
    manifest = {
        "built": time.strftime("%Y-%m-%d %H:%M"),
        "git": rev,
        "universes": UNIVERSES, "reference_universe": REFERENCE_UNIVERSE,
        "lanes": LANES, "lane_doc": LANE_DOC, "ks": KS,
        "rankings": [{"name": n, "family": R.get(n).family,
                      "doc": R.get(n).doc} for n in names],
        "n_labelled_proofs": label_meta["n_proofs_labelled"],
        "n_labels": label_meta["n_incidences_labelled"],
        "n_rater_files": label_meta["n_rater_files"],
        "vibe_proofs": [p["id"] for p in vibe_set],
        "files": ["manifest.json", "summary.json", "definitions.json",
                  "vibe.json"] + [f"ranking_{n}.json" for n in names],
        "explanations_are_inspection_only": True,
    }
    dump(manifest, os.path.join(OUT, "manifest.json"), indent=1)

    # ---- file:// loader bundle ------------------------------------------
    bundle = {"manifest": manifest, "summary": summary,
              "definitions": build_definitions(), "vibe": vibe_out,
              "rankings": {}}
    for nm in names:
        bundle["rankings"][nm] = json.load(
            open(os.path.join(OUT, f"ranking_{nm}.json")))
    with open(os.path.join(OUT, "all.js"), "w") as f:
        f.write("window.MAPDATA = ")
        json.dump(clean(bundle), f, allow_nan=False)
        f.write(";\n")

    sz = sum(os.path.getsize(os.path.join(OUT, f))
             for f in os.listdir(OUT)) / 1e6
    print(f"\nwritten {OUT}  ({sz:.1f} MB, {len(os.listdir(OUT))} files) "
          f"in {time.time() - t_all:.0f}s", flush=True)


if __name__ == "__main__":
    main()
