# Phase 2B — Contextual Use-Event Feasibility

Date: 2026-08-18. Data: `studies/use_events.json` (from the same six-file corpus). Events are observed elaborator data; attribution is via resolved `TermInfo` expressions, never parsed display text.

## What was measured

760 deduplicated events from the explicit tactic families, each carrying: role, source span, exact before/after state ids (linked to the Gate-1 state store — 1,303 exact states), named-declaration attributions with arg/universe counts, and a completeness flag.

## Results

- **Attribution rate: 72.2%** (549/760 events name at least one declaration).
- **Coverage: 82.5% of tactic-proof theorems** (302/366) have ≥1 attributed event with exact before/after states. Over *all* showcase theorems coverage is 27.1% — term proofs (76% of the population) produce no tactic events by definition; their named structure lives in P4/P4-route instead. This split is the central coverage fact for any future navigation dataset.
- **By role** (events, attribution rate): rewrite 254, 100% · unfold 3, 100% · induction 6, 100% · apply 23, 96% · exact 112, 83% · simp 208, 57% · refine 100, 44% · cases 17, 47% · rw-with-no-named-rule 29, 0% · constructor 3, 0% · simp_all 5, 20%.
- **Multiplicity vs ambiguity:** 311 events attribute exactly one declaration; 238 attribute several — inspection shows these are *multiple sequential uses in one tactic* (`rw [a, b, c]`, explicit simp lists), not attribution uncertainty; 211 attribute none (classified `no-named-attribution`).

## Manual precision (stratified sample, n=32, engineer inspection)

All 32 sampled attributions point to declarations genuinely used at that step — including dot-notation and reversed-rewrite resolution (`e.injective.semilatticeInf` → `Function.Injective.semilatticeInf`, `← inf_le_sup.ge_iff_eq` → `LE.le.ge_iff_eq`), anonymous constructors (`⟨fun h ↦ ?_, ?_⟩` → `Iff.intro`), and `refine if h : _` → `dite`. **Zero fabricated names.** Two partial-precision classes, both systematic and classifiable:

1. `cases`/`induction` attribute the case-alternative *constructors* (`Nat.zero`, `Or.inl`) rather than the eliminating principle;
2. cast-normalizing steps attribute elaboration machinery (`exact_mod_cast …` → `cast`) rather than the mathematically salient nested lemma.

This is engineer verification of extraction precision, not a human-usefulness judgment.

## Failure modes (all classified, none silent)

- Rewriting with local hypotheses: correctly yields no named declaration (the "tool" is context, not library).
- Structure-literal `where`-proofs: rewrite-rule TermInfo is lost to a different elaboration branch (~29 events) — the one genuine attribution-coverage bug found; fixable by following delayed-assignment InfoTree branches.
- `simp`/`simp_all` without explicit lemma lists and closed automation (`omega`, `decide`, `positivity`): no honest single-declaration attribution exists; volume tallied per file in `nonFamilyTacticKinds`.
- Bare `constructor`: the applied constructor is not in the syntax or a TermInfo; recoverable from the proof term (P4) if wanted.

## Conclusion for the decision (per `handoff/05` §6)

A **high-precision, partial-coverage** event set is feasible today: precise named attribution with exact contexts for roughly 4 in 5 tactic-proof theorems, honest classification everywhere else. The measured gaps point to the already-anticipated mitigations: use P4/P4-route occurrences as the term-proof and automation fallback (weak labels), and treat heavy automation as explicitly unattributable rather than guessed. The rich use-event hypothesis (H4) survives this feasibility test; it is not yet evidence of learning value.
