# Review packet — `pow_iterate`

*domain file:* Algebra_Group_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[to_additive, simp]
lemma pow_iterate (k : ℕ) : ∀ n : ℕ, (fun x : M ↦ x ^ k)^[n] = (· ^ k ^ n)
  | 0 => by ext; simp
  | n + 1 => by ext; simp [pow_iterate, Nat.pow_succ', pow_mul]

```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V5:** `Monoid`, `Nat`, `Nat.brecOn`, `Eq`, `Nat.iterate`, `HPow.hPow`, `instHPow`, `NPow.toPow`
**V6:** `Nat`, `HPow.hPow`, `instHPow`, `Monoid.toNPow`, `NPow.toPow`, `Eq`, `Monoid`, `Nat.brecOn`
**V4:** `pow_iterate._f`, `Eq`, `HPow.hPow`, `Monoid`, `Monoid.toNPow`, `NPow.toPow`, `Nat`, `Nat.brecOn`
**V3:** `Monoid`, `Nat`, `Eq`, `Nat.iterate`, `Nat.brecOn`, `HPow.hPow`, `instHPow`, `NPow.toPow`
**V2:** `Monoid`, `Nat`, `Nat.brecOn`, `Eq`, `pow_iterate._f`, `HPow.hPow`, `Nat.iterate`, `instHPow`
**V8:** `Nat`, `Monoid`, `HPow.hPow`, `instHPow`, `Eq`, `NPow.toPow`, `Monoid.toNPow`, `Nat.iterate`
**V7:** `Nat`, `Monoid`, `Eq`, `HPow.hPow`, `Nat.brecOn`, `Nat.iterate`, `instHPow`, `NPow.toPow`
**V1:** `Nat`, `Monoid`, `Eq`, `HPow.hPow`, `Nat.brecOn`, `Nat.iterate`, `instHPow`, `NPow.toPow`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[to_additive, simp]
lemma pow_iterate (k : ℕ) : ∀ n : ℕ, (fun x : M ↦ x ^ k)^[n] = (· ^ k ^ n)
  | 0 => by ext; simp
  | n + 1 => by ext; simp [pow_iterate, Nat.pow_succ', pow_mul]

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
