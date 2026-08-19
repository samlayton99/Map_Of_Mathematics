# Honest Assessment — Phase 2A/2B (required by handoff/00 §14)

Date: 2026-08-18. Every answer is labeled per the evidence language of `handoff/02` §E.

**1. Which projections are exact?** P0 (record expression graph) and P1 (reference occurrences with paths) are lean-exact. States and transitions backing P5 are lean-exact/observed. [reproduced evidence]

**2. Which are deterministic views?** P2 (support), P3 (classifications), P4 (application occurrences), P4-route (filtered P4), P6 (one-level expansion) — all recomputable from the record; two clean runs are byte-identical. [reproduced evidence]

**3. Which require semantic judgment?** Any claim that a view is a *good proof hint or explanation* (P3 residue, P4-route readability); conceptual step boundaries; P7 entirely. None were treated as formal truth. [design judgment]

**4. Does raw support look like meaningful mathematics or machinery?** Both, in domain-dependent proportion: median infrastructure fraction of body support is 29% in logic but 60–71% in algebra/order/analysis. Raw P2 alone is a poor human-facing view in algebraic domains. [deterministic projection]

**5. Does filtering help without hiding important structure?** The eight reversible classifiers cleanly separate machinery, and on inspected showcases the domain residue reads as the proof's toolset. Every exclusion carries a reason and the raw set persists. Whether the residue is *sufficient* for a human is unresolved pending review. [implementation result + open question]

**6. Does multiplicity/order/nesting matter?** P4-route retains order/nesting/relation labels and on inspection this is what makes it read as a route rather than a bag of names; P2 discards exactly that. Human confirmation pending. [engineer judgment]

**7. Can named application routes be recovered beyond toy proofs?** Yes: the P4 walker completed on all 1,233 showcase candidates including 10k+-node Mathlib proofs, with inferred result types (`resultOk` true for the overwhelming majority of spines) and zero walker failures. [implementation result]

**8. How much explicit use-event coverage exists?** 82.5% of tactic-proof theorems have ≥1 attributed event; 27.1% of all theorems (term proofs produce none by definition). 72.2% of family events attribute a name. [deterministic projection]

**9. How accurately can theorem instantiation be recovered?** Head + argument/universe counts: precisely (32/32 manual sample). Full σ as exact argument expressions was recorded only as counts in events; complete instantiations live in P4 occurrences. Two systematic partial-precision classes (case-constructor attribution; cast machinery). [implementation result]

**10. What appears irretrievably lost after elaboration?** Author's conceptual grouping and narrative step boundaries; attribution inside closed automation (`omega`, `decide`, un-listed `simp` sets — the simp *trace* is not preserved in the term); rewrite-rule TermInfo inside structure-literal proofs (recoverable with more InfoTree work — classified, not fundamental). [reproduced evidence for the third; design judgment for the first]

**11. Which candidate views work across proof styles?** P2/P3/P4/P4-route: all styles including term proofs. P5: tactic proofs only. The natural pairing is P4-route (universal, skeleton) + P5 (tactic proofs, roles and states) + P3 (filtering layer) — a hybrid, as `handoff/01` anticipated. [deterministic projection + design judgment]

**12. Which proposed schema entities turned out unnecessary?** All of the deferred list (`handoff/07` §4) stayed unnecessary — no statement families, no permanent route objects, no AND–OR schema, no map regions. Everything Phase 2 produced is a computed view plus one flat event array. The only new persistent thing is the study JSON container itself. [implementation result]

**13. Does selective expansion appear informative or merely verbose?** Undetermined by automation. P6 data (direct deps of direct deps with classifications) is produced in every review artifact; whether it helps is precisely a reviewer question. Raw P4 without filtering is decisively *verbose*. [open question]

**14. Where would the natural-language harness add indispensable information?** (a) conceptual grouping of P4-route steps into human steps; (b) naming what automation did (`positivity`-closed goals); (c) motivation/prerequisites. The formal layer bottoms out exactly where those begin. [design judgment]

**15. Is there enough evidence to select a primary map representation?** Quantitatively, a front-runner exists: the P3-filtered support + P4-route skeleton + P5 events hybrid — recoverable, deterministic, style-covering, compressive, provenance-complete. But the decision rules require human review before "more useful than raw dependency output" may be claimed, and none was performed. **Not yet — one bounded human-review step short.** [decision per pre-registered rules]
