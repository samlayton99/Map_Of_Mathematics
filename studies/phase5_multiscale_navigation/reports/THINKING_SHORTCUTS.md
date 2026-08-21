# Thinking: relative shortcuts, and what a map edge should mean

Not a results report. This is the reasoning before the next round, written to
be argued with.

---

## 1. The correction that started this

I measured whether the graph stays *connected* without junk edges (94.8%
retained) and concluded junk was not a problem. Wrong question. Junk does not
hold the graph together — it holds it too **close**. Components barely move;
distances collapse.

Measuring the right thing showed severe failure: junk is 9% of declarations but
**49–70% of top hubs**, and graded real mathematics reaches the high-degree
tail only 28–34% of the time against junk at 82–89%.

## 2. But "junk" is the wrong frame too

The project lead's objection: the natural numbers could connect all of
mathematics. `Nat` would be a terrible hub between algebraic topology and
geometry — and a perfectly good one within number theory.

`Nat` is not junk. Neither is `mul_comm`. Both are real mathematics and both
are terrible landmarks. So the property that makes a bad shortcut is **not
junkiness — it is universality.**

Measured directly, over 18.1M candidate edges:

| declaration | depth | cited by | delta-depth p10 | p50 | p90 | spread |
|---|---|---|---|---|---|---|
| `Eq` | 0 | 301,634 | 8 | 48 | 148 | 140 |
| `Nat` | 0 | 190,566 | 8 | 49 | 137 | **129** |
| `congrArg` | 3 | 165,584 | 13 | 63 | 171 | 158 |
| `Eq.trans` | 3 | 113,830 | 13 | 57 | 164 | 151 |

`Nat` sits 8 levels below some theorems and 137 below others. **The same node
is a near neighbour of some mathematics and a distant one of other
mathematics.** No node-level label can express that, which means every
junk-classifier approach — including the one I built — is attacking the wrong
object.

## 3. The reframe: badness is a property of the EDGE, not the node

Define `delta_depth(T, c) = depth(T) - depth(c)`: how far below the theorem the
cited declaration sits.

- `Nat` cited by a number-theory result at depth 10 → delta 10. It is part of
  the neighbourhood. Legitimate hub.
- `Nat` cited by an algebraic-topology result at depth 200 → delta 200. It is
  a 200-level plunge to something universal. False shortcut.

**Same node, same signal, opposite verdict — decided by the pair, not the
node.** That is exactly the relativity the project lead described, and it is
computable.

Crucially `delta_depth` is **append-safe**: both depths are properties of what
lies beneath, so adding theorems above changes neither. It needs no counts and
no name matching.

Distribution over all edges: 6.2% have delta 1–2, while **52% have delta above
50** and 24.8% above 100. Half the graph consists of long plunges.

## 4. Why this dissolves a problem the forensics called unsolvable

The M2 forensics concluded: depth cannot separate universal automation
(`congrArg`) from universal mathematics (`mul_comm`) because both bottom out at
depth 0–4 — "no cone-local quantity can recover this."

That is true, and **for the shortcut question it does not matter**, because
both are bad landmarks. The separation that is hard for local ranking is
unnecessary for global navigation.

This yields a clean split that I had been conflating:

| question | what must be distinguished | signals that work |
|---|---|---|
| **local**: is this a key move of *this* proof? | junk from content | role, rarity — hard, needs the fitted stuff |
| **global**: is this a good landmark *between these two things*? | universal from specific | `delta_depth` — easy, append-safe, no constants |

Two questions, two mechanisms. Trying to serve both with one score is probably
why the score kept needing arbitrary weights.

## 5. On the weighted-graph proposal

The lead suggested: deep connections cheap, Lean machinery expensive, so a trip
from algebraic topology to geometry is expensive through `Nat` but cheap
through real theorems.

**What is right about it:** it makes cost a property of the traversal, which is
the correct object, and it lets structure "fold out" rather than be imposed.

**Two reservations.**

*First, it reintroduces constants.* Any cost function needs a shape, and
"expensive" versus "cheap" is exactly the exchange rate we just spent this
session eliminating. If the cost is `f(delta_depth)`, the choice of `f` is a
fitted decision.

*Second, shortest-path may be the wrong model of reading.* A reader does not
compute geodesics; they expand a node and look at what is offered. The
quantity that matters is what appears at each expansion, not the length of an
optimal route nobody takes.

**An alternative with no constants: filter rather than weight.** Admit an edge
only when `delta_depth` is small *relative to the other edges of that proof* —
a within-proof rank, which is exactly the constant-free device already in hand.
Then the map connects things at comparable levels of abstraction, and a
depth-300 theorem reaches `Eq` the way mathematics actually does: through
intermediate structure, over several hops, rather than in one plunge.

That is a **multiscale** structure rather than a weighting: at each zoom level
you see connections spanning a bounded abstraction distance. It matches the
phase's original ambition better than a cost function does, and it costs
nothing in constants.

Both should be tested. I lean to the filter, but not confidently.

## 6. The circularity trap — the most serious methodological risk

The lead's warning: do not manufacture arbitrary structure that happens to
match the artificial lines we drew.

We are already inside this trap. The dominance agent caught it: the low
junk-edge share of some schemes is **partly definitional**, because the junk
mask is built from the same two kernel signals those schemes rank on. I defined
junk, then measured junk removal, and scored myself.

Any validation that uses our own junk definition is circular. We need a check
that is **independent of the construction**. Candidates:

1. **Module co-location as weak ground truth.** Two theorems in the same
   Mathlib file are probably related. A map full of false shortcuts will show
   map-distance poorly correlated with module proximity. Note carefully: using
   names to *build* a ranking is forbidden; using an independent human artifact
   to *validate* one is a different act. That distinction must be stated
   explicitly every time it is used, or it will drift.
2. **Held-out prediction.** Does the map predict which declarations a proof
   will cite, on proofs never used to build it? A structure with real content
   predicts; a manufactured one does not.
3. **Pairwise rater judgement.** Show two theorems, ask whether they are
   related, compare with map distance. Most expensive, most direct.

(1) and (2) are cheap and should be standing checks. (3) is the real test.

## 7. On test-set economics

The lead's guidance: do not be precious about burning test sets; use common
sense; if procuring one is cheap, make a new one every time.

The cost is asymmetric and worth stating plainly:

- **Sampling a fresh set of proofs: seconds.** Free. Should be done every time.
- **Grading it: expensive.** The 552-proof round cost 69 agent tasks and about
  4 hours of wall-clock.

So the rule that follows: **re-sample freely, re-grade rarely.** Any check
answerable from structure alone — append-safety, hub composition, distance
distortion, delta-depth distributions, gradient shape — should run on a fresh
random sample every single time, because it costs nothing and removes any doubt
about tuning to a fixed set. Only checks needing human-equivalent judgement
should reuse the graded corpus, and those should be spent deliberately.

This also means the "TEST-R is burned" caution I have been repeating is
overstated for structural questions and correct only for graded ones.

## 8. What I would test next

1. **delta_depth as an edge admission rule**, as a within-proof rank so it
   carries no constant. Measure hub composition, distance distortion and
   shortcut recall — not per-proof precision, which it is not designed to
   improve.
2. **Tier coarsening** (5 tiers to 3): recovers P@1 0.836 → 0.972 with zero
   constants and no escape hatch. Cheapest compliant win available.
3. **Independent validation** via module co-location and held-out citation
   prediction, to escape the circularity in every number reported so far.
4. **Whether the local and global rules can differ.** Nothing requires the
   ranking that orders a proof's citations to be the same rule that decides
   which edges enter the map. Ranking is ours; inclusion is the user's. Two
   mechanisms may be correct.

## 9. The claim I am least sure of

That `delta_depth` is a sufficient proxy for universality. It is a statement
about the down-set, and universality is really about the up-set (how many
things route through here), which is a count and therefore not append-safe.
They correlate 0.57 within a proof — good, not conclusive.

If depth turns out to be an inadequate proxy, the honest options are to accept
a pinned count table for the global question only, or to accept that the map
cannot be fully append-safe and say exactly where it is not. I would rather
name that now than discover it after building on it.
