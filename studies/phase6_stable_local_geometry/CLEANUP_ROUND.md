# The bounded cleanup round (2026-08-21, final)

Sam's directive: one honest doubled-down round on F1 low-hanging fruit.
GPT's directive: bounded cleanup of concretely observed defects, then
freeze. Both satisfied. DISCIPLINE NOTE: this round DEVELOPS on the
blind instrument (the only clean one); blind is therefore now dev data,
and the adopted rules await confirmation on the next fresh sample.

## The blind oracle decomposition (new)

| group | policy (union) | pool oracle | prefix oracle | ceiling |
|---|---|---|---|---|
| theorems | 0.715 | 0.922 | 0.885 | 0.836 |
| definitions | 0.519 | 0.756 | 0.675 | 0.836 |

Unlike the old corpus, clean labels show real headroom: theorem
cut-rule slack ~0.17, definition pool loss ~0.24.

## Three fixes adopted, each dictated by a named failure class

1. **Constructor exclusion from the inclusion lane-side** (def targets;
   23 FPs named): def F1 0.519 -> 0.550, theorems untouched.
2. **U1D admission above the gap threshold, def targets only, non-ctor**
   (28 FNs named: instStarRing-class instances): def recall
   0.616 -> 0.755, def F1 -> 0.588; theorem variant tested and
   rejected (costs precision).
3. **Class-projection demotion — the interface species finally has a
   kernel identity.** New extractor fact (`mathrecord projflags`,
   env.getProjectionFnInfo + isClass): 14,969 projections; class
   projections are 95% junk / 1.4% useful on blind grades (n=281).
   Adopted in ranking (infra lane) and inclusion (out of lane-side):
   definitions KM@1 0.677 -> 0.742, R@4 0.666 -> 0.758; inclusion
   all-F1 0.655 -> 0.686, junk 23.5% -> 17.7%. Theorems unchanged.

Cumulative definition arc this phase: KM@1 0.516 -> 0.742.
Final inclusion (V3): all 0.686 / thm 0.714 / def 0.622 against
ceiling 0.836.

## The defect table (stop-rule accounting)

| defect | frequency | current effect | attempted principled fix | result | verdict |
|---|---|---|---|---|---|
| packaging ctor in def inclusion | 23 FP | junk in def sets | kernel-kind exclusion from lane-side | +0.03 def F1 | KEEP |
| useful instances U1D-locked | 28 FN | def recall cap | u1d>=gap, def targets, non-ctor | +0.14 def recall | KEEP |
| class-projection interface junk | ~20 FP + hub mass | junk both layers | env projection flag -> infra | +0.065 def KM, -6pts junk | KEEP |
| useful transport below gap | 11 FN | gray-zone recall | (stmt-drop tested before: hurts) | none viable | FREEZE |
| thm cut-rule slack | ~0.17 F1 | prefix oracle gap | no grade-free cut signal found | not pursued | DEFER (needs new signal class) |
| human forwarders as landmarks | 7.4% of thms, 3.3% of GAP edge dsts | minor | audit only | not material at map level | DEFER (view grouping) |
| foundations transport demotion | 3/48 foundational proofs (6.2%) | rare | audit only | scale-consistent | FREEZE (no depth regime) |
| rho threshold tuning risk | — | rendering | sweep 0.25-0.75 | smooth, plateau at [0.33,0.6] | KEEP rho=1/2 |

## Frozen

The citation construction is now FROZEN per the stop rule: universe
(U1D + def-target admissions), lanes (transport/infra/classproj),
ordering (laneD_stmt + ctor demotion), inclusion (gap zoom filtration +
lane-side exclusions), rendering (scoped, rho<=1/2 vertical). Further
per-proof optimization requires a new signal class or a new instrument,
not new rule combinations. The program's center moves to lateral
geometry, navigation benchmarks, and time-stability (GPT Parts 2-4).
