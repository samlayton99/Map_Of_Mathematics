/* Generate the per-ranking Markdown reports headlessly.
 *
 * These are exactly what the dashboard's "Export this report" button
 * produces; generating them here means the package can ship them as worked
 * examples without anyone clicking ten buttons.
 *
 *   node src/export_reports.js <out_dir> [dist_dir]
 */
const fs = require("fs");
const path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");

const outDir = process.argv[2];
const dist = process.argv[3] || path.join(__dirname, "..", "dashboard", "dist",
                                          "map_results");
if (!outDir) { console.error("usage: node src/export_reports.js <out_dir>"); process.exit(1); }
fs.mkdirSync(outDir, { recursive: true });

const vc = new VirtualConsole();
JSDOM.fromFile(path.join(dist, "viewer.html"), {
  runScripts: "dangerously", resources: "usable", virtualConsole: vc,
  pretendToBeVisual: true,
  beforeParse(win) { win.scrollTo = function () {}; },
}).then(async dom => {
  const w = dom.window;
  await new Promise(r => setTimeout(r, 4000));
  if (!w.MAPDATA) { console.error("data never loaded"); process.exit(1); }
  const M = w.MAPDATA.manifest;
  const U = M.reference_universe;
  let total = 0;
  for (const r of M.rankings) {
    const md = w.Report.build({
      ranking: r.name, data: w.MAPDATA.rankings[r.name],
      summary: w.MAPDATA.summary, definitions: w.MAPDATA.definitions,
      manifest: M, vibe: w.MAPDATA.vibe, sweep: w.MAPDATA.sweep,
      state: { universe: U, lane: "all", k: 4 },
    });
    const fn = `${r.name}__${U}.md`;
    fs.writeFileSync(path.join(outDir, fn), md);
    total += md.length;
    console.log(`  ${fn}  ${md.length.toLocaleString()} chars`);
  }
  console.log(`${M.rankings.length} reports, ${total.toLocaleString()} chars total`);
  process.exit(0);
}).catch(e => { console.error(e.stack || e); process.exit(1); });
