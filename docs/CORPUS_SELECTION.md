# Phase 2A Corpus Selection

Pinned source: `leanprover-community/mathlib4` tag `v4.33.0` (commit `db584cd6d46c92f209a44c0f1c829460d327499d`), toolchain `leanprover/lean4:v4.33.0` — identical to the MathRecord toolchain. Local checkout: `corpusenv/mathlib` (shallow clone at tag; gitignored; recreate with `git clone --depth 1 --branch v4.33.0`).

## Files (6 areas)

| File | Area | Why chosen |
|---|---|---|
| `Mathlib/Algebra/Group/Basic.lean` | algebra | dense simp-lemma file; mix of one-line term proofs, rewriting, calc |
| `Mathlib/Order/Lattice.lean` | order theory | typeclass-heavy (`SemilatticeSup` etc.); instance synthesis in every proof |
| `Mathlib/Topology/Basic.lean` | topology | deep import closure; filter/instance machinery; small enough to elaborate |
| `Mathlib/Data/Nat/GCD/Basic.lean` | number theory | recursion/induction (`Nat.gcd` well-founded), explicit lemma application |
| `Mathlib/Logic/Function/Basic.lean` | logic/foundations | injective/surjective reasoning, classical logic, function extensionality |
| `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` | analysis | automation-heavy (`simp`, `field_simp`, `positivity`), coercion-heavy (ℝ casts) |

Each file is processed standalone (one file per extractor process, ADR-0001); its declarations land in `map₂` (exact records with proof bodies) and every referenced imported declaration gets a shallow exact record (type + sid + classification). Target of 500–2,000 backing declarations is checked after extraction and reported in the characterization, not assumed.

## Why representative enough for this stage

The six files span algebra/order/topology/number theory/logic/analysis; proof styles include term-mode one-liners, rewrite chains, typeclass-driven proofs, induction/recursion, and automation-heavy analysis lemmas — the styles the handoff requires (tactic, term, explicit application, rewriting, simplification, structures, typeclasses, recursion, automation). Generated declarations enter as a measured minority (they appear in `map₂` alongside their parents and are classified, not excluded). This is a bounded characterization sample, not a claim of Mathlib-wide representativeness; domain-level conclusions are reported per file so no single area dominates silently.

## Showcase set

40–80 proofs drawn across all six files after extraction, stratified by proof style (term / rewrite / typeclass / induction / automation) and size. Selection is recorded in the review bundle (`analysis/` output) with the stratification labels; every non-internal theorem/def in each file gets the full projection treatment regardless, so the showcase choice only affects which proofs get human-review artifacts.
