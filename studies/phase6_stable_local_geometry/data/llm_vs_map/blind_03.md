# Premise retrieval — batch 03

For each Lean 4 / Mathlib theorem below you are shown ONLY its statement.
The proof is not shown and you must not try to recall the file.

For each item, predict which Mathlib declarations the PROOF uses: name
the 10 declarations you judge most likely to be cited by the proof,
most likely first. Rules:

- Give fully-qualified Mathlib names exactly as they appear in the
  library (e.g. `Finset.sum_congr`, `Polynomial.degree_mul`).
- Predict the substantive mathematical lemmas/definitions the proof
  builds on, not tactic-level plumbing (`Eq.mpr`, `congrArg`, `rfl`,
  `id`) and not things already named in the statement itself.
- Exactly 10 names per item, no commentary, no duplicates.

Answer as JSON only:
{"q01": ["Name.one", "Name.two", ...], "q02": [...], ...}

---


## q21

```lean
theorem target_thm (X Y : C) [HasBinaryProduct X Y] :
    (pullbackZeroZeroIso X Y).hom ≫ prod.fst = pullback.fst 0 0
```

## q22

```lean
theorem target_thm : ¬Disjoint s t ↔ ∃ a, a ∈ s ∧ a ∈ t
```

## q23

```lean
instance (priority := 100) target_thm [NonAssocRing α]
    [Semiring β] [PartialOrder β] [MulRingNormClass F α β] : RingNormClass F α β
```

## q24

```lean
theorem target_thm : t⁻¹ = t
```

## q25

```lean
theorem target_thm {n : ℕ} {t : ℝ} (ht' : t ≤ n) : (1 - t / n) ^ n ≤ exp (-t)
```

## q26

```lean
theorem target_thm (P : Matrix n n 𝕜 → Prop) (M : Matrix n n 𝕜)
    (hdiag : ∀ D : n → 𝕜, det (diagonal D) = det M → P (diagonal D))
    (htransvec : ∀ t : TransvectionStruct n 𝕜, P t.toMatrix) (hmul : ∀ A B, P A → P B → P (A * B)) :
    P M
```

## q27

```lean
theorem target_thm (o : Ordinal) : invVeblen₂ (Γ_ o) = 0
```

## q28

```lean
theorem eq_one_of_sq_sub_mul_sq_eq_zero' {p : ℕ} [Fact p.Prime] {a : ℤ} (ha : (a : ZMod p) ≠ 0)
    {x y : ZMod p} (hx : x ≠ 0) (hxy : x ^ 2 - a * y ^ 2 = 0) : legendreSym p a = 1
```

## q29

```lean
theorem target_thm (Q : Subgroup G) (hQ : IsPGroup p Q) :
    Disjoint (transferSylow P hP).ker Q
```

## q30

```lean
lemma target_thm (m : M) : IsGroupLikeElem R (of A M m)
```
