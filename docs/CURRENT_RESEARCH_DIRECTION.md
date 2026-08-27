# Current Research Direction — Typed Proof Search (study-paths)

*Supersedes the phase-3 structural-separability direction (archived at `archive/handoff_phase3/`). Written 2026-08-27.*

## Thesis

Proof search over Lean proof states is graph construction: a state is a partially built proof term with typed holes (metavariables); a move fills a hole by unifying a constant's conclusion with it, spawning argument holes; success is a kernel-checked term. Human-written Mathlib proofs — stored as elaborated proof terms — are certified witness paths through exactly this graph. They serve three roles, never consulted at inference time: failure attribution (oracle ladders), engine conformance testing (replay), and unbiased training data (per-node decisions with Lean-verified alternatives).

## Established results (all on the 80-theorem module-holdout benchmark unless noted)

1. **Engine conformance is a solved gate.** Exact replay 100% (380 theorems / 8,252 nodes); guided execution with the exact route (G1) 80/80, audit-clean. Every past G1 failure was a nameable engine defect (dedup slots, context binding, deferred-data divergence, instance-synthesis preemption, elaborator-vs-kernel defeq incompleteness) — fixed by general mechanisms, catalogued in the cycle reports.
2. **The action generator is near-complete and the space stays sparse.** First-order visibility of reference heads 74.7%; + mechanical higher-order operators (motive-from-goal, positional diff-congruence, argument abstraction, conclusion deferral) → 88.4%. Median legal actions/state: 5.
3. **Kernel certificate grain ≠ search decision grain.** Machine-generated simp/congruence certificates (congrArg/Eq.mpr chains) are multiplicatively fragile to reconstruct node-by-node but compress to single rewrite actions parameterized by ~2 facts (semantic traces: 0.38–0.44 action/node ratio). The stable search IR is: semantic action → exact expandable certificate.
4. **Semantic ladder.** Representability (regions by exact expansion) 80/80; mechanical execution via `simp only` with extracted facts: 67 with residual-data oracle, 64 without, 69–73 with node-grain fallback; free search with the semantic action ranked first: 65 vs 30 budget-matched control (node-grain hint: 30). Fabrication gap (C−D) = 3 theorems.
5. **Per-decision ranking is learnable.** LGBMRanker v3 on the complete higher-order-visible decision space (29,585 train / 1,046 held-out): top-1 0.645, top-3 0.915, MRR 0.786 vs 0.353 best hand baseline.
6. **Inference-shadow tiers** (25,768 data-argument occurrences): 62% immediately inferable, 33% inferable after sibling constraints, 5.2% genuine fabrication (mostly lambdas/motives).

## Architecture invariants

- Two-layer action representation: stable semantic actions (apply/intro/have/rewrite-with-explicit-set/cases/constructor/exact) expanding to exact kernel certificates. Explicit fact sets, never live global simp state, define canonical edges.
- State identity is structural (local context + goal types), never mvar-id-based.
- Success requires kernel verification + source-accessibility audit (no target auxiliaries, no forbidden module constants); dirty proofs are normalized (forbidden-constant unfolding) or rejected.
- Every capability claim rides an oracle-ladder condition with budget-matched controls; solved-set dominance is checked.

## Where the program is heading

Learned hierarchical policy over semantic actions (family, then parameter — retrieval-style for rewrite sets), plugged into best-first search; expert iteration only after per-decision quality is established. See `NEXT_RECOMMENDATION.md` for the immediate step.
