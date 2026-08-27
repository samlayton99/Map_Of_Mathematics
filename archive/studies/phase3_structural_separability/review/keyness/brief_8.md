# Proof 8

Theorem `WfDvdMonoid.not_isUnit_iff_exists_factors_eq` (Mathlib source below).

```lean
theorem not_isUnit_iff_exists_factors_eq (a : α) (hn0 : a ≠ 0) :
    ¬IsUnit a ↔ ∃ f : Multiset α, (∀ b ∈ f, Irreducible b) ∧ f.prod = a ∧ f ≠ ∅ :=
  ⟨fun hnu => by
    obtain ⟨f, hi, u, rfl⟩ := exists_factors a hn0
    obtain ⟨b, h⟩ := Multiset.exists_mem_of_ne_zero fun h : f = 0 => hnu <| by simp [h]
    classical
      refine ⟨(f.erase b).cons (b * u), fun a ha => ?_, ?_, Multiset.cons_ne_zero⟩
      · obtain rfl | ha := Multiset.mem_cons.1 ha
        exacts [Associated.irreducible ⟨u, rfl⟩ (hi b h), hi a (Multiset.mem_of_mem_erase ha)]
      · rw [Multiset.prod_cons, mul_comm b, mul_assoc, Multiset.prod_erase h, mul_comm],
    fun ⟨_, hi, he, hne⟩ =>
    let ⟨b, h⟩ := Multiset.exists_mem_of_ne_zero hne
    not_isUnit_of_not_isUnit_dvd (hi b h).not_isUnit <| he ▸ Multiset.dvd_prod h⟩

```

## Candidate views (anonymized)

### View A
  - Associated.irreducible
  - Eq.symm
  - Eq.trans
  - Exists.casesOn
  - Iff.mp
  - Irreducible.not_isUnit
  - Multiset.cons_ne_zero
  - Multiset.dvd_prod
  - Multiset.exists_mem_of_ne_zero
  - Multiset.mem_cons
  - Multiset.mem_of_mem_erase
  - Multiset.prod_cons
  - Multiset.prod_erase
  - Or.casesOn

### View B
  1. mul_comm
  2. congrArg
  3. Multiset.dvd_prod
  4. Irreducible.not_isUnit
  5. Or.casesOn
  6. _private.Mathlib.RingTheory.UniqueFactorizationDomain.Defs.0.WfDvdMonoid.not_isUnit_iff_exists_factors_eq.match_1_3
  7. Eq.symm
  8. mul_assoc
  9. Multiset.prod_cons
  10. Multiset.prod_erase

### View C
  1. mul_comm
  2. Multiset.exists_mem_of_ne_zero
  3. rfl
  4. not_isUnit_of_not_isUnit_dvd
  5. mul_assoc
  6. WfDvdMonoid.exists_factors
  7. Multiset.prod_erase
  8. Multiset.prod_cons
  9. Multiset.mem_of_mem_erase
  10. Multiset.mem_cons

### View D
  - Multiset.mem_of_mem_erase
  - Multiset.prod_erase
  - Multiset.cons_ne_zero
  - Multiset.exists_mem_of_ne_zero
  - WfDvdMonoid.exists_factors
  - Multiset.dvd_prod

### View E
  1. Multiset.mem_of_mem_erase
  2. Multiset.prod_erase
  3. Multiset.cons_ne_zero
  4. Multiset.exists_mem_of_ne_zero
  5. WfDvdMonoid.exists_factors
  6. Multiset.dvd_prod
  7. _private.Mathlib.RingTheory.UniqueFactorizationDomain.Defs.0.WfDvdMonoid.not_isUnit_iff_exists_factors_eq.match_1_3
  8. _private.Mathlib.RingTheory.UniqueFactorizationDomain.Defs.0.WfDvdMonoid.not_isUnit_iff_exists_factors_eq.match_1_1
  9. Multiset.mem_cons
  10. not_isUnit_of_not_isUnit_dvd