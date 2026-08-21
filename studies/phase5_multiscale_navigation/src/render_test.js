/* Headless render test for the shipped dashboard.
 *
 * `dashboard_check.py` proves the DATA is well formed. This proves the PAGE
 * actually renders it: it loads the real viewer.html in a DOM, drives every
 * tab, every universe, every lane and every policy, and fails on any thrown
 * exception, any console error, or any panel that came out empty.
 *
 *   node src/render_test.js [dist_dir]
 *
 * Needs jsdom on NODE_PATH. Written as a throwaway harness, not shipped.
 */
const fs = require("fs");
const path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");

const dist = process.argv[2] || path.join(__dirname, "..", "dashboard", "dist",
                                          "map_results");
const file = path.join(dist, "viewer.html");
if (!fs.existsSync(file)) {
  console.error("no viewer at " + file);
  process.exit(1);
}

const errors = [];
const vc = new VirtualConsole();
vc.on("jsdomError", e => errors.push("jsdomError: " + (e.stack || e.message)));
vc.on("error", (...a) => errors.push("console.error: " + a.join(" ")));

JSDOM.fromFile(file, {
  runScripts: "dangerously",
  resources: "usable",
  virtualConsole: vc,
  pretendToBeVisual: true,
  // jsdom has no scrollTo and reports every call as a jsdomError, which would
  // otherwise bury real failures under harness noise. Real browsers have it.
  beforeParse(win) { win.scrollTo = function () {}; },
}).then(async dom => {
  const w = dom.window, doc = w.document;
  // give the inline <script src="data/all.js"> time to load and boot()
  await new Promise(r => setTimeout(r, 4000));

  const fail = [];
  const note = m => console.log("  " + m);

  if (!w.MAPDATA) fail.push("window.MAPDATA never loaded (all.js did not run)");
  if (!w.Charts) fail.push("window.Charts missing");
  if (!w.Report) fail.push("window.Report missing");
  if (!w.D) fail.push("viewer never bound its data");
  const picker = doc.getElementById("picker");
  if (picker && !picker.hidden) fail.push("the folder picker is showing, so " +
    "automatic loading failed");
  if (fail.length) { report(fail); return; }

  const M = w.MAPDATA.manifest;
  note(`loaded: ${M.rankings.length} rankings, universes ` +
       `${M.universes.join("/")}, lanes ${M.lanes.join("/")}`);

  const main = doc.getElementById("main");
  const bodyText = () => main.textContent || "";
  const check = (label, minLen) => {
    const before = errors.length;
    let txt;
    try { txt = bodyText(); }
    catch (e) { fail.push(`${label}: reading DOM threw ${e.message}`); return; }
    if (main.querySelector(".card.err"))
      fail.push(`${label}: render error card -> ` +
                main.querySelector(".card.err pre").textContent.slice(0, 300));
    if (txt.length < (minLen || 800))
      fail.push(`${label}: rendered only ${txt.length} chars`);
    if (errors.length > before)
      fail.push(`${label}: ${errors.length - before} console errors`);
    const svgs = main.querySelectorAll("svg").length;
    const tables = main.querySelectorAll("table").length;
    return {chars: txt.length, svgs, tables};
  };

  const set = (k, v) => { w.S[k] = v; w.render(); };

  // --- every tab, at defaults ------------------------------------------
  for (const tab of ["howto", "summary", "vibe"]) {
    set("tab", tab);
    const r = check("tab=" + tab);
    if (r) note(`tab ${tab}: ${r.chars} chars, ${r.svgs} svg, ${r.tables} tables`);
  }
  // --- every ranking tab -------------------------------------------------
  for (const r of M.rankings) {
    w.S.tab = "ranking"; set("ranking", r.name);
    const res = check("ranking=" + r.name);
    if (res && res.svgs === 0) fail.push(`ranking ${r.name}: no charts drawn`);
  }
  note(`${M.rankings.length} ranking tabs rendered`);

  // --- every universe x lane, on summary and a ranking ------------------
  for (const u of M.universes) {
    for (const l of M.lanes) {
      w.S.universe = u; w.S.lane = l;
      w.S.tab = "summary"; w.render(); check(`summary ${u}/${l}`);
      w.S.tab = "ranking"; w.render(); check(`ranking ${u}/${l}`);
    }
  }
  note(`${M.universes.length * M.lanes.length} universe/lane combinations ok`);

  // --- every policy, incl. the vibe highlighting ------------------------
  w.S.universe = M.reference_universe; w.S.lane = "all";
  for (const p of ["topk", "pct", "global", "cluster"]) {
    w.S.policy = p;
    for (const tab of ["summary", "vibe", "ranking"]) {
      w.S.tab = tab; w.render(); check(`policy=${p} tab=${tab}`);
    }
  }
  note("4 policies x 3 tabs ok");

  // --- slider sweeps -----------------------------------------------------
  w.S.policy = "topk";
  for (let k = 1; k <= 12; k++) { w.S.k = k; w.S.tab = "vibe"; w.render(); }
  check("k sweep 1..12");
  w.S.policy = "pct";
  for (const q of [1, 5, 25, 50, 100]) { w.S.pct = q; w.render(); }
  check("pct sweep");
  w.S.policy = "global";
  for (const q of [1, 25, 100]) { w.S.q = q; w.render(); }
  check("global sweep");
  note("slider sweeps ok");

  // --- vibe highlighting actually marks rows ----------------------------
  w.S.policy = "topk"; w.S.k = 4; w.S.tab = "vibe"; w.render();
  const adm = main.querySelectorAll("tr.admitted").length;
  const exc = main.querySelectorAll("tr.excluded").length;
  if (!adm) fail.push("vibe: nothing highlighted as admitted at top-4");
  if (!exc) fail.push("vibe: nothing marked excluded at top-4");
  note(`vibe highlighting: ${adm} admitted rows, ${exc} excluded rows`);
  const g = main.querySelectorAll(".gr").length;
  if (!g) fail.push("vibe: no reviewer grade badges rendered");
  const gloss = main.querySelectorAll("tr.expl").length;
  if (!gloss) fail.push("vibe: no LLM gloss rows rendered");
  note(`vibe: ${g} grade badges, ${gloss} gloss rows`);

  // toggling ranking must change the order shown
  const firstOf = rk => {
    w.S.vibeRanking = rk; w.render();
    const c = main.querySelector("table.cands tbody tr td:nth-child(4) code");
    return c ? c.textContent : null;
  };
  const a = firstOf("R_v8_faithful"), b = firstOf("B1_reverse_depth");
  if (a && b && a === b)
    fail.push("vibe: two very different rankings put the same item first; " +
              "the ranking toggle may not be wired");
  else note(`vibe toggle changes order: ${a} -> ${b}`);

  // --- export report -----------------------------------------------------
  for (const rk of M.rankings.map(r => r.name)) {
    let md;
    try {
      md = w.Report.build({ranking: rk, data: w.MAPDATA.rankings[rk],
        summary: w.MAPDATA.summary, definitions: w.MAPDATA.definitions,
        manifest: M, vibe: w.MAPDATA.vibe, sweep: w.MAPDATA.sweep,
        state: {universe: M.reference_universe, lane: "all", k: 4}});
    } catch (e) {
      fail.push(`Report.build(${rk}) threw: ${e.message}`);
      continue;
    }
    if (!md || md.length < 3000)
      fail.push(`Report.build(${rk}) produced only ${md ? md.length : 0} chars`);
    for (const bad of ["undefined", "NaN", "[object Object]"])
      if (md.includes(bad))
        fail.push(`Report.build(${rk}) contains ${bad}`);
  }
  note("export reports build for all rankings");

  report(fail);

  function report(f) {
    console.log();
    for (const e of errors.slice(0, 10)) console.log("  JS  " + e.slice(0, 300));
    for (const x of f) console.log("  FAIL " + x);
    console.log(`\n${f.length} failures, ${errors.length} console errors`);
    process.exit(f.length || errors.length ? 1 : 0);
  }
}).catch(e => { console.error("harness failed: " + (e.stack || e)); process.exit(1); });
