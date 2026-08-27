# Kernel-Invariant Ranking — Design + First Measurements (2026-08-19)

Requirement (Sam): fixes must approach 100% as the library deepens and survive Lean's evolution — no naming conventions, no per-tactic patches. Principle adopted: every rule must be expressible in the kernel calculus (type vs value, Prop vs Type, the reference graph), the layer that cannot change without Lean ceasing to be Lean. Code: `src/invariant_rank.py`; data: `data/invariant_rank_results.json`; same 2,355-theorem sample as FORENSICS_REPORT.

## Rules tested

- **R1 moves-must-be-Props**: rank only Prop-valued references (kind=theorem proxy; final form should check `type : Prop` directly). Kernel fact: an instance constructs an object, so it cannot be a propositional step.
- **R2 inline-single-use**: a reference cited by exactly one constant in the library is private workings, not shared knowledge; replace it by its own references, recursively (≤4 rounds). Pure graph fact.

| variant | top-1 content | top-2 | shallow | mid | deep |
|---|---|---|---|---|---|
| baseline (new,depth) | 79.2% | 88.3% | 66.1% | 84.5% | 87.1% |
| + R1 Prop-only | 82.5% | 89.1% | 77.1% | 83.7% | 85.6% |
| + R2 inlining | **85.3%** | **91.1%** | **80.0%** | 86.9% | 87.9% |

Self-helper failure mode: 96 → 6 (dead). R1 additionally produces 360 "no Prop ingredients → holds by definition/computation" verdicts (mostly `rfl`-style lemmas; spot-verification of this set still pending). Shallow tercile +14 points — much of the shallow floor was Type-valued noise, not glue ties.

## Negative result (report honestly)

R3 simple statement-exposure (count how many types mention a concept; hypothesis: tactic vocabulary is unexposed) **failed**: AUC 0.40, medians identical. Cause: raw mention-counts saturate on universal vocabulary, and large tactic libraries state hundreds of internal lemmas about their own types (`Lean.Grind.CommRing.Expr` has 412 type-mentions vs `Nat.gcd`'s 345). Exposure must be *directional*: nothing **outside** a tactic's own cluster ever mentions its vocabulary in a statement; omega/grind are statement-secluded islands connected to mathematics only through proof edges. That seclusion measure is designed but untested.

## Anatomy of the remaining 15% (V3 failures, read manually)

1. **Prop-valued instances** (~99 blames): `Real.locallyFinite_volume`, `IsTopologicalRing.toIsSemitopologicalRing`, `Finset.instMulRightMono` — kernel-honest propositions that function as typeclass plumbing. R1 cannot see them. True invariant: **occurrence position in the proof term** — a reference *applied as the head of a Prop-producing application* is a move; one *filled into an instance-implicit binder* is setting. Both are term-structure facts (this is the Phase 2 P4-route definition globalized — the extractor must record positions; `getUsedConstantsAsSet` is position-blind).
2. **Neighbor byproducts** (~96): other lemmas' `._simp_N`/`._proof_N` variants, multi-use so R2 doesn't touch them. They are shadows of real lemmas; displaying statements instead of names dissolves most of the harm, attribution-to-parent the rest.
3. **Glue ties** (~70): `Iff.rfl`, `congrArg`, `And.left` — Prop-valued logical bookkeeping, worst in shallow regions. Designed fix (untested): **universal-vocabulary rule** — a move whose statement mentions only concepts present in ~every statement-closure (Eq, Iff, And) is bookkeeping; rank moves by the rarity of their rarest subject concept. Library-relative, name-free.
4. **Tactic certificates** (~23): small blame share; awaits the seclusion measure.
5. Some `no_content` (5.5%) verdicts are **correct**: proofs that only manipulate local hypotheses (`SSet.Subcomplex.prod_monotone` = take parts of a conjunction) have no named moves — the known structural ceiling, not a ranking failure.

## Longevity argument

Each failure family is either (a) eliminated at all depths by a kernel rule (instances/R1+positions, self-helpers/R2), or (b) confined to a bounded region near the axioms (glue ties live below depth ~15), so error → 0 as the library deepens. The seclusion separation for tactic machinery *widens* as the library grows: real concepts accumulate statement-mentions, tactic vocabulary structurally cannot. Nothing references a name, a namespace, or any convention above the kernel.

## Next

1. Extend `mathrecord depdump` to record occurrence positions (head-of-Prop-application vs instance-binder vs type-only) — one extractor change that upgrades R1 to the true move test and likely absorbs most of failure modes 1–2.
2. Test the universal-vocabulary rule on the glue-tie residue.
3. Design + test statement-seclusion for tactic vocabulary.
