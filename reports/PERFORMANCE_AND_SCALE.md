# MathRecord Performance Pass + Scalability Note (2026-08-19)

Scope: the Lean extractor (`mathrecord/`) and the Python analysis layer (`studies/phase3_structural_separability/src/`). Research-prototype priorities respected: correctness and debuggability first; only measured, low-risk changes implemented. Core design preserved: Lean objects are the source of truth, P0 exact, derived graphs derived; round-trip/kernel validation re-verified after every change.

## Measured baselines (before any change)

| path | cost | frequency |
|---|---|---|
| per-file `extract` (GCD/Basic, Log/Basic) | 2.9s / 5.7s | per corpus file |
| full-library `depdump` (771,129 constants) | 96s (deps+hb); ~5 min with root chains | rare (Mathlib version change) |
| Python analysis load (parse 900MB JSONL + topo + depth) | 14s (7s + 7s) | every script run |
| batched statement-cone propagation | ~2 min per 600-root batch | the actual analysis hot loop |

Correction recorded: the JSONL parse was assumed to cost minutes; measured at 7s (page-cached). The scripts' long runtimes are dominated by cone propagation, not loading.

## Implemented now (all measured, all byte-verified)

**1. `stripMData` made sharing-preserving** (`Record.lean`). Was: unconditional tree rebuild — destroyed DAG sharing before every encode, a latent exponential blowup on heavily-shared proof terms. Now: per-call pointer-keyed memo, identity-preserving (returns the original object when nothing changed), so terms stay DAGs and the validator's structural compares stay pointer-fast.

**2. `encodeExpr` pointer-memoized per scope** (`Record.lean`). Shared subterms are traversed and interned once per scope instead of once per occurrence. Caches are cleared at every declaration/state boundary (`resetEncScope`).

**3. `sidOf` memoized** on subterms free of fvars/mvars/level-params, keyed by structural equality — which is *semantically exact* for sids, since Lean's `Expr ==` ignores binder display names and sids exclude them by design.

Result: Log/Basic extract **5.7s → 3.0s (−47%)**; GCD unchanged (startup-dominated); **outputs byte-identical** to pre-change records on both benchmark files; kernel round-trip validation passes (decode-equals-original, kernel recheck, deps recomputable, state sid fixpoint — all green).

Two encoder war stories, recorded because they gate all future encoder work:
- Lean's `Expr ==` and `hash` **ignore binder display names**. A structural-keyed encode memo silently collapsed display-name variants (3 nodes in the GCD record) — caught only by byte-comparison. Structural keys are correct for sids, wrong for storage.
- Pointer-keyed memos have an address-reuse hazard: a freed expression's address can be reallocated within the same scope, producing false hits (caught, again, by byte-comparison on Log/Basic). Sound pattern: the memo stores the keyed `Expr` itself, pinning the address for the cache's lifetime. **Any future encoder change must be gated on byte-identical re-extraction of at least two corpus files.**

**4. Binary analysis cache** (`src/mmcache.py`). One parse of the 900MB JSONL produces a 299MB `.npz` with names, kinds, classification bitmasks, all four edge relations in CSR form, and the standard derived projections (topo order, depth, in-degrees) precomputed. Load: **14s → 0.1s**, verified against canonical results (24/24 depth anchors exact). The JSONL remains the source of truth; the cache is disposable and derived. Existing scripts are untouched (their recorded results stay reproducible); new scripts should use `mmcache.load`.

Python test suite: 9/9 passing after all changes.

## Classification of the audit list

| optimization | verdict | reason |
|---|---|---|
| memoize visited exprs (encode/sid/strip) | **DO NOW — done** | −47% on analysis-heavy file; kills latent exponential; byte-verified |
| binary analysis cache (`mmcache`) | **DO NOW — done** | 140× load; one canonical loader replaces six copies of boilerplate |
| integer IDs instead of `"x123"` in records | **NOT WORTH IT** | ids are interned/deduped; records are MBs; analysis side already integer-based via the cache; churn > gain |
| reduce JSON/string work in `depdump` rows | **DEFER** | dump runs rarely (~5 min); manual JSON escaping is a correctness risk (unicode names) for a rare-run win |
| cache derived projections | **DO NOW — done** | topo/depth/indeg ship inside the cache |
| vectorize cone/bitmask propagation | **DEFER** | the true analysis hot loop (~2 min/batch); acceptable today; scipy-sparse or numba sketch exists when it blocks iteration |
| compact typed/binary storage for P0 records | **DEFER** | per-file records are small; becomes relevant at full-library P0 |
| Merkle/content hashes instead of full-string SIDs | **DEFER — but the one flagged design item** | see below |
| global cross-file expression interning | **DEFER** | natural companion of content addressing; needed only for full-library P0 |
| incremental extraction | **DEFER** | falls out of content addressing; corpus re-extraction is currently minutes |
| file-level parallel extraction | **DEFER** | already embarrassingly parallel (one process per file, ADR-0001); a 10-line orchestrator when the corpus grows |
| dependency/occurrence indexes (SQLite/LMDB) | **DEFER** | needed when queries become interactive (map UI backend), not for batch research |
| task-specific graph/ML representations | **DEFER** | derived-layer additions; nothing in the record blocks them |

## The fundamental question

**The representation is fundamentally suitable for long-term scale; what will need work is storage and one identity protocol — not the design.** The layering (exact kernel objects → P0 → derived projections, everything derived recomputable) is the layering that scales: extraction is linear and file-parallel (771k constants dep-dumped in minutes single-threaded; per-file P0 in seconds), every analysis so far is one or two linear passes over a graph that fits in a 16GB laptop with headroom, and the semantic design never forces whole-corpus state into one process.

One element will not survive full-library P0 as-is: **`sid` as the full canonical string for proof VALUES.** A sid is tree-sized — it deliberately defeats the DAG sharing everything else preserves — and the cone study measured the unfolded-tree/DAG gap at ~10^8. For statements and corpus-file records this is fine (and is why nothing has hurt yet); for full-library value sids it is not. The fix is the planned one: content hashes (Merkle over the canonical node encoding) as the working identity, with the exact-string definition retained as the *specification* that hashes commit to. That is an identity-protocol ADR and a storage change — the record's semantics, layering, and validation story are unchanged by it. Nothing else in the design points toward a forced redesign; the second-largest pressure (state volume, if tactic states are ever extracted at Mathlib scale) is a data-volume concern already mitigated by state dedup, not a structural one.
