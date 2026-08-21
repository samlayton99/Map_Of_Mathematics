# P0 cleanup — phase5 study

## Needs lead attention

- **`src/build_incidence.py` still points DUMP at the volatile scratchpad**
  (lines 21-22; owned by another agent, not touched). Fix to
  `~/mathmap_data/mathlib_deps7.jsonl`.
- **The reference ranking is NOT `R_phase5_composite`.** The registered
  `R_phase5_composite` gives P@1 0.9833 / P@4 0.6892 / KeyMove@1 0.8861 /
  core@4 0.9869 on TEST-R — it does not reproduce the quoted line. The recipe
  that reproduces all four exactly is the DOMINANCE-study reference
  `REF_weighted_role_x_rarity_5dec` (scratchpad `famAB_ref.py`):
  `-(W[tier5] * IDF50[decl])`, W=[1.0,0.7,0.5,0.35,0.15], term-order tie-break.
  Now committed in `src/reference_numbers.py`; both sets recorded in
  `results/reference_numbers.json`.
- **`prov/` provenance JSONs still live only in the scratchpad** (referenced by
  `mathmap_eval/corpus.py` DEFAULT_PROV and `src/{candidates,glue_by_depth,
  coverage_by_kind,suite}.py`). Same data-loss trap as the dump; not copied
  (out of scope).

## Reference numbers — all four reproduce exactly

`src/reference_numbers.py` (sealed TEST-R, 360 proofs, median rater grades):

| metric | value |
|---|---|
| precision@1 | 0.9750 |
| precision@4 | 0.7123 |
| KeyMoveAt1 | 0.8250 |
| recall_core@4 | 0.9738 |

Fourth metric identified: `recall_core@4` (battery.local; recall of grade-4
KEY moves in top-4 — "core@4 0.974" in SCHEME_SOCIAL_CHOICE.md's quoted line).
Output: `results/reference_numbers.json` with provenance. Exits non-zero on
mismatch.

## navigability deleted

- `mathmap_eval/battery.py`: function, its scipy imports, and the `nav` arg of
  `report()` removed; docstring points to `shortcuts.py`.
- `src/run_social_choice_nav.py`: deleted (existed only to run it).
- `src/scheme_conditional.py`: `sec_nav` section removed from code + SECTIONS.
- `src/make_sc_table.py`: nav columns dropped (table is 11 metric cols now).
- Stale docstrings fixed in `src/run_social_choice.py`,
  `src/run_social_choice_shortcuts.py`. Report prose left alone.
- Verified: `import mathmap_eval.battery` OK; `python -m mathmap_eval.tests`
  all invariants pass; touched src files compile.

## Dump secured

`~/mathmap_data/mathlib_deps7.jsonl` (1,311,518,013 bytes), full `cmp`
byte-identical to the scratchpad original. `src/build_v8_mask.py` DUMP updated;
`src/depth_scc.py` already prefers `~/mathmap_data`. Only `build_incidence.py`
remains (see above).

## SEALED_R1_RESULTS.md

VOID banner added at top, pointing to `phase6_stable_local_geometry/PROGRAM.md`.
