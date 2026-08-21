/* report.js -- MathMap dashboard Markdown report generator.
 *
 * Dependency-free. Loaded with a plain <script> tag from a file:// page.
 * No imports, no modules, no CDN, no build step. Defines exactly one global:
 * window.Report.
 *
 * THE DISCIPLINE THIS FILE EXISTS TO PRESERVE
 * -------------------------------------------
 * A number is either a property of the RANKING or a property of the CURRENTLY
 * DISPLAYED SLICE, and the report never blurs the two:
 *
 *   experiments[universe].ranking_quality  -- semantic scorecard, source
 *       agreement, structural rank composition, ties. Computed on the FULL
 *       ranked universe. These do NOT move when the viewer changes lane or k.
 *
 *   experiments[universe].views["<lane>|<k>"] -- size, composition, key
 *       retention, graph connectivity of the slice on screen right now. These
 *       are the ONLY numbers the display controls may move.
 *
 * They get separate top-level sections with headers that say which is which.
 *
 * Further rules enforced here:
 *   - Source* measures agreement with what the human author WROTE. It is not
 *     keyness, is labelled as such at every appearance, and no ranking is
 *     promoted on it.
 *   - Semantic* comes from graded rater labels on 180 proofs. Every figure is
 *     printed with its n and 95% Wilson interval, and the report states
 *     plainly that differences smaller than the intervals are not real.
 *   - Fields ending _llm in vibe.json are LLM-generated glosses for
 *     inspection only. They feed no metric and are flagged wherever shown.
 *   - Missing/null numbers print as an em dash. Never undefined, never NaN.
 */
(function () {
  "use strict";

  var DASH = "—";
  var VERSION = "1.0";

  /* Canonical orderings, mirrored from mathmap_eval. Data-driven where the
   * data supplies an order; these are only fallbacks / sort hints. */
  var BAND_ORDER = ["0-10", "11-25", "26-50", "51-75", "76-125", "126+"];
  var GRADE_ORDER = ["KEY", "SUPPORT", "LEGIT_GLUE", "BAD_GLUE", "JUNK"];
  var GRADE_CODE = { KEY: 4, SUPPORT: 3, LEGIT_GLUE: 2, BAD_GLUE: 1, JUNK: 0 };
  var STRUCT_CATS = ["machinery", "logic-glue", "theorem",
                     "definition/construction", "constructor/recursor"];

  /* Corpus arrays that are indexing plumbing rather than scoring signals.
   * Used only to avoid crying wolf about undocumented signals. */
  var PLUMBING = {
    inc_artifact: 1, inc_decl: 1, inc_target: 1, names: 1, name_to_id: 1,
    node_kind: 1, node_depth: 1, n_nodes: 1, n_incidences: 1, art_of_decl: 1,
    source_refs: 1, kind_group: 1, universe: 1, evaluation_set: 1,
    n_proofs: 1, n_artifacts: 1
  };

  /* ------------------------------------------------------------------ *
   * Primitives: everything that can print a value goes through here so
   * that a missing field can never reach the page as undefined or NaN.
   * ------------------------------------------------------------------ */

  function isNum(x) {
    return typeof x === "number" && isFinite(x);
  }

  function get(obj, path, dflt) {
    var cur = obj, parts = path.split("."), i;
    for (i = 0; i < parts.length; i++) {
      if (cur === null || cur === undefined) return dflt;
      cur = cur[parts[i]];
    }
    return (cur === undefined || cur === null) ? dflt : cur;
  }

  /* Fixed-decimal proportion, or an em dash. */
  function fx(v, d) {
    return isNum(v) ? v.toFixed(d === undefined ? 3 : d) : DASH;
  }

  /* Percentage, or an em dash. */
  function pc(v, d) {
    return isNum(v) ? (v * 100).toFixed(d === undefined ? 1 : d) + "%" : DASH;
  }

  /* Integer with thousands separators, or an em dash. */
  function iv(v) {
    if (!isNum(v)) return DASH;
    return Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  /* Any string-ish value, or an em dash. */
  function tx(v) {
    if (v === undefined || v === null) return DASH;
    if (typeof v === "string") return v.length ? v : DASH;
    if (typeof v === "boolean") return v ? "yes" : "no";
    if (typeof v === "number") return isNum(v) ? String(v) : DASH;
    return DASH;
  }

  /* Escape a value for use inside a Markdown table cell. */
  function cell(v) {
    var s = (v === undefined || v === null) ? DASH : String(v);
    if (s === "" ) s = DASH;
    s = s.replace(/\\/g, "\\\\").replace(/\|/g, "\\|");
    /* A table cell is one line: collapse any wrapping the source JSON had. */
    s = s.replace(/\s+/g, " ").trim();
    return s.length ? s : DASH;
  }

  /* Collapse a possibly multi-line docstring to a single line. */
  function oneline(v) {
    var s = tx(v);
    return s === DASH ? DASH : s.replace(/\s+/g, " ").trim();
  }

  function code(v) {
    var s = tx(v);
    return s === DASH ? DASH : "`" + s.replace(/`/g, "'") + "`";
  }

  function clip(s, n) {
    if (typeof s !== "string" || !s.length) return DASH;
    s = s.replace(/\s+/g, " ").trim();
    return s.length <= n ? s : s.slice(0, n - 1).replace(/\s+\S*$/, "") + "…";
  }

  /* Wilson score interval, identical to mathmap_eval.composition._wilson.
   * Used ONLY to fill an interval the exporter did not precompute (the
   * SUPPORT row of the rank-1 scorecard); every such cell is footnoted. */
  function wilson(k, n, z) {
    if (!isNum(k) || !isNum(n) || n <= 0) return null;
    z = z || 1.96;
    var p = k / n;
    var d = 1 + z * z / n;
    var c = (p + z * z / (2 * n)) / d;
    var h = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d;
    return [Math.max(0, c - h), Math.min(1, c + h)];
  }

  /* "[0.035, 0.106]" from a ci95 array, or an em dash. */
  function ciStr(ci) {
    if (!ci || ci.length !== 2 || !isNum(ci[0]) || !isNum(ci[1])) return DASH;
    return "[" + ci[0].toFixed(3) + ", " + ci[1].toFixed(3) + "]";
  }

  /* "11/180" from a {k, n} share object, or an em dash. */
  function knStr(o) {
    if (!o || !isNum(o.k) || !isNum(o.n)) return DASH;
    return iv(o.k) + "/" + iv(o.n);
  }

  /* "0.061 [0.035, 0.106] (11/180)" from a share object. */
  function shareStr(o) {
    if (!o) return DASH;
    var parts = [fx(o.value)];
    if (o.ci95) parts.push(ciStr(o.ci95));
    if (isNum(o.k) && isNum(o.n)) parts.push("(" + knStr(o) + ")");
    return parts.join(" ");
  }

  function ciOverlap(a, b) {
    if (!a || !b || a.length !== 2 || b.length !== 2) return null;
    if (!isNum(a[0]) || !isNum(a[1]) || !isNum(b[0]) || !isNum(b[1])) return null;
    return a[1] >= b[0] && b[1] >= a[0];
  }

  /* ------------------------------------------------------------------ *
   * Markdown construction
   * ------------------------------------------------------------------ */

  function table(headers, rows) {
    if (!rows || !rows.length) {
      return "_No rows._";
    }
    var out = [];
    out.push("| " + headers.map(cell).join(" | ") + " |");
    out.push("|" + headers.map(function () { return " --- "; }).join("|") + "|");
    for (var i = 0; i < rows.length; i++) {
      out.push("| " + rows[i].map(cell).join(" | ") + " |");
    }
    return out.join("\n");
  }

  function fence(text, lang) {
    var body = (typeof text === "string" && text.length)
      ? text.replace(/\s+$/, "")
      : "(source unavailable)";
    var tick = "```";
    /* Widen the fence if the body itself contains a fence. */
    while (body.indexOf(tick) !== -1) tick += "`";
    return tick + (lang || "") + "\n" + body + "\n" + tick;
  }

  function quote(text) {
    if (typeof text !== "string" || !text.length) return "> " + DASH;
    return text.replace(/\r?\n/g, "\n").split("\n").map(function (l) {
      return "> " + l;
    }).join("\n");
  }

  /* Sort a set of band labels into canonical depth order, unknowns last. */
  function sortBands(labels) {
    return labels.slice().sort(function (a, b) {
      var ia = BAND_ORDER.indexOf(a), ib = BAND_ORDER.indexOf(b);
      if (ia === -1 && ib === -1) return a < b ? -1 : (a > b ? 1 : 0);
      if (ia === -1) return 1;
      if (ib === -1) return -1;
      return ia - ib;
    });
  }

  function sortedKs(obj) {
    if (!obj) return [];
    return Object.keys(obj).map(Number).filter(function (n) {
      return isNum(n);
    }).sort(function (a, b) { return a - b; });
  }

  function catOrder(compObj) {
    if (!compObj) return STRUCT_CATS.slice();
    var keys = Object.keys(compObj);
    var out = [], i;
    for (i = 0; i < STRUCT_CATS.length; i++) {
      if (keys.indexOf(STRUCT_CATS[i]) !== -1) out.push(STRUCT_CATS[i]);
    }
    for (i = 0; i < keys.length; i++) {
      if (out.indexOf(keys[i]) === -1) out.push(keys[i]);
    }
    return out;
  }

  /* ------------------------------------------------------------------ *
   * Context normalisation
   * ------------------------------------------------------------------ */

  function normCtx(ctx) {
    ctx = ctx || {};
    var data = ctx.data || {};
    var summary = ctx.summary || {};
    var manifest = ctx.manifest || {};
    var state = ctx.state || {};
    var exps = data.experiments || {};

    var ranking = ctx.ranking || data.ranking || DASH;

    /* Universe: the viewer's choice if this ranking actually has it,
     * otherwise the declared reference universe, otherwise whatever exists. */
    var wanted = state.universe;
    var universe = null;
    if (wanted && exps[wanted]) universe = wanted;
    var refU = manifest.reference_universe || summary.reference_universe || null;
    if (!universe && refU && exps[refU]) universe = refU;
    if (!universe) {
      var keys = Object.keys(exps);
      universe = keys.length ? keys[0] : (wanted || refU || DASH);
    }

    var ks = summary.ks || manifest.ks || [1, 2, 4, 8];
    var lanes = summary.lanes || manifest.lanes || [];

    var lane = state.lane;
    var k = state.k;

    return {
      ranking: ranking,
      data: data,
      summary: summary,
      definitions: ctx.definitions || {},
      manifest: manifest,
      vibe: ctx.vibe || null,
      sweep: ctx.sweep || null,
      state: { universe: state.universe, lane: lane, k: k },
      universe: universe,
      universeFellBack: !!(wanted && wanted !== universe),
      exp: exps[universe] || null,
      exps: exps,
      ks: ks,
      lanes: lanes
    };
  }

  /* ------------------------------------------------------------------ *
   * Section 1 -- identity
   * ------------------------------------------------------------------ */

  function secHeader(C, out) {
    var m = C.manifest, s = C.summary, d = C.data, e = C.exp;
    var doc = get(d, "spec.doc", null) || get(s, "rankings." + C.ranking + ".doc", null);
    var family = get(d, "spec.family", null) || get(d, "family", null) ||
                 get(s, "rankings." + C.ranking + ".family", null);

    out.push("# MathMap ranking report: `" + tx(C.ranking) + "`");
    out.push("");
    out.push("**" + oneline(doc) + "**");
    out.push("");
    out.push("This report is about ONE ranking, `" + tx(C.ranking) + "`, on ONE universe, `" +
             tx(C.universe) + "`. MathMap ranks the citations inside each Mathlib " +
             "proof by how KEY each citation is to that proof. Everything below " +
             "either describes that ranking or describes the slice of it the " +
             "viewer had on screen, and the two are kept in separate sections.");
    out.push("");

    out.push(table(
      ["Field", "Value"],
      [
        ["Ranking", code(C.ranking)],
        ["Family", tx(family)],
        ["Universe (experiment identity)", code(C.universe)],
        ["Reference universe", code(m.reference_universe || s.reference_universe)],
        ["Candidates in universe", iv(get(e, "n_candidates", null))],
        ["Proofs in universe", iv(get(e, "n_proofs", null))],
        ["Proofs with source provenance", iv(get(e, "n_proofs_with_provenance", null))],
        ["Labelled proofs (semantic panel)", iv(m.n_labelled_proofs)],
        ["Graded candidate labels", iv(m.n_labels)],
        ["Rater files", iv(m.n_rater_files)],
        ["Data built", tx(m.built)],
        ["Git rev", code(m.git)],
        ["Report generator", "report.js v" + VERSION]
      ]
    ));
    out.push("");

    if (C.universeFellBack) {
      out.push("> Note: the viewer's universe `" + tx(C.state.universe) +
               "` is not present in this ranking's payload; the report fell back to `" +
               tx(C.universe) + "`.");
      out.push("");
    }

    var complexity = get(d, "spec.complexity", null);
    if (complexity && typeof complexity === "object") {
      var crows = Object.keys(complexity).map(function (kk) {
        return [code(kk), tx(complexity[kk])];
      });
      if (crows.length) {
        out.push("Declared complexity of the scoring function:");
        out.push("");
        out.push(table(["Property", "Value"], crows));
        out.push("");
      }
    }

    out.push("### Reading the numbers");
    out.push("");
    out.push("- Proportions are printed to three decimals. Shares carry `(k/n)` " +
             "and, where the exporter computed one, a 95% Wilson interval.");
    out.push("- A dash (" + DASH + ") means the field was absent or null in the " +
             "exported JSON. It never means zero.");
    out.push("- `Source*` metrics measure agreement with what the human author " +
             "wrote. **They are not keyness.**");
    out.push("- `Semantic*` metrics come from graded rater labels on a small " +
             "panel. **Differences smaller than the printed intervals are not real.**");
    out.push("- `Role*` / structural composition describes what our own classifier " +
             "says is sitting at a rank. It is a statistic, not a judgement.");
    out.push("");

    /* Candidate coverage: a property of the universe, not of the ranking. */
    var cov = get(e, "coverage", null) || get(s, "coverage." + C.universe, null);
    if (cov && typeof cov === "object") {
      out.push("### Candidate coverage of universe `" + tx(C.universe) +
               "` (property of candidate generation, NOT of this ranking)");
      out.push("");
      out.push(tx(get(C.definitions, "metric_families.Coverage*",
                      "Coverage* is a property of candidate generation.")));
      out.push("");
      var ckeys = Object.keys(cov).filter(function (kk) { return kk !== "ALL"; }).sort();
      if (cov.ALL) ckeys.push("ALL");
      out.push(table(
        ["Declaration kind", "Written by humans", "In record", "In universe",
         "CoverageInUniverse"],
        ckeys.map(function (kk) {
          var r = cov[kk] || {};
          return [kk === "ALL" ? "**ALL**" : kk, iv(r.written), iv(r.in_record),
                  iv(r.in_universe), fx(r.CoverageInUniverse)];
        })
      ));
      out.push("");
    }
  }

  /* ------------------------------------------------------------------ *
   * Section 2 -- how the ranking is constructed
   * ------------------------------------------------------------------ */

  function secConstruction(C, out) {
    var spec = get(C.data, "spec", {}) || {};
    var defs = C.definitions || {};
    var signals = defs.signals || {};
    var src = typeof spec.source === "string" ? spec.source : "";

    /* Subsections are numbered as they are emitted, so an absent optional
     * input leaves no gap in the numbering. */
    var sub = 0;
    function h(title) { sub += 1; return "### 2." + sub + " " + title; }

    out.push("## 2. How this ranking is constructed");
    out.push("");
    out.push("Everything needed to rebuild `" + tx(C.ranking) + "` from the " +
             "incidence record is in this section: the literal scoring source, " +
             "the sort semantics, and the definition of every signal it reads. " +
             "There are no hidden constants, no name lists and no learned " +
             "parameters in any ranking in this study.");
    out.push("");

    out.push(h("Literal source of the scoring function"));
    out.push("");
    out.push(fence(src, "python"));
    out.push("");

    out.push(h("Sort semantics"));
    out.push("");
    out.push(quote(tx(spec.sort_semantics)));
    out.push("");

    out.push(h("Signals read by this source"));
    out.push("");

    /* Which documented signals appear literally in the source. */
    var used = [], k;
    for (k in signals) {
      if (Object.prototype.hasOwnProperty.call(signals, k) &&
          src.indexOf(k) !== -1) {
        used.push(k);
      }
    }
    used.sort();

    if (used.length) {
      out.push(table(
        ["Signal", "Definition (verbatim from `definitions.signals`)"],
        used.map(function (s) { return [code(s), tx(signals[s])]; })
      ));
    } else {
      out.push("_No entry in `definitions.signals` matches any token in this " +
               "source._");
    }
    out.push("");

    /* Corpus attributes referenced but not documented -- flagged, never
     * invented. */
    var refs = {}, m, re = /\bc\.([A-Za-z_][A-Za-z0-9_]*)/g;
    while ((m = re.exec(src)) !== null) refs[m[1]] = 1;
    var undoc = Object.keys(refs).filter(function (r) {
      return !signals[r] && !PLUMBING[r];
    }).sort();
    var plumb = Object.keys(refs).filter(function (r) {
      return !signals[r] && PLUMBING[r];
    }).sort();

    if (undoc.length) {
      out.push("**Referenced by the source but carrying no entry in " +
               "`definitions.signals`.** These are real inputs to the score and " +
               "must be resolved against the corpus code before claiming a full " +
               "reproduction; this report will not invent a definition for them.");
      out.push("");
      out.push(table(
        ["Corpus attribute", "Status"],
        undoc.map(function (r) {
          return [code("c." + r), "No entry in `definitions.signals`"];
        })
      ));
      out.push("");
    }
    if (plumb.length) {
      out.push("Indexing plumbing referenced by the source (lookup arrays, not " +
               "scoring signals): " +
               plumb.map(function (r) { return code("c." + r); }).join(", ") + ".");
      out.push("");
    }

    /* Pipeline, verbatim. */
    var pipeline = get(defs, "how_a_run_is_built.pipeline", null);
    if (pipeline && pipeline.length) {
      out.push(h("How a run is built (verbatim from `definitions`)"));
      out.push("");
      for (var i = 0; i < pipeline.length; i++) {
        /* The exported strings already begin "1. ", "2. "; do not number twice. */
        out.push("" + (i + 1) + ". " +
                 tx(pipeline[i]).replace(/^\s*\d+\.\s*/, ""));
      }
      out.push("");
    }
    var repro = get(defs, "how_a_run_is_built.reproducing_a_ranking", null);
    if (repro) {
      out.push(quote(tx(repro)));
      out.push("");
    }

    /* Universe definition, since it is part of experiment identity. */
    var udoc = get(defs, "universes." + C.universe, null);
    if (udoc) {
      out.push(h("The universe this experiment ran on"));
      out.push("");
      out.push("`" + tx(C.universe) + "` " + DASH + " " + tx(udoc));
      out.push("");
      var unote = get(defs, "universes._note", null);
      if (unote) {
        out.push(quote(tx(unote)));
        out.push("");
      }
    }

    /* Ties: a property of the score itself. */
    var ties = get(C.exp, "ranking_quality.ties", null);
    if (ties) {
      out.push(h("Tie structure of the score (property of the ranking)"));
      out.push("");
      out.push("Where the score ties, order falls back to a stable identifier. " +
               "That is reproducible but not meaningful, so the size of the tied " +
               "blocks bounds how much of the observed order is actually the " +
               "ranking's doing.");
      out.push("");
      out.push(table(
        ["Statistic", "Value"],
        [
          ["Distinct score levels (sampled)", iv(ties.distinct_levels)],
          ["Median tie block", fx(ties.median_tie_block, 1)],
          ["p90 tie block", fx(ties.p90_tie_block, 1)],
          ["Max tie block", iv(ties.max_tie_block)],
          ["Approx. fraction of pairs tied", fx(ties.approx_frac_pairs_tied, 6)],
          ["Candidates sampled", iv(ties.sampled)]
        ]
      ));
      out.push("");
    }
  }

  /* ------------------------------------------------------------------ *
   * Section 3 -- ranking quality (invariant)
   * ------------------------------------------------------------------ */

  function secSemantic(C, out) {
    var rq = get(C.exp, "ranking_quality", null);
    var sem = get(rq, "semantic", null);
    var defs = C.definitions || {};

    out.push("## 3. Ranking quality: semantic scorecard (INVARIANT under the " +
             "display controls)");
    out.push("");
    out.push("**Everything in this section is a property of the RANKING on " +
             "universe `" + tx(C.universe) + "`, computed over the full ranked " +
             "universe. None of it moves when the viewer changes lane or k.** " +
             "Changing the universe does re-rank, which is why the universe is " +
             "part of the experiment's identity and the lane and k are not.");
    out.push("");
    out.push(quote(tx(get(defs, "metric_families.Semantic*",
      "Semantic* comes from graded rater labels. Small n; every figure carries " +
      "its n and a 95% Wilson interval."))));
    out.push("");

    if (!sem) {
      out.push("_No semantic scorecard present in this payload._");
      out.push("");
      return;
    }

    var n = sem.n_proofs_scored;
    out.push("Panel size: **n = " + iv(n) + " proofs scored** at rank 1. " +
             "**Any difference smaller than the 95% intervals below is not real.**");
    out.push("");

    /* 3.1 grade composition at rank 1 */
    out.push("### 3.1 Grade composition at rank 1");
    out.push("");
    var shareObj = {
      KEY: sem.SemanticKeyMoveAt1,
      LEGIT_GLUE: sem.SemanticLegitGlueAt1,
      BAD_GLUE: sem.SemanticBadGlueAt1,
      JUNK: sem.SemanticJunkAt1
    };
    var gradeDefs = defs.grades || {};
    function gradeDoc(name) {
      var want = GRADE_CODE[name] + " " + name;
      if (gradeDefs[want]) return gradeDefs[want];
      var kk;
      for (kk in gradeDefs) {
        if (kk.indexOf(name) !== -1) return gradeDefs[kk];
      }
      return null;
    }
    var derived = false;
    var rows = GRADE_ORDER.map(function (g) {
      var o = shareObj[g];
      var share = o ? o.value : get(sem, "grade_at_1." + g, null);
      var kk = o ? o.k : (isNum(share) && isNum(n) ? Math.round(share * n) : null);
      var nn = o ? o.n : n;
      var ci = o ? o.ci95 : null;
      var flag = "";
      if (!ci) {
        ci = wilson(kk, nn);
        if (ci) { flag = " *"; derived = true; }
      }
      return [
        String(GRADE_CODE[g]) + " " + g + flag,
        fx(share),
        (isNum(kk) && isNum(nn)) ? iv(kk) + "/" + iv(nn) : DASH,
        ciStr(ci),
        tx(gradeDoc(g))
      ];
    });
    out.push(table(["Grade", "Share at rank 1", "k/n", "95% Wilson CI",
                    "What the grade means"], rows));
    out.push("");
    if (derived) {
      out.push("`*` the exporter does not precompute an interval for this row; " +
               "the report computed it with the same Wilson formula " +
               "(`mathmap_eval.composition._wilson`, z = 1.96) from the printed " +
               "k and n.");
      out.push("");
    }

    /* 3.2 headline */
    out.push("### 3.2 Headline figures");
    out.push("");
    out.push(table(
      ["Metric", "Value", "95% CI", "k/n", "What it means"],
      [
        ["SemanticBadAt1 (**headline failure rate**)",
         fx(get(sem, "SemanticBadAt1.value", null)),
         ciStr(get(sem, "SemanticBadAt1.ci95", null)),
         knStr(sem.SemanticBadAt1),
         tx(get(defs, "headline_metrics.SemanticBadAt1", null))],
        ["SemanticKeyMoveAt1",
         fx(get(sem, "SemanticKeyMoveAt1.value", null)),
         ciStr(get(sem, "SemanticKeyMoveAt1.ci95", null)),
         knStr(sem.SemanticKeyMoveAt1),
         tx(get(defs, "headline_metrics.SemanticKeyMoveAt1", null))],
        ["SemanticKeyOrSupportAt1",
         fx(get(sem, "SemanticKeyOrSupportAt1.value", null)),
         ciStr(get(sem, "SemanticKeyOrSupportAt1.ci95", null)),
         knStr(sem.SemanticKeyOrSupportAt1),
         "Rank-1 item graded 4 or 3: real mathematical content, key or secondary."],
        ["SemanticLegitGlueAt1",
         fx(get(sem, "SemanticLegitGlueAt1.value", null)),
         ciStr(get(sem, "SemanticLegitGlueAt1.ci95", null)),
         knStr(sem.SemanticLegitGlueAt1),
         tx(get(defs, "headline_metrics.SemanticLegitGlueAt1", null))],
        ["SemanticBadGlueAt1",
         fx(get(sem, "SemanticBadGlueAt1.value", null)),
         ciStr(get(sem, "SemanticBadGlueAt1.ci95", null)),
         knStr(sem.SemanticBadGlueAt1),
         tx(get(defs, "headline_metrics.SemanticBadGlueAt1", null))],
        ["SemanticJunkAt1",
         fx(get(sem, "SemanticJunkAt1.value", null)),
         ciStr(get(sem, "SemanticJunkAt1.ci95", null)),
         knStr(sem.SemanticJunkAt1),
         tx(get(defs, "headline_metrics.SemanticJunkAt1", null))],
        ["SemanticMeanGradeAt1",
         fx(sem.SemanticMeanGradeAt1, 3), DASH,
         isNum(n) ? "n = " + iv(n) : DASH,
         "Mean of the 0-4 grade of the rank-1 item. Not a proportion, so no " +
         "Wilson interval applies."]
      ]
    ));
    out.push("");
    out.push("The separation of `SemanticLegitGlueAt1` from `SemanticBadGlueAt1` " +
             "is the entire reason the graded panel exists: the structural " +
             "channel in section 4 can see that glue is at rank 1 but cannot " +
             "say whether that glue is wrong.");
    out.push("");

    /* 3.3 recall */
    out.push("### 3.3 KeyMoveRecall at k");
    out.push("");
    out.push(tx(get(defs, "headline_metrics.SemanticKeyMoveRecall@k",
      "Of all candidates graded KEY in a proof, the share appearing in the top k.")));
    out.push("");
    var ks = C.ks || [1, 2, 4, 8];
    out.push(table(
      ["k", "SemanticKeyMoveRecall@k", "SemanticKeyOrSupportRecall@k"],
      ks.map(function (kk) {
        return [String(kk),
                fx(sem["SemanticKeyMoveRecall@" + kk]),
                fx(sem["SemanticKeyOrSupportRecall@" + kk])];
      })
    ));
    out.push("");
    out.push("These are means over proofs of a per-proof recall, so they carry no " +
             "single k/n and no Wilson interval; they are averaged over the " +
             "proofs that have at least one graded KEY. Read them against the " +
             "same n = " + iv(n) + " panel.");
    out.push("");

    var klp = sem.SemanticKeyLostToPolicy;
    if (klp) {
      out.push("**SemanticKeyLostToPolicy** (candidate-generation loss, not a " +
               "ranking failure and not a lane effect): " + fx(klp.value) +
               " (" + knStr(klp) + "). Of all candidates graded KEY, this is the " +
               "share universe `" + tx(C.universe) + "` never offered to the " +
               "ranking at all. A ranking cannot be blamed for a candidate it " +
               "was never shown.");
      out.push("");
    }

    /* 3.4 by depth band */
    out.push("### 3.4 Semantic scorecard by target-depth band");
    out.push("");
    out.push("Target depth is the depth of the theorem being proved. Per-band n " +
             "is small; the `SemanticBadAt1` interval is printed for each band so " +
             "that band-to-band differences are not over-read.");
    out.push("");
    var bd = sem.by_target_depth || {};
    var bands = sortBands(Object.keys(bd));
    out.push(table(
      ["Depth band", "n", "KEY", "SUPPORT", "LEGIT_GLUE", "BAD_GLUE", "JUNK",
       "BadAt1", "BadAt1 95% CI", "Mean grade"],
      bands.map(function (b) {
        var r = bd[b] || {};
        var g = r.grade_at_1 || {};
        return [b, iv(r.n), fx(g.KEY), fx(g.SUPPORT), fx(g.LEGIT_GLUE),
                fx(g.BAD_GLUE), fx(g.JUNK), fx(r.SemanticBadAt1),
                ciStr(r.ci95_bad), fx(r.SemanticMeanGradeAt1, 3)];
      })
    ));
    out.push("");
    out.push("KeyMoveRecall by band:");
    out.push("");
    out.push(table(
      ["Depth band", "n"].concat(ks.map(function (kk) {
        return "Recall@" + kk;
      })),
      bands.map(function (b) {
        var r = bd[b] || {};
        return [b, iv(r.n)].concat(ks.map(function (kk) {
          return fx(r["SemanticKeyMoveRecall@" + kk]);
        }));
      })
    ));
    out.push("");

    /* 3.5 the measuring instrument */
    var meta = get(C.summary, "labels.meta", null);
    var agree = get(C.summary, "labels.agreement", null);
    var glue = get(C.summary, "labels.glue_classifier", null);
    if (meta || agree || glue) {
      out.push("### 3.5 The measuring instrument itself");
      out.push("");
      out.push("These describe the label set and our own glue classifier, not " +
               "this ranking. They bound how much any `Semantic*` number above " +
               "can be trusted.");
      out.push("");
    }
    if (meta) {
      out.push("**Label set**");
      out.push("");
      out.push(table(
        ["Field", "Value"],
        [
          ["Raters", Array.isArray(meta.raters) ? meta.raters.join(", ") : tx(meta.raters)],
          ["Rater files", iv(meta.n_rater_files)],
          ["Proofs labelled", iv(meta.n_proofs_labelled)],
          ["Candidate labels", iv(meta.n_incidences_labelled)],
          ["Multi-rated candidates", iv(meta.n_multi_rated)],
          ["Mean spread on multi-rated", fx(meta.mean_spread_multi_rated, 3)],
          ["Missing-key rate", fx(meta.missing_key_rate, 3)],
          ["Confidence histogram",
           meta.confidence ? Object.keys(meta.confidence).map(function (kk) {
             return kk + ": " + iv(meta.confidence[kk]);
           }).join(", ") : DASH]
        ]
      ));
      out.push("");
      out.push("Where several raters graded the same candidate the MEDIAN grade " +
               "is used and the spread is reported, so a disputed label is never " +
               "silently averaged into a clean-looking number.");
      out.push("");
    }
    if (agree) {
      out.push("**Rater agreement on the 0-4 rubric**");
      out.push("");
      out.push(table(
        ["Statistic", "Value"],
        [
          ["Overlap candidates", iv(agree.n_overlap_candidates)],
          ["Rater pairs", iv(agree.n_pairs)],
          ["Exact agreement", fx(agree.ExactAgreement)],
          ["Adjacent agreement (|diff| <= 1)", fx(agree.AdjacentAgreement)],
          ["Mean absolute difference", fx(agree.MeanAbsDiff, 3)],
          ["Quadratic-weighted kappa", fx(agree.QuadraticWeightedKappa, 3)]
        ]
      ));
      out.push("");
    }
    if (glue && glue.GluePrecision) {
      out.push("**Our own glue classifier, judged against the graded labels**");
      out.push("");
      out.push(table(
        ["Metric", "Value", "95% CI", "k/n", "What it means"],
        [
          ["GluePrecision", fx(get(glue, "GluePrecision.value", null)),
           ciStr(get(glue, "GluePrecision.ci95", null)), knStr(glue.GluePrecision),
           tx(get(C.definitions, "headline_metrics.GluePrecision", null))],
          ["GlueRecall", fx(get(glue, "GlueRecall.value", null)),
           ciStr(get(glue, "GlueRecall.ci95", null)), knStr(glue.GlueRecall),
           tx(get(C.definitions, "headline_metrics.GlueRecall", null))],
          ["GlueF1", fx(glue.GlueF1), DASH, DASH, "Harmonic mean of the two above."],
          ["KeyMovesFlaggedAsGlue",
           fx(get(glue, "KeyMovesFlaggedAsGlue.value", null)),
           ciStr(get(glue, "KeyMovesFlaggedAsGlue.ci95", null)),
           knStr(glue.KeyMovesFlaggedAsGlue),
           tx(get(C.definitions, "headline_metrics.KeyMovesFlaggedAsGlue", null))]
        ]
      ));
      out.push("");
      var conf = glue.confusion_by_grade;
      if (conf) {
        out.push("Confusion of the glue flag against grade, over " +
                 iv(glue.n_labelled_candidates) + " labelled candidates:");
        out.push("");
        out.push(table(
          ["Grade", "n labelled", "flagged glue by system", "flagged machinery by system"],
          GRADE_ORDER.filter(function (g) { return conf[g]; }).map(function (g) {
            var r = conf[g];
            return [String(GRADE_CODE[g]) + " " + g, iv(r.n), iv(r.system_glue),
                    iv(r.system_machinery)];
          })
        ));
        out.push("");
      }
    }
  }

  /* ------------------------------------------------------------------ *
   * Section 4 -- structural rank composition
   * ------------------------------------------------------------------ */

  function secStructural(C, out) {
    var comp = get(C.exp, "ranking_quality.composition", null);
    var defs = C.definitions || {};

    out.push("## 4. Structural rank composition (INVARIANT, full corpus)");
    out.push("");
    out.push("**Also a property of the RANKING, not of the displayed slice.** " +
             "This is our own classifier's description of what sits at each rank " +
             "prefix, over every proof in the corpus, so n is huge and the depth " +
             "breakdown is exact.");
    out.push("");
    out.push("> **Caveat, and it is the important one: this channel can say " +
             "\"there is glue at rank 1\". It cannot say \"that glue is wrong.\"** " +
             "Some plumbing genuinely is the content of a proof near the " +
             "foundations. Only the graded panel in section 3 separates " +
             "LEGIT_GLUE from BAD_GLUE.");
    out.push("");
    out.push(quote(tx(get(defs, "metric_families.Role*",
      "Role* is a descriptive composition of what our OWN classifier says is " +
      "sitting at a rank. A statistic, not a judgement."))));
    out.push("");

    if (!comp) {
      out.push("_No structural composition present in this payload._");
      out.push("");
      return;
    }

    var glueDoc = get(defs, "headline_metrics.RoleGlueAt1", null);
    out.push("Proofs covered: **" + iv(comp.n_proofs) + "**. Headline " +
             "`RoleGlueAt1` = **" + fx(comp.RoleGlueAt1) + "**" +
             (glueDoc ? " " + DASH + " " + tx(glueDoc) : "") + ".");
    out.push("");

    var atk = comp.at_k || {};
    var ks = sortedKs(atk);
    var cats = catOrder(get(atk, String(ks[0]) + ".composition", null));

    out.push("### 4.1 Composition of the top-k prefix, whole corpus");
    out.push("");
    out.push(table(
      ["k", "items ranked"].concat(cats).concat(["glue (machinery + logic-glue)"]),
      ks.map(function (kk) {
        var a = atk[String(kk)] || atk[kk] || {};
        var cc = a.composition || {};
        return [String(kk), iv(a.n_items)].concat(cats.map(function (cat) {
          return pc(cc[cat]);
        })).concat([pc(a.glue)]);
      })
    ));
    out.push("");

    out.push("### 4.2 Composition at rank 1, by target-depth band");
    out.push("");
    var a1 = atk["1"] || atk[1] || {};
    var bd1 = a1.by_target_depth || {};
    var b1 = sortBands(Object.keys(bd1));
    out.push(table(
      ["Depth band", "items"].concat(cats).concat(["glue"]),
      b1.map(function (b) {
        var r = bd1[b] || {};
        return [b, iv(r.n)].concat(cats.map(function (cat) {
          return pc(r[cat]);
        })).concat([pc(r.glue)]);
      })
    ));
    out.push("");

    out.push("### 4.3 Glue share by depth band across every k");
    out.push("");
    var allBands = [];
    ks.forEach(function (kk) {
      var a = atk[String(kk)] || atk[kk] || {};
      Object.keys(a.by_target_depth || {}).forEach(function (b) {
        if (allBands.indexOf(b) === -1) allBands.push(b);
      });
    });
    allBands = sortBands(allBands);
    out.push(table(
      ["Depth band"].concat(ks.map(function (kk) { return "glue @ k=" + kk; }))
        .concat(ks.map(function (kk) { return "items @ k=" + kk; })),
      allBands.map(function (b) {
        var row = [b];
        ks.forEach(function (kk) {
          var a = atk[String(kk)] || atk[kk] || {};
          row.push(pc(get((a.by_target_depth || {})[b] || {}, "glue", null)));
        });
        ks.forEach(function (kk) {
          var a = atk[String(kk)] || atk[kk] || {};
          row.push(iv(get((a.by_target_depth || {})[b] || {}, "n", null)));
        });
        return row;
      })
    ));
    out.push("");
    out.push("Structural headline breakdown at rank 1: machinery " +
             pc(comp.RoleMachineryAt1) + ", theorem " + pc(comp.RoleTheoremAt1) +
             ", definition/construction " + pc(comp.RoleDefinitionAt1) + ".");
    out.push("");
  }

  /* ------------------------------------------------------------------ *
   * Section 5 -- named failures
   * ------------------------------------------------------------------ */

  function secFailures(C, out) {
    var sem = get(C.exp, "ranking_quality.semantic", null);

    out.push("## 5. What it got wrong, named (INVARIANT)");
    out.push("");
    out.push("The most actionable section. Every row is a specific proof and a " +
             "specific declaration, drawn from the graded panel, so each one can " +
             "be opened in Mathlib and argued about. Nothing here is truncated " +
             "beyond the cap the exporter itself applies.");
    out.push("");

    if (!sem) {
      out.push("_No semantic diagnostics present in this payload._");
      out.push("");
      return;
    }

    var wm = sem.worst_misses || [];
    out.push("### 5.1 Worst misses " + DASH + " graded KEY (4), buried by this ranking");
    out.push("");
    out.push("A rater called these core moves of the proof and this ranking put " +
             "them at rank 4 or worse. Sorted by how deeply they were buried " +
             "relative to how many candidates the proof had. **" + iv(wm.length) +
             " rows.**");
    out.push("");
    out.push(table(
      ["#", "Proof", "Theorem", "Buried declaration", "Rank", "of", "Depth band",
       "Target depth", "Grade"],
      wm.map(function (r, i) {
        return [String(i + 1), tx(r.proof), code(r.theorem), code(r.name),
                iv(r.rank), iv(r.of), tx(r.band), iv(r.target_depth),
                (isNum(r.grade) ? String(r.grade) + " KEY" : DASH)];
      })
    ));
    out.push("");

    var fp = sem.false_promotions || [];
    out.push("### 5.2 False promotions " + DASH + " graded BAD_GLUE (1) or JUNK (0) at rank 1");
    out.push("");
    out.push("This ranking put these at the very top of their proof and a rater " +
             "said they carry no idea (1) or are irrelevant machinery (0). " +
             "`best available` is the highest grade the proof actually offered, " +
             "so a row with `best available = 4` is a proof where a core move was " +
             "sitting right there and was passed over. `system says glue` is our " +
             "own classifier's opinion: where it reads `no`, the glue channel " +
             "would not have caught this. **" + iv(fp.length) + " rows.**");
    out.push("");
    out.push(table(
      ["#", "Proof", "Theorem", "Promoted declaration", "Grade", "Best available",
       "System says glue", "Depth band", "Target depth"],
      fp.map(function (r, i) {
        return [String(i + 1), tx(r.proof), code(r.theorem), code(r.name),
                (isNum(r.grade) ? String(r.grade) + " " + tx(r.grade_name) : tx(r.grade_name)),
                iv(r.best_available_grade),
                (r.system_says_glue === undefined || r.system_says_glue === null)
                  ? DASH : (r.system_says_glue ? "yes" : "no"),
                tx(r.band), iv(r.target_depth)];
      })
    ));
    out.push("");
    var missed = fp.filter(function (r) { return r.best_available_grade === 4; }).length;
    var uncaught = fp.filter(function (r) { return r.system_says_glue === false; }).length;
    if (fp.length) {
      out.push("Of the " + iv(fp.length) + " false promotions listed, " +
               iv(missed) + " occurred in a proof that had a graded KEY " +
               "available, and " + iv(uncaught) + " were NOT flagged as glue by " +
               "our own classifier " + DASH + " that second number is the part " +
               "the structural channel in section 4 is blind to.");
      out.push("");
    }
  }

  /* ------------------------------------------------------------------ *
   * Section 6 -- source agreement
   * ------------------------------------------------------------------ */

  function secSource(C, out) {
    var src = get(C.exp, "ranking_quality.source", null);
    var defs = C.definitions || {};

    out.push("## 6. Source agreement (INVARIANT) " + DASH +
             " NOT a measure of keyness");
    out.push("");
    out.push("> **`Source*` measures agreement with the identifiers the human " +
             "author actually wrote. It is not keyness and this ranking may not " +
             "be promoted on it.**");
    out.push("");
    out.push(quote(tx(get(defs, "metric_families.Source*",
      "Agreement with the identifiers the human author actually wrote. THIS IS " +
      "NOT KEYNESS. A ranking may not be promoted on it."))));
    out.push("");

    if (!src) {
      out.push("_No source-agreement metrics present in this payload._");
      out.push("");
      return;
    }

    out.push("Measured on **" + iv(src.n_proofs) + " proofs with source " +
             "provenance** in universe `" + tx(C.universe) + "`.");
    out.push("");
    var ks = C.ks || [1, 2, 4, 8];
    out.push(table(
      ["Metric (authorship agreement, NOT keyness)", "Value"],
      [["SourceHit@1", fx(src["SourceHit@1"])],
       ["SourceMRR", fx(src.SourceMRR)]].concat(ks.map(function (kk) {
        return ["SourceRecall@" + kk, fx(src["SourceRecall@" + kk])];
      }))
    ));
    out.push("");

    var bd = src.by_target_depth || {};
    var bands = sortBands(Object.keys(bd));
    out.push("By target-depth band (still authorship agreement, still not keyness):");
    out.push("");
    out.push(table(
      ["Depth band", "n proofs", "SourceHit@1", "SourceRecall@4"],
      bands.map(function (b) {
        var r = bd[b] || {};
        return [b, iv(r.n), fx(r["SourceHit@1"]), fx(r["SourceRecall@4"])];
      })
    ));
    out.push("");
    out.push("Two reasons not to difference these against section 3. First, the " +
             "SourceOracle " + DASH + " which by construction ranks the author's " +
             "own citations first " + DASH + " scores only 0.619 on semantic " +
             "keyness and is beaten there by several candidate rankings, so " +
             "authorship agreement and keyness are demonstrably different " +
             "targets. Second, the labelled panel and the provenance set are " +
             "almost disjoint samples (see the cautions in section 9).");
    out.push("");
  }

  /* ------------------------------------------------------------------ *
   * Section 7 -- current view (slice-dependent)
   * ------------------------------------------------------------------ */

  function secView(C, out) {
    var exp = C.exp;
    var views = get(exp, "views", {}) || {};
    var lane = C.state.lane;
    var k = C.state.k;
    var defs = C.definitions || {};
    var laneDoc = get(C.manifest, "lane_doc." + lane, null) ||
                  get(defs, "lanes." + lane, null);

    out.push("## 7. Current view (SLICE-DEPENDENT " + DASH +
             " these numbers move when you move the controls)");
    out.push("");
    out.push("**Nothing in this section is a property of the ranking.** A view " +
             "never re-orders anything: the lane hides rows from the " +
             "already-ranked list and k takes the first k survivors. Every figure here " +
             "changes the moment the viewer touches lane or k, and that is its " +
             "entire purpose.");
    out.push("");
    out.push(quote(tx(get(defs, "metric_families.Graph*/View*",
      "Structure and content of the currently displayed slice. These MOVE when " +
      "you change lane or k. They say nothing about ranking quality."))));
    out.push("");

    out.push("### 7.1 Viewer state at export time");
    out.push("");
    out.push(table(
      ["Control", "Value", "Kind of control"],
      [
        ["universe", code(C.state.universe === undefined ? C.universe : C.state.universe),
         "EXPERIMENT control " + DASH + " changing it genuinely re-ranks"],
        ["lane", code(lane), "DISPLAY control " + DASH + " hides rows only"],
        ["k", code(k), "DISPLAY control " + DASH + " takes the first k survivors"]
      ]
    ));
    out.push("");
    if (laneDoc) {
      out.push("Lane `" + tx(lane) + "`: " + tx(laneDoc));
      out.push("");
    }

    var haveControls = (lane !== undefined && lane !== null && lane !== "") &&
                       (k !== undefined && k !== null && k !== "");
    var key = haveControls ? (String(lane) + "|" + String(k)) : null;
    var v = key ? views[key] : null;
    if (!v) {
      out.push(haveControls
        ? "_No view recorded for `" + cell(key) + "` in this payload._"
        : "_The viewer state carried no lane and/or k, so no slice can be " +
          "identified._");
      out.push("");
      out.push("Available views: " +
               (Object.keys(views).length
                 ? Object.keys(views).slice(0, 40).map(code).join(", ")
                 : DASH) + ".");
      out.push("");
      return;
    }

    out.push("### 7.2 The slice `" + tx(key) + "`");
    out.push("");
    out.push(table(
      ["Property", "Value", "Note"],
      [
        ["ViewSize", iv(v.ViewSize), "Rows visible in the slice."],
        ["ViewProofsCovered", iv(v.ViewProofsCovered),
         "Distinct proofs with at least one visible row."],
        ["ViewGlueShare", pc(v.ViewGlueShare),
         "Our classifier's glue share of the slice. Structural, not a judgement."],
        ["ViewLaneHidesOfUniverse", pc(v.ViewLaneHidesOfUniverse),
         "Fraction of the universe this lane hides from display. Nothing is " +
         "deleted from the ranking."]
      ]
    ));
    out.push("");

    var comp = v.ViewComposition || {};
    var cats = catOrder(comp);
    out.push("Composition of the slice:");
    out.push("");
    out.push(table(
      ["Category", "Share of visible rows"],
      cats.map(function (cat) { return [cat, pc(comp[cat])]; })
    ));
    out.push("");

    var kr = v.ViewKeyRetained;
    if (kr) {
      out.push("**ViewKeyRetained@" + tx(k) + "** = " + fx(kr.value) + " (" +
               knStr(kr) + "). " +
               tx(get(defs, "headline_metrics.ViewKeyRetained@k",
                      "Of candidates graded KEY, the share visible in the " +
                      "current slice.")) + " This is a VIEW property: it is the " +
               "joint effect of the ranking and the lane, and it moves with the " +
               "controls, so it must not be quoted as this ranking's recall. " +
               "The ranking's own recall is in section 3.3.");
      out.push("");
    }

    var g = v.graph;
    if (g) {
      out.push("### 7.3 Graph connectivity of the slice");
      out.push("");
      out.push("The projection induced by the visible rows only. The virtual " +
               "root is excluded.");
      out.push("");
      out.push(table(
        ["Metric", "Value"],
        [
          ["GraphEdges", iv(g.GraphEdges)],
          ["GraphComponents", iv(g.GraphComponents)],
          ["GraphGiantFraction", pc(g.GraphGiantFraction, 2)],
          ["GraphSecondLargest", iv(g.GraphSecondLargest)],
          ["GraphEntropy", fx(g.GraphEntropy, 3)],
          ["GraphSusceptibility", fx(g.GraphSusceptibility, 2)],
          ["GraphActiveNodeFraction", pc(g.GraphActiveNodeFraction, 2)]
        ]
      ));
      out.push("");
    }

    /* Same lane across all k, for context. Still slice-dependent. */
    var ks = C.ks || [1, 2, 4, 8];
    var sameLane = ks.filter(function (kk) { return views[lane + "|" + kk]; });
    if (sameLane.length > 1) {
      out.push("### 7.4 The same lane at every k (all still slice-dependent)");
      out.push("");
      out.push(table(
        ["k", "ViewSize", "ViewProofsCovered", "ViewGlueShare", "ViewKeyRetained",
         "Components", "Giant fraction"],
        sameLane.map(function (kk) {
          var vv = views[lane + "|" + kk] || {};
          var gg = vv.graph || {};
          return [String(kk) + (String(kk) === String(k) ? " (current)" : ""),
                  iv(vv.ViewSize), iv(vv.ViewProofsCovered), pc(vv.ViewGlueShare),
                  fx(get(vv, "ViewKeyRetained.value", null)),
                  iv(gg.GraphComponents), pc(gg.GraphGiantFraction, 2)];
        })
      ));
      out.push("");
    }

    /* Every lane at the current k. */
    var lanes = C.lanes || [];
    var sameK = lanes.filter(function (L) { return views[L + "|" + k]; });
    if (sameK.length > 1) {
      out.push("### 7.5 Every lane at k = " + tx(k) + " (all still slice-dependent)");
      out.push("");
      out.push(table(
        ["Lane", "Hides of universe", "ViewSize", "ViewGlueShare",
         "ViewKeyRetained", "Components"],
        sameK.map(function (L) {
          var vv = views[L + "|" + k] || {};
          var gg = vv.graph || {};
          return [L + (L === lane ? " (current)" : ""),
                  pc(vv.ViewLaneHidesOfUniverse), iv(vv.ViewSize),
                  pc(vv.ViewGlueShare),
                  fx(get(vv, "ViewKeyRetained.value", null)),
                  iv(gg.GraphComponents)];
        })
      ));
      out.push("");
      out.push("A lane that hides more will usually retain fewer KEY moves. That " +
               "trade is a policy choice about the display and says nothing about " +
               "whether the underlying order is any good.");
      out.push("");
    }
  }

  /* ------------------------------------------------------------------ *
   * Section 8 -- comparison
   * ------------------------------------------------------------------ */

  function secCompare(C, out) {
    var U = C.universe;
    var rk = get(C.summary, "rankings", null);

    out.push("## 8. Comparison with every other ranking at universe `" +
             tx(U) + "` (INVARIANT)");
    out.push("");
    out.push("Supporting context for the sections above. All rankings are " +
             "compared on the same universe, so the candidate set is identical " +
             "and the only thing that differs is the order.");
    out.push("");

    if (!rk) {
      out.push("_No summary of other rankings present._");
      out.push("");
      return;
    }

    var names = Object.keys(rk).sort();
    var rows = [];
    var recs = [];
    var i;
    for (i = 0; i < names.length; i++) {
      var nm = names[i];
      var bu = get(rk[nm], "by_universe." + U, null);
      if (!bu) continue;
      recs.push({
        name: nm,
        family: get(rk[nm], "family", null),
        doc: get(rk[nm], "doc", null),
        isThis: nm === C.ranking,
        key1: bu.SemanticKeyMoveAt1 || null,
        bad1: bu.SemanticBadAt1 || null,
        legit1: bu.SemanticLegitGlueAt1 || null,
        mean1: bu.SemanticMeanGradeAt1,
        recall: bu,
        glue1: bu.RoleGlueAt1,
        src1: bu["SourceHit@1"],
        mrr: bu.SourceMRR
      });
    }

    if (!recs.length) {
      out.push("_No ranking in the summary carries universe `" + cell(U) + "`._");
      out.push("");
      return;
    }

    var ks = C.ks || [1, 2, 4, 8];
    var byKey = recs.slice().sort(function (a, b) {
      var av = get(a, "key1.value", -1), bv = get(b, "key1.value", -1);
      return (isNum(bv) ? bv : -1) - (isNum(av) ? av : -1);
    });

    out.push("### 8.1 Semantic scorecard, all rankings (n = " +
             iv(get(recs[0], "key1.n", null)) + " graded proofs)");
    out.push("");
    out.push("Sorted by `SemanticKeyMoveAt1`, best first. The row for this " +
             "report is marked.");
    out.push("");
    for (i = 0; i < byKey.length; i++) {
      var r = byKey[i];
      rows.push([
        String(i + 1),
        (r.isThis ? "**" + r.name + "** (this report)" : r.name),
        tx(r.family),
        shareStr(r.key1),
        shareStr(r.bad1),
        fx(get(r, "legit1.value", null)),
        fx(r.mean1, 3),
        fx(r.recall["SemanticKeyMoveRecall@4"])
      ]);
    }
    out.push(table(
      ["#", "Ranking", "Family", "SemanticKeyMoveAt1 [95% CI] (k/n)",
       "SemanticBadAt1 [95% CI] (k/n)", "LegitGlue@1", "Mean grade",
       "KeyMoveRecall@4"],
      rows
    ));
    out.push("");

    out.push("### 8.2 KeyMoveRecall at every k, all rankings");
    out.push("");
    out.push(table(
      ["Ranking"].concat(ks.map(function (kk) { return "Recall@" + kk; })),
      byKey.map(function (r) {
        return [(r.isThis ? "**" + r.name + "** (this report)" : r.name)]
          .concat(ks.map(function (kk) {
            return fx(r.recall["SemanticKeyMoveRecall@" + kk]);
          }));
      })
    ));
    out.push("");

    out.push("### 8.3 Structural glue at rank 1, and source agreement");
    out.push("");
    out.push("`RoleGlueAt1` is the structural channel (full corpus, cannot say " +
             "whether the glue is wrong). `Source*` is authorship agreement and " +
             "**is not keyness**; it is printed for completeness only and no " +
             "ranking may be promoted on it.");
    out.push("");
    out.push(table(
      ["Ranking", "RoleGlueAt1 (structural, full corpus)",
       "SourceHit@1 (NOT keyness)", "SourceMRR (NOT keyness)",
       "SourceRecall@4 (NOT keyness)"],
      byKey.map(function (r) {
        return [(r.isThis ? "**" + r.name + "** (this report)" : r.name),
                fx(r.glue1), fx(r.src1), fx(r.mrr),
                fx(r.recall["SourceRecall@4"])];
      })
    ));
    out.push("");

    out.push("### 8.4 One-line doc of every ranking compared");
    out.push("");
    out.push(table(
      ["Ranking", "Family", "What it does"],
      byKey.map(function (r) {
        return [(r.isThis ? "**" + r.name + "**" : r.name), tx(r.family), tx(r.doc)];
      })
    ));
    out.push("");

    /* ---- prose verdict ---- */
    out.push("### 8.5 Where this ranking stands");
    out.push("");
    out.push(compareProse(C, byKey, U));
    out.push("");
  }

  function compareProse(C, byKey, U) {
    var i, me = null, myIdx = -1;
    for (i = 0; i < byKey.length; i++) {
      if (byKey[i].isThis) { me = byKey[i]; myIdx = i; }
    }
    var N = byKey.length;
    if (!me) {
      return "`" + tx(C.ranking) + "` does not appear in the summary at universe `" +
             tx(U) + "`, so no comparative placement can be stated.";
    }

    var s = [];
    var myKey = get(me, "key1.value", null);
    var myCi = get(me, "key1.ci95", null);
    var n = get(me, "key1.n", null);

    s.push("On `SemanticKeyMoveAt1` at universe `" + tx(U) + "`, `" +
           tx(C.ranking) + "` places **" + (myIdx + 1) + " of " + N +
           "** with " + fx(myKey) + " " + ciStr(myCi) + " on n = " + iv(n) +
           " graded proofs.");

    var best = byKey[0];
    if (best && !best.isThis) {
      var ov = ciOverlap(myCi, get(best, "key1.ci95", null));
      var gap = (isNum(get(best, "key1.value", null)) && isNum(myKey))
        ? best.key1.value - myKey : null;
      s.push("The leader is `" + best.name + "` at " +
             fx(get(best, "key1.value", null)) + " " +
             ciStr(get(best, "key1.ci95", null)) + ", a gap of " +
             (isNum(gap) ? gap.toFixed(3) : DASH) + ".");
      if (ov === true) {
        s.push("**The two 95% intervals overlap, so that gap is not resolved by " +
               "this panel** " + DASH + " on n = " + iv(n) + " the two rankings " +
               "are not distinguishable and neither should be promoted over the " +
               "other on this number.");
      } else if (ov === false) {
        s.push("The two 95% intervals do not overlap, so the gap survives the " +
               "panel's resolution.");
      } else {
        s.push("One of the two intervals is missing, so the gap cannot be tested.");
      }
    } else if (best && best.isThis) {
      var second = byKey[1];
      if (second) {
        var ov2 = ciOverlap(myCi, get(second, "key1.ci95", null));
        var gap2 = (isNum(myKey) && isNum(get(second, "key1.value", null)))
          ? myKey - second.key1.value : null;
        s.push("It is the top-scoring ranking here; the runner-up is `" +
               second.name + "` at " + fx(get(second, "key1.value", null)) + " " +
               ciStr(get(second, "key1.ci95", null)) + ", a gap of " +
               (isNum(gap2) ? gap2.toFixed(3) : DASH) + ".");
        if (ov2 === true) {
          s.push("**Those intervals overlap, so the lead is not established by " +
                 "this panel.** Being first in the table is not the same as being " +
                 "better.");
        } else if (ov2 === false) {
          s.push("Those intervals do not overlap, so the lead survives the " +
                 "panel's resolution.");
        }
      }
    }

    /* How many rankings are statistically indistinguishable from this one. */
    var tiedWith = [];
    for (i = 0; i < N; i++) {
      if (byKey[i].isThis) continue;
      if (ciOverlap(myCi, get(byKey[i], "key1.ci95", null)) === true) {
        tiedWith.push(byKey[i].name);
      }
    }
    s.push("Counting overlap of the 95% intervals, " + iv(tiedWith.length) +
           " of the other " + (N - 1) + " ranking(s) are **not distinguishable** " +
           "from `" + tx(C.ranking) + "` on `SemanticKeyMoveAt1`" +
           (tiedWith.length ? ": " + tiedWith.map(code).join(", ") : "") + ".");

    /* Failure rate placement. */
    var byBad = byKey.slice().sort(function (a, b) {
      var av = get(a, "bad1.value", 2), bv = get(b, "bad1.value", 2);
      return (isNum(av) ? av : 2) - (isNum(bv) ? bv : 2);
    });
    var badIdx = -1;
    for (i = 0; i < byBad.length; i++) if (byBad[i].isThis) badIdx = i;
    var bestBad = byBad[0];
    s.push("On the headline failure rate `SemanticBadAt1` (lower is better) it " +
           "places **" + (badIdx + 1) + " of " + N + "** with " +
           fx(get(me, "bad1.value", null)) + " " +
           ciStr(get(me, "bad1.ci95", null)) + "; the lowest failure rate in the " +
           "field is `" + tx(bestBad && bestBad.name) + "` at " +
           fx(get(bestBad, "bad1.value", null)) + " " +
           ciStr(get(bestBad, "bad1.ci95", null)) +
           (bestBad && !bestBad.isThis
             ? (ciOverlap(get(me, "bad1.ci95", null), get(bestBad, "bad1.ci95", null)) === true
                ? ", and those intervals overlap." : ", and those intervals do not overlap.")
             : "."));

    /* Source placement, explicitly quarantined. */
    var bySrc = byKey.slice().sort(function (a, b) {
      return (isNum(b.src1) ? b.src1 : -1) - (isNum(a.src1) ? a.src1 : -1);
    });
    var srcIdx = -1;
    for (i = 0; i < bySrc.length; i++) if (bySrc[i].isThis) srcIdx = i;
    s.push("For completeness, on `SourceHit@1` it places " + (srcIdx + 1) +
           " of " + N + " with " + fx(me.src1) + " " + DASH + " **but that is " +
           "agreement with what the author wrote, not keyness, and this ranking " +
           "must not be promoted or demoted on it.**");

    s.push("The panel is 180 proofs, single-rated for most of them. Read every " +
           "placement above as a statement about this panel, not about Mathlib.");

    return s.join(" ");
  }

  /* ------------------------------------------------------------------ *
   * Section 9 -- caveats, verbatim
   * ------------------------------------------------------------------ */

  function secCautions(C, out) {
    var cautions = get(C.definitions, "cautions", null);
    out.push("## 9. Caveats (verbatim from `definitions.cautions`)");
    out.push("");
    if (!cautions || !cautions.length) {
      out.push("_No cautions present in `definitions.json`._");
      out.push("");
      return;
    }
    for (var i = 0; i < cautions.length; i++) {
      out.push("" + (i + 1) + ". " + tx(cautions[i]));
    }
    out.push("");
  }

  /* ------------------------------------------------------------------ *
   * Optional appendices
   * ------------------------------------------------------------------ */

  function secVibe(C, out) {
    var vibe = C.vibe;
    if (!vibe || !vibe.proofs || !vibe.proofs.length) return;

    out.push("## 10. Appendix: worked examples (INSPECTION ONLY)");
    out.push("");
    out.push("> **The English text in this appendix is LLM-generated. It feeds no " +
             "metric anywhere in this study, it was produced after all grading " +
             "was complete, and the exporter carries a live assertion that no " +
             "metric module so much as references it. Treat it as a reading aid " +
             "and nothing else.** The grades, ranks, kinds and system categories " +
             "in these tables are real data.");
    out.push("");
    out.push("Each table shows the candidates of one graded proof in the order `" +
             tx(C.ranking) + "` put them, on universe `" + tx(C.universe) + "`.");
    out.push("");

    var orderKey = C.universe + "|" + C.ranking;
    var MAXC = 8;

    for (var i = 0; i < vibe.proofs.length; i++) {
      var p = vibe.proofs[i];
      var orders = (p.orders || {})[orderKey] || {};
      out.push("### 10." + (i + 1) + " `" + tx(p.theorem) + "`");
      out.push("");
      out.push("Proof id " + code(p.id) + " " + DASH + " depth band " +
               tx(p.band) + ", target depth " + iv(p.theorem_depth) +
               ", definition fraction " + fx(p.def_fraction) +
               ", source provenance: " + (p.has_provenance ? "yes" : "no") + ".");
      out.push("");
      if (p.statement_en_llm) {
        out.push("_Statement, LLM gloss, inspection only:_");
        out.push("");
        out.push(quote(tx(p.statement_en_llm)));
        out.push("");
      }
      if (p.proof_sketch_en_llm) {
        out.push("_Proof sketch, LLM gloss, inspection only:_");
        out.push("");
        out.push(quote(tx(p.proof_sketch_en_llm)));
        out.push("");
      }

      var cands = (p.candidates || []).slice();
      cands.sort(function (a, b) {
        var ra = get(orders[String(a.n)], "rank", null);
        var rb = get(orders[String(b.n)], "rank", null);
        if (!isNum(ra) && !isNum(rb)) return 0;
        if (!isNum(ra)) return 1;
        if (!isNum(rb)) return -1;
        return ra - rb;
      });
      var shown = cands.slice(0, MAXC);
      out.push(table(
        ["Rank", "Declaration", "Kind", "Grade", "System category",
         "System glue", "In statement", "Cited depth", "LLM gloss (inspection only)"],
        shown.map(function (cd) {
          var r = get(orders[String(cd.n)], "rank", null);
          return [
            isNum(r) ? String(r + 1) : DASH,
            code(cd.name),
            tx(cd.kind),
            (isNum(cd.grade) ? String(cd.grade) + " " + tx(cd.grade_name)
                             : tx(cd.grade_name)),
            tx(cd.system_category),
            cd.system_glue === undefined || cd.system_glue === null
              ? DASH : (cd.system_glue ? "yes" : "no"),
            cd.in_statement === undefined || cd.in_statement === null
              ? DASH : (cd.in_statement ? "yes" : "no"),
            iv(cd.cited_depth),
            clip(cd.explanation_llm, 180)
          ];
        })
      ));
      if (cands.length > shown.length) {
        out.push("");
        out.push("_" + iv(cands.length - shown.length) +
                 " further candidate(s) in this proof, ranked below the rows shown._");
      }
      out.push("");
    }
  }

  function secSweep(C, out) {
    var sw = C.sweep;
    if (!sw) return;
    out.push("## 11. Appendix: parameter sweep");
    out.push("");
    out.push("`sweep.json` is not produced by `dashboard_export.py`, so this " +
             "report does not assume a fixed shape for it and renders what it " +
             "finds. Interpret it against whatever produced it.");
    out.push("");
    if (Array.isArray(sw)) {
      var cols = [];
      sw.slice(0, 200).forEach(function (row) {
        if (row && typeof row === "object" && !Array.isArray(row)) {
          Object.keys(row).forEach(function (kk) {
            if (cols.indexOf(kk) === -1) cols.push(kk);
          });
        }
      });
      if (cols.length) {
        out.push(table(cols, sw.slice(0, 200).map(function (row) {
          return cols.map(function (kk) {
            var vv = row ? row[kk] : null;
            if (vv && typeof vv === "object") return clip(JSON.stringify(vv), 80);
            return isNum(vv) ? (Number.isInteger(vv) ? iv(vv) : fx(vv, 4)) : tx(vv);
          });
        })));
      } else {
        out.push(fence(clip(JSON.stringify(sw, null, 1), 4000), "json"));
      }
    } else if (typeof sw === "object") {
      out.push(table(["Key", "Value"], Object.keys(sw).map(function (kk) {
        var vv = sw[kk];
        if (vv && typeof vv === "object") {
          return [code(kk), clip(JSON.stringify(vv), 200)];
        }
        return [code(kk), isNum(vv) ? fx(vv, 4) : tx(vv)];
      })));
    } else {
      out.push(fence(tx(sw)));
    }
    out.push("");
  }

  function secProvenance(C, out) {
    out.push("## Appendix A: provenance of this report");
    out.push("");
    var files = get(C.manifest, "files", null);
    out.push(table(
      ["Field", "Value"],
      [
        ["Generated by", "`dashboard/report.js` v" + VERSION],
        ["Ranking", code(C.ranking)],
        ["Universe", code(C.universe)],
        ["Viewer lane at export", code(C.state.lane)],
        ["Viewer k at export", code(C.state.k)],
        ["Data built", tx(get(C.manifest, "built", null))],
        ["Git rev", code(get(C.manifest, "git", null))],
        ["Source files", files && files.length
          ? files.map(function (f) { return "`" + f + "`"; }).join(", ") : DASH],
        ["Explanations are inspection only",
         tx(get(C.manifest, "explanations_are_inspection_only", null))]
      ]
    ));
    out.push("");
    out.push("Every number above was read straight out of those JSON files. The " +
             "report computes nothing of its own except the one Wilson interval " +
             "footnoted in section 3.1, the count summaries under the failure " +
             "tables, and the interval-overlap comparisons in section 8.5.");
    out.push("");
  }

  /* ------------------------------------------------------------------ *
   * Public API
   * ------------------------------------------------------------------ */

  function build(ctx) {
    var C = normCtx(ctx);
    var out = [];

    secHeader(C, out);

    out.push("---");
    out.push("");
    out.push("## Contents");
    out.push("");
    out.push("1. Identity of this experiment (above)");
    out.push("2. How this ranking is constructed");
    out.push("3. Ranking quality: semantic scorecard " + DASH + " INVARIANT");
    out.push("4. Structural rank composition " + DASH + " INVARIANT");
    out.push("5. What it got wrong, named " + DASH + " INVARIANT");
    out.push("6. Source agreement " + DASH + " INVARIANT, and NOT keyness");
    out.push("7. Current view " + DASH + " SLICE-DEPENDENT");
    out.push("8. Comparison with every other ranking " + DASH + " INVARIANT");
    out.push("9. Caveats");
    if (C.vibe && C.vibe.proofs && C.vibe.proofs.length) {
      out.push("10. Appendix: worked examples (inspection only)");
    }
    if (C.sweep) out.push("11. Appendix: parameter sweep");
    out.push("");
    out.push("Sections 3 to 6 and section 8 are properties of the RANKING and do " +
             "not move when the viewer changes lane or k. Section 7 is the only " +
             "section describing the slice on screen. The two are never mixed.");
    out.push("");
    out.push("---");
    out.push("");

    if (!C.exp) {
      out.push("## Data missing");
      out.push("");
      out.push("No experiment payload for universe `" + cell(C.universe) +
               "` was found in this ranking's JSON, so sections 3 to 7 cannot be " +
               "produced. Available universes: " +
               (Object.keys(C.exps).length
                 ? Object.keys(C.exps).map(code).join(", ") : DASH) + ".");
      out.push("");
      secConstruction(C, out);
      secCompare(C, out);
      secCautions(C, out);
      secProvenance(C, out);
      return out.join("\n").replace(/\n{3,}/g, "\n\n") + "\n";
    }

    secConstruction(C, out);
    out.push("---");
    out.push("");
    secSemantic(C, out);
    out.push("---");
    out.push("");
    secStructural(C, out);
    out.push("---");
    out.push("");
    secFailures(C, out);
    out.push("---");
    out.push("");
    secSource(C, out);
    out.push("---");
    out.push("");
    secView(C, out);
    out.push("---");
    out.push("");
    secCompare(C, out);
    out.push("---");
    out.push("");
    secCautions(C, out);
    out.push("---");
    out.push("");
    secVibe(C, out);
    secSweep(C, out);
    secProvenance(C, out);

    return out.join("\n").replace(/\n{3,}/g, "\n\n") + "\n";
  }

  function safe(s, dflt) {
    var t = (s === undefined || s === null) ? "" : String(s);
    t = t.replace(/[^A-Za-z0-9._-]+/g, "_").replace(/^_+|_+$/g, "");
    return t.length ? t : (dflt || "unknown");
  }

  function filename(ctx) {
    var C = normCtx(ctx);
    var built = get(C.manifest, "built", null);
    var date = null;
    if (typeof built === "string" && /^\d{4}-\d{2}-\d{2}/.test(built)) {
      date = built.slice(0, 10);
    }
    if (!date) {
      var d = new Date();
      function p2(x) { return (x < 10 ? "0" : "") + x; }
      date = d.getFullYear() + "-" + p2(d.getMonth() + 1) + "-" + p2(d.getDate());
    }
    return "mathmap_" + safe(C.ranking, "ranking") + "_" +
           safe(C.universe, "universe") + "_" + date + ".md";
  }

  function download(name, text) {
    name = safe(name, "report.md");
    if (!/\.md$/i.test(name)) name += ".md";
    text = (text === undefined || text === null) ? "" : String(text);

    if (typeof document === "undefined") {
      throw new Error("Report.download requires a browser document");
    }

    var url = null, revoke = false;
    try {
      var blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
      url = URL.createObjectURL(blob);
      revoke = true;
    } catch (e) {
      /* Fallback for any environment where Blob URLs are unavailable. */
      url = "data:text/markdown;charset=utf-8," + encodeURIComponent(text);
    }

    var a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.rel = "noopener";
    a.style.display = "none";
    (document.body || document.documentElement).appendChild(a);
    a.click();
    setTimeout(function () {
      if (a.parentNode) a.parentNode.removeChild(a);
      if (revoke) {
        try { URL.revokeObjectURL(url); } catch (e2) { /* ignore */ }
      }
    }, 1000);
    return name;
  }

  var Report = {
    version: VERSION,
    build: build,
    filename: filename,
    download: download
  };

  var root = (typeof window !== "undefined") ? window
           : (typeof globalThis !== "undefined") ? globalThis
           : this;
  root.Report = Report;

  /* Convenience for the Node verification harness only; adds no browser global. */
  if (typeof module !== "undefined" && module.exports) {
    module.exports = Report;
  }
}());
