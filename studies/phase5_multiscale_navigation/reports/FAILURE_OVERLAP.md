# Failure overlap across M1 / M2 / M3

**Status: EXPLORATORY.** Computed on the sealed TEST-R labels *after* unsealing,
same standing as `ABLATION.md`. It partitions known failures and generates
hypotheses. It cannot promote anything. TEST-R is burned for these questions.

Source: `review/failures/testr/{M1,M2,M3}*.json`, semantics per `src/mine_failures.py`.
All 360 TEST-R proofs were re-scored from the corpus to obtain per-proof status for
*non-failing* proofs too, so every claimed property is checked against successes.
The reconstruction reproduces the shipped banks exactly (39/14/1, 62/25/0, 33/5/1).

| method | factors | append-safe | NavAP | P@1 | prec | recall items | grad | **proofs failing** |
|---|---|---|---|---|---|---|---|---|
| M1_role_x_frozen_rarity | role x rarity_frozen | yes | 0.8621 | 0.975 | 39 | 14 | 1 | **53** |
| M2_role_x_depth | role x depth | yes | 0.8458 | 0.897 | 62 | 25 | 0 | **78** |
| M3_promoted_composite | role x stmt x depth x rarity_live | **no** | 0.8712 | 0.983 | 33 | 5 | 1 | **39** |

`prec` counts proofs; `recall items` counts buried CORE moves (23 M2 proofs hold 25).

---

## 1. The partition

Proof-level, "fails" = trips any of the three criteria. 360 proofs.

| M1 | M2 | M3 | proofs | reading |
|---|---|---|---|---|
| . | . | . | **257** | clean everywhere |
| . | X | . | 47 | M2-only failure |
| X | X | X | **24** | **universal — the ceiling** |
| X | . | X | 12 | M2 wins (deep proofs) |
| X | . | . | 11 | M1-only failure |
| X | X | . | **6** | **M3-only success — the price of append-safety** |
| . | . | X | 2 | M3-only failure |
| . | X | X | 1 | — |

**103 proofs (28.6%) fail at least one method. 257 (71.4%) are clean under all three.**

By failure class:

| pattern | precision | recall | gradient |
|---|---|---|---|
| none | 279 | 329 | 359 |
| all three | **21** | **3** | 0 |
| M1 only | 8 | 6 | 0 |
| M2 only | 39 | 17 | 0 |
| M3 only | 2 | 0 | 0 |
| M1+M3 (M2 ok) | 9 | 2 | 1 |
| M1+M2 (M3 ok) | 1 | 3 | 0 |
| M2+M3 (M1 ok) | 1 | 0 | 0 |

Precision failures are where the overlap concentrates (21 universal of 81 failing proofs);
recall failures are almost entirely M2's own (17 of 31).

Pairwise, "row fails where column succeeds":

| | vs M1 | vs M2 | vs M3 | total failing |
|---|---|---|---|---|
| M1 | — | 23 | 17 | 53 |
| M2 | 48 | — | 53 | 78 |
| M3 | 3 | 14 | — | 39 |

---

## 2. Universal failures — the ceiling

24 proofs. **Half of them are not ranking failures at all: they are failures of the
proof to contain anything worth ranking.**

### 2a. The forced set (13 of 24)

The `top4_mostly_defects` criterion fires when >=3 of the top 4 are graded <=1 and
n>=6. A proof with n>=6 and **at most one useful (>=2) candidate** trips it under
*every possible permutation* — if the useful item is placed first, ranks 2-4 are
necessarily defects; if not, `defect_at_rank_1` fires instead.

| | proofs |
|---|---|
| n>=6 and n_useful<=1 (forced `top4_mostly_defects` or rank-1 defect) | **12** |
| ...of which all three methods fail | **12 (100%)** |
| n_useful == 0, n<6 (forced `defect_at_rank_1` at any n) — `proof_0117` | **1** |
| **total structurally unrankable** | **13** |

**Discriminating check:** of the 257 clean proofs, **0** have n>=6 and n_useful<=1, and
**0** have n_useful == 0. The 16 clean proofs with n_useful<=1 all have n<6 *and* one
useful candidate, so a correct ordering clears both criteria. The property is perfectly
separating.

**13 of 53 M1 failures (25%) and 13 of 39 M3 failures (33%) are arithmetic, not error.**

### 2b. The rankable universal set (11 of 24)

| proof | theorem | n | n_useful | universal mode |
|---|---|---|---|---|
| 0093 | `propext_iff` | 11 | 4 | `propext` buried at 8/6/7 |
| 0115 | `addLECancellable_zero` | 18 | 2 | top4 / rank-1 defect |
| 0146 | `CategoryTheory.prod.prodμ_counitIso_inv_app` | 18 | 2 | defect at rank 1, all three |
| 0204 | `CategoryTheory.MonoidalOpposite.mopMopEquivalenceInverseMono` | 18 | 2 | defect at rank 1 (M1,M3) |
| 0208 | `Int.lt_min` | 7 | 2 | top4 |
| 0262 | `Finset.weightedVSub_filter_of_ne` | 20 | 2 | top4 |
| 0318 | `...IsCardinalFiltered.exists_cardinal_directed.f` | 23 | 6 | `Category.assoc` buried at 10/12/7 |
| 0396 | `WithLp.prod_lipschitzWith_ofLp` | 9 | 2 | top4 |
| 0402 | `AEMeasurable.nullMeasurable` | 12 | 7 | defect at rank 1, all three |
| 0410 | `ModularForm.coe_const` | 25 | 3 | top4 |
| 0411 | `Polynomial.splits_mul_X` | 25 | 4 | `mul_comm` buried at 6/12/5 |

Six of these have exactly n_useful == 2, one short of clearing `top4`. The recall cases
(0093, 0318, 0411) share a signature: **the buried CORE is a universal foundational lemma**
(`propext`, `Category.assoc`, `mul_comm`) — maximally common, therefore minimum rarity,
minimum cited depth, and demoted by every signal any method reads.

### 2c. Characterisation, with the discrimination check

Rate in universal failures vs rate in the 257 clean proofs.

| property | universal | clean | ratio | verdict |
|---|---|---|---|---|
| n_useful <= 1 | 0.542 | 0.062 | **8.7x** | explains |
| n_useful <= 1 and n>=6 | 0.500 | **0.000** | inf | **explains, perfectly** |
| frac_defect >= 0.8 | 0.792 | 0.109 | **7.3x** | explains |
| max_grade <= 2 (no MAJOR at all) | 0.167 | 0.043 | 3.9x | explains |
| >=1 rater not "high" confidence | 0.750 | 0.490 | 1.5x | weakly explains |
| `missing_key` flagged by any rater | 0.208 | 0.074 | 2.8x | weak, n=5 |
| `missing_key` flagged by majority | 0.083 | 0.012 | — | weak, n=2 |
| max rater disagreement >= 2 | 0.167 | 0.093 | 1.8x | weak, n=4 |
| target depth <= 10 | 0.250 | 0.171 | 1.5x | **explains nothing** |
| n_candidates >= 15 | 0.292 | 0.331 | 0.88x | **explains nothing** |
| has >=1 CORE candidate | 0.750 | 0.774 | 0.97x | **explains nothing** |
| any auto-generated candidate | 0.125 | 0.051 | 2.5x | weak, n=3 |

Means: target depth 68.6 vs 67.1 (clean); n_candidates 12.0 vs 12.1; mean rater
disagreement 0.307 vs 0.293; frac auto-generated 0.007 vs 0.006. **None of the
obvious structural suspects survive the check against successes.**

Kind mix is indistinguishable:

| | def | inductive | theorem | constructor |
|---|---|---|---|---|
| universal (288 cands) | 0.545 | 0.271 | 0.153 | 0.024 |
| clean (3108 cands) | 0.554 | 0.275 | 0.127 | 0.041 |

The grade distribution is where the difference lives:

| | CORE | MAJOR | LEGIT_GLUE | BAD_GLUE | JUNK |
|---|---|---|---|---|---|
| universal | 0.073 | **0.017** | **0.076** | 0.479 | 0.354 |
| clean | 0.085 | **0.070** | **0.191** | 0.372 | 0.282 |

**Universal failures are not missing the CORE — they are missing the middle.**
CORE share is the same (0.073 vs 0.085). MAJOR is depleted 4.1x and LEGIT_GLUE 2.5x.
These proofs have one real move and a wall of junk, with nothing in between to fill
ranks 2-4. No reordering creates the mass that is absent.

**Ceiling statement.** 24 of 360 proofs (6.7%) fail under all three methods. At least
13 of those are arithmetically forced by candidate scarcity. The residual 11 are
dominated by one recurring case — a universal foundational lemma (`mul_comm`,
`propext`, `Category.assoc`) that is the actual move, and that every rarity- or
depth-driven signal must rank last by construction.

---

## 3. The price of append-safety

### 3a. The strict M3-only-success set: 6 proofs

Both append-safe methods fail, the non-append-safe incumbent succeeds.
**6 of 103 failing proofs (5.8%); 6 of 360 proofs (1.7%).**

| proof | theorem | d | n | M1 fails by | M2 fails by | signal M3 had |
|---|---|---|---|---|---|---|
| 0184 | `Set.image_domRestrict` | 18 | 22 | `Set.image_comp` (CORE) buried at 5 | `Eq.mpr` (BAD_GLUE) at rank 1 | **live rarity** demotes `Eq.mpr` (2.07) from 1 to 11; **stmt** lifts `image_comp` to 4 |
| 0227 | `UInt64.toFin_sub` | 28 | 8 | `UInt64.size` (BAD_GLUE) at rank 1 | `UInt64.toFin` (CORE) buried at 5 | **depth x rarity jointly**; all 8 candidates are in-statement so `stmt` is constant here |
| 0241 | `...SmallObject.hasPushouts` | 41 | 18 | top4 defects | top4 defects | **live rarity only** (see 3c) |
| 0311 | `Finset.Ico_disjoint_Ico_consecutive` | 59 | 24 | `LT.lt.not_ge` buried at 7 | `LT.lt.not_ge` at 6, `Finset.mem_Ico` at 8 | **the in-statement term** |
| 0348 | `rank_le_card` | 84 | 24 | `ciSup_le'` buried at 5 | `ciSup_le'` buried at 5 | **the in-statement term** |
| 0383 | `MeasureTheory.Measure.add_left_inj` | 198 | 19 | `add_comm` (CORE) buried at 5 | top4 + `add_comm` at 7 | **live rarity only** (see 3c) |

Group profile vs clean: n_candidates 19.2 vs 12.1, n_useful 6.2 vs 4.2, n_core 2.0 vs 1.0.
These are large, content-rich proofs — the opposite of the universal set. They are cases
where a real ordering decision existed and the append-safe signals got it wrong.

### 3b. Four of the six are recoverable *without* giving up append-safety

Append-safe variants built from the same factor table (`stmt` is a per-citation local
fact — `inc_in_stmt_world` — so it is append-safe by construction):

| variant | factors | append-safe | NavAP | P@1 | prec | recall | grad | proofs failing | fixes of the 6 |
|---|---|---|---|---|---|---|---|---|---|
| M1 (incumbent safe) | role x rarity_frozen | yes | 0.8621 | 0.975 | 39 | 14 | 1 | 53 | 0 |
| M2 | role x depth | yes | 0.8458 | 0.897 | 62 | 25 | 0 | 78 | 0 |
| **M4** | **role x stmt x rarity_frozen** | **yes** | **0.8671** | 0.978 | 39 | **9** | 1 | **48** | 3 (0184, 0311, 0348) |
| M6 | role x stmt x depth x rarity_frozen | yes | 0.8604 | **0.986** | 41 | 11 | 1 | 51 | 3 (0184, 0227, 0348) |
| M7 | role x depth x rarity_frozen | yes | 0.8566 | 0.983 | 41 | 16 | 1 | 54 | 2 (0184, 0227) |
| M5 | role x stmt x depth | yes | 0.8491 | 0.931 | 52 | 15 | 1 | 61 | 2 (0311, 0348) |
| M3 (incumbent, unsafe) | role x stmt x depth x rarity_live | no | 0.8712 | 0.983 | 33 | 5 | 1 | 39 | — |
| M3 minus stmt | role x depth x rarity_live | no | 0.8689 | 0.983 | 33 | 9 | 1 | 43 | — |

Union of the 6 fixed by *some* append-safe variant: **{0184, 0227, 0311, 0348} = 4 of 6.**
Never fixed by any append-safe variant: **{0241, 0383} = 2 of 360 (0.6%).**

**M4 = role x in-statement x frozen rarity is append-safe and dominates M1 on every axis:**
NavAP 0.8671 vs 0.8621, P@1 0.978 vs 0.975, recall failures 9 vs 14, failing proofs 48 vs 53.
It closes 55% of the M1 -> M3 NavAP gap at zero cost to append-safety, and cuts M1's
losses against M3 from 17 proofs to 12. This is the single most consequential finding here.

Why it works: `in_statement` is by far the sharpest append-safe discriminator in the
candidate pool, and neither M1 nor M2 reads it.

| | n candidates | P(CORE) | P(useful) | P(defect) |
|---|---|---|---|---|
| in_statement = True | 3998 | 0.014 | 0.239 | 0.761 |
| in_statement = False | 802 | **0.408** | **0.700** | 0.300 |
| pooled base rate | 4800 | 0.080 | 0.316 | 0.684 |

A 5.1x lift on P(CORE) from a boolean the proof itself determines. `ABLATION.md` measured
`stmt` as worth 0.002 by leave-one-out *from the full composite* — correct, because
`rarity_live` was already carrying the same information. Added to a frozen-rarity model
it is worth +0.005 NavAP and 5 recall failures. **Leave-one-out understates a factor
whose information is duplicated by the factor you are trying to remove.**

### 3c. The irreducible two, and the mechanism

Both require live rarity because **frozen rarity systematically over-rates declarations
whose user base lives above the freeze depth.**

`proof_0383`, `MeasureTheory.Measure.add_left_inj`. The CORE move is `add_comm`
(role 0.70, rarity_frozen 6.55, rarity_live 5.95). It is outranked by
`MeasureTheory.SigmaFinite` (LEGIT_GLUE, role 0.50, rarity_frozen **11.36**, rarity_live **7.06**).

```
frozen:  add_comm 0.70 x 6.55 = 4.585   <   SigmaFinite 0.50 x 11.36 = 5.680   -> CORE buried
live:    add_comm 0.70 x 5.95 = 4.165   >   SigmaFinite 0.50 x  7.06 = 3.530   -> CORE surfaces
```

`SigmaFinite` is a depth-2 declaration with in-degree 642 — common library-wide — but its
citers are measure-theory proofs living far above depth 50, so it is almost absent from the
frozen foundation and the frozen IDF inflates it by **+4.30 nats**.

`proof_0241`, `CategoryTheory.SmallObject.hasPushouts`. Margin case:

```
frozen:  IsCardinalForSOA (MAJOR) 0.50 x DEP(39) x 9.02 = 1.3087  <  IsRegular (BAD_GLUE) 0.70 x DEP(19) x 7.86 = 1.3421
live:    IsCardinalForSOA         0.50 x DEP(39) x 8.84 = 1.2826  >  IsRegular            0.70 x DEP(19) x 7.28 = 1.2431
```

Live rarity separates the pair by 21.4% where frozen separates them by 14.8%. That 6.6
points is exactly the margin needed to overcome the role penalty. There is no append-safe
substitute; the information is in the library-wide count.

The bias is general, not anecdotal. Restricting to declarations that matter for ranking
(in-degree >= 200, declaration depth <= 50, n=5423), correlation between mean citer depth
and `rarity_frozen - rarity_live` is **0.651**:

| mean depth of citers | n | rarity_frozen | rarity_live | bias |
|---|---|---|---|---|
| 0-25 | 305 | 7.74 | 7.44 | +0.30 |
| 26-50 | 1404 | 7.00 | 7.12 | -0.12 |
| 51-100 | 2382 | 7.65 | 6.74 | **+0.92** |
| 101-400 | 1219 | 9.21 | 6.74 | **+2.46** |

### 3d. Net accounting

| comparison | append-safe method fails, M3 ok | M3 fails, safe method ok | net cost, proofs |
|---|---|---|---|
| M1 vs M3 (as shipped) | 17 | 3 | **14** (53 - 39) |
| M4 vs M3 (best safe found) | 12 | 3 | **9** (48 - 39) |
| strict "both safe methods fail, M3 succeeds" | 6 | — | 6 |
| of which no append-safe variant recovers | 2 | — | **2** |

**Append-safety as currently shipped costs 14 proofs of 360 (3.9%) and 0.009 NavAP.
Adopting M4 reduces that to 9 proofs (2.5%) and 0.004 NavAP. The irreducible core,
where live library counts carry information no append-safe signal can reconstruct, is
2 proofs of 360 (0.6%).**

---

## 4. M1 vs M2: there is a structural predictor, and it is target depth

| | proofs |
|---|---|
| M1 fails, M2 ok | 23 |
| M2 fails, M1 ok | **48** |
| both fail | 30 |
| neither | 259 |

M1 dominates in aggregate, but the failures are not nested — they cross over cleanly.

| target depth band | n | M1 fails | M2 fails | M1 NavAP | M2 NavAP | M1 P@1 | M2 P@1 |
|---|---|---|---|---|---|---|---|
| 0-10 | 60 | 7 | 14 | **0.9094** | 0.8604 | **0.983** | 0.850 |
| 11-50 | 120 | 17 | 39 | **0.8598** | 0.8231 | **0.967** | 0.783 |
| 51-150 | 134 | 21 | **17** | 0.8505 | **0.8624** | 0.978 | **0.993** |
| 151+ | 46 | 8 | 8 | 0.8409 | 0.8376 | 0.978 | 0.978 |

Crossover swept over thresholds — it lands exactly on the freeze depth:

| threshold | below: M1 / M2 fails | above: M1 / M2 fails |
|---|---|---|
| d <= 10 | 7 / 14 | 46 / 64 |
| d <= 25 | 12 / 30 | 41 / 48 |
| **d <= 50** | **24 / 53** | **29 / 25** |
| d <= 75 | 36 / 61 | 17 / 17 |
| d <= 150 | 45 / 70 | 8 / 8 |

**Predictor: trust frozen rarity at target depth <= 50, trust depth above it.**
The crossover coincides with the d<=50 freeze, and the mechanism is exact.

**Why M1 degrades above depth 50 — saturation.** `IDF50 = log(n50 / pop50)` with
`n50 = 430,358`, so the cap is `log(430358) = 12.9724`. A declaration at depth > 50
*cannot* be cited by a proof at target depth <= 50 (depth is well-founded), so its
`pop50` is 0 and its frozen rarity is *identically the cap*: **99.98% of cited
declarations above depth 50 have pop50 == 0.** Frozen rarity is a constant function on
the entire above-freeze subgraph, and ties fall back to input order.

| band | candidates | % at the frozen cap | % of proofs with a tie at rank 1 | mean tie-group size at top |
|---|---|---|---|---|
| 0-10 | 550 | 0.7% | 0.0% | 1.00 |
| 11-50 | 1807 | 1.5% | 0.8% | 1.01 |
| 51-150 | 1767 | **18.7%** | **23.1%** | 1.42 |
| 151+ | 676 | **29.4%** | 15.2% | 1.35 |

M2's tie-at-top rate never exceeds 2.2% in any band.

**Why M2 degrades below depth 50 — compression.** The depth score is
`0.20 + 0.80 * cited_depth / 346`. Shallow proofs cite shallow things, so the score has
essentially no dynamic range:

| band | mean cited depth | mean within-proof depth-score spread | mean within-proof frozen-rarity spread |
|---|---|---|---|
| 0-10 | 1.9 | **0.011** | 7.822 |
| 11-50 | 6.2 | 0.057 | 9.572 |
| 51-150 | 18.5 | 0.189 | 10.779 |
| 151+ | 44.8 | 0.412 | 10.194 |

At band 0-10 the depth factor varies by 1.1% across a proof's candidates. `role` alone
decides the order, which is why M2's P@1 collapses to 0.850 / 0.783 in the two shallow
bands while holding 0.993 deep. This corroborates the note already in
`APPEND_SAFETY.md` and supplies the mechanism.

**The two methods degenerate at opposite ends of the same axis.** Neither is a subset of
the other and the switch point is not a tuned hyperparameter — it is the freeze depth
itself. A depth-gated composite is the obvious move; note that the naive product
M7 = role x depth x rarity_frozen scores *worse* than M1 alone (0.8566 vs 0.8621), so
multiplying them together is not the right combination.

---

## 5. Gradient reversals

Rarest class and the most diagnostic. 315 of 360 proofs are eligible (n >= 6).
**Exactly one proof reverses, and it reverses under M1, M3 and M4 but not M2.**

`proof_0305`, `BoolAlg.dualEquiv_inverse`, target depth 66, n=6.
Unanimous rater note: *"Proved by rfl — it just projects a field out of the equivalence
as constructed. Purely definitional."*

M1 order (top half useful rate 0.333, bottom half 0.667):

| rank | grade | declaration | kind | role | cited depth | rarity_frozen | rarity_live |
|---|---|---|---|---|---|---|---|
| 1 | **4** | `BoolAlg.dualEquiv` | def | explicit-arg | 65 | 12.97 | 12.83 |
| 2 | 1 | `BoolAlg` | inductive | explicit-arg | 0 | 9.61 | 8.37 |
| 3 | **0** | `BoolAlg.instCategory` | def | instance-slot | 56 | **12.97 (at cap)** | 8.81 |
| 4 | 2 | `CategoryTheory.Equivalence.inverse` | def | explicit-arg | 2 | 5.59 | 5.89 |
| 5 | 2 | `Eq.refl` | constructor | applied | 1 | 1.55 | 1.56 |
| 6 | 1 | `CategoryTheory.Functor` | inductive | implicit-arg | 1 | 2.57 | 2.88 |

**Diagnosis.** Rank 1 is correct — the CORE is surfaced. The reversal is entirely in
ranks 2-6, and its cause is that this proof has no mathematics. When the proof is `rfl`,
the only *useful* content is generic plumbing (`Equivalence.inverse`, `Eq.refl`), which is
by definition low-rarity and low-depth. What sits above it is namespace-local apparatus —
the ambient structure `BoolAlg` and its instance `BoolAlg.instCategory` — which is
near-unique and deep, therefore maximal on every signal, and which raters graded
BAD_GLUE and JUNK.

`BoolAlg.instCategory` is cited at depth 56, above the freeze, so its frozen rarity is
*exactly the cap* — the same saturation defect as section 4, surfacing here as a rank-3
JUNK item. M3 is worse, not better, promoting it to rank 2 (grades `[4,0,1,2,2,1]`).

**Every scoring factor except `role` is monotone increasing in specificity.** When the
content of a proof *is* the generic plumbing, the ordering must invert. M2 is the only
method that escapes, and not through depth — the depth spread is negligible here — but
because `Eq.refl` carries role `applied` (1.00) against `BoolAlg`'s `explicit-arg` (0.70),
so role alone lifts it to rank 2 (`[4,2,0,2,1,1]`).

Pooled across all 4800 graded candidates, the signal profile by grade explains why the
inversion is confined to the LEGIT_GLUE band:

| grade | n | rarity_frozen | rarity_live | cited depth | role | frac in-statement |
|---|---|---|---|---|---|---|
| CORE | 382 | 11.44 | 10.97 | 55.9 | 0.81 | **0.14** |
| MAJOR | 302 | 9.61 | 8.61 | 32.1 | 0.68 | 0.65 |
| LEGIT_GLUE | 833 | 7.08 | 6.14 | 15.2 | 0.67 | 0.85 |
| BAD_GLUE + JUNK | 3283 | 4.91 | 3.98 | 8.3 | 0.56 | 0.93 |

CORE is cleanly separated on rarity and depth. LEGIT_GLUE is not: it sits close to the
defect population on every continuous signal (7.08 vs 4.91 frozen; 15.2 vs 8.3 depth) and
is *indistinguishable* on role (0.67 vs 0.56) and in-statement share (0.85 vs 0.93).
The ranking problem is essentially solved for CORE and essentially unsolved for
LEGIT_GLUE. That is where the reversal lives, and it is also where the universal
failures' missing mass lives (section 2c).

**One reversal in 315 eligible proofs (0.3%) is not a rate worth optimising against, but
the case is a clean pointer at the two structural defects the aggregate scores hide:
frozen-rarity saturation above the freeze depth, and the absence of any signal that
separates LEGIT_GLUE from JUNK.**

---

## 6. What follows

1. **Test `role x in-statement x frozen rarity` (M4) on a fresh sample.** Append-safe,
   and on burned TEST-R it strictly dominates the shipped M1: +0.005 NavAP, recall
   failures 14 -> 9, failing proofs 53 -> 48. `in_statement` gives a 5.1x lift on
   P(CORE) and neither append-safe candidate currently reads it.
2. **The frozen foundation has a known, measurable bias**: it inflates the rarity of
   declarations whose citers live above the freeze depth (+2.46 nats for the deepest
   quartile of well-cited declarations) and is *constant* on the entire above-freeze
   subgraph. Both of the irreducible append-safety losses are this bias. A deeper freeze
   (d<=100 or d<=150) trades append-safety headroom for less saturation and is the
   obvious thing to measure next.
3. **Do not pursue M2 or any depth-only variant.** It is dominated everywhere below
   depth 50 and its aggregate advantage above depth 50 (25 vs 29 failures) is small and
   comes with 37 rank-1 defects against M1's 9.
4. **Set expectations at the ceiling.** 13 of 360 TEST-R proofs (3.6%) cannot clear the
   precision criteria under any permutation of their candidates. Any precision-failure
   count should be reported net of them: M1 is 39 gross, 26 net; M3 is 33 gross, 20 net.
5. **The next real gain is a LEGIT_GLUE detector, not a better rarity term.** Rarity and
   depth already separate CORE from everything else. They do not separate plumbing that
   is the content from plumbing that is noise, and that is where the universal failures,
   the gradient reversal, and the missing top-4 mass all sit.
