# ACCOUNTING STATUS — every flagged case, marked (2026-08-20)

Latest certified run (seed 20260828): 2,400 theorems -> 60 too small,
506 verdicts, 1,834 scored. Rank-1 pass 94.84% -> 95 flagged. Markers:

| at #1 | n | marker | cause | fix status |
|---|---|---|---|---|
| machine-generated, several claims inside | 44 | OK-mislabel (mostly; ledger-read) | multi-parent derivations; step 3 cannot pick one | display label floated, NOT implemented (cosmetic) |
| grader-stamped glue | 27 | 2/3 OK-mislabel (interface facts, byContradiction), 1/3 OK-by-owner-ruling (thin lists) | grader stamps structure fields / logic ops | none needed (grader work ruled out) |
| automation internals | 20 | NOT OK (true junk, ~1.1%) | tactic certificates are genuine claims | island measure NOT implemented (two prior formulations falsified; needs design, not rush) |
| Prop-typed instances | 2 | OK-mislabel (read: real facts) | grader | none needed |
| own compiled helpers | 2 | OK (zoom opens) | kept by design | implemented |

Verdicts (506; 80 sampled, audited TWICE):
- v1 (source text): 39/39 resolvable verified correct (30 literal rfl).
- v2 (exact-module + provenance channel; IMPLEMENTED this round via new
  `mathrecord modules` command -- no name-based file search): 28 confirmed
  correct; 2 flagged then read -- both statement-side citations with := rfl
  proofs, i.e. audit artifacts, verdicts correct; 14 are machine-generated
  lemmas (auto-ext family, trivially fine); 36 human theorems show zero
  written identifiers (consistent with definitional proofs; not positively
  certifiable by this tool). ZERO false verdicts found in any channel.

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

Remaining goal posts, in order: (1) ~1.1% automation junk (only NOT-OK
marker); (2) positive certification of the 36 identifier-free verdicts
(audit gap, no known error); (3) cross-version run; (4) keyness at scale.
