# 06 — Metamorphic and Internal Validation

This is the most objective way to test whether MathMap follows mathematics rather than Lean compilation.

## 1. Alpha and binder changes

Transform:

- local variable names;
- binder order where definitionally equivalent;
- syntactic parenthesization.

Expected:

- exact syntax IDs may change as designed;
- structural local move view remains equivalent.

## 2. Explicit versus implicit instance

Produce equivalent proofs where an instance is:

- inferred;
- supplied explicitly.

Expected:

- infrastructure lane changes;
- high-level move lane does not.

## 3. Inline versus named intermediate fact

Replace:

- an inline subterm;
- with `have h := ...`.

Expected:

- exact local hierarchy changes by one named boundary;
- collapsed high-level route is equivalent;
- expansion exposes the new boundary.

## 4. Wrapper insertion/removal

Introduce a theorem or definition whose body forwards directly to an existing declaration.

Expected:

- exact graph records the wrapper;
- normal navigation groups/collapses it under the owner or marks it as a transparent boundary;
- no artificial long-distance landmark appears.

## 5. Tactic versus term proof

Construct semantically equivalent:

- tactic proof;
- term proof.

Expected:

- provenance/infrastructure differs;
- major named applications and constructions remain aligned where the mathematical route is the same.

## 6. `simpa` versus explicit rewrite

Expected:

- rewrite/provenance details differ;
- high-level relation is equivalent.

## 7. Fold versus unfold

Use a named definition versus its body.

Expected:

- concept and representation lanes reflect the change;
- map users can move between the two by expansion;
- no loss of exactness.

## 8. Constructor/witness variants

Present equivalent existential or structure constructions in different syntax.

Expected:

- witness/construction move is preserved.

## 9. Alternative proof route

Use genuinely different proofs of the same theorem.

Expected:

- routes remain different;
- theorem interface is shared;
- the system does not force false invariance.

## Metrics

For each pair report:

- high-level node/edge overlap;
- typed graph edit distance;
- owner-collapsed route equivalence;
- rank correlation of shared moves;
- artificial-jump difference;
- exact recoverability;
- relation-lane changes.

A good map is invariant only to harmless refactoring, not to genuine mathematical change.
