# Rater Protocol — semantic keyness vibes check

You are one of three independent raters. You will not see any ranking our
system produces, and you should not try to guess one. Your judgements are the
ground truth those rankings get scored against.

## The task

For each of 25 proofs you get:

- the **theorem being proved**;
- the **citations its proof actually uses**, in random order, each labelled
  with its declaration kind, its depth, and whether it already appears in the
  theorem's statement or is introduced by the proof.

For each proof, answer one question:

> **Which of these citations are the KEY MOVES of this proof?**

A key move is something whose removal would make the proof's central idea
unintelligible — the mathematical step a person would name if asked "how does
this proof go?"

Pick **1 to 3** numbers. Prefer fewer. If two citations are equally central,
list both.

## Important instructions

**Answer `NONE_LISTED` if the real key move is not in the list.** This happens
and it is a genuine result, not a failure to do the task. Some proofs work by
manipulating local hypotheses, exhibiting a witness, splitting into cases, or
rewriting — none of which appear as a cited declaration. If you look at the
list and the actual mathematical content of the proof is simply not there,
say `NONE_LISTED`. Do not force a pick.

**Glue can be the key move.** Near the foundations of the library, a proof
about booleans or equality may genuinely have logical assembly as its entire
content. If `Eq.trans` really is what the proof does, pick it. Do not
downgrade something merely because it looks like plumbing — judge it in the
context of *this* theorem.

**Depth is context, not a hint.** The depth number tells you roughly how much
mathematics sits underneath a declaration. It is there to help you understand
what you are looking at. It is not a ranking signal and you should not prefer
deep things because they are deep.

**"in-statement" versus "introduced-by-proof"** tells you whether a citation
was already implied by what the theorem says, or whether the proof brought it
in. Both can be key moves.

Work quickly. This is a vibes check — roughly 25 seconds per proof, about ten
minutes total. Your first considered judgement is what we want.

## Output format

Return **only** a JSON object, no commentary:

```json
{
  "proof_01": {"picks": [3, 7], "confidence": "high"},
  "proof_02": {"picks": "NONE_LISTED", "confidence": "medium"},
  "proof_03": {"picks": [12], "confidence": "low"}
}
```

`confidence` is one of `high`, `medium`, `low` — your own sense of whether you
understood the proof well enough to judge. Low-confidence answers are still
useful; they are weighted separately.

Every one of the 25 proof ids must appear exactly once.
