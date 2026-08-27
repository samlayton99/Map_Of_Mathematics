# MathMap Move Formulation — Adversarial Review Package

You are the judge. Two briefs argue over whether the current model is the right foundation; you rule and set direction.

## The question before the court

The MathMap program needs, for every theorem in Mathlib (771k constants), a list of its proof's *mathematically meaningful moves* — the applied lemmas that carry the argument — separated from structural noise (typeclass instances, compiler helpers, tactic certificates, logic glue), with a ranking and zoomable abstraction layers. The program's constitution, set by the project owner: results must be **exact** (no learned/probabilistic scoring), **name-free** (no naming conventions, no namespace rules, no per-tactic knowledge), and **future-proof** (must survive Lean/Mathlib evolution, and get *more* accurate as the library deepens).

The model on trial ("kernel-invariant move formulation"): candidates = constants at load-bearing positions in the proof term (applied step / let-bound / explicit argument — not instance/implicit slots or type annotations); keep Prop-valued constants only; single-use citations are containers (opened for ranking, kept for membership); rank new-to-statement first, then by unfolding depth; group by measured subject-matter relevance (relevant / imported / bookkeeping); strategy facets (induction, case-split, extensionality) from the proof term's root shape.

## What you are asked to deliver

1. A ruling: is this formulation the right foundation to build on — accept / accept-with-conditions / reject?
2. The decisive weaknesses, ranked, with which prosecution charges you find proven vs. dismissed.
3. Concrete next steps: experiments or changes, in priority order. Note: the defense brief §4 lists alternatives already tried and measured — please distinguish genuinely new suggestions from those.

## Procedural notes

- `briefs/DEFENSE.md` was written by the implementing agent (Claude), which built the model and ran all experiments.
- `briefs/PROSECUTION.md` was written by an independent agent instructed to attack the model and the defense with access to all the same files, including the evaluation source code.
- Neither brief was edited after the fact. The prosecution had the defense brief; the defense did not see the prosecution's.
- All numbers in both briefs are reproducible from `data/` (JSON results), `src/` (evaluation code), and the extractor `lean/DepDump.lean`. Seeds are fixed (20260819).

## Package contents

- `CASE_HISTORY.md` — **start here**: the complete chronological narrative of everything learned since the previous results handoff (the Phase 3 zip), stage by stage with evidence files — including the dead ends and negative results.
- `briefs/` — DEFENSE.md, PROSECUTION.md
- `reports/` — the program's research reports in chronological order of the work: DEPTH_ADDENDUM (the depth measure at full scale), CONES_REPORT (statement-cone vs proof-cone; what depth measures), FORENSICS_REPORT (failure taxonomy of the pre-kernel ranking), INVARIANT_RANK_REPORT (Prop-filter + inlining), MOVES_REPORT (the position-aware formulation and its precision/recall), GRADIENT_RELEVANCE_REPORT (subject-matter relevance + abstraction layers), STRATEGIES_REPORT (strategy detection, incl. the documented v1 failure). Plus earlier Phase 3 reports (MACHINERY_SEPARABILITY, LANDMARK_STRUCTURE_AND_RANKING, HONEST_ASSESSMENT) for the learned-topology baseline this program superseded.
- `data/` — all result JSONs cited by the briefs.
- `src/` — Python evaluation code; `lean/DepDump.lean` — the extractor whose output everything consumes.
- `NEXT_RECOMMENDATION.md` — the program's own standing recommendation before this trial.

## Context that may matter for your ruling

- Evaluation sets: 2,355 random theorems (precision-style metrics), 130 proofs with resolvable human source citations (recall), 20 hand-verified proofs (consistency), ~50 hand-read exemplars, 6-11 anchor theorems (qualitative). All from a single Mathlib snapshot (Lean 4.33 era, extracted 2026-08-19).
- The program has a known evaluation gap it admits: rank-1 "genuineness" is measured at scale; rank-1 "keyness" (is it the move a mathematician would name) is verified only qualitatively.
- The intended consumer is a navigation/map interface for humans; a per-proof "moves" view is its core primitive.
