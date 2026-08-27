# Reference — Phase 2 Facts and Corrections

## Established implementation evidence

Gates 0–1 established, on the tested pinned environment and micro-corpus:

- deterministic serialization;
- exact expression round trips;
- tested alpha-invariant structural identities;
- separate type and body dependencies;
- local-context reconstruction;
- Lean kernel rechecking;
- alternative proof artifacts;
- explicit failure and `sorryAx` handling.

Phase 2 represented:

- 1,711 stored declarations with bodies;
- 3,493 additional shallow referenced declarations;
- 5,204 backing declarations total;
- 1,233 theorem/definition candidates;
- 1,303 local states;
- 4,827 observed transitions.

The raw proof-style totals were:

- 850 term;
- 168 automation;
- 180 rewrite;
- 27 other tactic;
- 8 induction;
- total 1,233.

P3 used overlapping deterministic classifications:

- `typeclass-instance` from the environment instance table;
- `recursor` from declaration kind;
- `structure-projection` from the environment projection table;
- `generated` from documented generated suffix patterns;
- `internal-detail` from Lean internal-detail metadata;
- `eq-machinery` from a fixed list;
- `logic-core` from a fixed list;
- `coercion` from name-root rules.

P3’s empty classification was treated as presumed domain mathematics in the report, but this was a design heuristic rather than verified semantics.

## Three corrections that must remain visible

### 1. Containment was not universal

Per-file median containment could be 1.0, but individual theorem rows violated the claimed strict nesting. At least 61 relevant rows had P5-to-P2 containment below 1.

P2, P4, and P5 are related views, not universally nested sets.

### 2. Term proofs were not 76%

The raw fraction was:

\[
850/1233 \approx 68.94\%.
\]

Depending on filtering and denominator, the defensible summary is roughly 67–69%.

### 3. P4 result-type inference was not overwhelmingly successful

Weighted raw success was approximately 61% overall, with substantial domain variation.

Because P4-route filters partly on inferred result type, missing inference can remove useful applications. Compression can therefore reflect both abstraction and missingness.

## What Phase 2 did not establish

- that P3 residue is true mathematical content;
- that P4-route captures human proof strategy;
- that the P3/P4/P5 hybrid improves theorem proving;
- that graph topology identifies semantic importance;
- that any projection should become canonical.
