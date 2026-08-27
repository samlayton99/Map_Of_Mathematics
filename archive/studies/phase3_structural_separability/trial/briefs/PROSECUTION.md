# Prosecution Brief — Against Acceptance of the Kernel-Invariant Move Formulation

All file paths are relative to `/Users/sam/my-repos/research/Map_Of_Mathematics/studies/phase3_structural_separability/` unless absolute. The extractor is `/Users/sam/my-repos/research/Map_Of_Mathematics/mathrecord/Mathrecord/DepDump.lean`. Every number cited below was read from the named file.

## 1. Summary of charges

1. **The system on trial was never measured.** The headline precision (90.3%) belongs to V4 *without* container semantics; the headline recall (~0.99) is a *projection* for a variant with container semantics whose precision was never re-measured. The two flagship numbers describe two different systems.
2. **The yardstick is circular and contaminated.** "Precision" is scored against a category function built from the very name patterns and namespace prefixes the model is forbidden to use; the program's own data shows ~12.7% of "content" labels are junk; the defense's "±3–4 points by hand audit" figure appears nowhere in the record.
3. **Recall is structurally incapable of detecting extraction misses.** Ground truth is intersected with the model's own dependency extraction before scoring; recall has a built-in ceiling and a heavy selection bias (130 of 600 sampled proofs).
4. **"Kernel purity" is asserted, not implemented.** The claims filter is a declaration-kind proxy, binder roles are read from a syntactic Pi prefix with a keep-on-failure default, the root chain is a wrong-for-eliminators heuristic, five magic constants govern the pipeline, and the strategy channel hardcodes literal lemma names.
5. **The longevity argument is refuted by the program's own data** ("no one states theorems about a solver's internals" — 412 statements mention `Lean.Grind.CommRing.Expr`), and the outputs — as opposed to the rules — are demonstrably version-unstable. No cross-version experiment exists.
6. **The headline metric answers the wrong question.** "Rank-1 is any content" is not "rank-1 is the key move"; on the only key-identification benchmark the ranking scores 0.225 — statistically adjacent to the PageRank (0.20) the graveyard executes for scoring 0.2.
7. **The "shrinking shallow floor" is evidence-free**, and depth-purification conflates depth with time and domain.
8. **The strategy channel is not shippable.** Induction precision 0.297 (11 true positives), case-split recall 0.205, extensionality recall 0.127; four of seven strategies at zero; validation cells as small as tp=2.
9. **The alien/imported conflation defeats the stated navigation goal** at exactly the point where navigation matters most.
10. **One seed, one sample, five design iterations.** Every improvement was tuned and certified on the same 2,355 theorems (seed 20260819); there is no held-out set, and the 862 MB dump underlying everything lives in an ephemeral session scratchpad.

## 2. Charges in detail

### Charge 1 — The certified system is not the system on trial

The formulation on trial (defense §1, item 3) includes container semantics: single-use constants "opened for ranking, label retained for membership." But:

- The measured precision — 90.3% top-1, 94.2% top-2 (`data/moves_results.json` `V4`) — was produced by `hb_thm_expand` in `src/moves.py` (lines 168–177), which *discards* single-use labels entirely (plain inlining). No precision run exists for the pipeline that keeps them.
- The measured recall is **0.925 mean** (`B_source_recall`, n=130). The advertised "~0.99" (`reports/MOVES_REPORT.md` §B: "projected recall ≈ 0.99") is arithmetic on a forensic reading of **30 of 35** losses (`loss_examples` is truncated at 30 in `src/moves.py` line 334; the remaining 5 losses were never examined). Container semantics was adopted *after* seeing these losses and never re-run end to end.

So the defense's opening claims — "90.3%" and "~97–99%" — are precision of system A and projected recall of system B. Neither number certifies the formulation as defined. Retaining container labels changes list composition (nested "via X" members re-enter the displayed set); the effect on precision is unknown, and the burden of measuring it was never met.

### Charge 2 — Circular, contaminated evaluation labels; unsourced uncertainty claim

The precision criterion is `category()` (`src/moves.py` lines 144–166; duplicated in `src/relevance.py` lines 129–151). It classifies by:

- name-substring patterns `GEN_MARKS = (".match_", "._simp", "._proof_", ...)` (line 32–34),
- namespace prefixes `TACTIC_NS = ("Lean.", "Mathlib.Tactic.", "Aesop.", ...)` (line 31),
- `_private.` prefixes and P3 classes.

These are precisely the "name/namespace cuts" the formulation forbids for itself (defense §1: "No names, no namespaces") and which graveyard item 7 rejects as "the paradigm of what the longevity constraint forbids." The model is certified name-free *by a name-based judge*. If name heuristics are too unreliable to be in the model, they are too unreliable to be the sole yardstick of a 90.3% claim; if they are reliable enough to be the yardstick, graveyard item 7 loses its force.

Moreover, "content" is a *residual* category — anything that escaped the junk regexes (line 163–165: any theorem/def/opaque not otherwise flagged). The defense translates "top-1 content" as "rank-1 is a **genuine named lemma**: 90.3%" (defense §2). The measured statement is weaker: rank-1 was not caught by the junk regexes.

Documented contamination is not hypothetical. `data/relevance_results.json` `verdict_x_category`: of 13,385 "content"-labeled candidates in V5 lists, **1,694 (12.7%) land in bookkeeping** and, per the program's own reading, "are `of_eq_true`/`eq_self`-style logic that the P3 labels miscount as content" (`reports/GRADIENT_RELEVANCE_REPORT.md` §2); another 798 land alien. `reports/MOVES_REPORT.md` §D concedes these leftovers "count as 'content' in the metrics." Contamination in the positive class inflates top-1 precision whenever such an item tops a shallow list.

Finally, the defense asserts the labels are good to "±3–4 points by hand audit" (defense §5.3). A grep of `reports/` finds no such audit. The only manual work on record is a reading of ~50 *broken* exemplars and 20 ground-truth proofs (`reports/FORENSICS_REPORT.md` Stage B) — an error-analysis of failures, not a calibration of the label set. The ±3–4 figure is unsourced in the record before this court.

### Charge 3 — Recall cannot fall below a structural ceiling

`src/moves.py` section B (lines 289–334) constructs ground truth as follows:

1. `refs = set(deps_v[r])` — **only constants already in the model's own extracted proof-term dependencies** are eligible (line 307);
2. tokens from the source body are matched against those refs (lines 310–315);
3. the ref must pass `category(c) in ("content", "glue")` — the name-based judge again filters the ground truth (line 316);
4. proofs with fewer than 2 resolved citations are discarded (line 317).

Consequence: **any lemma the human wrote that the extraction missed entirely — a `simp [foo]` that leaves only a `._simp` variant in the term, a rewrite compiled away, a lemma folded by the elaborator — can never enter the ground truth.** Recall as computed measures only the *filters* (theorem-kind + inlining) relative to `deps_v`; it is blind to losses at the `deps_v`/`hb` extraction layer itself. It is structurally incapable of detecting the class of miss that would most damage the formulation. The answer to the court's question is yes: recall has a built-in ceiling.

Selection bias compounds this: 600 proofs sampled, **130 evaluated** (78% discarded) — surviving proofs are those whose sources explicitly name ≥2 resolvable lemmas, i.e., term-style/explicit proofs. Heavy-automation proofs (`simp`, `omega`, `aesop` one-liners) — exactly where the model's junk problem lives — are systematically excluded from the recall sample.

A further defect: line 305–306, when a proof has ` by` but no `:=`, sets `body = block` — the **statement text is included in the token pool**, so lemma names appearing in the statement can be counted as proof "citations," contaminating gt in the model's favor (statement-adjacent refs are the easiest to recover).

The C2 "consistency with prior best" (median 100% coverage) is similarly soft: the route set is filtered by `app_head_count > 0 and prop_result_frac > 0.5 and not p3_classified` (lines 342–344) — application-head, Prop-valued, unclassified: the model's own three defining filters, applied to the reference. Partial self-agreement is being reported as external validation.

### Charge 4 — "Every primitive is a kernel fact" is false of the implementation

The defense claims (§1): "Every primitive is a fact of the kernel calculus… No names." The code says otherwise:

1. **Prop-valued is not implemented.** The claims filter is `kinds[c] == "theorem"` (`src/moves.py` line 177). `reports/INVARIANT_RANK_REPORT.md` itself flags this: "kind=theorem proxy; final form should check `type : Prop` directly." Which kind a constant receives is the *author's keyword choice* in the elaboration layer; Prop-valued `def`s are silently dropped from candidates *and* from recall ground truth (line 308). The shipped model does not implement its own stated definition.
2. **Binder roles come from a syntactic Pi prefix only.** `sigBinders` (`DepDump.lean` lines 27–39) collects `.forallE` binders syntactically and stops at the first non-Pi head. Any signature hidden behind a definition or abbreviation yields roles `none`, which the walker treats as load-bearing (`DepDump.lean` line 67: "beyond syntactic signature: conservative"). Worse, when the applied head is not a constant — an applied lambda or a local hypothesis, ubiquitous in proof terms — *all* arguments inherit the current load flag (lines 69–72). The frequency of these fallbacks is unmeasured; no experiment quantifies how often the "position rule" silently degrades to position-blind.
3. **The root chain is a heuristic that is wrong for the very constructs it claims to serve.** `rootChain` (lines 89–122) descends into "the LAST explicit argument (the continuation position of eliminators, byContradiction, fix)." For `Nat.rec` and `WellFounded.fix` the last explicit argument is the **major premise/element**, not the continuation. This plausibly explains the measured recall collapse of root-grain detection (case-split 0.205, extensionality 0.127 — `data/strategies2_results.json`).
4. **Magic constants everywhere:** inlining capped at 4 rounds (`src/moves.py` line 171), root chain ≤5 layers (`DepDump.lean` line 96), chain splice 2 rounds truncated at 16 entries (`src/strategies2.py` lines 146–155), wrapper closure 2 rounds (line 126), θ = 2% (`src/relevance.py` line 33). None of these is a kernel fact; each is a tuned knob.
5. **The strategy channel hardcodes literal library names.** `CORE` in `src/strategies2.py` (lines 36–46) lists `"absurd"`, `"Not.elim"`, `"mt"`, `"not_imp_not"`, `"Not.imp"`, `"funext"`, `"Exists.choose"`, `"of_decide_eq_true"` — ordinary named lemmas, several of them Mathlib-renameable. A formulation advertised as "nothing names a tactic, a namespace, or a convention" (`reports/MOVES_REPORT.md` Verdict) ships a name list at its heart.
6. **"Cited exactly once" is implemented as `indeg_v[c] <= 1`** (`src/moves.py` line 172) — which includes cited *zero* times. Trivial, but symptomatic: even the container definition does not match its prose.

The honest statement is: the formulation is kernel-*flavored*, with syntactic approximations, unmeasured fallback rates, tuned constants, and one name-based subsystem. That is a different thing from what the defense asks the court to accept.

### Charge 5 — The longevity argument is contradicted by the defendant's own data, and confuses rule-stability with output-stability

Defense §3: "Any future automation's certificate vocabulary structurally cannot enter mathematical statements (no one states theorems about a solver's internal data structures)."

The record says the opposite. `data/invariant_rank_results.json` `R3_anchor_t_indeg`: **`Lean.Grind.CommRing.Expr` is mentioned in 412 statement types — more than `Nat.gcd` (345)**. `reports/INVARIANT_RANK_REPORT.md` explains the R3 failure (AUC **0.40**, worse than chance) by exactly this: "large tactic libraries state hundreds of internal lemmas about their own types." The premise the defense offers as a structural law was already falsified inside this program; the patched version ("directional seclusion") is, in the defense's own words, "designed but unproven" (defense §4 item 8).

Second, the longevity argument defends the *rules*' statability, not the *outputs*' stability — and only outputs matter to a map user. Three of the model's load-bearing quantities are library-relative and will churn every release:

- **container status** flips when a second citation of a lemma lands (`indeg_v <= 1`);
- **universality** u(k) and the 149-concept stop-word set drift with library composition — and the set is already hypersensitive to θ within one snapshot: 261 → 149 → 47 concepts across θ ∈ {1%, 2%, 5%} (`data/relevance_results.json` `universality`). The report's claim of θ-stability ("stable under θ ∈ {1%, 5%}", `reports/GRADIENT_RELEVANCE_REPORT.md` §1) is supported only by the top-8 example list being identical; downstream verdicts were computed at θ=0.02 only;
- **depth** is a max-over-chain statistic ("max-brittleness," `reports/DEPTH_ADDENDUM.md`) that a single refactored import can move.

No experiment measures cross-version output churn. All data derive from one snapshot (Mathlib v4.33.0 lineage, `reports/DATA_AND_GRAPH_AUDIT.md`; one dump `mathlib_deps2.jsonl`). The defense concedes this is "the cheapest decisive experiment available" (§5.4) — the prosecution asks why the cheapest decisive experiment was not run before asking for acceptance.

### Charge 6 — The headline metric cannot distinguish a proof sketch from a list of true trivia; on the only keyness benchmark, the model matches an executed alternative

The metric: `fc = first rank whose category is "content"` (`src/moves.py` line 255); top-1 success = *any* non-junk theorem at rank 1. A list of true-but-trivial lemmas passes at 100%. The question Sam actually posed — "does the ranking put the most mathematically useful ideas on top every time" (`reports/FORENSICS_REPORT.md` header) — is answered nowhere at scale. The defense concedes keyness rests on ~50 hand-read proofs and 20 skeletons (§5.1), i.e., n≈20 for ordering quality, with the 20-proof route view partially self-defined (Charge 3).

Worse, the graveyard applies a double standard. PageRank is executed for "p@5 = 0.2 on proxy keys" (defense §4 item 2). The current ranking's own score on the same proxy keys is **0.225** (`reports/CONES_REPORT.md` §4: "Against the (rigged-against-us) proxy keys: 0.225 vs 0.20"). If proxy keys are valid, the model is a rounding error away from the corpse; if the proxies are "rigged" and invalid, graveyard item 2 must be struck and the field of alternatives reopens. The defense cannot have both.

### Charge 7 — "The shallow floor shrinks in relative weight" is an assumption wearing the costume of a result

Defense §5.2 and `reports/GRADIENT_RELEVANCE_REPORT.md` §Standing residue claim the shallow region (top-1 = 83.4%, `data/moves_results.json`) "shrinks in relative weight as the library deepens." No measurement supports this: no time-series, no cross-version data, no growth model. Mathlib growth adds shallow material continuously (elementary combinatorics, order theory, new algebraic hierarchies start shallow). Equally, "error decreases with depth ⇒ the measure purifies as the library grows" (defense §2) conflates depth-within-a-snapshot with time, and ignores the domain confound: deep terciles are dominated by analysis/measure-theory proofs with a particular citation style; nothing separates "depth purifies" from "analysis proofs are cleaner." The tercile boundaries themselves are sample quantiles (`src/moves.py` line 268), not absolute depths.

### Charge 8 — Shipping the strategy facets is indefensible on the shipped numbers

`data/strategies2_results.json`, validation n=1,427:

| facet | precision | recall | tp | fp | fn |
|---|---|---|---|---|---|
| induction | 0.297 | 0.458 | 11 | 26 | 13 |
| case_split | 0.465 | 0.205 | 33 | 38 | 128 |
| extensionality | 0.75 | 0.127 | 15 | 5 | 103 |
| contradiction | 0.091 | 0.333 | 2 | 20 | 4 |
| choice | 0.0 | 0.0 | 0 | 5 | 8 |
| contrapositive | 0.0 | 0.0 | 0 | 1 | 13 |
| computation | 0.0 | 0.0 | 0 | 0 | 4 |

The recommendation (`reports/STRATEGIES_REPORT.md`) is to "ship the three term-visible tags" — including an induction facet where **7 of 10 displayed tags would be false** and a case-split facet that misses 4 of 5 case splits. The cells are tiny (conclusions about contradiction rest on tp=2; about choice on 8 positives), the ground truth is a regex over tactic text that the report itself calls noisy (counting `obtain`/`match`/`split` as case analysis), and the report's escape hatch — "the numbers are lower bounds on signature quality" — is unfalsifiable as stated: noisy ground truth moves numbers in both directions, and no cleaner ground truth was constructed for even a 50-proof subsample. Four of seven strategies are conceded structurally unrecoverable at this grain. A facet channel where the best shipped detector is 75%-precise-at-13%-recall and the flagship (induction) is 30%-precise is not a shippable feature; it is a negative result being shipped.

### Charge 9 — The alien/imported conflation fails the navigation goal at its most important point

`reports/GRADIENT_RELEVANCE_REPORT.md` §Discovery concedes: the model cannot distinguish `Nat.dvd_factorial` in Euclid's proof (the creative move — "considering n!+1 *is* Euclid's creative move") from omega certificate residue, "because structurally they are the same event." The proposed remedy is a display label ("imported"). But for the stated goal — a mathematician navigating to *the idea worth reading the proof for* — this bins the single most valuable item in a proof together with the single least valuable, and delegates the separation to the human. The same report shows 1,096 tactic-library items landing *relevant* (`verdict_x_category`), defended as "kernel-invariantly they ARE mathematics." At some point, "the structural verdict is correct by definition" stops being a defense and becomes an admission that structure alone does not deliver the product the program set out to build.

### Charge 10 — One seed, one sample, five iterations: the numbers are development-set numbers

`SEED = 20260819` appears in `src/features.py`, `src/cones.py`, `src/invariant_rank.py`, `src/landmark.py`, `src/moves.py`, `src/relevance.py`, `src/strategies2.py`. The same 2,355-root sample (n_analyzed = 2355 in both `data/forensics_results.json` and `data/invariant_rank_results.json`; identical pool construction in `src/moves.py` line 191 and `src/relevance.py` line 164) was used to: diagnose V1's failures, design and certify R1, design and certify R2, motivate the position rule, certify V4, adopt container semantics from V4's loss forensics, and certify V5. Every design decision was made looking at the evaluation set, and the final numbers were computed on that same set. This is the textbook garden of forking paths; the honest expectation is that 90.3% is an *upper* estimate, and small reported deltas (V5's 90.45% vs V4's 90.25% — 0.2 points on ~1,950 live rows, well inside one binomial standard error of ~0.7 points) are noise being narrated.

Two reproducibility notes: (a) the defense's "all numbers are reproducible from the included data files and scripts" is weakened by the fact that every script reads its 862 MB dump from a **session-scoped scratchpad path** (`SCRATCH2 = /private/tmp/claude-501/...` in `src/moves.py` line 22) that is not in the repository; (b) the layer-coherence statistic of 1.0 is admitted to "cover few pairs by construction" (`reports/GRADIENT_RELEVANCE_REPORT.md` §Gradient) yet appears in the data file as a bare 1.0.

## 3. Rebuttal of the defense's strongest points

**"The formulation contains zero facts a Lean release could invalidate" (§3).** Three answers. First, false in implementation: kind=theorem is an elaboration-era artifact of author keyword choice; `CORE` name lists in `src/strategies2.py` are renameable lemmas; `sigBinders`' syntactic prefix breaks under signature refactors that hide Pis behind definitions. Second, the argument's centerpiece premise (statement/proof asymmetry for automation vocabulary) is refuted by the program's own R3 data (Charge 5). Third, even where the rules survive, the *outputs* churn (containers, universality, depth) — and a naming-convention system's rules are also eternally statable; statability was never the interesting property.

**"90.3% / 94.6% deep / ~97–99 recall" (§2).** The precision number is measured against a name-based, documented-contaminated judge, on the development sample, for a variant without container semantics; the recall number is a projection whose ground truth is intersected with the model's own extraction and drawn from a 22%-surviving, term-proof-biased subsample. Each number is real; none of them certifies what the defense says it certifies.

**The graveyard (§4).** It is genuinely impressive that eleven alternatives were executed and measured — the prosecution does not dispute the deaths of PageRank-as-importance, reuse-as-importance, or bag-of-constants strategies. But the graveyard proves *those* corpses, not the formulation's optimality: item 2 is killed by a metric on which the champion scores 0.225 (Charge 6); item 7 (name cuts) is rejected on principle while name cuts judge every headline number (Charge 2); and the nearest live alternatives — provenance extraction from the elaboration layer, and the model's own specified-but-unimplemented "final form" (true Prop check, real binder roles) — are in no grave (§4 below).

**The vibe exhibits (§2).** Six to sixteen hand-picked anchors (`ANCHORS`, `src/moves.py` lines 36–40), several of which (exp_add, gcd_comm, exists_infinite_primes) were used as working examples throughout development. Euclid-verbatim is charming and is exactly the kind of evidence (curated, textbook-famous, development-set) that a court should weight at approximately zero against 2,355-row statistics with a contaminated judge.

## 4. Alternatives the defense did not try (steelmanned)

**A. Elaboration-layer provenance extraction (InfoTree mining).** The recall evaluation already treats *the identifiers the human wrote in the tactic script* as gold (`src/moves.py` §B). If source citations are the gold standard, extract them directly: Lean 4's `InfoTree` API exposes, per elaborated tactic, the exact constants referenced with full resolution — no regex, no term-level reconstruction. This recovers by construction everything §B measures recall against (~1.0 on that metric), and it recovers the four intent-level strategies (`by_contra`, `contrapose`, `choose`, `decide`) that `reports/STRATEGIES_REPORT.md` proves are *structurally unrecoverable* at the kernel grain. The defense's longevity objection (the tactic layer churns) cuts less than claimed: InfoTrees are a stable public API used by every Lean editor, and — decisively — the defense's own strategy report already concedes the endgame is to extract intent "from the tactic layer... as provenance, labeled as such." A hybrid (kernel-invariant move set + provenance channel for names/strategies) was never implemented or measured, so the graveyard cannot claim it. The court should ask: if the program's own recall gold and its own strategy recommendation both point at the elaboration layer, why is the pure-kernel formulation the one on trial?

**B. The formulation's own "final form," never run.** `reports/INVARIANT_RANK_REPORT.md` specifies it: check `type : Prop` directly instead of kind=theorem; read binder roles under `whnf`/definitional unfolding instead of the syntactic Pi prefix. Both are strictly *more* kernel-faithful than the shipped proxies, both are cheap (one extractor pass), and neither was implemented. The defense cannot argue these were tried and found wanting — they are the defense's own stated correct versions of its two central primitives. Accepting the model now means accepting the proxy while the specified primitive sits untested; if the proxy and the primitive disagree materially, the certification transfers to neither.

**C. Threshold-free relevance via rarity weighting.** The shipped universality rule is a binary stop-word cut at θ=2% whose concept set swings 261→47 across the swept range (Charge 5). `reports/INVARIANT_RANK_REPORT.md` §3 already designs the continuous version — "rank moves by the rarity of their rarest subject concept" — an idf-style, threshold-free, library-relative measure with no arbitrary constant. Designed in-house, never tested; not in the graveyard.

**D. A pre-registered, held-out evaluation protocol** (methodological alternative): fresh seed, fresh 2,000-theorem sample untouched by any design iteration, human-labeled 200-theorem gold subset judged blind to model output, metrics fixed before running. This is not exotic; it is the difference between a development score and a result. It was available at every step and never used.

## 5. What would change the prosecution's mind

The prosecution is not asking for the model's destruction; it is asking that acceptance be withheld until the following falsifiable tests are run. Passing them would convert most charges into footnotes:

1. **Cross-version churn test.** Dump a second Mathlib version (anything ≥ v4.34). Measure: move-set Jaccard per theorem, rank-1 identity stability, container-status flip rate, universality-set drift. Acceptance bar: rank-1 stable on ≥95% of unchanged theorems. This single experiment tests defense §3 empirically; the defense itself calls it "the cheapest decisive experiment available."
2. **Fresh-seed, held-out precision.** Re-run `src/moves.py` section A with a new seed on theorems disjoint from the 2,355. If top-1 stays within 2 points of 90.3%, Charge 10 dies.
3. **Human-judged gold set.** 200 theorems, a human labels rank-1 as genuine-move / junk / trivial-but-true, blind to the model's category labels. If agreement with `category()` is ≥96% (the implied ±3–4), Charge 2's contamination argument dies and the defense's audit claim is retroactively vindicated.
4. **Extraction-independent recall.** Build ground truth from InfoTree-resolved tactic citations (not intersected with `deps_v`), on a sample including simp/omega-heavy proofs. If recall holds ≥0.9, Charge 3 dies.
5. **Measure the actual system.** One run of the full container-semantics pipeline (labels retained) reporting both precision and recall. If precision holds, Charge 1 dies.
6. **Keyness at scale.** For 100 proofs with ≥3 genuine moves, ask a blinded human which listed move is *the* key step; measure how often it is rank-1. Any result ≥70% would satisfy the prosecution that ordering means something; today the number does not exist.
7. **Quantify the syntactic fallbacks.** Instrument `loadBearingHeads` to count how often binder roles fall off the syntactic prefix or the head is a non-constant (role unknown → load-bearing). If <5% of role decisions are fallbacks, Charge 4.2 shrinks to a footnote.
8. **Strategy facets against clean ground truth.** Hand-label 100 proofs' strategies from the source. If induction precision stays ~0.3, unship the facet; if the regex was the problem and true precision is ≥0.7, ship it. Either way, the current numbers cannot support shipping.

## Closing

The program's discipline — executed graveyard, honest negative results (R3, strategies v1), documented residues — is the best thing about it, and the prosecution has relied on that honesty throughout: nearly every charge above is built from the defendant's own files. But honesty about weaknesses is not the same as having overcome them. What stands proven today is: a kernel-flavored pipeline with unimplemented core primitives, certified by a name-based judge on its own development sample, whose two headline numbers describe two different systems, whose longevity thesis is contradicted by its own measurements, and whose strategy channel fails its own validation. The correct verdict is not "wrong formulation" — it is **not proven**, with an eight-item experiment list, most of it cheap, standing between the model and legitimate acceptance.
