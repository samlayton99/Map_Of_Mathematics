# ACCOUNTING STATUS — every flagged case, marked (2026-08-20)

Latest certified run (seed 20260828): 2,400 theorems -> 60 too small,
506 verdicts, 1,834 scored. Rank-1 pass 94.84% -> 95 flagged. Markers:

| at #1 | n | marker | cause | fix status |
|---|---|---|---|---|
| machine-generated, several claims inside | 44 | OK-mislabel (mostly; ledger-read) | multi-parent derivations; step 3 cannot pick one | display label floated, NOT implemented (cosmetic) |
| grader-stamped glue | 27 | 2/3 OK-mislabel (interface facts, byContradiction), 1/3 OK-by-owner-ruling (thin lists) | grader stamps structure fields / logic ops | none needed (grader work ruled out) |
| automation internals | 20 | NOT OK (true junk, ~1.1%) | tactic certificates are genuine claims | SIX detector designs now falsified under test (raw exposure; root-grain; registries; co-mention islands; weighted islands; author-written analysis at file AND declaration grain — the last identifies automation-discharged proofs as a 9% class but cannot separate certificate junk from benign simp-closure). Correct instrument identified: per-proof recorded tactic invocations from the provenance channel (level-3 behavioral fact, not a namespace rule); requires a full provenance sweep (~1-3h elaboration); scheduled as its own registered round |
| Prop-typed instances | 2 | OK-mislabel (read: real facts) | grader | none needed |
| own compiled helpers | 2 | OK (zoom opens) | kept by design | implemented |

Verdicts (506; 80 sampled, audited THREE ways):
- v1 (source text): 39/39 resolvable verified correct (30 literal rfl).
- v2 (exact-module + provenance channel via `mathrecord modules`): 28
  confirmed; 2 flags read as statement-side artifacts (proofs := rfl).
- v3 (KERNEL CERTIFICATION, new `mathrecord defcheck`): for each verdict
  theorem, Lean itself checks whether the statement's sides are
  definitionally equal. 58/80 POSITIVELY KERNEL-CERTIFIED. Union with v1:
  64/80 certified by at least one hard channel; of the 16 remaining, 10 are
  machine-generated congruence/injectivity lemmas (correct by construction:
  congruence is logic, not defeq), 6 named individually (Iff-statements
  provable by logic; no evidence of error; likely reducibility barriers).
  ZERO false verdicts found by any channel.

Below rank 1: 97% of visible glue sits below the real moves (OK by owner
ruling). Plumbing-boundary display cut: floated, NOT implemented, cosmetic.

Recall: filters lose zero human citations; ~14% erased by compilation before
extraction; provenance sidecar implemented, not yet merged into views.

Implemented and certified: position filter; claims filter; attribution;
verdict semantics; logic-only demotion; statement-world priority; depth
ranking; zoom; provenance sidecar; exact-module resolver + verdict audit v2.
Floated, NOT implemented (all non-blocking): tactic-island measure (~1.1%);
multi-parent display label; plumbing display cut; cross-version run;
larger/human keyness panel.

Remaining goal posts, in order: (1) ~1.1% automation junk — only NOT-OK
marker; instrument identified (recorded per-proof tactic invocations),
sweep scheduled; (2) CLOSED this round: verdicts now kernel-certified
(58/80 defeq; 64/80 union; 10 congruence-by-construction; 6 named, no
evidence of error); (3) cross-version run; (4) keyness at scale.
