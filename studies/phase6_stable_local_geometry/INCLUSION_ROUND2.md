# Inclusion round 2: oracle ceilings and the zoom filtration (2026-08-21)

## The structural finding: single-cut policies have a hard ceiling

Oracle experiment: per proof, choose the BEST POSSIBLE cut with
knowledge of the answers. Depth-threshold family: F1 0.799. Prefix of
the laneD_stmt order: F1 0.825. Perfect precision+recall (the
mathematician's-head model) is NOT reachable by any cut of the current
ordering — the remaining ~0.18 requires signals that reorder or
re-pool, not better cut selection. Concretely (gap_all's 501 missed
useful items): 233 deep moves below the gap, 147 useful definitions
cited only implicitly (excluded from the pool entirely), 95 useful
transport lemmas, 26 outside the universe (mostly target-owned helper
contents — the known extractor gap).

## Measured frontier (strict matching, 522 proofs)

| policy | prec | junk | rec | F1 | stability (harmless/control) |
|---|---|---|---|---|---|
| gap_all | 0.793 | 0.043 | 0.635 | 0.653 | **0.772** / 0.062 |
| gap OR move-lane | 0.778 | 0.047 | 0.743 | **0.719** | 0.655 / 0.037 |
| + U1D above gap | 0.742 | 0.096 | 0.805 | 0.719 | — |
| top2gap (zoom-2) | 0.609 | 0.137 | 0.778 | 0.636 | — |
| prefix_gap | 0.796 | 0.046 | 0.657 | 0.666 | — |
| oracle ceiling | — | — | — | 0.80-0.83 | — |

No single winner: gap_all is the most refactoring-stable and precise;
the union has the best graded F1 (and the best stability RATIO,
17.7:1); +U1D is a pure recall dial (same F1, junk doubles). Grades are
the contaminated instrument, metamorphic the clean one — so gap_all
remains the canonical tight cut, and the others are VIEWS.

## The reframe: inclusion is a per-proof ZOOM FILTRATION, not one set

Successive depth gaps give canonical zoom levels with no constants:
zoom-1 = above the largest gap (the proof's headline mathematics);
zoom-2 = above the next structural gap (top2gap, recall 0.778);
zoom-3 = + move lane; ... ; full = everything (expansion completeness).
This dissolves the "which cut" question the same way the lane ordering
dissolved "which weights": the user/agent picks the level; every level
is local, ordinal, append-safe. Matches principle 14 and the phase's
name (multiscale navigation).

## Untested-ideas ledger (asked and answered)

- Helper expansion (target-owned `_proof_N` contents): still the
  largest single unlock outside cut selection — 26 universe exclusions
  here + the metamorphic wrapper failure. Extractor work, queued.
- U1D usefulness signal: 147 useful implicit definitions exist but the
  U1D pool is junk-rich (adding it doubles junk). Needs a def-level
  separator; definitions were never graded as targets (audit caveat),
  so this wants the blind regrade with definition targets.
- Lambda-based inclusion: rejected on principle — co-use is
  cross-proof information; inclusion must stay local.
- Transport-statement dropping: tested, hurts (0.694).
- Recursor-to-infra: tested earlier, grade-neutral, not adopted.
- External pair source, vertical rendering, corpus scoping: open,
  deferred by decision.

## Map level: the tight zoom draws the best map

Union (GEL, 1.93M edges) vs gap-only (GAP, 1.06M): AMI 0.340 vs 0.386;
modularity 0.695 vs 0.886; distance AUC 0.597 vs 0.627; within-area
share 59% vs 79%; hub concentration 15% vs 11%. The union wins only
cross-area plumbing share (12.5% vs 35%, the lane filter's
contribution). Verdict: GAP (zoom-1) remains the map's default edge
set; looser zooms serve per-proof recall and reading views, not the
global drawing. Consistent with the filtration framing: you draw the
atlas at tight zoom and expand locally.
