# Phase 2 Errata and Corrections

Date: 2026-08-19. The Phase 2 reports are historical records and are not rewritten; this note corrects three claims. Each correction was re-verified against `studies/characterization.json` and the raw study data before being recorded here.

## E1. Containment was not universal

`REPRESENTATION_CHARACTERIZATION.md` F4 claimed "Every P5-attributed declaration … occurs in the P2 support of the same proof (containment 1.0)". The 1.0 values were per-file **medians**, reported as if universal. Row-level check: **61 of 1,233 rows have P5-in-P2 containment below 1** (events attributing declarations that do not appear in the final proof term's support — e.g. rewrites later erased, or steps inside `where`-structure elaboration). P4-heads-in-P2 does hold on all 1,233 rows. P2, P4, and P5 are related views, not universally nested sets.

## E2. Term proofs were not 76%

`USE_EVENT_FEASIBILITY.md` said term proofs are "76% of the population". The raw fraction is **850/1233 ≈ 68.9%** (defensible range 67–69% depending on denominator).

## E3. P4 result-type inference was not "overwhelmingly" successful

`HONEST_ASSESSMENT.md` Q7 said `resultOk` held for "the overwhelming majority of spines". Occurrence-weighted success is **61.4%** (324k/528k spines), with substantial domain variation. Since P4-route filters on inferred result type (`resultIsProp`), missing inference removes candidate applications: P4-route's small size reflects both abstraction **and missingness**. Any use of P4-route must carry this caveat.

## Standing consequence

No current-direction document may cite universal containment, a 76% term fraction, overwhelming P4 inference success, human validation (none occurred), or a selected primary map representation. The Phase 2 quantitative tables remain otherwise accurate.
