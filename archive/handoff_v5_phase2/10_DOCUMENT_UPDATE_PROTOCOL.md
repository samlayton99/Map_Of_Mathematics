# Document Update Protocol

## 1. Do not erase history

Keep Gates 0–1 reports unchanged.

Do not delete earlier v4 documents if they are already in a repository. Mark them as historical design proposals rather than current authority.

## 2. Current direction

Create `docs/CURRENT_RESEARCH_DIRECTION.md` stating:

- the exact core is preserved;
- no final MathMap ontology has been selected;
- Phase 2 compares candidate projections;
- use-event extraction is a feasibility study;
- model training follows only after representation selection.

## 3. ADR

Create an ADR titled approximately:

`ADR-0002-characterize-before-committing-to-map-ontology.md`

It should explain why the project moved from “implement the declaration-centered map” to “compare candidate representations.”

## 4. Language discipline

Replace claims such as:

- “the primary map is...”
- “the correct object is...”
- “the theorem has three faces...”

with:

- “candidate projection...”
- “working hypothesis...”
- “one useful decomposition to test...”

unless evidence from the current study supports stronger wording.

## 5. No forced consistency

Documentation should be consistent about evidence and current assignment, but it should not suppress unresolved competing representations.
