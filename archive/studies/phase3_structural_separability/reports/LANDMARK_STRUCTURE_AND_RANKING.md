# Phase 3 — Question B: Landmark Structure and Ranking

Sample: 24 stratified proofs (fixed seed, chosen before model outputs; `data/landmark_sample_manifest.json`), 845 candidate occurrences. Rankings and per-proof features: `data/rankings.json`. Review: two independent reasoning-agent passes over blinded, per-proof-shuffled packets (`review/agent_packet/`, provenance in the response files) + a 12-proof user packet awaiting the user. Proxy metrics are labeled and circular (they derive from P4/P5); the review is the evidence.

## Reviewed results (24 proofs × 8 anonymized views × 2 reviewers; agreement ρ = 0.966 on 192 shared ratings)

| method | usefulness A/B | fidelity A/B | best-view votes (48) |
|---|---|---|---|
| **M_hybrid** (P4-route ∪ P5 first, then salience−machinery) | **4.04 / 4.17** | **4.17 / 4.17** | **19** |
| M_p4_route | 3.88 / 3.96 | 3.96 / 3.96 | 11 |
| M_global_pagerank | 3.29 / 3.38 | 3.42 / 3.33 | 9 |
| M_p3_filter | 3.17 / 3.33 | 3.25 / 3.33 | 0 |
| M_combined (salience − λ·machineryProb) | 2.71 / 2.75 | 2.79 / 2.75 | 0 |
| M_local_salience | 2.38 / 2.50 | 2.46 / 2.50 | 3 |
| M_p2_order | 2.21 / 2.38 | 2.29 / 2.38 | 2 |
| M_multiplicity | 2.12 / 2.12 | 2.21 / 2.12 | 4 |

8 of 24 proofs were degenerate (single-candidate one-lemma proofs; all views identical, rated equally) — they compress the spread; the ordering above is driven by the 16 discriminating proofs.

## Findings

**B2 answer — soft downweighting alone does not beat structured evidence.** The pre-registered success condition ("machinery probability + local salience outperforms raw support, P3 filtering, global centrality, and P4-route") **fails**: M_combined (2.7) sits below global PageRank (3.3), P3 filtering (3.2), and P4-route (3.9). The hybrid wins, but its lead over P4-route (+0.2, 19 vs 11 votes) comes chiefly from putting exact route/event members first; the topology components act as a useful tie-breaker, not the signal.

**B3 — structural signatures.** On proxy labels, combined beats salience alone (nDCG 0.58 vs 0.44) — the machinery prior does help *within* topology-only ranking — and global centrality is the best single topology signal (0.66). In-statement occurrence, shallow application depth, and P5 attribution are the strongest local features; multiplicity is the weakest ranker reviewed (2.1) and also degraded Question A — multiplicity ≠ importance is now double-evidenced.

**Distinguishing global role from local salience (B1) is confirmed as necessary but insufficient**: both reviewers independently flagged the same blind-spot classes that *no declaration ranking can express* — local hypotheses and witnesses, `simpa`/`suffices` transports, case-split structure, and representation-change steps (e.g. `isOpen_compl_iff`). Declaration-level views hit a ceiling around 4/5 for structural reasons, not tuning reasons.

## Limitations

- Both reviewers are Claude-based reasoning agents (independent contexts, blinded packets, no shared outputs) — high agreement partly reflects shared model priors. The 12-proof user packet (`review/user_packet/`) is prepared for a human pass; provenance fields distinguish reviewer types throughout.
- Packet defects found by reviewers (kept, documented): 2–3 proofs with truncated Part 2 source (span starts at an attribute line), and one worst case where every view shows only compilation artifacts — see DISAGREEMENT_AUDIT.md.
- Proxy metrics in `rankings.json` favor P4/P5-based methods by construction and were used descriptively only.
