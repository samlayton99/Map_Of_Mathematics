# P2 — Metamorphic benchmark for the laneD skeleton (2026-08-21)

Does the top of the laneD ranking survive harmless proof refactoring, and does
it diverge when the proof route genuinely changes? This validation touches no
human grades, so the round-2 contamination caveat in `SYNTHESIS_LANED.md` does
not apply to it.

## Verdict

**laneD's rank-1 move is invariant; its rank 2-4 tail is not.**

Top-1 agreement is 0.868 on harmless pairs and **0.000** on control pairs —
perfect separation of the navigational move from the noise. Top-4 set overlap
separates too (0.619 vs 0.101) but is much weaker, because positions 2-4 fill
with type/interface vocabulary (`HAdd.hAdd`, `OfNat.ofNat`, `Nat`,
`Real.instCommSemiring`) whose membership tracks proof *length*, not proof
*route*. Every one of the six required families beats the control baseline.

Two real defects found, both already on the register:
1. **Wrapper insertion destroys rank 1** (family F5, top-1 agreement 0/3). A
   forwarding helper becomes the rank-1 "move"; a helper Lean names under the
   target is dropped entirely and takes the mathematics with it.
2. **`fun_prop`/`ring`-style automation is not a harmless refactor** at the
   citation level — it substitutes a different certificate vocabulary.

## Corpus

`metamorphic/Variants.lean` (compiles clean against Mathlib @ Lean 4.33),
14 groups / 49 variant declarations / 46 pairs, extracted with
`mathrecord hierdump` into `metamorphic/variants_hier.jsonl` —
**52/52 rows ok=true, 0 truncated**. Ground truth in `metamorphic/manifest.json`.

## Ordering under test — laneD, not laneD_stmt

    key = (dem, lane, -depth_value, first_occurrence)

Every variant in a group proves the **same statement**, so the `stmt` key
(proof-introduced vocabulary before statement vocabulary) is a group-constant
relabelling of candidates and cannot separate variants. `laneD` is the honest
object here. `dem` = U1D demoted entry (non-Prop cited only via non-load-bearing
roles); `lane` = infra(2) if generated or instance-slot-only, transport(1) if
`depth_stmt <= 1`, move(0) otherwise; load-bearing roles `{0,1,2,7}`.
Generated-owner redirect: owner = longest non-gen dot-prefix; owned by the
target itself (or by nothing) -> dropped as internal.

New declarations absent from the frozen `names.json`: a name owned by another
known declaration (`mm_g1_v1.proof_1`, `mm_g5_v3.aux`) is treated as generated
and goes through the redirect; an otherwise-unknown declaration
(`mm_g5_helper`, `mm_dbl`) gets lane 0 and depth = 1 + max depth of what its
own body cites. Adding role tier back as a tiebreak changes nothing
(0.6187 -> 0.6266 mean top-4 Jaccard).

## Results

`top4C` = |A∩B| / min(4, |A|, |B|) — a length-robust companion, since several
term-mode proofs cite fewer than four constants at all and cap Jaccard
mechanically. `rawJ` = Jaccard of the unordered load-bearing citation sets,
i.e. what you would get with no ranking at all.

| family | groups | n | top4 J | top4 C | **top-1** | rawJ | beats control |
|---|---|---|---|---|---|---|---|
| F1 simp/simpa vs rewrite chain | g1 g3 g8 g9 g11 | 7 | 0.292 | 0.441 | 0.857 | 0.284 | yes |
| F2 inline vs named `have` | g1 g2 g3 g7 g8 g9 g10 g11 | 11 | 0.718 | 0.803 | **1.000** | 0.763 | yes |
| F3 tactic vs term mode | g1 g2 g3 g4 g7 g8 g9 g10 | 8 | 0.767 | 0.844 | 0.875 | 0.691 | yes |
| F4 explicit vs inferred instance | g4 | 3 | 0.833 | 1.000 | **1.000** | 0.667 | yes |
| F5 wrapper insertion | g5 | 3 | 0.611 | 0.889 | **0.000** | 0.333 | yes (J only) |
| F6 fold vs unfold | g6 | 4 | 0.275 | 0.438 | **1.000** | 0.239 | yes |
| F8 witness/constructor syntax | g7 | 2 | 1.000 | 1.000 | **1.000** | 1.000 | yes |
| **HARMLESS (all)** | | **38** | **0.619** | **0.739** | **0.868** | 0.575 | — |
| **CONTROL (all)** | g2 g10 g11 c1 c2 c3 | **8** | **0.101** | **0.156** | **0.000** | 0.060 | — |

Spearman over shared candidates is ~0.99 for harmless *and* ~0.98 for control
and does not discriminate: once two proofs cite the same constant, laneD is a
deterministic function of that constant, so shared candidates are always
ordered the same way. All the signal is in *which* candidates are present.
Reported in the JSON, not used for the verdict.

## Worst offenders

**mm_g8_v1 vs mm_g8_v2** (F1, J = 0.00, top-1 differs) — `Continuous fun x : ℝ => x^2 + 3*x`

    fun_prop : Continuous.fun_pow, Continuous.prodMk, Continuous.comp', Continuous.const_mul
    manual   : continuous_pow, Continuous.add, Continuous.mul, continuous_const

Honest reading: this is misclassified as harmless. `fun_prop` proves it by
composing through a product, which is a genuinely different route. Same for the
`ring` control in g11, whose top-4 is entirely `Mathlib.Tactic.Ring.*` /
`Mathlib.Meta.NormNum.*`. Automation tactics that synthesise a certificate are
control-like, not refactor-like — a finding, not a bug in laneD.

**mm_g5_v1 vs mm_g5_v2 / v3** (F5, top-1 agreement 0/3) — `l.reverse.reverse = l`

    v1 direct        : List.reverse_reverse, Nat, List
    v2 free wrapper  : mm_g5_helper, Nat, List          <- wrapper IS the move
    v3 owned wrapper : Nat, List                        <- move vanished entirely

This is exactly the "wrapper demotion (human wrappers) — NOT done" row of the
old-idea sweep, and the "3 keys inside target-owned private helpers" residual
failure, reproduced deliberately and now measured. Two distinct bugs: a
free-standing wrapper is admitted as a landmark, and a target-owned wrapper is
dropped without expanding into it. Both need helper EXPANSION (walk the
helper's own term), an extractor extension.

**mm_g6_v1/v2 vs mm_g6_v3** (F6, J = 0.17, top-1 identical) — `mm_dbl n = n + n`

    folded   : two_mul, mm_dbl, HAdd.hAdd, HMul.hMul
    unfolded : two_mul, Nat, Nat.instNonAssocSemiring

Rank 1 (`two_mul`) is stable; the definition `mm_dbl` appears only in the
folded proofs, which is *correct* behaviour (the unfolded proof term genuinely
never mentions it). Low Jaccard here is the metric being unfair, not laneD
being unstable.

**mm_g3_v1 vs mm_g3_v2** (F1, J = 0.14, top-1 identical `min_assoc`) and
**mm_g11_v1 vs mm_g11_v2** (J = 0.17, top-1 identical `add_sq`) — the tail is
`Eq.mpr, congrArg, Eq.refl` (tactic-mode plumbing) vs `Real, Real.instCommSemiring`
(term-mode type arguments). Same species: rank 1 right, tail is proof-mode
residue.

## What this says for P3

- Rank 1 is the product worth shipping. Top-4 as a *set* is not stable enough
  to be a promise; either shorten the visible budget or filter the tail.
- The tail instability is one species — interface/plumbing vocabulary
  (`HAdd.hAdd`, `OfNat.ofNat`, `Eq.mpr`, `congrArg`, bare types) surviving into
  lane 0. This is the same OfNat/HAdd hub species already named in the
  residual-failure taxonomy. A lane rule that catches it should be re-run
  against this benchmark, which is grade-free and therefore a legal test.
- Wrapper handling (F5) is the one family where laneD is outright wrong at
  rank 1 and must change.

## Reproduce

    cd corpusenv/mathlib
    ~/.elan/bin/lake env lean <repo>/studies/phase6_stable_local_geometry/metamorphic/Variants.lean
    ~/.elan/bin/lake env <repo>/mathrecord/.lake/build/bin/mathrecord hierdump \
        <repo>/studies/.../metamorphic/Variants.lean \
        <repo>/studies/.../metamorphic/names.txt \
        <repo>/studies/.../metamorphic/variants_hier.jsonl
    ~/venv/general_ml/bin/python studies/phase6_stable_local_geometry/src/metamorphic_eval.py

Full per-pair records, including every top-4 list, in
`data/metamorphic_results.json`.
