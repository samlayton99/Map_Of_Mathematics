# Keyness Evaluation — Blind Panel (2026-08-19)

The judge's final gate: does rank 1 correspond to the move a mathematician would tell a colleague first? Protocol per the ruling (`review/keyness/RATER_PROTOCOL.md`): 26 proofs selected by structural criteria only (seed 20260823, from the never-used population remainder, ≥8 candidates each, depth-stratified); five anonymized views per proof, labels shuffled per proof; three independent Opus raters, no cross-talk, each required to name the key move from the source BEFORE seeing any view. Three briefs (11, 14, 21) were excluded post hoc for verified source-resolution collisions (wrong same-shortname theorem pasted; flagged independently by a rater); primary results on the 23 clean proofs (69 rater-proof judgments), full-26 numbers in `data/keyness_results.json`.

## Results (primary, 23 proofs × 3 raters)

| view | mean "tells how it works" (1–5) | rank-1 IS the key move | yes or partial | best-view votes |
|---|---|---|---|---|
| **zoom** (certified ranking + single-use containers opened inline) | **4.33** | **56.5%** | **92.8%** | **35** |
| **ranked** (certified V5v flat ranking) | 3.80 | 37.7% | 71.0% | 28 |
| prov (human source citations, elaborator-resolved) | 2.61 | 18.8% | 27.5% | 4 |
| applied (occurrence-frequency order) | 2.54 | 13.0% | 24.6% | 2 |
| moveset (unordered) | 2.81 | 1.4% | 21.7% | 0 |

Best-view unanimity across raters: 73.9%. Our two views take **63 of 69** best-view votes.

## Reading

1. **The hierarchical zoom view is the winner**, exactly as the judge's model predicted ("that gives you the hierarchical map you wanted anyway"): rank-1 is the key move or a partial match **92.8%** of the time, and raters rate it 4.33/5 as an explanation of how the proof works.
2. **Ordering carries most of the value**: the same move set unordered scores 2.81 with zero votes; the certified ranking lifts it to 3.80; opening containers lifts it to 4.33. Extraction ≠ ranking ≠ keyness, measured — and each layer adds.
3. **The kernel view beats the human's own citations** (2.61): what the author typed is neither complete (elaboration erases ~14%) nor ordered by importance. The provenance channel remains necessary for recall and intent, but it is not the explanation view.
4. Against the judge's prior of ~25% that pure kernel structure could reach human-level keyness: rank-1 exact-match 56.5% and exact-or-partial 92.8% on hard proofs is substantially beyond that expectation. Keyness is no longer the open front; the open fronts are the shallow floor, cross-version testing, and scaling the panel (more proofs, human raters).

## Honesty box

Raters are Opus reasoning agents, not human mathematicians; single-blind; n=23 proofs / 69 judgments; the brief generator's source resolver produced 3 collisions out of 26 (caught by a rater and by keymap verification — future briefs should resolve sources via the provenance channel's declaration names, which are exact). Ratings and keymap are committed for reanalysis.
