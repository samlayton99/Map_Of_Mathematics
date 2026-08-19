# Review packet — `Bool.involutive_not`

*domain file:* Logic_Function_Basic

## PART 1 — statement and candidate views (do NOT read Part 2 yet)

Theorem statement:

```lean
theorem _root_.Bool.involutive_not : Involutive not
```

Each view lists up to 8 declarations that the view considers the most important mathematical content of this proof. Rate each view 1–5 for: *would this list help a mathematically informed reader see how the theorem is proved?*

**V6:** `Bool.not_not`
**V8:** `Bool.not_not`
**V1:** `Bool.not_not`
**V5:** `Bool.not_not`
**V4:** `Bool.not_not`
**V3:** `Bool.not_not`
**V2:** `Bool.not_not`
**V7:** `Bool.not_not`

## PART 2 — source proof (read only after Part 1 ratings)

```lean
theorem _root_.Bool.involutive_not : Involutive not :=
  Bool.not_not

```

Now rate each view 1–5 for *certificate fidelity*: does it preserve the important moves of THIS proof? Note any key move (local hypothesis, witness, case split, representation change) that no view captures.
