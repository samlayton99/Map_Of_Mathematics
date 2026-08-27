# Proof 22

Theorem `CochainComplex.HomComplex.Cocycle.toSingleMk_postcomp` (Mathlib source below).

```lean
lemma toSingleMk_postcomp
    {p q : ℤ} (f : K.X p ⟶ X) {n : ℤ} (h : p + n = q) {X' : C} (g : X ⟶ X') :
    toSingleMk (f ≫ g) h =
      (toSingleMk f h).comp (.ofHom ((singleFunctor C q).map g)) (add_zero n) := by
  apply (toSingleEquiv h).injective
  simp [toSingleEquiv, singleFunctor, singleFunctors, HomologicalComplex.single_map_f_self]

set_option backward.isDefEq.respectTransparency false in
lemma toSingleMk_precomp
    {p q : ℤ} (f : K.X p ⟶ X) {n : ℤ} (h : p + n = q)
    {L : CochainComplex C ℤ} (g : L ⟶ K) :
    toSingleMk (g.f p ≫ f) h =
      (Cochain.ofHom g).comp (toSingleMk f h) (zero_add n) :=
  (toSingleEquiv h).injective (by simp [toSingleEquiv, singleFunctor, singleFunctors])

```

## Candidate views (anonymized)

### View A
  1. CochainComplex.HomComplex.Cochain.toSingleMk_postcomp

### View B
  - CochainComplex.HomComplex.Cocycle.toSingleMk_coe
  - CochainComplex.HomComplex.Cochain.toSingleMk_postcomp
      . CochainComplex.HomComplex.Cochain.toSingleMk_v
      . CochainComplex.HomComplex.Cochain.comp_zero_cochain_v
      . CochainComplex.HomComplex.Cochain.ofHom_v
      . HomologicalComplex.single_map_f_self
  - CochainComplex.HomComplex.Cocycle.postcomp_coe
  - CochainComplex.HomComplex.Cocycle.ext
  - AddEquiv.injective
  - CochainComplex.HomComplex.Cocycle.toSingleMk_postcomp._proof_1

### View C
  1. CochainComplex.HomComplex.Cocycle.ext
  2. CochainComplex.HomComplex.Cocycle.toSingleMk_coe
  3. congrArg
  4. congr
  5. of_eq_true
  6. add_zero
  7. congrFun'
  8. CochainComplex.HomComplex.Cocycle.postcomp_coe
  9. eq_self
  10. CochainComplex.HomComplex.Cocycle.toSingleMk_postcomp._proof_1

### View D
  - AddEquiv.injective
  - CochainComplex.HomComplex.Cochain.toSingleMk_postcomp
  - CochainComplex.HomComplex.Cocycle.ext
  - CochainComplex.HomComplex.Cocycle.homOf._proof_1
  - CochainComplex.HomComplex.Cocycle.postcomp_coe
  - CochainComplex.HomComplex.Cocycle.toSingleMk_coe
  - CochainComplex.HomComplex.Cocycle.toSingleMk_postcomp._proof_1
  - Eq.trans
  - add_zero
  - congr
  - congrArg
  - congrFun'
  - eq_self
  - of_eq_true

### View E
  1. CochainComplex.HomComplex.Cocycle.toSingleMk_coe
  2. CochainComplex.HomComplex.Cochain.toSingleMk_postcomp
  3. CochainComplex.HomComplex.Cocycle.postcomp_coe
  4. CochainComplex.HomComplex.Cocycle.ext
  5. AddEquiv.injective
  6. CochainComplex.HomComplex.Cocycle.toSingleMk_postcomp._proof_1
  7. CochainComplex.HomComplex.Cocycle.homOf._proof_1
  8. of_eq_true
  9. eq_self
  10. add_zero