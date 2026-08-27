# Phase 3 — Question A: Machinery Separability (no names, no text)

Data: `data/qa_results.json`, `data/ablations.json`. Models: logistic regression + depth-4 tree (interpretable primary), random forest (labeled ceiling only). Splits: grouped-by-file ≡ leave-one-domain-out here (six files, six domains). All features pass automated no-leakage tests (no names, kinds, P3 fields, files, or coverage flags).

## Broad label (`p3_any`), primary population (stored ∧ evaluated, n=876, prev 0.448)

| track / variant | grouped AUC | PR-AUC | notes |
|---|---|---|---|
| prevalence / permutation | 0.50 (perm-95: 0.55–0.56) | 0.45 | floor |
| degree-only logistic | 0.693 | 0.591 | the null to beat |
| strict, P1-weighted graph | 0.677 | 0.557 | *below* degree-only |
| strict, without community features | 0.691 | 0.588 | community features slightly hurt |
| **strict, P2-simple graph (dedup, unweighted)** | **0.757** | **0.635** | occurrence multiplicity is noise for this label |
| **typed formal-occurrence track** | **0.802** | — | statement-vs-body profile is the main signal |
| typed, degree-matched control (n=578) | 0.859 vs degree-only 0.660 | — | signal survives degree matching |
| strict, degree-matched control | 0.722 vs 0.641 | — | modest but real |

**Answer A1:** yes, modestly — beyond-degree structural signal exists under cross-domain holdout, but the strict "topology alone" gain is small (≈+0.06 AUC over degree on the best graph variant). The *typed* track (how a declaration is referenced: statement vs proof-body, depth, relation entropy) is substantially stronger (+0.11 over degree; +0.20 degree-matched). Interpretable drivers (logistic coefficients, strict/primary): high `in_deg` with low unique-degree-to-weight ratio, `cross_comm_frac`, `harmonic_in`, low `coreness`, `hits_hub` negative.

## Class-specific (A2), primary population, grouped holdout

| class | n pos | strict AUC | degree-only | typed AUC | verdict |
|---|---|---|---|---|---|
| typeclass-instance | 47 | **0.973** | 0.888 | 0.938 | genuinely structurally recognizable |
| internal-detail | 310 | 0.684 | 0.667 | **0.853** (PR 0.75) | recognizable only via typed occurrence profile |
| generated | 75 | 0.810 | 0.810 | 0.811 | pure degree effect |
| structure-projection | 18 | 0.915 | 0.922 | 0.868 | pure degree effect (small n) |
| eq-machinery / logic-core / recursor / coercion | 0–5 | — | — | — | **skipped: no stored positives** (these classes live in the imported shallow stratum; sensitivity-population results in `qa_results.json` carry boundary caveats) |

**Answer A3:** separability survives degree matching and domain holdout for typeclass-instance and (typed track) internal-detail; it does *not* for generated and structure-projection, whose apparent separability is degree. Coverage cannot drive the primary result (single stratum). Permutation tests: all reported AUCs exceed the within-domain shuffled-label 95th percentile except strict/p3_any on the weighted graph (0.677 vs perm-95 0.547 — above, but closest).

## Sensitivity population (all evaluated, n=2,827)

Same ordering (strict 0.676, typed 0.728, degree-only 0.631); the smaller typed gain reflects shallow nodes lacking body-side structure. No conclusion rests on this population.

## Interpretation limits

Reproducing P3 shows P3 classes have distinct formal roles; it does not validate P3 as human truth (see the disagreement audit for where topology and P3 part ways, including a real P3 label gap: structure constructors).
