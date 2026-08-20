# Proof 21

Theorem `Module.Projective.of_split` (Mathlib source below).

```lean
theorem of_split (f : P →ₐ[R] A) (g : A →ₐ[R] P ⧸ RingHom.ker f.toRingHom ^ 2)
    (h : f.kerSquareLift.comp g = AlgHom.id R A) :
    FormallySmooth R A := by
  refine (iff_split_surjection f fun x ↦ ?_).mpr ⟨g, h⟩
  obtain ⟨y, hy⟩ := Ideal.Quotient.mk_surjective (g x)
  exact ⟨y, congr(f.kerSquareLift $hy).trans congr($h x)⟩

set_option backward.isDefEq.respectTransparency false in
theorem of_comp_surjective
    (H : ∀ ⦃B : Type max u v⦄ [CommRing B] [Algebra R B] (I : Ideal B) (_ : I ^ 2 = ⊥),
        Function.Surjective ((Ideal.Quotient.mkₐ R I).comp : (A →ₐ[R] B) → A →ₐ[R] B ⧸ I)) :
    FormallySmooth R A := by
  let P := Generators.self R A
  let f := IsScalarTower.toAlgHom R P.Ring A
  rw [iff_split_surjection f P.algebraMap_surjective]
  have surj : Function.Surjective f.kerSquareLift :=
    Ideal.Quotient.lift_surjective_of_surjective _ _ P.algebraMap_surjective
  have sqz : RingHom.ker f.kerSquareLift.toRingHom ^ 2 = ⊥ := by
    rw [AlgHom.ker_kerSquareLift, Ideal.cotangentIdeal_square]
  dsimp only [AlgHom.toRingHom_eq_coe, RingHom.ker_coe_toRingHom] at sqz
  obtain ⟨g, hg⟩ := H _ sqz (Ideal.quotientKerAlgEquivOfSurjective surj).symm.toAlgHom
  refine ⟨g, AlgHom.ext fun x ↦ congr(f.kerSquareLift.kerLift ($hg x)).trans ?_⟩
  obtain ⟨x, rfl⟩ := (Ideal.quotientKerAlgEquivOfSurjective surj).surjective x
  obtain ⟨x, rfl⟩ := Ideal.Quotient.mk_surjective x
  simp only [AlgHom.toRingHom_eq_coe, AlgEquiv.coe_toAlgHom, AlgEquiv.symm_apply_apply,
    AlgHom.coe_id, id_eq]
  simp only [Ideal.quotientKerAlgEquivOfSurjective_apply]

```

## Candidate views (anonymized)

### View A
  (none)

### View B
  - Module.projective_lifting_property
  - Finsupp.linearCombination_single
  - LinearMap.comp_apply
  - LinearMap.id_apply
  - one_smul
  - of_eq_true

### View C
  - Eq.symm
  - Eq.trans
  - Exists.casesOn
  - Finsupp.linearCombination_single
  - LinearMap.comp_apply
  - LinearMap.id_apply
  - Module.projective_lifting_property
  - congrArg
  - congrFun'
  - eq_self
  - of_eq_true
  - one_smul

### View D
  1. Module.projective_lifting_property
  2. Finsupp.linearCombination_single
  3. LinearMap.comp_apply
  4. LinearMap.id_apply
  5. one_smul
  6. of_eq_true
  7. eq_self
  8. Exists.casesOn
  9. congrArg
  10. congrFun'

### View E
  1. Exists.casesOn
  2. LinearMap.id_apply
  3. LinearMap.comp_apply
  4. Module.projective_lifting_property
  5. congrArg
  6. Finsupp.linearCombination_single
  7. one_smul
  8. of_eq_true
  9. congrFun'
  10. eq_self