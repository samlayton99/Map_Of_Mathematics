"""Render MAP_STRUCTURE_RESULTS.md from map_analysis.json + edge_stats.json.

  python src/map_report.py data/map/map_analysis.json data/map/edge_stats.json
"""
import json
import sys

SETS = ["E4_flat", "E4", "EL0"]


def f3(x):
    return "%.3f" % x


def load_opt(path):
    try:
        return json.load(open(path))
    except Exception:
        return None


def main():
    import os
    ana = json.load(open(sys.argv[1]))
    est = json.load(open(sys.argv[2]))
    d = os.path.dirname(os.path.abspath(sys.argv[1]))
    sens = load_opt(os.path.join(d, "el0_sensitivity.json"))
    seeds = load_opt(os.path.join(d, "auc_seed_stability.json"))
    alt = load_opt(os.environ.get("MAP_ALT_ANALYSIS_JSON", ""))
    label = sys.argv[3] if len(sys.argv) > 3 else "SMOKE (v7_backup, OLD stmt flag)"
    E = ana["edge_sets"]
    P = print

    P("# Global map structure: E4_flat vs E4 vs EL0")
    P("")
    P("Run label: **%s**" % label)
    P("")
    P("Data: `%s`" % ana["data_dir"])
    P("Modules: `%s` (present=%s)"
      % (ana["modules_tsv"], ana["modules_tsv_present"]))
    P("")
    P("Areas are validation-only evidence of human organization. They never")
    P("enter the ordering or the admission rule.")
    P("")
    P("## Method")
    P("")
    P("Edges run `target_decl -> candidate_decl`, one block of candidates per")
    P("artifact, restricted to artifacts whose `is_generated` is False.")
    P("Candidates are ordered by `(dem, lane, stmt, -depth, position)`:")
    P("")
    P("- `dem` 0 for load-bearing occurrences (roles applied / let-value /")
    P("  explicit-arg / unresolved), 1 for the U1D demoted entry (non-Prop")
    P("  declarations cited only through non-load roles).")
    P("- `lane` 2 when the candidate's minimum role tier is instance-only,")
    P("  else 1 when `depth_stmt <= 1` (transport), else 0 (move).")
    P("- `stmt` the incidence's `in_stmt_world` flag; proof-introduced (0) first.")
    P("- `depth` the cited declaration's value depth (`d_cite`, verified equal")
    P("  to `nodes.depth[decl]`); deepest first.")
    P("- `position` the incidence's index inside its artifact row block. Row")
    P("  blocks are NOT sorted by declaration id (checked: 35/2931 sampled")
    P("  blocks are ascending), so this approximates extractor term order.")
    P("")
    P("Generated candidates are redirected to the longest proper dot-prefix")
    P("that is an existing non-generated declaration; a generated candidate")
    P("owned by the artifact's own target is internal and dropped, as is one")
    P("with no owner. Redirected candidates take the owner's `depth_stmt` and")
    P("node depth and never receive lane 2. Candidates are deduplicated after")
    P("redirect, keeping the best key. Self-loops are dropped.")
    P("")
    P("`E4_flat` is the control: top-4 by `(role tier, position)` over")
    P("load-bearing candidates only, no lanes, no redirect.")
    P("")
    P("The admission code was checked against a brute-force Python")
    P("reimplementation on 400 random artifacts: 0 mismatches for E4 and EL0.")
    P("")
    P("### Reading the class shares honestly")
    P("")
    P("Hub classes are assigned with precedence")
    P("`notation > generated > transport > mathematics`, where `transport` is")
    P("`depth_stmt <= 1`, `notation` is a lookup in the seven-name observed")
    P("interface set, and `mathematics` is the residual.")
    P("")
    P("**The transport share of EL0 is zero by construction**: EL0 is defined")
    P("as lane 0, and lane 1 is exactly `depth_stmt <= 1`. So EL0's")
    P("\"mathematics\" share is not independent evidence. Two diagnostics that")
    P("are independent of the construction are reported alongside it: the")
    P("notation share (all seven interface constants have `depth_stmt = 2`, so")
    P("they are lane 0 and survive EL0), and the share of cross-area link mass")
    P("landing in the infrastructure AREAS (Core, Tactic, Util, Lean, ...),")
    P("which is a pure human-organization label.")
    P("")

    # ---- edge sets ------------------------------------------------------
    P("## Admitted edge sets")
    P("")
    P("| set | edges | source decls | target decls | nodes |")
    P("|---|---|---|---|---|")
    for s in SETS:
        if s not in est:
            continue
        e = est[s]
        P("| %s | %d | %d | %d | %d |"
          % (s, e["n_edges"], e["n_src"], e["n_dst"], e["n_nodes"]))
    P("")
    k = est.get("EL0_k", {})
    if k:
        P("EL0 admission budget k per artifact (dem=0, lane=0, stmt=0):")
        P("")
        P("| mean | median | p90 | p99 | max | k=0 share | mean given k>0 |")
        P("|---|---|---|---|---|---|---|")
        P("| %.2f | %.0f | %.0f | %.0f | %d | %.3f | %.2f |"
          % (k["mean"], k["median"], k["p90"], k["p99"], k["max"],
             k["frac_zero"], k["mean_nonzero"]))
        P("")
    if sens:
        P("Where the EL0 budget comes from (same candidate pool, successively")
        P("dropping keys). The `stmt` key is the one whose input flag is being")
        P("rebuilt, so EL0's final size is the least settled number here:")
        P("")
        P("| filter | edges | mean k | median | p90 | max | k=0 share |")
        P("|---|---|---|---|---|---|---|")
        for r in sens:
            P("| %s | %d | %.2f | %.0f | %.0f | %d | %s |"
              % (r["label"], r["n_edges"], r["mean"], r["median"], r["p90"],
                 r["max"], f3(r["frac_zero"])))
        P("")
    pool = est.get("pool", {})
    if pool:
        P("Candidate pool (%d rows): U1D-demoted %.3f; lane 0/1/2 = %.3f/%.3f/%.3f;"
          " stmt=1 %.3f."
          % (pool["n_candidates"], pool["dem1_frac"], pool["lane_frac"][0],
             pool["lane_frac"][1], pool["lane_frac"][2], pool["stmt1_frac"]))
        P("")

    # ---- areas ----------------------------------------------------------
    P("## Area distribution (validation labels)")
    P("")
    P("%d areas over %d declarations."
      % (ana["n_areas"], sum(d["n_decls"] for d in ana["area_distribution"])))
    P("")
    P("| area | decls |")
    P("|---|---|")
    for d in ana["area_distribution"][:20]:
        P("| %s | %d |" % (d["area"], d["n_decls"]))
    rest = ana["area_distribution"][20:]
    if rest:
        P("| (%d smaller areas) | %d |"
          % (len(rest), sum(d["n_decls"] for d in rest)))
    P("")

    # ---- headline -------------------------------------------------------
    P("## Headline three-way comparison")
    P("")
    P("| metric | E4_flat | E4 | EL0 |")
    P("|---|---|---|---|")

    def row(name, fn):
        cells = []
        for s in SETS:
            try:
                cells.append(fn(E[s]))
            except Exception:
                cells.append("-")
        P("| %s | %s | %s | %s |" % (name, cells[0], cells[1], cells[2]))

    row("edges", lambda r: "%d" % r["n_edges"])
    row("largest component (nodes)",
        lambda r: "%d" % r["graph"]["largest_component_nodes"])
    row("LCC share of active nodes",
        lambda r: f3(r["graph"]["largest_component_frac_of_active"]))
    row("cross-area mass -> mathematics",
        lambda r: f3(r["hubs"]["link_mass"]["cross_area"]["mathematics"]))
    row("cross-area mass -> transport",
        lambda r: f3(r["hubs"]["link_mass"]["cross_area"]["transport"]))
    row("cross-area mass -> notation",
        lambda r: f3(r["hubs"]["link_mass"]["cross_area"]["notation"]))
    row("cross-area mass -> generated",
        lambda r: f3(r["hubs"]["link_mass"]["cross_area"]["generated"]))
    row("same-area mass -> mathematics",
        lambda r: f3(r["hubs"]["link_mass"]["same_area"]["mathematics"]))
    row("within-area edge share",
        lambda r: f3(r["hubs"]["area_assortativity"]["within_area_edge_share"]))
    row("edges landing in a meta area (Core/Tactic/...)",
        lambda r: f3(r["hubs"]["area_assortativity"]["dst_in_meta_area_share"]))
    row("cross-area mass -> meta areas (Core/Tactic/...)",
        lambda r: f3(r["hubs"]["link_mass"]["cross_area_core_or_tactic_share"]))
    row("top-100 hubs' share of all links",
        lambda r: f3(r["hubs"]["top100_hub_mass"]["share_of_all_links"]))
    row("top-100 hubs' share of cross-area links",
        lambda r: f3(r["hubs"]["top100_hub_mass"]["share_of_cross_links"]))
    row("AMI (communities vs areas)", lambda r: "%.4f" % r["communities"]["AMI"])
    row("communities", lambda r: "%d" % r["communities"]["n_communities"])
    row("modularity", lambda r: f3(r["communities"]["modularity"]))
    row("distance AUC (same vs cross)", lambda r: "%.4f" % r["distance"]["AUC"])
    row("mean dist same-area", lambda r: f3(r["distance"]["same_area"]["mean"]))
    row("mean dist cross-area", lambda r: f3(r["distance"]["cross_area"]["mean"]))
    row("delta_depth median (all)",
        lambda r: "%.0f" % r["verticality"]["all_edges"]["q"]["50"])
    row("delta_depth median (cross-area)",
        lambda r: "%.0f" % r["verticality"]["cross_area"]["q"]["50"])
    P("")

    # ---- 1 hubs ---------------------------------------------------------
    P("## 1. Relative hubs")
    P("")
    for s in SETS:
        if s not in E:
            continue
        h = E[s]["hubs"]
        P("### %s" % s)
        P("")
        lm = h["link_mass"]
        P("| link population | links | mathematics | transport | notation | generated |")
        P("|---|---|---|---|---|---|")
        for key in ("all_edges", "same_area", "cross_area"):
            m = lm[key]
            P("| %s | %d | %s | %s | %s | %s |"
              % (key, m["n_links"], f3(m["mathematics"]), f3(m["transport"]),
                 f3(m["notation"]), f3(m["generated"])))
        P("")
        pt = h["pooled_top15_classes"]
        P("Pooled class composition of the per-area top-15 lists:")
        P("")
        P("| list | n | mathematics | transport | notation | generated |")
        P("|---|---|---|---|---|---|")
        for key in ("within_area_hubs", "cross_area_mediators"):
            c = pt[key]
            P("| %s | %d | %s | %s | %s | %s |"
              % (key, c["n"], f3(c["mathematics"]), f3(c["transport"]),
                 f3(c["notation"]), f3(c["generated"])))
        P("")
        if "global_top_hubs" in h:
            P("Global top hubs by total in-degree (top 15 of 100 scored):")
            P("")
            P("| hub | in-degree | in-cross | class | area | areas citing |")
            P("|---|---|---|---|---|---|")
            for g in h["global_top_hubs"][:15]:
                P("| `%s` | %d | %d | %s | %s | %d |"
                  % (g["name"], g["in_all"], g["in_cross"], g["class"],
                     g["area"], g["n_areas_citing"]))
            P("")
            t = h["top100_hub_mass"]
            P("Top-100 hubs absorb %s of all links and %s of cross-area links;"
              " classes %s."
              % (f3(t["share_of_all_links"]), f3(t["share_of_cross_links"]),
                 t["class_counts"]))
            P("")
        if "cross_mass_by_hub_area" in h:
            P("Cross-area link mass by hub AREA (area-based, independent of the"
              " lane construction):")
            P("")
            P("| hub area | cross-links | share |")
            P("|---|---|---|")
            for g in h["cross_mass_by_hub_area"]:
                P("| %s | %d | %s |" % (g["area"], g["links"], f3(g["share"])))
            P("")
        pa = h["per_area"]
        shown = sorted(pa.items(), key=lambda kv: -kv[1]["in_cross_total"])[:6]
        for aname, v in shown:
            P("**%s** (%d decls, in-same %d, in-cross %d)"
              % (aname, v["n_decls"], v["in_same_total"], v["in_cross_total"]))
            P("")
            P("| rank | within-area hub | in-same | class | cross-area mediator | in-cross | class |")
            P("|---|---|---|---|---|---|---|")
            for i in range(min(8, max(len(v["within_area_hubs"]),
                                      len(v["cross_area_mediators"])))):
                a = v["within_area_hubs"][i] if i < len(v["within_area_hubs"]) else None
                b = v["cross_area_mediators"][i] if i < len(v["cross_area_mediators"]) else None
                P("| %d | %s | %s | %s | %s | %s | %s |"
                  % (i + 1,
                     "`%s`" % a["name"] if a else "-", a["in_same"] if a else "-",
                     a["class"] if a else "-",
                     "`%s`" % b["name"] if b else "-", b["in_cross"] if b else "-",
                     b["class"] if b else "-"))
            P("")

    # ---- 2 communities --------------------------------------------------
    P("## 2. Community emergence")
    P("")
    P("| set | method | nodes | undirected edges | subsampled | communities | >=100 | largest frac | modularity | AMI vs areas |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    for s in SETS:
        if s not in E:
            continue
        c = E[s]["communities"]
        P("| %s | %s | %d | %d | %s | %d | %d | %s | %s | **%.4f** |"
          % (s, c.get("method", "louvain"), c["n_nodes"],
             c["n_edges_undirected"], c["subsampled"],
             c["n_communities"], c["n_communities_ge_100"],
             f3(c["largest_community_frac"]), f3(c["modularity"]), c["AMI"]))
    P("")

    if alt:
        P("Cross-check with a second community algorithm (vectorised weighted")
        P("label propagation, same graphs, same seed):")
        P("")
        P("| set | method | communities | modularity | AMI vs areas |")
        P("|---|---|---|---|---|")
        for s in SETS:
            c = alt.get("edge_sets", {}).get(s, {}).get("communities")
            if not c:
                continue
            P("| %s | %s | %d | %s | **%.4f** |"
              % (s, c.get("method", "?"), c["n_communities"],
                 f3(c["modularity"]), c["AMI"]))
        P("")

    # ---- 3 distance -----------------------------------------------------
    P("## 3. Distance honesty")
    P("")
    P("Non-generated theorem declarations (`kind == 0`) in the largest")
    P("component with a known area. The source is drawn uniformly from that")
    P("pool; the partner is drawn uniformly from the source's own area")
    P("(same-area) or uniformly from the pool with rejection (cross-area).")
    P("Sampling the source uniformly rather than sampling pairs uniformly")
    P("keeps the large areas (Core, Algebra) from dominating the same-area")
    P("sample. Undirected BFS, capped at 12; unreachable counts as 12.")
    P("")
    P("| set | pairs each | same mean | cross mean | same median | cross median | same capped | cross capped | AUC |")
    P("|---|---|---|---|---|---|---|---|---|")
    for s in SETS:
        if s not in E:
            continue
        d = E[s]["distance"]
        if "AUC" not in d:
            continue
        P("| %s | %d | %s | %s | %.0f | %.0f | %s | %s | **%.4f** |"
          % (s, d["n_pairs_each"], f3(d["same_area"]["mean"]),
             f3(d["cross_area"]["mean"]), d["same_area"]["median"],
             d["cross_area"]["median"], f3(d["same_area"]["frac_capped"]),
             f3(d["cross_area"]["frac_capped"]), d["AUC"]))
    P("")
    for s in SETS:
        if s not in E or "AUC" not in E[s]["distance"]:
            continue
        d = E[s]["distance"]
        P("%s distance histogram (same / cross):" % s)
        P("")
        P("| d | " + " | ".join(str(i) for i in range(13)) + " |")
        P("|---|" + "---|" * 13)
        P("| same | " + " | ".join(str(d["same_area"]["hist"][str(i)])
                                   for i in range(13)) + " |")
        P("| cross | " + " | ".join(str(d["cross_area"]["hist"][str(i)])
                                    for i in range(13)) + " |")
        P("")

    if seeds:
        P("Sampling noise on the AUC: two independent re-draws of 750+750")
        P("pairs per edge set.")
        P("")
        P("| set | re-draw 1 | re-draw 2 |")
        P("|---|---|---|")
        for s in SETS:
            if s in seeds:
                P("| %s | %.4f | %.4f | " % (s, seeds[s][0], seeds[s][1]))
        P("")

    # ---- 4 verticality --------------------------------------------------
    P("## 4. Verticality (delta_depth = depth[src] - depth[dst])")
    P("")
    for pop in ("all_edges", "same_area", "cross_area"):
        P("**%s**" % pop)
        P("")
        P("| set | n | mean | p1 | p5 | p25 | p50 | p75 | p90 | p99 | frac <= 0 |")
        P("|---|---|---|---|---|---|---|---|---|---|---|")
        for s in SETS:
            if s not in E:
                continue
            v = E[s]["verticality"][pop]
            if v.get("n", 0) == 0:
                continue
            q = v["q"]
            P("| %s | %d | %.1f | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %s |"
              % (s, v["n"], v["mean"], q["1"], q["5"], q["25"], q["50"],
                 q["75"], q["90"], q["99"], f3(v["frac_le_0"])))
        P("")


if __name__ == "__main__":
    main()
