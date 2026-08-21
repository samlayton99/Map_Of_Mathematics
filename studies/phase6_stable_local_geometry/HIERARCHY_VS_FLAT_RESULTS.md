# P1 — Hierarchy vs flat: pilot results (2026-08-21)

Data: fresh 48-proof depth-stratified sample (seed 20260901, structural),
552 graded sealed proofs (secondary, contamination-flagged — see
`p0/P0_GRADING_BRIEF_AUDIT.md`), fresh 20k-artifact map sample (seed
20260902). Substrate: `mathrecord hierdump` occurrence forests (new; exact
parent-application hierarchy, all roles, zero truncation on all 20,600
walked proofs; expansion completeness 1.000).

## Verdict on H1

**Partially supported, with a sharpened mechanism.** The hierarchy is real
and cheap to extract, but its value is NOT "roots-only visibility":

1. **Roots-only fails.** Root-level items are 16% of candidates; a
   roots-only view flatlines useful-recall at 0.31 (flat: 0.77 at k=8).
   Term-proof roots are single application heads; content is nested below.
2. **Nesting is an ordering key, not a cut.** Sorting shallower-first
   restores recall (0.760) but by itself moves nothing else: rewriting
   plumbing (`Eq.mpr`, `id`, `congrArg`) is genuinely SHALLOW in the term
   — nesting cannot demote it, falsifying the strong reading of H2
   (rarity-as-surrogate-for-lost-nesting).
3. **The missing lane was found in the statement vocabulary.**
   `depth_stmt` (exact SCC depth over the TYPE-only dependency graph, new
   in `data/depth_scc.npz`) separates universal automation from universal
   mathematics where value-depth provably cannot: `Eq.mpr`'s type mentions
   only `Eq` (depth_stmt 1); `mul_comm`'s type needs `CommMonoid`
   (depth_stmt 3). On graded items: 81% of BAD_GLUE and 73% of JUNK sit at
   depth_stmt <= 1, vs 6.8% of CORE. Raters never saw this signal.

## The `laned` view

Ordinal lexicographic order, zero fitted constants, every key append-safe:

    (lane, min-nesting, role-tier, first-occurrence)
    lane: 0 move | 1 transport (depth_stmt <= 1) | 2 infra (generated,
          instance-only); generated helpers owned by the target drop,
          owned elsewhere redirect to the owner (elaborator provenance)

Demotion, not removal — a purely logical proof still shows its logic
(relativity, principle 10). All items stay expandable (completeness 1.0).

## Numbers (graded corpus, fixed protocol, 522 proofs)

| view | KeyMove@1 | R@1 | R@2 | R@4 | R@8 |
|---|---|---|---|---|---|
| flat (tier, occ) | 0.472 | 0.303 | 0.497 | 0.658 | 0.771 |
| + nesting (hier) | 0.472 | 0.303 | 0.498 | 0.634 | 0.760 |
| + lanes (laned) | **0.679** | **0.426** | **0.602** | **0.751** | **0.810** |

Paired: KeyMove@1 flips +96/-8, McNemar p = 2.8e-20; recall@8 diff +0.039,
bootstrap CI [+0.020, +0.058]. Laned dominates flat at every budget.

TEST-R protocol (371 proofs): laned 0.685 vs void fitted+rarity reference
0.825 and Copeland+rarity 0.897. **The gap to live rarity is real and
remaining** — target of H6 (append-safe local magnitudes) and Layer D
distillation, not of more lane rules.

## Map level (20k fresh artifacts, top-4 edges per proof, top-100 hubs)

| | transport link-mass | math link-mass |
|---|---|---|
| flat | 0.777 | 0.223 |
| laned | **0.288** | **0.712** |

No edge deleted; the hubs shift from `Eq.mpr`/`of_eq_true`/`Eq.trans` to
`Membership.mem`/`CategoryTheory.Functor.obj`/`RingHom.id`.

**Next problem, precisely located:** the new top hubs include interface /
notation vocabulary (`OfNat.ofNat`, `HAdd.hAdd`, `DFunLike.coe`) — a
second species of universal plumbing that is NOT transport (its types need
real vocabulary) and NOT junk. It is span-relative: these edges are
vertical support for deep targets, lateral only near the foundations.
This is exactly the P5 multifiltration axis (span-aware rendering), not a
lane rule.

## Caveats

- Grade-based numbers inherit the brief contamination (roles/depth were
  visible to raters); the laned gain rests mostly on depth_stmt, which
  raters could not see, and on paired same-label comparisons, which the
  audit sanctions.
- depth_stmt is coarse (max 13, mean 3.2); the `<= 1` boundary is a stated
  small integer over the logical core, but its stability across Mathlib
  versions is untested (P4 material).
- Sampling filter for the pilot excludes compiler schemes by NAME
  (sampling only, never scoring) — stated in `src/pilot_sample.py`.
