# Proof 10

Theorem `iteratedDeriv_vcomp_three` (Mathlib source below).

```lean
theorem iteratedDeriv_vcomp_three (hg : ContDiffAt 𝕜 3 g (f x)) (hf : ContDiffAt 𝕜 3 f x) :
    iteratedDeriv 3 (g ∘ f) x =
      iteratedFDeriv 𝕜 3 g (f x) (fun _ ↦ deriv f x) +
      iteratedFDeriv 𝕜 2 g (f x) ![iteratedDeriv 2 f x, deriv f x] +
      2 • iteratedFDeriv 𝕜 2 g (f x) ![deriv f x, iteratedDeriv 2 f x] +
      fderiv 𝕜 g (f x) (iteratedDeriv 3 f x) := by
  simp only [← iteratedDerivWithin_univ, ← iteratedFDerivWithin_univ,
    ← derivWithin_univ, ← fderivWithin_univ]
  exact iteratedDerivWithin_vcomp_three hg hf uniqueDiffOn_univ
    uniqueDiffOn_univ (mem_univ x) (mapsTo_univ f _)

```

## Candidate views (anonymized)

### View A
  1. uniqueDiffOn_univ
  2. iteratedFDerivWithin_univ
  3. iteratedDerivWithin_vcomp_three
  4. iteratedDerivWithin_univ
  5. fderivWithin_univ
  6. derivWithin_univ
  7. Set.mem_univ
  8. Set.mapsTo_univ

### View B
  - Set.mapsTo_univ
  - Set.mem_univ
  - _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_1
  - _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_2
  - _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_3
  - _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_4
  - congr
  - congrArg
  - congrFun
  - congrFun'
  - funext
  - iteratedDerivWithin_vcomp_three
  - uniqueDiffOn_univ

### View C
  1. iteratedDerivWithin_vcomp_three
  2. _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_1
  3. _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_2
  4. _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_3
  5. _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_4
  6. uniqueDiffOn_univ
  7. Set.mapsTo_univ
  8. Set.mem_univ
  9. funext
  10. congrFun

### View D
  1. congrFun
  2. congrArg
  3. Set.mapsTo_univ
  4. congr
  5. funext
  6. uniqueDiffOn_univ
  7. congrFun'
  8. iteratedDerivWithin_vcomp_three
  9. Set.mem_univ
  10. _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_4

### View E
  - iteratedDerivWithin_vcomp_three
  - _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_1
      . iteratedDerivWithin_univ
      . Eq.symm
  - _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_2
      . iteratedFDerivWithin_univ
      . Eq.symm
  - _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_3
      . derivWithin_univ
      . Eq.symm
  - _private.Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno.0.iteratedDeriv_vcomp_three._simp_1_4
      . fderivWithin_univ
      . Eq.symm
  - uniqueDiffOn_univ