# P0 — Substrate corrections (2026-08-21)

Full detail in `p0/`. Status of the eight required items
(gpt_handoff/05, Phase 0):

1. **Exact SCC depth: DONE.** 3-pass cycle relaxation replaced by exact SCC
   condensation (`src/depth_scc.py` + patched `build_incidence.py`).
   356/771,129 nodes change (all increases, up to +143); every nontrivial
   SCC is Lean-internal `_unsafe_rec` machinery — no mathematics in cycles.
   `data/depth_scc.npz` also carries `depth_stmt` (type-only graph, a DAG,
   max 13) — which became the transport-lane separator (see
   `HIERARCHY_VS_FLAT_RESULTS.md`).
2. **Type vs value dependencies separated: DONE** (`depth_stmt` vs
   `depth_exact`).
3. **Statement-world closure: VIOLATION CONFIRMED, PATCHED, NOT YET
   REBUILT.** The old closure traversed other theorems' proof bodies:
   9.5% of incidences flip under the corrected rule, concentrated on
   rewriting machinery (`congrArg`, `Eq.mpr`, `id`, `propext`) — the old
   flag inflated statement-world membership exactly on plumbing. Rebuild of
   `incid.npz` pending (expect global in-world rate to drop ~10 points).
4. **Stable IDs: OPEN** (still array positions; carry to next rebuild).
5. **Expression paths / application parents: DONE** — `mathrecord hierdump`
   (new `Mathrecord/HierDump.lean`) emits occurrence-level forests: const,
   parent application, arg index, role, nesting. Zero truncation observed.
6. **Generated-owner: DONE** via elaborator provenance (gen flag + name
   prefix; stated exception to the no-names principle).
7. **All roles preserved: was already true** (8-vector per incidence).
8. **Grading-brief audit: DONE, material findings** — raters saw depth,
   role, in-statement, and kind tags; the rubric text encoded predictions
   (grade-0 defined as instance resolution; the depth-conditional glue
   claim was written into the instructions). Consequences: role-bucket
   MAGNITUDES are contaminated (direction probably real); instance-slot's
   uniquely low disagreement (0.11) suggests tag-following; the graded
   corpus is theorem-only, so nothing measured transfers to definitions;
   paired rule-vs-rule comparisons on fixed labels remain valid. See
   `p0/P0_GRADING_BRIEF_AUDIT.md`.

Housekeeping: `battery.navigability` deleted; reference numbers landed as
committed code (`phase5/src/reference_numbers.py` — and the quoted four
numbers turn out to belong to the dominance-study weighted reference, not
`R_phase5_composite`; both value sets recorded with provenance); the 1.2 GB
raw dump copied out of volatile tmp to `~/mathmap_data/`; SEALED_R1 report
carries a VOID banner. Remaining trap: `prov/` provenance JSONs still live
only in the scratchpad.
