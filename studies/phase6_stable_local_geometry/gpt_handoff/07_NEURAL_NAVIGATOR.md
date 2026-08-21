# 07 — Implications for a Neural Navigator

The user’s stability requirement is especially important if a neural model will navigate the graph.

## 1. Two-channel representation

### Stable local encoder

Input:

- exact local move hierarchy;
- occurrence roles;
- substitutions/types;
- depth/span;
- declaration type features;
- relation lane;
- generated-owner structure.

For unchanged proofs, these inputs remain stable across library extension.

### Dynamic global encoder

Input at time \(t\):

- current usage;
- rarity;
- communities;
- centrality;
- branch activity;
- semantic embeddings;
- successful-use history.

These may evolve.

### Policy

\[
\pi_t(e\mid s)
=
F_\theta
\left(
h_{\mathrm{local}}(e,p),
h_{\mathrm{global},t}(e),
s
\right).
\]

The model can adapt to global growth without rewriting the local graph.

## 2. Temporal consistency objective

For an unchanged proof/occurrence across versions:

\[
h_{\mathrm{local},t}(e)
\approx
h_{\mathrm{local},t+1}(e).
\]

Do not require global embeddings to remain fixed.

Evaluate:

- local embedding drift;
- policy drift on unchanged local tasks;
- transfer to newly added proofs;
- robustness to new unrelated modules.

## 3. Dynamic rarity as teacher

The powerful live-rarity composite can remain useful as:

- a teacher signal;
- an upper-bound comparator;
- a current-version global prior.

Distill its useful behavior into a student using stable local features.

Then test whether the student transfers across versions better than the teacher.

## 4. Do not bake one UI score into training data as truth

Train on:

- graded usefulness;
- actual successful use events;
- navigation tasks;
- refactoring invariance;
- alternative proof structure.

The graph supplies stable actions and relations. The learned policy supplies context-dependent choice.

## 5. Self-similarity objective

Test whether normalized local representations yield comparable policy calibration across:

- target depth;
- proof size;
- mathematical domain;
- time.

If not, use explicit hierarchical or mixture-of-regime models rather than forcing one stationary distribution.
