# Verification and freeze certification (2026-08-21, final)

Sam's directive: verify the cleanup gains are real; one more disciplined
push. Result: verification CORRECTED the freeze (rules re-scoped), then
the frozen construction was propagated through every apparatus and
certified. No new search was opened.

## 1. Verification of the cleanup gains

- **Flag integrity**: 8/8 spot checks (OfNat.ofNat/DFunLike.coe/
  Membership.mem/HAdd.hAdd flagged; mul_comm/Real.exp/sum_congr/
  Nat.card not).
- **The load-bearing statistic is solid**: class-projection junk share
  0.954, Wilson 95% CI [0.922, 0.973] (n=281 blind slots).
- **Honest small-n statement**: the definition KM jump 0.677 -> 0.742
  is TWO proofs (n=31). The rule stands on the per-item statistic, not
  the per-target delta.
- **Held-out transfer tests CAUGHT AN OVER-REACH**: on the old corpus
  (independent for this rule), classproj demotion on THEOREM targets is
  slightly negative in ranking (KM 0.9127 -> 0.9057, flips +0/-3) and
  inclusion (F1 0.7188 -> 0.7104). On blind theorems it was neutral.
  **Correction adopted: all three cleanup rules (ctor exclusion, U1D
  admission, classproj demotion) are scoped to DEFINITION TARGETS
  ONLY.** Theorems keep the twice-confirmed base construction.
- **Residual failure mine**: no large clean class remains (largest: 23
  diffuse near-target junk defs; transport-stmt items proven
  unfixable). The stop rule fires genuinely.

## 2. Propagation: the frozen construction through every apparatus

| artifact | edges | AMI | AUC | within-area | hub share | co-use lift |
|---|---|---|---|---|---|---|
| GAP2 = frozen zoom-1 (gap + def admissions) | 1.15M | **0.391** | 0.631 | 78.0% | 10.6% | **20.7x** |
| LATFIX_GAP2M = frozen ATLAS DEFAULT (scoped, rho<=1/2) | 816k | 0.393 | 0.669 | 77.4% | 9.4% | — |
| FINAL = union reading view (raw) | 1.96M | 0.360 | 0.572 | 60.0% | 13.3% | 5.8x |
| LATFIX_FINAL = union view, rendered | 1.28M | **0.414** | **0.702** | 80.1% | 8.7% | — |

Two architectural facts certified quantitatively:
1. **The layers are real objects with different jobs**: the tight zoom-1
   carries the kinship geometry (20.7x, indistinguishable from the
   pre-freeze 23x); the union is a per-proof reading boundary whose raw
   form dilutes kinship (5.8x) but whose RENDERED form has the best
   structure numbers yet (AMI 0.414, AUC 0.702).
2. The def-target admissions HELP the map (AMI 0.386 -> 0.391), they do
   not dilute it.

Metamorphic: unchanged by construction — the scoped rules fire only on
definition targets and the variant corpus is theorems.

## 3. The frozen construction, final statement

- Ranking: laneD_stmt; for definition targets additionally ctor
  demotion and classproj -> infrastructure.
- Inclusion zoom-1: largest-gap cut; definition targets additionally
  admit U1D items above the threshold (non-ctor, non-classproj).
- Reading view: zoom-1 UNION move-lane; definition targets exclude
  ctor/classproj from the lane side.
- Atlas: zoom-1, sources scoped to Mathlib mathematics, rho<=1/2
  vertical rendering (swept: plateau).
- All rules: kernel/elaborator facts, ordinal keys, stated small
  integers; no names, no fitted constants in any canonical layer.

Confirmation debt (stated wherever the numbers appear): the def-target
rules were developed on the blind set (now dev data) and their
theorem-side scoping on the old corpus; one fresh sample confirms or
trims them. The construction is otherwise FROZEN.
