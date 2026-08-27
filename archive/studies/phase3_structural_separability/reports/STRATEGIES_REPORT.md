# Proof-Strategy Detection from Kernel Signatures (2026-08-19)

Goal (Sam): detect proof strategies — contradiction, cases, contrapositive, induction, etc. Constraint: kernel signatures, no tactic names. Code `src/strategies.py` (v1), `src/strategies2.py` (v2); data `data/strategies{,2}_results.json`. Validation: regex over human tactic text in Mathlib source (imperfect ground truth) on 1,100–4,000 resolved proofs.

## v1 (set-membership anywhere in the term) — failed, kept for the record

Contradiction precision 0.095 (False-handling appears inside compiled automation everywhere); induction recall 0.0 (compiled recursion never cites itself — it lives in `WellFounded.fix`/`brecOn` inside single-use helpers). Lesson: **strategy is the root-level shape of the proof term, not a bag of constants.**

## v2 (root grain) — extractor extended, mixed results

Dump v3 adds `rt` (outermost head chain: peel binders, take head, descend into the last explicit argument, ≤5 layers, spliced through single-use helpers) and `ir` (`InductiveVal.isRec` — kernel fact). Signatures: induction = well-founded fix operators, recursors of recursive inductives, and the recursion-combinator closure (defs whose body head is such a combinator — catches `WellFounded.Nat.fix → fix.go → Nat.rec` without any name); case-split = eliminator (or wrapper) of a multi-constructor inductive; the rest = core logical operators in the chain, with a goal-polarity guard for contradiction (False-handling in a proof of a `Not`-statement is inherent, not a strategy).

| strategy | rate | precision vs source | recall vs source | verdict |
|---|---|---|---|---|
| induction | 2.4% | 0.30 | 0.46 | **works** — all anchor recursion proofs correct (`pow_iterate`, `zpow_mul`, `List.length_append`, `pow_sub_one_gcd`); precision cost from the combinator closure's known over-breadth |
| case_split | 4.0% | 0.47 | 0.21 | **works at the root**; misses mid-proof case splits the chain cannot see |
| extensionality | 10.3% | 0.75 | 0.13 | precise at the root; `ext` mostly fires mid-proof |
| contradiction | 3.0% | 0.09 | 0.33 | grain mismatch (below) |
| choice / contrapositive / computation | ≤0.2% | ~0 | ~0 | grain mismatch (below) |

## The finding: two kinds of "strategy"

**Term-visible strategies** — induction, case analysis, extensionality — are *structural events*: the kernel term's root shape is the strategy, and detection works and will keep working (recursors and fix operators are kernel machinery; `isRec` is a kernel fact).

**Intent-level strategies** — by_contra, contrapose, choose, decide — are *human moves in the tactic layer* that compile into terms with no distinctive root shape: classical case analysis appears in compiled helpers of proofs whose authors never typed `by_contra` (all 20 contradiction false-positives), and `contrapose`/`choose` leave only mid-term traces. At the kernel grain, "the term does classical negation reasoning" and "the human chose proof by contradiction" are different facts, and only the first is structurally recoverable. Recovering the second honestly needs either occurrence-prominence data (which strategy constant dominates the term's mass — a further dump extension) or acceptance that intent lives in the tactic layer and should be extracted from there *as provenance, labeled as such*.

Validation ground truth is itself noisy (regex over tactic text; `obtain` on an existential is destructuring, not case analysis; `simp` hides case splits), so the precision/recall numbers are lower bounds on signature quality.

## Standing recommendation

Ship the three term-visible tags (induction, case-split, extensionality) as map facets now; hold intent-level tags until either prominence data or an explicit provenance channel exists. Keep v1's failure documented — it is the argument for grain in any future signature design.
