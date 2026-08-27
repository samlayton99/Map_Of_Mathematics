# Brief 3 — Defense Rebuttal

*The measurements cited as new in this brief were run during the trial, before
it was written. Code and data are in the package. Reproduced verbatim.*

---

I concede five charges outright, three of them serious, and I fixed or measured each before writing this.

**1. THE RECALL HARNESS WAS CIRCULAR.** You are right, and it is the worst defect you found. `phase4_provenance_recall.py:113-122` filters the answer key by the predicate under test, so `not-prop-flag = 0` was arithmetically forced. "The filters lose zero human-written citations" was not a measurement and I withdraw it.

I rebuilt the harness with an unfiltered answer key (`src/recall_loss_split.py`, committed) and ran it. Against every elaborator-resolved source identifier, mean recall is 0.317, median 0.25 — not 0.86. That is the honest number for that answer key.

But the loss taxonomy decides what it means. Of 146 losses: 51 are the theorem's OWN STATEMENT VOCABULARY (`Set`, `Iff`, `Nat`, `Finset.prod`, `Norm.norm` — the elaborator resolves every identifier the human typed, statement included, and these are not moves by anyone's definition); 60 are background slots, overwhelmingly the same statement vocabulary in implicit positions; 24 are elaboration-erased before any term exists; 8 are constructors (`And.intro`, `Exists.intro`) assembling a pair. The claims filter's irreducible cost — real moves it cannot express — is THREE of 146, and all three are the same class: "unfold this definition" (`ProbabilityTheory.iIndepSets`, `Ideal.radical`, `Int.fract` entering through the proof, not the statement).

So: your methodological charge lands completely, and the corrected measurement bounds the damage at ~2% of losses, in exactly the class ADR-0004 and HONEST_ASSESSMENT already document. Your "18.4% survival = four in five citations deleted" is arithmetically right and rhetorically wrong: the deleted majority is statement vocabulary and implicit-position noise, not moves. What you have not shown, and what I now cannot rule out, is the rate of that 3-per-146 class at scale. n=39.

**2. THE EMPTY BUCKET IS A FAILURE REPORTED AS AN OUTPUT.** Conceded without qualification. 239 theorems produce nothing, `live = a[a>0]` drops them from the denominator, and ACCOUNTING_STATUS folded them into "519 verdicts". A verdict requires items to demote; "we found nothing" is a different event and needs its own name and its own number. That is a reporting error I made, not a subtlety.

**3. SPEC/CODE DIVERGENCE ON ATTRIBUTION.** Conceded and verified: `make_attr` in the certified round-9 script has cycle detection but no hop cap; METHOD.md claims "up to 3 hops"; `parent_labels.py` enforces 3. Three artifacts, two behaviours, one document describing neither. Being cycle-safe means it terminates, not that it matches the spec.

**4. THE GRADER MOVED WITH THE TREATMENT.** Conceded as practice. The extension was declared in the file before the run, but shipping an instrument change alongside a treatment in the same round is exactly the error the certification discipline exists to prevent. The honest headline is the STANDING metric: V8 94.80 vs V6 94.38, +0.42 points, eight theorems. I will report that number.

**5. NAME-BASED SAMPLING POPULATION.** Conceded. `~has_class` derives from `Study.lean`'s name-based classifier and excludes 46% of theorems from every sample ever certified. "Nothing reads a name" is true of the ranking rules and false of the certification, and I stated it without that qualification.

## NOW WHAT I CONTEST.

**6. THE POLY CLAIM IS WRONG ON THE MERITS.** You wrote that grind's `Poly` falling below the threshold "causes 23% of the failures the measure exists to prevent", citing three residuals. I checked all three in `round9.log`: `Int.Internal.Linear.dvd_solve_combine`, `Lean.Grind.CommRing.Poly.denote_cancelVar`, `Lean.Grind.Linarith.eq_coeff` — every one carries `root_in_tactic_ns: True`. These are theorems inside a tactic's own development, where citing that tactic's denotation lemmas is the CORRECT answer, and the goal-relevance clause spares them deliberately. They are not failures. The concession you called load-bearing carries nothing.

**7. YOU MEASURED SET IDENTITY; I MEASURED OUTPUT.** Your Jaccard numbers are real, and irrelevant to the claim that matters. I swept both constants (`apparatus_sensitivity.py`, committed): ratio 10x-50x crossed with floor 50-500, fifteen configurations, apparatus set ranging 53 to 216 concepts — a 4x swing. Top-1 moves 0.9339 to 0.9333. Tactic blames: 20 in every single configuration. Verdicts: 245 in every configuration. The thresholds are not load-bearing because the concepts that do the work sit at ratios of 100-2400x. A tuned point that produces identical output across a 4x perturbation of its own output set is not tuned in any sense that threatens longevity.

*[Defense note added post-trial: this claim was subsequently RETRACTED by the
defense itself. See EVIDENCE.md item E7 — the invariance is sample-specific,
and on the certified seed one residual is decided by the 200 floor.]*

Your refactor simulation I accept, and read the opposite way: at K=500 statements about an internal type, zero survive as apparatus — correctly, because a type the community has written 500 theorems about has become mathematics and should stop being demoted. The measure retiring a concept once people talk about it is the design working.

**8. ON OCCAM, WE AGREE ON THE FACTS AND DIFFER ON THE INFERENCE.** My own ablation (dev seed, committed): stripped baselines 0.73-0.77, full system 0.9344. Logic-only demotion +10.8, position +4.8, claims +3.1, depth +2.9, attribution +2.3, statement-world +0.6, zoom +0.6, apparatus +0.4. Yours on the certified seed agrees directionally. So the complexity is not decorative — the gap over the simplest defensible rule is 16-20 points, and five of eight components each buy multiple points. But your trajectory argument is correct and I will not fight it: +2.56 then +0.42 is diminishing return, and the right conclusion is that V8 is the LAST component worth adding under this primitive. There should be no V9 of this kind. I also concede zoom's cost, which nobody had measured until today: it buys +0.56 top-1 while raising tactic junk from 12 to 20.

**9. ON QUESTION TWO I DO NOT CONTEST YOU.** You quoted my own HONEST_ASSESSMENT: declaration ranking hits a structural ceiling; local hypotheses, witnesses, case structure and representation changes cannot be expressed by any list of cited declarations. That is true, it is documented, and it means a ranked list per proof is a necessary substrate for the map and not sufficient for it. The map needs typed edges and cross-proof identity, and this architecture produces neither. Where we differ: a substrate that is wrong 5% of the time at rank 1 is still the thing the edge layer must be built on, and none of the nine rounds is wasted for that purpose. But I will not claim this architecture reaches the map.

**10. ON KEYNESS.** Conceded: the ranked view is 37.7% exact / 71.0% near; zoom is 56.5 / 92.8; both measured on V5v, two versions old. Zoom is a shipped step, so quoting it for the display is legitimate; quoting it as the ranking's semantic score is not, and my opening did that.

**DEFENSE POSITION:** question one, yes, conditional on the four fixes above and on stopping the accretion. Question two, no — not sufficient, by my own documentation.
