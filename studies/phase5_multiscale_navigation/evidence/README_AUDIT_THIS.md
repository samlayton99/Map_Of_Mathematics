# Evidence Audit Package — check these claims against the receipts

The owner does not fully believe a set of claims I made and has asked for an
independent audit. Below is every claim, the exact receipt, and — where they
exist — the weaknesses in my own evidence. **Please attack this.** I would
rather be corrected than believed.

Everything derives from one extraction of Lean's Mathlib (dump v7, 771,129
declarations). All raw console logs are in `logs/`, the scripts that produced
them in `src/`, machine-readable results in `data/`.

The large arrays (18.7M-row incidence table, 230MB) are excluded; regenerate
with `src/build_incidence.py` then `src/build_v8_mask.py`.

---

## CLAIM 1 — "Mathematics is essentially one connected object; there is no undeveloped continent"

**Numbers claimed:** with every load-bearing citation admitted, 761,386 of
763,027 declarations (99.78%) lie in a single weak component. 569 components
total; 42.7% of them are size ≤ 2. The 1,641 declarations outside the giant
have median depth 5 and are 21.3% machine-generated.

**Receipt:** `logs/islands.log`, section A. Script: `src/island_forensics.py`,
which builds the graph from every incidence with `load_bearing = True` and
runs `scipy.sparse.csgraph.connected_components(directed=False)`.

**Supporting detail claimed:** the fragments outside the giant are Lean's own
infrastructure and typeclass plumbing rather than mathematics — `Lean.Parser`
(54 nodes, 100% single-namespace), `Lean.PrefixTreeNode`, `Lean.Lsp`, and
class-projection fragments such as `SubsemiringClass.toSubmonoidClass` (11
nodes, 90.9% machine-generated) and `NonUnitalRingHomClass.toAddMonoidHomClass`
(9 nodes, 88.9% machine-generated). Area breakdown printed in the same log.

**Weaknesses to attack:**
- "Load-bearing" is itself a filter (occurrence roles {applied, let-value,
  explicit-arg, unresolved}). I did NOT run this on the fully unfiltered graph
  P1. P1 has 2 components — even more connected — so the direction of the
  claim is safe, but the exact 569 is conditional on the role filter.
- Weak connectivity ignores edge direction. A "connected" mathematics under
  weak connectivity may still be unreachable in the direction that matters
  for navigation. I did not test strong connectivity or reachability.
- Namespaces are used to describe what the fragments are. That is a naming
  heuristic, fine for description, but it is not a kernel fact.

---

## CLAIM 2 — "The 25,230 islands under top-1 ranking are artifacts of keeping one edge per proof, not mathematical structure"

**Numbers claimed:** top-1 under the frozen V8 ranking touches 487,735
declarations with 462,505 edges and yields 25,230 components, largest holding
8.87%. Since a one-parent-per-node structure is a forest,
components = nodes − edges = 487,735 − 462,505 = 25,230 exactly.

**Receipt:** `logs/strat.log` sections B–E; `logs/geometry.log` (the
projection table); `data/stratified_purity.json`. The arithmetic identity is
checkable by hand from those three numbers.

**Weaknesses to attack:**
- The identity holds only if the top-1 graph is genuinely a forest. It is, if
  and only if every node has at most one outgoing edge and there are no
  cycles. I assert both (one edge per proof, DAG) but did not print a direct
  verification of acyclicity here.

---

## CLAIM 3 — "The small islands are mostly machinery, but NOT mostly a lemma plus its own compiler twin"

This is a claim where **I was partly wrong and corrected myself**, so it is a
good place to check whether I am grading myself honestly.

**Numbers claimed:** 16,367 of 25,230 components (64.9%) have size 2–3. Of
4,000 sampled such components: **29.3%** consist entirely of one declaration
plus its own compiler-generated offspring (shared "stem"); **76.1%** contain
at least one machine-generated node. Merging twins into parents would remove
roughly 4,800 components, leaving ~20,431 — i.e. it does NOT dissolve the
fragmentation.

**Receipt:** `logs/twin_analysis.log`, script `src/twin_analysis.py`.

**Weaknesses to attack — this is the softest evidence in the package:**
- The "same stem" test is a **regular expression** over names
  (`._simp_N`, `._proof_N`, `._unary`, `.eq_N`, `.match_N`, `._aux`, `._f`,
  `._g`, `._sparseCasesOn`, `.eq_def`, `._eq_N`) plus `_private.` prefix
  stripping. It is a heuristic and will both over- and under-match. A stricter
  test would use the recorded `gen` flag together with the actual parent
  resolution from `src/parent_labels.py`, which I did not do here.
- 4,000 of 16,367 sampled, single seed, no confidence interval reported.
- Components of size 4+ were not examined for the twin pattern at all.

---

## CLAIM 4 — "The large components cluster by TECHNIQUE, not by subject"

**Numbers claimed:** across 400 sampled components of size ≥ 5, dominant
namespace purity averages 41.2% (median 32.5%); only **20.0%** are
single-area (≥80% one namespace); 10.8% are ≥80% machine-generated.

**The qualitative claim** rests on two component samples printed in
`logs/islands.log`:
- a component whose members include `Classical.propDecidable`,
  `linearOrderOfSTO`, `Classical.choose_spec`, `eq_or_ne` — read as "proofs
  whose key move is classical choice";
- a component whose members include `Quot.ind`, `Con.commGroup._proof_1`,
  `Quotient.mk''_surjective`, `Ordinal.instLinearOrder` — read as "proofs
  whose key move is a quotient".

**Receipt:** `logs/islands.log`, section B and the coherence block;
`data/island_forensics.json`.

**Weaknesses to attack — this is the claim I am least sure of:**
- The quantitative part (purity 41%) establishes only that components are
  **not** subject-coherent. It does NOT establish that they are
  technique-coherent. That is my reading of **four sampled member names from
  each of two components**, and it is an interpretation, not a measurement.
- A rigorous version would test whether membership is predicted by the shared
  rank-1 move across the component, and would report that as a number. I have
  not done this. **If you think this claim is unsupported, say so — I think
  it is the weakest strong-sounding sentence I wrote.**

---

## CLAIM 5 — "Connectivity is orthogonal to ranking: the virtual root buys connectivity without changing any proof's rank"

**Numbers claimed:** grounding every sink at one virtual root gives 64
components at the most-filtered level (99.98% giant) and exactly 1 component
from the top-25% level onward, while "mathematics only" (no root) gives
34,337 / 1,716 / 569 at the same levels.

**Receipt:** `logs/backbone2.log`, the slider table with both column pairs.
Script `src/backbone.py`, function `components(mask, with_root)`.

**Weaknesses to attack:**
- The *logical* argument that the root does not disturb ranking is sound (it
  adds edges only from sinks, which by definition have no outgoing edge, so no
  node's chosen parent changes). But I did not run V8's own top-1 graph with
  a virtual root and confirm 1 component. **That specific configuration —
  the one I am recommending — has not actually been executed.** It is
  inference from the two measurements above.

---

## CLAIM 6 — "V8's ranking is validated for keyness; my new depth×idf weight is not"

**Numbers claimed:** V8's ranked view scored 37.7% exact / 71.0%
exact-or-partial agreement with three independent blind raters who named the
key move before seeing any system output; the zoom display view scored 56.5%
/ 92.8%. n = 23 proofs.

**Receipt:** `data/keyness_results.json`, key `primary_(23_clean_proofs)`,
fields `top1_yes_rate` and `top1_yes_or_partial_rate` for views `ranked` and
`zoom`.

**Weaknesses to attack:**
- n = 23, one panel, agent raters rather than human mathematicians. This is
  thin, and it was disclosed as thin in the earlier trial.
- Those numbers were measured on formulation **V5v**, two revisions before
  the V8 that is now frozen. Strictly, the validated object is not identical
  to the object I am recommending.
- The new weight is genuinely untested — that half of the claim needs no
  audit, it is an admission.

---

## CLAIM 7 — "Stratified purity: glue at the base, content at the top"

**Numbers claimed:** rank-1 content purity by depth of the theorem: 48.9%
(depth 0–10), 59.8% (10–25), 53.1% (25–50), 74.8% (50–75), 72.3% (75–125),
78.6% (125+). Separately, backbone edges whose cited endpoint is content:
27.7% rising to 70.2% across the same bands.

**Receipt:** `logs/strat.log` section A; `logs/backbone2.log` final section;
`data/stratified_purity.json`, `data/backbone_results.json`.

**Weaknesses to attack:**
- The gradient is not monotone — it dips at 25–50 and again at 75–125. I
  described it as rising, which is true end-to-end but glosses the dips.
- "Content" here means "a claim that is not logic-only", i.e. it is defined by
  the frozen V8 categories. So this measures agreement between V8's own
  notions, not agreement with an external standard.

---

## What I would attack first if I were you

1. **Claim 4** — the technique-clustering reading. It is an interpretation of
   eight declaration names and I stated it with more confidence than the
   evidence carries.
2. **Claim 3's regex.** If the stem heuristic is wrong, the 29.3% is wrong,
   and that number is what I used to walk back my earlier stronger claim.
3. **Claim 5's untested configuration** — I am recommending a setup I never
   ran.
4. **Whether Claim 1 survives on the directed graph.** Everything here is weak
   connectivity. For navigation, direction may be what matters.
