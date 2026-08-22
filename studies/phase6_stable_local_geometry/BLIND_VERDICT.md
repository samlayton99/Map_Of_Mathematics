# The blind verdict (2026-08-21, late)

Three independent blind raters, 5,124 judgments, 120 fresh targets
(84 theorems + 36 definitions — the first definition targets ever
graded), briefs grep-proven free of every system coordinate.
Instrument resolution: rater-vs-rest F1 0.836 (old contaminated
instrument: 0.856).

## What survived decontamination

- **Theorems: laneD_stmt KM@1 0.894 blind** (contaminated instrument
  said 0.913 — the depth-visibility inflation was ~2 points, not the
  feared invalidation). R@4 0.920, R@8 0.959.
- **Depth's signal is mostly real**: grade-depth Spearman 0.475 with
  depth invisible to raters.
- Inclusion policy ORDERING preserved (gap > union > top-4 on
  precision); absolute junk rates are not comparable across rubrics.

## What the blind instrument exposed

- **Definitions: KM@1 0.516** — the theorem-tuned ordering misses
  definition semantics. Failure mining: 10 of 15 misses have a
  CONSTRUCTOR at rank 1 (`SetLike.mk`, `Equiv.mk`, `Inhabited.mk`)
  while the blind key is the defining field / underlying definition —
  matching the convention both raters stated independently.
- **Fix adopted: constructor demotion for definition targets** (kernel
  kind == constructor sorts after non-constructors, definition targets
  only): KM@1 0.516 -> 0.677, theorems untouched by construction.
  Small-n caveat (31 graded defs); out-of-sample check queued.
- **stmt-concept separator killed**: 0.53 precision on noisy labels
  collapses to 0.14 on clean ones. It was fitting label noise.

## Caveats

Raters are the same model family as the designers (convergent grading
conventions may be shared priors, not independent confirmation); some
kernel-level candidates invisible in tactic source were judged by
inferred role; definition results rest on 31-36 targets.
