# Next Recommendation (2026-08-27, semantic-conformance cycle)

**The 80 benchmark is now DEV80 - a development/conformance set, not a clean test set.** Gate C/E numbers (67/80, 65/80) are oracle results (reference-derived actions inside budgeted search); make no generalization claims from them. Data splits are in `bigdata/splits.json` (`tools/splits.py`): TRAIN / DEV-LARGE (DEV80 ⊂, module-granular) / SEALED-MODULE (388 modules sharing none with DEV80; never used to modify IR or executor).

The immediate gate is **semantic conformance, not solve rate**:

1. **Deterministic semantic replay** (`mathrecord semreplay`, `Mathrecord/SemIR.lean`): extraction records IR v1 actions (family + parameters, orientation/mode/order determined by bounded trial); replay executes the record with no search, no budget, no ranker, no reference access; kernel verification arbitrates. Every failure carries a named mechanism (`tools/semreplay_analysis.py`); "dead end/budget" is impossible by construction. Current DEV80: extract 65/80, replay 64/80, verified 64/80, zero fallback.
2. **Drive DEV80 toward 80/80 with general mechanisms only** - a new IR field/mechanism requires the same failure class in multiple theorems (check at 300/3k scale first). Unrepresentable actions stay UNSUPPORTED, never raw-node fallback.
3. **Scale conformance measurement**: 300 (running), 3k (`bigdata/dev3k_tasks.json`, DEV-LARGE only). Report per-action and per-theorem success, family distribution, failures by mechanism, compression ratio, horizon, fallback %.
4. **Freeze semantic IR v1** once DEV80 ~80/80 and 3k coverage is high; after freeze, SEALED-MODULE failures must not motivate IR changes while the set keeps that name.
5. Only then: semantic-grain decision dataset (family + parameter labels, source-accessible env only, no certificate-grain congrArg/Eq.mpr decisions), supervised hierarchical policy P(family|state)*P(params|family,state), then autonomous search on SEALED-MODULE.

Do not start value learning / MCTS / expert iteration / RL before all of the above.
