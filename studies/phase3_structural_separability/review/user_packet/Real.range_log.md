# Review packet — `Real.range_log`

*domain file:* Analysis_SpecialFunctions_Log_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
@[simp]
theorem range_log : range log = univ
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V8:** `Function.Surjective.range_eq`, `Real`, `Real.log`, `Real.log_surjective`
**V6:** `Real`, `Function.Surjective.range_eq`, `Real.log`, `Real.log_surjective`
**V1:** `Real.log`, `Real.log_surjective`, `Function.Surjective.range_eq`, `Real`
**V4:** `Function.Surjective.range_eq`, `Real`, `Real.log`, `Real.log_surjective`
**V3:** `Function.Surjective.range_eq`, `Real`, `Real.log`, `Real.log_surjective`
**V2:** `Real`, `Function.Surjective.range_eq`, `Real.log`, `Real.log_surjective`
**V5:** `Real`, `Function.Surjective.range_eq`, `Real.log`, `Real.log_surjective`
**V7:** `Function.Surjective.range_eq`, `Real`, `Real.log`, `Real.log_surjective`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
@[simp]
theorem range_log : range log = univ :=
  log_surjective.range_eq

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
