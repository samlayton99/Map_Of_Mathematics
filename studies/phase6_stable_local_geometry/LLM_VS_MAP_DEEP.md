# Where does the map win? A full accounting (2026-08-22)

Sam asked which areas his version wins and what it adds. I went looking
for wins and mostly did not find them. Everything below is measured on
the same 60 held-out theorems; nothing here is asserted.

## The decisive experiment: does the map help an LLM?

Union recall (0.475) was an ORACLE union -- it credits a hit in either
list without anyone having to choose. The real system test is to hand
the LLM the map's top-10 as hints and let it commit to a final 10.

| condition | recall@10 |
|---|---|
| LLM alone, run 1 | 0.444 |
| LLM alone, run 2 (independent agent, same items) | **0.476** |
| LLM + map hints | 0.464 |
| LLM alone, anonymised statement | 0.359 |
| map alone | 0.098 |

**The hints add +0.020, and a second unaided run swung +0.032.** The
augmentation delta is smaller than this LLM's own run-to-run noise.
The LLM adopted 2 of 10 slots from the hints on average, and across all
60 theorems exactly **3** adopted names were both correct and absent
from its unaided answer.

The cleanest way to say it, using 20 candidate slots either way:

| 20-slot budget | recall |
|---|---|
| LLM top-10 + map top-10 | 0.475 |
| **LLM top-10 + a second LLM top-10** | **0.537** |

If you have room for ten more candidates, a second sample from the
model beats the map. On this task the map is not merely weaker; it is
not worth the context.

## Claimed advantages that did NOT survive measurement

1. **"It knows when it is right."** False. Bucketing by the map's own
   top-1 co-use score, hit rate is flat: 0.154 / 0.071 / 0.154 across
   terciles. The score carries no calibration, so it cannot tell a
   solver when to trust it.
2. **"It locates the right neighbourhood."** False, and I asserted this
   last round from a single example. When each system MISSES, the LLM
   is closer: it proposes a same-namespace sibling 0.829 of the time vs
   the map's 0.543, with token overlap 0.272 vs 0.189 and a median depth
   gap of 1 vs 3. The LLM is also more on-area overall (0.620 vs 0.448).
3. **"It finds the obscure lemmas an LLM would not know."** False, and
   backwards. Moves found ONLY by the LLM have median in-degree **4**;
   moves found only by the map, 18; found by both, 35. The LLM is the
   one reaching obscure material.
4. **"Its popularity bias is a fixable artifact."** Half true. The bias
   is real -- the truth has median in-degree 5, the map proposes median
   51 (the LLM, 23). Normalising co-use by marginal frequency fixes the
   bias exactly as intended (median 58 -> 20) and changes recall by
   **-0.005**. The bias is not the bottleneck; the signal is.
5. **"It abstains where it is unsure."** It abstains on 15% (9/60,
   statement worlds with no co-use neighbour), and the LLM scores
   **0.778** on precisely those nine. It goes blank where the task is
   easy.

## What DOES hold up

1. **Determinism.** Two independent runs of the same model on the same
   items share only **0.475** of their top-10 by Jaccard, and on 13.3%
   of items one run scores while the other does not. The map returns a
   bit-identical answer every time. Note the honest flip side: that
   instability is exploitable, which is why two runs beat one.
2. **Every proposal is real.** 1.000 of the map's names exist in
   Mathlib against 0.878 of the LLM's -- 12% of its suggestions are
   names that do not exist. For an agent that must then elaborate the
   term, that is a hard failure, not a soft one.
3. **Level targeting.** True moves sit at median depth 88. The map
   proposes median depth 68; the LLM, 41. Even when the map is wrong it
   is wrong at closer to the right level of specificity -- the LLM
   reaches for more foundational, more famous lemmas.
4. **Cost.** 0.2 ms per theorem against roughly 6 s of model inference:
   about 30,000x. Real, but an engineering property, not a mathematical
   one.
5. **The four wins, itemised** (4 of 117 moves, all deep, 74-121):

   | target | map found | LLM proposed instead |
   |---|---|---|
   | `CoxeterSystem.IsReflection.inv` | `CoxeterSystem.inv_simple` (r1) | `...mul_self`, `...simple_sq` |
   | `Finsupp.mem_range_embDomain_iff` | `Finsupp.ext` (r1), `embDomain_eq_mapDomain` (r3) | `support_embDomain`, `embDomain_apply` |
   | `UniformOnFun.postcomp_uniformContinuous` | `uniformContinuous_iff_le_comap` (r2) | `UniformFun.postcomp_uniformContinuous` |
   | `eventually_singleton_add_smul_subset` | `norm_nonneg` (r3) | `Metric.isBounded_iff_subset_closedBall` |

   The shape is suggestive -- structural workhorses (`Finsupp.ext`,
   `norm_nonneg`) that are load-bearing but not topically salient, while
   the LLM chased same-namespace siblings. **But I tested that story and
   it did not generalise**: splitting all 117 moves by whether the
   answer shares the target's namespace, the map/LLM ratio is
   essentially unchanged (0.35x inside, 0.29x outside). With n=4 this
   is a hint, not a finding.

## The LLM's failure mode, for the record

**82.9% of the LLM's misses came with a same-namespace sibling in its
top 10.** It reliably identifies the right file-level neighbourhood and
then picks the wrong lemma from it. That is the gap a structural index
ought to close -- and the measurements above say ours does not close it.

## Honest strategic conclusion

On premise retrieval the map has no measurable edge, does not help as
context, and is beaten by simply sampling the model twice. Its case
cannot rest on retrieval accuracy. What remains is that it is a
different KIND of object, and those properties are real but are not
accuracy claims:

- every edge is a kernel fact with a deterministic derivation
  (auditable; an LLM's suggestion is a guess to be checked);
- append-safety: adding mathematics never re-scores existing proofs;
- it covers mathematics written after any training cutoff -- the
  chronological test (13.5x) is evidence no language model can
  currently be given;
- it is stable under refactoring (0.868 vs 0.000 metamorphic), where a
  model's answer moves with the surface text;
- it produces a global decomposition of 771k declarations (AMI 0.416
  vs 0.212 flat), which is not a thing you can prompt for.

The retrieval benchmark was the right test to run and it returned a
negative. The program should be re-aimed at the properties above, or at
a use of the geometry that is not next-move prediction.

## Caveats

- n=60, mean 1.95 answers per theorem; subgroup splits (n=4 to n=36)
  are indicative only.
- One model, one prompt, default reasoning budget, no retrieval
  augmentation on either side.
- Ground truth is our own inclusion policy's move set; it scores both
  systems identically, so the comparison is fair, but the ceiling is
  not 1.0.
- Contamination remains unquantified in the strict sense; the
  anonymised control (0.359 vs 0.444) bounds but does not eliminate it.
