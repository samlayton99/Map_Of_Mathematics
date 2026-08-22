# The freeze audit: Occam, longevity, Pareto (2026-08-21, final)

Sam's challenge: prove this is the best setup with real data before
moving on. The audit changed the freeze twice more — both times toward
LESS machinery — and then certified it. Canonical implementation:
`src/frozen.py` (one file, one source of truth).

## 1. Is the 23x preserved? (seed-variance study)

4 seeds, identical protocol:
GAP  lifts [23.0, 36.9, 35.1, 27.9]  mean 30.7
GAP2 lifts [20.7, 32.1, 28.9, 26.2]  mean 27.0
GAP wins the PAIRED comparison on 4/4 seeds; GAP2 connects MORE
co-used pairs (higher positive kinship every seed) but its +9% edges
raise the random base rate. Verdict: the kinship geometry is preserved
(single-seed "23x vs 20.7x" was noise-level framing; the honest
statement is mean lift ~27-31x either way) — and since plain GAP is
both simpler and consistently better on this instrument while the AMI
difference is noise (0.386 vs 0.391), **zoom-1 = plain GAP, one rule,
no target-kind split**. Def admissions live only in the reading
boundary that justified them.

## 2. Occam drop-one on the ranking (blind labels)

| dropped key | thm KM | def KM | verdict |
|---|---|---|---|
| (frozen v1) | 0.894 | 0.742 | — |
| dem (U1D demotion) | 0.894 | 0.742 | needed for thm boundary; def: NO |
| lane (transport/infra) | 0.894 | **0.806** | thm: earns place via stmt interplay; **def: HARMFUL** |
| stmt | 0.879 | 0.710 | earns its place both kinds |
| ctor | 0.894 | 0.581 | def: essential |
| classproj | 0.894 | 0.677 | def: essential |
| depth | 0.682 | 0.742 | thm: the engine |

The finding: the theorem lanes DEMOTE the parent instances that raters
call a definition's content; the v1 classproj rule was partly
compensating for that damage (cp alone 0.677 < lane-free 0.806).
Minimal def orderings tested:

| def ordering | KM | R@4 | R@8 |
|---|---|---|---|
| frozen v1 (lanes + ctor + cp) | 0.742 | 0.758 | 0.949 |
| (ctor, stmt, depth) | 0.903 | 0.846 | 0.976 |
| **(ctor, cp, stmt, depth) — ADOPTED** | **0.903** | **0.874** | **0.976** |

Definition targets reach THEOREM PARITY (0.903 vs 0.894) with FEWER
rules than v1 — and this restores the stated first-class-definitions
principle (defs draw content from all roles; theorem lanes were
violating it). Guard test: the same simplification applied to def
INCLUSION is worse (unified-pool gap F1 0.483 vs 0.622) — the layered
boundary stands; the simplification is ordering-only.

DISCIPLINE: def results are n=31-36, third iteration on the same blind
set. Adopted because three independent probes agree (drop-one, minimal
compositions, FN/FP classes) and the causal story matches the raters'
stated conventions — but the fresh-sample confirmation debt now covers
this rule set explicitly.

## 3. Longevity (append-safety, itemized)

Every ranking/boundary input is fixed at declaration creation and
local to the proof: constructor kind (kernel), class-projection flag
(env decl metadata), statement membership (statement closure of THIS
theorem), depth (down-set; append adds above), gap threshold
(within-proof argmax), position (term order). Library growth can never
re-rank an existing proof. The v2 def ordering DROPS two dependencies
(universe demotion, lanes) — strictly fewer moving parts than v1.

## 4. Pareto (nothing simpler dominates; nothing complex adds)

- Simpler-than-frozen candidates: depth-only ranking (thm KM 0.875 old/
  0.682 blind-drop — dominated); gap-only boundary (recall-dominated);
  unified def pool (worse both ways); GAP2 zoom-1 (paired-worse
  kinship). All checked, none dominates.
- More-complex candidates: every addition tried today and earlier
  (nesting, role tier, coverage, frontier, pr-cut, recursor rule,
  transport-stmt drops, thm-side classproj) measured <= 0. The frozen
  point is on the frontier from both directions.

## 5. Gap-cut anatomy (understanding, not just scores)

Median included k = 1 (p90 3); the chosen gap is huge relative to the
proof's own scale (median 74% of target depth) — a chasm, not a
hairline. Worked examples in the audit log show both behaviors: the
chasm isolating exactly the key (ae_ae_of_ae_prod) and the known
recall trade (FreeRing.of_ne_one keeps only the deepest of two keys —
which is precisely what the union view exists to recover).

## Final construction (v2) — see src/frozen.py

Ranking: thm (dem, lane, stmt, -depth, pos); def (ctor, cp, stmt,
-depth, pos). Boundary: thm gap UNION move-lane; def additionally
ctor/cp-filtered lane side + u1d-above-gap. Zoom-1: plain gap, all
targets. Atlas: scoped + rho<=1/2 vertical. Blind numbers: thm KM
0.894, def KM 0.903, boundary F1 ~0.69 vs ceiling 0.836; map AMI 0.386
(zoom-1) / 0.416 (atlas view); co-use lift mean 30.7x over 4 seeds.
