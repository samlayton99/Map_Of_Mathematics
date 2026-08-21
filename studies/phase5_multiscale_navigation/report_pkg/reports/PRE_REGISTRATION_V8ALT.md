# Pre-Registration — V8-alt candidate ranking comparison

Written 2026-08-20 **before any candidate was scored**. Fixed by the owner's
brief. Corrections after results go in a dated addendum with the reason.

## Governing principles (from the brief, binding)

1. **Nothing is deleted.** Every candidate is an *ordering* over the complete
   load-bearing incidence record. "Glue", "definition", "construction",
   "instance" are roles and ranking signals, never reasons information
   disappears. At the fully open end of the slider the exact underlying
   support is recoverable.
2. **Definitions are first-class candidates**, with declaration kind and
   occurrence role preserved so theorem-moves, definition/construction-moves,
   or both can be viewed separately.
3. **No intuition-tuning of a new V8.** Freeze the candidates below and
   compare them scientifically.
4. **Three evaluation questions stay separate.** Do not change the answer to
   Q1 or Q2 to make Q3 look prettier or more connected.
5. **Robustness means the meaning of relations and the procedure survives**
   library growth — not that ranks, depths or components stay numerically
   frozen. Library-relative geometry should evolve as mathematics grows.

## The frozen candidates

All are total orders over the same base: every load-bearing incidence
(8,485,349 of them; roles applied / let-value / explicit-arg / unresolved).
Ties break by declaration id for determinism. Non-content items are ranked
LOW, never removed.

| id | ranking | sort key (ascending) |
|---|---|---|
| **C1** | V8-faithful | (not a claim, logic-only or machinery, not proof-introduced, −depth) |
| **C2** | V8 + all kinds restored | (logic-only or machinery, not proof-introduced, −depth) — kind ignored, so definitions compete on equal footing |
| **C3** | pure depth | (−depth) |
| **C4** | proof-introduced, then depth | (not proof-introduced, −depth) |
| **C5** | Phase 5 composite | (−w), w = role × statement-relation × depth × idf |

C1 reproduces the frozen V8 ordering as faithfully as possible while obeying
principle 1: what V8 *filtered out*, C1 merely *ranks last*. This is the only
difference from V8 and it is required by the brief.

## Ground truth for Q1 and Q2

Lean's elaborator records which identifiers the human actually wrote in each
declaration's source. That answer key never passes through our extraction and
uses no naming heuristics. Available for **4,544 declarations** across 40
elaborated files.

**Proof-written citations** = elaborator-resolved references of the
declaration MINUS those already resolved from its own statement. This
approximates "what the human typed as part of the argument" and is the
semantic target. The earlier circular-harness defect (filtering the answer key
by the predicate under test) is explicitly not repeated: **no candidate's own
filter is applied to the answer key.**

## Q1 — Coverage / recall. Did we preserve the meaningful moves?

- **Q1.1** For each proof, the fraction of proof-written citations present
  anywhere in the ranked list. This tests the RECORD, and should be near
  identical across candidates by principle 1 — any difference is a bug.
- **Q1.2** recall@k for k ∈ {1, 2, 4, 8, 16} per candidate.
- **Q1.3** Mean reciprocal rank of proof-written citations.
- **Q1.4** The same, restricted to proofs V8 currently leaves empty
  (21.9% of theorem proofs). *Registered question: does restoring
  definitions explain proofs the claim-only view could not?*

## Q2 — Precision / keyness. Are the top-ranked items the important ones?

- **Q2.1** P@1: is the rank-1 citation one the human wrote in the proof?
- **Q2.2** P@1 restricted to citations that are definitions/constructions —
  does restoring definitions *cost* precision, as the brief anticipates?
- **Q2.3** Stratified by **theorem depth** and by **cited-declaration depth**.

**Registered hypothesis, to be tested and not assumed** (the owner's, stated
as a hypothesis): *what counts as acceptable glue or a meaningful move changes
with mathematical depth — glue at rank 1 would badly hurt precision for a deep
theorem, while similar logical machinery may legitimately be the mathematical
content of a theorem near the foundations.*

**Operationalised:** if true, then for shallow theorems the human-written
citations should themselves frequently be logic-only/glue declarations, and
P@1 for a glue-ranking candidate should *rise* as depth falls. If instead
human-written citations at shallow depth are just as non-glue as at deep
depth, the hypothesis is falsified. Report the curve either way.

## Q3 — Global structure. What emerges across Mathlib?

- **Q3.1** Components and giant-component fraction as a function of k
  (citations admitted per proof), per candidate.
- **Q3.2 (the merge census).** For every component merge as k increases,
  record **which ranked citation caused the merge and what kind it was**:
  theorem, definition/construction, instance, or glue. *Registered question:
  are definitions the long-distance bridges the claim-only view was hiding?*
- **Q3.3** Principled slider locations. Look for phase transitions rather
  than picking k ∈ {1,2,4,8} for convenience: rate of component merging,
  derivative and change-point behaviour of the giant-component curve, and
  graph entropy of the component-size distribution. These are used to
  **select and navigate** slider positions, never baked into the local
  ranking.
- **Q3.4 (island/technique hypothesis, with controls).** Preliminary examples
  suggested sparse top-1 components group proofs by technique (classical
  choice, quotients) rather than subject. **Do not infer this from examples.**
  Compare real components against size-, depth- and module-matched controls
  and against shuffled-ranking controls. Report the effect size or its
  absence.

## What would change our mind

- If C1 and C2 have indistinguishable Q2 precision, restoring definitions is
  free and should be adopted immediately.
- If C3 (pure depth) matches or beats the composites on Q2, the elaborate
  machinery is not earning its complexity and the simplest ranking wins.
- If the depth-stratified curve is flat, the owner's glue-by-depth hypothesis
  is falsified and the evaluation should not be stratified by depth.
- If merges are caused overwhelmingly by glue rather than definitions or
  theorems, then rapid reconnection is a plumbing artifact and not the
  structural property it appears to be.

## Explicitly out of scope this round

No new ranking invented by intuition. No optimisation of any ranking against
a graph statistic. No forcing of connectivity through the ranking. The virtual
root remains a display/topology device only.
