# The synthesis ordering and its forensics (2026-08-21)

## The standing candidate: laneD_stmt

Sort a proof's citations by five ordinal keys, nothing else:

    1. universe    load-bearing occurrences first; data/def constants cited
                   only via implicit/annotation roles enter DEMOTED (U1D)
    2. lane        move (0) < transport (depth_stmt <= 1) (1) < infra
                   (generated or instance-only) (2)
    3. stmt        proof-introduced before statement vocabulary
    4. depth       deepest cited value-depth first (== smallest delta_depth
                   first within a proof)
    5. position    first occurrence in the term

Generated helpers: owned by the target = internal, dropped from the list
(contents still expandable); owned elsewhere = redirected to the owner.
Role tier is NOT a key: with (lane, stmt, depth) in place it changes
nothing (0.9127 with, 0.9127 without) — the role signal that mattered
(instance-slot) lives inside the lane. Every key append-safe; no fitted
constants; demotion never deletion.

## Results (522 graded proofs, owner-equivalent scoring)

| order | KeyMove@1 | R@1 | R@4 | R@8 |
|---|---|---|---|---|
| flat (tier, occ) | 0.472 | 0.303 | 0.734 | 0.877 |
| + lanes | 0.686 | 0.451 | 0.848 | 0.942 |
| + depth key | 0.894 | 0.553 | 0.894 | 0.962 |
| + stmt key | **0.913** | **0.560** | **0.894** | 0.959 |

laneD_stmt vs flat: flips +197/-10, McNemar p = 3.3e-46. Reference points
(both non-compliant, both void): fitted+rarity composite 0.825;
Copeland + live-rarity voter 0.897.

Map level (20k fresh artifacts, top-4 admission, top-100 hubs): laneD
holds 61% mathematics link-mass vs flat 22% (lanes-only view 71% — the
depth key trades ~10 points of hub cleanliness for +21 points KeyMove@1).
stmt at map scale awaits the corrected statement-world rebuild.

## What the failure mining found (54 -> 37 misses)

Round 1 on laneD classified every rank-1 miss by the sort key that made
the wrong call:

- **Metric artifact (8 cases, fixed in scoring)**: graded keys were
  generated `._simp_N` variants whose OWNER was our rank 1 — the
  owner-redirect was right and the metric punished it. Scoring now
  owner-equivalent.
- **Statement vocabulary tops (12, fixed by stmt key, +9/-1)**: deep
  definitions from the theorem's own statement outranked the proof's move.
  This is the OLD proof-introduced-first rule, previously unimplemented.
- **Universe exclusions (3, fixed by U1D expansion)**: definitions cited
  only implicitly could never be ranked. The old U1D rule, previously
  unimplemented. (Also the main driver of R@4 0.81 -> 0.89.)
- **Projection defect of value depth (identified, cure rejected)**: class
  fields (`whisker_exchange`, `vadd_comm`) have value-depth 1-2 because a
  field's proof is a trivial projection — depth measures proof effort, not
  conceptual height. Statement-depth-as-primary fixes these but loses far
  more (+18/-56): deep technical lemmas usually ARE the key and ds (max
  13) is too coarse to lead. Verdict: value depth leads; ds stays a lane
  boundary only.

## Residual failures (37/424), honest taxonomy

- 17 depth inversions — mostly grade-3-vs-4 near misses (`Subtype.ext`
  over `Disjoint.mono`) plus the instance-definition `.mk`-constructor vs
  field-lemma ambiguity. Grade-noise territory.
- 9 lane demotions where the graded key IS `rfl`/`Eq.refl`/`propext` —
  definitional-equality proofs whose whole content is transport, but a
  lane-0 interface operator (`HSub.hSub`) exists and wins. Interface
  vocabulary again (the OfNat/HAdd hub species).
- 3 keys inside target-owned private helpers (`..._proof_1`) — the
  mathematics lives in the collapsed internal step; needs helper
  EXPANSION (walk the helper's own term), an extractor extension.
- Foundations band 0-10 is the weak band (0.771 vs 0.92-1.00 elsewhere):
  depth is flat there — the one place the old rarity signal genuinely
  helped. Candidate Layer D sidecar use, never canonical.
- 6 ties/other.

## Old-idea sweep: status

| idea | status |
|---|---|
| role re-bucketing / instance repricing | absorbed into infra lane; tier key now dead weight, dropped |
| tier merge 5->3 | moot (tier dropped) |
| U1D universe (defs keep all roles) | IMPLEMENTED today (demoted entry) |
| proof-introduced first | IMPLEMENTED today (stmt key) |
| within-proof delta rank | equivalent to the depth key (validated) |
| Condorcet/Copeland | tested compliant: loses to lexicographic (0.741); its old edge was the rarity voter |
| pinned rarity table | deferred to Layer D sidecar; candidate fix for the 0-10 band |
| dmax normaliser removal | moot — no normalisers exist anymore |
| glue rule on arity/isProof | superseded by transport lane (outperforms) |
| wrapper demotion (human wrappers) | NOT done — metamorphic benchmark territory |

## Caveats

- Round-2 keys were chosen after failure analysis on these same labels.
  Mitigation: stmt and U1D are pre-existing registered rules, not
  inventions; owner-equivalence is a metric fix; the grid was small and
  ordinal. Still: fresh validation (metamorphic, or any new graded round)
  before promotion.
- Raters saw candidate depth (brief contamination), which inflates
  depth-keyed scores by an unknown amount.
- stmt flag currently from brief annotations (graded candidates only);
  production needs the corrected statement-world rebuild.
