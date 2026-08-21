# The ground must not shift — which signals survive

Constraint from the project lead: the map is built iteratively, and **anything
added at the edge must not change the foundation beneath it**.

This is a hard structural constraint, not a preference, and it disqualifies
signals rather than merely penalising them.

---

## 1. First-principles audit

When a new declaration `D` is added to the library, which signals change for
declarations that already existed?

| signal | changes on append? | why |
|---|---|---|
| **depth** | **no** | depth counts unfolding levels *beneath* a declaration. Adding above changes nothing below. |
| **occurrence role** | **no** | a property of an existing proof term, which is immutable once elaborated |
| **in-statement** | **no** | same |
| **declaration kind** | **no** | immutable |
| **auto-generated flag** | **no** | immutable |
| **arity** | **no** | immutable |
| **rarity / idf** | **YES** | `log(n_proofs / citation_count)`; both terms move when anything is added |
| **library in-degree** | **YES** | every new citer increments it |
| **popularity** | **YES** | same |

**Only the count-based signals violate the constraint**, and they are exactly
the ones the promoted ranking leans on hardest.

---

## 2. How much does the ground actually move?

Simulated by recomputing rarity from a random subset of the library and
comparing within-proof orderings on the graded proofs.

| library size | rarity alone: top item changes | rarity x role: top item changes | Kendall tau |
|---|---|---|---|
| 90% of today | 1.4% of proofs | 0.3% | 0.993–0.997 |
| 75% | 4.7% | 3.1% | 0.984–0.993 |
| 50% | 6.1% | 4.2% | 0.973–0.994 |
| 25% | **11.1%** | 6.1% | 0.949–0.987 |

The *ordering* is largely preserved (tau stays above 0.95) but **the headline
item moves in up to 1 proof in 9** across a 4x growth in library size. For a
map whose top-level view is exactly that headline item, that is the ground
shifting.

Append-safe signals move in 0.0% by construction, not by measurement.

---

## 3. The frozen-foundation fix — it works

The project lead's proposal: compute the global quantity once over a frozen
stratum, so growth at the edge cannot disturb it.

Implemented as: **rarity computed only from proofs whose target theorem has
depth ≤ 50.** Adding a theorem above depth 50 cannot change the set of proofs
below it, so the value is fixed by construction — no measurement needed.

| foundation | incidences | proofs | candidates with a nonzero value |
|---|---|---|---|
| depth ≤ 25 | 3,657,211 | 304,518 | 100% |
| depth ≤ 50 | 6,952,395 | 430,358 | 100% |
| depth ≤ 75 | 9,687,995 | 533,754 | 100% |

**Coverage is complete.** Deep declarations are still cited *within* the
shallow foundation, so nothing ends up without a value — the obvious failure
mode of this idea does not occur.

### Cost of freezing

| model | append-safe | NavAP | P@1 | major recall@4 |
|---|---|---|---|---|
| role x live rarity | no | 0.878 | 0.967 | 0.889 |
| promoted 4-factor | no | 0.871 | 0.983 | 0.893 |
| **role x frozen rarity (d≤50)** | **yes** | **0.862** | 0.975 | 0.864 |
| role x frozen rarity (d≤25) | yes | 0.854 | 0.969 | 0.861 |
| **role x depth** | **yes** | **0.846** | 0.897 | 0.820 |

**Freezing costs 0.016.** Dropping counts entirely costs 0.032. Both are far
smaller than the 0.35+ gap to the baselines, so append-safety is affordable.

Note `role x depth` gives up most of its ground at rank 1 (0.897 vs 0.975) —
its weakness is concentrated at the very top and at shallow depth, where it
scores 0.783–0.850 against the frozen-rarity model's 0.969+.

### Residual risk, stated

Freezing is append-safe **only while additions land above the frozen depth**.
A newly added low-depth lemma would perturb the foundation. That is a policy
choice — "the foundation is pinned at version V" — not a property of the
mathematics, and it should be stated as such rather than assumed.

---

## 4. Wrapper demotion — the obvious fix fails

Constraint from the project lead: demote artificial wrapper citations.

The obvious implementation is to demote everything carrying the kernel's
auto-generated flag. **Tested, and it makes things worse in every model:**

| model | without demotion | with demotion |
|---|---|---|
| promoted composite | 0.871 | 0.860 |
| role x frozen rarity | 0.862 | 0.851 |
| role x depth | 0.846 | 0.836 |

The reason is visible in the graded data: **some auto-generated declarations
genuinely are the proof's content** — 4 of 20 in the development sample were
graded CORE. A blanket rule loses those.

This is consistent with, not contradicted by, the challenge-set finding that
proofs *containing* auto-generated candidates have a 0.400 rank-1 defect rate
against 0.017 overall. The population is enriched for defects; the individual
flag is not a sufficient condition.

**A sharper, conditional rule is needed.** That is the subject of
`WRAPPER_DEMOTION.md`.

---

## 5. Viable contenders after both constraints

| method | append-safe | wrapper problem solved | NavAP |
|---|---|---|---|
| **role x frozen rarity (d≤50)** | yes | not yet | **0.862** |
| **role x depth** | yes | not yet | **0.846** |
| ~~promoted 4-factor~~ | **no** | not yet | 0.871 |
| ~~role x live rarity~~ | **no** | not yet | 0.878 |

**The promoted ranking fails the append-safety constraint and is therefore no
longer a candidate**, notwithstanding that it won the sealed test. The sealed
test did not measure this property because it was not stated at the time.

Failure forensics were run only on the two surviving methods, plus the
incumbent as a reference point, on the principle that rigorous forensics
should not be spent on a method that fails the reality check.
